# TriggerFlow Graph And Observation

Use this reference when the workflow design needs to stay inspectable in local DevTools, exported configs, or review artifacts.

## Why This Matters In v4.0.9

TriggerFlow execution metadata is now rich enough for graph-oriented debugging without inventing a second workflow description.

The practical outcome is:

- TriggerFlow executions can publish the workflow definition for graph rendering
- chunk runs carry trigger signal metadata such as `trigger_event`, `trigger_type`, and `signal_id`
- workflow stream and result events can preserve `origin_chunk` metadata

That means the same TriggerFlow design can power:

- execution graphs in DevTools
- runtime troubleshooting
- exported JSON or YAML flow configs
- Mermaid diagrams kept with project assets or review docs

## Design Rules

- keep business stages explicit as chunks or sub flows
- use stable chunk names that explain business intent, not temporary implementation details
- model UI-facing progress as workflow-owned stream events, not parser-path leaks
- let TriggerFlow remain the source of truth for stage order, branch shape, and sub-flow boundaries

If a graph or trace looks confusing, fix the workflow structure first instead of patching the visualization layer.

## Export And Reload

Prefer native TriggerFlow assets when the team needs reviewable workflow definitions:

- `flow.get_flow_config(...)`
- `flow.get_json_flow(...)`
- `flow.get_yaml_flow(...)`
- `flow.to_mermaid(...)`
- `flow.load_json_flow(...)`
- `flow.load_yaml_flow(...)`

Use these when:

- comparing workflow variants in code review or evaluation
- checking whether a refactor really simplified the flow shape
- handing a flow definition to a tooling layer without re-describing it manually

## Execution-State Debugging

Use native execution save and load when the workflow must pause, resume, or be debugged across process boundaries:

- `execution.save(...)`
- `execution.load(...)`

Keep runtime resources and flow structure separate:

- definition and state export are for workflow structure plus serializable execution state
- non-serializable resources should be injected back through runtime resources

## DevTools Relationship

When the user wants local visualization through `agently-devtools`, keep the responsibilities split:

- `agently-agent-extensions` owns attaching `ObservationBridge`, evaluation tooling, and the local console
- `agently-triggerflow` owns making the workflow readable, stable, and graph-friendly enough to observe well

Do not move workflow responsibility into DevTools. Make the TriggerFlow clearer.
