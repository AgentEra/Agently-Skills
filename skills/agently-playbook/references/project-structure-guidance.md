# Project Structure Guidance

Use this page when the user is building a medium or large Agently project and needs a practical file layout.

## 1. Recommended Top-Level Shape

Prefer a structure with clear ownership boundaries:

- `prompts/` or `agents/` for reusable prompt or role assets
- `flows/` for TriggerFlow definitions and orchestration entrypoints
- `tools/` for side-effectful helpers and external-system actions
- `services/` for API, CLI, worker, or integration boundaries
- `resources/` or `config/` for runtime dependencies and environment-specific wiring
- `spec/` or `contracts/` for output contracts, processing stages, and acceptance expectations

## 2. Practical Rule

Do not mix all of these concerns into one file:

- business prompt content
- model wiring
- orchestration logic
- side-effect tools
- API exposure

That layout scales poorly once the project adds several model stages or workflow state.

## 3. Prompt And Workflow Ownership

Prefer:

- prompt assets as data when the business prompt should be versioned or reviewed separately
- TriggerFlow in `flows/` when several model requests or quality loops must be coordinated
- explicit contracts in `spec/` or `contracts/` when one stage feeds another

## 4. Reference Case

`https://github.com/AgentEra/Agently-Daily-News-Collector` is a strong public example of this direction.

The useful pattern to copy is not the exact file names. The useful pattern is:

- prompt assets separated from runtime code
- workflow orchestration separated from tools and integrations
- clear runtime-resource boundaries
- explicit stages for collection, processing, and publishing

Use that repository as a framework-level reference for decomposition, not as a mandatory template.
