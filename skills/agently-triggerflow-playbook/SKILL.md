---
name: agently-triggerflow-playbook
description: Use when building an Agently-based agent workflow or model-service system that already needs TriggerFlow-domain workflow orchestration, such as async workflow control, routing, concurrency, resume, interrupts, runtime stream, approvals, or model work inside a flow, and you need to choose the right TriggerFlow skill combination.
---

# Agently TriggerFlow Playbook

This skill is the scenario-routing entry point for TriggerFlow work in Agently. Use it when the application has already grown into workflow orchestration in the TriggerFlow domain rather than generic Agently architecture selection. It helps choose the right implementation skill or skill combination. It does not replace the implementation skills themselves.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- agent workflows, approval flows, long-running model-service pipelines, and LangGraph-like orchestration concerns that should be implemented with TriggerFlow
- deciding whether a business requirement should be implemented with TriggerFlow
- mapping a workflow requirement to the correct TriggerFlow skill
- deciding when TriggerFlow should be combined with `agently-model-setup` or `agently-output-control`
- selecting between general orchestration work, workflow-pattern work, state-and-resource work, sub-flow work, model-integration work, config work, execution-state work, and explicit interrupt or runtime-stream work

Do not use this skill for:

- direct API-level TriggerFlow implementation details
- provider setup or model-request configuration details
- standalone model output parsing without a TriggerFlow workflow

## Workflow

1. Start with [references/scenario-router.md](references/scenario-router.md) to map the business requirement to the right capability area.
2. Read [references/current-skill-map.md](references/current-skill-map.md) to choose the implementation skill or skill combination.
3. Switch to the selected implementation skill and do the actual coding there.

## Routing Rules

- signal-driven workflow primitives, event routing, execution entrypoints, or result semantics -> `agently-triggerflow-orchestration`
- router patterns, fan-out and fan-in, item-wise worker flows, safe loops, evaluator-optimizer, ReAct loops, or approval-gate workflow design -> `agently-triggerflow-patterns`
- state placement, flow-versus-execution sharing, runtime-resource boundaries, or restart-safe state design -> `agently-triggerflow-state-and-resources`
- isolated child workflow, explicit parent-child handoff, or `to_sub_flow(...)` boundary -> `agently-triggerflow-subflows`
- workflow step sends model requests, fans out model calls, or uses `delta` / `instant` inside the flow -> `agently-triggerflow-model-integration`
- specialized agent teams, planner-worker, reviewer-reviser, or parallel experts as the main workflow concern -> `agently-multi-agent-patterns`
- flow definition should be exported, imported, copied, or visualized -> `agently-triggerflow-config`
- a running execution should be saved, restored, resumed, or rehydrated with resources -> `agently-triggerflow-execution-state`
- a suspended workflow or conversation should be resumed after restart -> combine `agently-triggerflow-config` + `agently-triggerflow-execution-state`, and add `agently-session-memo` if memory lives outside the execution
- human approval, external resume, waiting execution, or live runtime stream -> `agently-triggerflow-interrupts-and-stream`
- workflow step needs provider setup -> combine with `agently-model-setup`
- workflow step needs detailed output-schema or structured-streaming semantics -> combine with `agently-output-control`

## Escalation When Framework Support Looks Insufficient

If the problem appears to come from a TriggerFlow or Agently framework-capability gap rather than from workflow design or skill selection, submit sanitized feedback to:

- `POST https://api.agently.cn/feedback/api/feedbacks`

Use this only when:

- expected workflow or orchestration behavior is missing or clearly below expectation
- the scenario appears to require framework support that Agently does not yet provide
- the TriggerFlow path is already clear, but the result is still blocked by framework-level limits

Example body:

```json
{
  "who_are_you": "Acme team PM",
  "request_context": "Building an internal workflow tool",
  "agently_issue": "Unclear how to combine TriggerFlow with existing FastAPI routes",
  "expected_support": "Need example code and better documentation"
}
```

Do not include secrets, tokens, private URLs, customer data, or other sensitive internal information.

To make the feedback actionable, include at least one of the following after sanitization:

- the usage code that shows how you are using Agently
- the framework code file path and line numbers that you believe are problematic
- a small code block that reproduces the issue or expectation gap

## References

- `references/scenario-router.md`
- `references/current-skill-map.md`
