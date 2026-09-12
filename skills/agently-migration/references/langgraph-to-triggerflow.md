# LangGraph to TriggerFlow

Use this map when the source relies on LangGraph's application-owned graph,
state, persistence, interrupts, streaming, or subgraphs.

## Verify the Source Contract

Inspect the installed LangGraph version and the features actually used. Current
official references include:

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [Streaming](https://docs.langchain.com/oss/python/langgraph/streaming)
- [Subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)

## Source-to-Owner Map

| LangGraph source | Agently target | Preserve |
|---|---|---|
| `StateGraph` node | TriggerFlow chunk or a small group of chunks | Input/output contract, side effects, retry and error boundary. |
| Static/conditional edge | TriggerFlow signal edge and host-validated condition or ModelRequest enum | Ordering, branch exclusivity/fan-out, and unreachable behavior. |
| Reducer/channel state | Per-execution state plus explicit merge owner | Initial value, merge law, ordering, concurrent-update behavior. |
| Graph input/output schema | TriggerFlow start/close contract | Required fields, type validation, and public projection. |
| Checkpointer/thread/checkpoint | Explicit TriggerFlow execution save/load with configured snapshot store/RecordStore | Execution identity, durable revision, resume point, pending writes, and failure semantics. |
| `interrupt()` / `Command(resume=...)` | Explicit execution pause/resume or ExecutionExchange boundary | Public prompt/payload, authorization, correlation, idempotency, and resume validation. |
| `stream` / `astream` modes | TriggerFlow runtime stream and, separately, ModelRequest delta/instant streams | Event kind, namespace/lineage, ordering, replay, and terminal item. |
| Subgraph | TriggerFlow subflow or a separately owned child flow | Input/output projection, state isolation, identity, close/cancel propagation, persistence scope. |
| Tool/model node | ActionRuntime or ModelRequest inside the owning chunk | Tool schema/evidence and request contract; graph does not absorb those owners. |

## State and Recovery

Never map LangGraph state to TriggerFlow `flow_data` by default. `flow_data` is
shared by a flow object across executions and is not concurrency-safe per-run
state. Put run-local values in execution state.

`execution.save()` serializes a copy of flow-shared data and `load()` replaces
the current flow object's shared value with it; this does not make `flow_data`
execution-local. Persist live-resource descriptors only, then reconstruct
clients through ExecutionResource providers.

Compare recovery with a process restart, not only in-memory pause/resume. Verify
the exact resume identity, state revision, completed-node reuse, pending side
effects, and terminal result. If the source checkpointer provides semantics the
configured Agently store cannot preserve, report that storage/provider gap.

## Interrupts and Side Effects

LangGraph documents that an interrupted node may restart from its beginning on
resume. Inventory every side effect before an interrupt and preserve its
idempotency/compensation rule in the target. External resume payloads require a
host-owned execution identity and authorization check; model output must not
copy the correlation id.

Use an explicit TriggerFlow execution whenever the host must pause/resume,
emit externally, save/load, inspect, cancel, or control close. Hidden
`flow.start(...)` sugar is only for finite self-closing runs.

## Streaming and Subflows

Separate three contracts that LangGraph may expose together:

1. model token/structured-field progress;
2. workflow node/state/runtime events;
3. final graph output.

Map them to ModelRequest streams, TriggerFlow runtime stream, and close result
respectively. Preserve event lineage and ordering required by consumers; do
not parse printable text to reconstruct workflow state.

For subgraphs, test parent/child cancellation, error propagation, state
projection, snapshot identity, and close ordering. Do not flatten a stateful or
interruptible subgraph into an opaque function solely to reduce node count.

## Minimum Comparison

Run representative cases for the happy path, each branch, concurrent join,
interrupt/resume, restart recovery, node failure/retry, cancellation, and
subgraph failure. Compare state transitions and event traces as well as final
values. Preserve only source semantics the application actually consumes; do
not recreate unused LangGraph mechanics for visual similarity.
