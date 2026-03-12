# TriggerFlow Project Structure Guidance

Use this page when the user is building a workflow-oriented Agently project with several files or services.

## 1. Keep These Concerns Separate

Prefer:

- `flows/` for TriggerFlow definitions
- `prompts/` or `agents/` for reusable request assets per stage
- `tools/` for external actions and side effects
- `services/` for API or worker entrypoints
- `resources/` or `config/` for runtime injections
- `spec/` or `contracts/` for stage-to-stage data contracts and acceptance targets

## 2. Why This Matters

Once a workflow includes:

- several model stages
- bounded loops
- runtime stream
- approval or resume behavior

the project becomes much easier to evolve if orchestration, prompts, and side effects do not live in one file.

## 3. Reference Case

`https://github.com/AgentEra/Agently-Daily-News-Collector` is a useful public example of this decomposition style.

The main lesson is:

- prompts can be versioned separately
- orchestration can stay explicit
- tools and integrations can stay isolated
- runtime resources can be wired at service boundaries instead of being hidden inside flow logic
