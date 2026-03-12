---
name: agently-knowledge-base
description: Use when the main task is Agently embeddings, Chroma-backed indexing, retrieval, or retrieval-to-answer design, including embedding-agent setup, collection add/query, and KB-backed answer flows.
---

# Agently Knowledge Base

Use this skill when embeddings and retrieval are the main capability surface.

## Native-First Rules

- prefer embedding-agent plus Chroma integration before custom vector plumbing
- separate indexing, retrieval, and answer generation concerns
- keep retrieval results explicit when they feed a later request

## Anti-Patterns

- do not hide KB retrieval inside unrelated prompt logic
- do not treat embeddings-only setup and KB-backed answer flow as unrelated stacks

## Read Next

- `references/overview.md`
