# Agently Output Control Authoring Notes

This file records author-side constraints for maintaining the `agently-output-control` skill.

## Authoring Rules

- All skill-facing content must be written in English.
- This includes `SKILL.md`, skill references, usage notes, and any explanatory text intended for skill users.
- Do not leave mixed-language headings, lists, inline notes, or examples in the published skill.
- Use the public Agently GitHub repository as the publishable source-code citation target.
- Use local checkouts only for author-side validation.
- Use `examples/` as runnable examples, not as authority over implementation semantics.
- Use `tests/` to validate behavior and edge cases.
- Use the public docs portal only as a low-priority supplement when source, examples, and tests are insufficient: `https://agently.tech/docs/en/`.
- Keep author-side constraints out of `SKILL.md` and the skill references unless they directly help the skill user complete a task.
- Keep the frontmatter and opening paragraph phrased as a direct leaf for output-side schema, retries, parsing, and structured streaming, not as a one-request architecture router.
- Lead with output-contract problems such as structured fields, parsed results, retries, response reuse, or structured streaming before naming internal Agently API methods.
- Published guidance for this skill should recommend async-first usage whenever the caller runtime can support it.
- Frame sync getters and sync generators as compatibility wrappers over the async core, not as the primary execution model.
- Route provider setup, auth, endpoint, and transport questions to `agently-model-setup`.
- Route prompt-slot, mapping, attachment-composition, and low-level `chat_history` questions to `agently-input-composition`.
