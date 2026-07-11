---
name: agently-dynamic-task
description: Use when the user needs Agently TaskDAG / Dynamic Task, model-generated or app-submitted DAG planning, TaskDAG validation, TaskDAGResolver handlers, TaskDAGExecutor execution, or the Agently.create_dynamic_task compatibility facade. TaskDAG is the DAG foundation capability; Dynamic Task is the convenience facade over it and uses TriggerFlow as the execution substrate.
---

# Agently Dynamic Task

Use this skill when the problem is a dynamic task graph: a model or application
submits DAG data that must be planned, validated, pruned, resolved to handlers,
and executed.

TaskDAG is the Agently DAG foundation capability. Dynamic Task is the current
compatibility and convenience facade over TaskDAG planning and execution, not a
TriggerFlow sub-API and not the strategic Agent task lifecycle. TriggerFlow is
the execution substrate under `TaskDAGExecutor`, while
`Agently.create_dynamic_task(...)` is the current app-facing facade entrypoint;
`agent.create_dynamic_task(...)` remains a compatibility facade for legacy
prompt-snapshot callers, not the default guidance.

When lower-level evidence or runtime visualization matters, use
`TaskDAGExecutor.compile_blocks(...)` or `async_run_blocks(...)`: TaskDAG still
owns graph validation, dependency semantics, and semantic outputs; Blocks only
lowers the validated DAG segment into a TriggerFlow-backed
`ExecutionBlockGraph` and maps EvidenceEnvelope/ResultAdapter output.
The default `TaskDAGExecutor.async_run(...)` path does not pass through Blocks;
it compiles the validated DAG directly to TriggerFlow.

## Native-First Rules

- use `Agently.create_dynamic_task(...)` when ordinary app code wants the compact facade
- when a DAG is one phase inside a broader business task, run the DAG
  independently and pass its snapshot to AgentExecution as evidence; do not
  expose DynamicTask as an AgentExecution route candidate or turn the Dynamic
  Task facade into the long-running AgentTask lifecycle owner
- split into `AgentlyTaskDAGPlanner`, `TaskDAGValidator`, `TaskDAGResolver`, and `TaskDAGExecutor` only when staged control is required
- use `TaskDAGExecutor.compile_blocks(...)` or `async_run_blocks(...)` when the
  caller needs the Blocks lifecycle evidence path; do not bypass
  `TaskDAGValidator` or treat Blocks as the DAG owner
- use `plan=<TaskDAG>` when the caller already owns the DAG and should skip model planning
- use `TaskDAG.from_yaml(...)` or `TaskDAG.from_json(...)` when the submitted DAG is a reviewed config artifact
- use submitted DAG `inputs` placeholders for small runtime wiring:
  `${INIT}` / `${INIT.foo}` for initial graph input,
  `${DEPS.task_id.path}` for dependency results, `${STATE...}` for
  execution-local state, and `${TRIGGER...}` for the raw TriggerFlow trigger
  payload. Slot names are case-insensitive, but examples should use uppercase.
  Whole-string placeholders preserve the original value type; embedded
  placeholders stringify into the surrounding text. Missing runtime paths fail
  closed during execution
- when a submitted DAG runs through `create_dynamic_task(...)` or
  `TaskDAGExecutor`, keep `${INIT...}` wired to the submitted graph input owned
  by that facade/executor. Do not use the old AgentExecution-local DynamicTask
  hook in new examples; AgentExecution plans ordinary work through TaskGraph and
  ExecutionGraph.
- use `planner=<agent-or-provider-settings>` when the model must generate the DAG
- use `model=<agent-or-provider-settings>` for model task execution resources
- use `handlers={"risk_check_handler": handler}` for local/custom tasks; handler names should be explicit and usually end in `_handler`
- pass `actions=...` or `skills=...` only when the planner should be allowed to use those task kinds; do not expose them by default
- use Agently output schemas for model-owned semantic outputs instead of parsing model text with example-local JSON/code-block parsers
- keep backend business-system calls mockable in examples, but keep model-owned planning, classification, drafting, evaluation, revising, and final response generation model-driven
- require each model task that matters to have a clear output schema, either through facade-level `output_schema` or node-level `inputs.output_schema`
- set model-task `inputs.output_format` by result type when the plan is
  generated or submitted: omit it to let the request read
  `prompt.default_output_format` (global default `json`); use `json` for compact machine-control data, action
  arguments, routing flags, standalone booleans/numbers, strict extraction,
  model judges, and dense all-typed arrays/objects; `xml_field` for flat string long
  text/code/HTML/SVG/Markdown/SQL/templates; explicit `hybrid` for long
  prose/code fields mixed with typed list/object/boolean/number fields when
  retry latency is acceptable; explicit `flat_markdown` only for legacy
  section-header compatibility; explicit `yaml_literal` only
  when a YAML target document is intentionally desired; `auto` only when
  structural schema-driven selection and retry latency are acceptable after the
  target model has passed representative stability checks. qwen2.5:7b checks
  found hybrid can omit section headers or echo old scaffold comments into text
  fields
- let `TaskDAGValidator` reject duplicate ids, missing dependencies, cycles, unsupported required task kinds, schema-version mismatches, unsafe side-effect policy, and unknown required handlers before execution
- allow unknown optional handlers to be pruned only when they do not affect required semantic outputs, required downstream nodes, approvals, or side-effect policy
- keep generated plan data in execution input or execution state; do not use shared TriggerFlow flow data for per-run DAG state
- use `${INIT...}` / `${DEPS...}` placeholders for small declarative input
  wiring; for larger transformations, keep the logic in a handler or model task
