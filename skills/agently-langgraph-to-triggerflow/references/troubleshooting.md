# Troubleshooting

- The migration is trying to recreate `StateGraph` syntax directly:
  Translate graph capabilities into TriggerFlow skills first, then rewrite the implementation.
- State fields have no clear home:
  Move to `agently-triggerflow-state-and-resources` and decide between `runtime_data`, `flow_data`, resources, and external persistence.
- Checkpointer or thread semantics are unclear in the target:
  Split the problem into definition restore, execution restore, and conversation continuity.
- The source graph depends on `Send` or `Command` and the migration is searching for one exact TriggerFlow API:
  Keep the orchestration intent, then redesign it with TriggerFlow patterns or interrupt-and-resume control instead of matching syntax.
- Streaming behavior looks mismatched:
  Separate runtime stream, model streaming, and structured output streaming before rewriting.
- The source graph behaves more like a specialist-agent system than a plain workflow:
  Add `agently-multi-agent-patterns`.
