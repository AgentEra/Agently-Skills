---
name: agently
description: Use when the user wants to build, initialize, validate, optimize, or refactor a model-powered assistant, internal tool, automation, evaluator, or workflow from a business scenario or common problem statement, including project-structure refactors or starter skeletons that may separate model setup, prompt config, and orchestration, even if the request also mentions a UI, app shell, or local model service such as Ollama, and it is still unclear whether the solution should stay a single request, add supporting capabilities, or become orchestration. The user does not need to mention Agently explicitly.
---

# Agently

Use this skill first when the request still starts from business goals, refactor goals, product behavior, or broad model-app language.

The user does not need to say Agently, TriggerFlow, or any other framework term. Generic asks such as "build an assistant", "help me design an internal tool", or "create a validator for common problems" should still start here when the owner layer is unresolved.

Requests that also mention a UI, a web page, a desktop shell, or a local model service such as Ollama should still start here when the request is fundamentally about shaping a model-powered tool rather than only wiring one narrow capability.

## Workflow

1. Reduce the request into scenario and atomic goals.
2. If the request is a project initialization or structure refactor, choose the owner layers, async boundary, and repo skeleton first.
3. Choose the narrowest native Agently capability path.
4. Name the concrete operations or primitives that should be used.
5. Name the validation rule that proves the design stayed native-first.
6. For non-trivial apps, recommend optional local DevTools observation or
   evaluation when it will help the developer inspect runtime behavior, logs,
   traces, playground runs, or repeated scenario evaluations. Keep DevTools as
   optional tooling and route details through `agently-runtime`.
7. If native framework capability is missing, broken, unexpectedly awkward, or
   forces business code to add patches or glue that should belong to Agently,
   generate a clear issue report and recommend filing it at
   `https://github.com/AgentEra/Agently/issues`.
8. For manual issue filing, only provide the issue content and filing method to
   the user. Ask before filing automatically; if the user wants automatic
   filing, first verify local submit capability/permission, reproduce that the
   problem still exists locally, and carefully re-check Agently usage so the
   report is not caused by missed documentation or incorrect API use. Before
   either manual or automatic filing, redact local absolute paths, usernames,
   account names, tokens, private repo/workspace names, internal project names,
   raw logs containing private prompts, and any customer or project-private data.
   Use placeholders for local context and run a privacy scan on the final issue
   body.

## Native-First Rules

- default to async-first guidance for service code, streaming, TriggerFlow, and any path that may overlap work or benefit from cancellation
- treat sync APIs as wrappers for scripts, REPL use, or compatibility bridges unless the host truly requires sync-only integration
- before choosing the execution shape for a complex service or script, map the
  real stage dependencies. Keep genuine ordering constraints serial, but run
  independent work concurrently with bounded pressure controls. Use provisional
  `instant` fields for UI or cancelable/idempotent preparation and TriggerFlow
  signals/joins for
  application-owned coordination. An all-serial design chosen without this
  analysis is an anti-pattern
- when the request is a project-shape refactor, separate settings, prompts, services, domain contracts, workflow, and tests before discussing low-level implementation details
- when a development script, service module, or test needs semantic judgment
  over model-owned behavior, use Agently model requests with explicit output
  schemas. Development-time intent recognition, scenario matching, business
  classification, output quality checks, grading, and review decisions should
  be model-owned unless the check is only a deterministic smoke gate for
  structure or required-field presence.
- when model output must strictly satisfy a documented API request, module
  interface, or function call, build one explicit integration contract: put
  runtime facts in `.input(...)`, authoritative API/schema documentation,
  signatures, and docstrings in `.info(...)`, transformation and call rules in
  `.instruct(...)`, and the exact machine-consumable type and shape in
  `.output(...)`. Describe every downstream-consumed field with its type,
  semantics, requiredness, and any applicable enum, format, range, nullability,
  or cross-field constraint. This is necessary boundary/output control, not
  business-logic intrusion. Keep unrelated business decisions out of the
  contract and run deterministic validation before a real call.
