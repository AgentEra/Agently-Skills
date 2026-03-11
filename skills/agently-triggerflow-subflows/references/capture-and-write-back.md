# Capture And Write Back

This page covers explicit parent-child data handoff in TriggerFlow sub flows.

## 1. Capture

`capture` copies selected parent data into the child flow.

Capture target scopes:

- `input`
- `runtime_data`
- `flow_data`
- `resources`

Capture source scopes:

- `value`
- `runtime_data`
- `flow_data`
- `resources`

Default behavior without `capture` is equivalent to passing parent `value` into child `input`.

## 2. Write Back

`write_back` copies selected child result data back into the parent.

Write-back target scopes:

- `value`
- `runtime_data`
- `flow_data`

Write-back source scopes:

- `result`

Default behavior without `write_back` is equivalent to writing child `result` into parent `value`.

## 3. Shape Guidance

Use simple whole-value mappings when:

- the whole parent value becomes the child input
- the whole child result should replace parent value

Use key-path mappings when:

- only selected fields should cross the boundary
- one child result should update several parent fields
- the child needs parent resources or selected runtime state

## 4. Important Boundary

`capture` and `write_back` are explicit copy rules.

Do not assume:

- automatic shared state
- automatic write-through from child to parent
- automatic exposure of all parent resources or state
