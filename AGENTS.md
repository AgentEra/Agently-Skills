---
name: agently-skills-catalog
description: Central catalog and documentation for Agently Skills V2. Use when working with Agently skill installation, routing, and installed-skill usage guidance.
---

# Agently Skills Catalog

This package publishes the current Agently Skills catalog generation `v2` under
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
  owners for Action, ExecutionResource, TriggerFlow, and DynamicTask. A
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
- The main repository release commit must update `pyproject.toml`, `agently/compatibility.py`, `compatibility/index.json`, and the matching `compatibility/releases/<version>.json`; keep `compatibility/in-development.json` aligned until the release line moves on.
- If the release recommends a new `agently-devtools` build, update the DevTools package version in `../Agently-Devtools/packages/python/pyproject.toml` during the same release-prep pass; changing only docs, tests, or compatibility text does not trigger the DevTools publish workflow.
- Keep the Agently DevTools `recommended_version_specifier` in the current release manifest aligned with the version that will be published to PyPI.
- Before creating or updating the main repository PR, run `pyright` and `python -m pytest` in the main repository, using the same Python environment that will validate the release.
- Before considering this Skills repository aligned, run `python validate/validate_compatibility.py`, `python validate/validate_catalog.py`, `python validate/validate_bundle_manifest.py`, `python validate/validate_trigger_paths.py`, `python validate/validate_native_usage.py`, `python validate/validate_reference_retrieval.py`, and `python validate/validate_project_template.py`.
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
- Do not force example correctness by overfitted prompt wording that exists only to make the expected output pass. Prefer realistic business facts, typed output contracts, validation, deterministic non-model business checks, and clear frontend/backend result shaping.
- Local functions may be used only as business capabilities, Actions, fake external systems, executor/provider smoke targets, or deterministic resources called by the model-driven flow.
- Low-level infrastructure smoke examples may run without a model only when they are explicitly scoped to executor/provider behavior and are not presented as model-app patterns.

## Project Defaults

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
- When model output must strictly satisfy a documented API request, module
  interface, or function call, use one explicit integration contract: runtime
  facts in `input`, authoritative API/schema documentation, signatures, and
  docstrings in `info`, transformation and call rules in `instruct`, and the
  exact machine-consumable shape in `output`. Add field-level type, semantics,
  requiredness, enum, format, range, nullability, and dependency details where
  applicable. This is necessary boundary/output control, not business-logic
  intrusion; deterministic validation still runs before the real call.
- Keep provider settings under the namespace actually read by the active plugin. For `OpenAICompatible`, prefer `plugins.ModelRequester.OpenAICompatible.*`.
- Prefer `Agently.load_settings("yaml_file", path, auto_load_env=True)` for file-backed settings. Use `Agently.set_settings(...)` for inline overrides.
- Keep optional DevTools wiring in the integration layer through `ObservationBridge`, `EvaluationBridge`, or `create_local_observation_app` instead of scattering debug hooks across workflow code.

## Skill Routing Reminders

- `agently`: unresolved owner layer, project shape, or broad product request
- `agently-design`: cross-owner architecture, ModelRequest/value/event topology,
  evidence and identity boundaries, lifecycle, pressure, and audit design
- `agently-request`: provider wiring, env placeholders, model settings, prompt config, structured output, response reuse, session memory, embeddings, and retrieval
- `agently-runtime`: Action Runtime, tools, MCP, Execution Environment, FastAPIHelper, `auto_func`, `KeyWaiter`, and optional `agently-devtools` observation, evaluation, and playground integration
- `agently-triggerflow`: explicit orchestration, branching, concurrency, runtime stream, workflow-owned business events, and execution-graph-friendly workflow definitions
- `agently-dynamic-task`: submitted or model-generated TaskDAG planning,
  validation, resolver binding, and execution through the TriggerFlow substrate
- `agently-migration`: migration from LangChain, LangGraph, LlamaIndex, CrewAI, or similar systems into Agently-native layers

## Anti-Patterns

- Do not treat sync sample code as the default architecture for async-capable services.
- Do not choose an all-serial complex workflow before identifying its real data,
  ordering, side-effect, and capacity constraints.
- Do not expose raw model parser paths directly to the UI when the workflow can translate them into stable business events.
- Do not keep provider auth, model name, or base URL in ad hoc Python literals when settings plus `${ENV.xxx}` placeholders fit.
- Do not tell users to clone or editable-install the private DevTools source when the public package `pip install agently-devtools` already matches the supported integration path.
- Do not make a goal-pursuit task use a required capability by leaning on a strong prompt instruction or a business-specific special case. When a task must use a particular Action, Skill, Skill pack, or DynamicTask, express it as framework contract: make capabilities visible to the planner (`planner_capabilities`), bound the step with structured `step_scope`, and declare a structured `capability_evidence_requirements` entry that the AgentTaskLoop host guard checks deterministically against execution evidence. The prompt is explanatory, not the guarantee; keep scenario-specific checks (visual fingerprints, domain names, source choices) in examples and tests, never in framework paths.
