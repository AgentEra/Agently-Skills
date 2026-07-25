from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
from agently import StreamingData


EXAMPLE = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "agently-triggerflow"
    / "examples"
    / "instant_retrieval_overlap.py"
)


def load_example():
    spec = importlib.util.spec_from_file_location("instant_retrieval_overlap", EXAMPLE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeResult:
    async def get_async_generator(self, *, type):
        assert type == "instant"
        provisional = {
            "query": "provisional query",
            "purpose": "candidate evidence",
        }
        yield StreamingData(
            path="retrieval_tasks[0]",
            value=provisional,
            is_complete=True,
        )
        yield StreamingData(
            path="retrieval_tasks[0]",
            value=provisional,
            is_complete=True,
        )
        yield StreamingData(
            path="progress_message",
            value="Planning",
            delta="Planning",
        )

    async def async_get_data(self, *, max_retries):
        assert max_retries == 1
        return {
            "retrieval_tasks": [
                {
                    "query": "accepted query",
                    "purpose": "final evidence",
                }
            ],
            "progress_message": "Planning",
            "answer_plan": ["Use the accepted evidence"],
        }


class FakeAgent:
    def input(self, _value):
        return self

    def instruct(self, _value):
        return self

    def output(self, _schema, *, format):
        assert format == "json"
        return self

    def validate(self, _handler):
        return self

    def get_result(self):
        return FakeResult()


@pytest.mark.asyncio
async def test_provisional_retrieval_is_deduplicated_and_final_set_wins():
    example = load_example()
    example.agent = FakeAgent()

    execution = example.flow.create_execution(auto_close=False, concurrency=4)
    await execution.async_start("question")
    state = await execution.async_close()

    assert state["final_result"]["plan"]["retrieval_tasks"] == [
        {
            "query": "accepted query",
            "purpose": "final evidence",
        }
    ]
    assert state["final_result"]["retrievals"] == [
        {
            "query": "accepted query",
            "hits": [{"title": "Demo result"}],
        }
    ]
    provisional = {
        "query": "provisional query",
        "purpose": "candidate evidence",
    }
    assert (
        execution.result.get_state(f"retrieval:{example.task_key(provisional)}")
        is None
    )
