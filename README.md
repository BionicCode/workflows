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

`BionicCode/workflows` owns the reusable managed-file sync engine:

- `.github/workflows/sync-files-from-manifest.yml`
- `.github/scripts/sync-files-from-manifest/schema/sync-manifest.schema.json`
- `.github/scripts/sync-files-from-manifest/schema/sync-rules.json`
- `.github/scripts/sync-files-from-manifest/templates/sync-manifest.template.json`
- `.github/scripts/sync-files-from-manifest/documentation/`
- `.github/scripts/sync-files-from-manifest/*.py`

Each caller repository owns its manifest at:

```text
.github/sync-config/sync-manifest.json
```

The schema copied to caller repositories at `.github/sync-config/sync-manifest.schema.json` is for editor tooling, documentation, and human guidance. Authoritative validation always uses the schema bundled with the exact reusable workflow version being executed.

`template-visual-studio-repository` owns the real default manifest for Visual Studio template descendants. New repositories created from that GitHub template inherit the caller workflow and manifest naturally, and may customize the manifest later.

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

### Commands

- `init` copies or updates `.github/sync-config/sync-manifest.schema.json`, creates `.github/sync-config/sync-manifest.json` only when missing, opens or updates one initialization PR, and then stops. It does not fetch source files or sync managed files.
- `validate` validates `manifest_json` against the bundled JSON Schema, runs semantic rules from `sync-rules.json`, writes a normalized manifest for diagnostics, and performs no fetch/write behavior.
- `sync` validates first, writes the normalized manifest, and then verifies PRs or creates/updates one aggregated sync PR on branch events.

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
      "target_path": "README.md",
      "direction": "source_to_target",
      "lifecycle_policy": "seed_once",
      "uniqueness_policy": "none",
      "managed_scope": "whole_file"
    }
  ]
}
```

Old top-level array manifests are intentionally rejected. Wrap the array under `entries` and add `schema_version`.

Each entry supports:

- `source_repo`
- `source_ref`
- exactly one of `source_path` or `source_glob`
- `target_path`
- optional `glob` settings for `source_glob`
- `direction`
- `lifecycle_policy`
- `uniqueness_policy`
- `managed_scope`
- `markers` only when required by marker-scoped managed scopes

The current version executes:

- `direction: source_to_target`
- `lifecycle_policy: enforce`, `seed_once`, `disabled`
- `uniqueness_policy: basename_unique`, `none`
- `managed_scope: whole_file`, `outside_markers`, `inside_markers`

Managed scopes:

| Scope | Runtime support | Intended content |
|---|---:|---|
| `whole_file` | Yes | Byte-for-byte source-to-target sync. Suitable for text files and binary files that can be fetched through the GitHub source API. |
| `outside_markers` | Yes | Source owns content outside source-defined marker blocks. Target owns content inside those blocks. Marker-scoped sync is strict UTF-8 text-file behavior. |
| `inside_markers` | Yes | Source owns content inside marker blocks. Target owns outside content. Marker-scoped sync is strict UTF-8 text-file behavior. |

Marker delimiters are exact substring matches. They are not regular expressions and are not trimmed, case-folded, or whitespace-normalized.

### Feature Support Matrix

| Feature | Schema-valid | Runtime-supported | Notes |
|---|---:|---:|---|
| `source_path` exact-file sync | Yes | Yes | One source file maps to one target file. |
| `source_glob` directory/file-set sync | Yes | Yes | Expands matching source files into exact-file sync operations. |
| `source_to_target` + `whole_file` | Yes | Yes | Byte-for-byte target replacement or verification. |
| `source_to_target` + `outside_markers` | Yes | Yes | Source outside content is enforced; target-owned blocks may be preserved or fully omitted by projection. |
| `source_to_target` + `inside_markers` | Yes | Yes | Source inner content is enforced by occurrence order. |
| `target_to_source` | Yes | No | Recognized for future contract stability; rejected by current execution rules. |
| `two_way` | Yes | No | Recognized for future contract stability; rejected by current execution rules. |
| Delete unmatched targets | No | No | Extra files are not deleted automatically. |

### `source_path` Vs `source_glob`

`source_path` means exactly one source file. Wildcards are not interpreted in `source_path`.

`source_glob` means many source files. The workflow expands the pattern into deterministic exact-file sync operations before verify or sync planning. `target_path` must end with `/` for `source_glob` entries and is treated as the target directory root. Relative layout below the glob base directory is preserved. No workflow-call inputs changed for this feature.

Example recursive documentation sync:

```json
{
  "source_repo": "BionicCode/workflows",
  "source_ref": "main",
  "source_glob": ".github/scripts/sync-files-from-manifest/documentation/**/*.md",
  "target_path": ".github/sync-config/documentation/",
  "glob": {
    "recursive": true
  },
  "direction": "source_to_target",
  "lifecycle_policy": "enforce",
  "uniqueness_policy": "none",
  "managed_scope": "whole_file"
}
```

### Marker-Scoped Behavior

For marker-scoped entries, source files and existing target files are decoded with strict UTF-8. Undecodable files fail clearly. Use `whole_file` for binary files or for files where byte-for-byte replacement is desired.

`outside_markers`:

- Source-side marker blocks define target-owned extension points.
- If the target has the same number of exact marker blocks as the source, target inner content is preserved by occurrence order.
- If the target has zero exact marker blocks, the target must equal the source-owned outside projection; partial or extra target marker blocks fail.

`inside_markers`:

- The target must contain the same exact marker count as the source, matched by occurrence order.
- Source inner content is enforced into occurrence-matched target blocks.
- The workflow does not use fuzzy diff, LCS, `difflib`, or heuristic moved-block detection. Same-source-context movement detection requires future marker IDs, named anchors, or source-owned outside context anchors.

### Validation Model

JSON Schema is the source of truth for structural manifest metadata:

- top-level object shape
- required properties
- allowed properties with `additionalProperties: false`
- enum values
- marker object shape
- marker conditional requirements
- schema version

Python semantic validation handles checks that require normalization, Git state, repository context, or cross-entry analysis:

- duplicate normalized source identities
- duplicate normalized target paths
- source/target basename mismatches
- `source_glob` local pattern safety
- repository-relative safe paths
- file-like paths only
- reserved `_sync-files-from-manifest-workflow/` target paths
- symlink targets and symlink parent directories
- tracked-file scanning for `basename_unique`
- rejection of schema-recognized but currently unsupported execution policies such as `target_to_source` and `two_way`

After validation, execution reads only the normalized manifest file produced by validation. `sync_files.py` does not reinterpret raw `manifest_json`.

### Caller Workflow Pattern

Caller repositories should keep the workflow generic and keep managed file mappings out of workflow YAML. The Visual Studio template caller workflow:

- runs on `workflow_dispatch`, `pull_request`, `push`, and schedule `17 3 * * *`
- omits trigger branch filters and gates jobs dynamically against `github.event.repository.default_branch`
- runs manual maintenance only when `workflow_dispatch` is executed on the default branch
- fails non-default manual runs with `Manifest initialization must be run from the repository default branch.`
- fails pull requests with a clear message if the manifest is missing
- calls `command: init` when the manifest is missing on default-branch maintenance events
- calls `command: sync` when the manifest exists

This broader-trigger plus dynamic-gating shape is intentional because GitHub Actions trigger branch lists cannot use a dynamic default-branch expression.

### Common Recipes

Sync `.editorconfig` as a singleton whole file:

```json
{
  "source_repo": "BionicCode/bioniccode-code-style",
  "source_ref": "main",
  "source_path": ".editorconfig",
  "target_path": ".editorconfig",
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
  "target_path": "Directory.Build.props",
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
  "target_path": "README.md",
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
  "target_path": ".github/sync-config/documentation/",
  "glob": {
    "recursive": true
  },
  "direction": "source_to_target",
  "lifecycle_policy": "enforce",
  "uniqueness_policy": "none",
  "managed_scope": "whole_file"
}
```

### Failure Mode Examples

- Old top-level array manifest: wrap the array under `entries` and add `schema_version`.
- Duplicate `target_path`: each normalized target path may appear once.
- Basename mismatch: `source_path` and `target_path` basenames must match.
- `source_glob` with `target_path` not ending in `/`: glob targets must be directory roots.
- `source_glob` with no matches: the workflow fails rather than creating an empty sync PR.
- `source_glob` tree truncation: source enumeration fails rather than syncing a partial file set.
- Private source without `source_token`: provide an explicit read-only source token secret.
- Marker exact-match failure: marker delimiters must match the manifest strings exactly.
- `outside_markers` partial marker mismatch: keep all source-defined marker blocks or omit all target-owned blocks.
- Marker-scoped binary or invalid UTF-8 content: use `whole_file` or convert the file to strict UTF-8 text.

### Security Model

- The caller repository `GITHUB_TOKEN` writes only to the caller repository.
- `source_token` is optional and should be read-only; use it only when private source repositories require it.
- Avoid implicit secret inheritance; pass only the named `source_token` secret when needed.
- Pin reusable workflows for production, preferably to a full commit SHA.

### Limits And Roadmap

Current:

- `source_path`
- `source_glob`
- `source_to_target`
- `whole_file`
- `outside_markers`
- `inside_markers`

Not supported:

- delete unmatched target files

Possible later:

- delete policy for unmatched targets
- marker IDs, named anchors, or source-owned outside context anchors

Deferred:

- `target_to_source`
- `two_way`

### Authentication And Assumptions

Use optional read-only `source_token` for private cross-repo source reads. Otherwise, public access is used where possible. If a private source repository cannot be read, the workflow fails clearly and asks for `source_token`.

Source files are fetched through GitHub repository contents/raw API behavior. Marker-scoped sync is intended for managed UTF-8 text, config, and document-style files such as `.editorconfig`, `Directory.Build.props`, `AGENTS.md`, and Copilot instruction files. `whole_file` sync remains byte-for-byte behavior and can handle binary files when GitHub source-fetch behavior supports them. Large files are constrained by GitHub repository contents/raw API behavior.

If this reusable workflow is hosted in a private repository and consumed by another private repository, GitHub Actions repository/reuse settings must allow that sharing relationship.

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
