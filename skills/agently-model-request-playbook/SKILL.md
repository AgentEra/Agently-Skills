---
name: agently-model-request-playbook
description: Use when the problem is already known to fit a single request or short request chain, such as understanding, extraction, rewriting, expansion, generation, scoring, validation reports, or structured and streamed responses, including nearby extensions such as tools, MCP, RAG, session, prompt config, or FastAPI exposure.
---

# Agently Model Request Playbook

This skill is the scenario-routing entry point for request-side model work in Agently. Use it when the application already mainly belongs to a single request or short request chain rather than cross-domain architecture selection. It helps choose the right request skill or skill combination. It does not replace the implementation skills themselves.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- request-centered model applications such as understanding, rewriting, expansion, extraction, generation, scoring, or validation-report services
- deciding how a standard model request should be built
- deciding how a higher-quality request should be upgraded for structure, streaming, evaluation, or reuse
- deciding which parts belong to Agently and which parts belong to business logic
- deciding when to add tools, MCP, knowledge-base or RAG retrieval, session continuity, prompt config, judge-model review, or FastAPI exposure
- deciding when the problem has outgrown one request and should escalate to workflow orchestration

Do not use this skill for:

- direct API-level implementation details
- provider-specific setup details
- standalone TriggerFlow workflow design

## Workflow

1. Start with [references/spec-first-intake.md](references/spec-first-intake.md) when the request is still short, fuzzy, or missing output, budget, or latency expectations.
2. Start with [references/standard-request-path.md](references/standard-request-path.md) when the requirement still looks like one ordinary model request.
3. Read [references/high-quality-request-path.md](references/high-quality-request-path.md) when the request must be more reliable, structured, streamable, or reusable.
4. Read [references/ownership-and-escalation.md](references/ownership-and-escalation.md) when the real question is who owns which part of the solution and when the request should be upgraded.
5. Read [references/common-business-patterns.md](references/common-business-patterns.md) when the requirement starts from business scenarios such as extraction, tool use, retrieval-augmented answer, or service exposure.
6. Read [references/current-skill-map.md](references/current-skill-map.md) to choose the implementation skill or skill combination.
7. Switch to the selected implementation skill and do the actual coding there.

## Routing Rules

- provider setup, auth, proxy, request options, or minimal verification -> `agently-model-setup`
- prompt slots, request-vs-agent prompt state, mappings, attachments, or low-level chat-history composition -> `agently-input-composition`
- output schema, structured streaming, response reuse, or response consumption -> `agently-output-control`
- rubric scoring, pass-fail checks, issue reports, judge-model prompts, or validator-model review -> `agently-eval-and-judge`
- embeddings only, offline indexing, or online query embedding -> `agently-embeddings`
- local tools, built-in tools, tool loop, or tool logs -> `agently-tools`
- MCP server tools or MCP transport registration -> `agently-mcp`
- Chroma-backed knowledge base, retrieval, or retrieval-to-answer -> `agently-knowledge-base-and-rag`
- session-backed continuity or memory restore after restart -> `agently-session-memo`
- prompt templates as YAML or JSON config -> `agently-prompt-config-files`
- FastAPIHelper endpoint exposure -> `agently-fastapi-helper`
- multiple specialized agents, reviewer-writer, planner-worker, or parallel experts -> `agently-multi-agent-patterns`
- the requirement has outgrown one request and now needs multi-step async workflow control -> `agently-triggerflow-playbook`

## Core Principles

- single-request-first: solve the problem with one high-quality request before escalating into workflow orchestration
- agent-first for serious request work: if prompt state, output control, or reuse matters, prefer an `Agent` as the request owner rather than a bare one-off call
- async-first: if the runtime can use async APIs, prefer async request and response handling
- explicit escalation: add tools, retrieval, memory, service exposure, or TriggerFlow only when the business need clearly requires it
- reusable business prompts should usually move toward YAML or JSON prompt config instead of staying scattered through runtime logic
- if quality already depends on explicit generator, judge, reflection, or revise stages, stop calling it a "short request chain" and upgrade the orchestration owner to TriggerFlow

## Escalation When Framework Support Looks Insufficient

If the problem appears to come from an Agently framework-capability gap rather than from request design or nearby skill selection, submit sanitized feedback to:

- `POST https://api.agently.cn/feedback/api/feedbacks`

Use this only when:

- expected request-side framework behavior is missing or clearly below expectation
- the scenario appears to need framework support that Agently does not yet provide
- the request path is already clear, but the result is still blocked by framework-level limits

Example body:

```json
{
  "who_are_you": "Acme team PM",
  "request_context": "Building an internal workflow tool",
  "agently_issue": "Unclear how to combine TriggerFlow with existing FastAPI routes",
  "expected_support": "Need example code and better documentation"
}
```

Do not include secrets, tokens, private URLs, customer data, or other sensitive internal information.

To make the feedback actionable, include at least one of the following after sanitization:

- the usage code that shows how you are using Agently
- the framework code file path and line numbers that you believe are problematic
- a small code block that reproduces the issue or expectation gap

## References

- `references/source-map.md`
- `references/spec-first-intake.md`
- `references/standard-request-path.md`
- `references/high-quality-request-path.md`
- `references/ownership-and-escalation.md`
- `references/common-business-patterns.md`
- `references/current-skill-map.md`
