---
name: agently-triggerflow-state-and-resources
description: Use when designing TriggerFlow state placement and dependency boundaries, including `runtime_data` vs `flow_data`, flow-level vs execution-level runtime resources, `data.set_resource(...)`, save/load resource-key boundaries, sub-flow state handoff, or restart-safe state and resource design.
---

# Agently TriggerFlow State And Resources

This skill covers TriggerFlow runtime state placement and runtime-only dependency design in Agently. It focuses on `runtime_data` versus `flow_data`, flow-level versus execution-level runtime resources, execution-scoped `data.set_resource(...)`, what survives execution save/load, what does not, and how state or resources cross sub-flow boundaries. It does not cover generic branching patterns, model requests, interrupts as a standalone topic, flow-config export/import, or the mechanics of execution restore.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- choosing between `runtime_data` / `data.state` and `flow_data` / `data.flow_state`
- deciding whether a dependency should be a flow-level or execution-level runtime resource
- `data.set_resource(...)` and execution-scoped resource injection
- understanding what execution save/load captures and what it does not
- understanding what flow-config export/import keeps and what it does not
- restart-safe state and resource design
- deciding how state and resources should cross a sub-flow boundary

Do not use this skill for:

- ordinary flow structure such as `when(...)`, `batch(...)`, `for_each(...)`, or `collect(...)`
- `to_sub_flow(...)`, `capture`, and `write_back` as the main topic
- model-provider setup or model-call design
- `pause_for(...)`, `continue_with(...)`, or runtime-stream lifecycle
- the mechanics of `execution.save()` / `execution.load()` and resume-after-restore

## Workflow

1. Start with [references/state-placement.md](references/state-placement.md) to choose between `runtime_data` and `flow_data`.
2. If the task is about resource injection, overrides, or `data.set_resource(...)`, read [references/resources-and-overrides.md](references/resources-and-overrides.md).
3. If the task is about restart-safe design, save/load boundaries, or what must be re-injected, read [references/persistence-boundaries.md](references/persistence-boundaries.md).
4. If the task is about nested parent-child state or resource handoff, read [references/subflow-boundaries.md](references/subflow-boundaries.md).
5. If the task is about actual save/load and resume mechanics, switch to `agently-triggerflow-execution-state`.
6. If behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

TriggerFlow has three different runtime surfaces:

- `runtime_data` for one execution only
- `flow_data` for shared flow-level state
- runtime resources for non-serializable dependencies

Choosing the wrong surface causes most real-world TriggerFlow state bugs:

- request-local values accidentally leak across executions
- shared flags accidentally disappear because they were stored in execution state
- restored executions fail because runtime resources were never re-injected

## Selection Rules

- request-local context, per-run intermediate values, or one execution's working state -> `runtime_data`
- shared flags or values that later executions of the same flow should see -> `flow_data`
- logger, client, service object, renderer, or helper callable -> runtime resources
- one execution should override a flow default resource -> execution-level `runtime_resources=...`
- a handler creates a temporary resource for the current run only -> `data.set_resource(...)`
- a saved execution should resume after restart -> combine with `agently-triggerflow-execution-state`
- state or resources must cross parent-child flow boundaries -> combine with `agently-triggerflow-subflows`
- long-lived memory outside the TriggerFlow runtime itself -> use external persistence or `agently-session-memo`, not `flow_data`

## Important Boundaries

- `runtime_data` is execution-scoped and should not be used for cross-execution sharing
- `flow_data` is shared on one flow object and may be visible to later executions of the same flow
- runtime resources are not serialized into execution state or flow config; only resource-key expectations survive
- flow config export/import preserves the need for resources, not the resource objects themselves
- sub flows only receive the state or resources that are explicitly captured into them

## References

- `references/source-map.md`
- `references/state-placement.md`
- `references/resources-and-overrides.md`
- `references/persistence-boundaries.md`
- `references/subflow-boundaries.md`
- `references/troubleshooting.md`
