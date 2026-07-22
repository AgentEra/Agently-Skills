# System Boundaries

Use this reference before selecting APIs. Assign each decision, state, effect,
and dependency to the smallest existing owner. Developer-owned stable execution
topology belongs to TriggerFlow; model-generated or application-submitted DAG
data belongs to TaskDAG / Dynamic Task. Per-execution state, task information,
task files, durable records, external resources, and shared `flow_data` are
different boundaries.

## Owner Matrix

| Owner | Owns | Does not own |
|---|---|---|
| ModelRequest | one prompt/output contract and provider response | multi-stage lifecycle or business workflow |
| AgentExecution / AgentTask | one Agent-owned execution or bounded task strategy | application-wide orchestration |
| Action | a model-callable capability and its evidence | resource lifetime or workflow policy |
| ExecutionResource | managed live dependency lifecycle | business decisions or state transitions |
| TaskContext | one task's bound information and internal derived ContextIndex | source truth, files, persistence, or execution |
| TaskWorkspace | one task's files, file refs, containment, exact readback, and atomic file promotion | records, semantic retrieval, or task policy |
| RecordStore | durable records, direct retrieval indexes, links, checkpoints, snapshots, leases, and durable refs | task file editing, model-hot context, or execution policy |
| TriggerFlow | trusted, developer-owned executable signals, dependencies, state transitions, waits, and close | unvalidated runtime plan data |
| TaskDAG / Dynamic Task | submitted or model-generated acyclic DAG data, validation, resolution, and execution | a second stable workflow framework |
| host code | admission, authorization, canonical identity joins, UI/transport, and external integration | model-owned semantic judgment |
| human/external system | approval or external response facts | hidden in-process blocking loops |

`agently-design` describes these boundaries. It does not own executable
TriggerFlow definitions and does not own submitted TaskDAG data.

## Deep Modules and Inward Dependencies

- Prefer a small stable contract over pass-through managers and shallow facades.
- Keep domain decisions independent from providers, storage, transport, UI,
  DevTools, and framework glue.
- Put mechanism adapters at the outside; point dependencies toward domain and
  execution contracts.
- Add a public entity only when an existing owner cannot carry the behavior.
  Record the nearest concept, the gap, and the non-overlap argument.
- Do not replace model-owned semantic decisions with keywords, regex, or local
  score tables. Use a structured ModelRequest and deterministic validation.

## Project and Layer Layout

Plan the owner/invariant, node, edge, and production-necessity ledgers before
choosing files. A logical node is not automatically a module, and an
architecture layer is not automatically a directory. Keep a small program
small; add a boundary only when it owns a current consumer, invariant,
lifecycle, policy, representation translation, or stable external contract.

The canonical conditional project shapes, wrapper acceptance test, runnable
asset, and FastAPI/FastMCP delivery boundaries live in
[`../../agently/references/project-framework.md`](../../agently/references/project-framework.md).
Do not maintain a second directory tree here.

## Stable Flow or Submitted DAG

Use direct TriggerFlow when trusted source code owns a stable executable graph.
Use TaskDAG / Dynamic Task when a model or application submits DAG-shaped plan
data at runtime. Validate and resolve that data before its TriggerFlow substrate
executes it; do not compile unvalidated plan data into ad hoc flow definitions.

An analysis diagram may show both paths, but it is not executable source of
truth and must not introduce a second graph protocol.

## State and Storage Boundaries

- execution state owns data private to one TriggerFlow execution and its
  chunk-to-chunk handoff;
- TaskContext owns task-information aggregation and its internal derived index;
- TaskWorkspace owns contained files, file refs, and physical readback;
- RecordStore owns durable records, links, checkpoints, snapshots, leases, and
  durable refs;
- ExecutionResource owns live clients and managed resource lifetime;
- host storage owns domain persistence and cross-service contracts;
- `flow_data` is shared on the flow object. `execution.save()` serializes a copy
  and `load()` replaces the current flow-shared value; this does not make it
  execution-local or concurrency-safe.

Do not create a translation helper or second state store when the existing
execution state, TaskContext, TaskWorkspace, RecordStore, or host persistence
boundary already fits.

## Terminology and Occam Gate

Before naming a new concept, check the repository concept registry, naming
conventions, public glossary, and owning feature docs. Reuse an existing term
when it carries the behavior. If a new term is unavoidable, document:

1. the nearest existing concept;
2. why it is insufficient;
3. the layer that owns the new term;
4. why a local alias or documentation clarification is not enough;
5. how the term avoids overlapping public APIs, events, placeholders, or graphs.

`agently-design` is a coding-agent Skill id, not a new Agently runtime concept.
“Model-request topology” is an analysis and audit view, not an executable graph.

## Design Review Checklist

- Are business decisions and completion invariants explicit?
- Does every decision, state, effect, and wait have one primary owner?
- Are policy layers independent from provider, storage, transport, and UI?
- Is stable source topology separated from submitted DAG data?
- Are execution state, TaskContext, TaskWorkspace, RecordStore, `flow_data`,
  resources, and domain storage used according to their real lifecycles?
- Was terminology overlap checked before adding a concept?
- Can the design become smaller by removing a wrapper, manager, or duplicate
  execution path?
- Are concrete API questions routed to the owning leaf Skill?
