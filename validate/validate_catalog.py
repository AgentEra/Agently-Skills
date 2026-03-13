#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
ROUTE_FIXTURES = ROOT / "validate" / "fixtures" / "route_cases.json"
EXPECTED_SKILLS = {
    "agently-playbook",
    "agently-model-setup",
    "agently-prompt-management",
    "agently-output-control",
    "agently-model-response",
    "agently-session-memory",
    "agently-agent-extensions",
    "agently-knowledge-base",
    "agently-triggerflow",
    "agently-migration-playbook",
    "agently-langchain-to-agently",
    "agently-langgraph-to-triggerflow",
}
PUBLIC_FILES = [
    ROOT / "README.md",
    ROOT / "README_CN.md",
    ROOT / "AGENTS.md",
    ROOT / "bundles" / "manifest.json",
]
RETIRED_SKILLS = [
    "agently-model-request-playbook",
    "agently-input-composition",
    "agently-tools",
    "agently-mcp",
    "agently-session-memo",
    "agently-prompt-config-files",
    "agently-fastapi-helper",
    "agently-eval-and-judge",
    "agently-embeddings",
    "agently-knowledge-base-and-rag",
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
    "agently-langchain-langgraph-migration-playbook",
]


def check(name: str, condition: bool, details: str, failures: list[str], passes: list[str]) -> None:
    if condition:
        passes.append(f"{name}: {details}")
    else:
        failures.append(f"{name}: {details}")


def main() -> None:
    passes: list[str] = []
    failures: list[str] = []

    check("skills_dir_exists", SKILLS.exists(), "skills directory exists", failures, passes)
    actual_skills = {path.name for path in SKILLS.iterdir() if path.is_dir()}
    check("catalog_exact", actual_skills == EXPECTED_SKILLS, "public catalog matches V2 skill set", failures, passes)

    playbook_text = (SKILLS / "agently-playbook" / "SKILL.md").read_text(encoding="utf-8")
    triggerflow_text = (SKILLS / "agently-triggerflow" / "SKILL.md").read_text(encoding="utf-8")
    check(
        "playbook_framework_name_optional",
        "does not need to mention Agently explicitly" in playbook_text
        and "Generic asks" in playbook_text,
        "playbook explicitly allows scenario-led discovery without framework-name requirements",
        failures,
        passes,
    )
    check(
        "triggerflow_framework_name_optional",
        "does not need to say TriggerFlow or Agently" in triggerflow_text,
        "triggerflow explicitly allows scenario-led discovery without framework-name requirements",
        failures,
        passes,
    )

    for skill_name in sorted(EXPECTED_SKILLS):
        skill_dir = SKILLS / skill_name
        skill_md = skill_dir / "SKILL.md"
        check(f"{skill_name}_skill_md", skill_md.exists(), "SKILL.md exists", failures, passes)
        for subdir in ("references", "examples", "outputs", "scripts"):
            check(
                f"{skill_name}_{subdir}",
                (skill_dir / subdir).exists(),
                f"{subdir} directory exists",
                failures,
                passes,
            )
        if skill_md.exists():
            text = skill_md.read_text(encoding="utf-8")
            frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
            check(f"{skill_name}_frontmatter", frontmatter is not None, "frontmatter exists", failures, passes)
            if frontmatter is not None:
                block = frontmatter.group(1)
                check(
                    f"{skill_name}_name",
                    f"name: {skill_name}" in block,
                    "frontmatter name matches directory",
                    failures,
                    passes,
                )
                check(
                    f"{skill_name}_description",
                    "description:" in block,
                    "frontmatter description exists",
                    failures,
                    passes,
                )
            for ref in re.findall(r"`(references/[^`]+)`", text):
                check(
                    f"{skill_name}_{ref}",
                    (skill_dir / ref).exists(),
                    f"referenced file {ref} exists",
                    failures,
                    passes,
                )

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    check("old_skills_ignored", "/old_skills/" in gitignore, "old_skills is ignored", failures, passes)

    for public_file in PUBLIC_FILES:
        text = public_file.read_text(encoding="utf-8")
        check(
            f"{public_file.name}_no_old_skills",
            "old_skills/" not in text,
            "public file does not reference old_skills",
            failures,
            passes,
        )
        tokens = set(re.findall(r"agently-[a-z0-9-]+", text))
        check(
            f"{public_file.name}_no_retired_skills",
            not any(skill in tokens for skill in RETIRED_SKILLS),
            "public file does not reference retired V1 skills",
            failures,
            passes,
        )

    fixture_text = ROUTE_FIXTURES.read_text(encoding="utf-8")
    fixture_data = json.loads(fixture_text)
    fixture_cases = fixture_data.get("cases", [])
    check(
        "route_fixture_covers_generic_non_framework_case",
        "generic-unresolved-no-framework-en" in fixture_text and "generic-unresolved-no-framework-zh" in fixture_text,
        "route fixtures cover generic kickoff cases without Agently mentions",
        failures,
        passes,
    )
    check(
        "route_fixture_covers_chinese_quality_validator_case",
        any(case.get("id") == "skills-quality-simulator-kickoff-zh" for case in fixture_cases),
        "route fixtures cover the Chinese skills-quality-validator kickoff scenario",
        failures,
        passes,
    )
    check(
        "route_fixture_covers_ui_ollama_skill_tool_case",
        any(case.get("id") == "skill-creation-tool-ui-ollama-zh" for case in fixture_cases),
        "route fixtures cover the Chinese UI plus local Ollama skill-tool kickoff scenario",
        failures,
        passes,
    )
    check(
        "route_fixture_covers_direct_leaf_cases",
        any(
            any(path and path[0] != "agently-playbook" for path in case.get("expected_route_paths", []))
            for case in fixture_cases
        ),
        "route fixtures cover direct leaf discovery cases",
        failures,
        passes,
    )
    check(
        "route_fixture_uses_intent_group_metadata",
        all(
            isinstance(case.get("scenario_id"), str)
            and isinstance(case.get("locale"), str)
            and isinstance(case.get("intent_style"), str)
            for case in fixture_cases
        ),
        "route fixtures group natural-language expressions by scenario and intent style",
        failures,
        passes,
    )
    check(
        "route_fixture_covers_output_efficiency_refactor_group",
        sum(case.get("scenario_id") == "triggerflow-output-efficiency-refactor" for case in fixture_cases) >= 4,
        "route fixtures cover the TriggerFlow output-efficiency refactor scenario with multiple user expressions",
        failures,
        passes,
    )
    check(
        "route_fixture_covers_mixed_sync_async_group",
        sum(case.get("scenario_id") == "triggerflow-mixed-sync-async-orchestration" for case in fixture_cases) >= 3,
        "route fixtures cover the mixed sync/async TriggerFlow orchestration scenario with multiple user expressions",
        failures,
        passes,
    )
    check(
        "route_fixture_covers_process_clarity_group",
        sum(case.get("scenario_id") == "triggerflow-process-clarity-refactor" for case in fixture_cases) >= 3,
        "route fixtures cover the TriggerFlow process-clarity refactor scenario with multiple user expressions",
        failures,
        passes,
    )
    check(
        "route_fixture_covers_project_structure_group",
        sum(case.get("scenario_id") == "project-structure-separated-refactor" for case in fixture_cases) >= 4,
        "route fixtures cover the project-structure separation refactor scenario with multiple user expressions",
        failures,
        passes,
    )

    print("V2 catalog validation")
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
