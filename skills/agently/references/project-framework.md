# Project Framework

Use this reference when the task is not just one Agently API call, but the initial shape or refactor boundary of a real project.

## Default Split

The default Agently project should usually separate these layers:

- `SETTINGS.yaml` or another settings file for provider config, `${ENV.xxx}` placeholders, workflow knobs, search and browse options, output directories, and deployment-time switches
- `app/` or integration code for loading settings, validating required env values when needed, choosing async entrypoints, and wiring the flow or service
- `prompts/` for YAML or JSON prompt contracts
- `services/` for request wrappers, business-facing adapters, and response normalization
- `domain/` or `schemas/` for enums, input/output contracts, and shared value objects
- `dynamic_task/` or service modules for Dynamic Task facades, submitted DAG contracts, resolver handlers, and planner constraints when plans are data
- `workflow/` for TriggerFlow graphs and chunk modules
- `tools/` for replaceable adapters such as search, browse, MCP, or external services
- `tests/` for settings smoke checks, prompt or response checks, and API or flow validation
- `outputs/` and `logs/` for runtime artifacts

Treat this as a menu of owner boundaries, not a required directory checklist.

## Information Locality

Minimize the cross-file lookup count and nesting depth required by people and
coding agents to understand the current behavior. Do not split one-use schemas,
constants, helpers, factories, classes, or wrappers into separate locations
unless the new boundary has actual reuse value or an independently
owned/versioned contract. Formal separation without either benefit is over-design.

## Framework Internal Module Rules

When the project-shape refactor is inside Agently itself, `agently/core/` and
`agently/builtins/` both support feature ownership through subdirectory
packages. Choose the layout by architectural roles before writing code:

- facade or manager surface;
- default implementation or provider/backend;
- registry, discovery, adapter, resolver, policy, or validation logic;
- data contracts or plugin protocols.

Use a subdirectory package when multiple roles are present or the feature is
expected to grow. Keep public imports stable through package `__init__.py`
files and top-level re-exports. Use a single file only for genuinely small,
single-responsibility capabilities where splitting would be over-design.

Landed examples include `core/Action`, `core/TriggerFlow`,
`core/TaskDAGExecutor`, `core/Workspace`,
`builtins/plugins/ExecutionResourceProvider`, and
`builtins/plugins/SkillsManager`.

## Model Output Test Rules

- For model-owned semantic content, use an Agently model judge with output
  control instead of keyword matching. Feed the candidate model output,
  explicit business rules, expected output contract, and relevant execution
  context into the judge.
- The judge output schema should put evidence, missing/weak points, and concise
  reasons before each final boolean judgment, and put the overall pass/fail
  boolean last.
- Tests should assert the judge's structured boolean fields. Keyword,
  substring, regex, and text snapshot checks may stay as deterministic smoke
  gates for structure, routing, or required-field presence, but should not be
  the primary content correctness signal.

## Routing and Classification Rules

- Scenario routing, intent detection, and business classification are
  model-owned semantic decisions. Do not use tokenization, word segmentation,
  keyword hits, substring rules, or regex as the route owner.
- Use an appropriately sized model plus an Agently output schema for the
  decision contract. Simple scenarios with a few labels and straightforward
  rules may use a smaller model, including a local model when available.
- Prefer a larger model when the scenario has many labels, dense or interacting
  rules, ambiguous inputs, high-stakes handling, or a complex returned data
  structure. Let deterministic code consume the structured result and perform
  the actual dispatch.

## Framework Gap Reporting

- When real application development exposes missing framework capability,
  behavior that does not match the documented or intuitive business contract,
  an unexposed or unfriendly API, or Skills/docs/examples that disagree with
  actual behavior, treat it as framework feedback rather than only a local
  implementation problem.
- If architectural review shows that business code is adding patches,
  workarounds, glue, private wrappers, or duplicated mechanisms only because
  Agently does not own the responsibility it should own, write a normalized
  issue report and recommend filing it at
  `https://github.com/AgentEra/Agently/issues`.
- The issue report should make the encountered scenario concrete: explain what
  kind of model-application development problem was being solved, where in the
  workflow the framework gap appeared, and why that responsibility should belong
  to Agently. If the business context is confidential, omit or anonymize
  sensitive details, but still describe the application category, workflow
  shape, decision point, expected framework responsibility, actual behavior or
  missing surface, why the local workaround is not the right long-term owner,
  minimal reproduction or affected docs/examples, and any compatibility or
  migration concern.
- For manual filing, provide the normalized issue content plus the filing
  method only; do not imply that the agent has submitted it.
- Before manual or automatic filing, sanitize the issue body. Remove local
  absolute paths, usernames, account names, access tokens, private repository or
  workspace names, internal project names, raw logs containing private prompts,
  and any customer or project-private data. Use placeholders such as
  `<workspace>`, `<repo>`, `<task-file>`, and `outputs/debug/<turn-id>.jsonl`
  while keeping enough technical context for maintainers to reproduce the
  framework behavior.
