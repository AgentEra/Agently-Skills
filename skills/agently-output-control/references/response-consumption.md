# Response Consumption

This page explains how to read one Agently response in different forms.

## 1. `get_response()` First, Then Consume

`get_response()` creates a response snapshot for one request.

That response can then be consumed as:

- text
- parsed structured data
- a dynamic data object
- metadata
- streaming events

Use `get_response()` when the user needs more than one view of the same result.

Important consequence:

- repeated reads from one `response.result` reuse one request
- repeated shorthand calls on `agent` or `request` create new responses and therefore new requests

## 2. `get_text()`

`get_text()` returns the final text result.

Use it for:

- plain answer display
- logging the final assistant text
- quick integrations that do not need parsed fields

## 3. `get_data()`

`get_data()` returns parsed result data.

Common `type` values:

- `parsed` -> parsed structured result, default
- `original` -> original provider-style final payload
- `all` -> the full cached result record

Use `parsed` for normal structured-output workflows.

Use `original` when debugging provider payloads.

Use `all` when inspecting everything Agently cached for the response.

## 4. `get_data_object()`

`get_data_object()` returns the dynamic Pydantic object generated from the output schema.

Use it when:

- attribute access is more convenient than dictionary access
- the caller wants model-backed validation behavior

Important boundary:

- this only works for structured JSON output
- for non-structured output, it raises a type error

## 5. `get_meta()`

`get_meta()` returns response metadata accumulated from response events.

Typical contents may include:

- response id
- role
- finish reason
- usage

This depends on what the model requester broadcasts into `meta`.

## 6. Shorthand Methods

These are equivalent:

```python
response = agent.input("Hello").get_response()
data = response.result.get_data()
```

```python
data = agent.input("Hello").get_data()
```

The shorthand is good for one-shot consumption.

The explicit `response` form is better when the same result must be reused in several ways.

Example anti-pattern:

```python
text = agent.input("Hello").get_text()
meta = agent.input("Hello").get_meta()
```

That is not one request with two views. It is two requests.

## 7. Async Variants

Async versions are available for the same result types:

- `async_get_text()`
- `async_get_data()`
- `async_get_data_object()`
- `async_get_meta()`

Use them for concurrent or async-native services.

This is the preferred Agently guidance when the caller can use async APIs:

- Agently exposes async response methods directly
- sync getters are convenience wrappers built from those async methods
- sync generators are bridge layers over async generation

Prefer async variants when:

- the application already runs inside an event loop
- the service may issue multiple model requests concurrently
- the caller wants to keep request handling non-blocking

Do not oversell this:

- async-first is mainly about concurrency, throughput, and integration quality
- it is not a blanket claim that one isolated request always becomes faster

## 8. One Response, Multiple Views

This is a core Agently pattern:

```python
response = (
  agent
  .input("Explain recursion.")
  .output({"answer": (str, "Final answer")})
  .get_response()
)

text = response.result.get_text()
data = response.result.get_data()
meta = response.result.get_meta()
```

These reads operate on the same response result. They do not require another model request.

## 9. When To Use Which Form

- raw answer for UI text -> `get_text()`
- machine-readable result -> `get_data()`
- typed object access -> `get_data_object()`
- usage / finish information -> `get_meta()`
- multiple consumers from one request -> `get_response()` first
- async-native or high-concurrency runtime -> `async_get_*()` and `get_async_generator()`

For scene-based selection, read [response-patterns.md](response-patterns.md).
