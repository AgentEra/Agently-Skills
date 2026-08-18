---
name: agently-design
description: "Use when the user is designing, reviewing, optimizing, or auditing a non-trivial Agently system across multiple owner layers, including execution-layer selection, ModelRequest prompt/output schema handoffs, point-to-point/fan-out/join topology, instant structured streams, context/evidence/identity boundaries, lifecycle/retry/repair/terminal behavior, concurrency/pressure, observability, or locating where information was lost between requests. The user may describe a multi-model-request application without naming Agently. Use agently-request for one request family and agently-triggerflow for already-decided executable orchestration details."
---

# Agently Design

Use this skill to design or audit a non-trivial Agently system before choosing
mechanism APIs. It owns cross-layer reasoning and request-chain audit methods;
it does not own executable TriggerFlow definitions and does not own submitted
TaskDAG data.

Treat this page as routing and workflow guidance. When the request needs an
owner matrix, project-layer separation, or the stable-versus-submitted topology
boundary, read `references/system-boundaries.md` rather than answering from this
summary alone.

## Core Workflow

1. Reduce the system into business decisions and completion invariants.
2. Classify each decision as model-owned semantic work, host-owned deterministic
   work, or a hybrid decision before deciding ModelRequest node boundaries.
3. Assign every decision, state, and effect to an existing owner layer.
4. Draw planned request and execution dependencies before choosing APIs.
5. Test the request-time input snapshot: combine ordered supporting steps only
   when later fields need no fact beyond dispatch-time input and earlier fields
   in the same response. Split after any Action, system access, approval,
   readback, or host computation whose new observation a later model step needs.
6. Design each ModelRequest prompt/output contract from declared consumer needs,
   and check every prompt-slot item for current-node relevance: it must change
   that node's task, contract, evidence, permission, restriction, or required
   result.
7. Map output fields to same-response, next-pass, external, user-process,
   point-to-point, fan-out, join, stream, and terminal edges.
8. Design information, evidence, and identity boundaries with fail-closed behavior.
   For a selection that can cross cache, queue, retry, persistence, or replay,
   record the Host freshness/correlation boundary before canonical lookup;
   a strictly inline awaited response that cannot cross a request boundary has
   no extra model-returned correlation requirement.
9. Design lifecycle, retry/repair convergence, concurrency, and pressure controls.
10. Design observability and validation before implementation. Every
    model-satisfiable acceptance rule must reach the producer before its first
    attempt; classify deliberately hidden host gates separately.
11. Route concrete implementation to the owning leaf Skills.
12. For audits, reconstruct actual topology and diff it against the plan.

Keep these two views distinct:

- analysis topology describes logical ModelRequests, information contracts, and
  consumers;
- execution topology describes trusted runtime mechanisms after ownership is
  resolved.

The design view may recommend an owner and produce implementation contracts. It
must not become a second scheduler, flow definition, TaskDAG, retry engine, or
runtime event protocol.

## Route Inside This Skill

- owner layers, project boundaries, stable flow versus submitted DAG, state,
  storage, terminology, or architecture review ->
  `references/system-boundaries.md`
- ModelRequest nodes, prompt/output contracts, schema edges, `instant` fan-out,
  joins, request ledgers, or planned-versus-observed topology ->
  `references/model-request-topology.md`
- ContextPackage, Workspace evidence, trusted selection keys, identity joins,
  refs, citations, snapshots, or evidence fail-closed rules ->
  `references/information-and-evidence-design.md`
- serial/parallel dependencies, concurrency limits, retries, repair, replan,
  approvals, pause/resume, cancellation, close, or terminal status ->
  `references/lifecycle-and-pressure-design.md`
- lineage, RuntimeEvents, request telemetry, topology reconstruction, model
  judges, experiment comparison, or request-chain audit ->
  `references/observability-and-validation.md`

After design ownership is clear, route exact mechanisms as follows:

- single-request provider, prompt, output, response, Session, or retrieval APIs
  -> `agently-request`;
- Action, MCP, ExecutionResource, Workspace, service, or telemetry mechanics ->
  `agently-runtime`;
- model-generated or application-submitted DAG validation and execution ->
  `agently-dynamic-task`;
