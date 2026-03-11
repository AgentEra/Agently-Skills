# Verification

After model setup, a minimal verification request is recommended. It is not mandatory, but it should usually be suggested as a standard follow-up step.

## 1. Verification Goal

The goal is not to prove the whole business flow is correct. The goal is to quickly confirm:

- auth is correct
- the URL is correct
- the model name is correct
- the user scenario was mapped correctly across text, completions, or image-understanding usage
- extra parameters are at least entering the request

## 2. Minimal chat verification

```python
from agently import Agently

Agently.set_settings("OpenAICompatible", {
  "base_url": "https://api.example.com/v1",
  "model": "your-chat-model",
  "api_key": "YOUR_API_KEY",
})

agent = Agently.create_agent()
print(agent.input("Reply with OK only.").start())
```

## 3. Minimal completions verification

```python
from agently import Agently

Agently.set_settings("OpenAICompatible", {
  "base_url": "https://api.example.com/v1",
  "model": "your-completions-model",
  "model_type": "completions",
  "api_key": "YOUR_API_KEY",
})

agent = Agently.create_agent()
print(agent.input("Complete this sentence: Agently is").start())
```

## 4. Minimal VLM verification

```python
from agently import Agently

Agently.set_settings("OpenAICompatible", {
  "base_url": "https://api.example.com/v1",
  "model": "your-vlm-model",
  "api_key": "YOUR_API_KEY",
})

agent = Agently.create_agent()

result = (
  agent
  .attachment([
    {"type": "text", "text": "What is in this image?"},
    {
      "type": "image_url",
      "image_url": {"url": "https://example.com/demo.png"}
    }
  ])
  .start()
)

print(result)
```

Key reminders:

- do not set `model_type="vlm"`
- if it fails, check model vision support and image reachability before assuming the wrong Agently pattern

## 5. Verification with extra parameters

If the main concern is whether `temperature`, `tools`, or `thinking` is taking effect:

```python
result = (
  agent
  .input("Reply in one sentence.")
  .options({"temperature": 0.2})
  .start()
)
```

## 6. Recommended debug settings

```python
Agently.set_settings("debug", True)
```

or:

```python
Agently.set_settings("runtime.show_model_logs", True)
```

Check these first:

- `request_url`
- `request_options`
- `stream`
- whether the primary field is `messages` or `prompt`

If the user is relying on a proxy, also confirm:

- `proxy` is configured at the plugin settings layer
- the proxy address itself is reachable
- the failure is not caused by a wrong `base_url` being mistaken for a proxy problem

## 7. Common failure signals

- `401 Unauthorized`
- `404` / endpoint not found
- model not found
- VLM image understanding does not work
- parameters do not take effect

All of these should route back to `troubleshooting.md`.

Additional proxy-related signals:

- connect timeout before any auth error
- TLS or reachability failure before the provider returns a response
- the same config works after removing regional network restrictions or after switching proxy

## 8. When it can be skipped

You can usually skip it only when:

- the provider, model name, endpoint, and auth have not changed
- only the prompt changed, not the model setup
