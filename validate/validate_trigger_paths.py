#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "validate" / "fixtures" / "route_cases.json"
SKILLS = ROOT / "skills"
VALID_LOCALES = {"en", "zh"}
INTENT_GROUP_RULES = {
    "triggerflow-output-efficiency-refactor": {
        "min_cases": 4,
        "required_styles": {
            "owner-unresolved",
            "response-reuse-explicit",
            "structured-fanout-explicit",
            "combo-explicit",
        },
        "require_playbook_led": True,
        "require_direct_combo": True,
    },
    "triggerflow-mixed-sync-async-orchestration": {
        "min_cases": 3,
        "required_styles": {
            "owner-unresolved",
            "orchestration-explicit",
            "event-wait-explicit",
        },
        "require_playbook_led": True,
        "require_direct_combo": True,
    },
    "triggerflow-process-clarity-refactor": {
        "min_cases": 3,
        "required_styles": {
            "owner-unresolved",
            "process-clarity-explicit",
            "stage-visibility-explicit",
        },
        "require_playbook_led": True,
        "require_direct_combo": True,
    },
    "project-structure-separated-refactor": {
        "min_cases": 4,
        "required_styles": {
            "owner-unresolved",
            "separation-explicit",
            "structure-refactor-explicit",
            "config-bridge-explicit",
        },
        "require_playbook_led": True,
        "require_direct_combo": True,
    },
}


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
    scenario_map: dict[str, list[dict]] = {}

    check("cases_present", bool(cases), "route fixtures contain cases", failures, passes)

    for case in cases:
        case_id = case.get("id", "<missing-id>")
        scenario_id = case.get("scenario_id")
        locale = case.get("locale")
        intent_style = case.get("intent_style")
        query = case.get("query")
        installed = case.get("installed_skills")
        expected_paths = case.get("expected_route_paths")

        check(
            f"{case_id}_shape",
            (
                isinstance(scenario_id, str)
                and isinstance(locale, str)
                and isinstance(intent_style, str)
                and isinstance(query, str)
                and isinstance(installed, list)
                and isinstance(expected_paths, list)
                and bool(expected_paths)
                and all(isinstance(path, list) and bool(path) for path in expected_paths)
            ),
            "case has scenario metadata, query, installed_skills, and expected_route_paths",
            failures,
            passes,
        )
        if not isinstance(installed, list) or not isinstance(expected_paths, list):
            continue
        if isinstance(scenario_id, str):
            scenario_map.setdefault(scenario_id, []).append(case)

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
            f"{case_id}_locale",
            locale in VALID_LOCALES,
            "locale is one of the supported route-fixture languages",
            failures,
            passes,
        )
        check(
            f"{case_id}_intent_style",
            isinstance(intent_style, str) and bool(intent_style),
            "intent_style exists for intent-driven routing coverage",
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

    check(
        "intent_grouped_routes_present",
        any(len(group) > 1 for group in scenario_map.values()),
        "fixtures group multiple natural-language expressions under shared scenarios",
        failures,
        passes,
    )

    for scenario_id, rule in INTENT_GROUP_RULES.items():
        group = scenario_map.get(scenario_id, [])
        styles = {case.get("intent_style") for case in group}
        check(
            f"{scenario_id}_min_cases",
            len(group) >= rule["min_cases"],
            "intent group has enough natural-language expressions",
            failures,
            passes,
        )
        check(
            f"{scenario_id}_styles",
            rule["required_styles"].issubset(styles),
            "intent group covers the expected expression styles",
            failures,
            passes,
        )
        check(
            f"{scenario_id}_playbook_led",
            not rule["require_playbook_led"]
            or any(
                any(path and path[0] == "agently-playbook" for path in case.get("expected_route_paths", []))
                for case in group
            ),
            "intent group includes unresolved phrasing that should stop at or start from agently-playbook",
            failures,
            passes,
        )
        check(
            f"{scenario_id}_direct_combo",
            not rule["require_direct_combo"]
            or any(
                any(path and path[0] != "agently-playbook" for path in case.get("expected_route_paths", []))
                for case in group
            ),
            "intent group includes explicit phrasing that should route to a non-playbook path",
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
