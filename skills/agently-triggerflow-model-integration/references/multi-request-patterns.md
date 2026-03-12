# Multiple Model Request Patterns

This page covers how to organize several model requests inside one TriggerFlow workflow.

## 1. One Workflow Step, One Model Call

Use one chunk with one request when:

- the workflow is still linear
- only one final model result is needed
- there is no reason to expose intermediate routing

## 2. Fan-Out Across Fixed Branches

Use `batch(...)` when one input should trigger several named model branches.

Good fit:

- summarize the same source for different audiences
- run several analysis lenses on one document
- produce several independent fields through separate model calls

Why:

- branch names stay explicit
- collected results remain structured
- concurrency can be bounded on the orchestration side

## 3. Item-Wise Model Calls

Use `for_each(concurrency=...)` when a list of items should each run through model logic.

Good fit:

- summarize each section
- classify each message
- expand each outline item

This is usually the cleanest way to control parallelism for many similar model calls.

## 4. Several Independent Calls Inside One Chunk

Use controlled `asyncio.gather(...)` only when:

- all calls logically belong to one chunk
- separate flow routing would add noise
- the caller still wants async overlap

Keep it bounded:

- use a fixed small set of tasks
- or apply a semaphore before gathering many tasks

## 5. `instant`-Driven Follow-Up Work

`instant` does not create model requests by itself.

What it does:

- exposes structured fields or list items as soon as they complete

That earlier visibility can be used to trigger more work.

Preferred pattern:

- read `instant` items
- wait for `is_complete`
- emit a flow event and route it with `when(...)`, or accumulate items
- hand them to `for_each(concurrency=...)` or another bounded orchestration path

Avoid:

- spawning unbounded background tasks directly inside the `instant` consumer loop

`delta` can also be bridged into `when(...)`, but it is usually too granular for heavy downstream work.

## 6. Which Pattern To Choose

- fixed set of named branches -> `batch(...)`
- variable list of similar items -> `for_each(concurrency=...)`
- small one-off set of internal helper requests -> controlled `asyncio.gather(...)`
- progressive structured output that should trigger more work -> `instant` plus bounded flow routing

For quality-focused systems:

- visible draft, judge, revise stages -> separate TriggerFlow steps
- cheaper or local models that need bounded improvement passes -> evaluator-optimizer plus explicit turn budget
