# Agently Prompt Management

Use this skill when the core problem is how prompt state should be structured before one request or request family runs.

## Native-First Rules

- prefer `input(...)`, `instruct(...)`, `info(...)`, and `output(...)` over concatenated prompt strings
- for a one-off Agently fluent request, keep `.input(...)`, `.info(...)`,
  `.instruct(...)`, `.output(...)`, and the terminal `.get_result()`,
  `.get_data()`, `.async_get_data()`, or equivalent call visible in one chain.
  A single Prompt Configure YAML/JSON file loaded with explicit `mappings` is
  the equivalent declarative form
- split that request chain only when a piece is reused unchanged, independently
  owned/versioned or product-edited, or genuinely generated/conditional. Do not
  move a one-use schema or prompt step elsewhere merely to shorten the chain
- when model output must satisfy a documented API request, SDK/module
  interface, or function signature, compose the prompt as one integration
  contract: runtime facts in `input`, authoritative API/schema documentation,
  signatures, and docstrings in `info`, transformation and call rules in
  `instruct`, and the exact downstream-consumable shape in `output`. This
  contract information is necessary boundary control, not business-logic
  intrusion; do not assume ordinary requests can see Python docstrings or
  external schemas unless they are supplied
- move reusable prompt structure into prompt config or YAML instead of ad hoc literals
- keep runtime variables as `${...}` placeholders in prompt files and inject them through mappings at load time
- use render-time slot references when one prompt slot should point the model to
  another slot without duplicating its value: `${INPUT.foo}` -> `[INPUT > foo]`,
  `${INFO.customer}` -> `[INFO > customer]`, `${INSTRUCT.step}` ->
  `[INSTRUCT > step]`, and `${OUTPUT}` -> `[OUTPUT REQUIREMENT]`. Slot names are
  case-insensitive; examples should use uppercase. Do not validate the path
  after the slot name because it is a model-facing reference label, not a value
  extraction
- keep task-specific request contracts in prompt config, and keep only widely reused persona setup in small code-side factories
- when the output contract is stable and shared across a request family, keep it
  in prompt config such as `.execution.output` instead of rebuilding it ad hoc
  in Python. Removed turn/request prompt config keys should be migrated to
  `.execution`
- use `agent.define(...)` for reusable Agent definition state such as model
  defaults, stable persona, fixed prompt, mounted Actions or Skills,
  TaskWorkspace/RecordStore bindings, and policy defaults. TaskContext and
  ContextReader remain execution/task scoped. Ordinary quick prompt calls are execution-local
  drafts, not shared Agent definition writes
- Agent quick prompt chains create AgentExecution-local ModelRequest drafts. Expression-local
  chaining can configure and run one execution directly, for example
  `agent.input(...).output(...).async_start()`. If setup is split across
  statements, conditions, helper calls, or later configuration steps, capture
  `execution = agent.create_execution()` and mutate that execution with
  `execution.set_execution_prompt(...)` or quick prompt methods; do not rely on
  shared Agent pending prompt accumulation. Agent-level persistent setup remains
  on `agent.define(...)`, `always=True`, `set_agent_prompt(...)`, settings, and
  stable prompt config.
- set structured output format in prompt config with `$format` inside the
  `output` block when the contract needs a fixed mode, for example
  `.execution.output.$format: json`, `flat_markdown`, `hybrid`, `xml_field`,
  `yaml_literal`, or `auto`. This maps to the same Prompt slot as
  `.output(..., format=...)`; `.format`, `$output_format`, and
  `.output_format` are accepted aliases
- keep prompt composition separate from transport and orchestration
- use config files as an editable bridge when UI or product teams need to adjust prompt-driven behavior without rewriting workflow code

## Collaborative Prompt Design and Review

For collaborative design or review of a complex business workflow or one scoped
block, first explain the overall scenario and ask the user to confirm the
logical ModelRequest inventory and each request's responsibility. Use a concise
view of the existing node/edge plan: role, relevant input, output consumer, and
important dependencies. Separate Host work from model work, and distinguish a
request family repeated across items from provider retry attempts.

After that inventory is confirmed:

1. Select detailed reviews according to the user's needs or explain why a
   request needs confirmation, such as an unresolved business choice, important
   policy boundary, or consequential downstream contract change. Do not require
   detailed approval of every routine request.
