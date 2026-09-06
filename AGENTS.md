---
name: agently-skills-catalog
description: Central catalog and documentation for Agently Skills V3. Use when working with Agently skill installation, routing, and installed-skill usage guidance.
---

# Agently Skills Catalog

This package publishes the current Agently Skills catalog generation `v3` under
`skills/`. Historical catalogs are preserved on frozen archive branches instead
of the default branch so coding-agent retrieval only sees the current catalog.

Use this file as installation-time guidance after the skills are added into another project or agent environment.

## Usage Priorities

- Route unresolved product, assistant, and workflow requests through `agently` first.
- Prefer Agently-native capabilities before custom output parsers, retry loops, or orchestration layers.
- Apply Occam's razor to APIs, architecture, and examples: do not add a new entity,
  method, facade, or compatibility patch when an existing Agently surface already
  carries the concept clearly. Prefer a narrow alias or docs clarification for unclear names.
- Default to async-first guidance for services, streaming, TriggerFlow, and concurrent execution. Treat sync APIs as wrappers for scripts, REPL use, or compatibility bridges unless there is a clear reason not to.
- Before designing a complex Agently service or script, map its real serial and
  parallel dependencies. Prefer async Agently APIs, provisional `instant`
  structured streams for UI or cancelable/idempotent preparation, and
  TriggerFlow signal networks for explicit
  fan-out, joins, and downstream triggers. Run independent work concurrently
  under bounded execution, operator, model-scheduler, and host admission limits;
  expose host worker/thread-pool settings when blocking code is present.
  Defaulting an unanalyzed complex workflow to all-serial execution is prohibited.
- Treat `agently-devtools` as an optional companion package installed from PyPI, not as a required source-repo dependency.
- Keep public skill boundaries capability-first and mutually exclusive.
- Treat multi-agent, judge, and review flows as scenario recipes unless they need a dedicated framework surface.
- For Agently framework internals, follow the core module style: class-owned
  runtime state, typed data contracts under `agently/types/data`, protocol or
  handler seams under `agently/types/plugins`, and retained implementation
  owners for Action, ExecutionResource, TriggerFlow, and TaskDAG. A
  high-level capability can live outside `agently/core` when it composes
  several core systems; split large implementations by registry, planner,
  executor, adapter, facade, and contract boundaries rather than by arbitrary
  line count.
- Do not recommend archived catalog branches for new projects; they exist only
  for explicit rollback or historical inspection.

## Coordinated Release Rules

- For an Agently framework release, validate the main repository and companion repositories before merging or publishing.
- Feature acceptance is not complete until each relevant spec records the final
  implemented design, any fully landed planned spec has moved to `spec/implemented/`,
  and `spec/README.md` points to the completed location.
- When reporting public API, recommended usage, examples, or compatibility-line
  changes, include concise sample code that shows the updated usage shape.
  Prefer current usage snippets or before/after snippets over abstract prose
  when that will make the change easier to inspect.
- Version numbers are part of the release-prep change and must be updated before final validation, merging, or publishing; do not rely on post-publish metadata-only edits to trigger a release workflow.
- Agently-Stage is the required-runtime companion. A Stage version that raises
  Agently's minimum dependency must be built and tested against Agently,
  published to PyPI, and clean-installed before the Agently minimum and lock
  move. A tag or local wheel is not publication evidence.
- Development-line planning must not change package release numbers. In the
  main repository, do not update `pyproject.toml`, `agently/compatibility.py`,
  `compatibility/index.json` `latest_release`, or create
  `compatibility/releases/<future-version>.json` only to mark the next planned
  version. Use `compatibility/in-development.json` for the next target until an
  actual release-prep change begins.
- If new version-development work starts after the previous public version has
  already been released, treat `compatibility/in-development.json` as the
  current work version while no release-prep or release-promotion action has
  started for a newer batch. Do not ask the maintainer to restate that version
  on every task. If the in-development manifest is missing, stale, or being
  replaced, ask for the current work version. If the intended task branch is
  not specified, ask for the branch before editing implementation, specs, docs,
  examples, compatibility metadata, or companion guidance.
