# Troubleshooting

This page only covers embeddings issues.

## 1. The Request Hits The Wrong Endpoint

Most common cause:

- `model_type` was left as `chat`

Check:

- whether `OpenAICompatible.model_type` is set to `embeddings`
- whether the request URL ends with `/embeddings`

## 2. The Caller Expected Prompt Text Or Messages

Most common cause:

- embeddings were treated like chat generation

Reminder:

- embeddings requests are built from `input`
- they do not use chat `messages` or completions `prompt`

## 3. The Caller Added `info(...)` Or `.output(...)` But Nothing Changed

This is expected for embeddings request shape.

Check:

- whether the real payload is in `input(...)`

## 4. The Result Is Not A Single Vector

Most common cause:

- the caller assumed one input means one bare vector

Reminder:

- parsed embeddings results are normally returned as a list of vectors
- one input usually means a one-item list

## 5. `get_text()` Looks Wrong

Most common cause:

- a text getter was used for a vector workflow

Use:

- `start()`
- `get_data()`
- `async_start()`
- `async_get_data()`

## 6. The Batch Request Fails

Check:

- provider batch-size limits
- total input size
- whether the job should be split into several smaller batches

## 7. The Service Needs Better Throughput

Default advice:

- batch texts that belong together first
- then prefer `async_start()` for concurrent batches

## 8. The Caller Expected Streaming Embeddings Events

Most common cause:

- embeddings were treated like chat/completions streaming

Reminder:

- embeddings are not the `delta` / `instant` / `specific` workflow
- `stream` does not give embeddings a streaming event flow
- embeddings return one completed result

## 9. Fast Triage

- endpoint shape issues: check `model_type="embeddings"`
- request body confusion: check `input(...)`
- result shape confusion: check `get_data()` versus `get_text()`
- throughput issues: check batching first, then async concurrency
- streaming confusion: check whether the task is really embeddings rather than chat/completions
- vector-store wiring issues: validate the embedding agent before debugging retrieval
