---
name: agently-skills-catalog
description: Central catalog and documentation for Agently Skills V2. Use when working with Agently skill installation, routing, and installed-skill usage guidance.
---

# Agently Skills Catalog

This package publishes the Agently Skills V2 catalog under `skills/`.

Use this file as installation-time guidance after the skills are added into another project or agent environment.

## Usage Priorities

- Route unresolved product, assistant, and workflow requests through `agently-playbook` first.
- Prefer Agently-native capabilities before custom output parsers, retry loops, or orchestration layers.
- Default to async-first guidance for services, streaming, TriggerFlow, and concurrent execution. Treat sync APIs as wrappers for scripts, REPL use, or compatibility bridges unless there is a clear reason not to.
- Keep public skill boundaries capability-first and mutually exclusive.
- Treat multi-agent, judge, and review flows as scenario recipes unless they need a dedicated framework surface.

## Project Defaults

- Prefer separating `settings/`, `prompts/`, `services/`, `domain/` or `schemas/`, `workflow/`, `tools/`, and `tests/` when the project is more than a tiny demo.
- Keep stable shared prompt and output contracts in prompt config rather than scattering them across Python helpers.
- Keep provider settings under the namespace actually read by the active plugin. For `OpenAICompatible`, prefer `plugins.ModelRequester.OpenAICompatible.*`.
- Prefer `Agently.load_settings("yaml_file", path, auto_load_env=True)` for file-backed settings. Use `Agently.set_settings(...)` for inline overrides.

## Skill Routing Reminders

- `agently-playbook`: unresolved owner layer, project shape, or broad product request
- `agently-model-setup`: provider wiring, env placeholders, model settings, namespace placement, and connectivity checks
- `agently-prompt-management`: prompt config, mappings, reusable request contracts, and prompt-side output contracts
- `agently-output-control`: structured output shape, required keys, reliability, and structured streaming
- `agently-model-response`: response reuse, async getters, metadata, and stream consumption
- `agently-triggerflow`: explicit orchestration, branching, concurrency, runtime stream, and workflow-owned business events

## Anti-Patterns

- Do not treat sync sample code as the default architecture for async-capable services.
- Do not expose raw model parser paths directly to the UI when the workflow can translate them into stable business events.
- Do not keep provider auth, model name, or base URL in ad hoc Python literals when settings plus `${ENV.xxx}` placeholders fit.
