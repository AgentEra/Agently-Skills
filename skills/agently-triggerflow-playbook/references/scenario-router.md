# TriggerFlow Scenario Router

Use this page to decide whether the requirement should enter TriggerFlow work at all, and which TriggerFlow implementation skill should do the real work.

## When TriggerFlow Is Usually The Right Fit

Choose TriggerFlow when the business requirement implies one or more of these properties:

- the workflow is signal-driven instead of purely linear
- several steps must run concurrently or in coordinated branches
- the workflow may need nested or reusable child flows
- the workflow must wait for human or external-system input before continuing
- the workflow should emit progressive business output while still running

## Route To The Correct Skill

- general TriggerFlow construction, signal routing, event gates, or result ownership:
  use `agently-triggerflow-orchestration`
- router patterns, fan-out and fan-in, `batch(...)`, `for_each(...)`, `collect(...)`, `side_branch(...)`, safe loops, evaluator-optimizer, ReAct loops, or approval-gate workflow design:
  use `agently-triggerflow-patterns`
- state placement, runtime-resource boundaries, or restart-safe state design:
  use `agently-triggerflow-state-and-resources`
- isolated child workflow, `to_sub_flow(...)`, explicit parent-child handoff, or child stream bridge:
  use `agently-triggerflow-subflows`
- model requests inside chunks, several model calls in one workflow, or `instant`-driven downstream model work:
  use `agently-triggerflow-model-integration`
- flow definition export, import, blueprint copy, or Mermaid inspection:
  use `agently-triggerflow-config`
- one running execution should survive save/load or resume later:
  use `agently-triggerflow-execution-state`
- a suspended workflow should come back after process restart or persisted shutdown:
  combine `agently-triggerflow-config` + `agently-triggerflow-execution-state`
- a suspended conversation also depends on long-lived memory outside the execution:
  add `agently-session-memo`
- waiting, resume, pending interrupts, or runtime stream:
  use `agently-triggerflow-interrupts-and-stream`
- provider setup:
  add `agently-model-setup`
- detailed structured-output control:
  add `agently-output-control`

## Practical Boundary

If the problem statement starts with business language such as "review pipeline", "approval workflow", "agent loop", "multi-step async processing", or "live progress UI", start here first and then route into the concrete implementation skill.
