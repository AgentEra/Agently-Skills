# Project Framework

Use this reference to initialize or refactor an Agently project without turning
logical stages into a fixed directory tree. Plan the real owner and consumer
topology first, then create the smallest physical layout that carries it.

The runnable full-stack reference is
[`../assets/full-stack-reference/`](../assets/full-stack-reference/). Copy it
selectively: it demonstrates many optional boundaries at once and is not a
default template or mandatory scaffold for a small application.

## Topology Before Files

For every non-trivial linear, branching, concurrent, or looped model
application, write four ledgers before creating modules:

1. **Owner and invariant ledger** — which model, host, Action, flow, storage,
   transport, or human owner makes each decision and what must remain true.
2. **Planned node ledger** — each logical ModelRequest or host stage, its input,
   exact output schema, context/evidence, lifecycle, and split reason.
3. **Planned edge ledger** — every value, state, signal, effect, and user
   projection, with its exact producer, transform/validation, and consumer.
4. **Production-necessity ledger** — why each node and field exists, who
   consumes it, its visibility/retention, failure behavior, and whether a
   claimed quality benefit is hypothetical, observed, or A/B verified.

A planned node is not automatically a file. Several small host validations may
belong beside one owning Chunk; one reusable external adapter may deserve a
module. Use the owner boundary, not the diagram box count, to choose files.

Runtime Mermaid graphs, RuntimeEvents, traces, and artifacts validate the plan.
They do not replace it: adjacency proves activation, not field-level value
transfer or production necessity.

For a key edge with an independent consumer, parallel-development benefit, or
local-validation value, consider small replaceable reference data so downstream
work can proceed before the real producer is complete. Keep the form
project-defined: a DTO, structured example, JSON fixture, event payload, file
artifact, or domain case plus topology data can all fit. Model-generated drafts
remain simulated until confirmed, and the finished producer must prove its real
output can replace the reference data. Do not add a universal packet, required
field list, file, or handoff layer where no independent value exists.

## Choose Model Participation Before Request Count

Use models for prose-derived intent, semantic routing, relevance, planning,
tradeoffs, natural-language responses, and quality judgment. Use host code for
schema/type/enum validation, trusted-key membership, exact arithmetic,
authorization, hard policy, lifecycle state, canonical identity joins, and
side effects.

Model participation does not imply a separate ModelRequest for every semantic
step. Split only when decision, context/evidence, output consumer,
authorization/model settings, retry/repair, lifecycle, or parallelism requires
an independent boundary. Keep one ordered request when later fields consume an
earlier bounded field under the same boundary.

Never request or store hidden chain-of-thought. A bounded task-specific process
field is allowed only when its semantic role, evidence boundary, type and
bounds, consumer, visibility, retention, failure behavior, and quality-evidence
status are explicit. A generic unconsumed `reasoning`, `analysis`, or `thinking`
field is not a quality mechanism.

## Start From the Minimum Shape

### One request family

```text
project/
├── app.py
├── SETTINGS.yaml
├── prompts/
│   └── request.yaml
└── tests/
```

The Python request owner may stay in `app.py` when it is small and has one
consumer. Add a request module only when it owns a reusable Prompt/output
contract or meaningful validation. Do not add TriggerFlow, `services/`,
`domain/`, `tools/`, or empty packages for appearance.

### Stable multi-stage workflow

Add only the owners the topology proves:

```text
project/
├── app.py
├── SETTINGS.yaml
├── TOPOLOGY.md
├── prompts/
├── workflows/
│   ├── main_flow.py
│   └── chunks/
└── tests/
```

Developer-owned stable topology belongs to TriggerFlow. Keep graph and
execution lifecycle in `main_flow.py`; put one independently observable
business stage in each justified Chunk. Do not add a separate join Chunk when
`for_each(...).end_for_each()` already returns the joined list and no additional
transformation or policy exists.

### Submitted or model-generated DAG

TaskDAG is a low-frequency advanced option when the plan itself is runtime
data. Read `task-dag.md` before adding it:

```text
project/
├── app.py
├── SETTINGS.yaml
├── task_dag/
│   ├── contracts.py
│   ├── handlers.py
│   └── runtime.py
└── tests/
```

