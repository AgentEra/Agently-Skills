# Overview

This skill owns prompt slots, `input(...)`, `instruct(...)`, `info(...)`, prompt config, YAML-backed prompt structure, recursive placeholder mappings, and config-file bridges for request-side behavior.

Use it when:

- prompt files should keep `${topic}`, `${language}`, `${column_title}`, or similar variables and receive values through `mappings`
- one request family needs stable `input`, `info`, `instruct`, and `output` contracts outside Python code
- frontend or product teams need to edit request-side behavior through config files without rewriting workflow code

Do not use it to store workflow state or provider settings.
