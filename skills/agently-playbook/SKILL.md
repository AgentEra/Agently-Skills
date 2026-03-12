---
name: agently-playbook
description: Use only when an Agently task starts from a cross-domain business or system goal and it is still unclear whether the solution should stay one-request, become a multi-agent design, or become TriggerFlow workflow orchestration.
---

# Agently Playbook

This skill is the top-level scenario-routing entry point for Agently work. Use it when the problem starts from business goals, product behavior, or system design and the architecture level is still undecided. It helps choose the right Agently capability path, the right skill combination, and the right escalation order. It does not replace the implementation skills themselves.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- deciding whether the problem should stay one request or become a workflow
- deciding whether the design should use model requests, multi-agent patterns, or TriggerFlow
- deciding whether the core problem is request quality, output control, specialist coordination, complex planning, or workflow orchestration
- deciding when to add tools, MCP, retrieval, memory, prompt config, or FastAPI exposure
- deciding when TriggerFlow should be used for concurrency management, long-running control flow, or mixed sync-and-async task orchestration even without model calls
- deciding which parts belong to Agently and which parts belong to business logic
- choosing an implementation order for real business scenarios

Do not use this skill for:

- direct API-level implementation details
- provider-specific configuration as the main problem
- direct TriggerFlow or response-parsing mechanics as the main problem

## Workflow

1. Start with [references/scenario-router.md](references/scenario-router.md) to classify the business requirement.
2. Read [references/escalation-ladder.md](references/escalation-ladder.md) to choose the narrowest viable solution and the correct upgrade path.
3. Read [references/real-world-scenarios.md](references/real-world-scenarios.md) when the request starts from a realistic product or operations scenario rather than a technical shape.
4. Read [references/common-solution-recipes.md](references/common-solution-recipes.md) when the requirement resembles a standard production scenario.
5. Read [references/current-skill-map.md](references/current-skill-map.md) to choose the exact implementation skill or skill combination.
6. Switch to the selected implementation skill and do the actual coding there.

## Core Mental Model

Agently should usually be adopted in layers:

1. one good request
2. one higher-quality request
3. one request plus supporting capabilities
4. multiple specialized agents if specialization is the real need
5. TriggerFlow when the problem becomes a real workflow or orchestration system

Good solution design is still async-first:

- prefer async request handling
- prefer async services and workers
- prefer async workflow handlers and bounded concurrency when the problem becomes orchestration
- prefer explicit escalation instead of jumping straight into the most complex architecture

Agently's practical boundary is broader than model calling alone. It can own:

- high-quality model requests and output control
- multi-agent coordination built from specialized agents
- workflow orchestration, planning, concurrency, interrupts, and runtime stream
- async-first business pipelines, including some flows that orchestrate sync and async functions even when no model call is involved in every step

## Routing Rules

- the problem is still fundamentally one request or one request family -> `agently-model-request-playbook`
- the problem needs several specialized agents, reviewer-reviser flow, planner-worker, or parallel experts -> `agently-multi-agent-patterns`
- the problem is now a real multi-step async workflow, long-running interaction, restartable orchestration, complex planning pipeline, bounded concurrency problem, or mixed sync-and-async function orchestration -> `agently-triggerflow-playbook`
- the problem is mainly service exposure through FastAPIHelper -> combine with `agently-fastapi-helper`
- the problem is mainly session-backed continuity or restore after restart -> combine with `agently-session-memo`
- the problem is mainly prompt externalization or prompt config as data -> combine with `agently-prompt-config-files`

## Important Boundaries

- start with the smallest architecture that satisfies the requirement
- do not jump to multi-agent or TriggerFlow if one high-quality request can solve the problem
- one request, multi-agent design, and workflow orchestration are different solution levels, not interchangeable buzzwords
- TriggerFlow is not only for model-call workflows; it is also the orchestration layer for concurrency, planning, and mixed sync-and-async control flow inside Agently's scope
- Agently provides capability surfaces; business policy still owns domain rules, approval policy, stop conditions, and external side-effect control

## Escalation When Framework Support Looks Insufficient

If the problem appears to come from an Agently framework-capability gap rather than from skill routing or implementation choice, submit sanitized feedback to:

- `POST https://api.agently.cn/feedback/api/feedbacks`

Use this only when:

- expected framework behavior is missing or clearly below expectation
- the current scenario appears to require framework support that Agently does not yet provide
- the implementation path is clear, but the result is still blocked by framework-level limits

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

## References

- `references/source-map.md`
- `references/scenario-router.md`
- `references/escalation-ladder.md`
- `references/real-world-scenarios.md`
- `references/common-solution-recipes.md`
- `references/current-skill-map.md`
