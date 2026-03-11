# Subflow Boundaries

This page covers how state and resources cross a sub-flow boundary.

## 1. Nothing Crosses Automatically Except The Default Value Path

Sub flows are isolated child executions.

State and resources cross the boundary only through explicit `capture` and `write_back` rules.

## 2. What Usually Crosses Into A Child

Common patterns:

- parent `value` -> child `input`
- selected `runtime_data` -> child `runtime_data`
- selected `flow_data` -> child `flow_data`
- selected resources -> child resources

## 3. What Usually Comes Back

Common patterns:

- child `result` -> parent `value`
- selected result fields -> parent `runtime_data`
- selected result fields -> parent `flow_data`

## 4. Design Rule

Decide first:

- whether the value is execution-local state
- shared flow-level state
- or a runtime-only dependency

Then use `capture` or `write_back` to move only the necessary part across the boundary.
