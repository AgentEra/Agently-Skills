# Stage Task Lifetime

## Backend Selection

`Stage()` is lazy. Construction creates no loop or thread. The first accepted
root in an active epoch selects:

- the current running loop inside an async service;
- a safe inherited caller loop or carrier inside Stage-owned work;
- otherwise a finite process-wide Stage carrier.

After complete settlement, an automatic Stage releases the binding and a later
root selects again. One active epoch never spans multiple loops. Use
`Stage(loop="stage")` only when the caller deliberately requires the Stage
carrier; pass an exact loop only when it must remain pinned.

`with Stage()` requests a synchronous boundary and selects a physically safe
carrier even inside an async function. `async with Stage()` prefers the
current loop. Native async code should prefer the async form because the sync
form blocks its thread.

Both context-manager forms are standalone lifecycle APIs. Use them directly
when a component needs a bounded scope that accepts work and settles retained
descendants on exit; no TriggerFlow wrapper is required.

```python
from agently_stage import Stage


with Stage() as stage:
    value = stage.get(lambda: "ready")

assert value == "ready"
```

## Root Result and Settlement

```python
import asyncio

from agently_stage import Stage


async def request() -> str:
    await asyncio.sleep(0)
    return "ok"


stage = Stage()
handle = stage.go(request)
assert handle.get() == "ok"
handle.wait_settled()
stage.close()
```

`StageHandle.get()` and `async_get()` expose the root/body outcome.
`wait_settled()` and `async_wait_settled()` additionally cover Stage-owned
descendants, callbacks, and finalizers.

Body failures remain body failures. Callback, finalizer, or retained-descendant
failures become `StageSettlementError` and do not replace a successful body
value. Future-shaped methods such as `result()`, `exception()`,
`add_done_callback()`, and `await handle` read body completion, not complete
settlement.

## Caller-Loop Task Ownership

Use `Stage.create_task()` when Stage should create and own a native task on the
current caller loop:

```python
async def main() -> None:
    stage = Stage()
    task = stage.create_task(asyncio.sleep(0, result="ready"), origin="hook:ready")
    assert await task == "ready"
    await stage.async_close()
```

Use `adopt(task, origin=...)` only when the task was already scheduled before
the handoff. Both surfaces retain native `asyncio.Task` identity and add
origin diagnostics, cancellation, idle tracking, and settlement. They do not
wrap the task in a second handle.

On caller-owned loops, raw unrelated `asyncio.create_task()` calls stay owned
by the caller. Stage never replaces a caller loop's task factory. On the Stage
carrier, tasks created inside Stage work are retained by its carrier task
factory.

## Cancellation and Close

`cancel()` fences the handle's Stage-owned task tree and delivers
cancellation. Wait for settlement afterward when cleanup and the absence of
later Stage-owned work matter. A zero-timeout cancel may request cancellation
without claiming settlement.

`seal()` rejects new external roots while accepted work drains.
`wait_settled()` waits without sealing. `close()` combines both. Timeout
leaves the scope sealed and reports unresolved origins; close may be retried
after work settles.

Stage never closes a caller-owned event loop. It cannot preempt a
non-cooperative blocking function or reverse an external side effect.

## Pressure and Diagnostics

- `max_concurrency`: concurrently running external `go()` roots.
- `max_pending`: admitted roots waiting for a root permit; overflow raises
  `StageBackpressureError`.
- `max_workers`: blocking executor workers.
- `idle_timeout`: maximum time unresolved work may show no Stage activity;
  cooperative providers call `stage.tick()`.

Nested Stage-owned work does not consume a second root permit. Adopted tasks
were already scheduled, so root admission limits cannot delay them honestly.

`snapshot()` returns bounded process-local diagnostics: scope/backend state,
active and pending counts, unresolved origins, activity, idle state, and
carrier generation. It is not a workflow or persistence snapshot.
