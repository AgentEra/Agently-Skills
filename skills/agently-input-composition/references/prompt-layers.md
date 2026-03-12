# Prompt Layers

Agently input composition uses two prompt layers.

## 1. Agent Prompt

Use the agent prompt for context that should survive across future requests on the same agent instance.

Main entry points:

- `set_agent_prompt(key, value, mappings=None)`
- quick prompt methods with `always=True`

Typical uses:

- long-lived system instructions
- stable persona or role framing
- shared background information
- persistent `chat_history`

## 2. Request Prompt

Use the request prompt for context that belongs to the next request only.

Main entry points:

- `set_request_prompt(key, value, mappings=None)`
- quick prompt methods without `always=True`

Typical uses:

- the current user task
- temporary facts or retrieved context
- one-off examples
- one-off attachments

## 3. Snapshot And Clear Behavior

`get_response()` creates a response snapshot from the current merged prompt state and then clears the live request prompt.

Practical consequence:

- agent-level prompt state remains available for later requests
- request-level prompt state does not remain available after the response is created

If the user says a prompt "disappeared after one call", this is usually the reason.

## 4. When To Prefer Exact Slot APIs

Use `set_agent_prompt(...)` or `set_request_prompt(...)` when:

- the target slot must be exact
- the caller needs the `developer` slot
- the caller wants a custom extra prompt key
- the caller does not want helper behavior from convenience wrappers

## 5. One-Off Request Style

If the user wants a standalone request without agent-level prompt reuse, the cleanest pattern is a request instance and direct prompt mutation.

Typical path:

- `request = Agently.create_request()`
- `request.set_prompt(...)`

This keeps the input scope local to that request object.

## 6. Prompt Asset Boundary

If the prompt content should be:

- reviewed outside runtime code
- reused across services
- versioned as data

move the reusable part into YAML or JSON prompt config instead of keeping the whole prompt shape inline in Python.
