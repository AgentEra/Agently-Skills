# Provider Recipes

These recipes only demonstrate standard setup patterns.

## 1. Generic Template

```python
from agently import Agently

Agently.set_settings("OpenAICompatible", {
  "base_url": "https://api.example.com/v1",
  "model": "your-model-name",
  "api_key": "YOUR_API_KEY",
})
```

If the user only wants to “get it connected first”, start with this template and then customize `base_url` and `model` for the provider.

If the provider can only be reached through a proxy in the user's region, add:

```python
"proxy": "http://127.0.0.1:7890",
```

## 2. OpenAI

```python
Agently.set_settings("OpenAICompatible", {
  "base_url": "https://api.openai.com/v1",
  "model": "gpt-5",
  "api_key": "<OpenAI-API-Key>",
})
```

If the environment needs a proxy, add:

```python
"proxy": "http://127.0.0.1:7890"
```

## 3. Claude

```python
Agently.set_settings("OpenAICompatible", {
  "base_url": "https://api.anthropic.com/v1",
  "model": "claude-sonnet-4-5",
  "api_key": "<Anthropic-API-Key>",
})
```

Make it explicit that:

- this is the OpenAI-compatible access path
- this is not the Anthropic native SDK path

## 4. DeepSeek

```python
Agently.set_settings("OpenAICompatible", {
  "base_url": "https://api.deepseek.com/v1",
  "model": "deepseek-chat",
  "api_key": "<DeepSeek-API-Key>",
})
```

If the user asks about reasoning-style extra parameters, do not overload the basic recipe. Move that discussion to `request_options` / `agent.options()`.

## 5. Gemini

```python
Agently.set_settings("OpenAICompatible", {
  "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
  "model": "gemini-2.5-flash",
  "api_key": "<Google-AIStudio-API-Key>",
})
```

## 6. Ollama

```python
Agently.set_settings("OpenAICompatible", {
  "base_url": "http://127.0.0.1:11434/v1",
  "model": "qwen2.5-coder:14b",
  "auth": None,
})
```

Check these first:

- whether the Ollama service is running
- whether the model has been pulled
- whether `base_url` really ends with `/v1`

## 7. Self-Hosted Or Gateway-Rewritten OpenAI-Compatible Endpoint

Try the standard form first:

```python
Agently.set_settings("OpenAICompatible", {
  "base_url": "https://your-gateway.example.com/v1",
  "model": "your-model",
  "api_key": "YOUR_API_KEY",
})
```

If the path is non-standard, switch immediately to:

```python
Agently.set_settings("OpenAICompatible", {
  "full_url": "https://your-gateway.example.com/custom/chat/completions",
  "model": "your-model",
})
```

## 8. VLM Recipe

If the user wants image understanding, visual Q&A, or OCR, treat it as a VLM scenario. In Agently, the base model configuration stays the same and only the request content changes by adding `attachment()`:

```python
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
```

## 9. Default Selection Rules

- official OpenAI-compatible endpoint -> use `base_url`
- only one fixed full endpoint -> use `full_url`
- local Ollama -> do not start with complex auth
- image understanding / OCR / visual Q&A -> treat as a VLM scenario, then implement as `chat + attachment()`
- region-restricted or proxy-required access -> add top-level `proxy`, do not put it in `request_options`

## 10. What Not To Add By Default In A Recipe

- do not start by adding complex `request_options`
- do not start by changing `content_mapping`
- do not start by assuming a custom requester is needed
