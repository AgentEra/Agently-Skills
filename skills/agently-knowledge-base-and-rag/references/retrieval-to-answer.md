# Retrieval To Answer

Use this page when the main question is how retrieval should influence the final answer.

## 1. Standard RAG Shape

The common Agently pattern is:

1. query the collection with the user question
2. inject retrieved results into `info(...)`
3. answer with a normal agent request

This keeps retrieval and answer generation separate and inspectable.

## 2. Why This Split Matters

The separation helps because:

- retrieval can be logged and inspected independently
- prompt design stays explicit
- output control still works as usual on the answer request

## 3. Common Prompt Shape

Use retrieval results as context, not as hidden implicit state.

Typical request structure:

- `input(question)`
- `info({"retrieval_results": results})`
- `instruct("Answer based on {retrieval_results}.")`
