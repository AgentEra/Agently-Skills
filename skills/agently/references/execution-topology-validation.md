# Execution Topology Validation

Use this reference to diagnose or evaluate a complex Agently run that contains
multiple ModelRequests, TriggerFlow chunks, business blocks, Actions, Workspace
readbacks, external waits, repairs, or terminal gates.

## Core Rule

Build the execution topology from declared schemas, host mappings, and observed
RuntimeEvents before reading business prose for a root cause. A stage occurring
after another stage does not prove that its values were transferred. An event
edge proves activation only; a value edge must identify the exact carrier.

Use content only after the topology identifies an ambiguous or failed edge, and
then read only the bounded values needed to test that edge. Keep full private
prompts, raw payloads, and large artifacts in protected cold evidence.

## Required Node Standard

Every node in the audit must have a stable audit key and one owner. Record the
following fields; do not replace them with a prose stage summary.

### ModelRequest node

- logical request key plus request, response, attempt, model-run, parent-run,
  task, execution, stage, and owner lineage when available;
- trigger event or calling block;
- `prompt.input`: every field name, declared or observed type, requiredness,
  source owner, completeness/bounds, and value ref or bounded preview;
- `prompt.info`: authoritative contracts, source/schema documentation, enums,
  identity rules, and policy facts;
- `prompt.instruct`: the material transformation, selection, judgment, and
  completion rules, with a protected ref when the text is large or private;
- `output schema`: every field name, type, requiredness, enum/format/range,
  nullability, cross-field constraint, and downstream consumer;
- actual parsed output: field presence, parsed type, bounded value/ref, schema
  validation result, and any dropped or defaulted fields;
- lifecycle: `request.started`, `model.request_started`, `prompt.built`,
  `model.requesting`, provider completion/error, `request.completed`,
  `model.completed` or `model.parse_failed`, `model.meta`, status, usage, retry,
  cancellation, and timestamps when those events belong to the configured
  path.

### TriggerFlow or business-block node

- flow, execution, chunk/block, iteration, parent, and correlation identity;
- declared business input payload/schema and the exact start or inbound signal;
- inbound signal name, payload schema, correlation key, and trigger condition,
  recorded separately from business input values;
- state keys read and their versions before execution;
- handler, ModelRequest, Action, Workspace, subflow, or external-exchange calls;
- declared business output/result schema and exact downstream consumers;
- state writes, emitted signal names and payload schemas, RuntimeEvents,
  interrupts, artifact/ref writes, and side effects, each recorded separately;
- retry, replay, idempotency, fan-out concurrency, join mode, stop condition,
  and close/terminal behavior when applicable.

Include Action, Workspace, subflow, and external-wait nodes when they own a real
contract boundary. Do not hide them inside a generic “execution” node.

## Required Edge Standard

Record an edge ledger beside every diagram. Each row must name:

- `from`: exact node plus output/state/payload field or emitted event;
- carrier kind: `value edge`, `signal/event edge`, state edge, ref/readback edge,
  control edge, or side-effect edge;
- host transform: validation, projection, join, merge, filtering, compaction,
  defaulting, version selection, serialization, or identity reconstruction;
- `to`: exact downstream `prompt.input` field, block input, state key, signal
  handler, join, gate, or external consumer;
- cardinality and correlation: one-to-one, fan-out, fan-in, iteration, selection
  key, execution id, content version, or other host-owned join key;
- observed evidence: RuntimeEvent ids/timestamps and source-code owner when
  runtime evidence alone cannot prove the mapping;
- status: transferred, absent, schema-mismatched, filtered, truncated, stale,
  duplicated, overwritten, defaulted, unconsumed, or unknown.

A `signal/event edge` must name the exact emitted signal or RuntimeEvent, its
payload schema, trigger condition, and consumer. It does not imply that any
other value was transferred. A `value edge` must trace one exact upstream field
through every host transform into an exact downstream field. Similar wording in
two prompts is not lineage evidence.

For host-issued identities, show the model-visible selection key, host
validation, canonical lookup, and reconstructed record as separate steps. For
Workspace files or other mutable resources, show locator id and content/snapshot
version; path equality alone is not a current-value join.

