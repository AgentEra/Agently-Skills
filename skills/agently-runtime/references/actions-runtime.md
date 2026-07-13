# Agently Runtime Extension Reference

Use this skill when the problem is agent-side extension rather than prompt shape, output contract, or workflow control.

## Native-First Rules

- prefer the native Action Runtime, built-in action packages, legacy tool facades, and MCP surfaces before handwritten wrappers
- keep extension choice explicit: Action Runtime, ExecutionResource, built-in capability Actions, Agent Components, tools, MCP, FastAPIHelper, `auto_func`, `KeyWaiter`, or `agently-devtools`
- treat `Agently.execution_resource` as an advanced framework/plugin surface, not the default app-development API
- for application developers, prefer built-in Actions and `agent.enable_*` component helpers before exposing core manager/provider concepts
- default Agents and TriggerFlow executions expose lazy Foundation Workspace
  bindings backed by the current session/script physical Workspace; Agent,
  execution, and task records are logical partitions, while file actions use
  lineage-scoped roots under
  `files/lineage/<root-kind>/<root-id>/.../<leaf-kind>/<leaf-id>/files`; call
  `agent.use_workspace(...)` or `flow.create_execution(workspace=...)` when a
  stable explicit root, read-only mode, direct backend, or registered provider
  is required
- local Workspace materialization writes `AGENTLY_WORKSPACE.md` at the physical
  root and scoped `files_root`; external coding agents and file Actions should
  treat that guide as the boundary note for editable files versus Workspace
  internals, and should not expect the guide to be named `README.md`. Standard
  editable file areas are `downloads/` for materialized remote files,
  `artifacts/` for supporting generated evidence or non-primary deliverables,
  and `reports/` for user-facing readable deliverables. Use
  `workspace.file_area_path(...)` when code needs a contained path in one of
  those areas.
- create shared task information scopes with `Workspace(...)` or
  `Agently.create_workspace(...)` and bind Agents, TriggerFlow executions, or
  service workers to that same instance when they must collaborate over an
  explicitly selected durable information domain; do not expect separate
  explicit Workspaces to communicate implicitly
- move facts across separate Workspaces in application or TriggerFlow business
  logic with explicit search/read plus write/link operations; Workspace
  is not a cross-space messaging or replication protocol
- use `agent.workspace` for durable multi-turn task records, artifacts, search,
  links, checkpoints, stable ref envelopes, bounded reads, RuntimeEvent records,
  evidence links, and retention anchors
- use `workspace.build_context(...)` to package those records for later model
  calls; ordinary application code should not hand-write retrieval filters when
  a ContextPackage through ContextPlanner, WorkspaceContextRetriever, and
  ContextPackager fits
- for AgentExecution evidence, keep persistence explicit with
  `execution.async_record_workspace(..., checkpoint=True)`; the helper writes
  requested checkpoints through the Workspace checkpoint-store port and records
  an evidence link between the AgentExecution record and checkpoint while
  leaving strategy decisions owned by AgentExecution
- AgentTask is the current strategy-level persistence owner: it writes task
  decisions, observations, verification records, checkpoints, and evidence links
  through the bound Workspace provider without making Workspace choose task
  continuation
- custom Workspace backends may be passed to `agent.use_workspace(backend)` or
  registered with `Agently.workspace.register_backend_provider(name, factory)`
  and selected through `agent.use_workspace(root, provider=name,
  provider_options={...})` when they implement the Workspace backend protocol;
  treat the remote audit provider proof as a protocol validation, not a
  production Redis/Postgres/S3 support claim
