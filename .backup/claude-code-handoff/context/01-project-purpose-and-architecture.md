# Project purpose and architecture

## 1. Program goal

The recovery program consolidates two related automation systems:

1. manifest-driven managed-file synchronization;
2. document-metadata analysis, repair, and validation.

The desired end state is:

- `BionicCode/workflows` owns the reusable engines, engine tests, schemas, authoritative engine documentation, package templates, and installer/upgrader logic;
- caller repositories own event orchestration, permissions, caller-specific policy/manifests, and a thin generated adapter pinned to an immutable Workflows commit;
- the template repository is the first caller migration, not the implementation authority;
- duplicated caller engine/test copies are removed only after parity and live convergence are proven;
- current, planned, historical, copied, and generated documentation are distinguishable;
- every ordered recovery pass can be resumed from durable repository evidence rather than chat memory.

This is a recovery and consolidation program, not a greenfield rewrite. The backlog review found the current Workflows code to be a usable baseline. The goal is to correct authority, safety, packaging, and documentation boundaries while preserving proven behavior unless a later pass explicitly changes it.

## 2. Why two repositories and two sessions

### Session A: Workflows implementation authority

`BionicCode/workflows` is the only writable implementation repository during the W passes. It must eventually deliver an immutable release-candidate SHA.

### Session B: first caller migration

`BionicCode/template-visual-studio-repository` is migrated only after the Workflows release gate. It owns its local orchestration, permissions, policy, and generated thin wrapper. Shared-engine defects discovered during migration must be corrected in a new bounded Workflows follow-up; they must not be patched locally in the caller merely to make migration pass.

The separation exists to prevent mixed authority, circular fixes, and a state in which neither repository clearly owns behavior.

## 3. Current implementation snapshot

The following describes the implementation observed at the assessed checkout. Revalidate it against the actual task SHA.

### Managed-file sync

Current workflow: `.github/workflows/sync-files-from-manifest.yml`

Current properties:

- declares `workflow_call`;
- accepts `init`, `validate`, and `sync` commands;
- checks out the workflow implementation using `job.workflow_repository` and `job.workflow_sha`;
- runs Python implementation from the defining Workflows checkout;
- keeps caller checkout and implementation checkout separate;
- supports exact paths, globs, marker scopes, lifecycle policy, source-to-target synchronization, verification, and aggregated repair PR behavior;
- uses an optional read-only source token for private source repositories.

The initializer currently writes caller package material under `.github/sync-config/`, copies schema and documentation, creates a starter manifest only when missing, and preserves an existing caller-owned manifest. It is not yet a complete package installer or upgrader.

### Document metadata

Current workflow: `.github/workflows/doc-metadata.yml`

Current properties:

- declares `workflow_call` and `workflow_dispatch`;
- separates a trusted checkout and a working checkout;
- analyzes, optionally repairs, and post-validates metadata;
- avoids repairing fork pull requests with caller write credentials;
- runs scripts through paths such as `../trusted/.github/scripts/doc-metadata/update-doc-metadata.ps1`.

The central defect is that the `trusted` checkout is the caller/base repository, not necessarily the Workflows repository that defined the reusable workflow. A cross-repository call would therefore still execute a caller-local engine copy. The workflow is callable, but Workflows is not yet the sole executable doc-metadata authority.

### Repository maintenance orchestrator

Current workflow: `.github/workflows/repository-maintenance.yml`

Observed problems:

- it has a schedule even though Workflows is intended to remain a passive shared source;
- it contains caller-style sync orchestration;
- it calls `./.github/workflows/sync-managed-files.yml`, which is absent;
- doc-metadata routing hardcodes `main` and `master` instead of consistently using repository context.

### Current doc-metadata policy

`.github/tools/doc-metadata/doc-metadata-manifest.json` currently contains:

- a separate `documentEligibility` policy layer;
- `.txt` as an allowed extension;
- a broad `**/*.txt` include entry.

The approved future direction is simpler include-minus-exclude governance, but that is not yet current behavior. Documentation must not describe the future contract as implemented before the owning pass changes engine, schema, manifest, tests, examples, and docs together.

### Test harness

The PowerShell acceptance harness drains redirected output sequentially and uses unbounded process waiting. This can deadlock on full output pipes and cannot reliably diagnose a hung child process. A dedicated pass exists to stabilize the harness before treating later test runs as fresh executable evidence.

## 4. Approved target architecture and rationale

The backlog records the following target design. It remains subject to the current integrity review and later planning gates; do not implement unresolved details from this summary alone.

### 4.1 Workflows remains passive

Workflows must not discover descendants, broadcast updates, or run target-style scheduled synchronization. A caller explicitly invokes initialization, upgrade, metadata maintenance, or synchronization.

Why:

- caller repositories own their permissions and local policy;
- source-side broadcast creates unclear write authority;
- explicit invocation is reviewable and supports immutable pinning.

