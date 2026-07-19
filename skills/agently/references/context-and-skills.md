# Task Context, Files, Records, and Real-World Skills

Use this reference when a task must assemble information from several sources,
progressively disclose it to an Agent/model, work with task files, persist
records, or consume installed real-world Skills.

## Ownership

| Concept | Owns | Does not own |
|---|---|---|
| `TaskContext` | One task's revisioned source bindings/direct entries and its internal derived `ContextIndex` lifecycle | Source truth, files, execution, or persistence policy |
| `ContextIndex` | Internal structural, lexical, or optional hybrid partitions derived from attached sources | Public aggregate identity, source truth, exact body reads, or semantic model routing |
| `ContextSource` | Descriptor enumeration and exact bounded read for one source type | Cross-source selection or model routing |
| `ContextReader` | Consumer/phase/intent-specific selection, budgeting, read, diagnostics, and `ContextPackage` output | Source truth or storage |
| `TaskWorkspace` | Existing task files, generated artifacts, path policy, file identity, and bounded file reads | Records, semantic retrieval over records, model-hot packaging, or task lifecycle |
| `RecordStore` | Records, links, retrieval, RuntimeEvents, checkpoints, snapshots, leases, and durable refs | Task file editing, semantic task intent, or model execution |
| `SkillLibrary` | Parsing, installing, resolving, versioning, and reading immutable Skill revisions | Skill relevance, task routing, permissions, Actions, or execution strategy |
| `AgentExecution` | Task-scoped Skill binding, TaskContext construction/read, route selection, execution, and result/stream lifecycle | Installed package truth or source-specific storage |
| `AgentTask` | Long-task planning, work progression, evidence, verification, repair, and terminal acceptance | Package installation, file-space identity, or record backend implementation |

The data flow is:

```text
TaskWorkspace / RecordStore / SkillLibrary / direct caller facts / custom sources
                                ↓ ContextSource bindings
                 TaskContext snapshot + internal ContextIndex
                                ↓ ContextReader(intent, consumer, phase, budget)
                             ContextPackage(s)
                                ↓
                    AgentExecution / AgentTask / ModelRequest
```

## TaskContext and ContextReader

Create one TaskContext for one task identity. Attach sources or put small direct
entries; do not copy every source body into the aggregate.

```python
from agently.core import TaskContext
from agently.types.data import ContextBudget, ContextReadIntent

task_context = TaskContext(task_id="support-42")
task_context.put(
    role="state",
    content="Customer asks whether the proposed reply follows the refund policy.",
    entry_id="customer-request",
    required=True,
)

reader = task_context.reader(
    consumer="model_request",
    phase="draft_reply",
    budget=ContextBudget(max_chars=12_000),
)
package = await reader.async_read(
    ContextReadIntent(query="refund eligibility and reply constraints")
)
```

TaskContext is the sole public aggregate and lifecycle owner. It owns one
internal `ContextIndex` that builds, invalidates, and reuses source-derived
structural, lexical, or optional hybrid partitions. The index is not a public
manager, does not replace source truth, and never supplies exact bytes by
itself. Create readers
with `task_context.reader(...)`; restore their exported state with
`task_context.restore_reader(...)`. `ContextReader` remains a public handle for
typing and use, like an execution handle owned by its aggregate, but it cannot
be constructed or restored independently. `ContextPackage` is the immutable
cross-boundary delivery value, not another owner.

Important behavior:

- A reader is bound to a TaskContext snapshot. Refresh or create a new reader
  after the aggregate changes; do not silently read a newer revision through a
  stale reader. ContextIndex partitions are keyed by source revision, index
  profile, and provider identity; a changed source invalidates the affected
  derived partition rather than changing the reader's pinned task snapshot.
- A `ContextSource` implements `async_enumerate_descriptors(...)` for compact,
  indexable facts and `async_read_exact(...)` for the bounded canonical body of
  a selected source ref. Source kinds are an open adapter vocabulary. A filter
  may select only kinds attached to the current TaskContext; unknown kinds fail
  instead of silently disappearing.
