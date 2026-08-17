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

Real-world Skill scripts are resources, not trusted runtime handlers. After the
host binds an exact trusted revision into an `AgentExecution`, it may call
`agent.bind_skill_script_action(...)` with an explicit
`SkillScriptAuthorization`. That creates an ordinary Action which still uses
Action policy, a TaskWorkspace grant, and an ExecutionResource. Skill reading
itself never mounts or authorizes a script.

## Application Surface

- Select task files with `agent.use_task_workspace(...)`.
- Expose file work with `agent.enable_task_workspace_file_actions(...)` or
  `agent.enable_coding_agent_actions(...)`.
- Select durable record/recovery storage with `agent.use_record_store(...)`.
- Attach model-callable runtimes with `agent.enable_python(...)`,
  `agent.enable_shell(...)`, `agent.enable_nodejs(...)`,
  `agent.enable_code_runtime(...)`, `agent.enable_sqlite(...)`, or explicit
  `agent.use_actions(...)`.
- Pass explicit `root=` / `cwd=` only on file or shell surfaces that own those
  inputs. CodeExecution receives a TaskWorkspace grant instead of a provider
  cwd from model input.
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

Use the provider-neutral code execution Action with an ordered provider list and
a host-selected provisioning profile:

```python
agent.enable_code_runtime(
    language="go",
    providers=["docker"],
    isolation="required",
    provisioning_profile="developer",
)
```

The fixed execution chain is:

```text
TaskWorkspace
  -> issue scoped access grant
  -> bind selected code_execution provider
  -> materialize immutable code bundle
  -> execute trusted argv plan
  -> collect declared outputs into TaskWorkspace
  -> release provider and revoke grant
```

`TaskWorkspace` owns file containment and artifacts; it does not supply a
runtime or toolchain. `ExecutionResource` selects and manages the provider; it
is not renamed to Sandbox. Docker is the built-in isolated provider; the
optional `gvisor` provider uses Docker's registered `runsc` runtime. An explicit
`trusted_local` fallback is unsafe and may only be enabled by the host
with `unsafe_fallback=True` and non-required isolation. Never describe it as a
sandbox.

The public `isolation=` value is selection policy. Provider capability evidence
is a mapping of concrete boolean isolation axes: process containment,
host-filesystem restriction, privilege-escalation blocking, and syscall
restriction. Do not accept provider names or legacy strings such as
`"required"` as safety evidence. Preferred isolation searches all ordered
candidates for a full match before recording an explicit eligible fallback.

`agent.bind_skill_script_action(...)` registers its own narrow
`code_execution` requirement using the ordered
`code_execution.providers` setting. Do not call `enable_code_runtime(...)`
solely to execute that bound Skill script: doing so would expose an additional
general-purpose code Action. Use `enable_code_runtime(...)` only when the
application independently needs that broader capability.

Python 3.10+, Node.js 18+, Go 1.25+, and C++20 are the built-in adapter
contracts. Adapters build immutable files and trusted argv steps; providers
execute that plan without taking over language semantics. The model-visible
Action schema is `source_code`, optional `files`/`entrypoint`, bounded `args`,
and declared `expected_outputs`; it never accepts raw compiler, package-manager,
mount, sandbox-policy, or provider commands. Provider probes report observed
toolchain versions and safety/isolation facts, and those facts remain attached
to the Action result metadata for audit.

Use `agent.enable_python(sandbox="gvisor")` only when the host Docker daemon
has a working `runsc` runtime. This explicit selection verifies Docker, daemon
runtime registration, image availability under the host-selected policy, and a
bounded runsc container before it becomes ready. Missing, malformed,
unregistered, or non-executable runsc fails closed and never falls back to runc,
`auto`, or `trusted_local`; verified runtime facts remain in handle and Action
result metadata. gVisor does not add a default import dependency, and its name
does not upgrade unsafe Docker arguments into stronger safety claims.

On macOS, `agent.enable_python(sandbox="seatbelt")` selects only the optional
Seatbelt provider. Its SBPL profile denies network by default and derives all
writable paths from the TaskWorkspace grant; it accepts no raw SBPL or extra
host write roots and never falls back to Docker or `trusted_local`. The initial
toolchain-compatible profile permits broad host reads, so it truthfully reports
`host_filesystem_restricted=false` and uses preferred rather than required
isolation. Choose Docker/gVisor when host-read isolation is required.

On Linux, `agent.enable_python(sandbox="bubblewrap")` selects only the optional
Bubblewrap provider. It creates process and network namespaces by default,
mounts provider-owned system/toolchain roots read-only, and mounts TaskWorkspace
roots only according to their grants. It accepts no raw bwrap, bind, or tmpfs
arguments and never falls back to Docker or `trusted_local`. Bubblewrap does not
filter syscalls, so it reports `syscalls_restricted=false` and uses preferred
isolation. A host that blocks unprivileged namespaces fails closed; do not weaken
AppArmor or userns policy merely to make the provider available.

Expected outputs are bounded, normalized paths under `output/`; a missing
declared output fails the Action. Providers bound retained stdout/stderr, stop
their owned process or container on timeout/cancellation, and surface cleanup
failure instead of allowing false success.

Use install-capable shell only for explicitly trusted maintenance flows. There
is no universal full-trust switch; broaden commands and network/file access at
the owning provider while keeping isolation and roots explicit.

External sandbox contributions must implement the provider-neutral
`code_execution` contract and pass its conformance fixtures. A container-runtime
variant should subclass or compose `DockerExecutionResourceProvider` and
override `create_resource(...)`; this reuses the base provider's grant binding,
image, health, cleanup, and Workspace lifecycle while
`ExecutionResourceManager` retains ordered selection and ensure-time re-probe.
The contribution owns its mechanism-specific probe and command construction. A
host-policy sandbox implements an independent provider against the same grant,
bundle, and result contracts. Keep community PR ownership intact: guide
contributor branches to rebase and adapt; do not copy their provider
implementations into the framework base branch.

## Failure Behavior

- Missing/unhealthy required resources fail closed or enter an explicit
  approval/pending state according to policy.
- Dependency repair must run through controlled host/provider steps, not silent
  downgrade or model-visible package-manager improvisation.
- Provider selection follows the configured order and capability probes. A
  required-isolation request fails closed when no eligible provider is
  available; it never silently falls through to unsafe local execution.
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
