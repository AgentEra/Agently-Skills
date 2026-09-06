# Table-First Prompt Collaboration Example

Presentation specimen only: synthetic design content, not an observed model
run or a production-approved business plan. Both phases are shown to illustrate
the layout; in actual collaboration, pause for inventory confirmation and
then review one selected request at a time. Adapt the tables to the project.

## 1. Confirm the Request Inventory

**Scenario:** turn meeting-action follow-up product requirements into a design
document for product and engineering review.

**Flow:** requirements -> section plan -> section writing -> Host assembly ->
optional whole-document review.

| Request | Core responsibility | Consumer | Review state |
|---|---|---|---|
| **R1: Section plan** | Define coverage, order, and unresolved questions. | Writers and business user. | **Expanded below as an example.** |
| R2: Section writer | Develop the current section with relevant continuity. | Host assembly. | Later, as needed. |
| R3: Document review | Find gaps, contradictions, and repetition. | Scoped revision. | Optional; not yet selected. |

R2 is one request family invoked for multiple sections. Host code owns identity,
ordering, storage, structure checks, and exact body assembly.

**Pause here in actual collaboration:** is this inventory and allocation of
responsibilities correct? Which boundaries should change?

## 2. Review One Request

### R1: Section Plan — Awaiting Confirmation

| Item | Proposed design |
|---|---|
| **Question to solve** | How should the document cover the requirements and support section-by-section writing? |
| **Stage result** | An ordered section plan, section scopes, and questions for the user. |
| **Out of scope** | Writing section bodies, inventing system capabilities, or creating real tasks. |
| **Consumers** | Writers use the plan; the user resolves information gaps. |

### Prompt Main Table

These are proposed model-visible contents. Review headings and approval state
are not automatically added to the model request.

| Slot | Topic | Actual proposed prompt content |
|---|---|---|
| **`system`** | Role and boundary | You are a product-design analyst. Use the supplied requirements and facts; distinguish known facts, proposals, and unresolved questions. |
| **`input`** | Background | The team mainly collaborates through enterprise IM. Organizers need follow-through, attendees need owners and due dates, and managers need progress visibility. |
| `input` | Current problem | Conclusions are scattered across minutes, chat messages, and personal notes. Actions are lost during copying, confirmation, and follow-up. |
| `input` | Desired outcome | Connect meeting conclusions, task confirmation, and continued follow-up into a clear business loop with less repeated manual chasing. |
| **`info`** | Document use | For this example, the document supports product and engineering review and explains business behavior and implementation boundaries. |
| `info` | Unknowns | The IM vendor, task system, API capabilities, permission policy, and reminder policy are not specified. Do not treat them as confirmed facts. |
| **`instruct`** | Current task | Plan sections covering the requirements. Give each a title and scope summary; do not write section bodies in this request. |
| `instruct` | Organization | Organize around business problems and the business loop, make section boundaries clear, avoid duplicate coverage, and order for later writing. Do not prescribe a fixed section count. |
| `instruct` | Missing information | Ask concrete questions in `open_questions` when a missing fact affects an important decision. Continue planning independent parts without inventing capabilities. |
| `instruct` | Return contract | Return only the agreed JSON. A section brief must guide writing rather than merely repeat its title. |
| **`output`** | Structure | Return `parts` and `open_questions` using the field constraints below. |

### Model-Visible Example

**Actual placement:** `info.examples`. **Source:** synthetic.
**Purpose:** explain the existing missing-information rule, not create a rule.
This is not a new Agently slot or `.examples()` API.

| Rule illustrated | Example input | Appropriate behavior | Inappropriate behavior |
|---|---|---|---|
| Ask about relevant missing facts instead of inventing them. | Action synchronization is required, but the task system is unspecified. | Keep the relevant section and, when needed, ask which task system will be used. | Claim that the system already supports automatic task creation. |

Reviewer-only notes or display-only output illustrations are separately marked
**not sent to the model**. Do not fill an example section when examples are not
needed; keep actual model examples subordinate to normative prompt content.

### Output Contract

**Return format: JSON.**

| Field | Type | Required / empty behavior | Meaning |
|---|---|---|---|
| **`parts`** | Array | Required, non-empty. | Section plan in writing order. |
| `parts[].title` | String | Required, non-empty. | Section title. |
| `parts[].brief` | String | Required, non-empty. | Questions covered and section boundaries. |
| **`open_questions`** | Array of strings | Required, may be empty. | Questions requiring user confirmation. |

### Confirmation Point

| Confirm | Review focus |
|---|---|
| **Responsibility** | Did writing or real system operations leak into the planner? |
| **Rules and facts** | Are facts sufficient? Any conflicts or single-instance rules? |
| **Examples** | Are they necessary and explanatory, without changing the rules? |
| **Output and handoff** | Can the next writer consume this plan correctly? |

**Wait for confirmation or revision of R1 before showing the next selected
design.** Apply revisions to the actual prompt/config; if scope or output
changes, check affected workflow handoffs. Keep unchanged confirmations.

This example demonstrates a review format, not a required workflow, schema,
section count, or fixed business policy.
