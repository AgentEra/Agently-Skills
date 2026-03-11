---
name: agently-input-composition
description: Use when composing Agently model input through prompt slots, quick prompt methods, agent-vs-request prompt layering, placeholder mappings, chat history, attachments, or other serializable prompt data before the request is sent.
---

# Agently Input Composition

This skill covers how to compose model input in Agently before the request is sent. It focuses on prompt slots, prompt layering, quick prompt methods, placeholder mappings, serializable prompt data, low-level `chat_history`, and attachments. It does not cover model setup, output schema control, YAML/JSON prompt template files, or session lifecycle management.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- choosing between agent-level and request-level prompt state
- using `set_agent_prompt(...)` and `set_request_prompt(...)`
- using quick prompt methods such as `system()`, `role()`, `rule()`, `user_info()`, `input()`, `info()`, `instruct()`, `examples()`, and `attachment()`
- deciding when to use `always=True`
- composing input with standard prompt slots
- using placeholder mappings in prompt keys and values
- passing lists, dicts, and other serializable data as prompt content
- using low-level `chat_history` as input-side context
- using `attachment()` for rich-content input
- inspecting prompt materialization with `to_text()` or `to_messages(...)`

Do not use this skill for:

- provider, endpoint, auth, proxy, or timeout setup
- `.output(...)`, `ensure_keys`, response streaming, or result parsing
- YAML/JSON prompt file loading or prompt round-tripping
- session activation, session resizing, or long-lived memory management
- TriggerFlow runtime stream composition

## Workflow

1. If the task is about persistent versus one-request prompt state, read [references/prompt-layers.md](references/prompt-layers.md).
2. If the task is about what each slot means or which slot to use, read [references/input-slots.md](references/input-slots.md).
3. If the task is about convenience methods such as `role()` or `input()`, read [references/quick-methods.md](references/quick-methods.md).
4. If the task is about variable substitution, nested data, or custom prompt keys, read [references/mappings-and-serialization.md](references/mappings-and-serialization.md).
5. If the task is about low-level `chat_history`, rich content, message rendering, or attachments, read [references/chat-history-and-attachments.md](references/chat-history-and-attachments.md).
6. If the behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

Agently input composition has two layers:

1. persistent agent prompt state
2. one-request prompt state

`get_response()` snapshots both layers into one response and then clears the request prompt. That is why some prompt content persists across turns and some does not.

Prompt generation then materializes that combined state into either:

- plain prompt text through `to_text()`
- chat-style messages through `to_messages(...)`

This matters most when low-level `chat_history` or `attachment` is involved, because rich content is only faithfully represented in message mode.

## Selection Rules

- long-lived baseline instructions -> agent-level prompt
- one-turn question or transient context -> request-level prompt
- explicit `system` or `developer` message control -> `set_agent_prompt(...)` or `set_request_prompt(...)`
- stable assistant identity or persona -> usually `system()` or `role(..., always=True)`
- supporting facts or retrieved context -> `info(...)`
- explicit behavioral constraints -> `instruct(...)` or `rule(...)`
- few-shot demonstrations -> `examples(...)`
- manual multi-turn conversation context without session lifecycle management -> `chat_history`
- image or rich-content input -> `attachment(...)`
- repeated prompt templates with variable substitution -> placeholder mappings
- exact inspection of multimodal payloads -> `to_messages(rich_content=True)`
- activated session, session-backed `chat_history`, or automatic turn recording -> `agently-session-memo`

## Minimal Valid Prompt Rule

At least one of these must be present for a normal prompt:

- `input`
- `info`
- `instruct`
- `output`
- `attachment`

If all of them are empty and no custom extra prompt keys are present, prompt generation fails.

`system`, `developer`, and `chat_history` alone do not satisfy this rule.

## References

- `references/source-map.md`
- `references/prompt-layers.md`
- `references/input-slots.md`
- `references/quick-methods.md`
- `references/mappings-and-serialization.md`
- `references/chat-history-and-attachments.md`
- `references/troubleshooting.md`
