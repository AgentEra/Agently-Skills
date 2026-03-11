# Common Business Patterns

Use this page when the requirement starts from business language rather than API language.

## 1. Plain Q&A Or Transformation

Typical fit:

- `agently-model-setup`
- `agently-input-composition`

Use this for:

- Q&A
- rewriting
- summarization
- translation

## 2. Extraction, Classification, Or Structured Generation

Typical fit:

- `agently-model-setup`
- `agently-input-composition`
- `agently-output-control`

Use this when downstream code needs stable fields instead of only text.

## 3. Structured Streaming UI

Typical fit:

- `agently-model-setup`
- `agently-input-composition`
- `agently-output-control`

Prefer `instant` or `streaming_parse` when the UI or downstream system should receive partial structured updates before the full result is done.

## 4. Tool-Augmented Assistant

Typical fit:

- `agently-model-setup`
- `agently-input-composition`
- `agently-tools`

If the tools come from MCP instead of local Python or built-ins, add `agently-mcp`.

## 5. Retrieval-Augmented Answer

Typical fit:

- `agently-embeddings`
- `agently-knowledge-base-and-rag`
- optionally `agently-output-control`

Use this when the answer should be grounded in a retrievable corpus.

## 6. Multi-Turn Assistant

Typical fit:

- standard request skills
- `agently-session-memo`

Use this when continuity across turns matters.

## 7. Config-Driven Prompting

Typical fit:

- `agently-prompt-config-files`
- plus whatever request skill actually answers the task

Use this when prompt structure should live outside business code.

## 8. API Exposure

Typical fit:

- request skills for the core request
- `agently-fastapi-helper`

Use this when the issue is HTTP, SSE, or WebSocket exposure of the request surface.

## 9. Escalate To TriggerFlow

Escalate when the business requirement becomes:

- multi-step
- concurrent
- signal-driven
- interruptible
- resumable

Then route into `agently-triggerflow-playbook`.
