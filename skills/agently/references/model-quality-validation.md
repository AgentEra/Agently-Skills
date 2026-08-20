# Model Quality Validation

Use this reference when an Agently project needs to classify intent, choose a
business scenario, evaluate model output quality, grade a response, or test
semantic behavior.

## Rule

Agently projects are AI application projects. Semantic decisions should normally
be made through Agently model requests with explicit output schemas, not through
tokenization, word segmentation, keyword matching, substring checks, regex, or
text snapshots.

Use deterministic checks only for smoke-level facts:

- required keys exist
- returned lists are non-empty
- enum values are in an allowed set
- numeric values are inside a deterministic range
- files or API calls were created

For meaning, quality, relevance, intent, scenario match, grading, or business
classification, call a model and make the result structured.

## Two-Axis Acceptance Matrix

Do not treat every acceptance criterion as the same kind of gate. Classify it
on two independent axes before writing tests:

1. **Acceptance criticality**
   - **Hard gate:** failure makes the result unsafe, invalid, unauthorized, or
     unusable and must block acceptance.
   - **Soft target:** a preferred quality direction. Record its level and
     feedback, but tolerate declared imperfections or degradation unless a
     predeclared unacceptable floor is crossed.
2. **Evaluation method**
   - **Deterministic check:** exact structure, type, enum membership, required
     paths, offered-key membership, arithmetic, authorization, side-effect
     evidence, or another reliably computable invariant.
   - **Semantic review:** intent alignment, factual use of supplied evidence,
     reasoning quality, usefulness, clarity, tone, visual quality, or another
     open-ended judgment. Use a structured model judge, a coding-agent
     human-like review during preflight, or a real human review according to
     risk.

These axes are not aliases. A mandatory semantic requirement can be a hard
gate while still needing a calibrated model judge or human reviewer. A soft
target can have deterministic diagnostics. If a soft target's lower bound
blocks release, that lower bound is a hard gate and must be named as such.

| Criterion | Typical criticality | Evaluation method | Acceptance behavior |
|---|---|---|---|
| schema, types, required fields, enum membership | hard gate | deterministic check | fail closed or bounded repair |
| authorization, offered ids, exact calculations, committed side effects | hard gate | deterministic check | block on any violation |
| mandatory semantic faithfulness or business-direction correctness | hard gate | semantic review with explicit rubric | block below the declared minimum; escalate uncertain/high-risk cases |
| completeness, clarity, tone, layout aesthetics, nice-to-have strategy | soft target | semantic review | score and advise; do not block for ordinary imperfections |

Structured output makes the result shape and bounded values controllable; it
does not make open-ended model content byte-identical or exactly reproducible
on every run. Do not test semantic content with one expected string, keyword
hits, or a snapshot of one lucky response.

## Calibrate Quality Across Repeated Runs

- Define representative cases, rubric levels, hard minima, soft targets, and
  escalation rules before tuning. The developer owns the final business-risk
  tolerance.
- Run representative cases across repeated real runs for each relevant
  provider/model/configuration. Record individual results, judge evidence,
  pass-rate or level distribution, disagreements, and variance; do not demand
  identical prose.
- Calibrate a model judge or coding-agent review against a small
  human-labeled sample. Use human review directly for high-risk, ambiguous, or
  disputed cases. A coding-agent simulation is useful preflight evidence, not
  proof of target-model capability.
- Adjust rubric wording, sampling, escalation, and operational thresholds when
  repeated evidence shows the evaluator is poorly calibrated. The developer-
  approved minimum business standard must not be silently lowered merely to
  make a weaker model pass.
- If task input is accurate and sufficient, the request is clear, and repeated
  real runs still miss the minimum business direction, report a capability or model-fit gap.
  Discuss a different model, context/request design, scoped
  fallback, or human review with the developer instead of hiding the gap with
  unlimited retries or keyword gates.

Keep the test record model-specific and versioned. A threshold established for
one model or configuration is not automatically evidence for another.

## Simulation-First Experiment Gate

When problem discovery or strategy tuning is expected to require several model
rounds, separate cheap design iteration from real-model evidence:

1. Write the cases and acceptance criteria before tuning.
2. Ask the development agent in the current task to self-simulate realistic
   target requests, responses, decisions, and behavior traces without calling
   the target model API. Mark every artifact `simulated` and `warm_preflight`.
