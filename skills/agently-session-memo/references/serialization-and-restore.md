# Serialization And Restore

This page covers saving and restoring `Session` state.

## 1. Export

Use:

- `session.get_json_session()`
- `session.get_yaml_session()`

These include:

- `id`
- `auto_resize`
- `full_context`
- `context_window`
- `memo`
- `session_settings`

## 2. Restore

Create a `Session` and then load:

- `load_json_session(...)`
- `load_yaml_session(...)`

You can load from:

- raw JSON / YAML content
- a file path

## 3. Nested Session Data

If session data is nested inside a larger payload, use:

- `session_key_path=...`

That lets the loader read the session object from a nested key path.

## 4. Reattach To An Agent

After restoring:

1. assign the restored session into `agent.sessions[...]`
2. `activate_session(session_id=...)`

Then the normal request-prefix and finally hooks resume.

## 5. What This Does Not Restore

Session restore does not rebuild:

- model settings or provider credentials
- tool registration or runtime resources
- application-specific routing state
- TriggerFlow flow definition or execution progress

Restore those separately when the surrounding application needs them.

## 6. Practical Advice

- export after important checkpoints
- restore into a fresh session object before reattaching
- validate the restored `id`, `context_window`, and `memo` before using it in production
