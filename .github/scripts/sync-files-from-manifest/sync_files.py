from __future__ import annotations

import argparse
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from common import (
    ManifestEntry,
    ManifestError,
    SourceFetchError,
    assert_safe_worktree_file_path,
    emit_output,
    fetch_source_bytes,
    load_normalized_manifest,
    log_error,
    log_info,
    read_file_bytes,
    run_basename_unique_tracked_file_scan,
    target_abspath,
)
from marker_scope import (
    compose_marker_scoped_bytes,
    is_marker_scope,
    text_location,
    validate_source_marker_blocks,
)
from source_glob import expand_source_glob_entry, list_source_tree_files


LIFECYCLE_DISABLED = "disabled"
LIFECYCLE_ENFORCE = "enforce"
LIFECYCLE_SEED_ONCE = "seed_once"
MANAGED_SCOPE_WHOLE_FILE = "whole_file"


@dataclass(frozen=True)
class PlannedWrite:
    entry: ManifestEntry
    target_path: Path
    expected_bytes: bytes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify or sync files from a normalized manifest.")
    parser.add_argument("--mode", choices=("verify", "sync"), required=True)
    parser.add_argument(
        "--normalized-manifest-path",
        required=True,
        help="Path to the normalized manifest produced by validate_manifest.py.",
    )
    parser.add_argument(
        "--repo-root",
        required=True,
        help="Absolute path to the checked-out caller repository.",
    )
    return parser.parse_args()


def is_whole_file_scope(entry: ManifestEntry) -> bool:
    return entry.managed_scope == MANAGED_SCOPE_WHOLE_FILE


def assert_supported_scope(entry: ManifestEntry) -> None:
    if not is_whole_file_scope(entry) and not is_marker_scope(entry):
        raise ManifestError(f"{entry.describe()} uses unsupported managed_scope '{entry.managed_scope}'.")


def first_differing_byte_offset(left: bytes, right: bytes) -> int | None:
    shared_length = min(len(left), len(right))
    for offset in range(shared_length):
        if left[offset] != right[offset]:
            return offset
    if len(left) != len(right):
        return shared_length
    return None


def marker_scoped_byte_location(target_bytes: bytes, byte_offset: int) -> str | None:
    try:
        prefix = target_bytes[:byte_offset].decode(encoding="utf-8", errors="strict")
        text = target_bytes.decode(encoding="utf-8", errors="strict")
    except UnicodeDecodeError:
        return None

    location = text_location(text, len(prefix))
    return f"target line {location.line}, column {location.column}"


def drift_diagnostic(entry: ManifestEntry, target_bytes: bytes, expected_bytes: bytes) -> str:
    byte_offset = first_differing_byte_offset(target_bytes, expected_bytes)
    if byte_offset is None:
        return ""

    details = f" First differing byte offset: {byte_offset}."
    if is_marker_scope(entry):
        text_location_details = marker_scoped_byte_location(target_bytes, byte_offset)
        if text_location_details is not None:
            details += f" First differing target text location: {text_location_details}."
    return details


def verify_enforced_entry(
    entry: ManifestEntry,
    target_path: Path,
    source_token: str | None,
) -> None:
    if not target_path.is_file():
        raise ManifestError(f"{entry.describe()} is missing enforced target '{entry.target_path}'.")

    source_bytes = fetch_source_bytes(entry, source_token)
    target_bytes = read_file_bytes(target_path)
    expected_bytes = (
        source_bytes
        if is_whole_file_scope(entry)
        else compose_marker_scoped_bytes(source_bytes, target_bytes, entry)
    )

    if target_bytes != expected_bytes:
        raise ManifestError(
            f"{entry.describe()} is out of sync with its canonical source. "
            "Merge the sync PR created by this workflow."
            f"{drift_diagnostic(entry, target_bytes, expected_bytes)}"
        )

    log_info(f"Verified target is in sync for {entry.describe()}.")


