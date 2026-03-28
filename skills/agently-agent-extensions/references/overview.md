# Overview

This skill owns Agently-native extension surfaces: tools, MCP, FastAPIHelper, `auto_func`, `KeyWaiter`, and optional `agently-devtools` integration.

Use it when:

- the user needs built-in tools such as `Browse`, including Playwright or PyAutoGUI-backed browsing paths
- the user wants MCP or FastAPIHelper without hand-rolled wrappers
- the user wants local observation, evaluation, playground, or logs support through `agently-devtools`
- the app owner layer is already known and the work is about attaching tooling around that app instead of redesigning the workflow itself

For the public DevTools integration path, read `references/devtools.md`.
