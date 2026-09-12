# LlamaIndex to Agently

Use this map for LlamaIndex agents, RAG/data components, storage, or Workflows.
Do not assume that replacing the final query call also migrates ingestion,
indexing, source identity, or workflow behavior.

## Verify the Source Contract

Current official references separate the framework's agent, data, and workflow
surfaces:

- [Agents](https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/)
- [Loading data](https://developers.llamaindex.ai/python/framework/module_guides/loading/)
- [Indexing](https://developers.llamaindex.ai/python/framework/module_guides/indexing/)
- [Querying](https://developers.llamaindex.ai/python/framework/module_guides/querying/)
- [Agent Workflows](https://developers.llamaindex.ai/python/llamaagents/workflows/)

LlamaIndex's older Query Pipeline is feature-frozen in favor of Workflows. Do
not preserve a deprecated pipeline abstraction as a new Agently owner; map the
behavior to ModelRequest, context/storage, Actions, or TriggerFlow.

## Source-to-Owner Map

| LlamaIndex source | Agently target | Preserve |
|---|---|---|
| LLM/prompt/structured prediction | `agently-request` ModelRequest and output control | Prompt facts, schema, validation, model/provider behavior. |
| Agent + tools | AgentExecution/AgentTask plus ActionRuntime | Autonomy boundary, tool schemas, observed tool evidence, memory, and terminal result. |
| Reader/data connector | Existing connector behind a host ingestion step or Action | Source authorization, incremental sync, document identity, metadata, and failure behavior. |
| Document/node transforms | Host-owned ingestion/transformation code | Deterministic chunk identity, metadata, ordering, and reproducibility. |
| Index/vector store/doc store | RecordStore only when its contract fits; otherwise retain the existing store behind an adapter | Durability, filters, namespaces, embedding model/revision, update/delete semantics. |
| Retriever/router/postprocessor | RecordStore retrieval or a ContextSource/Action adapter plus model-owned structured rerank where needed | Candidate set, scores, filters, semantic selection, and exact source readback. |
| Query engine/response synthesizer | ContextReader-delivered evidence followed by ModelRequest synthesis | Source attribution, response mode, streaming, and final answer contract. |
| Chat engine/memory | Session / SessionMemory, optionally backed by RecordStore | Conversation scope, compression, persistence, and isolation. |
| Workflow step/event/state | TriggerFlow chunk/signal/execution state | Branches, loops, concurrency, waits, streamed events, and terminal behavior. |
| Workflow resource | ExecutionResource or host-owned dependency injection | Live lifetime, health, secrets, reconstruction, and cleanup. |

## Data Migration Is a Separate Decision

Do not describe RecordStore as a drop-in replacement for every LlamaIndex
index, vector database, managed service, graph store, or query engine. First
decide whether the user wants:

1. orchestration/agent migration while retaining the current retrieval system;
2. an adapter that exposes existing retrieval as a ContextSource or Action; or
3. actual data/index migration into a supported RecordStore provider.

For an adapter, project compact descriptors and host-issued refs, then read
canonical bodies through the source. For a store migration, preserve tenant
scope, document/node ids, metadata, deletes, embedding model and dimensions,
index revision, and rebuild/checkpoint behavior. Compare recall and grounded
answer quality on representative queries; row counts are insufficient.

## Semantic Retrieval and Citations

Deterministic/vector retrieval may produce candidates, but prose relevance,
rerank, and synthesis remain model-owned. Use bounded structured ModelRequest
output rather than keyword routing. Give the model one trusted short ref per
candidate and rejoin canonical source records host-side.

For final answers, preserve the source contract: exact source readback,
application-approved citation tokens/cards, and diagnostics for unavailable or
omitted sources. Do not ask the model to copy URLs, vector-store ids, or full
metadata.

## Workflow Migration

Map typed Workflow events to TriggerFlow signals and per-run Context/state to
execution state. Preserve fan-out/join cardinality, branch and loop terminal
conditions, external input, streamed events, and resource cleanup. Use a later
ModelRequest whenever a step needs retrieval/tool/host output produced after an
earlier model dispatch.

Do not wrap a single query engine call in TriggerFlow. Conversely, do not
flatten a multi-step LlamaIndex Workflow with concurrency, human input, or
durable resume into one request.

## Minimum Comparison

Compare source and target on ingestion/update/delete, representative retrieval
queries, exact source readback, grounded final answers, citations, agent tool
calls, workflow branches/joins, streaming, failure, and restart behavior. Label
any retained LlamaIndex component and external managed service as an explicit
source boundary rather than implying full replacement.