def expected_sync_bytes(
    entry: ManifestEntry,
    source_bytes: bytes,
    current_bytes: bytes | None,
) -> bytes:
    if is_whole_file_scope(entry):
        return source_bytes

    if current_bytes is None:
        validate_source_marker_blocks(source_bytes, entry)
        return source_bytes

    return compose_marker_scoped_bytes(source_bytes, current_bytes, entry)


def verify_entries(repo_root: Path, normalized_manifest_path: Path, source_token: str | None) -> None:
    entries = expand_entries_for_execution(load_normalized_manifest(normalized_manifest_path), repo_root, source_token)

    for entry in entries:
        log_info(f"Verifying {entry.describe()}.")
        assert_supported_scope(entry)

        target_path = target_abspath(repo_root, entry.target_path)
        assert_safe_worktree_file_path(repo_root, target_path, entry.target_path, entry.describe())

        if entry.lifecycle_policy == LIFECYCLE_DISABLED:
            log_info(f"Skipping {entry.describe()} because lifecycle_policy is disabled.")
            continue

        if entry.lifecycle_policy == LIFECYCLE_SEED_ONCE:
            if not target_path.is_file():
                raise ManifestError(
                    f"{entry.describe()} is missing required seed_once target '{entry.target_path}'."
                )
            log_info(f"Verified seed_once target exists for {entry.describe()}.")
            continue

        if entry.lifecycle_policy != LIFECYCLE_ENFORCE:
            raise ManifestError(f"{entry.describe()} uses unsupported lifecycle policy '{entry.lifecycle_policy}'.")

        verify_enforced_entry(entry, target_path, source_token)


def build_pr_body(changed_entries: list[ManifestEntry]) -> str:
    lines = [
        "Automated sync of manifest-managed files.",
        "",
        "Changed files:",
    ]
    lines.extend(
        f"- `{entry.target_path}` <- `{entry.source_repo}@{entry.source_ref}:{entry.source_path}`"
        for entry in changed_entries
    )
    lines.extend(
        [
            "",
            "This PR was generated by `.github/workflows/sync-files-from-manifest.yml`.",
        ]
    )
    return "\n".join(lines)


def plan_sync_entry(repo_root: Path, entry: ManifestEntry, source_token: str | None) -> PlannedWrite | None:
    log_info(f"Planning synchronization for {entry.describe()}.")
    assert_supported_scope(entry)

    target_path = target_abspath(repo_root, entry.target_path)
    assert_safe_worktree_file_path(repo_root, target_path, entry.target_path, entry.describe())

    if entry.lifecycle_policy == LIFECYCLE_DISABLED:
        log_info(f"Skipping {entry.describe()} because lifecycle_policy is disabled.")
        return None

    if entry.lifecycle_policy == LIFECYCLE_SEED_ONCE and target_path.is_file():
        log_info(f"Leaving existing seed_once target unchanged for {entry.describe()}.")
        return None

    if entry.lifecycle_policy not in {LIFECYCLE_ENFORCE, LIFECYCLE_SEED_ONCE}:
        raise ManifestError(f"{entry.describe()} uses unsupported lifecycle policy '{entry.lifecycle_policy}'.")

    source_bytes = fetch_source_bytes(entry, source_token)
    current_bytes = read_file_bytes(target_path) if target_path.is_file() else None
    expected_bytes = expected_sync_bytes(entry, source_bytes, current_bytes)

    if current_bytes == expected_bytes:
        log_info(f"Target already matches canonical source for {entry.describe()}.")
        return None

    return PlannedWrite(entry=entry, target_path=target_path, expected_bytes=expected_bytes)


def expand_entries_for_execution(
    entries: list[ManifestEntry],
    repo_root: Path,
    source_token: str | None,
) -> list[ManifestEntry]:
    expanded_entries: list[ManifestEntry] = []
    for entry in entries:
        assert_supported_scope(entry)

        if entry.lifecycle_policy == LIFECYCLE_DISABLED:
            log_info(f"Skipping {entry.describe()} because lifecycle_policy is disabled.")
            continue

        if entry.is_glob_entry:
            log_info(f"Expanding {entry.describe()}.")
            source_paths = list_source_tree_files(entry, source_token)
            expanded_entries.extend(expand_source_glob_entry(entry, source_paths))
        else:
            expanded_entries.append(entry)

    validate_expanded_entries(expanded_entries, repo_root)
    return expanded_entries


