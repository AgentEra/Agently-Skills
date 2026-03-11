# Source Map

This reference points to the most relevant public Agently sources for TriggerFlow interrupts and runtime stream work.

## 1. Core implementation files

- [TriggerFlow execution](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/Execution.py)
  `pause_for`, `continue_with`, interrupt state, runtime stream queue, contract-aware stream validation, timeout behavior, and result interaction live here.
- [TriggerFlow runtime data type](https://github.com/AgentEra/Agently/blob/main/agently/types/trigger_flow/trigger_flow.py)
  `TriggerFlowRuntimeData` exposes interrupt and runtime-stream helpers to chunks.
- [TriggerFlow core](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/TriggerFlow.py)
  `get_async_runtime_stream(...)`, `get_runtime_stream(...)`, and execution entrypoints live here.
- [TriggerFlow contract types](https://github.com/AgentEra/Agently/blob/main/agently/types/trigger_flow/contract.py)
  Interrupt system-stream schema and exported contract metadata live here.

## 2. Example files

- [Runtime stream](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-10_runtime_stream.py)
- [Runtime stream lifecycle](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-13_runtime_stream_lifecycle.py)
- [Execution state resume](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-14_execution_state_resume.py)
- [Safe cycle](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-15_safe_cycle.py)

## 3. Test files

- [Pause and resume tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_pause_resume.py)
- [Execution state tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_execution_state.py)
- [TriggerFlow contract tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_contract.py)

## 4. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
