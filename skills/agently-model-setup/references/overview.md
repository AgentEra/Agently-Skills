# Overview

This skill owns provider setup, dotenv loading, `${ENV.xxx}`-backed settings, `auto_load_env=True`, `OpenAICompatible` configuration, and minimal connectivity verification.

Use it when:

- model settings live in `SETTINGS.yaml` or another config file instead of Python literals
- provider base URL, model name, or auth should come from `${ENV.xxx}` placeholders
- the app should load `.env`, validate required env names, and then hand the same settings payload to Agently

Keep this layer separate from prompt contracts and workflow code.
