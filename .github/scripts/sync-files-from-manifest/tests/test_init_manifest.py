from __future__ import annotations

import argparse
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import init_manifest  # noqa: E402


class InitManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

        self.test_root = Path(self.temporary_directory.name)
        self.repository_root = self.test_root / "caller"
        self.source_root = self.test_root / "sources"
        self.documentation_source = self.source_root / "documentation"
        self.schema_source = self.source_root / "sync-manifest.schema.json"
        self.template_source = self.source_root / "sync-manifest.template.json"

        self.repository_root.mkdir()
        (self.documentation_source / "types").mkdir(parents=True)
        self.schema_source.write_bytes(b'{"schema": "current"}\n')
        self.template_source.write_bytes(b'{"manifest": "starter"}\n')
        (self.documentation_source / "types" / "manifest.md").write_bytes(
            b"# Manifest documentation\n"
        )

        self.canonical_config_directory = (
            self.repository_root / ".github" / "tools" / "sync-config"
        )
        self.legacy_config_directory = (
            self.repository_root / ".github" / "sync-config"
        )

    def run_initializer(self) -> dict[str, str]:
        arguments = argparse.Namespace(
            repo_root=str(self.repository_root),
            schema_source=str(self.schema_source),
            template_source=str(self.template_source),
            documentation_source=str(self.documentation_source),
        )

        with (
            mock.patch.object(init_manifest, "parse_args", return_value=arguments),
            mock.patch.object(init_manifest, "emit_output") as emit_output,
        ):
            exit_code = init_manifest.main()

        self.assertEqual(0, exit_code)
        return {
            str(call.args[0]): str(call.args[1])
            for call in emit_output.call_args_list
        }

    def snapshot_repository_files(self) -> dict[str, bytes]:
        return {
            path.relative_to(self.repository_root).as_posix(): path.read_bytes()
            for path in self.repository_root.rglob("*")
            if path.is_file()
        }

    def test_fresh_initialization_creates_only_canonical_configuration(self) -> None:
        outputs = self.run_initializer()

        self.assertEqual(
            b'{"schema": "current"}\n',
            (self.canonical_config_directory / "sync-manifest.schema.json").read_bytes(),
        )
        self.assertEqual(
            b'{"manifest": "starter"}\n',
            (self.canonical_config_directory / "sync-manifest.json").read_bytes(),
        )
        self.assertEqual(
            b"# Manifest documentation\n",
            (
                self.canonical_config_directory
                / "documentation"
                / "types"
                / "manifest.md"
            ).read_bytes(),
        )
        self.assertFalse(self.legacy_config_directory.exists())
        self.assertEqual("true", outputs["changed"])
        self.assertEqual("3", outputs["changed_count"])
        self.assertEqual(
            "\n".join(
                (
                    ".github/tools/sync-config/sync-manifest.schema.json",
                    ".github/tools/sync-config/sync-manifest.json",
                    ".github/tools/sync-config/documentation/types/manifest.md",
                )
            ),
            outputs["changed_paths"],
        )
        self.assertIn(
            "`.github/tools/sync-config/sync-manifest.json`",
            outputs["pull_request_body"],
        )
        self.assertNotIn(
            "`.github/sync-config/sync-manifest.json`",
            outputs["pull_request_body"],
        )

    def test_existing_canonical_manifest_is_preserved(self) -> None:
        self.canonical_config_directory.mkdir(parents=True)
        manifest_path = self.canonical_config_directory / "sync-manifest.json"
        caller_owned_manifest = b'{"caller": "owned"}\n'
        manifest_path.write_bytes(caller_owned_manifest)

        outputs = self.run_initializer()

        self.assertEqual(caller_owned_manifest, manifest_path.read_bytes())
        self.assertNotIn(
            ".github/tools/sync-config/sync-manifest.json",
            outputs["changed_paths"].splitlines(),
        )
        self.assertIn(
            "The existing caller-owned manifest was preserved and not overwritten.",
            outputs["pull_request_body"],
        )

    def test_repeated_initialization_is_idempotent(self) -> None:
        self.run_initializer()
        first_snapshot = self.snapshot_repository_files()

        outputs = self.run_initializer()

        self.assertEqual(first_snapshot, self.snapshot_repository_files())
        self.assertEqual("false", outputs["changed"])
        self.assertEqual("0", outputs["changed_count"])
        self.assertEqual("", outputs["changed_paths"])

    def test_legacy_manifest_is_not_probed_or_migrated(self) -> None:
        (self.legacy_config_directory / "documentation").mkdir(parents=True)
        legacy_manifest_path = self.legacy_config_directory / "sync-manifest.json"
        legacy_manifest = b'{"legacy": "sentinel"}\n'
        legacy_manifest_path.write_bytes(legacy_manifest)
        (self.legacy_config_directory / "sync-manifest.schema.json").write_bytes(
            b'{"legacy_schema": "sentinel"}\n'
        )
        (self.legacy_config_directory / "documentation" / "legacy.md").write_bytes(
            b"# Legacy sentinel\n"
        )
        legacy_snapshot = {
            path.relative_to(self.legacy_config_directory).as_posix(): path.read_bytes()
            for path in self.legacy_config_directory.rglob("*")
            if path.is_file()
        }

        outputs = self.run_initializer()

        self.assertEqual(
            legacy_snapshot,
            {
                path.relative_to(self.legacy_config_directory).as_posix(): path.read_bytes()
                for path in self.legacy_config_directory.rglob("*")
                if path.is_file()
            },
        )
        self.assertEqual(legacy_manifest, legacy_manifest_path.read_bytes())
        self.assertEqual(
            b'{"manifest": "starter"}\n',
            (self.canonical_config_directory / "sync-manifest.json").read_bytes(),
        )
        self.assertIn(
            ".github/tools/sync-config/sync-manifest.json",
            outputs["changed_paths"].splitlines(),
        )
        self.assertNotIn(
            ".github/sync-config/sync-manifest.json",
            outputs["changed_paths"].splitlines(),
        )


if __name__ == "__main__":
    unittest.main()