- Simple documentation or behavior-guidance-only updates may be edited and
  committed directly on `dev` without asking for or creating a branch when they
  do not change public APIs, runtime behavior, examples, compatibility metadata,
  or spec contracts. If the scope expands beyond those boundaries, stop and
  apply the ordinary independent-branch rule before continuing.
- After validation, documentation or behavior-guidance-only updates that do not
  depend on an unreleased framework version may also be synchronized directly to
  the online `dev` and `main` branches without waiting for a coordinated release.
  This exception does not apply to documentation, examples, compatibility
  metadata, or spec contracts that require unreleased APIs or runtime behavior.
  Examples that only explain already-released behavior may follow the exception.
  Before pushing, inspect the complete outgoing commit range and exclude unrelated
  implementation or version-dependent changes.
- Maintainer standing authorization applies across Agently-Skills branches,
  workspaces and worktrees: methodology, solution-design, architecture-design
  and collaboration guidance may be cherry-picked directly to `main` and pushed
  without waiting for a framework release or another publication approval when
  it changes no framework functionality/code and has no dependency on framework
  versions, concrete implementations, method usage, parameters or configuration.
  Inspect full diffs and dependencies; isolate mixed commits without rewriting
  unrelated source history. Use a clean, freshly fetched target, preserve its
  public catalog/API/compatibility line, retain cherry-pick provenance, skip
  equivalent already-published changes, and run the target's required checks.
  Push only the reviewed outgoing range without force or bypassing protections;
  stop for unresolved dependencies, validation failures or remote rejection.
  Sync affected installed guidance without overwriting unrelated development
  work. This does not authorize a whole-branch merge, version bump or private
  spec publication; implementation-dependent guidance keeps its release gates.
- The main repository release commit must update `pyproject.toml`, `agently/compatibility.py`, `compatibility/index.json`, and the matching `compatibility/releases/<version>.json`; keep `compatibility/in-development.json` aligned until the release line moves on.
- If the release recommends a new `agently-devtools` build, update the DevTools package version in `../Agently-Devtools/packages/python/pyproject.toml` during the same release-prep pass; changing only docs, tests, or compatibility text does not trigger the DevTools publish workflow.
- Keep the Agently DevTools `recommended_version_specifier` in the current release manifest aligned with the version that will be published to PyPI.
- Before creating or updating the main repository PR, run `pyright` and `python -m pytest` in the main repository, using the same Python environment that will validate the release.
- Before considering this Skills repository aligned, run `python validate/validate_compatibility.py`, `python validate/validate_catalog.py`, `python validate/validate_bundle_manifest.py`, `python validate/validate_trigger_paths.py`, `python validate/validate_native_usage.py`, `python validate/validate_reference_retrieval.py`, and `python validate/validate_full_stack_reference.py`.
- Before publishing default-branch metadata that names frozen archive branches,
  push those archive refs first and rerun
  `python validate/validate_compatibility.py --require-remote-archives`.
- `validate_reference_retrieval.py` is static-only by default. Its model-backed
  cases require separate explicit authorization through
  `--allow-model-calls`, a positive `--max-model-requests` budget that covers
  the worst-case case-and-retry count, and an approved retry limit. Do not use
  the live path as part of an ordinary companion sync.
- Before considering `../Agently-Devtools` aligned, run `pyright --pythonpath "$(command -v python)"` and `python -m pytest packages/python/tests`; after push, confirm the GitHub Actions CI and publish workflow results.
- DevTools CI must work with the checkout layout used by `.github/workflows/ci.yml`; tests must not assume only a sibling `../Agently` checkout when the workflow checks Agently out as `agently-src`.
- Check whether companion repository heads are already merged into `origin/main`; if they are, treat them as no-op rather than creating unnecessary merge commits.
- If a companion repository has unrelated local dirty files, do not overwrite them. Report the dirty state if it affects release validation.
- PR titles and bodies for release work must not mention Codex, coding-agent internals, or generated-by metadata.
- If any release validation fails, list the failure and stop before merging, publishing, or creating the main release PR.