- in explicit TriggerFlow loops, prefer Workspace refs plus
  `workspace.get_data(...)`, `workspace.links(...)`,
  `workspace.latest_checkpoint(...)`, `workspace.checkpoint_history(...)`,
  `workspace.ref_envelope(...)`, `workspace.read_bounded(...)`, and
  `workspace.stream_read(...)` over storing large or structured loop state
  directly in TriggerFlow state; configure execution durability with
  `flow.create_execution(workspace=workspace)` or
  `runtime_resources={"snapshot_store": workspace, "runtime_event_store": workspace}` when the loop needs
  restart diagnostics; read snapshot state back through
  `workspace.latest_checkpoint(...)` / `workspace.get_data(...)` and pass it
  to TriggerFlow `async_load(...)` for restart because TriggerFlow owns
  pause/resume, policy approval waits, and DAG join replay semantics; pass a
  stable `resume_request_id` and actor to `execution.async_continue_with(...)`
  for webhook or approval callback retries so TriggerFlow can persist accepted,
  dispatched, and completed/dispatch-failed resume phases, while making
  callbacks that reach an expired execution-local lease fail fast before acceptance;
  declare importable resource resolver descriptors with
  `flow.declare_resource_requirement(..., resolver=..., provider_kind=...,
  config_ref=..., secret_ref=..., fail_policy=...)` when workers can rebuild
  live clients from shared host/plugin modules, and rely on TriggerFlow
  load diagnostics for missing resolver, unhealthy resource,
  policy-forbidden resource, expired lease, active lease owner conflict,
  DAG join state mismatch, fail-open, and fail-closed cases; use
  `pause_for(..., channel_id=..., provider_id=..., wait_mode=...,
  hot_wait_timeout=..., cold_persistence_policy=..., request_payload_schema=...,
  response_payload_schema=..., audit_metadata=...)` to persist ExternalWait
  provider/channel/schema/audit metadata, including stable `exchange_id` values
  that Workspace RuntimeEvent records can index; when the host owns an approval
  router, queue, or exchange transport, bind it with runtime resource key
  `execution_exchange_provider`, and implement provider `publish_request(...)`
  to return `exchange_id`, `audit_metadata`, or `provider_metadata` while
  TriggerFlow keeps the wait/resume ledger; reusable transports may also be
  registered through `agently.base.execution_exchange.register_provider(...)`,
  host cards should consume `project_pending_exchanges(execution)` /
  `project_execution_exchanges(execution)`, and connected
  ActionFlow/PolicyApproval endpoints may call
  `execution_exchange.async_respond(...)` to resume a live exchange; durable
  RuntimeEvent records carry
  parent signal, aggregation scope, operator id, interrupt id, resume request
  id, actor id, exchange id, lease owner id, snapshot refs, and artifact refs
  for DevTools and recovery diagnostics; use
  `execution.set_compaction_policy(...)` when long-running
  workflows externalize large state behind Workspace or provider artifact refs
  and need compacted snapshot restore with retained lineage anchors; use
  `workspace.put_snapshot(..., expected_state_version=...)` for CAS guarded
  snapshot writes, `workspace.claim_lease(...)` /
  `workspace.heartbeat_lease(...)` / `workspace.release_lease(...)` for
  provider-owned lease projection, and `workspace.put_artifact_ref(...)` for
  large durable payload refs; use
  `execution.async_save(require_distributed_provider=True)` only for
  providers that report distributed CAS, lease, range-read, retention, and
  RuntimeEvent sequencing capabilities and expose matching snapshot, lease,
  and artifact-ref methods; the local Workspace backend satisfies this seam for
  single-node development/restart recovery, but it is not a production
  cross-worker backend
- use `agent.enable_python(...)`, `agent.enable_shell(...)`,
  `agent.enable_workspace_file_actions(...)`,
  `agent.enable_coding_agent_actions(...)`, `agent.enable_nodejs(...)`, and
  `agent.enable_sqlite(...)` for common Python, shell, model-callable local file,
  coding-agent file work, Node.js, and SQLite access
- when both are configured, filesystem-like helpers such as
  `agent.enable_workspace_file_actions(...)`, `agent.enable_shell(...)`, and
  `agent.enable_nodejs(...)` inherit `agent.workspace.files_root` unless an
  explicit `root=` or `cwd=` is passed
