---
name: agently-prompt-config-files
description: Use only when the main task is externalized YAML or JSON prompt-template config in Agently, such as loading prompt config from files or strings, selecting by key path, applying mappings, executing `.alias`, or exporting prompt state back to reusable config.
---

# Agently Prompt Config Files

This skill is the direct leaf for prompt-template config externalization after the request path is already known. It focuses on prompt templates as data assets: loading prompt config from files or strings, routing config into agent/request prompt layers, applying mappings, selecting nested prompt packs, executing `.alias`, and exporting current prompt state back to YAML or JSON. It does not choose between direct Python prompt composition, session restore, or TriggerFlow definition export, and it does not cover provider setup or response consumption.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- `load_yaml_prompt(...)` and `load_json_prompt(...)`
- `get_yaml_prompt(...)` and `get_json_prompt(...)`
- `.agent`, `.request`, and `.alias`
- top-level `$key` agent shorthand and top-level request-key shorthand
- `mappings` for placeholder substitution in config keys and values
- `prompt_key_path` for selecting one prompt config from a larger YAML or JSON document
- prompt-template roundtrip between code-built prompt state and exported config text
- externalizing prompt structure out of business code

Do not use this skill for:

- regular prompt composition written directly in Python code
- session export / restore, session ids, or session-backed memory
- TriggerFlow flow config, blueprint export, or execution-state restore
- provider setup, auth, proxy, or request transport configuration
- `.output(...)` response parsing or streaming-consumption decisions

## Workflow

1. If the task is about how a prompt config file is structured, read [references/structure-and-routing.md](references/structure-and-routing.md).
2. If the task is about file-vs-string loading, mappings, JSON5 behavior, or `prompt_key_path`, read [references/loading-mappings-and-key-paths.md](references/loading-mappings-and-key-paths.md).
3. If the task is about `.alias`, exporting config, or roundtripping prompt state, read [references/alias-and-roundtrip.md](references/alias-and-roundtrip.md).
4. If the behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

Prompt config in Agently is a serialized form of prompt state, not a new prompt system.

- `.agent` maps to persistent agent prompt state
- `.request` maps to per-request prompt state
- top-level `$key` is shorthand for writing into agent prompt state
- top-level ordinary keys are shorthand for writing into request prompt state
- `.alias` is an imperative hook that executes agent methods during load

That means this feature is best used when prompt structure should live outside business code, be versioned as data, or be shared across services and environments.

## Selection Rules

- prompt template should live in YAML or JSON instead of Python -> use prompt config files
- one config file contains multiple reusable prompt packs -> use `prompt_key_path`
- placeholders should be filled at load time -> use `mappings`
- prompt state should be exported and restored elsewhere -> use `get_yaml_prompt()` / `get_json_prompt()`
- config should drive simple prompt-building methods -> use `.alias`
- long-lived conversation memory or state snapshot -> use `agently-session-memo`, not this skill
- flow-definition export -> use `agently-triggerflow-config`, not this skill
- TriggerFlow runtime restore -> use `agently-triggerflow-execution-state`, not this skill

## Key Limits

- mappings are applied when prompt keys and values are written into prompt state
- `.alias` arguments are executed as written; they do not receive the same load-time `${...}` mapping substitution
- exported prompt config serializes current `.agent` and `.request` state
- export does not preserve `.alias`, comments, `prompt_key_path`, or the original unresolved template text

## References

- `references/source-map.md`
- `references/structure-and-routing.md`
- `references/loading-mappings-and-key-paths.md`
- `references/alias-and-roundtrip.md`
- `references/troubleshooting.md`
