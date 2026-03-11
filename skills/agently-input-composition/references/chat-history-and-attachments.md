# Chat History And Attachments

This page covers the two richest input-side structures in Agently.

## 1. `chat_history`

Use low-level `chat_history` for previous conversation turns when the developer is manually managing conversation state.

Main agent helpers:

- `set_chat_history(...)`
- `add_chat_history(...)`
- `reset_chat_history()`

On an agent instance, `set_chat_history(...)` and `add_chat_history(...)` write to persistent prompt state.

`reset_chat_history()` clears the stored low-level prompt-side history.

Important boundary:

- once a session is activated, these helpers become session-backed operations through `SessionExtension`
- prompt-side `chat_history` is then a mirror of session `context_window`, not the source of truth
- session lifecycle, auto recording, and resize logic belong in `agently-session-memo`

## 2. Chat Message Shape

Each history item is a message with:

- `role`
- `content`

`content` can be:

- plain text
- a list of rich content parts

## 3. How `to_text()` Treats Chat History

`to_text()` includes chat-history text content in a readable prompt block.

Important limitation:

- non-text rich content in `chat_history` is skipped during text rendering
- Agently emits warnings when that happens

## 4. How `to_messages(...)` Treats Chat History

`to_messages(rich_content=True)` preserves rich message content.

`to_messages(rich_content=False)` simplifies content down to text and drops non-text items that cannot be represented in plain message text.

`strict_role_orders=True` also normalizes history by:

- merging consecutive messages from the same role
- ensuring the history starts with `user`
- ensuring the history ends with `assistant`

This is helpful for requesters that expect alternating roles.

## 5. `attachment`

Use `attachment(...)` for input-side rich content that should travel with the user message.

Typical uses:

- image understanding requests
- text-plus-file requests
- multimodal prompt construction

## 6. How `attachment` Is Rendered

For actual message payload inspection, prefer:

- `to_messages(rich_content=True)`

Important behavior:

- rich attachments are preserved in rich message mode
- non-text attachments are skipped in plain message mode
- plain prompt text does not faithfully represent rich attachment payloads

## 7. Practical Debugging Rule

If the user says an image or rich attachment "is missing", inspect the composed prompt with `to_messages(rich_content=True)` before assuming the requester or provider is wrong.
