# Request-Side Spec-First Intake

Use this page when the work probably stays request-centered, but the actual request design is still under-specified.

## 1. Lock The Request Contract First

Collect:

- the user-visible goal
- the expected final output shape
- whether downstream code consumes fields or only text
- whether the caller needs streaming
- model budget and latency sensitivity
- whether local or lower-cost models are preferred

## 2. Choose The Quality Path Early

Decide whether quality should come from:

- one stronger request
- one request plus structured output control
- one request plus tools or retrieval
- several explicit model turns

If the answer is "several explicit model turns", the work is already near TriggerFlow.

## 3. Pick The Right Request Owner

Prefer an `Agent` when:

- prompt state should be reused
- output control matters
- nearby tools, session, or prompt config may be added

Use a bare request object only when the input scope is intentionally isolated.

## 4. Acceptance Planning For Real Applications

For the final effect validation of a real Agently application, service, or module, prefer real model runs when possible.

Validation order:

1. local model
2. lower-cost online model
3. authorized paid model
4. no-model fallback only when real-model validation is not available
