---
name: agently-triggerflow-execution-state
description: Use only when the main task is saving, loading, or resuming one running TriggerFlow execution instance, including `execution.save()`, `execution.load()`, restoring waiting or ready result state, continuing after restore, loading from dict/JSON/YAML/file, or reinjecting runtime resources.
---

# Agently TriggerFlow Execution State

This skill is the runtime-instance persistence leaf inside the TriggerFlow domain. It focuses on `execution.save()`, `execution.load()`, resume-after-restore, waiting-interrupt recovery, ready-result recovery, file or string state loading, and runtime-resource reinjection. It does not decide whether the user should use TriggerFlow in the first place, and it does not cover flow-definition export/import or Mermaid.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- `execution.save()`
- `execution.load()`
- saving to or loading from dict, JSON string, YAML string, JSON file, or YAML file
- restoring waiting executions
- restoring executions whose final result is already ready
- using `continue_with(...)` after restore
- understanding what execution state contains and what it does not contain
- reinjecting runtime resources after restore

Do not use this skill for:

- `get_flow_config()`, `get_json_flow()`, `get_yaml_flow()`, or Mermaid
- blueprint copy and definition export/import
- choosing between `runtime_data`, `flow_data`, and runtime-resource placement
- provider setup, model schema design, or non-TriggerFlow persistence topics

## Workflow

1. Start with [references/state-surfaces.md](references/state-surfaces.md) to distinguish execution state from flow config and from general state-placement design.
2. If the task is about save/load roundtrip, read [references/save-load-roundtrip.md](references/save-load-roundtrip.md).
3. If the task is about waiting flows, pending interrupts, or resume-after-restore, read [references/waiting-and-resume.md](references/waiting-and-resume.md).
4. If the task is about restoring a suspended business workflow or conversation after restart, read [references/business-restore-recipes.md](references/business-restore-recipes.md).
5. If the task is about runtime resources after restore, read [references/runtime-resource-reinjection.md](references/runtime-resource-reinjection.md).
6. If behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

Execution state is the saved runtime surface of one execution instance.

It captures:

- execution status
- runtime data
- flow data snapshot
- pending interrupts
- last signal
- final result readiness and value
- resource key names

It does not carry executable resource objects themselves.

So the standard restore pattern is:

1. rebuild or reuse the correct flow definition
2. create a fresh execution
3. load the saved execution state
4. reinject any required runtime resources
5. continue or read the result

In real systems, a suspended workflow usually needs more than `execution.load(...)` alone.

Typical business restore sequence:

1. restore or rebuild the correct flow definition
2. create a fresh execution on that definition
3. load the saved execution state
4. reinject runtime resources
5. if the execution is waiting, inspect interrupts and continue it
6. if the result is already ready, read the result directly

## Selection Rules

- resume a waiting execution later -> `execution.save()` then `execution.load()` on a fresh execution
- restore a completed execution whose result was already ready -> `execution.load()` then `get_result()` / `async_get_result()`
- persist to transportable artifact -> save to JSON or YAML file
- restore from in-memory payload -> load from dict or JSON/YAML string
- restored execution needs runtime-only tools or services -> pass `runtime_resources=...` to `load(...)` or reinject before continuing
- choosing where state or resources should live before persistence -> use `agently-triggerflow-state-and-resources`
- definition itself must be exported or imported -> use `agently-triggerflow-config`, not this skill

## Important Boundaries

- execution state is for one running or completed execution, not the reusable flow definition
- runtime resources are represented only by `resource_keys`, not by serialized callable objects or clients
- waiting interrupts can be restored and resumed, but they still need the proper execution definition and resources in place
- flow config and execution state are complementary, not interchangeable

## References

- `references/source-map.md`
- `references/state-surfaces.md`
- `references/save-load-roundtrip.md`
- `references/waiting-and-resume.md`
- `references/business-restore-recipes.md`
- `references/runtime-resource-reinjection.md`
- `references/troubleshooting.md`
