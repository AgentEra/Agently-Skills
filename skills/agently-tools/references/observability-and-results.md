# Observability And Results

Use this page when the request is about what Agently keeps after tool use.

## 1. Tool Logs In Response Metadata

After a tool-enabled request completes, Agently stores tool execution records in response metadata.

The most direct inspection path is:

- `response.result.full_result_data["extra"]["tool_logs"]`

Use this when the application needs:

- auditing
- debugging
- UI trace display
- post-request analytics

## 2. Tool Results Feed Back Into The Same Request

During the loop, tool results are converted into action results and injected back into the request so the model can continue planning or answer directly.

In practice this means:

- tool outputs belong to the same request cycle
- the final answer can reflect tool outputs immediately
- the trace is easier to inspect from one response snapshot

## 3. Runtime Logging

Agently can also surface tool logs during the request lifecycle.

Use explicit response inspection for reliable programmatic handling. Treat console-style logging as supplemental.
