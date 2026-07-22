"""统一记录业务事实，并从 EventCenter 订阅少量框架事实。"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Literal

from agently import Agently, RuntimeEvent


TraceLayer = Literal["business", "framework"]
TraceStatus = Literal["started", "completed", "failed", "observed"]

FRAMEWORK_EVENT_TYPES = frozenset(
    {
        "triggerflow.execution_started",
        "triggerflow.execution_completed",
        "triggerflow.execution_failed",
        "chunk.started",
        "chunk.completed",
        "chunk.failed",
        "model.request_started",
        "model.completed",
        "model.request_failed",
        "model.meta",
    }
)

_TRACE_LAYERS = {"business", "framework"}
_TRACE_STATUSES = {"started", "completed", "failed", "observed"}
_MODEL_FACT_KEYS = (
    "response_id",
    "attempt_index",
    "provider",
    "provider_family",
    "model",
    "duration_ms",
    "usage_summary",
)


def bounded(value: Any, *, depth: int = 0) -> Any:
    """把事实限制为适合写入 JSON 的小对象。"""

    if depth >= 6:
        return "<max-depth>"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {
            str(key): bounded(item, depth=depth + 1)
            for key, item in list(value.items())[:50]
        }
    if isinstance(value, (list, tuple)):
        return [bounded(item, depth=depth + 1) for item in value[:50]]
    if isinstance(value, str):
        return value if len(value) <= 2_000 else value[:2_000] + "…"
    if value is None or isinstance(value, (bool, int, float)):
        return value
    model_dump = getattr(value, "model_dump", None)
    if callable(model_dump):
        return bounded(model_dump(mode="json"), depth=depth + 1)
    return str(value)


def value_shape(value: Any) -> dict[str, Any]:
    """框架层只保留输入输出形状，业务值由业务事件负责。"""

    if isinstance(value, Mapping):
        keys = sorted(str(key) for key in value)
        return {"type": "object", "keys": keys[:20], "size": len(keys)}
    if isinstance(value, (list, tuple)):
        return {"type": "array", "size": len(value)}
    if isinstance(value, str):
        return {"type": "string", "length": len(value)}
    if value is None:
        return {"type": "null"}
    return {"type": type(value).__name__}


def error_payload(error: Any) -> dict[str, Any] | None:
    if error is None:
        return None
    if isinstance(error, Mapping):
        return bounded(error)
    return {"type": type(error).__name__, "message": str(error)}


class TraceLog:
    """一次 execution 的有序事实列表。"""

    def __init__(self, task_id: str, execution_id: str) -> None:
        if not task_id.strip() or not execution_id.strip():
            raise ValueError("task_id and execution_id must not be empty")
        self.task_id = task_id
        self.execution_id = execution_id
        self.events: list[dict[str, Any]] = []
        self._root_run_id: str | None = None

    def log(
        self,
        *,
        layer: TraceLayer,
        event_type: str,
        status: TraceStatus,
        subject_id: str | None = None,
        input: Any = None,
        output: Any = None,
        facts: Mapping[str, Any] | None = None,
        error: Any = None,
        runtime: Mapping[str, Any] | None = None,
        timestamp: str | None = None,
    ) -> dict[str, Any]:
        if layer not in _TRACE_LAYERS:
            raise ValueError(f"unsupported trace layer: {layer}")
        if status not in _TRACE_STATUSES:
            raise ValueError(f"unsupported trace status: {status}")
        if not event_type.strip():
            raise ValueError("event_type must not be empty")

        event = {
            "event_id": f"{self.task_id}:event:{len(self.events) + 1:04d}",
            "task_id": self.task_id,
            "execution_id": self.execution_id,
            "layer": layer,
            "event_type": event_type,
            "status": status,
            "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
            "subject_id": subject_id,
            "input": bounded(input) if input is not None else None,
            "output": bounded(output) if output is not None else None,
            "facts": bounded(dict(facts or {})),
            "error": error_payload(error),
            "runtime": bounded(dict(runtime)) if runtime is not None else None,
        }
        self.events.append(event)
        return event


def framework_status(event_type: str) -> TraceStatus:
    if event_type.endswith("_started") or event_type == "chunk.started":
        return "started"
    if event_type.endswith("_completed") or event_type in {
        "chunk.completed",
        "model.completed",
    }:
        return "completed"
    if event_type.endswith("_failed") or event_type in {
        "chunk.failed",
        "model.request_failed",
    }:
        return "failed"
    return "observed"


def record_framework_event(trace: TraceLog, event: RuntimeEvent) -> None:
    run = event.run
    if event.event_type not in FRAMEWORK_EVENT_TYPES or run is None:
        return
    belongs_to_execution = run.execution_id == trace.execution_id
    if event.event_type.startswith("model."):
        belongs_to_execution = belongs_to_execution or (
            trace._root_run_id is not None and run.root_run_id == trace._root_run_id
        )
    if not belongs_to_execution:
        return
    if event.event_type == "triggerflow.execution_started":
        trace._root_run_id = run.root_run_id or run.run_id

    payload = event.payload if isinstance(event.payload, Mapping) else {}
    input_value = value_shape(payload["input"]) if "input" in payload else None
    output_value = value_shape(payload["output"]) if "output" in payload else None
    facts: dict[str, Any] = {}
    if event.event_type.startswith("chunk."):
        for key in ("chunk_id", "chunk_name", "operator_kind", "trigger_event"):
            if payload.get(key) is not None:
                facts[key] = payload[key]
    if event.event_type.startswith("model."):
        telemetry = payload.get("model_request_telemetry")
        source = telemetry if isinstance(telemetry, Mapping) else payload
        facts.update(
            {key: source[key] for key in _MODEL_FACT_KEYS if source.get(key) is not None}
        )

    trace.log(
        layer="framework",
        event_type=event.event_type,
        status=framework_status(event.event_type),
        subject_id=run.run_id,
        input=input_value,
        output=output_value,
        facts=facts,
        error=event.error,
        runtime={
            "event_id": event.event_id,
            "source": event.source,
            "run": run.model_dump(mode="json"),
        },
        timestamp=datetime.fromtimestamp(
            event.timestamp / 1_000, tz=timezone.utc
        ).isoformat(),
    )


def register_framework_hook(trace: TraceLog) -> str:
    hook_name = f"project-template.trace.{trace.execution_id}"

    def capture(event: RuntimeEvent) -> None:
        record_framework_event(trace, event)

    Agently.event_center.register_hook(
        capture,
        event_types=sorted(FRAMEWORK_EVENT_TYPES),
        hook_name=hook_name,
    )
    return hook_name


def unregister_framework_hook(hook_name: str) -> None:
    Agently.event_center.unregister_hook(hook_name)


def save_run(run: dict[str, Any], output_directory: Path) -> None:
    output_directory.mkdir(parents=True, exist_ok=True)
    serializable = bounded(run)
    (output_directory / "run.json").write_text(
        json.dumps(serializable, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    events = [bounded(event) for event in run.get("events", [])]
    (output_directory / "events.jsonl").write_text(
        "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
        encoding="utf-8",
    )


__all__ = [
    "FRAMEWORK_EVENT_TYPES",
    "TraceLog",
    "register_framework_hook",
    "save_run",
    "unregister_framework_hook",
]
