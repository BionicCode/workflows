from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any
from uuid import uuid4

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


GITHUB_API_VERSION = "2022-11-28"
SOURCE_FETCH_TIMEOUT_SECONDS = 30
RESERVED_TARGET_PATH_PREFIXES = ("_sync-files-from-manifest-workflow/",)


class ManifestError(Exception):
    """Raised when the manifest or repository policy validation fails."""


class SourceFetchError(Exception):
    """Raised when a source file cannot be fetched from GitHub."""


def manifest_entry_path(index: int, field: str | None = None) -> str:
    path = f"$.entries[{index}]"
    if field:
        path += "".join(f".{part}" for part in field.split("."))
    return path


@dataclass(frozen=True)
class ManifestMetadata:
    entries_property: str
    schema_version_property: str
    fields: dict[str, str]

    def field(self, role: str) -> str:
        try:
            return self.fields[role]
        except KeyError as exc:
            raise ManifestError(
                f"Schema metadata is missing required field role '{role}'."
            ) from exc


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
    direction: str
    lifecycle_policy: str
    uniqueness_policy: str
    managed_scope: str
    markers: Markers | None = None
    manifest_properties: dict[str, Any] | None = None

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
            f"lifecycle={self.lifecycle_policy}, "
            f"uniqueness={self.uniqueness_policy}, "
            f"scope={self.managed_scope})"
        )

    def manifest_value(self, property_name: str) -> Any:
        properties = self.manifest_properties or {}
        return properties.get(property_name)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "index": self.index,
            "source_repo": self.source_repo,
            "source_ref": self.source_ref,
            "source_path": self.source_path,
            "target_path": self.target_path,
            "direction": self.direction,
            "lifecycle_policy": self.lifecycle_policy,
            "uniqueness_policy": self.uniqueness_policy,
            "managed_scope": self.managed_scope,
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
            direction=str(data["direction"]),
            lifecycle_policy=str(data["lifecycle_policy"]),
            uniqueness_policy=str(data["uniqueness_policy"]),
            managed_scope=str(data["managed_scope"]),
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

    delimiter = f"__SYNC_FILES_FROM_MANIFEST_{uuid4().hex}__"
    with open(output_path, "a", encoding="utf-8") as handle:
        if "\n" in value:
            handle.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")
        else:
            handle.write(f"{name}={value}\n")


def script_root() -> Path:
    return Path(__file__).resolve().parent


def default_schema_path() -> Path:
    return script_root() / "schema" / "sync-manifest.schema.json"


def default_rules_path() -> Path:
    return script_root() / "schema" / "sync-rules.json"


def default_template_path() -> Path:
    return script_root() / "templates" / "sync-manifest.template.json"


def default_documentation_path() -> Path:
    return script_root() / "documentation"


