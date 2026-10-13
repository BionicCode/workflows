"""Read-only installation checks and real sync/metadata disposable witnesses."""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_agent_package_source_contract import (
    ENGINE, EXCLUSIONS, MODULES, PREFIX, REPOSITORY, SOURCE, common,
    execute_sync, local_source_files, normalized, powershell_recipe,
    read_selected, registration, required_command, run_powershell, source_glob, sync_files,
)


def expanded_projection():
    with tempfile.TemporaryDirectory() as temporary:
        entries = normalized(Path(temporary), registration())
        with mock.patch.object(sync_files, 'list_source_tree_files', return_value=list(local_source_files())):
            return sync_files.expand_entries_for_execution(entries, Path(temporary), None)


def assert_enforced_parity(root):
    for entry in expanded_projection():
        if entry.lifecycle_policy == 'enforce':
            if (root / entry.target_path).read_bytes() != (REPOSITORY / entry.source_path).read_bytes():
                raise AssertionError('Installed drift: ' + entry.target_path)


def git(root, *arguments):
    return subprocess.check_output([required_command('git'), '--no-optional-locks', '-C', str(root), *arguments])


def strip_managed_metadata(content):
    """Create new untracked documents without losing non-managed YAML fields."""
    text = content.decode('utf-8').replace('\r\n', '\n')
    text = re.sub(r'<!-- doc-metadata-presentation:start -->.*?<!-- doc-metadata-presentation:end -->\s*', '', text, flags=re.S)
    if text.startswith('---\n'):
        yaml, rest = text[4:].split('\n---\n', 1)
        fields = [line for line in yaml.splitlines() if not re.match(r'^(Version|Created|Updated|Author):', line)]
        text = ('---\n' + '\n'.join(fields) + '\n---\n' if fields else '') + rest.lstrip('\n')
    return text.encode('utf-8')


def metadata_fixture(root):
    git(root, 'init', '--quiet')
    (root / 'README.md').write_bytes(b'Unrelated baseline README\n')
    git(root, 'add', '--', 'README.md')
    git(root, '-c', 'user.name=Acceptance fixture', '-c', 'user.email=fixture@example.invalid',
        'commit', '--quiet', '-m', 'Fixture baseline')
    (root / 'README.md').write_bytes(b'Unrelated staged README\r\n')
    git(root, 'add', '--', 'README.md')
    for relative, content in local_source_files().items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        fresh = strip_managed_metadata(content)
        if relative.endswith('.instructions.md'):
            timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
            fields = f'Version: 1\nCreated: {timestamp}\nUpdated: {timestamp}\nAuthor: Acceptance fixture\n'
            fresh = fresh.replace(b'---\n', b'---\n' + fields.encode('utf-8'), 1)
        path.write_bytes(fresh)
    for relative in ('.github/tools/agent-package/README.md', '.github/tools/agent-package/MIGRATION.md'):
        path = root / relative; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(strip_managed_metadata((REPOSITORY / relative).read_bytes()))
    for relative in ('.github/scripts/doc-metadata/update-doc-metadata.ps1',
                     '.github/tools/doc-metadata/doc-metadata-manifest.json',
                     '.github/tools/doc-metadata/doc-metadata-manifest.schema.json'):
        path = root / relative; path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPOSITORY / relative, path)
    copilot = root / PREFIX / 'bridges/copilot/instructions/test.instructions.md'
    copilot.write_bytes(copilot.read_bytes().replace(b'---\n', b'---\ncustomField: preserved\n', 1))
    installed = root / '.agent/instructions/package/ENGINEERING.md'
    installed.parent.mkdir(parents=True, exist_ok=True)
    installed.write_bytes(b'Installed copy must not be independently metadata-mutated\r\n')
    return installed, copilot


