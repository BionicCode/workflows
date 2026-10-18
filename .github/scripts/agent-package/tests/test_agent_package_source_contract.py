"""Source and declaration contracts; native-client acceptance is separate."""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPOSITORY = Path(__file__).resolve().parents[4]
PREFIX = 'deployment/packages/agent-package/'
SOURCE = REPOSITORY / PREFIX
ENGINE = REPOSITORY / '.github/scripts/sync-files-from-manifest'
MODULES = ('ENGINEERING', 'IMPLEMENTATION', 'CODE_REVIEW', 'DOTNET', 'TESTING', 'GUARDRAILS', 'DOCUMENTATION')
EXCLUSIONS = ('**/deployment/packages/agent-package/AGENTS.md', '**/deployment/packages/agent-package/bridges/claude/CLAUDE.md')
sys.path.insert(0, str(ENGINE))
import common  # noqa: E402
import source_glob  # noqa: E402
import sync_files  # noqa: E402


def registration():
    return json.loads((SOURCE / 'configuration/sync-manifest-template.json').read_text(encoding='utf-8'))


def required_command(name):
    command = os.environ.get('AGENT_PACKAGE_PWSH') if name == 'pwsh' else None
    command = command or shutil.which(name)
    if not command or not Path(command).is_file():
        raise RuntimeError(f'Required dependency unavailable: {name}')
    return command


def powershell_recipe(name):
    text = (REPOSITORY / '.github/tools/agent-package/README.md').read_text(encoding='utf-8')
    match = re.search(r'<!-- acceptance:' + re.escape(name) + r':start -->\s*```powershell\n(.*?)\n```', text, re.S)
    if not match:
        raise AssertionError(f'Missing exercised maintenance recipe: {name}')
    return match.group(1)


def run_powershell(root, script):
    wrapper = root / 'acceptance-recipe.ps1'
    wrapper.write_text("$ErrorActionPreference = 'Stop'\n" + script + '\n', encoding='utf-8')
    return subprocess.run([required_command('pwsh'), '-NoProfile', '-NonInteractive', '-File', str(wrapper)],
                          cwd=root, capture_output=True, text=True, encoding='utf-8', timeout=90)


def assert_empty_seed(content):
    text = content.decode('utf-8')
    lines = text.splitlines()
    log_positions = [index for index, line in enumerate(lines) if line == '## Log']
    if len(log_positions) != 1 or any(line.strip() for line in lines[log_positions[0] + 1:]):
        raise AssertionError('Source REVIEW must contain one empty Log.')
    if re.search(r'^\s*- \[[ xX]\]', text, re.M):
        raise AssertionError('Source REVIEW must not contain operational findings.')


def assert_claude_import(content):
    lines = content.decode('utf-8').splitlines()
    if not lines or lines[0] != '@AGENTS.md':
        raise AssertionError('Claude bridge must begin with the real @AGENTS.md import.')


def router_rows(text):
    rows = {}
    for line in text.splitlines():
        columns = [column.strip().strip('`') for column in line.strip('|').split('|')]
        if line.startswith('| ') and columns[0] in MODULES:
            if columns[0] in rows or len(columns) != 4:
                raise AssertionError('Router pairs must be unique and explicit.')
            rows[columns[0]] = tuple(columns[1:])
    if tuple(rows) != MODULES:
        raise AssertionError('Seven complete routes must appear in the prescribed order.')
    return rows


def read_selected(root, names, target=None):
    """Artifact-resolution fixture, not a simulation of native/model compliance."""
    rows = router_rows((root / 'AGENTS.md').read_text(encoding='utf-8'))
    result = []
    for name in MODULES:
        if name not in names:
            continue
        _, required, optional = rows[name]
        path = root / required
        if not path.is_file():
            raise FileNotFoundError('Missing selected package module: ' + required)
        result.append(path)
        if (root / optional).is_file():
            result.append(root / optional)
    if target is not None:
        directory = (root / target).parent
        for ancestor in reversed((directory, *directory.parents)):
            if ancestor == root or not ancestor.is_relative_to(root):
                continue
            override = ancestor / 'AGENTS.override.md'
            native = override if override.is_file() else ancestor / 'AGENTS.md'
            if native.is_file():
                result.append(native)
    return result


