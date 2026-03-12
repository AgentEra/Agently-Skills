# Current Skill Map

This page lists the current public skills in this repository by solution layer.

## Top-level routing

- `agently-playbook`

## Model-request-side routing

- `agently-model-request-playbook`
- `agently-model-setup`
- `agently-input-composition`
- `agently-output-control`
- `agently-eval-and-judge`
- `agently-embeddings`
- `agently-tools`
- `agently-mcp`
- `agently-knowledge-base-and-rag`
- `agently-session-memo`
- `agently-prompt-config-files`
- `agently-fastapi-helper`

## Multi-agent routing

- `agently-multi-agent-patterns`

## TriggerFlow routing

- `agently-triggerflow-playbook`
- `agently-triggerflow-orchestration`
- `agently-triggerflow-patterns`
- `agently-triggerflow-state-and-resources`
- `agently-triggerflow-subflows`
- `agently-triggerflow-model-integration`
- `agently-triggerflow-config`
- `agently-triggerflow-execution-state`
- `agently-triggerflow-interrupts-and-stream`

## Practical entry rules

- one request or one request family -> `agently-model-request-playbook`
- specialized agent-team design -> `agently-multi-agent-patterns`
- long-running or stateful workflow -> `agently-triggerflow-playbook`
- complex planning, concurrency management, or mixed sync-and-async orchestration -> `agently-triggerflow-playbook`
- direct scoring, rubric checks, validator-model review, or pass-fail reports inside the request domain -> `agently-model-request-playbook` then `agently-eval-and-judge`
- transport exposure around an existing backend -> add `agently-fastapi-helper`
