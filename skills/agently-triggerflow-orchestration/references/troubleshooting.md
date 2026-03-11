# Troubleshooting

This page only covers TriggerFlow orchestration.

## 1. Flow Never Returns A Result

Check these first:

- whether any branch calls `end()`
- whether the flow expects manual `set_result(...)`
- whether the caller used `wait_for_result=True` on a stream-only or interrupt-only flow

Common cause:

- a `when(...)` branch or side branch runs, but no result sink ever finalizes the execution

## 3. State, Resource, Or Sub-Flow Boundaries Look Wrong

If the real problem is:

- `runtime_data` versus `flow_data`
- flow-level versus execution-level resources
- `to_sub_flow(...)`, `capture`, or `write_back`

switch to `agently-triggerflow-state-and-resources` or `agently-triggerflow-subflows`.

## 4. Interrupt Or Runtime Stream Requirements Appear

If the real task is:

- `pause_for(...)`
- `continue_with(...)`
- pending interrupt handling
- runtime stream lifecycle
- live business output during execution

switch to `agently-triggerflow-interrupts-and-stream`.

## 5. Workflow-Pattern Choice Feels Unclear

If the real question is:

- router versus fan-out
- `batch(...)` versus `for_each(...)`
- safe loops
- approval gates

switch to `agently-triggerflow-patterns`.

## 6. Sync Integration Feels Awkward Or Blocks Too Much

Default advice:

- move to async APIs first
- treat sync wrappers as compatibility bridges, not the preferred runtime layer

This is especially important when the flow handles several concurrent executions or complex event-driven branches.
