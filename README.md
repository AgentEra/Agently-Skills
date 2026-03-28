# Agently Skills

Official installable skills for coding agents working with Agently.

Main framework repository: <https://github.com/AgentEra/Agently>  
Official documentation: <https://agently.tech/docs/en/> | <https://agently.cn/docs/>

## What Is Agently?

Agently is a framework for building model-powered applications and workflows.

It provides native surfaces for:

- async-first model requests, streaming consumption, and web-service integration
- model setup and provider settings
- prompt composition and prompt config
- structured output and required-key enforcement
- response reuse, metadata access, and streaming consumption
- tools, MCP, memory, and knowledge-base flows
- workflow orchestration through TriggerFlow
- optional developer tooling through `agently-devtools`

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
- They are checked against realistic scenario language instead of relying only on hand-written snippets.

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
- tools, MCP, FastAPIHelper, `auto_func`, `KeyWaiter`, Browse with Playwright or PyAutoGUI, or optional `agently-devtools` integration -> `agently-agent-extensions`
- embeddings, indexing, retrieval, or KB-to-answer -> `agently-knowledge-base`
- explicit orchestration, TriggerFlow, mixed sync/async execution, event-driven fan-out, process-clarity refactors, graph-friendly workflow definitions, or resumable multi-stage flows -> `agently-triggerflow`
- migration from LangChain or LangGraph -> `agently-migration-playbook`, then the matching migration leaf

Async should usually be the default execution stance:

- prefer async APIs for service code, streaming, TriggerFlow, tool concurrency, and any path that may benefit from overlap or cancellation
- treat sync APIs as convenience wrappers for local scripts, teaching examples, or compatibility bridges
- if the solution will live behind HTTP, SSE, WebSocket, or a long-running worker, assume async-first unless a concrete constraint proves otherwise

## Standard Project Shape

When an Agently project needs to stay maintainable, initialize or refactor it around explicit capability boundaries instead of one oversized `app.py`.

The default shape should usually separate:

- `SETTINGS.yaml` or a settings layer for provider config, `${ENV.xxx}` placeholders, workflow/search/browse knobs, and other deployment-time switches
- `app/` or another integration layer that loads settings, validates required env names when needed, chooses async boundaries, and wires tools plus the main flow
- `prompts/` for YAML or JSON prompt contracts that own `input`, `info`, `instruct`, and `output`
- `services/` for request wrappers, response normalization, and business-facing adapters
- `domain/` or `schemas/` for enums, request/response contracts, and shared value objects
- `workflow/` for TriggerFlow graphs and chunk implementations
- `tools/` for replaceable search, browse, MCP, or external adapters
- `tests/` for settings smoke checks, prompt/response checks, and API or flow validation
- `outputs/` and `logs/` for runtime artifacts instead of mixing them into source folders
- optional `agently-devtools` wiring in the integration layer for local observation, evaluation, playground, and logs

Two source-backed details matter here:

- Configure Prompt supports placeholder mappings recursively across prompt values and keys. Keep `${topic}`, `${language}`, `${column_title}`, and similar variables in prompt files and inject them through `load_yaml_prompt(..., mappings={...})` or `load_json_prompt(...)`.
- Model settings can keep `${ENV.NAME}` placeholders and let `Agently.load_settings("yaml_file", "...", auto_load_env=True)` resolve them by finding and loading a local `.env` file. If settings are created inline instead of in a file, use `Agently.set_settings(...)`.

Two high-frequency rules prevent common drift:

- keep stable shared output contracts in prompt config rather than scattering them across Python helpers
- keep `OpenAICompatible` and similar provider settings under the plugin namespace that the requester actually reads, for example `plugins.ModelRequester.OpenAICompatible.*`
- keep optional DevTools endpoints and bridge wiring outside prompt files and workflow helpers; use `ObservationBridge`, `EvaluationBridge`, or `create_local_observation_app(...)` from the public `agently-devtools` package instead of repo-specific install guidance

This is the pattern used by `Agently-Daily-News-Collector`: settings stay in `SETTINGS.yaml`, prompt contracts stay in `prompts/`, flow construction stays in `workflow/`, and the app layer does env loading plus Agently wiring.

Project initialization should not be a separate public skill. It belongs to `agently-playbook`: decide the owner layers, create the skeleton, and then hand implementation work to the owning leaf skills.

A fuller public reference lives in [`skills/agently-playbook/references/project-framework.md`](skills/agently-playbook/references/project-framework.md).

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
  Tools, MCP, FastAPIHelper, `auto_func`, `KeyWaiter`, Browse with Playwright or PyAutoGUI, and optional `agently-devtools` integration.
- `agently-knowledge-base`
  Embeddings plus Chroma-backed indexing, retrieval, and retrieval-to-answer flows.

### Workflow

- `agently-triggerflow`
  TriggerFlow orchestration, runtime state, runtime stream, workflow-side model execution, event-driven fan-out, process-clarity refactors, mixed sync/async orchestration, and graph-friendly workflow definitions for debugging and visualization.

## Optional Companion Package

Agently `v4.0.9` also introduces `agently-devtools` as an optional developer-tooling companion package.

- Install: `pip install -U agently agently-devtools`
- Compatibility line: `agently-devtools 0.1.x` targets `agently >=4.0.9,<4.1.0`
- Public entrypoints: `ObservationBridge`, `EvaluationBridge`, `EvaluationRunner`, and `create_local_observation_app`
- Recommended startup: `agently-devtools start`

Use this package when an Agently app needs local runtime observation, evaluations, logs, or playground support during development and debugging. The skills package treats this as an optional extension surface, not as a required source-repo dependency.

### Migration

- `agently-migration-playbook`
  Migration router for existing LangChain or LangGraph systems.
- `agently-langchain-to-agently`
  Direct LangChain agent-side migration guidance.
- `agently-langgraph-to-triggerflow`
  Direct LangGraph orchestration migration guidance.

## Install

Fastest full install across all detected agents:

```bash
npx skills add AgentEra/Agently-Skills --all
```

Safer full install when you want to control the target agent explicitly:

```bash
npx skills add AgentEra/Agently-Skills --agent codex --skill '*' -y
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
