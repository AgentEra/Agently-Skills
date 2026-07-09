# Agently Knowledge Base

Use this skill when embeddings, Workspace recall, and retrieval are the main
capability surface.

## Native-First Rules

- prefer embedding-agent plus Chroma integration before custom vector plumbing
- use `workspace.retrieve(...)` for shared intelligent retrieval over Workspace
  records and files: keyword/tag candidates, `method="auto"` candidate-strategy
  selection, optional vector/hybrid mode,
  structure-gated model rerank over a bounded candidate-summary window,
  dropped-candidate refill, length-budget or `top_n` packaging, and compact
  selected-record representation packaging with `projection`/`original_ref`
  metadata. Default `record_representation="auto"` preserves short structured
  records as compact structure, omits cold fields such as `audit`,
  `source_system`, `tags`, and `noise` from the model-hot package, projects
  long/noisy records, and leaves raw Workspace records available for readback
- for multi-turn task information already stored in Workspace, prefer
  `workspace.build_context(goal=..., scope=..., budget=..., profile=...)` so
  ContextPlanner, Retriever, and ContextBuilder plugins own the retrieval path
- use `workspace.grep(...)` and `workspace.grep_files(...)` for low-level
  deterministic debugging or explicit filters, not as the normal app-facing
  recall API. `workspace.search(...)` and `workspace.search_files(...)` keep
  compatibility return shapes while automatically choosing deterministic grep
  or retrieval packaging internally
- keep candidate retrieval strategy and rerank separate. `method="auto"` chooses
  keyword versus hybrid from Workspace retrieval policy; `rerank=None` uses the
  structural rerank gate and does not become mandatory just because embeddings
  are configured
- if vector mode is requested without both an `EmbeddingProvider` and a
  `VectorStoreProvider`, expect deterministic fallback plus diagnostics such as
  `embedding_provider_unavailable` or `vector_store_unavailable` rather than
  silent failure
- the default local Workspace backend uses `db_store_provider="sqlite"` for the
  record DB and `vector_store_provider="auto"` for vector storage: Chroma is
  used when available and initialized successfully, otherwise Workspace falls
  back to a SQLite vector table. Record DB adapters attach through
  `db_store_provider`, embedding clients attach through `embedding_provider`,
  and vector storage attaches through `vector_store_provider`. Lower-capability
  `DBStoreProvider` implementations keep the same protocol surface and return
  empty/absent values for unsupported advanced features. `LocalVectorIndex(embedder)`
  remains only as a compatibility adapter for older code that combines
  embedding and local vector scoring
- use `workspace.get_data(...)` for structured records/checkpoints and
  `workspace.links(...)` for decision/evidence lineage when retrieval feeds a
  later loop step
- separate indexing, retrieval, and answer generation concerns
- keep retrieval results explicit when they feed a later request

## Anti-Patterns

- do not hide KB retrieval inside unrelated prompt logic
- do not treat embeddings-only setup and KB-backed answer flow as unrelated stacks
- do not ask business code to hand-write ordinary multi-turn recall filters when
  a Workspace ContextPackage is the right shape
- do not hide structure-gated model rerank, refill, or retrieval budgets inside
  Session memory code when `workspace.retrieve(...)` is the shared substrate

## Read Next

- `references/session-memory.md`
- `references/prompt-management.md`
