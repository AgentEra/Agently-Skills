# Agently Model Setup Authoring Notes

This file records author-side constraints for maintaining the `agently-model-setup` skill.

## Authoring Rules

- All skill-facing content must be written in English.
- This includes `SKILL.md`, skill references, usage notes, and any explanatory text intended for skill users.
- Do not leave mixed-language headings, lists, inline notes, or examples in the published skill.
- Use the public Agently GitHub repository as the publishable source-code citation target.
- Use local checkouts only for author-side validation.
- Use `examples/` as runnable examples, not as authority over implementation semantics.
- Use `tests/` to validate behavior and edge cases.
- Use the public docs portal only as a low-priority supplement for terminology, provider pages, and navigation: `https://agently.tech/docs/en/`.
- Keep author-side constraints out of `SKILL.md` and the skill references unless they directly help the skill user complete a task.
- Keep the frontmatter and opening paragraph phrased as a direct leaf for model connection and request-transport setup, not as a one-request architecture router.
- Lead with scenario language such as local model setup, Ollama, OpenAI-compatible endpoints, generator-model and judge-model wiring, or connectivity checks before naming internal Agently APIs.
- Route prompt-slot, mapping, attachment-composition, and low-level `chat_history` questions to `agently-input-composition`.
- Route `.output(...)`, `ensure_keys`, structured streaming, and response-consumption questions to `agently-output-control`.
- Route embeddings requests to `agently-embeddings`.
