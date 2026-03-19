# Project Framework

Use this reference when the task is not just one Agently API call, but the initial shape or refactor boundary of a real project.

## Default Split

The default Agently project should usually separate these layers:

- `SETTINGS.yaml` or another settings file for provider config, `${ENV.xxx}` placeholders, workflow knobs, search and browse options, output directories, and deployment-time switches
- `app/` or integration code for loading settings, validating required env values when needed, choosing async entrypoints, and wiring the flow or service
- `prompts/` for YAML or JSON prompt contracts
- `services/` for request wrappers, business-facing adapters, and response normalization
- `domain/` or `schemas/` for enums, input/output contracts, and shared value objects
- `workflow/` for TriggerFlow graphs and chunk modules
- `tools/` for replaceable adapters such as search, browse, MCP, or external services
- `tests/` for settings smoke checks, prompt or response checks, and API or flow validation
- `outputs/` and `logs/` for runtime artifacts

## Prompt Rules

- keep task-specific `input`, `info`, `instruct`, and `output` contracts in prompt files instead of Python string literals
- keep runtime variables as `${topic}`, `${language}`, `${column_title}`, and similar placeholders in YAML or JSON, then inject them through prompt mappings at load time
- use small code-side agent factories only for shared persona or editor roles that are reused across many prompts
- do not turn prompt files into workflow state stores

## Model Settings Rules

- keep provider settings outside prompt files and workflow code
- prefer `${ENV.xxx}` placeholders in settings files instead of committing secrets or environment-specific endpoints into Python
- when settings live in a file, prefer `Agently.load_settings("yaml_file", path, auto_load_env=True)` so the same config stays deployable outside Python
- when settings are created inline as a Python mapping, use `Agently.set_settings(...)`
- put provider-specific keys where the owning plugin actually reads them. For `OpenAICompatible`, prefer `plugins.ModelRequester.OpenAICompatible.*` instead of a root-level namespace
- if the application must fail fast on missing env values, load `.env` in the integration layer first, validate required names, and then still hand the raw placeholder-based settings to Agently
- after loading settings, validate the effective keys that matter in production: provider activation, base URL, model, and auth presence

## Workflow Rules

- keep `workflow/` focused on TriggerFlow graph construction and chunk boundaries
- keep business stages explicit as chunks or sub flows instead of helper-to-helper jumps
- inject tool instances, loggers, and other dependencies as runtime resources rather than hardcoding them inside chunk logic
- use sub flows when a repeated business pipeline deserves an explicit reusable unit

## Async Rules

- default to async-first design for HTTP services, streaming, tool concurrency, TriggerFlow execution, and any path that benefits from overlap or cancellation
- treat sync APIs as wrappers for scripts, teaching examples, or compatibility bridges, not as the default service architecture
- keep async boundaries visible near the app or integration layer so request handlers, flow runners, and stream consumers do not hide blocking behavior
- if the project needs progressive UI updates, combine model-side structured streaming with workflow-side runtime stream rather than building ad hoc thread-based fan-out

## Frontend Bridge

- when frontend teams need to adjust wording, fields, or behavior frequently, prefer config files as the bridge
- if the config only changes request-side prompt behavior, route it through prompt config
- if the config also changes stage counts, branch counts, concurrency, or other flow parameters, route it through settings plus TriggerFlow

## Initialization Decision

Project initialization should stay inside `agently-playbook`, not become a separate public skill.

Reason:

- initialization is not one mutually exclusive capability surface
- the first job is choosing owner layers and boundaries, which is what `agently-playbook` already owns
- only after that decision should work fan out into `agently-model-setup`, `agently-prompt-management`, `agently-triggerflow`, or other leaf skills

## Reference Pattern

`Agently-Daily-News-Collector` is the clearest public example of this split:

- `SETTINGS.yaml` keeps model, search, browse, workflow, and output knobs
- `news_collector/` acts as the app and integration layer
- `prompts/` keeps structured prompt contracts with placeholder injection
- `workflow/` builds the parent flow, sub flows, and chunk modules
- `tools/` stays replaceable and is injected into the runtime
