# AgentExecution Plugins and Final Policies

Use this reference for the 4.1.4.9 development-line execution contract; released 4.1.x compatibility is identified below.
An Agent owns reusable configuration and module capabilities; its factory
constructs the actual selected AgentExecution class. The plugin owns one draft,
identity, production lifecycle, result, and final policies. Nested ModelRequest,
TaskContext, Actions, or other plugins are typed components, not extra owners.

## Selection

`auto_continue(enabled=True)` configures conditional model-output continuation
on an unstarted execution; it defaults off and all readers share the policy.
The released `ensure_long_output` spelling delegates to the same implementation.
Normal completion adds no continuation request. This does not select
`long_content`, expand short answers, resume a task or replace rework. Existing
`long_output` metadata/events and snapshot compatibility remain unchanged.
`long_content` produces whole text. The development line also supports explicit
`(LongContent, "writing requirements")` output declarations, with the compatible
`("long_content", "writing requirements")` string form; import LongContent from
agently. The final value remains str, and field production reuses the existing
long-content producer under the parent Execution. See the request skill's
output-control reference for declaration and dependency guidance.

`agent.create_execution(name=None)` uses the configured `AgentExecution`
plugin or bundled `auto`. Explicit names override that default.

| Plugin | Producer | Explicit strategy |
|---|---|---|
| auto | Existing deferred request/task/DAG selection | Existing route strategies |
| request | Direct output production; may compose explicit output producers | auto/direct |
| long_task | Retained multi-step goal work | auto/task/task_loop/long_task/flat/taskboard |
| plan | Readiness, necessary connected clarification, final plan | auto |
| long_content | Section plan, dependent writing, host assembly | auto |

Reject conflicting choices before model/Action dispatch. A route policy must
not silently replace an explicitly selected producer. Registration alone adds
no planning or review. The unreleased AgentPattern / `pattern()` API is
replaced, not a parallel selector. Released AgentOrchestrator activation and
AgentTask imports are compatibility paths to the same implementation.

`direct` is an Execution strategy, not permission to bypass Execution.
In the Jev development build, request execution can compose judgment and LLM
stages with explicit `from_output`/`after_output` dependencies and Host assembly.
SystemOne selects the dedicated template model from `system_one` configuration
or an existing model pool entry. Configured means enabled by default;
`.use_system_one(False)` uses the ordinary LLM while preserving dependencies.
OutputTemplate contracts remain provider-independent; Execution groups ready
templates by provider capability, preserving ordinary schema field order. ModelRequester
owns only the provider protocol; TriggerFlow owns stage/retry edges. Read
the request skill's output-control reference before using judgment declarations.

```python
execution = (
    agent.create_execution("plan")
    .input(request_facts)
    .interact(handle_exchange)
    .output(plan_schema)
    .validate(validate_plan)
)
plan = await execution.async_get_data()
```

For subclass reuse import `RequestExecution` and `ProductionOptions` from
`agently.builtins.plugins.AgentExecution`; specialize
`async _async_produce(self, options: ProductionOptions) -> tuple[str, object]`.
Call super() when reusing default production, then return the selected route
and final value. Register that class with
`agent.plugin_manager.register("AgentExecution", CustomExecution, activate=False)`.
Set activate=True only to change the default. A complete replacement can
implement the public protocol instead. Do not assign instance run aliases
that hide subclass overrides.

## Goals and Conditional Preparation

`goal(goal, success_criteria=None, *, turn_on_long_task=True)` declares semantic
Prompt fields. True additionally enables long-task convenience in the auto
producer. False is Prompt-only, not a ban on independently selected long_task
execution. Explicit plugin/strategy choices remain in force. Repeating goal()
before start replaces its convenience switch; goals() is the plural alias.
Neither declaration enables review automatically.

New goal-driven long tasks use one decision Loop with a model-editable Markdown
TaskBoard. It can add/remove/split/merge/reorder/check/reopen items; no default
per-card execution, per-card judge or independent finalizer is implied.
ContextPackage supplies effective context; existing ActionRuntime returns actual
observations before dependent decisions. Original goals/output remain authoritative.
Do not add a goal-preparation request when the original input already defines the task.

```python
execution = agent.create_execution("long_task").input(task).use_actions(actions).output(result_schema)
result = await execution.async_get_data()
```

