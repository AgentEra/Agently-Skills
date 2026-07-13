---
name: agently-runtime
description: "Use when the user wants Agently runtime extension capabilities: Action Runtime, built-in action packages, legacy tool compatibility, MCP access, ExecutionResource lifecycle, FastAPIHelper or streaming API exposure, auto-function helpers, KeyWaiter, or optional agently-devtools observation, evaluation, and playground integration."
---

# Agently Runtime

Use this skill when the app needs model-callable capabilities, managed execution
dependencies, service exposure, or development/runtime tooling around an
existing request or workflow design.

If the owner layer is still undecided, start with `agently`. If the
problem is multi-step orchestration, use `agently-triggerflow` first and return
here for Actions, ExecutionResource, service, or DevTools details.

## Route Inside This Skill

- Action Runtime, `@agent.action_func`, `agent.use_actions(...)`, built-in Search/Browse, sandbox actions, or legacy tools -> `references/actions-runtime.md`
- Action vs ExecutionResource boundaries, `agent.enable_*` helpers, provider lifecycle, managed MCP/sandbox/process/browser/SQLite resources -> `references/actions-execution-resource.md`
- observation, evaluation, playground, local logs, or `agently-devtools` -> `references/devtools.md`

## Native-First Rules

- prefer `@agent.action_func` and `agent.use_actions(...)`; `tool_func`, `use_tool`, `use_tools`, and `agently.builtins.tools` are compatibility surfaces
- use built-in web packages through `from agently.builtins.actions import Search, Browse` and mount with `agent.use_actions(Search(...))` / `agent.use_actions(Browse(...))`
- do not invent `enable_search(...)`; Search/Browse proxy, timeout, backend,
  and transient retry configuration belongs to the package/executor, not
  ExecutionResource. Registered Browse actions fail closed with structured
  diagnostics when all backends fail; direct `Browse.browse(...)` remains a
  text-returning compatibility helper. Browse defaults to Jina Reader ->
  Playwright -> BS4 -> restricted curl, where curl is an internal normalized-URL
  fallback and not model-visible shell execution. Jina Reader is an external
  URL-to-Markdown first pass and Browse automatically tries the official
  alternate endpoint `https://r.jinaai.cn/` when the primary Reader endpoint has
  a transport or service failure; disable it with
  `Browse(enable_jina_reader=False, fallback_order=("playwright", "bs4", "curl"))`
  when that external service boundary is not acceptable. Browse should
  try same-host protocol and canonical candidates before giving up, and remote
  PDF/Office/image/download bytes should be materialized into the bound Workspace
  with file refs rather than copied into the model hot path.
- treat `agent_task.heartbeat` as observation only: AgentTask may emit it after
  a quiet interval with no other stream items, but any normal progress,
  snapshot, child-execution, delta, or phase event resets the quiet timer.
  Heartbeats help consumers show liveness; they do not satisfy evidence,
  hide stalls, or replace request/no-progress/task deadline timeouts.
- default Agents and TriggerFlow executions expose lazy Foundation Workspace
  bindings backed by the current session/script physical Workspace; Agent,
  execution, and task records are logical partitions, while file actions use
  lineage-scoped roots under
  `files/lineage/<root-kind>/<root-id>/.../<leaf-kind>/<leaf-id>/files`; use
  `agent.use_workspace(...)` or `flow.create_execution(workspace=...)` when
  the app needs an explicit root, read-only mode, direct backend, or registered
  provider, and keep in mind that ordinary model requests do not persist
  automatically
- local Workspace materialization writes `AGENTLY_WORKSPACE.md` at the physical
  root and scoped `files_root`; external coding agents and file Actions should
  treat that guide as the boundary note for editable files versus Workspace
  internals, and should not expect the guide to be named `README.md`. Standard
  editable file areas are `downloads/` for materialized remote files,
  `artifacts/` for supporting generated evidence or non-primary deliverables,
  and `reports/` for user-facing readable deliverables. Use
  `workspace.file_area_path(...)` instead of hand-building those roots when
  application or framework code needs a contained path.
- create application-owned shared Workspace instances with
  `Workspace(...)` or `Agently.create_workspace(...)` and bind each participant
  with `agent.use_workspace(shared_workspace)` or
  `flow.create_execution(workspace=shared_workspace)` when Agents,
  TriggerFlow executions, or service workers must share task information across
  an explicitly selected domain; do not rely on separate explicit Workspaces to
  communicate; use
  `flow.create_execution(workspace=False)` only when an execution should have no
  Workspace binding; finite internal ActionRuntime execution flows, ActionFlows,
  and TaskDAG executions use this no-Workspace path, while TriggerFlowActionFlow binds a lazy Workspace only
  when an approval pause needs save/resume recovery
- move information between separate Workspaces in application or TriggerFlow
  business logic by searching/reading the source Workspace, writing or
  storing records in the destination Workspace, and linking refs as needed;
  Workspace itself is not a cross-space messaging or replication protocol
- for durable multi-turn task records, write through `agent.workspace` or
  explicitly configure it with `agent.use_workspace(...)`; for model-callable
  local file actions, use `agent.enable_workspace_file_actions(...)`, which
  exposes the current Workspace file working tree and inherits
  `agent.workspace.files_root`; for coding-agent style file work, use
  `agent.enable_coding_agent_actions(...)` so reads, glob/grep search,
  targeted edits, unified-diff patches, and full-file writes stay under
  Workspace path, readback, and stale-guard semantics
- Workspace file IO is handler-backed: `workspace.read_file(...)`,
  `workspace.write_file(...)`, `workspace.materialize_file(...)`, and
  `workspace.export_file(...)` use registered `WorkspaceFileIOHandler`
  implementations or Workspace-owned byte materialization. Workspace owns path
  containment, file info, digests, refs, and diagnostics; handlers own format
  parsing, optional dependencies, image preparation, and export rendering. Use
  `agent.enable_workspace_file_actions(write=True, export=True)` only when the
  model should receive an `export_file` Action.
- use `workspace.build_context(...)` for Workspace-backed context building;
  advanced model-assisted planners, vector retrieval, rerankers, and
  compressors should plug into ContextPlanner, WorkspaceContextRetriever, or
  ContextPackager instead of becoming WorkLoop or Action shortcuts