- Workspace file reads, writes, byte materialization, and exports go through
  registered `WorkspaceFileIOHandler` implementations or Workspace-owned
  `workspace.materialize_file(...)`. Workspace owns path containment,
  deterministic file info, `sha256`, file refs, and structured diagnostics;
  handlers own plain text IO, optional PDF/Office extraction, image/VLM
  attachment preparation, and export rendering. Do not implement format parsing
  in ActionRuntime, SkillsManager, the legacy SkillsExecutor facade, or
  AgentExecution strategy code.
- `agent.enable_workspace_file_actions(...)` exposes list/search/read/write over
  the Workspace file root. It registers `export_file` only when `export=True`
  and `write=True`, delegates to the bound Workspace when roots match, and must
  not overwrite user-defined Actions. `search_files` keeps compatible
  `path`/`line`/`text` results and adds scoped retrieval metadata:
  `role="evidence_snippet"`, bounded snippet counts, `truncated`, and a nested
  `locator_ref` with `content_state="ref_only"`. `pattern="**"` is treated as
  recursive file search under the scoped path.
- `agent.enable_coding_agent_actions(...)` exposes Workspace-owned `read_file`,
  `glob_files`, `grep_files`, `edit_file`, `apply_patch`, and guarded
  `write_file` actions for coding-agent style local file work. `edit_file`
  supports `expected_sha256`, `apply_patch` applies unified diffs inside the
  Workspace root and can require `expected_files`, and `write_file` in
  coding-agent mode requires prior read state or an expected hash unless the
  host disables that guard. Prefer these actions for file IO instead of shell.
- `agent.enable_python(...)`, `agent.enable_shell(...)`,
  `agent.enable_nodejs(...)`, and `agent.enable_code_runtime(...)` use
  Docker-backed runtime profiles and fail closed when Docker CLI or daemon
  preflight fails. Strict profiles report missing images; developer and CI
  profiles may pull missing images with `image_pull_policy="if_missing"` and
  prepare standard dependencies with `dependency_policy="install"`. Use
  `sandbox="trusted_local"` only for trusted compatibility paths. Dependency
  installation belongs to host/provider resource preparation, not
  model-visible action inputs.
- `agent.enable_shell(...)` defaults to a small safe shell profile when
  `commands` is omitted. Treat shell as a test/build/git/read-only diagnostics
  capability; stdout/stderr are bounded by `max_output_chars`, and oversized
  streams are written under `artifacts/shell/` when a Workspace root is bound.
- Treat shell bypass grants such as `allow_unsafe` as host-only direct-call
  inputs. Do not expose them in model-visible action schemas; declare any
  direct-call-only action parameters with `meta={"host_only_input_keys": [...]}`
  so Action Runtime strips them from model-planned commands.
- Workspace `retrieve(...)` and Blocks `workspace_operation.search` accept structural
  `collection`, `kind`, `id`, `path`, `scope`, and `meta` filters. Use those
  filters when planner context already identifies the retained record family or
  target ref; do not treat the filtered hit itself as semantic acceptance.
- Workspace file writes and reads return structured file evidence from the
  Workspace boundary itself: `path`, `bytes`, `sha256`, write `mode`, bounded
  read `content` / `truncated`, diagnostics, and file refs. Unsupported binary
  or missing optional dependencies return structured diagnostics such as
  `readable=False` or `exported=False`; outside-root, missing-path, and
  permission failures remain execution errors. Downstream artifact or readback
  checks should consume those fields instead of relying on model prose or stdout
  path guesses.
