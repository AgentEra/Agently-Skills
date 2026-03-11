# Concept Map

Use this page to translate LangGraph orchestration concepts into the current TriggerFlow skill tree.

## `StateGraph`

Nearest Agently target:

- `agently-triggerflow-orchestration`

## Nodes and edges

Nearest Agently target:

- `agently-triggerflow-orchestration`

## Router, fan-out, loop, or handoff-like graph shape

Nearest Agently target:

- `agently-triggerflow-patterns`

## `Send`

Nearest Agently target:

- `agently-triggerflow-patterns`

This is usually where the migration redesigns dynamic worker fan-out and collected joins instead of looking for one direct `Send` replacement.

## `Command`

Nearest Agently target:

- `agently-triggerflow-interrupts-and-stream`

Sometimes also add:

- `agently-triggerflow-orchestration`
- `agently-triggerflow-execution-state`

## Graph state

Nearest Agently target:

- `agently-triggerflow-state-and-resources`

This is where the migration decides whether data belongs in:

- `runtime_data`
- `flow_data`
- runtime resources
- external persistence

## Interrupts and human-in-the-loop

Nearest Agently target:

- `agently-triggerflow-interrupts-and-stream`

## Persistence and checkpoints

Nearest Agently target:

- `agently-triggerflow-config`
- `agently-triggerflow-execution-state`

Add `agently-session-memo` when conversational memory exists outside the workflow execution itself.

## Subgraphs

Nearest Agently target:

- `agently-triggerflow-subflows`

## Graph streaming

Nearest Agently target:

- runtime stream -> `agently-triggerflow-interrupts-and-stream`
- model streaming inside the workflow -> `agently-triggerflow-model-integration`
- structured response streaming -> also add `agently-output-control`
