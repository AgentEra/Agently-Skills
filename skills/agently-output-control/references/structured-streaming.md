# Structured Streaming

This page covers the streaming modes exposed by Agently response consumers.

## 1. Streaming Types

Agently supports these response-generator types:

- `delta`
- `specific`
- `original`
- `all`
- `instant`
- `streaming_parse`

Both sync and async variants exist.

## 2. `delta`

`type="delta"` yields text deltas only.

Use it for:

- token-style streaming text in a CLI or chat UI
- simple live display when structured field paths are not needed

## 3. `specific`

`type="specific"` yields selected raw event tuples.

Default event selection includes:

- `reasoning_delta`
- `delta`
- `reasoning_done`
- `done`
- `tool_calls`

Use this when the user cares about event classes such as:

- reasoning stream
- tool calls
- final answer stream

Example:

```python
for event, data in response.get_generator(type="specific"):
  ...
```

## 4. `original`

`type="original"` yields provider-original response data emitted as `original_*` events.

Use this for:

- low-level debugging
- inspecting the final provider payload

## 5. `all`

`type="all"` yields raw `(event, data)` pairs for everything the parser emits.

Use this when debugging the full response event stream.

## 6. `instant` And `streaming_parse`

These are the structured-streaming modes.

This is the mode family to emphasize when the user wants Agently's "structured output plus streaming" capability.

Important facts:

- `instant` is the v3-compatible alias of `streaming_parse`
- both modes yield `StreamingData` objects, not plain strings
- they only work when the response parser has a structured JSON schema to parse against
- they are the default answer when the caller needs field-level progressive updates instead of plain text deltas

Use them when:

- the UI needs path-level updates
- downstream logic should react as soon as one field or list item is complete
- the user wants structured output and streaming at the same time

## 7. `StreamingData`

Key fields on each `StreamingData` item:

- `path`
- `wildcard_path`
- `indexes`
- `value`
- `delta`
- `is_complete`
- `event_type`
- `full_data`

Typical usage:

- `path` for the concrete field path
- `wildcard_path` for matching list items such as `tips[*]`
- `delta` for incremental text updates
- `is_complete` for actions that should only happen once a field is finalized

## 8. Tool Calls In Structured Streaming

When a `tool_calls` event arrives during `instant` / `streaming_parse`, the parser yields:

- `StreamingData(path="$tool_calls", value=data)`

Use this when the user needs one structured stream that includes both JSON field updates and tool-call signals.

## 9. Path Style

`response.streaming_parse_path_style` controls structured-streaming path style:

- `dot` -> `tips[*]`, `final.answer`
- `slash` -> `/tips/[*]`, `/final/answer`

Default:

- `dot`

Use `slash` only when the consumer already expects slash-style paths.

## 10. Async Variants

Use `get_async_generator(...)` for async services or concurrent workloads.

The meaning of each streaming type stays the same.

## 11. Common Patterns

### Plain text streaming

```python
for delta in agent.input("Explain recursion").get_generator(type="delta"):
  print(delta, end="", flush=True)
```

### Structured list streaming

```python
for item in response.get_generator(type="instant"):
  if item.wildcard_path == "tips[*]" and item.delta:
    ...
```

### Reasoning and tool-call streaming

```python
for event, data in response.get_generator(type="specific"):
  if event == "reasoning_delta":
    ...
  if event == "tool_calls":
    ...
```

## 12. Why `instant` Matters In Real Systems

`instant` / `streaming_parse` is not just a convenience mode.

It is particularly valuable when:

- the model is slow and the caller wants meaningful progress before the full object is complete
- one structured response needs to drive both UI feedback and backend handling
- the UI renders sections, cards, notifications, or list items that can appear independently
- downstream code can act on completed nodes or list items before the whole object finishes

In practice, this means one request can support:

- progressive feedback for the user
- schema-constrained output for the application
- earlier downstream work without waiting for a second request or a final full-object barrier

This recommendation is consistent with the broader ecosystem's use of partial-object streaming, streamed object UIs, and eager structured/tool-parameter streaming.
