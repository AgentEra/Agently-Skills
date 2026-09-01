---
name: agently-request
description: "Use when the user is shaping or collaboratively reviewing Agently request-side behavior: model setup, settings files, business Prompt contracts, structured output, response reuse, streaming consumption, session memory, embeddings, RecordStore retrieval, or retrieval-backed answers within one request family."
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

- When it is known that the user is developing with Agently and is doing
  solution design, process optimization, or Prompt review, use the collaborative
  method by default without waiting for the user to request a table. Confirm the scoped request inventory and
  responsibilities first. For user-selected or justified critical requests,
  default to one table-first Prompt design, then wait for confirmation/revision.
  Group long slots by topic and expose model-visible examples separately from
  reviewer-only notes. See `references/prompt-management.md`; routine unselected
  requests do not need a new approval ceremony.
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
- When one direct business result may exceed a provider output window, put
  `.ensure_long_output()` on the unstarted AgentExecution. It keeps the first
  request ordinary and activates TriggerFlow-backed, TaskWorkspace-verified
  continuation only after normalized length/incomplete termination. Use plain
  text or JSON, preserve nested containers when projecting each model-visible
  slot contract, preserve nested Pydantic constraints, validate each value
  independently before append-only commit, enforce exact list bounds/order,
  expose one exact mnemonic `path_key` per slot,
  close the revision/digest/anchor header before business updates, retain valid
  prefixes across rejected tails, keep the exact anchor as a short accepted-unit
  digest, pass the bounded document start, exact accepted tail, and host-counted
  character total as one read-only plain-text continuity context, commit one
  plain-text block per logical continuation so every next join sees the
  refreshed accepted suffix, and keep declared coverage validators
  explicit. Preserve trusted explicit
  empty-list/empty-text facts, treat each closed structured string as an
  immutable atomic value (use a chunk list beyond the per-unit bound), and require
  declared ensure paths before accepting continuation finality. A length
  terminal before header closure preserves the manifest as bounded no progress;
  the third consecutive no-progress continuation terminates. The delivery flow
  owns one-physical-request continuation recovery; do not hide another
  ModelRequest retry loop inside it. A malformed provider-complete envelope is
  bounded observable no progress, while an authoritative complete final parse
  must not be replaced by an older instant snapshot. Final
  schema/declared-validator repair retains accepted units and remains bounded;
  storage/digest/lineage integrity failures fail immediately. Do not mix this
  delivery policy with an explicit AgentTask strategy.

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
