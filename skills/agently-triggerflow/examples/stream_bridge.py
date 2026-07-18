import asyncio
import os
import re

from agently import Agently, TriggerFlow

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY", "ollama")
USE_LIVE_MODEL = bool(os.getenv("AGENTLY_TRIGGERFLOW_USE_LIVE_MODEL"))
# Default path: local Ollama qwen2.5:7b. Live mode is opt-in and uses explicit AGENTLY_TRIGGERFLOW_LIVE_* env vars.


def configure_model():
    if USE_LIVE_MODEL:
        base_url = os.environ.get("AGENTLY_TRIGGERFLOW_LIVE_BASE_URL")
        model = os.environ.get("AGENTLY_TRIGGERFLOW_LIVE_MODEL")
        api_key = os.environ.get("AGENTLY_TRIGGERFLOW_LIVE_API_KEY")
        if not base_url or not model or not api_key:
            raise RuntimeError(
                "Enable live mode only after setting AGENTLY_TRIGGERFLOW_LIVE_BASE_URL, "
                "AGENTLY_TRIGGERFLOW_LIVE_MODEL, and AGENTLY_TRIGGERFLOW_LIVE_API_KEY."
            )
        Agently.set_settings(
            "OpenAICompatible",
            {
                "base_url": base_url,
                "api_key": api_key,
                "model": model,
                "model_type": "chat",
                "request_options": {"temperature": 0},
            },
        )
        return

    Agently.set_settings(
        "OpenAICompatible",
        {
            "base_url": OLLAMA_BASE_URL,
            "api_key": OLLAMA_API_KEY,
            "model": OLLAMA_MODEL,
            "model_type": "chat",
            "request_options": {"temperature": 0},
        },
    )


configure_model()

flow = TriggerFlow(name="stream-bridge-demo")
# Real instant paths arrive as judge_items[0].name; keep the parser tolerant to older dot-style traces.
PATH_PATTERN = re.compile(r"^judge_items\[(\d+)\]\.(\w+)$")


def item_is_complete(item):
    return isinstance(item, dict) and {"name", "score", "comment"}.issubset(item.keys())


def _extract_item_path(path: str):
    match = PATH_PATTERN.match(path)
    if match:
        return int(match.group(1)), match.group(2)

    parts = path.split(".")
    if len(parts) == 3 and parts[0] == "judge_items" and parts[1].isdigit():
        return int(parts[1]), parts[2]
    return None


@flow.chunk("judge")
async def judge(data):
    agent = Agently.create_agent()
    agent.role(
        "Return JSON only. judge_items must contain exactly two items: item 0 is clarity with score 8 and comment Clear and direct. item 1 is evidence with score 7 and comment Backed by examples.",
        always=True,
    )
    result = (
        agent.input(f"Score this draft and explain strengths: {data.input}")
        .output(
            {
                "judge_items": [
                    {
                        "name": (str, None, True),
                        "score": (int, None, True),
                        "comment": (str, None, True),
                    }
                ]
            }
        )
        .get_result()
    )

    partial = {"judge_items": []}
    emitted = set()

    async for msg in result.get_async_generator(type="instant"):
        path = getattr(msg, "path", None) or getattr(msg, "wildcard_path", None)
        parsed = _extract_item_path(path or "")
        if parsed is None:
            continue
        index, field = parsed
        while len(partial["judge_items"]) <= index:
            partial["judge_items"].append({})
        value = getattr(msg, "value", None)
        if value is None:
            value = getattr(msg, "delta", None)
        partial["judge_items"][index][field] = value
        if index not in emitted and item_is_complete(partial["judge_items"][index]):
            emitted.add(index)
            await data.async_put_into_stream(
                {
                    "stage": "judge_item_ready",
                    "index": index,
                    "item": partial["judge_items"][index],
                }
            )

    final = await result.async_get_data(max_retries=1)
    await data.async_set_state("judge_result", final)
    return final


flow.to(judge)


async def main():
    execution = flow.create_execution(auto_close=False)
    await execution.async_start("demo")
    close_task = asyncio.create_task(execution.async_close())
    items = [item async for item in execution.get_async_runtime_stream(timeout=None)]
    state = await close_task
    assert [item["stage"] for item in items] == ["judge_item_ready", "judge_item_ready"]
    judge_result = execution.result.get_state("judge_result")
    assert judge_result["judge_items"][0]["name"] == "clarity"
    assert judge_result["judge_items"][0]["score"] == 8
    assert judge_result["judge_items"][0]["comment"] == "Clear and direct."
    assert judge_result["judge_items"][1]["name"] == "evidence"
    assert judge_result["judge_items"][1]["score"] == 7
    assert judge_result["judge_items"][1]["comment"] == "Backed by examples."
    print({"items": items, "meta": execution.result.get_meta()})
    return state


asyncio.run(main())
