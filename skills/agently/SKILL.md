---
name: agently
description: Use when the user wants to build, initialize, validate, optimize, or refactor a model-powered assistant, internal tool, automation, evaluator, or workflow from a business scenario or common problem statement, and the correct Agently owner layer is still unclear. The user does not need to mention Agently.
---

# Agently

Start here when the request is expressed as product behavior, a business
scenario, an architecture/refactor goal, or a broad model-application problem.
Choose the owner layer before selecting APIs.

Generic asks are scenario-led; a request does not need to mention Agently explicitly.

When Agently use is explicit and the user is designing, optimizing, or reviewing
a solution, workflow/block, or Prompt, route through `agently-design` for the
request inventory and `agently-request` for selected Prompt details, using the
collaborative confirm-and-revise method by default.

## Workflow

1. Reduce the request to scenario, atomic goals, inputs, outputs, side effects,
   evidence, and lifecycle needs.
2. Separate model-owned semantic decisions from host-owned deterministic
   validation and effects.
3. Choose the narrowest native owner and record the value/event topology for
   every non-trivial flow.
4. Define the exact model request contracts and host-issued identity keys.
5. Map context sources, file space, durable records, permissions, retries,
   pressure controls, and observation to their owners.
6. Implement async-first, test the owned protocol deterministically, then run
   the smallest representative real-model check for model-owned behavior.
   Classify acceptance criticality (hard gate or soft target) separately from
   evaluation method (deterministic check or semantic review).
7. If the framework lacks the right seam, report the architecture gap instead
   of hiding it behind business-specific glue.

## Route by Owner

- One request family: model setup, prompt, structured output, response,
  session memory, embeddings, knowledge retrieval -> `agently-request`.
- Actions, MCP, ExecutionResource, task files, durable records, service APIs,
  RuntimeEvent, or DevTools -> `agently-runtime`.
- Stage task lifetime, sync/async call bridging, loop-neutral handles,
  settlement, replay channels, or local listeners -> `agently-stage`.
- Multi-owner architecture, topology, evidence/identity boundaries, lifecycle,
  pressure, or information-loss review -> `agently-design`.
- Branching, concurrency, approval, wait/resume, retry, visible multi-stage
  execution, or restart-safe orchestration -> `agently-triggerflow`.
- Model-generated or application-submitted acyclic task graphs ->
  `agently-dynamic-task`.
- Migration from LangChain, LangGraph, LlamaIndex, CrewAI, or similar systems ->
  `agently-migration`.

## Read by Need

- Layer selection and repository shape: `references/capability-map.md` and
  `references/project-framework.md`.
- TaskContext, ContextReader, TaskWorkspace, RecordStore, SkillLibrary, and the
  SkillsExecutor compatibility facade: `references/context-and-skills.md`.
- Model/application topology and evidence consumption:
  `references/execution-topology-validation.md`.
- Simulation-first and real-model validation:
  `references/model-quality-validation.md`.

## Model and Host Ownership

Model-owned work includes prose-derived intent, scenario recognition, semantic
routing, relevance, planning, natural-language generation, ambiguity,
tradeoffs, and quality judgment. Use Agently ModelRequest structured output for
these decisions.

Host-owned work includes schema/type/enum validation, offered-key membership,
exact arithmetic/filtering, authorization, hard policy, lifecycle state,
identity reconstruction, and side effects. Hybrid decisions let the model
return a bounded enum/key/plan and let the host validate and execute it.

Model participation does not by itself justify another request. Split requests
only when decision, context/evidence, output consumer, authorization/model
settings, retry/repair, lifecycle, or parallelism needs an independent boundary.

Never use keyword tables, tokenization, substring/regex language patterns, or
hand-written scorecards as the semantic owner for intent, route, Skill
relevance, evidence usefulness, quality, or business acceptance.

## ModelRequest Contract

When model output must satisfy an API or downstream interface:

- put runtime facts in `.input(...)`;
- put authoritative schemas, signatures, docs, and source facts in `.info(...)`;
- put transformation and call rules in `.instruct(...)`;
- put the exact machine-consumable contract in `.output(...)`.

