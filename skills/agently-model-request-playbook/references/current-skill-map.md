# Current Model-Request Skill Map

This page lists the current public model-request-side skills in this repository and what each one owns.

## `agently-model-setup`

Use for:

- provider setup
- endpoint/auth/proxy/timeout
- request options
- minimal connection verification

## `agently-input-composition`

Use for:

- prompt slots
- request-vs-agent prompt layering
- mappings
- attachments
- low-level chat history as input context

## `agently-output-control`

Use for:

- output schema
- retries and `ensure_keys`
- response consumption
- structured streaming
- response reuse

## `agently-eval-and-judge`

Use for:

- rubric scoring
- pass or fail checks
- issue lists and review reports
- validator-model prompts
- generator versus judge boundaries

## `agently-embeddings`

Use for:

- embeddings model requests
- batch embedding
- async embedding jobs
- offline indexing and online query embedding

## `agently-tools`

Use for:

- local tools
- built-in tools
- tool loop
- custom plan or execution handlers
- tool logs

## `agently-mcp`

Use for:

- MCP server tools
- MCP transport registration
- MCP schema mapping
- agent-scoped MCP visibility

## `agently-knowledge-base-and-rag`

Use for:

- Chroma-backed KB/RAG
- retrieval
- retrieval-to-answer path
- process-level KB reuse

## `agently-session-memo`

Use for:

- session continuity
- context window
- memo
- restore after restart

## `agently-prompt-config-files`

Use for:

- YAML/JSON prompt config
- mappings
- prompt export/import
- `.alias`

## `agently-fastapi-helper`

Use for:

- FastAPIHelper
- POST/GET
- SSE
- WebSocket
- wrapped helper responses

## `agently-multi-agent-patterns`

Use for:

- deciding whether the problem should stay one request or become a specialized agent team
- planner-worker or supervisor-router patterns
- parallel experts and synthesizer
- reviewer-reviser design
- generator-judge specialist design
- agent handoff contracts and ownership boundaries

## Escalation

When a request is no longer just one request, route to:

- `agently-multi-agent-patterns`
- `agently-triggerflow-playbook`

Typical TriggerFlow escalation signals:

- draft -> judge -> revise loops
- reflection or self-check stages with explicit budgets
- several model requests whose order matters for quality
