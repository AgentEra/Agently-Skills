# Agently Output Control

Use this skill when the question is what shape the model should return and how that shape should stay reliable.

The user does not need to say `.output(...)`, tuple `ensure`, `ensure_keys`, or `.validate(...)`. Requests for stable JSON-like fields, structured reports, or machine-readable sections should route here.

## Rule-First Business Validation

When application code expects model output to satisfy a business rule and a
post-generation validator will accept, reject, or retry that output, give the
model the satisfiable rule before the first attempt. Put runtime candidate
values and limits in `input`, authoritative policy or interface facts in
`info`, behavior and transformation rules in `instruct`, and field types,
requiredness, enum/range/format/nullability, and cross-field constraints in
`output`.

Keep `.validate(...)`, Pydantic, DTO, authorization, and side-effect checks as
deterministic acceptance authorities. Telling the model the rule does not
replace enforcement. A validator's bounded retry `reason` is correction
feedback for an already-declared contract; it is not the primary way to reveal
rules. The topology

```text
underspecified generation -> hard rejection -> retry learns one more rule
```

is blind gate discovery and an anti-pattern. It wastes calls, raises latency
and cost, makes acceptance depend on collision order, and may exhaust retries
without proving whether the task is impossible or merely underspecified.

Host-only authorization, security, anti-abuse, integrity, and holdout evaluation
details may remain hidden when disclosure would weaken the gate or leak an
expected answer. Still provide the safe public contract the model is allowed to
follow. Do not turn an intentionally hidden gate into an automatic
trial-and-error tutor; prefer a non-retryable fail-closed result, safe
normalization, manual review, or another explicitly owned fallback.

If a requested production gate cannot be expressed safely or concretely but
the developer still asks to hard-reject or retry model output, stop before
implementation and issue a warning that names:

- the missing or intentionally hidden rule and affected output;
- why the model cannot anticipate the acceptance condition;
- expected retry, latency, cost, nondeterminism, and liveness risks;
- safer options such as declaring a non-sensitive rule subset, changing the
  schema, deterministic normalization, fail-closed handling, or manual review;
- the proposed retry/terminal policy if the hidden gate is retained.

Implement only after a new developer response explicitly confirms that named
gate and its risks. A prior blanket instruction to proceed is not this second
confirmation. Without confirmation, do not silently add the gate.

## Host-Resolved Selection Outputs

For a model-selected host record, return the offered selection key, not copied
canonical ids or another request id. A selection's offered-set membership
proves membership, not freshness. If the decision can cross a cache, queue,
retry, persistence, or replay boundary, bind it to a Host-owned
request/execution revision or issue per-request opaque keys, and validate Host
correlation before canonical lookup. Prefer Host-bound lineage over asking the
model to copy another request id. A strictly inline awaited response that
cannot cross a request boundary needs no extra model-returned correlation
field.

## Restructure Complex Output After Measured Failures

Deep nesting is not automatically a defect. Consider a simpler model-facing
structure when representative runs show more schema violations, missing keys,
ensure failures/retries, or output-length failures. First inspect the rendered
prompt, supported schema/format, raw result, provider finish reason and actual
output limit; separate input/contract gaps, provider truncation, and parser
defects from model-generation complexity.

- Flatten redundant hierarchy into a compact decision projection where useful.
  For example, Host-owned groups need not be copied around each item decision:
  the model can return an offered item key and the decision, and the Host can
  restore group membership and the full object. Preserve all decision-relevant
  context, relationships, types, and evidence; do not hide structure inside an
  untyped string or rely on positional joins between unrelated arrays.
- Split coherent business sections or bounded batches when their consumer,
  evidence, output size, or independent validation/repair boundary justifies
  it. Model-owned semantic decisions remain model-owned. Map serial dependencies
  and bounded parallel work through TriggerFlow, then assemble in Host code.
  Do not make every field a separate request or split a reliable contract only
  because it looks nested.
