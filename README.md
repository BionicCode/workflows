# Reusable Workflows

Central repository of reusable GitHub Actions workflows that can be called from any repository in the organization.

## Available Workflows

| Workflow | File | Description |
|---|---|---|
| CI | [`ci.yml`](.github/workflows/ci.yml) | Build and test a project, with optional artifact upload |
| Release | [`release.yml`](.github/workflows/release.yml) | Create a GitHub Release and optionally attach build artifacts |
| Lint | [`lint.yml`](.github/workflows/lint.yml) | Run code-quality checks (.NET format, Node.js/npm lint) |
| Sync .editorconfig on every push | [`sync-editorconfig-on-push.yml`](.github/workflows/sync-editorconfig-on-push.yml) | Synchronizes the Visual Studio .editorconfig file with the latest version defined in the [bionic-code-style](https://github.com/BionicCode/bioniccode-code-style) repository |

---

## Usage

Reference any workflow in this repository using the `uses` key with the format:

```
BionicCode/workflows/.github/workflows/<workflow-file>.yml@<ref>
```

where `<ref>` is a branch name (e.g. `main`), a tag, or a full commit SHA.

---

### CI Workflow (`ci.yml`)

Builds and tests a project. Supports .NET and Node.js out of the box; other runtimes can be driven by supplying custom `build-command` and `test-command` values.

**Inputs**

| Input | Type | Required | Default | Description |
|---|---|---|---|---|
| `runs-on` | string | No | `ubuntu-latest` | Runner label |
| `dotnet-version` | string | No | _(empty)_ | .NET SDK version (e.g. `9.0.x`). Skipped when empty. |
| `node-version` | string | No | _(empty)_ | Node.js version (e.g. `20`). Skipped when empty. |
| `build-command` | string | No | _(empty)_ | Shell command to build the project |
| `test-command` | string | No | _(empty)_ | Shell command to run tests |
| `working-directory` | string | No | `.` | Working directory for build/test commands |
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

**Example – .NET project**

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

**Example – Node.js project**

```yaml
jobs:
  ci:
    uses: BionicCode/workflows/.github/workflows/ci.yml@main
    with:
      node-version: '20'
      build-command: npm ci && npm run build
      test-command: npm test
      artifact-name: dist
      artifact-path: dist/
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
| `tag` | string | No | `${{ github.ref_name }}` | Release tag (e.g. `v1.2.3`) |
| `release-name` | string | No | _(tag value)_ | Display name of the release |
| `body` | string | No | _(empty)_ | Release description / changelog |
| `draft` | boolean | No | `false` | Create the release as a draft |
| `prerelease` | boolean | No | `false` | Mark the release as a pre-release |
| `artifact-name` | string | No | _(empty)_ | Name of a workflow artifact to attach. Skipped when empty. |
| `artifact-path` | string | No | `release-artifacts` | Local path for the downloaded artifact |

**Secrets**

| Secret | Required | Description |
|---|---|---|
| `token` | **Yes** | GitHub token with permissions to create releases and upload assets |

**Outputs**

| Output | Description |
|---|---|
| `release-url` | URL of the created GitHub Release |

**Example – release after CI**

```yaml
jobs:
  ci:
    uses: BionicCode/workflows/.github/workflows/ci.yml@main
    with:
      dotnet-version: 9.0.x
      build-command: dotnet publish --configuration Release --output publish/
      artifact-name: published-app
      artifact-path: publish/
    secrets:
      token: ${{ secrets.GITHUB_TOKEN }}

  release:
    needs: ci
    uses: BionicCode/workflows/.github/workflows/release.yml@main
    with:
      tag: ${{ github.ref_name }}
      release-name: Release ${{ github.ref_name }}
      artifact-name: published-app
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

**Example – .NET project**

```yaml
jobs:
  lint:
    uses: BionicCode/workflows/.github/workflows/lint.yml@main
    with:
      dotnet-version: 9.0.x
```

**Example – Node.js project**

```yaml
jobs:
  lint:
    uses: BionicCode/workflows/.github/workflows/lint.yml@main
    with:
      node-version: '20'
```

---

## Versioning

It is recommended to pin callers to a specific tag or commit SHA for stability:

```yaml
uses: BionicCode/workflows/.github/workflows/ci.yml@v1.0.0
```

Using a branch name (e.g. `@main`) always picks up the latest changes on that branch.

---

## Contributing

1. Add or update a workflow file under `.github/workflows/`.
2. Follow the existing conventions: `workflow_call` trigger, typed inputs with defaults, documented secrets and outputs.
3. Update this README to reflect any new or changed inputs/outputs.
