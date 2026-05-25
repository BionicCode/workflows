# Reusable Workflows

Central repository of reusable GitHub Actions workflows for BionicCode repositories.

## Available Workflows

| Workflow | File | Description |
|---|---|---|
| CI | `.github/workflows/ci.yml` | Build and test projects with optional artifact upload. |
| Release | `.github/workflows/release.yml` | Create a GitHub Release and optionally attach build artifacts. |
| Lint | `.github/workflows/lint.yml` | Run .NET and Node.js code-quality checks. |
| Sync files from manifest | `.github/workflows/sync-files-from-manifest.yml` | Generic managed-file sync workflow driven by caller-owned manifests. |
| Deprecated: Sync `.editorconfig` | `.github/workflows/sync-editorconfig-on-push.yml` | Legacy `.editorconfig`-specific migration path. |

Reference reusable workflows with:

```yaml
uses: BionicCode/workflows/.github/workflows/<workflow-file>.yml@<ref>
```

Using `@main` is acceptable during development and early testing. After release, descendant repositories should pin reusable workflows to a tag or, preferably, a full commit SHA for immutable production use and supply-chain safety.

## Managed-File Sync Ownership

`BionicCode/workflows` owns the reusable managed-file sync engine, bundled schema, semantic rules, starter manifest, script implementation, and copied reference documentation.

Each caller repository owns its manifest at:

```text
.github/sync-config/sync-manifest.json
```

The schema copied to caller repositories at `.github/sync-config/sync-manifest.schema.json` is for editor tooling, documentation, and human guidance. Authoritative validation always uses the schema bundled with the reusable workflow version being executed.

`VisualStudioGitHubTemplate` copied schema/docs/manifest content must be migrated separately after this contract change; this repository change does not modify that template repository.

## Sync Files From Manifest

### Interface

```yaml
jobs:
  sync-managed-files:
    permissions:
      contents: write
      pull-requests: write
    uses: BionicCode/workflows/.github/workflows/sync-files-from-manifest.yml@main
    with:
      command: sync
      manifest_json: ${{ needs.inspect-manifest.outputs.manifest_json }}
    # Omit this block when all source repositories are public.
    secrets:
      source_token: ${{ secrets.SOURCE_REPO_READ_TOKEN }}
```

Inputs:

| Input | Type | Required | Default | Description |
|---|---|---|---|---|
| `command` | string | No | `sync` | One of `init`, `validate`, or `sync`. Invalid values fail before checkout/fetch/write. |
| `manifest_json` | string | For `validate` and `sync` | `""` | Object-shaped manifest JSON. Forbidden for `init`. |
| `sync_branch_prefix` | string | No | `chore/sync-managed-files` | Branch prefix for generated sync PRs. |

Secrets:

| Secret | Required | Description |
|---|---|---|
| `source_token` | No | Optional read-only token for private cross-repo source reads. Public sources are read without it. |

Caller jobs that invoke `init` or `sync` should grant `contents: write` and `pull-requests: write`. The reusable workflow narrows permissions at job level: PR verification uses `contents: read`; init and branch sync PR creation use `contents: write` and `pull-requests: write`.

No workflow-call inputs changed for `target_directory` or `source_glob`; both are manifest fields.

### Commands

- `init` copies or updates `.github/sync-config/sync-manifest.schema.json`, copies documentation, creates `.github/sync-config/sync-manifest.json` only when missing, opens or updates one initialization PR, and stops without source fetch or sync.
- `validate` validates `manifest_json` against the bundled JSON Schema and local semantic rules only. It does not enumerate remote trees, fetch sources, parse marker content, or write files.
- `sync` validates first, writes the normalized manifest, expands remote globs during planning, and then verifies PRs or creates/updates one aggregated sync PR on branch events.

### Manifest Shape

Object-shaped manifests are the only supported shape:

```json
{
  "$schema": "./sync-manifest.schema.json",
  "schema_version": 1,
  "entries": [
    {
      "source_repo": "BionicCode/template-visual-studio-repository",
      "source_ref": "main",
      "source_path": "README.md",
      "target_directory": "",
      "direction": "source_to_target",
      "lifecycle_policy": "seed_once",
      "uniqueness_policy": "none",
      "managed_scope": "whole_file"
    }
  ]
}
```

Old top-level array manifests are intentionally rejected. Wrap the array under `entries` and add `schema_version`.

### Path Naming Rules

Manifest paths are logical repository-relative POSIX paths. They always use `/` and are never repaired with host OS normalization.

`source_path`:

- Selects exactly one source file.
- Must be non-empty, repository-relative, and file-like.
- Must not end with `/`.
- Must not contain wildcards. Use `source_glob` for patterns.

`source_glob`:

