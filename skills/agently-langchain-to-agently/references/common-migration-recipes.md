# Common Migration Recipes

## 1. `create_agent(model, tools=[...])`

Typical Agently target:

- `agently-model-request-playbook`
- `agently-tools`

Then route into:

- `agently-model-setup`
- `agently-input-composition`

## 2. `create_agent(..., response_format=Schema)`

Typical Agently target:

- `agently-model-request-playbook`
- `agently-output-control`

If the source relies on provider-native structured output or strategy choice:

- also add `agently-model-setup`

## 3. Agent with short-term memory or thread continuity

Typical Agently target:

- `agently-model-request-playbook`
- `agently-session-memo`

## 4. `create_agent(..., middleware=[...])` with guardrails

Typical Agently target:

- `agently-model-request-playbook`

Then split the behavior into:

- request shaping or provider control
- output constraints
- tool policy
- workflow-level approval or escalation

Common target skills:

- `agently-model-setup`
- `agently-input-composition`
- `agently-output-control`
- `agently-tools`
- `agently-triggerflow-playbook`

## 5. `HumanInTheLoopMiddleware(...)` with approval or resume

Typical Agently target:

- `agently-triggerflow-interrupts-and-stream`
- `agently-triggerflow-playbook`

Add:

- `agently-tools` if approval gates tool execution
- `agently-session-memo` if conversation continuity must survive outside the paused workflow

## 6. Agent with retrieval

Typical Agently target:

- `agently-model-request-playbook`
- `agently-knowledge-base-and-rag`

## 7. Agent exposed through FastAPI

Typical Agently target:

- whichever skill owns the backend logic
- `agently-fastapi-helper`

## 8. LangChain handoff or specialist pattern

Typical Agently target:

- `agently-multi-agent-patterns`

Add `agently-triggerflow-playbook` if the source design depends on explicit long-running orchestration rather than only specialist agent roles.