- when adding or refactoring Agently framework internals under `core/` or
  `builtins/`, prefer a subdirectory package when the feature has multiple
  roles such as facade, manager, backend/provider, registry, adapter, policy, or
  validation. Use a single file only when the capability is genuinely small and
  splitting would be over-design.
- when a project must test model-generated semantic content, design the test as
  an Agently model-judge request with output control: explicit rules and context
  go in, per-rule evidence/reason and final boolean fields come out, and tests
  assert those booleans
- for business examples with mocked systems, keep mocks limited to facts,
  records, policies, incomplete data, or conflicting source material; do not
  return hidden expected answers, pass/fail labels, or local quality verdicts.
  Let AgentTask verification or a separate Agently model judge decide whether
  the model handled defective data correctly.
- for model-app evaluation, grading, confidence, relevance, or quality
  judgments, prefer explicit conceptual levels and definitions over direct
  numeric scores. If later workflow logic needs thresholds or aggregate metrics,
  map those levels to deterministic numeric values in code after the model
  response.
- for scenario routing, intent detection, or business classification in AI apps,
  use an appropriately sized model request with an Agently output schema.
  Smaller models, including local models when available, are acceptable for
  simple routes with few labels and rules. Use a larger model when labels,
  decision conditions, rule interactions, or the returned data structure are
  complex.
- configure reusable Agent definition state with `agent.define(...)` when the
  code owns model defaults, fixed persona/prompt, mounted Actions, Skills,
  Workspace, ContextBuilder profile, or policy defaults. Keep ordinary
  `agent.input(...)`,
  `agent.output(...)`, `.goal(goal_or_goals, success_criteria=None)` /
  `.goals(...)` as the same goal-pursuit entrypoint, and execution options on
  an AgentExecution draft; do not teach shared Agent
  pending prompt mutation as the default setup pattern.
- use `agent.effort("low" | "medium" | "high")` for ordinary strategy depth.
  When the app needs explicit strategy posture, keep the same method and pass
  sections such as `budget`, `planning`, `execution`, `verification`, `replan`,
  and `progress`; treat `budget` values as soft planning, reflection, repair,
  and evidence-depth hints rather than silent hard limits. Use explicit
  `limits={...}` or task options when the host needs hard resource controls.
  Framework defaults should not impose model-request, iteration, TaskBoard tick,
  Action round, node-count, or tool-call quotas; no-progress and idle timeouts
  are liveness guards for stuck executions, not strategy evidence.
  Do not introduce raw iteration-count builders or treat effort as permission,
  data visibility, resource gating, or completion acceptance. In AgentTask,
  effort also controls reflection density: low means final reflection plus only
  planner-marked important process nodes, medium means each major node or
  TaskBoard card/tick, and high means every framework-observable bounded step,
  Action/ACP call, TaskBoard card, and final reflection. Reflection is evidence
  for replan/verifier input, not completion evidence by itself.
- in Goal Pursuit / AgentTask examples, caller facts and the requested
  structured output contract may live on the same `AgentExecution` draft through
  `.input(...)` and `.output(...)`; AgentTask treats that execution prompt
  snapshot as task context during planning, bounded step execution, and
  verification. Do not duplicate those facts into framework hardcode only to
  make the task loop see them.
- for every intermediate process with a strong structured contract, use
  Agently `.output(..., format=...)` on the owning request/execution. Choose the
  format that fits the payload (`json`, `hybrid`, `flat_markdown`,
  `xml_field`, or `yaml_literal`); if a declared non-JSON format fails,
  Agently may recover through JSON parsing, but only dict-shaped parsed payloads
  satisfy structured control or final task output contracts.
  AgentTask internals may add short process fields only where the framework has
  a concrete consumer: intent or decision-basis fields before route/plan/control
  decisions, and compact self-check, summary, verification, repair, or
  progress-message fields after main result fields. These are bounded
  `process_summary` facts for next-step clarity and observation, not raw
  chain-of-thought, not EvidenceEnvelope evidence, not completion evidence, and
  not a public runtime mode.