2. By default, present one selected request's design at a time and wait for
   confirmation or revision. Do not advance to the next selected design or
   treat this one as approved without the user's response. Follow an explicit
   request for batch review or delegated decisions instead when given.
3. Apply revisions to the actual request/config, show the changed topics, and
   check affected producer/consumer contracts and workflow responsibilities.
   Reconfirm changed scope or handoffs; keep unchanged confirmations rather
   than restarting the entire review.

Inventory confirmation is not approval of every selected Prompt. Make the
current subject and pending/confirmed/revising state legible in ordinary review
notes, without creating a new protocol or mandatory tracking schema. Reuse a
previously confirmed, unchanged inventory.

## Show a Business Prompt for Review

When a user needs to confirm business intent or a consequential prompt choice,
offer a readable review view: explain the scenario, what this ModelRequest owns
and does not own, and who consumes its result. Then show concrete prompt content
using Agently's `input`, `info`, `instruct`, and `output` slots, with
field-level type, meaning, requiredness, enum/range/format/nullability where
relevant. Prefer a table-first presentation: a request overview, then a main
`Slot | Topic | Actual prompt content` table for the current request, a visible
examples table when used, and an output-field constraint table. Keep cells
short enough to scan; expand long topics into named sections rather than one
giant cell. Show real proposed wording, not merely “put rules here.”

Adapt or omit tables for the decision. The layout is not a mandatory business
template or new runtime schema; selected collaborative reviews still follow
the confirmation sequence above. Use redacted representative inputs.
Keep the view aligned with the real request chain/config and the rendered-prompt
audit below; a design table alone does not prove what was dispatched.

### Long Slots and Visible Examples

Organize a long slot by paragraphs, topics, or sections in both the source
Prompt and its review view. Keep related content together; this does not justify
extra files, wrappers, or ModelRequests. For each block, check current-request
relevance, the authority of facts/rules, redundancy or contradiction, and
whether a single instance has become a non-generalizable rule.

Show every model-visible example's content, the existing rule it illustrates,
its actual slot/config location, and whether it is synthetic or a redacted
source example. Keep examples non-normative and within the example-volume guard
below. Clearly separate reviewer-only illustrations or notes that are not sent
to the model; do not inject review labels/approval history into the Prompt by
default. “Examples” is a presentation section, not a new Agently slot or API.
Do not manufacture examples when none are needed.

Collapsed sections may aid navigation, but make full permitted content
accessible and mark omissions/redactions; do not imply a truncated view was a
complete audit.

For a concrete optional presentation, read the
[table-first collaboration example](prompt-collaboration-example.md). Its
business facts, request inventory, and output fields are illustrative, not a
required application template.

## Reusable Agent Request Isolation

When a reusable configured Agent must create a strict hot-only request, use a
native isolated request boundary:

```python
request = agent.create_temp_request()

# Equivalent when the caller needs create_request(...) options:
request = agent.create_request(
    inherit_agent_prompt=False,
    inherit_extension_handlers=False,
)
```

These calls disable inheritance of the Agent prompt and Agent extension
handlers; they still use the Agent's request infrastructure and settings. If
inheritance is intentional, declare the approved inherited slots and handlers,
then test that explicit contract rather than claiming the request is hot-only.

Audit the final post-prefix ModelRequest prompt through the installed runtime
after inheritance and extension injection have had their opportunity to run.
The audit must cover every mechanism allowed by the request contract and redact
secrets before retaining evidence. A fake fluent-call test that only records
`.input(...)`, `.instruct(...)`, or `.output(...)` calls cannot prove
projection isolation when it does not implement real Agent inheritance,
extension handling, or prompt prefixes.

## Request-Local Context

Each model-visible prompt item must serve at least one current-request role:

1. Interpret a supplied input.
2. Provide an authoritative fact, policy, schema, or evidence item.
3. Change the model-owned decision or transformation.
4. Define an output, consumer, tool, or capability boundary.
5. Provide useful user-visible process context, state, or explanation with a declared user or UI consumer.

Use the prompt slots deliberately: `agent` supplies stable role/capabilities;
`input` supplies current facts; `info` supplies authoritative contract and
evidence; `instruct` supplies task rules; and `output` supplies the required
result shape. Together they must give the model a self-contained account of
the current request, rather than assuming unexplained external project context.

