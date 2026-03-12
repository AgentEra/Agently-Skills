#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "agently-model-request-playbook"
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
            "name: agently-model-request-playbook" in block,
            "frontmatter name matches the directory name",
            failures,
            passes,
        )
        check(
            "description_routes_request_domain",
            ("single request" in block or "short request chain" in block)
            and ("understanding" in block or "rewriting" in block or "generation" in block or "validation reports" in block)
            and ("tools" in block or "FastAPI exposure" in block or "RAG" in block),
            "frontmatter description marks this skill as the request-domain router through scenario-led language",
            failures,
            passes,
        )

    referenced_files = [
        SKILL_DIR / "references" / "source-map.md",
        SKILL_DIR / "references" / "standard-request-path.md",
        SKILL_DIR / "references" / "high-quality-request-path.md",
        SKILL_DIR / "references" / "ownership-and-escalation.md",
        SKILL_DIR / "references" / "common-business-patterns.md",
        SKILL_DIR / "references" / "current-skill-map.md",
    ]
    check(
        "reference_files_exist",
        all(path.exists() for path in referenced_files),
        "referenced routing files exist",
        failures,
        passes,
    )

    skill_map = (SKILL_DIR / "references" / "current-skill-map.md").read_text(encoding="utf-8")
    expected_skills = [
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
    ]
    check(
        "routing_targets_are_current",
        all((ROOT / "skills" / skill).exists() for skill in expected_skills)
        and all(skill in skill_map for skill in expected_skills),
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
            "trigger_fixture_covers_model_request_playbook",
            any(case.get("should_trigger") == "agently-model-request-playbook" for case in fixtures),
            "trigger fixtures include a case won by agently-model-request-playbook",
            failures,
            passes,
        )
        check(
            "trigger_fixture_covers_generic_request_query",
            any(case.get("id") == "router-one-request-generic-domain-known" for case in fixtures),
            "trigger fixtures include a generic single-request query",
            failures,
            passes,
        )

    public_markdown = [SKILL_MD, *referenced_files]
    contains_cjk = any(re.search(r"[\u4e00-\u9fff]", path.read_text(encoding="utf-8")) for path in public_markdown)
    check(
        "english_only_public_markdown",
        not contains_cjk,
        "public model-request playbook Markdown is English-only",
        failures,
        passes,
    )

    print("Agently model-request-playbook validation")
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
