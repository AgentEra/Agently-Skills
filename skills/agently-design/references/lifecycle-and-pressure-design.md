# Lifecycle and Pressure Design

Draw real dependencies before scheduling. Ordered facts stay serial; independent
work should overlap with an explicit owner and bound. Pressure controls live at
the layer that admits or creates work: host in-flight coroutines, TriggerFlow
execution concurrency, operator fan-out, model scheduler/rate limits, and host
thread pools for blocking code. Retry and repair need progress evidence and a
terminal rule: three occurrences of the same unchanged terminal problem with no
new trusted fact, capability, or state must stop and fail closed.

## Dependency Classification

For each stage, label it:

- required-before: a real data, ordering, authorization, or side-effect
  dependency requires serial execution;
- independent: work can run concurrently;
- provisional: structured progress may start only cancelable/idempotent
  preparation;
- join: downstream work waits for a declared set and partial/failure policy;
- terminal: final validation authorizes completion or irreversible effects.

All-serial design without this analysis is an anti-pattern. So is concurrency
that ignores provider, external-system, memory, or side-effect capacity.

## Execution Ownership

Application-owned branching, fan-out, joins, loops, approvals, pause/resume,
runtime streams, and close belong to TriggerFlow. A local async caller may
overlap a small set of independent single requests when no graph-visible
lifecycle is needed. Submitted acyclic plans belong to TaskDAG / Dynamic Task.

Use async Agently APIs in services and workflows. Consume `instant` only when a
real UI, observer, state update, or cancelable/idempotent preparation uses it;
otherwise await final data directly.

## Pressure-Control Owners

| Layer | Control |
|---|---|
| host admission | request queue, semaphore, per-tenant quota, in-flight coroutine limit |
| TriggerFlow | concurrent executions and lifecycle ownership |
| operator | `batch` / `for_each` fan-out cap and join scope |
| model scheduler | model/provider concurrency, rate, retry-after, token/request budget |
| Action/external adapter | dependency-specific pool, quota, timeout, circuit policy |
| blocking host code | bounded worker or thread-pool size |

Expose the controls users actually need to tune. Do not describe coroutine or
thread counts as one universal TriggerFlow setting.

## Provisional Work and Side Effects

An `instant` field is attempt-local and provisional. It may update a UI or start
work that is both idempotent and cancelable. Irreversible actions, domain state
changes, external publication, payment, deletion, and final business decisions
must wait for the final parsed result and configured validation. When the
attempt fails or is superseded, invalidate its provisional work.

For provisional fan-out, keep a host-owned map from canonical task payload to
the managed task or cached result. Complete early items may start within the
external adapter's concurrency and rate limits while the stream consumer keeps
reading. After final validation, join only accepted keys, start any accepted
key missed by streaming, and cancel or discard every extra provisional key.
This final reconciliation is the correctness barrier and also prevents provider
replay or repeated deltas from repeating retrievals.

## Retry, Repair, and Replan

Before another attempt, record:

1. the failure owner and evidence;
2. what trusted fact, capability, state, prompt contract, or hypothesis changes;
3. which prior provisional outputs become invalid;
4. the expected measurable improvement;
5. the next terminal condition.

Retry repeats a mechanism after a transient failure. Repair changes a malformed
or incomplete contract result. Replan changes the task path after evidence shows
the current path cannot complete. Do not use any of them as an unbounded loop or
as a substitute for missing capability.

If the same terminal problem appears three times without a new trusted fact,
capability, state transition, or narrower verified hypothesis, stop. Return a
structured blocked or failed result with the repeated evidence; do not keep
spending model or tool calls.

## Approval, Wait, Resume, Cancel, and Close

- approvals and external replies are explicit waits with authorized request and
  response contracts;
- pause/resume preserves execution lineage and validates resume identity;
- cancellation propagates to provisional work and prevents later side effects;
- finite self-closing work may use flow-level start/runtime-stream helpers when
  the caller needs no execution handle;
