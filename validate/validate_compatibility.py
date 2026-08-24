#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUPPORT = ROOT / "compatibility" / "support.json"
DEFAULT_BUNDLE_MANIFEST = ROOT / "bundles" / "manifest.json"
AGENTLY_ROOT = Path(os.environ.get("AGENTLY_ROOT", str(ROOT.parent / "Agently"))).resolve()
AGENTLY_INDEX = AGENTLY_ROOT / "compatibility" / "index.json"
AGENTLY_IN_DEVELOPMENT = AGENTLY_ROOT / "compatibility" / "in-development.json"
EXPECTED_ARCHIVES = {
    "v2": {
        "generation": "v2",
        "branch": "update/archive-v2-catalog",
        "last_supported_framework_version": "4.1.4.7",
        "status": "frozen",
    },
    "v1": {
        "generation": "v1",
        "branch": "update/archive-legacy-v1-catalog",
        "last_supported_framework_version": "4.1.1",
        "status": "frozen",
    },
}


def check(
    name: str,
    condition: bool,
    details: str,
    failures: list[str],
    passes: list[str],
) -> None:
    (passes if condition else failures).append(f"{name}: {details}")


def version_tuple(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split("."))


def archive_map(value: object) -> dict[str, dict]:
    if not isinstance(value, list):
        return {}
    result: dict[str, dict] = {}
    for item in value:
        if isinstance(item, dict) and isinstance(item.get("generation"), str):
            result[item["generation"]] = item
    return result


