# Agent Use And Tagging

Use this page when the main problem is which agent should see which MCP tools.

## 1. Agent-Level Visibility

`agent.use_mcp(...)` registers MCP tools with the same agent-scoping tag model used by normal tools.

This matters when:

- different agents should see different tool sets
- one agent uses MCP and another should not
- an application mixes local tools and MCP tools

## 2. Mixing MCP And Normal Tools

After MCP registration, the agent can still use:

- local Python tools
- built-in Search/Browse/Cmd tools
- MCP tools

in the same overall tool system.

Choose MCP only for the tools that truly need an MCP server boundary.
