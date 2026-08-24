"""阶段三：只依据已回收的结构化证据形成回答。"""

from pathlib import Path
from typing import Any, cast

from agently import Agently, TriggerFlowRuntimeData

from trace_log import TraceLog


PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts/compose_answer.yaml"


async def compose_answer(data: TriggerFlowRuntimeData) -> dict[str, Any]:
    evidence = cast(list[dict[str, Any]], list(data.input))
    trace = cast(TraceLog, data.require_resource("trace"))
    offered_ids = [str(item["evidence_id"]) for item in evidence]

    result = await (
        Agently.create_agent(name="template-compose-answer")
        .use_task_workspace(PROMPT_PATH.parent)
        .load_yaml_prompt(
            PROMPT_PATH,
            mappings={
                "question": str(data.get_state("question")),
                "evidence": evidence,
                "evidence_ids": offered_ids,
            },
        )
        .create_execution()
        .async_start()
    )
    answer = dict(result)
    used_ids = [str(item) for item in answer.get("evidence_ids", [])]
    unknown_ids = sorted(set(used_ids) - set(offered_ids))
    if not answer.get("answer"):
        raise ValueError("answer must not be empty")
    if unknown_ids:
        raise ValueError(f"unknown evidence ids: {', '.join(unknown_ids)}")

    trace.log(
        layer="business",
        event_type="business.answer.composed",
        status="completed",
        subject_id=trace.task_id,
        input={"evidence_ids": offered_ids},
        output=answer,
        facts={"used_evidence_count": len(used_ids)},
    )
    await data.async_set_state("final_answer", answer, emit=False)
    return answer


__all__ = ["compose_answer"]
