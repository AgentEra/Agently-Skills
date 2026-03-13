# Agently Skills

Official installable skills for coding agents working with Agently.

Main framework repository: <https://github.com/AgentEra/Agently>  
Official documentation: <https://agently.tech/docs/en/> | <https://agently.cn/docs/>

## What Is Agently?

Agently is a framework for building model-powered applications and workflows.

It provides native surfaces for:

- model setup and provider settings
- prompt composition and prompt config
- structured output and required-key enforcement
- response reuse, metadata access, and streaming consumption
- tools, MCP, memory, and knowledge-base flows
- workflow orchestration through TriggerFlow

## What Is Agently-Skills?

Agently-Skills is the official skills package for coding agents that need to build with Agently.

It does more than explain API syntax. It teaches coding agents:

- how to recognize Agently-appropriate scenarios from natural-language product requests
- how to choose the right skill or skill combination
- how to structure projects around Agently-native capability boundaries
- how to apply best-practice project layout, orchestration, and performance refactors
- how to stay inside Agently's design philosophy instead of writing generic glue first

The goal is not shallow snippet generation. The goal is to help a coding agent produce a complete project that actually fits Agently.

For example, a broad request such as `build a travel planning tool on top of local Ollama` should not be treated as just one local model call. The skills should help the coding agent decide the right setup path, prompt structure, workflow shape, and project layout from that natural-language intent.

## Why Use The Official Skills?

- They improve scenario capture for broad, under-specified model-app requests.
- They encode Agently-native best practices instead of generic framework-agnostic habits.
- They include guidance on project layout, routing, performance optimization, and design philosophy.
- They are validated with both route fixtures and implementation fixtures, so the skills are checked against real scenario language rather than only hand-written examples.

## Routing Model

Use this mental model when choosing a skill:

- If the request starts from business goals, product behavior, refactor intent, or an unclear owner layer, start with `agently-playbook`.
- If the request is already narrow and explicit, route directly to the owning leaf skill.
- Prefer native Agently surfaces before custom wrappers, custom parsers, custom retry loops, or custom workflow infrastructure.

The most important routing rules are:

- unresolved product, assistant, automation, or workflow request -> `agently-playbook`
- provider wiring, env vars, or model settings separation -> `agently-model-setup`
- prompt structure, prompt config, YAML-backed prompt behavior, or config-file prompt bridge -> `agently-prompt-management`
- stable structured fields, required keys, or machine-readable output -> `agently-output-control`
- reuse one response as text, data, metadata, or streaming updates -> `agently-model-response`
- session continuity or restore-after-restart -> `agently-session-memory`
- tools, MCP, FastAPIHelper, `auto_func`, or `KeyWaiter` -> `agently-agent-extensions`
- embeddings, indexing, retrieval, or KB-to-answer -> `agently-knowledge-base`
- explicit orchestration, TriggerFlow, mixed sync/async execution, event-driven fan-out, process-clarity refactors, or resumable multi-stage flows -> `agently-triggerflow`
- migration from LangChain or LangGraph -> `agently-migration-playbook`, then the matching migration leaf

## Public Catalog

The public catalog currently contains 12 skills.

### Entry

- `agently-playbook`
  Top-level router for unresolved model-powered product, assistant, internal-tool, automation, evaluator, workflow, or project-structure refactor requests.

### Request Side

- `agently-model-setup`
  Provider connection, dotenv-based settings, model transport setup, and settings-file-based model separation.
- `agently-prompt-management`
  Prompt composition, prompt config, YAML-backed prompt behavior, mappings, and reusable request-side prompt structure.
- `agently-output-control`
  Output schema, field ordering, required keys, and structured output reliability.
- `agently-model-response`
  `get_response()`, parsed results, metadata, streaming consumption, and response reuse.
- `agently-session-memory`
  Session-backed continuity, memo, restore, and request-side conversational state.

### Request Extensions

- `agently-agent-extensions`
  Tools, MCP, FastAPIHelper, `auto_func`, and `KeyWaiter`.
- `agently-knowledge-base`
  Embeddings plus Chroma-backed indexing, retrieval, and retrieval-to-answer flows.

### Workflow

- `agently-triggerflow`
  TriggerFlow orchestration, runtime state, runtime stream, workflow-side model execution, event-driven fan-out, process-clarity refactors, and mixed sync/async orchestration.

### Migration

- `agently-migration-playbook`
  Migration router for existing LangChain or LangGraph systems.
- `agently-langchain-to-agently`
  Direct LangChain agent-side migration guidance.
- `agently-langgraph-to-triggerflow`
  Direct LangGraph orchestration migration guidance.

## Install

You can install the whole official skills repository:

```bash
npx skills add AgentEra/Agently-Skills
```

You can also ask your coding agent to install `AgentEra/Agently-Skills`.

If you want a narrower install, start with `agently-playbook`:

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
```

`request-core`  
Use when the solution stays on the request side and needs model setup, prompt shaping, structured output, and response reuse.

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-model-setup
npx skills add AgentEra/Agently-Skills --skill agently-prompt-management
npx skills add AgentEra/Agently-Skills --skill agently-output-control
npx skills add AgentEra/Agently-Skills --skill agently-model-response
```

`request-extensions`  
Use when the request side also needs tools, MCP, session continuity, or a knowledge base.

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-agent-extensions
npx skills add AgentEra/Agently-Skills --skill agently-session-memory
npx skills add AgentEra/Agently-Skills --skill agently-knowledge-base
```

`workflow-core`  
Use when the owner layer is workflow orchestration, especially for event-driven fan-out, performance-sensitive refactors, resumable flows, or mixed sync/async execution.

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow
npx skills add AgentEra/Agently-Skills --skill agently-output-control
npx skills add AgentEra/Agently-Skills --skill agently-model-response
npx skills add AgentEra/Agently-Skills --skill agently-session-memory
```

`migration`  
Use when the request is explicitly about moving an existing LangChain or LangGraph system into Agently.

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-migration-playbook
npx skills add AgentEra/Agently-Skills --skill agently-langchain-to-agently
npx skills add AgentEra/Agently-Skills --skill agently-langgraph-to-triggerflow
```
