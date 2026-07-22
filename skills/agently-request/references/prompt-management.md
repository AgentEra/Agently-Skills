# Agently Prompt Management

Use this skill when the core problem is how prompt state should be structured before one request or request family runs.

## Native-First Rules

- prefer `input(...)`, `instruct(...)`, `info(...)`, and `output(...)` over concatenated prompt strings
- keep information with the same change reason and consumer together. For a
  one-off request, prefer one expression-local execution block that shows
  `input`, `info`, `instruct`, `output`, and result consumption together. A
  single Prompt Configure YAML/JSON file loaded with explicit `mappings` is the
  equivalent declarative form
- optimize for review-time lookup count and depth for both people and coding
  agents. Do not extract a one-use schema, prompt fragment, or forwarding helper
  merely to make the file tree or call expression look formally layered
- extraction is justified when the extracted contract has an independent owner
  or version/review lifecycle, is reused unchanged by multiple consumers, must
  be product-editable outside Python, or is genuinely generated/conditional.
  Keep the extracted owner directly discoverable from the request call site
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

## Anti-Patterns

- do not flatten business context into one opaque string unless the task is trivial
- do not trade a readable request block for distant one-use constants, tiny
  getters, pass-through request builders, or wrapper layers that only satisfy a
  preferred visual format
- do not rebuild prompt templates through ad hoc `.format(...)` or string concatenation when prompt mappings already fit
- do not duplicate a large slot into another slot just to refer to it; use
  `${INPUT...}` / `${INFO...}` / `${INSTRUCT...}` references so the rendered
  prompt points at the existing section
- do not scatter stable prompt or output contracts across multiple Python helpers when one prompt config can own them
- do not invent a parallel prompt DSL for workflows or task nodes; use a
  `prompt` field with Configure Prompt shape when an internal model request
  needs configurable `input`, `instruct`, `output`, or `output_format`
- do not use prompt config files as a substitute for workflow state

## Read Next

- `references/overview.md`
