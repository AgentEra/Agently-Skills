# Human Gates

This page covers human-in-the-loop patterns at the workflow-design level.

## 1. Approval Gate

Use an approval gate before:

- sensitive side effects
- external writes
- irreversible actions

Typical pattern:

1. prepare draft or recommendation
2. stop at an approval checkpoint
3. continue only after human approval

## 2. Pause-Between-Turns

Use this pattern when the workflow should alternate between one automated turn and one outside response.

Typical cases:

- review cycles
- interview-like guided flows
- long-running research with periodic operator review

## 3. Checkpoint Rule

If a human gate matters, checkpoint before waiting so the workflow can resume without replaying prior work.

That usually means combining the pattern with:

- `agently-triggerflow-interrupts-and-stream`
- `agently-triggerflow-execution-state`

## 4. Boundary

This page covers where human gates belong in the workflow.

Actual `pause_for(...)`, `continue_with(...)`, pending interrupt handling, and runtime stream belong in `agently-triggerflow-interrupts-and-stream`.
