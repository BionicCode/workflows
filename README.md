# Reusable Workflows

Central repository of reusable GitHub Actions workflows that can be called from any repository in the organization.

## Available Workflows

| Workflow | File | Description |
|---|---|---|
| CI | [`ci.yml`](.github/workflows/ci.yml) | Build and test a project, with optional artifact upload |
| Release | [`release.yml`](.github/workflows/release.yml) | Create a GitHub Release and optionally attach build artifacts |
| Lint | [`lint.yml`](.github/workflows/lint.yml) | Run code-quality checks (.NET format, Node.js/npm lint) |
| Sync files from manifest | [`sync-files-from-manifest.yml`](.github/workflows/sync-files-from-manifest.yml) | Generic reusable sync workflow driven by a JSON manifest |
| Deprecated: Sync `.editorconfig` from canonical | [`sync-editorconfig-on-push.yml`](.github/workflows/sync-editorconfig-on-push.yml) | Legacy `.editorconfig`-specific workflow kept temporarily for migration |

---

## Usage

Reference any workflow in this repository using the `uses` key with the format:

```yaml
BionicCode/workflows/.github/workflows/<workflow-file>.yml@<ref>
```

where `<ref>` is a branch name (for example `main`), a tag, or a full commit SHA.

---

### CI Workflow (`ci.yml`)

Builds and tests a project. Supports .NET and Node.js out of the box; other runtimes can be driven by supplying custom `build-command` and `test-command` values.

**Inputs**

| Input | Type | Required | Default | Description |
|---|---|---|---|---|
| `runs-on` | string | No | `ubuntu-latest` | Runner label |
| `dotnet-version` | string | No | _(empty)_ | .NET SDK version (for example `9.0.x`). Skipped when empty. |
| `node-version` | string | No | _(empty)_ | Node.js version (for example `20`). Skipped when empty. |
| `build-command` | string | No | _(empty)_ | Shell command to build the project |
| `test-command` | string | No | _(empty)_ | Shell command to run the tests |
| `working-directory` | string | No | `.` | Working directory for build and test commands |
| `artifact-name` | string | No | _(empty)_ | Name for the uploaded artifact. Skipped when empty. |
| `artifact-path` | string | No | _(empty)_ | Path of files to include in the artifact |

**Secrets**

| Secret | Required | Description |
|---|---|---|
| `token` | No | GitHub token for authenticated API calls |

**Outputs**

| Output | Description |
|---|---|
| `artifact-name` | Name of the uploaded artifact (empty when no artifact was uploaded) |

**Example**

```yaml
jobs:
  ci:
    uses: BionicCode/workflows/.github/workflows/ci.yml@main
    with:
      dotnet-version: 9.0.x
      build-command: dotnet build --configuration Release
      test-command: dotnet test --configuration Release --no-build
      artifact-name: build-output
      artifact-path: src/MyApp/bin/Release/net9.0/publish
    secrets:
      token: ${{ secrets.GITHUB_TOKEN }}
```

---

### Release Workflow (`release.yml`)

Creates a GitHub Release and optionally attaches artifacts that were produced in a previous job.

**Inputs**

| Input | Type | Required | Default | Description |
|---|---|---|---|---|
| `runs-on` | string | No | `ubuntu-latest` | Runner label |
| `tag` | string | No | `${{ github.ref_name }}` | Release tag |
| `release-name` | string | No | _(tag value)_ | Display name of the release |
| `body` | string | No | _(empty)_ | Release description / changelog |
| `draft` | boolean | No | `false` | Create the release as a draft |
| `prerelease` | boolean | No | `false` | Mark the release as a pre-release |
| `artifact-name` | string | No | _(empty)_ | Name of a workflow artifact to attach |
| `artifact-path` | string | No | `release-artifacts` | Local path for the downloaded artifact |

**Secrets**

| Secret | Required | Description |
|---|---|---|
| `token` | Yes | GitHub token with permissions to create releases and upload assets |

**Outputs**

| Output | Description |
|---|---|
| `release-url` | URL of the created GitHub Release |

**Example**

