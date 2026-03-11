# Resources And Overrides

This page covers runtime-only dependencies in TriggerFlow.

## 1. Use Runtime Resources For Non-Serializable Dependencies

Use runtime resources for:

- service clients
- search helpers
- loggers
- renderers
- helper callables

These should not be stored in `runtime_data` or `flow_data`.

## 2. Flow-Level Versus Execution-Level Resources

Set flow defaults with:

- `flow.update_runtime_resources(...)`

Override for one execution with:

- `flow.create_execution(runtime_resources=...)`
- `flow.async_start(..., runtime_resources=...)`

Execution-level resources win over flow-level defaults for that execution.

## 3. `data.set_resource(...)`

Use `data.set_resource(...)` when a handler creates a temporary runtime dependency for the current execution only.

That resource does not automatically become a flow-level default and should not be expected in another execution.

## 4. Practical Rule

- reusable default dependency for the whole flow -> flow-level resource
- one request or one execution override -> execution-level resource
- temporary dependency created while handling the current run -> `data.set_resource(...)`
