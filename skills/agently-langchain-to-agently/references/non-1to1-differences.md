# Non-1to1 Differences

## 1. No direct all-in-one `create_agent` replacement

Agently usually wants the design split across clearer capability skills instead of one umbrella abstraction.

## 2. Middleware is usually not migrated literally

Many LangChain middleware patterns should become:

- explicit request composition
- output-control logic
- tool policy
- workflow logic

instead of trying to recreate a middleware stack mechanically.

## 3. Structured-output strategy selection is not one Agently enum

LangChain can route structured output through `ProviderStrategy` or `ToolStrategy`.

In Agently, the target is usually:

- explicit output schema and response-consumption design
- provider and request capability choice
- retry or reliability design where needed

not one direct strategy object replacement.

## 4. Short-term memory is not thread/checkpointer semantics

LangChain short-term memory is described through agent state and checkpointers.

In Agently, conversational continuity usually belongs to:

- `agently-session-memo`

If the source system really depends on durable workflow persistence, move into TriggerFlow skills instead.

## 5. Human approval middleware usually becomes workflow control

If the source relies on `HumanInTheLoopMiddleware`, thread IDs, or resume commands, the Agently target usually becomes:

- explicit interrupt-and-resume flow design
- optional session continuity
- optional execution restore

not one middleware list.

## 6. Some old LangChain abstractions should collapse

If the source still carries `langchain-classic` style layers, do not preserve them just because they exist.

Prefer the smallest Agently target architecture that preserves the behavior you actually need.