- for long or prose-heavy deliverables whose main value is the natural-language
  body, do not force the body through `.output()` only to carry text. Let the
  body generate as natural text, then use a compact structured judge/readback
  contract for status, evidence, quality, and artifact refs. For trusted file
  deliverables, use Workspace artifact write/readback plus a compact manifest.
  Do not add `.output()` solely to trigger instant fields for the body stream;
  plain public delta remains a valid body source when the consumer handles
  replay boundaries.
  For AgentTask-backed AgentExecution, public `delta` may also project
  framework-owned progress, action observation, Flat plan/action summaries,
  TaskBoard status tables, phase, retry, and terminal-result facts as short
  paragraphs separated by blank lines, while `instant` remains the structured
  stream for UI state and diagnostics. Flat projections stay linear: plan
  completion can state the previous completed action and current action plan,
  and terminal output can summarize what was done and the result. TaskBoard
  status tables are display-only projections from structured AgentTask events;
  the first TaskBoard projection may render a table and later ticks may render
  card-state changes instead of reprinting the whole table.
  These projections do not own completion or quality judgment. Do not add a
  default parallel narrator request for process prose; use bounded process
  fields such as `progress_message`,
  `short_summary`, `verification_summary`, and `final_response` from the
  existing planner, verifier, card, or finalizer request, then consume them
  through `instant` / synthetic `$delta` when the UI needs richer structure.
  Internal artifact writers should consume AgentExecution stream facts: natural
  body text comes from raw delta items, and retry boundaries come from `$status`
  when the provider reports it. If the public `"<$retry>...</$retry>"` delta
  replay marker reaches the artifact consumer, treat that exact marker as a
  retry control event; never write, clean into, or transport it as artifact
  content.
  If a complete Markdown artifact body appears inside structured `evidence`,
  treat it as a deliverable body only when the evidence item is explicitly labeled
  as artifact/body/deliverable/Markdown or tied to the manifest path; ordinary
  source content and source excerpts remain evidence snippets. After trusted Workspace write/readback
  succeeds, let terminal verification judge any stale artifact-write
  `remaining_work` instead of planning another write-only step.
  For long trusted Workspace artifacts, artifact delivery should record
  `workspace_artifact.acceptance_locator` ledger items after real Workspace
  write/readback. Locators may use artifact-manifest sections, TaskBoard card
  criteria, and optional model-returned `acceptance_points` intent, but line
  ranges, offsets, headings, and fingerprints must come from the actual file.
  Verifier-visible evidence may include bounded
  `workspace_artifact.targeted_readback` ledger items read from those locators,
  with declared output-contract sections and generic anchors only as fallback;
  treat locators as readback pointers and targeted readbacks as scoped evidence
  snippets, not completion judgments.
  TaskBoard finalization should keep file-backed deliverable bodies in
  Workspace and return only a concise summary or path/ref pointer as
  `final_result`, not a second copy of the file body. AgentTask terminal
  results should carry a user-facing `final_response` for accepted, degraded,
  partial, and blocked outcomes: Flat terminal verification may return it in the
  existing verifier request, TaskBoard finalization may return it in the
  existing finalizer request, and framework fallback should be deterministic
  from structured status, artifact refs, final_result pointers, and unmet
  criteria without starting a separate narrator request. Accepted degraded
  deliveries use `artifact_status="degraded"` with disclosed evidence limits,
  while useful but unaccepted artifacts remain `artifact_status="partial"` and
  should explain unmet requirements instead of being reported as completed.
  `get_text()` / `async_get_text()` may prefer `final_response` for
  task-strategy result dicts; `get_data()` / `async_get_data()` return the
  business `final_result` view when present, while `get_full_data()` /
  `async_get_full_data()` return the complete route/task envelope.
  TaskBoard terminal payloads may include bounded `taskboard.completion_notes`
  for card summaries, known gaps, verifier notes, and acceptance progress; use
  them to disclose final-response limitations, but treat them as projection-only
  process context, not EvidenceEnvelope evidence or completion proof.
  For model-produced verifier/finalizer content, prose fields such as `status`,
  `reason`, `progress_message`, and `final_response` are display context only;
  semantic completion, repairability, and acceptance state must come from
  structured output fields such as `is_complete`, `requires_block`, and
  `criterion_checks[].satisfied` plus host guards, never from tokenization,
  keyword, substring, regex, or status-text matching over model prose.
  TaskBoard planning card ids are optional model hints. The framework owns
  canonical card ids, deduplication, and dependency remapping; ambiguous id
  hints should fail closed rather than being guessed.
  Intermediate downloads, webpage snapshots, generated code, search notes,
  memory-like task notes, and large extracted text may also be persisted as
  Workspace/Action refs and opened later through bounded readback; these refs are execution evidence, not proof
  that the final deliverable exists. A discovered URL, path, download, or
  snapshot ref is also not evidence that its content has been read; treat it as
  `ref_only` until a bounded readback/content preview is available. Explicit
  `content`, `excerpt`, or `snippet` fields are bounded previews only for the
  visible excerpt, not proof that the whole file was read. When a
  TaskBoard control card needs a new concrete URL, path, or ref materialized
  before continuing, return structured `target_refs` with
  `next_board_action=readback`; do not rely on URLs hidden inside `gaps` prose
  as executable targets. Intermediate TaskBoard artifacts should stay on
  working/evidence paths; framework-marked final repair or continuation cards
  may write the required final deliverable path when that path is part of the
  task output contract. If a TaskBoard control card returns
  `next_board_action=patch` with a Workspace text patch proposal, AgentTask
  should materialize the patch into the bound Workspace file and expose the
  resulting readback refs; the verifier still owns completion judgment. For
  Flat repository/file tasks, clone or list manifest paths are `ref_only` until a
  file read, artifact readback, or bounded content preview is visible; use them
  as retrieval targets, not source-content evidence.
  TaskBoard final verification receives board-level source refs with preserved
  `content_state` boundaries, so final synthesis must not upgrade discovered
  paths into source-content evidence without bounded preview/readback.
  TaskBoard checkpoints may include a bounded acceptance-index projection and
  handoff projection for long-running resume and inspection. Treat those
  projections as orientation only: they summarize criteria/card status,
  evidence refs, artifact refs, preflight facts, and explicit task-scoped dirty
  or unresolved state facts, but they are not `EvidenceEnvelope` evidence and do
  not accept the task. The acceptance index may also carry dirty/cache state,
  verdict fingerprints, scoped evidence refs, and progress counters so
  TaskBoard can avoid re-verifying unchanged green criteria; dirty items,
  required deliverable guards, and explicit blocking facts still go through
  verifier or host checks. Preflight requirements must come from mounted Actions,
  ExecutionResources, or existing Workspace refs; do not assume universal git,
  browser, shell, or startup-script checks.
  TaskBoard scheduling defaults to event-driven `frontier` mode: completed
  cards can immediately unlock ready successors, while fan-in cards still wait
  for all declared dependencies. Use `taskboard_scheduler="batch"` only for
  historical tick-batch diagnostics or regression comparison.
  AgentTask grounding uses the canonical `EvidenceEnvelope.evidence_items`
  ledger. Prefer visible `cite_as` handles or canonical ids in `evidence_use`;
  path, URL, record, artifact, and action/ref aliases are producer-declared
  structural compatibility affordances that host guards canonicalize only when
  unambiguous. Guards must not rely on business-specific action-name rules.
  Compatibility views such as `scoped_retrieval_results` and TaskBoard `source_refs` are projections.
  Treat `status=failed|empty` as unavailable/missing-data evidence only, never
  as support for positive facts. Treat `body_state=ref_only` as discovery/ref-
  pointer evidence only. When structured output supports it, return
  `evidence_use` bindings with `claim`, `evidence_ids`, and `support_type`.
  File-backed task outputs may also return optional `acceptance_points` with a
  criterion, expected heading or exact anchor, and supporting evidence ids so
  the framework can build locator evidence after Workspace readback; do not
  invent line numbers or byte offsets.
