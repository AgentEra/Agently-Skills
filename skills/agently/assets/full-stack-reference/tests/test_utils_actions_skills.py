from pathlib import Path
from tempfile import TemporaryDirectory

TEMPLATE_ROOT = Path(__file__).resolve().parents[1]


def test_utils_load_host_owned_metric_facts() -> None:
    from utils.metrics import load_metric_facts

    facts = load_metric_facts(
        TEMPLATE_ROOT / "resources/metrics.json",
        metric="net_revenue",
        periods=["2024", "2025"],
    )

    assert facts == [
        {"metric": "net_revenue", "period": "2024", "value": 120.0},
        {"metric": "net_revenue", "period": "2025", "value": 150.0},
    ]


def test_action_registers_a_model_callable_calculation() -> None:
    from actions.growth import calculate_growth, register_growth_action

    assert calculate_growth(previous=120.0, current=150.0) == {
        "change": 30.0,
        "growth_rate": 0.25,
    }

    class FakeAgent:
        def __init__(self) -> None:
            self.registered = None
            self.enabled = None

        def action_func(self, function):
            self.registered = function
            return function

        def use_actions(self, action_id, *, always: bool):
            assert always is True
            self.enabled = action_id
            return self

    agent = FakeAgent()
    assert register_growth_action(agent) is agent
    assert agent.registered is calculate_growth
    assert agent.enabled == "calculate_growth"


def test_sandbox_script_exposes_a_small_pure_entrypoint() -> None:
    from actions.sandbox.calculate_growth import calculate

    assert calculate({"previous": 80, "current": 100}) == {
        "change": 20.0,
        "growth_rate": 0.25,
    }


def test_local_skill_can_be_installed_as_an_immutable_revision() -> None:
    from agently.core import SkillLibrary
    from skills.install_local import install_local_skills

    with TemporaryDirectory() as temp_dir:
        library = SkillLibrary(Path(temp_dir) / "library")
        revisions = install_local_skills(library, TEMPLATE_ROOT / "skills/local")

    assert len(revisions) == 1
    assert revisions[0].startswith("skill:analysis-writing@sha256:")
