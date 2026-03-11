# Contract And Runtime Types

Use this page when the main TriggerFlow question is about typed boundaries rather than only control flow.

## 1. Contract Surface

Use:

- `flow.set_contract(...)`
- `flow.get_contract()`

Current public contract sections are:

- `initial_input`
- `stream`
- `result`
- optional `meta`

## 2. What Runtime Validation Covers

When a live contract is set on a flow:

- `start(...)` / `async_start(...)` validate the initial input
- `put_into_stream(...)` / `async_put_into_stream(...)` validate user-defined stream items
- `set_result(...)` validates the final result

This is runtime validation, not only type-hint decoration.

## 3. Good Fit

Use a contract when:

- the workflow should reject wrong initial input early
- runtime stream items should have a stable shape
- final result should be guarded by one explicit output type
- several workers or services depend on a stable workflow boundary

## 4. Contract Versus Patterns

The contract does not decide workflow shape.

It does not replace:

- router design
- loop stopping rules
- state placement
- interrupt behavior

It only constrains the runtime payload shape at key boundaries.

## 5. Important Boundary

Even with a user stream contract, runtime stream can still contain system interrupt events. Those system events belong to TriggerFlow's own runtime surface and are not rejected by the user stream contract.
