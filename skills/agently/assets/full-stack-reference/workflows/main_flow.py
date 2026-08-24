"""项目的稳定拓扑与一次 execution 生命周期。"""

from pathlib import Path
from typing import Any, cast

from agently import TriggerFlow

from trace_log import (
    TraceLog,
    register_framework_hook,
    save_run,
    unregister_framework_hook,
)
from utils.metrics import load_snapshot_id
from workflows.chunks.compose_answer import compose_answer
from workflows.chunks.load_metric_facts import load_metric_facts
from workflows.chunks.plan_analysis import plan_analysis


ANALYSIS_FLOW = TriggerFlow(name="reference-business-analysis")
(
    ANALYSIS_FLOW.to(plan_analysis)
    .for_each(concurrency=4)
    .to(load_metric_facts)
    .end_for_each()
    .to(compose_answer)
)


async def run_analysis(
    question: str,
    *,
    task_id: str,
    metrics_path: Path,
    output_directory: Path,
    max_concurrency: int = 4,
) -> dict[str, Any]:
    if not question.strip():
        raise ValueError("question must not be empty")
    if max_concurrency < 1:
        raise ValueError("max_concurrency must be positive")

    execution = ANALYSIS_FLOW.create_execution(
        concurrency=max_concurrency,
        runtime_resources={"metrics_path": metrics_path},
        auto_close=False,
    )
    trace = TraceLog(task_id, execution.id)
    execution.update_runtime_resources({"trace": trace})
    hook_name = register_framework_hook(trace)
    try:
        await execution.async_start({"question": question})
        state = await execution.async_close()
    finally:
        unregister_framework_hook(hook_name)

    run = {
        "task_id": task_id,
        "execution_id": execution.id,
        "status": "completed",
        "question": question,
        "snapshot_id": load_snapshot_id(metrics_path),
        "analysis_plan": cast(dict[str, Any], state["analysis_plan"]),
        "metric_facts": cast(list[dict[str, Any]], state["metric_facts"]),
        "final_answer": cast(dict[str, Any], state["final_answer"]),
        "events": trace.events,
    }
    save_run(run, output_directory)
    return run


__all__ = ["ANALYSIS_FLOW", "run_analysis"]