- Keep the external API/DTO contract and hard acceptance rules unchanged.
  Declare the simpler intermediate contract, restore the required shape through
  an explicit Host mapping, and validate both parts and the assembled result.
  Missing required fields are not fixed by removing ensure or making them
  optional merely to pass tests.
- Compare the same representative cases before and after: format/key success,
  ensure failures, retries, length failures, request count, latency, observed usage, and
  semantic coverage. A structurally valid but information-losing flattening is
  not an improvement.

For planned section-by-section prose rather than one structured result, read
[planned long-form writing](../../agently-design/references/lifecycle-and-pressure-design.md).

## Native-First Rules

- default to async-first response consumption when structured output will be streamed, reused, or served over an async boundary
- prefer prompt-config-owned output contracts such as `.execution.output` when
  the schema is stable and shared across a request family
- prefer `.output(...)` for machine-readable results when the schema is dynamic, exploratory, or easier to keep close to code
- for Agently `4.1.4.3+`, a Pydantic v2 `BaseModel` class may be passed
  directly to `.output(ModelClass, format=...)`, including models with nested
  `BaseModel` fields and lists. Agently projects requiredness, nullability,
  aliases, enum/literal values, length constraints, numeric bounds,
  `multiple_of`, patterns, and recognized formats recursively into the
  model-facing field requirements for every structured output format. The
  original class remains the typed acceptance authority for
  `get_data_object()` / `async_get_data_object()`
- when parsed output feeds an API, SDK, module interface, or function directly,
  mirror the consumed request/argument structure instead of an opaque dict.
  If a measured complexity problem justifies an intermediate projection, use
  the explicit Host reconstruction and final validation described above.
  Describe every consumed field with its contract meaning, exact type,
  requiredness, and any applicable enum, format, range, unit, nullability, or
  cross-field dependency. Pair the schema with authoritative interface material
  in `info(...)`, request facts in `input(...)`, and transformation/call rules
  in `instruct(...)`. This field-level output control is not business-logic
  intrusion and does not replace deterministic validation before side effects
- choose output format deliberately:
  - omitted `.output(..., format=...)` reads `prompt.default_output_format`;
    the framework default is `json`, and individual agents or requests may
    override it through settings. Explicit `format="auto"` or
    `prompt.default_output_format="auto"` uses structural selection and does
    not inspect field names or business meaning: flat string-only dict schemas
    resolve to `xml_field`; dict schemas that mix string fields with typed
    non-string fields resolve to `hybrid`; all-control, all-complex, and
    non-dict schemas resolve to `json`. `yaml_literal` is explicit opt-in, and
    `flat_markdown` is explicit-only compatibility mode
  - use `format="flat_markdown"` only when preserving legacy section-header
    output is required
  - use `format="hybrid"` for string prose/code fields mixed with typed fields,
    such as `summary` plus `citations`, `analysis` plus `components`, or
    `notes` plus `ready` and `next_steps`, after the target provider/model has
    passed representative stability checks.
    Non-string hybrid sections must use fenced JSON, including booleans and
    numbers; Agently's built-in prompt generator renders JSON value examples
    for current `hybrid` output
  - use explicit `format="xml_field"` for flat string-only dict schemas or when
    XML-like field boundaries are intentionally preferred. Auto also selects
    `xml_field` for flat string-only dict schemas. Agently parses this with a
    custom boundary parser, not strict XML
  - use explicit `format="yaml_literal"` only when the team intentionally
    wants a YAML target document and accepts YAML indentation sensitivity
  - use `format="json"` when downstream code needs the legacy JSON-only
    contract, external API interop, exact raw JSON behavior, or dense all-typed
    arrays/objects
  - use plain text instead of `.output(...)` for one freeform artifact: an
    article, email, explanation, report, Markdown page, HTML page, or other
    single multi-paragraph document; read it with `start()` / `async_start()` or
    `response.result.get_text()`
