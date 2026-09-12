from pathlib import Path


TEMPLATE_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_FILES = {
    ".gitignore",
    "SETTINGS.yaml",
    "TOPOLOGY.md",
    "app.py",
    "pyrightconfig.json",
    "requirements.txt",
    "trace_log.py",
    "prompts/plan_analysis.yaml",
    "prompts/compose_answer.yaml",
    "resources/metrics.json",
    "utils/metrics.py",
    "workflows/main_flow.py",
    "workflows/chunks/plan_analysis.py",
    "workflows/chunks/load_metric_facts.py",
    "workflows/chunks/compose_answer.py",
    "actions/growth.py",
    "actions/sandbox/calculate_growth.py",
    "skills/install_local.py",
    "skills/local/analysis-writing/SKILL.md",
    "services/contracts.py",
    "services/api.py",
    "services/mcp_server.py",
}


def test_template_contains_each_owned_boundary() -> None:
    missing = sorted(
        relative_path
        for relative_path in EXPECTED_FILES
        if not (TEMPLATE_ROOT / relative_path).is_file()
    )

    assert missing == []
    assert not (TEMPLATE_ROOT / "tools").exists()
    assert not (TEMPLATE_ROOT / "actions/mcp.py").exists()


def test_app_is_only_the_composition_root() -> None:
    source = (TEMPLATE_ROOT / "app.py").read_text(encoding="utf-8")

    assert len(source.splitlines()) <= 40
    assert "Agently.load_settings" in source
    assert "auto_load_env=True" in source
    assert "from workflows.main_flow import run_analysis" in source
    for forbidden in ("TriggerFlow(", "load_yaml_prompt", "TraceLog(", "json.dumps"):
        assert forbidden not in source


def test_flow_owns_topology_but_not_business_implementations() -> None:
    source = (TEMPLATE_ROOT / "workflows/main_flow.py").read_text(encoding="utf-8")

    assert "TriggerFlow(name=" in source
    assert "create_execution(" in source
    assert "register_framework_hook" in source
    assert "unregister_framework_hook" in source
    for forbidden in ("load_yaml_prompt", "def load_metrics", "@agent.action_func"):
        assert forbidden not in source


def test_optional_capability_directories_do_not_absorb_utils() -> None:
    action_source = (TEMPLATE_ROOT / "actions/growth.py").read_text(encoding="utf-8")
    util_source = (TEMPLATE_ROOT / "utils/metrics.py").read_text(encoding="utf-8")

    assert "action_func" in action_source
    assert "action_func" not in util_source
    assert "use_mcp" not in util_source


def test_services_are_direct_inbound_adapters() -> None:
    api_source = (TEMPLATE_ROOT / "services/api.py").read_text(encoding="utf-8")
    mcp_source = (TEMPLATE_ROOT / "services/mcp_server.py").read_text(
        encoding="utf-8"
    )

    assert "from fastapi import FastAPI" in api_source
    assert "from fastmcp import FastMCP" in mcp_source
    assert "from workflows.main_flow import run_analysis" in api_source
    assert "from workflows.main_flow import run_analysis" in mcp_source
    for forbidden in ("FastAPIHelper", "async_use_mcp"):
        assert forbidden not in api_source
        assert forbidden not in mcp_source


def test_topology_records_the_four_planning_ledgers() -> None:
    topology = (TEMPLATE_ROOT / "TOPOLOGY.md").read_text(encoding="utf-8")

    for heading in (
        "Owner and Invariant Ledger",
        "Planned Node Ledger",
        "Planned Edge Ledger",
        "Production-Necessity Ledger",
    ):
        assert heading in topology
