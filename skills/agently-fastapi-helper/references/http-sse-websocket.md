# HTTP, SSE, And WebSocket

Use this page when choosing the transport shape for the helper.

## 1. POST And GET

Use:

- `use_post(...)`
- `use_get(...)`

when the client should wait for one wrapped final result.

This is the simplest exposure mode for:

- one-shot chat
- one-shot structured output
- one-shot retrieval-then-answer

## 2. SSE

Use:

- `use_sse(...)`

when the client needs progressive one-way output.

This is usually the best fit for:

- token streaming
- runtime-stream events
- lightweight progress updates

## 3. WebSocket

Use:

- `use_websocket(...)`

when the interaction should stay open for repeated bidirectional messages.

Choose WebSocket only when the client really needs a persistent interactive channel.