- for explicit TriggerFlow loops, store structured observations and decisions
  in Workspace, link decisions to evidence with `workspace.link(...)` or
  `workspace.link_evidence(...)`, keep large payloads behind
  `workspace.ref_envelope(...)`, recover state with
  `workspace.latest_checkpoint(...)`, bind durable execution ports by creating
  the execution with `flow.create_execution(workspace=workspace)` or with
  `runtime_resources={"snapshot_store": workspace, "runtime_event_store": workspace}`,
  and inspect backend wiring
  with `workspace.capabilities()`; when restoring, read the snapshot state
  through `workspace.latest_checkpoint(...)` / `workspace.get_data(...)` and
  pass it back to TriggerFlow `async_load(...)` so pause/resume and DAG
  join semantics stay owned by TriggerFlow; use
  `flow.declare_resource_requirement(..., resolver=..., provider_kind=...,
  config_ref=..., secret_ref=..., fail_policy=...)` for importable resource
  resolver descriptors when workers can reconstruct live clients from shared
  host/plugin modules, relying on TriggerFlow load diagnostics for
  missing resolver, unhealthy resource, policy-forbidden resource, fail-open,
  and fail-closed cases; use `pause_for(..., channel_id=..., provider_id=...,
  wait_mode=..., hot_wait_timeout=..., cold_persistence_policy=...,
  request_payload_schema=..., response_payload_schema=..., audit_metadata=...)`
  to persist ExternalWait provider/channel/schema/audit metadata, and put a
  stable `exchange_id` in `audit_metadata` when Workspace RuntimeEvent records
  should be queryable by exchange; when the host owns an approval router, queue,
  or exchange transport, bind it with runtime resource key
  `execution_exchange_provider`, and implement provider `publish_request(...)`
  to return `exchange_id`, `audit_metadata`, or `provider_metadata` without
  taking over TriggerFlow resume lifecycle; reusable host transports may also be
  registered with `agently.base.execution_exchange.register_provider(...)`, and
  hosts should render normalized views from
  `project_pending_exchanges(execution)` / `project_execution_exchanges(execution)`
  instead of raw interrupts; connected ActionFlow/PolicyApproval endpoints may
  resolve live exchanges with `execution_exchange.async_respond(exchange_id,
  payload, actor=...)`, which still funnels through TriggerFlow
  `continue_with(...)`; use
  `execution.set_compaction_policy(...)` for long-running
  TriggerFlow executions that externalize large payloads behind Workspace or
  provider artifact refs while keeping only compaction facts and retained
  lineage anchors in the execution snapshot; use
  `workspace.put_snapshot(..., expected_state_version=...)` for CAS guarded
  snapshot writes, `workspace.claim_lease(...)` /
  `workspace.heartbeat_lease(...)` / `workspace.release_lease(...)` for
  provider-owned lease projection, and `workspace.put_artifact_ref(...)` for
  large durable payload refs
- for restart diagnostics in explicit workflows, persist compact RuntimeEvent
  facts through a configured TriggerFlow runtime event store or explicit
  `workspace.append_runtime_event(...)` calls, then query bounded ranges with
  `workspace.query_runtime_events(...)`; Workspace stores durable facts and refs,
  while TriggerFlow still owns pause/resume, replay, DAG readiness, and
  approval/exchange lifecycle semantics; durable RuntimeEvent records now carry
  parent signal, aggregation scope, operator id, interrupt id, resume request
  id, actor id, lease owner id, snapshot refs, and artifact refs. This storage
  is opt-in, so ordinary observation stays in logging/DevTools
  unless the host explicitly binds `runtime_event_store` or appends Workspace
  RuntimeEvents
- for ModelRequest observability, read `payload.model_request_telemetry` from
  existing `model.*` RuntimeEvents when present; it is a compact diagnostic
  payload for provider/model, attempt, run lineage, duration, raw usage,
  normalized/estimated `usage_summary`, request URL, side-channel, and error
  facts; terminal `model.status` may carry estimated input/output character
  lengths without exposing raw request payload. It is not an input to route,
  retry, verifier, quality, planner, or prompt logic
- for webhook, approval, or external callback resume flows, pass a stable
  `resume_request_id` and actor to `execution.async_continue_with(...)`; the
  TriggerFlow resume ledger records accepted, dispatched, and completed or
  dispatch-failed phases; callbacks delivered to expired execution-local leases
  fail fast before acceptance without writing resume ledger entries, while the interrupt carries an ExternalWait
  request envelope for projection and restart diagnostics
- AgentExecution-owned ActionFlow approval waits are projected as stream items
  with path `exchange.pending` / `exchange.resolved`,
  `meta.stream_kind=="exchange"`, and value
  `{"action": "...", "exchanges": [ExecutionExchangeView, ...]}`; frontend or
  service consumers should treat these normalized views as the render contract
  instead of inspecting policy-gate implementation details
- for distributed TriggerFlow recovery, pass
  `require_distributed_provider=True` when persisting snapshots; this must fail
  closed unless the selected providers report CAS, lease, range-read,
  retention, and RuntimeEvent sequence capabilities and expose matching
  snapshot, lease, and artifact-ref methods; use `inspect_load(...)`
  to surface expired lease warnings and active lease owner conflicts before
  dispatch; the local Workspace backend
  satisfies this seam for single-node development/restart recovery, but do not
  describe it as a production cross-worker Redis/Postgres/object-storage
  backend
- third-party Workspace backends can replace the local backend through
  `agent.use_workspace(backend)` or named provider registration with
  `Agently.workspace.register_backend_provider(name, factory)` plus
  `agent.use_workspace(root, provider=name, provider_options={...})` when they
  implement the Workspace backend protocol; current framework tests include a
  protocol-level remote audit provider proof plus Workspace-backed snapshot
  load tests for pause/continue, policy approval waits, and
  `when(..., mode="and")` join progress, but public guidance must not imply
  production Redis, Postgres, or object-storage support until real adapters and
  operational guarantees exist
