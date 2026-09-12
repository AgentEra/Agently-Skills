#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from pathlib import Path
from typing import Literal

from dotenv import find_dotenv, load_dotenv

from agently import Agently, TriggerFlow


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "validate" / "fixtures" / "reference_retrieval_cases.json"
SKILLS = ROOT / "skills"
MAX_EXCERPT_CHARS = 2400
MAX_ANCHORED_MARKDOWN_CHARS = 3200
MARKDOWN_HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+\S")
MARKDOWN_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def configure_deepseek() -> bool:
    load_dotenv(find_dotenv())
    base_url = os.environ.get("DEEPSEEK_BASE_URL")
    model = os.environ.get("DEEPSEEK_DEFAULT_MODEL")
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not all([base_url, model, api_key]):
        return False
    Agently.set_settings(
        "OpenAICompatible",
        {
            "base_url": base_url,
            "model": model,
            "auth": api_key,
            "request_options": {"temperature": 0},
        },
    )
    return True


def check(name: str, condition: bool, details: str, failures: list[str], passes: list[str]) -> None:
    if condition:
        passes.append(f"{name}: {details}")
    else:
        failures.append(f"{name}: {details}")


def load_cases() -> list[dict]:
    data = json.loads(FIXTURES.read_text(encoding="utf-8"))
    return data.get("cases", [])


def list_candidate_paths(skill_name: str) -> list[Path]:
    skill_dir = SKILLS / skill_name
    candidates: list[Path] = [skill_dir / "SKILL.md"]
    for subdir in ("references", "examples"):
        target_dir = skill_dir / subdir
        if not target_dir.exists():
            continue
        for path in sorted(target_dir.rglob("*")):
            if (
                not path.is_file()
                or path.name in {".gitkeep", ".DS_Store"}
                or "__pycache__" in path.parts
                or path.suffix == ".pyc"
            ):
                continue
            candidates.append(path)
    return candidates


def build_candidate_docs(case: dict) -> list[tuple[str, str]]:
    seen: set[str] = set()
    docs: list[tuple[str, str]] = []
    declared_anchors = case.get("excerpt_anchors", {})
    anchors_by_path = declared_anchors if isinstance(declared_anchors, dict) else {}
    for skill_name in case["matched_skills"]:
        for path in list_candidate_paths(skill_name):
            rel_path = path.relative_to(ROOT).as_posix()
            if rel_path in seen:
                continue
            seen.add(rel_path)
            path_anchors = anchors_by_path.get(rel_path, [])
            anchors = (
                [anchor for anchor in path_anchors if isinstance(anchor, str) and anchor]
                if isinstance(path_anchors, list)
                else []
            )
            docs.append((rel_path, build_excerpt(path, anchors=anchors)))
    return docs


def markdown_section_bounds(text: str, anchor: str) -> tuple[int, int] | None:
    anchor_offset = text.find(anchor)
    if anchor_offset < 0:
        return None

    lines = text.splitlines(keepends=True)
    headings: list[tuple[int, int, int]] = []
    offset = 0
    open_fence: tuple[str, int] | None = None
    for line_index, line in enumerate(lines):
        fence = MARKDOWN_FENCE.match(line)
        if fence:
            marker = fence.group(1)
            if open_fence is None:
                open_fence = (marker[0], len(marker))
            elif marker[0] == open_fence[0] and len(marker) >= open_fence[1]:
                open_fence = None
        heading = MARKDOWN_HEADING.match(line) if open_fence is None and fence is None else None
        if heading is not None:
            headings.append((line_index, offset, len(heading.group(1))))
        offset += len(line)

    containing_heading: tuple[int, int, int] | None = None
    for heading in headings:
        if heading[1] > anchor_offset:
            break
        containing_heading = heading

    if containing_heading is None:
        end = headings[0][1] if headings else len(text)
        return (0, end)

    heading_index, start, level = containing_heading
    end = len(text)
    for next_index, next_offset, next_level in headings:
        if next_index > heading_index and next_level <= level:
            end = next_offset
            break
    return (start, end)


