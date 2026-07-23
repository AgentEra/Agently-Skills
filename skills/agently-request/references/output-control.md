# Agently Output Control

Use this skill when the question is what shape the model should return and how that shape should stay reliable.

The user does not need to say `.output(...)`, tuple `ensure`, `ensure_keys`, or `.validate(...)`. Requests for stable JSON-like fields, structured reports, or machine-readable sections should route here.

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
- when parsed output feeds an API, SDK, module interface, or function, mirror
  the consumed request/argument structure instead of returning an opaque dict.
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
  - for typed handlers, import `StreamingData`, `AgentlySpecificResultMessage`,
    and `AgentlyModelResultMessage` from `agently`; use `agently.types.data`
    for the full typed data namespace
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
  `raise_ensure_failure=False`. Retries commonly recover ordinary omissions,
  JSON/markdown parse mistakes, and auto-format degradation. They can still
  fail after all attempts when the model repeatedly echoes placeholder
  scaffolding, fills boolean/numeric fields with prose, produces malformed
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
- do not default to sync-only result handling when the caller is already async-capable
- do not rely on keyword, substring, regex, or text snapshot checks as the main
  assertion for whether model-generated content satisfies business rules

## Read Next

- `references/overview.md`
