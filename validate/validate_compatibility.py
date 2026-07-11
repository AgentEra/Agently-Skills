#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUPPORT = ROOT / "compatibility" / "support.json"
DEFAULT_BUNDLE_MANIFEST = ROOT / "bundles" / "manifest.json"
AGENTLY_ROOT = ROOT.parent / "Agently"
AGENTLY_INDEX = AGENTLY_ROOT / "compatibility" / "index.json"
AGENTLY_IN_DEVELOPMENT = AGENTLY_ROOT / "compatibility" / "in-development.json"


def check(name: str, condition: bool, details: str, failures: list[str], passes: list[str]) -> None:
    if condition:
        passes.append(f"{name}: {details}")
    else:
        failures.append(f"{name}: {details}")


def version_tuple(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split("."))


def main() -> None:
    passes: list[str] = []
    failures: list[str] = []

    support = json.loads(SUPPORT.read_text(encoding="utf-8"))
    protocols = support.get("supported_protocols", {})
    authoring = protocols.get("authoring", [])
    devtools_guidance = protocols.get("devtools_guidance", [])
    catalog_generation = support.get("catalog_generation")
    supported_catalog_generations = support.get("supported_catalog_generations", [])
    recommended_bundle = support.get("recommended_bundle")
    aligned_version = support.get("aligned_framework_version")
    archived_catalogs = support.get("archived_catalog_generations", [])

    check("schema_version", support.get("schema_version") == 1, "support manifest schema is 1", failures, passes)
    check("framework", support.get("framework") == "agently", "framework is agently", failures, passes)
    check("aligned_framework_version", isinstance(aligned_version, str), "aligned framework version exists", failures, passes)
    check("catalog_generation", catalog_generation == "v2", "current support manifest declares catalog generation v2", failures, passes)
    check(
        "supported_catalog_generations",
        isinstance(supported_catalog_generations, list) and catalog_generation in supported_catalog_generations,
        "current generation is listed in supported catalog generations",
        failures,
        passes,
    )
    check("recommended_bundle", recommended_bundle == "app", "current support manifest recommends app bundle", failures, passes)
    check("authoring_protocols", bool(authoring), "authoring protocols declared", failures, passes)
    check("devtools_guidance_protocols", bool(devtools_guidance), "devtools guidance protocols declared", failures, passes)
    archived_v1 = next((item for item in archived_catalogs if item.get("generation") == "v1"), None)
    check("archived_v1_listed", isinstance(archived_v1, dict), "support manifest lists archived V1 generation", failures, passes)
    if isinstance(archived_v1, dict):
        check(
            "archived_v1_branch",
            isinstance(archived_v1.get("branch"), str) and "/" in archived_v1.get("branch", ""),
            "archived V1 catalog is referenced by branch, not by a default-branch path",
            failures,
            passes,
        )
        check(
            "archived_v1_no_path",
            "path" not in archived_v1,
            "archived V1 catalog does not declare an in-tree path",
            failures,
            passes,
        )
        check(
            "archived_v1_last_supported",
            archived_v1.get("last_supported_framework_version") == "4.1.1",
            "archived V1 catalog declares its last supported Agently version",
            failures,
            passes,
        )
        check(
            "archived_v1_frozen",
            archived_v1.get("status") == "frozen",
            "archived V1 catalog is marked frozen",
            failures,
            passes,
        )

    default_manifest = json.loads(DEFAULT_BUNDLE_MANIFEST.read_text(encoding="utf-8"))
    check(
        "default_bundle_manifest_generation",
        default_manifest.get("catalog_generation") == catalog_generation,
        "default bundle manifest catalog generation matches support manifest",
        failures,
        passes,
    )
    check(
        "recommended_bundle_exists",
        any(bundle.get("id") == recommended_bundle for bundle in default_manifest.get("bundles", [])),
        "recommended bundle exists in default bundle manifest",
        failures,
        passes,
    )

    default_skills = {
        skill
        for bundle in default_manifest.get("bundles", [])
        for skill in bundle.get("active_skills", [])
    }
    archived_default_refs = {skill for skill in default_skills if skill.startswith("legacy/")}
    check(
        "archived_catalogs_not_default_bundle",
        not archived_default_refs,
        "default bundle active skills do not reference archived catalog paths",
        failures,
        passes,
    )

    if AGENTLY_INDEX.exists():
        index = json.loads(AGENTLY_INDEX.read_text(encoding="utf-8"))
        release_files = index.get("release_files", {})
        current_target = index.get("latest_release")
        if AGENTLY_IN_DEVELOPMENT.exists():
            current_target = json.loads(
                AGENTLY_IN_DEVELOPMENT.read_text(encoding="utf-8")
            ).get("target_version", current_target)
        check(
            "aligned_current_framework_target",
            aligned_version == current_target,
            "Agently-Skills aligned version matches the current Agently development/release target",
            failures,
            passes,
        )
        release_path = release_files.get(aligned_version)
        if not isinstance(release_path, str) and AGENTLY_IN_DEVELOPMENT.exists():
            in_development = json.loads(AGENTLY_IN_DEVELOPMENT.read_text(encoding="utf-8"))
            check(
                "aligned_development_target",
                in_development.get("target_version") == aligned_version,
                "aligned framework version may point at the Agently in-development target before release",
                failures,
                passes,
            )
        check(
            "aligned_release_manifest_entry",
            isinstance(release_path, str) or AGENTLY_IN_DEVELOPMENT.exists(),
            "Agently compatibility registry contains the aligned release entry or matching in-development target",
            failures,
            passes,
        )
        if isinstance(release_path, str):
            release_manifest = json.loads((AGENTLY_ROOT / release_path).read_text(encoding="utf-8"))
            skills = release_manifest.get("companions", {}).get("skills", {})
            check(
                "authoring_protocol_supported",
                skills.get("authoring_protocol") in authoring,
                "Agently release authoring protocol is supported by Agently-Skills",
                failures,
                passes,
            )
            check(
                "devtools_guidance_protocol_supported",
                skills.get("devtools_guidance_protocol") in devtools_guidance,
                "Agently release DevTools guidance protocol is supported by Agently-Skills",
                failures,
                passes,
            )

    if AGENTLY_IN_DEVELOPMENT.exists():
        in_development = json.loads(AGENTLY_IN_DEVELOPMENT.read_text(encoding="utf-8"))
        skills = in_development.get("companions", {}).get("skills", {})
        target_version = in_development.get("target_version")
        check(
            "in_development_authoring_protocol_supported",
            skills.get("authoring_protocol") in authoring,
            "Agently in-development authoring protocol is supported by Agently-Skills",
            failures,
            passes,
        )
        check(
            "in_development_devtools_guidance_protocol_supported",
            skills.get("devtools_guidance_protocol") in devtools_guidance,
            "Agently in-development DevTools guidance protocol is supported by Agently-Skills",
            failures,
            passes,
        )
        check(
            "in_development_catalog_generation_supported",
            skills.get("catalog_generation") == catalog_generation,
            "Agently in-development Skills catalog generation is supported by Agently-Skills",
            failures,
            passes,
        )
        check(
            "in_development_recommended_bundle_supported",
            skills.get("recommended_bundle") == recommended_bundle,
            "Agently in-development recommended Skills bundle is supported by Agently-Skills",
            failures,
            passes,
        )
        in_dev_archives = skills.get("archived_catalog_generations", [])
        in_dev_archived_v1 = next((item for item in in_dev_archives if item.get("generation") == "v1"), None)
        check(
            "in_development_archived_v1_declared",
            isinstance(in_dev_archived_v1, dict),
            "Agently in-development manifest declares archived V1 generation",
            failures,
            passes,
        )
        if isinstance(in_dev_archived_v1, dict) and isinstance(archived_v1, dict):
            last_supported = in_dev_archived_v1.get("last_supported_framework_version")
            check(
                "in_development_archived_v1_last_supported_matches",
                last_supported == archived_v1.get("last_supported_framework_version"),
                "Agently in-development archived V1 last-supported version matches Agently-Skills",
                failures,
                passes,
            )
            check(
                "in_development_archived_v1_branch_matches",
                in_dev_archived_v1.get("branch") == archived_v1.get("branch"),
                "Agently in-development archived V1 branch matches Agently-Skills",
                failures,
                passes,
            )
            if isinstance(target_version, str) and isinstance(last_supported, str):
                check(
                    "archived_v1_not_after_target",
                    version_tuple(last_supported) <= version_tuple(target_version),
                    "archived V1 last-supported version is not newer than the current development target",
                    failures,
                    passes,
                )

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_cn = (ROOT / "README_CN.md").read_text(encoding="utf-8")
    aligned_version = str(aligned_version)
    check(
        "readme_mentions_aligned_version",
        f"Agently {aligned_version}" in readme,
        "README mentions the aligned Agently release line",
        failures,
        passes,
    )
    check(
        "readme_no_legacy_v1_path",
        "legacy/v1" not in readme,
        "README does not document retired catalog directories as an in-tree path",
        failures,
        passes,
    )
    check(
        "readme_cn_no_legacy_v1_path",
        "legacy/v1" not in readme_cn,
        "README_CN does not document retired catalog directories as an in-tree path",
        failures,
        passes,
    )
    check(
        "readme_cn_mentions_aligned_version",
        f"Agently {aligned_version}" in readme_cn,
        "README_CN mentions the aligned Agently release line",
        failures,
        passes,
    )

    print("Compatibility support validation")
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