## Model Example Guidance

- Examples are capability probes, not pass-through theater. They must test
  whether Agently can solve a real business problem with the claimed
  architecture and runtime capability. If the framework layer is incomplete,
  missing a protocol seam, missing executor capability, or unable to solve the
  scenario honestly, stop and report the capability gap so the feature design
  can be adjusted. Do not fake success with framework-level business mappings,
  canned outputs, overfitted prompts, deterministic substitutes for
  model-owned behavior, or test-only branches hidden in production code.
- When problem discovery or strategy tuning would otherwise require repeated
  target-model calls, start with a same-context development-agent warm preflight.
  Define acceptance criteria first, simulate realistic request/response and
  behavior chains, and refine prompt, schema, topology, instrumentation, and
  failure paths until the preflight meets them. Label it `simulated` and
  `warm_preflight`; it does not satisfy a real-model validation gate.
- Simulated provider usage and metadata are never observed telemetry. Label
  invented values `synthetic`, estimates `estimated`, unavailable fields
  `unavailable`, and recorded-trace playback `replayed`; only current values
  returned by the target provider may be labeled `observed` or included in real
  experiment totals.
- After warm preflight, choose at most one feasible cold carrier: a native
  fresh-context subagent, handshake-verified ACP coding agent, or fresh isolated
  task/session. ACP is optional. Supply only task-local input, authoritative
  `info`, `instruct`, exact `output` contract, and criteria; withhold intended
  answers, prior conclusions, unrelated context, and customer secrets. Enforce
  host tool/network/file/time/call boundaries. Label the result `simulated`,
  `cold_preflight`, and—unless exactly one underlying request is proven—
  `agent_simulation`, not `single_model_request_simulation`.
- Same-context simulation never counts as cold review. If no isolated carrier
  exists, record `cold_preflight=skipped` with the reason and continue to the
  smallest representative, bounded real-model comparison. Final conclusions
  come from real traces. Default to authorized project/developer credentials
  with call, concurrency, retry, and budget caps; never consume customer API
  credentials or quota without explicit authorization and a disclosed cap.
- User-visible feature work must add or update examples for the scenario the
  feature enables before the task is considered complete. The example should be
  runnable in its declared environment, use the current recommended API shape,
  and keep an `Expected key output` comment with stable key values from one real
  run. Do not replace that with a generic statement such as "shows X". When the
  behavior is not obvious from output alone, add concise working-principle notes
  or an ASCII flow diagram in the example comment.
- Agently recommended examples, cookbook examples, public teaching examples, and training-derived examples must exercise a real model through DeepSeek or local Ollama.
- DeepSeek credentials may be loaded through dotenv by the example itself. Do not mark DeepSeek unavailable only because `DEEPSEEK_API_KEY` is absent from the parent shell environment.
- Model-owned planner, router, decomposer, evaluator, reviser, action selector, and response generator behavior must not be replaced with mock, deterministic, or hand-written local substitutes.
- Business-system feedback, such as ticket lookup, billing status, approval records, incident status, CRM writes, or notification delivery, may be mocked when the example is not connected to the real external system. Make the mock boundary explicit and keep it out of model-owned reasoning.
- Example model-processing stages must use real model output for natural-language analysis, planning, evaluation, and response generation. Do not hard-code final model text, parse a fixed canned answer, or replace model results with deterministic local text.
- Tests that validate model-output content should use a second Agently
  model-judge request with output control for semantic rule evaluation: feed the
  candidate output, explicit rules, expected contracts, and relevant execution
  context into the judge; require structured per-rule evidence, concise reason,
  and a final boolean field, then assert the boolean fields. Avoid keyword,
  substring, regex, or snapshot-style text checks as the primary correctness
  signal for model-owned semantic content; keep them only as deterministic
  smoke gates for structure, routing, or presence checks.
