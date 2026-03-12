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
Treat the repository as a published catalog, but treat runtime activation as a bundle-sized choice.

The full catalog contains:

- top-level routing from business requirements into the right Agently implementation path
- a complete one-request capability tree covering model setup, input composition, output control, tools, MCP, session, FastAPI, embeddings, and RAG
- a complete TriggerFlow capability tree covering orchestration, patterns, state and resources, sub flows, model integration, interrupts and stream, config, and execution state
- migration playbooks for LangChain and LangGraph

Prerequisite:

- `Agently >= 4.0.8.5`

## Install

Recommended activation order:

1. start with one entry skill or one documented bundle
2. add nearby leaf skills only after the request has already narrowed into that domain
3. install the full repository only when you deliberately want the whole catalog to coexist

If your tool cannot install a named bundle directly, use the install sequences below.
For client-side activation, use the public bundle manifest at `bundles/manifest.json` and activate only one bundle-sized skill set by default.

### Entry installs

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

### Bundle install sequences

`request-core` keeps the active set centered on one-request Agently work:

```bash
npx skills add AgentEra/Agently-Skills --skill agently-model-request-playbook
npx skills add AgentEra/Agently-Skills --skill agently-model-setup
npx skills add AgentEra/Agently-Skills --skill agently-input-composition
npx skills add AgentEra/Agently-Skills --skill agently-output-control
```

`request-extensions` is additive. Start from `request-core`, then add only the leaf skills you actually need:

- `agently-tools`
- `agently-mcp`
- `agently-session-memo`
- `agently-prompt-config-files`
- `agently-fastapi-helper`
- `agently-eval-and-judge`
- `agently-embeddings`
- `agently-knowledge-base-and-rag`

`multi-agent` keeps the active set focused on specialist-agent architecture only:

```bash
npx skills add AgentEra/Agently-Skills --skill agently-multi-agent-patterns
```

`triggerflow-core` keeps the active set inside the TriggerFlow workflow domain:

```bash
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-playbook
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-orchestration
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-patterns
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-state-and-resources
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-subflows
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-model-integration
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-config
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-execution-state
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow-interrupts-and-stream
```

`migration` keeps the active set focused on LangChain or LangGraph adaptation:

```bash
npx skills add AgentEra/Agently-Skills --skill agently-langchain-langgraph-migration-playbook
npx skills add AgentEra/Agently-Skills --skill agently-langchain-to-agently
npx skills add AgentEra/Agently-Skills --skill agently-langgraph-to-triggerflow
```

List installable skills from the repository:

```bash
npx skills add AgentEra/Agently-Skills -l --full-depth
```

Install the whole repository only if you want the full capability tree to coexist in one environment:

```bash
npx skills add AgentEra/Agently-Skills
```

Even after a full-repository install, client integrators should still prefer activating one bundle from `bundles/manifest.json` instead of exposing the full catalog by default.

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

The groups below describe the published catalog. The recommended runtime activation sets are the entry installs, bundle sequences above, and the public machine-readable bundle manifest at `bundles/manifest.json`.

### 1. Top-Level Entry Skills

- `agently-playbook`
  The cross-domain router for model-powered work when it is not yet clear whether the solution should stay one request, become multi-agent, or become workflow orchestration.
- `agently-model-request-playbook`
  The router for single-request and short request-chain work after the problem is already known to stay in that domain.
- `agently-triggerflow-playbook`
  The router for workflow orchestration and event-driven processing after the problem is already known to be orchestration-first.

### 2. One-Request Core

- `agently-model-setup`
  Direct model connection and request-transport setup: `OpenAICompatible`, auth, endpoint, proxy, timeout, `request_options`, and minimal verification
- `agently-input-composition`
  Direct input-side prompt composition: prompt slots, prompt layering, mappings, attachments, low-level `chat_history`, and prompt inspection
- `agently-output-control`
  Direct output-side schema, retries, response consumption, and structured streaming with `instant` / `streaming_parse`

### 3. Request-Enhancement Skills

- `agently-tools`
  Direct local and built-in tool registration plus request-time tool-loop control
- `agently-mcp`
  Direct MCP server registration into Agently tools with transport and schema mapping
- `agently-session-memo`
  Session-backed conversation continuity, memo, resize, serialization, and restore
- `agently-prompt-config-files`
  Direct YAML/JSON prompt-template config loading, mappings, `.alias`, and roundtrip export
- `agently-fastapi-helper`
  Direct HTTP, SSE, and WebSocket exposure through `FastAPIHelper`
- `agently-eval-and-judge`
  Direct rubric scoring, pass-fail checks, review reports, and validator-model design
- `agently-embeddings`
  Direct embeddings request setup, batching, vector consumption, and embedding-agent handoff