- do not teach planners to use internal resolver entries such as `validate` or `emit` as ordinary task kinds
- do not mark ordinary read-only model tasks as network side effects just because they call an LLM provider
- do not add approval gates to analysis, synthesis, drafting, or final response model tasks unless the user explicitly asks for approval

## API Shape

Submitted DAG:

```python
from agently import Agently

async def risk_check_handler(context):
    return {
        "task_id": context.task.id,
        "deps": dict(context.dependency_results),
    }

task = Agently.create_dynamic_task(
    target="review policy",
    plan={
        "graph_id": "review",
        "task_schema_version": "task_dag/v1",
        "tasks": [
            {"id": "extract", "kind": "local", "binding": "risk_check_handler"},
            {
                "id": "final",
                "kind": "local",
                "binding": "risk_check_handler",
                "depends_on": ["extract"],
                "inputs": {
                    "source": "${INIT}",
                    "extract_result": "${DEPS.extract}",
                },
            },
        ],
        "semantic_outputs": {"final": "final"},
    },
    handlers={"risk_check_handler": risk_check_handler},
)

snapshot = await task.async_start(timeout=10)
result = snapshot["semantic_outputs"]["final"]
```

Config-backed submitted DAG:

```python
from agently import Agently
from agently.core import TaskDAG

graph = TaskDAG.from_yaml("plans/review.yaml")
task = Agently.create_dynamic_task(
    target="review policy",
    plan=graph,
    handlers={"risk_check_handler": risk_check_handler},
)
snapshot = await task.async_run(graph_input={"doc": "policy"}, timeout=10)
```

Use `TaskDAG.from_json(...)` for JSON/JSON5 files or raw content. Both loaders
support `task_dag_key_path="plans.review"` for selecting one DAG from a larger
config. Use `graph.get_yaml(path)` or `graph.get_json(path)` to export a
normalized graph.

Auto-planned DAG:

```python
from agently import Agently

task = Agently.create_dynamic_task(
    target=user_goal,
    planner=planner_agent,
    model=worker_agent,
    output_schema={
        "answer": (str, "final user-facing answer", True),
    },
)

graph = await task.async_plan(max_retries=3)
task.validate(graph, strict_schema_version=True)
snapshot = await task.async_run(graph_input={"goal": user_goal}, timeout=30)
```

Lower-level integration:

```python
from agently.builtins.plugins import AgentlyTaskDAGPlanner
from agently.core import TaskDAGExecutor, TaskDAGResolver, TaskDAGValidator

resolver = TaskDAGResolver({"risk_check_handler": risk_check_handler})
validator = TaskDAGValidator(resolver)
planner = AgentlyTaskDAGPlanner(validator=validator)

graph = await planner.async_plan(planner_agent, {"target": "review policy"})
validation = validator.validate(graph, strict_schema_version=True)
snapshot = await TaskDAGExecutor(resolver, validator=validator).async_run(graph)
```

## Planner Constraints

Planner plugins and planner prompts must declare:

- task schema version, normally `task_dag/v1`
- allowed task kinds and available binding names
- required semantic output leaves
- maximum task count when the scenario has a practical limit
- validation checks that become retryable model-output failures
- forbidden behavior: unstable task ids, dependency results embedded in static task inputs, implicit side effects, hidden action/skill use, and internal resolver task kinds

The facade planner should wire `.output(planner.output_schema(), format="json")`, required
`planner.ensure_keys()`, and `.validate(planner.validate_output)` so structural
problems become model-output validation failures before execution. Compile/run
still revalidates the graph.

Layer ownership:

- `TaskDAG` / `TaskDAGNode` data contracts and YAML/JSON graph config belong to `agently.types.data`
- `TaskDAGExecutor`, `TaskDAGValidator`, and `TaskDAGResolver` belong to core
- `AgentlyTaskDAGPlanner` owns planner output schema, ensure keys, and planner instructions as a plugin concern
- `Agently.create_dynamic_task(...)` is the app-facing facade entrypoint;
  `agent.create_dynamic_task(...)` is compatibility-only guidance

## Anti-Patterns

- do not put Dynamic Task guidance under TriggerFlow as if it were TriggerFlow syntax
- do not hand-roll a scheduler for submitted DAG data
- do not parse model text with `json.loads(...)`, regex marker splits, or code-block extraction when Agently output schemas can own the shape
- do not expose `actions` or `skills` to the planner by default
- do not hide model-owned classification, drafting, quality checks, or final response generation behind deterministic local substitutes in recommended examples
- do not call low-level `TaskDAGExecutor` from ordinary app code when `Agently.create_dynamic_task(...)` is enough
- do not describe Blocks as mandatory for TaskDAG execution; the ordinary
  `async_run(...)` path is direct, while Blocks requires explicit
  `compile_blocks(...)` / `async_run_blocks(...)`
- do not use vague handler names such as `risk_check`; use `risk_check_handler` or another name that describes the callable role
- do not duplicate TriggerFlow docs here; explain only that Dynamic Task compiles to TriggerFlow internally

## Read Next

- `references/overview.md`
- `examples/minimal.py`
