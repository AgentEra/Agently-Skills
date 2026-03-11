# Source Map

This reference points to the most relevant public Agently sources for input-composition work.

## 1. Core implementation files

- [Agent core](https://github.com/AgentEra/Agently/blob/main/agently/core/Agent.py)
  Agent-level prompt storage, quick prompt methods, `always=True`, and `chat_history` helpers live here.
- [ModelRequest core](https://github.com/AgentEra/Agently/blob/main/agently/core/ModelRequest.py)
  Request-level prompt storage, direct request composition, and `get_response()` prompt clearing live here.
- [Prompt core](https://github.com/AgentEra/Agently/blob/main/agently/core/Prompt.py)
  Core prompt mutation methods, placeholder mappings, and prompt inheritance behavior live here.
- [Prompt data model](https://github.com/AgentEra/Agently/blob/main/agently/types/data/prompt.py)
  Standard prompt slots, `chat_history` validation, `attachment` validation, and the prompt data model live here.
- [AgentlyPromptGenerator](https://github.com/AgentEra/Agently/blob/main/agently/builtins/plugins/PromptGenerator/AgentlyPromptGenerator.py)
  Prompt emptiness checks, `to_text()`, `to_messages()`, chat-history rendering, attachment rendering, and prompt ordering live here.
- [SessionExtension](https://github.com/AgentEra/Agently/blob/main/agently/builtins/agent_extensions/SessionExtension.py)
  Active-session override behavior for `chat_history` lives here. This skill treats that as a boundary, not its main subject.
- [DataFormatter](https://github.com/AgentEra/Agently/blob/main/agently/utils/DataFormatter.py)
  Recursive placeholder substitution and prompt-data sanitization live here.
- [ConfigurePromptExtension](https://github.com/AgentEra/Agently/blob/main/agently/builtins/agent_extensions/ConfigurePromptExtension.py)
  YAML and JSON prompt import/export live here. This skill treats that as a separate concern and does not document the full file-based workflow.

## 2. Example files

- [Prompt methods example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/02-prompt_methods.py)
- [Configure prompt example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/04-configure_prompt.py)
- [Chat history example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/08-chat_history.py)

## 3. Test files

- [Prompt generator tests](https://github.com/AgentEra/Agently/blob/main/tests/test_plugins/test_prompt_generator/test_agently_prompt_generator.py)
- [Session extension tests](https://github.com/AgentEra/Agently/blob/main/tests/test_extensions/test_session_extension.py)

## 4. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
- Prompt management overview: `https://agently.tech/docs/en/prompt-management/overview.html`
- Prompt layers docs: `https://agently.tech/docs/en/prompt-management/layers.html`
- Quick syntax docs: `https://agently.tech/docs/en/prompt-management/quick-syntax.html`
- Variables docs: `https://agently.tech/docs/en/prompt-management/variables.html`
