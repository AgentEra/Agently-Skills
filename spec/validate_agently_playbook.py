#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "agently-playbook"
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
            "name: agently-playbook" in block,
            "frontmatter name matches the directory name",
            failures,
            passes,
        )
        check(
            "description_routes_top_level",
            ("model-powered" in block or "assistant" in block or "generator" in block or "evaluator" in block)
            and ("single request" in block or "single-request" in block)
            and ("specialist-agent" in block or "specialized agents" in block or "multi-agent" in block)
            and ("workflow orchestration" in block or "workflow" in block),
            "frontmatter description marks this skill as the top-level scenario router without requiring framework-only trigger words",
            failures,
            passes,
        )

    referenced_files = [
        SKILL_DIR / "references" / "source-map.md",
        SKILL_DIR / "references" / "scenario-router.md",
        SKILL_DIR / "references" / "escalation-ladder.md",
        SKILL_DIR / "references" / "real-world-scenarios.md",
        SKILL_DIR / "references" / "common-solution-recipes.md",
        SKILL_DIR / "references" / "current-skill-map.md",
    ]
    check(
        "reference_files_exist",
        all(path.exists() for path in referenced_files),
        "all referenced public files exist",
        failures,
        passes,
    )

    check(
        "routes_to_domain_playbooks",
        "agently-model-request-playbook" in text
        and "agently-multi-agent-patterns" in text
        and "agently-triggerflow-playbook" in text
        and "top-level scenario-routing entry point" in text,
        "public playbook routes to the current domain entry skills",
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
            "trigger_fixture_covers_playbook",
            any(case.get("should_trigger") == "agently-playbook" for case in fixtures),
            "trigger fixtures include a case won by agently-playbook",
            failures,
            passes,
        )
        check(
            "trigger_fixture_covers_generic_playbook_query",
            any(case.get("id") == "router-cross-domain-generic-model-app-unclear" for case in fixtures),
            "trigger fixtures include a generic non-Agently playbook query",
            failures,
            passes,
        )

    skill_map = (SKILL_DIR / "references" / "current-skill-map.md").read_text(encoding="utf-8")
    expected_skills = [
        "agently-model-request-playbook",
        "agently-model-setup",
        "agently-input-composition",
        "agently-output-control",
        "agently-eval-and-judge",
        "agently-embeddings",
        "agently-tools",
        "agently-mcp",
        "agently-knowledge-base-and-rag",
        "agently-session-memo",
        "agently-prompt-config-files",
        "agently-fastapi-helper",
        "agently-multi-agent-patterns",
        "agently-triggerflow-playbook",
        "agently-triggerflow-orchestration",
        "agently-triggerflow-patterns",
        "agently-triggerflow-state-and-resources",
        "agently-triggerflow-subflows",
        "agently-triggerflow-model-integration",
        "agently-triggerflow-config",
        "agently-triggerflow-execution-state",
        "agently-triggerflow-interrupts-and-stream",
    ]
    check(
        "current_skill_map_is_current",
        all((ROOT / "skills" / skill).exists() for skill in expected_skills)
        and all(skill in skill_map for skill in expected_skills),
        "current skill map points to currently published skills",
        failures,
        passes,
    )

    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    check(
        "readme_lists_skill",
        "agently-playbook" in readme_text,
        "repository README lists the new public skill",
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

    print("Agently playbook validation")
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
