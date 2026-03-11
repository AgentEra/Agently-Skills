# Agently Skills

This repository contains Agent Skills for the Agently framework.

Prerequisite: Agently `>= 4.0.8.5`.

## Available Skills

### `agently-playbook`

Use this skill when the request starts from a business or system requirement rather than one Agently API, including:

- deciding whether the solution should stay one model request
- deciding whether it should become a multi-agent design
- deciding whether it should escalate into TriggerFlow
- choosing supporting combinations such as FastAPIHelper, session continuity, or prompt config
- choosing the right skill combination and implementation order

Skill path:

- `skills/agently-playbook/SKILL.md`

### `agently-langchain-langgraph-migration-playbook`

Use this skill when migrating a LangChain or LangGraph codebase or mental model into Agently, including:

- deciding whether the source design maps to LangChain-side or LangGraph-side migration
- choosing between one-request, multi-agent, or TriggerFlow migration targets
- choosing the correct migration skill and implementation order

Skill path:

- `skills/agently-langchain-langgraph-migration-playbook/SKILL.md`

### `agently-langchain-to-agently`

Use this skill when migrating LangChain agent-side concepts into Agently, including:

- `create_agent`
- `response_format`, `ProviderStrategy`, and `ToolStrategy`
- tools
- structured output
- short-term memory
- middleware or guardrails
- `HumanInTheLoopMiddleware`
- retrieval and service exposure

Skill path:

- `skills/agently-langchain-to-agently/SKILL.md`

### `agently-langgraph-to-triggerflow`

Use this skill when migrating LangGraph orchestration concepts into Agently TriggerFlow, including:

- `StateGraph`
- nodes and edges
- `Send` and `Command`
- graph state
- threads, checkpoints, and persistence
- interrupts
- streaming and subgraphs

Skill path:

- `skills/agently-langgraph-to-triggerflow/SKILL.md`

### `agently-model-setup`

Use this skill when configuring Agently model access for Chat LLM, Completions LLM, or VLM, including:

- `OpenAICompatible` setup
- provider switching
- auth and endpoint configuration
- `request_options`
- `agent.options(...)`
- `proxy`, `timeout`, and `client_options`
- minimal connection verification

Skill path:

- `skills/agently-model-setup/SKILL.md`

### `agently-model-request-playbook`

Use this skill when the request starts from business needs around one Agently model request, including:

- the standard request path
- the high-quality request path
- responsibility boundaries between framework and business logic
- when to add tools, MCP, KB/RAG, session, prompt config, or FastAPIHelper
- when to escalate from one request into TriggerFlow

Skill path:

- `skills/agently-model-request-playbook/SKILL.md`

### `agently-multi-agent-patterns`

Use this skill when designing a multi-agent solution in Agently, including:

- deciding whether the problem should stay one request or become a specialized agent team
- planner-worker or supervisor-router patterns
- staged specialist pipelines
- parallel experts and synthesizer
- reviewer-reviser design
- agent handoff contracts and ownership boundaries

Skill path:

- `skills/agently-multi-agent-patterns/SKILL.md`

### `agently-output-control`

Use this skill when defining or consuming Agently model output, including:

- `.output(...)` schema design
- `ensure_keys` and retries
- `get_text()`, `get_data()`, `get_data_object()`, and `get_meta()`
- `delta`, `specific`, `instant`, and `streaming_parse`
- reusing the same `response` without sending another request

Skill path:

- `skills/agently-output-control/SKILL.md`

### `agently-input-composition`

Use this skill when composing Agently request input before sending a model call, including:

- prompt slots
- quick prompt methods
- agent-vs-request prompt layering
- placeholder mappings
- `chat_history`
- `attachment(...)`
- nested serializable prompt data
- prompt inspection through `to_text()` and `to_messages(...)`

Skill path:

- `skills/agently-input-composition/SKILL.md`

### `agently-embeddings`

Use this skill when configuring and sending Agently embeddings requests, including:

- `model_type="embeddings"`
- single or batch `input(...)`
- parsed vector results through `start()` / `get_data()`
- `async_start()` and async embeddings usage
- original payload or metadata inspection through `get_response()`
- offline indexing and online query embedding patterns

