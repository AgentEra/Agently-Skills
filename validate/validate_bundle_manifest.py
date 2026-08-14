#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "bundles" / "manifest.json"
VALID_KINDS = {"entry", "core", "addon", "specialized"}
EXPECTED_IDS = {"app", "migration"}
APP_SKILLS = {
    "agently",
    "agently-design",
    "agently-request",
    "agently-runtime",
    "agently-stage",
    "agently-dynamic-task",
    "agently-triggerflow",
}
MIGRATION_EXTRA_SKILLS = {
    "agently-migration",
}
RETIRED_SKILLS = {
    "agently-playbook",
    "agently-model-setup",
    "agently-prompt-management",
    "agently-output-control",
    "agently-model-response",
    "agently-agent-extensions",
    "agently-session-memory",
    "agently-knowledge-base",
    "agently-migration-playbook",
    "agently-langchain-to-agently",
    "agently-langgraph-to-triggerflow",
}


def check(name: str, condition: bool, details: str, failures: list[str], passes: list[str]) -> None:
    if condition:
        passes.append(f"{name}: {details}")
    else:
        failures.append(f"{name}: {details}")


def main() -> None:
    passes: list[str] = []
    failures: list[str] = []
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    bundles = data.get("bundles", [])
    bundle_map = {bundle["id"]: bundle for bundle in bundles}

    check("version_is_v3", data.get("version") == 3, "manifest version is 3", failures, passes)
    check("catalog_generation", data.get("catalog_generation") == "v2", "default manifest declares catalog generation v2", failures, passes)
    check("bundle_ids", set(bundle_map) == EXPECTED_IDS, "bundle ids match current app/migration set", failures, passes)

    for bundle in bundles:
        bundle_id = bundle["id"]
        active = bundle.get("active_skills", [])
        install = bundle.get("recommended_install_order", [])
        entry = bundle.get("entry_skill")

        check(f"{bundle_id}_kind", bundle.get("kind") in VALID_KINDS, "kind is valid", failures, passes)
        check(f"{bundle_id}_skills", bool(active), "bundle declares skills", failures, passes)
        check(
            f"{bundle_id}_skills_exist",
            all((ROOT / "skills" / skill).exists() for skill in active),
            "all bundle skills exist",
            failures,
            passes,
        )
        check(
            f"{bundle_id}_install_order",
            install and install[0] == "agently",
            "bundle install order starts with agently",
            failures,
            passes,
        )
        check(
            f"{bundle_id}_install_matches_active",
            set(install) == set(active),
            "recommended install order covers active skills exactly",
            failures,
            passes,
        )
        check(
            f"{bundle_id}_entry",
            entry == "agently",
            "entry skill is agently",
            failures,
            passes,
        )

    app = bundle_map["app"]
    migration = bundle_map["migration"]
    app_active = set(app.get("active_skills", []))
    migration_active = set(migration.get("active_skills", []))

    check(
        "app_skills",
        app_active == APP_SKILLS,
        "app bundle combines router, cross-layer design, request, Stage, runtime, Dynamic Task, and TriggerFlow skills",
        failures,
        passes,
    )
    check(
        "migration_base",
        migration.get("base_bundle") == "app",
        "migration attaches to app bundle",
        failures,
        passes,
    )
    check(
        "migration_superset",
        app_active.issubset(migration_active),
        "migration includes every app skill",
        failures,
        passes,
    )
    check(
        "migration_extra_skills",
        MIGRATION_EXTRA_SKILLS.issubset(migration_active),
        "migration adds compact framework migration skill",
        failures,
        passes,
    )
    check(
        "default_no_legacy_v1_skills",
        not (migration_active | app_active).intersection(RETIRED_SKILLS),
        "default bundles do not reference legacy-only V1 skill ids",
        failures,
        passes,
    )

    print("V2 bundle manifest validation")
    print(f"passes: {len(passes)}")
    for item in passes:
        print(f"PASS  {item}")
    print(f"failures: {len(failures)}")
    for item in failures:
        print(f"FAIL  {item}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
