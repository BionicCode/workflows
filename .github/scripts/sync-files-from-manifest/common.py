from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from enum import Enum
from pathlib import Path, PurePosixPath
from typing import Any


GITHUB_API_VERSION = "2022-11-28"
RECOGNIZED_UNSUPPORTED_DIRECTIONS = {"target_to_source", "two_way"}


class ManifestError(Exception):
    """Raised when the manifest or repository policy validation fails."""


class SourceFetchError(Exception):
    """Raised when a source file cannot be fetched from GitHub."""


class Direction(str, Enum):
    SOURCE_TO_TARGET = "source_to_target"


class LifecyclePolicy(str, Enum):
    ENFORCE = "enforce"
    SEED_ONCE = "seed_once"
    DISABLED = "disabled"


class UniquenessPolicy(str, Enum):
    BASENAME_UNIQUE = "basename_unique"
    NONE = "none"


class ManagedScope(str, Enum):
    WHOLE_FILE = "whole_file"
    OUTSIDE_MARKERS = "outside_markers"
    INSIDE_MARKERS = "inside_markers"


@dataclass(frozen=True)
class Markers:
    start: str
    end: str


@dataclass(frozen=True)
class ManifestEntry:
    index: int
    source_repo: str
    source_ref: str
    source_path: str
    target_path: str
    direction: Direction
    lifecycle_policy: LifecyclePolicy
    uniqueness_policy: UniquenessPolicy
    managed_scope: ManagedScope
    markers: Markers | None = None

    @property
    def basename(self) -> str:
        return PurePosixPath(self.target_path).name

    @property
    def source_identity_key(self) -> tuple[str, str, str]:
        return (self.source_repo, self.source_ref, self.source_path)

    @property
    def target_identity_key(self) -> str:
        return self.target_path

    def describe(self) -> str:
        return (
            f"manifest entry {self.index} "
            f"({self.source_repo}@{self.source_ref}:{self.source_path} -> {self.target_path}; "
            f"lifecycle={self.lifecycle_policy.value}, "
            f"uniqueness={self.uniqueness_policy.value}, "
            f"scope={self.managed_scope.value})"
        )

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "index": self.index,
            "source_repo": self.source_repo,
            "source_ref": self.source_ref,
            "source_path": self.source_path,
            "target_path": self.target_path,
            "direction": self.direction.value,
            "lifecycle_policy": self.lifecycle_policy.value,
            "uniqueness_policy": self.uniqueness_policy.value,
            "managed_scope": self.managed_scope.value,
        }
        if self.markers is not None:
            data["markers"] = {"start": self.markers.start, "end": self.markers.end}
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ManifestEntry":
        markers = data.get("markers")
        marker_value = None
        if markers is not None:
            marker_value = Markers(start=markers["start"], end=markers["end"])

        return cls(
            index=int(data["index"]),
            source_repo=str(data["source_repo"]),
            source_ref=str(data["source_ref"]),
            source_path=str(data["source_path"]),
            target_path=str(data["target_path"]),
            direction=Direction(str(data["direction"])),
            lifecycle_policy=LifecyclePolicy(str(data["lifecycle_policy"])),
            uniqueness_policy=UniquenessPolicy(str(data["uniqueness_policy"])),
            managed_scope=ManagedScope(str(data["managed_scope"])),
            markers=marker_value,
        )


def log_info(message: str) -> None:
    print(message)


def log_error(message: str) -> None:
    print(f"::error::{message}", file=sys.stderr)


def emit_output(name: str, value: str) -> None:
    output_path = os.getenv("GITHUB_OUTPUT")
    if not output_path:
        return

    delimiter = "__SYNC_FILES_FROM_MANIFEST__"
    with open(output_path, "a", encoding="utf-8") as handle:
        if "\n" in value:
            handle.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")
        else:
            handle.write(f"{name}={value}\n")


def require_string(value: Any, field_name: str, index: int) -> str:
    if not isinstance(value, str):
        raise ManifestError(f"Manifest entry {index}: '{field_name}' must be a string.")

    result = value.strip()
    if not result:
        raise ManifestError(f"Manifest entry {index}: '{field_name}' must not be empty.")

    return result


def normalize_source_repo(value: Any, index: int) -> str:
    repo = require_string(value, "source_repo", index)
    parts = repo.split("/")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ManifestError(
            f"Manifest entry {index}: 'source_repo' must use the 'owner/repository' format."
        )

    if any(any(char.isspace() for char in part) for part in parts):
        raise ManifestError(
            f"Manifest entry {index}: 'source_repo' must not contain whitespace."
        )

    return f"{parts[0].lower()}/{parts[1].lower()}"


def normalize_source_ref(value: Any, index: int) -> str:
    return require_string(value, "source_ref", index)


