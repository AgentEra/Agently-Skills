# Independent Stage Bridges, Streams, Channels, and Events

The surfaces in this reference are public Stage capabilities. They can be used
directly in a Python component without Agently or TriggerFlow when their
process-local contracts match the problem.

## Scoped Scalar Adapters

Use `Stage.as_sync()` and `Stage.as_async()` for deliberate scalar call-shape
adaptation:

```python
import asyncio

from agently_stage import Stage


async def fetch(identifier: int) -> str:
    await asyncio.sleep(0)
    return f"item-{identifier}"


fetch_sync = Stage.as_sync(fetch)
assert fetch_sync(7) == "item-7"
```

Each invocation owns an automatic Stage scope and waits for its settlement.
`as_sync()` blocks its calling thread. `as_async()` sends blocking sync work
to an executor. Direct call/direct await remains the fast path when no bridge is
needed.

Typical standalone uses are exposing a synchronous facade for an async SDK,
adapting a blocking library to an async service, or preserving one callable API
while migrating its implementation between sync and async. These adapters own
one scalar invocation at a time; they do not create workflow stages.

## StageCallBridge

Use `StageCallBridge` when the caller needs one of these advanced contracts:

- injected or reusable Stage/executor lifetime;
- `submit()` returning a loop-neutral `StageHandle`;
- `iter_sync(async_iterator)` or `iter_async(sync_iterator)`;
- `managed=True` cancellation acknowledgement for blocking sync work;
- explicit bridge `close()`/`async_close()`.

The default bridge is light. It adapts call shape without adding application
retry, event, or workflow semantics. A supplied Stage or executor is borrowed
and is never closed by the bridge.

Use `managed=True` only when the boundary actually owns descendant settlement
or must wait until a running blocking call returns after cancellation.

## StageStream

Running a sync or async generator through `Stage.go()` returns a read-only
`StageStream`. Sync and async readers receive independent cursors over one
canonical complete replay. `get()`/`async_get()` and success callbacks
receive a complete result-list copy.

This complete replay/result contract is intentionally unbounded. Use
`lazy=True` to delay source start until the first reader. A consumer that
stops early should close the stream so the source is terminated and settled.

## Tunnel

`Tunnel` is independently writable and is not a Stage task:

```python
from agently_stage import Tunnel

channel: Tunnel[int] = Tunnel(max_history=128)
channel.put(1)
subscription = channel.subscribe(start="earliest", timeout=None)
channel.put(2)
channel.close()
assert list(subscription) == [1, 2]
```

Accepted values have one total order. Every sync/async subscription owns its
cursor. `close()` publishes EOF; `fail(error)` publishes a terminal failure
after accepted values.

Default replay is unbounded. `max_history` retains a bounded suffix and never
hides loss: a lagging reader receives `TunnelLagError` with absolute sequence
facts. It is replay retention, not producer backpressure, durable
acknowledgement, retry, or exactly-once delivery.

Use `Tunnel` independently for in-process fan-out, replayable progress,
sync/async consumer interop, or checkpointed local subscriptions. Use a durable
broker or application-owned event store when values must survive the process or
participate in delivery acknowledgement.

## EventEmitter

`EventEmitter` owns one reusable Stage scope for local listener work.
`emit(..., wait=False)` returns listener handles; `wait=True` waits while
keeping each listener failure on its own handle. A `once` listener is removed
atomically before invocation.

Use it only for process-local registration and invocation. Remote delivery,
durability, message matching, and application event policy belong elsewhere.
It does not replace Agently EventCenter, RuntimeEvent, SignalNet, or
TriggerFlow.

Use `EventEmitter` independently for plugin hooks, local lifecycle callbacks,
or one-process extension points where listeners may be sync or async. It does
not require a workflow; introducing TriggerFlow for listener registration alone
would add the wrong owner layer.