def build_markdown_section_excerpt(text: str, anchors: list[str]) -> str:
    selected_bounds = {
        bounds
        for anchor in anchors
        if (bounds := markdown_section_bounds(text, anchor)) is not None
    }
    if not selected_bounds:
        return text[:MAX_EXCERPT_CHARS].rstrip() + ("\n..." if len(text) > MAX_EXCERPT_CHARS else "")

    sections = [text[start:end].rstrip() for start, end in sorted(selected_bounds)]
    excerpt = "\n\n...\n\n".join(sections)
    if len(excerpt) > MAX_ANCHORED_MARKDOWN_CHARS:
        excerpt = excerpt[:MAX_ANCHORED_MARKDOWN_CHARS].rstrip() + "\n..."
    return excerpt


def build_excerpt(path: Path, *, anchors: list[str] | None = None) -> str:
    text = path.read_text(encoding="utf-8")
    if anchors and path.suffix.lower() in {".md", ".markdown"}:
        return build_markdown_section_excerpt(text, anchors)

    lines = text.splitlines()
    if path.suffix in {".py", ".json"}:
        clipped = "\n".join(lines[:80])
    else:
        clipped = "\n".join(lines[:120])
    if len(clipped) > MAX_EXCERPT_CHARS:
        clipped = clipped[:MAX_EXCERPT_CHARS].rstrip() + "\n..."
    return clipped


