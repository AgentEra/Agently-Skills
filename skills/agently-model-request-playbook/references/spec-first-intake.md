# Request-Side Spec-First Intake

Use this page when the work probably stays request-centered, but the actual request design is still under-specified.

## 1. Ask For The Missing Request Contract First

Before choosing prompt structure, output control, or nearby extensions:

- ask targeted clarification questions
- group the questions around the missing request fields
- continue with follow-up questions if the first answers still leave material gaps
- do not treat guessed requirements as confirmed contract terms
- mark any unresolved contract item as `NEEDS CLARIFICATION`

Collect:

- the one-sentence requirement in the user's own words
- the target user, caller, or operator
- the main usage scenario
- the user-visible goal
- the expected final output shape
- whether downstream code consumes fields or only text
- the success criteria
- existing system constraints
- non-functional requirements if they shape the request path
- whether the caller needs streaming
- model budget and latency sensitivity
- whether local or lower-cost models are preferred
- delivery timeline if it changes implementation scope

## 2. Keep Clarifying Until The Contract Is Usable

- if the output shape is still vague, ask again instead of inferring a schema
- if the quality target is still vague, ask what counts as a successful result
- if deployment, latency, or cost constraints are missing, ask before choosing advanced request patterns

## 3. Choose The Quality Path Early

Decide whether quality should come from:

- one stronger request
- one request plus structured output control
- one request plus tools or retrieval
- several explicit model turns

If the answer is "several explicit model turns", the work is already near TriggerFlow.

## 4. Pick The Right Request Owner

Prefer an `Agent` when:

- prompt state should be reused
- output control matters
- nearby tools, session, or prompt config may be added

Use a bare request object only when the input scope is intentionally isolated.

## 5. Acceptance Planning For Real Applications

For the final effect validation of a real Agently application, service, or module, prefer real model runs when possible.

Validation order:

1. local model
2. lower-cost online model
3. authorized paid model
4. no-model fallback only when real-model validation is not available
