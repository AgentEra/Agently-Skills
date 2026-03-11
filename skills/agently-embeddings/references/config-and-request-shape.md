# Config And Request Shape

This page covers how Agently builds an embeddings request.

## 1. Required Setup Shape

The standard path is:

```python
embedding = Agently.create_agent()
embedding.set_settings(
    "OpenAICompatible",
    {
        "base_url": "...",
        "model": "...",
        "model_type": "embeddings",
    },
)
```

Core settings:

- `model_type="embeddings"`
- `model`
- `base_url` or `full_url`
- auth as needed

Normal networking settings still apply:

- `proxy`
- `timeout`
- `client_options`
- `request_options`

## 2. Endpoint Shape

With `model_type="embeddings"`, the default OpenAI-compatible path is:

- `/embeddings`

If `full_url` is set, it overrides `base_url + path_mapping`.

## 3. Request Body Shape

Embeddings requests are not built from chat messages.

The request body uses:

- `input`

It does not build:

- `messages`
- `prompt`

That is the main behavioral difference from `chat` and `completions`.

## 4. Prompt Boundary

For embeddings, the meaningful prompt payload is `input(...)`.

Do not expect these to become the embeddings request body:

- `info(...)`
- `instruct(...)`
- `examples(...)`
- `.output(...)`
- `attachment(...)`

If the user is asking about prompt composition in general, that belongs elsewhere.

## 5. Extra Provider Parameters

Embeddings-specific provider parameters still follow the normal OpenAICompatible layering rules:

- persistent defaults -> `request_options`
- one-request overrides -> `agent.options({...})`

Typical examples include provider-specific fields such as:

- `dimensions`
- `encoding_format`
- `user`

As with other model types, `model` and `stream` are finalized by the plugin layer.

## 6. Streaming Boundary

Do not model embeddings as a streaming workflow.

Practical guidance:

- treat `stream` as irrelevant for embeddings
- do not plan around `delta`, `instant`, or other response-streaming patterns
- embeddings return one completed result after the request finishes
- use parsed result consumption after that normal request completes
