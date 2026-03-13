# Capability Map

Use `agently-playbook` to reduce a broad request into one Agently-native capability path.

The request can start from a generic scenario and does not need to mention Agently explicitly.

Examples that should still start here:

- "help me kick off a model-powered internal tool"
- "build a requirements assistant and validate the outputs"
- "create a skills quality simulator and decide whether it should be one request or a workflow"
- "build a heuristic skill creation tool with a UI and local Ollama"
- "scaffold a new Agently project and decide how settings, prompts, and workflow should be split"

- unresolved business, product, or refactor request -> stay here first
- project initialization, repo skeleton, or first-pass standard structure for a model app -> stay here first
- provider wiring, settings-file model separation, `${ENV.xxx}` placeholders, or auto `.env` loading -> `agently-model-setup`
- prompt composition, prompt config, placeholder mappings, or config-file bridge for prompt behavior -> `agently-prompt-management`
- output contract and required keys -> `agently-output-control`
- response reuse, metadata, and stream consumption -> `agently-model-response`
- session continuity or restore -> `agently-session-memory`
- tools, MCP, FastAPIHelper, `auto_func`, or `KeyWaiter` -> `agently-agent-extensions`
- embeddings and retrieval -> `agently-knowledge-base`
- branching, concurrency, waiting/resume, mixed sync/async orchestration, event-driven fan-out, process-clarity refactors, or multi-stage quality loops -> `agently-triggerflow`
- unresolved migration ownership -> `agently-migration-playbook`
