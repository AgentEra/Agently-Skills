from unittest.mock import AsyncMock, Mock

import httpx
import pytest
from fastmcp import Client


def sample_run(task_id: str) -> dict[str, object]:
    return {
        "task_id": task_id,
        "execution_id": "execution-1",
        "status": "completed",
        "final_answer": {
            "answer": "净营收从 120 增长到 150。",
            "evidence_ids": ["metric:annual-revenue"],
        },
        "events": [{"internal": "not-public"}],
    }


def test_contract_projects_only_public_fields() -> None:
    from services.contracts import AnalysisResponse, project_analysis_run

    response = project_analysis_run("task-1", sample_run("task-1"))

    assert response == AnalysisResponse(
        task_id="task-1",
        execution_id="execution-1",
        status="completed",
        answer="净营收从 120 增长到 150。",
        evidence_ids=["metric:annual-revenue"],
    )
    assert "events" not in response.model_dump()


@pytest.mark.asyncio
async def test_fastapi_analysis_projects_the_application_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from services import api

    run_analysis = AsyncMock(side_effect=lambda _question, **kwargs: sample_run(kwargs["task_id"]))
    monkeypatch.setattr(api, "run_analysis", run_analysis)

    transport = httpx.ASGITransport(app=api.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/analysis",
            json={"question": "比较两年净营收", "max_concurrency": 2},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "completed"
    assert payload["answer"].startswith("净营收")
    assert payload["evidence_ids"] == ["metric:annual-revenue"]
    assert set(payload) == {
        "task_id",
        "execution_id",
        "status",
        "answer",
        "evidence_ids",
    }
    call = run_analysis.await_args
    assert call is not None
    args, kwargs = call
    assert args == ("比较两年净营收",)
    assert kwargs["max_concurrency"] == 2
    assert kwargs["output_directory"].name == payload["task_id"]


@pytest.mark.asyncio
async def test_fastapi_lifespan_loads_settings(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from services import api

    load_settings = Mock()
    monkeypatch.setattr(api.Agently, "load_settings", load_settings)

    async with api.lifespan(api.app):
        pass

    load_settings.assert_called_once_with(
        "yaml_file",
        str(api.ROOT / "SETTINGS.yaml"),
        auto_load_env=True,
    )


@pytest.mark.asyncio
async def test_fastmcp_analysis_projects_the_application_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from services import mcp_server

    run_analysis = AsyncMock(side_effect=lambda _question, **kwargs: sample_run(kwargs["task_id"]))
    load_settings = Mock()
    monkeypatch.setattr(mcp_server, "run_analysis", run_analysis)
    monkeypatch.setattr(mcp_server.Agently, "load_settings", load_settings)

    async with Client(mcp_server.mcp) as client:
        result = await client.call_tool(
            "analyze",
            {"question": "比较两年净营收", "max_concurrency": 3},
        )

    assert result.data["status"] == "completed"
    assert result.data["answer"].startswith("净营收")
    assert result.data["evidence_ids"] == ["metric:annual-revenue"]
    call = run_analysis.await_args
    assert call is not None
    args, kwargs = call
    assert args == ("比较两年净营收",)
    assert kwargs["max_concurrency"] == 3
    assert kwargs["output_directory"].name == result.data["task_id"]
    load_settings.assert_called_once_with(
        "yaml_file",
        str(mcp_server.ROOT / "SETTINGS.yaml"),
        auto_load_env=True,
    )
