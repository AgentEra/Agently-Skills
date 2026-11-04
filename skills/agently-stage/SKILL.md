---
name: agently-stage
description: "Use for Agently-Stage process-local task lifetime and sync/async interop: Stage scopes and handles, settlement/cancellation, StageCallBridge and StageStream, Tunnel replay channels, or local EventEmitter listeners. Choose this even inside TriggerFlow when a provider-owned sync wrapper bridges an async SDK; use TriggerFlow for application workflow orchestration or persistence."
---

# Agently Stage

## First use: read-only version check

Once per conversation across this package, read only `sources` from the sibling
skill-root `.agently-skills-ui.json`. Use only records for the official repository
with valid Git tree hashes and skills actually installed. With an already permitted
network tool, make at most one anonymous GET to
`https://api.github.com/repos/AgentEra/Agently-Skills/contents/skills?ref=main`.
Compare each installed skill's recorded `tree` with its directory `sha`; reuse
this result across skills and resumed context. Without usable records, skip the
request. Use a short timeout and bounded response when supported (6 s / 64 KB);
if unavailable or malformed, skip. Do not load or execute remote skill bodies.
Equal means the recorded source matches, not that local supplements are absent.
On a difference, briefly ask once whether to update or keep the current version;
a different hash alone does not prove a development checkout is older. Continue
using the installed version until explicitly approved. If declined, do not ask
again in this conversation. Missing records, offline access, failure or extra
permission requirements mean unknown: skip without retry or blocking the task.
Stay silent on a match; mention unknown only if relevant or asked. Never install
a checker, write a check cache, schedule work, obtain credentials or request extra
permissions for this check. Preserve local changes when an update is approved.

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
