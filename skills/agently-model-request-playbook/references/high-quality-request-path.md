# High-Quality Request Path

Use this page when one request is still the right unit, but the request quality must go beyond a plain prompt-and-reply call.

## 1. High-Quality Path

The high-quality request path is usually:

1. a short request spec with output, budget, and latency assumptions
2. correct model setup
3. an `Agent` as the request owner when reuse or control matters
4. intentional input composition
5. reusable prompt config when business prompts should live outside code
6. explicit output design
7. async-first response handling
8. response reuse instead of duplicate requests

In skill terms, that usually means:

- `agently-model-setup`
- `agently-input-composition`
- `agently-output-control`

## 2. Common Quality Upgrades

- plain text is not stable enough -> add `agently-output-control`
- UI needs progressive structured feedback -> use `instant` or `streaming_parse`
- one request result must serve several consumers -> use response reuse instead of multiple shorthand getters
- the runtime is async -> prefer async request and response APIs
- prompt text should be versioned or shared -> add `agently-prompt-config-files`
- quality only improves if several explicit draft, judge, or revise turns are introduced -> escalate to TriggerFlow instead of stretching the one-request story

## 3. When Not To Escalate Yet

Do not escalate just because the request is complex.

If one request can still produce:

- the answer
- the structure
- the stream
- the metadata

then keep it a request problem, not a workflow problem.

If the design already requires explicit multi-turn quality control, it is no longer just a higher-quality single request.
