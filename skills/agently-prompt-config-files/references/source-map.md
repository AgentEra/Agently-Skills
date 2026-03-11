# Source Map

This reference points to the most relevant public Agently sources for prompt-config work.

## 1. Core implementation files

- [ConfigurePromptExtension](https://github.com/AgentEra/Agently/blob/main/agently/builtins/agent_extensions/ConfigurePromptExtension.py)
  `load_yaml_prompt(...)`, `load_json_prompt(...)`, `.agent`, `.request`, `.alias`, mappings handoff, and prompt export all live here.
- [Agent core](https://github.com/AgentEra/Agently/blob/main/agently/core/Agent.py)
  `set_agent_prompt(...)`, `set_request_prompt(...)`, quick prompt methods, and the low-level prompt-writing targets live here.
- [Prompt core](https://github.com/AgentEra/Agently/blob/main/agently/core/Prompt.py)
  Placeholder substitution on prompt keys and values is applied here.

## 2. Example files

- [Step-by-step configure prompt example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/04-configure_prompt.py)
- [Load YAML prompt](https://github.com/AgentEra/Agently/blob/main/examples/configure_prompt/load_yaml_prompt.py)
- [Load JSON prompt](https://github.com/AgentEra/Agently/blob/main/examples/configure_prompt/load_json_prompt.py)
- [Load multiple YAML prompts by key path](https://github.com/AgentEra/Agently/blob/main/examples/configure_prompt/load_multiple_yaml_prompts.py)
- [Export prompt to YAML / JSON](https://github.com/AgentEra/Agently/blob/main/examples/configure_prompt/to_configure_prompt.py)
- [YAML prompt real case](https://github.com/AgentEra/Agently/blob/main/examples/configure_prompt/yaml_prompt_real_case.py)

## 3. Test files

- [ConfigurePromptExtension tests](https://github.com/AgentEra/Agently/blob/main/tests/test_extensions/test_configure_prompt_extension.py)

## 4. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
