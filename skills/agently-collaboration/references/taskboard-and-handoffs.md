# Taskboard and handoffs

Use with the [conversation entry](../SKILL.md) for actionable work that spans
steps or rounds. First orient the reader with the current task, goal and main
result; then show the board and relevant supporting information. An explicit
status/remaining-work request also receives the current board, even if nothing
changed; label it as the current state rather than new progress. A one-off
informational answer or unchanged tool activity needs no invented plan or log.

## Complete current taskboard after the opening summary

Before the rows, tell the reader what problem this work solves or what outcome
it delivers. Prefer a meaningful **task/document title linked to its actual
source** when one is already provided or can be read through available access.
Reuse the authoritative title when clear; a generic title such as “Follow-up,”
an internal ID or a list of actions needs a brief goal/problem explanation.
The visible title and current statuses must make sense without opening the link;
the link supplies optional background and detail, not hidden prerequisites.
Do not invent a URL, require the user to create a task/document or search unrelated
systems merely to decorate a report. Without a source, use a plain descriptive title.

If the report contains distinct work items, introduce each group separately and
associate its rows with that task. One concise overall summary can describe the
combined goal when it genuinely exists; do not invent a common parent just from
ID prefixes. A table per group or a single table with explicit groups is fine.
Grouping does not reset task identities or omit completed, pending or cancelled
items. A standalone or repeated board still needs its local task introduction;
do not assume the reader remembers an earlier reply's title.

The board is a view of this conversation's actual plan, not a new runtime or
external task-management system. Use the existing plan/tool when available;
otherwise a Markdown table is sufficient. This reporting method does not require
a separately installed `taskboard` Skill or imply that a board tool was called.

- Keep one board across specialties and rounds. Preserve stable task IDs and
  show **all current planned items**, including unchanged, completed, not started,
  blocked, paused and cancelled items. A subtopic, context compaction or a new
  Skill does not silently discard the rest of the conversation's active plan.
  Genuinely different work may start another board with the scope change named;
  recover missing prior history rather than inventing it.
- Put status on the left and the task beside it. State the **actual progress of
  each task**, not just a generic label: what artifact/change/evidence exists,
  what remains or the next action. Link evidence as a supplement. Reuse native
  task identities; reconcile the board with the latest tool/record before
  reporting, and do not assume a successful plan write proves task execution.
