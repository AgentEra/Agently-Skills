# Registration And Selection

Use this page when the main question is how a tool enters an agent request.

## 1. Local Python Tool

Use a local Python tool when the logic already exists in the same codebase and should run deterministically.

Common entrypoints:

- `@agent.tool_func`
- `agent.register_tool(...)`

Use `@agent.tool_func` when the function signature and docstring already describe the tool well.

Use `register_tool(...)` when:

- the tool name should differ from the Python function name
- kwargs metadata should be written explicitly
- return metadata should be supplied explicitly

## 2. Attaching Tools To One Agent

Use `agent.use_tools(...)` when the tool already exists and should only be visible to one agent.

You can pass:

- a callable
- a tool name
- a mixed list of callables and names

Agently scopes tools to the agent by tag, so one shared tool registry can still support different agents safely.

## 3. Choosing Between Local Tools, Built-In Tools, And MCP

- local business logic -> local Python tool
- common web search, browsing, or guarded shell commands -> built-in tools
- external tool server or remote capability catalog -> `agently-mcp`

## 4. Async-First Rule

Prefer async tool functions when:

- the tool performs I/O
- several tool calls may run in one request round
- the application already runs inside an async service

Sync tools still work, but async tools fit Agently's runtime better.