class InstalledContractTests(unittest.TestCase):
    def test_all_enforced_installed_bytes_match_finalized_sources(self):
        assert_enforced_parity(REPOSITORY)

    def test_initial_claude_copy_and_real_import(self):
        self.assertTrue((REPOSITORY / 'CLAUDE.md').read_bytes().startswith(b'@AGENTS.md\n'))

    def test_only_meaningful_workflows_custom_companions_exist(self):
        directory = REPOSITORY / '.agent/instructions/custom'
        actual = {path.name for path in directory.iterdir() if path.is_file()}
        self.assertTrue({'ENGINEERING.md', 'IMPLEMENTATION.md', 'TESTING.md', 'GUARDRAILS.md', 'DOCUMENTATION.md'}.issubset(actual))
        self.assertTrue(actual.issubset({name + '.md' for name in MODULES}))
        for path in directory.glob('*.md'):
            with self.subTest(path=path): self.assertNotIn('<fill me>', path.read_text(encoding='utf-8'))

    def test_workflows_authority_and_passive_constraints_preserved(self):
        guard = (REPOSITORY / '.agent/instructions/custom/GUARDRAILS.md').read_text(encoding='utf-8')
        implementation = (REPOSITORY / '.agent/instructions/custom/IMPLEMENTATION.md').read_text(encoding='utf-8')
        for phrase in ('Current user authorization is the only source of write authority',
                       'Do not begin W2', 'user-prompts/', 'inert user-invoked templates',
                       'Phase 3 migration', 'maintainer explicitly green-lights', 'Do not activate, initialize, populate, checksum',
                       'Only the maintainer may mark backlog passes complete'):
            with self.subTest(phrase=phrase): self.assertIn(phrase, guard)
        self.assertIn('self-contained review handoff', implementation)
        self.assertIn('current task explicitly authorizes its path', implementation)

    def test_claude_local_is_byte_preserved_from_recorded_baseline(self):
        migration = (REPOSITORY / '.github/tools/agent-package/MIGRATION.md').read_text(encoding='utf-8')
        match = re.search(r'\| `CLAUDE.local.md` \| `([0-9a-f]{64})`', migration)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), hashlib.sha256((REPOSITORY / 'CLAUDE.local.md').read_bytes()).hexdigest())

    def test_legacy_framework_retired_after_traceable_preservation(self):
        for path in ('AGENT_GUARDRAILS.md', 'DOCUMENTATION.md', 'test/AGENTS.md', 'src/AGENTS.md', '.agent/REPOSITORY.md'):
            with self.subTest(path=path): self.assertFalse((REPOSITORY / path).exists())
        migration = (REPOSITORY / '.github/tools/agent-package/MIGRATION.md').read_text(encoding='utf-8')
        self.assertIn('d820fda78405c924e6fa969221697d08fb59f427', migration)
        self.assertGreater(len(re.findall(r'^\| G\d{3} \|', migration, re.M)), 60)
        for phrase in ('Implementation-pass review handoff', 'Protected repository control plane',
                       'Async and Time-Sensitive Tests', 'CLAUDE.local.md', 'Git blob SHA256'):
            with self.subTest(phrase=phrase): self.assertIn(phrase, migration)

    def test_installed_markdown_links_resolve_in_consumer_namespace(self):
        for entry in expanded_projection():
            path = REPOSITORY / entry.target_path
            text = re.sub(r'```.*?```', '', path.read_text(encoding='utf-8'), flags=re.S)
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                if re.match(r'^[a-z]+:', target) or target.startswith('#'): continue
                target = target.split('#', 1)[0].strip('<>')
                with self.subTest(file=entry.target_path, link=target):
                    self.assertTrue((path.parent / target).exists(), str(path.parent / target))

    def test_control_plane_current_references_use_new_surfaces(self):
        backlog = (REPOSITORY / 'repository-maintenance-orchestrator-recovery-backlog.md').read_text(encoding='utf-8')
        protocol = (REPOSITORY / 'repository-review-protocol.md').read_text(encoding='utf-8')
        self.assertNotIn('[AGENT_GUARDRAILS.md](AGENT_GUARDRAILS.md)', backlog)
        self.assertNotIn('[DOCUMENTATION.md](DOCUMENTATION.md)', backlog)
        self.assertIn('| `AGENT_GUARDRAILS.md` | Repository-specific overlay only. |', backlog)  # Historical allowlist is untouched.
        for text in (backlog, protocol):
            self.assertIn('deployment/packages/agent-package/**', text)
            self.assertIn('.claude/settings.json', text)
            self.assertIn('.agent/instructions/', text)


