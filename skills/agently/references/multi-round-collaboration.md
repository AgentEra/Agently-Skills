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
  Show this round's log delta with access to earlier history; if nothing changed,
  say so without inventing a change.
- Reuse the existing plan, review notes or experiment record. A short task can
  keep both tables in the conversation; use an existing durable project record
  when long work needs recovery or handoff. Do not require another tracking
  system, file format, model output schema, or runtime ledger.
- For large lists, group by phase and summarize settled items with a link or
  pointer to the full record. Keep unresolved, changed, removed and abandoned
  items visible at the relevant round. These records do not add approval gates
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