def load_json_file(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise ManifestError(
            f"JSON file '{path}' is invalid: {exc.msg} at line {exc.lineno}, column {exc.colno}."
        ) from exc


def load_schema(schema_path: Path) -> dict[str, Any]:
    schema = load_json_file(schema_path)
    if not isinstance(schema, dict):
        raise ManifestError(f"Schema file '{schema_path}' must contain a JSON object.")

    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        raise ManifestError(f"Schema file '{schema_path}' is not a valid Draft 2020-12 schema: {exc}.") from exc

    return schema


def load_rules(rules_path: Path) -> dict[str, Any]:
    rules = load_json_file(rules_path)
    if not isinstance(rules, dict) or not isinstance(rules.get("rules"), list):
        raise ManifestError(f"Rules file '{rules_path}' must contain a JSON object with a rules array.")
    return rules


def load_manifest_metadata(schema: dict[str, Any]) -> ManifestMetadata:
    metadata = schema.get("x-sync-files-from-manifest")
    if not isinstance(metadata, dict):
        raise ManifestError("Schema is missing x-sync-files-from-manifest metadata.")

    manifest_shape = metadata.get("manifest_shape")
    fields = metadata.get("entry_fields")
    if not isinstance(manifest_shape, dict) or not isinstance(fields, dict):
        raise ManifestError(
            "Schema x-sync-files-from-manifest metadata must define manifest_shape and entry_fields."
        )

    entries_property = manifest_shape.get("entries_property")
    schema_version_property = manifest_shape.get("schema_version_property")
    if not isinstance(entries_property, str) or not entries_property:
        raise ManifestError("Schema metadata must define manifest_shape.entries_property.")
    if not isinstance(schema_version_property, str) or not schema_version_property:
        raise ManifestError("Schema metadata must define manifest_shape.schema_version_property.")

    normalized_fields: dict[str, str] = {}
    for role, field_name in fields.items():
        if not isinstance(role, str) or not isinstance(field_name, str) or not field_name:
            raise ManifestError("Schema entry_fields metadata must map string roles to string property names.")
        normalized_fields[role] = field_name

    return ManifestMetadata(
        entries_property=entries_property,
        schema_version_property=schema_version_property,
        fields=normalized_fields,
    )


def parse_manifest_document(manifest_json: str) -> Any:
    try:
        parsed = json.loads(manifest_json)
    except json.JSONDecodeError as exc:
        raise ManifestError(
            f"Manifest JSON is invalid: {exc.msg} at line {exc.lineno}, column {exc.colno}."
        ) from exc

    if isinstance(parsed, list):
        raise ManifestError(
            "Manifest JSON uses the old top-level array shape. "
            "Wrap the array under an 'entries' property and add 'schema_version': 1."
        )

    return parsed


def format_schema_error(error: ValidationError) -> str:
    location = "$"
    if error.absolute_path:
        location += "".join(
            f"[{item}]" if isinstance(item, int) else f".{item}"
            for item in error.absolute_path
        )
    return f"Manifest schema validation failed at {location}: {error.message}"


def validate_manifest_schema(manifest_document: Any, schema: dict[str, Any]) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(manifest_document), key=lambda item: list(item.absolute_path))
    if errors:
        raise ManifestError(format_schema_error(errors[0]))


def require_string_property(raw_entry: dict[str, Any], field_name: str, index: int) -> str:
    value = raw_entry.get(field_name)
    if not isinstance(value, str):
        raise ManifestError(
            f"Manifest entry {index}: '{field_name}' must be a string at {manifest_entry_path(index, field_name)}."
        )

    result = value.strip()
    if not result:
        raise ManifestError(
            f"Manifest entry {index}: '{field_name}' must not be empty at {manifest_entry_path(index, field_name)}."
        )

    return result


def normalize_source_repo(value: str, index: int, field_name: str = "source_repo") -> str:
    parts = value.split("/")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ManifestError(
            f"Manifest entry {index}: source repository must use the 'owner/repository' format "
            f"at {manifest_entry_path(index, field_name)}."
        )

    if any(any(char.isspace() for char in part) for part in parts):
        raise ManifestError(
            f"Manifest entry {index}: source repository must not contain whitespace "
            f"at {manifest_entry_path(index, field_name)}."
        )

    return f"{parts[0].lower()}/{parts[1].lower()}"


def normalize_repo_relative_path(value: str, field_name: str, index: int) -> str:
    if "\\" in value:
        raise ManifestError(
            f"Manifest entry {index}: '{field_name}' must use forward slashes "
            f"at {manifest_entry_path(index, field_name)}."
        )
    if value.startswith("/"):
        raise ManifestError(
            f"Manifest entry {index}: '{field_name}' must be repository-relative, not absolute "
            f"at {manifest_entry_path(index, field_name)}."
        )
    if value.endswith("/"):
        raise ManifestError(
            f"Manifest entry {index}: '{field_name}' must point to a file path, not a directory "
            f"at {manifest_entry_path(index, field_name)}."
        )

    segments = value.split("/")
    if any(segment == "" for segment in segments):
        raise ManifestError(
            f"Manifest entry {index}: '{field_name}' must not contain empty path segments "
            f"at {manifest_entry_path(index, field_name)}."
        )
    if any(segment in {".", ".."} for segment in segments):
        raise ManifestError(
            f"Manifest entry {index}: '{field_name}' must not contain '.' or '..' path segments "
            f"at {manifest_entry_path(index, field_name)}."
        )

    normalized = PurePosixPath(value).as_posix()
    if normalized in {"", "."} or PurePosixPath(normalized).name in {"", ".", ".."}:
        raise ManifestError(
            f"Manifest entry {index}: '{field_name}' must point to a file path "
            f"at {manifest_entry_path(index, field_name)}."
        )

    return normalized


