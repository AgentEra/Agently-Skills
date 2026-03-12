---
name: agently-langchain-to-agently
description: Use when the main task is directly migrating LangChain agent-side surfaces into Agently, including agent setup, tools, structured output, middleware-like boundaries, retrieval, and short-term memory.
---

# LangChain To Agently

Use this skill after migration ownership is already confirmed to be LangChain agent-side work.

## Native-First Rules

- map source LangChain behavior to existing Agently capability surfaces
- keep migration focused on request-side and agent-side behavior
- escalate to TriggerFlow only when the source design truly depends on orchestration semantics

## Anti-Patterns

- do not treat every LangChain migration as a workflow migration
- do not preserve old abstractions when Agently already has a direct native surface

## Read Next

- `references/overview.md`
