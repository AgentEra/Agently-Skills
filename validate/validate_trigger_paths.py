#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "validate" / "fixtures" / "route_cases.json"
SKILLS = ROOT / "skills"
PUBLIC_SKILLS = {
    "agently",
    "agently-design",
    "agently-migration",
    "agently-request",
    "agently-runtime",
    "agently-stage",
    "agently-triggerflow",
}
VALID_LOCALES = {"en", "zh"}
TASKDAG_ROUTE_SKILLS = {"agently", "agently-design", "agently-triggerflow"}
INTENT_GROUP_RULES = {
    "triggerflow-output-efficiency-refactor": (
        4,
        {"owner-unresolved", "response-reuse-explicit", "structured-fanout-explicit", "combo-explicit"},
    ),
    "triggerflow-mixed-sync-async-orchestration": (
        3,
        {"owner-unresolved", "orchestration-explicit", "event-wait-explicit"},
    ),
    "triggerflow-process-clarity-refactor": (
        3,
        {"owner-unresolved", "process-clarity-explicit", "stage-visibility-explicit"},
    ),
    "project-structure-separated-refactor": (
        4,
        {"owner-unresolved", "separation-explicit", "structure-refactor-explicit", "config-bridge-explicit"},
    ),
}


def check(
    name: str,
    condition: bool,
    details: str,
    failures: list[str],
    passes: list[str],
) -> None:
    (passes if condition else failures).append(f"{name}: {details}")


def unique_nonempty_strings(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item for item in value)
        and len(value) == len(set(value))
    )


def main() -> None:
    data = json.loads(FIXTURES.read_text(encoding="utf-8"))
    passes: list[str] = []
    failures: list[str] = []
    cases = data.get("cases", [])
    case_ids = [case.get("id") for case in cases if isinstance(case, dict)]
    scenario_map: dict[str, list[dict]] = {}

    check("cases_present", isinstance(cases, list) and bool(cases), "route fixtures contain cases", failures, passes)
    check("case_ids_unique", len(case_ids) == len(set(case_ids)) and all(isinstance(item, str) and item for item in case_ids), "case ids are unique non-empty strings", failures, passes)

    for case in cases:
        case_id = case.get("id", "<missing-id>")
        scenario_id = case.get("scenario_id")
        locale = case.get("locale")
        intent_style = case.get("intent_style")
        query = case.get("query")
        installed = case.get("installed_skills")
        expected_paths = case.get("expected_route_paths")
        shape_ok = (
            isinstance(scenario_id, str)
            and bool(scenario_id)
            and locale in VALID_LOCALES
            and isinstance(intent_style, str)
            and bool(intent_style)
            and isinstance(query, str)
            and bool(query.strip())
            and unique_nonempty_strings(installed)
            and isinstance(expected_paths, list)
            and bool(expected_paths)
            and all(unique_nonempty_strings(path) and 1 <= len(path) <= 4 for path in expected_paths)
        )
        check(f"{case_id}_shape", shape_ok, "case has bounded, unique route data and scenario metadata", failures, passes)
        if not isinstance(installed, list) or not isinstance(expected_paths, list):
            continue
        if isinstance(scenario_id, str):
            scenario_map.setdefault(scenario_id, []).append(case)

        normalized_paths = [tuple(path) for path in expected_paths if isinstance(path, list)]
        check(f"{case_id}_paths_unique", len(normalized_paths) == len(set(normalized_paths)), "acceptable route paths are unique", failures, passes)
        check(f"{case_id}_installed_public", set(installed).issubset(PUBLIC_SKILLS), "installed skills belong to the public catalog", failures, passes)
        check(f"{case_id}_installed_exist", all((SKILLS / skill).is_dir() for skill in installed), "all installed skills exist", failures, passes)
        check(f"{case_id}_paths_installed", all(set(path).issubset(set(installed)) for path in expected_paths if isinstance(path, list)), "route paths use only installed skills", failures, passes)

    for skill in sorted(PUBLIC_SKILLS):
        direct_cases = {
            case.get("id")
            for case in cases
            if any(path and path[0] == skill for path in case.get("expected_route_paths", []))
        }
        boundary_cases = {
            case.get("id")
            for case in cases
            if any(len(path) > 1 and skill in path for path in case.get("expected_route_paths", []))
        }
        check(f"{skill}_direct_route", bool(direct_cases), "skill has direct route coverage", failures, passes)
        check(f"{skill}_boundary_route", bool(boundary_cases), "skill has multi-skill boundary route coverage", failures, passes)

    taskdag_cases = scenario_map.get("taskdag-dag-execution", [])
    router_parts = (SKILLS / "agently" / "SKILL.md").read_text(
        encoding="utf-8"
    ).split("---", 2)
    router_frontmatter = router_parts[1] if len(router_parts) == 3 else ""
    check(
        "taskdag_router_metadata",
        "TaskDAG" in router_frontmatter,
        "agently frontmatter makes the low-frequency TaskDAG route discoverable",
        failures,
        passes,
    )
    check("taskdag_cases_present", len(taskdag_cases) >= 2, "low-frequency TaskDAG routing has English and Chinese coverage", failures, passes)
    check(
        "taskdag_routes_via_agently",
        bool(taskdag_cases)
        and all(
            all(path and path[0] == "agently" and set(path).issubset(TASKDAG_ROUTE_SKILLS) for path in case.get("expected_route_paths", []))
            for case in taskdag_cases
        ),
        "TaskDAG requests start at agently and use only design or TriggerFlow boundaries",
        failures,
        passes,
    )

    check(
        "generic_non_framework_router_case",
        any(
            any(path == ["agently"] for path in case.get("expected_route_paths", []))
            and "agently" not in case.get("query", "").lower()
            and "triggerflow" not in case.get("query", "").lower()
            for case in cases
        ),
        "unresolved scenarios can discover agently without framework names",
        failures,
        passes,
    )
    check(
        "stage_does_not_take_workflow_owner",
        any(
            case.get("id") == "mixed-sync-async-orchestration-en"
            and "agently-stage" in case.get("installed_skills", [])
            and all(not path or path[0] != "agently-stage" for path in case.get("expected_route_paths", []))
            for case in cases
        ),
        "Stage remains a process-local runtime owner rather than workflow owner",
        failures,
        passes,
    )

    for scenario_id, (minimum, required_styles) in INTENT_GROUP_RULES.items():
        group = scenario_map.get(scenario_id, [])
        styles = {case.get("intent_style") for case in group}
        check(f"{scenario_id}_size", len(group) >= minimum, "intent group has representative phrasings", failures, passes)
        check(f"{scenario_id}_styles", required_styles.issubset(styles), "intent group covers required expression styles", failures, passes)
        check(
            f"{scenario_id}_router_and_leaf",
            any(any(path and path[0] == "agently" for path in case.get("expected_route_paths", [])) for case in group)
            and any(any(path and path[0] != "agently" for path in case.get("expected_route_paths", [])) for case in group),
            "intent group covers unresolved-router and resolved-owner paths",
            failures,
            passes,
        )

    print("V3 trigger fixture validation")
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