- `agently-knowledge-base-and-rag`
  Direct Chroma-backed knowledge-base indexing, retrieval, and retrieval-to-answer flow

### 4. Multi-Agent and Complex Systems

- `agently-multi-agent-patterns`
  Multi-agent pattern selection and handoff design after the architecture is already known to need multiple specialized agents.

### 5. TriggerFlow Capability Tree

- `agently-triggerflow-orchestration`
  Low-level TriggerFlow primitives, execution entrypoints, contracts, and result semantics
- `agently-triggerflow-patterns`
  Reusable workflow shapes such as routers, fan-out and fan-in, safe loops, ReAct loops, and approval gates
- `agently-triggerflow-state-and-resources`
  State placement and runtime-resource boundaries such as `runtime_data`, `flow_data`, and `data.set_resource(...)`
- `agently-triggerflow-subflows`
  Explicit child-flow boundaries through `to_sub_flow(...)`, `capture`, and `write_back`
- `agently-triggerflow-model-integration`
  Model execution inside workflows, including request creation, bounded concurrency, `delta`, and `instant`
- `agently-triggerflow-config`
  TriggerFlow definition export, import, blueprint copy, Mermaid, and contract metadata
- `agently-triggerflow-execution-state`
  Running-execution save, restore, resume, and runtime-resource reinjection
- `agently-triggerflow-interrupts-and-stream`
  Waiting, resume, runtime-stream lifecycle, and live interaction

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

Use this skill when the main problem is direct local or built-in Agently tool registration and request-time tool-loop control, including:

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

Use this skill when the main problem is direct MCP server registration into Agently tools, including:

- `agent.use_mcp(...)`
- `Agently.tool.use_mcp(...)`
- stdio or HTTP transports
- MCP schema mapping into tool metadata
- agent-scoped MCP tool visibility
- structured MCP tool results and validation errors

Skill path:

- `skills/agently-mcp/SKILL.md`

### `agently-session-memo`

Use this skill when the main problem is Session-backed conversation continuity and restore, including:

- `activate_session()` and `deactivate_session()`
- session-backed `chat_history`
- `full_context`, `context_window`, and `memo`
- `session.input_keys` and `session.reply_keys`
- resize handlers and `session.max_length`
- session export and restore

Skill path:

- `skills/agently-session-memo/SKILL.md`

### `agently-prompt-config-files`

Use this skill when the main problem is externalized YAML or JSON prompt-template config in Agently, including:

- `load_yaml_prompt(...)` and `load_json_prompt(...)`
- `get_yaml_prompt(...)` and `get_json_prompt(...)`
- `.agent`, `.request`, and `.alias`
- `mappings` and `prompt_key_path`
- config-driven prompt roundtrip and template externalization

Skill path:

- `skills/agently-prompt-config-files/SKILL.md`

### `agently-fastapi-helper`

Use this skill when the main problem is direct HTTP, SSE, or WebSocket exposure through `FastAPIHelper`, including:

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

### `agently-eval-and-judge`

Use this skill when the main problem is direct evaluation, scoring, or judge-model design, including:

- rubric scoring
- pass-fail checks
- issue reports and evidence-backed review
- validator-model prompts
- pairwise comparison
- generator-versus-judge boundary decisions

Skill path:

- `skills/agently-eval-and-judge/SKILL.md`

### `agently-embeddings`

Use this skill when the main problem is direct Agently embeddings request setup and vector consumption, including:

- `model_type="embeddings"`
- single or batch `input(...)`
- parsed vector results through `start()` / `get_data()`
- `async_start()` and async embeddings usage
- original payload or metadata inspection through `get_response()`
- offline indexing and online query embedding patterns

Skill path:

- `skills/agently-embeddings/SKILL.md`

### `agently-knowledge-base-and-rag`

Use this skill when the main problem is Agently's Chroma-backed knowledge-base or retrieval-to-answer path, including:

- `ChromaCollection`
- embedding-agent-backed indexing
- collection `add(...)` and `query(...)`
- query-to-`info(...)` answer flow
- `ChromaData` and `ChromaEmbeddingFunction`
- process-level collection reuse

Skill path:

- `skills/agently-knowledge-base-and-rag/SKILL.md`

### `agently-multi-agent-patterns`

Use this skill when the problem is already known to need multiple specialized agents and the main task is choosing a multi-agent pattern, including:

- deciding whether the problem should stay one request or become a specialized agent team
- planner-worker or supervisor-router patterns
- staged specialist pipelines
- parallel experts and synthesizer
- reviewer-reviser design
- agent handoff contracts and ownership boundaries

Skill path:

- `skills/agently-multi-agent-patterns/SKILL.md`

### `agently-triggerflow-playbook`

Use this skill when the main problem is already workflow orchestration or event-driven processing rather than generic architecture selection, including:

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

Use this skill when the main problem is TriggerFlow state placement or runtime-dependency boundaries, including:

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

