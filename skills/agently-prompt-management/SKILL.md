---
name: agently-prompt-management
description: Use when the main task is request-side prompt composition in Agently, including input slots, instruct/info layering, prompt config, mappings, reusable prompt templates, and prompt-state organization.
---

# Agently Prompt Management

Use this skill when the core problem is how prompt state should be structured before one request or request family runs.

## Native-First Rules

- prefer `input(...)`, `instruct(...)`, `info(...)`, and `output(...)` over concatenated prompt strings
- move reusable prompt structure into prompt config instead of ad hoc literals
- keep prompt composition separate from transport and orchestration

## Anti-Patterns

- do not flatten business context into one opaque string unless the task is trivial
- do not use prompt config files as a substitute for workflow state

## Read Next

- `references/overview.md`