- Never promote literals or behavior from a single observed instance into
  normative prompt instruction. This includes entity literals, one-time input
  or environment state, historical incidents, test fixtures, and expected
  answers. Derive a general invariant and verify it against contrasting cases.
  Current authoritative business policy, domain invariants, authorization,
  interface contracts, and runtime facts remain required request context and
  are not special cases merely because they are business-specific.
- Illustrative examples may explain only rules already stated in the normative
  prompt. They cannot introduce behavior, priority, exceptions, or expected
  answers. Keep total rendered illustrative-example content smaller than the
  non-example normative prompt. If a task appears to require a larger few-shot
  set, treat selection as a separate evaluated design and test selection/order,
  label balance, and model-specific regressions instead of smuggling special
  cases into the ordinary prompt.
- Define AI-application acceptance on two independent axes: hard gate versus
  soft target, and deterministic check versus semantic review. Structured
  shape/type/enum, authorization, identity, arithmetic, and side-effect facts
  normally use deterministic hard gates. Open-ended intent alignment,
  groundedness, usefulness, clarity, tone, aesthetics, and other qualitative
  results use structured model, coding-agent, or human review. A mandatory
  semantic rule may still be a hard gate, but keyword/regex proxies do not make
  it deterministic. Score soft targets and advise on ordinary imperfections;
  only a predeclared unacceptable floor may block acceptance.
- Calibrate semantic rubrics on representative repeated real runs and compare
  model/coding-agent judges with human-labeled samples. Do not require exact
  prose reproducibility or silently lower the developer-approved business
  minimum to fit a weak model. If sufficient, accurate input and a clear
  request repeatedly miss that minimum, report a model capability/fit gap and
  discuss model choice, request design, fallback, or human review.
- Do not force example correctness by overfitted prompt wording that exists only to make the expected output pass. Prefer realistic business facts, typed output contracts, validation, deterministic non-model business checks, and clear frontend/backend result shaping.
- Local functions may be used only as business capabilities, Actions, fake external systems, executor/provider smoke targets, or deterministic resources called by the model-driven flow.
- Low-level infrastructure smoke examples may run without a model only when they are explicitly scoped to executor/provider behavior and are not presented as model-app patterns.

## Project Defaults

- When both facts are known—development uses Agently, and the user is doing
  solution design, workflow/block optimization, or Prompt review—apply the
  collaborative Prompt method by default even when the user did not ask for a
  table. Ordinary implementation, bug fixing, provider setup, or unrelated
  configuration is not enough to trigger it. For a complex workflow or scoped block,
  first ask the user to confirm the scenario, logical request inventory, and
  each request's responsibility. Then review user-selected or justified
  critical requests one design at a time by default, waiting for confirmation
  or revision before advancing. Inventory approval is not detailed Prompt
  approval. Follow explicit batch/delegation preferences and retain unchanged
  confirmations; review only affected handoffs when scope changes.
- Use a table-first review with topic-sized slot rows, visible model examples,
  and output-field constraints. Organize long slots into meaningful source and
  display sections, audit case-specific/non-generalizable rules, distinguish
  reviewer-only material from model-visible content, and keep the view aligned
  with the actual chain/config. No new slot/API, mandatory packet, or approval
  requirement for every routine request is implied.
- If representative runs show complex output causing schema/key/ensure/retry
  or length failures, diagnose the owner first; then consider flattening the
  model-facing projection or splitting coherent business units. Host code
  reconstructs the unchanged downstream contract and validates parts and final
  assembly; do not remove required fields or hard gates to improve pass rate.
