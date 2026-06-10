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
  prove replan behavior from stream verification/replan events and snapshots
  rather than hiding the proof in a local Python loop; mocked business systems
  may supply defective facts or conflicting source data, but must not return
  pass/fail verdicts or deterministic quality judgments
- default to async-first workflow handlers, execution entrypoints, and runtime stream consumers
- treat sync TriggerFlow APIs as wrappers for scripts or compatibility bridges, not as the default service interface
- prefer explicit execution lifecycle control with `close()` / `async_close()` for completion and cleanup
- treat `create_execution(concurrency=N)` and `execution.set_concurrency(N)` as an execution-wide handler dispatch budget, including nested dispatch from chunk continuations and `data.async_emit(...)`; use operator-local `batch(..., concurrency=...)` or `for_each(..., concurrency=...)` only for local fan-out caps
- use `execution.result` when services, UIs, stream consumers, or intervention-aware workflows need multiple views of one execution outcome, such as state, compatibility final result, interventions, and metadata; use `execution.close()` / `execution.async_close()` for close snapshots
- use runtime intervention for optional supplemental context added while an execution is already running: define explicit `.intervention_point(...)` boundaries so execution creation can infer planned mode, or create the execution with `intervention_mode="auto"` for boundary policy insertion; chunks read inserted context with `data.get_interventions(...)` and explicitly audit usage with `data.async_mark_intervention_consumed(...)`, relying on the chunk-name consumer default unless another consumer identity is clearer
- for human approvals, webhooks, or externally resumed waits, use `pause_for(..., resume_to="next" | "self" | {"event": ...})`; treat it as a durable graph interrupt, not Python coroutine stack persistence; teach model-decided autonomous interrupts with model-owned `pause_for(..., resume_to="self")`, where the resumed chunk handles `data.is_resume` and the default `max_resumes=1` prevents unbounded self-replay; teach prearranged approval gates with an explicit pause chunk plus `when(...)`
- for framework policy approvals, use the global PolicyApproval contract and
  represent pending approvals as `pause_for(type="policy_approval", ...)`
  interrupts that resume through `continue_with(...)`
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
- when discussing restart or distributed recovery, describe `execution.save()`
  as an execution snapshot that includes a versioned `checkpoint` envelope with
  durable TriggerFlow progress, flow definition fingerprint validation,
  interrupt/resume ledgers, resource requirements, lease metadata, and managed
  execution environment requirements.
  Do not imply live `runtime_resources`, clients, callbacks, tasks, semaphores,
  or Python coroutine frames are serialized. Declare future resources with
  `flow.declare_resource_requirement(...)` or
  `execution.declare_resource_requirement(...)`, inspect or restore with
  `execution.inspect_rehydration(...)` / `execution.async_rehydrate(...)`, pass a
  stable `resume_request_id` to `continue_with(...)` for external callbacks, and
  persist through a checkpoint store that implements `put_checkpoint(...)` while
  the production store owns atomic claim, lease enforcement, and conflict
  handling. If a checkpoint fingerprint is missing or does not match the
  current flow definition, `inspect_rehydration(...)` reports
  `invalid_snapshot` and `load(...)` rejects the snapshot
- for service packaging, treat ordinary `TriggerFlow(...)` as the definition/planning surface; prefer module-level named chunks and conditions, inject stable dependencies through flow-level `runtime_resources`, and inject request-specific dependencies through execution-level `runtime_resources`
- route model-generated or app-submitted DAG data to `agently-dynamic-task`; Dynamic Task is a first-class Agently API that uses TriggerFlow as an execution substrate, not a TriggerFlow sub-API
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
- when a TriggerFlow + SkillsExecutor example relies on a trusted local Skill
  bundle to provide declared helper capabilities, pass selector-level
  `auto_allow=True`; explicit host `configure_skill_capabilities(...)` policy
  still wins and Skill metadata alone is not a capability grant
- keep runtime stream consumers safe by relying on execution close to stop the stream
- keep workflow stages visible instead of hiding nested request loops
- name chunks and stage boundaries so exported flow configs, Mermaid diagrams, and runtime graphs stay readable
- let TriggerFlow definition export and runtime metadata drive visualization instead of maintaining a second manual graph description
- combine with `agently-request` when one workflow step needs model setup, prompt contracts, structured output, response reuse, session behavior, or retrieval

## Python API Shape

When generating or editing Python code, use the actual Agently API shape:

```python
from agently import Agently, TriggerFlow, TriggerFlowRuntimeData

agent = Agently.create_agent()
flow = TriggerFlow(name="workflow-name")
```

`when`, `emit_nowait`, and `pause_for` are not top-level imports from
`agently`. They are methods on flow or runtime data objects:

- define graph branches with `flow.when(...).to(handler, name="...")`
- fan out from inside a chunk with `data.emit_nowait(...)`
- pause from inside a chunk with `await data.async_pause_for(...)`
- create and close long-running/manual executions with
  `execution = flow.create_execution(auto_close=False)`,
  `await execution.async_start(input_value)` using a positional start value, and
  `snapshot = await execution.async_close()`
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
Do not import `Agent` from `agently` or call `Agent()` directly; create agents
with `Agently.create_agent()` so plugin manager and settings ownership stay
inside the framework boundary.

## Dynamic Task Boundary

Do not treat Dynamic Task as TriggerFlow syntax. If a model or application
submits a DAG as data, route to `agently-dynamic-task` and use
`Agently.create_dynamic_task(...)`, `TaskDAGValidator`, and `TaskDAGExecutor`
there. TriggerFlow remains the substrate for stable workflow definitions that
the developer owns in code.

## Anti-Patterns

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