def normalize_string_list(values: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = str(value).strip().strip("`")
        if item and item not in seen:
            normalized.append(item)
            seen.add(item)
    return normalized


async def judge_case(case: dict, *, max_retries: int) -> dict:
    candidate_docs = build_candidate_docs(case)
    candidate_paths = [path for path, _ in candidate_docs]
    docs_block = "\n\n".join(
        f"[FILE] {path}\n{excerpt}"
        for path, excerpt in candidate_docs
    )
    concept_block = "\n".join(
        f"- {concept['id']}: {concept['description']}"
        for concept in case["concepts"]
    )
    allowed_paths = ", ".join(candidate_paths)
    allowed_concepts = ", ".join(concept["id"] for concept in case["concepts"])

    prompt = (
        "You are simulating post-route supporting-document retrieval for a coding agent.\n"
        "Routing is already complete. Do not re-route the problem.\n"
        f"The matched skills are: {', '.join(case['matched_skills'])}.\n"
        "Choose which repository files should be opened first to answer the user accurately.\n"
        "Prefer a specific reference over a generic overview when it directly owns the needed detail.\n"
        "Prefer examples when the user asks for a concrete implementation pattern.\n"
        "Prefer SKILL.md when the question is mainly about skill boundary, routing, or anti-patterns.\n"
        "Choose 1 to 4 files only.\n"
        "Only mark a concept as covered when at least one selected file directly supports it.\n\n"
        f"User request:\n{case['query']}\n\n"
        "Allowed concept ids:\n"
        f"{concept_block}\n\n"
        "Candidate files with excerpts:\n"
        f"{docs_block}\n\n"
        f"Every selected path must be exactly one of: {allowed_paths}.\n"
        f"Every covered concept must be exactly one of: {allowed_concepts}.\n"
    )

    agent = Agently.create_agent(f"v3-reference-retrieval-{case['id']}")
    result = (
        agent.input(prompt)
        .output(
            {
                "decision": (
                    Literal["sure", "unsure"],
                    "Use sure only when the selected files directly support the request.",
                    True,
                ),
                "selected_paths": [(str, f"Exact repo-relative path. Must be one of: {allowed_paths}.", True)],
                "covered_concepts": [(str, f"Exact concept id. Must be one of: {allowed_concepts}.", True)],
                "reason": (str, "Short reason for the chosen supporting files.", True),
                "evidence": [(str, "Short file-based evidence for the chosen files.", True)],
            }
        )
        .get_result()
    )
    data = await result.async_get_data(max_retries=max_retries)
    data["decision"] = str(data["decision"]).strip().lower()
    data["selected_paths"] = normalize_string_list(data["selected_paths"])
    data["covered_concepts"] = normalize_string_list(data["covered_concepts"])
    return data


async def validate_live_case(
    case: dict,
    *,
    timeout_seconds: int,
    max_retries: int,
) -> dict:
    case_name = f"reference_{case['id']}"
    try:
        judged = await asyncio.wait_for(
            judge_case(case, max_retries=max_retries),
            timeout=timeout_seconds,
        )
    except TimeoutError:
        return {"name": case_name, "ok": False, "details": f"timed out after {timeout_seconds}s"}
    except Exception as exc:
        return {"name": case_name, "ok": False, "details": f"raised {type(exc).__name__}: {exc}"}

    candidate_paths = {path for path, _ in build_candidate_docs(case)}
    selected = judged["selected_paths"]
    selected_set = set(selected)
    required_concepts = set(case["required_concepts"])
    covered_concepts = set(judged["covered_concepts"])
    expected_sets = [set(paths) for paths in case["expected_reference_sets"]]

    ok = (
        judged["decision"] == "sure"
        and 1 <= len(selected) <= 4
        and selected_set.issubset(candidate_paths)
        and any(expected.issubset(selected_set) for expected in expected_sets)
        and required_concepts.issubset(covered_concepts)
    )
    return {
        "name": case_name,
        "ok": ok,
        "details": (
            f"expected_reference_sets={case['expected_reference_sets']} selected={selected} "
            f"required_concepts={case['required_concepts']} covered_concepts={judged['covered_concepts']} "
            f"decision={judged['decision']} reason={judged['reason']} evidence={judged['evidence']}"
        ),
    }


async def run_live_validation(
    failures: list[str],
    passes: list[str],
    *,
    timeout_seconds: int,
    concurrency: int,
    max_retries: int,
) -> None:
    flow = TriggerFlow(name="v3-reference-retrieval-validation")

    async def validate_in_flow(data):
        return await validate_live_case(
            data.value,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
        )

    @flow.chunk("store_results")
    async def store_results(data):
        await data.async_set_state("results", data.input)
        return data.input

    flow.for_each(concurrency=concurrency).to(validate_in_flow).end_for_each().to(store_results)
    execution = flow.create_execution(auto_close=False)
    await execution.async_start(load_cases())
    state = await execution.async_close()
    results = state["results"]
    for result in results:
        check(result["name"], result["ok"], result["details"], failures, passes)


def run_static_checks(failures: list[str], passes: list[str]) -> None:
    cases = load_cases()
    check("reference_cases_present", bool(cases), "reference retrieval fixtures contain cases", failures, passes)
    for case in cases:
        case_id = case.get("id", "<missing-id>")
        matched_skills = case.get("matched_skills")
        expected_sets = case.get("expected_reference_sets")
        excerpt_anchors = case.get("excerpt_anchors", {})
        concepts = case.get("concepts")
        required_concepts = case.get("required_concepts")

        check(
            f"{case_id}_shape",
            (
                isinstance(case.get("query"), str)
                and isinstance(matched_skills, list)
                and isinstance(expected_sets, list)
                and isinstance(excerpt_anchors, dict)
                and isinstance(concepts, list)
                and isinstance(required_concepts, list)
                and bool(expected_sets)
                and bool(concepts)
            ),
            "case has query, matched_skills, expected reference sets, excerpt anchors, and concepts",
            failures,
            passes,
        )
        if not isinstance(matched_skills, list) or not isinstance(expected_sets, list) or not isinstance(concepts, list):
            continue

        check(
            f"{case_id}_skills_exist",
            all((SKILLS / skill_name).exists() for skill_name in matched_skills),
            "all matched skills exist",
            failures,
            passes,
        )

        candidate_docs = dict(build_candidate_docs(case))
        candidate_paths = set(candidate_docs)
        for idx, expected in enumerate(expected_sets):
            check(
                f"{case_id}_expected_set_{idx}",
                isinstance(expected, list) and bool(expected) and all(path in candidate_paths for path in expected),
                "expected reference set points to candidate files inside matched skills",
                failures,
                passes,
            )

        anchors_shape_ok = isinstance(excerpt_anchors, dict) and all(
            isinstance(path, str)
            and bool(path)
            and isinstance(anchors, list)
            and bool(anchors)
            and all(isinstance(anchor, str) and bool(anchor) for anchor in anchors)
            and len(anchors) == len(set(anchors))
            for path, anchors in excerpt_anchors.items()
        )
        check(
            f"{case_id}_excerpt_anchors_shape",
            anchors_shape_ok,
            "excerpt anchors map candidate paths to unique non-empty strings",
            failures,
            passes,
        )
        if anchors_shape_ok:
            for rel_path, anchors in excerpt_anchors.items():
                path = ROOT / rel_path
                anchor_path_ok = rel_path in candidate_paths and path.is_file()
                check(
                    f"{case_id}_{rel_path}_anchor_path",
                    anchor_path_ok,
                    "anchor path exists and belongs to the matched-skill candidates",
                    failures,
                    passes,
                )
                full_text = path.read_text(encoding="utf-8") if anchor_path_ok else ""
                check(
                    f"{case_id}_{rel_path}_anchors_in_source",
                    all(anchor in full_text for anchor in anchors),
                    "every declared excerpt anchor exists in the full source file",
                    failures,
                    passes,
                )
                excerpt = candidate_docs.get(rel_path, "")
                check(
                    f"{case_id}_{rel_path}_anchors_delivered",
                    all(anchor in excerpt for anchor in anchors),
                    "every declared excerpt anchor is present in the delivered candidate excerpt",
                    failures,
                    passes,
                )

        concept_ids = [concept.get("id") for concept in concepts if isinstance(concept, dict)]
        check(
            f"{case_id}_concept_ids",
            len(concept_ids) == len(set(concept_ids)) and all(isinstance(item, str) and item for item in concept_ids),
            "concept ids are unique and non-empty",
            failures,
            passes,
        )
        check(
            f"{case_id}_required_concepts",
            isinstance(required_concepts, list) and set(required_concepts).issubset(set(concept_ids)),
            "required concepts are declared in the concept list",
            failures,
            passes,
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run V3 post-route reference retrieval validation.")
    parser.add_argument(
        "--allow-model-calls",
        action="store_true",
        help=(
            "Explicitly authorize model-backed cases. Without this flag the "
            "validator runs static checks only."
        ),
    )
    parser.add_argument(
        "--max-model-requests",
        type=int,
        help=(
            "Required with --allow-model-calls. Must cover the declared "
            "worst-case request budget before any model configuration is loaded."
        ),
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=1,
        help="Maximum retries per model-backed case (default: 1).",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=60,
        help="Per-request timeout for model-backed reference retrieval validation.",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=4,
        help="Concurrent TriggerFlow workers for reference retrieval validation.",
    )
    return parser


def model_validation_authorized(args: argparse.Namespace) -> bool:
    return bool(
        args.allow_model_calls
        and args.max_model_requests is not None
        and args.max_model_requests > 0
    )


async def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    passes: list[str] = []
    failures: list[str] = []
    run_static_checks(failures, passes)

    if args.allow_model_calls:
        if not model_validation_authorized(args):
            failures.append(
                "model_authorization: --allow-model-calls requires a positive "
                "--max-model-requests budget"
            )
        elif args.max_retries < 0:
            failures.append("model_authorization: --max-retries must be non-negative")
        else:
            worst_case_requests = len(load_cases()) * (1 + args.max_retries)
            if worst_case_requests > args.max_model_requests:
                failures.append(
                    "model_authorization: declared budget "
                    f"{args.max_model_requests} is below worst-case request count "
                    f"{worst_case_requests}"
                )
            elif configure_deepseek():
                await run_live_validation(
                    failures,
                    passes,
                    timeout_seconds=args.timeout_seconds,
                    concurrency=args.concurrency,
                    max_retries=args.max_retries,
                )
            else:
                failures.append(
                    "deepseek_env: model calls were authorized but one or more "
                    "required vars are missing: DEEPSEEK_BASE_URL, "
                    "DEEPSEEK_DEFAULT_MODEL, DEEPSEEK_API_KEY"
                )
    else:
        passes.append(
            "model_authorization: skipped model-backed retrieval; explicit "
            "--allow-model-calls and --max-model-requests are required"
        )

    print("V3 reference retrieval validation")
    print(f"passes: {len(passes)}")
    for item in passes:
        print(f"PASS  {item}")
    print(f"failures: {len(failures)}")
    for item in failures:
        print(f"FAIL  {item}")
    if failures:
        raise SystemExit(1)


def run(argv: list[str] | None = None) -> None:
    asyncio.run(main(sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    run()
