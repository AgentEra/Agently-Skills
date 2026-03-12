# Agently Eval And Judge Authoring Notes

This file records author-side constraints for maintaining the `agently-eval-and-judge` skill.

## Authoring Rules

- All skill-facing content must be written in English.
- Keep the frontmatter and opening paragraph phrased as a direct leaf for evaluation, grading, or judge-model design, not as a generic request router.
- Lead with scenario language such as rubric scoring, pass-fail checks, review reports, or validator-model prompts before naming lower-level APIs.
- Route provider setup, local Ollama wiring, and endpoint configuration questions to `agently-model-setup`.
- Route output-schema enforcement, retries, and structured streaming questions to `agently-output-control`.
- Route generator-judge specialist architecture questions to `agently-multi-agent-patterns`.
- Route long-running approval or evaluation workflows to `agently-triggerflow-playbook`.