- for AgentTask applications, enable only the bounded capabilities the task
  may use, such as `agent.enable_shell(...)`,
  `agent.enable_workspace_file_actions(...)`,
  `agent.enable_coding_agent_actions(...)`, `agent.use_actions(...)`, or
  `agent.use_skills(...)`, then create the
  task-strategy AgentExecution draft with `agent.create_task(...)` or the more
  explicit `agent.create_task_loop(...)`; both return AgentExecution drafts, not
  public AgentTask handles. Do not expose broad shell, filesystem, MCP, or
  browser access just because the task loop exists
- when a running task-strategy AgentExecution needs additional optional context,
  use `execution.async_add_guidance(...)` / `execution.add_guidance(...)`.
  This records guidance to the retained AgentTask Workspace and applies it at
  the next safe Flat or TaskBoard boundary. Do not use guidance as completion
  evidence, do not inject it into non-task route prompts, and use TriggerFlow
  `pause_for(...)` / `continue_with(...)` instead when an external answer is
  required before execution may continue.
- when an AgentTask Skills step must perform side effects, grant the
  relevant ActionRuntime tools/actions explicitly through route or effort
  configuration, declare required side-effect actions when a Skills React loop
  should stop after they succeed, and pair the task with structured
  `action_succeeded` evidence requirements for those host Actions. A Skills
  response that says it wrote or read an artifact is not execution evidence by
  itself.
- for AgentTask business examples, print or persist AgentExecution
  stream/result/meta items: use `meta.stream_kind=="snapshot"` for intermediate
  state captures such as context readiness, plan, execution evidence summary,
  and verification gaps;
  enable `options={"agent_task": {"stream_progress": True}}` only when
  natural-language progress is needed; omit `progress_model_key` for template
  progress with no model requests, or set `progress_model_key` to run a
  separate background model that summarizes only existing snapshots/task
  metadata without adding main-loop fields or latency; model-generated progress
  streams `progress_delta` items before the final `progress` item; set
  `agent.language(...)` when final output, process text, progress text, and
  Action package locale defaults should share a language policy; Search derives
  provider-specific region codes inside the Search package, while Browse may use
  `Accept-Language`; use
  `progress_language` per execution or `agent_task.progress.language` globally
  only as progress-text compatibility controls when operator updates must be
  Chinese, English, or another fixed language;
  progress model failures are side-channel diagnostics/warnings, not main task
  `model.request_failed` errors; progress model inputs should be operator-safe
  and omit low-level Workspace/SQLite fallback diagnostics that remain
  available in task meta; requirements, planner, and verifier model requests can
  stream `model_delta` observation items with
  `validation_role=="observation_only"` only when `stream_model_stage_deltas` or
  a stage-specific override is explicitly enabled; use them for UI/log
  visibility only, not for acceptance or verifier evidence; frontend consumers
  should buffer/bucket high-frequency deltas or use smooth incremental rendering
  to avoid render pressure and visible screen jitter
- for AgentTask terminal results, treat `completed` as accepted output
  (`accepted=True`, `artifact_status="accepted"`); explicitly configured
  `max_iterations` can still leave useful Workspace files, but those are partial artifacts
  (`accepted=False`, `artifact_status="partial"`); accepted degraded results use
  `artifact_status="degraded"` and should include a user-facing
  `final_response` that explains the disclosed unavailable/partial evidence
  boundary; useful but unaccepted artifacts and blocked outcomes should also
  include `final_response` so callers can show what was produced, where work
  stopped, and which requirements remain unmet. Prefer `final_response` for
  task-strategy `get_text()` display; use `get_data()` for the business
  `final_result` view and `get_full_data()` for the complete route/task
  envelope. When semantic content quality
  matters, combine deterministic smoke checks with current docs/spec/source
  references or an Agently model-judge request, and do not use counts, keyword
  hits, or task verifier acceptance alone as the primary acceptance signal
- when an AgentTask bounded step or TaskBoard card returns a short
  `artifact_markdown` body or a sectioned `artifact_manifest`, the framework
  writes the deliverable through the bound Workspace and reads it back for
  `path`, `bytes`, `sha256`, preview, and trusted `file_refs` as cold
  evidence; model-hot verifier input uses path/ref handles, bounded content or
  preview, truncation status, and readback path handles rather than
  SHA/byte/MIME integrity metadata; for long,
  sectioned, or prose-heavy deliverables, choose the content carrier
  deliberately: draft a single freeform document as natural Markdown/plain text
  without `.output()`, or use Agently `.output(..., format=...)` with
  `xml_field`, `hybrid`, or `yaml_literal` when separately addressable fields
  are required instead of forcing the body into compact JSON fields; keep
  status, evidence, and verification in separate compact judgment/readback
  contracts; do not add `.output()` solely to trigger instant fields for the
  body stream; use `artifact_manifest.sections` plus Workspace readback when
  AgentTask must deliver a trusted file artifact;
  AgentTask artifact writers consume AgentExecution stream facts: natural body
  text comes from raw delta items, and retry boundaries come from `$status` when
  the provider reports it. If the public `type="delta"`
  `"<$retry>...</$retry>"` replay marker reaches the artifact consumer, treat
  that exact marker as a retry control event; never write, clean into, or
  transport it as artifact content;
  if a complete Markdown artifact body appears inside structured `evidence`,
  treat it as a deliverable body only when the evidence item is explicitly labeled
  as artifact/body/deliverable/Markdown or tied to the manifest path; ordinary
  source content and source excerpts remain evidence snippets. After trusted Workspace write/readback
  succeeds, let terminal verification judge any stale artifact-write
  `remaining_work` instead of planning another write-only step;
  verifier-visible long Workspace artifacts may include bounded
  `workspace_artifact.targeted_readback` ledger items from declared
  output-contract sections and generic source/risk/reference/coverage anchors;
  treat those as scoped evidence snippets, not completion judgments;
  TaskBoard finalization keeps file-backed deliverable bodies in Workspace and
  returns only a concise summary or path/ref pointer as `final_result`, not a
  second copy of the file body;
  host file-producing Actions should return typed `file_refs` or
  `artifact_refs` when later AgentTask, TaskBoard, verifier, or UI consumers
  need the produced file. A path-only payload such as `{filename, path, size}`
  remains bounded Action result evidence and an external ref pointer; it is not
  a trusted Workspace file unless the path is Workspace-contained and real
  `Workspace.read_file(...)` succeeds, or the host returns explicit framework
  refs;
  model-declared `file_refs` remain diagnostics until readback exists; if write
  succeeds but readback fails or lacks trusted fields, expect
  `agent_task.workspace_artifact.readback_failed` or
  `agent_task.workspace_artifact.readback_insufficient` diagnostics rather than
  a generic budget or iteration failure
