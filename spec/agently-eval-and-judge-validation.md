# Agently Eval And Judge Validation

This note records the author-side validation boundary for `agently-eval-and-judge`.

## Scope

- validate the frontmatter and routing boundary of the evaluation skill
- validate that the public references exist and stay English-only
- validate that trigger fixtures cover direct judge-model and rubric scenarios
- validate that the public skill distinguishes direct evaluation design from multi-turn workflow orchestration

## Expected Boundary

- direct rubric scoring, pass-fail gating, issue reports, and validator-model prompt design belong here
- local model setup and transport belong to `agently-model-setup`
- response-shape enforcement belongs to `agently-output-control`
- specialist-team architecture belongs to `agently-multi-agent-patterns`
- workflow orchestration belongs to `agently-triggerflow-playbook`

## Validation Script

Run:

```bash
python spec/validate_agently_eval_and_judge.py
```

The script exits non-zero on public-boundary failures.

Repository validation here checks the skill boundary. Final acceptance for a built evaluator service should still use representative real-model runs.
