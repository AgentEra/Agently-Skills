# Agently Skills

Official installable skills for coding agents working with
[Agently](https://github.com/AgentEra/Agently).

Documentation: [English](https://agently.tech/docs/en/) |
[中文](https://agently.cn/docs/)

## Compatibility

The default branch publishes catalog generation `v3`, aligned with the Agently
`4.1.4.7` public release. It contains only the current 7-skill catalog.

Historical catalogs are frozen on archive branches:

- `v2`: `update/archive-v2-catalog`, last supported Agently `4.1.4.7`
- `v1`: `update/archive-legacy-v1-catalog`, last supported Agently `4.1.1`

See [`compatibility/support.json`](compatibility/support.json) for the
machine-readable compatibility contract. Archive branches are for rollback and
historical inspection, not new installations.

## Current Catalog

- `agently` - route and shape model-powered assistants, internal tools,
  automations, evaluators, and workflows when the correct owner layer is still
  unclear. Low-frequency TaskDAG guidance also starts here.
- `agently-design` - design and audit non-trivial systems across owner layers,
  request/value/event topology, evidence, identity, lifecycle, pressure, and
  observability.
- `agently-request` - configure model requests, prompts, structured output,
  response consumption, session memory, embeddings, and retrieval.
- `agently-runtime` - use Action Runtime, MCP, ExecutionResource,
  TaskWorkspace, RecordStore, service adapters, and optional DevTools.
- `agently-stage` - work with process-local task lifetime, sync/async bridges,
  loop-neutral handles, streams, replay channels, events, and backpressure.
- `agently-triggerflow` - build explicit branching, concurrent, resumable, and
  restart-safe workflows with inspectable runtime state and events.
- `agently-migration` - map LangChain, LangGraph, LlamaIndex, CrewAI, and
  similar systems to Agently-native owner layers.

TaskDAG is intentionally not a standalone Skill in v3. It is a low-frequency
foundation for submitted or model-generated acyclic graph data; begin with
`agently`, then add `agently-design` or `agently-triggerflow` only when the
cross-layer boundary or execution substrate needs separate treatment.

## Install

Choose the target coding agent first, for example:

```bash
export AGENT=codex
```

Install the `app` bundle for new Agently applications:

```bash
for skill in \
  agently \
  agently-design \
  agently-request \
  agently-runtime \
  agently-stage \
  agently-triggerflow
do
  npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill "$skill" -y
done
```

For migration work, install the `app` bundle and then add:

```bash
npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill agently-migration -y
```

For the smallest discovery surface, install only the router:

```bash
npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill agently -y
```

List the current public catalog with:

```bash
npx skills add . --list
```
