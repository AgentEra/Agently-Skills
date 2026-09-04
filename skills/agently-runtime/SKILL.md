---
name: agently-runtime
description: "Use when the user wants Agently runtime extension capabilities: AgentExecution Patterns or terminal review/artifact policies, Action Runtime, built-in Action packages, MCP access, ExecutionResource lifecycle, TaskWorkspace file Actions, RecordStore durability, FastAPIHelper or streaming API exposure, or optional agently-devtools observation and evaluation."
---

# Agently Runtime

Use this Skill after the request/workflow owner is known. Start with `agently`
when the layer is still undecided, and use `agently-triggerflow` for visible
branching, concurrency, pause/resume, retry, or multi-stage orchestration.

## Read Only What the Task Needs

- Actions, Search/Browse, MCP, approval, Action artifacts, or AgentTask evidence:
  read `references/actions-runtime.md`.
- Action versus ExecutionResource, managed runtimes, sandbox/process/browser/
  SQLite resources: read `references/actions-execution-resource.md`.
- RuntimeEvent, logs, traces, evaluation, playground, or DevTools: read
  `references/devtools.md`.
- Stage task lifetime, sync/async bridging, loop-neutral handles, settlement,
  StageStream, Tunnel, or EventEmitter: use `agently-stage`.
- TaskContext, ContextReader, TaskWorkspace, RecordStore, SkillLibrary, or the
  SkillsExecutor compatibility facade: read
  `../agently/references/context-and-skills.md`.
- AgentExecution Pattern, review, verification, or artifact delivery: use the
  `AgentExecution and AgentTask` section below.

## Owner Boundaries

| Owner | Responsibility |
|---|---|
| `ActionRuntime` | Model-callable operations, schema validation, dispatch, policy, and Action results. |
| `ExecutionResource` | Lifecycle of live clients, sandboxes, processes, browsers, database connections, and MCP sessions. |
| `TaskWorkspace` | One task's existing files, generated artifacts, path containment, bounded readback, file identity, and verified terminal promotion. |
| `RecordStore` | Records, links, retrieval, RuntimeEvent persistence, checkpoints, snapshots, leases, and durable artifact refs. |
| `TaskContext` | Sole task-information aggregate; revisioned bindings/direct entries, internal derived `ContextIndex`, and read-handle lifecycle. |
| `ContextReader` | TaskContext-created intent-driven, budgeted progressive-disclosure handle for one consumer and phase. |
| `SkillLibrary` | Installed immutable real-world Skill revisions and resource reads. |
| `AgentExecution` | Task-scoped Skill binding, TaskContext preparation, route selection, execution, and result/stream APIs. |
| `AgentPattern` (beta) | One reusable whole-request behavior using the carrying AgentExecution's existing input, output, capabilities, policy, and result lifecycle. |

Do not merge these owners into a generic Workspace or runtime manager. File
space is not record storage; record storage is not model-hot context; a Skill
package is not an executor or permission grant.

## Native Action Rules

- Prefer `@agent.action_func` and `agent.use_actions(...)`; `tool_func`,
  `use_tool`, `use_tools`, and `agently.builtins.tools` are compatibility
  surfaces.
- Mount built-in Search/Browse with
  `agent.use_actions(Search(...))` / `agent.use_actions(Browse(...))`; do not
  invent `enable_search(...)`.
- Treat multi-Action package registration as atomic. A partial Search or MCP
  registration failure must remove batch-created Actions and restore any
  same-id host registration.
- Treat model-planned Action arguments as untrusted. Validate against the
  registered schema, authorization, and policy before dispatch.
- Use `agent.set_action_loop(planning_protocol="programmatic")` only for one
  bounded round of data-dependent read Actions. V1 exposes only visible
  `side_effect_level="read"`, `replay_safe=True`, non-approval Actions with an
  explicit lossless-JSON return contract. Nested calls default to exclusive;
  explicitly parallel Actions overlap under the bounded ordinary
  ActionRuntime/ActionDispatcher boundary, and exclusive calls form barriers.
- Treat Action output and Action artifacts as evidence only after the host has
  recorded the actual call. Model prose claiming a side effect is not Action
  evidence.
- Keep permission profiles explicit and narrow. Do not expose shell,
  filesystem, MCP, browser, install, or network capabilities merely because an
  AgentTask exists.

## File and Storage Rules

- Select a task file root with `agent.use_task_workspace(path, mode=...)`.
  Enable model-callable file work with
  `agent.enable_task_workspace_file_actions(...)` or
  `agent.enable_coding_agent_actions(...)`.
- `TaskWorkspace` is a file boundary only. Use its read/write/edit/glob/grep/
  patch/export methods for task files and artifacts; do not store arbitrary
  durable records inside it through a hidden database API.
- Direct `.ensure_long_output()` delivery uses execution-private TaskWorkspace
  files for raw segments, immutable accepted units, manifests, and final
  candidate readback. Those refs are staging evidence, not automatically
  durable public artifacts. Every accepted write must be completely read back
  with matching bytes and digest before the manifest advances. Structured
  units must also pass their slot schema before commit. Model-repairable final
  validation may add new units without discarding accepted ones, but any
  manifest/readback/digest/lineage mismatch fails immediately.