def parse_markers(raw_entry: dict[str, Any], metadata: ManifestMetadata, index: int) -> Markers | None:
    markers_field = metadata.field("markers")
    marker_start_field = metadata.field("marker_start")
    marker_end_field = metadata.field("marker_end")
    raw_markers = raw_entry.get(markers_field)
    if raw_markers is None:
        return None
    if not isinstance(raw_markers, dict):
        raise ManifestError(
            f"Manifest entry {index}: '{markers_field}' must be an object "
            f"at {manifest_entry_path(index, markers_field)}."
        )

    start = raw_markers.get(marker_start_field)
    end = raw_markers.get(marker_end_field)
    if not isinstance(start, str) or not start.strip():
        raise ManifestError(
            f"Manifest entry {index}: '{markers_field}.{marker_start_field}' must not be empty "
            f"at {manifest_entry_path(index, f'{markers_field}.{marker_start_field}')}."
        )
    if not isinstance(end, str) or not end.strip():
        raise ManifestError(
            f"Manifest entry {index}: '{markers_field}.{marker_end_field}' must not be empty "
            f"at {manifest_entry_path(index, f'{markers_field}.{marker_end_field}')}."
        )
    if start == end:
        raise ManifestError(
            f"Manifest entry {index}: marker start and marker end must not be identical "
            f"at {manifest_entry_path(index, markers_field)}."
        )

    return Markers(start=start, end=end)


def build_entries(manifest_document: dict[str, Any], metadata: ManifestMetadata) -> list[ManifestEntry]:
    raw_entries = manifest_document.get(metadata.entries_property)
    if not isinstance(raw_entries, list):
        raise ManifestError(f"Manifest must contain an array property '{metadata.entries_property}'.")

    entries: list[ManifestEntry] = []
    fields = metadata.fields
    for raw_index, raw_entry in enumerate(raw_entries, start=1):
        if not isinstance(raw_entry, dict):
            raise ManifestError(
                f"Manifest entry {raw_index}: each entry must be a JSON object at {manifest_entry_path(raw_index)}."
            )

        source_repo = normalize_source_repo(
            require_string_property(raw_entry, fields["source_repo"], raw_index),
            raw_index,
            fields["source_repo"],
        )
        source_ref = require_string_property(raw_entry, fields["source_ref"], raw_index)
        source_path = normalize_repo_relative_path(
            require_string_property(raw_entry, fields["source_path"], raw_index),
            fields["source_path"],
            raw_index,
        )
        target_path = normalize_repo_relative_path(
            require_string_property(raw_entry, fields["target_path"], raw_index),
            fields["target_path"],
            raw_index,
        )

        manifest_properties = dict(raw_entry)
        manifest_properties[fields["source_repo"]] = source_repo
        manifest_properties[fields["source_path"]] = source_path
        manifest_properties[fields["target_path"]] = target_path

        entries.append(
            ManifestEntry(
                index=raw_index,
                source_repo=source_repo,
                source_ref=source_ref,
                source_path=source_path,
                target_path=target_path,
                direction=require_string_property(raw_entry, fields["direction"], raw_index),
                lifecycle_policy=require_string_property(raw_entry, fields["lifecycle_policy"], raw_index),
                uniqueness_policy=require_string_property(raw_entry, fields["uniqueness_policy"], raw_index),
                managed_scope=require_string_property(raw_entry, fields["managed_scope"], raw_index),
                markers=parse_markers(raw_entry, metadata, raw_index),
                manifest_properties=manifest_properties,
            )
        )

    return entries