- Selects many source files and must contain at least one glob metacharacter: `*`, `?`, or `[`.
- Must be non-empty, repository-relative, and use forward slashes.
- `**` is valid only as a complete path segment and only with `glob.recursive: true`.
- `*`, `?`, and character classes match within one path segment.

`target_directory`:

- Is required for every entry and is directory-only.
- Use `""` for the repository root.
- Use a trailing `/` for every non-root directory, for example `.github/` or `docs/reference/`.
- Do not include the target file name.
- The workflow never ignores a filename-like suffix. Values such as `AGENTS.md`, `.github`, and `.github/AGENTS.md` are invalid.
- `docs.v1/` is valid because the trailing slash makes it directory syntax; dots are not used as filename heuristics.

All manifest path fields reject leading `/`, backslashes, Windows drive prefixes, empty path segments, and exact `.` or `..` segments. Dot-prefixed ordinary names such as `.github/` remain valid.

### Source Selection And Target Computation

Each entry uses exactly one source selector:

- `source_path` means one exact source file. The target is `target_directory + basename(source_path)`, so source parent directories are intentionally flattened.
- `source_glob` means many source files. The workflow expands matches into exact-file operations, preserving relative layout below the glob base directory under `target_directory`.

`glob_base` is the longest leading directory prefix before the first path segment containing `*`, `?`, or `[`.

| `source_glob` | `glob_base` | Matched source | Relative part | With `target_directory: "out/"` |
|---|---|---|---|---|
| `*.md` | `""` | `README.md` | `README.md` | `out/README.md` |
| `docs/*.md` | `docs/` | `docs/readme.md` | `readme.md` | `out/readme.md` |
| `docs/**/*.md` | `docs/` | `docs/readme.md` | `readme.md` | `out/readme.md` |
| `docs/**/*.md` | `docs/` | `docs/types/markers.md` | `types/markers.md` | `out/types/markers.md` |
| `.github/scripts/**/*.md` | `.github/scripts/` | `.github/scripts/a/b.md` | `a/b.md` | `out/a/b.md` |

Hidden matching:

- `include_hidden: false` prevents wildcard segments from implicitly matching dot-prefixed path segments.
- Explicit dot segments such as `.github` are allowed.
- A pattern segment starting with `.` may match dot-prefixed names for that segment.
- `include_hidden: true` allows wildcard segments to match hidden path segments broadly.
- `**/*.md` with `include_hidden: false` does not traverse `.github`.

`*.*` only matches names containing a dot. Use `*` for all files, `*.md` for Markdown files, and `**/*.md` with `glob.recursive: true` for recursive Markdown sync.

Example recursive documentation sync:

```json
{
  "source_repo": "BionicCode/workflows",
  "source_ref": "main",
  "source_glob": ".github/scripts/sync-files-from-manifest/documentation/**/*.md",
  "target_directory": ".github/sync-config/documentation/",
  "glob": {
    "recursive": true
  },
  "direction": "source_to_target",
  "lifecycle_policy": "enforce",
  "uniqueness_policy": "none",
  "managed_scope": "whole_file"
}
```

### Feature Support Matrix

| Feature | Schema-valid | Runtime-supported | Notes |
|---|---:|---:|---|
| `source_path` exact-file sync | Yes | Yes | One source file maps to one computed target file. |
| `source_glob` directory/file-set sync | Yes | Yes | Expands matching source files into exact-file sync operations. |
| `source_to_target` + `whole_file` | Yes | Yes | Byte-for-byte target replacement or verification. |
| `source_to_target` + `outside_markers` | Yes | Yes | Source outside content is enforced; target-owned blocks may be preserved or fully omitted by projection. |
| `source_to_target` + `inside_markers` | Yes | Yes | Source inner content is enforced by occurrence order. |
| `target_to_source` | Yes | No | Recognized for future contract stability; rejected by current execution rules. |
| `two_way` | Yes | No | Recognized for future contract stability; rejected by current execution rules. |
| Delete unmatched targets | No | No | Extra files are not deleted automatically. |

### Marker-Scoped Behavior

`whole_file` is byte-for-byte behavior and is suitable for binary files when GitHub source-fetch behavior supports them.

Marker-scoped entries are strict UTF-8 text-file behavior. Marker delimiters are exact substring matches; they are not regular expressions and are not trimmed, case-folded, or whitespace-normalized.

`outside_markers`:

- Source-side marker blocks define target-owned extension points.
- If the target has the same number of exact marker blocks as the source, target inner content is preserved by occurrence order.
- If the target has zero exact marker blocks, the target must equal the source-owned outside projection; partial or extra target marker blocks fail.

`inside_markers`:

