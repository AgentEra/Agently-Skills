---
name: agently-triggerflow-orchestration
description: Use only when the main task is low-level TriggerFlow primitives, execution entrypoints, contracts, or result semantics, such as `to(...)`, `when(...)`, `if_condition(...)`, `match(...)`, `create_execution()`, `start()/async_start()`, or `set_contract(...)`.
---

# Agently TriggerFlow Orchestration

This skill is the low-level primitive and runtime leaf inside the TriggerFlow domain. It focuses on chunks, signals, event routing, execution entrypoints, contracts, and result ownership. It does not decide whether the user should use TriggerFlow in the first place, and it does not cover reusable workflow-pattern selection, state-placement design, runtime-resource boundaries, sub-flow-specific parent-child boundaries, interrupt handling, runtime stream, flow-config export/import, Mermaid generation, or execution-state persistence and restore.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- understanding TriggerFlow as a signal-driven orchestrator
- `chunk`, `to(...)`, `when(...)`, `if_condition(...)`, `match(...)`, `end()`, and `set_result(...)`
- `create_execution()`, `async_start_execution()`, `async_start()`, and `start()`
- `set_contract(...)` and `get_contract()`
- runtime validation of initial input, user stream items, and final result

Do not use this skill for:

- `pause_for(...)`, `continue_with(...)`, or pending-interrupt handling
- `get_runtime_stream()`, `get_async_runtime_stream()`, or runtime-stream lifecycle
- flow config export/import, blueprint reuse, or Mermaid output
- execution `save()` / `load()` and resume-after-restart state handling
- `runtime_data`, `flow_data`, runtime resources, or restart-safe state placement as the main problem
- `to_sub_flow(...)`, `capture`, `write_back`, or child-flow isolation as the main problem
- model provider setup, auth, proxy, or timeout configuration
- model requests inside chunks or several model calls inside one workflow
- flow config export/import, blueprint copy, or Mermaid inspection
- prompt-template file management
- structured output parsing outside the TriggerFlow orchestration boundary
- choosing between `batch(...)`, `for_each(...)`, `collect(...)`, `side_branch(...)`, safe loops, evaluator-optimizer, ReAct loops, or approval-gate workflow patterns

## Workflow

1. Start with [references/mental-model-and-async.md](references/mental-model-and-async.md) to choose the correct execution model. Default to async APIs whenever the runtime can support them.
2. If the task is about typed input, stream, or result boundaries, read [references/contract-and-runtime-types.md](references/contract-and-runtime-types.md).
3. If the task is about building the first flow or understanding basic routing/result mechanics, read [references/orchestration-patterns.md](references/orchestration-patterns.md).
4. If the task is really about common workflow shapes such as router, fan-out, `for_each`, safe loops, or approval gates, switch to `agently-triggerflow-patterns`.
5. If the task is about state placement, resource injection, or restart-safe state design, switch to `agently-triggerflow-state-and-resources`.
6. If the task is about parent-child nested workflows, `to_sub_flow(...)`, `capture`, or `write_back`, switch to `agently-triggerflow-subflows`.
7. If the task is about model requests inside flow steps, switch to `agently-triggerflow-model-integration`.
8. If the task is about flow config export/import or Mermaid, switch to `agently-triggerflow-config`.
9. If the task is about human-in-the-loop waiting or runtime stream, switch to `agently-triggerflow-interrupts-and-stream`.
10. If behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

TriggerFlow is not just a linear chain helper.

- a flow reacts to signals
- `START` is only the default entry event
- chunks can emit more events, mutate execution state, and mutate flow state
- multiple executions of the same flow may run concurrently

Agently guidance for this skill should be async-first:

- prefer `async_start()`, `async_start_execution()`, and `async_emit()`
- use sync wrappers such as `start()` only for sync-only scripts, notebooks, or quick demos

Why:

- TriggerFlow internals are async
- concurrent executions, model streaming, and interrupt handling fit naturally into async runtimes
- sync entrypoints are compatibility bridges, not the preferred integration layer

## Selection Rules

- one linear async workflow -> `to(...).end()`
- signal gate that waits for event or state -> `when(...)`
- conditional routing by boolean or matched value -> `if_condition(...)` or `match(...)`
- event-driven re-entry inside one execution -> `emit(...)` or `async_emit(...)`
- explicit final-result ownership in event-heavy flows -> `set_result(...)`
- the flow should validate initial input, user stream items, or final result against a type contract -> `set_contract(...)`
- reusable workflow shape using `batch(...)`, `for_each(...)`, `collect(...)`, `side_branch(...)`, safe loops, or approval gates -> `agently-triggerflow-patterns`
- state placement or runtime-resource boundary -> `agently-triggerflow-state-and-resources`
- nested child workflow with explicit capture / write_back -> `agently-triggerflow-subflows`
- model requests inside flow logic -> `agently-triggerflow-model-integration`
- definition export/import or Mermaid -> `agently-triggerflow-config`
- human approval or live runtime streaming -> use `agently-triggerflow-interrupts-and-stream`

## Important Boundaries

- `end()` or `set_result(...)` decides how a final result becomes available to `get_result()` / `async_get_result()`
- `set_contract(...)` validates initial input, user-defined stream items, and final result at runtime
- `get_contract()` returns the live runtime contract spec, not just exported metadata
- system interrupt events can still appear in runtime stream even when a user stream contract is set
- workflow patterns, state placement, sub flows, interrupt handling, and runtime stream are separate skills, not part of this one
- config export/import and execution save/load are separate skills, not part of this one

## References

- `references/source-map.md`
- `references/mental-model-and-async.md`
- `references/contract-and-runtime-types.md`
- `references/orchestration-patterns.md`
- `references/troubleshooting.md`
