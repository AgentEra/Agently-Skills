# Concept Map

Use this page to translate LangChain agent-side concepts into the current Agently skill tree.

## `create_agent`

Nearest Agently target:

- `agently-model-request-playbook`

Then route into:

- `agently-model-setup`
- `agently-input-composition`
- `agently-output-control`

## `response_format`, `ProviderStrategy`, and `ToolStrategy`

Nearest Agently target:

- `agently-output-control`

If the source design depends on provider-native structured output support or tool-backed structured output retries:

- also add `agently-model-setup`

The practical migration target is usually explicit output schema plus provider or request design, not one direct strategy enum replacement.

## Tools

Nearest Agently target:

- `agently-tools`

If the source uses MCP-backed tools or external MCP servers:

- `agently-mcp`

## Structured output

Nearest Agently target:

- `agently-output-control`

LangChain `response_format` and strategy selection maps conceptually to Agently output schema plus response-consumption choices.

## Short-term memory

Nearest Agently target:

- `agently-session-memo`

This is about conversational continuity and memo/context-window behavior, not literal LangGraph thread/checkpointer semantics.

## Middleware or guardrails

Nearest Agently target:

- usually not one direct skill

Common Agently decomposition:

- model setup or request options -> `agently-model-setup`
- input shaping -> `agently-input-composition`
- output constraints -> `agently-output-control`
- tool policy or external capability control -> `agently-tools` / `agently-mcp`
- workflow-level approval or control -> `agently-triggerflow-playbook`

## `HumanInTheLoopMiddleware` or approval middleware

Nearest Agently target:

- `agently-triggerflow-interrupts-and-stream`

Often combined with:

- `agently-tools`
- `agently-session-memo`
- `agently-triggerflow-playbook`

## Retrieval or RAG

Nearest Agently target:

- `agently-knowledge-base-and-rag`

## FastAPI service exposure

Nearest Agently target:

- `agently-fastapi-helper`

## Handoffs or specialist agents

Nearest Agently target:

- `agently-multi-agent-patterns`

If the source design is actually a workflow with stateful routing and persistence:

- `agently-triggerflow-playbook`
