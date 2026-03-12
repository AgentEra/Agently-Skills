---
name: agently-triggerflow-interrupts-and-stream
description: Use only when the main task is live TriggerFlow waiting, resume, or runtime-stream behavior, such as `pause_for(...)`, `continue_with(...)`, pending interrupts, runtime-stream lifecycle, or forwarding live model output into TriggerFlow runtime stream.
---

# Agently TriggerFlow Interrupts And Stream

This skill is the live-interaction leaf inside the TriggerFlow domain. It focuses on `pause_for(...)`, `continue_with(...)`, pending interrupts, runtime stream lifecycle, interactive wait-and-resume loops, and forwarding live model output into TriggerFlow runtime stream. It does not decide whether the user should use TriggerFlow in the first place, and it does not cover general orchestration patterns, flow config export/import, or execution-state persistence and restore.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- `async_pause_for(...)` and `pause_for(...)`
- `get_pending_interrupts()`
- `async_continue_with(...)` and `continue_with(...)`
- interrupt status transitions and resume events
- `async_put_into_stream(...)`, `put_into_stream(...)`, `async_stop_stream(...)`, and `stop_stream(...)`
- `get_async_runtime_stream(...)` and `get_runtime_stream(...)`
- runtime stream behavior when a TriggerFlow stream contract exists
- runtime stream timeout behavior
- interactive loops that alternate between waiting and resuming
- forwarding model delta or other live producer output into runtime stream

Do not use this skill for:

- `batch(...)`, `for_each(...)`, `collect(...)`, or sub-flow orchestration design
- `runtime_data` vs `flow_data` architecture in general
- flow config export/import or Mermaid output
- execution `save()` / `load()` restore mechanics after restart
- provider setup or standalone model-output parsing outside the TriggerFlow boundary

## Workflow

1. Start with [references/pause-and-resume.md](references/pause-and-resume.md) if the workflow must wait for a human or external system.
2. Read [references/runtime-stream.md](references/runtime-stream.md) when the flow should produce live business output during execution.
3. Read [references/interactive-loop-patterns.md](references/interactive-loop-patterns.md) when the flow alternates between input, live output, and resume events.
4. If live model output should flow through TriggerFlow, read [references/model-stream-bridge.md](references/model-stream-bridge.md).
5. If the main task is saving and restoring a waiting execution, switch to `agently-triggerflow-execution-state`.
6. If behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

TriggerFlow has two live interaction surfaces:

- interrupts for waiting and resuming
- runtime stream for progressive output

They are related, but different:

- interrupts change execution status and wait for external continuation
- runtime stream pushes live items to consumers without deciding final result
- user stream contract validation applies to user-defined stream items, while system interrupt events can still pass through the runtime stream

Public guidance for this skill should remain async-first:

- prefer `async_pause_for(...)`
- prefer `async_continue_with(...)`
- prefer `get_async_runtime_stream(...)`
- prefer `async_put_into_stream(...)`

Use sync wrappers only when the caller truly needs a sync bridge.

## Selection Rules

- workflow must stop and wait for human approval -> `pause_for(...)`
- external system should resume a specific waiting execution -> `get_pending_interrupts()` + `continue_with(...)`
- UI should see live progress events before final result -> runtime stream
- runtime stream should carry both typed business events and built-in interrupt events -> use runtime stream and account for system interrupt events in the consumer
- long-running interactive loop should keep streaming output while re-entering the flow -> runtime stream plus explicit resume or loop events
- model tokens or structured stream events should be surfaced through the workflow -> forward them into runtime stream
- final result is still needed after streaming or resume -> reach `end()` or call `set_result(...)`
- saving and restoring a waiting execution -> use `agently-triggerflow-execution-state`

## Important Boundaries

- runtime stream is independent from final result
- `continue_with(...)` resumes through the interrupt's configured resume event
- runtime stream can end by explicit `stop_stream()` or by consumer timeout
- if a flow has a stream contract, user-defined stream items are validated but system interrupt events are still legal runtime stream items
- saving and restoring a waiting execution is a separate persistence skill, not this one

## References

- `references/source-map.md`
- `references/pause-and-resume.md`
- `references/runtime-stream.md`
- `references/interactive-loop-patterns.md`
- `references/model-stream-bridge.md`
- `references/troubleshooting.md`