When one structured output carries both local result state and orchestration
control, trace them as separate value edges. For example, TaskBoard card
`status`/`sufficient` describe the current card, while `next_board_action`
controls board progression. The topology must show each host mapping separately
and mark any transform that overwrites a completed card merely because the board
returns `stop` or `continue` as invalid.

For terminal material-claim verification, trace provenance eligibility in
addition to carrier/path/version identity. A generated carrier, delivery, copy,
host-applied patch, or readback derived from task output remains transport
evidence even when its path or content version changes; it cannot become an
independent source for a descendant carrier. Show producer `role`, `source`,
content-version lineage or carrier-derivative classification, the eligibility
filter, and the exact evidence records offered to the verifier. Treat a
carrier-supported-by-ancestor-copy edge as invalid self-support, not as semantic
model support.

## Carrier and Repair Identity

When one task has more than one delivery carrier, show each owner and transfer
explicitly. At minimum, trace this complete chain when it exists:

```text
planner.output.deliverable_mode
  -> host carrier normalization
  -> artifact-body / inline-result selector
  -> Action or Workspace write + physical readback
  -> trusted-artifact promotion
  -> current terminal-carrier inventory/version
  -> host exact-span projection + request-local claim_key map
  -> one semantic terminal verifier
       (criterion_checks + material_claim_checks)
  -> host claim/evidence-key validation + canonical carrier/quote reconstruction
  -> structured material-claim repair contract
     OR accepted terminal result/ref projection
```

The artifact body, compact inline result, and trusted artifact ref are distinct
values. Copying one into another is a separate value edge and requires an
explicit declared owner; graph adjacency or a shared final-result label does
not authorize the copy. A manifest-bound successful Action write may promote
its physical Workspace readback as the trusted artifact. Action prose, a
model-declared path, or an unverified ref cannot.

For that manifest path, the successful file Action is also the only write
owner. The materialization block must adopt its readback, never copy a
conflicting model-returned body onto the same path. A revision needs a new file
Action event and content version; unreadable Action-owned output fails closed.
A later TaskBoard leaf that only verifies or references the same path must join
to the canonical dependency `TaskBoardCardResult` artifact ref and adopt the
current physical readback. A model-repeated manifest or file-ref projection is
not a new write edge and must never trigger another artifact-body draft.

Record the repair target as one current host-issued carrier identity: carrier
id plus normalized locator and content/snapshot version for a file, or carrier
id plus bounded digest for an inline value. A repair loop must not switch to a
different carrier or historical version unless an explicit host-owned
replacement edge creates a new current inventory version and rebuilds every
downstream contract. Otherwise mark the run invalid even if a later carrier
passes.

Show validation of the terminal-verifier response and any structured patch as
host-owned nodes. Trace exact offered criterion ids, request-local claim keys,
and evidence reference ids into validation, then trace deterministic lookup of
the canonical carrier id, exact quote, path, and content version. Unknown or
duplicate keys, missing/duplicate joins, stale versions, or incomplete patch
coverage fail closed; do not discard invalid checks, reinterpret prose, or
continue with an empty projection.

Show one model-visible selection domain per returned field. The exact
`evidence_ledger.items[].reference_id` snapshot visible to the model must be
the exact set accepted in returned `evidence_ids`.
`material_claim_candidates[].claim_key` is the exact set accepted in returned
material checks. Candidate, delivery, and readback locators plus trusted
artifact indexes expose no competing selection ids and have no value edge into
either returned key domain. Execution and cumulative evidence summaries must
also strip evidence selection ids; a non-returnable Action call correlation id
may remain when it distinguishes inspection facts. Also trace `omitted_count` to eligible grounding
records only. A filtered carrier reference counted as omitted grounding
evidence is an invalid projection even when the offered item list is correct.
Finalizer-authored `evidence_use` may be joined host-side to pin canonical
ledger records, but it must not be copied into the terminal verifier's
`execution_result` as another model-visible selection-id domain. When a
required Workspace deliverable path exists, draw exactly one current Workspace
carrier edge from that path's physical readback; intermediate working files
remain cold evidence even when they are otherwise trusted.

