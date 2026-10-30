# Multi-Round Collaboration

Use this when a task needs repeated discussion, revision or evaluation, including
Prompt collaboration, Flow design and experiment tuning. At the beginning of
each substantive round's response, show the current item table, followed by a
change-log table, before the design, edits or results. Keep tool-by-tool updates
brief; they do not each create a new discussion version.

## Current Items and Change History

- Put **Status on the left, Item on the right**. Keep item numbers stable across
  rounds and append numbers for new work. Show completion and the current stage
  truthfully: proposed, awaiting confirmation, confirmed, implementing or
  verified are different states.
- Show additions, modifications, removals and abandonment explicitly. Use
  *italics* for this round's added text, ~~old text~~ → *new text* for edits,
  and ❌ ~~abandoned item~~ for abandonment, with text labels as well as icons.
  Removing duplicate work is different from abandoning its underlying goal;
  explain where any retained responsibility goes.
- Register changes in a table with **Time (and timezone), Discussion version,
  Item, Change and reason, Implementation status**. Simple versions such as D01,
  D02 are discussion revisions, not framework or artifact release versions.
  Record actual times at known precision; label unknown historical times rather
  than inventing them.
- Distinguish a proposed change, an accepted decision awaiting implementation,
  an applied change, verified work, and an abandoned proposal. Record whether
  an abandoned or removed design has actually been removed from its affected
  artifacts. A decision alone does not prove implementation or validation.
- Append later decisions and implementation outcomes to history rather than
  silently overwriting them. Reopen an affected completed item if new evidence
  invalidates it; retain the prior completion and the reopening reason.
- Highlight this round's differences. In later rounds, use readable current
  wording in the item table while retaining previous wording in the log.
- While the same work item remains active, every status/history presentation
  must include its complete item list and complete change history, including
  unchanged, completed, pending, removed and abandoned items. Highlight this
  round's differences within that full view; delta-only tables and links to
  earlier records do not replace it. If nothing changed, retain the full view
  and say so without inventing a change.
- Continuing, resuming or focusing on a subtopic does not by itself start a new
  work item. Reset the list only for genuinely different work, explicitly
  naming the scope change. Recover prior records after a handoff or context
  loss; label missing history rather than silently dropping or inventing it.
- Reuse the existing plan, review notes or experiment record. A short task can
  keep both tables in the conversation; use an existing durable project record
  when long work needs recovery or handoff. Do not require another tracking
  system, file format, model output schema, or runtime ledger.
- For large lists, group by phase and keep individual rows concise without
  omitting items or history entries. Links may supply supporting detail, not
  replace the full same-work-item view. These records do not add approval gates
  or reset existing authorization.

## Presentation Example

Synthetic presentation only; the times, versions and states below are not
observed work. This is a coding-agent/developer collaboration view, not content
to copy into the application's model prompts. Adapt labels to the user's
language while retaining the two tables and their meaning.

**Current items · D03**

| Status | Item |
|---|---|
| ✅ Confirmed | 1. Business goal and scope |
| 🔄 In progress · changed this round | 2. ~~Review every request separately~~ → *Review the coupled planning and writing requests together* |
| ⏳ Pending | 3. Evaluate representative scenarios |
| ❌ Abandoned | 4. ~~Add a separate summary request~~ |
| ➖ Removed | 5. ~~Store a duplicate full input snapshot~~ |
| 🆕 Pending · added this round | 6. *Check early retrieval deduplication and concurrency limits* |

**Change log · illustrative times in UTC+08:00**

| Time | Discussion version | Item | Change and reason | Implementation status |
|---|---|---|---|---|
| 2026-09-07 14:10 | D01 | 1–5 | Register initial scope. | ✅ Recorded |
| 2026-09-07 14:25 | D03 | 2 | Review coupled requests together to inspect their handoff. | ✅ Applied to the review plan |
| 2026-09-07 14:25 | D03 | 4 | No consumer for a separate summary. | ❌ Abandoned; removed from the design |
| 2026-09-07 14:25 | D03 | 5 | Existing records already preserve the input. | ✅ Duplicate removed; tracing retained |
| 2026-09-07 14:25 | D03 | 6 | Early retrieval needs bounded, deduplicated execution. | ⏳ Confirmed; not implemented |
| 2026-09-07 14:40 | D03 | 6 | Propose deduplication by task-relevant payload. | 💬 Awaiting confirmation |

Continue with this round's actual design, findings or implementation evidence.

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
Neither needs to copy this collaboration procedure. Standalone product installs
can use their existing local checklist without installing Agently or adopting
its runtime. Model prompts do not automatically receive these collaboration
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
