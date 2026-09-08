# AgentExecution Plugins and Final Policies

Use this reference for the 4.1.4.8 development-line execution contract.
An Agent owns reusable configuration and module capabilities; its factory
constructs the actual selected AgentExecution class. The plugin owns one draft,
identity, production lifecycle, result, and final policies. Nested ModelRequest,
TaskContext, Actions, or other plugins are typed components, not extra owners.

## Selection

`agent.create_execution(name=None)` uses the configured `AgentExecution`
plugin or bundled `auto`. Explicit names override that default.

| Plugin | Producer | Explicit strategy |
|---|---|---|
| auto | Existing deferred request/task/DAG selection | Existing route strategies |
| request | One logical request and request-local repair | auto/direct |
| long_task | Retained multi-step goal work | auto/task/task_loop/long_task/flat/taskboard |
| plan | Readiness, necessary connected clarification, final plan | auto |
| long_content | Section plan, dependent writing, host assembly | auto |

Reject conflicting choices before model/Action dispatch. A route policy must
not silently replace an explicitly selected producer. Registration alone adds
no planning or review. The unreleased AgentPattern / `pattern()` API is
replaced, not a parallel selector. Released AgentOrchestrator activation and
AgentTask imports are compatibility paths to the same implementation.

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

Only a selected producer needing a complete goal contract derives missing
fields. The bundled long_task currently needs them before construction and
persistence, so it uses a visible prerequisite ModelRequest when incomplete.
Plan/long_content can plan from the original request and do not add this call.
When an existing planning/readiness node can provide the needed contribution
before its consumers, put it there instead of imposing a universal preflight.

Keep explicit goals/criteria and the original request unchanged. Inferred
fields carry host-bound request provenance and remain interpretations, not new
business hard gates. Missing required facts yield an explicit blocked outcome.
Complete or restored contracts do not regenerate criteria. Review-only and
ordinary requests do not trigger goal inference. Count preparation against the
same execution model/deadline limits; it does not gain Action permissions.
Restored task review reads the persisted original request when available,
not only the compatibility resume draft's goal declaration.

## Final Validation, Artifact and Review

- `validate(handler)` hard-checks final business output, not internal readiness,
  section, or task-step outputs. Scalar callbacks use the existing
  `{"value": ...}` convention. For long_task, policies use the same parsed
  final_result as get_data; get_full_data retains the task envelope.
  Direct request/ensure_long_output repair stays request-owned. Other producers
  validate once without replaying successful side effects.
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
LongContent invalidates dependent sections, and LongTask uses model-selected work
plus Host-validated dependency closure. Selecting final candidate delivery alone
preserves completed work. It never substitutes terminal task resume.
Model/time budgets, Flat iterations and TaskBoard ticks remain cumulative, and
an established revision cap cannot be raised. Set overall model budgets on
`create_execution("long_task", limits=...)`; legacy `create_task(limits=...)`
retains per-step request caps but shares its wall-clock bound across rework.
Previously dispatched Actions,
including uncertain effects, need `replay_safe` or explicit Host `allow_replay=True`;
children cannot weaken ancestor protection. Artifact callbacks require that same
explicit replay choice. Historical references are not backups or transactions.

Pause requests settle before production or at candidate-ready before final policies.
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
resuming the rebound one. Revision history, settled producer state, replay gates,
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
When a completed TaskBoard control result has a draftable manifest but no body,
the dedicated artifact-draft stage uses the same bounded evidence ledger;
materialization is not semantic remaining work and still needs verification
and promotion.

Metadata names the selected plugin; stage events are
execution.stage.started/completed, with diagnostics.execution_run.
Retained task/route metadata remains available; these events are additive
observations, not a new execution scheduler.
