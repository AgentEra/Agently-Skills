# Reliability And Retries

This page covers `ensure_keys` and the retry behavior used for higher-reliability structured output.

## 1. Where Reliability Control Happens

Reliability control is implemented in `ModelResponseResult.async_get_data(...)`, not in the prompt-definition layer itself.

That means:

- `.output(...)` defines the desired structure
- `ensure_keys` verifies whether the parsed result actually contains the required paths
- retries happen only after Agently has a parsed result to inspect

## 2. `ensure_keys`

Use `ensure_keys` when some fields must exist before the result is considered acceptable.

Example:

```python
result = (
  agent
  .input("Summarize this repo.")
  .output({
    "summary": (str, "Short summary"),
    "risks": [(str, "Risk item")],
  })
  .start(
    ensure_keys=["summary", "risks[*]"],
    max_retries=2,
  )
)
```

## 3. Path Styles

Supported path styles:

- `dot`: `final.steps`, `resources[*].title`
- `slash`: `/final/steps`, `/resources/[*]/title`

Use `key_style` to match the path format you write.

## 4. Retry Behavior

When `type="parsed"` and `ensure_keys` is provided:

1. Agently parses the structured result
2. it checks each required path
3. if any required path is missing, it creates a fresh `ModelResponse` and retries the request
4. this continues until the required keys are present or the retry limit is reached

This is a real re-request, not a second parse of the same failed result.

## 5. `max_retries`

`max_retries` controls how many retry attempts Agently will make after the first failed attempt.

Practical guidance:

- keep it low for normal UX
- increase it only when the result structure is critical and the extra cost is acceptable

## 6. `raise_ensure_failure`

If retries are exhausted:

- `True` -> raise an exception
- `False` -> return the last parsed result even though required keys are still missing

Use `False` when partial output is still useful.

Use `True` when downstream code must not continue with an incomplete structure.

## 7. `get_data_object()` With `ensure_keys`

`get_data_object(ensure_keys=...)` first runs the same reliability check path, then builds and returns the dynamic Pydantic object.

Use this when:

- you need both key enforcement and object-style access

## 8. What `ensure_keys` Does Not Do

- it does not guarantee correctness of field values
- it does not force streaming events to appear earlier
- it does not repair a bad prompt design automatically
- it does not apply to non-structured text output

## 9. Common Reliable Patterns

### Required object keys

```python
ensure_keys=["summary", "decision"]
```

### Required nested fields

```python
ensure_keys=["final.steps", "final.next_action"]
```

### Required fields on every list item

```python
ensure_keys=["resources[*].title", "resources[*].url"]
```

## 10. Common Mistakes

- using `ensure_keys` without a structured JSON output schema
- writing the wrong path style for the chosen `key_style`
- requiring too many brittle fields when only a few business-critical keys matter
- assuming retries reuse the same failed response instead of issuing a new request
