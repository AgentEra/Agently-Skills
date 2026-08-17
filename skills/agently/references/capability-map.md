# Capability Map

Use `agently` to reduce a broad request into one Agently-native capability path.

The request can start from a generic scenario and does not need to mention Agently explicitly.

Examples that should still start here:

- "help me kick off a model-powered internal tool"
- "build a requirements assistant and validate the outputs"
- "create a skills quality simulator and decide whether it should be one request or a workflow"
- "build a heuristic skill creation tool with a UI and local Ollama"
- "scaffold a new Agently project and decide how settings, prompts, and workflow should be split"

- unresolved business, product, or refactor request -> stay here first
- unclear owner choice between ModelRequest, AgentExecution, TaskDAG, TriggerFlow, TaskContext, TaskWorkspace, or RecordStore -> stay here first and map the problem by scenario complexity
- project initialization, repo skeleton, or first-pass standard structure for a model app -> stay here first
- model setup, prompt management, output control, response reuse, session memory, embeddings, KB, or retrieval-to-answer -> `agently-request`
- Action Runtime, built-in actions, tools compatibility, MCP, ExecutionResource, TaskWorkspace, RecordStore, FastAPIHelper, `auto_func`, `KeyWaiter`, or `agently-devtools` observation/evaluation/playground integration -> `agently-runtime`
- Stage task-lifetime scopes, sync/async adapters, loop-neutral handles,
  settlement, StageStream, Tunnel, EventEmitter, pressure, or idle diagnostics
  -> `agently-stage`
- model-generated or app-submitted DAG planning, TaskDAG validation, resolver handlers, executor customization, or DynamicTask facade execution -> `agently-dynamic-task`
- branching, concurrency, waiting/resume, mixed sync/async orchestration, event-driven fan-out, process-clarity refactors, graph-friendly workflow definitions, or multi-stage quality loops -> `agently-triggerflow`
- unresolved migration ownership -> `agently-migration`
