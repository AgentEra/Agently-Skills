---
name: agently-request
description: "Use when the user is shaping Agently request-side behavior: model setup, settings files, prompt management, structured output, response reuse, streaming consumption, session memory, embeddings, knowledge-base indexing, retrieval, or retrieval-backed answers within one request family."
---

# Agently Request

Use this skill when the work stays on the request side: provider setup, prompt
contracts, output contracts, response consumption, session continuity, or
retrieval.

If the owner layer is still unclear, start with `agently`. If the
request clearly needs branching, waiting, resume, or durable orchestration, use
`agently-triggerflow` and read this skill only for model-step details.

## Route Inside This Skill

- model endpoint, env vars, `${ENV.xxx}`, settings namespaces, or connectivity checks -> `references/model-setup.md`
- prompt slots, prompt config, YAML/JSON prompt files, mappings, or reusable request contracts -> `references/prompt-management.md`
- VLM image questions, local image files, image URLs, or multi-image input -> use `.image(question=..., file=...|url=...|files=[...]|urls=[...])`; keep `.attachment([...])` for low-level rich-content passthrough or exact mixed-content ordering
- stable fields, required keys, machine-readable output, `.output(...)`, `ensure_keys`, or validation -> `references/output-control.md`
- model-output quality checks, intent routing, scenario matching, business
  classification, grading, or tests that should use model judges instead of
  keyword/regex checks -> start from `agently` and read
  `skills/agently/references/model-quality-validation.md`
- one result consumed as text/data/meta/stream without re-requesting -> `references/model-response.md`
- conversation continuity, SessionMemory plugins, `AgentlyMemory`, memo, chat history, or restore-after-restart -> `references/session-memory.md`
- embeddings, Chroma collections, Workspace `retrieve`/`grep`, Workspace recall, retrieval, or KB-to-answer -> `references/knowledge-base.md`

## Native-First Rules

- keep provider settings outside prompt and workflow code; prefer settings files with `${ENV.xxx}` placeholders when deployment values differ by environment
- keep stable prompt and output contracts in prompt config when shared across a request family
- for VLM image requests, prefer `.image(question=..., file=...|url=...|files=[...]|urls=[...])`; use `.attachment([...])` only when the caller already owns provider-style rich content blocks
- use `.output(...)` tuple ensure flags for fixed required leaves; use runtime `ensure_keys` only for runtime-dependent paths
- order output fields from supporting information to final decision. Agently
  output schemas are ordered: evidence, assumptions, clarifications, source
  notes, calculations to perform, concise rationale, and rule checks should
  come before final booleans, verdicts, replies, summaries, or actions.
  User-facing rendering may reorder sections for natural reading, but the model
  generation contract should keep support-before-conclusion order.
- for grading, judging, evaluation, confidence, trust, usability, relevance, or
  quality tasks, ask the model for conceptual levels with explicit definitions
  instead of precise numeric scores. Use labels such as high_trust,
  moderate_trust, low_trust, excellent, adequate, weak, or failed, and define
  each label in the prompt. If downstream code needs statistics, thresholds,
  weighting, or index math, map the labels to deterministic numbers in code
  after model output; do not ask the model to emit `0.78`, `3/5`, or `8/10` as
  the primary judgment.
- do not ask the model to perform complex, long, or high-precision arithmetic,
  derivations, or data transformations directly. Ask it to produce executable
  Python, Bash, SQL, or another appropriate calculation plan, run that code with
  tools, then feed the original question, code, and observed result back into
  the next model step.
- when testing model-owned content, use an Agently model judge with output
  control and assert structured boolean rule judgments; avoid keyword,
  substring, regex, or snapshot checks as the primary semantic correctness test
- in development scripts and service modules, make intent recognition, scenario
  matching, business classification, and route selection Agently model requests
  with explicit output schemas. Do not replace those decisions with jieba,
  token counters, keyword dictionaries, substring checks, or regex route rules.
- in test scripts, make output quality evaluation, grading, and semantic
  acceptance a second Agently model request with structured evidence, reasons,
  and boolean fields. Keep deterministic code for schema, enum, and smoke
  checks only.
- for scenario routing, intent detection, and business classification, use a
  model request with an Agently output schema instead of tokenization, word
  segmentation, keyword hits, or substring rules. Choose smaller or local models
  for simple decisions, and larger models for many labels, dense rules,
  ambiguity, or complex returned structures.
- use `get_result()` when the same result must be read multiple ways. Agent
  quick prompt chains return `AgentExecutionResult`; direct low-level
  ModelRequest calls return `ModelRequestResult`. `ModelResponseResult` is
  retired. For AgentExecutionResult, `get_data()` is the business-result view;
  use `get_full_data()` only when a task-strategy caller needs the full
  route/task envelope. `get_response()` remains a compatibility alias where
  present, but new Agent examples should prefer `get_result()`
- treat completed `AgentExecution` objects as immutable run records. For
  compatibility with older fluent chains, prompt/config mutators called on a
  completed execution return a fresh execution draft; continue from that
  returned object, and prefer one execution per request boundary in service
  code
- keep Session memory separate from TriggerFlow execution state; when durable
  long-term memory is needed, use `session.use_memory(mode="AgentlyMemory",
  workspace=...)` or bind it through an Agent session instead of inventing a
  parallel memory manager
- use `workspace.retrieve(...)` for shared intelligent retrieval over records
  and files; use `workspace.build_context(...)` when ordinary multi-turn task
  work specifically needs a ContextPackage from prior Workspace records; use
  low-level `workspace.grep(...)` / `workspace.grep_files(...)` for debugging
  or explicit deterministic filters. `workspace.search(...)` and
  `workspace.search_files(...)` keep their compatibility return shapes, but may
  automatically choose deterministic grep or retrieval packaging internally
- when the next request should be produced by an Agent-owned task loop, let
  `agent.create_task(...)` build the ContextPackage between iterations and record
  observations, decisions, verification, and checkpoints; do not duplicate that
  loop with ad hoc request retries
- use `workspace.get_data(...)`, `workspace.links(...)`,
  `workspace.latest_checkpoint(...)`, and `workspace.checkpoint_history(...)`
  when building explicit loops that store structured state and record lineage
- keep retrieval explicit when its results feed a later request or workflow step
- default to async-first response consumption in services, streaming paths, and workflows

## Anti-Patterns

- do not handwrite provider HTTP calls before checking native model requester settings
- do not rebuild prompt templates with ad hoc string formatting when prompt mappings fit
- do not handwrite JSON repair/retry loops before using output contracts and validation
- do not re-request the same model call only to get text, parsed data, or metadata separately
- do not hide retrieval inside unrelated prompt code

## Read Next

- `references/model-setup.md`
- `references/prompt-management.md`
- `references/output-control.md`
- `references/model-response.md`
- `references/session-memory.md`
- `references/knowledge-base.md`
