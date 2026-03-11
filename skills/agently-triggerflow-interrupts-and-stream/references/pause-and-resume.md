# Pause And Resume

Use interrupts when a running execution must wait for an external answer.

## 1. Pause

Use:

- `await data.async_pause_for(...)`
- or `data.pause_for(...)`

Typical parameters:

- `type`
- `payload`
- `resume_event`
- optional `interrupt_id`

Current behavior:

- the execution status becomes `waiting`
- the interrupt is recorded in pending interrupts
- a pause event is also written into runtime stream

## 2. Resume

Use:

- `execution.get_pending_interrupts()`
- `await execution.async_continue_with(interrupt_id, value)`

Current behavior:

- interrupt status becomes `resumed`
- a resume event is written into runtime stream
- if `resume_event` is configured, TriggerFlow emits that event into the same execution

## 3. Good Usage Pattern

Typical flow:

1. a chunk prepares context
2. it pauses for external input
3. external code reads the pending interrupt
4. external code resumes with a payload
5. a `when(resume_event)` branch continues the workflow

## 4. Important Boundary

Pause/resume is not the same as persistence.

This skill covers:

- waiting
- resuming
- interactive continuation

This skill does not cover:

- saving a waiting execution to disk
- loading it back after restart
