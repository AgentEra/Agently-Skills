# OpenAICompatible Config

`OpenAICompatible` is the default registered and activated model requester plugin in Agently v4. `OpenAICompatible`, `OpenAI`, and `OAIClient` are aliases of the same plugin.

## 1. Core Namespace

- activation path: `plugins.ModelRequester.activate`
- default activation value: `OpenAICompatible`
- plugin settings namespace: `plugins.ModelRequester.OpenAICompatible`

Common entry point:

```python
from agently import Agently

Agently.set_settings("OpenAICompatible", {
  "base_url": "https://api.openai.com/v1",
  "model": "gpt-4.1",
})
```

## 2. Default Settings

Key defaults from `OpenAICompatible.DEFAULT_SETTINGS`:

| Field | Default |
| --- | --- |
| `model_type` | `chat` |
| `model` | `None` |
| `default_model.chat` | `gpt-4.1` |
| `default_model.completions` | `gpt-3.5-turbo-instruct` |
| `default_model.embeddings` | `text-embedding-ada-002` |
| `client_options` | `{}` |
| `headers` | `{}` |
| `proxy` | `None` |
| `request_options` | `{}` |
| `base_url` | `https://api.openai.com/v1` |
| `full_url` | `None` |
| `path_mapping.chat` | `/chat/completions` |
| `path_mapping.completions` | `/completions` |
| `path_mapping.embeddings` | `/embeddings` |
| `auth` | `None` |
| `stream` | `True` |
| `rich_content` | `False` |
| `strict_role_orders` | `True` |
| `content_mapping_style` | `dot` |

## 3. Model And Routing Fields

### `model_type`

The source supports:

- `chat`
- `completions`
- `embeddings`

This skill mainly focuses on:

- `chat`
- `completions`
- image-understanding VLM scenarios still end up using `chat`

### `model`

Purpose:

- sets the provider model name
- falls back to `default_model[model_type]` when omitted

### `base_url` / `full_url` / `path_mapping`

Request URL assembly:

1. If `full_url` is a string, use it directly
2. Otherwise use `base_url + path_mapping[model_type]`

Therefore:

- use `base_url` first for standard OpenAI-compatible endpoints
- use `full_url` first for non-standard paths or custom gateways

## 4. Network And Auth Fields

### `headers`

- added as extra request headers
- `Connection: close` is added automatically

### `proxy`

- when present, it is written into `client_options["proxy"]`
- this is the standard field for model-request proxy configuration in Agently
- use it when the model service can only be reached through a local or regional proxy

Standard example:

```python
Agently.set_settings("OpenAICompatible", {
  "base_url": "https://api.openai.com/v1",
  "model": "gpt-5",
  "api_key": "YOUR_API_KEY",
  "proxy": "http://127.0.0.1:7890",
})
```

Agent-specific override:

```python
agent.set_settings("OpenAICompatible", {
  "proxy": "http://127.0.0.1:7890"
})
```

Use this field when:

- some regions require a proxy to reach the provider endpoint
- only one agent should use a proxy while the rest of the project should not

Do not put proxy configuration in:

- `request_options`
- `agent.options({...})`

Reason:

- `proxy` is an HTTP client transport setting
- `request_options` and `agent.options({...})` are for request-body fields, not network transport fields

### `timeout`

This is converted into `httpx.Timeout`, with defaults:

```yaml
connect: 30.0
read: 600.0
write: 30.0
pool: 30.0
```

### `client_options`

- passed directly into `httpx.AsyncClient`
- suitable for httpx-level configuration, not request-body fields
- if the user only needs a normal HTTP proxy, prefer the top-level `proxy` field instead of manually editing `client_options`
- Agently uses `httpx.AsyncClient` as its underlying network client for model requests
- in the current requester path, Agently builds a fresh `AsyncClient(**client_options)` for each request, then applies request headers and sends the POST call

Practical rule:

- use top-level Agently fields first when a dedicated field already exists, such as `proxy` or `timeout`
- use `client_options` when the requirement is really about the HTTP client itself

Important precedence:

- top-level `proxy` is merged into `client_options["proxy"]`
- top-level `timeout` is converted into `httpx.Timeout(...)` and then written into `client_options["timeout"]`
- if both top-level fields and `client_options` provide the same key, the dedicated top-level Agently field is the safer source of truth

Common `client_options` scenarios:

#### Connection pool and concurrency limits

Use `httpx.Limits(...)` when the user needs to cap concurrent connections or reduce keep-alive pool behavior for a gateway or restricted environment.

