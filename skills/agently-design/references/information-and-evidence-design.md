# Information, Evidence, and Identity Design

Keep model context task-scoped. Give the model one host-issued trusted selection
key plus relevant facts; host code validates that key and reconstructs canonical
ids, UUIDs, metadata, and records. Keep compact evidence hot and full metadata
or raw records cold behind Workspace/spec refs. Unknown keys, refs, snapshots,
or unauthorized evidence joins fail closed before downstream use.

## Hot Context and Cold Evidence

- hot model context contains only facts needed for the current decision,
  bounded evidence summaries, stable refs, and explicit constraints;
- cold Workspace/spec evidence retains full records, raw traces, artifacts,
  metadata, and audit history for scoped readback;
- a ContextPackage is a bounded carrier, not permission to copy an entire
  Workspace or conversation into every prompt;
- progressive readback should request the smallest authorized snippet that can
  resolve the current uncertainty.

Do not repeatedly inject full metadata “just in case.” Record compact previews,
sizes, truncation state, and the ref needed to retrieve more.

## Trusted Selection Key and Canonical Join

Project each candidate as:

```json
{
  "selection_key": "c3",
  "task_relevant_facts": {
    "title": "...",
    "evidence_summary": "..."
  }
}
```

Declare `selection_key` as a required string constrained to the offered key
set. Reject unknown keys and disallowed duplicate keys. After parsing, host code
performs the canonical lookup and restores all other identifiers and metadata.

The short key is an application-local projection, not a second canonical
identity. Never ask the model to reproduce several opaque ids, unrelated
`meta`, URLs, or complete records merely to join later.

## Resource, Snapshot, and Ref Identity

Distinguish:

- resource identity: the durable logical object;
- snapshot identity: one content/version observation of that resource;
- ref identity: an authorized handle to bounded content or metadata;
- content digest/version: evidence that the underlying bytes or record changed.

When content changes, create or record a new snapshot/version and invalidate
stale derived context. Do not silently reuse an old summary under a stable ref.

## Retrieval Citation Boundary

Give the model one short trusted `ref_id` or existing evidence `cite_as` for
each selected source. Ask it to cite application tokens such as
`[[ref:r1]]`. Host code must:

1. parse tokens and validate them against the offered ref map;
2. authorize the source projection;
3. render safe link/label output;
4. separately emit approved source-card data for hover cards or attached lists.

Keep source URLs, paths, credentials, and full retrieval metadata host-side.
Do not use bare `${ref_id}` because `${...}` belongs to Agently prompt and
TaskDAG placeholder families.

## Evidence Grounding Chain

When a capability or Action produces proof, preserve a chain equivalent to:

```text
Action observation
-> EvidenceEnvelope.evidence_items
-> bounded evidence summary / cite_as
-> model claim or verifier judgment
-> authorized consumer
```

Each evidence item should make origin, scope, freshness, content/ref, and
authorization inspectable. Action execution evidence is stronger than prose
claiming that an action ran. A model statement that it wrote, read, searched, or
called something is not proof by itself.

## Evidence Delivery Semantics

Define these states explicitly at each consumer edge:

| State | Meaning | Consumer behavior |
|---|---|---|
| `ref_only` | content remains behind an authorized ref | read back only when needed |
| bounded | complete within declared size | consume with provenance |
| truncated | preview is incomplete | do not infer absent content; request more |
| failed | retrieval/action did not produce trusted evidence | fail closed or retry owner mechanism |
| empty | successful lookup found no matching evidence | distinguish from failure and missing capability |

Preserve the difference between “no evidence exists,” “evidence was not read,”
“read failed,” and “the preview was truncated.”

## Retention and Compaction

- retain canonical records, refs, lineage anchors, and verification-critical
  evidence according to domain policy;
- compact repeated prompts, large payloads, and raw logs into bounded summaries
  while preserving refs and content/version facts;
- remove or invalidate stale snapshots and derived packages when source content
  changes;
- keep audit evidence long enough to verify reported causes and A/B comparisons;
- redact secrets, personal data, provider auth, and unauthorized source fields.

## Fail-Closed Checklist

Fail closed when a required capability is unavailable, a selection key was not
offered, a ref cannot be authorized or resolved, evidence provenance is absent,
a snapshot is stale for the decision, a required join has missing branches, or
an Action claim lacks execution evidence. Return a structured diagnostic naming
the missing owner fact; do not substitute a plausible model guess.

Use `agently-request` for exact retrieval and citation-token mechanics and
`agently-runtime` for Workspace, Action, EvidenceEnvelope, and resource APIs.