- The target must contain the same exact marker count as the source, matched by occurrence order.
- Source inner content is enforced into occurrence-matched target blocks.
- The workflow does not use fuzzy diff, LCS, `difflib`, or heuristic moved-block detection. Stronger same-source-context detection requires future marker IDs, named anchors, or source-owned outside context anchors.

### Validation And Planning Model

JSON Schema is the source of truth for structural manifest metadata: top-level shape, required fields, closed object fields, enum values, marker object shape, marker conditionals, source selector XOR, and `glob` option shape.

Python semantic validation handles checks that require normalization, Git state, repository context, or cross-entry analysis: normalized duplicates, source repository format, POSIX path safety, reserved `_sync-files-from-manifest-workflow/` destinations, symlink checks, `basename_unique`, and current execution-policy limits.

`validate` is local-only. Remote Git tree expansion, zero-match failure, tree truncation failure, generated duplicate target detection, source fetching, marker parsing, and write planning happen during PR verification or branch/default maintenance sync before any writes. Git tree responses marked as truncated fail safely instead of syncing a partial file set. Unmatched target files are not deleted.

### Common Recipes

Sync `.editorconfig` as a singleton whole file:

```json
{
  "source_repo": "BionicCode/bioniccode-code-style",
  "source_ref": "main",
  "source_path": ".editorconfig",
  "target_directory": "",
  "direction": "source_to_target",
  "lifecycle_policy": "enforce",
  "uniqueness_policy": "basename_unique",
  "managed_scope": "whole_file"
}
```

Sync `Directory.Build.props` as a whole file:

```json
{
  "source_repo": "BionicCode/bioniccode-code-style",
  "source_ref": "main",
  "source_path": "Directory.Build.props",
  "target_directory": "",
  "direction": "source_to_target",
  "lifecycle_policy": "enforce",
  "uniqueness_policy": "none",
  "managed_scope": "whole_file"
}
```

Sync `AGENTS.md` or Copilot instructions while preserving repository-specific text:

```json
{
  "source_repo": "BionicCode/template-visual-studio-repository",
  "source_ref": "main",
  "source_path": "AGENTS.md",
  "target_directory": "",
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

The corresponding source file can include this placeholder:

```markdown
<!-- BEGIN REPOSITORY SPECIFICS -->
<!-- Repository owners may edit only this section. -->
<!-- END REPOSITORY SPECIFICS -->
```

Do not append annotations to a marker delimiter unless the manifest marker string includes that annotation exactly. If no target-owned section is desired, use `managed_scope: "whole_file"` instead of marker scope.

Seed a starter file once:

```json
{
  "source_repo": "BionicCode/template-visual-studio-repository",
  "source_ref": "main",
  "source_path": "README.md",
  "target_directory": "",
  "direction": "source_to_target",
  "lifecycle_policy": "seed_once",
  "uniqueness_policy": "none",
  "managed_scope": "whole_file"
}
```

Sync workflow manifest documentation recursively:

```json
{
  "source_repo": "BionicCode/workflows",
  "source_ref": "main",
  "source_glob": ".github/scripts/sync-files-from-manifest/documentation/**/*.md",
  "target_directory": ".github/sync-config/documentation/",
  "glob": {
    "recursive": true
  },
  "direction": "source_to_target",
  "lifecycle_policy": "enforce",
  "uniqueness_policy": "none",
  "managed_scope": "whole_file"
}
```

### Security Model

- The caller repository `GITHUB_TOKEN` writes only to the caller repository.
- `source_token` is optional and should be read-only; use it only when private source repositories require it.
- Avoid implicit secret inheritance; pass only the named `source_token` secret when needed.
- Pin reusable workflows for production, preferably to a full commit SHA.

### Limits And Roadmap

Current: `source_path`, `source_glob`, `source_to_target`, `whole_file`, `outside_markers`, and `inside_markers`.

Not supported: delete unmatched target files.

Possible later: delete policy, marker IDs, named anchors, or source-owned outside context anchors.

Deferred: `target_to_source` and `two_way`.

## Migration From The Legacy `.editorconfig` Workflow

New callers should use `sync-files-from-manifest.yml`; the `.editorconfig`-specific workflow is kept only as a temporary migration path.

Migration steps:

1. Add the generic caller workflow to the caller or template repository.
2. Run the caller workflow from the default branch to initialize `.github/sync-config`.
3. Edit and commit `.github/sync-config/sync-manifest.json` with the real managed-file defaults.
4. Remove the legacy `.editorconfig` redirect workflow from the caller/template repository.
5. Pin the reusable workflow to a release tag or, preferably, a full commit SHA after the first tested release.

## Contributing

1. Keep reusable workflow YAML orchestration-focused.
2. Put substantial implementation logic under `.github/scripts/<workflow-name>/`.
3. Keep workflow-call interfaces typed and documented.
4. Update this README when inputs, command behavior, schemas, or migration requirements change.
