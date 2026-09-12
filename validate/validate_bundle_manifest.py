#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "bundles" / "manifest.json"
SKILLS = ROOT / "skills"
VALID_KINDS = {"entry", "core", "addon", "specialized"}
EXPECTED_BUNDLE_IDS = {"app", "migration"}
APP_ORDER = [
    "agently",
    "agently-design",
    "agently-request",
    "agently-runtime",
    "agently-stage",
    "agently-triggerflow",
]
MIGRATION_EXTRA_ORDER = ["agently-migration"]
EXPECTED_CATALOG = set(APP_ORDER + MIGRATION_EXTRA_ORDER)
RETIRED_SKILL = "agently-" + "dynamic-task"


def check(
    name: str,
    condition: bool,
    details: str,
    failures: list[str],
    passes: list[str],
) -> None:
    (passes if condition else failures).append(f"{name}: {details}")


def has_unique_strings(values: object) -> bool:
    return (
        isinstance(values, list)
        and all(isinstance(value, str) and value for value in values)
        and len(values) == len(set(values))
    )


def main() -> None:
    passes: list[str] = []
    failures: list[str] = []
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    bundles = data.get("bundles", [])
    bundle_ids = [bundle.get("id") for bundle in bundles if isinstance(bundle, dict)]
    bundle_map = {
        bundle["id"]: bundle
        for bundle in bundles
        if isinstance(bundle, dict) and isinstance(bundle.get("id"), str)
    }
    actual_catalog = {path.name for path in SKILLS.iterdir() if path.is_dir()}

    check("manifest_schema", data.get("version") == 3, "manifest schema version is 3", failures, passes)
    check("catalog_generation", data.get("catalog_generation") == "v3", "catalog generation is v3", failures, passes)
    check("bundle_ids_unique", len(bundle_ids) == len(set(bundle_ids)), "bundle ids are unique", failures, passes)
    check("bundle_ids_exact", set(bundle_map) == EXPECTED_BUNDLE_IDS, "only app and migration bundles are public", failures, passes)

    for bundle_id, bundle in bundle_map.items():
        active = bundle.get("active_skills")
        install = bundle.get("recommended_install_order")
        check(f"{bundle_id}_kind", bundle.get("kind") in VALID_KINDS, "bundle kind is valid", failures, passes)
        check(f"{bundle_id}_active_unique", has_unique_strings(active), "active skills are unique strings", failures, passes)
        check(f"{bundle_id}_install_unique", has_unique_strings(install), "install order contains unique strings", failures, passes)
        if not isinstance(active, list) or not isinstance(install, list):
            continue
        check(f"{bundle_id}_install_matches_active", install == active, "install order covers active skills exactly once", failures, passes)
        check(f"{bundle_id}_entry", bundle.get("entry_skill") == "agently" and active[:1] == ["agently"], "agently is the installed entry skill", failures, passes)
        check(f"{bundle_id}_skills_exist", all((SKILLS / skill).is_dir() for skill in active), "every bundled skill exists", failures, passes)
        check(f"{bundle_id}_retired_absent", RETIRED_SKILL not in active, "retired standalone TaskDAG skill is absent", failures, passes)

    app = bundle_map.get("app", {})
    migration = bundle_map.get("migration", {})
    app_active = app.get("active_skills", [])
    migration_active = migration.get("active_skills", [])
    app_set = set(app_active) if isinstance(app_active, list) else set()
    migration_set = set(migration_active) if isinstance(migration_active, list) else set()
    extra_set = set(MIGRATION_EXTRA_ORDER)

    check("app_exact", app_active == APP_ORDER, "app bundle has the six current application skills in install order", failures, passes)
    check("migration_base", migration.get("base_bundle") == "app", "migration extends app", failures, passes)
    check("migration_exact", migration_active == APP_ORDER + MIGRATION_EXTRA_ORDER, "migration contains app plus only agently-migration", failures, passes)
    check("migration_union", migration_set == app_set | extra_set, "migration equals app union migration extras", failures, passes)
    check("catalog_expected", actual_catalog == EXPECTED_CATALOG, "skills directory is the exact seven-skill catalog", failures, passes)
    check("manifest_catalog_union", app_set | migration_set == actual_catalog, "bundle union equals the public skills directory", failures, passes)

    print("V3 bundle manifest validation")
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
