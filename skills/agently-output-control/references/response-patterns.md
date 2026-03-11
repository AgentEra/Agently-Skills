# Response Patterns

This page gives scene-based guidance for choosing the right Agently response API.

## 1. One Quick Final Answer

Use:

- `agent.get_text()`
- `agent.get_data()`

Choose this when:

- the caller only needs one final form
- there is no need to reuse the same response as text plus data plus metadata

## 2. One Request, Multiple Views

Use:

```python
response = agent.input(...).output(...).get_response()
```

Then consume from:

- `response.result.get_text()`
- `response.result.get_data()`
- `response.result.get_data_object()`
- `response.result.get_meta()`

Choose this when:

- the UI needs final text and backend code also needs structured data
- metadata such as usage or finish reason is needed after reading the result
- one consumer streams first and another later reads the final result

## 3. Backend Business Logic Needs Stable Fields

Use:

- `.output({...})`
- `get_data()`

Add:

- `ensure_keys`

Choose this when:

- downstream code expects named fields
- the result feeds a database write, workflow step, or API response

## 4. Backend Code Prefers Attribute Access

Use:

- `.output({...})`
- `get_data_object()`

Choose this when:

- the caller wants attribute-style access
- typed object usage reads more clearly than dictionary indexing

Do not use this for plain text output.

## 5. Plain Chat UI Streaming

Use:

- `get_generator(type="delta")`

Choose this when:

- the UI only needs token-style progressive text
- structured field paths are not needed

## 6. Structured UI Or Progressive Field Updates

This is one of the most important Agently response patterns.

If the requirement is "structured output plus streaming", `instant` / `streaming_parse` should usually be the first answer.

Use:

- `.output({...})`
- `response = ...get_response()`
- `response.result.get_generator(type="instant")`

Choose this when:

- the UI updates individual fields separately
- the caller wants list items or object fields as soon as they become available
- downstream logic reacts to intermediate structured nodes before the final answer is done
- the task needs one capability that combines output control and live progressive consumption

Why this pattern is often the best fit:

- current model responses are often slow enough that waiting for the full structured object creates obvious dead time
- one request can start feeding UI and backend handling earlier instead of blocking on the final JSON object
- the caller can keep strong schema guidance while still avoiding a blank waiting state

## 7. Reasoning Or Tool Events Only

Use:

- `get_generator(type="specific", specific=[...])`

Choose this when:

- the caller wants only `reasoning_delta`
- the caller wants only `tool_calls`
- the caller wants a filtered event stream instead of the whole response

## 8. Provider Payload Debugging

Use:

- `get_data(type="original")`
- `get_generator(type="original")`
- `get_data(type="all")`

Choose this when:

- the caller is debugging provider payload shape
- the caller needs the raw final payload
- the caller needs the full cached response record

## 9. Async-First Services And Concurrency

Use:

- `async_get_text()`
- `async_get_data()`
- `async_get_data_object()`
- `async_get_meta()`
- `get_async_generator(...)`

Choose this when:

- the caller already runs inside an async web service, worker, or pipeline
- the same process may issue several model requests concurrently
- the caller needs streaming without blocking a sync wrapper bridge

Official guidance for Agently skills should treat this as the preferred path when the runtime can support it.

Why:

- Agently runtime paths are fundamentally async-first
- sync getters are convenience wrappers around async methods
- sync generators are bridge layers over async generation
- async usage is the better default for throughput and responsiveness when several requests may overlap

Important boundary:

- async-first does not mean one isolated request automatically has lower model latency
- the main benefit is cleaner async integration and better concurrent request handling

## 10. Important Anti-Pattern

Do not do this when you mean "same request, two views":

```python
text = agent.input("Hello").get_text()
meta = agent.input("Hello").get_meta()
```

That is two requests.

If the intent is one request, do this instead:

```python
response = agent.input("Hello").get_response()
text = response.result.get_text()
meta = response.result.get_meta()
```

## 11. Fast Selection Table

- final UI text only -> `get_text()`
- structured result for code -> `get_data()`
- typed structured object -> `get_data_object()`
- usage or finish info -> `get_meta()`
- one request reused several ways -> `get_response()` first
- async service or overlapping requests -> async getters or `get_async_generator()`
- simple live text stream -> `delta`
- structured output plus live field updates -> `instant` / `streaming_parse`
- filtered reasoning or tool events -> `specific`
- raw provider payload debugging -> `original` / `all`

## 12. High-Value Production Scenarios For `instant`

### Slow models or large structured outputs

Use `instant` when the model is slow enough that waiting for a full structured object would leave the UI blank for too long.

This is especially useful when:

- the schema is large
- list fields may grow item by item
- the caller wants early progress instead of one late payload

### Single request, multiple downstream consumers

Use `instant` when one model request should feed several downstream handlers without issuing several model calls.

Typical pattern:

- one field updates the user-visible preview
- another field feeds a validator, router, or persistence step
- list items can be processed as they become complete

This is an Agently design recommendation inferred from partial-object streaming and eager structured streaming patterns in the broader ecosystem.

### Structured UI that should not wait for the whole answer

Use `instant` when the response is naturally rendered as cards, sections, checklist items, notifications, or dashboard panels.

The goal is not only lower perceived latency. It is also better interaction design:

- fields can appear in the right place immediately
- list items can append progressively
- the UI does not need to wait for one final object before becoming useful

### Early handoff into tools or business workflow steps

Use `instant` when a later system can start work as soon as one structured field or list item is ready.

Examples:

- enqueue a search or fetch job when a query field completes
- start rendering or storing one completed section while the model continues generating later sections
- trigger partial business logic on one finished node instead of waiting for the whole reply

This is an Agently design recommendation inferred from the same incremental structured-streaming behavior.
