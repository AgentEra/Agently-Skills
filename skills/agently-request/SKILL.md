---
name: agently-request
description: "Use when shaping one Agently request family: model/settings setup, prompt contracts, structured output and validation, result or stream consumption, Session memory, embeddings, RecordStore retrieval, or retrieval-backed answers."
---

# Agently Request

Use this Skill when the work can be owned by one ModelRequest family. Use
`agently-triggerflow` when a later semantic step needs a tool result, system
lookup, approval, artifact readback, or host computation produced after the
first request, or when branching, concurrency, retry, or pause/resume must stay
visible in the application lifecycle.

## Read by Need

- Provider, endpoint, environment, settings namespace, or connectivity:
  [model-setup.md](references/model-setup.md).
- Prompt slots/config, mappings, reusable contracts, or Agent inheritance:
  [prompt-management.md](references/prompt-management.md).
- Structured output, Pydantic, ensure/validation, streaming formats, or direct
  long-output delivery: [output-control.md](references/output-control.md).
- Reusing one request result as text/data/meta or consuming its streams:
  [model-request-result.md](references/model-request-result.md).
- Session continuity and durable memory:
  [session-memory.md](references/session-memory.md).
- Embeddings, RecordStore, ContextSource, retrieval, and grounded citations:
  [knowledge-base.md](references/knowledge-base.md).
- Cross-source progressive disclosure and real-world Skills:
  [context-and-skills.md](../agently/references/context-and-skills.md).

## Request Contract

- Keep a one-off fluent request readable as one chain: `.input(...)`,
  `.info(...)`, `.instruct(...)`, `.output(...)`, then its result call. Split
  only for actual reuse, independently owned configuration, or dynamic
  composition.
- Put runtime facts in `input`, authoritative evidence/API/schema material in
  `info`, behavior and transformation rules in `instruct`, and the exact
  downstream-consumed shape in `output`.
- Define each consumed field's type, meaning, requiredness, enum/format/range,
  nullability, and cross-field constraints where applicable.
- Give the model every non-sensitive satisfiable validator rule before the
  first attempt. Deterministic validation remains authoritative; retry feedback
  repairs a declared contract and must not become blind rule discovery.
- Use ModelRequest structured output for prose-derived intent, routing,
  relevance, grading, and acceptance. Host code owns schema/type checks,
  authorization, arithmetic, offered-key membership, and side effects.
- Combine semantic fields in one ordered response only when they share the same
  request-time evidence snapshot and later fields need no post-dispatch fact.
  Streaming cannot inject a tool or host result into an in-flight request.
- Validate schema, offered keys, authorization, and deterministic constraints
  before a real call or side effect.

For VLM requests, prefer
`.image(question=..., file=...|url=...|files=[...]|urls=[...])`. Use
`.attachment(...)` only when the caller owns provider-style mixed content or
exact content ordering.

## Results, Context, and Memory

- Direct ModelRequest calls return `ModelRequestResult`; Agent quick chains
  return `AgentExecutionResult`. Reuse the same result facade for text, parsed
  data, metadata, and streams instead of issuing the request again.
- When no consumer needs progress, await the final getter directly. Treat
  `instant` fields as provisional UI or cancelable/idempotent preparation and
  reconcile them against the final validated result.
- Session memory is not workflow state. `SessionMemory` owns extraction and
  compression policy; `RecordStore` owns durable records and retrieval;
  TriggerFlow execution state owns workflow progression.
- Keep raw retrieval records cold. Give the model bounded task-relevant facts
  and one host-issued key per candidate, then validate and reconstruct canonical
  identities in host code.
- For retrieval-backed answers, offer trusted `ref_id` values, require
  `[[ref:<ref_id>]]`, and resolve approved source cards/links host-side.

## Avoid

- Handwritten provider HTTP, prompt templating, JSON repair, or retry loops
  before checking Agently settings and output contracts.
- Moving a one-use schema or prompt step away from its request chain only to
  shorten the visible code.
- Re-requesting the model separately for text, data, and metadata.
- Treating retrieval hits, memory records, provisional stream fields, or model
  prose as deterministic proof of authorization or side effects.
