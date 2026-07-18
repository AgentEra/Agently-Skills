#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "skills" / "agently" / "assets" / "project-template"

EXPECTED_FILES = {
    ".gitignore",
    "pyrightconfig.json",
    "requirements.txt",
    "SETTINGS.yaml",
    "app.py",
    "TOPOLOGY.md",
    "prompts/plan_analysis.yaml",
    "prompts/compose_answer.yaml",
    "workflows/main_flow.py",
    "workflows/chunks/plan_analysis.py",
    "workflows/chunks/load_metric_facts.py",
    "workflows/chunks/compose_answer.py",
    "utils/metrics.py",
    "actions/growth.py",
    "actions/sandbox/calculate_growth.py",
    "skills/install_local.py",
    "skills/local/analysis-writing/SKILL.md",
    "resources/metrics.json",
    "trace_log.py",
    "services/contracts.py",
    "services/api.py",
    "services/mcp_server.py",
    "tests/conftest.py",
    "tests/test_structure.py",
    "tests/test_trace.py",
    "tests/test_utils_actions_skills.py",
    "tests/test_workflow.py",
    "tests/test_services.py",
}

FORBIDDEN_PARTS = {
    ".agently",
    ".DS_Store",
    "__pycache__",
    "outputs",
}

FORBIDDEN_TEXT = {
    "attach_mcp",
    "agently_project_template_reference",
    "../../../..",
    "/Users/moxin/Library/Mobile Documents/",
}


def check(
    name: str,
    condition: bool,
    details: str,
    failures: list[str],
    passes: list[str],
) -> None:
    if condition:
        passes.append(f"{name}: {details}")
    else:
        failures.append(f"{name}: {details}")


def main() -> None:
    passes: list[str] = []
    failures: list[str] = []

    check(
        "template_exists",
        TEMPLATE.is_dir(),
        "the public project template asset exists",
        failures,
        passes,
    )

    actual_files = {
        path.relative_to(TEMPLATE).as_posix()
        for path in TEMPLATE.rglob("*")
        if path.is_file()
    } if TEMPLATE.exists() else set()

    for relative_path in sorted(EXPECTED_FILES):
        check(
            f"file_{relative_path}",
            relative_path in actual_files,
            f"required authored file exists: {relative_path}",
            failures,
            passes,
        )

    forbidden_paths = sorted(
        relative_path
        for relative_path in actual_files
        if FORBIDDEN_PARTS.intersection(Path(relative_path).parts)
        or relative_path == "actions/mcp.py"
        or relative_path.endswith(".pyc")
    )
    check(
        "generated_paths_absent",
        not forbidden_paths,
        f"generated and redundant paths are absent: {forbidden_paths}",
        failures,
        passes,
    )

    text_files = [
        TEMPLATE / relative_path
        for relative_path in sorted(actual_files)
        if (TEMPLATE / relative_path).suffix
        in {".json", ".md", ".py", ".txt", ".yaml", ".yml"}
        or relative_path == ".gitignore"
    ]
    forbidden_text_hits: list[str] = []
    for path in text_files:
        content = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_TEXT:
            if forbidden in content:
                forbidden_text_hits.append(
                    f"{path.relative_to(TEMPLATE).as_posix()}: {forbidden}"
                )
    check(
        "local_source_text_absent",
        not forbidden_text_hits,
        f"authored files contain no local source assumptions: {forbidden_text_hits}",
        failures,
        passes,
    )

    topology_path = TEMPLATE / "TOPOLOGY.md"
    topology = topology_path.read_text(encoding="utf-8") if topology_path.exists() else ""
    for heading in (
        "Owner and Invariant Ledger",
        "Planned Node Ledger",
        "Planned Edge Ledger",
        "Production-Necessity Ledger",
    ):
        check(
            f"topology_{heading.lower().replace(' ', '_').replace('-', '_')}",
            heading in topology,
            f"TOPOLOGY.md contains {heading}",
            failures,
            passes,
        )

    api_path = TEMPLATE / "services" / "api.py"
    api_source = api_path.read_text(encoding="utf-8") if api_path.exists() else ""
    check(
        "fastapi_direct_adapter",
        "from fastapi import FastAPI" in api_source,
        "the HTTP adapter uses FastAPI directly",
        failures,
        passes,
    )

    mcp_path = TEMPLATE / "services" / "mcp_server.py"
    mcp_source = mcp_path.read_text(encoding="utf-8") if mcp_path.exists() else ""
    check(
        "fastmcp_direct_adapter",
        "from fastmcp import FastMCP" in mcp_source,
        "the MCP server adapter uses FastMCP directly",
        failures,
        passes,
    )

    print("Agently public project template validation")
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
