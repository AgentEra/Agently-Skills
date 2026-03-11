# Request Lifecycle In Flow

This page explains how a TriggerFlow chunk should create and consume model requests.

## 1. Prefer Async In Chunk Handlers

Inside async TriggerFlow handlers:

- use async request getters
- use `get_async_generator(...)`
- avoid sync generator bridges

Typical safe pattern:

```python
async def step(data):
    request = agent.create_request()
    request.input(data.value)
    result = await request.async_get_data()
    return result
```

## 2. Choose The Right Request Object

### `agent.create_request()`

Use this when the request should inherit agent settings and stable agent prompt context.

Good fit:

- shared model settings
- shared role / rule / user info on the agent
- one request per flow step while still inheriting agent defaults

### `agent.create_temp_request()`

Use this when the chunk should start from agent settings without inheriting prompt or extension-handler context.

Good fit:

- isolated helper requests
- side calculations
- memo extraction or classification requests that should not reuse the main agent prompt

### `Agently.create_request()`

Use this when the flow does not need an existing agent object at all.

Good fit:

- standalone request logic
- simple flow-local request builders
- cases where agent prompt inheritance would only add confusion

## 3. Final Result Versus Reusable Response

Use `async_get_data()` / `async_get_text()` when the chunk only needs one final view.

Use `get_response()` first when the chunk needs:

- streaming plus final data
- text plus metadata
- text plus structured data
- one request reused in more than one way

## 4. Important Concurrency Note

Do not treat one long-lived shared response object as a reusable workflow singleton.

The stable reuse unit is:

- one request
- one response snapshot
- many consumers of that same response

If several flow branches or items need model work, create separate requests for those units of work.
