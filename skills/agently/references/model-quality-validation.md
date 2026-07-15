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

## Simulation-First Experiment Gate

When problem discovery or strategy tuning is expected to require several model
rounds, separate cheap design iteration from real-model evidence:

1. Write the cases and acceptance criteria before tuning.
2. Ask the development agent to self-simulate realistic target requests,
   responses, decisions, and behavior traces without calling an external model.
   Mark every generated artifact `simulated`.
3. Iterate prompt wording, output schema, request topology, instrumentation, and
   failure handling until the simulated preflight meets the written criteria.
4. Freeze the hypothesis and run the smallest representative, bounded
   real-model comparison that can confirm or reject it.
5. Inspect the real traces and base the final experiment conclusion on them. If
   simulation and reality differ, the real trace wins and the design returns to
   analysis and revision.

Self-simulation can expose unclear instructions, missing fields, impossible
handoffs, unlogged branches, and weak acceptance criteria. It cannot establish
model capability, semantic quality, provider behavior, latency, cost,
robustness, or stability; those claims require real-model evidence.

Use authorized project- or developer-owned test credentials by default. Put
explicit limits on calls, concurrency, retries, and budget. Do not consume
customer API credentials or quota unless the customer explicitly authorizes the
experiment after seeing the maximum call count or spend.

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
