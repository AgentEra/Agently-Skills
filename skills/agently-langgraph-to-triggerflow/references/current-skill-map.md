# Current Skill Map

Use this page to choose the target TriggerFlow skill combination for LangGraph-side migration.

## Primary targets

- `agently-triggerflow-playbook`
- `agently-triggerflow-orchestration`
- `agently-triggerflow-patterns`
- `agently-triggerflow-state-and-resources`
- `agently-triggerflow-subflows`
- `agently-triggerflow-interrupts-and-stream`
- `agently-triggerflow-config`
- `agently-triggerflow-execution-state`
- `agently-triggerflow-model-integration`

## Supporting cross-skill targets

- `agently-output-control`
- `agently-model-setup`
- `agently-session-memo`
- `agently-multi-agent-patterns`

## Practical routing

- graph structure first -> `agently-triggerflow-orchestration`
- workflow shape first -> `agently-triggerflow-patterns`
- persistence first -> `agently-triggerflow-config` + `agently-triggerflow-execution-state`
- interrupt or HITL first -> `agently-triggerflow-interrupts-and-stream`
