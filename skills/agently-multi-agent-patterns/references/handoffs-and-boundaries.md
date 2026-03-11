# Handoffs And Boundaries

This page covers the part that usually decides whether a multi-agent design remains maintainable.

## 1. Use explicit handoff contracts

Prefer structured handoffs between agents:

- extraction result
- task assignment
- critique result
- synthesis inputs

This reduces ambiguity and makes it easier to route the design into `agently-output-control`.

## 2. Keep agent context isolated by default

Do not treat all agent chat history as one shared conversation by default.

Prefer:

- isolated per-agent request context
- explicit handoff payloads
- shared workflow state in TriggerFlow runtime state or external storage only when truly necessary

## 3. Share capabilities intentionally

Different agents may need different:

- models or providers
- tools or MCP access
- retrieval access
- prompt templates
- memory scope

Only share these when the business design actually requires it.

## 4. Keep one final owner

One agent or one final workflow step should own the externally visible result.

Without a final owner, multi-agent systems tend to produce:

- duplicated outputs
- conflicting conclusions
- unclear failure handling

## 5. Bound delegation

Avoid recursive or open-ended delegation.

Prefer:

- bounded fan-out
- explicit turn budgets
- explicit stop conditions
- human gates before sensitive side effects
