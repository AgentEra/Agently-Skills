---
name: agently
description: Route ambiguous product, document, or Agentic work to the right design or implementation skill. Use for unresolved owner/project shape, mixed specialties or explicit low-frequency TaskDAG or DynamicTask requests. Clear tasks use their specialist directly; conversation expression, progress and handoffs use agently-collaboration alongside any task.
---

# Agently

Start here when the owner or working method is unclear, or several specialties
share one work item. First distinguish human product/document outcomes from
model-service behavior. Route clear product work directly to `agently-product-design`;
no model, Agently runtime or framework migration is required. For model systems,
choose the smallest suitable owner before files or mechanisms; use Agently-native
mappings only when Agently is in scope. Respect another selected stack.

When an Agently developer needs to understand model-node duties, tune execution
effects, check data flow or redundant context, or judge model/Host ownership,
use collaborative review without waiting for the phrase "Prompt review".
Route through `agently-agentic-design` for the highlighted flow and handoffs, and
`agently-request` for related Prompt tables grouped by readability and dependency.
Keep unrelated mechanical work outside this review method.

## Shared coordination

Use [Conversation and Collaboration](../agently-collaboration/SKILL.md) alongside
any task for reader-oriented communication, progress, decisions and handoffs.
It can be selected directly without this router. Specialist Skills retain their
execution and acceptance criteria; reuse one work record across them. If the
companion is unavailable, follow the host's base guidance and existing task
record; routing does not require installation or a new tracking system.

## Workflow

The following owner workflow applies to model-powered systems. For non-model
product or writing tasks, route to the product Skill and continue its method.

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

- Product goals, role/behavior coverage, interface/component/layout design,
  document readability or diagrams use `agently-product-design`. It has four
  conditional modules, not four mandatory phases or Agents.
- For mixed product + Agentic work, pass role goals, business constraints,
  observable event meanings, selected decisions and unresolved evidence to the
  next owner. Load only the necessary phase. Runtime traces prove system events;
  product walkthroughs prove how people understand and act on them.

- One request family—provider setup, prompt, structured output, LongContent,
  auto_continue, TTS/STT audio, result reuse, session memory, embeddings, or
  retrieval—uses `agently-request`.
- AgentExecution plugins, final policies, Actions, Shell, MCP, ExecutionResource, TaskWorkspace, RecordStore, service
  exposure, RuntimeEvent, or DevTools uses `agently-runtime`.
- Process-local task lifetime, sync/async bridging, loop-neutral handles,
  settlement, replay channels, or local listeners uses `agently-stage`.
- Cross-owner architecture, request/value/event topology, evidence and identity
  boundaries, lifecycle, pressure, or information-loss audit uses
  `agently-agentic-design`.
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
- Cross-layer topology audit methods live in `agently-agentic-design`, especially its
  `../agently-agentic-design/references/execution-topology-validation.md`.

## Core Ownership Rules

- `ModelRequest` owns one model interaction and its prompt/output contract.
- `AgentExecution` owns one Agent run and its selected producer, controls,
  result and streams. In 4.1.4.8, `request`, `plan`, `long_content` and
  `long_task` are plugins; read the runtime Skill's
  [execution contract](../agently-runtime/references/agent-execution.md).
- `agent.create_task(...)` returns a long-task AgentExecution draft. Its
  producer owns planning, evidence and replan; released AgentTask imports
  remain compatible.
- `AudioModelRequest` owns independent TTS/STT drivers. Agent audio calls and
  audio-dependent Execution plugins require an explicit audio binding.
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
