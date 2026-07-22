"""阶段一：把问题拆成可独立获取事实的分析任务。"""

from pathlib import Path
from typing import Any, cast

from agently import Agently, TriggerFlowRuntimeData

from trace_log import TraceLog
from utils.metrics import load_metric_catalog


PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts/plan_analysis.yaml"


async def plan_analysis(data: TriggerFlowRuntimeData) -> list[dict[str, Any]]:
    payload = cast(dict[str, Any], data.input)
    question = str(payload["question"])
    metrics_path = cast(Path, data.require_resource("metrics_path"))
    trace = cast(TraceLog, data.require_resource("trace"))

    result = await (
        Agently.create_agent(name="template-plan-analysis")
        .use_task_workspace(PROMPT_PATH.parent)
        .load_yaml_prompt(
            PROMPT_PATH,
            mappings={
                "question": question,
                "metric_catalog": load_metric_catalog(metrics_path),
            },
        )
        .create_execution()
        .async_start()
    )
    plan = dict(result)
    tasks = list(plan.get("analysis_tasks", []))
    identifiers = [str(item.get("analysis_id", "")) for item in tasks]
    if not plan.get("normalized_question") or not tasks:
        raise ValueError("analysis plan is incomplete")
    if any(not identifier for identifier in identifiers):
        raise ValueError("analysis_id must not be empty")
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("analysis_id must be unique")

    trace.log(
        layer="business",
        event_type="business.analysis.planned",
        status="completed",
        subject_id=trace.task_id,
        input={"question": question},
        output=plan,
        facts={"task_count": len(tasks)},
    )
    await data.async_set_state("question", question, emit=False)
    await data.async_set_state("analysis_plan", plan, emit=False)
    await data.async_set_state("metric_facts", [], emit=False)
    return tasks


__all__ = ["plan_analysis"]
