# Schema And Results

Use this page when the main problem is what Agently learns from the MCP server.

## 1. Schema Mapping

When Agently loads MCP tools, it converts:

- `inputSchema` -> tool kwargs metadata
- `outputSchema` -> tool return metadata

This means MCP tools become ordinary Agently tool definitions after registration.

## 2. Result Preference Order

When an MCP tool call succeeds, Agently prefers results in this order:

1. structured content
2. text content parsed as JSON
3. raw text content

When the MCP tool reports an error, Agently returns an error-shaped object instead of raising directly inside the tool result path.

## 3. Validation Errors

If MCP schema validation fails, the error comes back from the server response. Treat this as an input-shape problem first, not a registration problem.
