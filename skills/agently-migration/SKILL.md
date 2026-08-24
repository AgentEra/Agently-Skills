---
name: agently-migration
description: "Use when migrating an existing LangChain, LangGraph, LlamaIndex, or CrewAI system into Agently and mapping each source behavior to its actual request, runtime, context/storage, or TriggerFlow owner."
---

# Agently Migration

Use this Skill only when a source-framework system already exists. Do not
translate class names one for one. Inventory the source's observable semantics,
assign each to an Agently owner, and preserve those semantics with representative
before/after evidence.

## Read the Source-Specific Map

- LangChain agents, models, prompts, structured output, tools, retrieval, or
  short-term memory: [langchain-to-agently.md](references/langchain-to-agently.md).
- LangGraph graphs, state, checkpoints, interrupts, streams, or subgraphs:
  [langgraph-to-triggerflow.md](references/langgraph-to-triggerflow.md).
- LlamaIndex agents, loaders, indexes, retrievers, query engines, memory, or
  Workflows: [llamaindex-to-agently.md](references/llamaindex-to-agently.md).
- CrewAI Agents, Tasks, Crews, Processes, Flows, tools, memory, or knowledge:
  [crewai-to-agently.md](references/crewai-to-agently.md).

## Agently Owner Map

| Source behavior | Agently owner |
|---|---|
| One model call, prompt contract, structured result, or response stream | `agently-request` / ModelRequest |
| Model-callable tool, MCP server, sandbox, browser, database, or live client | `agently-runtime` / ActionRuntime + ExecutionResource |
| Conversation continuity | Session / SessionMemory |
| Durable records, links, retrieval, checkpoints, or snapshots | RecordStore |
| Cross-source task evidence and bounded reads | TaskContext + ContextSource + ContextReader |
| Stable multi-stage topology, branches, joins, loops, waits, resume, or runtime events | `agently-triggerflow` / TriggerFlow |
| Model-owned bounded planning, evidence, verification, and replan | AgentTask through AgentExecution |

Do not add TriggerFlow around a single request or Action. Do not flatten a real
workflow into one prompt. A source “agent” is not automatically an Agently
AgentTask, and a nominal source “workflow” is not automatically orchestration;
classify its behavior.

## Migration Method

1. Record source inputs/outputs, model calls, tool calls and side effects, state
   keys and lifetimes, topology, concurrency, retry/error behavior, stream
   events, checkpoint/resume behavior, memory, retrieval, and authorization.
2. Separate semantic work from deterministic work. Model-owned intent,
   relevance, planning, and synthesis use ModelRequest output control; host code
   owns types, arithmetic, offered-key membership, authorization, and effects.
3. Draw the target owner, node, and edge ledgers before choosing files. Preserve
   externally consumed event and result contracts or introduce an explicit
   adapter at the boundary.
4. Migrate one representative vertical slice. Compare source and target traces,
   final artifacts, state transitions, interruption/recovery behavior, and
   failure semantics before broad replacement.
5. Remove source-framework shims once their last real consumer is migrated.
   Keep a compatibility adapter only when it owns a released external contract.

## Required Cautions

- Preserve checkpoint, interrupt, idempotency, streaming, and subflow semantics
  explicitly; matching node names is not evidence of equivalent behavior.
- Keep live resources and secrets out of serialized execution state. Persist
  descriptors and reconstruct through host-owned providers.
- Keep identity joins host-owned. Give the model one offered selection key and
  rejoin canonical records after validation.
- Do not replace source semantic routing or evaluation with keywords, regex,
  snapshots, or hardcoded business mappings.
- If Agently lacks a protocol seam needed to preserve an essential source
  behavior, report the capability gap. Do not conceal it behind a prompt or a
  deterministic substitute.