- intermediate downloads, webpage snapshots, generated code, search notes, and
  large extracted text may be persisted as Workspace/Action artifact refs and
  opened later through bounded cold readback; hot prompts should carry compact
  refs/previews, and these refs are execution evidence rather than final
  deliverable proof. If Action artifact readback exposes Workspace `file_refs`
  for a materialized download, TaskBoard readback promotes those nested refs to
  card-level `file_refs` for later Workspace readback. If a non-final TaskBoard
  card proposes a required final path such as `final.md`, AgentTask relocates it
  to a working evidence path and reserves the final path for final synthesis
- for large Workspace, repository, or file-backed evidence, AgentTask may
  carry scoped retrieval query groups before broad reads. Flat uses
  `scoped_retrieval.query_groups`; the Flat BlockCarrier lowers those groups to
  pre-step Blocks `workspace_operation.search` facts. The operation name is
  compatibility-stable, while execution uses Workspace `retrieve(...)` for
  record/file candidates, optional vector/hybrid mode, structure-gated rerank
  over a bounded candidate-summary window, refill, and budget packaging before
  injecting a body-light model-hot `evidence_ledger` index plus
  compatibility `scoped_retrieval_results` view into the bounded `agent_step`;
  selected structured records may appear as compact projections with
  `projection`/`original_ref` metadata so later readback can recover the raw
  Workspace record;
  reconstructable provenance such as SHA, byte counts, backend/search-engine
  details, execution block ids, and full file refs stays in raw
  Workspace/Blocks evidence for programmatic audit and readback. TaskBoard
  exposes the same work-unit carrier contract and can inject ledger-backed retrieval facts
  into card execution. TaskBoard Workspace-operation prompt views and
  available readback handles, readback work-unit hot payloads, Action artifact readback previews, and
  intermediate Workspace readback previews use the same hot/cold split:
  content/path, range, truncation, and compact handles stay hot, while SHA,
  bytes, handler/media, backend/search-engine facts, execution block ids, and
  full refs stay in cold evidence, final artifact audit metadata, DevTools, or
  runner logs. SHA is integrity metadata, not source evidence. Query groups may
  set `search_surface` to `workspace_index`, `workspace_files`, or
  `workspace_index_and_files`; record collections belong in
  `filters.collection`, exact record kinds may use `filters.kind`, and file
  scopes use top-level `path`/`pattern`; that file `path` is not applied as a
  record filter. Singleton record filter lists are normalized to
  scalar values before execution so retained Workspace records and files can
  stay out of hot context until bounded search/readback needs them.
  For `workspace_files`, `query` is content text, `path` is the directory/file
  scope, and `pattern` is a file glob such as `*.md`, `*`, or `**` for recursive
  file search, not another content keyword. Local Workspace file search uses
  `rg` as a grep-style search engine when available and falls back to bounded
  file scanning. Blocks return a small bounded context around file matches by
  default, so nearby facts can be inspected without reading the whole file.
  `EvidenceEnvelope.evidence_items` records search success, empty result,
  failure, locator, snippet, and readback facts with stable ids, `status`,
  `body_state`, and model-hot `cite_as` handles. Failed/empty items support
  unavailable or missing-data claims only; `ref_only` items support only
  discovery until readback exists; snippet facts expose whether bounded context
  was `truncated`. Structured outputs may include `evidence_use` claim bindings
  to `cite_as` or canonical ids; path/URL/record/artifact/action aliases are
  canonicalized only when unambiguous.
  Ordinary intermediate Flat work units use non-empty `remaining_work` to make
  the next Flat iteration consume the new evidence by default instead of
  triggering an immediate independent verifier. They may also return
  `ready_for_final_verification=false` to make that intent explicit, while
  explicit `ready_for_final_verification=true` is reserved for terminal,
  blocking, or risk verification now.
  Ordinary intermediate TaskBoard cards should let downstream consumer cards
  decide whether evidence is enough. Independent verifier requests are for
  terminal acceptance, fan-in/control acceptance, evidence/artifact boundary
  audit, contradictions, or high-risk review.
  When terminal verification fails, compact `repair_context` is carried into
  the next Flat work unit and Workspace artifact draft request when present, so
  the consumer that actually rewrites or reads the artifact receives the latest
  `acceptance_delta`, repair constraints, next-step requirements, and exact
  evidence anchors without reintroducing cold integrity provenance into hot
  prompts.
  Workspace `retrieve(...)` plus `grep_files`/`search_files`, and Blocks
  `workspace_operation.search/read_bounded`, return factual `locator_ref` and
  `evidence_snippet` records; selected structured record snippets may be
  compact projections that preserve `projection`/`original_ref` metadata for
  raw Workspace readback; model-owned
  planning/verification decides whether snippets are useful. If a TaskBoard
  scoped-retrieval card reports blocked/insufficient output without an explicit
  next action, AgentTask synthesizes an expanded evidence card plus a
  continuation card so the downstream consumer can decide whether the new
  evidence is enough. Do not turn local grep/SQLite hits into semantic
  relevance gates, quality checks, or completion evidence
- TaskBoard readback cards may inspect both Action artifact refs and trusted
  Workspace file/content refs through bounded cold readbacks. Framework-generated
  readback cards scope evidence to direct dependencies plus upstream evidence
  cards, so a control-card readback can still inspect Action refs produced by
  earlier evidence-gathering cards; generated continuation cards should not
  recursively request another identical readback chain when the same evidence
  remains insufficient. When the missing evidence is a new concrete URL, path,
  or ref, the control card should return structured `target_refs` with
  `next_board_action=readback`; external HTTP/HTTPS refs become Action evidence
  work, while Workspace/content paths and retained-note refs become bounded
  Workspace readback cards. Prose-only gaps are diagnostics, not executable targets
