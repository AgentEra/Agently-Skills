# Agently Model Result

Use this skill when the output contract is already chosen and the remaining issue is how the result facade should be consumed or reused.

The user does not need to say `get_result()`. Requests to reuse one result as text, parsed data, metadata, or progressive updates should route here.

Optional request scheduling belongs to model request settings, not custom
caller-side semaphores. Use `model_request.scheduler.max_concurrency`,
`model_request.scheduler.rate_per_second`, and optional
`model_request.scheduler.providers.<provider>` overrides when a service or
long-running task needs provider-level dispatch limits. Use
`model_request.retry_backoff_base` and `model_request.retry_backoff_max` when
retries should back off instead of immediately re-issuing. If these settings are
absent, dispatch and retry timing keep the legacy immediate behavior.

## Reuse One Result or Start a Later Request

One result can expose text, structured data, metadata, and progressive fields
without reissuing its ModelRequest. It cannot gain new input after dispatch.
Keep supporting semantic fields and the final answer in one ordered output
contract when they share the request-time input/evidence snapshot and later
fields need only earlier fields from that same response.

Start a later ModelRequest when its semantic output needs a fact created by an
Action, tool, API/database read, file or artifact readback, approval/resume, or
host computation after the first request was dispatched:

```text
R1 plan
-> execute and validate observed result
-> R2 judgment or grounded answer
```

`instant` may start cancelable/idempotent work from a complete early field. If
the result of that work is needed by model generation, it still crosses this
boundary: reconcile and join first, then supply the observed result to R2.
Streaming cannot inject later data into the already-running R1.

## Native-First Rules

- prefer `get_result()` when one request result must be consumed more than once
- default to async-first response APIs in services, streaming paths, TriggerFlow steps, and any integration that may overlap work
- No progressive consumer means no stream: directly await
  `result.async_get_data()`. A discard-only `instant` drain loop adds queue,
  event-iteration, and parser work without creating output value. Open a
  generator only when its items are actually published, recorded, or applied
- treat sync getters and generators as convenience wrappers for scripts, REPL use, or compatibility bridges
- use `delta`, `instant`, `specific`, or `all` instead of custom stream splitting logic
- for AgentExecution streams, `type="delta"` remains the public string stream;
  `type="instant"` preserves source `AgentExecutionStreamData` items and appends
  synthetic `path="$delta"` text-projection items only when a source item can be
  projected to natural language; `type="all"` is for raw records/audits and must
  not include synthetic `$delta` items
- treat `$delta` as the unified natural-language stream slot inside
  `instant`, not as another source-addressed field delta. Consumers that need
  both `$delta` and detailed paths should render them into separate surfaces:
  append `$delta` to the visible text stream and use source-addressed deltas
  such as `model.delta` or output field paths only to update structured UI state.
  Internal bridges, recorders, and audits should consume `type="all"` so derived
  `$delta` projection items do not become source facts.
- for AgentTask or TaskBoard UI, prefer `instant` over parsing public text:
  render source-addressed paths into state panels and synthetic `$delta` into the
  visible process feed. Public `delta` remains printable CLI text; it may render
  the first TaskBoard board projection as a compact table and later ticks as
  card-state changes, and it separates process paragraphs from model body
  deltas. Do not add a default parallel narrator request only for prettier
  progress text; use bounded process fields from the existing planner/verifier
  request when richer wording is needed.
- when OpenAICompatible replays a transient disconnect after partial output,
  treat `StreamingData(path="$status", value=...)` as a framework control record:
  `failed` plus `retry=True` invalidates provisional output and requires the UI
  or SSE consumer to clear it before replacement deltas arrive. Plain `delta`
  streams emit the standalone `"<$retry>{reason}</$retry>"` marker at that
  same boundary; clear the local text buffer when it arrives. Use `instant`,
  `specific="status"`, or `all` when lineage or collision-free structured
  facts matter. Do not force a freeform document body through `.output()` only
  to obtain instant fields; handle replay boundaries at the consumer when
  plain delta is the right body stream
- annotate common stream consumers from `agently`: `StreamingData` for
  `instant` / `streaming_parse`, `AgentlySpecificResultMessage` for
  `specific`, and `AgentlyModelResultMessage` for `all`; use
  `agently.types.data` when the full typed data namespace is needed
- subscribe to `reasoning_delta` / `reasoning_done` through `type="specific"`
  when reasoning output is needed. Provider-native reasoning and a leading
  outer `<think>...</think>` before the answer payload belong in reasoning
  events; `original_delta` / `original_done` keep the raw provider content.
  Payload-internal `<think>` remains ordinary answer text
- treat `instant` `.is_complete` as path completion, not a global display-order
  barrier. For Web UI, SSE, or WebSocket consumers, render each path into its
  own slot. For CLI consumers that print multiple paths into one terminal area,
  use a small state flag or buffer and flush later-path deltas only after the
  earlier path's completion event has been handled
- map the first observed event under a target field to a stable host-owned
  status when "generation started" is useful. Start downstream work only from a
  complete canonical field or list item, such as
  `wildcard_path == "retrieval_tasks[*]" and is_complete`
- do not await long downstream work inside the stream loop. Dispatch it through
  a bounded, managed async owner and continue consuming. Deduplicate using a
  host-derived key from the task-relevant payload
- after the stream, treat `async_get_data()` as authoritative and reconcile its
  accepted items with provisional work. Validation retry can produce accepted
  data that was not observed on the original instant stream; start missing
  accepted work and cancel or discard provisional extras

Final-only consumption:

```python
result = (
    agent
    .input("Classify this ticket.")
    .output({"route": (str, "billing | technical | other", True)})
    .get_result()
)
data = await result.async_get_data()
```

Discard-only streaming is an anti-pattern:

```python
async for _item in result.get_async_generator(type="instant"):
    pass
data = await result.async_get_data()
```

When a real consumer exists, publish the stream and reuse the same result:

```python
async for item in result.get_async_generator(type="instant"):
    await publish_structured_patch(item)
data = await result.async_get_data()
```

For early retrieval or preparation, use:

```text
complete instant item
-> host payload key
-> managed bounded dispatch
-> keep consuming
-> final async_get_data()
-> reuse / start missing / cancel or discard extras
```

This avoids both all-serial latency and duplicate work. `$status` retry events
are useful observer facts, but they do not replace final reconciliation.
Irreversible effects still wait for the final accepted result. See
`../../agently-triggerflow/examples/instant_retrieval_overlap.py`.

## Anti-Patterns

- do not re-issue the same request to obtain text, data, and metadata separately
- do not open and discard a stream when a final getter is the only consumer
- do not build ad hoc field-level stream parsers when `instant` or `streaming_parse` already fits
- do not strip reasoning tags inside format-specific parsers

## Read Next

- `references/overview.md`
