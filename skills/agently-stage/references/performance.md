# Stage Performance Choices

Prefer direct await or `async with Stage()` for native async services. Measure
throughput, tail latency, memory and settlement; maximizing CPU usage alone is
not a performance objective.

- Keep one carrier lane by default. `Stage.set_settings("runtime.carrier_loop_count", N)`
  is process-wide and freezes at first carrier use; extra lanes cost threads,
  serve separate scopes and do not split one active scope or bypass the GIL.
- Group tiny related coroutines in one explicit async root only when they share
  result/cancellation ownership. Retain caller-loop children with
  `stage.create_task(coro, origin="batch item")`, bound application fan-out and
  cancel/drain children explicitly if fail-fast behavior is wanted. `gather`
  alone does not cancel siblings on the first failure. Never automatically merge
  independent `go()` handles.
- `max_concurrency` limits external roots, `max_pending` limits queued roots,
  and `max_workers` creates a private blocking thread pool. Nested children do
  not consume another root permit; an admission cap is not a fan-out cap.
- Blocking I/O and native computation releasing the GIL can benefit from
  threads. Pure Python CPU work under the GIL needs an explicit application
  process boundary for multicore execution. Do not pass ProcessPoolExecutor or
  InterpreterPoolExecutor as Stage's executor: Stage's context-bound submissions
  cannot cross those boundaries. Serialization, startup and cancellation costs
  must be measured; tiny tasks can become slower.
- Separate `Stage(executor=pool)` scopes can reserve a fixed total thread budget
  for short work when slow work harms latency. The caller owns borrowed pools;
  settle scopes before closing pools. Reserved capacity can increase total batch
  duration. Do not auto-classify tasks or create one pool per request.
- StageStream retains complete history, using O(N) memory; `get` and callbacks
  create list copies. Iteration avoids a requested result copy, not retention.
  `Tunnel(max_history=N)` permits bounded retention and explicit TunnelLagError,
  not producer backpressure or durable delivery.
- Native Rust/Go hotspots should use coarse operations behind ordinary Python
  callables. Bare ctypes function classification is a known 0.3.8 limitation.
  Kernel parallelism is not evidence that the Python scheduler needs rewriting.
- uvloop is an application-owned optional caller-loop choice. Do not install or
  select it globally on the user's behalf. Free-threaded Python and transparent
  interpreter-pool execution are not validated recommendations.

## Agently-Stage 0.3.9 performance options

Agently-Stage 0.3.9 uses indexed list storage for unbounded replay, preserving
bounded deque eviction. `Tunnel(wake_mode="grouped")` requires >=0.3.9,<0.4.0;
0.3.8 does **not** accept this keyword. Upgrade Stage explicitly before using it.
Agently's existing >=0.3.8,<0.4.0 runtime range accepts 0.3.9; this guidance
does not raise the framework dependency minimum.

Default `wake_mode="individual"` schedules readers separately. `"grouped"`
schedules one callback per waiting owner loop per notification and still resolves
all individual readers. It introduces no delay window, item merging or dropping.
Try it for many waiting readers on the same loop and measure producer cadence,
CPU and P99: small fan-out or latency-sensitive work can regress. It does not
replace application batching, change retention, or expose a Stage-wide backend.