- completed and sufficient TaskBoard control outputs may still disclose
  non-fatal `gaps`; those gaps do not block Workspace artifact materialization,
  while `remaining_work`, blocked status, repair, or readback intent still do.
  Materializing an artifact creates readback/verification evidence and is not
  final task acceptance
- AgentTask strategy persistence writes planning, observation, verification,
  checkpoint, and evidence-link records through the bound Workspace provider;
  checkpoints use the checkpoint-store port and task evidence relationships use
  `workspace.link_evidence(...)`. TaskBoard checkpoint payloads may also carry
  bounded acceptance-index and handoff projections for resume orientation; they
  point back to TaskBoard revision, EvidenceEnvelope, artifact, and checkpoint
  refs, and must not be treated as a second evidence ledger or completion
  verdict. Acceptance-index projections may include dirty/cache state, verdict
  fingerprints, scoped evidence refs, and progress counters so TaskBoard can
  skip redundant verifier work for unchanged green criteria while still
  verifying dirty items and required host guards
- for AgentTask business-system examples, mocks may provide facts, source
  records, policies, missing data, or conflicting inputs, but must not provide
  hidden expected answers, pass/fail fields, or deterministic business-quality
  verdicts; judgment belongs to the AgentTask verifier or an independent
  Agently model-judge request
- for app developers, prefer `agent.enable_python(...)`, `agent.enable_shell(...)`, `agent.enable_workspace_file_actions(...)`, `agent.enable_coding_agent_actions(...)`, `agent.enable_nodejs(...)`, `agent.enable_code_runtime(...)`, and `agent.enable_sqlite(...)` before direct manager/provider APIs; Python, shell, Node.js, and common-language code runtime helpers use Docker-backed runtime profiles and fail closed when Docker preflight fails. Strict profiles report missing images, while developer/CI profiles may pull missing images and prepare standard dependencies as host-owned provisioning. Use `sandbox="trusted_local"` only for trusted compatibility paths. Shell is for tests, builds, git inspection, and read-only diagnostics, while Workspace file actions own file read/search/edit/write semantics
- for instruction-heavy or large Actions, expect later model rounds to see compact execution digests, bounded previews, artifact refs, and file refs; oversized complete records are bounded before direct return or TriggerFlow state storage, including large kwargs/instructions, and may replace duplicate data/model_digest fields with same_as=result pointers. Custom execution-handler records cross that same bound before AgentExecution context, RuntimeEvents, TriggerFlow state, route logs, metadata, or public return; route logs keep one semantic payload without nested `raw` or duplicated data/model_digest records. Built-in TriggerFlow/DAG ActionFlows apply the Action-owned bounded/redacted observation projection before direct callbacks and official/compatibility events: plan observations keep one canonical `action_calls` list, command inputs are bounded/redacted, failure convergence carries bounded records, and `payload` plus `error` share one complete-carrier budget. A raw exception becomes one bounded/redacted ErrorInfo-compatible mapping before the direct callback; official `action.*` and compatibility `tool.*` events reuse it without reconstructing the original message or traceback. Previews are not complete evidence, so use `agent.action.read_action_artifact(selection_key=...)` only inside the currently bound AgentExecution, AgentTask, or standalone ActionFlow scope when full raw code, command output, SQL results, page content, or logs are needed. TaskBoard host code binds current task lineage for sibling-card readback; artifact id/action-call id fallback and cross-task/cross-execution readback fail closed; model/terminal `artifact_refs` and `artifacts` aliases must resolve to the same selection-key-only list
- treat model-planned Action inputs as untrusted: ActionDispatcher filters
  `structured_plan` and `native_tool_calls` kwargs to registered
  `ActionSpec.kwargs`, records stripped keys in `ActionResult.diagnostics`, and
  leaves direct host calls compatible
- `agent.action.get_action_info()` and `get_action_list()` return visible
  metadata with execution environment `env` values redacted; raw env values are
  only for the execution provider path
- after explicit `agent.get_action_result(prompt=..., store_for_reply=True)`,
  the prompt is marked as having consumed the action loop even when no records
  were produced, so later response materialization should not re-enter
  ActionRuntime for that prompt
- `agent.get_action_result(..., timeout=N)` bounds the full ActionFlow
  lifecycle, including planning/model-owned tool selection; catch
  `RuntimeStageStallError(stage="action_loop_close")` instead of relying on a
  host-side kill as the primary timeout signal
- for native tool-call planning, a zero-tool-call result can surface as a
  skipped diagnostic record with code `action_runtime.native_tool_calls.empty`;
  treat it as planning evidence, not executed work
- use `agent.action.summarize_records(records, validation_command_markers=...)`
  when a host needs authoritative action evidence such as failed actions,
  commands attempted/run, and latest validation result
- treat `Agently.execution_resource` as an advanced framework/plugin surface for lifecycle, policy, approval, health, and release
- Action executors should declare or consume managed resources instead of secretly owning long-lived MCP clients, sandboxes, browsers, SQLite connections, or process runners
- keep permission profiles explicit: search-only, local-files-only, network-read, install-capable shell, or trusted executor
- treat `agently-devtools` as optional PyPI-installed tooling; wire observation through public bridge APIs, not source-repo paths
- for framework internals, preserve Agently's core module style: class-owned
  runtime behavior, typed data contracts, protocol/handler seams for
  replacement, and high-level packages outside `agently/core` when they compose
  several core systems
- official Agently RuntimeEvent records are core-owned: built-in plugins should
  return typed observations, errors, decisions, or route stream facts to core
  rather than importing core RuntimeEvent emitters; plugin-owned custom Event
  Center messages must use plugin-owned namespaces and are not guaranteed as
  framework consumption contracts
- keep runtime naming aligned with DevTools: `agent_execution` is the canonical
  run lineage kind for one bounded Agent execution. The old turn-named runtime
  namespace is removed from the current development-line contract.
  `attempt_index` is model-request retry metadata and must not be treated as an
  AgentExecution counter. AgentExecution process streams are observed as
  `agent_execution.stream` RuntimeEvents for flat and TaskBoard execution
  progress; DevTools may display those facts but must not own task strategy
  selection.
