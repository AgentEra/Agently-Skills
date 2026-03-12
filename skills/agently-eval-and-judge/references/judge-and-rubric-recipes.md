# Judge And Rubric Recipes

Use this page when the main problem is how the review should think, score, and explain itself.

## 1. Binary Gate

Use when the output should be accepted or rejected.

Recommended fields:

- `pass`
- `reasons`
- `confidence`

Good fit:

- policy checks
- formatting checks after generation
- "is this good enough to send?" gates

## 2. Scored Rubric

Use when several criteria matter and a single pass-fail answer is too coarse.

Recommended fields:

- `criteria`
- `score`
- `weight`
- `summary`

Good fit:

- writing quality review
- answer helpfulness review
- product-spec or requirements completeness review

## 3. Issue List Review

Use when the consumer needs concrete defects rather than only a numeric score.

Recommended fields:

- `issues`
- `severity`
- `evidence`
- `suggested_fix`

Good fit:

- spec review
- prompt review
- generated-code review

## 4. Pairwise Comparison

Use when the judge should compare two candidates and pick one winner.

Recommended fields:

- `winner`
- `winner_reason`
- `tradeoffs`

Good fit:

- A/B answer choice
- choosing between two generated drafts

## 5. Practical Rules

- keep criteria explicit and bounded
- require evidence or reasons, not only scores
- keep category names stable for downstream code
- let business logic own thresholds and final side effects
