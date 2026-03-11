# Interactive Loop Patterns

This page covers the common interaction shapes built from interrupts and runtime stream.

## 1. Wait-Resume Loop

Use this when a flow should:

- do one step
- wait for feedback
- resume
- continue the next turn

Core ingredients:

- `pause_for(...)`
- `continue_with(...)`
- a `when(resume_event)` branch

## 2. Stream-Driven Interactive Loop

Use this when a flow should:

- receive user input
- stream output progressively
- emit another loop event
- continue until an exit condition stops the stream

Core ingredients:

- runtime stream
- explicit loop events
- a clear stop condition

## 3. Safety Rule

Whether the loop is pause-driven or stream-driven:

- make the stop condition explicit
- do not rely on an unbounded self-spin
- be deliberate about who owns the final result