- For long prose, consider a section plan, dependency-aware writing, bounded
  continuity context, and Host assembly. Summaries need actual consumers and
  may share the writer request unless they need validated/read-back text. Full
  bodies and source facts remain authoritative. Distinguish clean short output
  from truncation and possible learned brevity; do not assume pretraining is the
  cause. Sequential writing is justified only by real dependencies, while
  independent sections may run with bounded concurrency and ordered collection.
- Treat non-terminal model output as a stage-scoped contribution. It must
  satisfy its current schema, hard invariants, evidence boundary, and semantic
  subject while observably advancing state, narrowing uncertainty, selecting a
  useful next action, or producing a consumed handoff. It need not solve
  unrelated future stages or claim whole-task completion. Label provisional,
  unknown, and deferred work; terminal results and irreversible effects still
  require the full terminal acceptance contract.
- Plan owner/invariant, node, edge, and production-necessity ledgers before
  choosing files for every non-trivial model application. Planning nodes do not
  map one-to-one to modules. Start a one-request project from the composition
  entry, settings, Prompt contract, and tests; add `workflows/`, `services/`,
  Actions, local Skills, utilities, resources, or trace modules only when a real
  owner and current consumer require them.
- All public Skill examples, code fences, project assets, and generated project
  trees must be structurally concise. Reject stateless pass-through Services,
  Managers, factories, and request wrappers; renaming-only functions; duplicate
  facades; empty packages; unconsumed fields/nodes; and test-only production
  branches. Retain a wrapper only when it demonstrably owns authorization,
  validation, policy, state/lifecycle/cleanup/retry/concurrency/transactions, a
  non-trivial representation translation, a stable external contract, or a
  released compatibility boundary. Do not impose a universal line-count cap.
- Across code examples and project layouts, minimize the cross-file lookup
  count and nesting depth required by people and coding agents. Do not split
  one-use information into extra files, constants, helpers, classes, or wrappers
  unless the boundary has actual reuse value or an independently owned contract.
- In Agently fluent request examples, keep a one-off request's `.input(...)`,
  `.info(...)`, `.instruct(...)`, `.output(...)`, and terminal result call such
  as `.get_result()`, `.get_data()`, or `.async_get_data()` visible as one
  readable chain. One Prompt Configure file plus explicit `mappings` is the
  declarative equivalent. Split the chain only for actual reuse, independently
  owned/versioned configuration, or genuinely dynamic composition; do not move
  a one-use schema or prompt step elsewhere merely to make the chain shorter.
- Keep every prompt-slot item request-local: it must change the current
  request's task, contract, evidence, permission, restriction, or required
  result, or provide useful user-visible process context, state, or explanation
  with a declared user or UI consumer. Do not remove a real domain contract,
  allowlist, evidence item, input fact, or capability boundary merely because it
  came from project-level setup; apply the removal counterfactual to its effect
  on this request. Retain or behaviorally rewrite an effective upstream caller
  guarantee when it changes the model-owned decision or the allowed verdict
  set. Rewrite or remove unexplained implementation names only when they are
  request-irrelevant; the user-visible role does not authorize generic project
  narration. Before dispatch, `execution.get_prompt_text()` audits the rendered
  execution draft. When runtime extensions can inject later, use a bounded test
  to observe the final ModelRequest `prompt_text` after injection; the post-start
  execution snapshot is not sufficient evidence. Redact secrets before
  retaining prompt evidence.
- When a reusable configured Agent must create a strict hot-only request, use
  `agent.create_temp_request()` or
  `agent.create_request(inherit_agent_prompt=False,
  inherit_extension_handlers=False)`. If inheritance is intentional, declare
  the approved inherited slots and handlers and audit the final post-prefix
  ModelRequest prompt. A fake fluent-call test cannot establish projection
  isolation when it does not implement real Agent inheritance or prefixes.
- Use direct FastAPI for an ordinary typed HTTP API and FastMCP for MCP-server
  exposure. Keep both as inbound adapters over the same owned async application
  entry and approved result projection. `FastAPIHelper` remains available when
  its packaged task/stream transport is the desired contract; do not call it
  deprecated or make it the default template. MCP client consumption belongs to
  Agently Action management; do not add an application-local forwarding wrapper.
