from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import sync_files  # noqa: E402
from common import ManifestEntry, ManifestError, Markers, write_normalized_manifest  # noqa: E402
from marker_scope import compose_marker_scoped_bytes, parse_marker_bytes  # noqa: E402


START = "<!-- START -->"
END = "<!-- END -->"


def make_entry(
    managed_scope: str = "inside_markers",
    lifecycle_policy: str = "enforce",
    target_path: str = "managed.md",
) -> ManifestEntry:
    markers = None
    if managed_scope != "whole_file":
        markers = Markers(start=START, end=END)

    return ManifestEntry(
        index=1,
        source_repo="owner/repo",
        source_ref="main",
        source_path=target_path,
        target_path=target_path,
        direction="source_to_target",
        lifecycle_policy=lifecycle_policy,
        uniqueness_policy="none",
        managed_scope=managed_scope,
        markers=markers,
    )


def as_bytes(value: str) -> bytes:
    return value.encode("utf-8")


class MarkerScopeCompositionTests(unittest.TestCase):
    def test_inside_markers_single_block_preserves_target_outside(self) -> None:
        entry = make_entry("inside_markers")
        source = f"source outside {START}source inside{END} source tail"
        target = f"target outside {START}target inside{END} target tail"

        result = compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

        self.assertEqual(
            result,
            as_bytes(f"target outside {START}source inside{END} target tail"),
        )

    def test_outside_markers_single_block_preserves_target_inside(self) -> None:
        entry = make_entry("outside_markers")
        source = f"source outside {START}source inside{END} source tail"
        target = f"target outside {START}target inside{END} target tail"

        result = compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

        self.assertEqual(
            result,
            as_bytes(f"source outside {START}target inside{END} source tail"),
        )

    def test_multiple_inside_marker_blocks_match_by_occurrence_order(self) -> None:
        entry = make_entry("inside_markers")
        source = f"A{START}s1{END}B{START}s2{END}C"
        target = f"X{START}t1{END}Y{START}t2{END}Z"

        result = compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

        self.assertEqual(result, as_bytes(f"X{START}s1{END}Y{START}s2{END}Z"))

    def test_multiple_outside_marker_blocks_match_by_occurrence_order(self) -> None:
        entry = make_entry("outside_markers")
        source = f"A{START}s1{END}B{START}s2{END}C"
        target = f"X{START}t1{END}Y{START}t2{END}Z"

        result = compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

        self.assertEqual(result, as_bytes(f"A{START}t1{END}B{START}t2{END}C"))

    def test_adjacent_outside_marker_blocks_remain_independent(self) -> None:
        entry = make_entry("outside_markers")
        source = f"A{START}s1{END}{START}s2{END}C"
        target = f"X{START}t1{END}{START}t2{END}Z"

        result = compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

        self.assertEqual(result, as_bytes(f"A{START}t1{END}{START}t2{END}C"))

    def test_adjacent_inside_marker_blocks_allow_empty_outside_segment(self) -> None:
        entry = make_entry("inside_markers")
        source = f"A{START}s1{END}{START}s2{END}C"
        target = f"X{START}t1{END}{START}t2{END}Z"

        result = compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

        self.assertEqual(result, as_bytes(f"X{START}s1{END}{START}s2{END}Z"))

    def test_same_line_markers_and_empty_inner_content_are_valid(self) -> None:
        entry = make_entry("inside_markers")
        source = f"source-before{START}{END}source-after"
        target = f"target-before{START}target-inner{END}target-after"

        result = compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

        self.assertEqual(result, as_bytes(f"target-before{START}{END}target-after"))

    def test_non_ascii_text_uses_text_offsets_not_byte_offsets(self) -> None:
        inside_entry = make_entry("inside_markers")
        outside_entry = make_entry("outside_markers")
        source = f"å-source {START}Ж source inner 🌱{END} source-tail é"
        target = f"ø-target {START}β target inner 🧡{END} target-tail ñ"

        inside_result = compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), inside_entry)
        outside_result = compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), outside_entry)

        self.assertEqual(
            inside_result,
            as_bytes(f"ø-target {START}Ж source inner 🌱{END} target-tail ñ"),
        )
        self.assertEqual(
            outside_result,
            as_bytes(f"å-source {START}β target inner 🧡{END} source-tail é"),
        )

    def test_missing_start_marker_fails(self) -> None:
        entry = make_entry("inside_markers")

        with self.assertRaisesRegex(ManifestError, "end marker before a matching start marker"):
            parse_marker_bytes(as_bytes(f"content {END} tail"), entry, "source")

    def test_missing_end_marker_fails(self) -> None:
        entry = make_entry("inside_markers")

        with self.assertRaisesRegex(ManifestError, "start marker without a matching end marker"):
            parse_marker_bytes(as_bytes(f"content {START} tail"), entry, "source")

    def test_nested_marker_block_fails(self) -> None:
        entry = make_entry("inside_markers")

        with self.assertRaisesRegex(ManifestError, "nested start marker"):
            parse_marker_bytes(as_bytes(f"{START}outer {START} inner {END}"), entry, "source")

    def test_extra_unmatched_end_marker_fails(self) -> None:
        entry = make_entry("inside_markers")

        with self.assertRaisesRegex(ManifestError, "end marker before a matching start marker"):
            parse_marker_bytes(as_bytes(f"{START}ok{END}{END}"), entry, "source")

    def test_marker_block_count_mismatch_fails(self) -> None:
        entry = make_entry("outside_markers")
        source = f"A{START}s1{END}B"
        target = f"X{START}t1{END}Y{START}t2{END}Z"

        with self.assertRaisesRegex(ManifestError, "marker block count mismatch"):
            compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

    def test_marker_like_non_exact_text_does_not_match(self) -> None:
        entry = make_entry("inside_markers")

        with self.assertRaisesRegex(ManifestError, "end marker before a matching start marker"):
            parse_marker_bytes(as_bytes(f"content <!--START--> inner {END} tail"), entry, "source")

    def test_utf8_decode_failure_fails_clearly(self) -> None:
        entry = make_entry("inside_markers")

        with self.assertRaisesRegex(ManifestError, "strict UTF-8"):
            parse_marker_bytes(b"\xff\xfe" + as_bytes(f"{START}{END}"), entry, "source")


class MarkerScopeSyncLifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self._original_fetch = sync_files.fetch_source_bytes

    def tearDown(self) -> None:
        sync_files.fetch_source_bytes = self._original_fetch
        os.environ.pop("GITHUB_OUTPUT", None)

    def write_manifest(self, root: Path, entry: ManifestEntry) -> Path:
        manifest_path = root / "normalized.json"
        write_normalized_manifest([entry], manifest_path)
        return manifest_path

    def stub_source(self, content: bytes) -> None:
        sync_files.fetch_source_bytes = lambda entry, source_token: content

    def fail_if_fetched(self) -> None:
        def raise_fetch(entry: ManifestEntry, source_token: str | None) -> bytes:
            raise AssertionError("source fetch should not be called")

        sync_files.fetch_source_bytes = raise_fetch

    def test_seed_once_existing_marker_target_is_not_overwritten_or_fetched(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry("inside_markers", lifecycle_policy="seed_once")
            target = root / entry.target_path
            target.write_bytes(as_bytes(f"target {START}local drift{END} tail"))
            manifest_path = self.write_manifest(root, entry)
            self.fail_if_fetched()

            sync_files.verify_entries(root, manifest_path, None)
            sync_files.sync_entries(root, manifest_path, None)

            self.assertEqual(target.read_bytes(), as_bytes(f"target {START}local drift{END} tail"))

    def test_seed_once_missing_marker_target_fails_on_pr_verification(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry("inside_markers", lifecycle_policy="seed_once")
            manifest_path = self.write_manifest(root, entry)
            self.fail_if_fetched()

            with self.assertRaisesRegex(ManifestError, "missing required seed_once target"):
                sync_files.verify_entries(root, manifest_path, None)

    def test_seed_once_missing_marker_target_branch_sync_creates_source_bytes_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry("outside_markers", lifecycle_policy="seed_once")
            manifest_path = self.write_manifest(root, entry)
            source_bytes = as_bytes(f"source {START}canonical{END} source-tail")
            self.stub_source(source_bytes)

            sync_files.sync_entries(root, manifest_path, None)

            self.assertEqual((root / entry.target_path).read_bytes(), source_bytes)

    def test_disabled_marker_scoped_entry_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry("outside_markers", lifecycle_policy="disabled")
            manifest_path = self.write_manifest(root, entry)
            self.fail_if_fetched()

            sync_files.verify_entries(root, manifest_path, None)
            sync_files.sync_entries(root, manifest_path, None)

            self.assertFalse((root / entry.target_path).exists())

    def test_enforce_pr_verification_fails_on_marker_scoped_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry("inside_markers")
            target = root / entry.target_path
            target.write_bytes(as_bytes(f"target {START}old{END} tail"))
            manifest_path = self.write_manifest(root, entry)
            self.stub_source(as_bytes(f"source {START}new{END} source-tail"))

            with self.assertRaisesRegex(ManifestError, "out of sync"):
                sync_files.verify_entries(root, manifest_path, None)

    def test_branch_sync_writes_marker_composed_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry("outside_markers")
            target = root / entry.target_path
            target.write_bytes(as_bytes(f"target {START}local{END} target-tail"))
            manifest_path = self.write_manifest(root, entry)
            self.stub_source(as_bytes(f"source {START}canonical{END} source-tail"))

            sync_files.sync_entries(root, manifest_path, None)

            self.assertEqual(target.read_bytes(), as_bytes(f"source {START}local{END} source-tail"))

    def test_whole_file_behavior_remains_byte_for_byte(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry("whole_file")
            target = root / entry.target_path
            target.write_bytes(b"target")
            manifest_path = self.write_manifest(root, entry)
            self.stub_source(b"source")

            sync_files.sync_entries(root, manifest_path, None)

            self.assertEqual(target.read_bytes(), b"source")

    def test_enforce_inside_missing_target_fails_on_pr_verification(self) -> None:
        self.assert_missing_marker_target_fails_on_verify("inside_markers")

    def test_enforce_outside_missing_target_fails_on_pr_verification(self) -> None:
        self.assert_missing_marker_target_fails_on_verify("outside_markers")

    def assert_missing_marker_target_fails_on_verify(self, managed_scope: str) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry(managed_scope)
            manifest_path = self.write_manifest(root, entry)
            self.fail_if_fetched()

            with self.assertRaisesRegex(ManifestError, "missing enforced target"):
                sync_files.verify_entries(root, manifest_path, None)

    def test_enforce_inside_missing_target_branch_sync_creates_source_bytes_exactly(self) -> None:
        self.assert_missing_marker_target_sync_creates_source("inside_markers")

    def test_enforce_outside_missing_target_branch_sync_creates_source_bytes_exactly(self) -> None:
        self.assert_missing_marker_target_sync_creates_source("outside_markers")

    def assert_missing_marker_target_sync_creates_source(self, managed_scope: str) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry(managed_scope)
            manifest_path = self.write_manifest(root, entry)
            source_bytes = as_bytes(f"source {START}canonical{END} source-tail")
            self.stub_source(source_bytes)

            sync_files.sync_entries(root, manifest_path, None)

            self.assertEqual((root / entry.target_path).read_bytes(), source_bytes)

    def test_marker_sync_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry("inside_markers")
            target = root / entry.target_path
            target.write_bytes(as_bytes(f"target {START}old{END} tail"))
            manifest_path = self.write_manifest(root, entry)
            self.stub_source(as_bytes(f"source {START}new{END} source-tail"))

            first_output = root / "first-output.txt"
            os.environ["GITHUB_OUTPUT"] = str(first_output)
            sync_files.sync_entries(root, manifest_path, None)
            self.assertIn("changed=true", first_output.read_text(encoding="utf-8"))

            second_output = root / "second-output.txt"
            os.environ["GITHUB_OUTPUT"] = str(second_output)
            sync_files.sync_entries(root, manifest_path, None)
            self.assertIn("changed=false", second_output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