- for framework-side Skills work, treat `SkillsManager` as an internal
  capability-adapter owner, not a new public recommended facade. Internal code
  should depend on SkillsManager; user-facing examples should prefer
  `agent.use_skills(...)` and AgentExecution Skills selection. Use legacy
  `Agently.skills_executor` only when a compatibility registry/resolver hook is
  required. Context-pack calls are advanced custom-planner/TaskDAG integration
  surfaces, not the ordinary user path.
- for Agently 4.1.3 Skills runtime work, prefer Action-like management:
  declare installed ids or remote source selectors on `agent.use_skills(...)`
  and let Skills Manager lazily discover, install, and expose selected
  capability needs/candidates; AgentExecution owns run-local mounting,
  execution, and cleanup. Keep `install_skills_pack(...)` for prewarming, offline mirrors,
  deterministic CI fixtures, and explicit registry maintenance
- Skills installs default to the user-global registry `~/.agently/skills`;
  override `skills.registry.root` only for isolation, and use
  `skills.registry.proxy` or `runtime.network.proxy` when remote pack fetches
  need a configured proxy
- use `install_skills(...)` for one local Skill directory during
  authoring/smoke tests; use AgentExecution with `execution.require_skills(...)`
  for explicit required Skill activation; remote selectors may use git URLs,
  GitHub shorthand such as
  `anthropics/skills`, and `subpath=` when selecting one Skill from a pack
- `Agently.skills_executor` and `agent.run_skills_task(...)` are pre-4.2
  compatibility facades only. They still lower direct Skills execution through
  the current Blocks runtime, but new examples and app guidance should use
  Agent APIs and AgentExecution Skills selection instead.
- when a custom planner, Dynamic Task, or TaskDAG node needs full Skill context
  without forcing Skill activation execution, use
  `agent.build_skills_context_pack(...)`,
  `agent.async_build_skills_context_pack(...)`, or
  the legacy `Agently.skills_executor.build_context_pack(...)` facade; the returned
  `agently.skills.context_pack.v1` payload can include `SKILL.md` guidance,
  task-relevant references/examples/assets, citations, diagnostics, optional
  public lookup, and policy-gated script Action candidates
- when a planner needs progressive Skill context before lowering a Task to a
  `skill_activation` ExecutionBlock,
  use the internal SkillsManager adapter or the legacy
  `Agently.skills_executor.activate_skill(...)` compatibility facade. Treat the
  returned SkillActivation as
  skill-context evidence and capability need discovery only; it does not execute
  bundled resources, grant Actions/MCP/shell/browser access, or prove side
  effects
- for DAG-shaped consumers of Skill context, pass
  `Agently.skills_executor.task_dag_resolver()` to `TaskDAGExecutor` and use
  `kind="skill"` nodes; do not build a separate scheduler or execute bundled
  scripts while constructing context packs
- for explicit required Skills, create an AgentExecution draft, set prompt and
  output contracts on that draft, then call `execution.require_skills([...])`.
  Required multiple Skills are preserved in caller order and lowered to ordered
  TaskGraph Tasks plus ordered `skill_activation` ExecutionBlocks; later Skills
  receive compact previous Skill results as evidence
- when Skills are reached through Agent auto-orchestration, pass
  execution-block-owned effort with
  `agent.create_execution(options=ExecutionOptions(execution_blocks={
  "skill_activation": SkillActivationOptions(effort="normal")}))` or the
  equivalent dict;
  this is an execution option, not a prompt slot
- do not add application-specific Skills execution strategies through
  framework-level strategy registration. Model requests, ActionRuntime/MCP,
  ExecutionResource, TriggerFlow, Dynamic Task, and host policy should be
  composed by AgentExecution planning/lowering instead of a parallel
  Skills-owned dispatcher
- Skill activation stream handlers receive Skills runtime item dictionaries and
  can be annotated with
  `SkillRuntimeStreamHandler`; model stream handlers passed to
  `context.async_request_model(..., stream_handler=...)` receive `StreamingData`
  and can be annotated with `ModelStreamingHandler`; the common aliases are
  available from `agently`
- for MCP, prefer Streamable HTTP URLs for service integrations
  (`agent.use_mcp("https://host/mcp")`), use `headers=` for URL auth, and use
  MCP config dictionaries for stdio/multi-server local integrations; treat SSE
  as a legacy compatibility transport
- treat chained Agent quick prompt methods as AgentExecution-local configuration
  for one request/execution surface. Ordinary
  `agent.input(...).output(...).start()` expressions create a fresh execution
  for that expression, including inside loops. For multi-statement execution
  setup, use `execution = agent.create_execution()` and mutate the execution
  before it starts, not the shared Agent pending prompt. A completed explicit
  `AgentExecution` is an immutable run record; prompt/config mutators should
  fail fast on that object, and the next request should use a new execution.
  `semantic_outputs=` is only a deprecated compatibility alias for direct
  Skills execution, while Dynamic Task still uses `semantic_outputs` inside
  TaskDAG specs
- for framework-side Skills execution, keep standard `SKILL.md` as the only
  capability definition; selected Skills default to a `single_shot`
  compatibility label that lowers to handler-backed model-request execution,
  while staged/react/custom labels lower to handler-backed execution segments and
  should compose TriggerFlow and ActionFlow/ActionRuntime rather than adding a
  Skills-local executor
- for Skills `react` tool use, delegate model-owned action planning and
  execution to the Agent ActionRuntime so action/MCP kwargs schemas, policy,
  approvals, concurrency, and managed resources stay on the Action layer
- when Skills `react` delegates to ActionRuntime, keep the selected SKILL.md
  guidance/resource context in the ActionRuntime planning prompt. Delegation
  with only task text and observation history bypasses the Skill guidance.
- when Skills `react`, AgentTask, or another higher-level runtime delegates
  action planning to ActionRuntime, set `action.planning_model_key` to the
  intended `model_pool` business key so action planning uses the same model
  routing as the surrounding task
- Skills are public-standard `SKILL.md` guidance/resources, not Agently-private
  capability manifests; do not author or recommend `allowed-actions`,
  `allow-scripts`, `mcp`, `mcpServers`, `execution`, or `stages` frontmatter as
  Agently capability declarations