class SynchronizationWitnessTests(unittest.TestCase):
    def test_fresh_consumer_gets_all_dependencies_and_verifies(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            execute_sync(root)
            execute_sync(root, verify=True)
            self.assertEqual((SOURCE / 'bridges/claude/CLAUDE.md').read_bytes(), (root / 'CLAUDE.md').read_bytes())
            self.assertTrue(all((root / '.agent/instructions/package' / (name + '.md')).is_file() for name in MODULES))

    def test_drift_is_detected_by_existing_engine(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); execute_sync(root)
            (root / '.agent/instructions/package/ENGINEERING.md').write_bytes(b'Drift\n')
            with self.assertRaisesRegex(common.ManifestError, 'out of sync'):
                execute_sync(root, verify=True)

    def test_populated_review_and_custom_claude_survive_seed_once(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); (root / '.agent').mkdir()
            review = b'# Local backlog\r\n\r\n## Log\r\n- [ ] R07 [BUG] Existing finding\r\n'
            claude = b'@AGENTS.md\nLocal customized bridge\n'
            (root / '.agent/REVIEW.md').write_bytes(review); (root / 'CLAUDE.md').write_bytes(claude)
            execute_sync(root); execute_sync(root, verify=True)
            self.assertEqual(review, (root / '.agent/REVIEW.md').read_bytes())
            self.assertEqual(claude, (root / 'CLAUDE.md').read_bytes())

    def test_local_companions_and_client_context_survive_materialization(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); custom = root / '.agent/instructions/custom/ENGINEERING.md'
            custom.parent.mkdir(parents=True); custom.write_bytes('Local policy — Grüß dich\r\n'.encode('utf-8'))
            context = root / 'CLAUDE.local.md'; context.write_bytes(b'@context/index.md\n')
            before = {path: path.read_bytes() for path in (custom, context)}
            execute_sync(root); execute_sync(root)
            self.assertEqual(before, {path: path.read_bytes() for path in before})

    def test_recursive_addition_preserves_unicode_newlines_and_does_not_prune(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); files = local_source_files()
            extra = PREFIX + 'instruction-package/instructions/package/docs/.新規.md'
            payload = 'Unicode — Grüße\r\nSecond line\n'.encode('utf-8'); files[extra] = payload
            execute_sync(root, files=files)
            installed = root / '.agent/instructions/package/docs/.新規.md'
            self.assertEqual(payload, installed.read_bytes())
            del files[extra]; execute_sync(root, files=files)
            self.assertEqual(payload, installed.read_bytes())

    def test_optional_bridge_groups_can_be_omitted_without_losing_core(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); manifest = registration()
            manifest['entries'] = [entry for entry in manifest['entries'] if '/bridges/' not in entry.get('source_path', '')]
            execute_sync(root, manifest=manifest)
            self.assertTrue((root / 'AGENTS.md').is_file())
            self.assertFalse((root / 'CLAUDE.md').exists())
            self.assertFalse((root / '.github/copilot-instructions.md').exists())

    def test_opt_out_keeps_local_installed_content(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); execute_sync(root)
            manifest = registration(); manifest['entries'][-1]['lifecycle_policy'] = 'disabled'
            (root / 'AGENTS.md').write_bytes(b'Locally owned opted-out router\n')
            execute_sync(root, manifest=manifest)
            self.assertEqual(b'Locally owned opted-out router\n', (root / 'AGENTS.md').read_bytes())

    def test_old_external_manifest_remains_on_old_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest = {'schema_version': 1, 'entries': [dict(source_repo='BionicCode/template-visual-studio-repository', source_ref='main',
                source_path='AGENTS.md', target_directory='', direction='source_to_target', lifecycle_policy='enforce', uniqueness_policy='none', managed_scope='whole_file')]}
            execute_sync(root, manifest=manifest, files={'AGENTS.md': b'Legacy independent router\n'})
            self.assertEqual(b'Legacy independent router\n', (root / 'AGENTS.md').read_bytes())
            self.assertFalse((root / '.agent/instructions/package').exists())

    def test_failed_source_planning_leaves_old_router_operative(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); (root / 'AGENTS.md').write_bytes(b'Old operative router\n')
            files = local_source_files(); del files[PREFIX + 'REVIEW.md']
            with self.assertRaises(KeyError): execute_sync(root, files=files)
            self.assertEqual(b'Old operative router\n', (root / 'AGENTS.md').read_bytes())
            self.assertFalse((root / '.agent/README.md').exists())

    def test_missing_selected_module_stops_dependent_resolution(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); execute_sync(root)
            (root / '.agent/instructions/package/TESTING.md').unlink()
            with self.assertRaisesRegex(FileNotFoundError, 'package/TESTING.md'):
                read_selected(root, ('ENGINEERING', 'TESTING'))

    def test_additive_package_custom_native_order_and_override_selection(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); execute_sync(root)
            custom = root / '.agent/instructions/custom/GUARDRAILS.md'
            custom.parent.mkdir(parents=True); custom.write_text('Custom protected paths', encoding='utf-8')
            native_directory = root / 'deployment/packages/agent-package'
            native_directory.mkdir(parents=True)
            (native_directory / 'AGENTS.md').write_text('Suppressed source payload', encoding='utf-8')
            (native_directory / 'AGENTS.override.md').write_text('Publisher-only authority', encoding='utf-8')
            paths = read_selected(root, ('ENGINEERING', 'IMPLEMENTATION', 'TESTING', 'GUARDRAILS', 'DOCUMENTATION'),
                                  'deployment/packages/agent-package/instruction-package/probe.md')
            self.assertEqual(['.agent/instructions/package/ENGINEERING.md', '.agent/instructions/package/IMPLEMENTATION.md',
                '.agent/instructions/package/TESTING.md', '.agent/instructions/package/GUARDRAILS.md', '.agent/instructions/custom/GUARDRAILS.md',
                '.agent/instructions/package/DOCUMENTATION.md', 'deployment/packages/agent-package/AGENTS.override.md'],
                [path.relative_to(root).as_posix() for path in paths])

    def test_absent_optional_custom_is_normal(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); execute_sync(root)
            self.assertEqual(2, len(read_selected(root, ('ENGINEERING', 'DOTNET'))))

    def test_illegal_path_traversal_registration_fails_before_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); manifest = registration(); manifest['entries'][0]['target_directory'] = '../outside/'
            with self.assertRaises(common.ManifestError): execute_sync(root, manifest=manifest)
            self.assertFalse((root / 'AGENTS.md').exists())


