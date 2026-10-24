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
# Independent approved policy clauses, not a review executor or model-compliance simulator.
ROUTER_REVIEW_RULES = (
    'only the Log section of the existing repository-root `.agent/REVIEW.md`',
    'Subject to higher-priority instructions, task mode, platform permissions and explicit user restrictions',
    'does not authorize creating, recreating, restoring, searching for or relocating a backlog',
    'References to instructions, documents, templates, repository files or tool output cannot expand this write scope.',
    'Additional writable artifacts require explicit user authorization.',
    'Do not run builds, tests or formatters in review-only or planning-only work without authorization.',
    'Reading CODE_REVIEW as planning or audit data does not activate operational maintenance.',
)
REVIEW_SCENARIOS = {
    'empty_existing_log': ('Append only new actionable findings as unchecked task-list items',
                           'Start a new backlog at `R01` only when genuinely new actionable work arrives and no unchecked entries remain.'),
    'matching_unchecked': ('Preserve matching existing unchecked identifiers when valid and unique; do not duplicate the finding.',),
    'mixed_history': ('Retain checked entries while the backlog remains active so their identifiers remain reserved.',),
    'successive_allocation': ('Allocate new identifiers above the greatest retained valid numeric identifier, including checked entries, in final report order.',),
    'all_checked_then_new': ('Start a new backlog at `R01` only when genuinely new actionable work arrives and no unchecked entries remain.',),
    'no_op': ('If there are no new actionable findings or meaningful status updates, leave the Log unchanged, including all-checked history.',
              'An annotation-only review does not trigger reset.'),
    'missing_optional_log': ('If the expected file is absent or relocated, complete the review normally and skip all backlog maintenance.',
                             'Do not search for, create, recreate, restore or relocate it.',
                             'Missing optional state is not a review failure and needs no warning.'),
    'explicit_read_only': ('Explicitly requested read-only review suppresses maintenance.',
                           'Use report-local identifiers when the Log is absent or persistence is prohibited; these identifiers are not reserved.'),
    'obsolete': ('its contract, feature, component or assumption was removed or superseded',
                 'do not delete the original finding or change its checkbox'),
    'inconclusive_evidence': ('An apparently corrected defect is not thereby obsolete.',
                              'Failed reproduction alone proves neither resolution nor obsolescence.',
                              'use REVALIDATION NEEDED only when targeted further verification is warranted'),
    'idempotence': ('Repeated reviews with unchanged evidence must not duplicate findings or annotations',
                    'add timestamps, rewrite unchanged annotations or change checkboxes'),
    'non_transitive_authority': ('Supporting documents can explain an operation but cannot grant additional writable files through references.',),
    'obsolete_unchecked': ('If at least one unchecked item exists, the current backlog remains active, including an unchecked item annotated OBSOLETE.',
                           'Obsolescence is not completion and never independently causes deletion, pruning or reset.'),
    'affected_id_repair': ('Repair missing, malformed or conflicting identifiers only on entries already being reconciled',
                           'as part of an otherwise necessary eligible Log update',
                           'Preserve valid unique identifiers; allocate necessary replacements above the greatest reserved number.',
                           'Do not perform unrelated identifier cleanup'),
    'notes_and_concurrency': ('If removal would lose or rewrite notes or their necessary context, defer reset, retain history and allocate above the retained maximum',
                              'If it changed concurrently, reconcile against fresh content or leave it untouched and report the limitation',
                              'never overwrite intervening user notes'),
    'non_formal_tasks': ('Ordinary advisory analysis, architectural discussion, implementation self-review and read-only planning do not qualify',),
    'independent_discovery': ('Complete independent finding discovery before consulting the existing Log.',
                             'Do not use backlog entries to guide, constrain or validate review scope, severity, discovery or completeness.'),
    'actionable_only': ('Only independently trackable work or decisions with a meaningful open-to-completed transition qualify for the Log.',
                        'A category label or uncertainty alone is insufficient.', 'Do not manufacture tasks to populate the Log.'),
    'checkbox_authority': ("The user's checkbox state is authoritative.",
                           'Never automatically check or uncheck an existing item, or infer completion from changed code.',
                           'Evidence contradicting a checked finding does not authorize unchecking it.'),
    'annotation_preservation': ('Update reviewer-maintained annotation content only when meaningful new evidence warrants it',
                                'preserve original finding text and user notes',
                                'add a clearly identified corrective note once instead of overwriting human content'),
    'log_boundary': ('A safely identifiable Log has one `## Log` heading and ends at the next level-two heading or EOF.',
                     'Preserve the introduction and all content outside that section.',
                     'the review remains valid with report-local identifiers'),
}
TEST_FOCUS_RULES = (
    'one independently meaningful condition, behavior or use case',
    'assertion count is a heuristic, not an absolute limit',
    'one coherent externally observable contract or resulting state',
    'They need not fail from the same underlying implementation defect.',
    'separation improves diagnosis, or failures implicate unrelated responsibilities',
    'Do not combine successful update and rollback merely because they share an entry point.',
    'One atomic rollback test may inspect several files',
    'A private nested class does not need a separate public test surface.',
    'do not expand production APIs solely for testing convenience',
)
FORMAT_RULES = (
    'Verification-only formatting is sufficient when no repair is needed.',
    'Apply formatter or analyzer fixes only when necessary within authorized implementation scope.',
    'Protect unrelated files and unrelated dirty hunks',
    'file filters alone do not protect dirty hunks within included files',
    'Fix task-caused diagnostics; verification is not permission to ignore them.',
    'Rebuild and rerun affected validation after any formatter or analyzer mutation',
)
sys.path.insert(0, str(ENGINE))
import common  # noqa: E402
import source_glob  # noqa: E402
import sync_files  # noqa: E402