- AgentTask work units receive an internal task context contract with
  intermediate-resource ref/readback policy and prompt-safe runtime metadata.
  Runtime records may keep compact `current_time` diagnostics, but default
  model-hot prompts omit concrete runtime timestamps and only expose
  availability metadata. For current, latest, recent, or as-of tasks, require
  the caller or source evidence to provide the business date when it matters.
  This contract is model-decision context, not a model-call, tool-call,
  node-count, iteration, or wall-clock cap, and runtime time must not be used as
  a business/source fact by itself.
- AgentTask observation projects normalized `agent_task.action.started`,
  `agent_task.action.completed`, and `agent_task.action.failed` stream events
  from Action records. Treat them as factual observability for UI, DevTools, and
  experiment logs; recovered `success` or `partial_success` Action records
  project as completed observations, while failed observations are reserved for
  failed, blocked, timed-out, or unrecovered error records. Do not use them as a
  local quality, relevance, route, or completion judgment.
- treat `execution.step_plan` as compatibility guidance only. AgentTask no
  longer uses TaskDAG / DynamicTask as an internal bounded-step strategy; legacy
  `dynamic_task` / `execution_dag` step proposals and
  `effort(..., execution={"step_plan": "dag"})` degrade to one direct bounded
  AgentExecution step with diagnostics. Use TaskDAG / DynamicTask separately
  when the application or visual automation surface owns the submitted graph.
