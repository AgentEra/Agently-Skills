# Agently Multi-Agent Patterns Authoring

This file is author-side only. It does not belong in published skill payload.

## Scope rules

- Keep the frontmatter and opening paragraph phrased as the multi-agent pattern-routing leaf after the multi-agent decision is already made, not as the top-level architecture router.
- Let the frontmatter trigger on specialist-team signals such as planner-worker, reviewer-reviser, generator-judge, or parallel experts even when the user does not say "multi-agent" verbatim.
- Keep this as a pattern and routing skill, not an invented runtime capability.
- Do not describe Agently as if it had a separate built-in multi-agent kernel.
- Ground public claims in current Agently composition surfaces:
  - multiple `create_agent(...)` instances
  - TriggerFlow orchestration
  - structured handoffs through output control
  - tools, MCP, session, and KB/RAG as optional specialist capabilities
- Public guidance should state clearly that TriggerFlow usually owns explicit multi-turn specialist loops, budgets, and stop conditions.

## Routing rules

- Route undecided cross-domain architecture questions to `agently-playbook`.
- Route one-request extension questions to `agently-model-request-playbook`.
- Route concrete workflow APIs to TriggerFlow skills.
- Route concrete request details to model-request-side skills.
- Keep the skill focused on when to use multi-agent design and which pattern to choose.