- Required blocks are read before optional relevance selection. Optional
  prose relevance requires a semantic selector; if none is available, fail
  closed instead of falling back to keyword routing.
- The model sees host-issued block keys and returns only those keys. Host code
  validates them and rejoins canonical source ids and metadata.
- `ContextPackage` is a read result for a specific intent/consumer/phase, not
  the canonical task state.
- ContextIndex narrows reusable descriptor candidates. ContextReader owns
  consumer-local offsets, optional ModelRequest selection, budgeting, exact
  source reads, delivery diagnostics, and the immutable ContextPackage. A cache
  hit avoids rebuilding a derived partition; it does not prove that an LLM
  request used fewer prompt tokens.
- Keep full raw/meta records cold. Put bounded bodies and compact refs in the
  package, and let a later read request scoped detail when needed.
- Admit only text or source-parsed document text to model-hot package content.
  The built-in TaskWorkspace source parses supported PDF/DOCX/XLSX/PPTX files;
  missing parsers leave the file ref-only. Keep binary and unknown formats
  ref-only, and never infer their contents from filenames or summaries.
- Keep images ref-only unless the exact `ContextConsumer` explicitly declares
  `capabilities={"attachments": {"image": True}}`. A generic attachment flag
  or model-name guess is insufficient. For a capable consumer, validate the
  image attachment envelope and bind it through ModelRequest attachments, not
  the text context pack. Image interpretation remains model-owned.

Required content remains fail-closed when it cannot fit. If the Skill or caller
explicitly accepts a lossy disclosure, pass a `ContextReadIntent` with
`metadata={"required_overflow": "lossy_digest"}`. An oversized Skill then
returns a bounded `completeness="lossy"` digest containing its immutable full
ref and ordered section refs, while the section candidates remain available for
semantic selection. The digest records original and omitted sizes; it never
pretends to be the complete Skill. For AgentTask, carry the same explicit policy
through `context_budget={"chars": 12_000, "required_overflow":
"lossy_digest"}`. Without that opt-in, use a larger/focused consumer or fail
before business work.

AgentTask receives the same explicit image capability through
`execution.strategy(..., context_consumer_capabilities={"attachments":
{"image": True}})`. If model/provider capability is not explicitly known, use
the conservative ref-only path.

## TaskWorkspace

Bind a file space when the task reads or edits an existing directory or creates
file deliverables:

```python
agent.use_task_workspace("./customer-case", mode="read_write")
agent.enable_task_workspace_file_actions(write=True, export=True)
```

Use `agent.enable_coding_agent_actions(...)` for repository-style read, grep,
edit, patch, and guarded write work. TaskWorkspace owns containment, stale/read
guards, file refs, and readback facts. It does not expose `put`, `retrieve`,
checkpoints, RuntimeEvent persistence, or context-building APIs.

For a required AgentTask terminal deliverable, write candidate bytes to a
staged candidate and completely read them back for verifier inspection. Only
after verifier acceptance may TaskWorkspace perform digest-pinned atomic
promotion to the declared target, followed by a complete post-promotion
readback. Rejection leaves the previous target untouched; promotion or final
readback failure blocks delivery instead of reporting success.

The default Agent TaskWorkspace is isolated under
`<parent>/.agently/task_workspaces/<agent.id>`. Select the existing project or
business directory explicitly when the task is supposed to edit it.

## RecordStore

Bind a RecordStore for durable records or recovery:

```python
from agently.core import RecordStore

record_store = RecordStore("./customer-case-state", mode="read_write")
agent.use_record_store(record_store)

ref = await record_store.put(
    collection="policy",
    kind="refund-rule",
    content={"window_days": 30, "requires_receipt": True},
    tags=["refund"],
)
package = await record_store.retrieve(query="refund eligibility")
```

Use RecordStore explicitly for record retrieval, evidence links, RuntimeEvent
audit, checkpoints/snapshots, leases, and durable artifact refs. Do not make a
TaskWorkspace database implicit, and do not make every available RecordStore an
automatic execution archive.

## AgentTask Evidence Continuity

