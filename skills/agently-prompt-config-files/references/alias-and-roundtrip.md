# Alias And Roundtrip

This page covers `.alias` and prompt export / restore.

## 1. `.alias` Executes Methods During Load

`.alias` lets the config call methods on the agent while the prompt file is being loaded.

Current structure:

- alias name -> method name
- `.args` -> positional arguments
- remaining keys -> keyword arguments

Example:

```yaml
.alias:
  set_request_prompt:
    .args:
      - instruct
      - Reply politely.
```

This is best used for:

- concise prompt-building steps
- keeping a config file close to code-based prompt composition

Keep it predictable. If `.alias` becomes complex business logic, the config stops being readable prompt data.

## 2. `.alias` Is Not Preserved By Export

`get_yaml_prompt()` and `get_json_prompt()` export current prompt state, not the original prompt template source.

That means export keeps:

- `.agent`
- `.request`

And export does not keep:

- `.alias`
- comments
- formatting style
- the original `prompt_key_path`
- unresolved placeholder templates

This is expected, because `.alias` is executed during load and only its resulting prompt state remains.

## 3. Save-To Behavior

Both export methods:

- return the serialized content as a string
- optionally write the same content to `save_to=...`

That is useful when prompt state must be:

- checked into a repo
- cached after generation
- shipped to another service

## 4. Roundtrip Meaning

Roundtrip in this context means:

1. build prompt state in code or load it from config
2. export it to YAML / JSON
3. load that exported content into another agent
4. recover the same prompt state

Roundtrip does not mean preserving the exact source authoring style of the original template.

## 5. Output Schema Roundtrip

When output schema is present:

- config may use `$type` / `$desc` or `.type` / `.desc`
- exported content is normalized to `$type` / `$desc`
- reloaded prompt state still produces the same output model fields
