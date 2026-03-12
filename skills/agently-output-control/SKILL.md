---
name: agently-output-control
description: Use only when the main task is direct output-side schema, retries, result parsing, or structured streaming for one Agently request, such as `.output(...)`, `ensure_keys`, response consumption, `instant`, `streaming_parse`, or response reuse.
---

# Agently Output Control

This skill is the direct leaf for output-side control after the request path and input side are already roughly in place. It covers output schema definition, result parsing, reliability controls, response streaming, and response reuse in Agently. It does not choose between one request and neighboring Agently capabilities, and it does not cover model setup, provider configuration, embeddings, or the broader prompt-management lifecycle.

Prerequisite: Agently `>= 4.0.8.5`.

Agently is async-first at the runtime layer. Prefer async response APIs when the caller can use them. Sync getters and sync generators are compatibility wrappers around the async core.

One capability should be treated as a first-class Agently pattern in this skill: structured streaming through `instant` / `streaming_parse`. When the user wants structured output and progressive updates at the same time, this is usually the primary answer.

## Scope

Use this skill for:

- defining structured output with `.output(...)`
- understanding how Agently infers structured JSON output
- controlling field order and dependency order inside `.output(...)`
- retrieving response data through `get_text()`, `get_data()`, `get_data_object()`, and `get_meta()`
- choosing between sync and async response APIs for the same output-control workflow
- enforcing required keys with `ensure_keys`, `key_style`, `max_retries`, and `raise_ensure_failure`
- consuming streaming output through `delta`, `specific`, `instant`, `streaming_parse`, `original`, and `all`
- reusing the same `response` object multiple times without sending another request
- understanding `StreamingData` fields such as `path`, `wildcard_path`, `indexes`, `delta`, `value`, and `is_complete`

Do not use this skill for:

- provider or endpoint setup
- `OpenAICompatible` auth, proxy, timeout, or `client_options`
- prompt export/import and YAML/JSON prompt configuration files
- `chat_history`, session management, or long-lived prompt memory
- TriggerFlow runtime streaming
- embeddings workflows

## Minimal Prompt Boundary

This skill assumes the request already has the input side roughly in place.

The output-control path mainly depends on:

- `input(...)`
- `info(...)`
- `instruct(...)`
- `output(...)`

If the user is primarily asking how to compose the input side, that belongs in a separate input-composition skill.

## Workflow

1. If the task is about schema shape, field typing, nested objects, or list outputs, read [references/output-schema.md](references/output-schema.md).
2. If the task is about field order, dependency order, planning-before-reply, or CoT-like staged output control, read [references/order-and-dependencies.md](references/order-and-dependencies.md).
3. If the task is about reliability, missing keys, retries, or `ensure_keys`, read [references/reliability-and-retries.md](references/reliability-and-retries.md).
4. If the task is about what response form to use for a real integration scene, read [references/response-patterns.md](references/response-patterns.md).
5. If the task is about how to consume a response as text, parsed data, object, metadata, or async variants, read [references/response-consumption.md](references/response-consumption.md).
6. If the task is about live streaming, structured field streaming, reasoning events, or tool-call events, read [references/structured-streaming.md](references/structured-streaming.md).
7. If the task is about why a response can be read multiple times or why prompt changes do not affect an existing response, read [references/response-lifecycle.md](references/response-lifecycle.md).
8. If the task is failing or behaving unexpectedly, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

Agently output control is a chain, not a single API call:

1. `.output(...)` defines the desired structure.
2. The prompt layer infers a structured JSON output format and can build a dynamic output model.
3. `get_response()` snapshots the current prompt and settings for one response instance.
4. The response parser accumulates text, parsed JSON data, metadata, and streaming events into one reusable result object.
5. Reliability features such as `ensure_keys` and retries operate on that parsed result layer.

## Selection Rules

- If the user wants machine-readable output, start with `.output(...)`.
- If later fields depend on earlier fields, place the prerequisite fields first in `.output(...)`.
- If the user wants staged reasoning or planning fields, put those fields before `reply` or any other final-answer field.
- If an async variant fits the caller runtime, prefer the async variant over the sync wrapper.
- If the user needs more than one view of the same result, create `response = ...get_response()` first.
- If the user only needs one final form, the shorthand getters are fine.
- If the caller is an async service or may issue several model requests concurrently, prefer `async_get_*()` and `get_async_generator()`.
- If the user wants strict required fields, add `ensure_keys`.
- If the user wants typed object access, use `get_data_object()`.
- If the user wants token-by-token text, use `type="delta"`.
- If the user wants structured output and live field-level updates together, default to `type="instant"` or `type="streaming_parse"`.
- If the user wants path-based structured streaming, use `type="instant"` or `type="streaming_parse"`.
- If the user wants tool-call or reasoning events only, use `type="specific"`.
- If the user wants text, parsed data, metadata, and multiple views of one result without a second request, use `response = ...get_response()` first and then read from `response.result`.

## References

- `references/source-map.md`
- `references/output-schema.md`
- `references/order-and-dependencies.md`
- `references/reliability-and-retries.md`
- `references/response-patterns.md`
- `references/response-consumption.md`
- `references/structured-streaming.md`
- `references/response-lifecycle.md`
- `references/troubleshooting.md`