- treat `AgentExecution.strategy("auto"|"direct"|"flat"|"taskboard")` as the
  top-level route/execution selector. `direct` forces the ordinary
  model_request route with ActionLoop and does not create AgentTask; do not use
  `.effort("direct")` for route control. `auto` keeps ordinary prompt/action
  runs direct unless structural task signals such as goals, success criteria,
  task options, or Skill selectors enter AgentTask. Once AgentTask is selected,
  task `execution="auto"` uses one AgentTask-owned task-shape model request that
  allows free natural language analysis and then returns a thin structured
  `execution_hint`; do not route with keywords, regex, or local scorecards, and
  do not treat the hint as completion evidence. Use `execution="flat"` /
  `.strategy("flat")` to force the linear loop and `execution="taskboard"` /
  `.strategy("taskboard")` only when the host explicitly wants TaskBoard.
  Nested AgentExecution instances inherit the parent strategy context unless
  the child explicitly overrides it.
- treat Blocks as the internal lowering bridge from AgentTask
  `ExecutionPlan` / `PlanBlock` instances to TriggerFlow-backed
  `ExecutionBlockGraph`, not as a public task lifecycle. Validated TaskDAG nodes
  use this carrier only through explicit `compile_blocks(...)` /
  `async_run_blocks(...)`; ordinary `TaskDAGExecutor.async_run(...)` compiles
  directly to TriggerFlow.
  PlanBlock selection is evidence of need, not permission; ExecutionBlocks
  cannot accept task completion. Blocks registries fail closed on unknown block
  kinds, invalid runtime bindings, invalid signal contracts, denied
  capabilities, or pending capabilities without an `approval_wait`.
  `skill_activation` loads selected Skill guidance/resources and records
  skill-context evidence, while side-effect evidence must come from downstream
  ActionRuntime, Workspace, approval, or other concrete execution blocks.
