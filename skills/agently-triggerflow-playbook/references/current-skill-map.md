# Current TriggerFlow Skill Map

This page lists the current public TriggerFlow-related skills in this repository and what each one owns.

## `agently-triggerflow-orchestration`

Use for core TriggerFlow workflow construction and runtime semantics:

- `chunk`
- `to(...)`
- `when(...)`
- branching and matching
- execution entrypoints
- `end()` and `set_result(...)`
- `set_contract(...)` and live runtime contract validation

## `agently-triggerflow-patterns`

Use for repeatable business workflow shapes:

- routers and classify-then-route flows
- fan-out and fan-in
- `batch(...)`, `for_each(...)`, `collect(...)`, and `side_branch(...)`
- safe loops and dead-loop prevention
- evaluator-optimizer and maker-checker loops
- ReAct or tool loops
- approval gates and pause-between-turns patterns

## `agently-triggerflow-state-and-resources`

Use for runtime state placement and dependency boundaries:

- `runtime_data` versus `flow_data`
- flow-level versus execution-level runtime resources
- `data.set_resource(...)`
- restart-safe state design
- save/load and config persistence boundaries for resources

## `agently-triggerflow-subflows`

Use for isolated child workflows:

- `to_sub_flow(...)`
- `capture` and `write_back`
- child-flow state isolation
- parent-child runtime-stream bridge
- sub-flow-specific boundaries and limits

## `agently-triggerflow-model-integration`

Use for model execution inside TriggerFlow:

- request creation inside chunks
- async model calls per step, branch, or item
- multiple model requests through `batch(...)`, `for_each(...)`, or bounded gather
- using `delta` or `instant` inside the flow
- early dispatch from completed structured-streaming nodes

## `agently-multi-agent-patterns`

Use for specialist agent-team design on top of current Agently capabilities:

- planner-worker or supervisor-router
- staged specialist pipelines
- parallel experts and synthesizer
- reviewer-reviser
- explicit agent handoff contracts and ownership boundaries

## `agently-triggerflow-config`

Use for definition-level export, import, copy, and visualization:

- `save_blue_print()` / `load_blue_print()`
- `get_flow_config()`
- `get_json_flow()` / `get_yaml_flow()`
- `load_json_flow()` / `load_yaml_flow()`
- `to_mermaid(...)`
- exported contract metadata and contract-aware Mermaid
- handler registration and runtime-resource reinjection after restore

## `agently-triggerflow-execution-state`

Use for execution-instance persistence and restore:

- `execution.save()`
- `execution.load()`
- waiting or ready-result restore
- resume after restore
- runtime-resource reinjection

## Common Restore Combination

Use this combination for a suspended workflow after restart:

- `agently-triggerflow-config` for restoring the definition
- `agently-triggerflow-execution-state` for restoring the running instance

Add `agently-session-memo` when conversation memory lives outside the execution runtime itself.

## `agently-triggerflow-interrupts-and-stream`

Use for live interaction and wait-resume behavior:

- `pause_for(...)`
- `continue_with(...)`
- pending interrupts
- runtime stream output
- long-lived interactive loops
- forwarding live model output into runtime stream

## Common Cross-Skill Combinations

- TriggerFlow + restart-safe state design:
  add `agently-triggerflow-state-and-resources`
- TriggerFlow + provider setup:
  add `agently-model-setup`
- TriggerFlow + structured output or structured streaming:
  add `agently-output-control`
- TriggerFlow + session-backed memory:
  add `agently-session-memo` only if the workflow design truly depends on session state outside the flow runtime itself
