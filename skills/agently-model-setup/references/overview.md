# Overview

This skill owns provider setup, dotenv loading, `${ENV.xxx}`-backed settings, `auto_load_env=True`, `OpenAICompatible` configuration, and minimal connectivity verification.

Use it when:

- model settings live in `SETTINGS.yaml` or another config file instead of Python literals
- provider base URL, model name, or auth should come from `${ENV.xxx}` placeholders
- the app should load `.env`, validate required env names, and then hand the same settings payload to Agently
- provider configuration must sit under the namespace actually read by the active plugin
- the project needs a quick post-load check that activation, base URL, model, and auth are really effective

Prefer `Agently.load_settings("yaml_file", path, auto_load_env=True)` for file-backed configuration, keep this layer separate from prompt contracts and workflow code, and default to async-first guidance when the configured model will live inside services or workflows.
