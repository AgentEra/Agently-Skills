from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('skill_ui_installer', ROOT / 'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class SkillUIInstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.root, self.dest = base / 'source', base / 'installed'
        for folder in ['skills', 'locales', 'bundles']:
            shutil.copytree(ROOT / folder, self.root / folder)
        self.catalog = installer.catalog(self.root)

    def ui(self, name='agently-product-design'):
        return yaml.safe_load((self.dest / name / 'agents/openai.yaml').read_text())

    def snapshot(self):
        return {str(p.relative_to(self.dest)): p.read_bytes() for p in self.dest.rglob('*') if p.is_file()}

    def test_default_install_and_identities(self):
        result = installer.apply(self.root, self.dest)
        self.assertEqual(result['locale'], 'en')
        self.assertEqual(len(result['skills']), 8)
        self.assertFalse((self.dest / 'agently-design').exists())
        for name in result['skills']:
            self.assertEqual((self.dest / name / 'SKILL.md').read_bytes(), (self.root / 'skills' / name / 'SKILL.md').read_bytes())
            self.assertEqual(self.ui(name)['interface'], self.catalog['locales']['en'][name])
        self.assertEqual(installer.apply(self.root, self.dest)['changed_files'], [])

    def test_new_executable_asset_keeps_source_permissions(self):
        source = self.root / 'skills/agently/scripts/helper.sh'
        source.parent.mkdir(exist_ok=True)
        source.write_text('#!/bin/sh\nexit 0\n')
        source.chmod(0o755)
        installer.apply(self.root, self.dest)
        target = self.dest / 'agently/scripts/helper.sh'
        self.assertEqual(target.read_bytes(), source.read_bytes())
        self.assertEqual(target.stat().st_mode & 0o777, 0o755)

    def test_language_survives_dictionary_and_content_update(self):
        installer.apply(self.root, self.dest, 'zh-CN')
        source = self.root / 'skills/agently/SKILL.md'
        source.write_text(source.read_text() + '\nUpdated upstream instruction.\n')
        path = self.root / 'locales/skill-ui.json'
        data = json.loads(path.read_text())
        data['locales']['zh-CN']['agently']['display_name'] = 'Agently 任务与协作'
        path.write_text(json.dumps(data, ensure_ascii=False))
        result = installer.apply(self.root, self.dest)
        self.assertEqual(result['locale'], 'zh-CN')
        self.assertEqual(self.ui('agently')['interface']['display_name'], 'Agently 任务与协作')
        self.assertEqual((self.dest / 'agently/SKILL.md').read_bytes(), source.read_bytes())
        self.assertEqual(installer.apply(self.root, self.dest, 'en', ui_only=True)['locale'], 'en')
        self.assertEqual(self.ui()['interface'], data['locales']['en']['agently-product-design'])

    def test_policy_dependencies_and_other_interface_fields_preserved(self):
        installer.apply(self.root, self.dest)
        p = self.dest / 'agently-product-design/agents/openai.yaml'
        data = self.ui()
        data.update(policy={'allow_implicit_invocation': False}, dependencies={'tools': [{'type': 'env_var', 'value': 'SOME_KEY'}]})
        data['interface'].update(icon_small='./assets/custom.svg', brand_color='#123456')
        p.write_text(yaml.safe_dump(data))
        installer.apply(self.root, self.dest, 'zh-CN')
        after = self.ui()
        self.assertEqual(after['policy'], data['policy'])
        self.assertEqual(after['dependencies'], data['dependencies'])
        for k in ['icon_small', 'brand_color']:
            self.assertEqual(after['interface'][k], data['interface'][k])

    def test_first_adoption_keeps_local_supplements(self):
        installer.apply(self.root, self.dest)
        (self.dest / installer.STATE_FILE).unlink()
        p = self.dest / 'agently-request/references/model-capabilities.md'
        p.write_text(p.read_text() + '\nLocal preview with capability checks.\n')
        before = p.read_bytes()
        result = installer.apply(self.root, self.dest, 'zh-CN')
        self.assertIn('agently-request/references/model-capabilities.md', result['preserved_local_files'])
        self.assertEqual(p.read_bytes(), before)

    def test_conflicting_upstream_and_local_changes_abort_before_writes(self):
        installer.apply(self.root, self.dest)
        rel = 'agently-request/references/model-capabilities.md'
        p = self.dest / rel
        p.write_text(p.read_text() + '\nLocal development.\n')
        installer.apply(self.root, self.dest)
        source = self.root / 'skills' / rel
        source.write_text(source.read_text() + '\nNew upstream behavior.\n')
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'both changed'):
            installer.apply(self.root, self.dest, 'zh-CN')
        self.assertEqual(self.snapshot(), before)

    def test_ui_only_does_not_add_skills_or_touch_content(self):
        installer.apply(self.root, self.dest, skills=['agently-product-design'])
        other = self.dest / 'spotkit/SKILL.md'
        other.parent.mkdir()
        other.write_text('Custom standalone skill')
        body = (self.dest / 'agently-product-design/SKILL.md').read_bytes()
        result = installer.apply(self.root, self.dest, 'zh-CN', ui_only=True)
        self.assertEqual(result['skills'], ['agently-product-design'])
        self.assertEqual((self.dest / 'agently-product-design/SKILL.md').read_bytes(), body)
        self.assertEqual(other.read_text(), 'Custom standalone skill')
        self.assertFalse((self.dest / 'agently').exists())

    def test_invalid_locale_and_dry_run_make_no_changes(self):
        with self.assertRaisesRegex(ValueError, 'Unsupported locale'):
            installer.apply(self.root, self.dest, 'fr')
        self.assertFalse(self.dest.exists())
        result = installer.apply(self.root, self.dest, 'zh-CN', dry_run=True)
        self.assertTrue(result['dry_run'])
        self.assertFalse(self.dest.exists())

    def test_symlink_does_not_modify_the_source(self):
        self.dest.mkdir()
        original = self.root / 'skills/agently/SKILL.md'
        before = original.read_bytes()
        (self.dest / 'agently').symlink_to(self.root / 'skills/agently', target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            installer.apply(self.root, self.dest, 'zh-CN')
        self.assertEqual(original.read_bytes(), before)
        self.assertFalse((self.dest / installer.STATE_FILE).exists())

    def test_partial_write_failure_rolls_back_metadata_and_preference(self):
        installer.apply(self.root, self.dest)
        before = self.snapshot()
        original = installer.os.replace
        calls = []
        def fail_once(src, dst):
            calls.append(dst)
            if len(calls) == 3:
                raise OSError('simulated disk error')
            return original(src, dst)
        with mock.patch.object(installer.os, 'replace', side_effect=fail_once):
            with self.assertRaisesRegex(OSError, 'disk error'):
                installer.apply(self.root, self.dest, 'zh-CN')
        self.assertEqual(self.snapshot(), before)


if __name__ == '__main__':
    unittest.main()
