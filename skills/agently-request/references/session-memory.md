# Agently Session Memory

Use this reference when request/session continuity or durable long-term memory
is the main design problem.

## Ownership

- `Session` owns chat history, active context-window projection, memo,
  memory-plugin attachment, and import/export.
- `SessionMemory` owns extraction/recall behavior for a session.
- `RecordStore` owns durable memory records, scopes, retrieval indexes, and
  storage providers.
- `TaskContext`/`ContextReader` own broader per-task information assembly from
  memory, Skills, files, records, and direct entries.
- TriggerFlow execution state owns workflow progression; Session memory is not a
  substitute for it.

## Usage

```python
agent = Agently.create_agent("support").use_record_store(
    "./support-memory",
    mode="read_write",
)
agent.activate_session(session_id="customer-42")
session = agent.activated_session
assert session is not None
session.use_memory(mode="AgentlyMemory")
```

For a standalone Session, pass the storage owner explicitly:

```python
from agently.core import RecordStore, Session

record_store = RecordStore("./support-memory", mode="read_write")
session = Session()
session.use_memory(mode="AgentlyMemory", memory_store=record_store)
```

The local RecordStore materializes lazily at
`./support-memory/.agently/records/records.db`. No TaskWorkspace is created or
required for record-only memory.

`GLOBAL_MEMORY` shares the configured RecordStore scope. `SESSION_MEMORY` also
uses the active session id. Applications that need user, tenant, or project
isolation must set and enforce those scopes at the RecordStore boundary.

Configure extraction and retrieval under `session.memory.AgentlyMemory.*`.
Enable vector indexing only when real vector writes/queries are required:

```python
agent.set_settings("record_store.vector_index.enabled", True)
```

Memory extraction, summarization, query planning, prose relevance, and rerank
are model-owned semantic work. Host code validates shape, applies scopes,
persists records, enforces budgets, and records diagnostics. Do not replace
semantic recall with keyword routing.

## Anti-Patterns

- Keeping restart-sensitive memory only in process globals.
- Using Session as workflow orchestration state.
- Creating a TaskWorkspace solely to store memory records.
- Putting general RecordStore retrieval or ContextReader policy inside the
  SessionMemory plugin.
- Enabling vector infrastructure for record-only memory flows.

## Read Next

- `knowledge-base.md`
- `prompt-management.md`
