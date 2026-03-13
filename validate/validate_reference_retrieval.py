#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
from typing import Literal

from dotenv import find_dotenv, load_dotenv

from agently import Agently, TriggerFlow


load_dotenv(find_dotenv())
ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "validate" / "fixtures" / "reference_retrieval_cases.json"
SKILLS = ROOT / "skills"


def configure_deepseek() -> bool:
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
            if not path.is_file() or path.name == ".gitkeep":
                continue
            candidates.append(path)
    return candidates


def build_candidate_docs(case: dict) -> list[tuple[str, str]]:
    seen: set[str] = set()
    docs: list[tuple[str, str]] = []
    for skill_name in case["matched_skills"]:
        for path in list_candidate_paths(skill_name):
            rel_path = path.relative_to(ROOT).as_posix()
            if rel_path in seen:
                continue
            seen.add(rel_path)
            docs.append((rel_path, build_excerpt(path)))
    return docs


def build_excerpt(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if path.suffix in {".py", ".json"}:
        clipped = "\n".join(lines[:80])
    else:
        clipped = "\n".join(lines[:120])
    if len(clipped) > 2400:
        clipped = clipped[:2400].rstrip() + "\n..."
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


async def judge_case(case: dict) -> dict:
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

    agent = Agently.create_agent(f"v2-reference-retrieval-{case['id']}")
    response = (
        agent.input(prompt)
        .output(
            {
                "decision": (
                    Literal["sure", "unsure"],
                    "Use sure only when the selected files directly support the request.",
                ),
                "selected_paths": [(str, f"Exact repo-relative path. Must be one of: {allowed_paths}.")],
                "covered_concepts": [(str, f"Exact concept id. Must be one of: {allowed_concepts}.")],
                "reason": (str, "Short reason for the chosen supporting files."),
                "evidence": [(str, "Short file-based evidence for the chosen files.")],
            }
        )
        .get_response()
    )
    data = await response.result.async_get_data(
        ensure_keys=["decision", "selected_paths[*]", "covered_concepts[*]", "reason", "evidence[*]"],
        max_retries=1,
    )
    data["decision"] = str(data["decision"]).strip().lower()
    data["selected_paths"] = normalize_string_list(data["selected_paths"])
    data["covered_concepts"] = normalize_string_list(data["covered_concepts"])
    return data


async def validate_live_case(case: dict, *, timeout_seconds: int) -> dict:
    case_name = f"reference_{case['id']}"
    try:
        judged = await asyncio.wait_for(judge_case(case), timeout=timeout_seconds)
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
) -> None:
    flow = TriggerFlow(name="v2-reference-retrieval-validation")

    async def validate_in_flow(data):
        return await validate_live_case(data.value, timeout_seconds=timeout_seconds)

    flow.for_each(concurrency=concurrency).to(validate_in_flow).end_for_each().end()
    results = await flow.async_start(load_cases())
    for result in results:
        check(result["name"], result["ok"], result["details"], failures, passes)


def run_static_checks(failures: list[str], passes: list[str]) -> None:
    cases = load_cases()
    check("reference_cases_present", bool(cases), "reference retrieval fixtures contain cases", failures, passes)
    for case in cases:
        case_id = case.get("id", "<missing-id>")
        matched_skills = case.get("matched_skills")
        expected_sets = case.get("expected_reference_sets")
        concepts = case.get("concepts")
        required_concepts = case.get("required_concepts")

        check(
            f"{case_id}_shape",
            (
                isinstance(case.get("query"), str)
                and isinstance(matched_skills, list)
                and isinstance(expected_sets, list)
                and isinstance(concepts, list)
                and isinstance(required_concepts, list)
                and bool(expected_sets)
                and bool(concepts)
            ),
            "case has query, matched_skills, expected reference sets, and concepts",
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

        candidate_paths = {path for path, _ in build_candidate_docs(case)}
        for idx, expected in enumerate(expected_sets):
            check(
                f"{case_id}_expected_set_{idx}",
                isinstance(expected, list) and bool(expected) and all(path in candidate_paths for path in expected),
                "expected reference set points to candidate files inside matched skills",
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


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run V2 post-route reference retrieval validation.")
    parser.add_argument("--require-model", action="store_true", help="Fail if DeepSeek settings are missing.")
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
    args = parser.parse_args()

    passes: list[str] = []
    failures: list[str] = []
    run_static_checks(failures, passes)

    if configure_deepseek():
        await run_live_validation(
            failures,
            passes,
            timeout_seconds=args.timeout_seconds,
            concurrency=args.concurrency,
        )
    else:
        missing = ["DEEPSEEK_BASE_URL", "DEEPSEEK_DEFAULT_MODEL", "DEEPSEEK_API_KEY"]
        if args.require_model:
            failures.append(f"deepseek_env: missing one or more required vars {missing}")
        else:
            passes.append(f"deepseek_env: skipped model-backed retrieval because vars are not fully set {missing}")

    print("V2 reference retrieval validation")
    print(f"passes: {len(passes)}")
    for item in passes:
        print(f"PASS  {item}")
    print(f"failures: {len(failures)}")
    for item in failures:
        print(f"FAIL  {item}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
