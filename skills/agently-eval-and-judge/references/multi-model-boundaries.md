# Multi-Model Boundaries

Use this page when the question is whether generation and evaluation should stay together or be split.

## Keep One Model Or One Request Family When

- latency matters more than isolation
- the review is lightweight and mainly shapes the final response
- the risk of self-review bias is acceptable

## Use A Separate Judge Model When

- the review should be more neutral than the generator
- the generator and judge should use different model sizes or providers
- a local Ollama judge or cheaper validator model is desirable
- the design accepts extra latency in exchange for a bounded quality loop

Add `agently-model-setup` for the separate-model wiring.

## Escalate To `agently-multi-agent-patterns` When

- generator and judge need isolated roles and handoff contracts
- the judge should own a separate context boundary, tools, or retrieval
- the system already behaves like a specialist-agent team

## Escalate To `agently-triggerflow-playbook` When

- evaluation becomes a multi-step workflow
- the system needs bounded draft -> judge -> revise turns
- approval, waiting, or resume is required between stages
- batch evaluation, branching, or restart-safe orchestration is the main problem
