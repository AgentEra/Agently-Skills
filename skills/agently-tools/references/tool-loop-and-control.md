# Tool Loop And Control

Use this page when the main problem is loop behavior rather than registration.

## 1. Default Loop Model

Once an agent has visible tools and tool loop is enabled, Agently can:

1. plan whether to use tools
2. generate one or more tool commands
3. execute them
4. feed the results back into the same request
5. stop when the loop decides to answer directly

## 2. Main Loop Controls

Use `set_tool_loop(...)` when you need:

- `enabled`
- `max_rounds`
- `concurrency`
- `timeout`

Recommended defaults for real services:

- keep `max_rounds` explicit
- cap `concurrency` when tools perform network or heavy local I/O
- set `timeout` when requests should fail fast instead of hanging

## 3. Custom Planning Or Execution

Use:

- `register_tool_plan_analysis_handler(...)`
- `register_tool_execution_handler(...)`

when the default loop policy is not enough.

Typical reasons:

- custom tool-selection policy
- custom batching or concurrency policy
- centralized logging or retries
- policy checks before execution

## 4. When To Switch Away

- MCP transport or schema registration -> `agently-mcp`
- multi-step business workflow with signals or resumes -> `agently-triggerflow-playbook`
- structured output or response streaming as the main problem -> `agently-output-control`
