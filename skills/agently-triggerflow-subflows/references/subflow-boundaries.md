# Subflow Boundaries

This page covers when a TriggerFlow workflow should use `to_sub_flow(...)`.

## 1. When A Sub Flow Is The Right Tool

Use a sub flow when:

- a child workflow should be treated as one reusable nested unit
- parent-child data handoff should be explicit
- child state should stay isolated from the parent unless written back
- the nested workflow is large enough that keeping it inline hurts readability

## 2. When Inline Orchestration Is Still Better

Keep the work inline in `agently-triggerflow-orchestration` when:

- the logic is still one ordinary chain or branch structure
- there is no meaningful parent-child boundary
- the parent and child would only mirror the same state anyway

## 3. Function-Like Mental Model

Treat a sub flow like a function call with explicit arguments and explicit returned fields:

- `capture` is the input contract
- child execution is the isolated function body
- `write_back` is the return contract

That mental model is usually more accurate than thinking of sub flow as a live shared nested process.