Describe every consumed field: type, semantics, requiredness, enum/format/range,
nullability, and cross-field constraints. Validate deterministically before a
real side effect.

Do not request or preserve hidden chain-of-thought. Bounded process fields are
allowed only when they have a named semantic role, evidence boundary, type and
bounds, consumer, visibility, retention, and failure behavior.

## Identity and Evidence

When a model selects or judges host records, project one host-issued trusted selection key
plus only task-relevant facts. Declare it as a required string constrained to the offered key set.
The key is an application-local projection: do not ask the model to reproduce UUIDs or
identity-heavy objects. Validate it, then reconstruct UUIDs, metadata, and other identifiers deterministically
in host code.

A selection's offered-set membership proves membership, not freshness. If a
selection can cross a cache, queue, retry, persistence, or replay boundary,
bind it to a Host-owned request/execution revision or issue per-request opaque
keys, and validate Host correlation before canonical lookup. That binding must
cover the semantic input/evidence/request revision, not only candidate or
catalog state. A caller-supplied logical ID is insufficient unless Host storage
guarantees its unique association with that semantic revision. Prefer
non-overridable per-semantic-request lineage or a Host-owned canonical
input/evidence revision. Prefer Host-bound lineage over asking the model to copy
another request id; the model must not copy correlation ids. A strictly inline
awaited response that cannot cross a request boundary needs no extra
model-returned correlation field.

Evidence must have a source, state, bounded body/ref, and consumer. Search hits,
snippets, candidate artifacts, model claims, and verifier prose are not
automatically completion proof. Preserve raw facts cold and give model-hot
consumers only the bounded projection they need.

For retrieval-backed answers, expose short trusted `ref_id` values and ask for
`[[ref:<ref_id>]]`. Validate tokens host-side, render approved labels/links, and
keep raw URLs and metadata out of model transcription.

## Context, Files, Records, and Skills

- `TaskContext` is the sole task-information aggregate. It owns revisioned
  source bindings/direct entries and creates or restores its read handles.
- `ContextReader` is a public consumer/phase-bound handle, not an independent
  owner. It accepts a read intent, advances private source windows only after
  successful reads, and returns an immutable `ContextPackage` with bounded
  source coverage but no cursor.
- `TaskWorkspace` owns task files and artifacts only.
- `RecordStore` owns durable records, retrieval, links, RuntimeEvents,
  checkpoints, snapshots, leases, and durable refs.
- `SkillLibrary` owns immutable installed real-world Skill revisions.
- `AgentExecution` binds Skills, builds/reads TaskContext, selects the route,
  executes, and exposes results/streams.
- `AgentTask` owns long-task planning, evidence, verification, repair, and
  terminal acceptance.

Do not recreate the removed generic Workspace, ContextBuilder, SkillsManager,
Skills route/strategy owner, `skill_activation`, or `workspace_operation`.
`Agently.skills_executor` is a thin management/integration compatibility facade,
not an execution engine.

## Execution Selection

- Use ModelRequest for one model interaction without application-owned
  lifecycle orchestration.
- Use ActionRuntime for model-callable operations; use ExecutionResource for
  live dependency lifecycle.
- Use Agently-Stage for process-local task lifetime and call-shape bridging.
  Do not treat it as a workflow, event, persistence, or policy owner.
- Use a fresh `agent.create_execution()` for one bounded Agent run with
  reusable result/text/meta/stream readers.
- Use `agent.create_task(...)` when the model should own a long task's planning,
  bounded work, evidence, verification, and replan loop. It returns an
  AgentExecution draft, not a public AgentTask handle.
- For an interface user's free-form "continue" request, let a structured
  ModelRequest choose resume, new task, or clarification from host-offered
  resumable candidates; keep authorization, lifecycle state, key validation,
  and dispatch host-owned. Route the full design to `agently-design`.
- Use TriggerFlow for framework-visible progression, branching, concurrency,
  retry, approval, pause/resume, intervention, or signal-network behavior.
