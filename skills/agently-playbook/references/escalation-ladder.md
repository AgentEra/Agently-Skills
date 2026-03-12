# Escalation Ladder

Choose the narrowest viable solution first.

## 0. Capability-fit triage and targeted intake

Start here when:

- the request is low-information-density
- the quality target is unclear
- output shape, budget, or latency expectations are missing
- it is still unclear whether Agently's current capability tree can own the scenario

Do first:

- judge which current Agently layer is the leading fit candidate
- ask targeted clarification questions
- continue with follow-up questions if the first answers are still incomplete
- write a short working spec only after the missing fields are usable
- collect output, downstream, model-tier, and latency assumptions without silently inventing them
- stop the intake once the narrowest viable Agently path is clear; do not turn it into a longer spec process by default

## 1. Standard single request

Use this when:

- one prompt and one answer are enough
- no explicit workflow state is needed
- no specialist coordination is needed

Route to:

- `agently-model-request-playbook`

## 2. Higher-quality single request

Upgrade to this when:

- output must be structured
- streaming feedback matters
- response reuse matters
- tool use, retrieval, or memory become necessary
- output control and downstream consumption shape the product behavior more than raw prompt wording
- one Agent should own prompt state and output control, but the work is still one request

Stay in:

- `agently-model-request-playbook`

## 3. Multi-agent design

Upgrade to this when:

- several specialized roles are genuinely needed
- one final answer should be produced from several specialist stages or branches
- reviewer-reviser or planner-worker separation improves safety or clarity
- specialization and handoff ownership are the real problem, not just repeated quality loops

Route to:

- `agently-multi-agent-patterns`

## 4. TriggerFlow orchestration

Upgrade to this when:

- the problem is explicitly a workflow
- steps should branch, fan out, pause, resume, or persist
- quality depends on several explicit model turns such as reflection, judge, or revise stages
- steps should be planned, decomposed, or concurrency-limited under one runtime
- sync and async functions should be orchestrated under one business flow
- runtime state and orchestration semantics matter more than prompt-only composition
- some steps may not call a model at all, but workflow control is still the main need

Route to:

- `agently-triggerflow-playbook`

## Practical rule

Prefer the smallest Agently layer that can actually satisfy the requirement.

Do not escalate only because the architecture sounds more advanced. Escalate only when the simpler Agently layer cannot satisfy the actual business requirement, and escalate out of Agently only when a concrete capability gap remains after the fit check.