The same decision returns continue/completed/blocked and useful full text or
structured data. When blocked, preserve useful work and explain relevant unfinished
requirements, uncertainties to check, actual risks and missing information.
Disclosure alone does not fulfill missing required work. Do not invent percentages
or assume every failure is model incapacity. Respect permitted incomplete templates
and task-defined negative outcomes; an impossible positive recommendation is not
necessarily an unfinished analysis.

Host retains budgets, exact file-delivery checks, required successful Actions and
replay policy. Failed explicit commitments return observations to the same Loop.
Use require_actions for required execution and artifact(path) for Host publication
of the final result; no new business gate or always-on judge is implied.

4.1.x keeps explicit flat/taskboard, old task/task_loop strategies, create_task and
old task-id recovery on their legacy producer. Legacy goal preparation and card
options belong only there. New long_task or ordinary goal-driven auto execution
uses the unified Loop. 4.2 uses only canonical long_task and execution save/load/
resume; old strategy names, create_task/create_task_loop and Agent task-id resume
are removed. Finish old states on 4.1.x; do not imply automatic conversion.

## Final Validation, Artifact and Review

- `validate(handler)` hard-checks final business output, not internal readiness,
  section, or task-step outputs. Scalar callbacks use the existing
  `{"value": ...}` convention. For long_task, policies use the same parsed
  final_result as get_data; get_full_data retains the task envelope.
  Direct request/auto_continue repair stays request-owned. Ordinary instant
  observation, including internal streaming for final-only callers, does not
  disable bounded validation retry. Only an actual SystemOne stage suppresses
  replay after a complete field is observed; ordinary LLM composition stages
  retain the shared retry allowance. Failed results are not accepted or handed
  to dependent stages. Other producers validate once without replaying successful
  side effects.
- `artifact(path, handler=None)` converts the final business result to text or
  bytes. TaskWorkspace owns containment, write, complete digest readback,
  trusted refs and retention. A later blocked review does not roll back files.
- `review(handler=None, *, rules=None, on_fail="warn")` inspects final quality
  and actual key artifacts. A sync/async (result, context) handler replaces the
  evaluator; rules quickly inject business rubrics. Default warn preserves the
  result; block raises AgentReviewError. Do not invent retry support or public
  verify(). Neither mode biases the evaluator or hides production rework.
- Default review reads complete trusted text artifacts and checks their content
  version before one structured ModelRequest. It is not metadata-only,
  automatic progressive disclosure, or segmented review. Non-text/unreadable/
  incomplete evidence is not_assessable; use a suitable handler for other
  formats. Context overflow fails explicitly.
- Judge a plan as a plan, including accepted clarifications. With no goals,
  inspect the original contract; do not invent review requirements.
- Quality levels are strong, adequate, weak, or not_assessable, not a model-
  invented numeric score. Boolean handlers leave the level null. checks[]
  covers supplied rules; issues[] has criterion, finding, evidence, and
  suggestions[]. overall_suggestions[] is distinct whole-result advice.
- Put contracts/rubrics in info, the candidate in input, behavior in instruct,
  and field definitions in output. Literal references such as
  [info.review_rules] point to existing content without rendering or copying.
  See [Prompt writing](../../agently-request/references/prompt-management.md).

## Lifecycle and Observation

run/async_run and compatible start/async_start/readers share once-only
production. Ordinary draft mutation cannot turn a started record into a new
request. Check `execution.control_capabilities` for implemented boundaries.
`previous = execution.get_result()` captures the current revision. After a settled
candidate, `await execution.async_rework(feedback, max_reworks=3)` advances the same
execution object/ID and returns a newly produced full result; old readers remain
bound to their original revision, also available via `get_result(revision=0)`.
Request, Plan, LongContent and LongTask own re-entry; Plan keeps accepted answers,
LongContent invalidates dependent sections, and the unified LongTask retains its
checklist, observations and original task while handling the new feedback in the
same decision Loop. Legacy task rework retains its prior dependency contract.
Model/time budgets and Loop rounds remain cumulative, and
an established revision cap cannot be raised. Set overall model budgets on
`create_execution("long_task", limits=...)`; legacy `create_task(limits=...)`
retains per-step request caps but shares its wall-clock bound across rework.
Previously dispatched Actions,
including uncertain effects, need `replay_safe` or explicit Host `allow_replay=True`;
children cannot weaken ancestor protection. Artifact callbacks require that same
explicit replay choice. Historical references are not backups or transactions.

