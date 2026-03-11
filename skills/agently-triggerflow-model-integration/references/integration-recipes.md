# Integration Recipes

This page gives high-value integration patterns for model calls inside TriggerFlow.

## 1. One Request Per Step

Pattern:

- chunk creates request
- chunk awaits final structured or text result
- chunk returns that result

Use when:

- the step is simple
- no live output is needed

## 2. Stream To Runtime Stream, Then Return Final Result

Pattern:

- chunk creates `response = request.get_response()`
- chunk streams `delta` or `instant`
- chunk forwards selected items into `data.put_into_stream(...)`
- chunk returns final text or parsed data

Use when:

- the caller wants a useful live stream
- the flow still needs a final result

## 3. Planning Loop With Structured Streaming

Pattern:

- planning request uses `.output(...)`
- consume `instant` inside the chunk
- surface planning deltas or completed decision fields early
- emit the final plan into the next flow step

Use when:

- one model call should guide later orchestration
- the user should not wait for the whole plan object before seeing progress

## 4. Parallel Model Fan-Out

Pattern:

- `batch(...)` or `for_each(concurrency=...)`
- each branch or item creates its own request
- collect results back into the flow

Use when:

- several independent model calls can overlap
- one request per item keeps the workflow logic clearer

## 5. Service Endpoint Pattern

Pattern:

- TriggerFlow handles orchestration
- model deltas or structured updates are forwarded into runtime stream
- FastAPIHelper or another service layer exposes the runtime stream outward

Use when:

- the workflow serves HTTP or SSE clients
- the service needs a live response stream and a final business result