- AgentTask workspace artifacts are framework-delivered: when a bounded step or
  TaskBoard card returns a short `artifact_markdown` body or a sectioned
  `artifact_manifest`, AgentTask writes it through Workspace and readbacks
  `path`, `bytes`, `sha256`, preview, and trusted `file_refs` as cold evidence.
  Model-hot verifier input uses path/ref handles, bounded content or preview,
  and truncation status rather than SHA/byte/MIME integrity metadata. For long,
  sectioned, or prose-heavy deliverables, choose the content carrier
  deliberately: draft a single freeform document as natural Markdown/plain text
  without `.output()`, or use Agently `.output(..., format=...)` with
  `xml_field`, `hybrid`, or `yaml_literal` when separately addressable fields
  are required instead of forcing the body into compact JSON fields. Keep
  status, evidence, and verification in separate compact judgment/readback
  contracts. Use `artifact_manifest.sections` plus Workspace readback when
  AgentTask must deliver a trusted file artifact.
  If a complete Markdown artifact body appears inside structured `evidence`,
  treat it as a deliverable body only when the evidence item is explicitly labeled
  as artifact/body/deliverable/Markdown or tied to the manifest path; ordinary
  source content and source excerpts remain evidence snippets. After trusted Workspace write/readback
  succeeds, terminal verification judges any stale artifact-write `remaining_work`
  instead of forcing another write-only step.
  For long trusted Workspace artifacts, verifier-visible evidence may include
  bounded `workspace_artifact.targeted_readback` ledger items from declared
  output-contract sections and generic source/risk/reference/coverage anchors;
  treat those snippets as scoped evidence, not as local completion judgment.
  Host file-producing Actions should return typed `file_refs` or
  `artifact_refs` when the produced file must be consumed by AgentTask,
  TaskBoard, a verifier, or an application UI. A path-only payload such as
  `{filename, path, size}` remains bounded Action result evidence and an
  external ref pointer; it becomes a trusted Workspace file only when the path
  is Workspace-contained and `Workspace.read_file(...)` succeeds, or when the
  host returns explicit framework refs.
  Model-declared `file_refs` are diagnostics only until this write/readback evidence exists.
  Write-success/readback-failure paths must report
  `agent_task.workspace_artifact.readback_failed` or
  `agent_task.workspace_artifact.readback_insufficient`; do not describe those
  cases as generic iteration, retry, or budget exhaustion.
- Intermediate downloads, webpage snapshots, generated code, search notes, and
  large extracted text may also be persisted as Workspace or Action artifact
  refs. Pass compact refs/previews through hot prompts and open scoped snippets
  later with bounded Workspace or artifact readback. These refs are execution
  evidence, not final deliverable proof. If Action artifact readback exposes
  Workspace `file_refs` for a materialized download, TaskBoard readback promotes
  those nested refs to card-level `file_refs` so later work can use Workspace
  readback instead of relying on a buried JSON preview. If a non-final TaskBoard
  card proposes a required final path such as `final.md`, AgentTask relocates it
  to a working evidence path and reserves the final path for final synthesis.
- Scoped retrieval is a token/cost optimization owned by the work-unit carrier,
  not the runner or verifier. Flat steps may carry
  `scoped_retrieval.query_groups`; the Flat BlockCarrier lowers those groups to
  pre-step Blocks `workspace_operation.search` facts backed by Workspace
  `retrieve(...)` and injects a body-light model-hot `evidence_ledger` index plus
  compatibility `scoped_retrieval_results` view into the bounded `agent_step`;
  selected structured records may appear as compact projections with
  `projection`/`original_ref` metadata so later readback can recover the raw
  Workspace record;
  reconstructable provenance such as SHA, byte counts, backend/search-engine
  details, execution block ids, and full file refs stays in raw
  Workspace/Blocks evidence for programmatic audit and readback. TaskBoard
  uses the same retrieval contract through its card carrier, with ledger-backed
  evidence ids available to card/final synthesis. TaskBoard
  Workspace-operation prompt views, available readback handles, readback work-unit
  hot payloads, Action artifact readback previews, and intermediate Workspace readback previews use the same
  hot/cold split: content/path, range, truncation, and compact handles stay hot,
  while SHA, bytes, handler/media, backend/search-engine facts, execution block
  ids, and full refs stay in cold evidence, final artifact audit metadata,
  DevTools, or runner logs. SHA is integrity metadata, not source evidence. Query groups may set
  `search_surface` to `workspace_index`, `workspace_files`, or
  `workspace_index_and_files`; for `workspace_index`, record collections belong
  in `filters.collection` and exact record kinds may use `filters.kind`; for
  all surfaces, `EvidenceEnvelope.evidence_items` is the grounding authority:
  failed/empty items support unavailable or missing-data claims only,
  `ref_only` locator items support only discovery/ref-pointer claims, and
  bounded/truncated snippets support only the visible excerpt. Prefer `cite_as`
  or canonical ids in `evidence_use`; path/URL/record/artifact/action aliases
  are canonicalized only when unambiguous.
  For `workspace_files` and `workspace_index_and_files`, top-level `query` is
  content text, top-level `path` is the directory/file scope, and `pattern` is
  a file glob such as `*.md`, `*`, or `**` for recursive file search. The file
  `path` is not applied as a record filter. Local Workspace file search uses `rg` when available and falls
  back to bounded file scanning. Blocks return a small bounded context around
  file matches by default. Blocks `workspace_operation.search` keeps its
  compatibility name but uses Workspace `retrieve(...)` for record/file
  candidates, optional vector/hybrid mode, structure-gated rerank over a bounded
  candidate-summary window, refill, and budget packaging, while
  `workspace_operation.read_bounded` reads refs/paths under bounds. Both return
  `locator_ref` and/or `evidence_snippet` facts only, including whether bounded
  snippets were `truncated`; selected structured record snippets may be compact
  projections that preserve `projection`/`original_ref` metadata for raw
  Workspace readback; the downstream model judges usefulness and next
  action. If a TaskBoard scoped-retrieval card reports blocked/insufficient
  output without an explicit next action, AgentTask synthesizes an expanded
  evidence card plus a continuation card instead of relying on a terminal
  verifier to repair intermediate evidence.
