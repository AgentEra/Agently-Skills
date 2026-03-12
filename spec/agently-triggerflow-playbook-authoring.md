# Agently TriggerFlow Playbook Authoring Notes

This file is author-side only. It does not belong in published skill payload.

## Goal

`agently-triggerflow-playbook` is a routing skill, not an implementation skill.

Its job is to:

- recognize TriggerFlow from business requirements
- route to the correct implementation skill
- point out required cross-skill combinations
- present bounded quality-improvement loops as a natural TriggerFlow entry, not only as an advanced edge case

It should not:

- absorb detailed API explanations from implementation skills
- become a duplicate of `agently-triggerflow-orchestration`
- reference unpublished or non-existent skills in routing rules

## Current Public Routing Targets

- `agently-triggerflow-orchestration`
- `agently-triggerflow-patterns`
- `agently-triggerflow-state-and-resources`
- `agently-triggerflow-subflows`
- `agently-triggerflow-model-integration`
- `agently-triggerflow-config`
- `agently-triggerflow-execution-state`
- `agently-triggerflow-interrupts-and-stream`
- `agently-model-setup`
- `agently-output-control`
- `agently-session-memo`

## Discovery rules

- Frontmatter must state clearly that this is the workflow-orchestration router for the TriggerFlow side of the catalog.
- Lead the description with workflow, orchestration, concurrency, approval, resume, waiting, or runtime-stream signals rather than with the literal `TriggerFlow` name.
- The frontmatter should still be able to win when the user describes a long-running or resumable workflow without naming TriggerFlow explicitly.
- Do not compete with implementation skills on explicit API names when the user has already named the concrete TriggerFlow surface.
- Mention model setup or output control only as supporting combinations inside a TriggerFlow solution, not as primary trigger language.
- Public guidance should include spec-first intake for under-specified workflow requests.
- Public guidance should explicitly frame reflection, judge, revise, ReAct, and `instant`-driven follow-up work as normal TriggerFlow-quality patterns.

## Non-trigger examples

- Ordinary one-request generation or response-shaping work should route to `agently-model-request-playbook` or lower request skills.
- Explicit low-level TriggerFlow API questions such as `to_sub_flow(...)`, execution save/load, or config export/import should route to the corresponding implementation skill.
- Generic provider setup questions should route to `agently-model-setup` unless the workflow context is already the main problem.
