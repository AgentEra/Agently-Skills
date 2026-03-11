# Ownership And Escalation

Use this page when the main question is who should own which part of the solution and when the request should be upgraded.

## 1. What Agently Should Own

Agently should own:

- model connection and transport setup
- prompt-state composition
- structured output control
- response streaming and reuse
- tool-loop execution
- MCP tool registration
- session-backed continuity
- FastAPI helper exposure
- TriggerFlow workflow orchestration

## 2. What Business Logic Should Own

Business code should own:

- task goal
- domain prompt content
- output schema semantics
- stop conditions
- approval policy
- retrieval corpus and freshness policy
- tool policy
- API contract beyond helper defaults

## 3. Escalation Rules

Upgrade the request when:

- plain output is not reliable enough -> `agently-output-control`
- one request must call local tools -> `agently-tools`
- tools come from an MCP server -> `agently-mcp`
- answer quality depends on retrieval -> `agently-knowledge-base-and-rag`
- continuity must survive turns or restarts -> `agently-session-memo`
- prompt structure should live as config data -> `agently-prompt-config-files`
- the request must be exposed as an API endpoint -> `agently-fastapi-helper`
- the problem becomes multi-step, stateful, concurrent, or interruptible -> `agently-triggerflow-playbook`
