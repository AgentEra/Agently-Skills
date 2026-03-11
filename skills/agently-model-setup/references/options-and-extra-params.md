# Options And Extra Params

This page answers one question: how should extra request parameters be added?

## 1. Actual Merge Order In Source

The requester assembles parameters in this order:

1. Read plugin-root `options` as a backward-compatible fallback
2. Read plugin-level `request_options`
3. Read prompt-level `options`
4. Write `model` back into the request
5. Write `stream` back into the request

That leads to these conclusions:

- plugin-root `options` still works as a compatibility path
- `agent.options({...})` overrides `request_options`
- `agent.options({"model": ...})` does not actually override the final model name
- `agent.options({"stream": ...})` does not actually override the final stream mode

## 2. Two Supported Entry Points

### 2.1 Default extra parameters: `request_options`

```python
Agently.set_settings("OpenAICompatible", {
  "request_options": {
    "temperature": 0.2,
    "top_p": 0.9
  }
})
```

Good for:

- project-wide default temperature
- default token limits
- default provider-native extra fields

### 2.2 Per-request parameters: `agent.options({...})`

```python
result = (
  agent
  .input("Explain RAG briefly")
  .options({
    "temperature": 0.7,
    "max_tokens": 300
  })
  .start()
)
```

Good for:

- temporarily increasing temperature for one request
- adding `tools` for one request
- adding provider-native fields for one request

## 3. Compatibility And Preferred Field

Current request assembly reads:

- plugin-root `options` as a backward-compatible fallback
- plugin-level `request_options`
- prompt-level `options`

So the current guidance is:

- plugin-root `options` should still work on the compatibility path
- `request_options` is the preferred field for new default request-body parameters
- `agent.options({...})` remains the per-request override layer

## 4. Common Parameter Categories

### 4.1 Sampling and generation controls

- `temperature`
- `top_p`
- `max_tokens`
- `presence_penalty`
- `frequency_penalty`

### 4.2 Provider-native tools / function calling

```python
agent.options({
  "tools": [...],
  "tool_choice": "auto"
})
```

This refers to provider-native request-body fields, not Agently’s `@tool_func + use_tools()` flow.

### 4.3 Provider-native reasoning / thinking

For example:

```python
agent.set_settings("OpenAICompatible", {
  "request_options": {
    "thinking": {"type": "enabled"}
  }
})
```

These fields are not part of Agently’s abstraction layer, but they can be passed through directly.

### 4.4 Custom Body Fields

If it is a normal request-body field:

- put it in `request_options`
- or put it in `agent.options({...})`

If it is an auth-related field:

- prefer `auth`

## 5. Typical Scenarios

### Default low temperature, one-off override

```python
Agently.set_settings("OpenAICompatible", {
  "request_options": {"temperature": 0.2}
})

agent.input("Write a catchy slogan").options({"temperature": 0.8}).start()
```

### Pass provider-native tools on a single request

```python
agent.options({
  "tools": [...],
  "tool_choice": "auto"
})
```

### Limit output length for a single request

```python
agent.options({
  "max_tokens": 400
})
```

## 6. Explicitly Not Recommended

- treating plugin-root `options` as the preferred field for new default request-body parameters
- trying to change `model` via `agent.options()`
- trying to change `stream` via `agent.options()`
- treating Agently tool orchestration and provider-native `tools` as the same mechanism

## 7. Default Decision Rules

- long-lived default parameters: usually go in `request_options`
- per-request temporary parameters: usually go in `agent.options({...})`
- `model` / `stream`: do not treat them like normal extra parameters
