---
name: agently-request
description: "Use when the user is shaping Agently request-side behavior: model setup, settings files, prompt management, structured output, response reuse, streaming consumption, session memory, embeddings, RecordStore retrieval, or retrieval-backed answers within one request family."
---

# Agently Request

Use this Skill for one request family. Start with `agently` when the owner layer
is unclear; use `agently-triggerflow` when the application owns branching,
waiting/resume, concurrency, retry, or durable multi-stage lifecycle.

## Read by Need

- Provider, endpoint, env, settings namespace, or connectivity:
  `references/model-setup.md`.
- Prompt slots/config, YAML/JSON prompt files, mappings, reusable contracts:
  `references/prompt-management.md`.
- Required fields, `.output(...)`, parsing, validation, or structured output:
  `references/output-control.md`.
- Text/data/meta/stream reuse without another request:
  `references/model-response.md`.
- Session continuity and durable memory: `references/session-memory.md`.
- Embeddings, knowledge indexing, RecordStore retrieval, ContextSource, or
  retrieval-backed answers: `references/knowledge-base.md`.
- Cross-source progressive disclosure or real-world Skills:
  `../agently/references/context-and-skills.md`.

## Prompt and Output Contract

- Keep provider settings outside prompt/workflow code. Prefer settings files
  with `${ENV.xxx}` placeholders for environment-specific values.
- Keep a one-off Agently fluent request readable as one chain: show
  `.input(...)`, `.info(...)`, `.instruct(...)`, `.output(...)`, and its terminal
  result call such as `.get_result()`, `.get_data()`, or `.async_get_data()`
  together. A Prompt config file plus explicit `mappings` is the declarative
  equivalent. Split only for real reuse, independently owned/versioned
  configuration, or genuinely dynamic composition.
- Put runtime values in `input`, authoritative source/API/schema facts in
  `info`, transformation/call rules in `instruct`, and the exact
  machine-consumable shape in `output`.
- Define each downstream-consumed field's type, semantics, requiredness,
  enum/format/range, nullability, and cross-field constraints.
- When post-generation business validation expects the model to satisfy a rule,
  provide that rule before the first attempt through `input`, `info`,
  `instruct`, and `output` as appropriate. Keep deterministic validation as the
  acceptance authority; validator retry feedback repairs a declared contract
  and must not become blind rule discovery.
- Order structured fields support-before-conclusion: evidence, assumptions,
  checks, and concise rationale before verdict, reply, summary, or action.
- Combine would-be request steps when they share one request-time input/evidence
  snapshot and later fields depend only on that snapshot plus earlier bounded
  fields in the same response. If a later semantic result needs an Action,
  system lookup, approval, artifact readback, or host computation performed
  after dispatch, await and validate that observation and start a new request.
- Use `.output(...)` tuple ensure flags for fixed required leaves and runtime
  `ensure_keys` only for runtime-dependent paths.
- Validate schema, offered keys, authorization, and deterministic constraints
  before a real call or side effect.

For VLM requests, prefer
`.image(question=..., file=...|url=...|files=[...]|urls=[...])`. Use
`.attachment(...)` only for caller-owned provider-style mixed content or exact
content ordering.

## Semantic Decisions

Use ModelRequest structured output for prose-derived intent, route, scenario,
classification, relevance, grading, quality, and acceptance. Do not make
tokenization, word segmentation, keyword tables, substring matching, regex, or
snapshot comparison the semantic owner.

Prefer defined conceptual levels over model-generated numeric scores. If the
host needs thresholds or statistics, map validated labels to numbers after the
model response.

Use executable code/Actions for complex arithmetic, aggregation, and data
transformation. Let the model propose or review a calculation plan, then feed
observed results to the next semantic step.

## Result Consumption

- Agent quick chains return `AgentExecutionResult`; direct ModelRequest calls
  return `ModelRequestResult`.
- Use `get_data()` for the business value, `get_text()` for user-facing text,
  `get_meta()` for process facts, and `get_full_data()` for the full task/route
  envelope.
- A completed explicit AgentExecution is one immutable run record. Create a new
  execution for the next request.
- When no consumer needs progress, directly await `async_get_data()`. Avoid a
  discard-only `instant` drain loop.
- Treat `instant` updates as provisional. Use them for UI or explicitly
  cancelable/idempotent preparation; irreversible work waits for final parsed
  output and host validation.
- `instant` may start work before the response finishes, but its result is not
  new input to the same in-flight request. When later model output needs that
  result, join after final reconciliation and pass it to a later ModelRequest.

## Context and Retrieval

- `RecordStore` owns durable records, its direct retrieval/index provider
  seams, deterministic filters, links, checkpoints, snapshots, and durable
  refs.
- `TaskContext` owns the current task's bound information sources, direct
  entries, and one internal derived `ContextIndex` for reusable cross-source
  structural, lexical, or optional hybrid candidate partitions.
- A `ContextSource` exposes compact descriptors through
  `async_enumerate_descriptors(...)` and bounded canonical bodies through
  `async_read_exact(...)`; after one canonical ref is selected it may optionally
  expose deterministic bounded in-ref location through
  `ContextSourceScopedRead`. The optional mechanism is not a semantic relevance
  owner, and the internal ContextIndex is never source truth.
- `ContextReader` binds to a consumer and phase, accepts a read intent and
  budget, then returns one or more bounded information blocks in a
  `ContextPackage`.
- Keep raw records cold. Project host-issued keys, bounded summaries/previews,
  and scoped readback refs into model-hot context.
- Keep complete ContextPackage omissions cold/auditable; model-hot projections
  should carry bounded details plus counts instead of one record per unselected
  source. Bind each disclosed scoped snippet to one host-issued reference key
  without duplicating its body in a second ledger field.
- Attach a RecordStore or knowledge source through a ContextSource when its
  information must participate in cross-source progressive disclosure.
- Keep retrieval explicit when its output feeds another request or workflow
  stage. Deterministic grep/search may narrow candidates; the model owns prose
  relevance and usefulness.

For retrieval-backed natural-language answers, offer one short trusted
`ref_id` per selected source and require `[[ref:<ref_id>]]`. Validate tokens
host-side, render approved source cards separately, and do not ask the model to
reproduce URLs or full retrieval metadata.

## Session Memory

Session memory is not TriggerFlow execution state. Use a SessionMemory plugin
for extraction/compression and accepted memory writes, and a RecordStore when
memory must survive process restart. For AgentTask recall,
`AgentlyMemoryContextSource` exposes accepted memory to the TaskContext-owned
ContextIndex; ContextReader performs the consumer-bound exact read and
ContextPackage delivery. Do not build a second memory-to-prompt retrieval path
inside the plugin.

## Anti-Patterns

- Handwritten provider HTTP, JSON repair, retry, or prompt templating before
  checking native settings/output contracts.
- Moving a one-use schema or prompt step away from its Agently request chain
  only to make the chain look shorter.
- Re-requesting one model call separately for text, data, and metadata.
- Hiding retrieval inside unrelated prompt formatting.
- Recreating generic Workspace/ContextBuilder behavior instead of composing
  RecordStore, TaskContext, ContextSource, and ContextReader.
- Treating a retrieval hit, memory record, or provisional stream field as final
  semantic proof.
- Generating from an underspecified prompt and relying on hard-validator
  failures to teach the model one rule per retry. If a production gate cannot
  be safely stated, warn the developer with the risks and alternatives, then
  require explicit second confirmation before implementing that named gate.
