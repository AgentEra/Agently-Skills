# Migration Principles

Use these rules before translating any code.

## 1. Translate capabilities, not imports

Do not ask:

- which Agently import equals this LangChain import

Ask:

- what capability does this part of the source system actually provide

## 2. Use the smallest Agently target architecture

Typical order:

1. one request
2. one higher-quality request
3. one request plus tools, memory, or retrieval
4. multi-agent design
5. TriggerFlow orchestration

Do not migrate into a more complex target architecture than the business requirement needs.

## 3. Expect non-1:1 mappings

Some source abstractions map directly.

Some do not:

- LangChain middleware often becomes explicit Agently request composition or workflow logic
- LangGraph checkpointing often becomes TriggerFlow config plus execution-state restore
- LangChain short-term memory often becomes Agently session continuity rather than thread/checkpointer semantics

## 4. Preserve the external contract first

During migration, prioritize:

- request and response shape
- business rules
- approval rules
- restart behavior
- streaming contract

Internal architecture can change if the external contract remains correct or improves.
