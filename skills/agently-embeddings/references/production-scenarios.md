# Production Scenarios

This page covers the two most common real-world embeddings workloads.

## 1. Offline Indexing Or Backfill

This is the pattern for:

- initial corpus ingestion
- re-indexing after chunking changes
- scheduled backfill jobs

Recommended flow:

1. split documents into the chunks your retrieval system will actually use
2. keep source ids and chunk ids outside the embeddings request so vectors can be written back correctly
3. batch chunks that belong to one embeddings job into one `input([...])` request
4. if many jobs still remain, run those jobs concurrently with `async_start()` or `async_get_data()`
5. persist vectors together with the metadata your vector store needs

Prefer batch-first, then async concurrency.

## 2. Online Query Embedding

This is the pattern for:

- user search queries
- retrieval requests inside an API
- low-latency question answering paths

Recommended flow:

1. embed the current query as one short request
2. hand the vector to the vector store immediately
3. keep the path latency-oriented instead of waiting to assemble unrelated user queries into large batches

If the service is async, prefer `await async_start()` even for one query so the request path stays non-blocking.

## 3. Mixed Systems

Many systems need both:

- offline indexing for documents
- online query embedding for retrieval

In that case:

- keep the model choice compatible between indexing and querying
- treat indexing throughput and query latency as two different workloads
- do not force the online path to look like the offline path

## 4. Vector-Store Handoff Boundary

Agently embeddings stop at vector generation and embedding-agent handoff.

Chunking policy, document ids, write-back strategy, and retrieval ranking still belong to the application or vector-store layer.
