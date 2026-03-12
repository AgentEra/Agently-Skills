---
name: agently-model-setup
description: Use when the main task is model connection or request transport setup in Agently, including dotenv-loaded DeepSeek or other OpenAI-compatible endpoints, auth wiring, request options, and minimal connectivity verification.
---

# Agently Model Setup

Use this skill for provider wiring and transport setup before request logic is discussed.

## Native-First Rules

- use `Agently.set_settings(...)` or `agent.set_settings(...)`
- prefer dotenv-loaded environment variables for base URL, model, and auth
- keep provider setup outside business workflow logic

## Anti-Patterns

- do not hardcode provider-specific parsing into request code
- do not mix model setup with output parsing or workflow design

## Read Next

- `references/overview.md`