- Automatic filing requires explicit user confirmation. Before submitting,
  check that the local environment has GitHub submission capability and
  permission for `AgentEra/Agently`, verify the problem still reproduces
  locally, and carefully re-read the relevant Agently API, docs, examples, and
  Skills guidance to confirm the gap is not caused by overlooked information or
  incorrect usage. Run a privacy scan on the final issue body before creating
  the remote issue.

## Prompt Rules

- keep a one-off `input`, `info`, `instruct`, and `output` contract together in
  one readable request block. Move it into one Prompt Configure file with
  explicit mappings when the contract is reused, independently owned/versioned,
  product-editable, or genuinely dynamic
- keep runtime variables as `${topic}`, `${language}`, `${column_title}`, and similar placeholders in YAML or JSON, then inject them through prompt mappings at load time
- use small code-side agent factories only for shared persona or editor roles that are reused across many prompts
- do not turn prompt files into workflow state stores

## Model Settings Rules

- keep provider settings outside prompt files and workflow code
- prefer `${ENV.xxx}` placeholders in settings files instead of committing secrets or environment-specific endpoints into Python
- when settings live in a file, prefer `Agently.load_settings("yaml_file", path, auto_load_env=True)` so the same config stays deployable outside Python
- when settings are created inline as a Python mapping, use `Agently.set_settings(...)`
- when inline settings need self-explaining fields, use typed helpers from
  `agently.types.settings`, but keep YAML/TOML/JSON config as dict data and
  ensure every typed helper remains accepted anywhere the matching dict is
  accepted
- put provider-specific keys where the owning plugin actually reads them. For `OpenAICompatible`, prefer `plugins.ModelRequester.OpenAICompatible.*` instead of a root-level namespace
- for scenario-level model switching, prefer
  `model_pool -> model_profiles -> api_key_pools` over embedding provider
  names and keys in business workflow code
- if the application must fail fast on missing env values, load `.env` in the integration layer first, validate required names, and then still hand the raw placeholder-based settings to Agently
- after loading settings, validate the effective keys that matter in production: provider activation, base URL, model, and auth presence

## Workflow Rules

- keep `workflow/` focused on TriggerFlow graph construction and chunk boundaries
- keep Dynamic Task facades and handler registries separate from stable TriggerFlow graph definitions when the plan is submitted as DAG data
- keep business stages explicit as chunks or sub flows instead of helper-to-helper jumps
- inject tool instances, loggers, and other dependencies as runtime resources rather than hardcoding them inside chunk logic
- use sub flows when a repeated business pipeline deserves an explicit reusable unit
- keep chunk names readable enough that exported flow configs, Mermaid diagrams, and local observation graphs stay understandable
- for long-running or externally driven workflows, create an execution explicitly and close it with `close()` / `async_close()` when the service boundary decides work is complete
- use execution state for per-run data and avoid shared flow data unless the project explicitly needs cross-execution shared state

## Async Rules

- default to async-first design for HTTP services, streaming, tool concurrency, TriggerFlow execution, and any path that benefits from overlap or cancellation
- treat sync APIs as wrappers for scripts, teaching examples, or compatibility bridges, not as the default service architecture
- keep async boundaries visible near the app or integration layer so request handlers, flow runners, and stream consumers do not hide blocking behavior
- if the project needs progressive UI updates, combine model-side structured streaming with workflow-side runtime stream rather than building ad hoc thread-based fan-out
- when runtime stream is exposed to a UI or worker, make execution close responsible for stopping the stream instead of relying on client-side timeouts

## Frontend Bridge

- when frontend teams need to adjust wording, fields, or behavior frequently, prefer config files as the bridge
- if the config only changes request-side prompt behavior, route it through prompt config
- if the config also changes stage counts, branch counts, concurrency, or other flow parameters, route it through settings plus TriggerFlow

## Optional DevTools Loop

- use `agently-devtools` as an optional PyPI-installed companion package for development, debugging, and evaluation
- use `agently-devtools init <project>` when the team wants a scaffolded starting point before wiring observation or evaluation
- keep DevTools endpoints in env or settings, for example `AGENTLY_DEVTOOLS_BASE_URL` and `AGENTLY_DEVTOOLS_INGEST_URL`
- attach `ObservationBridge` or `EvaluationBridge` in the app or integration layer instead of hiding them inside request or workflow helpers
- if the team needs a local observation API inside its own server process, use `create_local_observation_app(...)`
- do not require the DevTools source repository or editable installs in public integration guidance

## Initialization Decision

Project initialization should stay inside `agently`, not become a separate public skill.

Reason:

- initialization is not one mutually exclusive capability surface
- the first job is choosing owner layers and boundaries, which is what `agently` already owns
- only after that decision should work fan out into `agently-request`, `agently-runtime`, `agently-dynamic-task`, `agently-triggerflow`, or another owning skill

## Reference Pattern

`Agently-Daily-News-Collector` is the clearest public example of this split:

- `SETTINGS.yaml` keeps model, search, browse, workflow, and output knobs
- `news_collector/` acts as the app and integration layer
- `prompts/` keeps structured prompt contracts with placeholder injection
- `workflow/` builds the parent flow, sub flows, and chunk modules
- `tools/` stays replaceable and is injected into the runtime
