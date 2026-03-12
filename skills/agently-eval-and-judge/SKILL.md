---
name: agently-eval-and-judge
description: Use only when the main task is model-based evaluation, scoring, or judge-model design for request-side work, such as rubric scoring, pass-fail checks, review reports, issue lists, validator-model prompts, pairwise comparison, or generator-versus-judge boundaries.
---

# Agently Eval And Judge

This skill is the direct leaf for request-side evaluation and judge-model design after the request domain is already known. It focuses on rubric construction, pass-fail thresholds, evidence capture, issue reporting, review prompts, and the boundary between a generator model and a validator model. It does not replace model setup, raw output-schema mechanics, or multi-agent pattern selection.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- rubric scoring and weighted review criteria
- pass or fail decisions with explicit reasons
- issue lists, review reports, and evidence-backed critique
- judge, reviewer, validator, or grader prompt design
- pairwise comparison between two candidate outputs
- deciding whether one request family can own both generation and evaluation or whether the judge should be isolated

Do not use this skill for:

- provider setup, endpoint wiring, or local-model connectivity as the main problem
- output schema mechanics, retries, or structured streaming as the main problem
- deciding whether the whole system should become multi-agent or workflow orchestration
- embeddings, retrieval architecture, or generic tool-loop design

## Workflow

1. Start with [references/judge-and-rubric-recipes.md](references/judge-and-rubric-recipes.md) to choose the evaluation pattern.
2. Read [references/response-shapes.md](references/response-shapes.md) to decide how the evaluation result should be returned.
3. Read [references/multi-model-boundaries.md](references/multi-model-boundaries.md) when the question is whether the generator and judge should share one model, use separate models, or escalate to multiple agents.
4. If the behavior is unstable or underspecified, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

Good evaluation design usually has five parts:

1. define the criteria
2. define what evidence the judge must cite
3. define the machine-readable score or decision shape
4. decide whether the judge can share the generator model or should be isolated
5. keep thresholds, issue categories, and stop conditions owned by business logic

Evaluation quality usually fails because one of those parts is missing rather than because the model API is wrong.

## Selection Rules

- one output should be graded against a rubric -> start here
- one output should be accepted or rejected with explicit reasons -> start here
- two outputs should be compared and one winner selected -> start here
- the main issue is local Ollama or separate judge-model setup -> combine with `agently-model-setup`
- the main issue is structured JSON review output, retries, or streamed evaluation fields -> combine with `agently-output-control`
- the main issue is a dedicated generator agent and a dedicated judge agent with handoff contracts -> combine with `agently-multi-agent-patterns`
- the main issue is a long-running approval or evaluation workflow -> combine with `agently-triggerflow-playbook`

## Important Boundaries

- this skill owns evaluation logic, not transport setup
- this skill owns rubric and review design, not generic output parsing
- this skill can live inside one request family, a multi-agent system, or a workflow, but it does not choose that architecture by itself
- business policy should still own pass thresholds, escalation rules, and external side effects

## References

- `references/source-map.md`
- `references/judge-and-rubric-recipes.md`
- `references/response-shapes.md`
- `references/multi-model-boundaries.md`
- `references/troubleshooting.md`
