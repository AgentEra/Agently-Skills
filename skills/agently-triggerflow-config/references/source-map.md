# Source Map

This reference points to the most relevant public Agently sources for TriggerFlow config work.

## 1. Core implementation files

- [TriggerFlow core](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/TriggerFlow.py)
  Exposes blueprint copy, flow-config export/import, and Mermaid helpers on the public `TriggerFlow` object.
- [TriggerFlow blueprint](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/BluePrint.py)
  Implements `get_flow_config()`, `get_json_flow()`, `get_yaml_flow()`, `load_*`, registry merging, and blueprint copy.
- [TriggerFlow definition](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/Definition.py)
  Defines serializable flow-definition structure, exported contract metadata, and Mermaid rendering.
- [TriggerFlow contract runtime](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/Contract.py)
  Shows how runtime contract metadata is exported from live Python contracts.
- [TriggerFlow base process](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/process/BaseProcess.py)
  Attaches chunks, branches, sub flows, and operator metadata into the definition.
- [TriggerFlow match-case process](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/process/MatchCaseProcess.py)
  Defines conditional-routing operators that appear in config and Mermaid.
- [TriggerFlow for-each process](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/process/ForEachProcess.py)
  Defines `for_each` operators that appear in config and Mermaid.

## 2. Example files

- [TriggerFlow blueprint example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-05_blueprint.py)
- [TriggerFlow flow-config and Mermaid example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-16_flow_config_and_mermaid.py)
- [TriggerFlow export Mermaid and flow-config example](https://github.com/AgentEra/Agently/blob/main/examples/trigger_flow/export_mermaid_and_flow_config.py)
- [TriggerFlow save and load blueprint example](https://github.com/AgentEra/Agently/blob/main/examples/trigger_flow/save_and_load_blue_print.py)

## 3. Test files

- [TriggerFlow config and Mermaid tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_config_and_mermaid.py)
- [TriggerFlow runtime-resources config test](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_runtime_resources.py)
- [TriggerFlow contract tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_contract.py)

## 4. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
- TriggerFlow docs home: `https://agently.tech/docs/en/triggerflow/`
