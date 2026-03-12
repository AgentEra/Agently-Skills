# Scenario Router

Use this page to classify the business problem before choosing any lower-level skill.

## 0. Low-Information Requests

If the request is still a one-line instruction or lacks output, quality, budget, or latency details:

- start with `spec-first-intake.md`
- ask targeted clarification questions first
- do not route or implement yet
- write a short working spec after the answers are usable
- then return to this router

## 1. One-request problems

Stay on the model-request side when the requirement is mainly:

- one answer
- one extraction or classification
- one structured result
- one streamed or progressively structured result
- one retrieval-augmented answer
- one tool-augmented answer
- one quality pass where the result still belongs to one request owner

Route to:

- `agently-model-request-playbook`

## 2. Multi-agent problems

Use multi-agent design when the requirement is mainly:

- planner-worker or supervisor-specialist collaboration
- writer-reviewer or evaluator-reviser collaboration
- several experts in parallel plus one synthesizer
- strong context or tool isolation between specialist roles

Route to:

- `agently-multi-agent-patterns`

## 3. Workflow problems

Use TriggerFlow when the requirement is mainly:

- several asynchronous steps with explicit control flow
- several synchronous and asynchronous functions must be orchestrated under one control flow
- planning, decomposition, fan-out, fan-in, or concurrency management is the core problem
- several explicit model turns are needed for quality, such as draft -> judge -> revise or reflection loops
- interrupts, resume, runtime stream, or long-running waits
- restart-safe orchestration
- stateful, multi-step business automation
- workflow semantics matter even if some steps do not call a model at all

Route to:

- `agently-triggerflow-playbook`

## 4. Cross-cutting support problems

Add these when they are supporting needs rather than the top-level architecture choice:

- FastAPI exposure -> `agently-fastapi-helper`
- session continuity -> `agently-session-memo`
- prompt config as data -> `agently-prompt-config-files`
