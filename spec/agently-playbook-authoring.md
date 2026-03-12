# Agently Playbook Authoring

This file is author-side only. It does not belong in published skill payload.

## Scope rules

- Keep this skill at the top routing layer.
- Do not turn it into an API guide.
- Do not duplicate lower-level implementation detail from model-request, multi-agent, or TriggerFlow skills.

## Routing rules

- Route one-request business requirements to `agently-model-request-playbook`.
- Route specialist-agent architecture questions to `agently-multi-agent-patterns`.
- Route true workflow orchestration problems to `agently-triggerflow-playbook`.
- Route FastAPI, session, and prompt-config needs as supporting combinations, not as the top architecture owner by default.

## Discovery rules

- Frontmatter must say that this skill is the top-level cross-domain router for Agently work.
- The discovery boundary must be visible from frontmatter alone. Do not rely on the body to explain that this skill sits above the domain playbooks.
- The description should trigger when the user starts from a business, product, or system goal and it is still unclear whether the solution belongs to single-request work, specialist-agent work, or workflow orchestration.
- The description should still be able to match generic model-app language even when the user does not explicitly say Agently.
- The description should not lead with provider setup, prompt composition, output-shape control, or low-level API terms that belong to lower skills.
- Route hierarchy belongs here only at the architecture-selection level. Detailed capability lists belong to the routed skills.

## Non-trigger examples

- Direct provider setup or model connection questions should route below this skill to `agently-model-setup`.
- Direct prompt-composition questions should route below this skill to `agently-input-composition`.
- Direct output-schema or structured-streaming questions should route below this skill to `agently-output-control`.
- Explicit TriggerFlow API questions should route below this skill to the TriggerFlow playbook or a concrete TriggerFlow implementation skill.
