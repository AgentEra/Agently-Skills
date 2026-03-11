---
name: agently-triggerflow-patterns
description: Use when implementing common TriggerFlow orchestration patterns such as routers, fan-out and fan-in, `batch(...)`, `for_each(...)`, `collect(...)`, `side_branch(...)`, safe loops, evaluator-optimizer loops, ReAct or tool loops, or human-in-the-loop approval-gate patterns.
---

# Agently TriggerFlow Patterns

This skill covers common business workflow patterns in TriggerFlow. It focuses on routing, fan-out and fan-in, item-wise worker patterns, safe loops, evaluator-optimizer loops, ReAct-style tool loops, and human-in-the-loop gate patterns. It does not replace the lower-level skills for core TriggerFlow primitives, state placement, sub-flow boundaries, explicit interrupt mechanics, model-request implementation, flow config, or execution-state restore.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- router and classify-then-route workflows
- fan-out and fan-in workflows
- `batch(...)`, `for_each(...)`, `collect(...)`, and `side_branch(...)` as pattern tools
- safe loops with stop conditions and loop budgets
- evaluator-optimizer or maker-checker loops
- ReAct or tool-loop workflow design
- human approval gates or pause-between-turns patterns at the business-workflow level

Do not use this skill for:

- `chunk`, `to(...)`, `when(...)`, `if_condition(...)`, or `match(...)` as standalone API questions
- `runtime_data`, `flow_data`, or runtime-resource placement as the main problem
- `to_sub_flow(...)`, `capture`, or `write_back` as the main problem
- actual model-call implementation inside a flow chunk
- explicit `pause_for(...)`, `continue_with(...)`, pending interrupts, or runtime-stream lifecycle as the main problem
- flow config export/import or execution save/load mechanics

## Workflow

1. Start with [references/router-and-fanout.md](references/router-and-fanout.md) when the workflow should branch, dispatch, or aggregate.
2. Read [references/loops-and-control.md](references/loops-and-control.md) when the workflow needs repeated turns, bounded retries, or dead-loop prevention.
3. Read [references/evaluator-optimizer-and-react.md](references/evaluator-optimizer-and-react.md) when the workflow alternates between generate/evaluate or think/act/observe cycles.
4. Read [references/human-gates.md](references/human-gates.md) when a human gate, approval checkpoint, or pause-between-turns design is part of the workflow.
5. If the task turns into concrete interrupt handling, switch to `agently-triggerflow-interrupts-and-stream`.
6. If the task turns into model requests or streaming model output inside the pattern, switch to `agently-triggerflow-model-integration`.
7. If the task turns into state placement or restart-safe dependency design, switch to `agently-triggerflow-state-and-resources`.
8. If behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

A pattern is not just one API call. It is a repeatable workflow shape with a clear failure mode.

The useful TriggerFlow pattern questions are usually:

- how should work be routed
- what should run in parallel
- how should results be rejoined
- how should a loop stop safely
- where should a human gate sit

Good TriggerFlow pattern design is still async-first:

- prefer async handlers
- prefer async entrypoints
- use explicit events, loop budgets, and bounded concurrency instead of implicit recursion or unbounded task spawning

## Selection Rules

- classify one request and send it down one branch -> router pattern
- one input must fan out into several independent branches then rejoin -> fan-out and fan-in
- one list should be processed item by item with bounded concurrency -> `for_each(...)`
- one branch should observe or log without owning the main result -> `side_branch(...)`
- repeated turns must stop under a clear condition -> safe loop
- one draft should be judged and revised until it passes or the budget is exhausted -> evaluator-optimizer
- one workflow should alternate between reasoning, tool action, and observation -> ReAct or tool loop
- one workflow must stop at an approval checkpoint or wait between turns -> human gate pattern
- actual pause/resume implementation -> `agently-triggerflow-interrupts-and-stream`
- actual model requests in the loop -> `agently-triggerflow-model-integration`

## Important Boundaries

- a loop is not safe unless it has a stop condition and a turn budget
- `batch(...)` and `for_each(...)` are pattern tools, not a substitute for state design
- approval gates should be placed before sensitive side effects, not after them
- long waits or approvals should checkpoint state rather than rely on replaying the whole workflow
- ReAct or evaluator loops should not spawn unbounded new work from raw model output

## References

- `references/source-map.md`
- `references/router-and-fanout.md`
- `references/loops-and-control.md`
- `references/evaluator-optimizer-and-react.md`
- `references/human-gates.md`
- `references/troubleshooting.md`
