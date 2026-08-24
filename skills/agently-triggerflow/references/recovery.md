# TriggerFlow Recovery

Use this reference for pause/resume snapshots, resource restoration, snapshot
projection and retention, and restart-safety claims.

## Save and Load Boundary

`execution.save()` serializes TriggerFlow progress, definition fingerprint,
execution state, interrupt/resume ledgers, declared resource requirements, and
eligible metadata. It does not serialize live clients, callbacks, semaphores,
tasks, coroutine frames, secrets, or stateful external sessions.

Use `inspect_load(...)` / `async_load(...)`, stable `resume_request_id` values,
snapshot-store CAS, and provider-owned lease/idempotency semantics. Pending or
unhealthy required resources are not ready. Restore ExecutionResources through
host/plugin resolvers; external systems retain their own ref, version, lease,
or fence token and validate it before continuation.

## Snapshot Projection

For payload-heavy terminal histories, opt into typed digest projection rather
than deleting snapshot fields:

```python
execution.set_snapshot_projection_policy(
    terminal_value_mode="digest",
    min_value_bytes=4096,
)
snapshot = execution.save(require_idle=True)
```

Projection preserves pending interrupts and incomplete resume records. It
projects only eligible terminal interrupt values and completed SignalNet resume
metadata while preserving duplicate/conflicting `resume_request_id` checks via
canonical digests. It gives up full body readback for projected values, defers
while execution is active, and does not bound current state or `last_signal`.

Keep this separate from RuntimeEvent `set_compaction_policy(...)`. RuntimeEvent
compaction does not project execution-snapshot interrupts, resume ledgers, or
SignalNet state.

## Physical Retention

Snapshot-version retention belongs to the provider. The built-in local
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

`keep_last=None` disables automatic pruning at that layer. An execution
override has precedence and survives save/load. Generic
`put_checkpoint(...)` records are not automatically pruned.

For explicit cleanup, require an idle execution and preserve at least one
recovery point:

```python
report = await execution.async_prune_recovery_snapshots(keep_last=1)
```

Use provider-level `prune_snapshots(run_id, keep_last=...)` for administration
and `delete_snapshot(run_id)` only for deliberate full cleanup. Snapshot
projection, physical retention, RuntimeEvent compaction, and business-data
retention are separate policies.

## Subflows and Restart Claims

Running subflow frame metadata may be inspectable, but the live child execution
is process-local. Loading a snapshot with a `running` or `cancel_requested`
frame fails closed. Settle or cancel active children before a restart-resumable
snapshot; waiting child frames retain their root-interrupt resume contract.

A local RecordStore demonstrates local restart behavior only. Production
distributed-worker claims require a real shared provider, resource restoration,
lease/fencing behavior, and observed operational evidence.
