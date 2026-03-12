---
name: agently-multi-agent-patterns
description: Use only when the problem is already known to need multiple specialized agents and the main task is choosing a specialist-team pattern, such as planner-worker, supervisor-router, parallel experts, reviewer-reviser, generator-judge, staged handoff design, or agent boundary and contract design.
---

# Agently Multi-Agent Patterns

This skill is the pattern-routing leaf for multi-agent architecture after cross-domain architecture selection is already resolved in favor of multiple specialized agents. It focuses on which multi-agent pattern fits the business problem, how agent boundaries and handoff contracts should be defined, and how the design should route into existing Agently implementation skills. It does not claim that Agently has a separate multi-agent runtime primitive. In Agently, multi-agent systems are composed from multiple specialized agents plus TriggerFlow, output control, tools, MCP, session, or service exposure as needed.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- deciding whether a business problem should stay one request or become a multi-agent design
- planner-worker, supervisor-router, specialist handoff, reviewer-reviser, generator-judge, or parallel-expert patterns
- deciding how agent boundaries, handoff schemas, and result ownership should work
- deciding which parts should be isolated per agent and which should be shared at workflow level
- combining multiple agents with TriggerFlow, tools, MCP, KB/RAG, session continuity, or FastAPI exposure

Do not use this skill for:

- direct `TriggerFlow` API questions as the main problem
- direct model setup, output schema, tool loop, or MCP transport details as the main problem
- a single high-quality request that does not actually need multiple specialized agents

## Workflow

1. Start with [references/when-to-use-multi-agent.md](references/when-to-use-multi-agent.md) when the main question is whether multi-agent design is justified at all.
2. Read [references/core-patterns.md](references/core-patterns.md) to select a business pattern such as planner-worker, parallel experts, or reviewer-reviser.
3. Read [references/handoffs-and-boundaries.md](references/handoffs-and-boundaries.md) when the risk is unclear ownership, context leakage, or unstable agent handoffs.
4. Read [references/implementation-routing.md](references/implementation-routing.md) to route the chosen pattern into the right Agently implementation skills.
5. If behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

Use multi-agent architecture only when specialization or isolation is the real requirement.

Good reasons to use multiple agents in Agently:

- different agents need different roles, tools, providers, or context boundaries
- one agent should review, constrain, or revise another
- several specialists should work in parallel and one final owner should synthesize the result
- the business flow needs explicit ownership boundaries instead of one overloaded prompt

Weak reasons to use multiple agents:

- the same result could be produced by one high-quality structured request
- the design has no explicit handoff contract between agents
- several agents are only repeating the same work with slightly different prompts

## Selection Rules

- one planner or supervisor decides which specialist should act next -> planner-worker or supervisor-router
- several specialist agents should work independently, then one agent should synthesize the result -> parallel experts and synthesizer
- one agent drafts and another agent critiques or revises -> reviewer-reviser
- one agent generates and another agent grades, validates, or gates the result -> generator-judge
- one agent collects or validates information, and another produces the final user-facing answer -> staged specialist pipeline
- one workflow must pause for approval or external input between agent steps -> combine the pattern with `agently-triggerflow-interrupts-and-stream`
- one design depends on explicit parent-child workflow isolation -> combine with `agently-triggerflow-subflows`

## Important Boundaries

- Agently does not expose a separate multi-agent runtime primitive; multi-agent systems are composed from existing agent and workflow capabilities
- one final owner should be responsible for the externally visible result
- agent handoffs should use explicit structured contracts whenever possible
- per-agent chat history should stay isolated by default; share only the state that truly must cross agent boundaries
- multi-agent design should stay async-first and use bounded fan-out instead of unbounded recursive delegation

## References

- `references/source-map.md`
- `references/when-to-use-multi-agent.md`
- `references/core-patterns.md`
- `references/handoffs-and-boundaries.md`
- `references/implementation-routing.md`
- `references/troubleshooting.md`
