# Source Map

This reference points to the most relevant public sources for Agently MCP work.

## 1. Core Agently implementation files

- [ToolExtension](https://github.com/AgentEra/Agently/blob/main/agently/builtins/agent_extensions/ToolExtension.py)
  Agent-facing `use_mcp(...)` and agent-tagging behavior live here.
- [Tool](https://github.com/AgentEra/Agently/blob/main/agently/core/Tool.py)
  Shared tool interfaces and tool-manager wiring live here.
- [AgentlyToolManager](https://github.com/AgentEra/Agently/blob/main/agently/builtins/plugins/ToolManager/AgentlyToolManager.py)
  MCP client registration, schema conversion, and result handling live here.

## 2. Agently example files

- [Step-by-step MCP](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/10-mcp.py)
- [MCP agent example](https://github.com/AgentEra/Agently/blob/main/examples/mcp/mcp_agent.py)
- [Local MCP server example](https://github.com/AgentEra/Agently/blob/main/examples/mcp/cal_mcp_server.py)

## 3. Agently test files

- [Tool tests including MCP](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_tool.py)
- [Local MCP server test fixture](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/cal_mcp_server.py)

## 4. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
