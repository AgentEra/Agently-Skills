# Vector-Store Handoff

This page covers the handoff point between an embeddings agent and a vector-store integration.

## 1. The Handoff Pattern

Agently can use an embeddings agent as the embedding function for Chroma integration.

Typical pattern:

```python
embedding = Agently.create_agent()
embedding.set_settings(
    "OpenAICompatible",
    {
        "model": "...",
        "base_url": "...",
        "model_type": "embeddings",
    },
)
```

Then hand it to the integration:

- `ChromaCollection(..., embedding_agent=embedding)`
- `ChromaEmbeddingFunction(embedding_agent=embedding)`

## 2. What The Integration Actually Calls

The integration path ultimately uses the embedding agent like this:

```python
embedding_agent.input(texts).start()
```

That is why the embeddings skill stops at:

- configuring the embedding agent
- sending one text or a batch of texts
- returning parsed vector lists

## 3. What This Skill Does Not Cover

This skill does not try to teach:

- chunking strategy
- retrieval thresholds
- ranking and reranking
- answer-generation prompts
- full knowledge-base lifecycle

Those are separate workflow concerns.

## 4. Practical Advice

- validate the embedding agent first
- confirm the returned vector shape and batch behavior
- only then wire it into the vector-store integration

If the user is blocked before vectors are returned, stay in the embeddings skill.

If the embeddings agent already works and the next problem is retrieval workflow design, that is outside this skill.
