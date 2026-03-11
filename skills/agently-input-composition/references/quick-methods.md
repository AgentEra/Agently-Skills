# Quick Methods

Agently exposes convenience methods for common input-composition operations.

## 1. Default Layering Rule

On an agent instance:

- without `always=True`, quick methods write to the request prompt
- with `always=True`, quick methods write to the agent prompt

This is the fastest way to decide whether a prompt part is persistent or one-shot.

## 2. Main Quick Methods

- `system(...)`
  Use for direct system framing.
- `role(...)`
  Use for assistant identity or persona. This is a high-level helper, not just a raw single-slot assignment.
- `rule(...)`
  Use for prominent behavior rules. This is also a helper, not just a blind slot setter.
- `user_info(...)`
  Use for user-specific background information that should influence the reply.
- `input(...)`
  Use for the main task or question.
- `info(...)`
  Use for supporting facts or structured context.
- `instruct(...)`
  Use for explicit directives and response constraints.
- `examples(...)`
  Use for few-shot demonstrations.
- `attachment(...)`
  Use for rich content attached to the user message.

## 3. When Convenience Wrappers Are The Right Tool

Use quick methods when:

- the prompt part matches a common intent
- concise chaining is more valuable than explicit slot-by-slot control
- the prompt should read clearly in code

## 4. When Exact Prompt APIs Are Better

Use `set_agent_prompt(...)` or `set_request_prompt(...)` when:

- the caller needs the `developer` slot
- the caller wants a custom prompt key
- the caller wants exact slot placement with no helper behavior
- the caller is debugging prompt shape and wants the least abstraction

## 5. Practical Rule For `role()`, `rule()`, And `user_info()`

Treat these as high-level helpers that inject prompt structure for a common intention.

If the user needs exact low-level message composition, switch to explicit slot APIs instead of describing these helpers as raw one-line aliases.
