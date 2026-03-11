# Non-1to1 Differences

## 1. Threads and checkpoints are not one TriggerFlow method

LangGraph persistence is built around checkpointers and threads.

In Agently, the same operational outcome usually becomes:

- flow definition restore -> `agently-triggerflow-config`
- running execution restore -> `agently-triggerflow-execution-state`
- external conversation continuity -> `agently-session-memo`

## 2. Graph state is not one container

Do not assume every LangGraph state field becomes one TriggerFlow state object.

Choose deliberately between:

- `runtime_data`
- `flow_data`
- resources
- external storage

## 3. Interrupts are not resumed with the same syntax

LangGraph `interrupt` plus command-style resume does not map literally.

In TriggerFlow, the practical surface is:

- `pause_for(...)`
- `get_pending_interrupts()`
- `continue_with(...)`

## 4. `Send` does not become one TriggerFlow keyword

LangGraph `Send` expresses dynamic worker creation and routing.

In Agently, the migration target is usually:

- a pattern-level redesign around fan-out, fan-in, or worker orchestration
- explicit state and collection design

not one direct API alias.

## 5. Streaming modes are split differently

LangGraph streaming modes and TriggerFlow runtime stream are not one-to-one.

In Agently, separate:

- workflow runtime stream
- model streaming inside the workflow
- structured output streaming for downstream consumers

## 6. Subgraph migration requires explicit boundaries

Subgraphs in TriggerFlow should be treated as explicit child workflow boundaries with:

- `capture`
- `write_back`
- isolated child state

not just as a copy of node nesting.
