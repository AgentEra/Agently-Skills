# Overview

This skill owns TriggerFlow orchestration, runtime data, runtime stream, sub-flow boundaries, workflow-side model execution, output-fan-out refactors, process-clarity refactors, and mixed sync/async orchestration.

Prefer async-first flow handlers and execution APIs. When the UI needs progressive updates, bridge model-side structured streaming into workflow-side runtime stream items so the frontend consumes stable business events instead of raw parser paths.

In Agently `v4.0.9`, TriggerFlow definitions, chunk signal metadata, and origin-chunk payloads are also strong enough to support graph-oriented debugging and local DevTools visualization without duplicating the workflow description.

For the concrete `instant -> runtime stream` pattern, read `references/stream-bridge.md`.
For graph, export, and observation design, read `references/devtools-graph.md`.