- Route model-generated or application-submitted DAG data through TaskDAG /
  DynamicTask validation and resolution; do not compile unvalidated runtime DAG
  data directly into new TriggerFlow definitions. Stable topology owned in
  trusted source code remains a direct TriggerFlow use case. The default
  `TaskDAGExecutor.async_run(...)` path compiles directly to TriggerFlow; Blocks
  is explicit opt-in through `compile_blocks(...)` / `async_run_blocks(...)`.
- Treat TriggerFlow `flow_data` as flow-shared even though `execution.save()`
  serializes a copy and `load()` replaces the current flow-shared value with it.
  Save/load does not make it isolated or concurrency-safe; per-run data belongs
  in execution state.
- Use TriggerFlow hidden execution sugar only for finite, self-closing runs when
  the caller does not need an execution handle. Pause/resume, external emits,
  save/load, intervention, inspection, cancellation, or controlled close require
  an explicit execution.
- Keep stable shared prompt and output contracts in prompt config rather than scattering them across Python helpers.
- Choose response consumption from actual consumer needs. When no caller uses
  progressive output, await `async_get_data()` directly; do not drain an
  `instant` generator into a no-op loop before reading the final result. Stream
  only when items are published, recorded, applied to state/UI, or used for
  explicitly cancelable/idempotent preparation.
- When `instant` is used to overlap model generation with downstream work, put
  compact trigger fields before long explanatory or artifact fields. Start work
  only from a complete canonical field or list item, deduplicate it by a
  host-owned payload key, dispatch it without blocking continued stream
  consumption, and reconcile the started set against the final validated data.
  Reuse matching work, start final items that were not observed provisionally,
  and cancel or discard provisional extras. A field-start event may map to a
  stable host-owned status, but raw parser paths are not the UI protocol.
- Treat a ModelRequest as a request-time input snapshot. Combine supporting
  semantic steps in one ordered request when later fields need only that
  snapshot plus earlier bounded fields in the same response. If a later model
  step needs an Action/tool result, system lookup, approval/resume payload,
  artifact readback, or host computation produced after dispatch, await and
  validate that new observation before starting a later ModelRequest.
  `instant` may start provisional work early, but it cannot feed that work's
  later result back into the already-running request.
- For retrieval-backed natural-language answers, expose one trusted `ref_id` or
  evidence `cite_as` per source and use application-level
  `[[ref:<ref_id>]]` tokens. Host code validates and resolves tokens, builds
  safe links, and emits application-approved source-card records for
  hover/source cards. Avoid bare `${ref_id}` because `${...}` is already
  Agently placeholder syntax.
- Keep record identity joins in host code. Give the model one trusted selection
  key per candidate plus only task-relevant facts, require only that key in the
  model judgment, validate it against the offered set, and then reconstruct
  UUIDs, canonical ids, opaque refs, metadata, and full records
  deterministically. Passing complete identity-heavy objects through the model
  and asking it to copy multiple ids or unrelated meta is an anti-pattern. Treat
  the selection key as an application-local required string constrained to the
  offered set, not as a second canonical identity.
- A selection's offered-set membership proves membership, not freshness. If a
  decision can cross a cache, queue, retry, persistence, or replay boundary,
  bind it to a Host-owned request/execution revision or issue per-request
  opaque keys, and validate Host correlation before canonical lookup. That
  binding must cover the semantic input/evidence/request revision, not only
  candidate or catalog state. A caller-supplied logical ID is insufficient
  unless Host storage guarantees its unique association with that semantic
  revision. Prefer non-overridable per-semantic-request lineage or a
  Host-owned canonical input/evidence revision. Prefer Host-bound lineage over
  asking the model to copy another request id; the model must not copy
  correlation ids. A strictly inline awaited response that cannot cross a
  request boundary needs no extra model-returned correlation field.
