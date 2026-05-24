from __future__ import annotations

import os
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import common  # noqa: E402
import sync_files  # noqa: E402
from common import (  # noqa: E402
    ManifestEntry,
    ManifestError,
    Markers,
    SourceFetchError,
    default_rules_path,
    default_schema_path,
    fetch_source_bytes,
    load_manifest_metadata,
    load_normalized_manifest,
    manifest_entry_path,
    load_schema,
    normalize_repo_relative_path,
    parse_markers,
    validate_and_normalize_manifest,
    write_normalized_manifest,
)
from marker_scope import compose_marker_scoped_bytes, parse_marker_bytes, text_location  # noqa: E402


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


def manifest_json(entries: list[dict[str, object]]) -> str:
    import json

    return json.dumps({"schema_version": 1, "entries": entries})


def manifest_entry_payload(
    *,
    source_repo: str = "owner/repo",
    source_ref: str = "main",
    source_path: str = "managed.md",
    target_path: str = "managed.md",
    direction: str = "source_to_target",
    lifecycle_policy: str = "enforce",
    uniqueness_policy: str = "none",
    managed_scope: str = "whole_file",
    markers: dict[str, str] | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "source_repo": source_repo,
        "source_ref": source_ref,
        "source_path": source_path,
        "target_path": target_path,
        "direction": direction,
        "lifecycle_policy": lifecycle_policy,
        "uniqueness_policy": uniqueness_policy,
        "managed_scope": managed_scope,
    }
    if markers is not None:
        payload["markers"] = markers
    return payload


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

    def test_outside_markers_empty_source_block_can_be_omitted_by_target(self) -> None:
        entry = make_entry("outside_markers")
        source = f"before{START}{END}after"
        target = "beforeafter"

        result = compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

        self.assertEqual(result, as_bytes("beforeafter"))

    def test_outside_markers_placeholder_source_block_can_be_omitted_by_target(self) -> None:
        entry = make_entry("outside_markers")
        source = f"before{START}placeholder{END}after"
        target = "beforeafter"

        result = compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

        self.assertEqual(result, as_bytes("beforeafter"))

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

    def test_multiple_outside_marker_blocks_can_all_be_omitted_by_target(self) -> None:
        entry = make_entry("outside_markers")
        source = f"A{START}s1{END}B{START}s2{END}C"
        target = "ABC"

        result = compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

        self.assertEqual(result, as_bytes("ABC"))

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

    def test_inside_markers_equal_count_blocks_are_occurrence_matched_without_context_detection(self) -> None:
        entry = make_entry("inside_markers")
        source = f"A{START}s1{END}B{START}s2{END}C"
        # Outside content is target-owned for inside_markers, so this intentionally
        # does not infer same-source-context movement without marker IDs/context anchors.
        target = f"target prefix {START}t1{END} moved outside {START}t2{END} target tail"

        result = compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

        self.assertEqual(
            result,
            as_bytes(f"target prefix {START}s1{END} moved outside {START}s2{END} target tail"),
        )

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

        with self.assertRaisesRegex(ManifestError, "partial set of marker blocks"):
            compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

    def test_outside_markers_partial_marker_set_fails(self) -> None:
        entry = make_entry("outside_markers")
        source = f"A{START}s1{END}B{START}s2{END}C"
        target = f"A{START}t1{END}BC"

        with self.assertRaisesRegex(ManifestError, "partial set of marker blocks"):
            compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

    def test_inside_markers_zero_target_blocks_fail(self) -> None:
        entry = make_entry("inside_markers")
        source = f"A{START}s1{END}B"
        target = "AB"

        with self.assertRaisesRegex(ManifestError, "inside_markers requires target marker blocks"):
            compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

    def test_inside_markers_removed_target_delimiters_and_body_fail(self) -> None:
        entry = make_entry("inside_markers")
        source = f"A{START}s1{END}B"
        target = "A local outside B"

        with self.assertRaisesRegex(ManifestError, "inside_markers requires target marker blocks"):
            compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

    def test_inside_markers_extra_exact_target_block_fails(self) -> None:
        entry = make_entry("inside_markers")
        source = f"A{START}s1{END}B"
        target = f"X{START}t1{END}Y{START}t2{END}Z"

        with self.assertRaisesRegex(ManifestError, "inside_markers requires target marker blocks"):
            compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

    def test_outside_markers_target_keeps_original_block_and_adds_another_fails(self) -> None:
        entry = make_entry("outside_markers")
        source = f"A{START}s1{END}B"
        target = f"A{START}t1{END}B{START}extra{END}C"

        with self.assertRaisesRegex(ManifestError, "partial set of marker blocks"):
            compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

    def test_marker_like_non_exact_text_does_not_match(self) -> None:
        entry = make_entry("inside_markers")

        with self.assertRaisesRegex(ManifestError, "end marker before a matching start marker"):
            parse_marker_bytes(as_bytes(f"content <!--START--> inner {END} tail"), entry, "source")

    def test_utf8_decode_failure_fails_clearly(self) -> None:
        entry = make_entry("inside_markers")

        with self.assertRaisesRegex(ManifestError, "strict UTF-8.*byte offset 0\\.\\.1"):
            parse_marker_bytes(b"\xff\xfe" + as_bytes(f"{START}{END}"), entry, "source")

    def test_text_location_counts_lf_lines_and_columns(self) -> None:
        location = text_location("alpha\nbeta", 6)

        self.assertEqual(location.line, 2)
        self.assertEqual(location.column, 1)
        self.assertEqual(location.offset, 6)

    def test_text_location_counts_crlf_as_one_newline(self) -> None:
        location = text_location("alpha\r\nbeta", 7)

        self.assertEqual(location.line, 2)
        self.assertEqual(location.column, 1)
        self.assertEqual(location.offset, 7)

    def test_end_marker_before_start_reports_line_column(self) -> None:
        entry = make_entry("inside_markers")

        with self.assertRaisesRegex(ManifestError, r"line 2, column 1, char offset 6"):
            parse_marker_bytes(as_bytes(f"intro\n{END} tail"), entry, "source")

    def test_start_marker_without_matching_end_reports_line_column(self) -> None:
        entry = make_entry("inside_markers")

        with self.assertRaisesRegex(ManifestError, r"line 2, column 1, char offset 6"):
            parse_marker_bytes(as_bytes(f"intro\n{START} tail"), entry, "source")

    def test_nested_start_marker_reports_nested_line_column(self) -> None:
        entry = make_entry("inside_markers")

        with self.assertRaisesRegex(ManifestError, r"line 2, column 7, char offset 26"):
            parse_marker_bytes(as_bytes(f"{START}outer\ninner {START} nested{END}"), entry, "source")

    def test_no_exact_marker_blocks_reports_expected_markers_and_content_length(self) -> None:
        entry = make_entry("inside_markers")

        with self.assertRaises(ManifestError) as context:
            parse_marker_bytes(as_bytes("plain text"), entry, "source")

        message = str(context.exception)
        self.assertIn("exact start marker", message)
        self.assertIn(repr(START), message)
        self.assertIn(repr(END), message)
        self.assertIn("content length is 10 character(s)", message)

    def test_outside_partial_mismatch_reports_counts_and_target_marker_location(self) -> None:
        entry = make_entry("outside_markers")
        source = f"A{START}s1{END}B{START}s2{END}C"
        target = f"target\n{START}t1{END}BC"

        with self.assertRaises(ManifestError) as context:
            compose_marker_scoped_bytes(as_bytes(source), as_bytes(target), entry)

        message = str(context.exception)
        self.assertIn("source has 2 block(s), target has 1 block(s)", message)
        self.assertIn("target marker block starts: #1 at line 2, column 1", message)


class MarkerScopeSyncLifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self._original_fetch = sync_files.fetch_source_bytes
        self._original_atomic_write = sync_files.write_file_bytes_atomically
        self._original_replace = sync_files.os.replace

    def tearDown(self) -> None:
        sync_files.fetch_source_bytes = self._original_fetch
        sync_files.write_file_bytes_atomically = self._original_atomic_write
        sync_files.os.replace = self._original_replace
        os.environ.pop("GITHUB_OUTPUT", None)

    def write_manifest(self, root: Path, entry: ManifestEntry | list[ManifestEntry]) -> Path:
        manifest_path = root / "normalized.json"
        entries = entry if isinstance(entry, list) else [entry]
        write_normalized_manifest(entries, manifest_path)
        return manifest_path

    def stub_source(self, content: bytes) -> None:
        sync_files.fetch_source_bytes = lambda entry, source_token: content

    def stub_sources(self, sources_by_target_path: dict[str, bytes]) -> None:
        sync_files.fetch_source_bytes = lambda entry, source_token: sources_by_target_path[entry.target_path]

    def fail_if_fetched(self) -> None:
        def raise_fetch(entry: ManifestEntry, source_token: str | None) -> bytes:
            raise AssertionError("source fetch should not be called")

        sync_files.fetch_source_bytes = raise_fetch

    def assert_no_success_outputs(self, output_path: Path) -> None:
        if output_path.exists():
            output = output_path.read_text(encoding="utf-8")
            self.assertNotIn("changed=", output)
            self.assertNotIn("changed_count=", output)
            self.assertNotIn("changed_paths", output)
            self.assertNotIn("pull_request_body", output)

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

    def test_outside_projection_with_zero_target_blocks_verifies_without_change(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry("outside_markers")
            target = root / entry.target_path
            target.write_bytes(as_bytes("source  source-tail"))
            manifest_path = self.write_manifest(root, entry)
            self.stub_source(as_bytes(f"source {START}placeholder{END} source-tail"))

            sync_files.verify_entries(root, manifest_path, None)
            sync_files.sync_entries(root, manifest_path, None)

            self.assertEqual(target.read_bytes(), as_bytes("source  source-tail"))

    def test_outside_projection_removed_delimiters_but_kept_body_is_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry("outside_markers")
            target = root / entry.target_path
            target.write_bytes(as_bytes("source placeholder source-tail"))
            manifest_path = self.write_manifest(root, entry)
            self.stub_source(as_bytes(f"source {START}placeholder{END} source-tail"))

            with self.assertRaisesRegex(ManifestError, "out of sync"):
                sync_files.verify_entries(root, manifest_path, None)

            sync_files.sync_entries(root, manifest_path, None)
            self.assertEqual(target.read_bytes(), as_bytes("source  source-tail"))

    def test_outside_projection_custom_text_where_block_was_omitted_is_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry("outside_markers")
            target = root / entry.target_path
            target.write_bytes(as_bytes("source custom source-tail"))
            manifest_path = self.write_manifest(root, entry)
            self.stub_source(as_bytes(f"source {START}placeholder{END} source-tail"))

            with self.assertRaisesRegex(ManifestError, "out of sync"):
                sync_files.verify_entries(root, manifest_path, None)

            sync_files.sync_entries(root, manifest_path, None)
            self.assertEqual(target.read_bytes(), as_bytes("source  source-tail"))

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

    def test_planning_marker_failure_writes_nothing_and_emits_no_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first_entry = make_entry("whole_file", target_path="first.txt")
            second_entry = make_entry("inside_markers", target_path="second.md")
            first_target = root / first_entry.target_path
            second_target = root / second_entry.target_path
            first_target.write_bytes(b"old first")
            second_target.write_bytes(as_bytes(f"target {START}old{END} tail"))
            manifest_path = self.write_manifest(root, [first_entry, second_entry])
            output_path = root / "github-output.txt"
            os.environ["GITHUB_OUTPUT"] = str(output_path)
            self.stub_sources(
                {
                    first_entry.target_path: b"new first",
                    second_entry.target_path: b"source without markers",
                }
            )

            with self.assertRaisesRegex(ManifestError, "found no exact marker blocks"):
                sync_files.sync_entries(root, manifest_path, None)

            self.assertEqual(first_target.read_bytes(), b"old first")
            self.assertEqual(second_target.read_bytes(), as_bytes(f"target {START}old{END} tail"))
            self.assert_no_success_outputs(output_path)

    def test_planning_source_fetch_failure_writes_nothing_and_emits_no_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first_entry = make_entry("whole_file", target_path="first.txt")
            second_entry = make_entry("whole_file", target_path="second.txt")
            first_target = root / first_entry.target_path
            second_target = root / second_entry.target_path
            first_target.write_bytes(b"old first")
            second_target.write_bytes(b"old second")
            manifest_path = self.write_manifest(root, [first_entry, second_entry])
            output_path = root / "github-output.txt"
            os.environ["GITHUB_OUTPUT"] = str(output_path)

            def fetch_or_fail(entry: ManifestEntry, source_token: str | None) -> bytes:
                if entry.target_path == first_entry.target_path:
                    return b"new first"
                raise SourceFetchError("source fetch failed")

            sync_files.fetch_source_bytes = fetch_or_fail

            with self.assertRaisesRegex(SourceFetchError, "source fetch failed"):
                sync_files.sync_entries(root, manifest_path, None)

            self.assertEqual(first_target.read_bytes(), b"old first")
            self.assertEqual(second_target.read_bytes(), b"old second")
            self.assert_no_success_outputs(output_path)

    def test_planning_failure_does_not_create_missing_nested_target_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first_entry = make_entry("whole_file", target_path="nested/first.txt")
            second_entry = make_entry("inside_markers", target_path="second.md")
            second_target = root / second_entry.target_path
            second_target.write_bytes(as_bytes(f"target {START}old{END} tail"))
            manifest_path = self.write_manifest(root, [first_entry, second_entry])
            self.stub_sources(
                {
                    first_entry.target_path: b"new first",
                    second_entry.target_path: b"source without markers",
                }
            )

            with self.assertRaisesRegex(ManifestError, "found no exact marker blocks"):
                sync_files.sync_entries(root, manifest_path, None)

            self.assertFalse((root / "nested").exists())
            self.assertEqual(second_target.read_bytes(), as_bytes(f"target {START}old{END} tail"))

    def test_commit_failure_emits_no_success_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry("whole_file", target_path="managed.txt")
            target = root / entry.target_path
            target.write_bytes(b"old")
            manifest_path = self.write_manifest(root, entry)
            output_path = root / "github-output.txt"
            os.environ["GITHUB_OUTPUT"] = str(output_path)
            self.stub_source(b"new")

            def fail_replace(source: str, destination: str) -> None:
                raise OSError("replace failed")

            sync_files.os.replace = fail_replace

            with self.assertRaisesRegex(ManifestError, "Unable to write target file"):
                sync_files.sync_entries(root, manifest_path, None)

            self.assertEqual(target.read_bytes(), b"old")
            self.assert_no_success_outputs(output_path)
            self.assertEqual(list(root.glob(".managed.txt.*.tmp")), [])

    def test_successful_multi_entry_sync_writes_all_changes_then_emits_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first_entry = make_entry("whole_file", target_path="first.txt")
            second_entry = make_entry("whole_file", target_path="second.txt")
            third_entry = make_entry("whole_file", target_path="third.txt")
            (root / first_entry.target_path).write_bytes(b"old first")
            (root / second_entry.target_path).write_bytes(b"same second")
            (root / third_entry.target_path).write_bytes(b"old third")
            manifest_path = self.write_manifest(root, [first_entry, second_entry, third_entry])
            output_path = root / "github-output.txt"
            os.environ["GITHUB_OUTPUT"] = str(output_path)
            self.stub_sources(
                {
                    first_entry.target_path: b"new first",
                    second_entry.target_path: b"same second",
                    third_entry.target_path: b"new third",
                }
            )

            sync_files.sync_entries(root, manifest_path, None)

            self.assertEqual((root / first_entry.target_path).read_bytes(), b"new first")
            self.assertEqual((root / second_entry.target_path).read_bytes(), b"same second")
            self.assertEqual((root / third_entry.target_path).read_bytes(), b"new third")
            output = output_path.read_text(encoding="utf-8")
            self.assertIn("changed=true", output)
            self.assertIn("changed_count=2", output)
            self.assertIn("first.txt", output)
            self.assertIn("third.txt", output)
            self.assertNotIn("second.txt", output)

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

    def test_verify_drift_reports_first_differing_byte_offset(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry("whole_file")
            target = root / entry.target_path
            target.write_bytes(b"abc")
            manifest_path = self.write_manifest(root, entry)
            self.stub_source(b"axc")

            with self.assertRaises(ManifestError) as context:
                sync_files.verify_entries(root, manifest_path, None)

            self.assertIn("First differing byte offset: 1", str(context.exception))

    def test_marker_verify_drift_reports_target_line_column_on_utf8_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry("inside_markers")
            target = root / entry.target_path
            target.write_bytes(as_bytes(f"line1\nprefix {START}old{END} tail"))
            manifest_path = self.write_manifest(root, entry)
            self.stub_source(as_bytes(f"source\nprefix {START}new{END} source-tail"))

            with self.assertRaises(ManifestError) as context:
                sync_files.verify_entries(root, manifest_path, None)

            message = str(context.exception)
            self.assertIn("First differing byte offset:", message)
            self.assertIn("target line 2, column", message)

    def test_marker_verify_drift_omits_line_column_inside_multibyte_sequence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            entry = make_entry("inside_markers")
            target = root / entry.target_path
            target.write_bytes(as_bytes(f"{START}é{END}"))
            manifest_path = self.write_manifest(root, entry)
            self.stub_source(as_bytes(f"{START}è{END}"))

            with self.assertRaises(ManifestError) as context:
                sync_files.verify_entries(root, manifest_path, None)

            message = str(context.exception)
            self.assertIn("First differing byte offset:", message)
            self.assertNotIn("target line", message)


    def test_manifest_entry_path_converts_human_entry_numbers_to_zero_based_jsonpath(self) -> None:
        self.assertEqual("$.entries[0]", manifest_entry_path(1))
        self.assertEqual("$.entries[1].target_path", manifest_entry_path(2, "target_path"))

    def test_manifest_entry_path_rejects_non_positive_entry_numbers(self) -> None:
        with self.assertRaises(ValueError):
            manifest_entry_path(0)

    def test_malformed_normalized_manifest_reports_line_column(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "normalized.json"
            path.write_text('{\n  "entries": [\n', encoding="utf-8")

            with self.assertRaises(ManifestError) as context:
                load_normalized_manifest(path)

            message = str(context.exception)
            self.assertIn("Normalized manifest file", message)
            self.assertIn("line 3, column 1", message)

    def test_duplicate_target_semantic_error_includes_jsonpath(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = manifest_json(
                [
                    manifest_entry_payload(source_repo="owner/one", source_path="same.md", target_path="same.md"),
                    manifest_entry_payload(source_repo="owner/two", source_path="same.md", target_path="same.md"),
                ]
            )

            with self.assertRaises(ManifestError) as context:
                validate_and_normalize_manifest(
                    manifest,
                    Path(temp_dir),
                    default_schema_path(),
                    default_rules_path(),
                )

            message = str(context.exception)
            self.assertIn("$.entries[1].target_path", message)
            self.assertIn("$.entries[0].target_path", message)

    def test_basename_mismatch_semantic_error_includes_jsonpaths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = manifest_json(
                [
                    manifest_entry_payload(source_path="source.md", target_path="target.md"),
                ]
            )

            with self.assertRaises(ManifestError) as context:
                validate_and_normalize_manifest(
                    manifest,
                    Path(temp_dir),
                    default_schema_path(),
                    default_rules_path(),
                )

            message = str(context.exception)
            self.assertIn("$.entries[0].source_path", message)
            self.assertIn("$.entries[0].target_path", message)

    def test_unsafe_path_semantic_error_includes_jsonpath(self) -> None:
        with self.assertRaises(ManifestError) as context:
            normalize_repo_relative_path("../bad.md", "target_path", 1)

        self.assertIn("$.entries[0].target_path", str(context.exception))

    def test_marker_semantic_error_includes_jsonpath(self) -> None:
        metadata = load_manifest_metadata(load_schema(default_schema_path()))

        with self.assertRaises(ManifestError) as context:
            parse_markers({"markers": {"start": START, "end": START}}, metadata, 1)

        self.assertIn("$.entries[0].markers", str(context.exception))

    def test_reserved_target_path_semantic_error_includes_jsonpath(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = manifest_json(
                [
                    manifest_entry_payload(
                        source_path="managed.md",
                        target_path="_sync-files-from-manifest-workflow/managed.md",
                    ),
                ]
            )

            with self.assertRaises(ManifestError) as context:
                validate_and_normalize_manifest(
                    manifest,
                    Path(temp_dir),
                    default_schema_path(),
                    default_rules_path(),
                )

            self.assertIn("$.entries[0].target_path", str(context.exception))

    def test_source_fetch_failure_includes_source_field_jsonpath_hints(self) -> None:
        entry = make_entry("whole_file")
        original_urlopen = common.urllib.request.urlopen

        def fail_urlopen(*args: object, **kwargs: object) -> object:
            raise urllib.error.URLError("boom")

        common.urllib.request.urlopen = fail_urlopen
        try:
            with self.assertRaises(SourceFetchError) as context:
                fetch_source_bytes(entry, None)
        finally:
            common.urllib.request.urlopen = original_urlopen

        message = str(context.exception)
        self.assertIn("$.entries[0].source_repo", message)
        self.assertIn("$.entries[0].source_ref", message)
        self.assertIn("$.entries[0].source_path", message)

    def test_atomic_write_mkdir_failure_is_wrapped_in_manifest_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            parent_file = root / "not-a-directory"
            parent_file.write_text("file", encoding="utf-8")

            with self.assertRaises(ManifestError) as context:
                sync_files.write_file_bytes_atomically(parent_file / "child.txt", b"content")

            self.assertIn("Unable to write target file", str(context.exception))


if __name__ == "__main__":
    unittest.main()
