# Troubleshooting

## Judge Output Is Vague

- narrow the rubric
- require evidence fields
- reduce overlapping criteria

## Scores Drift Too Much

- simplify the scoring scale
- separate pass or fail from explanatory commentary
- use a separate judge model if self-review bias is high

## Review Output Is Hard To Parse

- add `agently-output-control`
- use stable field names
- retry with `ensure_keys` when required fields are missing

## Unsure Whether This Should Be Multi-Agent

If the real problem is not the rubric itself but the boundary between a generator and a judge, route to `agently-multi-agent-patterns`.

## Unsure Whether This Should Be A Workflow

If the real problem is batching, approvals, pause and resume, or restart-safe orchestration, route to `agently-triggerflow-playbook`.
