---
name: agently-triggerflow
description: Use when the user needs workflow orchestration such as branching, concurrency, approvals, waiting and resume, runtime stream, restart-safe execution, mixed sync/async orchestration, event-driven fan-out, visible multi-stage quality loops, or workflow definitions and chunk-level runtime metadata that must remain inspectable.
---

# Agently TriggerFlow

Use TriggerFlow when the application or framework owns visible orchestration
semantics. Use ModelRequest/AgentExecution for one bounded request/run, and use
AgentTask when one Agent owns a long task's planning, evidence, verification,
and replan loop without application-authored stage topology.

The request does not need to say TriggerFlow or Agently; route by lifecycle and
topology needs.

## Read by Need

- Core graph/state/lifecycle: `references/overview.md`.
- Optional runtime guidance versus required external wait:
  `references/runtime-intervention.md`.
- Stable business stream projection: `references/stream-bridge.md`.
- DevTools graph/observation: `references/devtools-graph.md`.
- Full value/event topology review:
  `../agently/references/execution-topology-validation.md`.
- RecordStore, TaskWorkspace, TaskContext, or Skills ownership:
  `../agently/references/context-and-skills.md`.

## Topology First

Map the real dependencies before implementation:

- required serial value edges;
- independent branches and joins;
- provisional structured progress safe for UI or cancelable/idempotent work;
- request-time information boundaries: a later model stage that needs an
  Action/system/readback result must start after that observed result is
  validated, not remain a later field of the producing request;
- side-effect ordering and external capacity constraints;
- external waits, retries, repair, and terminal behavior.

Use `batch(...)`, `for_each(...)`, `when(...)`, and managed emits for bounded
concurrency and graph-visible joins. Do not default a complex flow to all-serial
execution merely because it is easier to write.

`instant` may trigger provisional work before its producing request completes.
If a later ModelRequest needs the work's result, make the join visible as
`R1 -> Action/system work -> validation -> R2`; do not treat `instant` as a
back-channel into R1.

Represent repetition with a graph-visible back edge. Do not hide a `while True`
lifecycle, retry, or revision loop inside a chunk handler.

For audits, trace exact values and signals through ModelRequest, Action,
subflow, TaskWorkspace/RecordStore, wait/resume, repair, and terminal boundaries.
Graph adjacency proves activation, not value transfer.

## Lifecycle

- Prefer async handlers, execution entrypoints, and stream consumers.
- Use `flow.start(...)` / `flow.async_start(...)` only for finite, self-closing
  runs whose caller needs no execution handle.
- Use `flow.create_execution(auto_close=False)` when the host needs pause/resume,
  external emit, save/load, intervention, inspection, cancellation, or
  host-controlled close.
- Start with a positional value: `await execution.async_start(value)`. The value
  is not a custom event.
- Close with `await execution.async_close()`. Close drains execution-managed
  nowait tasks and returns the close snapshot.
- Pending interrupts make close fail by default. Choose cancellation deliberately
  when abandoning waits.
- Active non-paused children created by `to_sub_flow(...)` are visible through
  `execution.get_sub_flow_frames()`. Use
  `async_emit_to_sub_flow(frame_id, ...)` for best-effort child signaling and
  `async_cancel_sub_flow(frame_id, reason=...)` to cancel/fence one child while
  keeping the parent execution open. A cancelled child does not write back or
  continue downstream. See `examples/active_sub_flow_control.py` for the
  explicit execution shape.

Do not make code after `await data.async_pause_for(...)` the restart contract.
Put post-resume behavior in a downstream chunk, `data.is_resume` branch, or
explicit resume event handler.

## State and Storage

- Execution state is the per-execution data store and chunk-to-chunk handoff contract.
  Use `data.get_state(...)` / `data.set_state(...)` and async variants;
  setters replace the complete value and `append_state(...)` is only for
  intentional list accumulation. Do not add a translation helper or shadow
  store; put durable cross-run data in RecordStore or another explicit provider.
- `flow_data` is shared across executions. The `execution.save()` snapshot includes a serialized copy
  of `flow_data`; `load()` replaces the current
  flow-shared value with that copy. This does not provide execution isolation,
  CAS, merge, or concurrency safety.
- Use `TaskWorkspace` for task files/artifacts and a business-owned database or
  RecordStore record collection when deterministic domain state must outlive or
  be shared across runs. Execution snapshots are for restart/disconnected-wait
  recovery, not business audit or state archival. Use durable RuntimeEvents or
  purpose-built audit records when durable history is actually required.
- Keep compact refs/status in execution state and full bodies cold.
- Bind RecordStore ports explicitly. Ordinary observation belongs in
  logs/DevTools; `runtime_event_store` is only for requested durable audit/replay.

```python
from agently import TriggerFlow
from agently.core import RecordStore

flow = TriggerFlow(name="approval-flow")
record_store = RecordStore("./flow-state", mode="read_write")
execution = flow.create_execution(
    record_store=record_store,
    runtime_resources={"runtime_event_store": record_store},
    auto_close=False,
)
```

`record_store=False` opts out of the default RecordStore view for finite flows
that need neither persistence nor record access.

## Concurrency and Pressure

- `create_execution(concurrency=N)` / `execution.set_concurrency(N)` bounds
  execution-wide handler dispatch, including nested emits.
- `batch(..., concurrency=N)` / `for_each(..., concurrency=N)` bounds local
  fan-out.
- Host admission/in-flight limits, model scheduler rate/concurrency limits, and
  worker/thread-pool limits belong to their own layers.
- Use `emit_nowait(...)` / `async_emit_nowait(...)` for non-blocking fan-out;
  do not default to untracked `asyncio.create_task(...)`.