Pause requests settle before production or at candidate-ready before final policies.
Unified long tasks also settle at long_task_step before a new decision, including
after an Action batch; saving and restoring that boundary does not replay settled
Actions. Observe long_task.progress for checklist/status/round and execution.stage.*
for model phases. Active Actions cannot be snapshotted.
At the actual TriggerFlow wait, run/readers raise `AgentExecutionPaused`;
`async_resume()` explicitly continues it. `async_interrupt(content)` supplies future
TaskContext information and reports consumption separately from insertion.
`async_cancel(timeout=...)` waits for owned cleanup; timeout is not settlement.
`async_close(pending="error")` drains and seals; use `pending="cancel"` to abandon a
pending wait. Draft close prevents production, completed close preserves readers.
Every control also has a sync wrapper.

`save()` returns a JSON snapshot only at a settled outer pause. Configure a fresh
execution with matching original draft, limits, Actions/Skills, callbacks, Workspace,
RecordStore and ContextSources, then `load(snapshot)` without dispatch. For task
creation, rebind the original task_id. Retire the original paused handle before
resuming the rebound one. The first restored typed reader validates the retained
candidate locally against the rebound original schema and caches it, including
nested/root Pydantic and LongContent declarations. Load does not run output-model
validators, and typed reads do not repeat production or final policies. Historical
typed readers use their own revision's candidate. Reconstruction errors raise.
Revision history, settled producer state, replay gates,
model counts and elapsed/offline time survive restoration. No settings, credentials,
live provider objects or executable code are restored. Missing/changed required
bindings fail; Skill catalog changes are conservatively rejected. Live
ExecutionResource state without a checkpoint contract prevents save; terminal
cleanup releases only owned execution scopes. Active children,
inner task checkpoints, disconnected clarification and nested-budget restoration
remain unsupported. Custom producers must declare safe rework explicitly.

Use TriggerFlow for visible branches, back edges and required waits;
ExecutionExchange owns the interaction envelope/provider seam. Plan currently
supports connected clarification, not a durable restorable plan handle.
The request-local interact handler receives a normalized ExecutionExchangeView
only when an exchange opens; it does not force interaction or replace the
global provider. Use existing async_add_guidance for non-blocking long-task
context; required answers use TriggerFlow waits. A dispatched request cannot
receive new Skills or Actions retroactively.

Treat instant streams as provisional and wait for final parsed data plus host
validation before irreversible work. Required side effects need actual Action
evidence; file readback proves file content, not an unrelated Action call.
On the 4.1.x legacy route only, when a completed TaskBoard control result has a draftable manifest but no body,
the dedicated artifact-draft stage uses the same bounded evidence ledger;
materialization is not semantic remaining work and still needs verification
and promotion.

Metadata names the selected plugin; stage events are
execution.stage.started/completed, with diagnostics.execution_run.
Retained task/route metadata remains available; these events are additive
observations, not a new execution scheduler.

## Extra Agent dependencies (4.1.4.8 development)

An Execution plugin declares `required_agent_capabilities = ("audio",)` when
its producer depends on an explicitly mounted capability. Use
`execution.require_agent_capability("audio")` to obtain the captured object;
dynamic dependencies use that same check before dependent work. This is not
an Action-use requirement, permission, model-support or health check. Shared
Execution instances retain captured bindings across Agent reconfiguration;
fully replaced implementations must preserve the contract. Extra-capability
snapshots currently fail explicitly rather than serializing live clients.
For audio setup and supported streams, read
`../../agently-request/references/audio.md`.

## Media and speech (model-capabilities development API)

Execution also owns STT/VLM/OCR input preparation and the say speech consumer.
Use the request skill's [model-capabilities reference](../../agently-request/references/model-capabilities.md)
for configuration-driven routing, direct image output, cached readers, shared
retry allowance, cancellation and audio delivery boundaries. ModelRequester
stays atomic. New execution.stage events and media metadata are additive; do
not infer text token usage for audio operations.
