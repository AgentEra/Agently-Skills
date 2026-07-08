# ExecutionResource Overview

This skill owns Agently-native extension surfaces: Action Runtime, ExecutionResource, built-in capability Actions, Agent Components, tools, MCP, FastAPIHelper, `auto_func`, `KeyWaiter`, and optional `agently-devtools` observation/evaluation tooling.

Use it when:

- the user needs built-in actions or tools such as `Browse`, including `@agent.action_func`, `agent.use_actions(...)`, MCP, or sandbox-backed execution
- the user wants MCP or FastAPIHelper without hand-rolled wrappers
- the user needs managed MCP, Bash, Python, Node.js, Docker, Browser, or SQLite lifecycle through the ExecutionResource compatibility surface
- the user is deciding whether a capability belongs in core, a plugin/provider, a built-in Action, or an Agent Component
- the user wants local observation, evaluation, playground, or logs support through `agently-devtools`
- the app owner layer is already known and the work is about attaching tooling around that app instead of redesigning the workflow itself

For the public DevTools integration path, read `references/devtools.md`.

## ExecutionResource Boundary

Use ExecutionResource when a capability needs a managed live dependency before
an Action or TriggerFlow execution can run.

- ExecutionResource owns lifecycle, policy, approval, scope, health, and release for managed dependencies.
- Action owns what is callable and how one call is normalized into an `ActionResult`.
- TriggerFlow `runtime_resources` remains the execution-local live handle surface. Managed resources can be injected there, but TriggerFlow does not create or release them.
- Built-in MCP, Bash, Python, Node.js, Docker, Browser, and SQLite actions should declare or consume ExecutionResource resources rather than owning lifecycle inside the executor.
- Search does not belong in ExecutionResource. Its proxy, timeout, backend,
  retry, and region settings belong to the Search package/executor
  configuration. Browse follows the same package-owned proxy/timeout/retry
  pattern unless it explicitly declares a managed browser resource. Browse may
  consume the bound Workspace to materialize remote PDF/Office/image/download
  bytes, but Workspace still owns the file boundary and file IO handlers own
  parsing.
- SkillsManager and artifact-producing workflows should repair missing local
  libraries, binaries, browser runtimes, or MCP packages through controlled
  install-capable Actions or ExecutionResource ensure steps. Do not silently
  downgrade the business result just because a local dependency is absent; if
  repair is blocked or fails, surface an explicit failed or approval-required
  execution state with the dependency ActionResult attached.
- Third-party Skill helper scripts are not trusted runtime handlers by default.
  The executor should first resolve the capability to a controlled Action or
  managed environment. Bash/shell-style requirements may be satisfied by a
  policy-bound Bash sandbox; if no controlled replacement exists, return a
  user-facing blocked explanation and remediation suggestions.

Audience split:

- App developers should use `agent.use_workspace(...)` when the application
  needs durable multi-turn task records, artifacts, search, links, and compact
  checkpoints. Use built-in Actions and Agent Components such as
  `agent.enable_python(...)`, `agent.enable_shell(...)`,
  `agent.enable_workspace_file_actions(...)`,
  `agent.enable_coding_agent_actions(...)`, `agent.enable_nodejs(...)`, and
  `agent.enable_sqlite(...)` for model-callable execution capabilities.
- When a Foundation Workspace is configured, filesystem-like helpers inherit
  `agent.workspace.files_root`, the editable file working tree, by default.
  Pass explicit `root=` / `cwd=` when an action must use an independent
  directory.
- For explicit long-running or looping workflows, keep TriggerFlow state compact
  and persist structured observations, decisions, links, and checkpoints in
  Workspace. Recover them through `workspace.get_data(...)`,
  `workspace.links(...)`, and checkpoint lookup APIs.
- For coding-agent style local file work, expose Workspace file actions through
  `agent.enable_coding_agent_actions(...)` instead of broad shell. Keep shell
  scoped to tests, builds, git status/diff/log inspection, and read-only
  diagnostics; command outputs are bounded and oversized streams should remain
  behind Workspace file/artifact refs.
