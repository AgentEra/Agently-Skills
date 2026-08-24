import asyncio
import os

from agently import Agently, TriggerFlow

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY", "ollama")

CRITERIA = [
    {"selection_key": "c1", "criterion": "clarity"},
    {"selection_key": "c2", "criterion": "evidence use"},
]
OFFERED_KEYS = {item["selection_key"] for item in CRITERIA}


Agently.set_settings(
    "plugins.ModelRequester.OpenAICompatible",
    {
        "base_url": OLLAMA_BASE_URL,
        "api_key": OLLAMA_API_KEY,
        "model": OLLAMA_MODEL,
        "model_type": "chat",
        "request_options": {"temperature": 0},
    },
)

flow = TriggerFlow(name="judge-stream-bridge")


def validate_judgment(result, _context):
    items = result.get("judge_items", [])
    keys = [item.get("selection_key") for item in items]
    valid = (
        set(keys) == OFFERED_KEYS
        and len(keys) == len(OFFERED_KEYS)
        and all(
            isinstance(item.get("score"), int)
            and 1 <= item["score"] <= 10
            and isinstance(item.get("comment"), str)
            and item["comment"].strip()
            for item in items
        )
    )
    if valid:
        return True
    return {
        "ok": False,
        "reason": (
            "return each offered selection_key exactly once with score 1..10 "
            "and a non-empty evidence-based comment"
        ),
    }


@flow.chunk("judge")
async def judge(data):
    result = (
        Agently.create_agent()
        .input({"draft": data.input, "criteria": CRITERIA})
        .info(
            {
                "judgment_contract": {
                    "selection_keys": sorted(OFFERED_KEYS),
                    "score_range": [1, 10],
                    "one_result_per_key": True,
                }
            }
        )
        .instruct(
            "Judge the draft against every offered criterion. Return only the "
            "host-issued selection_key, an integer score, and a concise comment."
        )
        .output(
            {
                "judge_items": [
                    {
                        "selection_key": (str, "One offered selection key", True),
                        "score": (int, "Integer from 1 to 10", True),
                        "comment": (str, "Evidence-based explanation", "not_null"),
                    }
                ]
            },
            format="json",
        )
        .validate(validate_judgment)
        .get_result()
    )

    provisionally_emitted = set()
    async for item in result.get_async_generator(type="instant"):
        if (
            item.wildcard_path == "judge_items[*]"
            and item.is_complete
            and isinstance(item.value, dict)
        ):
            selection_key = item.value.get("selection_key")
            if selection_key in OFFERED_KEYS and selection_key not in provisionally_emitted:
                provisionally_emitted.add(selection_key)
                await data.async_put_into_stream(
                    {
                        "stage": "judge_item_ready",
                        "selection_key": selection_key,
                        "item": item.value,
                        "provisional": True,
                    }
                )

    final = await result.async_get_data(max_retries=1)
    await data.async_set_state("judge_result", final)
    await data.async_put_into_stream(
        {
            "stage": "judge_completed",
            "items": final["judge_items"],
            "provisional": False,
        }
    )
    return final


flow.to(judge)


async def main():
    execution = flow.create_execution(auto_close=False)
    await execution.async_start(
        "The proposal names its sources and gives a concise implementation path."
    )
    close_task = asyncio.create_task(execution.async_close())
    events = [event async for event in execution.get_async_runtime_stream(timeout=None)]
    await close_task

    final = execution.result.get_state("judge_result")
    assert {item["selection_key"] for item in final["judge_items"]} == OFFERED_KEYS
    assert events[-1]["stage"] == "judge_completed"
    assert all(
        event.get("selection_key") in OFFERED_KEYS
        for event in events
        if event["stage"] == "judge_item_ready"
    )
    print({"events": events, "meta": execution.result.get_meta()})


asyncio.run(main())

# Expected key output invariant:
# zero or more provisional judge_item_ready events are followed by exactly one
# final judge_completed event containing both host-issued criterion keys.
