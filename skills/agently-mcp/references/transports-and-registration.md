# Transports And Registration

Use this page when the main problem is how the MCP server enters Agently.

## 1. Agent-Scoped Registration

Use:

- `await agent.use_mcp(transport)`

when the MCP tools should only be visible to one agent.

This is the usual choice for application code.

## 2. Shared Registration

Use:

- `Agently.tool.use_mcp(transport)`

when MCP tools should be registered on the shared tool manager first.

This is useful when several agents should later share the same registered MCP tools.

## 3. Common Transport Shapes

Agently accepts transport values that FastMCP client can use, including common cases such as:

- local stdio script path
- HTTP MCP endpoint URL
- richer MCP transport configuration objects

Choose stdio when the server lives in the same deployment boundary.

Choose HTTP when the MCP server is already exposed as a network service.