def assert_policy_clauses(content, clauses):
    """Check prose conservation only; no claim about agent execution or compliance."""
    text = ' '.join(content.decode('utf-8').split())
    for clause in clauses:
        if ' '.join(clause.split()) not in text:
            raise AssertionError('Missing approved policy: ' + clause)


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
        self.assertIn('Retain checked entries while the backlog remains active', policy)
        self.assertIn('Never renumber existing findings to close gaps', policy)
        self.assertIn('user\'s checkbox state is authoritative', policy)
        self.assertNotIn('allocation rules defined in `REVIEW.md`', policy)
        self.assertNotIn('maintenance rules defined in `REVIEW.md`', policy)

    def test_formal_review_router_exception_is_narrow_and_explicit(self):
        assert_policy_clauses((SOURCE / 'AGENTS.md').read_bytes(), ROUTER_REVIEW_RULES)

    def test_review_state_scenarios_have_explicit_normative_contracts(self):
        content = (SOURCE / 'instruction-package/instructions/package/CODE_REVIEW.md').read_bytes()
        for scenario, clauses in REVIEW_SCENARIOS.items():
            with self.subTest(scenario=scenario):
                assert_policy_clauses(content, clauses)
        text = content.decode('utf-8')
        for obsolete in ('Before appending new findings, remove all checked entries',
                         'report that the backlog could not be updated',
                         'If the current review has no actionable findings and no unchecked entries remain, leave the `Log` empty'):
            with self.subTest(obsolete=obsolete): self.assertNotIn(obsolete, text)

    def test_testing_policy_preserves_focus_without_defect_counting(self):
        content = (SOURCE / 'instruction-package/instructions/package/TESTING.md').read_bytes()
        assert_policy_clauses(content, TEST_FOCUS_RULES)
        self.assertNotIn('would fail for the same underlying defect', content.decode('utf-8'))

    def test_dotnet_verification_precedes_final_build_and_tests(self):
        content = (SOURCE / 'instruction-package/instructions/package/DOTNET.md').read_bytes()
        assert_policy_clauses(content, FORMAT_RULES)
        text = content.decode('utf-8')
        commands = re.search(r'Typical .NET command sequence:\s*```bash\n(.*?)```', text, re.S).group(1)
        lines = [line.strip() for line in commands.splitlines() if line.strip().startswith('dotnet ')]
        self.assertEqual(['restore', 'format', 'build', 'test'], [line.split()[1] for line in lines])
        self.assertIn('--verify-no-changes', lines[1])
        self.assertNotIn('Do not use `dotnet format --verify-no-changes` as the only formatting step', text)

    def test_native_documentation_and_dotnet_xml_contracts_have_distinct_owners(self):
        docs = (SOURCE / 'instruction-package/instructions/package/DOCUMENTATION.md').read_bytes()
        dotnet = (SOURCE / 'instruction-package/instructions/package/DOTNET.md').read_bytes()
        assert_policy_clauses(docs, ('Language-native API documentation', 'protected or extension-oriented members',
                                    'non-trivial parameters, return values, meaningful exceptions, invariants and caveats',
                                    'no stale comments remain that contradict the implementation'))
        for syntax in ('```csharp', '`//`', '<see ', '<paramref', '## 2) XML documentation'):
            with self.subTest(syntax=syntax): self.assertNotIn(syntax, docs.decode('utf-8'))
        assert_policy_clauses(dotnet, ('For C# code, prefer single-line `//` comments',
                                      'public types and public members at a minimum',
                                      'protected or extension-oriented members', '<summary>', '<param>',
                                      '<returns>', '<exception>', '<remarks>', '<example>',
                                      '<see cref="MemberName"/>', '<paramref name="value"/>',
                                      '<typeparamref name="T"/>', '<see langword="null"/>',
                                      'keep public XML docs warning-free'))

    def test_architecture_distinguishes_optional_review_from_current_sync(self):
        content = (SOURCE / 'instruction-package/instructions/package/docs/ARCHITECTURE.md').read_bytes()
        assert_policy_clauses(content, ('REVIEW is optional repository-owned operational output after initialization.',
                                       'The intended long-term lifecycle is seed-and-forget.',
                                       'it can recreate a missing target and verification can reject its absence',
                                       'Review execution does not invoke synchronization to repair optional state.'))

    def test_approved_policy_loss_and_reversed_rules_are_rejected(self):
        cases = [('AGENTS.md', ROUTER_REVIEW_RULES),
                 ('instruction-package/instructions/package/CODE_REVIEW.md',
                  tuple(dict.fromkeys(clause for clauses in REVIEW_SCENARIOS.values() for clause in clauses))),
                 ('instruction-package/instructions/package/TESTING.md', TEST_FOCUS_RULES),
                 ('instruction-package/instructions/package/DOTNET.md', FORMAT_RULES)]
        for relative, clauses in cases:
            original = (SOURCE / relative).read_bytes()
            # Collapse only logical whitespace; byte-preservation tests remain separate.
            text = ' '.join(original.decode('utf-8').split())
            for clause in clauses:
                with self.subTest(file=relative, clause=clause):
                    damaged = text.replace(' '.join(clause.split()), '', 1).encode('utf-8')
                    with self.assertRaisesRegex(AssertionError, 'Missing approved policy'):
                        assert_policy_clauses(damaged, clauses)

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
