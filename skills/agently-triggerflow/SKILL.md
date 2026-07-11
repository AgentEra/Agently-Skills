---
name: agently-triggerflow
description: Use when the user needs workflow orchestration such as branching, concurrency, approvals, waiting and resume, runtime stream, restart-safe execution, mixed sync/async function or module orchestration, event-driven fan-out, process-clarity refactors that make stages explicit, performance-oriented refactors that collapse split requests, or workflow definitions and chunk-level runtime metadata that must stay visible for debugging and visualization. The user does not need to say TriggerFlow explicitly.
---

# Agently TriggerFlow

Use this skill when the solution clearly needs orchestration semantics rather than one request family.

The user does not need to say TriggerFlow or Agently. Scenario language such as resumable approval flow, branching automation, output-fan-out refactor, mixed sync/async pipeline, process-clarity refactor, or draft-review-revise pipeline should still route here once orchestration is clearly the owner layer.

## Native-First Rules

- prefer TriggerFlow for explicit multi-stage quality loops, branching, concurrency, waiting/resume, restart-safe execution, output-fan-out performance refactors, process-clarity refactors, or mixed sync/async orchestration
- treat TriggerFlow as Agently's first-class orchestration substrate: framework
  features with multi-step loops, approval waits, retry, replan, verification,
  or resume semantics should be TriggerFlow-backed rather than hidden inside a
  local executor state machine
- prefer `agent.create_task(...)` when the app needs one Agent-owned business
  task loop where the model owns planning, verification, and replan; it returns
  a task-strategy `AgentExecution` draft, not a separate public AgentTask
  handle. Use `agent.create_task_loop(...)` only when the code should make the
  task-loop strategy explicit; it still returns an AgentExecution draft. Use
  TriggerFlow directly when the application owns explicit stages, branching,
  pause/resume, or restart topology
- for AgentTaskLoop examples, consume the AgentExecution result/stream/meta
  (`result = execution.get_result()`, `result.get_text()`,
  `result.get_data()`, `result.get_meta()`,
  `execution.get_async_generator()`, `execution.async_get_meta()`) and surface task refs or
  `meta.stream_kind=="snapshot"` items as compact intermediate state captures;
  enable `options={"agent_task": {"stream_progress": True}}` only when the
  example or host needs natural-language operator updates; omit
  `progress_model_key` for template progress with no model requests, or set
  `progress_model_key` to run a separate background model that summarizes only
  existing snapshots/task metadata without adding main-loop fields or latency;
  model-generated progress streams `progress_delta` items before the final
  `progress` item; use `progress_language` or the global
  `agent_task.progress.language` setting when the host needs a fixed language;
  prove replan behavior from stream verification/replan events and snapshots
  rather than hiding the proof in a local Python loop; mocked business systems
  may supply defective facts or conflicting source data, but must not return
  pass/fail verdicts or deterministic quality judgments
- default to async-first workflow handlers, execution entrypoints, and runtime stream consumers
- treat sync TriggerFlow APIs as wrappers for scripts or compatibility bridges, not as the default service interface
- derive complex workflow topology from the real business dependencies before
  implementation: mark required serial edges, independent branches, provisional
  structured progress that can support UI or cancelable/idempotent preparation,
  and side-effect/capacity
  constraints. Use `batch(...)`, `for_each(...)`, or `when(...)` plus managed
  emits for bounded concurrent work and graph-visible joins. Choosing an
  all-serial topology without this analysis is a prohibited anti-pattern
- prefer explicit execution lifecycle control with `close()` / `async_close()` for completion and cleanup
- treat `create_execution(concurrency=N)` and `execution.set_concurrency(N)` as an execution-wide handler dispatch budget, including nested dispatch from chunk continuations and `data.async_emit(...)`; use operator-local `batch(..., concurrency=...)` or `for_each(..., concurrency=...)` only for local fan-out caps
- expose pressure controls at the layer that owns them: host admission and
  in-flight execution/coroutine limits, TriggerFlow execution concurrency,
  operator-local fan-out caps, model scheduler concurrency/rate limits, and
  host worker or thread-pool sizes when blocking code is isolated. Do not
  present worker or thread counts as a universal TriggerFlow setting
