# Project Stages and Deliverables

Use this reference to adapt design work to the project's current evidence.
A stage is a work context, not a maturity score or runtime state. When stages
are mixed, name the primary question and preserve the useful existing work.
Infer what is already known; do not repeat answered questions or add approval
gates merely because a project is incomplete.

## Stage Selection

| Stage | Evidence | First useful deliverable |
|---|---|---|
| New design | Business goal or user journey without a working flow | Smallest viable end-to-end loop, owner/node/edge contracts, implementation order and acceptance criteria |
| Partial implementation | Prompts, scripts, interfaces, diagrams or trial outputs with gaps | Current flow, evidenced gaps, keep/change/add/remove decisions, target flow and migration steps |
| Production review | Completed system/design, logs, metrics, incidents or user feedback | Evidence-linked findings, impact and priority, short-term mitigation, evolution steps and verification plan |

Ask only when the answer would change ownership, scope, acceptance, or a
consequential implementation decision. Relevant unknowns can include users and
success criteria, actual data/tool availability, existing interfaces and state,
compatibility constraints, irreversible effects and authority, cost/latency
budgets, and applicable privacy or human-review requirements. State remaining
assumptions instead of silently filling gaps.

## New Design

Define the business outcome, scope and non-goals before choosing a model or
framework. Explain where semantic work is needed and which exact operations
remain deterministic. Plan a minimum useful loop and distinguish required
capabilities from optional future enhancements. Sequence implementation by real
consumer dependencies; identify how the first end-to-end result will be checked.

## Partial Implementation

Reconstruct the current flow before drawing a target. Use available code,
input/output samples, interface contracts and failure evidence. For each proposed
change, connect current state -> problem -> consequence -> recommendation;
mark it keep, change, add, or remove and state the reason and migration risk.
Preserve working contracts and compatibility requirements. Prioritize the gaps
that prevent a trustworthy result, such as missing data, unvalidated effects,
unobservable failures, or unsafe recovery, rather than automatically redesigning
all nodes. Separate confirmed defects from hypotheses requiring a probe.

## Production Review

Declare the review question, evidence scope, service targets/budgets, change
window and protected boundaries. For each finding record evidence, impact,
possible cause, priority, proposed action and verification. Distinguish observed
facts, inference and verified cause using the existing observability reference.
A finished system with no accessible traces permits a design review, not a
claim about observed runtime quality. Prioritize bounded mitigation before a
structural rewrite when that is sufficient, and state residual uncertainty.

## Scale the Deliverable

Use only the sections needed for the task, while preserving the existing
owner/invariant, node, edge and production-necessity contracts. Reuse those
ledgers rather than adding another mandatory node table or report protocol.
A useful order is:

1. Stage, evidence, goal, success criteria, assumptions and unresolved facts.
2. Current flow where one exists, then proposed changes and their rationale.
3. Flow overview and exact node/data contracts, with model participation,
   deterministic work, human roles and consumed outputs visible.
4. Applicable state, side-effect authorization, failure/recovery and human
   escalation boundaries; preserve existing authorization rather than demanding
   approval for every action.
5. Evaluation evidence and operating budgets, implementation or migration order,
   risks and remaining validation.

Use the task's requested language. A flow picture accompanies a concise text
walkthrough and precise contracts; it never proves behavior by itself. Read the
[flow presentation guidance](model-request-topology.md#flow-presentation) when
choosing or delivering a diagram.
