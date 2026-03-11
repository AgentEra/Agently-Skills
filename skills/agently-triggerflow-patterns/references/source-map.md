# Source Map

This reference points to the most relevant public sources for TriggerFlow pattern work.

## 1. Core Agently implementation files

- [BaseProcess](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/process/BaseProcess.py)
  `when`, `batch`, `collect`, `side_branch`, and event-driven orchestration live here.
- [ForEachProcess](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/process/ForEachProcess.py)
  `for_each(...)` and `end_for_each()` live here.
- [Execution](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/Execution.py)
  Result ownership, interrupts, and execution status live here.

## 2. Agently example files

- [Branching](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-02_branching.py)
- [Concurrency](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-03_concurrency.py)
- [Emit and when](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-07_emit_when.py)
- [Loop flow](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-08_loop_flow.py)
- [Side branch](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-11_side_branch.py)
- [Safe cycle](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-15_safe_cycle.py)

## 3. Agently test files

- [TriggerFlow runtime resources tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_runtime_resources.py)
- [TriggerFlow execution-state tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_execution_state.py)

## 4. External pattern references

- Anthropic, Building Effective AI Agents: https://resources.anthropic.com/building-effective-ai-agents
- LangGraph workflows and agents: https://docs.langchain.com/oss/python/langgraph/workflows-agents
- Azure AI agent orchestration patterns: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- ReAct paper: https://openreview.net/pdf?id=WE_vluYUL-X

## 5. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
