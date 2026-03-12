---
name: agently-langgraph-to-triggerflow
description: Use when directly migrating LangGraph orchestration surfaces into Agently TriggerFlow after the migration is already known to be workflow-orchestration-first rather than LangChain agent migration, such as `StateGraph`, nodes and edges, `Send`, `Command`, checkpoints, interrupts, persistence, streaming, or subgraphs.
---

# Agently LangGraph To TriggerFlow

This skill is the direct migration leaf for LangGraph orchestration concepts into Agently TriggerFlow. Use it when the source problem is already known to be workflow-orchestration-first rather than LangChain agent migration. It focuses on `StateGraph`, graph state, interrupts, persistence, streaming, subgraphs, and durable execution. It does not cover high-level LangChain agent migration unless that agent layer is secondary to the orchestration problem.

Prerequisite: Agently `>= 4.0.8.5`.

## When To Use This Skill

Use this skill for:

- direct migration of a known LangGraph orchestration design into TriggerFlow capabilities
- `StateGraph`
- nodes and edges
- `Send` or dynamic worker fan-out
- `Command`-style resume or control flow
- graph state
- interrupts
- persistence or checkpoints
- streaming
- subgraphs
- durable execution
- LangGraph-based human-in-the-loop behavior

## When Not To Use This Skill

- unresolved migration-entry work where you still need to decide between LangChain-side and LangGraph-side migration
- one-request agent migration as the main problem
- direct model-provider setup as the main problem
- non-migration TriggerFlow implementation work that already starts from Agently

## Workflow

1. Start with [references/concept-map.md](references/concept-map.md) to translate LangGraph orchestration concepts into the current TriggerFlow skill tree.
2. Read [references/common-migration-recipes.md](references/common-migration-recipes.md) when the source graph resembles a standard LangGraph production shape.
3. Read [references/non-1to1-differences.md](references/non-1to1-differences.md) when the migration should change design rather than mimic syntax.
4. Read [references/current-skill-map.md](references/current-skill-map.md) to choose the target TriggerFlow skill combination.
5. If the source problem is actually high-level LangChain agent behavior, switch to `agently-langchain-to-agently`.
6. If behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

LangGraph and TriggerFlow are both orchestration layers, but they are not shaped the same way.

LangGraph emphasizes:

- graph state
- nodes and edges
- interrupts plus checkpoints
- thread and checkpoint persistence

TriggerFlow emphasizes:

- signals and handlers
- runtime data and flow data
- explicit runtime stream
- config plus execution-state restore

So the migration target is usually:

- concept translation
- state-boundary redesign
- persistence-boundary redesign

not a syntax-by-syntax rewrite.

## Selection Rules

- `StateGraph`, core node and edge wiring -> `agently-triggerflow-orchestration`
- routers, `Send`-like fan-out, loops, evaluator-reviser, or handoff-like workflow shapes -> `agently-triggerflow-patterns`
- graph state, shared state, or dependency boundaries -> `agently-triggerflow-state-and-resources`
- subgraphs or isolated child workflow boundaries -> `agently-triggerflow-subflows`
- streaming model output inside the graph -> `agently-triggerflow-model-integration`
- definition export/import or graph visualization -> `agently-triggerflow-config`
- checkpoint-like restore of a running instance -> `agently-triggerflow-execution-state`
- interrupts, `Command`-style resume, and human-in-the-loop continuation -> `agently-triggerflow-interrupts-and-stream`
- the migration still needs a top-level LangChain-vs-LangGraph routing decision -> `agently-langchain-langgraph-migration-playbook`

## Important Boundaries

- LangGraph threads and checkpointers do not map literally to one TriggerFlow API
- LangGraph `Send` and `Command` do not map literally to one TriggerFlow primitive; keep the worker pattern or resume intent, then redesign the flow
- durable restore in Agently usually becomes `config + execution-state`, and sometimes also `session-memo`
- graph state does not map literally to one TriggerFlow state container; choose between `runtime_data`, `flow_data`, resources, and external storage
- streaming modes do not map literally one-to-one; route model streaming and runtime stream separately

## References

- `references/source-map.md`
- `references/concept-map.md`
- `references/common-migration-recipes.md`
- `references/non-1to1-differences.md`
- `references/current-skill-map.md`
- `references/troubleshooting.md`