Skill path:

- `skills/agently-embeddings/SKILL.md`

### `agently-tools`

Use this skill when registering, attaching, or controlling Agently tools, including:

- `@agent.tool_func`
- `register_tool(...)`
- `use_tools(...)`
- built-in Search, Browse, and Cmd
- tool-loop settings
- custom plan or execution handlers
- tool logs from one model request

Skill path:

- `skills/agently-tools/SKILL.md`

### `agently-mcp`

Use this skill when exposing MCP server tools to Agently, including:

- `agent.use_mcp(...)`
- `Agently.tool.use_mcp(...)`
- stdio or HTTP transports
- MCP schema mapping into tool metadata
- agent-scoped MCP tool visibility
- structured MCP tool results and validation errors

Skill path:

- `skills/agently-mcp/SKILL.md`

### `agently-fastapi-helper`

Use this skill when exposing Agently through `FastAPIHelper`, including:

- Agent, ModelRequest, TriggerFlow, or generator providers
- POST and GET endpoints
- SSE
- WebSocket
- helper payload shape
- wrapped response and error behavior
- TriggerFlow-contract-aware request and response typing
- OpenAPI contract metadata

Skill path:

- `skills/agently-fastapi-helper/SKILL.md`

### `agently-knowledge-base-and-rag`

Use this skill when building Agently knowledge-base or RAG flows, including:

- `ChromaCollection`
- embedding-agent-backed indexing
- collection `add(...)` and `query(...)`
- query-to-`info(...)` answer flow
- `ChromaData` and `ChromaEmbeddingFunction`
- process-level collection reuse

Skill path:

- `skills/agently-knowledge-base-and-rag/SKILL.md`

### `agently-session-memo`

Use this skill when managing Agently session-backed conversation memory, including:

- `activate_session()` and `deactivate_session()`
- session-backed `chat_history`
- `full_context`, `context_window`, and `memo`
- `session.input_keys` and `session.reply_keys`
- resize handlers and `session.max_length`
- session export and restore

Skill path:

- `skills/agently-session-memo/SKILL.md`

### `agently-prompt-config-files`

Use this skill when managing Agently prompts as YAML or JSON config, including:

- `load_yaml_prompt(...)` and `load_json_prompt(...)`
- `get_yaml_prompt(...)` and `get_json_prompt(...)`
- `.agent`, `.request`, and `.alias`
- `mappings` and `prompt_key_path`
- config-driven prompt roundtrip and template externalization

Skill path:

- `skills/agently-prompt-config-files/SKILL.md`

### `agently-triggerflow-orchestration`

Use this skill when building basic TriggerFlow workflows, including:

- async-first signal-driven orchestration
- `chunk`, `to(...)`, `when(...)`, `if_condition(...)`, and `match(...)`
- execution entrypoints and result semantics

Skill path:

- `skills/agently-triggerflow-orchestration/SKILL.md`

### `agently-triggerflow-patterns`

Use this skill when selecting or implementing common TriggerFlow workflow patterns, including:

- routers and classify-then-route workflows
- fan-out and fan-in
- `batch(...)`, `for_each(...)`, `collect(...)`, and `side_branch(...)`
- safe loops and dead-loop prevention
- evaluator-optimizer and ReAct-style loops
- human approval gates and pause-between-turns patterns

Skill path:

- `skills/agently-triggerflow-patterns/SKILL.md`

### `agently-triggerflow-state-and-resources`

Use this skill when a TriggerFlow design question is really about state or dependency boundaries, including:

- `runtime_data` vs `flow_data`
- flow-level vs execution-level runtime resources
- `data.set_resource(...)`
- restart-safe state design
- save/load and config boundaries for resources

Skill path:

- `skills/agently-triggerflow-state-and-resources/SKILL.md`

### `agently-triggerflow-subflows`

Use this skill when a TriggerFlow workflow needs an isolated child flow, including:

- `to_sub_flow(...)`
- `capture` and `write_back`
- child-flow state isolation
- parent-child runtime-stream bridge
- sub-flow-specific runtime limits

