---
name: agently-stage
description: "Use when the user needs Agently-Stage or Python process-local runtime foundations: independent Stage lifetime scopes, with Stage(), Stage.as_sync/as_async adapters, loop-neutral StageHandle results, retained-work settlement, cancellation, caller-loop task ownership, StageCallBridge, StageStream, independently writable Tunnel replay channels, process-local EventEmitter listeners, backpressure/idle diagnostics, or the private Stage mechanism beneath Agently TriggerFlow."
---

# Agently Stage

Use Agently-Stage for process-local task lifetime, call-shape bridging, replay
channels, and local listener dispatch. These are independent foundation
capabilities as well as mechanisms Agently may use internally. Keep workflow
state, business retry, persistence, authorization, and side effects in their
real owners.

Current Agently 4.1.4.7 guidance targets `agently-stage>=0.3.8,<0.4.0`.

## Read by Need

- Stage scopes, backend selection, `StageHandle`, settlement, cancellation,
  caller-loop tasks, pressure, idle timeout, and snapshots:
  read `references/task-lifecycle.md`.
- Independent `Stage.as_sync/as_async` adapters, `StageCallBridge`,
  `StageStream`, `Tunnel`, `EventEmitter`, and compatibility names:
  read `references/bridges-streams-events.md`.
- TriggerFlow state, signals, workflow close, recovery, or application
  orchestration: use `agently-triggerflow`.
- Action, ExecutionResource, TaskWorkspace, RecordStore, service, or DevTools
  behavior: use `agently-runtime`.

## Choose the Smallest Surface

| Need | Use |
|---|---|
| Native async caller and native async work | Direct `await` |
| Explicit async lifetime and settlement | `async with Stage()` |
| Deliberate sync boundary over async work | `with Stage()` or `Stage.as_sync(...)` |
| Async view of blocking sync work | `Stage.as_async(...)` |
| One submitted result readable from any loop/thread | `Stage.go(...)` plus `StageHandle` |
| Native caller-loop `asyncio.Task` owned by Stage | `Stage.create_task(...)` |
| Pre-existing caller-loop task handed to Stage | `Stage.adopt(...)` |
| Injected lifecycle, managed blocking cancellation, or iterator conversion | `StageCallBridge` |
| Generator result with complete replay and complete result list | `StageStream` |
| Independently writable replay channel | `Tunnel` |
| Process-local listener registry | `EventEmitter` |

Do not bridge a call that already has the correct native shape. A sync facade
blocks its calling thread even when Stage routes the async work safely.

`with Stage()`, `Stage.as_sync/as_async`, `Tunnel`, and `EventEmitter` are
standalone Stage APIs; TriggerFlow is not required. Add TriggerFlow only when the application needs visible
multi-step progression, branching, joins, retry, waiting/resume, workflow
signals, or durable workflow recovery.

## Owner Boundaries

`Stage` owns accepted process-local work, lineage, cancellation delivery,
origin diagnostics, and settlement. It does not own:

- workflow progression, signals, retry, pause/resume, or durable recovery;
- EventCenter or RuntimeEvent semantics;
- provider cancellation acknowledgement;
- authorization, idempotency, compensation, or external side effects;
- tenant, process, resource-isolation, or durable-storage boundaries.

Agently uses Stage as a private required-runtime companion. TriggerFlowExecution
remains the workflow lifecycle owner; Stage objects and carrier state must not
enter public execution state or snapshots. Stage `EventEmitter` does not
replace Agently EventCenter or SignalNet.

## Core Rules

- Prefer async APIs when the caller owns an async interface.
- Never block the same caller-owned loop needed by the work. Stage raises
  `StageLifecycleError`; switch to the matching async barrier and `await`.
- Treat body completion and settlement as separate facts. Read the body with
  `get()`/`async_get()`; use `wait_settled()`/`async_wait_settled()`
  when retained descendants, callbacks, and finalizers must be complete.
- Use `create_task()` when Stage creates caller-loop work. Use `adopt()` only
  for a task that existed before ownership transfer.
- After cancellation, wait for settlement when later Stage-owned work must be
  ruled out. Python cannot preempt a non-cooperative blocking function or undo
  an external effect.
- Set `max_concurrency`, `max_pending`, `max_workers`, and
  `idle_timeout` at their actual pressure boundaries. Do not describe carrier
  loop count as application admission or coroutine concurrency.
- Keep automatic Stage scopes independent. Safe carrier reuse does not merge
  task inventories, errors, or settlement barriers.

## Compatibility

`LocalTaskScope` is a deprecated 0.3 compatibility facade and is scheduled for
removal in 0.4. New code uses `Stage.go()`, `Stage.create_task()`, or
`Stage.adopt()`.

`StageHybridGenerator`, `StageResponse`, `StageDispatch`,
`StageDispatchEnvironment`, `StageCallBackTask`, `StageTaskProxy`,
`TaskThreadPool`, and `StageFunction` are compatibility names. Do not teach
them as new owner layers.

## Validation

- Reproduce lifecycle bugs before changing routing or settlement.
- Test both body outcome and settlement outcome.
- Cover caller-owned loop, Stage carrier, nested sync scope, cancellation,
  timeout, and process-exit behavior that the change claims.
- Test supported Python versions, especially task-factory behavior on Python
  3.14.
- For an Agently integration change, build the Stage wheel and run the affected
  Agently integration plus full suite before publication; after publication,
  rerun from the PyPI artifact.
