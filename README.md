<img width="640" alt="image" src="https://github.com/user-attachments/assets/c645d031-c8b0-4dba-a515-9d7a4b0a6881" />

# Agently Skills

> Official installable skills for Agently, designed to help coding agents understand, route, and implement real Agently work more accurately.

[English](https://github.com/AgentEra/Agently-Skills/blob/main/README.md) | [中文](https://github.com/AgentEra/Agently-Skills/blob/main/README_CN.md)

Main framework repository: <https://github.com/AgentEra/Agently>  
Official documentation: <https://agently.tech/docs/en/> | <https://agently.cn/docs/>

---

<p align="center">
  <b><a href="#install">Install</a> | <a href="#capability-overview">Capability Overview</a> | <a href="#detailed-skill-list">Detailed Skill List</a> | <a href="#repository-layout">Repository Layout</a> | <a href="#migration-and-adaptation">Migration and Adaptation</a></b>
</p>

---

## Official Installable Skills

This repository publishes official Agently skills for coding-agent use.

Best results usually come from starting with the narrowest entry skill that matches the problem domain, then adding nearby skills only as needed.

When you install the full repository, you get:

- top-level routing from business requirements into the right Agently implementation path
- a complete one-request capability tree covering model setup, input composition, output control, tools, MCP, session, FastAPI, embeddings, and RAG
- a complete TriggerFlow capability tree covering orchestration, patterns, state and resources, sub flows, model integration, interrupts and stream, config, and execution state
- migration playbooks for LangChain and LangGraph

Prerequisite:

- `Agently >= 4.0.8.5`

## Install

Recommended first install for general Agently work:

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
```

Recommended first install for one-request-focused work:

```bash
npx skills add AgentEra/Agently-Skills --skill agently-model-request-playbook
```

Recommended first install for TriggerFlow-focused work:

```bash
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-playbook
```

List installable skills from the repository:

```bash
npx skills add AgentEra/Agently-Skills -l --full-depth
```

Install the whole repository only if you want the full capability tree to coexist in one environment:

```bash
npx skills add AgentEra/Agently-Skills
```

## Core Resources

- Main repository: <https://github.com/AgentEra/Agently>
- Official docs (EN): <https://agently.tech/docs/en/>
- Official docs (CN): <https://agently.cn/docs/>
- Skills repository: <https://github.com/AgentEra/Agently-Skills>
- Install command: `npx skills add AgentEra/Agently-Skills`

## Why This Repository Exists

Agently's practical boundary is much broader than "send one model request":

- you may need stable structured output
- you may need `instant` structured streaming
- you may need tools, MCP, a knowledge base, or session continuity
- you may need to expose the result through FastAPI
- you may need TriggerFlow for orchestration, concurrency, interrupts, and restore
- you may need to migrate an existing LangChain or LangGraph system

If those boundaries must be re-explained from scratch in every coding session, the result is slower and less consistent. This repository turns that repeated knowledge into installable skills with explicit routing, boundaries, and implementation guidance.

## Capability Overview

### 1. Top-Level Entry Skills

- `agently-playbook`
  The cross-domain router for Agently work when it is not yet clear whether the solution should stay one request, become multi-agent, or become TriggerFlow orchestration.
- `agently-model-request-playbook`
  The router for one-request and request-adjacent work after the problem is already known to stay in the one-request domain.
- `agently-triggerflow-playbook`
  The router for TriggerFlow-domain orchestration after the problem is already known to be a TriggerFlow workflow.

### 2. One-Request Core

- `agently-model-setup`
  Direct model connection and request-transport setup: `OpenAICompatible`, auth, endpoint, proxy, timeout, `request_options`, and minimal verification
- `agently-input-composition`
  Direct input-side prompt composition: prompt slots, prompt layering, mappings, attachments, low-level `chat_history`, and prompt inspection
- `agently-output-control`
  Direct output-side schema, retries, response consumption, and structured streaming with `instant` / `streaming_parse`

### 3. Request-Enhancement Skills

- `agently-tools`
- `agently-mcp`
- `agently-session-memo`
- `agently-prompt-config-files`
- `agently-fastapi-helper`
- `agently-embeddings`
- `agently-knowledge-base-and-rag`

### 4. Multi-Agent and Complex Systems

- `agently-multi-agent-patterns`
  Covers planner-worker, parallel experts, reviewer-reviser, and other multi-agent design patterns built from current Agently capabilities.

### 5. TriggerFlow Capability Tree

- `agently-triggerflow-orchestration`
  Low-level TriggerFlow primitives, execution entrypoints, contracts, and result semantics
- `agently-triggerflow-patterns`
  Reusable workflow shapes such as routers, fan-out and fan-in, safe loops, ReAct loops, and approval gates
- `agently-triggerflow-state-and-resources`
  `runtime_data`, `flow_data`, and resource boundaries
- `agently-triggerflow-subflows`
  Explicit child-flow boundaries through `to_sub_flow(...)`, `capture`, and `write_back`
- `agently-triggerflow-model-integration`
  Model requests inside workflows, including `delta` and `instant`
- `agently-triggerflow-config`
  Flow definition export, import, Mermaid, and contract metadata
- `agently-triggerflow-execution-state`
  Execution save, restore, and resume
- `agently-triggerflow-interrupts-and-stream`
  Interrupts, resume, runtime stream, and interactive waiting

## Detailed Skill List

### `agently-playbook`

Use this skill when the request starts from a cross-domain business or system requirement and it is still unclear which Agently solution level owns the problem, including:

- deciding whether the solution should stay one model request
- deciding whether it should become a multi-agent design
- deciding whether it should escalate into TriggerFlow
- choosing supporting combinations such as FastAPIHelper, session continuity, or prompt config
- choosing the right skill combination and implementation order

Skill path:

- `skills/agently-playbook/SKILL.md`

### `agently-model-request-playbook`

Use this skill when the problem is already known to belong to one-request Agently work, including:

- the standard request path
- the high-quality request path
- responsibility boundaries between framework and business logic
- when to add tools, MCP, KB/RAG, session, prompt config, or FastAPIHelper
- when to escalate from one request into TriggerFlow

Skill path:

- `skills/agently-model-request-playbook/SKILL.md`

### `agently-model-setup`

Use this skill when the main problem is direct Agently model connection or request-transport setup, including:

- `OpenAICompatible` setup
- provider switching
- auth and endpoint configuration
- `request_options`
- `agent.options(...)`
- `proxy`, `timeout`, and `client_options`
- minimal connection verification

Skill path:

- `skills/agently-model-setup/SKILL.md`

### `agently-input-composition`

Use this skill when the main problem is direct input-side prompt composition before one Agently request, including:

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

### `agently-output-control`

Use this skill when the main problem is direct output-side schema, retry, parsing, or structured-streaming behavior, including:

- `.output(...)` schema design
- `ensure_keys` and retries
- `get_text()`, `get_data()`, `get_data_object()`, and `get_meta()`
- `delta`, `specific`, `instant`, and `streaming_parse`
- reusing the same `response` without sending another request

Skill path:

- `skills/agently-output-control/SKILL.md`

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

### `agently-triggerflow-playbook`

Use this skill when the main problem is already TriggerFlow-domain workflow orchestration rather than generic Agently architecture selection, including:

- deciding whether the solution should use TriggerFlow
- choosing between orchestration, state-and-resources, subflows, and interrupt-and-stream work
- combining TriggerFlow with model setup or output control

Skill path:

- `skills/agently-triggerflow-playbook/SKILL.md`

### `agently-triggerflow-orchestration`

Use this skill when the main problem is low-level TriggerFlow primitives and execution semantics, including:

- async-first signal-driven orchestration
- `chunk`, `to(...)`, `when(...)`, `if_condition(...)`, and `match(...)`
- execution entrypoints and result semantics

Skill path:

- `skills/agently-triggerflow-orchestration/SKILL.md`

### `agently-triggerflow-patterns`

Use this skill when the main problem is choosing or implementing reusable TriggerFlow workflow shapes, including:

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

Use this skill when the main problem is an isolated child-flow boundary in TriggerFlow, including:

- `to_sub_flow(...)`
- `capture` and `write_back`
- child-flow state isolation
- parent-child runtime-stream bridge
- sub-flow-specific runtime limits

Skill path:

- `skills/agently-triggerflow-subflows/SKILL.md`

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

## Repository Layout

Public skills live under `skills/`. A typical skill contains:

- `SKILL.md`
- `references/`
- optional `scripts/`

Typical structure:

```text
skills/
  agently-playbook/
    SKILL.md
    references/
  agently-model-request-playbook/
    SKILL.md
    references/
  agently-model-setup/
    SKILL.md
    references/
    scripts/
  ...
```

The `spec/` directory is author-side only. It exists for writing, validation, and upstream-coverage maintenance, and is not part of the public skill payload.

## Migration and Adaptation

If your current system is based on LangChain or LangGraph, start with the migration skills:

- `agently-langchain-langgraph-migration-playbook`
  Top-level router for deciding whether the migration is LangChain-side or LangGraph-side
- `agently-langchain-to-agently`
  Covers `create_agent`, structured output, middleware, tools, memory, and service exposure
- `agently-langgraph-to-triggerflow`
  Covers `StateGraph`, `Send`, `Command`, threads and checkpoints, interrupts, streaming, and subgraphs

The goal of these migration skills is not line-by-line replacement. The goal is to translate the source capabilities into Agently's current capability tree and redesign the implementation where a literal rewrite would be misleading.

## Recommended Reading Order

If you are new to this repository, start here:

1. `agently-playbook`
2. `agently-model-request-playbook`
3. `agently-model-setup`
4. `agently-input-composition`
5. `agently-output-control`
6. move into tools, MCP, session, FastAPI, embeddings, or RAG only as needed
7. move into `agently-triggerflow-playbook` when the problem becomes a multi-step, async, restartable workflow

## Release Status

This repository currently has:

- full `skills-ref validate`
- full author-side validator coverage
- remote discovery and install smoke tests through `npx skills add AgentEra/Agently-Skills`

If you find that a skill boundary, trigger, or routing rule is still off, open an issue or PR.
