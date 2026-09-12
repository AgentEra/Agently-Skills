---
name: agently-runtime
description: "Use for Agently runtime extensions: AgentExecution plugins and final review/artifact policies, Actions and MCP, Shell/BashExecutor and PowerShell permissions, ExecutionResource lifecycle, TaskWorkspace, RecordStore, auto_func and KeyWaiter, FastAPIHelper, or optional DevTools observation."
---

# Agently Runtime

Use this Skill after the request or workflow owner is known. Use
`agently-triggerflow` when branching, concurrency, pause/resume, retry, or
multi-stage progression must remain visible in the execution graph. Use
`agently-stage` only for process-local lifetime and sync/async bridging.

## Read by Need

- Execution selection, nested producers, run/rework/control, final validate,
  artifact/review, or declared Agent capabilities:
  [agent-execution.md](references/agent-execution.md).
- Callable Actions, Search/Browse, MCP/ACP, policy, artifacts, or AgentTask
  evidence: [actions-runtime.md](references/actions-runtime.md).
- Action versus ExecutionResource, managed clients/sandboxes/processes/
  browsers/databases, Shell/BashExecutor, PowerShell, offline/online/host
  profiles, approval, and streaming process I/O:
  [actions-execution-resource.md](references/actions-execution-resource.md).
- `auto_func`, KeyWaiter, `FastAPIHelper`, SSE, or WebSocket exposure:
  [helpers-and-services.md](references/helpers-and-services.md).
- RuntimeEvent, logs, traces, evaluation, playground, or DevTools:
  [devtools.md](references/devtools.md).
- TaskContext, ContextReader, SkillLibrary, and real-world Skill packages:
  [context-and-skills.md](../agently/references/context-and-skills.md).

## Owner Boundaries

| Owner | Responsibility |
|---|---|
| `ActionRuntime` | Model-callable operation schema, planning/dispatch, policy, and Action results. |
| `ExecutionResource` | Lifecycle of live clients, sandboxes, processes, browsers, databases, and MCP sessions. |
| `TaskWorkspace` | One task's contained files, generated artifacts, readback, identity, and promotion. |
| `RecordStore` | Durable records, links, retrieval, RuntimeEvents, checkpoints, snapshots, leases, and durable refs. |
| `TaskContext` / `ContextReader` | Task information bindings and consumer-bound progressive disclosure. |
| `SkillLibrary` | Installed immutable Skill revisions and resource reads; never execution permission. |
| `AgentExecution` | One run's replaceable producer, task-scoped bindings, context, control, terminal policies, result and streams. |

Do not collapse these into a generic Workspace or runtime manager. File space
is not record storage; records are not model-hot context; a Skill package is
not an executor or permission grant.

## Runtime Rules

- Prefer `@agent.action_func` and `agent.use_actions(...)`. The `tool_*` and
  `use_tool(s)` names are compatibility surfaces.
- Treat Action ids and model-planned arguments as untrusted. Validate schema,
  authorization, and policy before dispatch; require recorded Action evidence
  for claimed side effects.
- Keep permission profiles explicit and narrow. Do not expose shell, network,
  browser, install, file-write, or MCP capabilities merely because an
  AgentTask exists.
- Use TaskWorkspace for contained file work and verified artifact readback; use
  RecordStore for durable records and recovery. Keep large bodies cold behind
  refs until an explicit consumer reads them.
- A real-world Skill supplies guidance and addressable resources. Actions,
  MCP, ExecutionResources, script authorization, and side-effect proof remain
  explicit host-owned bindings.
- Use a fresh `agent.create_execution()` for multi-statement setup or an
  unrelated new request. A completed revision is immutable; explicit producer
  rework advances the same execution while old result readers retain their
  revision. See the execution contract above.
- In 4.1.4.8, select `request`, `plan`, `long_content`, or `long_task` through
  `create_execution(...)`. Final `.validate(handler)` is a hard output gate;
  `.review(..., on_fail="warn" | "block")` is a soft assessment with an explicit
  terminal policy. Review does not silently rework; rework belongs to the
  producer. `.artifact(...)` requires verified TaskWorkspace readback.
- Use `agent.create_task(...)` only when the model should own bounded planning,
  execution evidence, verification, and replan. `create_task_loop(...)` is a
  compatibility spelling, not the recommended surface. Stable application
  orchestration belongs to TriggerFlow.
- Persist resource descriptors, never live clients or secrets. Reconstruct
  resources through their provider/resolver during recovery.
- Bind RuntimeEvent persistence explicitly. Availability of a RecordStore does
  not turn every observation into a durable event archive.
- Observation and transport are adapters: they must not become owners of
  routing, authorization, workflow lifecycle, semantic acceptance, or retry.

## Fail Closed

Reject unknown Skill revisions, resource refs, Action ids, selection keys,
context block keys, recovery providers, and external-resume identities. Offer
models one short host-issued selection key, validate it against the offered
set, then reconstruct canonical records in host code.

Do not use keyword or regex matching as the semantic owner for intent, Skill
relevance, route choice, evidence usefulness, or output quality. Do not fake
model-owned success with canned outputs or deterministic business mappings.
