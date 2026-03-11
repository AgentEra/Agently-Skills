# Input Slots

These are the main input-side slots to think about when composing an Agently request.

## 1. `system`

Use for top-level system behavior or global framing.

Typical examples:

- assistant identity
- high-level behavior policy
- durable operating rules that should sit outside the user turn

## 2. `developer`

Use when the caller wants an explicit developer-role message instead of putting everything into `system` or `instruct`.

This slot is available through exact prompt APIs such as:

- `set_agent_prompt("developer", ...)`
- `set_request_prompt("developer", ...)`

## 3. `info`

Use for supporting facts, retrieved context, reference data, or side information the model should consider.

Good fit:

- knowledge snippets
- structured context dictionaries
- bullet-style supporting facts

## 4. `instruct`

Use for direct behavioral instructions or procedural constraints.

Good fit:

- required answer style
- forbidden behaviors
- step-by-step instructions

## 5. `examples`

Use for few-shot demonstrations or example I/O pairs.

Good fit:

- desired phrasing patterns
- classification examples
- format demonstrations

## 6. `input`

Use for the current user task, question, or primary payload.

This is the most common one-turn slot.

## 7. `chat_history`

Use for prior conversation turns when the caller is manually maintaining prompt-side history.

Each item is a message with:

- `role`
- `content`

`content` can be plain text or a list of rich content parts.

Important boundary:

- with an activated session, `chat_history` becomes session-backed and is better understood through the session-memo skill

## 8. `attachment`

Use for rich content that should accompany the user message.

Typical examples:

- image input for a VLM-capable request
- text attachment blocks
- other content parts that the target requester can forward as message content

## 9. Custom Extra Keys

Agently also accepts custom prompt keys outside the standard slot list.

These keys become extra prompt sections during rendering and are useful when the caller wants named structured context that does not naturally fit `info`, `instruct`, or `input`.

## 10. Important Boundary

For input-composition work, the main slots are:

- `system`
- `developer`
- `info`
- `instruct`
- `examples`
- `input`
- `chat_history`
- `attachment`

Other standard slots such as `output`, `options`, `tools`, and `action_results` exist, but they belong to other skills or broader workflows.