- when one direct business result may exceed the provider output window, put
  `.ensure_long_output()` on the unstarted `AgentExecution`, after the prompt
  and output contract and before any result reader. It defaults off and applies
  equally to `get_data`, `get_text`, `get_data_object`, result facades, and
  generators; do not hide it in one getter or overload `.output(...)` with
  execution policy
  - the first ModelRequest keeps the original contract. Only normalized
    `length` / `incomplete` starts the TriggerFlow-visible continuation loop
  - current lossless carriers are plain text and resolved `json`; other
    structured formats fail before dispatch when the option is enabled
  - continuation is append-only, uses TaskWorkspace write/readback/digest
    evidence, and applies the original schema/Pydantic/ensure/custom validators
    to the replayed final candidate
  - carry each slot's value contract in the private continuation input and
    project it from the original Agently declaration so nested array/object
    shapes and nested Pydantic constraints survive. Validate every structured
    unit with the independent local slot model before commit. Enforce exact
    list bounds incrementally and hold later dependent slots behind an
    incomplete exact list. Keep a valid contiguous prefix when a later
    update fails, but regenerate the rejected update and its whole tail from
    the next `unit_index`
  - expose one exact host-issued mnemonic `path_key` per offered slot; do not
    provide a second model-copyable schema-path identifier. Authorize the whole
    offered key and reconstruct canonical paths from host state
  - retain a trusted explicitly empty list as an empty-container manifest fact;
    do not synthesize missing list paths as empty or accept an empty declaration
    after any item/prior declaration
  - retain trusted explicitly empty text as a text-presence fact. Before
    accepting continuation `is_final`, require declared ensure paths to have
    manifest facts and continue missing delivery without spending the caller's
    final-validation retry allowance
  - treat a closed structured string as one immutable atomic schema value:
    never re-offer or append it after commit. Represent a value beyond the
    4000-character unit bound as an ordered chunk list, or use plain text for
    one freeform artifact
  - close the small `base_revision` / `base_digest` / `anchor` control header
    before emitting business updates. Use the latest accepted-unit digest as
    the exact anchor; give plain-text continuations a bounded document start,
    exact accepted tail, and host-counted accepted character total as one
    read-only continuity context rather than making the model echo long
    business text in the header or estimate prior length. Commit exactly one plain-text
    update per logical continuation so every next join is generated from a
    refreshed accepted suffix; retain the first valid update and regenerate a
    response-supplied tail. A provider `length` terminal
    before header closure is bounded observable no progress: preserve the
    manifest, retry with header-first/one-update guidance, and terminate after
    the third consecutive no-progress continuation
  - JSON units with `completion_source="synthetic_repair"` are provisional and
    must be regenerated; retain only `observed_boundary` or raw-final
    `final_reconciliation` units
  - let the long-output delivery flow own continuation repair, with one
    physical request per continuation. Record a malformed provider-complete
    envelope as bounded `continuation_envelope_invalid` no progress; reserve
    caller `max_retries` for final assembled-value validation
  - after large instant JSON parsing defers, keep a successful provider-complete
    final parse authoritative. Observed-boundary events may update the
    provisional snapshot only when no valid final parse exists
  - if final replay fails a model-repairable schema, ensure, or declared
    validator rule, retain accepted units and use the bounded validation retry
    allowance to request only missing/additional units. Manifest, readback,
    digest, and lineage failures are integrity failures and must fail
    immediately rather than enter model repair
  - the private envelope must not enter the business stream, and continuation
    requests must not inherit Action/tool handlers
  - treat a zero-update `is_final` assertion after provider `length` as
    no-progress evidence, not completion proof
  - use bounded `long_output_no_progress` diagnostics to inspect reason,
    observed header fields, manifest revision, and accepted-unit count without
    recording raw provider bodies
  - this is direct ModelRequest delivery, not AgentTask. Do not combine it with
    an explicit AgentTask strategy; split task planning/tool work from the long
    terminal delivery execution
  - never claim semantic exhaustiveness without a declared expected
    count/key/reference or equivalent validator
