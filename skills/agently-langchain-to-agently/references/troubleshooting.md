# Troubleshooting

- The migration keeps looking for one Agently class that equals LangChain `create_agent`:
  Split the design into provider setup, input composition, output control, tools, memory, and service exposure.
- Middleware mapping looks forced:
  Re-express the behavior as explicit Agently request logic or workflow logic.
- The source memory model depends on threads and checkpoints:
  Decide whether the target is conversational continuity (`agently-session-memo`) or durable workflow state (`agently-triggerflow-playbook`).
- The source uses `HumanInTheLoopMiddleware` or approval middleware and the migration keeps looking for one direct Agently middleware hook:
  Re-express it as explicit interrupt-and-resume workflow control, usually through `agently-triggerflow-interrupts-and-stream`.
- The source design uses LangGraph more than LangChain:
  Move to `agently-langgraph-to-triggerflow`.
