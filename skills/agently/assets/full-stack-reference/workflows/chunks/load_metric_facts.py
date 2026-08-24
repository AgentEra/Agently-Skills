"""阶段二：由宿主确定性读取每个分析任务需要的指标事实。"""

from pathlib import Path
from typing import Any, cast

from agently import TriggerFlowRuntimeData

from trace_log import TraceLog
from utils.metrics import load_metric_facts as read_metric_facts
from utils.metrics import load_snapshot_id


async def load_metric_facts(
    data: TriggerFlowRuntimeData,
) -> dict[str, Any]:
    task = cast(dict[str, Any], data.input)
    metrics_path = cast(Path, data.require_resource("metrics_path"))
    trace = cast(TraceLog, data.require_resource("trace"))
    analysis_id = str(task["analysis_id"])
    metric = str(task["metric"])
    periods = [str(period) for period in task["periods"]]

    facts = read_metric_facts(metrics_path, metric=metric, periods=periods)
    evidence = {
        "evidence_id": f"metric:{analysis_id}",
        "analysis_id": analysis_id,
        "metric": metric,
        "facts": facts,
        "snapshot_id": load_snapshot_id(metrics_path),
    }
    trace.log(
        layer="business",
        event_type="business.metric.loaded",
        status="completed",
        subject_id=analysis_id,
        input={"metric": metric, "periods": periods},
        output=evidence,
        facts={"period_count": len(facts)},
    )
    await data.async_append_state("metric_facts", evidence, emit=False)
    return evidence


__all__ = ["load_metric_facts"]
