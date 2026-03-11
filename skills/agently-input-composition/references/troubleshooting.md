# Troubleshooting

This page only covers input-composition issues.

## 1. A Prompt Part Disappears After One Request

Most common cause:

- it was written to the request prompt instead of the agent prompt

Check:

- whether the code used `set_request_prompt(...)`
- whether a quick method was called without `always=True`
- whether `get_response()` has already been created

## 2. The Prompt Fails Even Though `system` Or `chat_history` Is Set

Most common cause:

- there is no core prompt body

Reminder:

- `system`, `developer`, and `chat_history` alone do not satisfy the normal prompt emptiness check
- at least one of `input`, `info`, `instruct`, `output`, `attachment`, or a custom extra key must exist

## 3. `role()`, `rule()`, Or `user_info()` Feels Hard To Predict

Most common cause:

- these are helper wrappers, not exact low-level slot setters

Default advice:

- if the caller needs exact prompt shape, use `set_agent_prompt(...)` or `set_request_prompt(...)`

## 4. Placeholder Text Was Not Replaced

Check:

- whether `mappings` was provided
- whether the placeholder name matches exactly
- whether the unresolved placeholder should stay literal because no mapping entry exists

## 5. Rich Content Is Missing From Prompt Inspection

Most common cause:

- the prompt was inspected in plain-text or plain-message mode

Check:

- whether `to_text()` was used for multimodal content
- whether `to_messages(rich_content=False)` dropped non-text items

Use:

- `to_messages(rich_content=True)` for multimodal inspection

## 6. Chat History Looks Reordered Or Merged

Most common cause:

- `strict_role_orders=True`

Check:

- whether consecutive messages from the same role were merged
- whether synthetic boundary messages were inserted to normalize role order

## 7. The Caller's `chat_history` Was Overwritten

Most common cause:

- a session is activated and request-prefix logic replaced prompt history with session `context_window`

Check:

- whether `activate_session()` was called
- whether the active task really belongs to session-memo instead of low-level input composition

## 8. Custom Prompt Data Shows Up As Its Own Block

This is normal.

Custom prompt keys are rendered as extra prompt sections, not silently folded into `info` or `input`.

## 9. The User Is Really Asking About Session, Output, Or Provider Setup

Route the task to the right skill:

- session-backed continuity, auto recording, or resize -> `agently-session-memo`
- provider configuration -> `agently-model-setup`
- schema, parsing, streaming, or response reuse -> `agently-output-control`
