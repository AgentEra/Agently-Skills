# Core Patterns

Use this page to choose a multi-agent pattern from the business shape of the problem.

## 1. Planner-Worker Or Supervisor-Router

Use this pattern when one agent should decide which specialist should act next.

Typical fit:

- one planner decomposes work, then routes tasks to specialists
- one supervisor decides whether to call a research agent, a coding agent, or a summarizer
- the workflow needs explicit ownership for branch selection

## 2. Staged Specialist Pipeline

Use this pattern when several agents should act in sequence with different responsibilities.

Typical fit:

- collect or inspect -> analyze -> summarize
- extract -> validate -> produce final answer
- search or browse -> read -> synthesize

This is often the best first multi-agent pattern because the handoff points are easy to make explicit.

## 3. Parallel Experts And Synthesizer

Use this pattern when several specialists can work independently on the same request, then one final owner should synthesize.

Typical fit:

- several experts produce separate assessments
- several section workers draft in parallel
- several retrieval or evaluation branches return evidence that one final agent combines

The synthesizer should own the final external result. Do not leave several partial expert results without one final owner.

## 4. Reviewer-Reviser

Use this pattern when one agent should critique or constrain another.

Typical fit:

- writer -> reviewer -> reviser
- proposal -> compliance checker -> corrected proposal
- answer draft -> evaluator -> retry or finalize

Use explicit structured handoffs so the reviewer can point to concrete issues rather than only free-form criticism.

## 5. Human Gate Between Agent Stages

Use this pattern when the system should stop between agent stages for approval, clarification, or external input.

Typical fit:

- researcher prepares options and waits for user approval
- draft is reviewed by a human before tool execution or external side effects
- long-running workflow should wait for an operator before continuing

This pattern usually combines with `agently-triggerflow-interrupts-and-stream`.
