# Agently Skills V2

Official installable skills for coding agents working with Agently.

Main framework repository: <https://github.com/AgentEra/Agently>  
Official documentation: <https://agently.tech/docs/en/> | <https://agently.cn/docs/>

## What Changed In V2

V2 keeps one public router, aligns the public catalog to Agently's native capability surfaces, and validates both trigger choice and implementation quality.

Key rules:

- unresolved product or workflow requests start with `agently-playbook`
- structured output must prefer `.output(...)` and `ensure_keys`
- repeated result consumption must prefer `get_response()`
- explicit multi-stage quality loops and resumable workflows must prefer `TriggerFlow`

## Public Catalog

- `agently-playbook`
  Top-level router for unresolved model-powered product, assistant, internal-tool, or workflow requests.
- `agently-model-setup`
  Model connection, dotenv-based provider config, and OpenAI-compatible transport setup.
- `agently-prompt-management`
  Prompt composition, prompt config, mappings, and reusable request-side prompt structure.
- `agently-output-control`
  Output schema, field ordering, required keys, and structured output reliability.
- `agently-model-response`
  Response lifecycle, `get_response()`, parsed results, metadata, and streaming consumption.
- `agently-session-memory`
  Session-backed continuity, memo, restore, and request-side conversational state.
- `agently-agent-extensions`
  Tools, MCP, FastAPIHelper, `auto_func`, and `KeyWaiter`.
- `agently-knowledge-base`
  Embeddings plus Chroma-backed indexing, retrieval, and retrieval-to-answer flows.
- `agently-triggerflow`
  TriggerFlow orchestration, state, runtime stream, sub flows, and workflow-side model execution.
- `agently-migration-playbook`
  Migration router for existing LangChain or LangGraph systems.
- `agently-langchain-to-agently`
  Direct LangChain agent-side migration guidance.
- `agently-langgraph-to-triggerflow`
  Direct LangGraph orchestration migration guidance.

## Install

Recommended first install:

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
```

Bundle installs:

`request-core`

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-model-setup
npx skills add AgentEra/Agently-Skills --skill agently-prompt-management
npx skills add AgentEra/Agently-Skills --skill agently-output-control
npx skills add AgentEra/Agently-Skills --skill agently-model-response
```

`request-extensions`

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-agent-extensions
npx skills add AgentEra/Agently-Skills --skill agently-session-memory
npx skills add AgentEra/Agently-Skills --skill agently-knowledge-base
```

`workflow-core`

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-triggerflow
npx skills add AgentEra/Agently-Skills --skill agently-output-control
npx skills add AgentEra/Agently-Skills --skill agently-model-response
npx skills add AgentEra/Agently-Skills --skill agently-session-memory
```

`migration`

```bash
npx skills add AgentEra/Agently-Skills --skill agently-playbook
npx skills add AgentEra/Agently-Skills --skill agently-migration-playbook
npx skills add AgentEra/Agently-Skills --skill agently-langchain-to-agently
npx skills add AgentEra/Agently-Skills --skill agently-langgraph-to-triggerflow
```

## Validation

V2 validates both routing and implementation quality:

- `validate/validate_catalog.py`
- `validate/validate_bundle_manifest.py`
- `validate/validate_trigger_paths.py`
- `validate/validate_native_usage.py`
- `validate/validate_live_scenarios.py`

Live validation auto-loads `.env` with `dotenv.find_dotenv()` and uses:

- `DEEPSEEK_BASE_URL`
- `DEEPSEEK_DEFAULT_MODEL`
- `DEEPSEEK_API_KEY`

## Repository Layout

- `skills/`
  V2 published skill payloads.
- `validate/`
  Shared V2 validators and fixtures.
- `spec/`
  Local author workspace, ignored and not published.
