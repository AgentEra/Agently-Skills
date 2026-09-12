---
name: agently-runtime
description: "Use when the user wants Agently runtime extension capabilities: AgentExecution plugins or terminal review/artifact policies, Action Runtime, built-in Action packages, MCP access, ExecutionResource lifecycle, TaskWorkspace file Actions, RecordStore durability, FastAPIHelper or streaming API exposure, or optional agently-devtools observation and evaluation."
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
- AgentExecution plugin selection, goals, final validation, review, or artifact
  delivery: read `references/agent-execution.md`.

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
| `AgentExecution` plugin | One isolated draft, identity, production lifecycle, final policies and result/stream APIs; owns its typed nested components. |

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

On the 4.1.4.8 development line, `.auto_continue()` replaces the recommended
spelling `.ensure_long_output()`; the released spelling remains an alias.
This is conditional request delivery, not long-form production or task resume.

- Select a task file root with `agent.use_task_workspace(path, mode=...)`.
  Enable model-callable file work with
  `agent.enable_task_workspace_file_actions(...)` or
  `agent.enable_coding_agent_actions(...)`.
- `TaskWorkspace` is a file boundary only. Use its read/write/edit/glob/grep/
  patch/export methods for task files and artifacts; do not store arbitrary
  durable records inside it through a hidden database API.
- Direct `.auto_continue()` delivery uses execution-private TaskWorkspace
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

For general authorized Skill-script execution, one `agent.enable_shell(...)`
with explicit environment, approval and resource paths avoids per-script
Actions. Read [Shell environments](references/actions-execution-resource.md#general-shell-4148-development)
for the 4.1.4.8 development contract and platform limitations. The narrower
exact-revision script helpers below remain available; they are not a prerequisite
for the general Shell path.

- Treat standard `SKILL.md` packages as guidance plus addressable resources.
  They do not own execution strategy, routing, Action mounting, permissions, or
  side-effect proof.
- Install and inspect immutable revisions through `SkillLibrary` or the thin
  `Agently.skills_executor` management facade. Use registered
  `SkillSourceProvider` implementations for authorized local or Git sources;
  pin a Git `ref` and optional `subpath` rather than inventing a host checkout
  helper.
- Use the same composition grammar as Actions. Declare reusable Agent defaults
  with `agent.use_skills(..., always=True)` and one-run additions with
  `execution.use_skills(...)`, `execution.require_skills(...)`, or
  `execution.use_skills_packs(...)`. Do not introduce a second public
  collection manager for Skills.
- Treat only those declarations as the current execution's Skill scope.
  `AgentExecution` resolves and freezes exact revision refs before semantic
  selection; an empty declaration set does not expose the global SkillLibrary.
- Treat every later user request as a fresh AgentExecution. Agent defaults are
  reconsidered against the new task; execution-local Skill/Action declarations
  are not inherited. Session carries conversation and memory, never executable
  scope or permission.
- Let `AgentExecution` prepare the shared TaskContext and read it for the
  actual consumer/phase with `async_prepare_task_context()` and
  `async_read_task_context(...)`.
- When a complete root `SKILL.md` is already disclosed, do not also deliver or
  offer its indexed child sections. Use child sections only for a lossy parent
  projection or a later bounded read.
- Provide Actions/MCP/ExecutionResources explicitly. Reading a Skill may inform
  the model that an operation exists; it never creates or authorizes that
  operation.
- When trusted, exactly bound Skill revisions contain executable scripts, call
  `agent.enable_skill_script_exec(...)` only after
  `execution.async_prepare_task_context()`. Pass an explicit
  `SkillScriptAuthorization`; the helper reuses one stable restricted ordinary
  Action definition per Agent/language and binds authorization only to the
  current execution. Enabling it must preserve the already prepared Skill
  selection. The model
  supplies only a relative `script_path` and bounded `args`; the host resolves
  one unique resource from the frozen bindings. Narrow the Skill declarations
  when paths collide. The released `agent.bind_skill_script_action(...)`
  remains available when host code intentionally needs one exact-path binding.
  Read published artifacts through the same execution's TaskWorkspace.
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

## AgentExecution

Read [Execution plugins and final policies](references/agent-execution.md) before
selecting producers, declaring goals, or configuring validation/review/artifacts.
Use a fresh agent.create_execution() for multi-statement setup. Skills and
Actions remain execution-scoped; new user requests receive new executions.
Keep get_data for business values, get_full_data for the route/task envelope,
and get_meta for process facts. A declared Skill does not authorize its Actions.

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
