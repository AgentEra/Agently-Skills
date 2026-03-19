---
name: agently-output-control
description: Use when the user wants stable structured fields, required keys, reliable machine-readable sections, or downstream-consumable output from one model request, including prompt-config-owned output contracts, `.output(...)`, field ordering, `ensure_keys`, and structured streaming.
---

# Agently Output Control

Use this skill when the question is what shape the model should return and how that shape should stay reliable.

The user does not need to say `.output(...)` or `ensure_keys`. Requests for stable JSON-like fields, structured reports, or machine-readable sections should route here.

## Native-First Rules

- default to async-first response consumption when structured output will be streamed, reused, or served over an async boundary
- prefer prompt-config-owned output contracts such as `.request.output` when the schema is stable and shared across a request family
- prefer `.output(...)` for machine-readable results when the schema is dynamic, exploratory, or easier to keep close to code
- prefer `ensure_keys` when required fields must be enforced
- keep output schema explicit when downstream systems, workflow branches, or later model steps consume the result

## Anti-Patterns

- do not handwrite JSON post-processors when `.output(...)` already owns the contract
- do not rebuild a stable shared schema in Python if prompt config can own it once
- do not build custom retry loops for missing keys before checking `ensure_keys`
- do not default to sync-only result handling when the caller is already async-capable

## Read Next

- `references/overview.md`
