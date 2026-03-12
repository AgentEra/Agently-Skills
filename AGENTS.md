# Agently Skills Repository

This repository publishes the Agently Skills V2 catalog under `skills/`.

## Repository Layout

- `skills/`
  Published installable V2 skill payloads.
- `validate/`
  Shared V2 validation sources and fixtures that stay under version control.
- `spec/`
  Local-only author workspace. Ignore it and do not treat it as publishable content.

## Authoring Priorities

- Route unresolved product, assistant, and workflow requests through `agently-playbook` first.
- Prefer Agently-native capabilities before custom output parsers, retry loops, or orchestration layers.
- Keep public skill boundaries capability-first and mutually exclusive.
- Treat multi-agent, judge, and review flows as scenario recipes unless they need a dedicated framework surface.
- Keep `bundles/manifest.json`, README install guidance, and V2 validators in sync.
- When changing trigger boundaries, update both route fixtures and implementation fixtures.

## Primary References

- `bundles/manifest.json`
- `validate/fixtures/route_cases.json`
- `validate/fixtures/implementation_cases.json`
- `validate/validate_catalog.py`
- `validate/validate_bundle_manifest.py`
- `validate/validate_trigger_paths.py`
- `validate/validate_native_usage.py`
- `validate/validate_live_scenarios.py`