- consume Agent quick prompt results through `AgentExecutionResult`:
  `execution = agent.input(...).output(...)`, then
  `result = execution.get_result()` and `result.get_data()` /
  `await result.async_get_data()`, or use execution facade methods such as
  `execution.get_prompt_text()`, `execution.get_data_object()`,
  `execution.get_key_result(...)`, `execution.wait_keys(...)`,
  `execution.get_async_generator(type="specific")`,
  `execution.streaming_print()`, and `await execution.async_get_meta()` when the
  app needs prompt inspection, object/key readers, streams, or process facts.
  For task-strategy route internals such as `status`, `artifact_status`,
  `taskboard`, or diagnostics, use `result.get_full_data()` /
  `await result.async_get_full_data()`. Direct low-level ModelRequest calls
  return ModelRequestResult; do not use the retired ModelResponseResult name.
  Ordinary `agent.input(...).start()` expressions create a fresh one-run
  execution each time and remain valid in loops. Explicit completed
  `AgentExecution` objects are immutable run records; do not reconfigure or
  rerun the same object, and create a new execution for the next request.
- when the host owns a developer loop and needs one bounded Agent step, choose
  `agent.create_execution(lineage=..., limits=...)` plus explicit
  `execution.async_record_workspace(...)` observation/checkpoint writes before
  building the next ContextPackage; do not introduce task-step mode as a public
  category or make Workspace depend on AgentExecution semantics
- when the model should own a single business task's plan, bounded execution,
  evidence recording, verification, and replan loop, choose
  `agent.create_task(...)` before hand-writing a TriggerFlow loop; it returns a
  task-strategy `AgentExecution` draft, not a separate public AgentTask handle.
  Use `agent.create_task_loop(...)` only when the code needs to be explicit that
  the long-task loop strategy is selected; it still returns an AgentExecution
  draft and should be consumed through the same result/stream/meta facade.
  Keep the first-slice boundary to one Agent owner, one task, 2-5 iterations,
  and bounded steps that use only explicitly enabled Actions or Skills; treat
  completion as model verification plus conservative host evidence guards, read task refs
  through the execution result/meta, and use a second model judge for
  model-owned semantic content instead of accepting structural counters alone
- when an application needs to add optional operator context while a
  task-strategy AgentExecution is already running, use
  `await execution.async_add_guidance(...)` or `execution.add_guidance(...)`.
  Treat guidance as non-blocking context: AgentTask records it to Workspace
  `workspace_refs["guidance"]`, exposes `guidance_items` / `guidance_refs`,
  and applies it at the next Flat or TaskBoard safe boundary. It must not be
  used as completion evidence, must not be injected into non-task route prompts,
  and must not replace `pause_for(...)` / `continue_with(...)` when the workflow
  requires a blocking external answer.
- when AgentTask completion depends on a particular capability, express it
  as framework contract rather than prompt force: expose capabilities through
  planner metadata, use structured `step_scope` for bounded action steps, and
  use `capability_evidence_requirements` for completion evidence. For side
  effects such as workspace writes/readbacks, require `action_succeeded`
  evidence for the host Actions instead of accepting model claims. Preserve
  prior action evidence in Workspace context packs before bulky execution
  metadata so later Skills or Action steps can use the actual evidence, not only
  a summary saying evidence was collected.
- when a checkpointed AgentTask must resume after a crash, use
  `agent.resume(task_id)` or `await agent.async_resume(task_id)` and consume the
  returned task-strategy `AgentExecution` through `.start()`/`.async_start()`,
  result, stream, and meta surfaces. Treat `resume_task(...)` as a compatibility
  alias only; do not teach `AgentTask.async_resume(...)`, `task.async_run()`, or
  a bare AgentTask handle as the recommended public lifecycle
- for feature or release acceptance, use coverage-first reasoning: start from
  the target contract in roadmap/spec/issues/docs/compatibility/example rules,
  map each requirement to evidence from examples, deterministic tests, protocol
  tests, docs/spec, compatibility metadata, companion validation, or explicit
  deferral, and only then conclude whether the feature is complete
- for release acceptance that touches or claims a Foundation-layer capability,
  add a Foundation example effect gate after pyright/pytest: treat Foundation as
  framework substrate such as ModelRequest/ModelRequestResult, TriggerFlow, Dynamic
  Task/TaskDAG, ActionRuntime, ExecutionResource, Workspace/ContextBuilder,
  RuntimeEvent/EventCenter, and provider protocols, not application-level
  AgentExecution or Skills use cases by themselves; identify the affected
  Foundation capability, run the corresponding core example under `examples/`
  against the release candidate, use real DeepSeek or local Ollama when
  model-owned behavior is involved, and fail closed if the example effect is
  missing, broken, or only proven by tests