3. Iterate prompt wording, output schema, request topology, instrumentation, and
   failure handling until this warm preflight meets the written criteria.
4. Freeze the request contract and, if an isolated executor is available,
   choose at most one carrier for a cold preflight. Do not run all carriers.
5. If no carrier is available, record `cold_preflight=skipped` with the reason;
   do not block validation or relabel the warm preflight as cold.
6. Run the smallest representative, bounded target-model comparison that can
   confirm or reject the hypothesis.
7. Inspect the real traces and base the final experiment conclusion on them. If
   simulation and reality differ, the real trace wins and the design returns to
   analysis and revision.

### Choose One Cold-Preflight Carrier

Use the first feasible option that provides genuine context isolation:

1. a native coding-agent subagent started with fresh or no inherited context;
2. a handshake-verified ACP coding agent; or
3. a fresh isolated task or session of the development agent.

ACP is not mandatory, and a native subagent is not automatically better: the
required property is isolation from the warm-preflight answer and reasoning.
Direct generation by the agent in its existing context remains
`warm_preflight`, even if it is prompted to "act fresh."

Give the cold carrier only:

- task-relevant runtime input;
- authoritative API/schema/docs/docstrings as `info`;
- call, transformation, and behavior rules as `instruct`;
- the exact output type and field-level contract;
- written acceptance criteria that do not encode the intended answer.

Do not pass prior conclusions, expected answers, the full conversation,
customer secrets, unrelated metadata, or unrelated filesystem context. The
host must enforce authorized credentials/resources, tool and network policy,
file scope, timeout, and call limits. A prompt instruction alone is not an
isolation or cost-control boundary.

Label a cold result `simulated` and `cold_preflight`. ACP and coding-agent
subagents may plan, use tools, or issue several internal model requests. Unless
the carrier can prove exactly one underlying model request and expose its
accounting, label the result `agent_simulation`, not
`single_model_request_simulation`.

### Evidence And Telemetry Labels

Self-simulation and cold preflight can expose unclear instructions, missing
fields, impossible handoffs, unlogged branches, weak acceptance criteria, and
the expected shape of usage metadata. They cannot establish model capability,
semantic quality, provider behavior, latency, cost, robustness, or stability.

Use these labels without mixing categories:

| Label | Meaning |
|---|---|
| `simulated` | Generated for preflight; not an observed target-model fact |
| `synthetic` | Invented value used to exercise a field or branch |
| `estimated` | Calculated approximation with its method stated |
| `replayed` | Value copied from a named recorded trace, not a current run |
| `unavailable` | Required telemetry was not exposed; do not infer it |
| `observed` | Emitted by the target provider or host instrumentation in the current real run |

In particular, a simulator cannot accurately recreate provider-generated
request IDs, token accounting, cache or billing fields, latency, finish
behavior, or opaque metadata. A tokenizer estimate is still `estimated`; ACP or
subagent accounting describes that carrier, not the simulated target provider.
Never add simulated values to real experiment totals. If exact usage or
provider metadata matters to the conclusion, obtain it from the bounded real
comparison or report it `unavailable`.

Use authorized project- or developer-owned test credentials by default. Put
explicit limits on calls, concurrency, retries, time, and budget. Do not consume
customer API credentials or quota unless the customer explicitly authorizes
the experiment after seeing the maximum call count or spend.

## Development Script: Intent And Scenario Routing

Use this pattern when a script or service module must decide which model-app
scenario owns a request.

```python
from agently import Agently


ROUTES = [
    "support_ticket",
    "billing_question",
    "incident_report",
    "sales_lead",
    "needs_human_review",
]


def classify_user_message(message: str) -> dict:
    result = (
        Agently.create_request("scenario-router")
        .input({
            "message": message,
            "available_routes": ROUTES,
        })
        .instruct([
            "Classify the business intent from the full message.",
            "Do not choose a route by keyword hits or token counts.",
            "If the message is ambiguous or safety-sensitive, choose needs_human_review.",
            "Return concise evidence before the final route.",
        ])
        .output(
            {
                "evidence": [(str, "short evidence from the user message", True)],
                "ambiguities": [(str, "missing or ambiguous facts")],
                "route": (str, "one value from available_routes", True),
                "confidence": (str, "high | medium | low", True),
            },
            format="json",
        )
        .get_result()
    )
    data = result.get_data()

    if data["route"] not in ROUTES:
        raise ValueError(f"Unexpected route: {data['route']}")
    return data
```

