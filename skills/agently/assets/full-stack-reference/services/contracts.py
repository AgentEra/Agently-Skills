"""Public request and response shapes shared by inbound transports."""

from collections.abc import Mapping
from typing import Any, Literal

from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    question: str = Field(min_length=1)
    max_concurrency: int = Field(default=4, ge=1, le=4)


class AnalysisResponse(BaseModel):
    task_id: str
    execution_id: str
    status: Literal["completed"]
    answer: str
    evidence_ids: list[str]


def project_analysis_run(
    task_id: str,
    run: Mapping[str, Any],
) -> AnalysisResponse:
    """Expose approved result fields without leaking trace or internal metadata."""

    if str(run.get("task_id", "")) != task_id:
        raise ValueError("run task_id does not match the host-issued task_id")
    if run.get("status") != "completed":
        raise ValueError("only completed runs can cross the public boundary")

    final_answer = run.get("final_answer")
    if not isinstance(final_answer, Mapping):
        raise TypeError("final_answer must be a mapping")
    answer = final_answer.get("answer")
    evidence_ids = final_answer.get("evidence_ids")
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("final answer must not be empty")
    if not isinstance(evidence_ids, list):
        raise TypeError("final evidence_ids must be a list")

    return AnalysisResponse(
        task_id=task_id,
        execution_id=str(run["execution_id"]),
        status="completed",
        answer=answer,
        evidence_ids=[str(item) for item in evidence_ids],
    )


__all__ = ["AnalysisRequest", "AnalysisResponse", "project_analysis_run"]
