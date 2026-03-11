# Streaming And Dispatch

This page covers how model streaming behaves inside TriggerFlow logic.

## 1. `delta` In A Flow

Use `delta` when the chunk should react to plain text as it arrives.

Typical uses:

- forwarding assistant text to runtime stream
- logging progress
- lightweight progressive display

## 2. `instant` / `streaming_parse` In A Flow

Use `instant` when the chunk needs structured output and early field-level visibility.

Typical uses:

- planning fields that should appear before the final action object is complete
- list items that should trigger downstream work as soon as each item finishes
- structured status updates inside a long-running flow

## 3. Dispatch Rule For `instant`

When `instant` should trigger downstream work:

- match on `path` or `wildcard_path`
- wait for `is_complete` before dispatching a stable node
- then emit a flow event with `async_emit(...)`, route it with `when(...)`, push to runtime stream, or append to a bounded work list

Do not dispatch on every partial `delta` unless the consumer truly wants token-level noise.

## 4. `when(...)` As A Stream Fan-Out Hub

Yes, a stream can be turned into TriggerFlow signal fan-out.

The pattern is:

1. one chunk consumes `delta` or `instant`
2. that chunk calls `data.async_emit("SomeEvent", payload)` when a meaningful unit is ready
3. `when("SomeEvent")` branches handle the emitted payload

This is usually a better fit for `instant` than for raw `delta`:

- `instant` gives completed structured nodes
- `delta` often produces too many tiny events for heavy downstream work

Use `delta` fan-out mainly for:

- lightweight status or log events
- UI updates
- very cheap downstream handlers

Use `instant` fan-out for:

- tool or worker dispatch
- additional model requests
- structured business-step routing
## 5. Response Reuse In A Chunk

If the chunk needs both streaming and final data, use:

```python
response = request.get_response()
```

Then:

- stream from `response.get_async_generator(...)`
- read final text or data from `response.result`

This keeps one model call and several response views inside one flow step.

## 6. Boundary With Runtime Stream

If the main topic is:

- runtime-stream lifecycle
- external consumers
- timeout / stop control
- interrupt plus runtime-stream interaction

also use `agently-triggerflow-interrupts-and-stream`.

This page only covers the model side of that bridge.
