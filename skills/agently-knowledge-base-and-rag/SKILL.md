---
name: agently-knowledge-base-and-rag
description: Use only when the main task is Agently's Chroma-backed knowledge-base or retrieval-to-answer path, including `ChromaCollection`, embedding-agent-backed indexing, collection `add(...)` and `query(...)`, query-to-`info(...)` answer flow, lower-level `ChromaData` or `ChromaEmbeddingFunction`, or process-level KB reuse.
---

# Agently Knowledge Base And RAG

This skill is the direct leaf for Agently's current Chroma-backed KB/RAG path after the user already knows the task is retrieval and answer grounding rather than plain vector generation. It focuses on embedding-agent-backed indexing, Chroma collection usage, retrieval, and the common pattern of injecting retrieval results into a normal request. It does not attempt to document generic vector-database strategy outside Agently's current Chroma integration surface.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- `ChromaCollection`
- embedding-agent-backed indexing
- `add(...)`, `query(...)`, and `query_embeddings(...)`
- query results injected through `info(...)`
- lower-level `ChromaData` or `ChromaEmbeddingFunction`
- process-level reuse of one knowledge base across many requests

Do not use this skill for:

- plain embeddings requests without a knowledge base
- generic vector-database choices outside the current Chroma integration
- TriggerFlow workflow orchestration as the main problem
- service architecture as the main problem

## Workflow

1. Start with [references/chromacollection-basics.md](references/chromacollection-basics.md) when building or querying a collection.
2. Read [references/retrieval-to-answer.md](references/retrieval-to-answer.md) when turning retrieval results into a normal answer flow.
3. Read [references/process-lifecycle.md](references/process-lifecycle.md) when the real-world issue is build-once reuse or long-lived service behavior.
4. Read [references/chromadata-and-embedding-function.md](references/chromadata-and-embedding-function.md) when integrating with a lower-level Chroma client or precomputed data objects.
5. If the task is only about embedding vectors, switch to `agently-embeddings`.
6. If the task becomes flow orchestration or long-running agent loops, switch to `agently-triggerflow-playbook`.
7. If behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

Agently's current knowledge-base pattern is:

1. build or connect a Chroma collection
2. use an embedding agent to index documents
3. query the collection with a user question
4. inject retrieval results into a normal agent request
5. answer with retrieval context

The retrieval layer and the answer layer are separate on purpose.

## Selection Rules

- just need embeddings -> `agently-embeddings`
- need a retrievable document collection -> `ChromaCollection`
- need lower-level Chroma integration objects -> `ChromaData` or `ChromaEmbeddingFunction`
- retrieval results should guide a normal answer request -> query then inject through `info(...)`
- knowledge base should be reused across turns or requests -> build once and keep the collection outside the request loop

## Important Boundaries

- this skill documents Agently's current Chroma-backed KB/RAG path, not generic vector-database architecture
- retrieval should stay separate from final answering so the answer request can still use normal Agently prompt and output control
- process-level reuse matters in real services; avoid rebuilding the whole collection on every turn when the corpus is stable

## References

- `references/source-map.md`
- `references/chromacollection-basics.md`
- `references/retrieval-to-answer.md`
- `references/process-lifecycle.md`
- `references/chromadata-and-embedding-function.md`
- `references/troubleshooting.md`
