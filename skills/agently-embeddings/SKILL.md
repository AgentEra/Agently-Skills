---
name: agently-embeddings
description: Use only when the main task is direct Agently embeddings request setup and vector consumption through OpenAICompatible, including `model_type="embeddings"`, single or batch `input(...)`, parsed vector results, async embedding calls, or embedding-agent handoff.
---

# Agently Embeddings

This skill is the direct leaf for embeddings requests after the user already knows the task is vector generation rather than a retrievable knowledge base or answer-generation flow. It focuses on `OpenAICompatible` embeddings setup, request shape, input batching, async usage, parsed vector results, and the embedding-agent handoff used by vector-store integrations. It does not choose between plain embeddings and KB/RAG orchestration, and it does not cover general chat/completions setup, structured output control, prompt-template management, or full retrieval pipeline design.

Prerequisite: Agently `>= 4.0.8.5`.

Agently is async-first at the runtime layer. Prefer `async_start()` or `async_get_data()` when the caller can use async APIs. Use batching first for texts that belong to one embeddings job, then use async concurrency for overlapping embedding jobs.

## Scope

Use this skill for:

- configuring `OpenAICompatible` with `model_type="embeddings"`
- choosing between `base_url`, `full_url`, auth, proxy, timeout, `client_options`, and `request_options` for embeddings
- understanding that embeddings requests are built from `input`, not from chat-style prompt assembly
- sending one text or a batch of texts through `input(...)`
- understanding how non-scalar input is serialized before it is sent
- consuming parsed embedding vectors through `start()`, `get_data()`, `async_start()`, or `async_get_data()`
- understanding the parsed result shape for single-input and batch-input requests
- using an embedding agent as the handoff point for vector-store integrations such as Chroma
- organizing offline indexing or backfill jobs
- organizing low-latency online query embedding

Do not use this skill for:

- Chat LLM, Completions LLM, or VLM setup
- `.output(...)`, `ensure_keys`, or structured-output retries
- prompt-slot composition beyond the embeddings `input`
- retrieval ranking, knowledge-base orchestration, or answer-generation logic
- full Chroma or RAG workflow design

## Minimal Request Boundary

For embeddings, `input(...)` is the real payload.

`info(...)`, `instruct(...)`, `examples(...)`, `output(...)`, and `attachment(...)` are not the request body for the `embeddings` model type.

## Workflow

1. If the task is about model type, endpoint shape, or which settings matter for embeddings, read [references/config-and-request-shape.md](references/config-and-request-shape.md).
2. If the task is about single input, batch input, async usage, or throughput guidance, read [references/input-batching-and-async.md](references/input-batching-and-async.md).
3. If the task is about what the returned data looks like or which getter to use, read [references/result-shape-and-consumption.md](references/result-shape-and-consumption.md).
4. If the task is about offline indexing, backfill jobs, or online query embedding, read [references/production-scenarios.md](references/production-scenarios.md).
5. If the task is about passing an embedding agent into a vector-store integration, read [references/vector-store-handoff.md](references/vector-store-handoff.md).
6. If behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

Agently embeddings are simpler than chat or completions requests:

1. `OpenAICompatible` must use `model_type="embeddings"`.
2. The request body is built from `input(...)`.
3. A single input becomes one embeddings request; a list input becomes one batch embeddings request.
4. Parsed result data is a list of embedding vectors.
5. Embeddings are not a streaming-response workflow. Treat the `stream` parameter as irrelevant for this model type.
6. The same embedding agent can then be reused as the embedding function for vector-store integrations.

## Selection Rules

- embedding endpoint setup or request-body shape -> `config-and-request-shape.md`
- one text or one list of texts -> `input(...)`
- many texts that belong to the same embedding job -> batch them in one request first
- async service or overlapping embedding jobs -> prefer `async_start()` / `async_get_data()`
- normal embedding result consumption -> `start()` or `get_data()`
- meta or original payload inspection -> `get_response()` first, then read from `response.result`
- embeddings always return one completed result rather than `delta` / `instant` streaming events
- offline indexing or backfill -> batch within one job first, then overlap jobs with async concurrency
- online query embedding -> prefer one short request per user query and keep the path latency-oriented
- vector-store handoff -> `vector-store-handoff.md`
- do not treat `.output(...)` or `get_data_object()` as the normal embeddings path

## References

- `references/source-map.md`
- `references/config-and-request-shape.md`
- `references/input-batching-and-async.md`
- `references/production-scenarios.md`
- `references/result-shape-and-consumption.md`
- `references/vector-store-handoff.md`
- `references/troubleshooting.md`