The deterministic code only verifies that the model returned a known route. The
semantic route choice belongs to the model request.

## Development Script: Quality Gate Before Publishing

Use this pattern when a script generates content and must decide whether the
content is ready for a user-visible flow.

```python
from agently import Agently


QUALITY_LEVELS = {"excellent", "adequate", "weak", "failed"}


def review_release_note(candidate: str, source_facts: list[str]) -> dict:
    result = (
        Agently.create_request("release-note-quality-review")
        .input({
            "candidate": candidate,
            "source_facts": source_facts,
            "quality_levels": sorted(QUALITY_LEVELS),
        })
        .instruct([
            "Evaluate whether the candidate is faithful to the source facts.",
            "Do not score by keyword overlap.",
            "Use quality_level definitions:",
            "- excellent: all important facts are present and no unsupported claims appear.",
            "- adequate: core facts are present; minor wording or coverage gaps remain.",
            "- weak: important facts are missing or support is indirect.",
            "- failed: unsupported claims, wrong facts, or missing core facts.",
            "Return evidence and missing facts before the final quality_level.",
        ])
        .output(
            {
                "supported_claims": [(str, "candidate claim supported by source facts", True)],
                "missing_or_weak_facts": [(str, "important missing or weakly supported fact")],
                "unsupported_claims": [(str, "claim not supported by source facts")],
                "quality_level": (str, "excellent | adequate | weak | failed", True),
                "publish_ready": (bool, "true only for excellent or adequate with no unsupported claims", True),
            },
            format="json",
        )
        .get_result()
    )
    data = result.get_data()

    if data["quality_level"] not in QUALITY_LEVELS:
        raise ValueError(f"Unexpected quality_level: {data['quality_level']}")
    return data
```

Use conceptual levels first. If the workflow later needs metrics, map
`excellent`, `adequate`, `weak`, and `failed` to deterministic numbers in code
after the model result.

## Test Script: Model-Owned Output Judge

Use this pattern in pytest when testing whether model-generated text satisfies
business rules. The test can still check structure deterministically, but the
semantic pass/fail decision should come from a second Agently model request.

```python
from agently import Agently


def judge_support_reply(candidate: str, ticket_context: dict) -> dict:
    result = (
        Agently.create_request("support-reply-judge")
        .input({
            "candidate": candidate,
            "ticket_context": ticket_context,
            "rules": [
                "acknowledges the customer's billing concern",
                "does not promise a refund before checking policy",
                "asks for the missing invoice id when it is absent",
                "uses a calm and professional tone",
            ],
        })
        .instruct([
            "Judge semantic compliance with each rule.",
            "Do not use keyword overlap as the primary signal.",
            "For each rule, provide evidence and a concise reason before passed.",
            "Set overall_pass true only when every required rule passes.",
        ])
        .output(
            {
                "rule_results": [
                    {
                        "rule": (str, "rule being judged", True),
                        "evidence": (str, "specific evidence from candidate and context", True),
                        "reason": (str, "concise judgment reason", True),
                        "passed": (bool, "whether this rule passed", True),
                    }
                ],
                "overall_reason": (str, "brief reason for the overall verdict", True),
                "overall_pass": (bool, "true only if all required rules pass", True),
            },
            format="json",
        )
        .get_result()
    )
    return result.get_data()


def test_support_reply_quality(generated_reply):
    ticket_context = {
        "customer_message": "I was charged twice but cannot find the invoice id.",
        "account_status": "active",
        "refund_policy": "refunds require invoice lookup before approval",
    }

    judge = judge_support_reply(generated_reply, ticket_context)

    assert judge["overall_pass"], judge
    assert all(item["passed"] for item in judge["rule_results"]), judge
```

Do not replace this with assertions such as `"refund" in reply`,
`"invoice" in reply`, jieba segmentation matches, regex route rules, or
snapshots of one lucky model output. Those checks can miss wrong promises,
policy violations, missing nuance, or correct answers that use different words.

## When Deterministic Code Is Still Correct

Keep deterministic code for things the model should not own:

- exact enum validation after a model decision
- exact arithmetic, aggregation, and statistics
- schema shape and required-field presence
- file existence, API status codes, and database writes
- dispatching after the model returns a valid structured route

Use the model for meaning; use code for exact mechanics.
