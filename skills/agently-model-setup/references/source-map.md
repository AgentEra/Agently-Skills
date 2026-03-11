# Source Map

This reference helps locate the most relevant public Agently sources for model setup work.

## 1. Core implementation files

- [OpenAICompatible requester](https://github.com/AgentEra/Agently/blob/main/agently/builtins/plugins/ModelRequester/OpenAICompatible.py)
  Default settings, `model_type`, request-body assembly, `request_options` merging, URL construction, auth handling, and response mapping live here.
- [Agent core](https://github.com/AgentEra/Agently/blob/main/agently/core/Agent.py)
  Entry points for `agent.set_settings()`, `agent.options()`, and `attachment()`.
- [ModelRequest core](https://github.com/AgentEra/Agently/blob/main/agently/core/ModelRequest.py)
  The request-level prompt and response entry point.
- [AgentlyPromptGenerator](https://github.com/AgentEra/Agently/blob/main/agently/builtins/plugins/PromptGenerator/AgentlyPromptGenerator.py)
  How `chat`, `completions`, and rich-content messages are generated.
- [Prompt data model](https://github.com/AgentEra/Agently/blob/main/agently/types/data/prompt.py)
  Definitions and validation for `options`, `attachment`, and `PromptStandardSlot`.
- [Settings utility](https://github.com/AgentEra/Agently/blob/main/agently/utils/Settings.py)
  Path aliases and the mapping for `OpenAICompatible` / `OpenAI` / `OAIClient`.

## 2. Example files

- [Step-by-step settings example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/01-settings.py)
- [OpenAI example](https://github.com/AgentEra/Agently/blob/main/examples/model_configures/OpenAI.py)
- [DeepSeek example](https://github.com/AgentEra/Agently/blob/main/examples/model_configures/DeepSeek.py)
- [Gemini example](https://github.com/AgentEra/Agently/blob/main/examples/model_configures/Gemini.py)
- [AliQwen example](https://github.com/AgentEra/Agently/blob/main/examples/model_configures/AliQwen.py)
- [Baidu Ernie example](https://github.com/AgentEra/Agently/blob/main/examples/model_configures/BaiduErnie.py)
- [Ollama OpenAI-compatible example](https://github.com/AgentEra/Agently/blob/main/examples/model_configures/ollama-OpenAI-compatible-format.py)
- [Custom auth headers example](https://github.com/AgentEra/Agently/blob/main/examples/model_configures/auth_by_customize_headers.py)
- [Custom auth body example](https://github.com/AgentEra/Agently/blob/main/examples/model_configures/auth_by_customize_body_data.py)
- [Full URL example](https://github.com/AgentEra/Agently/blob/main/examples/model_configures/full_url_instead_of_base_url.py)
- [VLM step-by-step example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/13-vlm.py)
- [Baidu Ernie VLM example](https://github.com/AgentEra/Agently/blob/main/examples/vlm_support/Baidu-Ernie-4_5-turbo-vl.py)
- [Specific streaming example](https://github.com/AgentEra/Agently/blob/main/examples/basic/specific_streaming.py)

## 3. Test files

- [OpenAICompatible tests](https://github.com/AgentEra/Agently/blob/main/tests/test_plugins/test_model_requester/test_openai_compatible.py)
- [Request tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_request.py)
- [Prompt generator tests](https://github.com/AgentEra/Agently/blob/main/tests/test_plugins/test_prompt_generator/test_agently_prompt_generator.py)

## 4. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
- Model settings docs: `https://agently.tech/docs/en/model-settings.html`
- OpenAI API format docs: `https://agently.tech/docs/en/openai-api-format.html`
- Settings docs: `https://agently.tech/docs/en/settings.html`
