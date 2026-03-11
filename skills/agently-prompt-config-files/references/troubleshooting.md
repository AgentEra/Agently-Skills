# Troubleshooting

This page only covers prompt config files.

## 1. Mapping Did Not Apply

Check these first:

- whether the placeholder appears in a prompt key or prompt value that is written directly into prompt state
- whether the placeholder key exists in `mappings`
- whether the placeholder is inside `.alias` arguments

Important current behavior:

- `.alias` arguments are executed as written
- `${...}` mapping substitution is not applied to `.alias` arguments on the current path

## 2. Data Landed In The Wrong Prompt Layer

Check these first:

- whether the config used `.agent` or `.request`
- whether a top-level key started with `$`
- whether the key was intended to be persistent or one-request only

Reminder:

- top-level `$key` -> agent prompt
- top-level plain key -> request prompt

## 3. Nested Prompt Pack Did Not Load

Check these first:

- whether `prompt_key_path` points to the correct dictionary node
- whether the selected node is actually a dictionary prompt config
- whether the path exists in the parsed YAML / JSON structure

## 4. Exported Prompt Looks Different From The Original Template

This is expected if the original template relied on:

- `.alias`
- comments
- JSON5 formatting
- unresolved placeholders
- `.type` / `.desc` instead of `$type` / `$desc`

Export serializes resulting prompt state, not the original source authoring form.

## 5. JSON Prompt Did Not Load

Check these first:

- whether the top-level parsed value is a dictionary
- whether the JSON5 syntax is still structurally valid
- whether the user passed a non-existent file path that is also not valid JSON content

## 6. Prompt Config Was Used For The Wrong Kind Of State

Use another skill if the real task is:

- session snapshot export / restore
- flow-definition export / import
- TriggerFlow execution save / load
- provider, model, auth, proxy, or timeout setup
