# Structured Stream Bridge

Use this pattern when a model step emits structured partial updates and the UI or downstream consumer should receive stable business events instead of raw parser paths.

## When To Use It

- the model already returns structured output and you want progressive UI updates
- the frontend should render blocks such as `summary_ready`, `judge_item_ready`, or `report_section_ready`
- a TriggerFlow step should translate model parser events into workflow-owned stream items

## Core Rule

Do not couple the UI directly to raw `instant` paths such as `judge_items.0.comment` or `meta.risk_flags.1`.

Instead:

1. consume model-side `instant` or `streaming_parse`
2. accumulate partial state in the workflow step
3. detect when a business block is complete enough to emit
4. call `async_put_into_stream(...)` with a stable workflow event

## Minimal Shape

```python
from agently import Agently, TriggerFlow

agent = Agently.create_agent()
flow = TriggerFlow(name="stream-bridge")


@flow.chunk("judge")
async def judge(data):
    response = (
        agent
        .input(data.value["essay"])
        .get_response()
    )

    partial = {"judge_items": []}
    emitted_items = set()

    async for msg in response.get_async_generator(type="instant"):
        path = getattr(msg, "path", None) or getattr(msg, "wildcard_path", None)
        if not path:
            continue

        # update your partial state here
        # for example: set_value_by_path(partial, path, msg.delta or msg.value)

        if path.startswith("judge_items.") and item_is_complete(partial, path):
            item_index = int(path.split(".")[1])
            if item_index not in emitted_items:
                emitted_items.add(item_index)
                await data.async_put_into_stream(
                    {
                        "stage": "judge_item_ready",
                        "index": item_index,
                        "item": partial["judge_items"][item_index],
                    }
                )

    result = await response.result.async_get_data()
    await data.async_put_into_stream(
        {
            "stage": "report_ready",
            "summary": result["summary"],
        }
    )
    return result
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

## Validation Rule

A good bridge layer lets you change the model schema details without forcing the frontend to rewrite its event consumer, as long as the business event contract stays the same.
