# State Surfaces

This page explains what TriggerFlow execution state represents.

If the task is about where state or resources should live before persistence, use `agently-triggerflow-state-and-resources` instead.

## 1. Definition Versus Execution

Do not mix these two:

- flow definition
- execution instance state

Definition answers:

- what the workflow is
- what operators and handlers exist

Execution state answers:

- where one run currently is
- what runtime data exists
- whether it is waiting, running, failed, or completed
- whether a result is already ready

## 2. What `save()` Captures

Current execution state includes:

- `execution_id`
- `status`
- `runtime_data`
- `flow_data`
- `interrupts`
- `last_signal`
- `resource_keys`
- result readiness and final result value

## 3. What `save()` Does Not Capture

Execution state does not serialize:

- live runtime resource objects
- the whole flow definition
- arbitrary external process state

That is why execution-state restore must be paired with:

- the correct flow definition
- runtime-resource reinjection when needed