def rule_applies_to_entry(rule: dict[str, Any], entry: ManifestEntry) -> bool:
    condition = rule.get("when")
    if condition is None:
        return True
    if not isinstance(condition, dict):
        raise ManifestError(f"Semantic rule '{rule.get('name')}' has an invalid when condition.")

    property_name = condition.get("property")
    if not isinstance(property_name, str) or not property_name:
        raise ManifestError(f"Semantic rule '{rule.get('name')}' when condition must define a property.")

    value = entry.manifest_value(property_name)
    if "equals" in condition:
        return value == condition["equals"]
    if "in" in condition:
        allowed_values = condition["in"]
        if not isinstance(allowed_values, list):
            raise ManifestError(f"Semantic rule '{rule.get('name')}' when.in condition must be an array.")
        return value in allowed_values
    if "starts_with" in condition:
        prefix = condition["starts_with"]
        return isinstance(value, str) and isinstance(prefix, str) and value.startswith(prefix)

    raise ManifestError(
        f"Semantic rule '{rule.get('name')}' when condition must define equals, in, or starts_with."
    )


def enabled_rules(rules_config: dict[str, Any]) -> list[dict[str, Any]]:
    rules: list[dict[str, Any]] = []
    for raw_rule in rules_config.get("rules", []):
        if not isinstance(raw_rule, dict):
            raise ManifestError("Every semantic rule entry must be an object.")
        if raw_rule.get("enabled", False):
            name = raw_rule.get("name")
            if not isinstance(name, str) or not name:
                raise ManifestError("Every enabled semantic rule must have a non-empty name.")
            rules.append(raw_rule)
    return rules


def run_unique_normalized_source_identity(entries: list[ManifestEntry], rule: dict[str, Any]) -> None:
    seen: dict[tuple[str, str, str], int] = {}
    for entry in entries:
        existing_index = seen.get(entry.source_identity_key)
        if existing_index is not None:
            raise ManifestError(
                f"{entry.describe()} duplicates source identity already declared by manifest entry {existing_index}. "
                f"Current entry at {manifest_entry_path(entry.index)}; existing entry at "
                f"{manifest_entry_path(existing_index)}."
            )
        seen[entry.source_identity_key] = entry.index


def run_unique_normalized_target_path(entries: list[ManifestEntry], rule: dict[str, Any]) -> None:
    seen: dict[str, int] = {}
    for entry in entries:
        existing_index = seen.get(entry.target_identity_key)
        if existing_index is not None:
            raise ManifestError(
                f"{entry.describe()} duplicates target_path already declared by manifest entry {existing_index}. "
                f"Current target at {manifest_entry_path(entry.index, 'target_path')}; existing target at "
                f"{manifest_entry_path(existing_index, 'target_path')}."
            )
        seen[entry.target_identity_key] = entry.index


def run_source_target_basename_must_match(entries: list[ManifestEntry], rule: dict[str, Any]) -> None:
    for entry in entries:
        if PurePosixPath(entry.source_path).name != PurePosixPath(entry.target_path).name:
            raise ManifestError(
                f"{entry.describe()} has a basename mismatch between source_path '{entry.source_path}' "
                f"and target_path '{entry.target_path}' at {manifest_entry_path(entry.index, 'source_path')} "
                f"and {manifest_entry_path(entry.index, 'target_path')}."
            )


def run_repository_relative_safe_paths(entries: list[ManifestEntry], rule: dict[str, Any]) -> None:
    for entry in entries:
        normalize_repo_relative_path(entry.source_path, "source_path", entry.index)
        normalize_repo_relative_path(entry.target_path, "target_path", entry.index)


def run_file_like_paths_only(entries: list[ManifestEntry], rule: dict[str, Any]) -> None:
    for entry in entries:
        for field_name, path_value in (("source_path", entry.source_path), ("target_path", entry.target_path)):
            if path_value.endswith("/") or PurePosixPath(path_value).name == "":
                raise ManifestError(
                    f"{entry.describe()} uses {field_name} '{path_value}', but it must point to a file-like path "
                    f"at {manifest_entry_path(entry.index, field_name)}."
                )