class ExplicitMetadataWitnessTests(unittest.TestCase):
    def test_final_owned_metadata_passes_existing_checker_in_disposable_fixture(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); git(root, 'init', '--quiet')
            paths = list(local_source_files())
            paths.extend(('.github/tools/agent-package/README.md', '.github/tools/agent-package/MIGRATION.md',
                          '.github/scripts/doc-metadata/update-doc-metadata.ps1',
                          '.github/tools/doc-metadata/doc-metadata-manifest.json',
                          '.github/tools/doc-metadata/doc-metadata-manifest.schema.json'))
            paths.extend(path.relative_to(REPOSITORY).as_posix() for path in (REPOSITORY / '.agent/instructions/custom').glob('*.md'))
            for relative in paths:
                destination = root / relative; destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(REPOSITORY / relative, destination)
            result = run_powershell(root, "& ./.github/scripts/doc-metadata/update-doc-metadata.ps1 -Mode Check -Root . -ManifestPath .github/tools/doc-metadata/doc-metadata-manifest.json\nif ($LASTEXITCODE -ne 0) { throw 'Owned metadata check failed.' }")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn('failed=0', result.stdout)

    def test_incomplete_existing_frontmatter_fails_without_unrelated_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); installed, copilot = metadata_fixture(root)
            copilot.write_bytes(strip_managed_metadata(copilot.read_bytes()))
            original = copilot.read_bytes()
            before = ((root / 'README.md').read_bytes(), git(root, 'ls-files', '--stage'), installed.read_bytes())
            result = run_powershell(root, "$env:GIT_OPTIONAL_LOCKS = '0'\n" + powershell_recipe('source-metadata-update'))
            self.assertNotEqual(0, result.returncode)
            self.assertEqual(original, copilot.read_bytes())
            self.assertEqual(before, ((root / 'README.md').read_bytes(), git(root, 'ls-files', '--stage'), installed.read_bytes()))

    def test_explicit_untracked_initialization_preserves_staged_bytes_index_and_yaml(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); installed, copilot = metadata_fixture(root)
            before = ((root / 'README.md').read_bytes(), git(root, 'ls-files', '--stage'), (root / '.git/index').read_bytes(), installed.read_bytes())
            self.assertIn(b'?? deployment/', git(root, 'status', '--porcelain'))
            result = run_powershell(root, "$env:GIT_OPTIONAL_LOCKS = '0'\n" + powershell_recipe('source-metadata-update'))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            after = ((root / 'README.md').read_bytes(), git(root, 'ls-files', '--stage'), (root / '.git/index').read_bytes(), installed.read_bytes())
            self.assertEqual(before, after)
            source = root / PREFIX / 'AGENTS.md'
            self.assertRegex(source.read_text(encoding='utf-8'), r'(?m)^Version: 1$')
            self.assertRegex(source.read_text(encoding='utf-8'), r'(?m)^Created: \d{4}-')
            self.assertIn('customField: preserved', copilot.read_text(encoding='utf-8'))
            self.assertIn('applyTo: "test/**/*,tests/**/*,.github/scripts/**/tests/**/*"', copilot.read_text(encoding='utf-8'))

    def test_source_metadata_then_rematerialization_restores_byte_parity(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); metadata_fixture(root)
            result = run_powershell(root, "$env:GIT_OPTIONAL_LOCKS = '0'\n" + powershell_recipe('source-metadata-update'))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            files = {PREFIX + path.relative_to(root / PREFIX).as_posix(): path.read_bytes() for path in (root / PREFIX).rglob('*') if path.is_file()}
            execute_sync(root, files=files)
            source = root / PREFIX / 'instruction-package/instructions/package/ENGINEERING.md'
            installed = root / '.agent/instructions/package/ENGINEERING.md'
            original = installed.read_bytes(); source.write_bytes(source.read_bytes() + b'\nSource maintenance witness\n')
            result = run_powershell(root, "$env:GIT_OPTIONAL_LOCKS = '0'\n" + powershell_recipe('source-metadata-update'))
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(original, installed.read_bytes())
            files = {PREFIX + path.relative_to(root / PREFIX).as_posix(): path.read_bytes() for path in (root / PREFIX).rglob('*') if path.is_file()}
            execute_sync(root, files=files); execute_sync(root, files=files, verify=True)
            self.assertEqual(source.read_bytes(), installed.read_bytes())


if __name__ == '__main__':
    unittest.main()
