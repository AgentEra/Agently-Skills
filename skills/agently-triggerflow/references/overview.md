# Overview

This skill owns TriggerFlow orchestration, runtime data, runtime stream, sub-flow boundaries, workflow-side model execution, output-fan-out refactors, process-clarity refactors, and mixed sync/async orchestration.

Prefer async-first flow handlers and execution APIs. When the UI needs progressive updates, bridge model-side structured streaming into workflow-side runtime stream items so the frontend consumes stable business events instead of raw parser paths.

For the concrete `instant -> runtime stream` pattern, read `references/stream-bridge.md`.
