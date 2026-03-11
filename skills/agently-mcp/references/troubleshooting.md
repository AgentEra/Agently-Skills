# Troubleshooting

- The tool is local Python code, not an MCP server:
  Switch to `agently-tools`.
- The MCP tool appears registered but not visible to the agent:
  Check whether it was attached with `agent.use_mcp(...)` or only registered globally.
- The server rejects the call:
  Check the MCP input schema first; this is often a kwargs-shape issue.
- The main issue is now tool-loop policy rather than MCP registration:
  Switch to `agently-tools`.
