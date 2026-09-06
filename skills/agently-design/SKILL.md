---
name: agently-design
description: "Use to design, understand, tune, or audit a non-trivial Agently model workflow: model-node responsibilities, input/output completeness, data-flow correctness or redundancy, model-versus-Host/workflow ownership, topology, evidence, lifecycle, concurrency, or observed execution effects. The user need not say Prompt review or name Agently. Use agently-request for one request family and agently-triggerflow for already-decided executable orchestration details."
---

# Agently Design

Use this Skill for cross-owner design and audit. It produces ownership and
handoff contracts; it does not become a scheduler, TriggerFlow definition,
TaskDAG, retry engine, or RuntimeEvent protocol.

## Core Workflow

1. State the business decisions and completion invariants.
2. Classify each decision as model-owned semantic work, host-owned deterministic
   work, or a hybrid bounded-enum/key decision.
3. Assign every decision, state, effect, and wait to one existing owner.
4. Draw request-time value dependencies and execution-time event dependencies
   before choosing APIs.
5. Combine ordered fields in one ModelRequest only when later fields need no
   observation created after dispatch. Split after Actions, system access,
   approval, artifact readback, or host computation needed by a later model
   decision.
6. Derive each prompt/output field from an authorized consumer and declare its
   type, constraints, visibility, retention, and failure behavior.
7. Design evidence, canonical identity joins, lifecycle, convergence, pressure,
   and observation before implementation.
8. For an audit, reconstruct the observed topology and identify the earliest
   divergent node or edge rather than inferring root cause from final output.
9. Hand concrete implementation to the mechanism-owning Skill.

## Required Topology Contract

Use collaborative review when it can answer the developer's question about
model-node definitions, execution effects, data completeness/redundancy, or
model/Host division of work; do not require the phrase "Prompt review".
First show the whole in-scope flow, highlighting model nodes, their duties and
input/output handoffs alongside Host work. Read `references/model-request-topology.md`
for the question-to-evidence checks. Use the existing topology, not another
ledger; a drawing alone does not prove runtime correctness or quality.
Group related node tables for comparison under
`../agently-request/references/prompt-management.md`: up to three logical nodes
may share a reply, and tightly coupled larger groups are allowed. Clear scope
can be shown with its details in the same reply. Preserve consequential-change
confirmation and revisit only affected responsibilities/handoffs after revision.

Every non-trivial linear, branching, concurrent, or looped application needs:

- an owner/invariant ledger;
- a planned node ledger with each ModelRequest or host stage and its boundary
  reason;
- a value/event edge ledger with exact producer, validation, and consumer;
- a production-necessity ledger for every requested node, field, and artifact.

Use small project-defined reference data at a handoff only when it enables an
independent consumer, parallel development, replay, local validation, or fault
localization. Mark simulated data honestly and prove that real producer output
can replace it. Do not invent a universal handoff packet.

Treat a non-terminal model result as a stage-scoped contribution: it must
satisfy its local contract and create observable progress, but it does not need
to claim whole-task completion. Unknown or deferred work remains explicit;
terminal results and irreversible effects still require full acceptance.

## Read by Design Question

- Owner matrix, project layers, terminology, state/storage, and stable flow
  versus submitted DAG: `references/system-boundaries.md`.
- Model-node definitions, effect tuning, data-flow correctness/redundancy,
  flow-first review, prompt/output contracts, same-response consumption,
  fan-out, joins, and `instant`: `references/model-request-topology.md`.
- Full planned-versus-observed value/signal audit:
  `references/execution-topology-validation.md`.
- TaskContext packages, TaskWorkspace/RecordStore evidence, trusted selection
  keys, refs, citations, snapshots, and fail-closed joins:
  `references/information-and-evidence-design.md`.
- Concurrency, retries, repair, replan, approval, pause/resume, cancellation,
  close, pressure, and planned long-form section generation:
  `references/lifecycle-and-pressure-design.md`.
- RuntimeEvents, lineage, request telemetry, model-quality review, and
  experiment comparison: `references/observability-and-validation.md`.

After ownership is clear:

- one request family routes to `agently-request`;
- Action, MCP, ExecutionResource, TaskWorkspace, RecordStore, service, or
  telemetry mechanics route to `agently-runtime`;
- developer-owned executable orchestration routes to `agently-triggerflow`;
- explicit submitted TaskDAG data remains a low-frequency `agently` advanced
  reference rather than a standalone default Skill;
- source-framework mapping routes to `agently-migration`.

## Non-Negotiable Boundaries

- Model participation alone does not justify another request. Split only for a
  real decision, evidence, consumer, authorization, retry, lifecycle, or
  parallelism boundary.
- A ModelRequest is a dispatch-time snapshot. Provisional `instant` output may
  update UI or start cancelable/idempotent preparation, but cannot inject that
  preparation's result back into the running request.
- Give the model one host-issued selection key plus relevant facts. Host code
  validates the offered key and reconstructs canonical ids and metadata.
- If a selection can cross cache, queue, retry, persistence, or replay, bind it
  to host-owned semantic-request lineage and validate freshness before lookup.
- Every model-satisfiable business rule reaches the producer before its first
  attempt. Deliberately hidden security or integrity gates remain host-owned and
  need explicit failure/terminal policy.
- Do not request hidden chain-of-thought. Keep only bounded task-specific
  process fields with an explicit consumer and retention contract.

## Completion Gate

Before implementation, confirm that every invariant has one owner, every
request boundary has a reason, every output field has an authorized consumer,
every provisional path has invalidation behavior, every loop has progress and
terminal rules, every cross-boundary identity has freshness/correlation, and
every validation rule has a declared producer or deliberately hidden host gate.

Do not replace semantic routing, relevance, planning, or quality judgment with
keywords, regex, tokenization, or local score tables. Do not add a parallel
execution topology beside TriggerFlow or TaskDAG.