def local_source_files():
    return {PREFIX + path.relative_to(SOURCE).as_posix(): path.read_bytes()
            for path in SOURCE.rglob('*') if path.is_file()}


def normalized(root, manifest):
    return common.validate_and_normalize_manifest(json.dumps(manifest), root,
                                                  common.default_schema_path(), common.default_rules_path())


def execute_sync(root, manifest=None, files=None, verify=False):
    manifest = registration() if manifest is None else manifest
    files = local_source_files() if files is None else files
    entries = normalized(root, manifest)
    manifest_path = root / 'normalized-acceptance-manifest.json'
    common.write_normalized_manifest(entries, manifest_path)
    with mock.patch.object(sync_files, 'list_source_tree_files', return_value=list(files)), \
         mock.patch.object(sync_files, 'fetch_source_bytes', side_effect=lambda entry, _: files[entry.source_path]), \
         contextlib.redirect_stdout(io.StringIO()):
        operation = sync_files.verify_entries if verify else sync_files.sync_entries
        operation(root, manifest_path, None)


class SourceContractTests(unittest.TestCase):
    def test_exact_inventory_separates_publisher_and_payload(self):
        expected = {'AGENTS.md', 'AGENTS.override.md', 'README.md', 'REVIEW.md',
                    'instruction-package/instructions/README.md',
                    'instruction-package/instructions/package/docs/ARCHITECTURE.md',
                    'bridges/claude/CLAUDE.md', 'bridges/copilot/copilot-instructions.md',
                    'bridges/copilot/instructions/dotnet.instructions.md',
                    'bridges/copilot/instructions/test.instructions.md', 'configuration/sync-manifest-template.json'}
        expected.update('instruction-package/instructions/package/' + name + '.md' for name in MODULES)
        self.assertEqual(expected, {path.relative_to(SOURCE).as_posix() for path in SOURCE.rglob('*') if path.is_file()})

    def test_shared_policy_has_no_custom_or_mixed_ownership_fences(self):
        self.assertFalse((SOURCE / 'instruction-package/instructions/custom').exists())
        self.assertFalse((SOURCE / 'instruction-package/REPOSITORY.md').exists())
        for name in MODULES:
            with self.subTest(module=name):
                content = (SOURCE / 'instruction-package/instructions/package' / (name + '.md')).read_text(encoding='utf-8')
                self.assertNotIn('BEGIN REPOSITORY SPECIFICS', content)
                self.assertNotIn('.agent/REPOSITORY.md', content)

    def test_registration_is_valid_against_existing_schema_and_semantics(self):
        with tempfile.TemporaryDirectory() as temporary:
            self.assertEqual(8, len(normalized(Path(temporary), registration())))

    def test_exact_projection_and_router_last(self):
        entries = registration()['entries']
        selectors = [(entry.get('source_path', entry.get('source_glob')), entry['target_directory'], entry['lifecycle_policy']) for entry in entries]
        self.assertEqual([
            (PREFIX + 'README.md', '.agent/', 'enforce'),
            (PREFIX + 'instruction-package/**/*', '.agent/', 'enforce'),
            (PREFIX + 'REVIEW.md', '.agent/', 'seed_once'),
            (PREFIX + 'bridges/claude/CLAUDE.md', '', 'seed_once'),
            (PREFIX + 'bridges/copilot/copilot-instructions.md', '.github/', 'enforce'),
            (PREFIX + 'bridges/copilot/instructions/dotnet.instructions.md', '.github/instructions/', 'enforce'),
            (PREFIX + 'bridges/copilot/instructions/test.instructions.md', '.github/instructions/', 'enforce'),
            (PREFIX + 'AGENTS.md', '', 'enforce')], selectors)
        self.assertEqual({'recursive': True, 'include_hidden': True}, entries[1]['glob'])

    def test_all_declarations_keep_approved_engine_contract(self):
        for entry in registration()['entries']:
            with self.subTest(entry=entry):
                self.assertEqual(('BionicCode/workflows', 'main', 'source_to_target', 'whole_file', 'none'),
                                 tuple(entry[key] for key in ('source_repo', 'source_ref', 'direction', 'managed_scope', 'uniqueness_policy')))

    def test_projection_never_includes_publisher_only_or_custom_content(self):
        with tempfile.TemporaryDirectory() as temporary:
            entries = normalized(Path(temporary), registration())
            with mock.patch.object(sync_files, 'list_source_tree_files', return_value=list(local_source_files())):
                expanded = sync_files.expand_entries_for_execution(entries, Path(temporary), None)
            targets = {entry.target_path for entry in expanded}
            self.assertEqual(16, len(targets))
            self.assertFalse(any('override' in target or 'custom/' in target or 'settings.json' in target or 'configuration/' in target for target in targets))

    def test_explicit_pairs_are_root_relative_and_ordered(self):
        rows = router_rows((SOURCE / 'AGENTS.md').read_text(encoding='utf-8'))
        for name, (_, required, optional) in rows.items():
            with self.subTest(module=name):
                self.assertEqual(('.agent/instructions/package/' + name + '.md', '.agent/instructions/custom/' + name + '.md'), (required, optional))

    def test_every_accepted_activation_trigger_is_retained(self):
        # Golden trigger categories are the approved external routing contract.
        triggers = {
            'ENGINEERING': ('every task',),
            'IMPLEMENTATION': ('planning', 'preparing', 'reviewing', 'performing', 'requested implementation/file changes', 'without immediate file edits'),
            'CODE_REVIEW': ('requested formal reviews', '<review>'),
            'DOTNET': ('.NET', 'C#', 'Visual Studio', 'independent of path'),
            'TESTING': ('planning', 'designing', 'creating', 'modifying', 'reviewing', 'diagnosing', 'executing', 'tests', 'test-validation'),
            'GUARDRAILS': ('infrastructure', 'instruction maintenance', 'configuration', 'security', 'compatibility', 'migrations', 'authorization', 'protected paths', 'Git/GitHub', 'automation', 'consequential', 'read-only analysis', 'planning'),
            'DOCUMENTATION': ('documentation', 'instructions', 'comments', 'examples', 'metadata'),
        }
        rows = router_rows((SOURCE / 'AGENTS.md').read_text(encoding='utf-8'))
        for name, categories in triggers.items():
            for category in categories:
                with self.subTest(module=name, category=category):
                    self.assertIn(category, rows[name][0])

    def test_trigger_omission_is_a_failure_witness(self):
        text = (SOURCE / 'AGENTS.md').read_text(encoding='utf-8')
        for name, trigger in (('IMPLEMENTATION', 'planning'), ('TESTING', 'diagnosing'), ('GUARDRAILS', 'read-only analysis')):
            with self.subTest(module=name):
                rows = router_rows(text)
                self.assertNotIn(trigger, rows[name][0].replace(trigger, ''))
                self.assertIn(trigger, rows[name][0])

    def test_normative_review_policy_is_not_in_mutable_seed(self):
        assert_empty_seed((SOURCE / 'REVIEW.md').read_bytes())
        policy = (SOURCE / 'instruction-package/instructions/package/CODE_REVIEW.md').read_text(encoding='utf-8')
        self.assertIn('determine the next identifier before removing checked entries', policy)
        self.assertIn('Never renumber existing findings to close gaps', policy)
        self.assertIn('user\'s checkbox state is authoritative', policy)
        self.assertNotIn('allocation rules defined in `REVIEW.md`', policy)
        self.assertNotIn('maintenance rules defined in `REVIEW.md`', policy)

    def test_contaminated_source_seed_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'empty Log'):
            assert_empty_seed((SOURCE / 'REVIEW.md').read_bytes() + b'\n- [ ] R01 [BUG] Publisher finding\n')

    def test_testing_is_language_independent_and_dotnet_preserves_rules(self):
        testing = (SOURCE / 'instruction-package/instructions/package/TESTING.md').read_text(encoding='utf-8')
        dotnet = (SOURCE / 'instruction-package/instructions/package/DOTNET.md').read_text(encoding='utf-8')
        for phrase in ('`Task`', '`Task<T>`', '`async void`', '`<SolutionName>.Tests`'):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, testing)
                self.assertIn(phrase, dotnet)

    def test_copilot_frontmatter_covers_tool_tests_without_duplicate_rules(self):
        content = (SOURCE / 'bridges/copilot/instructions/test.instructions.md').read_text(encoding='utf-8')
        yaml = content.split('---', 2)[1]
        self.assertIn('.github/scripts/**/tests/**/*', yaml)
        self.assertIn('test/**/*', yaml)
        self.assertNotIn('BEGIN REPOSITORY SPECIFICS', content)

    def test_claude_bridge_retains_real_import(self):
        assert_claude_import((SOURCE / 'bridges/claude/CLAUDE.md').read_bytes())

    def test_publisher_settings_include_both_narrow_exclusions(self):
        settings = json.loads((REPOSITORY / '.claude/settings.json').read_text(encoding='utf-8-sig'))
        self.assertTrue(set(EXCLUSIONS).issubset(settings['claudeMdExcludes']))

    def test_claude_patterns_match_only_source_payload_paths(self):
        options = common.GlobOptions(recursive=True, include_hidden=True)
        positives = ('C:/publisher/' + PREFIX + 'AGENTS.md', '/repo/' + PREFIX + 'bridges/claude/CLAUDE.md')
        negatives = ('C:/publisher/AGENTS.md', '/repo/CLAUDE.md', '/repo/CLAUDE.local.md',
                     '/repo/.agent/instructions/custom/GUARDRAILS.md', '/repo/tools/AGENTS.md',
                     '/repo/' + PREFIX + 'AGENTS.override.md')
        for path in positives:
            with self.subTest(path=path): self.assertTrue(any(source_glob.path_matches_glob(pattern, path, options) for pattern in EXCLUSIONS))
        for path in negatives:
            with self.subTest(path=path): self.assertFalse(any(source_glob.path_matches_glob(pattern, path, options) for pattern in EXCLUSIONS))

    def test_documented_settings_merge_preserves_unrelated_keys_and_exclusions(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / '.claude').mkdir()
            settings = {'permissions': {'allow': ['Read']}, 'customSetting': {'enabled': True}, 'claudeMdExcludes': ['**/other/CLAUDE.md', EXCLUSIONS[0]]}
            path = root / '.claude/settings.json'
            path.write_text(json.dumps(settings), encoding='utf-8')
            script = "$repositoryRoot = (Get-Location).Path\n" + powershell_recipe('claude-settings-merge')
            for attempt in range(2):
                with self.subTest(attempt=attempt):
                    result = run_powershell(root, script)
                    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            updated = json.loads(path.read_text(encoding='utf-8-sig'))
            self.assertEqual(settings['permissions'], updated['permissions'])
            self.assertEqual(settings['customSetting'], updated['customSetting'])
            self.assertEqual(['**/other/CLAUDE.md', *EXCLUSIONS], updated['claudeMdExcludes'])

    def test_invalid_existing_exclusions_fail_without_replacement(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); (root / '.claude').mkdir()
            path = root / '.claude/settings.json'
            original = b'{"claudeMdExcludes":"retain malformed value"}\n'
            path.write_bytes(original)
            result = run_powershell(root, "$repositoryRoot = (Get-Location).Path\n" + powershell_recipe('claude-settings-merge'))
            self.assertNotEqual(0, result.returncode)
            self.assertEqual(original, path.read_bytes())

    def test_metadata_manifest_keeps_source_and_custom_ownership_separate(self):
        manifest = json.loads((REPOSITORY / '.github/tools/doc-metadata/doc-metadata-manifest.json').read_text(encoding='utf-8'))
        self.assertIn(PREFIX + '**/*.md', manifest['include'])
        self.assertIn('.agent/instructions/custom/**/*.md', manifest['include'])
        for path in (PREFIX + 'REVIEW.md', PREFIX + 'bridges/claude/CLAUDE.md', '.agent/REVIEW.md',
                     'CLAUDE.md', 'AGENTS.md', '.agent/README.md', '.agent/instructions/README.md',
                     '.agent/instructions/package/**/*.md', '.github/copilot-instructions.md',
                     '.github/instructions/dotnet.instructions.md', '.github/instructions/test.instructions.md'):
            with self.subTest(path=path): self.assertIn(path, manifest['exclude'])

    def test_claude_deferral_retains_failures_and_all_future_cases(self):
        text = (REPOSITORY / '.github/tools/agent-package/README.md').read_text(encoding='utf-8')
        for phrase in ('unsupported/unverified', 'source router loaded', 'source bridge loaded', 'root guidance missing',
                       'root-started', 'claude-md-or-agents-md', 'claude-md-and-agents-md', 'unrelated project instructions',
                       'custom companions', 'CLAUDE.local', 'compatibility restriction', 'duration_api_ms=0', 'pending'):
            with self.subTest(phrase=phrase): self.assertIn(phrase, text)


