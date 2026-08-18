# Information, Evidence, and Identity Design

Keep model context task-scoped. Give the model one host-issued trusted selection
key plus relevant facts; host code validates that key and reconstructs canonical
ids, UUIDs, metadata, and records. Keep compact evidence hot and full metadata
or raw records cold behind TaskWorkspace file refs, RecordStore durable refs,
or local spec refs. Unknown keys, refs, snapshots, or unauthorized evidence
joins fail closed before downstream use.

## Hot Context and Cold Evidence

- hot model context contains only facts needed for the current decision,
  bounded evidence summaries, stable refs, and explicit constraints;
- cold TaskWorkspace evidence retains task files and artifacts; RecordStore
  retains durable records, metadata, lineage, and audit facts; local spec
  evidence retains authorized experiment traces and design records;
- a ContextPackage is a bounded carrier, not permission to copy an entire
  TaskWorkspace tree, RecordStore collection, or conversation into every
  prompt;
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

### Freshness Across Request Boundaries

A decision's offered-set membership alone does not prove freshness. If a model
decision can cross a cache, queue, retry, persistence, or replay boundary, use
a request/execution revision binding owned by the Host or issue per-request
opaque keys. Perform Host correlation validation before canonical lookup, then
reconstruct the canonical record from Host state. Prefer Host-bound lineage over
asking the model to copy another request id. A strictly inline response that
cannot cross request boundaries needs no extra model-returned correlation field.

For example, the model may return only `"selection_key": "c3"`; the Host pairs
that output with the current revision or per-request opaque key before lookup.
The key remains an offered-set membership check, while the Host-owned binding
decides whether that membership belongs to the current request.

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
`agently-runtime` for TaskWorkspace, RecordStore, Action, EvidenceEnvelope, and
resource APIs.
