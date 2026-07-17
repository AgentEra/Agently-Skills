# Agently Knowledge and Retrieval

Use this reference when records, embeddings, vector search, retrieval, or
retrieval-backed answers are the main capability surface.

## Ownership

- `RecordStore` owns record DB, indexes, embedding/vector providers,
  deterministic filters, retrieval packages, links, and durable refs.
- `TaskWorkspace` owns files and file grep/readback. It is not a record/vector
  store.
- `RecordStoreContextSource` and other ContextSource adapters expose source
  candidates to a TaskContext.
- `ContextReader` owns cross-source intent/consumer/phase-specific progressive
  disclosure and budgeting.
- The model owns prose relevance, rerank judgment, citation choice, and answer
  synthesis; host code owns offered-key validation and canonical rejoin.

## RecordStore Retrieval

```python
from agently.core import RecordStore

record_store = RecordStore(
    "./knowledge-state",
    mode="read_write",
    db_store_provider="sqlite",
    embedding_provider=embed_texts,
    vector_store_provider="auto",
)

ref = await record_store.put(
    {"title": "Refund policy", "body": "Refunds require a receipt."},
    collection="policies",
    kind="policy",
    summary="Receipt requirement for refunds",
    scope={"tenant_id": "demo"},
    vector=True,
)

package = await record_store.retrieve(
    "What evidence is required for a refund?",
    filters={"collection": "policies", "kind": "policy"},
    scope={"tenant_id": "demo"},
    method="auto",
)
```

Keep candidate retrieval and semantic rerank separate. `method="auto"` may
choose an available deterministic/vector strategy; it does not make semantic
rerank mandatory. If required embedding/vector providers are unavailable,
surface diagnostics and use the documented deterministic fallback rather than
silently claiming vector retrieval.

The local default uses SQLite for records. `vector_store_provider="auto"` uses
Chroma when available and initialized, otherwise the SQLite vector table.
`DBStoreProvider`, `EmbeddingProvider`, and `VectorStoreProvider` are separate
replaceable seams.

Use `get_data(...)` for raw record readback, `links(...)` for record lineage,
and bounded retrieval packages for later model/context consumers. Keep full
raw/audit records cold.

## Progressive Disclosure

Attach records to a TaskContext instead of copying every record into a prompt:

```python
from agently.core import TaskContext
from agently.core.storage import RecordStoreContextSource
from agently.types.data import ContextBudget, ContextReadIntent

task_context = TaskContext("refund-review")
task_context.attach(
    RecordStoreContextSource(record_store),
    binding_id="policy-records",
)
reader = task_context.reader(
    consumer="model_request:refund-review",
    phase="evidence",
    budget=ContextBudget(max_chars=6000, max_blocks=12),
)
context_package = await reader.async_read(
    ContextReadIntent(query="refund receipt requirement")
)
```

Each ContextReader pins a TaskContext/source revision. Create/refresh a reader
after the source aggregate changes. Optional prose relevance requires a semantic
selector; never fall back to keyword routing as the semantic owner.

## Retrieval Reference Rendering

Keep source records host-side. Project one short trusted `ref_id` plus relevant
title/snippet facts, and require `[[ref:<ref_id>]]`, for example
`[[ref:r2]]`. Validate every token against the offered map, then render safe
links/labels and application-approved source cards or a hover card host-side.

Do not use bare `${ref_id}` because `${...}` belongs to Agently prompt/TaskDAG
placeholders. Do not ask the model to reproduce URLs or full source metadata.
The citation token protocol is deterministic transport; it does not decide
source relevance or answer quality. Treat `cite_as` only as a view-level
compatibility alias, never canonical source identity.

## Files and Records

Use TaskWorkspace `grep_files`/`read_file` for deterministic file discovery and
bounded readback. Use RecordStore `retrieve` for records. When a task needs both,
attach both source adapters to one TaskContext and let ContextReader package the
consumer-specific result.

## Anti-Patterns

- Hiding retrieval inside unrelated prompt formatting.
- Treating vector hits or keyword matches as final semantic relevance.
- Asking the model to copy canonical ids, URLs, or full retrieval metadata.
- Mixing task file editing with record/vector persistence.
- Recreating ContextBuilder or a generic Workspace instead of composing
  RecordStore, ContextSource, TaskContext, and ContextReader.