```yaml
jobs:
  release:
    uses: BionicCode/workflows/.github/workflows/release.yml@main
    with:
      tag: ${{ github.ref_name }}
      release-name: Release ${{ github.ref_name }}
    secrets:
      token: ${{ secrets.GITHUB_TOKEN }}
```

---

### Lint Workflow (`lint.yml`)

Runs code-quality checks. Supports .NET format verification and Node.js/npm lint scripts.

**Inputs**

| Input | Type | Required | Default | Description |
|---|---|---|---|---|
| `runs-on` | string | No | `ubuntu-latest` | Runner label |
| `dotnet-version` | string | No | _(empty)_ | .NET SDK version. Skipped when empty. |
| `node-version` | string | No | _(empty)_ | Node.js version. Skipped when empty. |
| `dotnet-format-command` | string | No | `dotnet format --verify-no-changes` | .NET format verification command |
| `node-lint-command` | string | No | `npm run lint` | Node.js lint command |
| `working-directory` | string | No | `.` | Working directory for lint commands |

**Secrets**

| Secret | Required | Description |
|---|---|---|
| `token` | No | GitHub token for authenticated API calls |

**Example**

```yaml
jobs:
  lint:
    uses: BionicCode/workflows/.github/workflows/lint.yml@main
    with:
      node-version: '20'
```

---

### Sync Files from Manifest Workflow (`sync-files-from-manifest.yml`)

Reusable workflow that validates a JSON manifest, then verifies or synchronizes managed files in the caller repository using source-to-target mappings only.

**Stage 1 interface**

| Input | Type | Required | Default | Description |
|---|---|---|---|---|
| `manifest_json` | string | Yes | _(none)_ | JSON manifest string describing file mappings and policy values |
| `sync_branch_prefix` | string | No | `chore/sync-managed-files` | Branch prefix for generated sync PRs |

**Secrets**

| Secret | Required | Description |
|---|---|---|
| `source_token` | No | Optional read-only token for private cross-repo source reads |

**Behavior**

- On pull requests, the workflow validates the full manifest and fails if any enforced target is missing or out of sync.
- On non-PR branch events, the workflow validates the full manifest, updates only changed managed files, and opens or updates one sync PR per base branch.
- Validation happens before any sync writes.
- Stage 1 supports only `direction: source_to_target` and `managed_scope: whole_file` execution.
- Stage 1 recognizes marker-scoped policies in the schema, but fails fast with a clear v1 unsupported error if they are used.

**Manifest entry fields**

- `source_repo`
- `source_ref`
- `source_path`
- `target_path`
- `direction`
- `lifecycle_policy`
- `uniqueness_policy`
- `managed_scope`
- `markers` when `managed_scope` is `outside_markers` or `inside_markers`

**Supported Stage 1 runtime policies**

- `lifecycle_policy`: `enforce`, `seed_once`, `disabled`
- `uniqueness_policy`: `basename_unique`, `none`
- `managed_scope`: `whole_file`

**Schema values recognized but deferred at runtime in Stage 1**

- `managed_scope: outside_markers`
- `managed_scope: inside_markers`

**Stage 1 executable example**

```yaml
jobs:
  sync-managed-files:
    uses: BionicCode/workflows/.github/workflows/sync-files-from-manifest.yml@main
    with:
      manifest_json: |
        [
          {
            "source_repo": "BionicCode/bioniccode-code-style",
            "source_ref": "main",
            "source_path": ".editorconfig",
            "target_path": ".editorconfig",
            "direction": "source_to_target",
            "lifecycle_policy": "enforce",
            "uniqueness_policy": "basename_unique",
            "managed_scope": "whole_file"
          },
          {
            "source_repo": "BionicCode/bioniccode-code-style",
            "source_ref": "main",
            "source_path": "Directory.Build.props",
            "target_path": "Directory.Build.props",
            "direction": "source_to_target",
            "lifecycle_policy": "enforce",
            "uniqueness_policy": "none",
            "managed_scope": "whole_file"
          },
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
    secrets:
      source_token: ${{ secrets.SOURCE_REPO_READ_TOKEN }}
```

**Full contract example**

The Stage 1 parser already understands the fuller policy schema that Stage 2 will build on. Marker-scoped entries are valid manifest shapes, but they are not executable in Stage 1.

