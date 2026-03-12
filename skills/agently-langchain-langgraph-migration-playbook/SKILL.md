---
name: agently-langchain-langgraph-migration-playbook
description: Use when migrating an existing LangChain or LangGraph system into Agently and it is still unresolved whether the source belongs to LangChain-side agent migration or LangGraph-side orchestration migration.
---

# Agently LangChain LangGraph Migration Playbook

This skill is the migration-router entry point for work from LangChain or LangGraph into Agently. Use it only when the request starts from an existing LangChain or LangGraph codebase, concept, or architecture and the migration path is still unresolved. It helps choose the right migration path and the right Agently skill combination. It does not replace the narrower migration skills themselves.

Prerequisite: Agently `>= 4.0.8.5`.

## When To Use This Skill

Use this skill for:

- an existing LangChain or LangGraph system where the main migration path is still unclear
- requests where it is still unresolved whether the source design is mainly LangChain-side or LangGraph-side
- deciding whether the migration target should stay one request, become a multi-agent design, or become TriggerFlow orchestration
- choosing the correct migration skill and implementation order
- identifying which parts can map directly and which parts require redesign

## When Not To Use This Skill

- direct migration work where the source side is already known to be LangChain agent migration
- direct migration work where the source side is already known to be LangGraph orchestration migration
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
- once the source side and target shape are already clear, stop using this router and switch to the narrower migration skill

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