- TaskBoard readback cards may inspect both Action artifact refs and trusted
  Workspace file/content refs through bounded cold readbacks. Framework-generated
  readback cards scope evidence to direct dependencies plus upstream evidence
  cards, so a control-card readback can still inspect Action refs produced by
  earlier evidence-gathering cards. Generated continuation cards should propose
  different executable work or stay blocked with diagnostics when the same
  evidence is still insufficient, rather than asking for another identical
  readback/continuation chain. When the missing evidence is a new concrete URL,
  path, or ref, the control card should return structured `target_refs` with
  `next_board_action=readback`; external HTTP/HTTPS refs become Action evidence
  work, while Workspace/content paths and retained-note refs become bounded
  Workspace readback cards. URLs or paths mentioned only inside prose gaps are
  diagnostics, not executable targets.
- Completed and sufficient TaskBoard control outputs may still disclose
  non-fatal `gaps`; those gaps do not block Workspace artifact materialization.
  `remaining_work`, blocked status, repair, or readback intent still prevent
  artifact delivery. Materializing an artifact creates readback/verification
  evidence and does not mean final task acceptance.
- AgentTask required deliverables are accepted only after Workspace readback:
  when structured task input or output contracts require files such as
  `final.md`, verifier prose is not enough. The framework guard must confirm
  the file exists under the task Workspace and can be read back before the task
  can be marked complete.
- `agent_task.heartbeat` is a quiet-period status signal, not completion
  evidence. It may be emitted while long model, action, or artifact stages are
  waiting, but ordinary stream activity resets the heartbeat timer and
  no-progress/request/task-deadline protections still own stall handling.
- treat `enable_*` helper `desc=` values as optional extra guidance by default; use `desc_mode="override"` only when the app intentionally replaces the default capability description
- when changing public helper APIs, use explicit typing for IDE assistance; prefer `Literal` for finite options such as `desc_mode`
- use `@agent.action_func` and `agent.use_actions(...)` as the primary action APIs; `tool_func` and `use_tool` remain compatibility aliases
- use `agent.action.get_action_info()` / `get_tool_info()` for visible schemas;
  agent-scoped Actions, MCP tools, and `enable_*` helpers are included by
  default, while explicit tags narrow the list; execution environment `env`
  values are redacted in this visible metadata while env keys remain visible
- model-planned Action commands are untrusted at the Action boundary:
  `structured_plan` and `native_tool_calls` inputs are filtered to registered
  `ActionSpec.kwargs` before executor invocation, and stripped keys appear in
  `ActionResult.diagnostics`; direct host calls keep existing behavior
