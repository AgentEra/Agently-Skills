---
name: agently-stage
description: "Use for Agently-Stage process-local task lifetime and sync/async interop: Stage scopes and handles, settlement/cancellation, StageCallBridge and StageStream, Tunnel replay channels, or local EventEmitter listeners. Choose this even inside TriggerFlow when a provider-owned sync wrapper bridges an async SDK; use TriggerFlow for application workflow orchestration or persistence."
---

# Agently Stage

Agently 4.1.4.7+ requires `agently-stage>=0.3.8,<0.4.0`. Use Stage for
process-local lifetime, call-shape bridging, replay channels, and local listener
dispatch. These APIs are independently useful, while Agently also uses Stage as
a private runtime mechanism.

## Read by Need

- Stage scopes/backend selection, `StageHandle`, settlement, cancellation,
  caller-loop task ownership, pressure, idle timeout, and snapshots:
  [task-lifecycle.md](references/task-lifecycle.md).
- `Stage.as_sync/as_async`, `StageCallBridge`, `StageStream`, `Tunnel`,
  `EventEmitter`, and compatibility names:
  [bridges-streams-events.md](references/bridges-streams-events.md).
- TriggerFlow state/signals, workflow close, recovery, or application
  orchestration: use `agently-triggerflow`.
- Actions, ExecutionResources, TaskWorkspace, RecordStore, services, or
  DevTools: use `agently-runtime`.

## Boundary

Choose the smallest surface that matches the caller:

- Direct call/`await` when caller and work already have the same shape.
- `async with Stage()` for explicit async lifetime; `with Stage()` for a
  deliberate blocking boundary.
- `Stage.as_sync/as_async` for one scalar adapter.
- `Stage.go(...)` plus `StageHandle` for a submitted result that must be read
  across loops or threads.
- `Stage.create_task(...)` for caller-loop work Stage creates; `adopt(...)`
  only for a task that already exists.
- `StageCallBridge` for injected lifetime, managed blocking cancellation, or
  iterator conversion; `StageStream` for generator replay.
- `Tunnel` for an independently writable process-local replay channel and
  `EventEmitter` for process-local listeners.

A synchronous facade blocks its calling thread. Do not bridge a call that
already has the correct native shape.

## Invariants

- Body completion and settlement are different facts. Read the body with
  `get()`/`async_get()` and wait for retained descendants/finalizers with
  `wait_settled()`/`async_wait_settled()` when their completion matters.
- Never block the caller-owned loop needed by the work. Use the matching async
  barrier when Stage reports a lifecycle conflict.
- After cancellation, wait for settlement before claiming no later Stage-owned
  work can occur. Stage cannot preempt a non-cooperative blocking function or
  undo an external side effect.
- Put concurrency, pending, worker, and idle limits at their actual pressure
  boundaries. Carrier-loop count is not application admission control.
- Automatic Stage scopes remain independent even when they safely reuse a
  carrier.

Stage does not own workflow progression, business retry, persistence,
authorization, provider cancellation acknowledgement, or external side
effects. `TriggerFlowExecution` remains Agently's public workflow lifecycle
owner; Stage objects and carrier state must not enter execution snapshots.

`LocalTaskScope` and the historical Stage dispatch/function type names are 0.3
compatibility surfaces. Do not teach them as new owner layers.
