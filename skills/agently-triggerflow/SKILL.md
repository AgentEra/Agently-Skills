---
name: agently-triggerflow
description: Use when developer-owned execution needs inspectable branching, concurrency, joins, waits, approval, retry, runtime streams, pause/resume, recovery, or mixed sync/async orchestration. Use agently-stage instead when a provider-owned sync wrapper only bridges an async SDK.
---

# Agently TriggerFlow

Use TriggerFlow when the application owns visible multi-stage execution
semantics. Use ModelRequest/AgentExecution for one bounded request/run, and use
`agent.create_task(...)` when one Agent owns a long task's planning, evidence,
verification, and repair without application-authored stage topology.

## Read by Need

- Graph construction, state, lifecycle, Stage bridging, and main-repo examples:
  `references/overview.md`.
- Pause/resume snapshots, resource restoration, retention, and restart claims:
  `references/recovery.md`.
- Optional runtime guidance versus required external wait:
  `references/runtime-intervention.md`.
- Stable application stream projection: `references/stream-bridge.md`.
- DevTools graph/observation: `references/devtools-graph.md`.
- Full value/signal topology review:
  `../agently-design/references/execution-topology-validation.md`.
- Direct Stage scopes, settlement, bridges, channels, or listeners use
  `agently-stage`.

## Topology First

Before implementation, map:

- required serial value edges;
- independent branches and bounded joins;
- request-time observation boundaries;
- provisional work that is safe to cancel or discard;
- side-effect ordering, external capacity, waits, repair, and terminal states.

Use `batch(...)`, `for_each(...)`, `when(...)`, and managed emits to make
fan-out and joins graph-visible. Represent repetition with an explicit back
edge; do not hide lifecycle, retry, or revision loops inside `while True` chunk
handlers.

A ModelRequest is a dispatch-time snapshot. `instant` output may update UI or
start idempotent/cancelable preparation, but a later model request that needs
the resulting observation must start after a visible join and validation
barrier.

Graph adjacency proves activation, not value transfer. For audits, trace exact
values, signals, refs, and consumers through ModelRequest, Action, subflow,
TaskWorkspace/RecordStore, wait/resume, repair, and terminal boundaries.

## Lifecycle and State

- Prefer async handlers and execution APIs when the caller owns the async
  boundary. A synchronous provider facade may use Agently-Stage internally;
  route direct bridge questions to `agently-stage`.
- Use `flow.start(...)` / `flow.async_start(...)` only for finite self-closing
  runs whose caller needs no execution handle.
- Use `flow.create_execution(auto_close=False)` for external emit, pause/resume,
  save/load, intervention, inspection, cancellation, or host-controlled close.
- Start with a positional value and close with `await execution.async_close()`.
  Close drains execution-managed nowait work and reports unresolved ownership.
- Put post-resume behavior in a downstream chunk, an explicit resume event, or
  a `data.is_resume` branch; a suspended Python frame is not the recovery
  contract.
- Execution state owns per-run chunk handoff. In async chunks, await async state,
  emit, and stream methods. Setters replace the complete value; append only for
  intentional list accumulation.
- `flow_data` is shared across executions. Save/load serializes and replaces a
  copy of that shared value; it does not provide isolation, CAS, merge, or
  concurrency safety.
- TaskWorkspace owns files, RecordStore owns durable records and recovery, and
  host storage owns business persistence. Keep compact refs/status in execution
  state and full bodies cold.

## Concurrency, Waits, and Streams

- `create_execution(concurrency=N)` bounds execution-wide handler dispatch;
  `batch(..., concurrency=N)` and `for_each(..., concurrency=N)` bound local
  fan-out.
- Host admission, provider/model rate limits, and blocking worker pools remain
  separate pressure owners.
- Use `emit_nowait(...)` / `async_emit_nowait(...)` instead of untracked
  `asyncio.create_task(...)`; execution close settles registered work.
- Use `pause_for(..., resume_to=...)` for required external input. Use runtime
  intervention only for optional context at declared boundaries.
- PolicyApproval owns framework policy gates; ExecutionExchange adapts host
  UI/webhook/queue transport; TriggerFlow owns the interrupt/resume ledger.
- Translate model parser events into stable application events. Do not expose
  raw parser paths as the frontend protocol, and reconcile provisional items
  against final validated output.

## Recovery and Dynamic-Graph Boundary

Save/load owns TriggerFlow progress and declared recovery metadata, not live
clients, callbacks, semaphores, coroutine frames, secrets, or external session
state. Restore live ExecutionResources through host/plugin resolvers and verify
external refs, versions, leases, and fence tokens before readiness. A local
RecordStore proves local restart only; do not claim distributed recovery
without a real shared provider and operational evidence.

Define developer-owned stable topology directly in importable TriggerFlow
modules with top-level handlers. Explicit submitted or model-generated DAG
data is a low-frequency TaskDAG case; read
`../agently/references/task-dag.md`. Never compile unvalidated runtime plan data
into ad hoc TriggerFlow definitions.

## API Shape

```python
from agently import Agently, TriggerFlow

flow = TriggerFlow(name="workflow-name")
factory_flow = Agently.create_trigger_flow("factory-workflow")
execution = flow.create_execution(auto_close=False)
```

`when`, `emit_nowait`, and `pause_for` are flow/runtime methods, not top-level
imports. Do not use `@flow.when(...)` as a decorator or pass a flow name as the
first positional `TriggerFlow(...)` argument.

## Anti-Patterns

- A custom event bus, state machine, DAG scheduler, or shadow execution store.
- Sleeps, polling, local completed sets, or untracked tasks in place of signals,
  joins, and execution-managed work.
- Closure-captured live business resources instead of explicit runtime
  resources and resolvers.
- `flow_data` as ordinary per-execution state.
- DevTools diagrams as topology source of truth instead of the definition and
  runtime metadata.
