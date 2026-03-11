# Input, Batching, And Async

This page covers how to send embeddings input efficiently in Agently.

## 1. Input Is The Payload

The normal embeddings entry point is:

```python
vectors = embedding.input("hello world").start()
```

or:

```python
vectors = embedding.input(["hello", "world"]).start()
```

## 2. Single Input Versus Batch Input

Use a single scalar input when:

- the caller truly has one text to embed

Use a list input when:

- several texts belong to the same embedding job
- the provider supports batch embeddings for that workload

Batching is usually the first efficiency lever.

## 3. Non-Scalar Input

Agently sanitizes the input before building the embeddings request.

Behavior to expect:

- strings stay strings
- numbers, booleans, and `None` are converted to strings
- non-scalar values are serialized before being sent

For batch input, this rule is applied item by item.

## 4. Async-First Guidance

Agently runtime paths are async-first.

Prefer:

- `async_start()`
- `async_get_data()`

when:

- the caller already runs inside an async service
- several embeddings jobs may overlap
- request handling should stay non-blocking

Sync `start()` and `get_data()` are still valid, but they are compatibility-friendly wrappers over the async core.

## 5. Batch First, Then Async Concurrency

Use this order of preference:

1. combine texts that belong to one embeddings job into one input list
2. if independent jobs still remain, run those jobs with async concurrency

Why:

- batching reduces request count
- async concurrency helps throughput when several requests overlap

Do not oversell the async claim:

- async-first is mainly about concurrency and integration quality
- it is not a blanket promise that one isolated embeddings request has lower model latency

## 6. Practical Selection

- one local script, one text -> `start()`
- one local script, one batch of texts -> `input([...]).start()`
- async API or worker, one batch -> `await async_start()`
- async API or worker, several independent batches -> batch each request first, then run `async_start()` concurrently

## 7. Two Common Production Patterns

- offline indexing or backfill -> build batches from document chunks, then run several batches concurrently if the system still has more work
- online query embedding -> keep each user query on a short path, usually one scalar input or one very small batch

Read [production-scenarios.md](production-scenarios.md) when the task is about job design rather than raw API shape.

## 8. Provider Limits

Batch size still depends on the upstream model service.

If the provider rejects the request:

- reduce batch size
- reduce per-item input size
- split large jobs into several async batches