Use this skill when the main problem is Agently model execution inside TriggerFlow flow logic, including:

- request creation inside chunks
- async-first model requests per step, branch, or item
- multiple model requests through `batch(...)`, `for_each(...)`, or bounded gather
- `delta` or `instant` inside the flow
- early structured-stream dispatch into later workflow work

Skill path:

- `skills/agently-triggerflow-model-integration/SKILL.md`

### `agently-triggerflow-config`

Use this skill when the main problem is TriggerFlow definition export, import, copy, or visual inspection, including:

- `save_blue_print()` and `load_blue_print()`
- `get_flow_config()`
- `get_json_flow()` / `get_yaml_flow()`
- `load_json_flow()` / `load_yaml_flow()`
- `to_mermaid(...)`

Skill path:

- `skills/agently-triggerflow-config/SKILL.md`

### `agently-triggerflow-execution-state`

Use this skill when the main problem is saving, loading, or resuming one running TriggerFlow execution instance, including:

- `execution.save()` and `execution.load()`
- waiting or ready-result restore
- `continue_with(...)` after restore
- runtime-resource reinjection

Skill path:

- `skills/agently-triggerflow-execution-state/SKILL.md`

### `agently-triggerflow-interrupts-and-stream`

Use this skill when the main problem is TriggerFlow waiting, resume, or runtime-stream behavior, including:

- `pause_for(...)` and `continue_with(...)`
- pending-interrupt handling
- runtime stream output and lifecycle
- interactive wait-and-resume loops
- forwarding live model output into runtime stream

Skill path:

- `skills/agently-triggerflow-interrupts-and-stream/SKILL.md`

### `agently-langchain-langgraph-migration-playbook`

Use this skill when migrating a LangChain or LangGraph codebase or mental model into Agently and the migration entry is still unresolved, including:

- deciding whether the source design maps to LangChain-side or LangGraph-side migration
- choosing between one-request, multi-agent, or TriggerFlow migration targets
- choosing the correct migration skill and implementation order

Skill path:

- `skills/agently-langchain-langgraph-migration-playbook/SKILL.md`

### `agently-langchain-to-agently`

Use this skill when directly migrating known LangChain agent-side concepts into Agently, including:

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

Use this skill when directly migrating known LangGraph orchestration concepts into Agently TriggerFlow, including:

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
  Top-level router only when the migration entry is still unresolved and you must choose LangChain-side vs LangGraph-side
- `agently-langchain-to-agently`
  Direct migration leaf for LangChain agent-side surfaces such as `create_agent`, structured output, middleware, tools, memory, and service exposure
- `agently-langgraph-to-triggerflow`
  Direct migration leaf for LangGraph orchestration surfaces such as `StateGraph`, `Send`, `Command`, threads and checkpoints, interrupts, streaming, and subgraphs

The goal of these migration skills is not line-by-line replacement. The goal is to translate the source capabilities into Agently's current capability tree and redesign the implementation where a literal rewrite would be misleading.

## Recommended Reading Order

If you are new to this repository, start here:

1. `agently-playbook`
2. `agently-model-request-playbook`
3. `agently-model-setup`
4. `agently-input-composition`
5. `agently-output-control`
6. `agently-eval-and-judge` when the problem becomes scoring, review, or validator-model design
7. move into tools, MCP, session, FastAPI, embeddings, or RAG only as needed
8. move into `agently-triggerflow-playbook` when the problem becomes a multi-step, async, restartable workflow

## Release Status

This repository currently has:

- full `skills-ref validate`
- full author-side validator coverage
- remote discovery and install smoke tests through `npx skills add AgentEra/Agently-Skills`

If you find that a skill boundary, trigger, or routing rule is still off, open an issue or PR.

## Capability Feedback

If real usage shows that the problem is not just skill routing or documentation quality, but an actual Agently framework-capability gap, submit sanitized capability feedback directly to the Agently feedback API.

Use this path when:

- current behavior does not match reasonable framework expectations
- the framework appears to be missing support that the scenario should require
- a concrete implementation path still performs materially below expectation because of framework-level limits

Endpoint:

- `POST https://api.agently.cn/feedback/api/feedbacks`

Example body:

```json
{
  "who_are_you": "Acme team PM",
  "request_context": "Building an internal workflow tool",
  "agently_issue": "Unclear how to combine TriggerFlow with existing FastAPI routes",
  "expected_support": "Need example code and better documentation"
}
```

Safety note:

- sanitize the feedback before sending it
- do not include secrets, tokens, private URLs, customer data, or other sensitive internal information

To make the feedback actionable, include at least one of the following after sanitization:

- the usage code that shows how you are using Agently
- the framework code file path and line numbers that you believe are problematic
- a small code block that reproduces the issue or expectation gap
