# Capability Map

Use `agently-playbook` to reduce a broad request into one Agently-native capability path.

The request can start from a generic scenario and does not need to mention Agently explicitly.

Examples that should still start here:

- "help me kick off a model-powered internal tool"
- "build a requirements assistant and validate the outputs"
- "create a skills quality simulator and decide whether it should be one request or a workflow"
- "build a heuristic skill creation tool with a UI and local Ollama"

- unresolved business, product, or refactor request -> stay here first
- provider wiring or settings-file model separation -> `agently-model-setup`
- prompt composition, prompt config, or config-file bridge for prompt behavior -> `agently-prompt-management`
- output contract and required keys -> `agently-output-control`
- response reuse, metadata, and stream consumption -> `agently-model-response`
- session continuity or restore -> `agently-session-memory`
- tools, MCP, FastAPIHelper, `auto_func`, or `KeyWaiter` -> `agently-agent-extensions`
- embeddings and retrieval -> `agently-knowledge-base`
- branching, concurrency, waiting/resume, mixed sync/async orchestration, event-driven fan-out, process-clarity refactors, or multi-stage quality loops -> `agently-triggerflow`
- unresolved migration ownership -> `agently-migration-playbook`