- A required AgentTask terminal deliverable starts as a staged candidate. The
  verifier receives a complete readback; only acceptance permits digest-pinned
  atomic promotion to the target and a complete post-promotion readback.
  Rejection preserves the previous target, and promotion/readback failure
  blocks delivery.
- For TaskWorkspace-bound shell execution, resolve relative `workdir` values
  inside the injected root. Accept `.`/child paths and consume an already
  root-prefixed logical `.agently/files/<execution-id>` locator exactly once;
  reject paths outside the root.
- Select durable records with `agent.use_record_store(...)` or pass a
  `RecordStore` to an explicit TriggerFlow execution. Use it for `put`, `get`,
  `retrieve`, links, RuntimeEvents, snapshots, checkpoints, leases, and durable
  artifact refs.
- Keep process state in memory/logs by default. Enable AgentTask
  `record_store_recovery` only when restart-safe recovery is required.
- Keep ordinary observation in logs/DevTools. Bind RuntimeEvent persistence
  explicitly; a RecordStore does not become an event archive merely because it
  is available.
- Keep large bodies cold behind TaskWorkspace, RecordStore, SkillLibrary, or
  another attached ContextSource. Put only compact handles, descriptors,
  bounded previews, status, and lineage facts in execution state and model-hot
  context. TaskContext's internal ContextIndex narrows reusable candidates;
  ContextReader obtains exact bodies from the source before delivery.

## Real-World Skills

- Treat standard `SKILL.md` packages as guidance plus addressable resources.
  They do not own execution strategy, routing, Action mounting, permissions, or
  side-effect proof.
- Install and inspect immutable revisions through `SkillLibrary` or the thin
  `Agently.skills_executor` management facade. Use registered
  `SkillSourceProvider` implementations for authorized local or Git sources;
  pin a Git `ref` and optional `subpath` rather than inventing a host checkout
  helper.
- Bind optional or required Skills on an `AgentExecution` with
  `execution.use_skills(...)`, `execution.require_skills(...)`, or
  `execution.use_skills_packs(...)`.
- Let `AgentExecution` prepare the shared TaskContext and read it for the
  actual consumer/phase with `async_prepare_task_context()` and
  `async_read_task_context(...)`.
- Provide Actions/MCP/ExecutionResources explicitly. Reading a Skill may inform
  the model that an operation exists; it never creates or authorizes that
  operation.
- When a trusted, exactly bound Skill revision contains an executable script,
  call `agent.bind_skill_script_action(...)` only after
  `execution.async_prepare_task_context()`. Pass the host-issued `binding_id`,
  exact resource path, and `SkillScriptAuthorization`; the binding registers an
  ordinary Action and never makes every script automatically callable. For a
  host-directed run, dispatch `bound_action.action_id` through
  `agent.action.async_execute_action(...)`, then read its published artifact
  path through the same execution's TaskWorkspace.
- `Agently.skills_executor` is a compatibility facade for source-backed or
  local install, configure, inspect, list, resource read, context-pack
  projection, and the TaskDAG Skill resolver. It is not a plugin route,
  planner, strategy registry, React loop, capability manager, or execution
  owner.
- `agent.run_skills_task(...)` remains a thin compatibility adapter to an
  ordinary AgentExecution. New code should create/configure the execution
  directly.
- There is no `SkillsManager`, `skill_activation` Block, Skills route,
  `single_shot`/`staged`/`react` Skills strategy family, or
  `configure_skill_capabilities(...)` auto-mount path in the current
  development-line contract.

## AgentExecution and AgentTask

- Use a fresh `agent.create_execution()` for multi-statement setup. A completed
  execution is an immutable run record; create another execution for another
  run.
- `.interact(handler)` is a standard AgentExecution method for one request-local
  connected response mechanism. The synchronous or asynchronous handler
  receives the complete normalized `ExecutionExchangeView` and returns the
  response payload expected by the existing exchange consumer. It is called
  only if an exchange opens, is replaced by a later pre-start declaration, and
  never mutates the global provider registry. Keep durable queues, webhooks,
  cross-process hosts, and application-wide routing on registered
  ExecutionExchange providers, routing handlers, and `interaction.*` settings.
- Treat `.pattern(...)` and the `AgentPattern` protocol as beta. Select one
  whole-request behavior with `.pattern(name_or_handler)`. Registering a
  Pattern does not select or instantiate it for an ordinary execution, and its
  name never replaces an Agent or AgentExecution method. The Pattern consumes
  the existing AgentExecution draft and returns its business value; a later
  `.pattern(...)` replaces rather than chains the selection.
  Its `run_default()` continuation may invoke the ordinary route once. Put
  Pattern-specific tuning in plugin settings or an instance instead of growing
  fluent kwargs. `.output(...)` remains the external result contract; a Pattern
  that bypasses `run_default()` must consume and honor it itself rather than
  creating a second Pattern-local input/output API.
