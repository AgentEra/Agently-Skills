# ChromaCollection Basics

Use this page when the main problem is building or querying the collection itself.

## 1. Create The Collection

The most common path is:

- create an embedding agent
- create `ChromaCollection(collection_name=..., embedding_agent=...)`

Key knobs include:

- `collection_name`
- `conn`
- `metadata`
- `get_or_create`
- `hnsw_space`

## 2. Add Documents

Use `add(...)` with documents that typically include:

- `document`
- optional `metadata`
- optional `id`

## 3. Query The Collection

Use:

- `query(...)`
- `query_embeddings(...)`

Common knobs:

- `top_n`
- `where`
- `where_document`
- `distance`

Use `distance` when the application should reject weak matches instead of always returning the top `n`.
