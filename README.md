# Agently Skills

Official installable skills for coding agents working with
[Agently](https://github.com/AgentEra/Agently).

Documentation: [English](https://agently.tech/docs/en/) |
[中文](https://agently.cn/docs/)

## Compatibility

The current catalog is generation `v3`, aligned with Agently
`4.1.4.10`. It contains eight canonical skills plus one deprecated forwarding entry. The product-design Skill has no Agently runtime dependency.

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
- `agently-agentic-design` - design and audit non-trivial systems across owner layers,
  request/value/event topology, evidence, identity, lifecycle, pressure, and
  observability.
- `agently-product-design` - framework-independent product/solution design, role and behavior coverage, UI experience and document expression; four conditional modules.
- `agently-design` - deprecated forwarding entry to `agently-agentic-design`; inspect and retire on the next update.
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
`agently`, then add `agently-agentic-design` or `agently-triggerflow` only when the
cross-layer boundary or execution substrate needs separate treatment.

## Design ownership and composition

`agently` owns routing and cross-round progress, decisions, evidence status and handoffs. Product design owns human goals, UI and reading acceptance; Agentic design owns model/Host/workflow contracts. Runtime progress events remain Agentic concerns; their presentation and comprehension belong to product design. Mixed tasks reuse one record and load only the current specialty.

The former `app-design-method` is now `agently-product-design`, without an old-name alias. Only `agently-design` remains temporarily deprecated. On the next update, verify the replacement and active callers before removing that entry; no scheduled cleanup and no rewriting historical evidence.

## Install

Standard local installations select the canonical `app`, `migration` and/or `product-design` bundles; `design-compat` is only for an explicitly needed old caller. Before updating, compare local changes and preserve useful development supplements with a declared feature/version, capability check and known evidence limits. Do not treat preview guidance as released support. Retire redundant local aliases after a recoverable backup; keep distinct host-specific workflows. Spotkit is an optional external illustration Skill used by product design, not a required Agently dependency.

Choose the target coding agent first, for example:

```bash
export AGENT=codex
```

Install the `app` bundle for new Agently applications:

```bash
for skill in \
  agently \
  agently-agentic-design \
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

Install product design independently from a checkout containing this migration; no framework is required:

```bash
npx skills add . --agent "$AGENT" --skill agently-product-design -y
```