### 4.2 True reusable doc-metadata engine

The intended public call is conceptually:

```yaml
uses: BionicCode/workflows/.github/workflows/doc-metadata-reusable.yml@<full-commit-sha>
```

The called workflow runs in caller context but checks out its executable implementation with:

```yaml
repository: ${{ job.workflow_repository }}
ref: ${{ job.workflow_sha }}
```

It separately checks out:

- trusted caller base/default state;
- caller working PR head or branch state.

Why:

- the caller's token and permissions remain caller-owned;
- executable engine code comes from the immutable Workflows reference;
- untrusted PR content is not executed as engine code;
- the same implementation can serve Workflows itself and external callers.

### 4.3 Generated thin caller wrapper

Each caller receives a small local wrapper, such as `doc-metadata-caller.yml`, that:

- contains no engine logic;
- contains a generated-file notice;
- forwards only the approved interface;
- invokes the reusable Workflows implementation at a literal full SHA;
- is installer-managed rather than manually edited.

Why:

- GitHub does not permit expressions in `jobs.<job_id>.uses`, so a dynamic SHA cannot be substituted at runtime;
- a literal SHA gives an auditable immutable dependency;
- the caller orchestrator keeps a stable local call path while upgrades remain explicit.

### 4.4 Coherent package init/upgrade

The intended installer commands are:

```text
init
upgrade
validate-installation
```

The package identity must tie together:

- wrapper pin;
- copied schema;
- copied authoritative documentation;
- package metadata;
- managed sync entries;
- default caller manifest behavior.

The default caller manifest is `seed_once`: created when absent and caller-owned afterward. Engine scripts and engine tests are never copied as package content.

Why:

- schema or docs must not silently move ahead of the engine pinned by the wrapper;
- one reviewable PR provides rollback and coherent version review;
- structural manifest edits preserve unrelated caller entries and reject conflicts instead of performing blind text insertion.

### 4.5 One sync authority classifier and ownership plan

Only the sync subsystem interprets the sync manifest, expands sources, determines lifecycle, and classifies write/version authority. It publishes a closed, versioned ownership plan. Doc-metadata consumes that plan rather than reimplementing marker or sync semantics.

Why:

- two independent classifiers can disagree about who owns a file;
- disagreement creates sync/doc-metadata ping-pong;
- a closed plan gives one auditable decision boundary and enables fail-closed validation.

Target authority model:

| Sync classification | Canonical version authority | Doc-metadata behavior |
|---|---|---|
| External source with `enforce` | Source repository | Skip the entire target file |
| Exact self-canonical `enforce` | Current repository | Allow local metadata governance; sync is a no-op |
| `seed_once`, target missing | Source for initial creation | Reserve until created |
| `seed_once`, target exists | Target repository | Allow local metadata governance |
| `disabled` | Target/no active sync authority | Allow normal metadata governance |

`Version` records the canonical source document revision. It is not a conflict-resolution score or merge priority. Local overlay edits remain visible in Git history without creating a second canonical version counter in the first product version.

### 4.6 Manifest governance

Approved future formula:

```text
governedFiles = files matching include minus files matching exclude
```

Planned consequences:

- remove `documentEligibility`;
- remove the repository-wide `**/*.txt` include;
- explicitly included unsupported/binary/invalid-UTF-8 content fails clearly;
- presentation settings do not decide governance.

The change is intentionally one contract pass across implementation, schema, manifest, tests, examples, API/type docs, and migration diagnostics.

### 4.7 Workflow role naming

Target suffixes expose architecture in filenames:

- `-orchestrator.yml`: repository-local event-triggered coordinator;
- `-caller.yml`: thin repository-local adapter;
- `-reusable.yml`: called implementation declaring `workflow_call`.

Renaming a reusable workflow is a public contract migration because external callers reference the literal path. The roadmap therefore separates planning the complete map and compatibility policy from applying a behavior-preserving rename.

## 5. Important unresolved design work

An independent strategy review identified useful questions that were not yet incorporated into the backlog. Its W2 conclusion was later undermined by the missed hallucinated allowlist, so treat all recommendations as hypotheses for independent validation:

- whether runtime policy comes from trusted base or working tree;
- resolving every mutable source ref once to an immutable source commit;
- target/base/head identity and trusted-policy digest in the ownership plan;
- canonical plan serialization, digest, transport, size limit, and attestation;
- exact first-install bootstrap at the release-candidate SHA;
- package staging, atomic promotion, downgrade, concurrency, and partial-failure behavior;
- immutable action/dependency references for write-capable release paths;
- GitHub.com versus GitHub Enterprise Server support boundary;
- whether manifest-governance correction should move earlier to avoid implementing obsolete `documentEligibility` behavior first.

Claude should review these against current GitHub capabilities, repository implementation, and roadmap dependencies rather than adopting them automatically.
