# Structure And Routing

Prompt config is routed by top-level keys.

## 1. Three Explicit Control Sections

### `.agent`

Writes into agent-level prompt state.

Use it for:

- persistent `system`
- persistent `info`
- persistent `instruct`
- persistent `output`

Shortcut:

- if `.agent` is a scalar instead of a dictionary, it is treated as `system`

### `.request`

Writes into request-level prompt state.

Use it for:

- one-request `input`
- one-request `info`
- one-request `instruct`
- one-request `output`

Shortcut:

- if `.request` is a scalar instead of a dictionary, it is treated as `input`

### `.alias`

Executes agent methods by name while the config is loading.

This is not pure prompt data. It is an imperative hook.

## 2. Top-Level Shorthand

When the top-level key is not one of `.agent`, `.request`, or `.alias`, current routing works like this:

- top-level keys that start with `$` but not `${...}` route to agent prompt after removing one leading `$`
- other top-level keys route to request prompt

Examples:

- `$extra_info` -> agent prompt key `extra_info`
- `extra_request_info` -> request prompt key `extra_request_info`

This matters when a config mixes explicit `.agent` / `.request` blocks with shorthand keys.

## 3. Output Schema In Config Files

Prompt config can describe `output` using the same structure as `.output(...)`, but in serialized form.

Accepted type-description keys in config:

- `$type` and `$desc`
- `.type` and `.desc`

Current export behavior:

- exported YAML / JSON normalizes these fields to `$type` and `$desc`

## 4. What This Skill Is Really For

Use prompt config when:

- prompt structure should be managed as data
- prompt templates should live in files, config stores, or CMS-like systems
- business code should inject mappings into a shared prompt template

Do not treat prompt config as session state or workflow state. Those are different objects with different lifecycles.