- Action developers can use the ExecutionResource requirement surface when one action requires a managed dependency.
- Plugin developers implement `ExecutionResourceProvider` for resource kinds such as Bash, Python, Node.js, Docker, SQLite, vector store, browser, or remote runner.
- Framework maintainers decide whether a feature belongs to core, provider, built-in capability, or Agent Component.
- `enable_*` helper `desc=` parameters supplement default capability descriptions by default. Use `desc_mode="override"` only when replacing baseline usage and safety guidance is intentional.
- Public helper APIs should use explicit typing for IDE assistance. Prefer `Literal` for finite option sets, including `desc_mode`.

For human approval or external exchange transports, ExecutionResource may own a
live client or queue handle, but the wait/resume protocol belongs to TriggerFlow
and ExecutionExchange. Bind the live transport as
`runtime_resources={"execution_exchange_provider": provider}` or register a
reusable provider through `agently.base.execution_exchange.register_provider(...)`.
Host UIs should render `ExecutionExchangeView` data from
`project_pending_exchanges(execution)` / `project_execution_exchanges(execution)`;
connected ActionFlow/PolicyApproval service endpoints may resolve the same live
run with `execution_exchange.async_respond(...)`.

Do not design custom ActionExecutors that secretly start long-lived MCP servers,
processes, or broad sandboxes when the environment can be declared and managed
through ExecutionResource.

For runnable main-repo examples, check the current execution-resource examples.
Start with the trusted-local `agent.enable_python(..., sandbox="trusted_local")`
quickstart when no Docker service is available, then use the Docker-backed
Ollama/DeepSeek and common-language code runtime examples. The TriggerFlow
example is for workflow or framework developers who need managed
execution-local resources.
For built-in Search/Browse package examples, check `examples/builtin_actions/`.

Do not turn Skills into a parallel executor. Skill scripts should map to built-in
Actions and component helpers such as `agent.enable_python(...)`,
`agent.enable_shell(...)`, `agent.enable_nodejs(...)`,
`agent.enable_code_runtime(...)`, and `agent.enable_sqlite(...)`; Python,
shell, Node.js, and common-language code runtime helpers use Docker-backed
runtime profiles, while dependency installation remains host/provider resource
preparation rather than model-visible package-manager commands. MCP assets
should map to
MCP-backed Actions plus ExecutionResource requirements; workflow templates
should map to TriggerFlow. Multi-step Skills strategies should reuse
TriggerFlow for orchestration and ActionFlow/ActionRuntime for tool/action
execution, including approval-required and blocked results.

## Practical Permission Profiles

Choose the smallest surface that still fits the task. The current codebase supports these patterns directly:

### Search Only

Use `Search` when the task is only to discover web results and you do not need page rendering or local shell access.

```python
import asyncio

from agently.builtins.actions import Search

search = Search(timeout=15, backend="auto")

async def main():
    results = await search.search("agently action runtime sandbox")
    return results

results = asyncio.run(main())
```

Keep the agent on `agent.use_actions(search)` when the model may choose any
Search action, or call `search.search(...)` directly when no agent loop is
needed. Do not add `Browse` or any sandbox executor if the job is just retrieval.
When a configured search backend fails but a fallback backend returns usable
results, the Action result is `status="partial_success"` with `success=True`
and backend diagnostics; treat that as usable evidence plus degraded-provider
observability.

### Local Files Only

Use Bash sandbox actions with a tight command allowlist and a root-scoped workspace.

```python
agent.action.register_bash_sandbox_action(
    action_id="repo_reader",
    allowed_cmd_prefixes=["pwd", "ls", "rg", "cat", "head", "tail"],
    allowed_workdir_roots=[repo_root],
    default_policy={
        "workspace_roots": [repo_root],
        "allowed_cmd_prefixes": ["pwd", "ls", "rg", "cat", "head", "tail"],
        "timeout_seconds": 10,
    },
)
```

