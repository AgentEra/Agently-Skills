---
name: agently-session-memory
description: Use when the main task is Session-backed continuity, memo, or restore in Agently, including session ids, chat history continuity, memo, restore after restart, and request-side conversational state placement.
---

# Agently Session Memory

Use this skill when the request path already exists but continuity or restore behavior is the main design problem.

## Native-First Rules

- prefer Session-backed continuity before inventing a custom memory layer
- keep request-side chat history and memo boundaries explicit
- separate request memory from workflow runtime state

## Anti-Patterns

- do not use session as a substitute for workflow orchestration state
- do not keep restart-sensitive memory only in transient globals

## Read Next

- `references/overview.md`
