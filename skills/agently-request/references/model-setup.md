# Agently Model Setup

Use this skill for provider wiring and transport setup before request logic is discussed.

## Native-First Rules

- default to async-first guidance when the configured model will be used from services, streaming paths, or concurrent workflows
- when settings live in files, prefer `Agently.load_settings("yaml_file", path, auto_load_env=True)`
- use `Agently.set_settings(...)` or `agent.set_settings(...)` for inline mappings or host-owned overrides
- when inline settings benefit from editor hints, use typed helper classes from
  `agently.types.settings` (for example `OpenAICompatibleSettings`) and pass
  the instance directly to `Agently.set_settings(...)`; treat the helper as a
  constructor/validator over the same durable dict settings contract
- prefer settings files with `${ENV.xxx}` placeholders for base URL, model, and auth
- put provider settings under the namespace read by the owning plugin. For `OpenAICompatible`, prefer `plugins.ModelRequester.OpenAICompatible.*`; for `AnthropicCompatible`, prefer `plugins.ModelRequester.AnthropicCompatible.*`
- call the matching settings loader with `auto_load_env=True` when the payload may rely on `.env`
- if the app must fail fast, validate required env names in the integration layer before calling Agently
- after loading, verify the effective provider activation, base URL, model, and auth presence instead of assuming the file shape was correct
- keep provider setup outside business workflow logic and prompt files
- when an Agent must switch among multiple configured models, use
  `agent.activate_model("ollama-qwen2.5")` for subsequent Agent-owned requests
  and `agent.create_request(model_key="deepseek-v4")` for one-off overrides.
  Prefer concrete model aliases such as `ollama-qwen2.5` and `deepseek-v4`,
  then map them through the current layered shape: `model_pool` maps the alias
  to a profile id, `model_profiles` stores provider/model/request settings, and
  `api_key_pools` stores credential pools, request-time selection policy, and
  optional provider-error failover policy. Keep legacy
  `key_pool_strategy` and `key_pool` examples only when explaining existing
  compatibility-line code.
- explain API key pool behavior precisely: keys are selected at request time by
  `api_key_pools.<pool>.selection` (`fixed`, `random`, `round_robin`,
  `least_used`; legacy top-level `strategy` remains accepted). Provider-error
  failover is opt-in through `api_key_pools.<pool>.failover`; without it,
  Agently does not try another key. The built-in requester plugins still retry
  transient transport disconnects with the same model, prompt, and output
  format according to `<Requester>.request_retry`. OpenAICompatible defaults to
  replaying after partial output; streaming consumers must process `$status` or
  clear plain-delta text on the
  `"<$retry>{reason}</$retry>"` marker before accepting replacement deltas.
  Failover handlers can inspect the provider error object and return `"try_next"`,
  `"retry_same"`, `"raise"`, a key id, a key entry dict, or a wrapper such as
  `{"key_id": "b"}` / `{"key_entry": context.keys[1]}`. Do not present
  `405` or `422` as universal credential failures; add them only when the
  specific provider uses those codes for key or quota problems.
- for custom `ModelRequester` plugins, keep public `generate_request_data`,
  `request_model`, and `broadcast_response` compatible. For non-trivial
  providers, follow the built-in package shape: a thin `plugin.py` coordinator
  plus private `modules/request_builder.py`, `credential.py`, `transport.py`,
  `handlers.py`, and `response_adapter.py`. Prefer adding optional
  `build_request_handlers()` that returns Agently core `AttemptHandlers` for
  request execution; annotate attempt stream messages with
  `AttemptStreamMessage` / `AttemptStreamGenerator` from `agently.types.data`.
  `broadcast_response(...)` must pass core-owned `("status", payload)` attempt
  records through unchanged; they are not provider wire payloads or model data.
  Official runtime events such as `model.requester.error`
  must be produced by core-owned coordinators such as ModelRequestRunner and
  AttemptRunner, not by plugin-level imports of core emitter helpers.
  Built-in HTTP error messages retain provider status/detail without appending
  the serialized model request; protected cold RuntimeEvent
  `payload.request_data` remains the full structured diagnostic carrier.
  Plugin-owned EventCenter messages are private diagnostics only and should not
  reuse official Agently event types.

## Anti-Patterns

- do not hardcode provider-specific parsing into request code
- do not bake secrets or environment-specific endpoints into committed Python code when settings plus env placeholders fit
- do not leave provider config at a root-level namespace that the active plugin will not read
- do not let sync-only samples dictate the architecture of async-capable services
- do not mix model setup with output parsing or workflow design
- do not use stage names such as `reason` as the main example for user-facing
  model switching; reserve those for internal stage routing docs. Use concrete
  switchable aliases such as `ollama-qwen2.5` and `deepseek-v4`.

## Read Next

- `references/overview.md`
