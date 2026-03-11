# Troubleshooting

This page only covers session-memo issues.

## 1. `chat_history` Keeps Changing Even Though The Caller Set It Manually

Most common cause:

- a session is activated

Reminder:

- session request-prefix logic overwrites prompt `chat_history` with session `context_window`

## 2. The Agent Forgot Earlier Turns

Check:

- whether the right `session_id` is active
- whether the caller accidentally deactivated the session
- whether resize logic trimmed `context_window`

## 3. History Looks Shorter Than Expected

Most common cause:

- `context_window` was resized while `full_context` remained longer

Check:

- `session.max_length`
- custom analysis handlers
- custom resize handlers

## 4. The Recorded User Or Assistant Content Looks Too Large

Most common cause:

- full prompt / full parsed result recording is still enabled

Use:

- `session.input_keys`
- `session.reply_keys`

to narrow recording down to only the fields that matter

## 5. `clean_context_window()` Did Not Delete Everything

Reminder:

- it clears the active `context_window`
- it does not mean `full_context` was erased

## 6. Restored Session Does Not Resume Automatically

Check:

- whether the restored session was inserted into `agent.sessions`
- whether `activate_session(session_id=...)` was called after restore

## 7. The Caller Is Really Asking About Manual Prompt Composition

Route it back:

- low-level `chat_history` and prompt slots -> `agently-input-composition`
- session-backed continuity, resize, memo, export/restore -> this skill