```python
import httpx

Agently.set_settings("OpenAICompatible", {
  "base_url": "https://api.example.com/v1",
  "model": "your-model",
  "api_key": "YOUR_API_KEY",
  "client_options": {
    "limits": httpx.Limits(
      max_connections=20,
      max_keepalive_connections=5,
      keepalive_expiry=30.0,
    )
  },
})
```

Use this when:

- the user wants to limit concurrent outbound connections
- a gateway behaves badly under a high connection count
- the user wants explicit connection-pool limits instead of defaults

#### Redirect handling

Use `follow_redirects=True` when a gateway, proxy, or enterprise endpoint returns redirects that should be followed automatically.

```python
Agently.set_settings("OpenAICompatible", {
  "client_options": {
    "follow_redirects": True
  }
})
```

#### HTTP/2

Use `http2=True` when the provider or gateway explicitly benefits from HTTP/2.

```python
Agently.set_settings("OpenAICompatible", {
  "client_options": {
    "http2": True
  }
})
```

#### TLS, CA bundle, and environment-driven network settings

Use `verify`, `cert`, or `trust_env` when the deployment environment needs custom TLS behavior or environment-provided proxy / certificate settings.

```python
Agently.set_settings("OpenAICompatible", {
  "client_options": {
    "verify": "/path/to/custom-ca.pem",
    "trust_env": True
  }
})
```

Use this when:

- the runtime relies on environment-level proxy variables or CA bundle settings
- the provider is behind a corporate gateway with a custom CA

#### Advanced transport customization

Use `transport` only when the user explicitly needs transport-level behavior that is not covered by the top-level Agently fields.

```python
import httpx

Agently.set_settings("OpenAICompatible", {
  "client_options": {
    "transport": httpx.AsyncHTTPTransport(retries=2)
  }
})
```

Default advice:

- do not start with `transport`
- use it only after `proxy`, `timeout`, `limits`, and normal TLS settings are not enough

What not to use `client_options` for:

- request-body fields such as `temperature`, `tools`, or provider-native generation parameters
- normal per-request prompt tuning
- replacing top-level `proxy` or `timeout` when the dedicated Agently field already covers the need

### `api_key` And `auth`

The current source reads:

- `auth`
- `api_key`

Behavior:

- when `auth` is not a dict, it is normalized as `{ "api_key": value }`
- when `api_key` is set separately and `auth.api_key` is empty, `api_key` is used as a fallback

These are the safest primary patterns to document:

```python
Agently.set_settings("OpenAICompatible", {
  "api_key": "YOUR_API_KEY"
})
```

```python
Agently.set_settings("OpenAICompatible", {
  "auth": "YOUR_API_KEY"
})
```

```python
Agently.set_settings("OpenAICompatible", {
  "auth": {
    "body": {
      "X-User-Token": "xxx"
    }
  }
})
```

`auth.headers` is merged into outgoing request headers.

If `api_key` is also set, Agently writes Bearer auth into `Authorization` after merging `auth.headers`, so custom non-Authorization headers are preserved while `Authorization` follows `api_key`.

## 5. Request Body Fields

### `request_options`

This is the standard plugin-level entry point for default extra request-body parameters.

Request assembly order in the current source:

1. Read legacy plugin-root `options`
2. Read `request_options`
3. Merge prompt `options`
4. Write `model` back into the request
5. Write `stream` back into the request

Therefore:

- `request_options` is the right place for default temperature, default tool fields, and default provider-specific extra fields
- plugin-root `options` is a backward-compatible fallback, not the preferred field for new config
- it does not override the final `model` and `stream` written by the plugin layer

### `stream`

Current source behavior:

- when explicitly set, the explicit value is used
- when not explicitly set:
  - `embeddings` -> `False`
  - everything else -> `True`

### `rich_content`

- defaults to `False`
- automatically turns on when `attachment` exists in the prompt

### `strict_role_orders`

- controls role-order normalization in `to_messages(...)`

## 6. Response Mapping Fields

These fields normalize provider responses into Agently events:

- `content_mapping`
- `content_mapping_style`
- `yield_extra_content_separately`

The default `content_mapping` covers:

- `id`
- `role`
- `reasoning`
- `delta`
- `tool_calls`
- `done`
- `usage`
- `finish_reason`
- `extra_delta.function_call`

If the user is integrating a non-standard compatible interface, they may need to adjust these mappings instead of changing the prompt layer.

## 7. Common Entry Points For Debugging

- URL or routing issues: start with `base_url`, `full_url`, `path_mapping`, and `model_type`
- auth issues: start with `api_key` and `auth`
- regional network or provider reachability issues: check `proxy`, then `timeout`, then `base_url`
- default request-body parameters: start with `request_options`
- per-request parameters: use `agent.options(...)`
