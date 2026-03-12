# Agently Skills Repository

This repository contains published Agently skills under `skills/` and author-side planning, validation, and maintenance material under `spec/`.

## Repository Layout

- `skills/`
  Published installable skill payloads.
- `spec/`
  Author-side rules, roadmap notes, validation scripts, and trigger fixtures. These files do not belong in published skill payloads.

## Authoring Priorities

- Keep frontmatter discovery boundaries explicit and mutually exclusive, especially for nearby routing skills.
- Prefer scenario-led trigger language over framework-led trigger language when the user may reasonably ask for the same capability without naming Agently.
- Treat internal product words such as `Agently` or `TriggerFlow` as supporting confirmation terms, not as the primary discovery requirement, unless the user already names the exact framework surface.
- Prefer narrow install guidance and explicit bundle boundaries over assuming full-repository coexistence.
- Keep public install docs aligned with the current bundle-first activation story, not only the catalog layout.
- Keep the public `bundles/manifest.json` aligned with README install guidance and internal bundle validation.
- Add or update trigger fixtures when changing routing descriptions or other high-overlap metadata, including generic model-app requests that do not mention Agently explicitly.

## Primary References

- `spec/skill-authoring-rules.md`
- `bundles/manifest.json`
- `spec/skill-bundles.json`
- `spec/validate_skill_bundles.py`
- `spec/validate_skill_trigger_live.py`
- `spec/skill-discovery-and-packaging-plan.md`
- `spec/*-authoring.md`
- `spec/*-validation.md`
