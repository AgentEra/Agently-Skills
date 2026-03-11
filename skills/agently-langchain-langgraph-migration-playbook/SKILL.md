---
name: agently-langchain-langgraph-migration-playbook
description: Use when migrating a LangChain or LangGraph codebase, mental model, or architecture into Agently, especially to decide whether the source design maps to one-request Agently skills, multi-agent patterns, or TriggerFlow, and to choose the correct migration skill combination and implementation order.
---

# Agently LangChain LangGraph Migration Playbook

This skill is the top-level routing entry point for migration work from LangChain or LangGraph into Agently. Use it when the request starts from an existing LangChain or LangGraph codebase, concept, or architecture rather than an Agently API. It helps choose the right migration path and the right Agently skill combination. It does not replace the implementation skills themselves.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- deciding whether the source design is mainly LangChain-side or LangGraph-side
- deciding whether the migration target should stay one request, become a multi-agent design, or become TriggerFlow orchestration
- choosing the correct migration skill and implementation order
- identifying which parts can map directly and which parts require redesign

Do not use this skill for:

- direct Agently API implementation details
- one isolated LangChain or LangGraph feature with no migration-design question
- general business design that is not starting from LangChain or LangGraph

## Workflow

1. Start with [references/scenario-router.md](references/scenario-router.md) to classify the source system.
2. Read [references/migration-principles.md](references/migration-principles.md) to set the right migration strategy.
3. Read [references/current-skill-map.md](references/current-skill-map.md) to choose the migration skill or supporting Agently skills.
4. Switch to `agently-langchain-to-agently` or `agently-langgraph-to-triggerflow` and do the actual migration work there.

## Routing Rules

- LangChain `create_agent`, tools, structured output, short-term memory, middleware, retrieval, or service exposure -> `agently-langchain-to-agently`
- LangGraph `StateGraph`, node/edge/state, interrupt, persistence, streaming, subgraphs, or durable execution -> `agently-langgraph-to-triggerflow`
- LangChain agent built on LangGraph and the real complexity lives in workflow orchestration -> start with `agently-langgraph-to-triggerflow`, then add `agently-langchain-to-agently` for agent internals
- source project should be simplified during migration rather than translated literally -> use this playbook first, then route to the narrower migration skill

## Important Boundaries

- migration is not a line-by-line import rewrite
- some LangChain or LangGraph abstractions map into several Agently skills rather than one API
- some source patterns should collapse into simpler Agently designs instead of being copied literally
- start from capability translation, then rewrite implementation

## References

- `references/source-map.md`
- `references/scenario-router.md`
- `references/migration-principles.md`
- `references/current-skill-map.md`