- SkillsManager discovers selected Skill capability needs from `SKILL.md`,
  resource indexes, public `compatibility`, public `metadata`, and optional
  model-assisted inference, then records structured `capability_needs`; selected
  Skills may guide the model to use capabilities when available, but they do not
  grant them
- host applications control Skills capability loading with
  `agent.configure_skill_capabilities(auto_load={...})`; `allow` can auto-load
  built-in Search/Browse/HTTP/Workspace/Python/shell-script/MCP capabilities,
  while `approval` and `off` fail closed with diagnostics instead of silently
  mounting tools
- with `capability_scope="execution"`, AgentExecution releases only capabilities
  newly mounted for that execution; if the host Agent already owns the requested
  action id, reuse that action and leave it registered after the Skills run
- for search-oriented Skills, prefer the framework Search package backed by the
  `ddgs` Python package; keep `ddgs` upgraded with
  `python -m pip install --upgrade ddgs` before real search runs, and leave the
  ddgs backend strategy configurable (`auto` by default) instead of hard-coding
  a single backend; Search treats backend-level "no results" as an empty
  successful action result and falls back through configured/default ddgs
  backends when a selected backend returns no usable parsed result; if fallback
  recovers after backend failures, Search reports `status="partial_success"`
  with `success=True` and diagnostics rather than an `action.failed` terminal
  condition
- when observing ActionFlow records, treat `action.approval_required` and
  `action.blocked` as policy/sandbox gate outcomes, not ordinary
  `action.failed` execution failures
- Workspace owns file-action roots and path boundaries; expose file access
  through Workspace-scoped file actions, and treat ActionRuntime as the callable
  surface rather than the owner of Workspace semantics, file type parsing, or
  export rendering
- Skills capability `approval` is resolved through Agently's global
  PolicyApproval handler, not a SkillsManager-local handler:
  `input_timeout_fail` by default, `auto_approve` for tests/trusted local
  profiles, `fail_closed` when a host wants pending diagnostics or TriggerFlow
  policy interrupts, `input` for local CLI interruption, or a host-provided
  durable/network handler
- trusted hosts may grant automatic approval through settings-backed
  `access_control_policy.auto_allow`, using
  `Agently.set_settings("access_control_policy.auto_allow", True)`,
  `agent.set_settings("access_control_policy.auto_allow", True)`, execution
  `.access_control_policy({"auto_allow": True})`, or selector-level
  `auto_allow=True` for a matching Skill. Do not introduce
  `configure_access_control_policy(...)`; if a wrapper is ever added, it must
  delegate to settings and own no independent state
- production services should choose a PolicyApproval handler that matches the
  service wrapping the TriggerFlow execution: database pending record, HTTP
  callback, webhook resume, SSE/WebSocket pending stream, save-and-return
  interrupt id, or another host-owned approval channel; tests may use
  `auto_approve`
- script resources under `scripts/` can be wrapped as scoped shell actions only
  when host policy allows `script_run` or a host-owned auto_allow grant applies;
  selector-level auto_allow is scoped to matching Skill ids. The action root must
  be the installed Skill directory and execution still goes through ActionRuntime
  / ExecutionResource boundaries
- public Agent Skills `allowed-tools` is experimental and, if supported, can
  only restrict or pre-approve already-mounted host tools; it must not create
  tools, synthesize backends, mount MCP, or choose Skills execution strategy by
  itself
- for Agently auto-orchestration work, treat
  `agent.use_skills(...).input(...).get_result()` as capability-candidate
  registration when the caller needs reusable data/text/meta/stream readers;
  this is owned by the AgentExecution planner, not prompt-only Skills guidance
  injection by default
- for ambiguous optional capability candidates, keep submitted Dynamic Task and
  required Skills deterministic, but let the model choose among optional auto
  Dynamic Task, model-decision Skills, and ordinary Action-backed model request
  Tasks
- for framework-side Skills, treat standard `SKILL.md` as the only capability
  definition; Agently install metadata and decision cards are descriptive
  runtime aids, not authoring formats or availability gates
- for Skills actions, use the global PolicyApproval contract plus
  Action/ExecutionResource boundaries; when the request is
  orchestrated, pending approvals must become TriggerFlow `policy_approval`
  interrupts instead of Skills snapshots
- keep Agent auto-orchestration behind the `AgentOrchestrator` plugin protocol:
  core owns the public `agent.create_execution()` entrypoint, while the active
  plugin owns Task planning, execution lowering, and stream bridging
- for unified Agent execution/result work, prefer a response-style
  `agent.create_execution()` object with data/text/meta/stream consumption; use
  TriggerFlow runtime stream plus ModelRequest `instant` checkpoints for process
  streaming, and expose model field deltas only through stable structured paths
  such as `task_dag.tasks.<task_id>.fields.<field_path>` rather than raw provider
  token events
- for bounded developer-owned loops, use
  `agent.create_execution(lineage=..., limits=..., options=...)`; lineage,
  diagnostics, stream correlation metadata, and shared model-request budget
  counting now describe the bounded step without a public mode name
- keep AgentExecution memory explicit through its bound Workspace. Do not use a
  fresh `async_record_workspace(..., purpose="process"|"recovery")` call as a
  checkpoint shortcut: process/recovery writes require an already active
  running execution, never start or wait for a fresh execution, and use the
  canonical AgentExecution id. The API rejects non-active and terminal writes.
  Post-terminal deliverable/audit
  writes require their explicit purpose and immediate Workspace governance;
  ordinary one-turn AgentExecution remains explicit, while AgentTask owns its
  strategy-level persistence
- treat AgentExecution terminal storage as one host-owned bounded projection:
  the result stream and terminal lifecycle event must carry the same projection,
  while the full result remains in the in-memory result API and durable bodies
  are reached through canonical retained refs
- pass the execution's explicitly scoped Workspace into a routed AgentTask so
  the physical scope is `AgentExecution -> AgentTask -> Action`; Task retention
  keeps the inherited parent `execution_id`, narrows by exact `task_id`, and must
  not clear a sibling Task or its owning execution scope