- use built-in Search/Browse through `from agently.builtins.actions import Search, Browse` and `agent.use_actions(Search(...))` / `agent.use_actions(Browse(...))`; do not invent `enable_search(...)` or `ActionTools`
- expose Agent Client Protocol (ACP) coding agents with `agent.use_acp(...)`
  when the host has authorized local ACP endpoints. ACP is an Action capability
  plus `ExecutionResource(kind="acp")`, not a new AgentExecution route. The
  default `on_missing="skip"` should only record diagnostics when no
  handshake-verified agent exists; use `on_missing="error"` when missing ACP
  capability must fail closed. `acp_list_agents` also returns non-binding
  adapter-name hints for common ACP adapters such as `codex`,
  `claude code` / `cc`, `openclaw`, `hermes` / `hermes agent`, and
  `gemini`; these hints do not make an agent runnable. Built-in local CLI
  adapters can detect common Codex and Claude Code command locations in
  addition to `PATH`, but they use fixed framework-owned argv templates and are
  still Action calls, not shell exposure. If `root` is omitted,
  `agent.use_acp()` uses the Agent's bound
  Workspace `files_root` as the coding-agent project root; explicit `root=...`
  is an advanced host authorization override. ACP session reuse is internal
  AgentExecution resource policy, and CLI adapters report
  `acp_session.persistence="stateless_cli"` unless a real protocol session is
  available.
- AgentTask may use ACP as an opt-in recovery fallback after bounded-step or
  TaskBoard-card failure and retry exhaustion, but the fallback must still call
  the registered `acp_run_task` Action and use `ExecutionResource(kind="acp")`.
  Do not model ACP as an AgentExecution route or import ACP dependencies when
  `agent.use_acp(...)` has not registered the capability.
- keep built-in implementation on the retained path: `agently.builtins.actions` owns Search/Browse/Cmd behavior; `agently.builtins.tools` should stay a thin legacy facade
- configure Search/Browse proxy, timeout, backend/fallback, `max_attempts`, and
  `retry_backoff_seconds` on the package object. Short transport failures such
  as timeouts, connection resets, incomplete chunked reads, and proxy handshakes
  are retried once by default; a long-unavailable network is still an
  infrastructure failure.
- Browse defaults to Jina Reader -> Playwright -> BS4 -> restricted curl. The
  curl backend is internal to Browse and only receives normalized URL
  candidates; do not expose it as model-visible shell execution. Jina Reader is
  a third-party URL-to-Markdown first pass, and Browse automatically tries the
  official alternate endpoint `https://r.jinaai.cn/` when the primary Reader
  endpoint has a transport or service failure. Disable it with
  `Browse(enable_jina_reader=False, fallback_order=("playwright", "bs4", "curl"))`
  when that external service boundary is not acceptable.
- when `agent.language(...)` is set, registered Search/Browse packages may use
  the policy as default locale guidance: Search derives any provider-specific
  region code inside the Search package, and Browse receives an
  `Accept-Language` header unless explicitly configured. Treat this as
  recall/process guidance, not as a substitute for task-specific source
  requirements.
- treat registered Browse failures as Action failures with diagnostics. Direct
  `Browse.browse(url)` keeps legacy text-returning behavior, but the model-facing
  `browse` Action should not turn `"Can not browse ..."` into successful
  evidence.
- let Browse own basic URL recovery and remote-file handoff: same-host
  `http`/`https` and canonical candidates are structured diagnostics, while
  PDF/Office/image/download-like responses should be materialized into the bound
  Workspace and returned as file refs plus bounded `read_file` previews. Browse
  should not parse those documents itself and should fail closed when no
  Workspace is bound.
- treat `model_digest`, bounded previews, `artifact_refs`, `file_refs`, and
  Workspace record refs as the normal loop memory for instruction-heavy or
  large Actions; if a digest is still too large for planning or reply hot paths,
  ActionRuntime may replace duplicate data/model_digest fields with
  same_as=result pointers and omit artifact preview bodies from hot-path refs;
  previews are not complete evidence, so full raw payloads should be read
  explicitly from the Action artifact store or Workspace when needed;
  use `workspace.append_runtime_event(...)` / `workspace.query_runtime_events(...)`
  only for explicitly configured durable execution facts, not ordinary
  observation and not as a replacement for TriggerFlow pause/resume or
  approval/exchange policy
