# Model Stream Bridge

Runtime stream is a good surface for forwarding live model output.

## 1. Core Pattern

Inside an async chunk:

1. create the Agently request
2. consume `get_async_generator(...)`
3. forward each model chunk into TriggerFlow runtime stream
4. optionally emit later workflow events

Typical pattern:

```python
async def stream_reply(data):
    request = agent.input(data.value)
    async for chunk in request.get_async_generator(type="delta"):
        await data.async_put_into_stream(chunk)
    await data.async_stop_stream()
```

## 2. Why This Belongs Here

From TriggerFlow's point of view, the important question is not provider setup or output schema design.

The important question is:

- how live model output becomes workflow-visible runtime stream

So this skill focuses on the runtime-stream side of that integration.

For model request setup or structured response control, combine this skill with:

- `agently-model-setup`
- `agently-output-control`

## 3. Async-First Rule

When forwarding model stream into TriggerFlow:

- prefer `get_async_generator(...)`
- prefer `async_put_into_stream(...)`
- prefer `async_emit(...)`

Do not default to sync wrappers in an async service.
