# TaskDAG: Advanced Submitted-Graph Guidance

TaskDAG is a low-frequency foundation for acyclic plan data submitted by a
model or application. It is not the default shape for Agent work and not a
second stable workflow DSL.

Use it only when the graph itself is runtime data that must be validated,
resolved to allowed handlers, and executed. Use TriggerFlow directly when
trusted source code owns a stable topology. Use `agent.create_task(...)` when
one Agent owns a long task's planning, evidence, verification, and repair.

## Current Ownership

- `TaskDAG` and `TaskDAGNode` own submitted graph data.
- `TaskDAGValidator` owns graph validation and pruning decisions.
- `TaskDAGResolver` binds allowed task kinds to handlers.
- `TaskDAGExecutor` owns validated DAG execution and semantic-output snapshots.
- `AgentlyTaskDAGPlanner` is an optional model planner plugin.
- `DynamicTask` is a convenience/compatibility facade over these owners.
- TriggerFlow is the execution substrate. It does not become the submitted DAG
  data owner.

Ordinary application code may use `Agently.create_dynamic_task(...)` when the
facade is genuinely simpler. `agent.create_dynamic_task(...)` is a compatibility
entry tied to the Agent prompt snapshot; do not make it the default. The removed
`use_dynamic_task(...)` Agent/AgentExecution route must not be taught.

## Decision Gate

Before introducing TaskDAG, require all of the following:

1. the topology is submitted or generated data rather than stable source code;
2. acyclic dependency semantics are sufficient;
3. allowed task kinds and handler bindings are explicit;
4. required semantic-output leaves are known;
5. validation and side-effect policy can fail closed before execution.

Otherwise prefer a direct ModelRequest/AgentExecution or an explicit
TriggerFlow definition.

## Execution Rules

- Validate duplicate ids, missing dependencies, cycles, required bindings,
  semantic-output leaves, and side-effect policy before execution.
- When schema-version equality is a requirement, call validation with
  `strict_schema_version=True`; the executor's ordinary validation is not a
  substitute for that explicit strict gate.
- Use `${INIT...}`, `${DEPS.task_id...}`, `${STATE...}`, and `${TRIGGER...}`
  only for small declarative value wiring. Keep larger transformations in an
  owned handler or model task.
- Whole-string placeholders preserve value types; embedded placeholders render
  text. Missing required paths fail closed.
- Expose Actions or Skill-backed task kinds only when the host explicitly
  authorizes them. Never make their availability a planner default.
- Give model task nodes explicit output contracts. Do not parse fenced JSON or
  use regex extraction when Agently output control can own the shape.
- Keep graph input and per-run state execution-local; do not use shared
  TriggerFlow `flow_data` as DAG-run memory.

`TaskDAGExecutor.async_run(...)` is the normal direct path from validated data
to TriggerFlow. `compile_blocks(...)` and `async_run_blocks(...)` are optional
lower-level carriers when Blocks lifecycle evidence or an
`ExecutionBlockGraph` is explicitly required; Blocks is not the DAG owner.

## Known 4.1.4.7+ Integration Gap

Do not recommend registering `Agently.skills_executor.task_dag_resolver()`
directly with `TaskDAGExecutor` as a proven Skill-task path. In the 4.1.4.7
release, the compatibility helper expects mapping-shaped input while the real
executor passes `TaskDAGContext`, so node
selectors are not transferred correctly. Treat this as a framework capability
gap until the adapter and a real executor integration test are fixed; reverify
the limitation before carrying it into a later Agently release line.

Do not hide the gap behind a scenario-specific adapter in recommended guidance.
If the task requires first-class Skill-backed DAG nodes, report the missing seam
and keep the rest of the DAG capability claim scoped to supported handlers.
