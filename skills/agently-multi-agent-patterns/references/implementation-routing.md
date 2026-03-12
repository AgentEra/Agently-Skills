# Implementation Routing

Use this page after the business pattern is clear and the next question is how to implement it with existing Agently skills.

## Common routing

- provider choice, proxy, auth, request options, or per-agent model setup -> `agently-model-setup`
- per-agent input slots, attachments, or request-vs-agent prompt layering -> `agently-input-composition`
- per-agent output schema, reviewer contracts, or structured streaming handoffs -> `agently-output-control`
- rubric-based review logic, pass-fail reports, or judge-model evaluation prompts -> `agently-eval-and-judge`
- local tools or built-in tools per specialist agent -> `agently-tools`
- MCP-backed specialist agents -> `agently-mcp`
- retrieval specialist or KB-backed expert agent -> `agently-knowledge-base-and-rag`
- per-user continuity or long-lived conversational state -> `agently-session-memo`
- reusable YAML or JSON prompts per agent role -> `agently-prompt-config-files`
- exposing the agent team behind helper endpoints -> `agently-fastapi-helper`

## Workflow routing

- multi-agent coordination as a business workflow -> `agently-triggerflow-playbook`
- generic workflow shape such as routers, loops, or fan-out -> `agently-triggerflow-patterns`
- explicit parent-child workflow isolation for specialist branches -> `agently-triggerflow-subflows`
- model calls inside the workflow and `instant`-driven dispatch -> `agently-triggerflow-model-integration`
- shared-versus-isolated workflow state and runtime resources -> `agently-triggerflow-state-and-resources`
- approval or external resume between agent steps -> `agently-triggerflow-interrupts-and-stream`

## Practical default

For most serious multi-agent systems in Agently, the practical combination is:

- `agently-model-setup`
- `agently-output-control`
- `agently-triggerflow-playbook`

Then add `agently-eval-and-judge`, tools, MCP, KB/RAG, session, prompt config, or FastAPIHelper only where the business design truly needs them.
