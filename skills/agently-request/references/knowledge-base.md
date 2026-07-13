# Agently Knowledge Base

Use this skill when embeddings, Workspace recall, and retrieval are the main
capability surface.

## Native-First Rules

- prefer embedding-agent plus Chroma integration before custom vector plumbing
- use `workspace.retrieve(...)` for shared intelligent retrieval over Workspace
  records and files: keyword/tag candidates, `method="auto"` candidate-strategy
  selection, optional vector/hybrid mode,
  structure-gated model rerank over a bounded candidate-summary window,
  dropped-candidate refill, length-budget or `top_n` packaging, and compact
  selected-record representation packaging with `projection`/`original_ref`
  metadata. Default `record_representation="auto"` preserves short structured
  records as compact structure, omits cold fields such as `audit`,
  `source_system`, `tags`, and `noise` from the model-hot package, projects
  long/noisy records, and leaves raw Workspace records available for readback
- for multi-turn task information already stored in Workspace, prefer
  `workspace.build_context(goal=..., scope=..., budget=..., profile=...)` so
  ContextPlanner, Retriever, and ContextBuilder plugins own the retrieval path
- use `workspace.grep(...)` and `workspace.grep_files(...)` for low-level
  deterministic debugging or explicit filters, not as the normal app-facing
  recall API. `workspace.search(...)` and `workspace.search_files(...)` keep
  compatibility return shapes while automatically choosing deterministic grep
  or retrieval packaging internally
- keep candidate retrieval strategy and rerank separate. `method="auto"` chooses
  keyword versus hybrid from Workspace retrieval policy; `rerank=None` uses the
  structural rerank gate and does not become mandatory just because embeddings
  are configured
- if vector mode is requested and the backend only has `NoopVectorIndex`, expect
  deterministic fallback plus diagnostics rather than silent failure
- the default local Workspace backend keeps `NoopVectorIndex`; provider-specific
  embedding clients belong in business code, custom backends, or plugins that
  install a backend `vector_index`. Workspace core does not own the embedding
  provider. If callers install the built-in `LocalVectorIndex(embedder)`, the
  default similarity formula is cosine; dot product and L2 are explicit
  options. Custom vector indexes own their own distance formula
- use `workspace.get_data(...)` for structured records/checkpoints and
  `workspace.links(...)` for decision/evidence lineage when retrieval feeds a
  later loop step
- separate indexing, retrieval, and answer generation concerns
- keep retrieval results explicit when they feed a later request

## Retrieval Reference Rendering

For a natural-language answer that cites retrieval results, keep complete source
records in host code. Project only one short trusted `ref_id` plus relevant
title/snippet facts into the model request. Require inline
`[[ref:<ref_id>]]` tokens such as `[[ref:r1]]`; AgentTask callers can reuse an
evidence-ledger `cite_as` such as `e1` as the token id.

Do not use bare `${ref_id}` because `${...}` already belongs to Agently prompt
and TaskDAG placeholder families. `[[ref:...]]` is an application rendering
protocol, not a new framework placeholder or Workspace API.

```python
from __future__ import annotations

import re
from collections.abc import Awaitable, Callable, Mapping, Sequence
from typing import Any
from urllib.parse import urlparse

from agently import Agently


REF_TOKEN = re.compile(r"\[\[ref:([A-Za-z0-9._:-]+)\]\]")


def prepare_refs(
    records: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, str]], dict[str, dict[str, Any]]]:
    refs_by_id: dict[str, dict[str, Any]] = {}
    model_refs: list[dict[str, str]] = []
    for index, record in enumerate(records, start=1):
        ref_id = f"r{index}"
        refs_by_id[ref_id] = {**dict(record), "ref_id": ref_id}
        model_refs.append({
            "ref_id": ref_id,
            "title": str(record.get("title", "")),
            "snippet": str(record.get("snippet", "")),
        })
    return model_refs, refs_by_id


def build_source_card(record: Mapping[str, Any]) -> dict[str, Any]:
    # Extend this explicit frontend contract; never emit the raw provider record.
    fields = ("ref_id", "title", "url", "snippet", "source_name", "published_at")
    return {field: record[field] for field in fields if field in record}


def trusted_http_url(value: Any) -> str:
    url = str(value)
    if urlparse(url).scheme not in {"http", "https"}:
        raise ValueError(f"unsupported source URL: {url}")
    return url


def render_refs(
    answer: str,
    refs_by_id: Mapping[str, Mapping[str, Any]],
) -> tuple[str, list[dict[str, Any]]]:
    used_ids: list[str] = []

    def replace(match: re.Match[str]) -> str:
        ref_id = match.group(1)
        record = refs_by_id.get(ref_id)
        if record is None:
            raise ValueError(f"unknown retrieval ref: {ref_id}")
        used_ids.append(ref_id)
        label = str(record.get("title") or ref_id).replace("\\", "\\\\").replace("]", "\\]")
        return f"[{label}]({trusted_http_url(record.get('url'))})"

    rendered = REF_TOKEN.sub(replace, answer)
    unique_ids = list(dict.fromkeys(used_ids))
    return rendered, [build_source_card(refs_by_id[ref_id]) for ref_id in unique_ids]


async def answer_with_refs(
    question: str,
    retrieved_records: Sequence[Mapping[str, Any]],
    emit: Callable[[dict[str, Any]], Awaitable[None]],
) -> None:
    model_refs, refs_by_id = prepare_refs(retrieved_records)

    def validate_refs(data: dict[str, Any], _ctx: Any) -> bool | dict[str, Any]:
        cited_ids = REF_TOKEN.findall(data.get("answer", ""))
        if not cited_ids:
            return {"ok": False, "reason": "answer must cite at least one offered ref"}
        unknown = {
            ref_id
            for ref_id in cited_ids
            if ref_id not in refs_by_id
        }
        return True if not unknown else {
            "ok": False,
            "reason": f"unknown refs: {sorted(unknown)}",
        }

    result = (
        Agently.create_request("retrieval-reference-answer")
        .input({"question": question, "retrieval_results": model_refs})
        .instruct([
            "Answer from retrieval_results.",
            "Cite sources as [[ref:<ref_id>]] using only offered ref_id values.",
            "Do not copy URLs or hidden source metadata into the answer.",
        ])
        .output({
            "answer": (str, "Answer with inline [[ref:<ref_id>]] citations", True),
        })
        .validate(validate_refs)
        .get_result()
    )

    # No progressive consumer: read the final object directly.
    data = await result.async_get_data()
    rendered_answer, source_cards = render_refs(data["answer"], refs_by_id)
    await emit({"type": "answer", "text": rendered_answer})
    await emit({"type": "retrieval_refs", "items": source_cards})
```

The regex above parses a deterministic token protocol; it does not decide
source relevance or answer quality. The model owns citation choice, while host
code owns id validation, safe link construction, authorized source-card
transport, and frontend rendering as a link plus hover card, source list, or
attached result card.

## Anti-Patterns

- do not hide KB retrieval inside unrelated prompt logic
- do not ask the model to reproduce full URLs or source metadata when a trusted
  ref token plus host-side lookup can carry the citation
- do not treat embeddings-only setup and KB-backed answer flow as unrelated stacks
- do not ask business code to hand-write ordinary multi-turn recall filters when
  a Workspace ContextPackage is the right shape
- do not hide structure-gated model rerank, refill, or retrieval budgets inside
  Session memory code when `workspace.retrieve(...)` is the shared substrate

## Read Next

- `references/session-memory.md`
- `references/prompt-management.md`
