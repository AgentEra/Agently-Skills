# Router And Fan-Out

This page covers the most common dispatch and aggregation patterns.

## 1. Router

Use a router pattern when one request should go down one branch.

Typical tools:

- `if_condition(...)`
- `match(...)`
- `when(...)`

Typical cases:

- route by task type
- route by urgency
- route by confidence or policy class

Use router patterns when one branch should own the next step. Do not use parallel fan-out just to simulate routing.

## 2. Fan-Out And Fan-In

Use fan-out and fan-in when one input should be processed by several independent branches and then rejoined.

Typical tools:

- `batch(...)`
- `collect(...)`
- custom `async_emit(...)` plus `when(...)`

Typical cases:

- multiple independent analyzers
- read/write/check branches
- several post-processors over the same input

## 3. Item-Wise Worker Pattern

Use `for_each(...)` when the workflow should process one sequence item per worker path.

Typical cases:

- one section at a time
- one candidate at a time
- one chunk at a time

Use `concurrency=` to cap parallel work.

## 4. Side Branch

Use `side_branch(...)` when auxiliary work should run without taking over the main result path.

Typical cases:

- logging
- metrics
- notifications
- best-effort secondary enrichment

## 5. Decision Rule

- one branch wins -> router
- several branches work on the same input -> fan-out and fan-in
- one list item per worker path -> `for_each(...)`
- auxiliary work should not own result semantics -> `side_branch(...)`