- choose streaming mode separately from output format:
  - use `get_generator(type="instant")` or
    `get_async_generator(type="instant")` when UI/progress consumers need
    structured `StreamingData` field updates before completion
  - `instant` is supported for `json`, `flat_markdown`, `hybrid`,
    `xml_field`, `yaml_literal`, and `auto` after auto resolves to one of its
    structured formats
  - plain text / `text` has no structured instant paths; use `type="delta"` for
    text-increment streaming or `get_text()` after completion
  - treat instant events as provisional UI state; use final `get_data()` /
    `async_get_data()` for durable writes, validation, and business decisions
  - do not treat `instant` `.is_complete` as a global display-order barrier.
    When several paths share one CLI output area, buffer later-path deltas until
    the earlier path completion event has been handled; Web UI, SSE, and
    WebSocket consumers should normally render paths into separate slots
  - when early fields start independent work, order compact trigger records
    before long explanations or artifacts. Start only from complete canonical
    fields/items, keep consuming while bounded work runs, and reconcile against
    final validated data
  - incremental JSON parsing may emit
    `$status.status == "streaming_parse_deferred"` after a large incomplete
    buffer crosses its safety threshold. Treat this as loss of progressive
    optimization, not final correctness; keep control fields compact and early
  - hybrid typed JSON blocks stream as block text and become typed values at
    finalization. Use JSON when nested path-level early triggers are required
  - for typed handlers, import `StreamingData`, `AgentlySpecificResultMessage`,
    and `AgentlyModelResultMessage` from `agently`; use `agently.types.data`
    for the full typed data namespace
- for large structured generation, an early bounded `generation_plan`,
  `evidence_assessment`, or `risk_checks` field is appropriate only when a
  later field, workflow node, or user-process view consumes it. Declare its
  bounds, visibility, retention, and failure behavior. Do not use a generic
  `reasoning`, `analysis`, or `thinking` field or request hidden chain-of-thought
- account for observed model reliability when recommending formats:
  - `auto` can degrade to JSON and retry when markdown-style parsing fails, but
    do not depend on retry latency for hot paths. Recent qwen2.5:7b checks
    found that hybrid-style responses can omit required section headers or echo
    old scaffold comments into text fields, so keep the framework default at
    `json` unless the target model has passed representative tests
  - `flat_markdown` is explicit-only compatibility mode; do not recommend it as
    an auto/default path
  - `hybrid` is an explicit path, and an auto path when auto is enabled, for
    mixed prose/code plus typed fields. It can
    handle complex nested arrays when the prompt includes the
    nested sub-schema. Do not blanket-ban complex structures; instead test the
    target provider/model with representative schemas such as EDA netlists,
    citations, tables, and judge result arrays
  - reasoning output belongs to response events, not format parsers. Provider
    native reasoning and a leading outer `<think>...</think>` before the answer
    payload should appear as `reasoning_delta` / `reasoning_done`; payload or
    code-internal `<think>` content remains ordinary answer text
  - use explicit `format="json"` when retry latency is unacceptable, raw JSON is
    required, a target model is known to ignore markdown section headers, or the
    schema contains no prose/code string fields and many nested arrays
- for Agently `4.1.0.1+`, prefer tuple `ensure` in `.output(...)` for fixed
  required leaves. Third-slot `True` and runtime `ensure_keys` check path/key
  presence only, so `None`, blank strings, `False`, `0`, empty lists, and other
  intentionally empty values remain valid when the path exists. Use third-slot
  `"not_null"` only when a required path must also contain a meaningful value;
  it rejects `None`, blank strings, empty lists or wildcard matches, and lists
  containing missing required values while still accepting `False` and `0`.
  Both policies are rendered into the initial model-facing field requirements,
  so generation guidance and result-side ensure checks use the same semantics