def normalize_repo_relative_path(value: Any, field_name: str, index: int) -> str:
    path_value = require_string(value, field_name, index)
    if "\\" in path_value:
        raise ManifestError(
            f"Manifest entry {index}: '{field_name}' must use forward slashes."
        )
    if path_value.startswith("/"):
        raise ManifestError(
            f"Manifest entry {index}: '{field_name}' must be repository-relative, not absolute."
        )
    if path_value.endswith("/"):
        raise ManifestError(
            f"Manifest entry {index}: '{field_name}' must point to a file path, not a directory."
        )

    segments = path_value.split("/")
    if any(segment == "" for segment in segments):
        raise ManifestError(
            f"Manifest entry {index}: '{field_name}' must not contain empty path segments."
        )
    if any(segment in {".", ".."} for segment in segments):
        raise ManifestError(
            f"Manifest entry {index}: '{field_name}' must not contain '.' or '..' path segments."
        )

    normalized = PurePosixPath(path_value).as_posix()
    if normalized in {"", "."} or PurePosixPath(normalized).name in {"", ".", ".."}:
        raise ManifestError(
            f"Manifest entry {index}: '{field_name}' must point to a file path."
        )

    return normalized


def parse_direction(value: Any, index: int) -> Direction:
    direction = require_string(value, "direction", index)
    if direction in RECOGNIZED_UNSUPPORTED_DIRECTIONS:
        raise ManifestError(
            f"Manifest entry {index}: direction '{direction}' is intentionally unsupported in v1."
        )

    try:
        return Direction(direction)
    except ValueError as exc:
        raise ManifestError(
            f"Manifest entry {index}: unsupported direction '{direction}'."
        ) from exc


def parse_lifecycle_policy(value: Any, index: int) -> LifecyclePolicy:
    lifecycle_policy = require_string(value, "lifecycle_policy", index)
    try:
        return LifecyclePolicy(lifecycle_policy)
    except ValueError as exc:
        raise ManifestError(
            f"Manifest entry {index}: unsupported lifecycle_policy '{lifecycle_policy}'."
        ) from exc


def parse_uniqueness_policy(value: Any, index: int) -> UniquenessPolicy:
    uniqueness_policy = require_string(value, "uniqueness_policy", index)
    try:
        return UniquenessPolicy(uniqueness_policy)
    except ValueError as exc:
        raise ManifestError(
            f"Manifest entry {index}: unsupported uniqueness_policy '{uniqueness_policy}'."
        ) from exc


def parse_managed_scope(value: Any, index: int) -> ManagedScope:
    managed_scope = require_string(value, "managed_scope", index)
    try:
        return ManagedScope(managed_scope)
    except ValueError as exc:
        raise ManifestError(
            f"Manifest entry {index}: unsupported managed_scope '{managed_scope}'."
        ) from exc


def parse_markers(raw_entry: dict[str, Any], managed_scope: ManagedScope, index: int) -> Markers | None:
    has_markers = "markers" in raw_entry
    raw_markers = raw_entry.get("markers")

    if managed_scope is ManagedScope.WHOLE_FILE:
        if has_markers:
            raise ManifestError(
                f"Manifest entry {index}: markers must not be provided when managed_scope is 'whole_file'."
            )
        return None

    if not has_markers or not isinstance(raw_markers, dict):
        raise ManifestError(
            f"Manifest entry {index}: markers.start and markers.end are required when managed_scope is '{managed_scope.value}'."
        )

    start = require_string(raw_markers.get("start"), "markers.start", index)
    end = require_string(raw_markers.get("end"), "markers.end", index)

    if start == end:
        raise ManifestError(
            f"Manifest entry {index}: markers.start and markers.end must not be identical."
        )

    return Markers(start=start, end=end)


def parse_manifest_json(manifest_json: str) -> list[Any]:
    try:
        parsed = json.loads(manifest_json)
    except json.JSONDecodeError as exc:
        raise ManifestError(f"Manifest JSON is invalid: {exc.msg} at line {exc.lineno}, column {exc.colno}.") from exc

    if not isinstance(parsed, list) or not parsed:
        raise ManifestError("Manifest JSON must be a non-empty array of manifest entries.")

    return parsed


