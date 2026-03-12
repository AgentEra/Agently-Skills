# Agently Model Request Playbook Authoring Notes

This file is author-side only. It does not belong in published skill payload.

## Goal

`agently-model-request-playbook` is a routing skill, not an implementation skill.

Its job is to:

- route one-request and request-adjacent business needs to the right skill
- preserve the single-request-first mindset
- escalate to TriggerFlow only when the business shape exceeds one request
- add a short spec-first intake when the request is still too compressed to implement safely

It should not:

- duplicate implementation details from the routed skills
- become a generic architecture essay
- absorb TriggerFlow details directly

## Discovery rules

- Frontmatter must make it clear that this is the router for single-request and request-adjacent work, not the top-level router for all model-app scenarios.
- Assume the problem already belongs to the single-request family. The description should not compete with `agently-playbook` for broad cross-domain architecture selection.
- Lead with scenario language such as understanding, rewriting, expansion, extraction, generation, scoring, or validation before naming internal framework surfaces.
- Do not lead with provider setup, prompt-composition, output-control, or tool-registration API terms. Those belong to the implementation skills that this playbook routes to.
- Mention TriggerFlow only as an escalation boundary, not as a parallel primary claim in the description.
- Public guidance should prefer `Agent`-owned request design when prompt state, output control, or reuse matters.
- Public guidance should recommend prompt config when business prompts should live outside runtime code.
- Public guidance should stop the one-request story once explicit draft, judge, revise, or reflection stages become part of the design.

## Non-trigger examples

- If the user is still deciding between one request, multi-agent design, and workflow orchestration, route up to `agently-playbook`.
- If the user is directly asking about auth, base URL, provider setup, or request options, route down to `agently-model-setup`.
- If the user is directly asking about prompt slots, mappings, attachments, or chat-history composition, route down to `agently-input-composition`.
- If the user is directly asking about output schemas, `ensure_keys`, `instant`, or `streaming_parse`, route down to `agently-output-control`.
