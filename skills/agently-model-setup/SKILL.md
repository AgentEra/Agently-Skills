---
name: agently-model-setup
description: Use when the request is already narrowed to wiring a model endpoint, env vars, settings-file-based model config, `${ENV.xxx}` placeholders, `auto_load_env=True`, or connectivity check for a model-powered feature, including local Ollama, dotenv-loaded DeepSeek or other OpenAI-compatible settings, plugin namespace placement, auth, request options, and minimal verification.
---

# Agently Model Setup

Use this skill for provider wiring and transport setup before request logic is discussed.

## Native-First Rules

- default to async-first guidance when the configured model will be used from services, streaming paths, or concurrent workflows
- when settings live in files, prefer `Agently.load_settings("yaml_file", path, auto_load_env=True)`
- use `Agently.set_settings(...)` or `agent.set_settings(...)` for inline mappings or host-owned overrides
- prefer settings files with `${ENV.xxx}` placeholders for base URL, model, and auth
- put provider settings under the namespace read by the owning plugin. For `OpenAICompatible`, prefer `plugins.ModelRequester.OpenAICompatible.*`
- call the matching settings loader with `auto_load_env=True` when the payload may rely on `.env`
- if the app must fail fast, validate required env names in the integration layer before calling Agently
- after loading, verify the effective provider activation, base URL, model, and auth presence instead of assuming the file shape was correct
- keep provider setup outside business workflow logic and prompt files

## Anti-Patterns

- do not hardcode provider-specific parsing into request code
- do not bake secrets or environment-specific endpoints into committed Python code when settings plus env placeholders fit
- do not leave provider config at a root-level namespace that the active plugin will not read
- do not let sync-only samples dictate the architecture of async-capable services
- do not mix model setup with output parsing or workflow design

## Read Next

- `references/overview.md`