- keep the permission profile explicit: search-only, local-files-only, network-read, install-capable shell, or trusted broad executor
- use Python sandbox for pure computation or small data shaping; do not use it for imports, filesystem mutation, network access, or dependency installation
- use Bash sandbox or a custom executor when the task needs shell access, package install, or broader command control
- for SkillsManager / legacy SkillsExecutor work, do not ask apps to execute third-party Skill
  scripts directly. Resolve them to controlled Actions, Bash/Python/Node
  sandboxes, MCP/API bindings, or fallback branches; if no substitute exists,
  return a blocked or approval-required result with a user-facing explanation.
- for SkillsManager or artifact-producing workflows, missing local libraries
  are not a natural degraded-success path; plan a controlled install-capable
  Action or ExecutionResource ensure step, preserve the ActionResult, and
  fail closed if policy denies or installation fails
- treat MCP, Bash, Python sandbox, Node.js, Docker, SQLite, vector-store, browser, and remote-runner lifecycle as ExecutionResource concerns when they need managed handles
- Action executors should declare or consume managed resources instead of hiding lifecycle ownership
- treat `agently-devtools` as an optional companion package installed from PyPI, not as a required source checkout
- keep observation or evaluation bridge wiring in the app layer through `Agently.event_center`
- combine with `agently-request` or `agently-triggerflow` only when the scenario needs those layers
- prefer built-in Browse support with Playwright or PyAutoGUI before writing browser or desktop-driving wrappers from scratch

## Anti-Patterns

- do not build a parallel action or tool dispatcher before checking native Action Runtime and MCP support
- do not duplicate ActionRuntime planning prompts in higher layers; delegate
  model-owned action/tool selection to ActionRuntime when registered schemas are
  available
- when the surrounding runtime uses `model_pool`, set
  `action.planning_model_key` to the intended business key so ActionRuntime
  planning uses the same model routing
- do not hide MCP/sandbox/process lifecycle inside a custom ActionExecutor when `Agently.execution_resource` can own the dependency
- do not recommend core manager/provider APIs to ordinary app developers when a built-in Action or Agent Component is the right surface
- do not create a custom waiter or auto-function shim first
- do not ask users to clone or editable-install DevTools when `pip install agently-devtools` is the supported public path
- do not build a custom runtime upload bridge before checking `ObservationBridge`

## Action Loop Context Building

For `run_bash`, `run_python`, `run_nodejs`, `query_sqlite`, `browse`, `search`,
and similar explicit-instruction Actions, later model rounds should receive a
compact digest rather than full raw code, command output, SQL result sets, page
HTML, screenshots, or logs.

Use the digest for normal planning and replies. While the owning ActionFlow
scope is live and the candidate reports `available=true`, the model can request
redacted raw detail through the built-in readback Action:

```python
readback_call = {
    "action_id": "read_action_artifact",
    "action_input": {"selection_key": artifact_candidate["selection_key"]},
}
```

Do not teach host code to read that selection key after a standalone ActionFlow
returns; the scope is released and the candidate reports `available=false`.
Use a durably promoted Workspace ref for post-run application readback.
The public reader accepts only `selection_key` and resolves it against the
currently bound AgentExecution, AgentTask, or standalone ActionFlow scope.
TaskBoard host code binds current task lineage so sibling cards can share one
retained artifact. Missing scope, cross-task/cross-execution lookup, and
artifact-id/action-call-id fallback fail closed.