TaskBoard dependency readbacks enter one host-canonical live evidence ledger
before a card prompt is built. The prompt projection, binding guard, acceptance
index, and persisted card result reuse that identity domain; do not construct a
second ordered ledger after the model has selected a reference. A control card
that explicitly reports `sufficient=false` is a setback even if it also returns
`status=completed` and `next_board_action=finalize`.

Across evidence-reacquisition rounds, `claim_N` is only a response-local model
selection key. The host tracks an exact material-claim subject separately, so
artifact reordering cannot bind new evidence to a different claim.

## SkillLibrary

A real-world Skill is a public `SKILL.md` package plus optional references,
scripts, examples, and assets. Installation produces an immutable revision.

```python
from agently.core import SkillLibrary

library = SkillLibrary("./.agently/skill-library")
revision = library.install("./skills/refund-review", trust="trusted")
same_revision = library.resolve(revision.revision_ref)
resource = library.read_resource(same_revision, "references/policy.md")
```

`skill_id` is a canonical package identity; `revision_ref` pins exact content.
Reinstalling changed content creates another revision. Existing executions keep
their bound revision rather than silently changing beneath a task.

For an authorized Git source, use the source-provider contract instead of a
custom checkout wrapper:

```python
from agently.types.data import SkillSourceRequest

agent.set_settings("code_execution.providers", ["docker"])
agent.use_task_workspace("./task-workspace", mode="read_only")
revision = await agent.skill_library.async_install_source(
    SkillSourceRequest(
        source="https://github.com/example/skills.git",
        source_type="git",
        ref="4a1d2f0",  # pin a reviewed revision in production
        subpath="skills/refund-review",
    ),
    trust="trusted",
)
```

`SkillSourceProvider` owns source materialization and provenance. The
`SkillLibrary` still parses and stores an immutable installed revision; source
access does not grant script execution permission. For the compatibility
facade, `Agently.skills_executor.install_skills_pack(..., fetch=True, ref=...,
subpath=..., source_type="git")` uses the same boundary.

Remote compatibility installs default to `untrusted`; explicitly promote only
a reviewed immutable revision. Local installs retain the local trust default.
Selected Git/local subpaths reject symlink components that escape the
materialized source root.

A complete Git pack compatibility call is:

```python
pack = Agently.skills_executor.install_skills_pack(
    "https://github.com/example/skills.git",
    fetch=True,
    ref="4a1d2f0",
    subpath="catalog/runtime-pack",
    source_type="git",
    trust_level="trusted",
)
execution = agent.create_execution().use_skills_packs(
    [pack["skill_pack_id"]],
    mode="required",
)
target_revision_ref = next(
    ref
    for ref in pack["revision_refs"]
    if Agently.skill_library.resolve(ref).skill_id == "target-skill-id"
)
```

`Agently.skills_executor`, `Agently.skill_library`, and agents created by that
same `Agently` application share one canonical `SkillLibrary` instance. The
facade reconfigures that instance in place; it does not own a separate pack
registry. Resolve facade-installed pack members through
`Agently.skill_library`, then bind the selected exact revision through the
agent execution.

`ref` accepts a Git ref; production authorization should pin the reviewed
immutable commit rather than a moving branch or tag. Repository allowlists,
credentials, and network access remain host/source-provider policy, not Skill
trust or script authorization.

## AgentExecution Skill Binding

Bind Skills to a fresh execution, then let the execution build/read the shared
TaskContext:

```python
execution = (
    agent.create_execution()
    .input("Draft a policy-grounded answer for the customer case.")
    .require_skills([revision.revision_ref])
)

task_context = await execution.async_prepare_task_context()
skill_context = await execution.async_read_task_context(
    intent="refund policy and response procedure",
    consumer_id="model_request:refund-draft",
    phase="draft_reply",
)
result = await execution.async_start()
```

Use `use_skills(...)` for optional candidates, `require_skills(...)` for an
availability contract, and `use_skills_packs(...)` for installed pack scope.
Required Skills fail closed before business work when the requested revision is
missing or unreadable.

Keep three facts separate:

- a revision bound into TaskContext is available to the task;
- a disclosed Skill block attached to a concrete ModelRequest response is
  consumed context;
- a successful Action record is executable capability evidence.

Availability alone does not prove model consumption. Skill consumption never
adds a planner capability or proves a side effect.

Skill reading and side effects are separate:

- Skill instructions may tell the model how to use an Action.
- The host must mount and authorize that Action explicitly.
- Only actual Action records prove the side effect.
- A script inside a Skill is an addressable resource, not an automatically
  callable Action.

When the host intentionally authorizes one exact trusted script, bind it after
TaskContext preparation:

```python
from agently.types.data import SkillScriptAuthorization

await execution.async_prepare_task_context()
binding = next(
    item
    for item in execution.skill_bindings
    if item.revision_ref == revision.revision_ref  # use target_revision_ref for a pack
)
bound_action = agent.bind_skill_script_action(
    execution,
    binding_id=binding.binding_id,
    resource_path="scripts/check.py",
    authorization=SkillScriptAuthorization(
        auto_allow=True,
        expected_outputs=("output/report.json",),
    ),
)

action_result = await agent.action.async_execute_action(
    bound_action.action_id,
    {"args": []},
)
if action_result["status"] != "success":
    raise RuntimeError(action_result.get("error") or "Skill script failed")

artifact = next(
    item
    for item in action_result["artifacts"]
    if item["path"].endswith("output/report.json")
)
readback = await execution.task_workspace.read_file(
    artifact["path"],
    max_bytes=64_000,
)
if readback.truncated:
    raise RuntimeError("Declared Skill output exceeded the readback budget")
report_json = readback.content
```

This verifies the exact revision, resource descriptor, and digest, then
registers an ordinary code-execution Action. At call time the script bytes are
copied into a scoped TaskWorkspace execution area before the selected provider
runs them. The installed Skill directory is never executed in place. Trust is
package provenance policy, not blanket permission; the explicit authorization
and ordinary Action evidence remain required.

`BoundSkillAction.action_id` is the exact Action dispatch key. The bound script
Action accepts only bounded `args`; stdin, environment, arbitrary source files,
runtime commands, and package-manager commands are not model inputs. The
binder supplies its own provider requirement from the ordered
`code_execution.providers` setting, so `enable_code_runtime(...)` is not a
prerequisite. Its successful Action result publishes declared artifacts as
TaskWorkspace-relative private paths such as
`.agently/files/<execution>/code_execution/<call>/output/report.json`; physical
readback through
`execution.task_workspace.read_file(...)` proves the bytes that were actually
collected.

## SkillsExecutor Compatibility Facade

`Agently.skills_executor` remains a thin application facade for released setup
and integration calls:

- configure the local SkillLibrary root/trust boundary;
- install, list, inspect, and read local or source-provider-backed Skill
  revisions;
- discover/install/list/inspect local or source-provider-backed Skill packs;
- build a compatibility context-pack projection through generic TaskContext and
  ContextReader behavior;
- expose the TaskDAG `kind="skill"` resolver.

It does not select a route, execute a Skill strategy, infer/mount capabilities,
own an AgentTask loop, or create `skill_activation` Blocks. The old
SkillsExecutor plugin, `SkillsManager`, Skills route, `single_shot`, `staged`,
`react`, runtime-chain strategies, `skill_activation`, and
`workspace_operation` are removed.

`agent.run_skills_task(...)` and `agent.async_run_skills_task(...)` are thin
compatibility adapters that construct an ordinary AgentExecution. New code
should configure the execution directly so its TaskContext, route, Actions,
limits, and result lifecycle remain explicit.

## Review Checklist

- Is each piece of information owned by one source rather than duplicated into
  the TaskContext?
- Does the ContextReader receive an explicit intent, consumer, phase, and
  budget?
- Are model-returned keys validated and rejoined host-side?
- Are task files in TaskWorkspace and durable records in RecordStore?
- Are Skill revisions immutable and pinned for active executions?
- Are Actions/permissions explicit and independent from Skill reading?
- Is SkillsExecutor only a compatibility facade rather than an execution owner?