Apply the removal counterfactual to every candidate item: If removing a candidate item would not change the current request's effective task, contract, evidence, decision, allowed verdict, or declared user/UI projection, remove or rewrite it. Project-level origin is not a removal test: retain a shared policy or fact when it changes this request. Retain or behaviorally rewrite an effective upstream caller guarantee when it changes the model-owned decision or the allowed verdict set. A proper name may remain only when it identifies a real domain contract, allowlist, evidence item, input fact, or capability boundary that changes the current request. Otherwise, rewrite an unexplained implementation name as its request-relevant role, or remove it. The fifth role does not justify generic project narration: name the user or UI consumer and the useful process context, state, or explanation it receives.

Compact example:

| | `info` |
|---|---|
| Bad | “Follow the project’s worker-manager convention.” |
| Good | “Allowed actions: approve or reject. Evidence: the attached request and its policy record.” |

Audit at two levels: first review each slot against its role and the removal
counterfactual; then inspect the actual rendered request, including mappings
and references. Before dispatch, `execution.get_prompt_text()` audits the rendered execution draft, not the final ModelRequest prompt. When TaskContext, Session, Skills, retrieval, Actions, or other runtime extensions can inject later, a bounded test must observe the final ModelRequest `prompt_text` emitted or built after injection. Do not treat the post-start execution snapshot as sufficient evidence for late injections. Redact secrets before retaining prompt evidence.

## General Rules, Special Cases, and Examples

Do not promote literals or behavior from a single observed instance into a
normative instruction. Entity literals, one-time input or environment state, a
historical incident, test fixture, or expected answer become prompt special
cases when their behavior cannot be derived from a general invariant or the
current request contract.

Do not misclassify required context as a special case. A current authoritative
business rule, domain invariant, authorization rule, interface contract, or
runtime fact that changes this request still belongs in `info`, `instruct`,
`input`, or `output` according to its owner. State the general condition and
required behavior without embedding incident-specific literals when those
literals are not themselves authoritative input.

When one observed failure exposes a prompt gap:

1. identify the violated general invariant or missing decision boundary;
2. write the smallest general conditional rule that covers that class of cases;
3. test the original case plus contrasting valid, invalid, and boundary cases;
4. remove instance-specific entity, state, incident, fixture, and
   expected-answer literals unless the current request supplies them as real
   facts.

An illustrative example may clarify an already stated rule; it cannot introduce
behavior, priority, an exception, or an expected answer that is absent from the
normative instruction. Mark examples clearly, keep them generic or synthetic
when possible, and include contrasting examples when one-sided demonstrations
would imply a false default.

As a repository authoring guard, the total illustrative example material in the
final rendered model-visible prompt must remain smaller than the non-example
normative prompt text. Measure both sides consistently by rendered characters
or model tokens. This is a prompt-review policy, not a claim that attention has
a universal 50 percent threshold.

If a task appears to require a few-shot demonstration set large enough to break
that guard, do not smuggle it in as “examples.” Treat demonstration selection
as a separate evaluated design: keep the normative contract dominant, bound the
selected demonstrations, and test selection and order, label/answer balance,
zero-shot versus few-shot behavior, and model-specific regressions.

## Anti-Patterns

- do not flatten business context into one opaque string unless the task is trivial
- do not trade a readable Agently request chain for distant one-use schemas,
  prompt constants, tiny getters, or pass-through request builders
- do not rebuild prompt templates through ad hoc `.format(...)` or string concatenation when prompt mappings already fit
- do not duplicate a large slot into another slot just to refer to it; use
  `${INPUT...}` / `${INFO...}` / `${INSTRUCT...}` references so the rendered
  prompt points at the existing section
- do not scatter stable prompt or output contracts across multiple Python helpers when one prompt config can own them
- do not invent a parallel prompt DSL for workflows or task nodes; use a
  `prompt` field with Configure Prompt shape when an internal model request
  needs configurable `input`, `instruct`, `output`, or `output_format`
- do not use prompt config files as a substitute for workflow state
- do not retain a name merely because it came from project setup, or rewrite a
  domain contract, allowlist, evidence item, input fact, or capability boundary
  that changes the current request.
- do not remove an effective upstream guarantee that changes the decision or
  allowed verdicts, and do not retain generic project narration under the
  user-visible-process role without a declared user or UI consumer.
- do not turn entity literals, one-time input or environment state, a
  historical incident, test fixture, or expected answer from one observed
  instance into normative case-specific behavior; generalize the invariant and
  use bounded illustrative examples only after the rule exists.

## Read Next

- `references/overview.md`
