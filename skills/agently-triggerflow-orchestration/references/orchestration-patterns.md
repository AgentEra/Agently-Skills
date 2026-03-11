# Core Orchestration Construction

This page covers the core TriggerFlow construction rules that sit below the reusable workflow-pattern skill.

## 1. Smallest Flow

Use:

- `flow.to(handler).end()`

This is the default linear path:

- `START` -> handler -> result

## 2. Signal Gates With `when(...)`

Use `when(...)` when a step should start only after one or more signals arrive.

Typical forms:

- `when("EventName")`
- `when({"event": ["A", "B"]}, mode="and")`
- `when({"runtime_data": ["flag", "phase"]}, mode="and")`
- `when({"flow_data": "shared_key"})`

Use this when the workflow is event-driven rather than a single linear pipeline.

## 3. Conditional Routing

Use:

- `if_condition(...)`
- `elif_condition(...)`
- `else_condition()`
- `match().case(...).case_else().end_match()`

Use this when the signal should branch by boolean logic or by value routing.

## 4. Event Re-Entry

Use explicit event re-entry when one execution should keep reacting to later events.

Typical tools:

- `emit(...)`
- `async_emit(...)`
- `when(...)`

Use this when the next step belongs to the same execution but should start from an event boundary instead of the current chain.

## 5. When To Switch To Workflow Patterns

Switch to `agently-triggerflow-patterns` when the question becomes:

- router versus fan-out
- `batch(...)` versus `for_each(...)`
- `collect(...)` or `side_branch(...)`
- safe loops
- evaluator-optimizer or ReAct
- human approval gates

## 6. When To Switch To Subflows

If the workflow needs:

- `to_sub_flow(...)`
- explicit `capture` and `write_back`
- isolated child-flow state
- parent-child runtime-stream bridging

switch to `agently-triggerflow-subflows`.

## 7. Result Mechanics

`end()` sets a default result sink.

Current behavior:

- if no result is already set, `end()` turns the current value into the final result
- if a result is already set manually, `end()` only unblocks result waiting

So use:

- `end()` for ordinary result-producing chains
- `execution.set_result(...)` when the flow is more event-driven and result ownership must be explicit
