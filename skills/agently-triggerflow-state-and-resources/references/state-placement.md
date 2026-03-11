# State Placement

This page covers where runtime values should live in TriggerFlow.

## 1. `runtime_data` / `data.state`

Use `runtime_data` for:

- request-local context
- one execution's working state
- intermediate values that should disappear with that execution

Typical examples:

- current ticket or draft
- one run's counters or loop state
- request-specific intermediate results

## 2. `flow_data` / `data.flow_state`

Use `flow_data` for:

- shared flags on one flow object
- values that later executions of the same flow should see
- cross-execution coordination when that sharing is intentional

Typical examples:

- shared locale
- one flow-level feature flag
- intentionally shared counters or coordination flags

## 3. Common Failure Mode

Do not put request-local or user-local data into `flow_data`.

That can leak values into later executions of the same flow and create hard-to-debug concurrency bugs.

## 4. Fast Decision Rule

- one execution only -> `runtime_data`
- shared across later executions of the same flow -> `flow_data`
- durable outside the process or outside the TriggerFlow runtime -> external persistence, not either one by itself
