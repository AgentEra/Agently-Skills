# Troubleshooting

This page only covers TriggerFlow config issues.

## 1. The Restored Flow Loads But Cannot Run

Most common cause:

- required handlers were not registered before loading

Check:

- whether chunk handlers were registered
- whether condition handlers were registered

## 2. Runtime Resources Disappear After Export And Import

This is expected.

Runtime resources are not part of portable flow config.

Fix:

- inject them again at flow or execution runtime

## 3. Mermaid Looks Fine But `get_flow_config()` Fails

Most common cause:

- the definition contains a non-serializable callable such as a lambda

Fix:

- replace the lambda with a named registered handler

## 4. Loaded JSON Or YAML Content Fails To Parse

Check:

- whether the content is valid JSON or YAML
- whether the content is a dictionary-shaped flow config
- whether the provided string was intended to be inline content or a file path

## 5. Config Persistence Is Expected To Resume A Running Workflow

This is the wrong skill boundary.

Flow config restores the workflow definition only.

Running execution state belongs in a separate execution-state skill.
