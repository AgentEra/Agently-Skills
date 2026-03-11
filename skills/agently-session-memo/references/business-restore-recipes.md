# Business Restore Recipes

This page covers real-world session recovery patterns.

## 1. Restore A Conversation After Service Restart

Use this sequence:

1. create a fresh agent
2. rebuild normal agent setup such as model settings, tools, and prompt defaults
3. create a fresh `Session`
4. load the saved JSON or YAML session state
5. assign the restored session into `agent.sessions[restored.id]`
6. `activate_session(session_id=restored.id)`

After that, the next request will use the restored `context_window` and `memo`.

## 2. Restore A Suspended Conversation After A Long Gap

Before reusing the restored session:

- validate the session id
- inspect whether `context_window` is still the right short-term context
- inspect whether `memo` still contains durable facts that should survive

If the short-term context is stale but the durable facts are still valid:

- keep `memo`
- trim or replace `context_window`

## 3. Restore Chat Continuity And TriggerFlow Progress Together

These are separate layers:

- `agently-session-memo` restores conversation continuity
- `agently-triggerflow-config` restores the flow definition
- `agently-triggerflow-execution-state` restores runtime progress

Use the combined sequence when all three matter:

1. rebuild or restore the correct flow definition
2. restore the saved execution state
3. restore the saved session state
4. reattach the session to the agent that will continue the conversation
5. re-inject any required runtime resources
6. continue the waiting execution or serve the next user turn

Do not assume session restore alone can recover a suspended workflow.

## 4. Web Chat Or Multi-Worker Services

Use a stable application-level conversation id as `session_id`.

Then:

- persist session snapshots to durable storage
- recreate agents on demand
- restore and activate the session when the user reconnects or another worker picks up the conversation

This keeps session continuity independent from a single process lifetime.
