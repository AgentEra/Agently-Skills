"""读取宿主拥有的指标数据；该能力不会注册给模型。"""

import json
from pathlib import Path
from typing import Any, cast


def load_metric_catalog(path: Path) -> dict[str, list[str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    metrics = cast(dict[str, dict[str, float]], payload["metrics"])
    return {name: sorted(periods) for name, periods in metrics.items()}


def load_metric_facts(
    path: Path,
    *,
    metric: str,
    periods: list[str],
) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    metrics = cast(dict[str, dict[str, float]], payload["metrics"])
    if metric not in metrics:
        raise ValueError(f"unknown metric: {metric}")

    values = metrics[metric]
    unknown_periods = [period for period in periods if period not in values]
    if unknown_periods:
        raise ValueError(f"unknown periods: {', '.join(unknown_periods)}")
    return [
        {"metric": metric, "period": period, "value": float(values[period])}
        for period in periods
    ]


def load_snapshot_id(path: Path) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return str(payload["snapshot_id"])


__all__ = ["load_metric_catalog", "load_metric_facts", "load_snapshot_id"]
