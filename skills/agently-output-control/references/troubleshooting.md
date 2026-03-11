# Troubleshooting

This page only covers output-control issues.

## 1. `get_data_object()` Raises A Type Error

Most common cause:

- the request is not using structured JSON output

Check these first:

- whether `.output(...)` defines a mapping or list schema
- whether the request actually needs structured output instead of plain text

## 2. `ensure_keys` Keeps Failing

Check these first:

- whether the key paths match the real schema
- whether the chosen `key_style` matches the path syntax
- whether wildcard paths such as `items[*].title` are needed
- whether the schema itself is too brittle or too large

Default advice:

- enforce only business-critical keys first

## 3. `instant` / `streaming_parse` Yields Nothing Useful

Most common causes:

- the output is not structured JSON
- the model response cannot be incrementally parsed into the expected JSON shape

Check these first:

- whether `.output(...)` is structured
- whether `delta` streaming is actually producing JSON-shaped content
- whether the schema is simple enough for the model to follow reliably

## 4. `specific` Streaming Does Not Show Expected Events

Check these first:

- whether the selected events are actually emitted by the requester
- whether the provider supports reasoning or tool-call streaming for that request
- whether `specific` was filtered too narrowly

## 5. Response Reuse Does Not Reflect New Prompt Changes

Most common cause:

- the response was created before the prompt changed

Reminder:

- `get_response()` snapshots the current prompt and then clears the request prompt
- create a new response after changing the request

## 6. The Parsed Result Is Incomplete But No Exception Was Raised

Most common cause:

- `raise_ensure_failure=False`

Check:

- whether the caller intentionally requested the last partial result after retries

## 7. `original` / `all` Returns More Than The Caller Expected

This is normal.

Use:

- `parsed` for business logic
- `original` for provider-payload debugging
- `all` for deep inspection of cached response state

## 8. The Caller Expected One Request But Accidentally Sent Two

Most common cause:

- shorthand getters were called separately on `agent` or `request`

Typical mistake:

- `agent.get_text()` and later `agent.get_meta()` for what should have been one response

Use:

- `response = ...get_response()` first

## 9. Fast Triage

- schema problems: check `.output(...)`
- reliability problems: check `ensure_keys`, `key_style`, and retries
- text vs structured confusion: check `get_text()` versus `get_data()`
- streaming problems: check `type`, path style, and whether the output is structured JSON
- response reuse confusion: check when `get_response()` was created
- async service integration issues: prefer `async_get_*()` and `get_async_generator()` over sync wrappers
