---
name: agently-migration-playbook
description: Use when migrating an existing LangChain or LangGraph system into Agently and the first decision is whether the migration is agent-side LangChain work or workflow-side LangGraph orchestration work.
---

# Agently Migration Playbook

Use this skill first for migration requests with unresolved migration ownership.

## Native-First Rules

- classify the source system before giving implementation steps
- route LangChain agent-side work to `agently-langchain-to-agently`
- route LangGraph orchestration work to `agently-langgraph-to-triggerflow`

## Anti-Patterns

- do not mix LangChain and LangGraph migration guidance in one undifferentiated answer
- do not redesign the target stack before mapping the source surface

## Read Next

- `references/overview.md`
