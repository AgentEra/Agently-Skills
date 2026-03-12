---
name: agently-tools
description: Use only when the main task is direct local or built-in Agently tool registration and request-time tool-loop control, including `@agent.tool_func`, `register_tool(...)`, `use_tools(...)`, Search, Browse, Cmd, custom tool-loop handlers, or tool logs.
---

# Agently Tools

This skill is the direct leaf for local and built-in tool usage after the Agently request path is already known. It focuses on tool registration, agent scoping, loop control, built-in Search/Browse/Cmd usage, and result inspection. It does not choose between local tools, MCP-backed tools, session continuity, or service exposure, and it does not cover TriggerFlow orchestration or generic web-service design.

Prerequisite: Agently `>= 4.0.8.5`.

## Scope

Use this skill for:

- `@agent.tool_func`
- `agent.register_tool(...)`
- `agent.use_tools(...)`
- built-in `Search`, `Browse`, and `Cmd`
- `set_tool_loop(...)`
- custom plan-analysis or tool-execution handlers
- tool logs and tool results from one model request

Do not use this skill for:

- MCP server registration or MCP transport choices
- model setup, output schema design, or structured streaming as the main problem
- TriggerFlow workflow design
- FastAPI service exposure

## Workflow

1. Start with [references/registration-and-selection.md](references/registration-and-selection.md) when choosing how a tool should be registered or attached to an agent.
2. Read [references/tool-loop-and-control.md](references/tool-loop-and-control.md) when the issue is loop behavior, rounds, concurrency, timeout, or custom handlers.
3. Read [references/builtin-tools.md](references/builtin-tools.md) when the task should use Search, Browse, or Cmd.
4. Read [references/observability-and-results.md](references/observability-and-results.md) when the task is about tool logs, action results, or response inspection.
5. If the tool comes from an MCP server, switch to `agently-mcp`.
6. If the task becomes a workflow or multi-step orchestration problem, switch to `agently-triggerflow-playbook`.
7. If behavior still looks wrong, use [references/troubleshooting.md](references/troubleshooting.md).

## Core Mental Model

Agently tools are request-time capability extensions.

- tools are registered on the shared tool manager
- `agent.use_tools(...)` scopes selected tools to one agent by tag
- the tool loop plans, executes, and feeds tool results back into the same request
- the final response keeps tool logs in metadata

Agently guidance for tool work should remain async-first:

- prefer async tool functions
- prefer async built-in tool calls
- cap tool-loop rounds and concurrency explicitly

## Selection Rules

- local deterministic Python helper -> `@agent.tool_func` or `register_tool(...)`
- attach one or more already-registered tools to an agent -> `use_tools(...)`
- expose web search, browsing, or shell access with existing helpers -> built-in tools
- tune max rounds, concurrency, or timeout -> `set_tool_loop(...)`
- replace planning or execution policy -> custom plan-analysis or execution handler
- external tool server instead of local Python function -> `agently-mcp`

## Important Boundaries

- the tool loop is an agent/request capability, not a TriggerFlow substitute
- MCP registration belongs to `agently-mcp`, even though MCP tools later participate in the same tool loop
- response metadata and output control are separate concerns; use `agently-output-control` when the main problem is response consumption

## References

- `references/source-map.md`
- `references/registration-and-selection.md`
- `references/tool-loop-and-control.md`
- `references/builtin-tools.md`
- `references/observability-and-results.md`
- `references/troubleshooting.md`
