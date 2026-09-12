# CrewAI to Agently

Use this map for CrewAI Agents, Tasks, Crews, Processes, Flows, tools, memory,
or knowledge. Separate autonomous collaboration from application-owned
orchestration before choosing the target.

## Verify the Source Contract

Current CrewAI documentation treats Crews and Flows as different layers. Check
the installed version and the behaviors the application actually consumes:

- [Agents](https://docs.crewai.com/en/concepts/agents)
- [Tasks](https://docs.crewai.com/en/concepts/tasks)
- [Crews](https://docs.crewai.com/en/concepts/crews)
- [Flows](https://docs.crewai.com/en/concepts/flows)
- [Memory](https://docs.crewai.com/en/concepts/memory)

## Source-to-Owner Map

| CrewAI source | Agently target | Preserve |
|---|---|---|
| Agent role/goal/backstory/LLM | Agent definition plus request prompt/model settings | Only role and policy that change requests; provider/model and inheritance boundaries. |
| Tool or MCP integration | ActionRuntime + ExecutionResource/MCP | Input schema, authorization, lifecycle, result evidence, and side effects. |
| Task description/expected output | ModelRequest or AgentExecution prompt and output contract | Inputs, done condition, output schema/Pydantic, guardrails, and context dependencies. |
| Task output passed to a later task | TriggerFlow edge and execution state, or a later ModelRequest after validated handoff | Ordering, typed value, lineage, and failure propagation. |
| Sequential/conditional process | TriggerFlow | Stable order, branches, stop conditions, state, and events. |
| Hierarchical/open-ended Crew planning | AgentTask when the model truly owns bounded planning/delegation/verification | Available capabilities, evidence, bounds, and terminal behavior. |
| Flow `start`/`listen`/`router` | TriggerFlow start, signal edges, and branch conditions | Event fan-out, routing, ordering, and completion. |
| Flow state/persistence/resume | TriggerFlow execution state plus snapshot store/RecordStore | Execution identity, revisions, recovery, and idempotency. |
| Human input/approval | TriggerFlow pause/resume or ExecutionExchange + policy | Prompt/payload, authorization, correlation, timeout, and terminal path. |
| Memory | Session/SessionMemory and RecordStore | Scope, extraction, accepted writes, persistence, and retrieval. |
| Knowledge/source material | ContextSource + TaskContext/ContextReader, optionally backed by RecordStore | Source identity, bounded exact reads, relevance, and citation behavior. |
| Crew/Flow event listener | RuntimeEvent/TriggerFlow runtime stream or a host adapter | Event type, lineage, ordering, redaction, and failure isolation. |

## Do Not Recreate Role Theater

A CrewAI Agent name does not require a separate Agently Agent, class, or model
request. Keep one Agent with request-local roles when all source agents share
the same model/settings, tools, evidence, lifecycle, and consumer and only their
prompt wording differs.

Create a separate Agent or request boundary only when it owns a real difference:
model/provider settings, stable prompt/policy, mounted Actions, evidence/context,
authorization, retry/validation, lifecycle, or parallelism. Preserve user-
visible authorship only when the product consumes it.

## Crew versus Flow

Map a stable application process to TriggerFlow even if CrewAI expressed it as
a Crew. Map open-ended model-owned decomposition/delegation to AgentTask only
when the source genuinely grants that authority. A sequence of fixed Tasks is
not evidence that multiple autonomous agents are required.

For hybrid systems, keep the boundary visible:

```text
TriggerFlow stage
  -> bounded AgentExecution or AgentTask
  -> validated result/evidence
  -> next TriggerFlow stage
```

Do not let a model-produced plan compile directly into trusted application
topology without validation. Do not hide approvals, external waits, or recovery
inside prompt instructions.

## Guardrails, Memory, and Knowledge

Move every non-sensitive model-satisfiable Task guardrail into the initial
request contract, then keep deterministic/Pydantic validation authoritative.
Security and authorization remain host-owned and fail closed.

Separate conversation memory, durable records, workflow state, and task
evidence. Do not copy a CrewAI memory blob into every prompt. Use Session for
conversation projection, RecordStore for durable records, execution state for
progression, and ContextReader for bounded task evidence.

If the source knowledge backend is operationally important, retain it behind a
ContextSource or Action adapter unless storage migration is explicitly in scope.
Preserve source ids and exact readback; do not claim RecordStore equivalence
from a successful final answer.

## Minimum Comparison

Compare at least one representative run for each process/Flow route, plus
tool failure, guardrail rejection, human input, cancellation, and restart when
the source supports them. Inspect model/tool request counts, task handoffs,
state transitions, stream events, memory writes, source refs, and the final
artifact. A final string with similar wording does not prove that Crew/Flow
semantics were preserved.
