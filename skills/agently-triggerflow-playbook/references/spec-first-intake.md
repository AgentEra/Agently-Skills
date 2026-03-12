# TriggerFlow Spec-First Intake

Use this page when the request already hints at workflow behavior, but the stages are not yet defined clearly.

## 1. Ask For The Missing Workflow Facts Before Designing Stages

Before choosing workflow structure:

- ask targeted clarification questions
- group them by missing workflow facts
- continue with follow-up questions if the first answers still leave stage boundaries unclear
- do not invent approval gates, resume points, stop rules, or retry semantics without confirmation
- mark any unresolved workflow decision as `NEEDS CLARIFICATION`

Lock:

- the one-sentence requirement in the user's own words
- the target user, operator, or approver
- the core business scenario
- the entry input
- the expected final result
- the intermediate stages
- whether any stage waits, resumes, or asks for approval
- whether any stage streams progressive output
- whether quality depends on several model turns
- the success criteria
- the model, cost, and latency constraints
- the existing system constraints
- the non-functional requirements
- the delivery timeline if schedule affects the flow boundary

## 2. Keep Clarifying Until The Flow Boundary Is Usable

- if the stage list is still fuzzy, ask what the real business checkpoints are
- if approval ownership is unclear, ask who can pause, approve, reject, or resume
- if stop conditions are unclear, ask how the workflow knows it is done

## 3. Recognize Quality Loops Early

Treat these as strong TriggerFlow signals:

- draft -> judge -> revise
- reflection loops
- evaluator-optimizer
- ReAct or tool loops
- lower-cost or local models that need bounded extra passes

## 4. Write And Confirm The Working Flow Spec

The flow spec should name:

- the stages
- the data written between stages
- the stop condition or turn budget
- the owner of the final externally visible result

The working flow spec should stay testable and bounded. If stage ownership, approval semantics, or stop conditions would materially change the architecture, ask for confirmation before implementation.

## 5. Acceptance Planning For Real Applications

For the final effect validation of a real Agently application, service, or module, prefer real model runs when possible.

Validation order:

1. local model
2. lower-cost online model
3. authorized paid model
4. no-model fallback only when real-model validation is not available
