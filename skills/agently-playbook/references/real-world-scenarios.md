# Real-World Scenarios

Use this page when the requirement starts from a realistic product or operations scenario rather than a low-level technical shape.

The goal is not to mirror every trend word in the AI ecosystem. The goal is to route common real-world scenarios into the current Agently skill tree without exceeding Agently's actual capability boundary. If the scenario fits that boundary, prefer solving it with the narrowest viable Agently capability path.

## 1. Research, Monitoring, Or Investigative Work

Typical fit:

- web research assistant
- market or competitor monitoring
- issue investigation
- evidence gathering before synthesis

Typical Agently route:

- one request plus tools -> `agently-model-request-playbook` + `agently-tools`
- MCP-backed external systems -> add `agently-mcp`
- several specialists with one synthesizer -> `agently-multi-agent-patterns`
- long-running or checkpointed research workflow -> `agently-triggerflow-playbook`

This aligns with common orchestrator-worker research systems and parallel specialist branches, but should stay inside Agently's existing tools, MCP, multi-agent, and TriggerFlow surfaces.

## 2. Customer Support, Service Triage, Or Guided Resolution

Typical fit:

- support assistant with retrieval and memory
- classify, route, answer, or escalate
- approval or human handoff before sensitive actions

Typical Agently route:

- answer and retrieval -> `agently-model-request-playbook` + `agently-knowledge-base-and-rag`
- multi-turn continuity -> add `agently-session-memo`
- specialist routing or escalation roles -> `agently-multi-agent-patterns`
- human gate, wait, resume, or restart-safe orchestration -> `agently-triggerflow-playbook`

## 3. Document Processing, Extraction, And Batch Analysis

Typical fit:

- extract structured fields from documents
- batch-process many items
- send structured outputs into several downstream systems
- show progressive field updates while the request is still running

Typical Agently route:

- one extraction request -> `agently-model-request-playbook` + `agently-output-control`
- batch embedding or retrieval enrichment -> add `agently-embeddings` or `agently-knowledge-base-and-rag`
- many documents, worker fan-out, or staged processing -> `agently-triggerflow-playbook`

## 4. Report Drafting, Review, And Revision

Typical fit:

- draft -> critique -> revise
- several section workers plus one final summarizer
- structured review checklist before final release

Typical Agently route:

- reviewer-reviser or parallel specialists -> `agently-multi-agent-patterns`
- explicit structured handoffs -> add `agently-output-control`
- nested report sections or larger orchestration -> add `agently-triggerflow-playbook`

## 5. Approval-Centered Business Workflow

Typical fit:

- compliance or policy checks
- operator approval before execution
- workflow stops and resumes later
- service restart should not lose business state

Typical Agently route:

- workflow control -> `agently-triggerflow-playbook`
- interrupt and resume -> `agently-triggerflow-interrupts-and-stream`
- restart-safe definition and execution restore -> `agently-triggerflow-config` + `agently-triggerflow-execution-state`

## 6. Async Concurrency, Worker Pools, And Mixed Sync-And-Async Pipelines

Typical fit:

- several workers should run concurrently under one runtime
- bounded fan-out or item-wise processing
- sync and async functions must be orchestrated together
- some workflow steps do not call models at all

Typical Agently route:

- workflow-level planning -> `agently-triggerflow-playbook`
- repeatable workflow shapes -> `agently-triggerflow-patterns`
- state and resource boundaries -> `agently-triggerflow-state-and-resources`

This is inside Agently's practical scope even when the workflow is not "LLM everywhere". TriggerFlow can own the control flow and concurrency semantics.

## 7. Streaming Or Service-Facing Agent Endpoints

Typical fit:

- SSE or WebSocket agent output
- streamed workflow events to clients
- helper-based HTTP exposure around an existing backend

Typical Agently route:

- backend logic first -> choose the real owning skill
- transport exposure second -> add `agently-fastapi-helper`

Do not let transport become the architecture owner by mistake.
