# Source Map

This reference points to the most relevant public Agently sources for TriggerFlow model-integration work.

## 1. Core implementation files

- [BaseAgent](https://github.com/AgentEra/Agently/blob/main/agently/core/Agent.py)
  Defines `create_request(...)`, `create_temp_request()`, and the shared agent/request structure.
- [ModelRequest](https://github.com/AgentEra/Agently/blob/main/agently/core/ModelRequest.py)
  Defines request prompt methods, `get_response()`, async getters, and async generators.
- [ModelResponseResult](https://github.com/AgentEra/Agently/blob/main/agently/core/ModelResponseResult.py)
  Defines parsed data access, response reuse, and result getters.
- [TriggerFlow core](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/TriggerFlow.py)
  Defines flow entrypoints and runtime-stream access.
- [TriggerFlow execution](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/Execution.py)
  Defines execution lifecycle, result handling, runtime stream, and interrupts.
- [TriggerFlow base process](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/process/BaseProcess.py)
  Defines `to(...)`, `batch(...)`, `collect(...)`, `side_branch(...)`, and sub-flow plumbing.
- [TriggerFlow for-each process](https://github.com/AgentEra/Agently/blob/main/agently/core/TriggerFlow/process/ForEachProcess.py)
  Defines `for_each(...)` fan-out and collected list behavior.
- [FastAPI integration](https://github.com/AgentEra/Agently/blob/main/agently/integrations/fastapi.py)
  Shows how Agently exposes `ModelRequest` or `TriggerFlow` outputs through HTTP streaming helpers.

## 2. Example files

- [TriggerFlow runtime stream example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-10_runtime_stream.py)
- [TriggerFlow sub-flow capture/write-back example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/11-triggerflow-18_sub_flow_capture_write_back.py)
- [Auto loop step-by-step example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/12-auto_loop.py)
- [Auto loop FastAPI flow example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/auto_loop_fastapi/app/flow.py)
- [FastAPI TriggerFlow + Ollama example](https://github.com/AgentEra/Agently/blob/main/examples/fastapi/fastapi_helper_triggerflow_ollama.py)
- [Response result example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/05-response_result.py)
- [Streaming example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/06-streaming.py)

## 3. Test files

- [Request tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_request.py)
- [Response tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_response.py)
- [TriggerFlow config and Mermaid tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_trigger_flow_config_and_mermaid.py)

## 4. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
- Async support docs: `https://agently.tech/docs/en/async-support.html`
- Output control overview: `https://agently.tech/docs/en/output-control/overview.html`
- Instant streaming docs: `https://agently.tech/docs/en/output-control/instant-streaming.html`
- TriggerFlow docs home: `https://agently.tech/docs/en/triggerflow/`
