from importlib import import_module


def test_trace_has_one_fact_write_contract() -> None:
    module = import_module("trace_log")
    trace = module.TraceLog("task-1", "execution-1")

    event = trace.log(
        layer="business",
        event_type="business.metric.loaded",
        status="completed",
        subject_id="net-revenue",
        output={"period_count": 2},
    )

    assert event == trace.events[0]
    assert set(event) == {
        "event_id",
        "task_id",
        "execution_id",
        "layer",
        "event_type",
        "status",
        "timestamp",
        "subject_id",
        "input",
        "output",
        "facts",
        "error",
        "runtime",
    }


def test_framework_trace_uses_a_small_explicit_whitelist() -> None:
    module = import_module("trace_log")

    assert module.FRAMEWORK_EVENT_TYPES == frozenset(
        {
            "triggerflow.execution_started",
            "triggerflow.execution_completed",
            "triggerflow.execution_failed",
            "chunk.started",
            "chunk.completed",
            "chunk.failed",
            "model.request_started",
            "model.completed",
            "model.request_failed",
            "model.meta",
        }
    )
