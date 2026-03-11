# Source Map

This reference points to the most relevant public Agently sources for TriggerFlow orchestration work.

## 1. Core implementation files

- [TriggerFlow core](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/TriggerFlow.py)
  Flow entrypoints, execution creation, runtime stream access, contract methods, and top-level orchestration methods live here.
- [TriggerFlow execution](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/Execution.py)
  Interrupts, runtime stream, result handling, contract validation, and execution-scoped state live here.
- [TriggerFlow contract runtime](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/Contract.py)
  Runtime contract validation, metadata export, and contract snapshot logic live here.
- [TriggerFlow process base](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/process/BaseProcess.py)
  `to`, `when`, `batch`, `collect`, `side_branch`, and `end` live here.
- [TriggerFlow for_each process](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/process/ForEachProcess.py)
  `for_each` and `end_for_each` live here.
- [TriggerFlow match process](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/process/MatchCaseProcess.py)
  `match`, `case`, `case_else`, and `if_condition` live here.
- [TriggerFlow runtime data type](https://github.com/AgentEra/Agently/blob/main/agently/types/trigger_flow/trigger_flow.py)
  `TriggerFlowRuntimeData`, `state`, `flow_state`, resources, emit, stream, and interrupt helpers live here.

## 2. Example files

- [Basics](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-01_basics.py)
- [Branching](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-02_branching.py)
- [Concurrency](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-03_concurrency.py)
- [Result mechanics](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-12_result_mechanics.py)

## 3. Test files

- [TriggerFlow basics and branch tests](https://github.com/AgentEra/Agently/tree/main/tests/test_cores)
- [TriggerFlow contract tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_contract.py)

## 4. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
