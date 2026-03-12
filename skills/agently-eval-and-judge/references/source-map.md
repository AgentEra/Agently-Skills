# Source Map

This reference points to the most relevant public Agently sources for evaluation and judge-model work.

## 1. Core implementation files

- [Agent core](https://github.com/AgentEra/Agently/blob/main/agently/core/Agent.py)
  Entry points for per-agent settings, prompt state, and request creation.
- [ModelRequest core](https://github.com/AgentEra/Agently/blob/main/agently/core/ModelRequest.py)
  Core request lifecycle and response entry points for generator and judge requests.
- [ModelResponseResult core](https://github.com/AgentEra/Agently/blob/main/agently/core/ModelResponseResult.py)
  Result getters, retries, and cached response reuse for review flows.
- [OpenAICompatible requester](https://github.com/AgentEra/Agently/blob/main/agently/builtins/plugins/ModelRequester/OpenAICompatible.py)
  Useful when the evaluation path depends on local Ollama or another OpenAI-compatible judge endpoint.
- [AgentlyResponseParser](https://github.com/AgentEra/Agently/blob/main/agently/builtins/plugins/ResponseParser/AgentlyResponseParser.py)
  Parsed-result and metadata handling for structured evaluation outputs.

## 2. Example files

- [Output format control example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/03-output_format_control.py)
- [Response result example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/05-response_result.py)
- [ensure_keys example](https://github.com/AgentEra/Agently/blob/main/examples/basic/ensure_keys_in_output.py)
- [Prompt mappings example](https://github.com/AgentEra/Agently/blob/main/examples/basic/prompt_mappings.py)
- [Ollama OpenAI-compatible example](https://github.com/AgentEra/Agently/blob/main/examples/model_configures/ollama-OpenAI-compatible-format.py)

## 3. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
- Model settings docs: `https://agently.tech/docs/en/model-settings.html`
- OpenAI API format docs: `https://agently.tech/docs/en/openai-api-format.html`
- Output control overview: `https://agently.tech/docs/en/output-control/overview.html`
- ensure_keys docs: `https://agently.tech/docs/en/output-control/ensure-keys.html`
