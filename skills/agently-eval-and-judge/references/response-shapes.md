# Response Shapes

Use this page when the review result must be machine-readable.

## Minimal Shapes

### Pass Or Fail

Recommended keys:

- `pass`
- `reasons`

### Scored Review

Recommended keys:

- `overall_score`
- `criteria`
- `summary`

### Issue Report

Recommended keys:

- `issues`
- `summary`
- `next_action`

## When To Combine With `agently-output-control`

Add `agently-output-control` when:

- the judge result must be returned as stable JSON fields
- missing keys should trigger retries
- the review should be consumed through `get_data()` or `get_data_object()`
- the review should stream partial structured fields

This skill decides what the review should contain.
`agently-output-control` decides how the response contract should be enforced and consumed.