def git_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def main(*, require_remote_archives: bool = False) -> None:
    passes: list[str] = []
    failures: list[str] = []
    support = json.loads(SUPPORT.read_text(encoding="utf-8"))
    protocols = support.get("supported_protocols", {})
    authoring = protocols.get("authoring", [])
    devtools_guidance = protocols.get("devtools_guidance", [])
    catalog_generation = support.get("catalog_generation")
    aligned_version = support.get("aligned_framework_version")
    recommended_bundle = support.get("recommended_bundle")
    archives = archive_map(support.get("archived_catalog_generations"))
    stage_dependency = support.get("supported_runtime_dependencies", {}).get("agently_stage", {})

    check("schema_version", support.get("schema_version") == 1, "support manifest schema is 1", failures, passes)
    check("framework", support.get("framework") == "agently", "framework is agently", failures, passes)
    check("aligned_framework_version", aligned_version == "4.1.4.7", "catalog is aligned with Agently 4.1.4.7", failures, passes)
    check("catalog_generation", catalog_generation == "v3", "current catalog generation is v3", failures, passes)
    check("supported_generations", support.get("supported_catalog_generations") == ["v3"], "only the default v3 catalog is actively supported", failures, passes)
    check("recommended_bundle", recommended_bundle == "app", "app is the recommended bundle", failures, passes)
    check("authoring_protocols", isinstance(authoring, list) and bool(authoring), "authoring protocols are declared", failures, passes)
    check("devtools_protocols", isinstance(devtools_guidance, list) and bool(devtools_guidance), "DevTools guidance protocols are declared", failures, passes)
    check(
        "stage_dependency",
        stage_dependency.get("package") == "agently-stage"
        and stage_dependency.get("skill") == "agently-stage"
        and isinstance(stage_dependency.get("version_specifier"), str),
        "required Agently-Stage package, Skill owner, and range are declared",
        failures,
        passes,
    )
    check("archive_generations", set(archives) == set(EXPECTED_ARCHIVES), "v2 and v1 are the only archived catalog generations", failures, passes)
    for generation, expected in EXPECTED_ARCHIVES.items():
        actual = archives.get(generation)
        check(f"archive_{generation}", actual == expected, f"{generation} archive metadata is frozen and exact", failures, passes)
        if isinstance(actual, dict):
            branch = actual.get("branch", "")
            check(f"archive_{generation}_out_of_tree", "path" not in actual and "/" in branch, f"{generation} is referenced by branch rather than an in-tree path", failures, passes)
            local_ref = git_command("show-ref", "--verify", "--quiet", f"refs/heads/{branch}")
            check(
                f"archive_{generation}_local_ref",
                local_ref.returncode == 0,
                f"{generation} archive branch exists locally: {branch}",
                failures,
                passes,
            )
            if require_remote_archives:
                remote_ref = git_command("ls-remote", "--exit-code", "--heads", "origin", branch)
                check(
                    f"archive_{generation}_remote_ref",
                    remote_ref.returncode == 0 and bool(remote_ref.stdout.strip()),
                    f"{generation} archive branch exists on origin: {branch}",
                    failures,
                    passes,
                )
            last_supported = actual.get("last_supported_framework_version")
            if isinstance(aligned_version, str) and isinstance(last_supported, str):
                check(f"archive_{generation}_version_order", version_tuple(last_supported) <= version_tuple(aligned_version), f"{generation} is not newer than the current catalog target", failures, passes)

    v2_support = git_command("show", f"{EXPECTED_ARCHIVES['v2']['branch']}:compatibility/support.json")
    try:
        v2_manifest = json.loads(v2_support.stdout) if v2_support.returncode == 0 else {}
    except json.JSONDecodeError:
        v2_manifest = {}
    check(
        "archive_v2_content",
        v2_manifest.get("catalog_generation") == "v2"
        and v2_manifest.get("aligned_framework_version") == "4.1.4.7",
        "v2 archive content remains pinned to catalog v2 and Agently 4.1.4.7",
        failures,
        passes,
    )
    v1_tree = git_command(
        "cat-file",
        "-e",
        f"{EXPECTED_ARCHIVES['v1']['branch']}:legacy/v1/README.md",
    )
    check(
        "archive_v1_content",
        v1_tree.returncode == 0,
        "v1 archive branch contains the frozen legacy/v1 catalog record",
        failures,
        passes,
    )

    bundle_manifest = json.loads(DEFAULT_BUNDLE_MANIFEST.read_text(encoding="utf-8"))
    bundles = bundle_manifest.get("bundles", [])
    check("bundle_generation", bundle_manifest.get("catalog_generation") == catalog_generation, "bundle and support manifests use one generation", failures, passes)
    check("recommended_bundle_exists", any(bundle.get("id") == recommended_bundle for bundle in bundles), "recommended bundle exists", failures, passes)
    check(
        "archived_catalogs_not_bundled",
        not any(skill.startswith("legacy/") for bundle in bundles for skill in bundle.get("active_skills", [])),
        "default bundles do not expose archive paths",
        failures,
        passes,
    )

    index = json.loads(AGENTLY_INDEX.read_text(encoding="utf-8")) if AGENTLY_INDEX.exists() else None
    in_development = json.loads(AGENTLY_IN_DEVELOPMENT.read_text(encoding="utf-8")) if AGENTLY_IN_DEVELOPMENT.exists() else None
    if index is not None:
        current_target = index.get("latest_release")
        if in_development is not None:
            current_target = in_development.get("target_version", current_target)
        check("framework_target_alignment", aligned_version == current_target, "Skills alignment matches the Agently release/development target", failures, passes)

        release_path = index.get("release_files", {}).get(aligned_version)
        if isinstance(release_path, str):
            release = json.loads((AGENTLY_ROOT / release_path).read_text(encoding="utf-8"))
            release_skills = release.get("companions", {}).get("skills", {})
            check("release_authoring_protocol", release_skills.get("authoring_protocol") in authoring, "release authoring protocol is supported", failures, passes)
            check("release_devtools_protocol", release_skills.get("devtools_guidance_protocol") in devtools_guidance, "release DevTools guidance protocol is supported", failures, passes)
        else:
            check("development_target_exists", in_development is not None and in_development.get("target_version") == aligned_version, "unreleased alignment points to the in-development target", failures, passes)

    if in_development is not None:
        skills = in_development.get("companions", {}).get("skills", {})
        stage_support = in_development.get("runtime_support", {}).get("agently_stage", {})
        stage_guidance = skills.get("runtime_dependency_guidance", {}).get("agently_stage", {})
        in_dev_archives = archive_map(skills.get("archived_catalog_generations"))
        check("in_dev_authoring", skills.get("authoring_protocol") in authoring, "in-development authoring protocol is supported", failures, passes)
        check("in_dev_devtools", skills.get("devtools_guidance_protocol") in devtools_guidance, "in-development DevTools guidance protocol is supported", failures, passes)
        check("in_dev_catalog_generation", skills.get("catalog_generation") == catalog_generation, "in-development manifest selects v3", failures, passes)
        check("in_dev_bundle", skills.get("recommended_bundle") == recommended_bundle, "in-development manifest selects app", failures, passes)
        check("in_dev_archives", in_dev_archives == archives, "Agently and Agently-Skills declare identical archive metadata", failures, passes)
        check("in_dev_stage_role", stage_support.get("role") == "required_runtime_dependency", "Agently keeps Stage as required runtime", failures, passes)
        check("in_dev_stage_range", stage_support.get("version_specifier") == stage_dependency.get("version_specifier"), "Stage runtime range matches", failures, passes)
        check(
            "in_dev_stage_guidance",
            stage_guidance.get("skill") == stage_dependency.get("skill")
            and stage_guidance.get("version_specifier") == stage_dependency.get("version_specifier"),
            "Stage Skill guidance matches package compatibility",
            failures,
            passes,
        )

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_cn = (ROOT / "README_CN.md").read_text(encoding="utf-8")
    for label, text in (("readme", readme), ("readme_cn", readme_cn)):
        check(
            f"{label}_version",
            "4.1.4.7" in text and "4.1.4.8" not in text,
            "README states the current 4.1.4.7 release alignment",
            failures,
            passes,
        )
        check(f"{label}_catalog", "7-skill catalog" in text, "README states the seven-skill catalog", failures, passes)
        check(f"{label}_v2_archive", "update/archive-v2-catalog" in text, "README documents the v2 archive branch", failures, passes)
        check(f"{label}_v1_archive", "update/archive-legacy-v1-catalog" in text, "README documents the v1 archive branch", failures, passes)
        check(f"{label}_legacy_path_absent", "legacy/v1" not in text, "README does not expose an archived in-tree path", failures, passes)

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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-remote-archives",
        action="store_true",
        help="also require every declared archive branch to exist on origin",
    )
    args = parser.parse_args()
    main(require_remote_archives=args.require_remote_archives)
