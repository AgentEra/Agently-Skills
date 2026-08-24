---
name: agently
description: Use when a model-powered product, assistant, automation, evaluator, or workflow request still needs the right Agently owner, execution shape, or project boundary chosen. Also use for explicit low-frequency TaskDAG or DynamicTask requests.
---

# Agently

Start here when the request is expressed as product behavior rather than an
Agently API. Choose the smallest native owner before choosing files or
mechanisms. The request does not need to mention Agently.

## Workflow

1. Reduce the request to goals, inputs, outputs, side effects, evidence, and
   lifecycle needs.
2. Separate model-owned semantic decisions from host-owned validation,
   authorization, identity joins, arithmetic, and effects.
3. Assign each decision, state, and effect to one existing owner.
4. For non-trivial flows, map nodes, value/event edges, invariants, and the
   production need for every requested field and stage.
5. Implement async-first where the caller owns an async boundary; validate
   deterministic contracts separately from model-owned quality.
6. Report a framework gap when no native owner can carry a required invariant.
   Do not hide the gap behind business-specific glue or a pass-through facade.

## Route by Owner

- One request family—provider setup, prompt, structured output, result reuse,
  session memory, embeddings, or retrieval—uses `agently-request`.
- Actions, MCP, ExecutionResource, TaskWorkspace, RecordStore, service
  exposure, RuntimeEvent, or DevTools uses `agently-runtime`.
- Process-local task lifetime, sync/async bridging, loop-neutral handles,
  settlement, replay channels, or local listeners uses `agently-stage`.
- Cross-owner architecture, request/value/event topology, evidence and identity
  boundaries, lifecycle, pressure, or information-loss audit uses
  `agently-design`.
- Developer-owned progression, branching, concurrency, approval, wait/resume,
  retry, or restart-safe orchestration uses `agently-triggerflow`.
- Migration from LangChain, LangGraph, LlamaIndex, CrewAI, or a similar system
  uses `agently-migration`.
- Explicit model-generated or application-submitted acyclic DAG data is a
  low-frequency advanced case. Keep it here and read `references/task-dag.md`;
  do not introduce TaskDAG for ordinary Agent or workflow work.

## Read by Need

- Conditional project shapes and the full-stack reference asset:
  `references/project-framework.md`.
- TaskContext, ContextReader, TaskWorkspace, RecordStore, SkillLibrary, and the
  SkillsExecutor compatibility facade: `references/context-and-skills.md`.
- Submitted TaskDAG data and the DynamicTask convenience facade:
  `references/task-dag.md`.
- Simulation-first and real-model validation:
  `references/model-quality-validation.md`.
- Cross-layer topology audit methods live in `agently-design`, especially its
  `../agently-design/references/execution-topology-validation.md`.

## Core Ownership Rules

- `ModelRequest` owns one model interaction and its prompt/output contract.
- `AgentExecution` owns one Agent run and exposes result, text, stream, and
  metadata readers.
- `agent.create_task(...)` returns an AgentExecution draft whose internal
  AgentTask strategy owns planning, evidence, verification, repair, and replan.
- `ActionRuntime` owns model-callable operations; `ExecutionResource` owns live
  dependency lifetime.
- `TriggerFlow` owns application-visible orchestration and runtime signals.
- `TaskContext` owns task information and creates consumer-bound readers;
  `TaskWorkspace` owns files; `RecordStore` owns durable records and recovery;
  `SkillLibrary` owns immutable installed Skill revisions.
- `Agently.skills_executor` is management/context compatibility only. Do not
  recreate the removed generic Workspace, ContextBuilder, SkillsManager,
  Skills route/strategy, `skill_activation`, or `workspace_operation` owners.

## ModelRequest Boundary

For output that must satisfy a downstream interface:

- runtime facts go in `.input(...)`;
- authoritative schemas, signatures, and source facts go in `.info(...)`;
- transformation and call rules go in `.instruct(...)`;
- the exact consumed shape goes in `.output(...)`.

Declare the type, semantics, requiredness, enum/format/range, nullability, and
cross-field constraints for every consumed field. Let a structured
ModelRequest own prose-derived intent, routing, planning, relevance, or quality
judgment; let host code validate bounded enums/keys and perform effects.

Do not request hidden chain-of-thought. A bounded process field is justified
only when it has a named role, bounds, consumer, retention rule, and failure
behavior.

## Project and Validation Gate

Start one-request applications with composition, settings, the prompt contract,
and tests. Add workflows, services, Actions, local Skills, utilities, or
resources only for a current owner and consumer. A logical node is not
automatically a file or class.

Deterministic tests prove schemas, identities, lifecycle, accounting, file or
record effects, and safety. Semantic quality needs declared criteria and a
structured coding-agent, model, or human review. Classify criticality (hard
gate or soft target) separately from evaluation method (deterministic or
semantic).

For real-model claims, define criteria first, label simulations honestly, use
the smallest authorized representative run, and record raw facts separately
from judgment. Real traces override simulated expectations.

## Anti-Patterns

- Custom parsers, retry managers, state stores, or schedulers before checking
  the native owner.
- Keyword, substring, regex, tokenization, or hand-written score tables as the
  semantic owner.
- Unconsumed output fields, request stages, wrappers, or project directories.
- All-serial complex flows without dependency analysis.
- Full source, identity-heavy records, or raw metadata copied into every
  prompt.
- Canned answers, hidden expected-answer fixtures, or test-only production
  branches presented as framework capability evidence.
