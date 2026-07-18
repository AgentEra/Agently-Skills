"""FastAPI delivery adapter for the analysis application."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

from agently import Agently
from fastapi import FastAPI

from services.contracts import AnalysisRequest, AnalysisResponse, project_analysis_run
from workflows.main_flow import run_analysis


ROOT = Path(__file__).resolve().parents[1]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Agently.load_settings(
        "yaml_file",
        str(ROOT / "SETTINGS.yaml"),
        auto_load_env=True,
    )
    yield


app = FastAPI(title="Agently Analysis Service", lifespan=lifespan)


@app.post("/analysis", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    task_id = f"analysis-{uuid4().hex}"
    run = await run_analysis(
        request.question,
        task_id=task_id,
        metrics_path=ROOT / "resources/metrics.json",
        output_directory=ROOT / "outputs" / task_id,
        max_concurrency=request.max_concurrency,
    )
    return project_analysis_run(task_id, run)


__all__ = ["app", "analyze", "lifespan"]
