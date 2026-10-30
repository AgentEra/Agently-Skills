#!/usr/bin/env python3
"""Install/update this checkout's canonical skills and select their UI language.

Uses PyYAML, also required by the repository validators. No network/model calls.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone

import yaml

ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = '.agently-skills-ui.json'
UI_FIELDS = {'display_name', 'short_description', 'default_prompt'}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def catalog(root: Path) -> dict:
    data = json.loads((root / 'locales/skill-ui.json').read_text())
    bundles = json.loads((root / 'bundles/manifest.json').read_text())['bundles']
    names = {s for b in bundles if b['id'] != 'design-compat' for s in b['active_skills']}
    if data.get('version') != 1 or data.get('default_locale') not in data['locales']:
        raise ValueError('Invalid UI catalog version/default locale')
    for locale, entries in data['locales'].items():
        if set(entries) != names:
            raise ValueError(f'{locale}: UI entries must match the canonical catalog')
        for name, fields in entries.items():
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
                raise ValueError('Invalid skill identity')
            if set(fields) != UI_FIELDS or any(not isinstance(v, str) or not v.strip() for v in fields.values()):
                raise ValueError(f'{name}: invalid UI fields')
            if not 25 <= len(fields['short_description']) <= 64:
                raise ValueError(f'{name}: description must contain 25–64 characters')
            if '$' + name not in fields['default_prompt']:
                raise ValueError(f'{name}: default prompt must retain its invocation identity')
    return data


class Quoted(str):
    pass


class Dumper(yaml.SafeDumper):
    pass


Dumper.add_representer(Quoted, lambda dumper, value: dumper.represent_scalar('tag:yaml.org,2002:str', value, style='"'))


def quote_values(value):
    if isinstance(value, str):
        return Quoted(value)
    if isinstance(value, list):
        return [quote_values(v) for v in value]
    if isinstance(value, dict):
        return {k: quote_values(v) for k, v in value.items()}
    return value


def metadata(existing: bytes | None, fields: dict) -> bytes:
    data = yaml.safe_load(existing) if existing else {}
    if data is None:
        data = {}
    if not isinstance(data, dict) or not isinstance(data.get('interface', {}), dict):
        raise ValueError('openai.yaml and interface must be mappings')
    data.setdefault('interface', {}).update(fields)
    return yaml.dump(quote_values(data), Dumper=Dumper, allow_unicode=True, sort_keys=False, width=4096).encode()


def identity(content: bytes) -> str:
    parts = content.decode().split('---', 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError('SKILL.md requires YAML frontmatter')
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict) or not isinstance(data.get('name'), str):
        raise ValueError('SKILL.md requires a name')
    return data['name']


def source_files(root: Path, name: str) -> dict[str, bytes]:
    folder = root / 'skills' / name
    result = {}
    for path in folder.rglob('*'):
        if '__pycache__' in path.parts or path.name == '.DS_Store':
            continue
        if path.is_symlink():
            raise ValueError(f'Source symlink requires explicit handling: {path}')
        if path.is_file():
            result[f'{name}/{path.relative_to(folder).as_posix()}'] = path.read_bytes()
    if identity((folder / 'SKILL.md').read_bytes()) != name:
        raise ValueError(f'{name}: SKILL.md identity mismatch')
    return result


def read_file(dest: Path, relative: str) -> bytes | None:
    path = dest / relative
    # Do not mutate a source worktree through an installed symlink.
    for part in [path, *path.parents]:
        if part == dest.parent:
            break
        if part.is_symlink():
            raise ValueError(f'Installed symlink requires explicit handling: {part}')
    if path.exists() and not path.is_file():
        raise ValueError(f'Expected a regular file: {path}')
    return path.read_bytes() if path.exists() else None


def apply(root: Path, dest: Path, locale: str | None = None, skills: list[str] | None = None,
          ui_only: bool = False, dry_run: bool = False) -> dict:
    data = catalog(root)
    source_root = (root / 'skills').resolve()
    dest = dest.expanduser().absolute()
    if dest.resolve() == source_root or source_root in dest.resolve().parents:
        raise ValueError('Install destination must not be the repository skills directory')
    prior = read_file(dest, STATE_FILE)
    state = json.loads(prior) if prior else {'version': 1, 'files': {}}
    if state.get('version') != 1 or not isinstance(state.get('files'), dict):
        raise ValueError('Invalid saved UI preference/baseline')
    selected_locale = locale or state.get('locale') or data['default_locale']
    if selected_locale not in data['locales']:
        raise ValueError(f'Unsupported locale: {selected_locale}')
    entries = data['locales'][selected_locale]
    selected = sorted(skills if skills is not None else
                      [n for n in entries if not ui_only or (dest / n / 'SKILL.md').exists()])
    if not selected or len(selected) != len(set(selected)) or not set(selected) <= set(entries):
        raise ValueError('Select one or more unique canonical skill names')
    changes, originals, preserved, conflicts = {}, {}, [], []
    baselines = dict(state['files'])
    for name in selected:
        files = source_files(root, name)
        installed_entry = read_file(dest, f'{name}/SKILL.md')
        if ui_only and installed_entry is None:
            raise ValueError(f'{name}: install the skill before configuring its UI')
        if installed_entry is not None:
            if identity(installed_entry) != name:
                raise ValueError(f'{name}: installed identity mismatch')
        if not ui_only:
            for relative, incoming in files.items():
                if relative.endswith('/agents/openai.yaml'):
                    continue
                current = read_file(dest, relative)
                old = baselines.get(relative)
                if current is None or current == incoming or digest(current) == old:
                    replacement = incoming
                elif old is None or digest(incoming) == old:
                    replacement = current
                    preserved.append(relative)
                else:
                    conflicts.append(relative)
                    continue
                if replacement != current:
                    changes[relative], originals[relative] = replacement, current
                baselines[relative] = digest(incoming)
        relative = f'{name}/agents/openai.yaml'
        current = read_file(dest, relative)
        incoming = files.get(relative)
        replacement = metadata(current if current is not None else incoming, entries[name])
        if replacement != current:
            changes[relative], originals[relative] = replacement, current
    if conflicts:
        raise ValueError('Upstream and local files both changed; reconcile before updating: ' + ', '.join(conflicts))
    saved = {'version': 1, 'locale': selected_locale, 'files': baselines}
    replacement = (json.dumps(saved, ensure_ascii=False, indent=2) + '\n').encode()
    if replacement != prior:
        changes[STATE_FILE], originals[STATE_FILE] = replacement, prior
    report = {'locale': selected_locale, 'skills': selected, 'changed_files': sorted(changes),
              'preserved_local_files': preserved, 'dry_run': dry_run, 'backup': None}
    if dry_run or not changes:
        return report
    backup = dest.parent / 'skill-update-backups' / ('ui-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    backup.mkdir(parents=True)
    for relative, previous in originals.items():
        if read_file(dest, relative) != previous:
            raise ValueError(f'File changed during planning: {relative}')
        if previous is not None:
            target = backup / 'files' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(previous)
            target.chmod((dest / relative).stat().st_mode & 0o777)
    (backup / 'manifest.json').write_text(json.dumps({'original_files': {k: v is not None for k, v in originals.items()},
                                                     'locale': selected_locale}, indent=2) + '\n')
    written = []
    try:
        # Preferences are committed after the corresponding UI files.
        for relative in sorted(changes, key=lambda value: value == STATE_FILE):
            target = dest / relative
            if read_file(dest, relative) != originals[relative]:
                raise ValueError(f'File changed before write: {relative}')
            target.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as handle:
                temporary = Path(handle.name)
                handle.write(changes[relative])
            try:
                source = root / 'skills' / relative
                mode = target.stat().st_mode & 0o777 if target.exists() else (source.stat().st_mode & 0o777 if source.is_file() else 0o644)
                temporary.chmod(mode)
                os.replace(temporary, target)
            finally:
                temporary.unlink(missing_ok=True)
            written.append(relative)
        for relative in changes:
            if read_file(dest, relative) != changes[relative]:
                raise ValueError(f'Readback mismatch: {relative}')
    except BaseException:
        for relative in reversed(written):
            target = dest / relative
            previous = originals[relative]
            if previous is None:
                target.unlink(missing_ok=True)
            else:
                target.write_bytes(previous)
        raise
    report['backup'] = str(backup)
    (backup / 'receipt.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return report


def write_defaults(root: Path) -> None:
    data = catalog(root)
    for name, fields in data['locales'][data['default_locale']].items():
        target = root / 'skills' / name / 'agents/openai.yaml'
        existing = target.read_bytes() if target.exists() else None
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(metadata(existing, fields))
    check(root)


def check(root: Path) -> None:
    data = catalog(root)
    for name, fields in data['locales'][data['default_locale']].items():
        current = yaml.safe_load((root / 'skills' / name / 'agents/openai.yaml').read_text())
        if any(current.get('interface', {}).get(k) != v for k, v in fields.items()):
            raise ValueError(f'{name}: default UI metadata differs from the catalog')
    print(f"UI catalog: {len(data['locales'])} locales, {len(data['locales'][data['default_locale']])} canonical skills")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path, default=Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills')
    parser.add_argument('--locale', help='en or zh-CN; omitted: saved preference, then English')
    parser.add_argument('--skills', nargs='+', help='Canonical skill IDs; default: all (UI-only: existing)')
    parser.add_argument('--ui-only', action='store_true', help='Only configure existing skill UI and save language')
    parser.add_argument('--dry-run', action='store_true')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--check', action='store_true', help='Validate dictionary and shipped English metadata; no writes')
    modes.add_argument('--write-defaults', action='store_true', help='Maintainer: regenerate this checkout’s default UI metadata')
    args = parser.parse_args()
    try:
        if args.check:
            check(ROOT)
        elif args.write_defaults:
            write_defaults(ROOT)
        else:
            print(json.dumps(apply(ROOT, args.dest, args.locale, args.skills, args.ui_only, args.dry_run), ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, yaml.YAMLError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