- When model output must strictly satisfy a documented API request, module
  interface, or function call, use one explicit integration contract: runtime
  facts in `input`, authoritative API/schema documentation, signatures, and
  docstrings in `info`, transformation and call rules in `instruct`, and the
  exact machine-consumable shape in `output`. Add field-level type, semantics,
  requiredness, enum, format, range, nullability, and dependency details where
  applicable. This is necessary boundary/output control, not business-logic
  intrusion; deterministic validation still runs before the real call.
- When post-generation business validation expects model output to satisfy a
  rule, provide the non-sensitive satisfiable rule before the first attempt in
  `input`, `info`, `instruct`, or `output`. Keep Pydantic, `.validate(...)`,
  authorization, and side-effect checks as deterministic acceptance
  authorities; their retry feedback repairs a declared contract and must not be
  the only way the model discovers it. Blind generation followed by hard
  rejection until the model happens to pass is prohibited. If a production
  gate cannot be safely or concretely stated but the developer still requests
  it, stop before implementation, explain the hidden/missing rule, affected
  output, retry/cost/latency/nondeterminism/liveness risks, safer alternatives,
  and proposed retry/terminal policy, then require a new explicit confirmation
  for that named gate. A prior blanket instruction is not sufficient.
- Keep provider settings under the namespace actually read by the active plugin. For `OpenAICompatible`, prefer `plugins.ModelRequester.OpenAICompatible.*`.
- Prefer `Agently.load_settings("yaml_file", path, auto_load_env=True)` for file-backed settings. Use `Agently.set_settings(...)` for inline overrides.
- Keep optional DevTools wiring in the integration layer through `ObservationBridge`, `EvaluationBridge`, or `create_local_observation_app` instead of scattering debug hooks across workflow code.

## Skill Routing Reminders

- `agently`: unresolved owner layer, project shape, broad product request, or
  low-frequency TaskDAG / DynamicTask guidance
- `agently-design`: cross-owner architecture, ModelRequest/value/event topology,
  evidence and identity boundaries, lifecycle, pressure, and audit design
- `agently-request`: provider wiring, env placeholders, model settings, prompt config, structured output, response reuse, session memory, embeddings, and retrieval
- `agently-runtime`: Action Runtime, tools, MCP, ExecutionResource, FastAPIHelper, `auto_func`, `KeyWaiter`, and optional `agently-devtools` observation, evaluation, and playground integration
- `agently-stage`: Stage task lifetime, sync/async bridges, loop-neutral
  handles, settlement, StageStream, Tunnel, EventEmitter, pressure, and idle
  diagnostics
- `agently-triggerflow`: explicit orchestration, branching, concurrency, runtime stream, workflow-owned business events, and execution-graph-friendly workflow definitions
- `agently-migration`: migration from LangChain, LangGraph, LlamaIndex, CrewAI, or similar systems into Agently-native layers

## Anti-Patterns

- Do not treat sync sample code as the default architecture for async-capable services.
- Do not choose an all-serial complex workflow before identifying its real data,
  ordering, side-effect, and capacity constraints.
- Do not expose raw model parser paths directly to the UI when the workflow can translate them into stable business events.
- Do not keep provider auth, model name, or base URL in ad hoc Python literals when settings plus `${ENV.xxx}` placeholders fit.
- Do not tell users to clone or editable-install the private DevTools source when the public package `pip install agently-devtools` already matches the supported integration path.
- Do not make a goal-pursuit task use a required capability by leaning on a strong prompt instruction or a business-specific special case. When an AgentTask must use a particular Action, Skill, or Skill pack, express it as a framework capability contract: make capabilities visible to the planner (`planner_capabilities`), bound the step with structured `step_scope`, and declare `capability_evidence_requirements` that the host validates against execution evidence. TaskDAG is an independent submitted-graph capability, not an AgentTask requirement or route. The prompt is explanatory, not the guarantee; keep scenario-specific checks in examples and tests, never in framework paths.