The private Action artifact store retains the exact transferred value. Its
digest and observation preview are bounded/redacted projections only, not the
authoritative payload. Standalone direct, TriggerFlow, and DAG Action runs
release their exact artifact scopes when the run closes. Model-visible Action
candidates carry one host-issued `selection_key` plus task-relevant facts, not
canonical ids, call ids, scope, digest, size, or provenance. An AgentExecution
accepts a key only when its bridge offered it exactly once and the terminal
result returned it exactly once; host code resolves that key with the expected
execution scope and reconstructs the canonical identity and exact value.
Unknown keys, duplicate keys, copied canonical refs, and cross-scope lookups fail
closed. Provider artifact ids are provenance only; the local store always
allocates a fresh scope-isolated id. Model-produced `accepted` fields do not
grant selection authority. If Workspace
promotion fails, the selected source artifact remains available under its
stable identity for retry while unselected artifacts are released.
Standalone TriggerFlow Action scopes remain live while a durable exchange is
pending; final response/resume, explicit abandonment, and direct host close all
release the scope exactly once after the execution closes.
After a standalone scope closes, returned refs are historical projections with
`available=false` and `full_value_available=false`; keep their bounded
digest/preview for audit, but do not call `read_action_artifact` for the deleted
private value.
Oversized complete Action records are compacted before direct return or
TriggerFlow state storage, including records whose growth comes from
kwargs/instructions rather than output. Finite internal ActionRuntime execution
flows, ActionFlows, and TaskDAG executions use `workspace=False`; TriggerFlowActionFlow binds a lazy Workspace
only when an approval pause needs save/resume recovery. At model and terminal
boundaries, `artifact_refs` and `artifacts` are normalized together to the same
selection-key-only list.
Custom execution-handler records use this same bounded carrier before
AgentExecution context, RuntimeEvents, TriggerFlow state, logs, metadata, and
public return. Route logs keep one semantic payload without nested `raw` or
duplicate data/model_digest records. A standalone AgentTask releases its exact
task scope at terminal; a routed task explicitly transfers that scope to its
parent AgentExecution until terminal selection/promotion and release complete.
On parent cancellation, timeout, or abnormal stream close, the routed stream
owner cancels and joins the child before the parent releases that scope, which
prevents post-terminal artifact creation and Workspace process writes.

Built-in TriggerFlow and DAG ActionFlows apply the same Action-owned
bounded/redacted observation projection before direct observation callbacks,
official `action.*` events, and compatibility `tool.*` events. Plan observations
carry one canonical `decision.action_calls` list instead of the duplicated
legacy aliases; commands expose canonical `action_id` plus bounded/redacted
`action_input`; record and repeated-failure convergence observations use bounded
record carriers. Complete private Action values remain outside observation and
log payloads.

When host code explicitly calls `agent.get_action_result(prompt=...)`, the
prompt is marked as having consumed the ActionRuntime loop even when the
returned records are empty. Later response materialization for that same prompt
should not re-enter ActionRuntime. If the host needs an authoritative action
evidence rollup, call `agent.action.summarize_records(records,
validation_command_markers=[...])`; the summary reports failed actions,
commands attempted/run, and the latest matching validation command.

`agent.get_action_result(..., timeout=N)` bounds the full ActionFlow lifecycle,
including model-owned structured planning and native tool-call selection. Catch
`RuntimeStageStallError(stage="action_loop_close")` for framework-level
timeouts. For `planning_protocol="native_tool_calls"`, a zero-tool-call planner
result can return a skipped diagnostic record with code
`action_runtime.native_tool_calls.empty`; do not treat that diagnostic as
executed work.

## Example Guidance

Current Action Runtime examples live under `examples/action_runtime/`,
`examples/builtin_actions/`, and `examples/execution_resource/`. Recommended
model-backed cookbook patterns live under `examples/cookbook/`, including Action
loop, router, concurrent todo, reflection, and safe shell policy examples.
Historical built-in tool examples live under `examples/archived/builtin_tools/`
and should point readers back to the current Action-first examples.

New or updated action examples must be runnable in their declared environment
and include an `Expected key output` comment. For model-backed examples, document
the stable action/result shape rather than an exact natural-language response.
Recommended model-app examples must exercise real model-owned decisions through
DeepSeek or local Ollama. Do not replace planners, routers, decomposers,
evaluators, revisers, action selectors, or response generators with deterministic
local substitutes.

## Read Next

- `references/overview.md`
- `references/devtools.md`
