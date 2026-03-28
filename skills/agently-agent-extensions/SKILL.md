---
name: agently-agent-extensions
description: Use when the user wants tool use, MCP access, HTTP or streaming API exposure, auto-function helpers, wait-for-key behavior, or optional `agently-devtools` observation, evaluation, and playground integration through Agently-native extension surfaces rather than custom wrappers first.
---

# Agently Agent Extensions

Use this skill when the problem is agent-side extension rather than prompt shape, output contract, or workflow control.

## Native-First Rules

- prefer built-in extension surfaces before handwritten wrappers
- keep extension choice explicit: tools, MCP, FastAPIHelper, `auto_func`, `KeyWaiter`, or `agently-devtools`
- treat `agently-devtools` as an optional companion package installed from PyPI, not as a required source checkout
- keep observation or evaluation bridge wiring in the app layer through `Agently.event_center`
- combine with `agently-model-response` or `agently-triggerflow` only when the scenario needs those layers
- prefer built-in Browse support with Playwright or PyAutoGUI before writing browser or desktop-driving wrappers from scratch

## Anti-Patterns

- do not build a parallel tool dispatcher before checking native tool and MCP support
- do not create a custom waiter or auto-function shim first
- do not ask users to clone or editable-install DevTools when `pip install agently-devtools` is the supported public path
- do not build a custom runtime upload bridge before checking `ObservationBridge`

## Read Next

- `references/overview.md`
- `references/devtools.md`
