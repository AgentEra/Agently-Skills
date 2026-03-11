# Business Restore Recipes

This page explains how suspended real-world workflows should be restored.

## 1. Same Process, Short Suspend

Use this when:

- the Python process is still alive
- the flow definition is still in memory
- only the execution should be resumed later

Typical sequence:

1. keep the original flow object
2. create or keep the execution
3. save execution state if needed
4. load the state into a fresh execution if you want a clean restore path
5. reinject runtime resources if they are needed
6. continue or read the result

## 2. Process Restart Or Service Restart

Use this when:

- the old process is gone
- the definition must be restored before the execution can resume

Typical sequence:

1. restore the flow definition with `agently-triggerflow-config`
2. register any required handlers
3. create a fresh execution
4. load the saved execution state
5. reinject runtime resources
6. continue or read the result

This is the standard answer for "a suspended workflow was persisted and the service restarted".

## 3. Waiting Approval Or Human-In-The-Loop Resume

Use this when:

- the execution was waiting on `pause_for(...)`
- the user or external system returns later with approval or feedback

Typical sequence:

1. restore the definition if needed
2. restore the execution state
3. inspect `get_pending_interrupts()`
4. choose the correct interrupt id
5. reinject any required runtime resources
6. call `continue_with(...)`
7. await the final result

## 4. Suspended Conversation-Like Workflow

Many real systems treat the workflow as an ongoing conversation.

If the suspended experience depends on:

- flow-local runtime data and pending interrupts

then execution-state restore is the main restore mechanism.

If it also depends on:

- session-backed memory outside the TriggerFlow execution
- agent chat history that should survive across turns independently from the execution

then also use `agently-session-memo`.

Practical guidance:

- workflow state -> `agently-triggerflow-execution-state`
- flow definition -> `agently-triggerflow-config`
- long-lived session memory outside the execution -> `agently-session-memo`

## 5. Hard Boundary

`execution.load(...)` restores the saved runtime surface.

It does not by itself guarantee that the business workflow is restorable unless:

- the correct definition is present
- required runtime resources are present
- external memory or session state is restored when the business scenario depends on it
