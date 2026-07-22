"""可注册给 Agent 的确定性增长率 Action。"""

from typing import Any


def calculate_growth(*, previous: float, current: float) -> dict[str, float]:
    """Calculate absolute change and growth rate for two metric values."""

    if previous == 0:
        raise ValueError("previous must not be zero")
    return {
        "change": round(current - previous, 6),
        "growth_rate": round((current - previous) / previous, 6),
    }


def register_growth_action(agent: Any) -> Any:
    """把函数注册并启用为模型可调用的 Action。"""

    agent.action_func(calculate_growth)
    return agent.use_actions("calculate_growth", always=True)


__all__ = ["calculate_growth", "register_growth_action"]
