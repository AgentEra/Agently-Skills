# Escalation Ladder

Choose the narrowest viable solution first.

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

Stay in:

- `agently-model-request-playbook`

## 3. Multi-agent design

Upgrade to this when:

- several specialized roles are genuinely needed
- one final answer should be produced from several specialist stages or branches
- reviewer-reviser or planner-worker separation improves safety or clarity

Route to:

- `agently-multi-agent-patterns`

## 4. TriggerFlow orchestration

Upgrade to this when:

- the problem is explicitly a workflow
- steps should branch, fan out, pause, resume, or persist
- steps should be planned, decomposed, or concurrency-limited under one runtime
- sync and async functions should be orchestrated under one business flow
- runtime state and orchestration semantics matter more than prompt-only composition
- some steps may not call a model at all, but workflow control is still the main need

Route to:

- `agently-triggerflow-playbook`

## Practical rule

Do not escalate only because the architecture sounds more advanced. Escalate only when the simpler layer cannot satisfy the actual business requirement.