This is the right profile for “read local files only” or “search the repo tree”.
Keep shell bypass grants host-only; do not include `allow_unsafe` or equivalent
escape hatches in model-visible schemas, and do not include `curl`, `wget`,
`pip`, `uv`, or `poetry` in read-only profiles. If the host passes `env=...` to
a managed action helper, those raw values are for the execution provider only;
visible action metadata should redact env values while preserving key names.

### Network Read Only

Use `Search` plus `Browse` when the task needs internet access but should not mutate the machine.

```python
import os

from agently.builtins.actions import Browse, Search

search = Search(proxy=os.getenv("BROWSE_PROXY"), timeout=15, max_attempts=2)
disable_jina_reader = os.getenv("BROWSE_DISABLE_JINA_READER", "0").lower() in {"1", "true", "yes"}
jina_reader_endpoint = os.getenv("BROWSE_JINA_READER_ENDPOINT", "https://r.jina.ai/")
fallback_order = (
    ("playwright", "bs4", "curl") if disable_jina_reader else ("jina_reader", "playwright", "bs4", "curl")
)
browse = Browse(
    proxy=os.getenv("BROWSE_PROXY"),
    max_attempts=2,
    enable_pyautogui=False,
    enable_playwright=True,
    enable_curl=True,
    enable_jina_reader=not disable_jina_reader,
    enable_bs4=True,
    jina_reader_endpoint=jina_reader_endpoint,
    fallback_order=fallback_order,
)
```

Prefer this for “read web pages”, “summarize docs”, or “verify an online page”. Keep shell sandboxes out of the path unless the task truly needs command execution. Browse uses Jina Reader by default as an external URL-to-Markdown first pass and automatically knows the official alternate endpoint `https://r.jinaai.cn/`; set `BROWSE_DISABLE_JINA_READER=1` when delegating public URLs to that external service is not acceptable. Set `BROWSE_JINA_READER_ENDPOINT` only when you need to choose a different primary Reader endpoint.
Attach them with `agent.use_actions([search, browse])` when you want the agent
to call both packages.

### Dependency Install Or Other Broad Shell Work

If the user wants to install packages, run migrations, or do other shell-heavy
work, do not route that through Python sandbox or model-visible package-manager
commands.

For code execution in common languages, prefer Docker-backed helpers with
host-selected provisioning policy:

```python
agent.enable_code_runtime(
    language="go",
    provisioning_profile="developer",
)
```

Use a bash sandbox action with a deliberate allowlist such as
`["python", "pip", "uv", "poetry", "git"]` only for trusted maintenance flows
where shell is the product behavior.

```python
agent.action.register_bash_sandbox_action(
    action_id="package_runner",
    allowed_cmd_prefixes=["python", "pip", "uv", "poetry", "git"],
    allowed_workdir_roots=[repo_root],
    default_policy={
        "workspace_roots": [repo_root],
        "allowed_cmd_prefixes": ["python", "pip", "uv", "poetry", "git"],
        "timeout_seconds": 60,
    },
)
```

If you need internet-enabled dependency preparation for model-planned code,
prefer `provisioning_profile="developer"` or `"ci"` with an explicit
`dependency_policy` over relaxing the Python sandbox. The legacy trusted-local
Python sandbox is for compatibility, not environment mutation.

### When You Really Want Big Permission

The current codebase does not have a single “full trust” switch for Python sandbox. The safe way to widen scope is to:

- use Bash sandbox or a custom executor, not Python sandbox
- broaden `allowed_cmd_prefixes` only for trusted flows
- keep `allowed_workdir_roots` narrow even when commands are broad
- use `allow_unsafe=True` only in explicitly trusted and reviewable host-owned execution paths

For the most permissive boundary, use a dedicated Docker-based executor with controlled network and filesystem settings, and keep that executor isolated from the default app path.
