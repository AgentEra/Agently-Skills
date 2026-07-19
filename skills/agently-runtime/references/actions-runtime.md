# Agently Action Runtime

Use this reference for callable Actions, built-in Search/Browse/Cmd, MCP/ACP,
Action planning/dispatch, artifacts, TaskWorkspace file Actions, policy, and
AgentTask Action evidence.

## Native Surface

- Prefer `@agent.action_func` and `agent.use_actions(...)`; `tool_func`,
  `use_tool`, and `use_tools` are compatibility aliases.
- Prefer built-in `agent.enable_*` helpers and Action packages before exposing
  provider/manager internals.
- Use `agent.action.get_action_info()` / `get_tool_info()` for model-visible
  schemas. Explicit tags narrow the set; environment values stay redacted.
- Treat model-planned Action inputs as untrusted. Filter/validate them against
  registered `ActionSpec.kwargs`, strip host-only keys, apply policy, then
  dispatch.
- Preserve `ActionSpec.required_input_keys`. Derive them from function
  parameters without defaults, or declare them explicitly for executor/MCP
  registrations. Emit them in native tool JSON Schema and reject missing keys
  before dispatching a model-authored command.
- Treat multi-Action package registration as atomic. Search/MCP batch failure
  removes batch-created Actions and restores same-id host registrations.

## Task Files and Durable Records

- Select files with `agent.use_task_workspace(...)`.
- Use `agent.enable_task_workspace_file_actions(...)` for general contained
  file work and `agent.enable_coding_agent_actions(...)` for read/glob/grep/
  edit/patch/guarded-write repository work.
- TaskWorkspace owns containment, write policy, stale/read guards, file refs,
  content versions, and bounded readback.
- RecordStore owns records, retrieval, links, RuntimeEvents, snapshots,
  checkpoints, leases, and durable artifact refs.
- TaskContext/ContextReader package selected file/record/Skill information for a
  consumer. ActionRuntime must not recreate ContextBuilder or a generic
  Workspace.

File helpers inherit the bound TaskWorkspace root unless the host passes an
explicit `root=` / `cwd=`. Use file Actions rather than shell for file IO; use
shell for builds, tests, git inspection, and bounded diagnostics.

TaskWorkspace file writes/readbacks return host facts such as path, byte count,
SHA-256, truncation/readability state, diagnostics, and file refs. Consume these
facts instead of model prose or stdout path guesses.

## Action Planning and AgentTask

For a TaskBoard Action card or Flat step with known required Actions:

1. give the model only the selected Actions' authoritative schemas;
2. ask for dependency-ordered `action_commands` with canonical `action_id` and
   schema-valid `action_input`;
3. validate offered ids/kwargs host-side;
4. dispatch directly through ActionRuntime;
5. record Action results/evidence.

Do not wrap a fixed command contract in a generic multi-round Action loop.
Reserve ActionLoop for open-ended behavior where later Action choice depends on
observed results. Unknown/unavailable required Actions fail closed before model
execution.

An authored `action_succeeded` requirement is a deterministic evidence gate.
Only a real successful call of the exact mounted Action satisfies it.
TaskWorkspace readback or verifier prose cannot substitute for Action dispatch.
If the Action is absent or policy-blocked, fail closed instead of choosing a
similar operation.

Keep TaskBoard scheduling/dependencies in TaskBoard/Blocks and Action execution
in ActionRuntime. A card receives one local objective/done-when plus dependency
evidence; the global task is orientation, not permission to execute sibling
work.

Keep `scoped_retrieval` in TaskContext/ContextReader. A retrieval-only TaskBoard
card or repair-support card uses the ordinary/auto carrier and must not be
relabeled as an Action card. Use `actions` only when a mounted Action or real
TaskWorkspace side effect is required.

## Artifact and Evidence Boundaries

Instruction-heavy or large Action values cross hot boundaries as bounded
digests/previews plus Action artifact/file refs. The private Action artifact
store retains the exact scoped value while its owning execution is live.

Model-visible artifact candidates receive one host-issued `selection_key` plus
task-relevant facts. Host code validates that exact key and reconstructs the
canonical artifact under the expected execution/task scope. Do not expose or
trust model-copied canonical ids, scopes, call ids, or provenance.

```python
readback_call = {
    "action_id": "read_action_artifact",
    "action_input": {"selection_key": offered_key},
}
```

The key is valid only in the bound live scope. Standalone ActionFlow/TriggerFlow/
TaskDAG scopes release their private artifacts when the run closes; historical
refs then report unavailable. Promote selected long-lived output to
TaskWorkspace/RecordStore before scope close when post-run readback is required.

Use `max_bytes` for progressive readback. One successful read is already a
bounded hot content page and keeps its typed `owner`, `locator`,
`content_version`, and byte range. It must not be artifactized again or turned
into a new selection-key chain. Treat Action success/ref availability as a
pointer fact only until the page body is consumed. If a TaskBoard verifier still
lacks the required snippet, reacquire a narrower or subsequent page; do not
weaken the original criterion. Three consecutive identical typed pages are an
ActionLoop no-information-progress exit back to TaskBoard, not acceptance.

Action evidence binding and artifact readback are separate. A host-issued
`action_call_id` may identify an offered Action result for evidence binding; it
is not an artifact selection key.

