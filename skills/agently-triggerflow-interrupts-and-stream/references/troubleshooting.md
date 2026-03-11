# Troubleshooting

This page only covers TriggerFlow interrupts and runtime stream.

## 1. Execution Did Not Resume

Check these first:

- whether the interrupt id is correct
- whether the interrupt is still in `waiting` status
- whether `resume_event` matches the `when(...)` listener

## 2. Runtime Stream Stopped Too Early

Check these first:

- whether the consumer timeout is too short
- whether `stop_stream()` was called intentionally
- whether `timeout=None` is needed for a long-lived session

## 3. Flow Streamed Output But Never Produced A Final Result

This is common when the flow is stream-driven.

Check these first:

- whether any path reaches `end()`
- whether the workflow should have called `set_result(...)`

## 4. Model Stream Bridge Feels Blocking

Default advice:

- use async generators
- use async runtime-stream APIs
- avoid sync wrapper bridges inside an already async runtime

## 5. Waiting Logic Seems To Need Persistence

If the real task is:

- save a waiting execution
- restore it after restart
- rehydrate resources and continue later

that belongs to a separate execution-state persistence skill.
