# Observability and Validation

Design observation for every node and edge before implementation. Correlate
execution, task, logical request, provider attempt, Action, state transition,
and artifact lineage. RuntimeEvents and `model_request_telemetry` are
observation facts only: they do not own routing, retry, verifier judgment,
semantic root cause, or completion. Verify causes with direct evidence and a
controlled A/B comparison when possible.

## Ordered Diagnosis Before Model Tuning

Separate execution reachability, execution logic and model-output effectiveness.
They are ordered diagnostic gates, not interchangeable labels or a menu of
optimizations. A readable artifact does not prove correct orchestration; sound
orchestration does not prove adequate model judgment. Report a separate result
and evidence boundary for each layer. Do not jump from a poor final answer to
Prompt changes or a model-capability diagnosis.

First fix the task, source boundary, deliverables, allowed partial results and
acceptance criteria. This makes the diagnosis fair; it is not a Prompt-tuning
step. Distinguish fulfilling the original goal from documenting why it could
not be fulfilled. Use only obligations actually applicable to the producer.

Work through these gates in order:

| Gate | Question and required evidence | Action before advancing |
|---|---|---|
| 1. Execution reachability | Do required stages and tools actually run? Can artifacts be materialized, discovered, read, handed to the caller and retained after close? Inspect actual effects and identities, not success prose or paths alone. | Fix the integration, capability, permissions, storage or handoff gap; demonstrate the repaired path. Do not compensate with Prompt wording. |
| 2. Execution logic | Does the fixed design satisfy its contract? Inspect owners, dependencies, value/control edges, state transitions, error feedback, declared hard constraints, budgets, retries and recovery. Use source review plus relevant normal, boundary and failure tests. | Repair confirmed design/runtime defects at their owner and verify the invariant. Keep unresolved or untested boundaries explicit; do not declare this gate passed merely because one demo runs. |
| 3. Actual model input | With gates 1 and 2 supported for the scenario, does the responsible request receive sufficient, accurate evidence, original scope, permissions, rules and output requirements? Inspect the dispatched request after injection and truncation. | Correct missing, misleading, conflicting or irrelevant information. Separate facts available to the reviewer from facts available to that request. If the omission comes from a broken edge, return to gate 1 or 2. |
| 4. Bounded input/Prompt optimization | Given adequate mechanics and a justified input diagnosis, does one general change improve the declared business outcome? Freeze cases, rubric, settings and limits; run controlled representative comparisons and inspect artifacts. | Adopt only a demonstrated improvement that also passes complete-task verification and affected regressions. More reads, fewer tokens or a better intermediate response alone do not pass. Exclude ineffective changes; stop when bounded attempts yield no gain or no new testable hypothesis remains. |
| 5. Model capability comparison | After adequate input and attempted optimization still miss the declared minimum, does a more capable candidate resolve the failure under comparable conditions? | Propose an authorized, bounded comparison, then test the same task/input/Prompt/workflow/rubric as far as practical. Record provider/configuration differences, repeated outcomes and cost/latency. A candidate's reputation or one better response is not proof of capability or a unique root cause. |

Reuse prior evidence when code, contract, input, environment and relevant
configuration are unchanged and no new failure challenges it. Do not rerun
everything to satisfy the order mechanically. State the covered scenario and
uncovered boundaries. New evidence of an upstream defect reopens that gate;
lower-layer success never waives an upstream invariant. Several defects may
coexist, so preserve secondary findings while repairing the earliest blocking
one. A model-independent configuration or unsupported capability gap belongs
in the prerequisite diagnosis, not in speculative semantic tuning.

### Decompose the Failure Before Selecting a Fix

Reconstruct the real flow and break it into nodes and handoffs using the
existing review record. For each relevant node/edge identify its owner,
required input, constraints, produced value/state/effect, consumer, dependency
and actual evidence. Trace task input through model decisions, tools, returned
observations, artifact access, later decisions and terminal delivery. Check
the earliest point where the declared contract ceases to hold; explain later
symptoms as consequences only when that connection is supported.