- Rely on execution close to drain registered work instead of polling a custom
  status loop.

## Waiting, Approval, and Exchange

- Use `pause_for(..., resume_to="next"|"self"|{"event": ...})` for required
  external input. It is a durable graph interrupt, not a persisted coroutine
  stack.
- Use explicit pause chunks plus `when(...)` for prearranged gates. A
  model-decided self-resume path must handle `data.is_resume` and keep a bounded
  resume count.
- Use global PolicyApproval for framework policy gates and represent pending
  approval as a TriggerFlow interrupt.
- Use ExecutionExchange providers for host UI/webhook/queue transport. The
  provider publishes typed requests; TriggerFlow owns the interrupt/resume
  ledger and `continue_with(...)` lifecycle.
- Project host-facing exchange views through the public execution-exchange
  helpers rather than raw interrupt internals.
- Use runtime intervention for optional context at declared boundaries; use
  pause/resume when the answer is required before continuing.

## Recovery Contract

`execution.save()` serializes TriggerFlow progress, definition fingerprint,
state, interrupt/resume ledgers, declared resource requirements, and eligible
metadata. It does not serialize live clients, callbacks, semaphores, tasks,
coroutine frames, secrets, or stateful external sessions.

For payload-heavy terminal histories, use the typed snapshot projection policy
instead of deleting raw snapshot fields:

```python
execution.set_snapshot_projection_policy(
    terminal_value_mode="digest",
    min_value_bytes=4096,
)
snapshot = execution.save(require_idle=True)
```

Digest projection is opt-in. It preserves pending interrupts and incomplete
resume records, projects only eligible terminal interrupt values and completed
SignalNet resume metadata, and keeps duplicate/conflicting
`resume_request_id` checks through canonical digests. It intentionally gives up
full historical body readback for projected values, defers while the execution
is active, and does not bound current state or `last_signal`.

Keep this separate from `set_compaction_policy(...)`: that policy compacts
durable RuntimeEvent records into segments, anchors, and artifact refs. It does
not project execution-snapshot `interrupts`, `resume_ledger`, or `signal_net`.
Physical snapshot version retention remains provider-owned. The built-in local
RecordStore keeps the latest three execution snapshots per `run_id` by default:

```python
record_store = RecordStore(
    "./recovery",
    mode="read_write",
    snapshot_retention={"keep_last": 5},
)
execution.set_snapshot_retention_policy(keep_last=2)
await execution.async_save(record_store)
```

`{"keep_last": None}` or the execution override with `keep_last=None` disables
automatic pruning at that layer. The execution override has precedence and
survives save/load. Generic `put_checkpoint(...)` writes are not automatically
pruned.

For active recovery hygiene, require the execution to be idle and preserve at
least one latest point:

```python
report = await execution.async_prune_recovery_snapshots(keep_last=1)
```

This method resolves `execution.run_id`; low-level provider administration
still requires `record_store.prune_snapshots(run_id, keep_last=...)`. Use
`delete_snapshot(run_id)` only for explicit full cleanup. Do not combine
snapshot projection, physical retention, RuntimeEvent compaction, and business
data retention into one policy.

Running sub-flow frame metadata may appear in a snapshot for audit, but the
live child execution is not restart-resumable. Loading a snapshot with a
`running` or `cancel_requested` frame fails closed. Settle or cancel active
children before taking a restart-resumable snapshot; projected `waiting` child
frames keep their normal root-interrupt resume contract.

Declare resource requirements and restore live ExecutionResources through
host/plugin resolvers. A stateful external system must persist its own ref,
version, lease, or fence token and validate it before load is ready.

Use `inspect_load(...)` / `async_load(...)`, stable `resume_request_id` values,
snapshot-store CAS, and provider-owned lease/idempotency semantics. Treat
pending or unhealthy required resources as not ready; fail closed according to
the declared policy.

A local RecordStore proves local restart behavior only. Do not claim production
distributed-worker guarantees without real shared providers and operational
evidence.

## Stable Definitions and Dynamic DAGs

- Define developer-owned stable topology directly with `flow.to(...)` and
  `flow.when(...)` in importable modules with top-level handlers.
- Use a builder only when multiple configured flow instances or test isolation
  is actually required.
- Route model-generated or application-submitted DAG data through
  TaskDAG/DynamicTask validation and resolvers. Do not compile model-generated or app-submitted DAG data directly into new TriggerFlow definitions.
- Ordinary `TaskDAGExecutor.async_run(...)` compiles validated DAG data directly
  to TriggerFlow. Blocks is explicit opt-in only when the caller needs Blocks
  lifecycle evidence or an `ExecutionBlockGraph`.

## API Shape

```python
from agently import Agent, Agently, TriggerFlow, TriggerFlowRuntimeData

agent = Agent()
factory_agent = Agently.create_agent()
flow = TriggerFlow(name="workflow-name")
factory_flow = Agently.create_trigger_flow("factory-workflow")
```

`when`, `emit_nowait`, and `pause_for` are methods on flow/runtime objects, not
top-level imports. Do not use `@flow.when(...)` as a decorator. Do not pass a
flow name as the first positional TriggerFlow constructor argument.

## Anti-Patterns

- Custom event bus, state machine, DAG scheduler, or shadow per-execution store
  before checking TriggerFlow/TaskDAG.
- `while True` lifecycle/retry/revision loops hidden inside a chunk.
- Sleeps/polling/local completed sets instead of signals and joins.
- Closure-captured live business resources instead of explicit runtime
  resources/resolvers.
- Flow data as normal task/execution state.
- DevTools/manual diagrams as topology source of truth instead of the flow
  definition and runtime metadata.
