# TriggerFlow Spec-First Intake

Use this page when the request already hints at workflow behavior, but the stages are not yet defined clearly.

## 1. Collect The Workflow Facts

Lock:

- the entry input
- the expected final result
- the intermediate stages
- whether any stage waits, resumes, or asks for approval
- whether any stage streams progressive output
- whether quality depends on several model turns
- the model, cost, and latency constraints

## 2. Recognize Quality Loops Early

Treat these as strong TriggerFlow signals:

- draft -> judge -> revise
- reflection loops
- evaluator-optimizer
- ReAct or tool loops
- lower-cost or local models that need bounded extra passes

## 3. Write The Working Flow Spec

The flow spec should name:

- the stages
- the data written between stages
- the stop condition or turn budget
- the owner of the final externally visible result

## 4. Acceptance Planning For Real Applications

For the final effect validation of a real Agently application, service, or module, prefer real model runs when possible.

Validation order:

1. local model
2. lower-cost online model
3. authorized paid model
4. no-model fallback only when real-model validation is not available
