#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
ROUTE_FIXTURES = ROOT / "validate" / "fixtures" / "route_cases.json"
REFERENCE_FIXTURES = ROOT / "validate" / "fixtures" / "reference_retrieval_cases.json"
EXPECTED_SKILLS = {
    "agently",
    "agently-request",
    "agently-runtime",
    "agently-dynamic-task",
    "agently-triggerflow",
    "agently-migration",
}
PUBLIC_FILES = [
    ROOT / "README.md",
    ROOT / "README_CN.md",
    ROOT / "AGENTS.md",
    ROOT / "bundles" / "manifest.json",
    ROOT / "compatibility" / "support.json",
]
RETIRED_SKILLS = [
    "agently-model-setup",
    "agently-prompt-management",
    "agently-output-control",
    "agently-model-response",
    "agently-session-memory",
    "agently-agent-extensions",
    "agently-knowledge-base",
    "agently-migration-playbook",
    "agently-langchain-to-agently",
    "agently-langgraph-to-triggerflow",
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
    check(
        "compatibility_support_exists",
        (ROOT / "compatibility" / "support.json").exists(),
        "compatibility support manifest exists",
        failures,
        passes,
    )
    check(
        "legacy_dir_absent",
        not (ROOT / "legacy").exists(),
        "default branch does not contain archived catalog directories",
        failures,
        passes,
    )
    actual_skills = {path.name for path in SKILLS.iterdir() if path.is_dir()}
    check("catalog_exact", actual_skills == EXPECTED_SKILLS, "public catalog matches current 6-skill set", failures, passes)

    playbook_text = (SKILLS / "agently" / "SKILL.md").read_text(encoding="utf-8")
    catalog_guidance_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    request_text = (SKILLS / "agently-request" / "SKILL.md").read_text(encoding="utf-8")
    request_prompt_management_text = (
        SKILLS / "agently-request" / "references" / "prompt-management.md"
    ).read_text(encoding="utf-8")
    project_framework_text = (
        SKILLS / "agently" / "references" / "project-framework.md"
    ).read_text(encoding="utf-8")
    request_model_response_text = (
        SKILLS / "agently-request" / "references" / "model-response.md"
    ).read_text(encoding="utf-8")
    request_knowledge_base_text = (
        SKILLS / "agently-request" / "references" / "knowledge-base.md"
    ).read_text(encoding="utf-8")
    dynamic_task_text = (SKILLS / "agently-dynamic-task" / "SKILL.md").read_text(encoding="utf-8")
    dynamic_task_overview_text = (
        SKILLS / "agently-dynamic-task" / "references" / "overview.md"
    ).read_text(encoding="utf-8")
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
        "playbook_trusted_identifier_join_boundary",
        "one host-issued trusted selection key" in playbook_text
        and re.search(
            r"reconstruct\s+UUIDs,\s+metadata,\s+and\s+other\s+identifiers\s+deterministically",
            playbook_text,
        )
        is not None
        and "do not ask the model to reproduce" in playbook_text
        and "application-local projection" in playbook_text
        and "required string constrained to the offered key set" in playbook_text,
        "playbook keeps opaque identity and metadata joins host-owned",
        failures,
        passes,
    )
    check(
        "request_final_getter_without_discarded_stream",
        "directly await `async_get_data()`" in request_text
        and re.search(
            r"discard-only\s+`instant`\s+drain\s+loop",
            request_text,
        )
        is not None
        and "No progressive consumer" in request_model_response_text,
        "request guidance chooses final data getters when no stream is consumed",
        failures,
        passes,
    )
    check(
        "project_information_locality",
        "cross-file lookup count and nesting depth" in playbook_text
        and "actual reuse value" in project_framework_text
        and "Formal separation without either benefit is over-design"
        in project_framework_text
        and "Across code examples and project layouts" in catalog_guidance_text,
        "general project guidance avoids splitting information without reuse or ownership value",
        failures,
        passes,
    )
    check(
        "request_contract_information_locality",
        "one-off Agently fluent request readable as one chain" in request_text
        and "terminal `.get_result()`" in request_prompt_management_text
        and "merely to shorten the chain" in request_prompt_management_text
        and "In Agently fluent request examples" in catalog_guidance_text
        and "One Prompt Configure file plus explicit" in catalog_guidance_text,
        "Agently fluent request guidance keeps one-off request chains locally readable",
        failures,
        passes,
    )
    check(
        "request_retrieval_ref_rendering_protocol",
        "[[ref:<ref_id>]]" in request_text
        and "[[ref:<ref_id>]]" in request_knowledge_base_text
        and "cite_as" in request_knowledge_base_text
        and "hover card" in request_knowledge_base_text,
        "retrieval guidance defines a host-resolved reference rendering protocol",
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
    check(
        "taskdag_foundation_dynamic_task_facade",
        "TaskDAG is the Agently DAG foundation capability" in dynamic_task_text
        and "compatibility and convenience facade" in dynamic_task_text
        and "TriggerFlow is" in dynamic_task_text
        and "execution substrate" in dynamic_task_text,
        "TaskDAG is documented as the DAG foundation, with Dynamic Task as facade and TriggerFlow as substrate",
        failures,
        passes,
    )
    check(
        "taskdag_default_direct_blocks_opt_in",
        "default direct path" in dynamic_task_overview_text
        and "Blocks path is opt-in" in dynamic_task_overview_text,
        "TaskDAG overview distinguishes direct execution from the opt-in Blocks carrier",
        failures,
        passes,
    )
    check(
        "runtime_dag_data_not_direct_triggerflow_definitions",
        "Do not compile model-generated or app-submitted DAG data directly into new TriggerFlow definitions"
        in triggerflow_text,
        "runtime-generated/submitted DAG data routes through TaskDAG instead of ad hoc TriggerFlow definitions",
        failures,
        passes,
    )
    check(
        "triggerflow_flow_data_snapshot_semantics",
        re.search(
            r"execution\.save\(\).{0,80}snapshot includes a serialized copy",
            triggerflow_text,
            re.DOTALL,
        )
        is not None
        and re.search(
            r"load\(\).{0,40}replaces\s+the\s+current\s+flow-shared\s+value",
            triggerflow_text,
            re.DOTALL,
        )
        is not None,
        "TriggerFlow guidance states the exact shared flow_data save/load behavior",
        failures,
        passes,
    )
    check(
        "triggerflow_hidden_execution_scope",
        "finite, self-closing" in triggerflow_text
        and "execution handle" in triggerflow_text,
        "TriggerFlow guidance scopes hidden execution sugar by lifecycle needs",
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
                description_match = re.search(r"^description:\s*(.+)$", block, re.MULTILINE)
                if description_match is not None:
                    description_value = description_match.group(1).strip()
                    check(
                        f"{skill_name}_description_yaml_safe",
                        ": " not in description_value
                        or (
                            len(description_value) >= 2
                            and description_value[0] in {"'", '"'}
                            and description_value[-1] == description_value[0]
                        ),
                        "frontmatter description is safe for YAML-based skill installers",
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
    retired_archive_name = "old" + "_skills"
    check(
        "retired_archive_dir_absent",
        not (ROOT / retired_archive_name).exists(),
        "retired archive directory is absent from the default branch",
        failures,
        passes,
    )
    check(
        "gitignore_does_not_preserve_retired_archive_name",
        retired_archive_name not in gitignore,
        "gitignore does not preserve the retired archive name",
        failures,
        passes,
    )

    for public_file in PUBLIC_FILES:
        text = public_file.read_text(encoding="utf-8")
        check(
            f"{public_file.name}_no_retired_archive_name",
            f"{retired_archive_name}/" not in text,
            "public file does not reference the retired archive name",
            failures,
            passes,
        )
        check(
            f"{public_file.name}_no_legacy_v1_path",
            "legacy/v1" not in text,
            "public file does not reference archived catalog filesystem paths",
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
    reference_fixture_data = json.loads(REFERENCE_FIXTURES.read_text(encoding="utf-8"))
    reference_cases = reference_fixture_data.get("cases", [])
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
            any(path and path[0] != "agently" for path in case.get("expected_route_paths", []))
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
        "route_fixture_covers_execution_lifecycle_group",
        sum(case.get("scenario_id") == "triggerflow-execution-lifecycle" for case in fixture_cases) >= 2,
        "route fixtures cover TriggerFlow execution lifecycle and manual close scenarios",
        failures,
        passes,
    )
    check(
        "route_fixture_covers_durable_execution",
        any(case.get("scenario_id") == "triggerflow-durable-execution" for case in fixture_cases),
        "route fixtures cover durable TriggerFlow execution scenarios",
        failures,
        passes,
    )
    check(
        "route_fixture_covers_distributed_management",
        any(case.get("scenario_id") == "triggerflow-distributed-management" for case in fixture_cases),
        "route fixtures cover distributed TriggerFlow execution management scenarios",
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
    check(
        "reference_fixture_present",
        bool(reference_cases),
        "reference retrieval fixtures exist",
        failures,
        passes,
    )
    check(
        "reference_fixture_covers_project_framework",
        any(case.get("id") == "project-framework-daily-news-zh" for case in reference_cases),
        "reference retrieval fixtures cover project framework guidance",
        failures,
        passes,
    )
    check(
        "reference_fixture_covers_prompt_placeholders",
        any(case.get("id") == "prompt-placeholder-config-en" for case in reference_cases),
        "reference retrieval fixtures cover prompt placeholder mappings",
        failures,
        passes,
    )
    check(
        "reference_fixture_covers_env_settings",
        any(case.get("id") == "model-settings-env-en" for case in reference_cases),
        "reference retrieval fixtures cover env-backed model settings",
        failures,
        passes,
    )
    check(
        "reference_fixture_covers_response_fanout",
        any(case.get("id") == "response-fanout-example-en" for case in reference_cases),
        "reference retrieval fixtures cover TriggerFlow response-fanout support docs",
        failures,
        passes,
    )
    check(
        "reference_fixture_covers_triggerflow_lifecycle",
        any(case.get("id") == "triggerflow-lifecycle-close-zh" for case in reference_cases),
        "reference retrieval fixtures cover TriggerFlow lifecycle close guidance",
        failures,
        passes,
    )
    check(
        "reference_fixture_covers_stream_close",
        any(case.get("id") == "triggerflow-runtime-stream-close-en" for case in reference_cases),
        "reference retrieval fixtures cover runtime stream close guidance",
        failures,
        passes,
    )
    check(
        "reference_fixture_covers_state_vs_flow_data",
        any(case.get("id") == "triggerflow-state-vs-flow-data-zh" for case in reference_cases),
        "reference retrieval fixtures cover execution state versus flow data guidance",
        failures,
        passes,
    )
    check(
        "reference_fixture_covers_model_quality_validation",
        any(case.get("id") == "model-quality-validation-routing-zh" for case in reference_cases),
        "reference retrieval fixtures cover model-request-based quality and routing guidance",
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
