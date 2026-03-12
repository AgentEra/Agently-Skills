# Common Solution Recipes

Use this page when the business requirement already resembles a common production shape.

## Plain assistant

Typical combination:

- `agently-model-request-playbook`

Then route into:

- `agently-model-setup`
- `agently-input-composition`

## Structured extraction or classification

Typical combination:

- `agently-model-request-playbook`
- `agently-output-control`

## Generator with judge or validation report

Typical combination:

- `agently-model-request-playbook`
- `agently-eval-and-judge`

Add `agently-model-setup` when the generator and validator should use different models or a local Ollama judge.
Add `agently-output-control` when the review result must be returned as stable machine-readable fields.

## Structured streaming or progressive UI feedback

Typical combination:

- `agently-model-request-playbook`
- `agently-output-control`

Use this when one request should produce user-visible feedback quickly while also feeding structured data to downstream logic.

## Tool-augmented assistant

Typical combination:

- `agently-model-request-playbook`
- `agently-tools`

Add `agently-mcp` if the tool surface should come from MCP servers instead of local tools.

## Retrieval-augmented answer

Typical combination:

- `agently-model-request-playbook`
- `agently-knowledge-base-and-rag`

## Multi-turn conversational assistant

Typical combination:

- `agently-model-request-playbook`
- `agently-session-memo`

Add `agently-prompt-config-files` when prompts should be externalized as data.

## Specialist-agent solution

Typical combination:

- `agently-multi-agent-patterns`
- `agently-output-control`

Add `agently-tools`, `agently-mcp`, `agently-knowledge-base-and-rag`, or `agently-session-memo` only for the specialist roles that really need them.
Add `agently-eval-and-judge` when one specialist owns rubric-based review or quality gates.

## Complex planning and decomposition system

Typical combination:

- `agently-multi-agent-patterns` or `agently-triggerflow-playbook`

Choose `agently-multi-agent-patterns` when the main problem is specialist ownership.
Choose `agently-triggerflow-playbook` when the main problem is workflow control, branching, waiting, persistence, or concurrency.

## Restart-safe business workflow

Typical combination:

- `agently-triggerflow-playbook`
- `agently-triggerflow-config`
- `agently-triggerflow-execution-state`

Add `agently-triggerflow-model-integration` when model calls live inside the workflow.

## Async concurrency or mixed sync-and-async orchestration

Typical combination:

- `agently-triggerflow-playbook`
- `agently-triggerflow-patterns`

Add `agently-triggerflow-state-and-resources` when worker state, shared resources, or restart-safe boundaries become important.

This solution shape still applies even when some or most workflow steps do not call a model.

## API or streaming service exposure

Typical combination:

- whichever capability actually owns the backend logic
- `agently-fastapi-helper`

Service exposure is usually not the architecture owner. It is usually the transport layer around one of the other solution shapes.