The directory name is optional; the ownership is not. Do not introduce this
shape for an ordinary Agent task or a stable developer-owned workflow. When it
is justified, validate and resolve the submitted DAG through TaskDAG, then let
`TaskDAGExecutor.async_run(...)` use the TriggerFlow substrate. Do not compile
unvalidated plan data into a new TriggerFlow definition. Blocks is opt-in only
when Blocks lifecycle evidence or `ExecutionBlockGraph` output is explicitly
required.

### Inbound service delivery

Add `services/` only when the project actually exposes an external transport:

```text
services/
├── contracts.py     # shared approved public projection, if two transports use it
├── api.py           # FastAPI inbound adapter
└── mcp_server.py    # FastMCP server adapter
```

Use direct FastAPI for an ordinary typed HTTP API and FastMCP for an MCP server.
Both adapters should validate admission, issue host identity, call the same
async application entry point, and project only approved public fields:

```python
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]


@app.post("/analysis", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    task_id = f"analysis-{uuid4().hex}"
    run = await run_analysis(
        request.question,
        task_id=task_id,
        metrics_path=ROOT / "resources/metrics.json",
        output_directory=ROOT / "outputs" / task_id,
        max_concurrency=request.max_concurrency,
    )
    return project_analysis_run(task_id, run)


@mcp.tool
async def analyze_with_mcp(
    question: str,
    max_concurrency: int = 4,
) -> dict[str, object]:
    request = AnalysisRequest(
        question=question,
        max_concurrency=max_concurrency,
    )
    task_id = f"analysis-{uuid4().hex}"
    run = await run_analysis(
        request.question,
        task_id=task_id,
        metrics_path=ROOT / "resources/metrics.json",
        output_directory=ROOT / "outputs" / task_id,
        max_concurrency=request.max_concurrency,
    )
    return project_analysis_run(task_id, run).model_dump()
```

The full-stack reference includes the complete imports, settings lifespans, task-local
output paths, and in-process transport tests. The abbreviated code above shows
only the ownership relationship.

`FastAPIHelper` remains an available Agently integration when its packaged
task/stream transport is the public contract you want. It is not deprecated,
but it is not the default for a project that needs an ordinary typed FastAPI
route.

MCP client consumption already belongs to Agently Action management. Do not add
an application-local MCP client service or a function that only forwards one
transport object to the Agently MCP registration call.

## Information Locality

Minimize the cross-file lookup count and nesting depth required by people and
coding agents to understand the current behavior. Do not split one-use schemas,
constants, helpers, classes, or wrappers into separate locations unless the new
boundary has actual reuse value or an independently owned/versioned contract.
Formal separation without either benefit is over-design.

## Wrapper Acceptance Test

Before adding a Service, Manager, Factory, repository facade, request wrapper,
or adapter, identify its current consumer and require at least one real owner:

- authorization, validation, policy, or safety;
- state, lifecycle, cleanup, retry/repair, concurrency, or transaction scope;
- a stable external contract or non-trivial representation translation;
- more than one consumer of the exact same owned contract;
- an already released compatibility boundary.

If none applies, inline it. Remove functions that only rename arguments, return
the same object, or forward one owner call unchanged. Delete empty packages,
dead fields, unused output nodes, duplicate facades, and test-only production
branches. Concision is an ownership and consumer property, not a universal file
or line-count limit.

## Prompt and ModelRequest Contracts

Keep stable Prompt contracts in YAML/JSON when they need independent evolution.
The consuming request or Chunk loads them directly; do not add `request_*` or
`service_*` wrappers that only rename `load_yaml_prompt()`.

- `input` holds current runtime facts.
- `info` holds authoritative source facts, API/schema documentation,
  signatures, docstrings, evidence, and offered key sets.
- `instruct` holds transformation and call rules.
- `output` describes the exact machine-consumable shape.

For every downstream-consumed field, specify type, meaning, requiredness,
enum/format/range, nullability, and cross-field constraints. This integration
contract is necessary output control, not business-logic intrusion. Host code
still validates before an external call or side effect.

When a model selects records, expose one host-issued trusted selection key plus
task-relevant facts. Validate the returned key against the offered set and
reconstruct canonical ids, metadata, and records host-side. Do not make the
model copy UUIDs, multiple ids, URLs, or unrelated metadata.

