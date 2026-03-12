#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "bundles" / "manifest.json"
VALID_KINDS = {"entry", "core", "addon", "specialized"}
EXPECTED_IDS = {"entry-general", "request-core", "request-extensions", "workflow-core", "migration"}


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

    check("version_is_v2", data.get("version") == 2, "manifest version is 2", failures, passes)
    check("bundle_ids", set(bundle_map) == EXPECTED_IDS, "bundle ids match V2 set", failures, passes)

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
            install and install[0] == "agently-playbook",
            "bundle install order starts with agently-playbook",
            failures,
            passes,
        )
        check(
            f"{bundle_id}_entry",
            entry == "agently-playbook",
            "entry skill is agently-playbook",
            failures,
            passes,
        )

    request_extensions = bundle_map["request-extensions"]
    check(
        "request_extensions_base",
        request_extensions.get("base_bundle") == "request-core",
        "request-extensions attaches to request-core",
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
