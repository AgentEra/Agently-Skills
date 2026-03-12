# Evaluator-Optimizer And ReAct

This page covers two high-value iterative agent patterns.

## 1. Evaluator-Optimizer

Use this pattern when one step produces a draft and another step checks whether the draft is good enough.

Typical shape:

1. generate a draft
2. evaluate against explicit criteria
3. if the draft fails, revise and try again
4. stop when the draft passes or the budget is exhausted

Good fits:

- maker-checker workflows
- structured review loops
- validation before side effects
- local or lower-cost model setups that need bounded extra passes for quality

Do not use this pattern when first-pass quality is already good enough or when no clear evaluation rule exists.

## 2. ReAct Or Tool Loop

Use this pattern when the workflow should alternate between:

- think
- act
- observe
- decide whether to continue

Typical shape:

1. reason about the next action
2. call a tool or worker step
3. read the observation
4. decide whether to continue or finalize

Good fits:

- search or research loops
- tool-using assistants
- agent workflows that need explicit observation handling between turns

## 3. Boundaries

- evaluator-optimizer is about iterative quality control
- ReAct is about iterative action selection with observations
- both patterns need explicit stop conditions and budgets
- if model calls are the main implementation topic, switch to `agently-triggerflow-model-integration`
- if a human should evaluate or approve, combine with `agently-triggerflow-interrupts-and-stream`
