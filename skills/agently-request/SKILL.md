---
name: agently-request
description: "Use for Agently request-side setup and contracts: model settings, Prompt/input/output design, effect tuning, missing or redundant context, structured output, response reuse, streaming, TTS/STT audio, session memory, embeddings, and retrieval within one request family. Review can be triggered by a developer's need to understand node behavior, not only by naming Prompt review. Use agently-design for cross-node data flow and model/Host ownership."
---

# Agently Request

Use this Skill for one request family. Start with `agently` when the owner layer
is unclear; use `agently-triggerflow` when the application owns branching,
waiting/resume, concurrency, retry, or durable multi-stage lifecycle.

For multi-round Prompt collaboration, start each substantive round with current
items (status first) and a timestamped, versioned change-log table. Use
[Multi-Round Collaboration](../agently/references/multi-round-collaboration.md)
to preserve pending decisions, modifications and abandonment.

## Read by Need

- Independent TTS/STT, audio model drivers, Agent audio binding, or audio streaming:
  `references/audio.md` (4.1.4.8 development; not the text Prompt pipeline).

- Provider, endpoint, env, settings namespace, or connectivity:
  `references/model-setup.md`.
- Request responsibility, effect tuning, input/output sufficiency or redundancy,
  collaborative review, Prompt config/references, or evaluation levels:
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

- Use collaborative review when request contracts can clarify model duties,
  improve execution effects, or reveal missing/redundant data; an explicit
  "Prompt review" request is unnecessary. Start complex reviews with a flow
  overview highlighting model nodes and Host handoffs, then group related
  Prompt tables for comparison. Up to three logical nodes may share a reply;
  tightly coupled larger groups are allowed. Prioritize developer understanding,
  not fixed counts or one-node approval turns. Preserve confirmation of
  consequential changes and distinguish design findings from measured effects.
  See `references/prompt-management.md`; use `agently-design` for cross-node
  flow/ownership analysis, not for unrelated mechanical work.
- After measured schema/ensure/length failures, consider a shallower model-facing
  projection or coherent request splits with Host reconstruction and unchanged
  final validation. See `references/output-control.md`.
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
- Do not repeat facts, rubric definitions, or field constraints in `instruct`.
  Point the model to their owning slots with literal `[info.rules]` /
  `[output.verdict]` references in ordinary strings. Keep these mentions
  unchanged; no f-strings, substitution, rendering, or content copying is needed.
  Read `references/prompt-management.md` for syntax and evaluation guidance.
- Keep request-local cohesion: retain prompt context only when it changes the
  current request's task, contract, evidence, permission, restriction, or
  required result, or provides useful user-visible process context, state, or
  explanation with a declared user or UI consumer. Retain or behaviorally
  rewrite an effective upstream caller guarantee when it changes the
  model-owned decision or the allowed verdict set. Do not assume the model can
  infer unexplained external project context; provide the compact facts it
  needs in this request.
- Do not promote literals or behavior from a single observed instance into
  normative prompt instructions. Derive a general invariant and test
  contrasting cases; use illustrative examples only to explain an already
  stated rule, and keep their total rendered content smaller than the
  non-example normative prompt.
- Before dispatch, use `execution.get_prompt_text()` only to audit the rendered
  execution draft. When TaskContext, Session, Skills, retrieval, Actions, or
  other runtime extensions can inject later, use a bounded test to observe the
  final ModelRequest `prompt_text` emitted or built after injection. Do not
  treat the post-start execution snapshot as sufficient evidence for late
  injections, and redact secrets before retaining prompt evidence.
- When a reusable configured Agent must create a strict hot-only request, use
  `agent.create_temp_request()` or
  `agent.create_request(inherit_agent_prompt=False,
  inherit_extension_handlers=False)`. If inheritance is intentional, declare
  the approved inherited slots and handlers and audit the final post-prefix
  ModelRequest prompt. A fake fluent-call test cannot prove projection
  isolation because it may not implement real Agent inheritance or prefixes.
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

Use explicitly defined descriptive levels for model-owned quality judgments,
not invented numeric scores. Host mappings of levels are ordinal policy codes,
not measured quality or calibrated probabilities. Reserve numeric metrics for
defined calculations over recorded facts.

Use executable code/Actions for complex arithmetic, aggregation, and data
transformation. Let the model propose or review a calculation plan, then feed
observed results to the next semantic step.

## Result Consumption

On the 4.1.4.8 development line, `.auto_continue()` is the preferred name for
conditional output continuation; `.ensure_long_output()` remains the released
compatibility spelling for the same policy. It is not task resume/rework or
proactive `long_content` generation. See `references/output-control.md` for
version scope and current capability limits.

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
- After a final getter completes validation, reopening any result generator on
  the same `ModelRequestResult` replays the accepted attempt. If validation
  replaced the original attempt, clear or replace provisional UI state before
  applying the replacement stream. An `AgentExecution` structured direct-model
  stream appends that accepted replacement before closing and identifies it
  through `meta.response_id` and `meta.attempt_index`.
- `instant` may start work before the response finishes, but its result is not
  new input to the same in-flight request. When later model output needs that
  result, join after final reconciliation and pass it to a later ModelRequest.
- When one direct result may exceed a model window, configure `.auto_continue()`
  before starting. The first request stays ordinary. Provider facts and strict
  raw-carrier evidence select normal validation or one combined tail-check and
  append request; no separate judge or forced semantic expansion is added.
  Complete/incomplete/undetermined is a private delivery decision, not an
  Execution mode. Reuse LongOutputDelivery, TriggerFlow, cumulative bounds and
  TaskWorkspace readback; preserve the original schema and validators.
  Both plaintext and initially open structured strings retain trusted prefixes.
  Read `references/output-control.md` for packet boundaries, per-path limits,
  empty completion, no-progress and fail-closed rules.

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
- Carrying implementation names or project history that do not affect the
  current request, while assuming the model understands their external context.
- Deleting an effective caller guarantee because it originated upstream, or
  retaining generic project narration as "user-visible" without a declared
  user or UI consumer.
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
- Turning entity literals, one-time input or environment state, a historical
  incident, test fixture, or expected answer from one observed instance into a
  prompt branch, or letting illustrative examples create behavior that the
  normative contract never states.