- for public API or compatibility-line releases, run the public typing allowlist
  gate. `compatibility/public-typing-allowlist.json` is an exception ledger for
  documented `Any` boundaries with owner, reason, narrowing plan, and expiry;
  it is not a public-method allowlist, so new public methods must be fully
  typed unless they add a reviewed exception.
- route complex arithmetic, long-number computation, weighting, aggregation, or
  statistical work through executable code or tools; use the model to produce or
  review the calculation plan, not to be the calculator.
- when application development reveals a framework gap, first identify whether
  the missing responsibility belongs to Agently's public API, runtime behavior,
  documentation, Skills guidance, examples, or architecture boundary. Produce a
  concise issue report with scenario, expected behavior, actual behavior,
  current workaround, architectural responsibility, and minimal reproduction or
  affected docs/examples; recommend filing it in the Agently repository. The
  scenario must be clear enough to explain what kind of model-application
  development problem was being solved. If business details are confidential,
  omit or anonymize them, but still describe the application category, workflow
  shape, decision point, and framework responsibility needed for maintainers to
  understand the issue.
- treat automatic issue submission as an explicit user-approved action. Before
  submitting, confirm the local environment has the needed GitHub capability and
  permission, reproduce the issue locally, and audit the relevant Agently docs,
  examples, Skills guidance, and API usage to rule out a reading omission or
  improper framework use. Submit only a sanitized issue body: no local absolute
  paths, usernames, account names, tokens, private repository or workspace names,
  internal project names, raw private logs, or customer/project-private prompts.
  Prefer placeholders such as `<workspace>`, `<repo>`, `<task-file>`, and
  `outputs/debug/<turn-id>.jsonl`.

## Capability Routing

- model setup, prompt management, output control, response reuse, session memory, embeddings, KB, or retrieval-to-answer -> `agently-request`
- Action Runtime, built-in actions, tools compatibility, MCP, ExecutionResource, FastAPIHelper, `auto_func`, `KeyWaiter`, or `agently-devtools` observation and evaluation integration -> `agently-runtime`
- model-generated or app-submitted DAG planning, TaskDAG validation, resolver handlers, or Dynamic Task execution -> `agently-dynamic-task`
- branching, concurrency, waiting/resume, mixed sync/async orchestration, event-driven fan-out, process-clarity refactors, runtime stream, graph-friendly workflow definitions, or explicit multi-stage quality loops -> `agently-triggerflow`
- migration choice between LangChain and LangGraph -> `agently-migration`

## Anti-Patterns

- do not skip this playbook when the owner layer is unresolved
- do not invent custom output parsers, retry loops, or orchestration first
- do not use keyword, substring, regex, or text snapshot checks as the primary
  correctness signal for model-owned semantic content; keep them only as smoke
  gates for structure, routing, or required-field presence
- do not use tokenization, word segmentation, keyword hits, or substring rules
  as the route owner for AI-app scenario routing, intent detection, or business
  classification
- do not put model-app quality gates, business scoring, or route choice into
  local helper functions that only count words, split tokens, search keywords,
  or compare snapshots when an Agently model request can own the judgment
- do not let sync-first sample code dictate the service architecture when the target is clearly async-capable
- do not default a complex service or script to all-serial execution without
  first identifying real data, ordering, side-effect, and capacity constraints
- do not split project initialization into a fake standalone framework surface before the owner layers are chosen
- do not treat multi-agent, judge, or review flows as separate framework surfaces before checking native Agently capabilities
- do not normalize long-lived business patches, workarounds, compatibility glue,
  or private wrappers when the underlying need is a missing, broken,
  misleading, undocumented, or unfriendly Agently framework capability

## Read Next

- `references/capability-map.md`
- `references/project-framework.md`
- `references/model-quality-validation.md`