- developer-owned executable stable workflow topology ->
  `agently-triggerflow`;
- source-framework mapping and migration sequencing -> `agently-migration`.

## Required Design Artifacts

Every non-trivial linear, branching, concurrent, or looped system requires one
planning-topology contract containing all four ledgers:

- owner/invariant ledger;
- planned node ledger;
- planned edge ledger;
- production-necessity ledger.

Add only the other artifacts needed for the task, usually a subset of:

- an owner matrix for decisions, state, effects, and mechanisms;
- planned logical-request and execution-dependency diagrams;
- one node contract card per logical ModelRequest;
- a schema-to-consumer edge matrix;
- information, evidence, identity, lifecycle, and pressure policies;
- observability fields and validation gates;
- an audit ledger with the first divergence and verified root cause;
- an implementation handoff naming the leaf Skill for each mechanism.

Use types and field-level constraints wherever a downstream system consumes
model output. Treat `instant` values as provisional until the final parsed
result and configured validation accept the originating attempt.

For every ModelRequest node, keep an item only when it changes the current
node's task, contract, evidence, permission, restriction, or required result,
or provides useful user-visible process context, state, or explanation with a
declared user or UI consumer. Retain or behaviorally rewrite an effective
upstream caller guarantee when it changes the model-owned decision or the
allowed verdict set. Audit the rendered execution draft before dispatch; when
runtime extensions can inject later, observe the final ModelRequest
`prompt_text` after injection in a bounded test and redact retained evidence.

## Anti-Patterns

- Do not turn this Skill into a broad `best-practices` dumping ground.
- Do not create a parallel executable topology beside TriggerFlow or TaskDAG.
- Do not review an output schema in isolation when its fields feed downstream
  requests, Actions, joins, UI streams, or terminal gates.
- Do not copy project history or unexplained implementation names into a node
  contract merely because they are available; retain only current-node-relevant
  context and preserve real domain contracts, allowlists, evidence, input facts,
  and capability boundaries that change the request.
- Do not delete effective upstream guarantees as project-origin context, or
  treat generic project narration as useful user-visible process context
  without a declared user or UI consumer.
- Do not replace model-owned semantic understanding, intent recognition,
  routing, response generation, judgment, planning, or ambiguity resolution
  with tokenization, keyword tables, substring rules, or regular expressions.
- Do not equate model participation with a separate ModelRequest; first test
  whether an existing ordered contract or an existing loop node owns the work.
- Do not force a post-Action or post-readback semantic step into the producing
  request. `instant` can start provisional work early, but it cannot inject that
  work's later result into an already-running ModelRequest.
- Do not request hidden chain-of-thought. Use bounded, task-specific
  deliberation artifacts only when their semantic role and consumption contract
  are explicit. A generic `reasoning`, `analysis`, or `thinking` field without
  those annotations is not a design justification or quality result.
- Do not trigger irreversible actions from provisional `instant` updates.
- Do not ask the model to copy canonical ids, UUIDs, or full metadata for joins.
- Do not treat offered-set membership as freshness for a delayed, replayed, or
  retried selection; bind it to Host-owned lineage or per-request opaque keys
  and validate Host correlation before canonical lookup.
- Do not diagnose from aggregate request counts without classifying logical
  requests, provider attempts, stages, and consumers.
- Do not claim root cause from final output alone; verify the earliest divergent
  node or edge against direct runtime, source, and artifact evidence.
- Do not use hard-validator rejection as an undisclosed prompt-discovery loop.
  If a production gate cannot be safely explained to the model, warn the
  developer and require explicit second confirmation before implementing it.

## Completion Gate

Before implementation, confirm that every business invariant has an owner,
every ModelRequest node has an ownership and boundary reason, and every
model-produced field has an authorized same-response, next-pass, external, or
user-process consumer with a declared consumption contract. Confirm that every
provisional path has invalidation behavior, every loop has progress and terminal
rules, every model-satisfiable validation rule is present before the first
attempt, every cross-boundary selection has a Host freshness/correlation
binding before canonical lookup, and every intentionally hidden gate has an
explicit host-owned policy.
Then hand concrete work to the
mechanism-owning Skills without copying their API instructions here.
