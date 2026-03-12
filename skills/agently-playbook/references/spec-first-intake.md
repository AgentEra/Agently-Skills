# Spec-First Intake

Use this page when the user request is still short, ambiguous, or too compressed to judge capability fit and implement safely.

## 1. Do Not Treat A One-Liner As A Full Spec

If the request is something like:

- "build an agent for this"
- "make it higher quality"
- "turn this into a workflow"
- "help me make a model app"

the next step is not blind implementation or a long planning ceremony. The next step is a short fit-and-clarification pass that is deep enough to decide whether Agently can own the job and which solution layer should own it.

## 2. Start With Capability-Fit Triage

Before collecting a fuller spec, ask:

- does the scenario appear to fit Agently's current request, multi-agent, or TriggerFlow surfaces
- which missing facts would actually change that fit decision
- whether the user is asking for a planning artifact, or simply for the right implementation path

If the fit is already clear, route early and keep the working spec lightweight.

## 3. Ask Clarification Questions Before Designing The Solution

When the request is still low-information-density:

- ask targeted questions before choosing architecture or implementation
- group the questions around the missing spec fields that materially change fit, ownership, or acceptance
- if the first round of answers is still incomplete, continue with focused follow-up questions
- do not silently convert guesses into requirements
- mark any material unknown as `NEEDS CLARIFICATION` until the user confirms it

Typical missing fields to collect explicitly:

- the one-sentence requirement in the user's own words
- the target user, operator, or audience
- the core usage scenario
- the success criteria and who accepts the result
- existing system constraints
- non-functional requirements
- delivery timeline if schedule affects the solution

## 4. Minimum Intake Checklist

Collect only the fields that materially change capability fit, architecture, downstream contract, or acceptance. In many cases the minimum set is enough:

- the business goal
- the target user or operator
- the main usage scenario
- the main input materials or source data
- the expected output form
- whether downstream systems need structured fields
- the success criteria and final acceptance owner
- the existing system constraints
- the non-functional requirements
- the delivery timeline when scope or architecture depends on it
- whether cost, latency, or local-model use matters
- whether the result must stream progressively
- whether quality should be improved through review, reflection, or revise loops

## 5. Write And Confirm A Short Working Spec

The working spec can stay lightweight. It is a routing and execution aid, not a mandatory product-spec ceremony. It should lock:

- the target behavior
- the main processing stages
- the key risks
- the likely Agently solution level: one request, specialist-agent design, or TriggerFlow workflow

The working spec should stay testable and bounded:

- prefer measurable success criteria over vague quality claims
- state important scope boundaries and edge cases when they change the solution path
- ask for confirmation before moving on if scope, cost, or architecture still depends on assumptions
- once the narrowest viable Agently layer is clear, prefer that path instead of postponing the implementation behind extra planning detail

A compact Spec-DD style working spec can use headings such as:

- Background And Goal
- Users And Scenarios
- Functional List
- User Flow Or Workflow
- Data Structure And Interface Sketch
- Boundaries And Exceptions
- Non-Functional Requirements
- Acceptance Criteria
- Risks, Assumptions, And `NEEDS CLARIFICATION` items

## 6. Early Architecture Signal

If the intake already reveals:

- several explicit model turns
- quality-improvement loops
- judge or revise stages
- pause, resume, or approval behavior

then treat the problem as a TriggerFlow candidate early inside Agently instead of stretching it into an ad hoc request chain.

## 7. Acceptance Planning For Real Applications

For the final effect validation of a real Agently application, service, or module, prefer real model runs when possible.

Validation order:

1. local model
2. lower-cost online model
3. authorized paid model
4. no-model fallback only when real-model validation is not available

This is an application acceptance rule, not a claim that every repository-level skill check must call a model.