- use manual `ensure_keys` only when the required path is runtime-dependent, conditional, or awkward to express in the static schema
- `max_retries=3` means Agently may make up to three additional model attempts
  after the initial call when parsing, Pydantic model validation, required-key
  extraction, strict output validation, or custom validators fail. Pydantic
  failures add bounded field-level correction feedback to the next attempt and
  are never accepted as raw invalid dicts, including when
  `raise_ensure_failure=False`. A retryable custom validator failure adds its
  bounded `reason` to the same complete-replacement correction prompt; its
  optional `payload` and handler exception details remain host/runtime-only.
  Retries commonly recover ordinary omissions, JSON/markdown parse mistakes,
  and auto-format degradation. They can still fail after all attempts when the
  model repeatedly echoes placeholder scaffolding, fills boolean/numeric fields
  with prose, produces malformed
  nested arrays, is truncated by long context, or must satisfy many wildcard
  paths such as `rule_results[*].evidence`
- prefer `.validate(...)` or `validate_handler=` when the field exists but the value still needs business validation
- keep output schema explicit when downstream systems, workflow branches, or later model steps consume the result
- use output schemas for scenario routing, intent detection, and business
  classification. The model should return structured fields such as category,
  confidence label, evidence, rule checks, and dispatch hints; deterministic
  code should consume those fields for the actual route. Do not make
  tokenization, word segmentation, keyword hits, substring rules, or regex the
  route owner.
- choose model size by decision complexity: smaller models, including local
  models when available, are reasonable for short label sets and straightforward
  rules; use a larger model when labels are numerous, conditions interact,
  ambiguity is common, risk is high, or the schema has nested/complex fields.
- order dependent fields before the final decision or user-facing answer field:
  put evidence, assumptions, clarifications, source notes, calculation plans,
  brief rationale, rule checks, and intermediate structured facts first, then
  put the final boolean, verdict, `reply`, summary, or action decision last.
  Agently output schemas are ordered; the model should generate supporting
  fields before conclusions even if the UI later reorders the final document for
  human reading. Do not ask for verbose hidden reasoning when a concise
  rationale, evidence list, or check list is enough.
- use conceptual grade labels for model-owned evaluation fields instead of
  precise numeric scores. Define each label in the prompt, for example:
  `high_trust` means authoritative sources, sufficient evidence, direct
  evidence-to-claim linkage, and broad domain support; `moderate_trust` means
  broad sources and direct or indirect support with some cross-domain inference;
  `low_trust` means missing sources, promotional-only sources, or weak
  evidence-to-claim linkage. When later code needs a number, map labels to
  deterministic values after generation.
- when a task needs complex arithmetic, long-number calculation, weighting,
  aggregation, or statistical transformations, make the model output an
  executable calculation plan or code, run it through tools, and pass the code
  plus raw result into a later model step. Do not make the model's text
  generation be the calculator.
- for tests that validate model-owned semantic content, prefer a second Agently
  model-judge request with output control: pass the candidate output, explicit
  rules, expected contract, and relevant context; ask for per-rule evidence,
  concise reason, and final boolean fields; assert the booleans. Use
  deterministic keyword/substring/regex checks only as smoke gates for
  structure, routing, or required-field presence, not as the primary content
  correctness signal.

## Anti-Patterns

- do not handwrite JSON post-processors when `.output(...)` already owns the contract
- do not rebuild a stable shared schema in Python if prompt config can own it once
- do not build custom retry loops for missing keys before using tuple `ensure` or, when necessary, runtime `ensure_keys`
- do not overload tuple `True` or runtime `ensure_keys` with value checks that belong in explicit `"not_null"` or `.validate(...)`
- do not use an underspecified first attempt plus hard-validator retries as a
  rule-discovery loop
- do not default to sync-only result handling when the caller is already async-capable
- do not rely on keyword, substring, regex, or text snapshot checks as the main
  assertion for whether model-generated content satisfies business rules
- do not treat offered-set membership as proof that a delayed, replayed, or
  retried selection belongs to the current Host request; correlate it before
  canonical lookup

## Read Next

- `references/overview.md`
