# LangChain to Agently

Use this map after confirming that the source behavior is LangChain agent-side
behavior rather than an application-owned LangGraph workflow.

## Verify the Source Contract

Current LangChain documentation distinguishes agents, tools, structured output,
and short-term state. Check the actual installed version and source code rather
than inferring behavior from a class name:

- [Agents](https://docs.langchain.com/oss/python/langchain/agents)
- [Tools](https://docs.langchain.com/oss/python/langchain/tools)
- [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output)
- [Short-term memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)
- [Retrieval](https://docs.langchain.com/oss/python/langchain/retrieval)

LangChain's `create_agent` uses LangGraph internally, but that implementation
fact does not require TriggerFlow when the application only consumes one agent
invocation. Migrate the behavior the application relies on.

## Source-to-Owner Map

| LangChain source | Agently target | Preserve |
|---|---|---|
| Chat model/provider configuration | `agently-request` model settings and model profiles | Provider/model selection, credentials, timeout, retry/failover policy. |
| PromptTemplate, ChatPromptTemplate, messages | `.input/.info/.instruct/.output` or Prompt Configure | Runtime variables, authoritative context, role/message semantics actually consumed. |
| `with_structured_output` or agent `response_format` | `.output(...)`, Pydantic, ensure, and validators | Field types, requiredness, constraints, retry/terminal behavior. |
| `@tool` / BaseTool | `@agent.action_func`, `agent.use_actions(...)`, MCP, or a custom Action executor | Input schema, authorization, timeout, side effects, and observed call results. |
| One `create_agent` tool loop | AgentExecution direct strategy with Actions | Tool-choice loop and final result contract; do not add workflow state solely because LangChain uses a graph internally. |
| Open-ended bounded planning/replan | AgentTask through AgentExecution | Planner authority, evidence requirements, verification, and terminal bounds. |
| Message/state short-term memory | Session / SessionMemory | Conversation scope, trimming/summarization, accepted writes, and isolation. |
| Retriever / vector store / RAG chain | RecordStore or an existing retriever exposed as ContextSource/Action, then ContextReader + ModelRequest synthesis | Filters, scores where meaningful, source identity, exact readback, citation and fallback behavior. |
| Middleware/callbacks/tracing | Agent/ModelRequest extension boundary or RuntimeEvent/DevTools | Ordering, mutation authority, failure behavior, and redaction. |
| Multi-stage application logic outside one invocation | TriggerFlow | Branches, joins, waits, state, events, and restart behavior. |

## Decisions That Need Evidence

### Agent loop versus workflow

Keep one AgentExecution when later tool choice depends on observed tool results
inside the agent loop and the application consumes one terminal result. Use
TriggerFlow when the application itself owns separately inspectable stages,
approvals, parallel branches, external resume, or recovery.

### Retrieval

Do not bulk-copy every LangChain vector-store integration into RecordStore.
When an existing retriever is operationally important, keep it behind a narrow
ContextSource or Action adapter and preserve its filter, tenant, and exact-source
readback contract. Move storage only when the user actually wants storage
migration and representative retrieval quality has been compared.

### Structured output and validation

Move every model-satisfiable business rule into the initial Agently request.
Keep host validation authoritative. Compare invalid-output retry counts and
terminal errors; a parse-success result is not enough if the source enforced
additional Pydantic or business constraints.

### Memory

Separate chat continuity from workflow state and durable knowledge. Session
owns conversation projection, RecordStore owns durable memory records, and
TriggerFlow execution state owns progression. Preserve tenant/user/session
scopes explicitly.

## Minimum Comparison

For at least one representative source run and target run, inspect:

- rendered model inputs and output schema;
- model request count and tool call order/results;
- final typed result and externally consumed metadata;
- memory writes and retrieval source identities;
- stream events used by the UI;
- invalid tool/output, timeout, policy denial, and provider-failure behavior.

Do not claim migration completion from a happy-path final string alone.
