# Isolation, Stream, And Limits

This page covers how sub flows behave at runtime.

## 1. Isolated Child State

The child flow runs as an isolated execution.

That means:

- child `runtime_data` is its own execution state
- child `flow_data` is isolated from the reusable child template unless explicitly written back
- parent state does not become child state unless captured

## 2. Runtime Stream Bridge

Child runtime-stream events are bridged into the parent execution stream.

This is useful when:

- the child emits progressive business output
- the parent should expose one combined runtime stream to the caller

Consume the parent runtime stream, not a separate child stream, when the sub flow runs inside the parent execution.

## 3. Current Limit

Child pause/resume and external re-entry are not supported through `to_sub_flow(...)` in the current runtime.

If the child workflow needs:

- `pause_for(...)`
- external resume
- long-lived waiting behavior

switch the design toward `agently-triggerflow-interrupts-and-stream` instead of hiding that behavior inside a sub flow.

## 4. Concurrency Note

`to_sub_flow(..., concurrency=...)` controls the child execution concurrency boundary.

Use it when the child flow itself fans out work and should run under a bounded child-execution limit.
