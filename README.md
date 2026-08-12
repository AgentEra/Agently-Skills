# Agently Skills

Official installable skills for coding agents working with Agently.

Main framework repository: <https://github.com/AgentEra/Agently>  
Official documentation: <https://agently.tech/docs/en/> | <https://agently.cn/docs/>

## Compatibility

The default public catalog is the current Agently-Skills generation `v2`,
aligned with the Agently 4.1.4.7 development line and the compact 7-skill
structure.

Machine-readable compatibility support lives in `compatibility/support.json`.
The default branch keeps only the current public catalog so coding-agent skill
discovery does not retrieve retired Skills.

Historical catalog generations are preserved on dedicated archive branches
instead of the default branch. The frozen V1 catalog is archived on
`update/archive-legacy-v1-catalog` and last supports Agently `4.1.1`.

## What Is Agently?

Agently is a framework for building model-powered applications and workflows.
It provides native surfaces for model requests, provider settings, prompt
composition, structured output, Action Runtime, MCP, knowledge-base flows,
TriggerFlow orchestration, and Dynamic Task DAG execution.

## What Is Agently-Skills?

Agently-Skills is the official skills package for coding agents that need to
build with Agently.

It is not the same thing as the framework-side `SkillLibrary`, `TaskContext`,
and AgentExecution Skill path inside the Agently runtime:

- `Agently-Skills` - guidance bundles for coding agents such as Codex and Claude Code
- Agently `SkillLibrary` - immutable installed Skill revision storage;
  `TaskContext` and `ContextReader` expose task-scoped context, while
  AgentExecution owns Skill binding, route selection, and execution lifecycle

Individual skill directories are standard `SKILL.md` packages with optional
references, examples, outputs, and scripts. Detailed API guidance belongs in
those skill packages and their one-level reference files, not in this repository
README.

## Current Catalog

The default catalog contains 7 public skills:

- `agently` - top-level router for unresolved model-powered product,
  assistant, internal-tool, automation, evaluator, workflow, or project-structure
  refactor requests.
- `agently-design` - cross-layer system design, review, optimization, and
  request-chain audit across ModelRequest contracts, evidence and identity
  boundaries, lifecycle, pressure, and observability.
- `agently-request` - request-side model setup, provider settings, prompt
  management, structured output, response reuse, streaming consumption, session
  memory, embeddings, knowledge-base indexing, retrieval, and retrieval-backed
  answers.
- `agently-runtime` - Action Runtime, built-in action packages, tool
  compatibility, MCP, ExecutionResource lifecycle, service exposure,
  auto-function helpers, and `KeyWaiter`.
- `agently-dynamic-task` - Dynamic Task DAG planning, `TaskDAG` validation,
  resolver handlers, and `TaskDAGExecutor` execution through
  `Agently.create_dynamic_task(...)`.
- `agently-triggerflow` - explicit orchestration, branching, concurrency,
  approvals, waiting and resume, runtime stream, restart-safe execution, mixed
  sync/async function or module orchestration, and graph-friendly workflow
  definitions.
- `agently-migration` - migration from LangChain, LangGraph, LlamaIndex,
  CrewAI, or similar systems into Agently-native request/runtime or TriggerFlow
  layers.

Use the current `skills/` directory as the default discovery surface. Do not add
archived catalog branches, historical directories, or retired Skill folders to a
coding agent's normal search path.

## Install

Choose the target agent first. The recommended path is to install one bundle
into one agent-specific skill directory, for example Codex:

```bash
export AGENT=codex
```

Use `AGENT=claude`, `AGENT=cursor`, or another supported agent when that is your
actual target.

`app`
Default bundle for building new Agently applications:

```bash
for skill in \
  agently \
  agently-design \
  agently-request \
  agently-runtime \
  agently-dynamic-task \
  agently-triggerflow
do
  npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill "$skill" -y
done
```

`migration`
Bundle for moving existing LangChain, LangGraph, LlamaIndex, CrewAI, or similar
systems into Agently. Install the `app` bundle first, then add the migration
skill:

```bash
npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill agently-migration -y
```

Install only the router when you want the smallest possible starting point:

```bash
npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill agently -y
```

Inspect the default public catalog:

```bash
npx skills add . --list
```

The default listing and standard install path expose only the current 7-skill
catalog.
