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
    "agently-design",
    "agently-request",
    "agently-runtime",
    "agently-stage",
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
    check("catalog_exact", actual_skills == EXPECTED_SKILLS, "public catalog matches current 8-skill set", failures, passes)

    playbook_text = (SKILLS / "agently" / "SKILL.md").read_text(encoding="utf-8")
    catalog_guidance_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    design_text = (SKILLS / "agently-design" / "SKILL.md").read_text(encoding="utf-8")
    design_system_boundaries_text = (
        SKILLS / "agently-design" / "references" / "system-boundaries.md"
    ).read_text(encoding="utf-8")
    design_information_text = (
        SKILLS
        / "agently-design"
        / "references"
        / "information-and-evidence-design.md"
    ).read_text(encoding="utf-8")
    design_model_request_topology_text = (
        SKILLS
        / "agently-design"
        / "references"
        / "model-request-topology.md"
    ).read_text(encoding="utf-8")
    request_text = (SKILLS / "agently-request" / "SKILL.md").read_text(encoding="utf-8")
    request_prompt_management_text = (
        SKILLS / "agently-request" / "references" / "prompt-management.md"
    ).read_text(encoding="utf-8")
    request_output_control_text = (
        SKILLS / "agently-request" / "references" / "output-control.md"
    ).read_text(encoding="utf-8")
    request_output_expected_text = (
        SKILLS / "agently-request" / "outputs" / "output-control-expected.md"
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
    request_session_memory_text = (
        SKILLS / "agently-request" / "references" / "session-memory.md"
    ).read_text(encoding="utf-8")
    context_skills_text = (
        SKILLS / "agently" / "references" / "context-and-skills.md"
    ).read_text(encoding="utf-8")
    runtime_text = (SKILLS / "agently-runtime" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    runtime_actions_text = (
        SKILLS / "agently-runtime" / "references" / "actions-runtime.md"
    ).read_text(encoding="utf-8")
    stage_text = (SKILLS / "agently-stage" / "SKILL.md").read_text(encoding="utf-8")
    stage_lifecycle_text = (
        SKILLS / "agently-stage" / "references" / "task-lifecycle.md"
    ).read_text(encoding="utf-8")
    stage_bridges_text = (
        SKILLS / "agently-stage" / "references" / "bridges-streams-events.md"
    ).read_text(encoding="utf-8")
    dynamic_task_text = (SKILLS / "agently-dynamic-task" / "SKILL.md").read_text(encoding="utf-8")
    dynamic_task_overview_text = (
        SKILLS / "agently-dynamic-task" / "references" / "overview.md"
    ).read_text(encoding="utf-8")
    triggerflow_text = (SKILLS / "agently-triggerflow" / "SKILL.md").read_text(encoding="utf-8")
    triggerflow_overview_text = (
        SKILLS / "agently-triggerflow" / "references" / "overview.md"
    ).read_text(encoding="utf-8")
    execution_topology_path = (
        SKILLS / "agently" / "references" / "execution-topology-validation.md"
    )
    execution_topology_text = (
        execution_topology_path.read_text(encoding="utf-8")
        if execution_topology_path.exists()
        else ""
    )
    check(
        "playbook_framework_name_optional",
        "does not need to mention Agently explicitly" in playbook_text
        and "Generic asks" in playbook_text,
        "playbook explicitly allows scenario-led discovery without framework-name requirements",
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
        "selection_key_freshness_and_host_correlation_guidance",
        "offered-set membership alone does not prove freshness" in design_information_text
        and "cache, queue, retry, persistence, or replay" in design_information_text
        and "request/execution revision binding" in design_information_text
        and "per-request opaque keys" in design_information_text
        and "Host correlation validation" in design_information_text
        and "before canonical lookup" in design_information_text
        and "strictly inline response" in design_information_text
        and "cannot cross request boundaries" in design_information_text
        and "request/execution revision binding" in design_model_request_topology_text
        and "Host correlation validation" in design_model_request_topology_text,
        "selection-key guidance binds cross-boundary responses to a fresh Host request before canonical lookup while exempting strictly inline responses",
        failures,
        passes,
    )
    check(
        "design_cross_owner_boundary",
        "agently-request" in design_text
        and "agently-runtime" in design_text
        and "agently-triggerflow" in design_text
        and "agently-dynamic-task" in design_text
        and "model-request-topology.md" in design_text,
        "agently-design owns cross-layer design while routing executable details to leaf owners",
        failures,
        passes,
    )
    check(
        "stage_owner_boundary",
        "process-local task lifetime" in stage_text
        and "TriggerFlowExecution" in stage_text
        and "It does not own" in stage_text
        and "Stage.create_task" in stage_lifecycle_text
        and "StageCallBridge" in stage_bridges_text
        and "TunnelLagError" in stage_bridges_text
        and "standalone lifecycle APIs" in stage_lifecycle_text
        and "Use `Tunnel` independently" in stage_bridges_text
        and "Use `EventEmitter` independently" in stage_bridges_text
        and "TriggerFlow is not required" in stage_text,
        "Agently-Stage guidance covers standalone scopes, adapters, channels, and listeners without taking workflow or policy ownership",
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
        "request_prompt_context_locality_guidance",
        "Interpret a supplied input."
        in request_prompt_management_text
        and "Provide an authoritative fact, policy, schema, or evidence item."
        in request_prompt_management_text
        and "Change the model-owned decision or transformation."
        in request_prompt_management_text
        and "Define an output, consumer, tool, or capability boundary."
        in request_prompt_management_text
        and "Provide useful user-visible process context, state, or explanation with a declared user or UI consumer."
        in request_prompt_management_text
        and "If removing a candidate item would not change the current request's effective task, contract, evidence, decision, allowed verdict, or declared user/UI projection, remove or rewrite it."
        in request_prompt_management_text
        and "Retain or behaviorally rewrite an effective upstream caller guarantee when it changes the model-owned decision or the allowed verdict set."
        in request_prompt_management_text
        and "Before dispatch, `execution.get_prompt_text()` audits the rendered execution draft, not the final ModelRequest prompt."
        in request_prompt_management_text
        and "observe the final ModelRequest `prompt_text` emitted or built after injection"
        in request_prompt_management_text
        and "Do not treat the post-start execution snapshot as sufficient evidence for late injections."
        in request_prompt_management_text
        and "Redact secrets before retaining prompt evidence."
        in request_prompt_management_text,
        "prompt-management guidance defines all five relevance roles, the retain-side boundary, and draft-versus-final prompt auditing",
        failures,
        passes,
    )
    check(
        "cross_surface_prompt_context_locality_guidance",
        all(
            re.search(r"declared\s+user or UI consumer", text) is not None
            and re.search(r"effective\s+upstream\s+caller\s+guarantee", text)
            is not None
            for text in (
                request_text,
                design_text,
                design_model_request_topology_text,
                catalog_guidance_text,
            )
        )
        and re.search(r"rendered\s+execution draft", catalog_guidance_text)
        is not None
        and re.search(
            r"final ModelRequest\s+`prompt_text`", catalog_guidance_text
        )
        is not None,
        "request, design, topology, and catalog guidance preserve the fifth role and distinguish draft from final prompt evidence",
        failures,
        passes,
    )
    check(
        "rule_first_business_validation_guidance",
        "Rule-First Business Validation" in request_output_control_text
        and "blind gate discovery" in request_output_control_text
        and "new developer response explicitly confirms" in request_output_control_text
        and "blind rule discovery" in request_text
        and "model-satisfiable acceptance rule" in design_text
        and "Blind generation followed by hard" in catalog_guidance_text
        and "rejection until the model happens to pass" in catalog_guidance_text
        and "trial-and-error retry tutor" in request_output_expected_text,
        "business validation rules reach the model before first attempt and hidden gates require confirmation",
        failures,
        passes,
    )
    check(
        "model_request_snapshot_and_new_observation_boundary",
        "request-time input snapshot" in design_model_request_topology_text
        and "Action, tool, API/database read" in design_model_request_topology_text
        and "cannot move a new observation back" in design_model_request_topology_text
        and "request-time input/evidence" in request_text
        and "snapshot and later fields" in request_text
        and "cannot inject the work's result into R1" in triggerflow_overview_text
        and "Treat a ModelRequest as a request-time input snapshot"
        in catalog_guidance_text,
        "request guidance merges same-snapshot work and splits after required new observations",
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
        "task_context_internal_context_index_contract",
        "internal `ContextIndex`" in context_skills_text
        and "async_enumerate_descriptors" in context_skills_text
        and "async_read_exact" in context_skills_text
        and "never supplies exact bytes" in context_skills_text,
        "TaskContext owns derived indexing while sources retain exact source truth",
        failures,
        passes,
    )
    check(
        "session_memory_task_context_recall_contract",
        "AgentlyMemoryContextSource" in request_text
        and "AgentlyMemoryContextSource" in request_session_memory_text
        and "parallel SessionMemory retrieval-to-prompt pipeline"
        in request_session_memory_text,
        "SessionMemory writes stay separate from TaskContext-owned task recall",
        failures,
        passes,
    )
    check(
        "task_workspace_terminal_promotion_contract",
        "staged candidate" in context_skills_text
        and "post-promotion" in context_skills_text
        and "staged candidate" in runtime_text
        and "post-promotion" in runtime_text,
        "required terminal artifacts are verified before atomic promotion",
        failures,
        passes,
    )
    check(
        "workspace_owner_terms_do_not_overlap",
        "| Workspace | durable records, files" not in design_system_boundaries_text
        and "| TaskWorkspace |" in design_system_boundaries_text
        and "| RecordStore |" in design_system_boundaries_text
        and "| TaskContext |" in design_system_boundaries_text
        and "Workspace/spec" not in design_information_text
        and "entire Workspace" not in design_information_text,
        "design guidance separates task files, durable records, and task context",
        failures,
        passes,
    )
    check(
        "action_and_terminal_promotion_owner_contract",
        "ActionRuntime owns model-callable file-write dispatch"
        in runtime_actions_text
        and "TaskWorkspace.atomic_promote_file" in runtime_actions_text
        and "Promotion copies the already accepted bytes" in runtime_actions_text,
        "Action evidence and host-controlled terminal file promotion have distinct owners",
        failures,
        passes,
    )
    check(
        "terminal_topology_orders_verification_before_target_promotion",
        "complete candidate readback + verifier-eligible candidate registration"
        in execution_topology_text
        and execution_topology_text.index("one semantic terminal verifier")
        < execution_topology_text.index(
            "digest-pinned TaskWorkspace target promotion"
        )
        and "complete target readback" in execution_topology_text
        and "trusted-artifact promotion" not in execution_topology_text
        and "only write owner" not in execution_topology_text,
        "topology guidance distinguishes candidate evidence from accepted target promotion",
        failures,
        passes,
    )
    check(
        "retrieval_token_evidence_contract",
        "input tokens separately from LLM prompt tokens"
        in request_knowledge_base_text
        and "provider-observed prompt-token usage" in request_knowledge_base_text
        and "Never derive billed tokens from character counts"
        in request_knowledge_base_text,
        "retrieval guidance separates embedding cost from observed LLM token effects",
        failures,
        passes,
    )
    check(
        "execution_topology_validation_reference",
        execution_topology_path.exists()
        and "prompt.input" in execution_topology_text
        and "prompt.info" in execution_topology_text
        and "prompt.instruct" in execution_topology_text
        and "output schema" in execution_topology_text
        and "value edge" in execution_topology_text
        and "signal/event edge" in execution_topology_text
        and "TriggerFlow" in execution_topology_text
        and "RuntimeEvent" in execution_topology_text,
        "cross-layer evaluation guidance defines schema-complete value and signal/event topology audits",
        failures,
        passes,
    )
    check(
        "execution_topology_validation_routing",
        "execution-topology-validation.md" in playbook_text
        and "execution-topology-validation.md" in triggerflow_text,
        "agently and TriggerFlow guidance route complex request/block handoff audits to one standard",
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
        "triggerflow_loop_back_edge_guidance",
        "graph-visible back edge" in triggerflow_text
        and "`while True`" in triggerflow_text
        and "chunk handler" in triggerflow_text,
        "triggerflow documents graph-visible loop edges and chunk-level while True as an anti-pattern",
        failures,
        passes,
    )
    check(
        "triggerflow_execution_state_owner_guidance",
        "per-execution data store and chunk-to-chunk handoff contract" in triggerflow_text
        and "translation helper" in triggerflow_text
        and "durable cross-run data" in triggerflow_text
        and "flow_data" in triggerflow_text,
        "triggerflow documents execution state as runtime data owner and custom state helpers as anti-patterns",
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
        for subdir in ("references", "examples", "outputs", "scripts", "agents"):
            resource_path = skill_dir / subdir
            if resource_path.exists():
                check(
                    f"{skill_name}_{subdir}",
                    resource_path.is_dir(),
                    f"optional {subdir} resource is a directory",
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
        "route_fixture_covers_agently_design",
        any(case.get("scenario_id") == "agently-system-design" for case in fixture_cases),
        "route fixtures cover unresolved and explicit cross-layer design requests",
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
        any(
            case.get("id") == "project-framework-daily-news-zh"
            and "runnable_template_asset" in case.get("required_concepts", [])
            for case in reference_cases
        ),
        "reference retrieval fixtures cover topology-first project guidance and the runnable asset",
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
        "reference_fixture_covers_request_prompt_context_locality",
        any(
            case.get("id") == "request-prompt-context-locality-zh"
            and case.get("matched_skills") == ["agently-request"]
            and case.get("expected_reference_sets")
            == [["skills/agently-request/references/prompt-management.md"]]
            and {
                "request_local_relevance",
                "self_contained_context",
                "implementation_name_rewriting",
                "user_visible_process_consumer",
                "effective_caller_guarantee",
                "execution_draft_audit",
                "observed_final_prompt_audit",
            }.issubset(case.get("required_concepts", []))
            for case in reference_cases
        ),
        "reference retrieval fixtures cover both locality extremes, a declared user/UI consumer, and draft-versus-final prompt auditing",
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
    check(
        "reference_fixture_covers_execution_topology_validation",
        any(case.get("id") == "execution-topology-validation-zh" for case in reference_cases),
        "reference retrieval fixtures cover schema/event topology audits",
        failures,
        passes,
    )
    check(
        "reference_fixture_covers_agently_design",
        any(case.get("id") == "design-system-boundaries-zh" for case in reference_cases)
        and any(case.get("id") == "design-model-request-topology-en" for case in reference_cases),
        "reference retrieval fixtures cover system boundaries and ModelRequest topology design",
        failures,
        passes,
    )
    check(
        "reference_fixture_covers_selection_key_freshness_correlation",
        any(
            case.get("id") == "design-selection-key-freshness-correlation-en"
            and case.get("matched_skills") == ["agently-design"]
            and case.get("expected_reference_sets")
            == [[
                "skills/agently-design/references/information-and-evidence-design.md",
                "skills/agently-design/references/model-request-topology.md",
            ]]
            and {
                "offered_set_membership_not_freshness",
                "cross_boundary_freshness_binding",
                "host_correlation_before_canonical_lookup",
                "strict_inline_response_exception",
            }.issubset(case.get("required_concepts", []))
            for case in reference_cases
        ),
        "reference retrieval fixtures cover selection-key freshness binding and Host correlation before canonical lookup",
        failures,
        passes,
    )
    check(
        "reference_fixture_covers_instant_overlap_reconcile",
        any(
            case.get("id") == "design-instant-overlap-reconcile-zh"
            and {
                "host_key_deduplication",
                "final_reconciliation",
                "bounded_structured_deliberation",
            }.issubset(case.get("required_concepts", []))
            for case in reference_cases
        ),
        "reference retrieval fixtures cover provisional instant fan-out and final reconciliation",
        failures,
        passes,
    )
    check(
        "reference_fixture_covers_request_snapshot_boundary",
        any(
            case.get("id") == "design-request-snapshot-boundary-zh"
            and {
                "same_snapshot_merge",
                "new_observation_split",
                "instant_no_backfeed",
            }.issubset(case.get("required_concepts", []))
            for case in reference_cases
        ),
        "reference retrieval fixtures cover same-request merging and new-observation splitting",
        failures,
        passes,
    )
    check(
        "reference_fixture_covers_rule_first_validation",
        any(
            case.get("id") == "request-rule-first-validation-zh"
            and {
                "rule_first_validation",
                "validator_remains_authority",
                "blind_gate_discovery_antipattern",
                "hidden_gate_second_confirmation",
            }.issubset(case.get("required_concepts", []))
            for case in reference_cases
        ),
        "reference retrieval fixtures cover rule-first validation and hidden-gate confirmation",
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