Distinguish a broken producer, a broken transfer, a wrong consumer and a
model-owned decision that misses its contract despite adequate evidence.
For a disputed handoff, compare producer output, actual transferred content,
consumer input and consumer output. When needed, isolate that boundary using
the same recorded state or valid protocol inputs. Label replayed or scripted
Host probes honestly: they test mechanics and do not prove model competence.
Verify any proposed improvement again from a complete fresh task before adoption.

For example, a generated file deleted at termination is a reachability or
lifecycle defect. A fixed review stage that has neither current content nor a
way to obtain it has a logic/data-flow defect. If obtaining the content is a
model-owned choice and the read capability and responsibility are present,
failure to choose it is a model decision/input/Prompt hypothesis, not automatic
proof that the fixed runtime is broken. If the actual current content reaches
the responsible request and its judgment is still wrong, measure that semantic
failure rather than claiming the content was absent. Conversely, delegating a
Host-computable authorization, identity or declared effect requirement to prose
alone is a design defect; a stronger model cannot replace its hard check.

Record what the experiment changes: a read reminder tests whether the model
obtains evidence; providing actual readback tests what it does once evidence
is present. If the reminder is ignored, do not claim to have tested the latter.
Keep acquisition, transmission, judgment and artifact revision outcomes separate.

The distinction between actual outcomes and traces is supported by
[Anthropic's agent-evaluation discussion](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
and [Google's trajectory/response evaluation documentation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/evaluation-agents).
The ordered gates above are the working diagnostic procedure here; those
sources do not prove a particular workflow or optimization correct.

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
[`../../agently/references/model-quality-validation.md`](../../agently/references/model-quality-validation.md).

Do not use keyword lists, substring checks, regex language rules, hidden target
answers, or deterministic local substitutes as semantic proof.

## Acceptance Criticality Is Separate From Evaluation Method

First establish
[constraint and evaluation parity](../../agently/references/model-quality-validation.md#ground-each-review-criterion):
trace each blocking judgment to the producing node's actual contract and
available prerequisites. Expanding review scope requires matching changes to
that node's inputs and constraints; an audit cannot silently add obligations.

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

For the repair-versus-strategy decision, stopping repeated tuning, human Prompt
review and authorized model comparison, read
[Bounded Optimization and Model Escalation](../../agently/references/model-quality-validation.md#bounded-optimization-and-model-escalation).
This prevents soft imperfections from becoming an endless design blocker.

## Experiment and A/B Evidence

Before judging content or proposing a Prompt fix, read
[Ground Each Review Criterion](../../agently/references/model-quality-validation.md#ground-each-review-criterion).
Apply it to instruction compliance, task semantics, lossy summaries, and
open-ended quality; do not turn an undeclared preference into a failed gate.

Fix the question, source boundaries, provider/model, environment, and comparison
criteria. Preserve raw bounded facts before summaries. Record command, branch,
commit, date, cases, selected routes, request/tool/external counts, input/output
sizes, timing, artifacts, readback, limitations, and baseline.

Before a change, state the decision being tested, supporting evidence, and
expected metric or behavior shift. After the change, rerun the same or a
deliberately versioned experiment and compare topology, first divergence,
quality, cost, and timing. A runner records facts; the agent inspects artifacts
and owns the judgment.

## Evaluation Coverage and Operating Budgets

Choose representative normal, boundary, adversarial and failure cases according
to the actual risk. Relate task completion, correctness, user experience and
safety criteria to their declared hard gates or soft targets. Do not create
universal numeric targets or rely on uncalibrated model confidence scores.

Where operation is in scope, declare end-to-end cost, latency and capacity
budgets, then attribute them to model attempts, tools, queues, joins and retries.
Identify the signal, threshold and owner for alerts, rollback, fallback or human
handoff when required. Mark an unknown budget as unresolved; do not turn a design
estimate into observed telemetry. Reuse current lineage and metrics rather than
adding a parallel observation protocol.

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

Use `agently-runtime` for concrete RuntimeEvent, telemetry, TaskWorkspace,
RecordStore, Action,
and DevTools mechanisms. Use the owning request or TriggerFlow Skill for any
implementation change found by the audit.
