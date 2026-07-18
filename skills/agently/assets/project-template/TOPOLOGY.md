# Planned Application Topology

This file plans the stable application topology before mapping it into project
files. Logical nodes are not required to become one file each. The project uses
the smallest physical boundary that has a real owner, lifecycle, policy, or
independently tested contract.

## Owner and Invariant Ledger

| Owner | Responsibility | Invariant |
|---|---|---|
| `app.py` | Load settings for the command-line process and call one application entry point | No Prompt, business-stage, topology, or trace implementation |
| `prompts/` | Authoritative ModelRequest `input`, `info`, `instruct`, and `output` contracts | Every output field has a declared consumer and field-level description |
| `workflows/chunks/` | One observable model or host-owned business stage | Reads declared inputs/resources, returns plain data, and writes only cross-stage state it owns |
| `workflows/main_flow.py` | Stable TriggerFlow graph, execution lifecycle, runtime resources, and global execution concurrency | Developer-owned topology is inspectable and one run's data stays in execution state |
| `utils/metrics.py` | Host-owned deterministic metric reads and validation | Model output cannot invent a metric, period, snapshot, or canonical evidence record |
| `trace_log.py` | Bounded business facts and an allowlist of framework events | Trace records facts; it does not judge semantic quality or copy full prompts/deltas |
| `services/contracts.py` | Approved public request/result projection shared by inbound transports | Raw events, internal metadata, and unrelated identities never cross the public boundary |
| `services/api.py` | FastAPI admission and HTTP projection | Transport code calls `run_analysis(...)` directly and owns no business stage |
| `services/mcp_server.py` | FastMCP tool admission and MCP result projection | Server exposure is separate from Agently Action-owned MCP client consumption |

The stable graph is written in trusted source code, so TriggerFlow owns it.
Submitted or model-generated DAG data would instead be validated and executed
through TaskDAG / Dynamic Task; it must not be compiled directly into a new
TriggerFlow definition.

## Planned Node Ledger

| Node | Owner | Input contract | Output contract | Lifecycle / failure |
|---|---|---|---|---|
| CLI/API/MCP admission | host transport | non-empty `question`; `max_concurrency` in `1..4` | host-issued `task_id`, task-local output path | Reject invalid input before starting a run |
| `plan_analysis` | ModelRequest chunk | question plus host-owned metric catalog | `normalized_question`; non-empty `analysis_tasks[]` with unique `analysis_id`, offered metric, and offered periods | Parser/request failure ends the execution; host validates ids and membership |
| `for_each` | TriggerFlow | `analysis_tasks[]` | one item per independent task | Local fan-out cap is 4; execution concurrency can lower total in-flight work |
| `load_metric_facts` | host deterministic chunk | trusted analysis key, metric, periods, metrics resource | canonical evidence record with `evidence_id`, facts, and snapshot id | Unknown metric/period fails closed; no model owns the lookup |
| evidence join | TriggerFlow | completed evidence items | ordered `evidence[]` | A failed item cancels the joined path instead of emitting partial final truth |
| `compose_answer` | ModelRequest chunk | question, evidence records, offered evidence ids | non-empty answer and selected evidence ids | Host rejects unknown evidence ids before the result is public |
| public projection | host contract | completed run mapping | task id, execution id, completed status, answer, evidence ids | Raw events and internal metadata stay in the task-local artifact |

## Planned Edge Ledger

| Source field / signal | Transform or validation | Consumer |
|---|---|---|
| admission `question` | trim/non-empty validation | `plan_analysis.input.question` and execution state `question` |
| metric catalog | host read from `resources/metrics.json` | `plan_analysis.info.metric_catalog` |
| `plan_analysis.analysis_tasks[]` | non-empty, unique trusted `analysis_id`, offered metric/period validation | TriggerFlow `for_each` item input |
| each task's `metric` and `periods` | exact host lookup | `load_metric_facts` evidence record |
| evidence records | TriggerFlow join | `compose_answer.input.evidence` |
| evidence `evidence_id` values | offered-set construction | `compose_answer.info.evidence_ids` |
| `compose_answer.evidence_ids[]` | offered-set membership validation | public `evidence_ids` and later UI citation rendering |
| `compose_answer.answer` | non-empty validation | public `answer` |
| execution/chunk/model RuntimeEvents | execution-id/root-run correlation plus allowlist | bounded trace artifact only |
| successful run mapping | public projection | CLI display, FastAPI response, or FastMCP tool result |

`instant` structured updates are not consumed in this example, so each
ModelRequest awaits its final structured result directly. Adding a no-op stream
drain would create work without a consumer. If a UI later consumes provisional
updates, it must correlate them to an attempt and invalidate them when that
attempt fails or is replaced.

## Production-Necessity Ledger

| Produced value or node | Consumer / quality role | Keep? |
|---|---|---|
| `normalized_question` | Stored in the analysis plan for audit/readback of the model's bounded interpretation | Yes |
| `analysis_tasks[]` | Drives TriggerFlow fan-out and deterministic evidence acquisition | Yes |
| `analysis_id` | One model-returned trusted selection key used to join evidence; other identity is reconstructed by the host | Yes |
| metric facts and snapshot id | Consumed by the answer request and retained as audit evidence | Yes |
| final answer | CLI/API/MCP user output | Yes |
| final evidence ids | Host-validatable citation projection for downstream rendering | Yes |
| bounded trace events | Operational readback and later evaluation | Yes |
| hidden reasoning / generic `thinking` field | No declared consumer or bounded semantic role | No; prohibited |
| application-local MCP client forwarding module | Only forwards to Agently's existing Action-owned MCP client surface | No; redundant |
| business `Service` wrapper around `run_analysis()` | No policy, state, lifecycle, or alternate implementation | No; transports call the application owner directly |

The `actions/` and local `skills/` packages are optional capability probes in
this full reference asset and have direct tests. Delete them when a copied
project does not register those capabilities. A one-request project should
start from `app.py`, `SETTINGS.yaml`, its Prompt, and tests rather than copying
this entire tree.

## Observed-Topology Check

After a representative run, compare this plan with:

- TriggerFlow Mermaid output for stable node and fan-out/join structure;
- the saved run and business events for field-level value lineage;
- allowlisted RuntimeEvents for execution/chunk/ModelRequest lifecycle;
- final artifact readback for answer and evidence identity;
- observed request counts, elapsed time, and provider telemetry when available.

Runtime observation validates the planned topology. It does not replace the
owner, consumer, and failure decisions recorded above.