For every TaskBoard Action card, trace the command-lowering edge explicitly:

```text
TaskBoard plan card.requires_capability_ids / action_commands
  -> host precedence normalization: non-empty exact action_commands override a
     conflicting generic allowed_execution_shape hint; preserve the conflict as diagnostics
  -> host Action-registry validation and required_action_ids projection
  -> zero-request direct ActionRuntime dispatch when kwargs are complete
     OR one narrow ModelRequest(action_commands only) when upstream values are required
  -> host command/schema validation
  -> direct ActionRuntime dispatch
  -> canonical action.started/completed/failed evidence
  -> card result / downstream evidence edge
```

Do not label a generic AgentExecution/ActionLoop as the TaskBoard Action owner
when the card already carries complete commands. The open-ended ActionLoop is
appropriate only when later Action selection genuinely depends on earlier
Action results. A known Action id with unresolved upstream arguments owns one
narrow request, not a post-Action planning loop. Show `requires_capability_ids`
entering the exact execution scope; if it remains only preflight metadata, mark
the value edge as lost. Unknown ids, omitted required ids, invalid inputs, or
unavailable Actions must fail closed. Exact final Workspace artifact handoff
must show the source content-version edge plus direct write/readback Action
events, not a model request that copies the file body.

Apply the same value/event audit to Flat AgentTask action steps:

```text
Flat planner.required_action_ids
  -> host lookup of only those authoritative Action schemas
  -> one narrow ModelRequest(action_commands only)
     OR zero requests when a trusted internal plan already carries complete commands
  -> host command/schema validation
  -> dependency-ordered serial ActionRuntime dispatch
  -> canonical action.started/completed/failed evidence
  -> Flat observation / terminal evidence edge
```

The compact planner capability list is selection context, not an authoritative
kwargs contract. Do not ask the planner to reproduce strict Action inputs from
that compact projection. Unknown or unavailable required Actions fail closed
before the narrow command request. A Flat step may retain ActionLoop only when
required Action ids are genuinely unresolved and later selection depends on
earlier Action results. Draw the command-order edges inside the Flat batch when
write/read or other intra-step dependencies exist; do not represent a dependent
batch as parallel fan-out.

## TriggerFlow Coverage

For a complex TriggerFlow run, include all of these when present:

- for AgentTask, the outer `lifecycle.start`, `context.prepare`, `work.plan`,
  `work.execute`, `outputs.materialize`, `evidence.ingest`, `terminal.verify`,
  and `transition.decide` nodes;
- for each AgentTask stage signal, `task_id`, monotonic `state_version`,
  `frame_id`, `iteration`, and the applicable `plan_id`, `work_result_id`, or
  `evidence_ref`; reject body-bearing signal payloads, stale versions, and
  cross-task joins;
- terminal-stage direct edges to `transition.decide`, including which
  unexecuted phases were skipped, and TaskBoard as a nested work producer inside
  `work.execute` rather than a second terminal lifecycle;
- for TaskBoard, the actual outer value/signal chain from its structured work
  result through `outputs.materialize`, `evidence.ingest`, `terminal.verify`,
  and `transition.decide`; declared-but-unexecuted outer nodes are invalid;
- start input, chunk continuations, `.to(...)` edges, and `when(...)` joins;
- every emitted signal, payload schema, correlation scope, and consuming chunk;
- fan-out branches and the exact values accumulated by fan-in/join;
- execution state reads/writes, distinguishing replacement from accumulation;
- ModelRequest prompt/output contracts inside chunks;
- Action inputs/results and success/failure RuntimeEvents;
- Workspace writes, trusted refs, readbacks, and content versions;
- subflow start/result/interrupt propagation;
- external wait, ExecutionExchange, interrupt, resume request, and actor data;
- retry/replay/repair back edges and their stable convergence subject;
- for terminal-verifier output-contract correction, the verifier-only back edge
  `transition.decide -> terminal.verify`, the immutable frame/reference
  snapshot it reuses, and proof that work/materialization/evidence and business
  artifact repair were not re-entered; normalize all response-join sections to
  one stable protocol subject, merge every invalid section requirement into the
  transmitted repair contract, include the current offered identity sets, reuse
  the prepared final candidate without another finalizer request, and stop on
  occurrence three;