- use `execution.result` when services, UIs, stream consumers, or intervention-aware workflows need multiple views of one execution outcome, such as state, compatibility final result, interventions, and metadata; use `execution.close()` / `execution.async_close()` for close snapshots
- use runtime intervention for optional guidance context added while an execution is already running: define explicit `.intervention_point(...)` boundaries so execution creation can infer planned mode, or create the execution with `intervention_mode="auto"` for boundary policy insertion; chunks read inserted context with `data.get_interventions(...)` and explicitly audit usage with `data.async_mark_intervention_consumed(...)`, relying on the chunk-name consumer default unless another consumer identity is clearer
- for human approvals, webhooks, or externally resumed waits, use `pause_for(..., resume_to="next" | "self" | {"event": ...})`; treat it as a durable graph interrupt, not Python coroutine stack persistence; teach model-decided autonomous interrupts with model-owned `pause_for(..., resume_to="self")`, where the resumed chunk handles `data.is_resume` and the default `max_resumes=1` prevents unbounded self-replay; teach prearranged approval gates with an explicit pause chunk plus `when(...)`
- for framework policy approvals, use the global PolicyApproval contract and
  represent pending approvals as `pause_for(type="policy_approval", ...)`
  interrupts that resume through `continue_with(...)`
- for host-owned approval, webhook, queue, or UI-card transports, use the
  ExecutionExchange provider seam instead of inventing a second wait/resume
  channel: the provider publishes typed requests, while TriggerFlow owns the
  interrupt ledger and all resumes still go through `continue_with(...)`
- when a TriggerFlow exchange should be rendered by a host, project it through
  `agently.base.execution_exchange.project_pending_exchanges(execution)` or
  `project_execution_exchanges(execution)`; do not make host code depend on raw
  TriggerFlow interrupt internals as the UI contract
- do not put `pause_for(...)` behind hidden execution sugar such as `flow.start()` or flow-level runtime stream helpers; create an explicit execution handle and consume `get_pending_interrupts()` / `continue_with(...)`
- close waiting executions explicitly: `close()` / `async_close()` rejects pending interrupts by default, and `pending_interrupts="cancel"` must be chosen deliberately when abandoning waits
- when a sub-flow can pause, keep the external API rooted at the parent execution id plus projected root interrupt id; do not require callers to manage child execution ids
- use `emit_nowait(...)` / `async_emit_nowait(...)` when a chunk must fan out without blocking the current handler, and rely on execution close to drain registered tasks
- after starting a finite workflow that uses execution-managed nowait fan-out,
  call `await execution.async_close()` to drain registered tasks and collect the
  close snapshot. Do not add `while True` status polling loops such as
  `execution.result.get_state("status")` unless a chunk explicitly owns and
  updates that status contract
- rely on chunk-internal `data.emit(...)`, `data.async_emit(...)`, `data.emit_nowait(...)`, and `data.async_emit_nowait(...)` to inherit the current TriggerFlow runtime scope; do not assume unrelated external emits can be paired by `when(..., mode="and")` unless the host routes them through one scoped flow stage or carries explicit correlation in the payload
- use execution runtime state through `get_state(...)` / `set_state(...)` instead of legacy runtime-data helpers in new examples
- treat shared flow data as a risky cross-execution surface and avoid it unless the task explicitly needs shared state
- when discussing restart or distributed pause/resume, describe TriggerFlow as
  providing foundations for host-managed recovery, not a complete production
  distributed workflow engine. `execution.save()` is a versioned top-level
  execution snapshot with durable TriggerFlow progress, flow definition
  fingerprint validation, interrupt/resume ledgers, resource requirements,
  lease metadata, and managed execution resource requirements. TriggerFlow
  core is process-stateless between save/load; live `runtime_resources`,
  clients, callbacks, tasks, semaphores, stateful sessions, and Python
  coroutine frames are not serialized. `runtime_resources` is only the
  process-local mount point for live objects that the host has already created,
  restored, and validated. If a resource carries state, the external system
  that owns it must persist a state ref/version/lease or fence token and a
  resolver/provider must validate it before load is ready. Declare future
  resources with `flow.declare_resource_requirement(...)` or
  `execution.declare_resource_requirement(...)`, inspect or restore with
  `execution.inspect_load(...)` / `execution.async_load(...)`, pass a stable
  `resume_request_id` to `continue_with(...)` for external callbacks, and
  persist through a snapshot store that implements `put_snapshot(...)` while
  the production store owns atomic claim, lease enforcement, conflict handling,
  outbox ordering, and external side-effect idempotency. Fail-closed pending
  resolvers or pending managed execution resources should be treated as
  `status="pending_resources"` and `ready=False` until `async_load(...)`
  resolves and validates live resources. Late callbacks delivered to an
  expired execution-local lease fail fast before resume acceptance without
  writing resume ledger entries; the reclaimed worker should load or claim
  first and then use the same stable `resume_request_id`. For long-running
  executions, use `execution.set_compaction_policy(...)` when snapshot writes
  should automatically run a host-owned reducer and store large payloads behind
  provider artifact refs; TriggerFlow records compaction facts, retained
  anchors, and load read bounds, while Workspace or an enterprise provider owns
  artifact storage and retention anchor persistence. For framework-level
  validation, run `examples/trigger_flow/durable_recovery.py` when available; it
  proves Workspace-backed snapshot load and duplicate callback idempotency
  without pretending a production approval transport exists. Use
  `examples/trigger_flow/fastapi_sqlite_exchange_provider.py` when service-level
  provider replacement should be shown: it packages the flow as a module-level
  `TriggerFlow(...)` object with top-level `.to(...)` / `.when(...)` wiring,
  stores top-level execution snapshots in SQLite, and routes approval waits
  through a SQLite `ExecutionExchangeProvider` exposed by FastAPI without
  claiming production distributed guarantees. If a snapshot
  fingerprint is missing or does not match the current flow definition,
  `inspect_load(...)` reports `invalid_snapshot` and `load(...)` rejects the
  snapshot
