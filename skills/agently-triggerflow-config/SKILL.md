---
name: agently-triggerflow-config
description: Use when exporting, importing, copying, or inspecting TriggerFlow definitions, including `save_blue_print()`, `load_blue_print()`, `get_flow_config()`, `get_json_flow()`, `get_yaml_flow()`, `load_json_flow()`, `load_yaml_flow()`, Mermaid visualization, or exported TriggerFlow contract metadata.
---

# Agently TriggerFlow Config

This skill covers TriggerFlow definition-level export, import, copy, and inspection. It focuses on blueprint copy, flow-config roundtrip, JSON or YAML flow files, handler registration for restored flows, and Mermaid visualization. It does not cover execution save/load, pause-and-resume runtime state persistence, or provider-specific model configuration.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- `save_blue_print()` and `load_blue_print()`
- `get_flow_config()`
- `get_json_flow()` and `get_yaml_flow()`
- `load_flow_config()`, `load_json_flow()`, and `load_yaml_flow()`
- `to_mermaid(mode="simplified" | "detailed")`
- exported TriggerFlow contract metadata in flow config and Mermaid
- flow-definition roundtrip across processes or repositories
- understanding what is serializable in a TriggerFlow definition and what must be re-registered or reinjected at runtime

Do not use this skill for:

- execution `save()` / `load()` after a workflow has already started running
- interrupt persistence and resume-after-restart mechanics
- model provider setup or output-schema design
- runtime-stream lifecycle as the primary topic

## Workflow

1. Start with [references/definition-surfaces.md](references/definition-surfaces.md) to choose between blueprint copy, config export, and Mermaid inspection.
2. If the task is about JSON or YAML roundtrip, read [references/export-import-roundtrip.md](references/export-import-roundtrip.md).
3. If the task is about what must be registered again after loading, read [references/handler-registration.md](references/handler-registration.md).
4. If the task is about contract metadata in exported config or Mermaid, read [references/contract-metadata.md](references/contract-metadata.md).
5. If the task is about diagrams and inspection, read [references/mermaid-usage.md](references/mermaid-usage.md).
6. If behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

TriggerFlow config APIs work on workflow definitions, not execution instances.

The main surfaces are:

- blueprint copy for in-process definition reuse
- flow config for serializable definition export and import
- Mermaid for inspection and communication

Use them like this:

- same process, same Python runtime, no file roundtrip required -> blueprint copy
- transport, repository storage, or human-editable artifacts -> JSON or YAML flow config
- architecture review or visual debugging -> Mermaid

## Selection Rules

- in-memory reusable definition object -> `save_blue_print()` / `load_blue_print()`
- serializable dictionary form -> `get_flow_config()`
- share or store the definition as a file -> `get_json_flow()` or `get_yaml_flow()`
- restore a definition from stored JSON or YAML -> `load_json_flow()` or `load_yaml_flow()`
- inspect the structure visually with grouped nodes -> `to_mermaid(mode="simplified")`
- inspect internal nodes and callable labels in more detail -> `to_mermaid(mode="detailed")`
- exported artifacts should preserve contract metadata for inspection or schema discussion -> flow config and Mermaid
- restored flow needs chunk handlers or condition handlers -> register them before loading the config
- restored flow needs runtime resources -> inject them again at runtime after loading
- workflow has already started and should resume later -> use a separate execution-state skill, not this one

## Important Boundaries

- flow config serializes the definition, not a running execution
- flow config preserves exported contract metadata, schema labels, and system interrupt metadata
- loading config restores contract metadata for inspection and re-export, but it does not reconstruct live runtime validators from the original Python contract types
- runtime resources are not serialized into flow config
- non-serializable handlers such as anonymous lambdas may still appear in Mermaid, but they are not valid export targets for `get_flow_config()`
- loading a config rebuilds the flow definition and then recompiles handlers against the currently registered callable registry

## References

- `references/source-map.md`
- `references/definition-surfaces.md`
- `references/export-import-roundtrip.md`
- `references/handler-registration.md`
- `references/contract-metadata.md`
- `references/mermaid-usage.md`
- `references/troubleshooting.md`
