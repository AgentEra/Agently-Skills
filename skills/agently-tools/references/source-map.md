# Source Map

This reference points to the most relevant public sources for Agently tool work.

## 1. Core Agently implementation files

- [ToolExtension](https://github.com/AgentEra/Agently/blob/main/agently/builtins/agent_extensions/ToolExtension.py)
  Agent-facing tool registration, scoping, loop settings, and request/broadcast hooks live here.
- [Tool](https://github.com/AgentEra/Agently/blob/main/agently/core/Tool.py)
  Loop planning, execution control, default handlers, and tool-result formatting live here.
- [AgentlyToolManager](https://github.com/AgentEra/Agently/blob/main/agently/builtins/plugins/ToolManager/AgentlyToolManager.py)
  Registration, tagging, callable shifting, and MCP-backed tool registration live here.

## 2. Built-in tool implementations

- [Search](https://github.com/AgentEra/Agently/blob/main/agently/builtins/tools/Search.py)
- [Browse](https://github.com/AgentEra/Agently/blob/main/agently/builtins/tools/Browse.py)
- [Cmd](https://github.com/AgentEra/Agently/blob/main/agently/builtins/tools/Cmd.py)

## 3. Agently example files

- [Step-by-step tools](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/07-tools.py)
- [Built-in search example](https://github.com/AgentEra/Agently/blob/main/examples/builtin_tools/search.py)
- [Built-in browse example](https://github.com/AgentEra/Agently/blob/main/examples/builtin_tools/browse.py)
- [Built-in cmd example](https://github.com/AgentEra/Agently/blob/main/examples/builtin_tools/cmd.py)

## 4. Agently test files

- [Tool tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_tool.py)
- [Browse extraction tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_browse.py)

## 5. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
