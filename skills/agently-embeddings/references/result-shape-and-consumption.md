# Result Shape And Consumption

This page covers how Agently returns embeddings results.

## 1. Normal Result Path

The normal embeddings consumer is:

- `start()`
- `get_data()`
- `async_start()`
- `async_get_data()`

These return parsed embeddings data.

## 2. Parsed Result Shape

For OpenAI-compatible embeddings payloads, Agently extracts the provider `data[*].embedding` values.

That means the parsed result is:

- a list of embedding vectors

Example shape:

```python
[
    [0.1, 0.2, 0.3],
    [0.4, 0.5, 0.6],
]
```

## 3. Single Input Still Returns A List

Even when the input is one text, the parsed result still follows the provider-style `data` list shape.

That means a single-input call normally returns:

```python
[
    [0.1, 0.2, 0.3],
]
```

Do not assume Agently automatically unwraps it to one vector.

## 4. Order Matters

For batch input, parsed vectors follow the response order of the provider payload.

In the normal case, that means the result order should match input order.

## 5. `get_response()` When You Need More Than Parsed Vectors

Use:

```python
response = embedding.input(["a", "b"]).get_response()
```

Then consume:

- `response.result.get_data()` for parsed vectors
- `response.result.get_data(type="original")` for the raw provider payload
- `response.result.get_meta()` for metadata such as usage, finish reason, or role if the provider emitted it

Use this when one embeddings request must be inspected in more than one way.

## 6. What Not To Prefer

Do not treat these as the normal embeddings path:

- `get_text()`
- `get_data_object()`

Why:

- `get_text()` is not the main embeddings result form
- `get_data_object()` is for structured JSON output models, not embeddings vectors

## 7. Fast Selection

- parsed vectors only -> `start()` / `get_data()`
- parsed vectors in async runtime -> `async_start()` / `async_get_data()`
- original provider payload too -> `get_response()` first
- metadata or usage too -> `get_response()` first
