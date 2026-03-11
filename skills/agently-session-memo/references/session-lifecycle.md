# Session Lifecycle

This page covers the on/off lifecycle of Agently sessions.

## 1. Turn Session On

Use:

- `agent.activate_session(session_id="...")`

When a matching id already exists:

- the existing session is reused

When the id does not exist:

- a new `Session` object is created

If no id is passed:

- Agently generates one

## 2. Session Isolation By Id

Use different ids for isolated histories.

Use the same id to continue the same history.

Typical production keys:

- `user_id`
- `tenant:user_id`
- `conversation_id`

## 3. Turn Session Off

Use:

- `agent.deactivate_session()`

This does two important things:

- clears `activated_session`
- clears prompt-side `chat_history`

## 4. Request Lifecycle Integration

Once a session is activated, the agent lifecycle changes:

- before request: current `context_window` is injected into prompt `chat_history`
- after response: the user turn and assistant turn are recorded back into the session

That is why session-backed history keeps moving even when the caller stops manually maintaining `chat_history`.

## 5. `full_context` Versus `context_window`

- `full_context` is the full recorded history
- `context_window` is the subset that will be injected into the next request

They may differ after resize logic runs.

## 6. Practical Selection

- one-off manual multi-turn examples -> low-level `chat_history`
- real conversation continuity -> activate a session
- separate user threads -> different `session_id`
- temporary stateless turn -> deactivate session or use a fresh agent
