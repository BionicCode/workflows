# Sync Manifest API Reference

This reference documents the JSON API consumed by the `sync-files-from-manifest` reusable workflow.

The caller-owned manifest lives at:

```text
.github/sync-config/sync-manifest.json
```

The authoritative schema and runtime rules are bundled with the reusable workflow version being executed. The schema copied into a caller repository is for editor tooling and human guidance.

Marker-scoped synchronization is supported for strict UTF-8 text files. Source marker blocks define authoritative sync regions where deterministically enforceable, marker delimiters are matched exactly, marker blocks are matched by occurrence order, and existing target delimiter text is preserved.

## Runtime Support

| Feature | Schema-valid | Runtime-supported | Notes |
|---|---:|---:|---|
| `source_path` exact-file sync | Yes | Yes | One source file maps to one target file. |
| `source_glob` directory/file-set sync | Yes | Yes | Expands matching files into exact-file sync operations. |
| `source_to_target` + `whole_file` | Yes | Yes | Byte-for-byte source-to-target sync. |
| `source_to_target` + `outside_markers` | Yes | Yes | Source owns outside content; target-owned blocks may be preserved or fully omitted by projection. |
| `source_to_target` + `inside_markers` | Yes | Yes | Source inner content is enforced by occurrence order. |
| `target_to_source` | Yes | No | Rejected by current execution rules. |
| `two_way` | Yes | No | Rejected by current execution rules. |
| Delete unmatched targets | No | No | Extra files are not deleted automatically. |

## Source Selection

Each `ManifestEntry` must specify exactly one source selector:

- `source_path`: exact-file mode. Wildcards are not interpreted.
- `source_glob`: pattern mode. Matching files are expanded into exact-file sync operations during verify/sync planning.

`source_glob` entries may include:

| Field | Type | Description |
|---|---|---|
| `source_glob` | string | Repository-relative POSIX glob pattern containing at least one glob metacharacter. |
| `glob` | object | Optional glob matching options. |
| `glob.recursive` | boolean | Defaults to `false`. Allows `**` when `true`. |
| `glob.include_hidden` | boolean | Defaults to `false`. Allows wildcard segments to match dot-prefixed path segments broadly when `true`. |

For `source_glob`, `target_path` must end with `/` and is the target directory root. Relative layout below the glob base directory is preserved.

Hidden matching:

- `include_hidden=false` prevents wildcard segments from implicitly matching dot-prefixed path segments.
- Explicit dot segments such as `.github` are allowed.
- A pattern segment starting with `.` may match dot-prefixed names for that segment only.
- `include_hidden=true` lets wildcard segments match hidden path segments broadly.

`*.*` only matches names containing a dot. Use `*` for all files, `*.md` for Markdown files, and `**/*.md` with `glob.recursive=true` for recursive Markdown sync.

## Marker-Scoped Runtime Errors

- Missing source markers for a marker-scoped entry.
- Malformed, unmatched, or nested source or target markers.
- `inside_markers` target missing, fewer, or extra exact marker blocks.
- `outside_markers` target containing a partial set of marker blocks or extra exact marker blocks.
- UTF-8 decode failure for marker-scoped source or target content.

## Source Glob Validation And Runtime Errors

- Both `source_path` and `source_glob` are present.
- Neither `source_path` nor `source_glob` is present.
- `source_glob` uses a `target_path` that does not end with `/`.
- `source_glob` does not contain a glob metacharacter.
- `source_glob` contains an invalid path segment, backslash, absolute path, drive-qualified path, `.`, or `..`.
- `source_glob` contains `**` while `glob.recursive=false`.
- `source_glob` matches zero files.
- The source tree response is truncated.
- Two exact or expanded entries generate the same target path.
- Marker parsing fails in an expanded marker-scoped file.

`validate` mode checks schema and local semantic rules only. Remote expansion, zero-match detection, generated duplicate detection, tree truncation, and source fetch errors are detected during verify/sync planning before writes.

## Types

| Type | Placement | Description |
|---|---|---|
| [`ManifestDocument`](types/manifest-document.md) | Top-level object | Root JSON object that identifies the schema version and contains manifest entries. |
| [`ManifestEntry`](types/manifest-entry.md) | Array item object | One strict source-to-target managed-file mapping plus its policy values. |
| [`Markers`](types/markers.md) | Nested object | Marker delimiters stored under `ManifestEntry.markers`. |
| [`RepoRelativeFilePath`](types/repo-relative-file-path.md) | Scalar string | Repository-relative file path string used by `source_path` and `target_path`. |
| [`SourceSelector`](types/source-selector.md) | Field group | Exactly one of `source_path` or `source_glob`. |
| [`Direction`](types/direction.md) | Enum string | Synchronization direction value used by `ManifestEntry.direction`. |
| [`LifecyclePolicy`](types/lifecycle-policy.md) | Enum string | Lifecycle value used by `ManifestEntry.lifecycle_policy`. |
| [`UniquenessPolicy`](types/uniqueness-policy.md) | Enum string | Uniqueness value used by `ManifestEntry.uniqueness_policy`. |
| [`ManagedScope`](types/managed-scope.md) | Enum string | Managed-scope value used by `ManifestEntry.managed_scope`. |

## Guides

| Document | Description |
|---|---|
| [`sync-manifest.md`](sync-manifest.md) | Purpose, usage, current version boundaries, type placement, and field-by-field manifest documentation. |