def validate_expanded_entries(entries: list[ManifestEntry], repo_root: Path) -> None:
    seen_sources: dict[tuple[str, str, str], ManifestEntry] = {}
    seen_targets: dict[str, ManifestEntry] = {}

    for entry in entries:
        if entry.source_path is None:
            raise ManifestError(f"{entry.describe()} must be expanded to an exact source_path before execution.")

        existing_source = seen_sources.get(entry.source_identity_key)
        if existing_source is not None:
            raise ManifestError(
                f"{entry.describe()} duplicates generated source identity already produced by "
                f"{existing_source.describe()}."
            )
        seen_sources[entry.source_identity_key] = entry

        existing_target = seen_targets.get(entry.target_identity_key)
        if existing_target is not None:
            raise ManifestError(
                f"Duplicate computed effective target '{entry.target_path}' from {entry.describe()} and "
                f"{existing_target.describe()}."
            )
        seen_targets[entry.target_identity_key] = entry

        if PurePosixPath(entry.source_path).name != PurePosixPath(entry.target_path).name:
            raise ManifestError(
                f"{entry.describe()} has a basename mismatch between expanded source_path "
                f"'{entry.source_path}' and expanded target_path '{entry.target_path}'."
            )

    run_basename_unique_tracked_file_scan(
        entries,
        {
            "when": {
                "property": "uniqueness_policy",
                "equals": "basename_unique",
            }
        },
        repo_root,
    )


def write_file_bytes_atomically(path: Path, content: bytes) -> None:
    temp_path: Path | None = None

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="wb",
            delete=False,
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
        ) as handle:
            temp_path = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())

        os.replace(temp_path, path)
        temp_path = None
    except OSError as exc:
        raise ManifestError(f"Unable to write target file '{path}': {exc}.") from exc
    finally:
        if temp_path is not None:
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass


def commit_planned_writes(planned_writes: list[PlannedWrite]) -> None:
    for planned_write in planned_writes:
        write_file_bytes_atomically(planned_write.target_path, planned_write.expected_bytes)
        log_info(f"Updated target '{planned_write.entry.target_path}' for {planned_write.entry.describe()}.")


def sync_entries(repo_root: Path, normalized_manifest_path: Path, source_token: str | None) -> None:
    entries = expand_entries_for_execution(load_normalized_manifest(normalized_manifest_path), repo_root, source_token)
    planned_writes: list[PlannedWrite] = []

    for entry in entries:
        planned_write = plan_sync_entry(repo_root, entry, source_token)
        if planned_write is not None:
            planned_writes.append(planned_write)

    commit_planned_writes(planned_writes)

    changed_entries = [planned_write.entry for planned_write in planned_writes]
    changed_paths = [planned_write.entry.target_path for planned_write in planned_writes]

    emit_output("changed", "true" if changed_paths else "false")
    emit_output("changed_count", str(len(changed_paths)))
    emit_output("changed_paths", "\n".join(changed_paths))
    emit_output(
        "pull_request_body",
        build_pr_body(changed_entries) if changed_entries else "Automated sync found no file changes.",
    )


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    normalized_manifest_path = Path(args.normalized_manifest_path).resolve()
    source_token = os.getenv("SOURCE_TOKEN") or None

    if args.mode == "verify":
        verify_entries(repo_root, normalized_manifest_path, source_token)
    else:
        sync_entries(repo_root, normalized_manifest_path, source_token)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ManifestError, SourceFetchError) as exc:
        log_error(str(exc))
        raise SystemExit(1) from exc
    except Exception as exc:  # pragma: no cover - defensive guard for workflow logs
        log_error(f"Unexpected sync execution failure: {exc}")
        raise SystemExit(1) from exc
