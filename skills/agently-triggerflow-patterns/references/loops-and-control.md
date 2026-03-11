# Loops And Control

This page covers loop patterns and dead-loop prevention.

## 1. Safe Loop

A TriggerFlow loop is only safe when it has:

- a clear stop condition
- a turn budget or retry budget
- explicit ownership of final result

Good loop state often includes:

- current step count
- seen states or attempts
- reason for stopping

## 2. Three Practical Loop Shapes

### Self-Emit Loop

Use when the workflow can continue immediately inside the same execution.

Typical tool:

- `async_emit("Loop", ...)`
- `when("Loop")`

### Pause-Between-Turns Loop

Use when each turn should wait for outside feedback before the next one.

Typical pattern:

- do one step
- pause
- continue on resume

Actual implementation belongs in `agently-triggerflow-interrupts-and-stream`.

### External Re-Entry Loop

Use when the safest design is to let outside events drive each next turn.

Typical pattern:

- initialize execution
- wait for external events
- process each event through `when(...)`

## 3. Anti-Loop Rules

Do not:

- run a loop without a turn budget
- let raw model output directly cause unbounded self-emission
- place expensive side effects before the stop condition is checked

## 4. Real-World Rule

If the loop can sleep, wait for humans, or survive restart, design explicit checkpoints and be ready to combine with:

- `agently-triggerflow-interrupts-and-stream`
- `agently-triggerflow-execution-state`