- treat Action artifact ownership the same way: a standalone AgentTask releases
  its exact task scope at terminal, while the routed construction seam explicitly
  transfers that scope to the parent AgentExecution for terminal
  selection/promotion and parent-owned release; cancellation, timeout, or
  abnormal stream close must cancel and join the routed child before that
  release, so no late artifact or Workspace process write can cross terminal
  cleanup
- on AgentTask failure, discard ordinary process records/files/checkpoints but
  anchor the compact `task_id::resume` snapshot from the last completed
  iteration when one exists; task cleanup joins checkpoint rows through scoped
  record identity across task and resume run ids, deletes their matching
  `checkpoint.latest.*` manifests, and preserves the anchored resume row plus
  manifest; successful and cancelled tasks do not retain that recovery point by
  default
- after an owner is terminal, reject new process/recovery records but allow
  deliverable/audit records and apply retention immediately; active recovery or
  lease state comes from `Workspace.get_retention_lifecycle(...)` and defers
  destructive retention until the lifecycle is safe
- inspect AgentExecution runtime facts through AgentExecutionResult or the
  execution facade: `result = execution.get_result()`, `result.get_text()`,
  `result.get_data()`, `result.get_full_data()`, `result.get_meta()`,
  `execution.get_prompt_text()`, `execution.get_data_object()`,
  `execution.get_key_result(...)`, `execution.wait_keys(...)`,
  `execution.get_async_generator()`, `execution.streaming_print()`, and
  `await execution.async_get_meta()`.
  `meta["task_frame"]`,
  `meta["task_graph"]`, and `meta["execution_blocks"]` record the selected Task
  structure and concrete execution lowering, while `meta["logs"]` exposes model
  response ids, ActionRuntime action logs, task refs, and artifact refs when available; use those
  framework-owned records for Workspace persistence instead of asking the model
  to copy raw action stdout into final text. `type="delta"` remains the public
	  string stream; `type="instant"` yields original structured items and appends
	  synthetic `path="$delta"` `AgentExecutionStreamData` items only as a consumer
	  text projection when a source item can be projected to natural language;
	  `type="all"` remains the raw audit stream and must not include synthetic
	  `$delta` items. Rich task UIs should consume `instant` for structured state
	  and render public/synthetic `$delta` only as visible process text; public
	  `delta` is a printable compatibility stream, not the UI state owner
- when AgentExecution planning selects direct `model_request`, treat
  Action and Observation as skipped business stages and consume the model result
  as passthrough. If Action or Skill candidates are available but the selected
  Task remains direct `model_request`, they are only available capabilities, not
  a planned Action/Skill task. Only actual action/tool records become
  side-effect evidence for verification, Workspace persistence, or replan.
- set `limits={"max_seconds": ..., "max_no_progress_seconds": ...}` only when
  the host explicitly needs hard wall-clock or no-progress controls while
  diagnosing or building host-owned loops; framework defaults should not impose
  model-request, iteration, TaskBoard tick, Action round, node-count, or
  tool-call quotas, while no-progress and idle timeouts remain liveness guards;
  catch `RuntimeStageStallError` from the root `agently.core` export or
  `agently.core.application.AgentExecution` and inspect
  `meta["diagnostics"]["last_progress"]`, `["timeouts"]`, and `["stalls"]`
  instead of adding ad hoc polling around the whole app
- for provider stream hangs, prefer framework settings such as
  `OpenAICompatible.stream_idle_timeout`,
  `OpenAIResponsesCompatible.stream_idle_timeout`, and
  `AnthropicCompatible.stream_idle_timeout`, plus
  `response.materialization_idle_timeout`; use `None` for unlimited budgets and
  avoid permanent debug-only timeout wrappers in examples; provider first-event
  and stream-idle waits should surface as `RuntimeStageStallError` with
  `stage="response_first_event"` or `stage="response_stream"`; transient
  disconnects use same-request `<Requester>.request_retry`; OpenAICompatible
  replays after partial output by default, which requires streaming consumers
  to process `$status` or clear plain-delta text on the
  `"<$retry>{reason}</$retry>"` marker before accepting replacement deltas;
  the marker belongs to public delta replay and must not be treated as internal
  artifact content;
  explicit response stream errors should propagate from response getters with the
  original provider or ActionFlow reason before materialization timeout is used
  as a fallback
- when high-frequency RuntimeEvent deltas would overload downstream consumers,
  keep producers raw and ask the expensive EventCenter outlet to summarize with
  hook/hooker `delivery_policy={"mode": "summary", "dispatch": "await",
  "emit_interval": ..., "max_items": ...}`; use `dispatch="background"` only
  for best-effort outlets that call `EventCenter.async_flush(...)` or expose an
  owning bridge flush/close point; EventCenter also has an idle flush safety net
  for long-lived loops, but CLI/script shutdown still needs explicit flush for
  background outlets; rely on AgentExecution liveness diagnostics rather than
  public delta frequency for stall detection
- for temporary development debugging, attach an EventCenter observation hook,
  call `.set_settings("debug", True)` for request/result and AgentTask process
  summaries, or call `.set_settings("debug", "detail")` for full observation
  detail including model delta output;
  remove debug hooks/settings from examples and production snippets after the
  issue is diagnosed

## Anti-Patterns

- do not build a parallel action/tool dispatcher before checking Action Runtime
- do not hand-roll tool schema prompts or kwargs planners in Skills when the
  Agent ActionRuntime can plan against the registered action list
- do not accept prompt-only or React Skills text as proof of file writes,
  readbacks, shell execution, HTTP calls, or other side effects; require
  ActionRuntime records and structured evidence
- do not expose core ExecutionResource manager APIs as the default app-development mental model
- do not route package installation or filesystem mutation through the Python sandbox
- do not ask users to clone or editable-install DevTools when `pip install agently-devtools` fits
- do not make DevTools the source of truth for workflow structure
- do not present prompt-only Skills disclosure as the default execution meaning
  of `agent.start()` once the 4.1.3 AgentExecution planner owns Skills candidates
- do not put TaskGraph/ExecutionBlock-owned Skills, Dynamic Task, or stream-composition logic
  directly in core when a plugin protocol can own the replaceable behavior

## Read Next

- `references/actions-runtime.md`
- `references/actions-execution-resource.md`
- `references/devtools.md`
