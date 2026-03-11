# Source Map

This reference points to the most relevant public Agently sources for session-memo work.

## 1. Core implementation files

- [SessionExtension](https://github.com/AgentEra/Agently/blob/main/agently/builtins/agent_extensions/SessionExtension.py)
  Session activation, session-backed chat-history overrides, request-prefix injection, and finally-stage recording live here.
- [Session core](https://github.com/AgentEra/Agently/blob/main/agently/core/Session.py)
  `full_context`, `context_window`, `memo`, resize analysis, resize handlers, and serialization live here.
- [Agent core](https://github.com/AgentEra/Agently/blob/main/agently/core/Agent.py)
  The low-level `set_chat_history(...)`, `add_chat_history(...)`, and `reset_chat_history()` helpers live here before session override is applied.
- [AgentlyPromptGenerator](https://github.com/AgentEra/Agently/blob/main/agently/builtins/plugins/PromptGenerator/AgentlyPromptGenerator.py)
  Prompt materialization and `chat_history` message rendering live here.
- [ChatSessionExtension](https://github.com/AgentEra/Agently/blob/main/agently/builtins/agent_extensions/ChatSessionExtension.py)
  Deprecated legacy path kept only for migration context; do not treat it as the primary design.

## 2. Example files

- [Basic session examples](https://github.com/AgentEra/Agently/blob/main/examples/basic/session.py)
- [Chat history step-by-step example](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/08-chat_history.py)
- [Auto-loop example with runtime memo](https://github.com/AgentEra/Agently/blob/main/examples/step_by_step/12-auto_loop.py)

## 3. Test files

- [Session extension tests](https://github.com/AgentEra/Agently/blob/main/tests/test_extensions/test_session_extension.py)
- [Session core tests](https://github.com/AgentEra/Agently/blob/main/tests/test_cores/test_session.py)
- [Prompt generator tests](https://github.com/AgentEra/Agently/blob/main/tests/test_plugins/test_prompt_generator/test_agently_prompt_generator.py)

## 4. Public Online Reference

- GitHub repository: `https://github.com/AgentEra/Agently`
- Docs home: `https://agently.tech/docs/en/`
- Session memo overview: `https://agently.tech/docs/en/agent-extensions/session-memo/index.html`
- Session quickstart: `https://agently.tech/docs/en/agent-extensions/session-memo/quickstart.html`
- Session concepts: `https://agently.tech/docs/en/agent-extensions/session-memo/concepts.html`
- Session resize docs: `https://agently.tech/docs/en/agent-extensions/session-memo/resize.html`
- Session memo docs: `https://agently.tech/docs/en/agent-extensions/session-memo/memo.html`
- Session serialization docs: `https://agently.tech/docs/en/agent-extensions/session-memo/serialization.html`
