"""把项目内 Skill 安装为 SkillLibrary 的不可变 revision。"""

from pathlib import Path

from agently.core import SkillLibrary


def install_local_skills(library: SkillLibrary, source_root: Path) -> list[str]:
    revision_refs: list[str] = []
    for skill_file in sorted(source_root.glob("*/SKILL.md")):
        revision = library.install(skill_file.parent, trust="trusted")
        revision_refs.append(revision.revision_ref)
    return revision_refs


__all__ = ["install_local_skills"]