- terminal result, close snapshot, pending tasks/interrupts, and stream stop.

For every business block, connect the outer flow topology to its internal call
topology. Show which inbound signal activates the block, which exact input/state
fields feed each internal ModelRequest or Action, which parsed fields or Action
facts reconstruct the block output, which state writes occur, and which emitted
signal payload activates each successor or join. A block-level success signal
does not prove that its declared business output was present, and a valid
business output does not prove that the successor signal was emitted.

When a repair flow deliberately replaces a generic Action-capable branch with a
host-owned control request, show that policy choice explicitly: the TriggerFlow
or Blocks node still receives and emits its declared signals, the ModelRequest
node returns only its control schema, the host validation node owns the
side-effect edge, and the absent AgentExecution/ActionRuntime branch is marked
as intentionally unreachable rather than mistaken for missing instrumentation.

Do not infer a value edge from TriggerFlow graph adjacency. Graph wiring proves
which signal can activate a chunk; the payload/state/ref contract proves what
information the chunk receives.

## Diagram Contract

The diagram and edge ledger are one evaluation artifact. Every request block in
the diagram must show, at minimum:

```text
request/stage key
trigger: <event or caller>
prompt.input: <field:type/source/...>
prompt.info: <authoritative contract keys>
prompt.instruct: <material rules or protected ref>
output schema: <field:type/required/constraints>
actual output: <present/missing/invalid fields>
lifecycle: <terminal event state>
```

Every TriggerFlow/business block must show its inbound signal and payload schema,
business input schema, state reads, owned calls, business output schema, state
writes, emitted signal and payload schemas, and terminal or continuation
behavior. Split the visual into overview and detail diagrams when full node
contracts would make one graph unreadable; never drop the edge ledger or the
cross-level edges between a block and its internal requests/Actions.

Use distinct, labeled edge forms for values and signals/events. Mermaid line
style is presentation only; the edge label and ledger remain authoritative.

## Evaluation Procedure

1. Enumerate owners and actual request/block instances from RuntimeEvents and
   flow definitions.
2. Reconstruct every node from `prompt.built`, output schema, parsed result,
   state/ref records, and lifecycle events.
3. Build event/signal edges from emitted and consumed events.
4. Build value edges field by field from output/state/payload to downstream
   input/state, including all host transforms and identity/version joins.
5. For TriggerFlow/business blocks, reconcile the outer signal topology with
   every internal request/Action value topology and prove both directions of
   each block boundary.
6. Trace carrier selection, artifact promotion, current inventory replacement,
   the single terminal-verifier request, host validation, repair identity, and
   terminal projection without allowing implicit carrier switching or
   cross-carrier copying.
7. Compare the observed topology with the declared dependency and output
   contracts. Mark unknown edges explicitly; do not guess them from prose.
8. Inspect bounded business content only on failed or ambiguous value edges.
9. Classify the owner: prompt/output contract, host mapping/projection,
   identity/version join, TriggerFlow signal/state wiring, provider/parse
   lifecycle, business model judgment, source input, or instrumentation.

## Verdict Standard

- `valid`: every required field and signal has a proven source, compatible
  schema, correct identity/version join, intended consumer, and clean required
  lifecycle.
- `invalid`: a required value or signal is missing, stale, misjoined, filtered,
  overwritten, schema-incompatible, or consumed by the wrong owner.
- `provider-invalidated`: provider, parse, retry, cancellation, or terminal
  lifecycle failure prevents a clean comparison.
- `instrumentation-incomplete`: the run may be correct, but the available
  events cannot prove a required edge.
- `semantic-failure`: topology and transfer are valid, but a model-owned
  selection, judgment, plan, or generated value is wrong.

Do not report a run as passed because the final prose looks correct when a
required edge is invalid or unprovable. Conversely, do not blame prompt content
when the topology shows that the correct structured field never reached the
consumer.
