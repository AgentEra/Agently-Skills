#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "agently-triggerflow-playbook"
SKILL_MD = SKILL_DIR / "SKILL.md"
TRIGGER_FIXTURES = ROOT / "spec" / "skill-trigger-fixtures.json"


def check(name: str, condition: bool, details: str, failures: list[str], passes: list[str]):
    if condition:
        passes.append(f"{name}: {details}")
    else:
        failures.append(f"{name}: {details}")


def main():
    passes: list[str] = []
    failures: list[str] = []

    check("skill_exists", SKILL_MD.exists(), "SKILL.md exists", failures, passes)

    text = SKILL_MD.read_text(encoding="utf-8")
    frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    check("frontmatter_present", frontmatter is not None, "frontmatter is present", failures, passes)

    if frontmatter is not None:
        block = frontmatter.group(1)
        check(
            "name_matches_directory",
            "name: agently-triggerflow-playbook" in block,
            "frontmatter name matches the directory name",
            failures,
            passes,
        )
        check(
            "description_routes_triggerflow_domain",
            ("workflow-orchestration" in block or "workflow orchestration" in block)
            and ("concurrency" in block or "resume" in block or "runtime stream" in block or "approvals" in block or "restart-safe" in block),
            "frontmatter description marks this skill as the workflow-orchestration router without requiring TriggerFlow-first wording",
            failures,
            passes,
        )

    referenced_files = [
        SKILL_DIR / "references" / "scenario-router.md",
        SKILL_DIR / "references" / "current-skill-map.md",
    ]
    check(
        "reference_files_exist",
        all(path.exists() for path in referenced_files),
        "referenced routing files exist",
        failures,
        passes,
    )

    current_skill_map = (SKILL_DIR / "references" / "current-skill-map.md").read_text(encoding="utf-8")
    expected_skills = [
        "agently-triggerflow-orchestration",
        "agently-triggerflow-patterns",
        "agently-triggerflow-state-and-resources",
        "agently-triggerflow-subflows",
        "agently-triggerflow-model-integration",
        "agently-multi-agent-patterns",
        "agently-triggerflow-config",
        "agently-triggerflow-execution-state",
        "agently-triggerflow-interrupts-and-stream",
        "agently-model-setup",
        "agently-eval-and-judge",
        "agently-output-control",
        "agently-session-memo",
    ]
    check(
        "routing_targets_are_current",
        all((ROOT / "skills" / skill).exists() for skill in expected_skills)
        and all(skill in current_skill_map for skill in expected_skills),
        "routing targets point to currently published skills",
        failures,
        passes,
    )

    check(
        "trigger_fixtures_exist",
        TRIGGER_FIXTURES.exists(),
        "trigger fixture file exists",
        failures,
        passes,
    )
    if TRIGGER_FIXTURES.exists():
        fixture_data = json.loads(TRIGGER_FIXTURES.read_text(encoding="utf-8"))
        fixtures = fixture_data.get("cases", [])
        check(
            "trigger_fixture_covers_triggerflow_playbook",
            any(case.get("should_trigger") == "agently-triggerflow-playbook" for case in fixtures),
            "trigger fixtures include a case won by agently-triggerflow-playbook",
            failures,
            passes,
        )
        check(
            "trigger_fixture_covers_generic_workflow_query",
            any(case.get("id") == "router-workflow-generic-domain-known" for case in fixtures),
            "trigger fixtures include a generic workflow query",
            failures,
            passes,
        )

    public_markdown = [SKILL_MD, *referenced_files]
    contains_cjk = any(re.search(r"[\u4e00-\u9fff]", path.read_text(encoding="utf-8")) for path in public_markdown)
    check(
        "english_only_public_markdown",
        not contains_cjk,
        "public playbook Markdown is English-only",
        failures,
        passes,
    )

    print("Agently triggerflow-playbook validation")
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
