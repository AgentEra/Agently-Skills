# Source Map

This reference points to the most relevant public Agently sources for TriggerFlow execution-state work.

## 1. Core implementation files

- [TriggerFlow execution](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/Execution.py)
  Defines `save()`, `load()`, interrupt state, result readiness, runtime resources, and resume behavior.
- [TriggerFlow core](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/TriggerFlow.py)
  Defines `create_execution(...)`, start helpers, and runtime-resource injection at flow or execution scope.
- [TriggerFlow types](https://github.com/AgentEra/Agently/blob/main/agently/types/trigger_flow/trigger_flow.py)
  Exposes runtime data helpers and execution-facing methods on the data object.

## 2. Example files

- [TriggerFlow execution-state resume example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-14_execution_state_resume.py)
- [TriggerFlow runtime-resources example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-17_runtime_resources.py)
- [TriggerFlow save/load execution-state example](https://github.com/AgentEra/Agently/blob/main/examples/trigger_flow/save_and_load_execution_state.py)

## 3. Test files

- [TriggerFlow execution-state tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_execution_state.py)
- [TriggerFlow pause/resume tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_pause_resume.py)
- [TriggerFlow runtime-resources tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_runtime_resources.py)

## 4. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
- TriggerFlow docs home: `https://agently.tech/docs/en/triggerflow/`