- Give each item a meaningful task/action name beside its ID. Follow the
  [reader-language rule](../SKILL.md#use-familiar-and-defined-language): prefer
  ordinary names over new aliases; IDs never replace the description, even when
  valid in an external system. Do not invent prefixes just to group the board.
  Exceptionally necessary private terms require the provided conversation
  glossary and its limits; a glossary is not permission to create more terms.
- Use icons **and text** consistently:

  | Status | Meaning |
  |---|---|
  | ⬜ Not started / 未开始 | No task execution yet; an accepted plan alone is not work completion |
  | 🔄 In progress / 进行中 | Actual work has started; name the current stage and remaining work |
  | ✅ Completed / 已完成 | The item's stated outcome and applicable checks have evidence |
  | 🚧 Blocked / 受阻 | Name the specific unmet dependency, owner and recovery condition; continue independent items |
  | ⏸ Paused / 已暂停 | Work intentionally paused under the user's instruction; do not infer a pause from waiting |
  | ❌ Cancelled / 已取消 | Preserve the original ID, cancellation reason and actual cleanup/removal state |

- A new task gets a new ID; changed scope and newly discovered work update the
  board before the next progress report. Cancellation is not completion. Keep
  accepted decisions separate from implementation and verification. If feedback
  invalidates a completed task, reopen the same ID as 🔄 or 🚧, retaining the
  prior result, new evidence and remaining checks.
- The displayed state is a snapshot, never an invented percentage or ETA.
  Partial success remains in progress with its verified part stated. Do not
  mark the whole task ✅ because code was written, a candidate was drawn, a
  message was sent or a tool returned success. Verification belongs to the
  outcome actually promised by that task.
- After the full board, explain the meaningful change, evidence and next action
  concisely. Large plans may be grouped by phase with compact rows, while every
  item remains visible; a total count, changed-only list, collapsed completed
  section or link to an earlier board does not replace the current full view.
  No polling, heartbeat, new external task or extra approval is introduced.

## Decision and change history

Keep one authoritative record for the current work. Preserve stable IDs,
original decisions and subsequent changes, including additions, modifications,
removal, abandonment and reopened failures. Record the reason, actual status,
responsible owner and evidence; include time/timezone and a discussion revision
when known and useful. Do not fabricate historical precision or create a new
tracking system merely to satisfy this guidance.

Distinguish proposed, accepted, implemented and verified states. Cancelling an
approach does not prove its code or data was removed; record actual cleanup and
where retained responsibilities moved. Reopen the same item when new evidence
invalidates an earlier conclusion, preserving both the earlier evidence and the
new finding.

Keep pending cleanup visible on the cancelled row with its next action and
owner, or add a linked cleanup item when it needs separate tracking. Do not
hide remaining work behind the cancelled status or invent a duplicate task
solely for presentation.

The current report shows the complete current taskboard and the changes that
matter to this round. The **complete history remains retained**, but need not be
reprinted in every message. Expand it for an explicit history request, audit,
handoff or a decision that depends on earlier reasoning. Never make the reader
open an old message to understand the current task, conclusion or required action.
Use a compact change table when comparing several changes helps; timestamps,
revision labels, strikethrough and a second table are not mandatory decoration.

Continuing a subtopic, resuming or compacting context does not start a new work
item. Recover the existing plan and history first. If unavailable, mark the
specific gap rather than inventing a fresh all-pending board or invented prior
success. Name a scope change when genuinely different work begins. For large
plans, group rows by phase without dropping current items. Store durable history
in an existing project record when recovery needs it; a short task can retain
it in the conversation.

## Progress, Evidence and Handoff Ownership

This reference owns coding-agent/developer collaboration records across product,
document and Agentic work. Reuse the project's authoritative issue, checklist or
review record: do not create a second progress ledger in each Skill. A design
finding can carry several evidence dimensions; keep one stable item identity.
A reviewed proposal, accepted decision, applied change, verified result,
deployment and business approval are different facts. Reopen the same item when
new evidence contradicts completion and retain its earlier evidence.

At a substantive checkpoint record the goal and scope, current item state,
actual artifact/version/environment, evidence and its limits, blockers, next
action and responsible owner. Preserve decision and change history. Progress
reports are a projection of these facts, not evidence of runtime completion;
never invent a completion percentage, ETA, benchmark or test result.

The product Skill owns the content/functional/interaction/visual review criteria
and the Agentic Skill owns request/state/lineage and convergence contracts.
Neither needs to copy this collaboration procedure. This Skill and product
design can be installed without Agently or its runtime; reuse existing local
checklists when the collaboration Skill is unavailable. Model prompts do not automatically receive these collaboration
records; include only information required by the current consumer.

### Work identity and continuous responsibility

Distinguish a business request/spec, a work item, a deliverable increment, a
release batch and the conversation carrying them. Check their actual cardinality;
never infer one-to-one relationships from the ambiguous word “task”. A stage
change or a shared executor does not by itself transfer responsibility. Preserve
the responsible conversation's continuity where that is the actual operating
model, including returns from shared resources. Context compaction is not a
business handoff; a fixed acceptance condition plus artifact/run evidence is
stronger than the executor's completion statement.

Module, iteration, execution segment and conversation lifetimes may differ.
Choose handoff boundaries by goal cohesion, useful context, dependencies and
verifiable checkpoints, not by a fixed time or one conversation per function.
A handoff must preserve source history, valid evidence, remaining work, in-flight
runs/events and the current responsibility/write authority. It does not authorize
new conversations, external messages, releases or permission changes.

### Report language

For experiment reports and design documents, when the task instructions are
not in English, prefer a complete document in that instruction language;
a bilingual version is also acceptable. An explicit requested output language
takes precedence. Apply this to the document itself, not only the chat summary.
Preserve code, identifiers, raw prompts and evidence as needed; their language
does not determine the surrounding report language.
