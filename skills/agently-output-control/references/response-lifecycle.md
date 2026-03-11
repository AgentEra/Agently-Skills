# Response Lifecycle

This page explains why one response can be consumed multiple times without sending another request.

## 1. Response Snapshot

`get_response()` creates a `ModelResponse` snapshot of:

- current settings
- current prompt
- current extension handlers

That snapshot becomes the stable source for one response instance.

## 2. Request Prompt Clearing

After `get_response()` creates the response object, the request prompt is cleared.

Implication:

- later prompt mutations do not retroactively change an already-created response

If the user wants a different result, create a new response after changing the request prompt.

## 3. When The Real Request Starts

The actual model request starts when the response result is consumed.

That means these calls trigger the request:

- `get_text()`
- `get_data()`
- `get_data_object()`
- `get_meta()`
- `get_generator(...)`
- `get_async_generator(...)`

## 4. Cached Result State

The response parser stores result state in one shared cached structure.

Important cached fields include:

- `text_result`
- `parsed_result`
- `result_object`
- `meta`
- `original_delta`
- `original_done`
- `errors`
- `extra`

## 5. Why Multiple Reads Do Not Re-Request

Agently uses `GeneratorConsumer` to consume the underlying response stream once and replay history to later consumers.

That is why this works:

```python
response = agent.input("Hello").get_response()

text = response.result.get_text()
meta = response.result.get_meta()
```

Both calls read from the same cached response lifecycle.

## 6. Good Usage Pattern

Use explicit `response = ...get_response()` when:

- the same result must be shown in several forms
- one consumer streams while another later reads final structured data
- metadata is needed after text or parsed data has already been read

## 7. Common Misunderstandings

- changing the request prompt after `get_response()` does not update that existing response
- reading `response.result.get_meta()` after `get_data()` does not trigger a second request
- calling `agent.get_text()` and then `agent.get_meta()` does trigger separate requests because each shorthand call creates its own response
- retries triggered by `ensure_keys` are new requests created on purpose; normal repeated reads are not