def run_reject_reserved_target_path(entries: list[ManifestEntry], rule: dict[str, Any]) -> None:
    prefixes = rule.get("prefixes", RESERVED_TARGET_PATH_PREFIXES)
    if not isinstance(prefixes, list):
        prefixes = list(RESERVED_TARGET_PATH_PREFIXES)

    for entry in entries:
        for prefix in prefixes:
            if isinstance(prefix, str) and entry.target_path.startswith(prefix):
                raise ManifestError(
                    f"{entry.describe()} targets reserved implementation scratch space '{prefix}' "
                    f"at {manifest_entry_path(entry.index, 'target_path')}."
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
        raise ManifestError(f"Failed to inspect tracked files in '{repo_root}': {exc}.") from exc

    output = result.stdout.decode("utf-8", errors="strict")
    return [item for item in output.split("\0") if item]


def run_basename_unique_tracked_file_scan(entries: list[ManifestEntry], rule: dict[str, Any], repo_root: Path) -> None:
    matching_entries = [entry for entry in entries if rule_applies_to_entry(rule, entry)]
    if not matching_entries:
        return

    tracked_files = load_tracked_files(repo_root)
    target_paths = {entry.target_path: entry for entry in entries}

    for entry in matching_entries:
        conflicting_manifest_targets = sorted(
            other.target_path
            for other in entries
            if other.target_path != entry.target_path and other.basename == entry.basename
        )
        if conflicting_manifest_targets:
            conflicts = ", ".join(conflicting_manifest_targets)
            raise ManifestError(
                f"{entry.describe()} declares basename uniqueness, but other manifest targets "
                f"share basename '{entry.basename}': {conflicts}. Entry at "
                f"{manifest_entry_path(entry.index, 'target_path')}."
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
                f"{entry.describe()} declares basename uniqueness, but tracked repository files "
                f"already share basename '{entry.basename}': {conflicts}. Entry at "
                f"{manifest_entry_path(entry.index, 'target_path')}."
            )


def target_abspath(repo_root: Path, target_path: str) -> Path:
    return repo_root.joinpath(*PurePosixPath(target_path).parts)


def assert_safe_worktree_file_path(
    repo_root: Path,
    target_path: Path,
    target_label: str,
    entry_description: str,
) -> None:
    resolved_root = repo_root.resolve(strict=True)
    lexical_parent = repo_root
    target_parts = PurePosixPath(target_label).parts

    for path_part in target_parts[:-1]:
        lexical_parent = lexical_parent / path_part

        if lexical_parent.is_symlink():
            raise ManifestError(
                f"{entry_description} cannot use target_path '{target_label}' because parent '{lexical_parent}' is a symlink."
            )
        if lexical_parent.exists() and not lexical_parent.is_dir():
            raise ManifestError(
                f"{entry_description} cannot use target_path '{target_label}' because parent '{lexical_parent}' is not a directory."
            )

    if target_path.is_symlink():
        raise ManifestError(
            f"{entry_description} cannot use target_path '{target_label}' because it is a symlink."
        )

    try:
        target_path.resolve(strict=False).relative_to(resolved_root)
    except ValueError as exc:
        raise ManifestError(
            f"{entry_description} points outside the checked-out repository: '{target_label}'."
        ) from exc

    if target_path.exists() and not target_path.is_file():
        raise ManifestError(
            f"{entry_description} points to target_path '{target_label}', but that path exists and is not a regular file."
        )


def run_worktree_target_path_safety(entries: list[ManifestEntry], rule: dict[str, Any], repo_root: Path) -> None:
    for entry in entries:
        target_path = target_abspath(repo_root, entry.target_path)
        assert_safe_worktree_file_path(repo_root, target_path, entry.target_path, entry.describe())


def run_reject_matching_entries(entries: list[ManifestEntry], rule: dict[str, Any]) -> None:
    message = rule.get("message")
    if not isinstance(message, str) or not message:
        message = f"Semantic rule '{rule.get('name')}' rejected this manifest entry."

    for entry in entries:
        if rule_applies_to_entry(rule, entry):
            property_name = (rule.get("when") or {}).get("property") if isinstance(rule.get("when"), dict) else None
            location = manifest_entry_path(entry.index, property_name if isinstance(property_name, str) else None)
            raise ManifestError(f"{entry.describe()} at {location}: {message}")


def validate_semantic_rules(entries: list[ManifestEntry], rules_config: dict[str, Any], repo_root: Path) -> None:
    dispatch = {
        "unique_normalized_source_identity": lambda rule: run_unique_normalized_source_identity(entries, rule),
        "unique_normalized_target_path": lambda rule: run_unique_normalized_target_path(entries, rule),
        "source_target_basename_must_match": lambda rule: run_source_target_basename_must_match(entries, rule),
        "repository_relative_safe_paths": lambda rule: run_repository_relative_safe_paths(entries, rule),
        "file_like_paths_only": lambda rule: run_file_like_paths_only(entries, rule),
        "reject_reserved_target_path": lambda rule: run_reject_reserved_target_path(entries, rule),
        "worktree_target_path_safety": lambda rule: run_worktree_target_path_safety(entries, rule, repo_root),
        "basename_unique_tracked_file_scan": lambda rule: run_basename_unique_tracked_file_scan(entries, rule, repo_root),
        "reject_matching_entries": lambda rule: run_reject_matching_entries(entries, rule),
        "reject_non_source_to_target": lambda rule: run_reject_matching_entries(entries, rule),
    }

    for rule in enabled_rules(rules_config):
        name = rule["name"]
        runner = dispatch.get(name)
        if runner is None:
            raise ManifestError(f"Semantic rule '{name}' is enabled but no executor is implemented.")
        runner(rule)


def validate_and_normalize_manifest(
    manifest_json: str,
    repo_root: Path,
    schema_path: Path,
    rules_path: Path,
) -> list[ManifestEntry]:
    schema = load_schema(schema_path)
    rules = load_rules(rules_path)
    metadata = load_manifest_metadata(schema)
    manifest_document = parse_manifest_document(manifest_json)

    validate_manifest_schema(manifest_document, schema)
    entries = build_entries(manifest_document, metadata)
    validate_semantic_rules(entries, rules, repo_root)
    return entries


def write_normalized_manifest(entries: list[ManifestEntry], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "entries": [entry.to_dict() for entry in entries],
    }
    with destination.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def load_normalized_manifest(path: Path) -> list[ManifestEntry]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ManifestError(
            f"Normalized manifest file '{path}' is invalid: {exc.msg} at line {exc.lineno}, column {exc.colno}."
        ) from exc

    if not isinstance(data, dict) or not isinstance(data.get("entries"), list):
        raise ManifestError(f"Normalized manifest file '{path}' must contain an object with an entries array.")

    return [ManifestEntry.from_dict(item) for item in data["entries"]]


def ensure_parent_directory(target_path: Path) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)


