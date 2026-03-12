#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "agently-multi-agent-patterns"
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
            "name: agently-multi-agent-patterns" in block,
            "frontmatter name matches the directory name",
            failures,
            passes,
        )
        check(
            "description_mentions_multi_agent",
            ("multi-agent" in block or "specialized agents" in block or "specialist-team" in block)
            and ("planner-worker" in block or "parallel experts" in block or "reviewer-reviser" in block or "generator-judge" in block)
            and ("handoff" in block or "contract" in block or "boundary" in block),
            "frontmatter description covers specialist-team pattern-routing triggers",
            failures,
            passes,
        )

    referenced_files = [
        SKILL_DIR / "references" / "source-map.md",
        SKILL_DIR / "references" / "when-to-use-multi-agent.md",
        SKILL_DIR / "references" / "core-patterns.md",
        SKILL_DIR / "references" / "handoffs-and-boundaries.md",
        SKILL_DIR / "references" / "implementation-routing.md",
        SKILL_DIR / "references" / "troubleshooting.md",
    ]
    check(
        "reference_files_exist",
        all(path.exists() for path in referenced_files),
        "all referenced public files exist",
        failures,
        passes,
    )

    check(
        "not_a_separate_runtime_claim",
        "does not expose a separate multi-agent runtime primitive" in text,
        "public skill keeps multi-agent framed as composed from existing capabilities",
        failures,
        passes,
    )
    check(
        "loop_ownership_guidance_present",
        "TriggerFlow should usually own their order, budgets, and stop conditions" in text,
        "public skill states that explicit specialist loops should be orchestrated by TriggerFlow",
        failures,
        passes,
    )

    implementation_routing = (SKILL_DIR / "references" / "implementation-routing.md").read_text(encoding="utf-8")
    expected_skills = [
        "agently-model-setup",
        "agently-input-composition",
        "agently-output-control",
        "agently-eval-and-judge",
        "agently-tools",
        "agently-mcp",
        "agently-knowledge-base-and-rag",
        "agently-session-memo",
        "agently-prompt-config-files",
        "agently-fastapi-helper",
        "agently-triggerflow-playbook",
        "agently-triggerflow-patterns",
        "agently-triggerflow-subflows",
        "agently-triggerflow-model-integration",
        "agently-triggerflow-state-and-resources",
        "agently-triggerflow-interrupts-and-stream",
    ]
    check(
        "routing_targets_are_current",
        all((ROOT / "skills" / skill).exists() for skill in expected_skills)
        and all(skill in implementation_routing for skill in expected_skills),
        "implementation routing points to currently published supporting skills",
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
            "trigger_fixture_covers_multi_agent_generator_judge_boundary",
            any(case.get("id") == "architecture-generator-judge-pattern" for case in fixtures),
            "trigger fixtures include a generator-judge specialist boundary case",
            failures,
            passes,
        )

    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    check(
        "readme_lists_skill",
        "agently-multi-agent-patterns" in readme_text,
        "repository README lists the new public skill",
        failures,
        passes,
    )

    public_markdown = [SKILL_MD, *referenced_files]
    contains_cjk = any(re.search(r"[\u4e00-\u9fff]", path.read_text(encoding="utf-8")) for path in public_markdown)
    check(
        "english_only_public_markdown",
        not contains_cjk,
        "public multi-agent Markdown is English-only",
        failures,
        passes,
    )

    print("Agently multi-agent-patterns validation")
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
