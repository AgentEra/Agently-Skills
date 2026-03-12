---
name: agently-agent-extensions
description: Use when the main task is extending Agently agents with native extension surfaces such as tools, MCP, FastAPIHelper, `auto_func`, or `KeyWaiter`, rather than replacing them with custom wrappers first.
---

# Agently Agent Extensions

Use this skill when the problem is agent-side extension rather than prompt shape, output contract, or workflow control.

## Native-First Rules

- prefer built-in extension surfaces before handwritten wrappers
- keep extension choice explicit: tools, MCP, FastAPIHelper, `auto_func`, or `KeyWaiter`
- combine with `agently-model-response` or `agently-triggerflow` only when the scenario needs those layers

## Anti-Patterns

- do not build a parallel tool dispatcher before checking native tool and MCP support
- do not create a custom waiter or auto-function shim first

## Read Next

- `references/overview.md`