def normalize_manifest(manifest_json: str, repo_root: Path) -> list[ManifestEntry]:
    raw_entries = parse_manifest_json(manifest_json)
    entries: list[ManifestEntry] = []

    source_identities: dict[tuple[str, str, str], int] = {}
    target_paths: dict[str, int] = {}

    for raw_index, raw_entry in enumerate(raw_entries, start=1):
        if not isinstance(raw_entry, dict):
            raise ManifestError(f"Manifest entry {raw_index}: each manifest entry must be a JSON object.")

        source_repo = normalize_source_repo(raw_entry.get("source_repo"), raw_index)
        source_ref = normalize_source_ref(raw_entry.get("source_ref"), raw_index)
        source_path = normalize_repo_relative_path(raw_entry.get("source_path"), "source_path", raw_index)
        target_path = normalize_repo_relative_path(raw_entry.get("target_path"), "target_path", raw_index)
        direction = parse_direction(raw_entry.get("direction"), raw_index)
        lifecycle_policy = parse_lifecycle_policy(raw_entry.get("lifecycle_policy"), raw_index)
        uniqueness_policy = parse_uniqueness_policy(raw_entry.get("uniqueness_policy"), raw_index)
        managed_scope = parse_managed_scope(raw_entry.get("managed_scope"), raw_index)
        markers = parse_markers(raw_entry, managed_scope, raw_index)

        if PurePosixPath(source_path).name != PurePosixPath(target_path).name:
            raise ManifestError(
                f"Manifest entry {raw_index}: basename mismatch between source_path '{source_path}' and target_path '{target_path}'."
            )

        entry = ManifestEntry(
            index=raw_index,
            source_repo=source_repo,
            source_ref=source_ref,
            source_path=source_path,
            target_path=target_path,
            direction=direction,
            lifecycle_policy=lifecycle_policy,
            uniqueness_policy=uniqueness_policy,
            managed_scope=managed_scope,
            markers=markers,
        )

        existing_source = source_identities.get(entry.source_identity_key)
        if existing_source is not None:
            raise ManifestError(
                f"{entry.describe()} duplicates source identity already declared by manifest entry {existing_source}."
            )
        source_identities[entry.source_identity_key] = entry.index

        existing_target = target_paths.get(entry.target_identity_key)
        if existing_target is not None:
            raise ManifestError(
                f"{entry.describe()} duplicates target_path already declared by manifest entry {existing_target}."
            )
        target_paths[entry.target_identity_key] = entry.index

        entries.append(entry)

    validate_stage1_policy_support(entries)
    validate_uniqueness_policies(entries, repo_root)
    return entries


def validate_stage1_policy_support(entries: list[ManifestEntry]) -> None:
    for entry in entries:
        if entry.managed_scope is not ManagedScope.WHOLE_FILE:
            raise ManifestError(
                f"{entry.describe()} is recognized by the manifest schema but not yet supported in execution for v1."
            )


def load_tracked_files(repo_root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ManifestError(
            f"Failed to inspect tracked files in '{repo_root}': {exc}."
        ) from exc

    output = result.stdout.decode("utf-8", errors="strict")
    return [item for item in output.split("\0") if item]


def validate_uniqueness_policies(entries: list[ManifestEntry], repo_root: Path) -> None:
    tracked_files = load_tracked_files(repo_root)
    target_paths = {entry.target_path: entry for entry in entries}

    for entry in entries:
        if entry.uniqueness_policy is not UniquenessPolicy.BASENAME_UNIQUE:
            continue

        conflicting_manifest_targets = sorted(
            other.target_path
            for other in entries
            if other.target_path != entry.target_path and other.basename == entry.basename
        )
        if conflicting_manifest_targets:
            conflicts = ", ".join(conflicting_manifest_targets)
            raise ManifestError(
                f"{entry.describe()} declares uniqueness_policy 'basename_unique', but other manifest targets share basename '{entry.basename}': {conflicts}."
            )

        conflicting_tracked_paths = sorted(
            tracked_path
            for tracked_path in tracked_files
            if tracked_path != entry.target_path
            and PurePosixPath(tracked_path).name == entry.basename
            and tracked_path not in target_paths
        )
        if conflicting_tracked_paths:
            conflicts = ", ".join(conflicting_tracked_paths)
            raise ManifestError(
                f"{entry.describe()} declares uniqueness_policy 'basename_unique', but tracked repository files already share basename '{entry.basename}': {conflicts}."
            )


def write_normalized_manifest(entries: list[ManifestEntry], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump([entry.to_dict() for entry in entries], handle, indent=2)
        handle.write("\n")


def load_normalized_manifest(path: Path) -> list[ManifestEntry]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ManifestError(f"Normalized manifest file '{path}' must contain a JSON array.")

    return [ManifestEntry.from_dict(item) for item in data]


def target_abspath(repo_root: Path, target_path: str) -> Path:
    return repo_root.joinpath(*PurePosixPath(target_path).parts)


def ensure_parent_directory(target_path: Path) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)


def fetch_source_bytes(entry: ManifestEntry, source_token: str | None) -> bytes:
    encoded_path = urllib.parse.quote(entry.source_path, safe="")
    encoded_ref = urllib.parse.quote(entry.source_ref, safe="")
    url = f"https://api.github.com/repos/{entry.source_repo}/contents/{encoded_path}?ref={encoded_ref}"

    headers = {
        "Accept": "application/vnd.github.raw",
        "User-Agent": "sync-files-from-manifest",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
    }
    if source_token:
        headers["Authorization"] = f"Bearer {source_token}"

    request = urllib.request.Request(url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(request) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        message = (
            f"Unable to fetch source for {entry.describe()} (HTTP {exc.code}). "
            "If the source repository is private, provide the optional read-only source_token secret. "
            "Otherwise verify source_repo, source_ref, and source_path."
        )
        raise SourceFetchError(message) from exc
    except urllib.error.URLError as exc:
        raise SourceFetchError(
            f"Unable to fetch source for {entry.describe()}: {exc.reason}."
        ) from exc


def read_file_bytes(path: Path) -> bytes:
    return path.read_bytes()


def write_file_bytes(path: Path, content: bytes) -> None:
    ensure_parent_directory(path)
    path.write_bytes(content)

