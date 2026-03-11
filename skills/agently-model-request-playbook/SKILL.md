---
name: agently-model-request-playbook
description: Use when analyzing a business requirement around one Agently model request or request-adjacent capability, especially to decide whether the solution should stay a standard single request, become a high-quality structured or streamed request, add tools or MCP, add knowledge-base or RAG retrieval, add session continuity, expose FastAPIHelper endpoints, become a multi-agent design, or escalate into TriggerFlow.
---

# Agently Model Request Playbook

This skill is the scenario-routing entry point for model-request-side work in Agently. Use it when the request starts from business needs rather than one specific API. It helps choose the right request skill or skill combination. It does not replace the implementation skills themselves.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- deciding how a standard Agently model request should be built
- deciding how a higher-quality request should be upgraded for structure, streaming, or reuse
- deciding which parts belong to Agently and which parts belong to business logic
- deciding when to add tools, MCP, knowledge-base or RAG retrieval, session continuity, prompt config, or FastAPI exposure
- deciding when the problem has outgrown one request and should escalate to TriggerFlow

Do not use this skill for:

- direct API-level implementation details
- provider-specific setup details
- standalone TriggerFlow workflow design

## Workflow

1. Start with [references/standard-request-path.md](references/standard-request-path.md) when the requirement still looks like one ordinary model request.
2. Read [references/high-quality-request-path.md](references/high-quality-request-path.md) when the request must be more reliable, structured, streamable, or reusable.
3. Read [references/ownership-and-escalation.md](references/ownership-and-escalation.md) when the real question is who owns which part of the solution and when the request should be upgraded.
4. Read [references/common-business-patterns.md](references/common-business-patterns.md) when the requirement starts from business scenarios such as extraction, tool use, retrieval-augmented answer, or service exposure.
5. Read [references/current-skill-map.md](references/current-skill-map.md) to choose the implementation skill or skill combination.
6. Switch to the selected implementation skill and do the actual coding there.

## Routing Rules

- provider setup, auth, proxy, request options, or minimal verification -> `agently-model-setup`
- prompt slots, request-vs-agent prompt state, mappings, attachments, or low-level chat-history composition -> `agently-input-composition`
- output schema, structured streaming, response reuse, or response consumption -> `agently-output-control`
- embeddings only, offline indexing, or online query embedding -> `agently-embeddings`
- local tools, built-in tools, tool loop, or tool logs -> `agently-tools`
- MCP server tools or MCP transport registration -> `agently-mcp`
- Chroma-backed knowledge base, retrieval, or retrieval-to-answer -> `agently-knowledge-base-and-rag`
- session-backed continuity or memory restore after restart -> `agently-session-memo`
- prompt templates as YAML or JSON config -> `agently-prompt-config-files`
- FastAPIHelper endpoint exposure -> `agently-fastapi-helper`
- multiple specialized agents, reviewer-writer, planner-worker, or parallel experts -> `agently-multi-agent-patterns`
- the requirement has outgrown one request and now needs multi-step async workflow control -> `agently-triggerflow-playbook`

## Core Principles

- single-request-first: solve the problem with one high-quality request before escalating into workflow orchestration
- async-first: if the runtime can use async APIs, prefer async request and response handling
- explicit escalation: add tools, retrieval, memory, service exposure, or TriggerFlow only when the business need clearly requires it

## References

- `references/source-map.md`
- `references/standard-request-path.md`
- `references/high-quality-request-path.md`
- `references/ownership-and-escalation.md`
- `references/common-business-patterns.md`
- `references/current-skill-map.md`
