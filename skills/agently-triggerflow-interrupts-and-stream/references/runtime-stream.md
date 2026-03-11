# Runtime Stream

Runtime stream is for live workflow output.

## 1. Produce Stream Items

Use:

- `await data.async_put_into_stream(item)`
- `data.put_into_stream(item)`

Typical stream content:

- progress updates
- incremental business data
- interrupt notifications
- user-facing live output

If a flow has a user stream contract:

- user-defined stream items are validated against that contract
- built-in interrupt events can still appear in the runtime stream as system events

## 2. Stop Stream

Use:

- `await data.async_stop_stream()`
- `data.stop_stream()`

Do this when the runtime stream is intentionally complete.

## 3. Consume Stream

Prefer async:

- `execution.get_async_runtime_stream(...)`
- `flow.get_async_runtime_stream(...)`

Sync bridge:

- `execution.get_runtime_stream(...)`
- `flow.get_runtime_stream(...)`

## 4. Timeout Behavior

If a consumer uses a finite timeout and no new stream item arrives:

- the consumer can stop by timeout warning

So:

- use `timeout=None` for long-lived sessions
- use explicit `stop_stream()` when the stream is complete

## 5. Final Result Boundary

Runtime stream does not define the final result automatically.

If the caller also needs a final result:

- still reach `end()`
- or set the result explicitly

## 6. Contract-Aware Consumer Design

If the flow uses a stream contract and also uses interrupts:

- expect typed business stream items
- also expect system interrupt events such as pause or resume

Do not assume every runtime stream item belongs to the user-defined business schema.
