# Agently Skills Repository

This repository contains published Agently skills under `skills/` and author-side planning, validation, and maintenance material under `spec/`.

## Repository Layout

- `skills/`
  Published installable skill payloads.
- `spec/`
  Author-side rules, roadmap notes, validation scripts, and trigger fixtures. These files do not belong in published skill payloads.

## Authoring Priorities

- Keep frontmatter discovery boundaries explicit and mutually exclusive, especially for nearby routing skills.
- Prefer narrow install guidance and explicit bundle boundaries over assuming full-repository coexistence.
- Add or update trigger fixtures when changing routing descriptions or other high-overlap metadata.

## Primary References

- `spec/skill-authoring-rules.md`
- `spec/skill-discovery-and-packaging-plan.md`
- `spec/*-authoring.md`
- `spec/*-validation.md`
