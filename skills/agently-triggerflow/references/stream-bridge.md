# Structured Stream Bridge

Use this pattern when a model step emits structured partial updates and the UI or downstream consumer should receive stable business events instead of raw parser paths.

## When To Use It

- the model already returns structured output and you want progressive UI updates
- the frontend should render blocks such as `summary_ready`, `judge_item_ready`, or `report_section_ready`
- a TriggerFlow step should translate model parser events into workflow-owned stream items

## Core Rule

Do not couple the UI directly to raw `instant` paths such as `judge_items[0].comment` or `meta.risk_flags[1]`.

Instead:

1. consume model-side `instant` or `streaming_parse`
2. accumulate partial state in the workflow step
3. detect when a business block is complete enough to emit
4. call `async_put_into_stream(...)` with a stable workflow event
5. close the execution with `async_close()` so the runtime stream receives its stop signal

## Minimal Shape

```python
import asyncio
import re
import os

from agently import Agently, TriggerFlow

Agently.set_settings(
    "OpenAICompatible",
    {
        "base_url": os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1"),
        "api_key": "ollama",
        "model": os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),
        "model_type": "chat",
        "request_options": {"temperature": 0},
    },
)

agent = Agently.create_agent()
flow = TriggerFlow(name="stream-bridge")
PATH_PATTERN = re.compile(r"^judge_items\[(\d+)\]\.(\w+)$")


def item_is_complete(item):
    return isinstance(item, dict) and {"name", "score", "comment"}.issubset(item.keys())


@flow.chunk("judge")
async def judge(data):
    agent.role(
        "Return JSON only. judge_items must contain exactly two items: item 0 is clarity with score 8 and comment Clear and direct. item 1 is evidence with score 7 and comment Backed by examples.",
        always=True,
    )
    result = (
        agent
        .input(f"Score this draft and explain strengths: {data.input['essay']}")
        .output({"judge_items": [{"name": (str, None, True), "score": (int, None, True), "comment": (str, None, True)}]})
        .get_result()
    )

    partial = {"judge_items": []}
    emitted_items = set()

    # `instant` yields agently.StreamingData items.
    async for msg in result.get_async_generator(type="instant"):
        path = getattr(msg, "path", None) or getattr(msg, "wildcard_path", None)
        match = PATH_PATTERN.match(path or "")
        if match is None:
            continue

        item_index = int(match.group(1))
        field_name = match.group(2)
        while len(partial["judge_items"]) <= item_index:
            partial["judge_items"].append({})
        value = getattr(msg, "value", None)
        if value is None:
            value = getattr(msg, "delta", None)
        partial["judge_items"][item_index][field_name] = value

        if item_is_complete(partial["judge_items"][item_index]) and item_index not in emitted_items:
            emitted_items.add(item_index)
            await data.async_put_into_stream(
                {
                    "stage": "judge_item_ready",
                    "index": item_index,
                    "item": partial["judge_items"][item_index],
                }
            )

    final = await result.async_get_data(max_retries=1)
    await data.async_set_state("judge_result", final)
    return final


async def main():
    execution = flow.create_execution(auto_close=False)
    await execution.async_start({"essay": "..."})
    close_task = asyncio.create_task(execution.async_close())
    async for item in execution.get_async_runtime_stream(timeout=None):
        print(item)
    state = await close_task
    meta = execution.result.get_meta()
    return {"judge_result": state["judge_result"], "execution_id": meta["execution_id"]}


asyncio.run(main())
```

## Recommended Event Shape

Prefer stream items that describe business readiness, not parser mechanics:

- `summary_ready`
- `judge_item_ready`
- `annotation_ready`
- `report_ready`
- `warning`

Avoid exposing:

- raw parser paths
- low-level partial tokens that the UI cannot interpret
- unstable field names that may change when the prompt contract evolves

## Placement Rule

- model contract stays in prompt config or output control
- path-to-state accumulation stays inside the workflow step or a small workflow-owned helper
- UI event naming belongs to TriggerFlow, because the workflow owns the delivery contract
- stream shutdown belongs to execution close, not to ad hoc UI timeout logic

## Validation Rule

A good bridge layer lets you change the model schema details without forcing the frontend to rewrite its event consumer, as long as the business event contract stays the same.

## Provisional Downstream Fan-Out

The same bridge can start independent work before the full model result exists,
but only with a start/cache/reconcile contract:

1. require a complete canonical `instant` item;
2. compute a host-owned key from its task-relevant payload;
3. call `await data.async_emit_nowait(...)` once for that key and continue the
   stream loop;
4. let the TriggerFlow execution own concurrency, close, and task draining;
5. read final validated data from the same result;
6. reuse matching work, emit missing accepted items, and cancel or discard
   provisional extras before the final join.

Do not await each retrieval inline in the model stream loop, and do not use a
partial string delta as an external request. Repeated deltas, provider replay,
and validation replacement attempts must converge on the same host key rather
than repeat work. Only read-only or otherwise idempotent/cancelable preparation
may start provisionally. See
`examples/instant_retrieval_overlap.py`.
