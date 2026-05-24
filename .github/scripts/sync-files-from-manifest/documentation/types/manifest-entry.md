# ManifestEntry

One source-to-target managed-file mapping. An entry selects either one exact source file with `source_path`, or a file set with `source_glob`.

## Shape

```json
{
  "source_repo": "BionicCode/template-visual-studio-repository",
  "source_ref": "main",
  "source_path": "AGENTS.md",
  "target_path": "AGENTS.md",
  "direction": "source_to_target",
  "lifecycle_policy": "enforce",
  "uniqueness_policy": "none",
  "managed_scope": "whole_file"
}
```

Marker-scoped entries include the conditional `markers` child object:

```json
{
  "source_repo": "BionicCode/template-visual-studio-repository",
  "source_ref": "main",
  "source_path": "AGENTS.md",
  "target_path": "AGENTS.md",
  "direction": "source_to_target",
  "lifecycle_policy": "enforce",
  "uniqueness_policy": "none",
  "managed_scope": "outside_markers",
  "markers": {
    "start": "<!-- BEGIN REPOSITORY SPECIFICS -->",
    "end": "<!-- END REPOSITORY SPECIFICS -->"
  }
}
```

## Placement

| Property | Value |
|---|---|
| Placement | Array item object |
| Valid parent | [`ManifestDocument`](manifest-document.md) |
| Parent property | `entries[]` |

## Attributes

| Attribute | Required | Type | Description |
|---|---:|---|---|
| `source_repo` | Yes | string | Source repository in `owner/repository` form. |
| `source_ref` | Yes | string | Source branch, tag, or commit SHA. |
| `source_path` | Conditional | [`RepoRelativeFilePath`](repo-relative-file-path.md) | Exact source file path. Required when `source_glob` is absent. Wildcards are not interpreted. |
| `source_glob` | Conditional | [`SourceSelector`](source-selector.md) | Source file pattern. Required when `source_path` is absent. |
| `target_path` | Yes | [`RepoRelativeFilePath`](repo-relative-file-path.md) | Target file path for `source_path`, or target directory root ending in `/` for `source_glob`. |
| `glob` | No | [`SourceSelector`](source-selector.md) | Options for `source_glob`; forbidden for exact `source_path` entries. |
| `direction` | Yes | [`Direction`](direction.md) | Synchronization direction. |
| `lifecycle_policy` | Yes | [`LifecyclePolicy`](lifecycle-policy.md) | Missing/changed/existing target behavior. |
| `uniqueness_policy` | Yes | [`UniquenessPolicy`](uniqueness-policy.md) | Optional basename uniqueness policy. |
| `managed_scope` | Yes | [`ManagedScope`](managed-scope.md) | Portion of the target file managed by the workflow. |
| `markers` | Conditional | [`Markers`](markers.md) | Required for marker scopes and forbidden for `whole_file`. |

## Child Values

| Child Property | Child Type | Description |
|---|---|---|
| `markers` | [`Markers`](markers.md) | Conditional marker delimiter object for marker-scoped entries. |
| `glob` | [`SourceSelector`](source-selector.md) | Optional glob options for `source_glob` entries. |

## Validation Rules

- Exactly one of `source_path` or `source_glob` is required.
- A normalized exact source identity is `source_repo + source_ref + source_path`.
- A normalized exact source identity may appear only once.
- A normalized exact or expanded `target_path` may appear only once.
- Exact `source_path` and `target_path` values must have the same basename.
- For `source_glob`, `target_path` is a directory root and basename validation applies after expansion.
- No implicit rename semantics are supported.
- Unknown entry properties are rejected.
