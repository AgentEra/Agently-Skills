---
name: agently-langgraph-to-triggerflow
description: Use when the main task is directly migrating LangGraph orchestration surfaces into Agently TriggerFlow, including graph stages, routing, checkpoints, interrupts, persistence, streaming, and subgraph boundaries.
---

# LangGraph To TriggerFlow

Use this skill after migration ownership is already confirmed to be LangGraph orchestration work.

## Native-First Rules

- map graph orchestration concerns into TriggerFlow rather than rebuilding a graph layer
- preserve explicit orchestration stages, state, and resume behavior
- combine with request-side response skills only when a workflow step needs them

## Anti-Patterns

- do not flatten orchestration semantics into one large request
- do not rebuild LangGraph primitives outside TriggerFlow first

## Read Next

- `references/overview.md`