Bound/redact custom Action handler results before they enter TaskContext,
RuntimeEvent, TriggerFlow state, logs, metadata, or public return. Opaque
exception strings/bytes expose no raw prefix; keep a fixed summary, original
size, digest, and structural-frame-only traceback facts.

## AgentTask File Delivery

For a declared deliverable path:

- ActionRuntime owns model-callable file-write dispatch, validation, and call
  evidence; TaskWorkspace owns the contained physical write/promotion mechanism
  and file truth;
- TaskWorkspace physical readback is the current source of truth;
- model-declared `file_refs` remain diagnostics until host readback succeeds;
- a model-requested content change requires another file Action;
- final acceptance requires the exact expected path/content version, not a
  same-basename sibling or older candidate.

For a required TaskBoard terminal deliverable, the file Action may write a
working or staged candidate. AgentTask owns the deterministic terminal
lifecycle decision: complete candidate readback, verifier acceptance, then a
digest-pinned `TaskWorkspace.atomic_promote_file(...)` transition and complete
target readback. Promotion copies the already accepted bytes; it is not a
second model-callable write or permission bypass. Rejection preserves the old
target, and promotion/readback failure blocks delivery.

AgentTask may materialize a short `artifact_markdown` or sectioned
`artifact_manifest`, then read back path/bytes/hash/preview/file refs. Keep
integrity metadata cold and give semantic verifiers bounded body/ref views.
For long prose, stream/generate natural text and use a compact judgment/manifest
contract; do not force the whole body through JSON only to obtain progress.

Downloads, page snapshots, generated code, and search notes may be intermediate
TaskWorkspace/Action refs. They are execution evidence, not final-deliverable
proof.

## Search and Browse

```python
from agently.builtins.actions import Browse, Search

agent.use_actions([
    Search(timeout=15, max_attempts=2),
    Browse(max_attempts=2, enable_playwright=True),
])
```

- Keep proxy, timeout, backend/fallback, retry, region/language, and Jina Reader
  policy on the package/executor. Do not invent `enable_search(...)`.
- A fallback recovery may be `partial_success` with diagnostics; treat it as
  usable evidence plus degraded-provider observability.
- Registered Browse failures are Action failures. Direct text-returning Browse
  helpers remain compatibility surfaces.
- Browse owns URL recovery; downloaded PDF/Office/image-like bytes are
  materialized into TaskWorkspace and returned as file refs/bounded previews.
  Browse does not become a document parser.

## MCP and ACP

- MCP tools are Actions backed by managed ExecutionResources. Prefer Streamable
  HTTP for service integrations and explicit config for stdio/multi-server
  local integrations.
- `agent.use_acp(...)` exposes handshake-verified coding agents as an Action
  capability plus `ExecutionResource(kind="acp")`; ACP is not an AgentExecution
  route.
- `on_missing="skip"` records diagnostics; use `on_missing="error"` when the
  capability is required.
- If ACP root is omitted, use the bound TaskWorkspace root. Explicit root is a
  host authorization override.
- AgentTask recovery may call the registered ACP Action after normal failure,
  but must not import/use ACP when it was not mounted.

## Skills and Actions

A real-world Skill is guidance plus addressable resources. It does not execute,
mount, or authorize Actions. The host explicitly maps required operations to
controlled Actions/ExecutionResources. A Skill script is not a trusted handler
by default.

If a dependency is missing, run a controlled host/provider ensure or
install-capable Action and retain the result. Policy denial or failed repair is
blocked/failed evidence, not silent degraded success. There is no SkillsManager
or Skills-owned React/strategy executor.

## Policy and Provisional Results

- Keep permission profiles explicit: search-only, network-read, task-files,
  read-only shell, install-capable maintenance, or isolated broad executor.
- Host-only escape grants never appear in model-visible schemas.
- Framework approval uses global PolicyApproval; durable waits become
  TriggerFlow interrupts and ExecutionExchange views.
- Structured Action planning fields are provisional until final parser data is
  available. `next_action="response"` stops further dispatch; it does not cancel
  the provider stream.
- `agent.get_action_result(..., timeout=N)` bounds the complete ActionFlow.
  Handle `RuntimeStageStallError(stage="action_loop_close")` rather than adding
  a host polling/kill loop.
- A native-tool planner result with no tool calls is skipped planning evidence,
  not executed work.

## Observation and Testing

- Keep Action RuntimeEvent payloads bounded/redacted; full private values stay
  out of logs and DevTools.
- Use `agent.action.summarize_records(...)` when host code needs a deterministic
  rollup of attempted/successful/failed Actions and validation commands.
- Deterministic tests may prove schemas, policy, scope, files, records,
  accounting, and lifecycle. Use a real model/model judge for semantic action
  selection or business usefulness.
- Examples must exercise actual framework paths and declare stable key effects;
  do not replace model-owned planning/selection with local canned mappings.

## Anti-Patterns

- Parallel tool dispatcher or duplicated Action planning prompts in higher
  layers.
- Hidden live-resource lifecycle inside an Action executor.
- Generic shell/file/database access when a narrower owner exists.
- Treating artifact previews, TaskWorkspace readback, Skill instructions, or
  model claims as proof that an Action ran.
- Keeping full Action values in every prompt/event/state/log boundary.