Skill path:

- `skills/agently-triggerflow-subflows/SKILL.md`

### `agently-triggerflow-playbook`

Use this skill when the request starts from business workflow analysis rather than TriggerFlow APIs, including:

- deciding whether the solution should use TriggerFlow
- choosing between orchestration, state-and-resources, subflows, and interrupt-and-stream work
- combining TriggerFlow with model setup or output control

Skill path:

- `skills/agently-triggerflow-playbook/SKILL.md`

### `agently-triggerflow-model-integration`

Use this skill when a TriggerFlow workflow needs model execution inside the flow, including:

- request creation inside chunks
- async-first model requests per step, branch, or item
- multiple model requests through `batch(...)`, `for_each(...)`, or bounded gather
- `delta` or `instant` inside the flow
- early structured-stream dispatch into later workflow work

Skill path:

- `skills/agently-triggerflow-model-integration/SKILL.md`

### `agently-triggerflow-config`

Use this skill when a TriggerFlow definition should be copied, exported, imported, or visualized, including:

- `save_blue_print()` and `load_blue_print()`
- `get_flow_config()`
- `get_json_flow()` / `get_yaml_flow()`
- `load_json_flow()` / `load_yaml_flow()`
- `to_mermaid(...)`

Skill path:

- `skills/agently-triggerflow-config/SKILL.md`

### `agently-triggerflow-execution-state`

Use this skill when a running TriggerFlow execution should be saved, restored, or resumed, including:

- `execution.save()` and `execution.load()`
- waiting or ready-result restore
- `continue_with(...)` after restore
- runtime-resource reinjection

Skill path:

- `skills/agently-triggerflow-execution-state/SKILL.md`

### `agently-triggerflow-interrupts-and-stream`

Use this skill when a TriggerFlow workflow needs live interaction, including:

- `pause_for(...)` and `continue_with(...)`
- pending-interrupt handling
- runtime stream output and lifecycle
- interactive wait-and-resume loops
- forwarding live model output into runtime stream

Skill path:

- `skills/agently-triggerflow-interrupts-and-stream/SKILL.md`

## Install

Before using these skills, ensure the Agently package version is `>= 4.0.8.5`.

Install the repository with the Skills CLI:

```bash
npx skills add <owner>/<repo>
```

Install only this skill from the repository:

```bash
npx skills add <owner>/<repo> --skill agently-embeddings
```

## Repository Layout

```text
skills/
  agently-playbook/
    SKILL.md
    references/
  agently-langchain-langgraph-migration-playbook/
    SKILL.md
    references/
  agently-langchain-to-agently/
    SKILL.md
    references/
  agently-langgraph-to-triggerflow/
    SKILL.md
    references/
  agently-model-setup/
    SKILL.md
    references/
    scripts/
  agently-model-request-playbook/
    SKILL.md
    references/
  agently-multi-agent-patterns/
    SKILL.md
    references/
  agently-output-control/
    SKILL.md
    references/
  agently-input-composition/
    SKILL.md
    references/
  agently-embeddings/
    SKILL.md
    references/
  agently-session-memo/
    SKILL.md
    references/
  agently-prompt-config-files/
    SKILL.md
    references/
  agently-tools/
    SKILL.md
    references/
  agently-mcp/
    SKILL.md
    references/
  agently-fastapi-helper/
    SKILL.md
    references/
  agently-knowledge-base-and-rag/
    SKILL.md
    references/
  agently-triggerflow-orchestration/
    SKILL.md
    references/
  agently-triggerflow-patterns/
    SKILL.md
    references/
  agently-triggerflow-state-and-resources/
    SKILL.md
    references/
  agently-triggerflow-subflows/
    SKILL.md
    references/
  agently-triggerflow-playbook/
    SKILL.md
    references/
  agently-triggerflow-model-integration/
    SKILL.md
    references/
  agently-triggerflow-config/
    SKILL.md
    references/
  agently-triggerflow-execution-state/
    SKILL.md
    references/
  agently-triggerflow-interrupts-and-stream/
    SKILL.md
    references/
```
