# Output Schema

This page explains how `.output(...)` works in Agently and what kinds of schema shapes it supports.

## 1. What `.output(...)` Actually Does

`.output(...)` writes the prompt slot named `output`.

That output slot is then used by the prompt generator to:

- infer the output format
- include a structured output requirement in the generated prompt
- build a dynamic Pydantic output model for parsed structured results

The entry point lives in `ModelRequest.output(...)`.

## 2. Output Format Inference

Current `PromptModel` behavior:

- mapping or sequence output -> `output_format = "json"`
- plain string-like output guidance -> `output_format = "markdown"`
- `output == str` is treated as non-structured text output, not as a structured JSON field

Default advice:

- if the user wants machine-readable data, always use a mapping or list schema
- do not rely on plain text output when the next step needs parsed fields

## 3. Supported Schema Shapes

### Object output

```python
.output({
  "summary": (str, "Short summary"),
  "risks": [(str, "Risk item")],
})
```

Use this for named fields.

### Nested object output

```python
.output({
  "plan": {
    "goal": (str, "Goal"),
    "steps": [(str, "Step")],
  }
})
```

Use this for hierarchical structures.

### List output

```python
.output([
  {
    "title": (str, "Title"),
    "url": (str, "URL"),
  }
])
```

Use this when the full output is a list rather than an object.

### Leaf tuple form

Leaf fields commonly use tuples:

- `(type,)`
- `(type, "description")`
- `(type, "description", default_value)`

Examples:

```python
"answer": (str,)
"score": (int, "Confidence score")
"done": (bool, "Whether the task is complete", False)
```

## 4. Practical Schema Rules

- use a mapping when downstream code needs stable field names
- use a list when the entire output is one collection
- use tuple leaves to tell the model the expected type and intent of a field
- keep field names stable and implementation-friendly
- avoid schema designs that require downstream code to guess whether a field is text, object, or list

## 5. Dynamic Output Model

For structured JSON output, Agently generates a dynamic Pydantic model from the schema.

That is what enables:

- parsed structured data via `get_data()`
- object access via `get_data_object()`
- incremental structured streaming through `instant` / `streaming_parse`

## 6. Field Order

The schema order is preserved through prompt generation and is also used by the structured streaming parser when tracking expected field order.

This is an actual control surface in Agently, not a cosmetic detail.

Practical recommendation:

- if one field depends on another, place the prerequisite field earlier in the schema
- if the user wants staged planning or CoT-like control, put intermediate fields before the final answer field
- for example, put `prethinking` before `reply`

For the full rule set, read [order-and-dependencies.md](order-and-dependencies.md).

## 7. Common Mistakes

- using plain text output when parsed structured data is required
- asking for a list in natural language but defining a single string field
- using unstable field names that later code cannot safely reference
- assuming `get_data_object()` is available for non-structured output
