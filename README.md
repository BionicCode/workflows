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

Using `@main` is acceptable during development and early testing. After release, descendant repositories should pin reusable workflows to a tag or full commit SHA for stability and supply-chain safety.

## Managed-File Sync Ownership

`BionicCode/workflows` owns the reusable managed-file sync engine:

- `.github/workflows/sync-files-from-manifest.yml`
- `.github/scripts/sync-files-from-manifest/schema/sync-manifest.schema.json`
- `.github/scripts/sync-files-from-manifest/schema/sync-rules.json`
- `.github/scripts/sync-files-from-manifest/templates/sync-manifest.template.json`
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
- `source_path`
- `target_path`
- `direction`
- `lifecycle_policy`
- `uniqueness_policy`
- `managed_scope`
- `markers` only when required by marker-scoped managed scopes

Stage 1 executes:

- `direction: source_to_target`
- `lifecycle_policy: enforce`, `seed_once`, `disabled`
- `uniqueness_policy: basename_unique`, `none`
- `managed_scope: whole_file`

The schema recognizes `managed_scope: outside_markers` and `managed_scope: inside_markers`, but Stage 1 rejects those entries before source fetch/write with a clear unsupported-in-v1 error.

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
- repository-relative safe paths
- file-like paths only
- reserved `_sync-files-from-manifest-workflow/` target paths
- symlink targets and symlink parent directories
- tracked-file scanning for `basename_unique`
- Stage 1 rejection of schema-recognized but runtime-deferred policies

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

### Authentication And Assumptions

Use optional read-only `source_token` for private cross-repo source reads. Otherwise, public access is used where possible. If a private source repository cannot be read, the workflow fails clearly and asks for `source_token`.

Source files are fetched through GitHub repository contents/raw API behavior. Stage 1 is intended for managed text, config, and document-style files such as `.editorconfig`, `Directory.Build.props`, `AGENTS.md`, and Copilot instruction files. It is not intended for large binary assets.

If this reusable workflow is hosted in a private repository and consumed by another private repository, GitHub Actions repository/reuse settings must allow that sharing relationship.

## Migration From The Legacy `.editorconfig` Workflow

New callers should use `sync-files-from-manifest.yml`; the `.editorconfig`-specific workflow is kept only as a temporary migration path.

Migration steps:

1. Add the generic caller workflow to the caller or template repository.
2. Run the caller workflow from the default branch to initialize `.github/sync-config`.
3. Edit and commit `.github/sync-config/sync-manifest.json` with the real managed-file defaults.
4. Remove the legacy `.editorconfig` redirect workflow from the caller/template repository.
5. Pin the reusable workflow to a release tag or SHA after the first tested release.

## Contributing

1. Keep reusable workflow YAML orchestration-focused.
2. Put substantial implementation logic under `.github/scripts/<workflow-name>/`.
3. Keep workflow-call interfaces typed and documented.
4. Update this README when inputs, command behavior, schemas, or migration requirements change.
