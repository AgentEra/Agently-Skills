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

## Read Next

- `references/overview.md`
