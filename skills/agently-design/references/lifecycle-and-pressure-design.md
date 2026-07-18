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