## Utils, Actions, Skills, and Resources

Add these only when the project has the corresponding owner:

| Boundary | Use it for | Do not use it for |
|---|---|---|
| `utils/` | host-only deterministic reads, validation, transformation, or persistence used by real consumers | model-callable capability, generic dumping ground |
| `actions/` | capabilities registered for Agent/model selection, ActionRuntime policy/evidence, MCP access, or controlled sandbox execution | ordinary formatting/database helpers |
| `skills/` | standard local Skill packages or controlled install/materialization entry points | automatic Action mounting, authorization, or workflow strategy |
| `resources/` | actual static project data or templates | generated outputs or hidden state |

The existence of an Action or Skill example does not mean a copied project
needs its directory. Delete optional packages when no application consumer or
capability test remains.

## Async, Concurrency, and Result Consumption

Map ordered, independent, and safely provisional work before implementation.
Run independent work concurrently under explicit bounds. Serial execution is
valid only for data dependency, ordering, side-effect safety, or external
capacity limits.

Place pressure controls with their owners:

- host admission and in-flight coroutine limits;
- TriggerFlow execution concurrency;
- `batch` / `for_each` fan-out caps;
- model scheduler concurrency and rate limits;
- source/client connection pools and timeouts;
- host worker or thread-pool size for blocking code.

Do not describe one worker/thread count as a universal TriggerFlow setting.

If no UI, transport, observer, or next stage consumes progressive output,
await final structured data directly with `async_get_data()`. Do not drain an
`instant` generator into a no-op loop. When `instant` fields have a real
consumer, treat them as provisional and allow only UI updates or explicitly
cancelable/idempotent preparation until final parsing and validation succeed.

## State, Trace, and Evaluation

- Put one TriggerFlow run's data in execution state.
- Use runtime resources for already-created live dependencies.
- Keep durable domain data in the owning host store or RecordStore.
- Treat `flow_data` as shared on the flow object even though save/load copies
  and replaces its serialized value.
- Use explicit execution handles for observation, external emits, pause/resume,
  save/load, intervention, cancellation, or host-controlled close.

For non-trivial flows, record bounded business facts at the stage that owns
them and use an allowlist of RuntimeEvents for framework lifecycle facts. Trace
records facts; Eval judges semantic quality. Do not copy full prompts, deltas,
secrets, or raw metadata into every event.

Attach optional DevTools observation in the integration layer. DevTools may
visualize and store facts; it does not own routing, workflow policy, or semantic
truth.

## Testing and Evidence

Test owned deterministic contracts first:

- settings loading and environment placeholders;
- Prompt/output shape and host field validation;
- TriggerFlow structure, state transfer, fan-out/join, and close behavior;
- TaskDAG validation and handler resolution;
- Action/Skill/resource boundaries when present;
- FastAPI/FastMCP transport projection;
- trace schema and allowlist.

Mocks may prove wiring but not model semantics. For model-owned behavior, define
criteria, run labeled simulation-first preflight, then the smallest authorized
real-model case when executable Prompt or behavior changed. Use a second
structured ModelRequest judge for semantic evaluation rather than keyword,
regex, or fixed-answer tests.

## Framework Internal Module Rules

Inside Agently itself, select the existing public concept, owner layer, and
plugin/provider seam before adding a module. Use subdirectory packages when a
feature has multiple real roles such as facade, registry, resolver, provider,
policy, and validation. Keep a genuinely small single-responsibility capability
in one file. Do not split by arbitrary line count or add pass-through managers.

If application work exposes a missing framework seam, verify the gap against
current code/docs/examples, then prepare a sanitized issue for
<https://github.com/AgentEra/Agently/issues> instead of hiding the gap behind
business-specific glue. Remote filing still requires explicit user approval.

## Final Structure Check

- Does every directory have a current owner and consumer?
- Did the four ledgers precede the physical tree?
- Is stable trusted topology TriggerFlow and runtime DAG data TaskDAG?
- Are model and host responsibilities separated?
- Are concurrent stages bounded at the correct layer?
- Do FastAPI/FastMCP remain inbound adapters over one application entry?
- Is MCP client consumption left to Agently Action management?
- Can any wrapper, node, field, or directory be removed without losing an
  invariant, lifecycle, policy, translation, or stable contract?