- Use TaskDAG/DynamicTask for untrusted model-generated or app-submitted DAG
  data. Validate and resolve it before it reaches TriggerFlow.

Blocks are an internal lowering bridge, not a public task lifecycle or semantic
owner. Ordinary TaskDAG execution compiles directly to TriggerFlow unless the
caller explicitly needs Blocks lifecycle evidence.

## Topology Gate

For every non-trivial linear, branching, concurrent, or looped application,
record:

- an owner/invariant ledger;
- a planned request/chunk/action node ledger;
- a value/event edge ledger with exact consumers;
- a production-necessity ledger for every node and artifact.

Map each model-produced field to a same-response consumer, later request, host
operation, or useful user projection. Remove unconsumed fields and requests.
Do not classify an ordered same-response field as unused merely because host
code discards it after later fields have consumed it.

## Concurrency and Lifecycle

Map real dependencies before coding. Run independent work concurrently with
explicit bounds; keep serial execution only for data dependency, ordering,
side-effect safety, or external capacity constraints.

Apply pressure controls at the owning layer: host admission/in-flight limits,
TriggerFlow execution/fan-out limits, model scheduler concurrency/rate limits,
and worker/thread-pool sizes for blocking code.

Treat `instant` values as provisional. They may update UI or start explicitly
cancelable/idempotent preparation; irreversible work waits for final parsed
output and host validation. If no consumer needs progressive output, await the
final result directly instead of draining a stream into a no-op loop.

Use hidden flow sugar only for finite self-closing runs. Pause/resume, external
emit, save/load, inspection, cancellation, intervention, or host-controlled
close requires an explicit execution handle.

## Project Structure

Keep business/execution policy independent from storage, UI, transport,
providers, DevTools, and framework glue. Prefer deep modules with small stable
interfaces and inward-pointing dependencies.

Start a one-request application with only its composition entry, settings,
Prompt contract, and tests. Add `workflows/` plus `TOPOLOGY.md` only for a real
stable multi-stage graph; add `services/` only for an actual inbound transport;
add Actions, local Skills, utilities, or resources only when the application has
that owner and a current consumer. Planning nodes do not map one-to-one to
files. See `references/project-framework.md` and its runnable project asset.

Minimize the cross-file lookup count and nesting depth needed by people and
coding agents. Do not split one-use information into extra files, constants,
helpers, classes, or wrappers unless the boundary has actual reuse value or an
independently owned contract.

Before adding a facade, manager, executor, adapter, alias, or protocol, identify
the current owner and prove the missing boundary. Do not add shallow pass-through
layers. If a cleaner owner becomes visible mid-implementation, stop and correct
the architecture instead of completing the convenient local patch.

## Validation

Deterministic tests may prove schemas, identities, lifecycle transitions,
accounting, file/record effects, safety, and protocol presence. They may not
stand in for model-owned semantic quality.

For model behavior:

1. define written acceptance criteria;
2. run a labeled realistic warm simulation without target-provider calls;
3. use at most one isolated cold carrier when available and authorized;
4. run the smallest bounded real-model case with authorized developer/project
   credentials;
5. record raw facts, request/tool counts, timings, sizes, artifacts, readback,
   limitations, and judgment separately.

Real traces override simulation. Do not invent provider ids, usage, billing,
cache, latency, or finish telemetry; label simulated/synthetic/estimated/
replayed/unavailable/observed values precisely.

## Anti-Patterns

- Inventing custom retry, parser, orchestration, context, or storage managers
  before checking native owners.
- All-serial design without dependency analysis.
- Deterministic business mappings, canned outputs, overfitted prompts, hidden
  expected-answer fixtures, or test-only production branches.
- Treating effort/resource limits as proof of strategy quality.
- Letting a runner's pass/fail flag replace direct artifact/trace inspection.
- Duplicating full source, Skill, record, or artifact bodies into every prompt.
- Treating Workspace, SkillsExecutor, Blocks, DevTools, or transport as a broad
  application policy owner.
- Copying a full scaffold into a one-request project, retaining empty packages,
  or creating one file per planned topology node.
