# Spec-First Intake

Use this page when the user request is still short, ambiguous, or too compressed to implement safely.

## 1. Do Not Treat A One-Liner As A Full Spec

If the request is something like:

- "build an agent for this"
- "make it higher quality"
- "turn this into a workflow"
- "help me make a model app"

the next step is not implementation. The next step is to gather enough information to write a short working spec.

## 2. Minimum Intake Checklist

Collect at least:

- the business goal
- the main input materials or source data
- the expected output form
- whether downstream systems need structured fields
- who owns final acceptance
- whether cost, latency, or local-model use matters
- whether the result must stream progressively
- whether quality should be improved through review, reflection, or revise loops

## 3. Write A Short Working Spec

The working spec can stay lightweight, but it should lock:

- the target behavior
- the main processing stages
- the key risks
- the likely Agently solution level: one request, specialist-agent design, or TriggerFlow workflow

## 4. Early Architecture Signal

If the intake already reveals:

- several explicit model turns
- quality-improvement loops
- judge or revise stages
- pause, resume, or approval behavior

then treat the problem as a TriggerFlow candidate early.

## 5. Acceptance Planning For Real Applications

For the final effect validation of a real Agently application, service, or module, prefer real model runs when possible.

Validation order:

1. local model
2. lower-cost online model
3. authorized paid model
4. no-model fallback only when real-model validation is not available

This is an application acceptance rule, not a claim that every repository-level skill check must call a model.
