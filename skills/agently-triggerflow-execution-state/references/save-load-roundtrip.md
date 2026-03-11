# Save And Load Roundtrip

This page covers the standard execution-state roundtrip.

## 1. In-Memory Roundtrip

Typical sequence:

1. start or create an execution
2. save the state to a dictionary
3. create a fresh execution
4. load the saved state
5. continue or read the result

## 2. File Roundtrip

`save(path)` supports JSON or YAML by file suffix.

Use this when:

- the state must survive process restart
- the restore path loads from a saved file

## 3. String Roundtrip

`load(...)` can also restore from:

- JSON string
- YAML string

Use this when:

- state is transported over a queue or API
- the caller already owns the serialized content in memory

## 4. Ready Result Roundtrip

Execution state can restore an already-ready final result.

This means:

- `load(...)` may restore an execution that no longer needs continuation
- the caller can directly read the result afterward
