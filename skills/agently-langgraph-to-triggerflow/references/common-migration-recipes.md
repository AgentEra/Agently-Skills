# Common Migration Recipes

## 1. `StateGraph` with ordinary nodes and conditional routing

Typical Agently target:

- `agently-triggerflow-orchestration`
- `agently-triggerflow-patterns`

## 2. LangGraph interrupt plus checkpoint

Typical Agently target:

- `agently-triggerflow-interrupts-and-stream`
- `agently-triggerflow-config`
- `agently-triggerflow-execution-state`

## 3. `Send`-based orchestrator-worker graph

Typical Agently target:

- `agently-triggerflow-patterns`
- `agently-triggerflow-state-and-resources`

Add:

- `agently-triggerflow-model-integration` if each worker performs model calls

## 4. Graph with graph-state-heavy workers

Typical Agently target:

- `agently-triggerflow-state-and-resources`
- `agently-triggerflow-patterns`

## 5. Subgraph-based architecture

Typical Agently target:

- `agently-triggerflow-subflows`

## 6. `Command`-style resume after approval or human input

Typical Agently target:

- `agently-triggerflow-interrupts-and-stream`
- `agently-triggerflow-execution-state`

## 7. Graph streaming plus model calls

Typical Agently target:

- `agently-triggerflow-model-integration`
- `agently-triggerflow-interrupts-and-stream`
- `agently-output-control`
