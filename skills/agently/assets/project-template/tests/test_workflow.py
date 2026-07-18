from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest


TEMPLATE_ROOT = Path(__file__).resolve().parents[1]


class FakeAgent:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload

    def use_task_workspace(self, root: Path) -> "FakeAgent":
        return self

    def load_yaml_prompt(
        self, path: Path, *, mappings: dict[str, Any]
    ) -> "FakeAgent":
        return self

    def create_execution(self) -> "FakeAgent":
        return self

    async def async_start(self) -> dict[str, Any]:
        return self.payload


@pytest.mark.asyncio
async def test_flow_runs_visible_chunks_and_returns_plain_business_data(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    from workflows.chunks import compose_answer, plan_analysis
    from workflows.main_flow import ANALYSIS_FLOW, run_analysis

    monkeypatch.setattr(
        plan_analysis,
        "Agently",
        SimpleNamespace(
            create_agent=lambda **_: FakeAgent(
                {
                    "normalized_question": "比较两年的净营收",
                    "analysis_tasks": [
                        {
                            "analysis_id": "annual-revenue",
                            "metric": "net_revenue",
                            "periods": ["2024", "2025"],
                        }
                    ],
                }
            )
        ),
    )
    monkeypatch.setattr(
        compose_answer,
        "Agently",
        SimpleNamespace(
            create_agent=lambda **_: FakeAgent(
                {
                    "answer": "净营收从 120 增长到 150。",
                    "evidence_ids": ["metric:annual-revenue"],
                }
            )
        ),
    )

    run = await run_analysis(
        "比较 2024 和 2025 年净营收",
        task_id="template-test",
        metrics_path=TEMPLATE_ROOT / "resources/metrics.json",
        output_directory=tmp_path,
    )

    mermaid = ANALYSIS_FLOW.to_mermaid(mode="simplified")
    assert "plan_analysis" in mermaid
    assert "load_metric_facts" in mermaid
    assert "compose_answer" in mermaid
    assert run["status"] == "completed"
    assert run["metric_facts"][0]["evidence_id"] == "metric:annual-revenue"
    assert run["final_answer"]["answer"].startswith("净营收")
    assert (tmp_path / "run.json").is_file()
    assert (tmp_path / "events.jsonl").is_file()
