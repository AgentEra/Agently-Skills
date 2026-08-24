#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
BUNDLE_MANIFEST = ROOT / "bundles" / "manifest.json"
ROUTE_FIXTURES = ROOT / "validate" / "fixtures" / "route_cases.json"
REFERENCE_FIXTURES = ROOT / "validate" / "fixtures" / "reference_retrieval_cases.json"
IMPLEMENTATION_FIXTURES = ROOT / "validate" / "fixtures" / "implementation_cases.json"
EXPECTED_SKILLS = {
    "agently",
    "agently-design",
    "agently-migration",
    "agently-request",
    "agently-runtime",
    "agently-stage",
    "agently-triggerflow",
}
PUBLIC_MARKDOWN = [ROOT / "README.md", ROOT / "README_CN.md", ROOT / "AGENTS.md"]
PUBLIC_MACHINE_FILES = [BUNDLE_MANIFEST, ROOT / "compatibility" / "support.json"]
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
ENTRY_RESOURCE = re.compile(
    r"`((?:\.\./)*(?:[a-z0-9-]+/)*(?:references|examples|assets|scripts)/[^`\n]+)`"
)
RETIRED_TASKDAG_SKILL = "agently-" + "dynamic-task"

# These checks stay at the single owning document. They protect architectural
# and safety contracts without requiring the same prose to be copied across
# every Skill surface.
OWNING_CONTRACTS: dict[str, tuple[Path, tuple[str, ...]]] = {
    "taskdag_owner_and_gap": (
        SKILLS / "agently" / "references" / "task-dag.md",
        (
            "TaskDAGValidator",
            "TaskDAGResolver",
            "TaskDAGExecutor",
            "DynamicTask",
            "TriggerFlow",
            "TaskDAGContext",
            "task_dag_resolver()",
        ),
    ),
    "execution_topology_evidence": (
        SKILLS
        / "agently-design"
        / "references"
        / "execution-topology-validation.md",
        (
            "prompt.input",
            "prompt.info",
            "prompt.instruct",
            "output schema",
            "value edge",
            "signal/event edge",
            "RuntimeEvent",
        ),
    ),
    "selection_freshness": (
        SKILLS
        / "agently-design"
        / "references"
        / "information-and-evidence-design.md",
        ("selection key", "freshness", "Host correlation", "canonical lookup"),
    ),
    "rule_first_validation": (
        SKILLS / "agently-request" / "references" / "output-control.md",
        ("input", "info", "instruct", "output", "blind gate discovery"),
    ),
    "model_request_result_views": (
        SKILLS / "agently-request" / "references" / "model-request-result.md",
        (
            "get_data(...)",
            "get_text()",
            "get_meta()",
            "get_data_object()",
            "get_async_generator(type=...)",
        ),
    ),
    "terminal_file_promotion": (
        SKILLS / "agently-runtime" / "references" / "actions-runtime.md",
        ("TaskWorkspace.atomic_promote_file", "digest", "candidate"),
    ),
    "triggerflow_state_and_lifecycle": (
        SKILLS / "agently-triggerflow" / "SKILL.md",
        ("Save/load", "serializes", "replaces", "flow_data", "finite self-closing", "execution handle"),
    ),
}


def check(
    name: str,
    condition: bool,
    details: str,
    failures: list[str],
    passes: list[str],
) -> None:
    (passes if condition else failures).append(f"{name}: {details}")


def markdown_section(text: str, heading: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else ""


def readme_catalog(path: Path, heading: str) -> list[str]:
    section = markdown_section(path.read_text(encoding="utf-8"), heading)
    return re.findall(r"^-\s+`(agently(?:-[a-z0-9-]+)?)`\s+-", section, re.MULTILINE)


def parse_frontmatter(path: Path) -> tuple[dict[str, object] | None, str | None]:
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if match is None:
        return None, "missing YAML frontmatter"
    try:
        value = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, f"invalid YAML frontmatter: {exc}"
    if not isinstance(value, dict):
        return None, "frontmatter is not a mapping"
    return value, None


def local_link_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split(maxsplit=1)[0]
    target = unquote(target).split("#", 1)[0]
    if not target or target.startswith(("http://", "https://", "mailto:", "data:")):
        return None
    candidate = Path(target)
    return candidate.resolve() if candidate.is_absolute() else (source.parent / candidate).resolve()


def text_files_for_retired_id_check() -> list[Path]:
    files = PUBLIC_MARKDOWN + PUBLIC_MACHINE_FILES + [
        ROUTE_FIXTURES,
        REFERENCE_FIXTURES,
        IMPLEMENTATION_FIXTURES,
    ]
    files.extend(
        path
        for path in SKILLS.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".py", ".json", ".yaml", ".yml"}
    )
    return files