- for service packaging, prefer an importable module that owns the complete flow
  definition: a module-level `TriggerFlow(...)` object, module-level chunk
  handlers, and module-level `.to(...)` / `.when(...)` wiring. Service modules
  should import that flow object and start executions from it. Normal Python
  imports execute the module body once per process for the same module name;
  TriggerFlow duplicate-definition protection is only the second line of
  defense when application code explicitly runs the same wiring again on the
  same flow object. Create live dependencies in host-owned factories or
  importable resolvers, and use `runtime_resources` only as the final
  process-local attachment point for already-created live objects. Use a
  `build_flow(...)` helper only when the application genuinely needs multiple
  configured flow instances or test isolation, not as the default service shape
- route model-generated or app-submitted DAG data to `agently-dynamic-task`; TaskDAG is the DAG foundation capability, Dynamic Task is the convenience facade over it, and TriggerFlow is the execution substrate rather than the facade API
- when discussing the new Blocks lifecycle, describe it as the framework
  lowering bridge from bounded ExecutionPlan / PlanBlock instances or
  validated TaskDAG nodes into TriggerFlow-backed ExecutionBlockGraph. Do not
  tell users to generate live Python TriggerFlow chunks from planner output for
  the current run; trusted ExecutionBlocks, handlers, Workspace resources, and
  PolicyApproval waits must be registered or provided by the host. Blocks
  wait blocks record waiting evidence, while resume state remains in the
  TriggerFlow interrupt/resume ledger
- use `when(...)` + `emit_nowait(...)` as the native signal-driven pattern for fan-out, loops, side branches, and dependency joins; definition idempotence must not be confused with runtime signal deduplication
- for a developer-owned Todo DAG or other dependency graph represented as
  stable Python flow code, express multi-dependency joins with
  `flow.when(["task_a_done", "task_b_done"], mode="and").to(...)` and have
  upstream chunks call `data.emit_nowait("task_a_done", payload)`. Do not
  replace joins with sleeps, polling loops, local `completed` sets, or
  `pause_for(..., resume_to="self")` unless the workflow is genuinely waiting
  for external input across process time
- when a model-generated Todo List is produced at runtime but the host owns the
  executor code, compile the returned task list into TriggerFlow definitions
  immediately after generation: root tasks attach to the execution start
  boundary with `flow.to(handler, name=...)`, dependent tasks attach with
  `flow.when(dep_signals, mode="and").to(handler)`, and task handlers emit their
  own completion signals. Do not implement a generic local scheduler that scans
  `task_status`, `completed`, or dependency lists to decide which task is ready;
  that hides the DAG from TriggerFlow and defeats graph visibility. Do not pass
  `lambda data: async_task_handler(data, task)` to `flow.to(...)`; that registers
  a sync lambda whose return coroutine may not be awaited. Use a normal factory
  that returns `async def handler(data): ...` and register that handler
- when a TriggerFlow + Skills example relies on a trusted local Skill
  bundle to provide declared helper capabilities, pass selector-level
  `auto_allow=True` or use settings-backed
  `access_control_policy.auto_allow` for trusted hosts; Skill metadata alone is
  not a capability grant, and selector-level auto_allow must stay scoped to the
  matching Skill
- keep runtime stream consumers safe by relying on execution close to stop the stream
- keep workflow stages visible instead of hiding nested request loops
- name chunks and stage boundaries so exported flow configs, Mermaid diagrams, and runtime graphs stay readable
- let TriggerFlow definition export and runtime metadata drive visualization instead of maintaining a second manual graph description
- combine with `agently-request` when one workflow step needs model setup, prompt contracts, structured output, response reuse, session behavior, or retrieval

## Python API Shape

When generating or editing Python code, use the actual Agently API shape:

```python
from agently import Agent, Agently, TriggerFlow, TriggerFlowRuntimeData, Workspace

agent = Agent()
factory_agent = Agently.create_agent()
flow = TriggerFlow(name="workflow-name")
factory_flow = Agently.create_trigger_flow("factory-workflow")
shared_workspace = Workspace("./.agently/workflows/shared")
```

