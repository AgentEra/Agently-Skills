#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "validate" / "fixtures" / "route_cases.json"
SKILLS = ROOT / "skills"


def check(name: str, condition: bool, details: str, failures: list[str], passes: list[str]) -> None:
    if condition:
        passes.append(f"{name}: {details}")
    else:
        failures.append(f"{name}: {details}")


def main() -> None:
    data = json.loads(FIXTURES.read_text(encoding="utf-8"))
    passes: list[str] = []
    failures: list[str] = []
    cases = data.get("cases", [])

    check("cases_present", bool(cases), "route fixtures contain cases", failures, passes)

    for case in cases:
        case_id = case.get("id", "<missing-id>")
        query = case.get("query")
        installed = case.get("installed_skills")
        expected_paths = case.get("expected_route_paths")

        check(
            f"{case_id}_shape",
            (
                isinstance(query, str)
                and isinstance(installed, list)
                and isinstance(expected_paths, list)
                and bool(expected_paths)
                and all(isinstance(path, list) and bool(path) for path in expected_paths)
            ),
            "case has query, installed_skills, and expected_route_paths",
            failures,
            passes,
        )
        if not isinstance(installed, list) or not isinstance(expected_paths, list):
            continue

        check(
            f"{case_id}_installed_exist",
            all((SKILLS / skill).exists() for skill in installed),
            "all installed skills exist",
            failures,
            passes,
        )
        check(
            f"{case_id}_expected_installed",
            all(skill in installed for path in expected_paths for skill in path),
            "all acceptable route paths only contain installed skills",
            failures,
            passes,
        )

    check(
        "generic_non_framework_playbook_case",
        any(
            case.get("expected_route_paths") == [["agently-playbook"]]
            and "agently" not in case.get("query", "").lower()
            and "triggerflow" not in case.get("query", "").lower()
            for case in cases
        ),
        "fixtures cover unresolved generic cases without framework-name requirements",
        failures,
        passes,
    )
    check(
        "chinese_quality_validator_case",
        any(
            case.get("id") == "skills-quality-simulator-kickoff-zh"
            and case.get("expected_route_paths") == [["agently-playbook"]]
            and "agently" not in case.get("query", "").lower()
            for case in cases
        ),
        "fixtures cover the Chinese skills-quality-validator kickoff scenario without Agently mention",
        failures,
        passes,
    )
    check(
        "ui_ollama_skill_tool_case",
        any(
            case.get("id") == "skill-creation-tool-ui-ollama-zh"
            and any(path and path[0] == "agently-playbook" for path in case.get("expected_route_paths", []))
            and "agently" not in case.get("query", "").lower()
            for case in cases
        ),
        "fixtures cover the Chinese UI plus local Ollama skill-tool case without Agently mention",
        failures,
        passes,
    )
    check(
        "direct_leaf_cases_present",
        any(
            isinstance(case.get("expected_route_paths"), list)
            and any(path and path[0] != "agently-playbook" for path in case["expected_route_paths"])
            for case in cases
        ),
        "fixtures cover direct leaf discovery without forcing agently-playbook first",
        failures,
        passes,
    )

    print("V2 trigger fixture validation")
    print(f"passes: {len(passes)}")
    for item in passes:
        print(f"PASS  {item}")
    print(f"failures: {len(failures)}")
    for item in failures:
        print(f"FAIL  {item}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
