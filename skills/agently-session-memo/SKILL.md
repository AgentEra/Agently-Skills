---
name: agently-session-memo
description: Use only when the main task is Session-backed conversation continuity and restore for Agently requests, such as `activate_session()`, session ids, session-backed chat history, `session.input_keys`, `session.reply_keys`, memo, context-window resizing, or session serialization.
---

# Agently Session Memo

This skill is the direct leaf for Session-backed conversation continuity after the request path is already known. It focuses on session activation, session isolation by id, session-backed `chat_history`, automatic request/reply recording, `full_context`, `context_window`, `memo`, resize strategies, and session serialization. It does not choose between low-level prompt history, service exposure, or workflow state design, and it does not cover provider setup, structured output control, or TriggerFlow runtime-data memo.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- `activate_session()` and `deactivate_session()`
- understanding how session-backed `chat_history` differs from manual `set_chat_history(...)` and `add_chat_history(...)`
- session isolation by `session_id`
- automatic request-prefix injection from `context_window`
- automatic finally-stage recording of user and assistant turns
- `session.input_keys` and `session.reply_keys`
- `full_context`, `context_window`, and `memo`
- `session.max_length`, default auto-resize, and custom analysis / resize handlers
- `clean_context_window()`
- exporting and restoring session state through JSON or YAML
- restoring conversation continuity into a fresh agent after service restart
- combining session restore with TriggerFlow execution restore when conversation memory and workflow state are separate

Do not use this skill for:

- general prompt-slot composition outside the session boundary
- model setup, auth, proxy, or network client configuration
- `.output(...)`, `ensure_keys`, response streaming, or response reuse patterns
- TriggerFlow runtime-data memo or workflow-state design
- full RAG or knowledge-base orchestration

## Core Boundary

Agently has two conversation-history layers:

1. low-level prompt-side `chat_history`
2. session-backed memory through `SessionExtension`

Without an activated session, `set_chat_history(...)`, `add_chat_history(...)`, and `reset_chat_history()` are low-level prompt-state helpers.

With an activated session, those same helpers become session-backed operations. They update `Session` state first and then mirror the current `context_window` back into prompt `chat_history`.

## Workflow

1. If the task is about turning session on or off, picking `session_id`, or switching between sessions, read [references/session-lifecycle.md](references/session-lifecycle.md).
2. If the task is about `chat_history`, automatic recording, request-prefix injection, or `session.input_keys` / `session.reply_keys`, read [references/recording-and-overrides.md](references/recording-and-overrides.md).
3. If the task is about trimming history, `session.max_length`, custom resize handlers, or memo updates, read [references/resize-and-memo.md](references/resize-and-memo.md).
4. If the task is about exporting, loading, or restoring session state, read [references/serialization-and-restore.md](references/serialization-and-restore.md).
5. If the task is about recovering a real conversation after restart, reconnect, or long suspension, read [references/business-restore-recipes.md](references/business-restore-recipes.md).
6. If the behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

Agently session memory has three state buckets:

1. `full_context` for the full recorded history
2. `context_window` for the history that will actually be injected into the next request
3. `memo` for durable summarized facts, preferences, or constraints

`SessionExtension` attaches that state to the agent lifecycle:

- request prefix -> inject `context_window` and `memo`
- finally hook -> record the current user and assistant turn back into the session

Session serialization restores session state, not the whole application runtime. Agent setup, model settings, tools, and TriggerFlow execution state still have to be rebuilt or restored separately.

## Selection Rules

- manual prompt-side multi-turn setup only -> `set_chat_history(...)` / `add_chat_history(...)` in input composition
- persistent conversation continuity across turns -> activate a session
- per-user or per-thread history isolation -> stable `session_id`
- only keep selected fields from input or reply -> `session.input_keys` / `session.reply_keys`
- shrinking history under a limit -> `session.max_length` or custom resize handlers
- storing long-lived compressed facts -> `memo`
- saving and restoring a session -> JSON / YAML serialization
- restarting a chat service and continuing the same conversation -> restore the session into a fresh agent
- restoring both workflow progress and chat continuity -> combine this skill with `agently-triggerflow-config` and `agently-triggerflow-execution-state`
- TriggerFlow execution-scoped memo -> not this skill

## References

- `references/source-map.md`
- `references/session-lifecycle.md`
- `references/recording-and-overrides.md`
- `references/resize-and-memo.md`
- `references/serialization-and-restore.md`
- `references/business-restore-recipes.md`
- `references/troubleshooting.md`
