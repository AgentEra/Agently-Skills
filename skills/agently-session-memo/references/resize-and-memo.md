# Resize And Memo

This page covers history trimming and memo updates inside `Session`.

## 1. Default Auto Resize

`Session` defaults to:

- `auto_resize=True`

When history changes:

- analysis runs
- a resize strategy may run

The default analyzer reads:

- `session.max_length`

## 2. Default Strategy

The built-in strategy is:

- `simple_cut`

Its job is to keep `context_window` within the configured length budget.

This can make:

- `full_context` larger than `context_window`

## 3. Custom Analysis Handler

Register:

- `register_session_analysis_handler(...)` through the agent
- or `session.register_analysis_handler(...)` on the session itself

The analysis handler decides which strategy name to run.

## 4. Custom Resize Handler

Register:

- `register_session_resize_handler("name", handler)` through the agent
- or `session.register_resize_handler("name", handler)` on the session itself

The handler returns:

1. `new_full_context` or `None`
2. `new_context_window` or `None`
3. `new_memo` or `None`

## 5. Memo Role

`memo` is for durable summarized facts, preferences, or constraints that should survive beyond the visible `context_window`.

Session request-prefix logic injects memo into the prompt as:

- `CHAT SESSION MEMO`

This is separate from:

- raw chat transcript history
- TriggerFlow runtime-data memo

## 6. Batch Of Guidance

- use `context_window` for recent turns
- use `memo` for compressed long-lived knowledge
- resize `context_window`, not `full_context`, when you only want to shorten what reaches the model
- update `memo` in custom resize handlers when summarization is needed

## 7. Important Boundary

`memo` here is session state.

If the caller is actually asking about workflow runtime state in TriggerFlow, that belongs to another skill.
