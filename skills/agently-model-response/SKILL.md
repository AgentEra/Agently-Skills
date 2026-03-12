---
name: agently-model-response
description: Use when the main task is Agently response lifecycle and consumption, including `get_response()`, `get_text()`, `get_data()`, metadata, async response APIs, and streaming consumers such as `delta`, `instant`, or `specific`.
---

# Agently Model Response

Use this skill when the output contract is already chosen and the remaining issue is how the response instance should be consumed or reused.

## Native-First Rules

- prefer `get_response()` when one request result must be consumed more than once
- prefer async response APIs in async runtimes
- use `delta`, `instant`, `specific`, or `all` instead of custom stream splitting logic

## Anti-Patterns

- do not re-issue the same request to obtain text, data, and metadata separately
- do not build ad hoc field-level stream parsers when `instant` or `streaming_parse` already fits

## Read Next

- `references/overview.md`
