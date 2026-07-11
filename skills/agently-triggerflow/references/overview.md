# Overview

This skill owns TriggerFlow orchestration, execution state, runtime stream, sub-flow boundaries, workflow-side model execution, output-fan-out refactors, process-clarity refactors, and mixed sync/async orchestration.

Prefer async-first flow handlers and execution APIs. When the UI needs progressive updates, bridge model-side structured streaming into workflow-side runtime stream items so the frontend consumes stable business events instead of raw parser paths.

Before implementing a complex service or script, draw the actual dependency
graph. Keep edges serial only for real data dependencies, ordering guarantees,
side-effect safety, or external capacity constraints. Run independent stages
concurrently through `batch(...)`, `for_each(...)`, or signal-driven
`when(...)` plus execution-managed emits; use model-side `instant` structured
streaming when provisional fields can improve UI or support explicitly
cancelable/idempotent preparation. A retry may invalidate an `instant` update,
so irreversible side effects and business decisions must wait for the final
parsed result and configured validation. An all-serial topology selected
without dependency analysis is an anti-pattern.

Make pressure controls user-adjustable at their real boundaries. Use
`create_execution(concurrency=N)` / `execution.set_concurrency(N)` for the
execution-wide dispatch budget, operator `concurrency=` for local fan-out,
`model_request.scheduler.max_concurrency` /
`model_request.scheduler.rate_per_second` and
`model_request.scheduler.providers.<provider>` overrides for model dispatch,
and host admission limits plus bounded queues for
the number of active executions or coroutines. When blocking SDK calls must be
offloaded, expose the host-owned worker/thread-pool size and queue bound; do not
invent a TriggerFlow thread-count setting.

Prefer explicit execution lifecycle control. New TriggerFlow code should create or start an execution, let chunks update execution state, and finish with `close()` or `async_close()` so pending non-blocking work and runtime stream consumers are drained consistently. Avoid using result polling as the default completion contract.

Use `execution.result` when code needs more than one view of the same execution outcome. It is a facade over execution-owned state, not a second result store. Use `await execution.async_close()` for the finalized close snapshot, `execution.result.get_state("key")` for state reads before or after close, `await execution.result.async_get_final_result()` only for compatibility final-result bridging, and `execution.result.get_meta()` for execution id, flow name, status, lifecycle state, timestamps, close reason, and state version. Intervention-aware code may use `execution.result.get_interventions(...)` when the runtime intervention ledger is enabled; otherwise the reader is an empty-list no-op.

For short scripts that need a synchronous wrapper, `flow.start(...)` is acceptable as an outer boundary: it waits for execution close and returns the close snapshot. If legacy `.end()` / `set_result()` compatibility is present, the snapshot may include `"$final_result"`. Hidden `flow.start(...)` uses immediate idle auto-close by default; do not use it as the default service/streaming pattern, and keep an execution handle plus explicit `close()` / `async_close()` for services.

Use execution-managed nowait emit for event fan-out that should not block the current chunk. Prefer `emit_nowait(...)` / `async_emit_nowait(...)` over raw `asyncio.create_task(data.async_emit(...))` so the execution can register the task and drain it during `close()` / `async_close()`.

Treat auto-close as the default for short workflows and manual close as the service/worker pattern for long-running or externally driven executions. A manual-close execution keeps accepting events until user code calls `close()` / `async_close()`.

Treat `pause_for(...)` as a durable graph interrupt. New approval or webhook examples should choose an explicit `resume_to`: use `"next"` when the resume payload should flow to the downstream chunk, `"self"` when the same model-owned chunk should re-enter with `data.is_resume` / `data.resume`, and `{"event": "..."}` for signal-routed continuation. Use model-owned `pause_for(..., resume_to="self")` for autonomous model-decided interrupts. Use an explicit pause chunk plus `when(...)` for prearranged human approval gates. `resume_event=...` is compatibility guidance for older event-routed examples, not the default teaching path.

When a sub-flow may pause, external systems should resume only the root execution. Child interrupts are projected into root pending interrupts; callers store the root execution id and root interrupt id, then call `root_execution.continue_with(...)`. Re-inject required `runtime_resources` when restoring a saved root execution.

Use execution state (`get_state(...)`, `set_state(...)`, and async variants) for per-execution data. Flow data is shared across executions and should be treated as a risky internal/shared-state surface rather than normal workflow memory.

For service packaging, treat ordinary `TriggerFlow(...)` as the definition/planning surface and `create_execution(...)` / `start_execution(...)` as the boundary into one run. Prefer module-level named chunks and conditions. Put stable live dependencies such as `agent_factory`, clients, prompt paths, or loggers into flow-level `runtime_resources`; put request- or tenant-specific values into execution-level `runtime_resources`. Chunks should read required live dependencies with `data.require_resource(...)` and write per-request business values to execution state. Closures are acceptable for compact scripts, but they are not the recommended service shape because they reduce handler reuse, testing, and config/blueprint round-trip clarity.

For model-app dynamic planning, keep reusable main flows and sub-flow templates module-safe, then compile model-generated To-Do Lists or dependency graphs into request-local or plan-local executors. Use task ids as dynamic stage identities, drive dependency execution with `when(...)` + `emit_nowait(...)`, and store generated plan data and task results in execution input/state rather than shared flow data. Definition idempotence prevents duplicate graph declarations; it must not dedupe runtime signals, because repeated emits are real business events.

In Agently `v4.1.2.5`, TriggerFlow definitions, chunk signal metadata, origin-chunk payloads, resume context, and sub-flow interrupt projection are strong enough to support graph-oriented debugging and local DevTools visualization without duplicating the workflow description.

For the concrete `instant -> runtime stream` pattern, read `references/stream-bridge.md`.
For graph, export, and observation design, read `references/devtools-graph.md`.

## Main Repository Examples

When writing or updating guidance, align with the current Agently examples:

- `examples/trigger_flow/*.py` for compact lifecycle, emit, stream, sub-flow, save/load, and config export examples
- `examples/step_by_step/11-triggerflow-*.py` for tutorial-style coverage of the same APIs
- `examples/fastapi/fastapi_helper_triggerflow_ollama.py` for local Ollama + FastAPIHelper integration
- `examples/devtools/*trigger_flow*.py` and observation bridge examples for DevTools integration
