---
name: agently-mcp
description: Use only when the main task is direct MCP server registration into Agently tools through `agent.use_mcp(...)` or `tool.use_mcp(...)`, including stdio or HTTP transports, schema mapping, agent-scoped MCP tool visibility, or MCP result and error handling.
---

# Agently MCP

This skill is the direct leaf for MCP-backed tool registration after the user already knows the tool should come from an external MCP server. It focuses on transport registration, schema mapping, agent scoping, and result behavior. It does not choose between local tools, generic tool-loop design, or service exposure, and it does not replace the general tool-loop skill or TriggerFlow workflow design.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- `agent.use_mcp(...)`
- `agent.async_use_mcp(...)`
- `Agently.tool.use_mcp(...)`
- stdio or HTTP MCP transports
- MCP tool schema mapping into Agently tool metadata
- agent-scoped MCP tool visibility
- MCP result and error interpretation

Do not use this skill for:

- local Python tool functions
- generic tool-loop tuning as the main problem
- TriggerFlow orchestration
- FastAPI service exposure

## Workflow

1. Start with [references/transports-and-registration.md](references/transports-and-registration.md) when the main problem is how an MCP server is attached.
2. Read [references/schema-and-results.md](references/schema-and-results.md) when the main problem is tool signatures, returned values, or MCP validation errors.
3. Read [references/agent-use-and-tagging.md](references/agent-use-and-tagging.md) when the main problem is which agent should see which MCP tools.
4. If the task becomes general tool-loop design or built-in tool selection, switch to `agently-tools`.
5. If behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

MCP in Agently is a tool-registration pathway.

- MCP tools are discovered from an MCP server
- their schemas are converted into Agently tool metadata
- after registration, they participate in the same tool system as other tools

So MCP answers:

- where the tool comes from
- how it is registered
- how its schema is mapped

The normal tool loop still belongs to `agently-tools`.

## Selection Rules

- external MCP server should supply tools -> `use_mcp(...)`
- tool should be visible to one agent only -> `agent.use_mcp(...)`
- tool should be globally registered first -> `Agently.tool.use_mcp(...)`
- local Python function is enough -> `agently-tools`

## Important Boundaries

- MCP registration is not a separate planning loop; the normal Agently tool loop still executes the tool later
- if the server returns structured content, Agently prefers that structured content directly
- if the server returns text, Agently tries JSON parsing first and falls back to raw text

## References

- `references/source-map.md`
- `references/transports-and-registration.md`
- `references/schema-and-results.md`
- `references/agent-use-and-tagging.md`
- `references/troubleshooting.md`