`Agent()` / `Agently.create_agent()` and `TriggerFlow()` /
`Agently.create_trigger_flow(...)` are both valid first-class creation styles.
`Workspace(...)` / `Agently.create_workspace(...)` are both valid first-class
Workspace creation styles. Use one style consistently in an example unless
showing the API equivalence.

`when`, `emit_nowait`, and `pause_for` are not top-level imports from
`agently`. They are methods on flow or runtime data objects:

- define graph branches with `flow.when(...).to(handler, name="...")`
- fan out from inside a chunk with `data.emit_nowait(...)`
- pause from inside a chunk with `await data.async_pause_for(...)`
- create and close long-running/manual executions with
  `execution = flow.create_execution(auto_close=False)`,
  `await execution.async_start(input_value)` using a positional start value, and
  `snapshot = await execution.async_close()`
- `flow.create_execution()` binds the current session/script default Workspace
  by default and assigns the execution a scoped file root under
  `files/lineage/<root-kind>/<root-id>/.../execution/<execution-id>/files`;
  pass `workspace=False` to opt out, or
  `flow.create_execution(workspace=shared_workspace)` when an application-owned
  Workspace should be selected explicitly for Agents, service workers, or other
  executions
- do not call `execution.async_start(input_value=...)`; pass the start value
  positionally
- do not assume `execution.async_start("start")` emits a custom `"start"` event.
  It starts the execution with `"start"` as the start input. Use `flow.to(...)`
  for start-bound chunks, or explicitly call `await execution.async_emit("start", payload)`
  after start when a custom event is intentional
- `async_close()` / `close()` returns the close snapshot as a dict. Read it as
  `snapshot["key"]` or inspect execution state through
  `execution.result.get_state("key")`; do not write `snapshot.state`,
  `snapshot.pending_interrupts`, or `execution.result.state`
- create named flows with `TriggerFlow(name="...")` or unnamed flows with
  `TriggerFlow()`. Do not write `TriggerFlow("name")`; the first positional
  argument is not the workflow name in the current API

Do not write `from agently import when, emit_nowait, pause_for`, and do not use
`@flow.when(...)` as a decorator.

## Dynamic Task Boundary

Do not treat Dynamic Task as TriggerFlow syntax. If a model or application
submits a DAG as data, route to `agently-dynamic-task` and use
`Agently.create_dynamic_task(...)`, `TaskDAGValidator`, and `TaskDAGExecutor`
there. TriggerFlow remains the substrate for stable workflow definitions that
the developer owns in code.

## Anti-Patterns

- do not default a complex workflow to serial execution merely because a serial
  loop is easier to write; keep serial edges only where dependencies, ordering,
  side-effect safety, or external capacity require them
- do not invent a custom event bus or state machine before checking TriggerFlow
- do not implement a custom DAG scheduler in TriggerFlow when Dynamic Task can validate and execute submitted task graphs
- do not use untracked `asyncio.create_task(data.async_emit(...))` as the default nowait pattern when execution-managed `emit_nowait(...)` is available
- do not recommend `.end()`, `get_result()`, or `set_result()` as the default lifecycle path for new TriggerFlow code
- do not add custom result containers around TriggerFlow executions when `execution.result` can expose the needed state/final-result/intervention/meta view
- do not use runtime intervention as a required wait gate; use `pause_for(...)` / `continue_with(...)` when the workflow must stop for external input
- do not treat `intervene(...)` as `emit(...)`, graph mutation, input rewriting, chunk cancellation, or replay of completed chunks
- do not use `get_runtime_data(...)` / `set_runtime_data(...)` in new guidance when `get_state(...)` / `set_state(...)` communicates the same intent
- do not treat repeated silence after one deprecation warning as approval; Agently emits each deprecated API warning once per Python process
- do not treat `runtime.show_deprecation_warnings=False` as a migration substitute; it is only a production noise-control setting
- do not use flow data for per-execution state
- do not write guidance that depends on code after `await data.async_pause_for(...)` surviving a process restart; put post-resume logic in the downstream chunk, `data.is_resume` branch, or explicit resume event handler
- do not make service chunks depend on closure-captured business context when `runtime_resources` would keep the handler reusable, testable, and export-friendly
- do not pass raw model stream paths directly to the UI when the workflow can translate them into stable business events
- do not hide draft/judge/revise or similar loops inside one opaque helper
- do not make DevTools or graph tooling the source of truth for workflow structure when TriggerFlow definitions already are

## Read Next

- `references/overview.md`
- `references/runtime-intervention.md`
- `references/stream-bridge.md`
- `references/devtools-graph.md`