def fetch_source_bytes(entry: ManifestEntry, source_token: str | None) -> bytes:
    encoded_path = urllib.parse.quote(entry.source_path, safe="/")
    encoded_ref = urllib.parse.quote(entry.source_ref, safe="")
    url = f"https://api.github.com/repos/{entry.source_repo}/contents/{encoded_path}?ref={encoded_ref}"

    headers = {
        "Accept": "application/vnd.github.raw+json",
        "User-Agent": "sync-files-from-manifest",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
    }
    if source_token:
        headers["Authorization"] = f"Bearer {source_token}"

    request = urllib.request.Request(url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(request, timeout=SOURCE_FETCH_TIMEOUT_SECONDS) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        message = (
            f"Unable to fetch source for {entry.describe()} (HTTP {exc.code}). "
            "If the source repository is private, provide the optional read-only source_token secret. "
            "Otherwise verify source_repo, source_ref, and source_path. Source field locations: "
            f"{manifest_entry_path(entry.index, 'source_repo')}, "
            f"{manifest_entry_path(entry.index, 'source_ref')}, "
            f"{manifest_entry_path(entry.index, 'source_path')}."
        )
        raise SourceFetchError(message) from exc
    except urllib.error.URLError as exc:
        raise SourceFetchError(
            f"Unable to fetch source for {entry.describe()}: {exc.reason}. Source field locations: "
            f"{manifest_entry_path(entry.index, 'source_repo')}, "
            f"{manifest_entry_path(entry.index, 'source_ref')}, "
            f"{manifest_entry_path(entry.index, 'source_path')}."
        ) from exc


def read_file_bytes(path: Path) -> bytes:
    return path.read_bytes()


def write_file_bytes(path: Path, content: bytes) -> None:
    ensure_parent_directory(path)
    path.write_bytes(content)