- pause/resume, external emit, save/load, intervention, inspection,
  cancellation, or host-controlled close requires an explicit execution.

Distinguish natural provider completion from consumer early-close. Provider
completion means the model/result reached its own final state. Consumer
early-close means a UI or transport stopped listening; it must not silently mark
the underlying work complete or authorize effects.

## User-Driven Task Continuation

Do not treat a user's word such as "continue" as a deterministic resume command.
Separate structured interface intent from prose-derived intent:

- a host-issued **Resume this task** action may route deterministically after
  authorization and lifecycle checks;
- a reply structurally bound to one task fixes the candidate identity, not the
  lifecycle intent. Its free-form text still needs semantic judgment;
- a free-form message requires one structured ModelRequest to judge whether the
  user means `resume_existing`, `start_new`, or `clarify`;
- a task that is still running is not resumable. Report or observe its current
  execution instead of starting a duplicate;
- a completed task is not continued by replaying its terminal snapshot. New
  follow-up work starts a fresh task and may consume the prior result or
  evidence through TaskContext.

Before the semantic request, host code must discover and authorize candidates.
Project each resumable candidate with one short `selection_key` plus only
task-relevant facts such as goal summary, last trusted progress, remaining work,
and snapshot compatibility. Keep canonical task ids, snapshot refs, and full
metadata host-side.

The ModelRequest owns only the semantic relationship between the current
message and the offered candidates. Its output contract should contain:

- `decision`: required enum `resume_existing | start_new | clarify`;
- `selection_key`: nullable string, required to be one of the offered keys when
  `decision=resume_existing`;
- `clarification_question`: nullable bounded string, required when
  `decision=clarify`.

After parsing, host code must validate authorization, offered-key membership,
canonical identity, non-terminal status, absence of another live execution,
snapshot presence/version, and the cross-field decision contract. Unknown,
stale, unauthorized, or ambiguous candidates fail closed to clarification.
Never ask the model to reproduce `task_id`, snapshot ids, or identity-heavy
records.

Resume preserves the original task goal, success criteria, and deliverable
contract. If the user changes any of them, asks for a fresh attempt, or requests
new work after completion, create a new AgentExecution/task id. The new task may
bind authorized prior results, evidence, or artifacts as context without
misrepresenting that relationship as resume.

Keep this as one logical ModelRequest: candidate facts, routing rules, decision,
selection key, and optional clarification share one request-time snapshot.
Dispatch remains a later host-owned effect after final parsing and deterministic
validation. Do not add a keyword router, Interface-owned task manager, or a
parallel resume lifecycle.

## Terminal Status Matrix

| Status | Required meaning |
|---|---|
| completed | all required invariants and final validations passed |
| partial | explicitly permitted subset completed; missing work and effects are named |
| blocked | completion needs new authority, input, capability, or external state |
| failed | owned mechanism or validation failed with no valid recovery path |
| cancelled | authorized cancellation stopped further work and invalidated provisional effects |

Every status should include the last trusted state, evidence refs, incomplete
invariants, authorized effects already committed, and safe resumption policy.

## Lifecycle Review Checklist

- Are serial edges justified by data, order, safety, or capacity?
- Are independent branches concurrent and bounded at the owning layer?
- Do fan-out and joins define identity, scope, partial failure, and collection?
- Are provisional fields correlated and invalidatable?
- Can retry/repair/replan prove progress rather than repetition?
- Are approvals, resume identity, cancellation, and close explicit?
- Is provider completion distinguished from consumer disconnect?
- Does each terminal status state which invariants passed or remain?
- Does the unchanged-problem rule stop after three evidence-equivalent failures?

Use `agently-triggerflow` for concrete flow, fan-out, wait, stream, state, and
close APIs; use `agently-request` for result consumption and model scheduler
details; use `agently-runtime` for Action/resource-specific pressure controls.
