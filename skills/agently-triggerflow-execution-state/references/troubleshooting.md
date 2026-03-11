# Troubleshooting

This page only covers TriggerFlow execution-state issues.

## 1. The Restored Execution Cannot Continue

Most common causes:

- missing runtime resources
- wrong flow definition loaded before restore

Check:

- whether required resources were reinjected
- whether the restored execution belongs to the correct flow shape

## 2. The Result Is Missing After Restore

Most common cause:

- the saved execution was not result-ready yet

Check:

- whether the execution should be continued
- whether it was waiting on an interrupt or event

## 3. Runtime Resources Seem To Disappear

This is expected.

Execution state saves resource key names, not resource objects.

## 4. Loading Content Fails

Check:

- whether the input is dict, valid JSON/YAML string, or an existing file path
- whether the content shape is a dictionary execution state

## 5. The Caller Expects `load(...)` To Restore The Definition Too

This is the wrong boundary.

Execution-state restore does not replace flow-definition restore.

Use `agently-triggerflow-config` for definition export/import.
