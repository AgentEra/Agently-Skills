# Mappings And Serialization

Agently prompt data supports both placeholder substitution and nested serializable structures.

## 1. Placeholder Mappings

Most prompt mutation APIs accept `mappings=...`.

Common entry points:

- `set_agent_prompt(...)`
- `set_request_prompt(...)`
- quick prompt methods such as `input(...)` and `info(...)`
- lower-level prompt mutation methods such as `Prompt.set(...)`, `Prompt.update(...)`, and `Prompt.append(...)`

Placeholder syntax:

- `${name}`

## 2. What Gets Replaced

Placeholder substitution is recursive.

It applies to:

- string values
- mapping keys
- nested dictionaries
- list items
- tuple items

## 3. Full Placeholder Versus Partial Placeholder

If a string is exactly one placeholder, Agently can replace it with a non-string value.

Example outcome:

- `"${profile}"` can become a dictionary

If a placeholder is only part of a larger string, the result is rendered as text.

Example outcome:

- `"Hello ${name}"` becomes `"Hello Alice"`

## 4. Serializable Prompt Data

Agently accepts nested serializable data in prompt slots.

Common patterns:

- lists in `input`
- dictionaries in `info`
- nested structures in `examples`
- named custom extra keys for structured context

This is a normal part of prompt composition, not a workaround.

## 5. Custom Extra Prompt Keys

When the prompt contains keys outside the standard slot list, Agently keeps them as extra prompt sections.

Practical use:

- add named blocks such as `project_context`, `rubric`, or `user_profile`
- keep structured context separate from the main `info` block when that reads more clearly

## 6. Boundary With Prompt File Management

Serializable prompt data and placeholder mappings belong in this skill.

Full YAML or JSON prompt import/export workflows do not. Those belong to a separate prompt-management concern.
