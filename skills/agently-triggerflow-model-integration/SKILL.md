---
name: agently-triggerflow-model-integration
description: Use only when the main task is running Agently model requests inside TriggerFlow flow logic, including async-first request execution, per-step request isolation, concurrent model calls, or using `delta` or `instant` streaming to drive downstream TriggerFlow work.
---

# Agently TriggerFlow Model Integration

This skill is the model-execution leaf inside the TriggerFlow domain. It focuses on async-first request execution inside flow handlers, request isolation per step or per item, multiple concurrent model requests, and using `delta` or `instant` streaming inside the flow. It does not decide whether the user should use TriggerFlow in the first place, and it does not cover provider setup, prompt-config files, or the standalone details of output-schema design.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- creating Agently model requests inside TriggerFlow chunks
- choosing between `Agently.create_request()`, `agent.create_request()`, and `agent.create_temp_request()`
- async-first response handling inside flow handlers
- single model request per step
- multiple model requests in one workflow through `batch(...)`, `for_each(...)`, or controlled `asyncio.gather(...)`
- reusing one response inside a flow step through `get_response()`
- using `delta` or `instant` / `streaming_parse` inside flow logic
- using structured streaming to emit downstream flow events or runtime-stream items earlier

Do not use this skill for:

- provider setup, auth, proxy, timeout, or `client_options`
- detailed `.output(...)` schema design rules and `ensure_keys` behavior
- runtime-stream lifecycle or interrupt mechanics as the primary topic
- flow config export/import or execution save/load

## Workflow

1. Start with [references/request-lifecycle-in-flow.md](references/request-lifecycle-in-flow.md) to choose the right request object and async response shape.
2. If the task involves several model requests in one workflow, read [references/multi-request-patterns.md](references/multi-request-patterns.md).
3. If the task uses `delta` or `instant` inside the flow, read [references/streaming-and-dispatch.md](references/streaming-and-dispatch.md).
4. If the task is an end-to-end recipe such as a planning loop, SSE endpoint, or fan-out summarization flow, read [references/integration-recipes.md](references/integration-recipes.md).
5. If behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

TriggerFlow does not replace Agently model requests. It orchestrates when and how they run.

The normal model-integration pattern is:

1. a chunk decides that model work should happen
2. the chunk creates or prepares a request object
3. the chunk consumes the response as final data, `delta`, or `instant`
4. the chunk either returns data, emits flow events, or writes into runtime stream

Agently guidance for this skill should remain async-first:

- prefer `async_start()`, `async_get_data()`, `async_get_text()`, and `get_async_generator(...)`
- prefer async chunk handlers
- use sync wrappers only for sync-only demos or scripts

## Selection Rules

- one simple model step that only needs a final parsed result -> request `async_start()` / `async_get_data()`
- one model step that needs text plus metadata or streaming plus final data -> `get_response()` first
- model request should inherit agent role or stable settings -> `agent.create_request()`
- model request should not inherit agent prompt or extension handlers -> `agent.create_temp_request()`
- one input must fan out into several model calls with clear orchestration structure -> `batch(...)`
- a list of items should each trigger a model call -> `for_each(concurrency=...)`
- several independent model calls belong to one chunk and do not need their own flow routing -> controlled `asyncio.gather(...)`
- plain text stream should drive UI or logs inside the flow -> `delta`
- structured output should drive field-level updates or early downstream work -> `instant` / `streaming_parse`
- model stream items should fan out into signal-driven downstream work -> consume the stream in one chunk, `async_emit(...)` custom events, then route with `when(...)`
- runtime-stream lifecycle itself is the main topic -> also use `agently-triggerflow-interrupts-and-stream`
- output schema shape, field order, or `ensure_keys` is the main topic -> also use `agently-output-control`

## Important Boundaries

- `instant` does not create more model requests by itself; it only exposes structured nodes earlier
- if `instant` output should trigger more model work, route completed nodes into controlled TriggerFlow events, `for_each(concurrency=...)`, or other bounded orchestration
- avoid unbounded task spawning directly inside a stream consumer loop
- provider setup belongs in `agently-model-setup`

## References

- `references/source-map.md`
- `references/request-lifecycle-in-flow.md`
- `references/multi-request-patterns.md`
- `references/streaming-and-dispatch.md`
- `references/integration-recipes.md`
- `references/troubleshooting.md`
