# Source Map

This reference points to the most relevant public Agently sources for TriggerFlow state and resource design.

## 1. Core implementation files

- [TriggerFlow core](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/TriggerFlow.py)
  Flow-level `flow_data`, flow-level runtime resources, and execution creation live here.
- [Execution](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/Execution.py)
  Execution-scoped runtime data, save/load state surfaces, and resource-key persistence live here.
- [BluePrint](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/BluePrint.py)
  Sub-flow capture/write-back, isolated child resources, and runtime-data / flow-data handler wiring live here.
- [TriggerFlow runtime data type](https://github.com/AgentEra/Agently/blob/main/agently/types/trigger_flow/trigger_flow.py)
  `TriggerFlowRuntimeData`, `state`, `flow_state`, resources, and helper accessors live here.

## 2. Example files

- [Data flow](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-04_data_flow.py)
- [Runtime resources](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-17_runtime_resources.py)
- [Sub flow capture and write-back](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-18_sub_flow_capture_write_back.py)
- [Execution state resume](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-14_execution_state_resume.py)

## 3. Test files

- [Runtime resources tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_runtime_resources.py)
- [Execution-state tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_execution_state.py)
- [Config and Mermaid tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_config_and_mermaid.py)

## 4. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
