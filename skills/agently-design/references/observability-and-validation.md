# Observability and Validation

Design observation for every node and edge before implementation. Correlate
execution, task, logical request, provider attempt, Action, state transition,
and artifact lineage. RuntimeEvents and `model_request_telemetry` are
observation facts only: they do not own routing, retry, verifier judgment,
semantic root cause, or completion. Verify causes with direct evidence and a
controlled A/B comparison when possible.

## Observation Contract

For each important node or edge, record bounded facts such as:

- execution/task/logical-request/attempt/action ids and parent lineage;
- stage, owner, status, sequence, and timestamp;
- prompt and output-schema fingerprints, not unrestricted sensitive bodies;
- bounded input/output previews, full sizes, truncation, and ref paths;
- provider/model, attempt number, duration, usage, error, and retry relation;
- produced field path, maturity, authorized consumer, and invalidation;
- state transition, artifact/checkpoint refs, Action evidence, and terminal fact.

Use stable application-stage and logical-request ids so a provider retry does
not look like a new business decision.

## Observation Is Not Policy

Existing RuntimeEvents, lineage, Action observations, and
`model_request_telemetry` can reconstruct what happened. DevTools may record,
query, visualize, and compare those facts. Neither surface decides whether a
route is correct, whether to retry, whether evidence is sufficient, or whether
the task is complete.

Do not add runtime event fields solely to satisfy this design Skill. First use
the existing observable contract. Report an instrumentation gap when a required
fact truly cannot be observed.

## Reconstruct Actual Topology

Normalize raw observations into:

1. execution and task boundaries;
2. logical ModelRequest nodes;
3. provider attempts grouped under each logical request;
4. Action and external-system calls;
5. output-field consumer edges and state transitions;
6. retry, repair, replan, fan-out, join, and terminal events;
7. produced artifacts and readback evidence.

Compare this graph with the planned owner matrix, node contracts, and
schema-to-consumer map. Find the first divergence, then explain later symptoms
as consequences only when lineage evidence supports that chain.

## Semantic and Deterministic Validation

Use deterministic checks for owned structure: schema shape, types, enums,
required paths, ids from offered sets, file existence, API status, accounting,
lineage presence, and safety diagnostics.

Use an Agently ModelRequest with structured output for semantic quality, intent,
relevance, groundedness, usefulness, or model-owned correctness. Ask for
evidence, rule judgments, and conceptual levels rather than unsupported precise
scores. Concrete model-judge patterns remain in
`skills/agently/references/model-quality-validation.md`.

Do not use keyword lists, substring checks, regex language rules, hidden target
answers, or deterministic local substitutes as semantic proof.

## Acceptance Criticality Is Separate From Evaluation Method

Classify every acceptance item twice: first by **acceptance criticality**
(`hard gate` or `soft target`), then by **evaluation method** (`deterministic
check` or `semantic review`). Do not infer one axis from the other.

- Use hard gates for declared invariants whose failure must block the result.
  Exact schema/type/enum, authorization, identity, arithmetic, side-effect, and
  safety invariants are normally deterministic. A mandatory semantic business
  requirement may also be a hard gate, but its evidence must come from a
  structured model judge or human review rather than keyword matching.
- Use soft targets for preferred quality, aesthetics, clarity, completeness,
  tone, or nice-to-have behavior where bounded imperfection or degradation is
  acceptable. Record a level, evidence, and advice. Do not reject solely
  because a soft target is imperfect; if a minimum level blocks acceptance,
  declare that floor as a hard gate before the run.

For semantic acceptance, define representative cases, conceptual rubric
levels, a developer-approved minimum, and escalation policy. Compare repeated
real runs rather than requiring exact text reproduction. Calibrate model judges
and coding-agent human-like reviews against a human-labeled calibration sample,
especially before high-risk use. When accurate, sufficient input and a clear
request repeatedly fail the approved minimum, report a model capability or fit
gap; do not silently lower the standard, hide the failure behind retries, or
replace semantic judgment with hard-coded language proxies.

## Experiment and A/B Evidence

Fix the question, source boundaries, provider/model, environment, and comparison
criteria. Preserve raw bounded facts before summaries. Record command, branch,
commit, date, cases, selected routes, request/tool/external counts, input/output
sizes, timing, artifacts, readback, limitations, and baseline.

Before a change, state the decision being tested, supporting evidence, and
expected metric or behavior shift. After the change, rerun the same or a
deliberately versioned experiment and compare topology, first divergence,
quality, cost, and timing. A runner records facts; the agent inspects artifacts
and owns the judgment.

## Claim Labels

Label report statements:

- **Observed:** directly present in events, source, output, state, Action
  evidence, or artifact readback;
- **Inferred:** the best explanation consistent with observations, with
  uncertainty and alternatives stated;
- **Verified cause:** changed or isolated through source proof, A/B behavior, or
  another causal check.

Do not upgrade an inference because the final output looks plausible or bad.

## Privacy and Redaction

- do not collect hidden chain-of-thought;
- observe an explicit task-specific deliberation artifact only when its
  consumer, visibility, retention, and redaction policy are declared; do not
  turn provider-native reasoning telemetry into application evidence;
- prefer fingerprints, bounded previews, field names, sizes, and authorized refs;
- redact secrets, auth headers, personal data, private source fields, and unsafe
  attachment content;
- keep raw evidence in controlled cold storage with retention policy;
- make truncation and redaction visible so absence is not misread as fact.

## Validation Checklist

- Can every logical request and provider attempt be distinguished?
- Can every required output field be traced to its consumer and state change?
- Are retries, repairs, and provisional invalidations visible?
- Are Action claims backed by execution evidence?
- Are prompt/schema changes fingerprinted and comparable?
- Is the actual topology reconstructed from facts rather than final output?
- Are semantic judgments model-owned and structural checks deterministic?
- Are observed facts, inference, and verified cause separated?
- Does A/B evidence test the claimed owner and first divergence?
- Are sensitive content, truncation, and retention handled explicitly?

Use `agently-runtime` for concrete RuntimeEvent, telemetry, Workspace, Action,
and DevTools mechanisms. Use the owning request or TriggerFlow Skill for any
implementation change found by the audit.
