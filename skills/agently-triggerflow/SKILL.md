---
name: agently-triggerflow
description: Use when the main task is workflow orchestration in Agently, including TriggerFlow branching, concurrency, runtime data, runtime stream, sub flows, execution state, and workflow-side model execution.
---

# Agently TriggerFlow

Use this skill when the solution clearly needs orchestration semantics rather than one request family.

## Native-First Rules

- prefer TriggerFlow for explicit multi-stage quality loops, branching, concurrency, waiting/resume, or restart-safe execution
- keep workflow stages visible instead of hiding nested request loops
- combine with `agently-output-control` and `agently-model-response` when a workflow step needs those surfaces

## Anti-Patterns

- do not invent a custom event bus or state machine before checking TriggerFlow
- do not hide draft/judge/revise or similar loops inside one opaque helper

## Read Next

- `references/overview.md`
