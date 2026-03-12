---
name: agently-langchain-to-agently
description: Use when directly migrating LangChain agent-side surfaces into Agently after the migration is already known to stay on the LangChain side rather than LangGraph orchestration, such as `create_agent`, tools, structured output, middleware, retrieval, or short-term memory.
---

# Agently LangChain To Agently

This skill is the direct migration leaf for LangChain's agent-side surface into Agently. Use it when the source problem is already known to belong to LangChain agent migration rather than LangGraph orchestration. It focuses on `create_agent`, tools, structured output, short-term memory, middleware-like behavior, retrieval, service exposure, and LangChain-side multi-agent patterns. It does not cover graph-orchestration-first migration from LangGraph; use `agently-langgraph-to-triggerflow` for that.

Prerequisite: Agently `>= 4.0.8.5`.

## When To Use This Skill

Use this skill for:

- direct migration of a known LangChain agent-side design into current Agently capabilities
- `create_agent`
- `response_format`, `ProviderStrategy`, or `ToolStrategy`
- tools
- structured output
- short-term memory
- middleware or guardrails
- human approval or HITL behavior attached through middleware
- retrieval or RAG
- service exposure around an agent
- LangChain-side handoff or specialist-agent patterns

## When Not To Use This Skill

- unresolved migration-entry work where you still need to decide between LangChain-side and LangGraph-side migration
- `StateGraph`, interrupts, persistence, or subgraph migration as the main problem
- direct TriggerFlow API implementation as the main problem
- non-migration Agently implementation work that already starts from Agently

## Workflow

1. Start with [references/concept-map.md](references/concept-map.md) to translate LangChain concepts into the current Agently skill tree.
2. Read [references/common-migration-recipes.md](references/common-migration-recipes.md) when the source code resembles a common LangChain production shape.
3. Read [references/non-1to1-differences.md](references/non-1to1-differences.md) when the migration should change design rather than mimic syntax.
4. Read [references/current-skill-map.md](references/current-skill-map.md) to choose the target Agently skill combination.
5. If the source code is actually graph-orchestration-heavy, switch to `agently-langgraph-to-triggerflow`.
6. If behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

LangChain's high-level agent API bundles several concerns together.

In Agently, the same solution usually splits across several clearer capability surfaces:

- request and provider setup
- input composition
- output control
- tools or MCP
- session continuity
- retrieval
- service exposure
- optional multi-agent or workflow orchestration

So the migration target is usually:

- fewer all-in-one abstractions
- more explicit capability composition

## Selection Rules

- LangChain `create_agent` with one main model path -> `agently-model-request-playbook`
- `response_format` or structured output strategy -> `agently-output-control`
- tools or tool loop -> `agently-tools`
- MCP-backed tool ecosystem -> `agently-mcp`
- short-term conversational continuity -> `agently-session-memo`
- retrieval or KB-backed answer -> `agently-knowledge-base-and-rag`
- service exposure through FastAPI -> `agently-fastapi-helper`
- middleware-based approval, guardrail escalation, or resume-after-approval behavior -> `agently-triggerflow-interrupts-and-stream` and often `agently-triggerflow-playbook`
- handoff or specialist-agent design -> `agently-multi-agent-patterns`
- the source design is actually a workflow rather than one agent -> `agently-triggerflow-playbook`
- the migration still needs a top-level LangChain-vs-LangGraph routing decision -> `agently-langchain-langgraph-migration-playbook`

## Important Boundaries

- there is no single Agently `create_agent` replacement that absorbs all LangChain concerns
- LangChain `ProviderStrategy` and `ToolStrategy` do not map to one Agently strategy enum; in Agently the target is usually explicit output schema plus provider and request choices
- LangChain middleware often becomes explicit request logic, output control, tool policy, or workflow logic in Agently
- short-term memory does not map literally to LangGraph thread/checkpointer semantics; in Agently, conversational continuity usually belongs to session-backed memory
- middleware-based human approval usually becomes explicit interrupt-and-resume workflow design, not one middleware list
- do not migrate old `langchain-classic` abstractions literally if the Agently target can be simpler

## References

- `references/source-map.md`
- `references/concept-map.md`
- `references/common-migration-recipes.md`
- `references/non-1to1-differences.md`
- `references/current-skill-map.md`
- `references/troubleshooting.md`
