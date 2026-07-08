# TaskDAG / Dynamic Task Overview

TaskDAG is the Agently DAG foundation capability. It owns graph data,
planning, validation, handler resolution, execution, dependency results,
semantic outputs, and runtime placeholders. Dynamic Task is the current
compatibility and convenience facade over that DAG substrate. It belongs above
Blocks and TriggerFlow conceptually:

```text
Agently.create_dynamic_task(...)
        |
        v
DynamicTask facade
        |
        +-- AgentlyTaskDAGPlanner
        +-- TaskDAGValidator
        +-- DynamicTaskResolver
        +-- TaskDAGExecutor
                |
                v
          Blocks ExecutionBlockGraph
                |
                v
          TriggerFlow execution substrate
```

Layer ownership:

- `TaskDAG` and `TaskDAGNode` are data contracts under `agently.types.data`;
  reviewed DAGs can be loaded with `TaskDAG.from_yaml(...)` or
  `TaskDAG.from_json(...)`.
- `AgentlyTaskDAGPlanner` is a plugin and owns planner output schema,
  `ensure_keys`, model instructions, and retry validation wiring.
- `TaskDAGValidator`, `TaskDAGResolver`, and `TaskDAGExecutor` are core
  runtime owners.
- `TaskDAGExecutor.compile_blocks(...)` and `async_run_blocks(...)` keep
  TaskDAG validation and semantic-output ownership in TaskDAG, then lower the
  validated segment through Blocks to TriggerFlow-backed execution and evidence.
- `Agently.create_dynamic_task(...)` is the app-facing facade entrypoint.
  `agent.create_dynamic_task(...)` is retained as a compatibility facade for
  legacy prompt-snapshot callers, not as default guidance.
  pending prompt. Explicit facade arguments override prompt-derived defaults.

Use TaskDAG modules when the graph is submitted as data and must be planned,
validated, pruned, customized, resolved to handlers, and executed. Use the
Dynamic Task facade when ordinary app code wants one compact compatibility
entrypoint. Use TriggerFlow directly when the developer owns a stable workflow
topology in code.

When a DAG is selected inside one long Agent-owned business task, keep the
outer handle as `agent.create_task(...)` or `agent.create_task_loop(...)`. Both
return task-strategy AgentExecution drafts; read final data, text, stream,
metadata, and task refs through AgentExecutionResult or the execution stream/meta
facade instead of introducing a separate public AgentTask handle.

The executor does not require an Agent instance. Agent or model-provider access
belongs to the facade, planner, model adapter, or resolver handler. That keeps
the core executor reusable for submitted local DAGs, model DAGs, action DAGs,
and Skills Manager context-pack integration.

TaskDAG node fallback can express bounded retry with
`fallback: {on_error: "retry", max_attempts: ..., backoff_base: ..., then: ...}`.
Keep this as a node-level execution policy: retry exhaustion should continue to
the terminal fallback such as `then: "skip"` or fail closed, and long-task
verification must still consume the DAG result as evidence instead of treating a
retried node as automatic task success.

When a submitted DAG needs Skill guidance, use the Skills Manager resolver
adapter instead of inventing a scheduler. Register
`Agently.skills_executor.task_dag_resolver()` with `TaskDAGExecutor` and model
that step as `kind: "skill"` with `inputs.skill_ids`, `inputs.task`,
`inputs.intent`, and optional include flags. The node result is an
`agently.skills.context_pack.v1` payload for downstream planner or model steps;
script Actionization and public lookup stay policy-gated by the host.

For model tasks, keep result control on the model task contract. Use
`inputs.output_schema` for the task result shape and `inputs.output_format` for
the response-control strategy: omit `inputs.output_format` to let the request
read `prompt.default_output_format` (global default `json`); use `json` for compact machine-control data,
standalone booleans/numbers, judges, dense all-typed arrays/objects, and strict extraction;
`xml_field` for flat string long text/code/HTML/Markdown fields; explicit
`hybrid` for long prose/code fields mixed with typed list/object/boolean/number
fields when retry latency is acceptable; explicit `flat_markdown` only for
legacy section-header compatibility; explicit `yaml_literal` only when
a YAML target document is intentionally desired; and `auto` only when structural
schema-driven selection and retry latency are acceptable after the target model
has passed representative stability checks.
If the host facade supplies `create_dynamic_task(..., output_schema=...,
ensure_keys=...)`, that semantic-output contract owns the frontstage shape. A
planner-chosen `inputs.output_format="flat_markdown"` must not break a
multi-field structured host contract; the framework coerces it back to `auto`.

Submitted DAG `inputs` support runtime placeholders for simple wiring:
`${INIT}` / `${INIT.foo}` read initial graph input,
`${DEPS.task_id.path}` reads dependency results, `${STATE...}` reads
execution-local state, and `${TRIGGER...}` reads the raw TriggerFlow trigger
payload.
Whole-string placeholders preserve the original value type; embedded
placeholders stringify into the surrounding text. Use placeholders for direct
references, and keep larger transformations in handlers or model tasks.
Use the same slot naming style as Prompt references: uppercase slot names in
examples (`INIT`, `DEPS`, `STATE`, `TRIGGER`), with path access after the dot.

When a submitted DAG runs through `create_dynamic_task(...)` or
`TaskDAGExecutor`, `${INIT...}` reads the submitted graph input owned by that
facade/executor. Use explicit graph input on the owning Dynamic Task or
TaskDAGExecutor path when it should differ from the task target or application
prompt context. Do not teach the old AgentExecution-local DynamicTask hook as
the current integration path; ordinary AgentExecution work is planned through
TaskGraph and ExecutionGraph.

When Dynamic Task needs streaming, consume the owning TriggerFlow runtime stream
from the compiled DynamicTask or TaskDAGExecutor execution. If a later
AgentExecution must consume the DAG result, pass the snapshot or Workspace
record as evidence; its stream and budget belong to that later AgentExecution
only.

Recommended API boundaries:

- app code: `Agently.create_dynamic_task(...)`
- planner control: `AgentlyTaskDAGPlanner`
- graph validation: `TaskDAGValidator`
- handler lookup: `DynamicTaskResolver`
- execution integration: `TaskDAGExecutor`
- Blocks lifecycle evidence: `TaskDAGExecutor.compile_blocks(...)` /
  `TaskDAGExecutor.async_run_blocks(...)`

For Skills Manager context work, use Dynamic Task as the DAG substrate rather than
placing Skill context construction under TriggerFlow directly. Skills Manager may
provide resolver handlers, context-pack adapters, or facade defaults, but the
public concept remains Dynamic Task.
