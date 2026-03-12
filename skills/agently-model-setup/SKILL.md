---
name: agently-model-setup
description: Use only when the main task is model connection or request-transport setup, such as local Ollama, OpenAI-compatible endpoints, generator-model and judge-model wiring, URL and auth configuration, request options, or minimal connectivity verification for Agently requests.
---

# Agently Model Setup

This skill is the direct leaf for model connection and request-transport setup after the user already knows the work should stay on the Agently request side or workflow side. It does not choose between one request, tools, MCP, session continuity, or TriggerFlow, and it does not cover structured output design, scoring logic, streaming result consumption details, or embedding workflows.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- Included: Chat LLM, Completions LLM, VLM
- text chat, standard generation, completions, judge-model review, image understanding, visual Q&A, and OCR model setup
- global model configuration with `Agently.set_settings("OpenAICompatible", {...})`
- per-agent overrides with `agent.set_settings("OpenAICompatible", {...})`
- endpoint, model, auth, and network-client setup: `base_url`, `full_url`, `model`, `auth`, `api_key`, `headers`, `proxy`, `timeout`, `client_options`
- extra request parameters through `request_options` and `agent.options({...})`
- separate generator-model and validator-model wiring
- VLM-style attachment input through `attachment()`
- a minimal runnable verification step to confirm URL, model name, auth, and basic response behavior
- Excluded: Embeddings (handled by a separate skill)

Do not use this skill for:

- deciding whether the solution should stay one request or escalate to tools, MCP, RAG, session continuity, multi-agent design, or TriggerFlow
- prompt-slot composition, placeholder mappings, `chat_history`, or attachment design as the main problem
- `.output(...)`, `ensure_keys`, structured streaming, or result parsing as the main problem
- embeddings workflows

## Workflow

1. Start from the user scenario: plain text generation, a traditional completions endpoint, or image understanding / visual Q&A / OCR.
2. Read [references/model-types.md](references/model-types.md) to map that scenario to the Agently implementation. For VLM scenarios, the Agently pattern is `chat + attachment()`.
3. Read [references/openai-compatible-config.md](references/openai-compatible-config.md) to decide which fields belong at which configuration layer.
4. If the user is asking about a specific provider, start from the closest recipe in [references/provider-recipes.md](references/provider-recipes.md).
5. If the question is about temperature, max tokens, tools, thinking, or other provider-specific parameters, read [references/options-and-extra-params.md](references/options-and-extra-params.md).
6. After configuration, run a minimal verification request using [references/verification.md](references/verification.md).
7. If it still fails, use [references/troubleshooting.md](references/troubleshooting.md).

## Configuration Layers

Agently model setup usually has three layers:

- Global setup with `Agently.set_settings()`
- Per-agent override with `agent.set_settings()`
- Per-request override with `agent.options(...)`

Guidelines:

- put global defaults in `Agently.set_settings(...)`
- put agent-specific overrides in `agent.set_settings(...)`
- put per-request request-body overrides in `agent.options(...)`
- put network proxy settings in `Agently.set_settings(...)` or `agent.set_settings(...)`, not in `agent.options(...)`
- do not promote one-off request parameters into global defaults, and do not put network or routing fields into `agent.options(...)`

## Primary Setup Path

The default path is always `OpenAICompatible`:

- Primary adapter: `OpenAICompatible`
- Provider examples will be used as standard recipes, not separate setup systems

Why:

- `OpenAICompatible`, `OpenAI`, and `OAIClient` are aliases of the same requester plugin in v4
- model type selection, request-body shape, stream mode, URL assembly, auth, and response mapping are handled by this single requester
- OpenAI, Claude, DeepSeek, Gemini, Ollama, and most self-hosted compatible endpoints should be understood through this path first
- if a user only says “help me connect this model service”, default to the OpenAI-compatible path before inventing a new requester

## Provider Recipes

The standard recipes should cover:

- OpenAI
- Claude
- DeepSeek
- Gemini
- Ollama
- OpenAI-compatible or self-hosted endpoints

These recipes are for fast setup and for aligning the user’s mental model. They do not imply that each provider has a separate Agently configuration system.

## Extra Parameters

This section follows the current requester behavior:

- `OpenAICompatible` supported config fields
- `.options()` supported extra parameters
- Common configuration scenarios

Key rules:

- persistent default request-body parameters -> `request_options`
- per-request temporary parameters -> `agent.options({...})`
- `model` and `stream` are not normal extra parameters; the plugin layer writes the final values
- current request assembly reads plugin-root `options` as a backward-compatible fallback, then plugin-level `request_options`, then prompt-level `options`
- prefer `request_options` in new guidance even though plugin-root `options` still works as a compatibility path

## Verification

After configuration, a minimal verification request is recommended:

- Verification is recommended, not mandatory
- The validation should use a minimal runnable request
- Chat / Completions: send a one-line prompt and confirm that it returns reliably
- VLM: use an image-understanding prompt with one text item and one `image_url`
- when `debug` or `runtime.show_model_logs` is enabled, check `request_url`, `request_options`, and `stream` first
- in practice, enable `debug` or `runtime.show_model_logs` early rather than only after several failed guesses

## Model Tiering And Quality Strategy

Model setup should reflect the planned quality path:

- stronger and higher-cost models usually need fewer explicit review loops
- local or lower-cost models can still reach good quality, but they often benefit from bounded judge, revise, or reflection stages
- if those extra stages become explicit parts of the design, let TriggerFlow own the orchestration instead of hiding the logic in ad hoc request chaining

For the final effect validation of a real Agently application, service, or module, prefer real model runs when possible:

1. local model
2. lower-cost online model
3. authorized paid model
4. no-model fallback only when real-model validation is not available

## References

- `references/source-map.md`
- `references/model-types.md`
- `references/openai-compatible-config.md`
- `references/provider-recipes.md`
- `references/options-and-extra-params.md`
- `references/verification.md`
- `references/troubleshooting.md`

## Scripts

`scripts/resolve-repo.sh` can locate the Agently repository root from the current directory or from a provided path.
