# High-Quality Request Path

Use this page when one request is still the right unit, but the request quality must go beyond a plain prompt-and-reply call.

## 1. High-Quality Path

The high-quality request path is usually:

1. correct model setup
2. intentional input composition
3. explicit output design
4. async-first response handling
5. response reuse instead of duplicate requests

In skill terms, that usually means:

- `agently-model-setup`
- `agently-input-composition`
- `agently-output-control`

## 2. Common Quality Upgrades

- plain text is not stable enough -> add `agently-output-control`
- UI needs progressive structured feedback -> use `instant` or `streaming_parse`
- one request result must serve several consumers -> use response reuse instead of multiple shorthand getters
- the runtime is async -> prefer async request and response APIs

## 3. When Not To Escalate Yet

Do not escalate just because the request is complex.

If one request can still produce:

- the answer
- the structure
- the stream
- the metadata

then keep it a request problem, not a workflow problem.