def validate_frontmatter(failures: list[str], passes: list[str]) -> None:
    for skill_name in sorted(EXPECTED_SKILLS):
        skill_md = SKILLS / skill_name / "SKILL.md"
        check(f"{skill_name}_entry", skill_md.is_file(), "SKILL.md exists", failures, passes)
        if not skill_md.is_file():
            continue
        metadata, error = parse_frontmatter(skill_md)
        check(f"{skill_name}_frontmatter_yaml", metadata is not None, error or "frontmatter is valid YAML", failures, passes)
        if metadata is None:
            continue
        check(
            f"{skill_name}_frontmatter_name",
            metadata.get("name") == skill_name,
            "frontmatter name exactly equals the directory name",
            failures,
            passes,
        )
        description = metadata.get("description")
        check(
            f"{skill_name}_frontmatter_description",
            isinstance(description, str) and bool(description.strip()),
            "frontmatter description is a non-empty string",
            failures,
            passes,
        )


def validate_catalog_sets(failures: list[str], passes: list[str]) -> None:
    actual = {path.name for path in SKILLS.iterdir() if path.is_dir()}
    readme_en = readme_catalog(ROOT / "README.md", "Current Catalog")
    readme_zh = readme_catalog(ROOT / "README_CN.md", "当前 Catalog")
    manifest = json.loads(BUNDLE_MANIFEST.read_text(encoding="utf-8"))
    manifest_skills = {
        skill
        for bundle in manifest.get("bundles", [])
        for skill in bundle.get("active_skills", [])
    }

    check("catalog_directory_exact", actual == EXPECTED_SKILLS, "skills directory is the exact seven-skill catalog", failures, passes)
    check("readme_en_unique", len(readme_en) == len(set(readme_en)), "README catalog entries are unique", failures, passes)
    check("readme_zh_unique", len(readme_zh) == len(set(readme_zh)), "README_CN catalog entries are unique", failures, passes)
    check("readme_en_exact", set(readme_en) == EXPECTED_SKILLS, "README catalog equals the public catalog", failures, passes)
    check("readme_zh_exact", set(readme_zh) == EXPECTED_SKILLS, "README_CN catalog equals the public catalog", failures, passes)
    check("manifest_catalog_exact", manifest_skills == EXPECTED_SKILLS, "bundle union equals the public catalog", failures, passes)
    check("catalog_surfaces_agree", actual == set(readme_en) == set(readme_zh) == manifest_skills, "directory, READMEs, and bundle manifest publish one catalog set", failures, passes)


def validate_local_links(failures: list[str], passes: list[str]) -> None:
    markdown_files = PUBLIC_MARKDOWN + sorted(SKILLS.rglob("*.md"))
    link_count = 0
    reachable_resources: set[Path] = set()
    for source in markdown_files:
        text = source.read_text(encoding="utf-8")
        for index, match in enumerate(MARKDOWN_LINK.finditer(text), start=1):
            target = local_link_target(source, match.group(1))
            if target is None:
                continue
            link_count += 1
            within_repo = target == ROOT or ROOT in target.parents
            if within_repo:
                reachable_resources.add(target)
            check(
                f"markdown_link_{source.relative_to(ROOT)}_{index}",
                within_repo and target.exists(),
                f"local Markdown link resolves inside the repository: {match.group(1)}",
                failures,
                passes,
            )

    entry_resource_count = 0
    for skill_name in sorted(EXPECTED_SKILLS):
        skill_dir = SKILLS / skill_name
        source = skill_dir / "SKILL.md"
        if not source.is_file():
            continue
        for index, raw_target in enumerate(ENTRY_RESOURCE.findall(source.read_text(encoding="utf-8")), start=1):
            entry_resource_count += 1
            target = (skill_dir / raw_target).resolve()
            reachable_resources.add(target)
            check(
                f"entry_resource_{skill_name}_{index}",
                ROOT in target.parents and target.exists(),
                f"SKILL.md resource reference resolves: {raw_target}",
                failures,
                passes,
            )

    implementation = json.loads(IMPLEMENTATION_FIXTURES.read_text(encoding="utf-8"))
    for case in implementation.get("cases", []):
        raw_path = case.get("reference_example")
        target = (ROOT / raw_path).resolve() if isinstance(raw_path, str) else ROOT.parent
        if isinstance(raw_path, str):
            reachable_resources.add(target)
        check(
            f"implementation_path_{case.get('id', '<missing-id>')}",
            isinstance(raw_path, str) and ROOT in target.parents and target.is_file(),
            "implementation fixture points to an existing repository file",
            failures,
            passes,
        )

    references = json.loads(REFERENCE_FIXTURES.read_text(encoding="utf-8"))
    for case in references.get("cases", []):
        declared_paths = {
            path
            for path_set in case.get("expected_reference_sets", [])
            for path in path_set
            if isinstance(path, str)
        } | {
            path for path in case.get("excerpt_anchors", {}) if isinstance(path, str)
        }
        for index, raw_path in enumerate(sorted(declared_paths), start=1):
            target = (ROOT / raw_path).resolve()
            reachable_resources.add(target)
            check(
                f"reference_fixture_path_{case.get('id', '<missing-id>')}_{index}",
                ROOT in target.parents and target.is_file(),
                f"reference fixture path exists: {raw_path}",
                failures,
                passes,
            )

    check("local_markdown_links_present", link_count > 0, "repository contains checked local Markdown links", failures, passes)
    check("entry_resource_links_present", entry_resource_count > 0, "public Skill entrypoints expose checked resources", failures, passes)
    public_support_files = {
        path.resolve()
        for skill_name in EXPECTED_SKILLS
        for resource_dir in ("references", "examples")
        for path in (SKILLS / skill_name / resource_dir).rglob("*")
        if path.is_file()
        and not path.name.startswith(".")
        and path.suffix != ".pyc"
        and "__pycache__" not in path.parts
    }
    unreachable = sorted(
        path.relative_to(ROOT).as_posix()
        for path in public_support_files - reachable_resources
    )
    check(
        "support_files_reachable",
        not unreachable,
        f"every public reference and example is linked or fixture-addressable: {unreachable}",
        failures,
        passes,
    )