class DocumentSemanticWitnessTests(unittest.TestCase):
    def test_empty_review_log_accepts_lf_and_crlf(self):
        for content in (b'# Review\n\n## Log\n', b'# Review\r\n\r\n## Log\r\n', b'# Review\n\n## Log'):
            with self.subTest(content=content):
                assert_empty_seed(content)

    def test_review_seed_rejects_missing_or_malformed_log(self):
        for content in (b'# Review\n', b'### Log\n', b'## Log: \n', b'##Log\r\n'):
            with self.subTest(content=content), self.assertRaisesRegex(AssertionError, 'one empty Log'):
                assert_empty_seed(content)

    def test_review_seed_rejects_duplicate_log_sections(self):
        with self.assertRaisesRegex(AssertionError, 'one empty Log'):
            assert_empty_seed(b'# Review\r\n\r\n## Log\r\n\r\n## Log\r\n')

    def test_review_seed_rejects_nonempty_log(self):
        for content in (b'## Log\n- [ ] R01 [BUG] Finding\n', b'## Log\r\nUnexpected content\r\n'):
            with self.subTest(content=content), self.assertRaisesRegex(AssertionError, 'one empty Log'):
                assert_empty_seed(content)

    def test_review_seed_rejects_findings_outside_log(self):
        with self.assertRaisesRegex(AssertionError, 'operational findings'):
            assert_empty_seed(b'# Review\r\n- [x] R01 [BUG] Finding\r\n\r\n## Log\r\n')

    def test_claude_import_accepts_lf_and_crlf(self):
        for content in (b'@AGENTS.md\n\nRouting\n', b'@AGENTS.md\r\n\r\nRouting\r\n', b'@AGENTS.md'):
            with self.subTest(content=content):
                assert_claude_import(content)

    def test_claude_import_rejects_missing_or_incorrect_first_line(self):
        for content in (b'', b'@OTHER.md\n', b'`@AGENTS.md`\r\n', b'# Bridge\n@AGENTS.md\n'):
            with self.subTest(content=content), self.assertRaisesRegex(AssertionError, 'real @AGENTS.md import'):
                assert_claude_import(content)


if __name__ == '__main__':
    unittest.main()
