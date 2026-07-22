"""FastMCP server adapter for the analysis application."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

from agently import Agently
from fastmcp import FastMCP

from services.contracts import AnalysisRequest, project_analysis_run
from workflows.main_flow import run_analysis


ROOT = Path(__file__).resolve().parents[1]


@asynccontextmanager
async def lifespan(_: FastMCP) -> AsyncIterator[dict[str, object]]:
    Agently.load_settings(
        "yaml_file",
        str(ROOT / "SETTINGS.yaml"),
        auto_load_env=True,
    )
    yield {}


mcp = FastMCP("Agently Analysis Service", lifespan=lifespan)


@mcp.tool
async def analyze(question: str, max_concurrency: int = 4) -> dict[str, object]:
    """Analyze one business question with bounded workflow concurrency."""

    request = AnalysisRequest(
        question=question,
        max_concurrency=max_concurrency,
    )
    task_id = f"analysis-{uuid4().hex}"
    run = await run_analysis(
        request.question,
        task_id=task_id,
        metrics_path=ROOT / "resources/metrics.json",
        output_directory=ROOT / "outputs" / task_id,
        max_concurrency=request.max_concurrency,
    )
    return project_analysis_run(task_id, run).model_dump()


if __name__ == "__main__":
    mcp.run()