def validate_resource_hygiene(failures: list[str], passes: list[str]) -> None:
    output_dirs = sorted(path.relative_to(ROOT).as_posix() for path in SKILLS.rglob("outputs") if path.is_dir())
    placeholders = sorted(path.relative_to(ROOT).as_posix() for path in SKILLS.rglob(".gitkeep"))
    meaningless_scripts: list[str] = []
    for scripts_dir in sorted(path for path in SKILLS.rglob("scripts") if path.is_dir()):
        files = [
            path
            for path in scripts_dir.rglob("*")
            if path.is_file() and path.name not in {".DS_Store"} and "__pycache__" not in path.parts
        ]
        if not files or all(path.name == "check.py" for path in files):
            meaningless_scripts.append(scripts_dir.relative_to(ROOT).as_posix())

    check("outputs_absent", not output_dirs, f"deprecated outputs directories are absent: {output_dirs}", failures, passes)
    check("gitkeep_absent", not placeholders, f"placeholder .gitkeep files are absent: {placeholders}", failures, passes)
    check("meaningless_scripts_absent", not meaningless_scripts, f"empty or check-only scripts directories are absent: {meaningless_scripts}", failures, passes)


def validate_retired_and_archived_absence(failures: list[str], passes: list[str]) -> None:
    stale_hits = [
        path.relative_to(ROOT).as_posix()
        for path in text_files_for_retired_id_check()
        if RETIRED_TASKDAG_SKILL in path.read_text(encoding="utf-8")
    ]
    check("retired_taskdag_skill_unreferenced", not stale_hits, f"removed standalone TaskDAG skill id is absent: {stale_hits}", failures, passes)
    check("legacy_tree_absent", not (ROOT / "legacy").exists(), "archived catalogs are not present in the default tree", failures, passes)
    check("retired_archive_tree_absent", not (ROOT / ("old" + "_skills")).exists(), "retired catalog directories are absent", failures, passes)


def validate_owning_contracts(failures: list[str], passes: list[str]) -> None:
    for contract_name, (path, terms) in OWNING_CONTRACTS.items():
        exists = path.is_file()
        text = path.read_text(encoding="utf-8") if exists else ""
        missing = [term for term in terms if term not in text]
        check(
            contract_name,
            exists and not missing,
            f"owning document preserves canonical contract terms; missing={missing}",
            failures,
            passes,
        )


def main() -> None:
    passes: list[str] = []
    failures: list[str] = []

    check("skills_directory", SKILLS.is_dir(), "skills directory exists", failures, passes)
    validate_catalog_sets(failures, passes)
    validate_frontmatter(failures, passes)
    validate_local_links(failures, passes)
    validate_resource_hygiene(failures, passes)
    validate_retired_and_archived_absence(failures, passes)
    validate_owning_contracts(failures, passes)

    print("V3 catalog validation")
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
