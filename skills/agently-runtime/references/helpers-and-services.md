# Runtime Helpers and Service Adapters

Use this reference for three small public surfaces that do not create new
owner layers: `auto_func`, KeyWaiter, and `FastAPIHelper`.

## Choose by Contract

| Need | Surface | Boundary |
|---|---|---|
| Turn one typed Python function contract into one model-backed call | `@agent.auto_func` | Request convenience; not workflow orchestration. |
| React to completed structured fields from one execution | KeyWaiter methods | Stream convenience; fields remain provisional until final validation. |
| Expose an existing Agent/request/flow through Agently's packaged HTTP or streaming envelope | `FastAPIHelper` | Inbound transport adapter; not lifecycle owner. |

## `auto_func`

`@agent.auto_func` derives request input from the function signature, uses the
docstring as the instruction, derives output control from the return annotation,
and runs the request through the decorated Agent. A synchronous function creates
a synchronous wrapper; an `async def` creates an async wrapper. Generator
functions are not supported.

```python
from agently import Agently

agent = Agently.create_agent()


@agent.auto_func
async def classify_ticket(subject: str, body: str) -> dict:
    """Classify the ticket and return route plus a concise reason."""
    ...


result = await classify_ticket("Refund delayed", "My refund is still pending.")
```

Use this surface only when the signature, docstring, and return annotation are
the complete reusable contract for one model-backed function. Use an ordinary
fluent request when the contract needs explicit `info`, detailed output-field
semantics, validation, provider selection, or result streaming. Use
TriggerFlow when later work depends on a post-dispatch observation or visible
multi-stage lifecycle.

Actions already mounted on the Agent remain the owned way to perform tool calls
or side effects. `auto_func` does not turn model prose into side-effect proof and
does not replace Action authorization or validation.

## KeyWaiter

KeyWaiter is a convenience facade on `AgentExecution` structured `instant`
output. Use it only after declaring the target fields in `.output(...)`:

```python
execution = (
    agent
    .input("Draft a release note.")
    .output(
        {
            "title": (str, "Release-note title", "not_null"),
            "body": (str, "Release-note body", "not_null"),
        }
    )
)

for path, value in execution.wait_keys(["title", "body"]):
    render_preview(path, value)
```

Current convenience shapes are:

- `get_key_result(key)` / `async_get_key_result(key)` for the first completed
  value at one path;
- `wait_keys(keys)` / `async_wait_keys(keys)` for completed values at selected
  paths;
- `when_key(key, callback).start_waiter()` and
  `.async_start_waiter()` for registered callbacks while the execution runs.

Path completion is a streaming fact, not final business acceptance. Use these
callbacks for UI updates or explicitly cancelable/idempotent preparation. Do
not authorize irreversible work from them. When final validation, replacement
retries, or reconciliation matters, consume the `ModelRequestResult` stream
and then its final getter as described by `agently-request`.

Prefer async waiter methods in async services. Do not wrap KeyWaiter around
plain-text output; it depends on structured output paths.

## `FastAPIHelper`

`FastAPIHelper` is a `FastAPI` subclass for Agently's packaged request and
stream transport. Construction registers no route; call `use_post`, `use_get`,
`use_sse`, or `use_websocket` explicitly.

```python
from agently import Agently
from agently.integrations.fastapi import FastAPIHelper

agent = Agently.create_agent()

app = FastAPIHelper(response_provider=agent)
app.use_post("/chat")
```

The default request envelope is `{"data": ..., "options": {...}}`. The default
response envelope is `{"status": ..., "data": ..., "msg": ...}` with a
bounded error projection. A custom `response_warper` owns both success and
exception shaping; the default wrapper is not layered on top of it.

Use an async generator as `response_provider` for SSE/WebSocket streaming. If
the provider is a TriggerFlow, the non-stream response data is the flow's close
snapshot; project an application response explicitly when that snapshot is not
the public contract.

Use direct FastAPI for an ordinary typed HTTP API and FastMCP for MCP-server
exposure. Choose `FastAPIHelper` when its packaged request/response envelope and
route builders are the intended public transport. In every case, keep
authorization, execution lifecycle, validation, and retry in their owning
application/runtime layers rather than transport callbacks.
