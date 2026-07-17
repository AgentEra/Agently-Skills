# Action and ExecutionResource Boundaries

Use this reference when deciding whether a capability is a callable Action, a
managed live dependency, a file boundary, or durable storage.

## Ownership

| Owner | Responsibility |
|---|---|
| `ActionRuntime` | Callable schema, model/host dispatch, policy, approval, bounded result, and Action evidence. |
| `ExecutionResource` | Lifecycle, scope, health, approval, and release for live clients, sandboxes, processes, browsers, databases, and MCP sessions. |
| `TaskWorkspace` | Contained task files, generated artifacts, file readback, and file identity. |
| `RecordStore` | Durable records, retrieval, RuntimeEvents, recovery snapshots/checkpoints, leases, and durable refs. |
| TriggerFlow `runtime_resources` | Execution-local attachment point for already-created live resources. |

Action executors must not secretly own long-lived MCP servers, browsers,
processes, or broad sandboxes. Declare/consume an ExecutionResource instead.
TriggerFlow can attach a live object but does not create, serialize, or release
it.

Search settings belong to the Search package/executor, not ExecutionResource.
Browse follows the same rule unless it explicitly consumes a managed browser.
Downloaded bytes may be materialized into TaskWorkspace; file handlers own
format parsing/rendering.

Real-world Skill scripts are resources, not trusted runtime handlers. A host may
map a script requirement to a controlled Action/ExecutionResource after policy
approval; Skill reading itself never mounts or authorizes it.

## Application Surface

- Select task files with `agent.use_task_workspace(...)`.
- Expose file work with `agent.enable_task_workspace_file_actions(...)` or
  `agent.enable_coding_agent_actions(...)`.
- Select durable record/recovery storage with `agent.use_record_store(...)`.
- Attach model-callable runtimes with `agent.enable_python(...)`,
  `agent.enable_shell(...)`, `agent.enable_nodejs(...)`,
  `agent.enable_code_runtime(...)`, `agent.enable_sqlite(...)`, or explicit
  `agent.use_actions(...)`.
- Pass explicit `root=` / `cwd=` when a runtime must not inherit the bound
  TaskWorkspace root.
- Use `desc_mode="override"` only when intentionally replacing default usage
  and safety guidance; ordinary `desc=` supplements it.

For host approval/webhook/queue transports, ExecutionResource may own the live
client, while TriggerFlow and ExecutionExchange own wait/resume. Attach the
provider as an execution resource and project public exchange views; do not make
the transport own workflow lifecycle.

## Permission Profiles

Choose the smallest surface that fits.

### Search Only

```python
from agently.builtins.actions import Search

search = Search(timeout=15, backend="auto")
agent.use_actions(search)
```

Do not add Browse or shell when web-result discovery is sufficient.

### Network Read

```python
from agently.builtins.actions import Browse, Search

agent.use_actions([
    Search(timeout=15, max_attempts=2),
    Browse(max_attempts=2, enable_playwright=True),
])
```

Keep Jina Reader/external service use, proxy, timeout, fallback order, and
backend policy explicit. Do not add a shell fallback merely for page reads.

### Task Files

```python
agent.use_task_workspace(repo_root, mode="read_write")
agent.enable_coding_agent_actions()
```

Use TaskWorkspace Actions for read/glob/grep/edit/patch/write. Use shell for
tests, builds, git inspection, and bounded diagnostics. Keep command roots and
allowlists narrow.

### Read-Only Shell

```python
agent.enable_shell(
    root=repo_root,
    commands=["pwd", "ls", "rg", "cat", "head", "tail"],
)
```

Do not include package managers, network commands, unsafe escape hatches, or
secret-bearing environment values in model-visible schemas. Visible metadata
may show env key names but must redact values.

### Code Runtime or Dependency Preparation

Prefer managed Docker-backed language runtimes with a host-selected provisioning
profile:

```python
agent.enable_code_runtime(
    language="go",
    provisioning_profile="developer",
)
```

Use install-capable shell only for explicitly trusted maintenance flows. There
is no universal full-trust switch; broaden commands and network/file access at
the owning provider while keeping isolation and roots explicit.

## Failure Behavior

- Missing/unhealthy required resources fail closed or enter an explicit
  approval/pending state according to policy.
- Dependency repair must run through controlled host/provider steps, not silent
  downgrade or model-visible package-manager improvisation.
- Multi-Action package registration is atomic: remove batch-created Actions and
  restore same-id host registrations on partial failure.
- Action results are bounded/redacted before they cross context, event, state,
  log, metadata, or public-return boundaries.
- Oversized bodies stay behind Action artifact, TaskWorkspace, or RecordStore
  refs and are read back under explicit scope.

## Anti-Patterns

- Treating SkillsExecutor/SkillLibrary as a capability or environment manager.
- Using TaskWorkspace for durable records or RecordStore for file editing.
- Passing live resources or secrets through save snapshots.
- Exposing broad shell because a narrower Action/managed runtime exists.
- Presenting provider/worker/thread counts as one universal TriggerFlow setting.
