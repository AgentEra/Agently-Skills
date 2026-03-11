# Troubleshooting

- The real task is just embedding vectors:
  Switch to `agently-embeddings`.
- The collection gets rebuilt every request and the service feels slow:
  Keep collection initialization outside the request loop.
- The main problem has become workflow design rather than retrieval:
  Switch to `agently-triggerflow-playbook`.
- The issue is the vector store itself rather than Agently's integration shape:
  Treat it as a Chroma-side or storage-side problem first.
