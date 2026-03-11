# Source Map

This reference points to the most relevant public Agently sources for TriggerFlow sub-flow work.

## 1. Core implementation files

- [BaseProcess](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/process/BaseProcess.py)
  `to_sub_flow(...)` is exposed here.
- [BluePrint](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/BluePrint.py)
  Capture, write-back compilation, isolated child-flow instantiation, runtime-stream bridging, and current limits live here.
- [Definition](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/Definition.py)
  Sub-flow config export validation and Mermaid rendering live here.

## 2. Example files

- [Sub flow capture and write-back](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-18_sub_flow_capture_write_back.py)
- [Export nested sub flow config and Mermaid](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-16_flow_config_and_mermaid.py)

## 3. Test files

- [TriggerFlow config and Mermaid tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_config_and_mermaid.py)

## 4. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
