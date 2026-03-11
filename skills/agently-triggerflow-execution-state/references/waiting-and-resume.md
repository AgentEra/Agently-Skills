# Waiting And Resume

This page covers waiting executions and resume-after-restore.

## 1. Save At A Waiting Point

Common pattern:

- execution reaches `pause_for(...)`
- state is saved while status is `waiting`
- a fresh execution loads the saved state
- the caller uses `continue_with(...)`

## 2. Pending Interrupts Survive Restore

After restore, the caller should inspect:

- `get_pending_interrupts()`

Then:

- choose the interrupt id
- call `continue_with(...)`

## 3. Continue Requires The Right Environment

A resumed execution still needs:

- the correct flow definition
- any required runtime resources

Otherwise resume may fail even though the interrupt state itself was restored.

## 4. Typical Resume Flow

1. restore the execution
2. inspect pending interrupts
3. reinject missing runtime resources if needed
4. `continue_with(...)`
5. await the final result