- `.goal(...)` remains the public goal-pursuit switch. Agently may carry it
  transparently through the internal goal Pattern while preserving AgentTask's
  planning, evidence, verification, replan, result, and failure behavior;
  callers do not need to configure the beta Pattern API. `.strategy(...)`
  remains the lower-level mechanism override.
- The default plugin registry distributes the beta `plan` and `long_content`
  from `agently.builtins.plugins.AgentPattern`. `plan` owns readiness -> optional
  connected clarification -> final-plan topology and preserves the caller's
  external `.output(...)`. `long_content` owns section planning -> sequential
  section writing -> host text assembly; use `.artifact(...)` afterward for
  file delivery. Keep tuning under `plugins.AgentPattern.<name>` instead of
  adding Pattern method parameters. Durable plan pause/result resumption is not
  supported until AgentExecution owns a resumable Pattern handle.
- `.artifact(path, handler=None)` transforms the accepted result to text or
  bytes, then leaves containment, write, complete digest readback, trusted ref,
  and retention to TaskWorkspace. The handler must not write arbitrary host
  paths or replace the business result.
- `.review(handler=None)` performs one advisory quality judgment;
  `.verify(handler=None)` uses the same handler shape as a hard terminal gate.
  Both run after artifact materialization and neither hides retry, reflection,
  revision, or replan behavior. `.interact(...)`, `.artifact(...)`,
  `.review(...)`, and `.verify(...)` are standard methods; only Pattern is
  beta.
- Use `agent.create_task(...)` / `agent.create_task_loop(...)` only when the
  model should own planning, bounded execution, evidence, verification, and
  replan. They return AgentExecution drafts, not public AgentTask handles.
- `strategy("direct")` selects an ordinary model request with the Action loop.
  `strategy("auto")` may select AgentTask when structural task signals exist;
  `flat` and `taskboard` explicitly select the corresponding AgentTask shape.
- Use `AgentExecutionResult.get_data()` for the business value,
  `get_full_data()` for the route/task envelope, `get_text()` for user-facing
  text, and `get_meta()` for process facts.
- Treat `instant` as provisional structured progress and `delta` as printable
  text. Irreversible work must wait for the final parsed result and host
  validation.
- Add non-blocking operator context to a running task with
  `execution.async_add_guidance(...)`. Use TriggerFlow pause/resume when an
  answer is required before work can continue.
- A complex Pattern uses TriggerFlow for branches, joins, loops, required HITL,
  pause/resume, and recovery. ExecutionExchange remains the interaction routing
  and provider seam. A Pattern may consume the carrying AgentExecution's
  standard `.interact(...)` declaration, but must not add a second Pattern-local
  interaction API.
- Require actual Action evidence for required side effects. TaskWorkspace
  readback proves a file fact; it does not prove an unrelated Action call.
- When a sufficient completed TaskBoard control result provides a draftable
  artifact manifest without a body, let the dedicated artifact-draft stage
  materialize it with the same bounded canonical Action/readback evidence
  ledger. Framework-owned materialization is not semantic `remaining_work`;
  the resulting candidate still requires terminal verification and promotion.

## TriggerFlow and Recovery

- Use TriggerFlow execution state for per-execution handoff. `flow_data` is
  shared across executions and is not concurrency-safe task memory.
- Bind `snapshot_store`, `runtime_event_store`, and other recovery ports to a
  RecordStore only when the workflow needs those durable capabilities.
- Persist live resource descriptors, never live clients or secrets. Reconstruct
  ExecutionResources through host/plugin resolvers during load.
- Use explicit execution handles for pause/resume, external emit, save/load,
  intervention, inspection, cancellation, or host-controlled close.
- A programmatic Action run is live and non-durable while active. Save before
  it starts or after it settles; never claim TriggerFlow can restore its Python
  interpreter, provider IPC channel, or awaited Action binding. After durable
  approval/resume, create a fresh program decision against current policy.
- A local RecordStore can prove local restart behavior. Do not describe it as a
  production multi-worker Redis/Postgres/object-storage adapter without a real
  provider and operational evidence.

## Observation and Service Boundaries

- RuntimeEvent and DevTools are observation surfaces. They do not own routing,
  semantic relevance, authorization, verification, or acceptance.
- Keep provider telemetry out of prompt, routing, retry-policy, and quality
  decisions unless the application explicitly owns such a deterministic policy.
- Use `FastAPIHelper` or another host transport to expose a known execution
  contract; do not move workflow lifecycle into transport callbacks.
- Treat high-frequency delta aggregation as an outlet/delivery policy. Flush
  best-effort background outlets at an owning close point.
- Keep `agently-devtools` optional and fail-open. Integrate through public
  observation bridges, not source-repository paths.

## Fail-Closed Checks

- Reject unknown Skill revisions, resource refs, candidate keys, Action ids,
  context block keys, recovery providers, and external-resume identities.
- Keep identity reconstruction host-owned. Offer one short selection key to a
  model, validate it, then rejoin canonical records in host code.
- Do not use keyword/regex matching as the semantic owner for intent, Skill
  relevance, route choice, evidence usefulness, or output quality.
- Do not fake model-owned success with canned outputs, framework-level business
  mappings, deterministic substitutes, or test-only production branches.
