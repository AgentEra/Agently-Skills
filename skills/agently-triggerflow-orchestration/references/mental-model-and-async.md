# Mental Model And Async

TriggerFlow is a signal-driven orchestration runtime.

## 1. Core Objects

- `TriggerFlow` defines the workflow structure
- `TriggerFlowExecution` is one running instance of that structure
- `TriggerFlowRuntimeData` is what each chunk receives while handling one signal

This distinction matters because one flow can serve many executions at the same time.

## 2. TriggerFlow Is Not Only A START Chain

`START` is just the default first signal.

Flows can also react to:

- normal events
- `runtime_data` signals
- `flow_data` signals

So the mental model should be:

- define handlers and wiring
- let signals move the workflow forward
- choose whether each step mutates state, emits more signals, writes to runtime stream, or sets a final result

## 3. Async-First Guidance

Public guidance for this skill should treat async APIs as the preferred path.

Prefer:

- `await flow.async_start(...)`
- `await flow.async_start_execution(...)`
- `await execution.async_emit(...)`
- `await execution.async_continue_with(...)`
- `execution.get_async_runtime_stream(...)`

Use sync wrappers only when the caller truly needs a sync bridge:

- `flow.start(...)`
- `flow.start_execution(...)`
- `execution.emit(...)`
- `execution.continue_with(...)`
- `flow.get_runtime_stream(...)`

Why async-first matters:

- TriggerFlow internals are async
- multiple executions can overlap cleanly in async services and workers
- model streaming, runtime stream, and human-in-the-loop resumes fit naturally into async code

Important boundary:

- async-first does not mean every single isolated flow run is magically faster
- the main benefit is correct integration and cleaner concurrency at scale

## 4. Result Is Separate From Stream

TriggerFlow has two independent output channels:

- final result
- runtime stream

Final result becomes available through:

- `end()`
- or `execution.set_result(...)`

Runtime stream is produced through:

- `put_into_stream(...)`
- `async_put_into_stream(...)`
- `stop_stream(...)`
- `async_stop_stream(...)`

A flow may stream many items before it has a final result, or it may stream and never define a final result unless the workflow explicitly does so.
