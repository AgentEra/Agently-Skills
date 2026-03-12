---
name: agently-triggerflow-subflows
description: Use only when the main task is an isolated TriggerFlow child-flow boundary through `to_sub_flow(...)`, `capture`, `write_back`, child-flow state isolation, or parent-child runtime-stream bridging.
---

# Agently TriggerFlow Subflows

This skill is the child-flow-boundary leaf inside the TriggerFlow domain. It focuses on `to_sub_flow(...)`, parent-child data handoff through `capture` and `write_back`, isolated child state, resource handoff, runtime-stream bridging, and the current sub-flow limits. It does not decide whether the user should use TriggerFlow in the first place, and it does not cover generic branching or batching, model-request details, interrupt handling as a standalone topic, flow-config export/import, or execution-state persistence.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- `to_sub_flow(...)`
- deciding when a child workflow should be isolated instead of inlined
- `capture` from parent `value`, `runtime_data`, `flow_data`, and resources
- `write_back` into parent `value`, `runtime_data`, and `flow_data`
- child-flow state isolation from the parent and from the reusable child template
- parent runtime-stream visibility for child stream events
- current sub-flow limits such as child pause/resume support

Do not use this skill for:

- ordinary linear flow construction, branching, `batch(...)`, `for_each(...)`, or `collect(...)`
- provider setup or model configuration
- model requests inside chunks as the main problem
- explicit interrupt design outside the sub-flow boundary
- flow config export/import or Mermaid generation
- execution save/load or resume-after-restart persistence

## Workflow

1. Start with [references/subflow-boundaries.md](references/subflow-boundaries.md) to decide whether the workflow should stay inline or become an isolated child flow.
2. If the task is about parent-child data handoff, read [references/capture-and-write-back.md](references/capture-and-write-back.md).
3. If the task is about child state isolation, stream propagation, or current limits, read [references/isolation-stream-and-limits.md](references/isolation-stream-and-limits.md).
4. If the task is about exporting or restoring a flow definition that already contains sub flows, switch to `agently-triggerflow-config`.
5. If the task is about child waiting, external re-entry, or human approval, switch to `agently-triggerflow-interrupts-and-stream`.
6. If behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

A sub flow is a function-like child workflow boundary inside TriggerFlow.

- the parent decides what to pass in through `capture`
- the child runs as its own isolated execution
- the parent only gets changes back through explicit `write_back`

Use a sub flow when nested workflow structure and explicit parent-child boundaries matter more than keeping everything inline in one flow.

## Selection Rules

- one nested workflow should behave like a reusable isolated unit -> `to_sub_flow(...)`
- parent input or state must be copied into the child explicitly -> `capture`
- child result or child-derived state must be written back explicitly -> `write_back`
- child needs parent resources such as logger or service client -> capture resources into the child
- child stream events should surface in the parent execution stream -> use a sub flow and consume the parent runtime stream
- child workflow may pause for human input or external resume -> do not use sub flow as the final design; move to `agently-triggerflow-interrupts-and-stream`
- exporting, loading, or visualizing a flow that contains sub flows -> combine with `agently-triggerflow-config`

## Important Boundaries

- `capture` copies selected parent data; it is not a live shared reference contract
- `write_back` is explicit; child changes do not automatically mutate the parent
- child `flow_data` is isolated from the reusable child-flow template unless written back
- child runtime stream events are bridged into the parent runtime stream
- child pause/resume and external re-entry are not supported through `to_sub_flow(...)` in the current runtime

## References

- `references/source-map.md`
- `references/subflow-boundaries.md`
- `references/capture-and-write-back.md`
- `references/isolation-stream-and-limits.md`
- `references/troubleshooting.md`
