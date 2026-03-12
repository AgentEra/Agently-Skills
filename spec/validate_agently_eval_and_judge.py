#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "agently-eval-and-judge"
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
            "name: agently-eval-and-judge" in block,
            "frontmatter name matches the directory name",
            failures,
            passes,
        )
        check(
            "description_mentions_eval_boundary",
            ("evaluation" in block or "judge-model" in block or "validator-model" in block)
            and ("rubric" in block or "pass-fail" in block or "scoring" in block)
            and ("review reports" in block or "issue lists" in block or "pairwise comparison" in block),
            "frontmatter describes direct evaluation and judge-model work",
            failures,
            passes,
        )

    referenced_files = [
        SKILL_DIR / "references" / "source-map.md",
        SKILL_DIR / "references" / "judge-and-rubric-recipes.md",
        SKILL_DIR / "references" / "response-shapes.md",
        SKILL_DIR / "references" / "multi-model-boundaries.md",
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
        "routing_mentions_neighbors",
        "agently-model-setup" in text
        and "agently-output-control" in text
        and "agently-multi-agent-patterns" in text
        and "agently-triggerflow-playbook" in text,
        "public skill routes nearby setup, output, multi-agent, and workflow questions to the right neighbors",
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
            "trigger_fixture_covers_eval_skill",
            any(case.get("should_trigger") == "agently-eval-and-judge" for case in fixtures),
            "trigger fixtures include a case won by agently-eval-and-judge",
            failures,
            passes,
        )

    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    check(
        "readme_lists_skill",
        "agently-eval-and-judge" in readme_text,
        "repository README lists the public skill",
        failures,
        passes,
    )

    public_markdown = [SKILL_MD, *referenced_files]
    contains_cjk = any(re.search(r"[\u4e00-\u9fff]", path.read_text(encoding="utf-8")) for path in public_markdown)
    check(
        "english_only_public_markdown",
        not contains_cjk,
        "public eval-and-judge Markdown is English-only",
        failures,
        passes,
    )

    print("Agently eval-and-judge validation")
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
