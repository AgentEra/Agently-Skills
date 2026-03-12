---
name: agently-output-control
description: Use when the main task is the output contract of one Agently request, including `.output(...)`, field ordering, required keys, `ensure_keys`, and structured output reliability.
---

# Agently Output Control

Use this skill when the question is what shape the model should return and how that shape should stay reliable.

## Native-First Rules

- prefer `.output(...)` for machine-readable results
- prefer `ensure_keys` when required fields must be enforced
- keep output schema explicit when downstream systems or later model steps consume the result

## Anti-Patterns

- do not handwrite JSON post-processors when `.output(...)` already owns the contract
- do not build custom retry loops for missing keys before checking `ensure_keys`

## Read Next

- `references/overview.md`
