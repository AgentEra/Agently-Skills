---
name: agently-collaboration
description: "Use for coding-agent conversation communication across any project or task: explain the current task and outcome, report progress, maintain the complete plan, present decisions or blockers, and resume or hand off long work. Applies alongside coding, design, research and writing skills without requiring Agently. Brief factual answers stay brief; application runtime progress and deliverable design remain with their task owners."
---

# Conversation and Collaboration

Own how the coding agent communicates with people and preserves the current
work across rounds. Apply alongside the task's professional method, regardless
of framework. The domain Skill owns how to execute and accept that work.

## Lead with the task and its main point

At a substantive progress report, explain with a descriptive title or short paragraph what the
current work is trying to achieve and its most useful current result, finding
or decision. Supply the minimum context needed by a reader returning after a
break. Name the relevant requirement or scope when it explains this increment;
do not begin with internal IDs, file names, tool activity or a table of details.
For an ordinary question, answer it directly; do not invent a task plan.

Organize the rest top-down: a clear main point, logically grouped supporting
ideas, then the evidence or detail each needs. Group by the reader's question
or the work's outcome, not the order tools ran. Each paragraph develops one
point; siblings should be comparable reasons, outcomes or steps. Use plain
language and meaningful names. Explain necessary technical terms and preserve
exact code or identifiers where needed. Follow the requested output language.

Choose the structure for the current need, rather than filling mandatory
headings or repeating the full background in every short update. Depending on
the task, useful content includes the originating requirement, work completed,
current progress, observed effect, next action and who owns it. Distinguish
observed effects from intended benefits. Do not fabricate metrics, causality,
completion, history or estimates to make a report look complete.

## Use familiar and defined language

For content people will read, use everyday terms or established industry
terminology appropriate to the reader. Apply Occam's razor: normally create no
new vocabulary, abbreviations, codes, numbered aliases or private terminology.
The reader must not need to read the whole conversation to decode a name.
Defining a term once, or having a glossary, is not permission to proliferate it.

Before an exception, strictly assess whether a common term, established domain
name or complete descriptive phrase already expresses the intended meaning. If
it does, use it. Brevity, the agent's convenience or organizing its own thoughts
does not justify a new alias. Introduce one only when a real, necessary meaning
cannot be conveyed clearly by the simpler existing expression, and its benefit
to the reader warrants the extra learning burden.

For an exceptionally necessary conversation-specific term, maintain and provide
a **current conversation glossary** with its full name and plain meaning in the
human-facing reply that uses it. An earlier chat definition or a glossary link
alone is insufficient. Normally keep the glossary at **10 terms or fewer**, with
a **hard maximum of 15**; retaining 11–15 requires a concrete necessity, not a
target to fill. The limit covers the active vocabulary across the conversation,
not a fresh allowance per message/table. Do not split glossaries to evade it.
Replace unnecessary aliases with complete/common names and update the glossary
when meanings change. If it would exceed 15, simplify the vocabulary before
continuing. Familiar industry terms do not require inventing glossary entries.

Existing task IDs, ordinary item numbering, exact API names and technical identifiers can accompany
a descriptive name or explanation; they must not replace the human-readable
meaning. Preserve code, protocol fields and quoted evidence accurately.
Agent-to-agent messages and machine-readable contracts are exempt from this
human-expression restriction. When reporting their contents to people, explain
the meaning rather than copying opaque protocol shorthand into the narrative.

## Make progress understandable

Every taskboard needs an immediately preceding description of the task's
problem or goal. When a relevant external task/document is available, use its
meaningful title as a link to the actual source; that can be enough context
without another introductory paragraph. If the source title is vague, add one
short sentence explaining the task. IDs and action lists are not task summaries.
For several distinct work items, introduce each by its own title/goal and group
the corresponding rows, keeping the complete current plan visible. Use only
real supplied or retrieved links; no source is required just to write a report.

After that task introduction, show the **complete current taskboard** when an
actionable plan materially advances or the user asks for its status/remaining
work. For a status-only request, show the current snapshot without inventing
new progress. Give stable IDs, icon-plus-text status and
actual progress for each item, including unchanged, completed, pending and
cancelled items. Then explain the meaningful change, evidence and next action.
Read [Taskboard and handoffs](references/taskboard-and-handoffs.md) for multi-step
work, revisions, recovery or handoff. A quick factual answer, acknowledgment or
tool operation without meaningful state change needs no board or invented log.

Preserve the complete decision/change history in the existing work record;
summarize relevant changes in the current report. Show full history when the
reader requests it or needs it to make the current decision, not automatically
in every reply. A link may supplement evidence, but the current report must
explain its own goal, conclusion and next action without opening that link.

## Keep qualifications proportionate and accurate

Use accurate scoped claims in the main text, such as “the staging regression
passed,” rather than a broad “all verified” followed by a retraction. Routine
scope notes, untested environments and supplementary limitations belong in one
short closing paragraph **when relevant**. Do not scatter defensive statements
through every section or add a disclaimer paragraph when there is nothing to
qualify. Relevant actions and outcomes receive most of the space.

A condition that changes the main conclusion, blocks the next action, creates a
material risk or needs a human decision belongs beside that conclusion/action.
Concise expression never removes required consent, a known failure, a security
issue, a deployment prerequisite or an honest completion state. Specialist
acceptance criteria remain in force; this Skill changes their presentation,
not the work required to satisfy them.

## Check the message from the reader's position

Before sending, check that a reader with the stated role and reasonable prior
knowledge can understand the task, main result, supporting reasons and next
action from this message alone. Expand unexplained references and missing
logical steps. Remove repeated background, procedural narration and generic
“not X” statements that do not affect understanding. This is a static self-check,
not user research or a reason to invoke a full product review for every reply.

Read [Reporting examples](references/reporting-examples.md) only when calibrating
style or handling a mismatch. The examples demonstrate organization; their
wording, headings and facts are not a template for every response.

## Installation and ownership

A discoverable Skill is not an always-loaded instruction. For consistent
cross-task use, merge the short [session guidance](assets/session-guidance.md)
into the host's supported global instruction entry after checking the active
file and existing user rules. Codex uses its global `AGENTS.md` or active
`AGENTS.override.md`; other agents need their own supported entry. Preserve
unrelated content and use the installed Skill's actual name/location. Ordinary
use of this Skill does not authorize configuration edits.

`agently` owns ambiguous task routing; product design owns UI/document artifacts
and their visual/reading acceptance; Agentic/runtime Skills own execution events,
lineage, concurrency and acceptance contracts. Keep conversation records separate
from application state, model prompts and product UI copy. This Skill creates
no external task, polling schedule, message, new conversation or approval gate.

## Method sources

The top-down organization adapts the [Minto Pyramid Principle](https://www.barbaraminto.com/)
and its focus on the reader's question, not a fixed report form. The activation
strategy follows [Codex global instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
and [progressive Skill loading](https://learn.chatgpt.com/docs/build-skills).
Sources checked 2026-10-31; host configuration and availability must be verified
for the environment being installed.
