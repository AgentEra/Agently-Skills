# Troubleshooting

This page only covers TriggerFlow model-integration issues.

## 1. `asyncio.run()` Or Sync-Bridge Errors In A Chunk

Most common cause:

- sync generator or sync getter used inside an async flow handler

Fix:

- use `async_get_*()` and `get_async_generator(...)`

## 2. Model Output Streams But The Flow Does Not Finish

Most common causes:

- the chunk streamed data but never returned a final value
- runtime stream was left open when the caller expected it to stop

Check:

- whether the chain reaches `end()` or sets a result
- whether runtime stream should be stopped explicitly

## 3. Too Many Model Calls Start At Once

Most common cause:

- unbounded dispatch from `instant` items or large item lists

Prefer:

- `for_each(concurrency=...)`
- `batch(...)`
- bounded `asyncio.gather(...)`

## 4. The Chunk Needs Streaming And Final Data But Only Sees One

Most common cause:

- shorthand getter used instead of `get_response()`

Fix:

- create one response first
- stream from the response
- then read the final data from `response.result`

## 5. Structured Streaming Is Hard To Reason About

Most common cause:

- too much output-control detail is being solved in the TriggerFlow skill

Fix:

- use `agently-output-control` for schema order, `ensure_keys`, and structured-streaming semantics
- keep this skill focused on how the flow uses the response
