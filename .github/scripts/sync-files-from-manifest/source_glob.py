from __future__ import annotations

import fnmatch
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import PurePosixPath

from common import (
    FIELD_SOURCE_GLOB,
    GITHUB_API_VERSION,
    SOURCE_FETCH_TIMEOUT_SECONDS,
    GlobOptions,
    ManifestEntry,
    ManifestError,
    SourceFetchError,
    contains_glob_metacharacter,
    manifest_entry_path,
    normalize_repo_relative_file_path,
)


def split_posix_path(value: str) -> list[str]:
    return value.split("/") if value else []


def source_glob_base_directory(pattern: str) -> str:
    base_segments: list[str] = []
    for segment in split_posix_path(pattern):
        if contains_glob_metacharacter(segment):
            break
        base_segments.append(segment)

    return f"{'/'.join(base_segments)}/" if base_segments else ""


def segment_matches(pattern_segment: str, path_segment: str, include_hidden: bool) -> bool:
    if path_segment.startswith(".") and not include_hidden and not pattern_segment.startswith("."):
        return False
    return fnmatch.fnmatchcase(path_segment, pattern_segment)


def path_matches_glob(pattern: str, source_path: str, options: GlobOptions) -> bool:
    pattern_segments = split_posix_path(pattern)
    path_segments = split_posix_path(source_path)

    def match_from(pattern_index: int, path_index: int) -> bool:
        if pattern_index == len(pattern_segments):
            return path_index == len(path_segments)

        pattern_segment = pattern_segments[pattern_index]
        if pattern_segment == "**":
            if match_from(pattern_index + 1, path_index):
                return True
            if path_index >= len(path_segments):
                return False
            if path_segments[path_index].startswith(".") and not options.include_hidden:
                return False
            return match_from(pattern_index, path_index + 1)

        if path_index >= len(path_segments):
            return False
        if not segment_matches(pattern_segment, path_segments[path_index], options.include_hidden):
            return False
        return match_from(pattern_index + 1, path_index + 1)

    return match_from(0, 0)


def list_source_tree_files(entry: ManifestEntry, source_token: str | None) -> list[str]:
    encoded_ref = urllib.parse.quote(entry.source_ref, safe="")
    url = f"https://api.github.com/repos/{entry.source_repo}/git/trees/{encoded_ref}?recursive=1"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "sync-files-from-manifest",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
    }
    if source_token:
        headers["Authorization"] = f"Bearer {source_token}"

    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=SOURCE_FETCH_TIMEOUT_SECONDS) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise SourceFetchError(
            f"Unable to enumerate source tree for {entry.describe()} (HTTP {exc.code}). "
            "If the source repository is private, provide the optional read-only source_token secret. "
            f"Source field locations: {manifest_entry_path(entry.index, 'source_repo')}, "
            f"{manifest_entry_path(entry.index, 'source_ref')}, "
            f"{manifest_entry_path(entry.index, FIELD_SOURCE_GLOB)}."
        ) from exc
    except urllib.error.URLError as exc:
        raise SourceFetchError(
            f"Unable to enumerate source tree for {entry.describe()}: {exc.reason}. "
            f"Source field locations: {manifest_entry_path(entry.index, 'source_repo')}, "
            f"{manifest_entry_path(entry.index, 'source_ref')}, "
            f"{manifest_entry_path(entry.index, FIELD_SOURCE_GLOB)}."
        ) from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SourceFetchError(f"Unable to parse source tree response for {entry.describe()}: {exc}.") from exc

    if payload.get("truncated") is True:
        raise SourceFetchError(
            f"Manifest entry {entry.index} source_glob '{entry.source_glob}' source tree listing was truncated; "
            "refusing partial sync."
        )

    tree = payload.get("tree")
    if not isinstance(tree, list):
        raise SourceFetchError(f"Source tree response for {entry.describe()} did not contain a tree array.")

    paths: list[str] = []
    for item in tree:
        if not isinstance(item, dict) or item.get("type") != "blob" or item.get("mode") == "120000":
            continue
        raw_path = item.get("path")
        if not isinstance(raw_path, str):
            continue
        try:
            paths.append(normalize_repo_relative_file_path(raw_path, "source tree path", entry.index))
        except ManifestError as exc:
            raise SourceFetchError(f"Source tree response for {entry.describe()} included unsafe path: {exc}") from exc

    return sorted(paths)


def expand_source_glob_entry(
    entry: ManifestEntry,
    source_paths: list[str],
) -> list[ManifestEntry]:
    if entry.source_glob is None:
        return [entry]

    options = entry.glob or GlobOptions()
    base_directory = source_glob_base_directory(entry.source_glob)
    matched_paths = sorted(
        source_path
        for source_path in source_paths
        if path_matches_glob(entry.source_glob, source_path, options)
    )

    if not matched_paths:
        raise ManifestError(f"Manifest entry {entry.index} source_glob '{entry.source_glob}' matched no source files.")

    expanded_entries: list[ManifestEntry] = []
    for expanded_index, source_path in enumerate(matched_paths, start=1):
        if base_directory:
            if not source_path.startswith(base_directory):
                continue
            relative_source_path = source_path[len(base_directory) :]
        else:
            relative_source_path = source_path

        if not relative_source_path:
            continue

        target_path = PurePosixPath(entry.target_path, relative_source_path).as_posix()
        expanded_entries.append(
            ManifestEntry(
                index=entry.index,
                source_repo=entry.source_repo,
                source_ref=entry.source_ref,
                source_path=source_path,
                target_path=target_path,
                direction=entry.direction,
                lifecycle_policy=entry.lifecycle_policy,
                uniqueness_policy=entry.uniqueness_policy,
                managed_scope=entry.managed_scope,
                markers=entry.markers,
                manifest_properties=dict(entry.manifest_properties or {}),
                expanded_file_index=expanded_index,
                parent_source_glob=entry.source_glob,
            )
        )

    return expanded_entries
