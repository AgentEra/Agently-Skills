# Agently Skills

Official installable skills for coding agents working with
[Agently](https://github.com/AgentEra/Agently).

Documentation: [English](https://agently.tech/docs/en/) |
[中文](https://agently.cn/docs/)

## Compatibility

The current catalog is generation `v3`, aligned with Agently
`4.1.4.10`. It contains nine canonical skills plus one deprecated forwarding entry. The product-design and collaboration Skills have no Agently runtime dependency.

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
- `agently-collaboration` - cross-task conversation expression, complete taskboard progress, decisions, change history and handoffs; independent of the framework or task router.
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

`agently` owns task routing; `agently-collaboration` owns how the coding agent explains work, progress, decisions and handoffs across tasks. The latter can be selected directly alongside any specialty. Product design owns human goals, UI and reading acceptance; Agentic design owns model/Host/workflow contracts. Runtime progress events remain Agentic concerns; their presentation and comprehension belong to product design. Mixed tasks reuse one record and load only the current specialty.

The former `app-design-method` is now `agently-product-design`, without an old-name alias. Only `agently-design` remains temporarily deprecated. On the next update, verify the replacement and active callers before removing that entry; no scheduled cleanup and no rewriting historical evidence.

## Install

Standard local installations select the canonical `app`, `migration`, `product-design` and/or `collaboration` bundles; `design-compat` is only for an explicitly needed old caller. Before updating, compare local changes and preserve useful development supplements with a declared feature/version, capability check and known evidence limits. Do not treat preview guidance as released support. Retire redundant local aliases after a recoverable backup; keep distinct host-specific workflows. Spotkit is an optional external illustration Skill used by product design, not a required Agently dependency.

### Codex display language

The nine canonical skills share one [English/Chinese UI dictionary](locales/skill-ui.json). Shipped metadata uses English; technical skill IDs and invocation names stay unchanged. Codex reads one static display name, so this tool selects the language at installation/update time rather than following each conversation's language.

From a checkout of the version you intend to install, using Python 3.10+ with PyYAML:

```bash
python scripts/install.py --locale zh-CN
python scripts/install.py
python scripts/install.py --locale en --ui-only
```

The first command installs/updates all nine canonical skills in `$CODEX_HOME/skills` (or `~/.codex/skills`) with Chinese UI. The second reuses the saved language. The third changes only existing skills' UI to English. Use `--skills agently-product-design` for a standalone install, `--dest PATH` for another skill root, and `--dry-run` to inspect changes.

The root-level `.agently-skills-ui.json` stores the language and managed-file baselines. Existing policy, dependencies, icons and other UI fields remain intact. First adoption preserves differing local files as supplements; subsequent upstream changes update unchanged files and stop before writing on overlapping local changes. No untracked files or retired aliases are deleted. A backup and receipt are saved beside the target skill root in `skill-update-backups/`. This tool installs from the checkout; it does not fetch remote updates. After using another installer, run `--ui-only` to reapply your saved language.

Maintainers edit the dictionary, run `python scripts/install.py --write-defaults`, and validate with `--check` plus `python -m unittest discover -s validate -p test_skill_ui_install.py`. Avoid changing SKILL.md identities to translate the interface.

### Conversation guidance across tasks

Install `agently-collaboration` for conversation expression, progress and handoffs
without a framework dependency:

```bash
python scripts/install.py --skills agently-collaboration
```

For persistent basic behavior, merge its short
[session guidance](skills/agently-collaboration/assets/session-guidance.md) into
the host's supported global instruction entry, preserving existing rules. In
Codex, inspect `$CODEX_HOME/AGENTS.override.md` and `AGENTS.md` (default root:
`~/.codex`) to identify the active file. Update the marked block in place; do not
overwrite the whole file or create a new override that hides existing guidance.
Other coding agents require their own supported global entry. Skill installation
alone does not make the full body always loaded, and this installer does not
edit global instructions automatically. New Codex runs reload the instruction
chain; check the active host after updating.

The short block orients reports before the full current board and routes to the
installed Skill when needed. Professional execution stays in task Skills; full
change history remains in existing records and is expanded when relevant. On
updating from the former router-owned guidance, inspect and back up any local
changes to `agently/references/multi-round-collaboration.md`, then remove that
obsolete copy after migrating callers. The generic installer intentionally does
not delete files absent from the new source.

### Other installers

Choose the target coding agent first, for example:

```bash
export AGENT=codex
```

Install the `app` bundle for new Agently applications:

```bash
for skill in \
  agently \
  agently-collaboration \
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
