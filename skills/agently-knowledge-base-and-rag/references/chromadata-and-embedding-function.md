# ChromaData And Embedding Function

Use this page when the higher-level `ChromaCollection(..., embedding_agent=...)` path is not enough.

## 1. `ChromaEmbeddingFunction`

Use `ChromaEmbeddingFunction(embedding_agent=...)` when a lower-level Chroma client expects an embedding function object.

Treat the returned value as a Chroma-compatible embedding payload rather than assuming each row is a plain Python list.

## 2. `ChromaData`

Use `ChromaData(...)` when you want a prepared Chroma-style add payload from Agently-side data before sending it into a lower-level collection API.

## 3. Selection Rule

- ordinary Agently KB/RAG flow -> `ChromaCollection`
- already operating closer to native Chroma APIs -> `ChromaEmbeddingFunction` or `ChromaData`