```json
[
  {
    "source_repo": "BionicCode/bioniccode-code-style",
    "source_ref": "main",
    "source_path": ".editorconfig",
    "target_path": ".editorconfig",
    "direction": "source_to_target",
    "lifecycle_policy": "enforce",
    "uniqueness_policy": "basename_unique",
    "managed_scope": "whole_file"
  },
  {
    "source_repo": "BionicCode/bioniccode-code-style",
    "source_ref": "main",
    "source_path": "Directory.Build.props",
    "target_path": "Directory.Build.props",
    "direction": "source_to_target",
    "lifecycle_policy": "enforce",
    "uniqueness_policy": "none",
    "managed_scope": "whole_file"
  },
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
      "start": "<!-- BEGIN REPOSITORY SPECIFICS: repository owners may edit only this section -->",
      "end": "<!-- END REPOSITORY SPECIFICS -->"
    }
  },
  {
    "source_repo": "BionicCode/template-visual-studio-repository",
    "source_ref": "main",
    "source_path": "src/AGENTS.md",
    "target_path": "src/AGENTS.md",
    "direction": "source_to_target",
    "lifecycle_policy": "enforce",
    "uniqueness_policy": "none",
    "managed_scope": "whole_file"
  },
  {
    "source_repo": "BionicCode/template-visual-studio-repository",
    "source_ref": "main",
    "source_path": ".github/copilot-instructions.md",
    "target_path": ".github/copilot-instructions.md",
    "direction": "source_to_target",
    "lifecycle_policy": "enforce",
    "uniqueness_policy": "none",
    "managed_scope": "whole_file"
  },
  {
    "source_repo": "BionicCode/template-visual-studio-repository",
    "source_ref": "main",
    "source_path": ".github/instructions/test.instructions.md",
    "target_path": ".github/instructions/test.instructions.md",
    "direction": "source_to_target",
    "lifecycle_policy": "enforce",
    "uniqueness_policy": "none",
    "managed_scope": "whole_file"
  },
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
```

**Validation rules enforced before any sync writes**

- reject malformed JSON and empty manifests
- reject duplicate normalized source identities
- reject duplicate normalized target paths
- reject basename mismatches between `source_path` and `target_path`
- reject unsupported directions
- reject unsafe repository-relative paths
- reject invalid marker combinations
- enforce repository-wide basename uniqueness only when `uniqueness_policy` is `basename_unique`

**Authentication and assumptions**

- Use optional read-only `source_token` for private cross-repo source reads.
- Otherwise use public access where possible.
- Fail clearly when a private source repository cannot be read.
- Source fetch helpers use GitHub repository contents and raw API behavior and are intended for managed text, config, and document-style files, not large binaries.
- If this reusable workflow is hosted in a private repository and consumed by another private repository, GitHub Actions access settings must allow sharing and reuse accordingly.

**Migration from the legacy `.editorconfig` workflow**

1. Switch callers from `sync-editorconfig-on-push.yml` to `sync-files-from-manifest.yml`.
2. Replace `canonical_raw_url` with `manifest_json`.
3. Represent `.editorconfig`, `Directory.Build.props`, `AGENTS.md`, and other managed files as manifest entries instead of workflow-specific logic.
4. Pass `source_token` only when private source repositories require authenticated reads.

---

### Deprecated `.editorconfig` Workflow (`sync-editorconfig-on-push.yml`)

This workflow remains available only as a temporary migration path for existing callers. New callers should use `sync-files-from-manifest.yml` instead.

---

## Versioning

It is recommended to pin callers to a specific tag or commit SHA for stability:

```yaml
uses: BionicCode/workflows/.github/workflows/ci.yml@v1.0.0
```

Using a branch name such as `@main` always picks up the latest changes on that branch.

---

## Contributing

1. Add or update a workflow file under `.github/workflows/`.
2. Keep reusable workflow interfaces typed and documented.
3. Keep reusable workflow orchestration in YAML and implementation logic in dedicated helper files when the logic grows beyond a small inline step.
4. Update this README to reflect any new or changed inputs, outputs, policies, or migration notes.
