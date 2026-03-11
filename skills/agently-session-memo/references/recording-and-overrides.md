# Recording And Overrides

This page covers how session-backed history changes the meaning of `chat_history`.

## 1. Low-Level `chat_history` Without Session

Without an activated session:

- `set_chat_history(...)`
- `add_chat_history(...)`
- `reset_chat_history()`

operate on prompt-side agent state.

That is the low-level interface. It gives the developer direct responsibility for maintaining conversation history.

## 2. Session-Backed Override

With an activated session, those same helpers are overridden by `SessionExtension`.

They now update session state first:

- `full_context`
- `context_window`

Then they mirror the current `context_window` back into prompt `chat_history`.

So after session activation, prompt-side `chat_history` is no longer the source of truth.

## 3. Request Prefix Override

Before each request, session request-prefix logic overwrites prompt `chat_history` with the current session `context_window`.

That means:

- stale request-level `chat_history` is not authoritative
- the active session wins

## 4. Automatic Recording After The Response

After the response finishes, `SessionExtension` records:

- one user entry
- one assistant entry

Default behavior:

- user side records the current prompt text
- assistant side records parsed response data

## 5. Selective Recording With Keys

Use:

- `session.input_keys`
- `session.reply_keys`

to record only the fields that matter.

Supported forms include:

- direct keys like `city`
- nested paths like `info.task`
- special paths like `.agent.system` and `.request.input`

If these settings are `None`:

- session records the full prompt / full parsed result path

## 6. `clean_context_window()`

Use:

- `agent.clean_context_window()`

This clears the active session `context_window` and mirrors that empty window back into prompt `chat_history`.

It does not mean the entire `full_context` was deleted.

## 7. Practical Rule

- developer wants full manual control -> low-level `chat_history`
- developer wants lifecycle-managed continuity -> activate session and treat `chat_history` as session-backed
