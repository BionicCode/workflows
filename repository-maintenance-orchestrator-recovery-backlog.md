# Repository Maintenance Recovery Backlog

- Historical review snapshot date: 2026-07-11
- Backlog authority: authoritative recovery roadmap and project-state record
- Current execution state: resolved separately at the start of each authorized task; the historical snapshot below is not an execution lease
- Primary implementation repository: `BionicCode/workflows`
- First caller migration repository: `BionicCode/template-visual-studio-repository`

## 1. Purpose and authority

This backlog is the authoritative ordered roadmap and project-state record for recovering and consolidating managed-file synchronization and document-metadata automation.

It records:

- the reviewed repository state;
- approved architecture and product conventions;
- confirmed defects and unverified areas;
- the only allowed pass order;
- exact repository/session boundaries;
- per-pass scope, validation, stop conditions, and review gates;
- the evidence required before later passes unlock.

The supporting authorities are:

- [backlog-workflow-documentation.md](backlog-workflow-documentation.md) for the reusable pass lifecycle, admission, handoff, and orchestration rules;
- [evidence-ledger-documentation.md](evidence-ledger-documentation.md) for ledger columns, states, transitions, and evidence invariants;
- [repository-review-protocol.md](repository-review-protocol.md) for repository evidence, start, stop, validation, and review gates;
- [AGENTS.md](AGENTS.md), [AGENT_GUARDRAILS.md](AGENT_GUARDRAILS.md), [DOCUMENTATION.md](DOCUMENTATION.md), and any applicable path-specific instruction file for repository execution and documentation rules.

This file does not authorize repository or GitHub writes by itself. Every activated pass, in every task mode, requires current user authorization and an authorized execution handoff that supplies the exact runtime scope and lease.

## 2. Reviewed immutable state

### `BionicCode/workflows`

Reviewed `main`:

```text
fbdd7ff310a42b58a25757407ed81537e2fa066b
```

### `BionicCode/template-visual-studio-repository`

Reviewed `main`:

```text
dd569d77b46e0198185958cda865118b8508b7d6
```

Open automation PRs at the reviewed target state:

- PR #34: sync branch, currently zero changed files;
- PR #35: doc-metadata repair branch created before ownership convergence.

Both repositories must be re-resolved at the start of every pass. A moving automation branch is evidence, not a new roadmap baseline.

## 3. Full review verdict for the Workflows version

### 3.1 Usable baseline

The Workflows copy is a valid starting implementation and must not be rewritten from scratch.

At the reviewed commits, the following core blobs are identical between Workflows and the template repository:

| Surface | Blob SHA |
|---|---|
| `.github/workflows/doc-metadata.yml` | `7e9f28c9258079fa0953723b8cd584e69d01a41a` |
| `.github/scripts/doc-metadata/update-doc-metadata.ps1` | `8d46e585df9df83337a152f6e84bfb05602e302a` |
| `.github/scripts/doc-metadata/resolve-content-change-links.ps1` | `94f2900b6b93210e8ad7ea360c28faa46174d73d` |
| `.github/scripts/doc-metadata/tests/Invoke-DocMetadataAcceptanceTests.ps1` | `b84f5508c3214da05854ce2362c19810ef4efff3` |
| `.github/tools/doc-metadata/doc-metadata-manifest.schema.json` | `28dc0bb7fbe1d9d4c3f50f1c74f4d894f1e73f12` |

No manual “copy newer code into Workflows” step is required before implementation begins.

Documentation and repository-specific manifests are not assumed identical or interchangeable.

### 3.2 Confirmed defects and readiness gaps

1. **Not yet a centrally authoritative engine.**  
   `.github/workflows/doc-metadata.yml` already supports `workflow_call`, but it checks out the caller/default repository as `trusted` and executes:

   ```text
   ../trusted/.github/scripts/doc-metadata/update-doc-metadata.ps1
   ```

   In a cross-repository call, that would still execute a caller-local engine copy. The reusable workflow must instead check out its own defining repository and commit through `job.workflow_repository` and `job.workflow_sha`, while separately checking out caller trusted state and caller working state.

2. **Broken Workflows self-orchestrator.**  
   `.github/workflows/repository-maintenance.yml` contains target-style sync orchestration and calls:

   ```text
   ./.github/workflows/sync-managed-files.yml
   ```

   That file is absent in `BionicCode/workflows`. The workflow also has a schedule and hardcoded `main`/`master` doc-metadata routing. Workflows must remain passive as a shared source and must not contain target-style sync orchestration.

3. **Initializer destination mismatch.**  
   `.github/scripts/sync-files-from-manifest/init_manifest.py` writes to:

   ```text
   .github/sync-config/
   ```

   The current caller wrapper reads:

   ```text
   .github/tools/sync-config/sync-manifest.json
   ```

   The initializer cannot be extended safely until one canonical caller path is approved and all code, schema references, documentation, fixtures, and examples use it.

4. **Initializer is not a package installer.**  
   The current `init` behavior installs only sync schema, starter manifest, and sync documentation. It cannot yet:

   - install a thin doc-metadata wrapper;
   - render a pinned reusable-workflow SHA;
   - install doc-metadata schema/docs/default manifest;
   - structurally add or update managed entries in an existing sync manifest;
   - distinguish caller-owned seed files from continuously managed package files;
   - upgrade an existing installation safely.

5. **Literal pinning requires generated wrapper content.**  
   GitHub does not allow contexts or expressions in `jobs.<job_id>.uses`. A caller wrapper therefore needs a literal ref. The installer must render the exact approved Workflows commit SHA into the wrapper. The wrapper cannot be treated as a plain byte-for-byte source file while also remaining immutably pinned.

6. **Documentation is not ready to drive Codex.**

   Confirmed examples:

   - Workflows `README.md` does not list doc-metadata in its reusable-workflow table.
   - Sync documentation still describes `.github/sync-config/`, conflicting with the current caller wrapper.
   - Current doc-metadata documentation describes current output forms containing `Changes:` and unquoted current links that conflict with the approved future canonical format.
   - Documentation still presents `documentEligibility` as supported configuration.
   - Workflows and template doc-metadata documentation have diverged.
   - Planned, current, and historical behavior are not consistently labelled.

7. **The PowerShell acceptance harness is not execution-safe.**  
   `Invoke-Process` drains stdout and stderr sequentially and calls unbounded `WaitForExit()`. This can hang on a full redirected pipe and has no finite child-process timeout.

8. **Manifest governance is overly broad and duplicated.**  
   The current Workflows doc-metadata manifest contains both:

   - an independent `documentEligibility` policy layer; and
   - a repository-wide `**/*.txt` include.

   Approved behavior is include-minus-exclude selection, with explicitly included unprocessable files failing clearly.

9. **Cross-engine ownership is unresolved.**  
   Active external `enforce` ownership can cause sync/doc-metadata ping-pong. Canonical version authority must be derived from sync authority before caller migration.

10. **Self-canonical entries are not explicitly classified.**  
    Exact same-repository, same-ref, same-source-path, same-target-path operations must be recognized as canonical no-ops. Same-repository different-path copies remain real sync operations.

11. **No release/install/upgrade contract exists.**  
    There is no approved model tying together:

    - reusable workflow commit;
    - generated wrapper pin;
    - copied schema;
    - copied documentation;
    - default manifest version;
    - managed sync entries;
    - package upgrade PR.

12. **Current static and historical evidence is not a fresh executable baseline.**  
    The complete PowerShell acceptance suite and parser validation must be rerun after harness stabilization. Generic YAML parsing is not GitHub Actions semantic validation.

## 4. Approved architecture

### 4.1 Repository roles

`BionicCode/workflows` owns:

- the only active doc-metadata engine;
- the reusable doc-metadata workflow;
- engine tests;
- authoritative schema;
- authoritative engine, manifest, API, and type documentation;
- package templates and installer logic;
- sync engine, sync schema, tests, and documentation;
- ownership-plan contract and generator.

Each caller repository owns:

- the event-triggering top-level orchestration;
- execution permissions;
- caller-specific manifests;
- repository-specific policy and examples;
- a generated thin local wrapper;
- local copied schema and documentation for discoverability/editor support.

Workflows never discovers or broadcasts to descendants. A caller explicitly invokes initialization, upgrade, metadata maintenance, or synchronization.

### 4.2 True reusable doc-metadata workflow

The authoritative reusable workflow must be callable as:

```yaml
uses: BionicCode/workflows/.github/workflows/doc-metadata-reusable.yml@<full-commit-sha>
```

The called workflow executes in caller context but checks out its implementation from:

```yaml
repository: ${{ job.workflow_repository }}
ref: ${{ job.workflow_sha }}
```

It separately checks out:

- trusted caller base/default state;
- caller working PR head or branch state.

No executable engine script may be loaded from an untrusted PR head.

### 4.3 Thin local wrapper

Initialization installs a small local wrapper, for example:

```text
.github/workflows/doc-metadata-caller.yml
```

The wrapper:

- contains no engine logic;
- contains a generated notice;
- forwards the approved input/secret contract;
- calls the Workflows reusable workflow at a literal full SHA;
- is installer-managed and not manually edited.

The local top-level orchestrator calls this wrapper through:

```yaml
uses: ./.github/workflows/doc-metadata-caller.yml
```

This preserves a stable local interface while keeping one implementation authority.

### 4.4 Installation and upgrade model

The Workflows repository must expose a reusable repository-tool installer with an explicit `init` command. The exact filename may be selected in Plan Mode, but the public contract must distinguish:

```text
command=init
command=upgrade
command=validate-installation
```

`init` and `upgrade` create or update one reviewable caller PR.

The installer must render the exact called Workflows commit SHA into the thin wrapper. Re-running the installer at a newer SHA is the controlled upgrade mechanism.

The initializer installs or updates, as one coherent package version:

- generated thin wrapper;
- caller-owned default doc-metadata manifest when missing;
- local schema copy;
- local human documentation;
- package metadata needed for validation;
- structurally managed sync-manifest entries where applicable.

It must not copy:

- the PowerShell engine;
- the resolver engine;
- engine tests;
- another full reusable workflow implementation.

### 4.5 Package ownership and lifecycle

| Installed surface | Ownership/lifecycle |
|---|---|
| Thin wrapper with literal Workflows SHA | installer-managed generated file |
| Authoritative schema copy | package-managed; must match wrapper engine commit |
| Authoritative documentation copy | package-managed; must match wrapper engine commit |
| Default caller doc-metadata manifest | `seed_once`; caller-owned after creation |
| Caller-specific examples/configuration | caller-owned |
| PowerShell engine/tests | never copied |

Schema and documentation must never update independently to a newer engine contract while the wrapper still pins an older engine.

### 4.6 Sync/version authority

The ownership plan is generated only by sync logic and consumed by doc-metadata as a closed, versioned contract.

Doc-metadata must not parse sync marker semantics or reinterpret the sync manifest.

Version authority:

| Sync classification | Canonical version authority | Target doc-metadata |
|---|---|---|
| External source + `enforce` | source repository | skip entire file |
| Exact self-canonical `enforce` no-op | current repository | allowed |
| `seed_once`, target missing | source for creation | reserve until created |
| `seed_once`, target exists | target repository | allowed |
| `disabled` | target/no active sync authority | allowed |

For the first viable product:

- a descendant `AGENTS.md` with repository-specific marker content is skipped by doc-metadata when the canonical source has active external `enforce` authority;
- local marker edits remain represented by Git history;
- `Version` represents the canonical source document revision;
- no separate local-overlay version is created;
- `Version` is never merge priority.

### 4.7 Manifest governance

Approved public formula:

```text
governedFiles = files matching include minus files matching exclude
```

Rules:

- no include match means not governed;
- exclude subtracts from include;
- presentation settings do not determine governance;
- remove `documentEligibility`;
- explicitly included unsupported, binary/NUL-containing, or invalid-UTF-8 files fail clearly;
- remove repository-wide `**/*.txt`;
- critical files should be explicit;
- globs are appropriate only for directories intentionally dedicated to governed documentation.

### 4.8 Documentation is a product contract

Every behavior pass is incomplete unless implementation, tests, schema, manifests, examples, and human documentation agree.

Required documentation layers:

1. workflow overview/README;
2. manifest tutorial and recipes;
3. manifest API reference;
4. individual type/property reference;
5. architecture/design decisions for non-obvious conventions.

Documentation must explain reasons and conventions, including:

- caller authority versus definition authority;
- source-to-target only;
- source configuration, not inferred ancestry, establishes authority;
- canonical version ownership;
- `enforce` versus `seed_once`;
- marker ownership;
- exact self-canonical no-op;
- why wrapper pin upgrades are explicit;
- why `Version` is not conflict resolution;
- why local overlay edits do not increment a canonical source version.

Use GitHub callouts and human-oriented examples. Do not expose implementation internals as a substitute for conceptual documentation.

### 4.9 Workflow file-role naming

Workflow filenames must expose their architectural role without requiring the reader to inspect YAML internals.

Use these suffixes:

| Suffix | Meaning |
|---|---|
| `-orchestrator.yml` | repository-local, event-triggered top-level workflow that coordinates maintenance jobs |
| `-caller.yml` | thin repository-local adapter whose primary responsibility is invoking a reusable workflow |
| `-reusable.yml` | called implementation workflow that declares `workflow_call` |

Approved target names:

| Current or planned role | Canonical filename |
|---|---|
| repository maintenance orchestration | `.github/workflows/repository-maintenance-orchestrator.yml` |
| managed-file sync caller adapter | `.github/workflows/sync-managed-files-caller.yml` |
| shared manifest-driven sync implementation | `.github/workflows/sync-files-from-manifest-reusable.yml` |
| doc-metadata caller adapter | `.github/workflows/doc-metadata-caller.yml` |
| shared doc-metadata implementation | `.github/workflows/doc-metadata-reusable.yml` |

A filename migration is incomplete until every literal path reference is updated and validated, including references in:

- workflow `uses:` clauses;
- scripts and package templates;
- tests and fixtures;
- manifests or generated-file definitions;
- README files, tutorials, API/type references, examples, and migration documentation.

Because a cross-repository reusable-workflow reference contains the exact workflow path, externally consumed old paths require an explicit compatibility and removal plan. A rename must not silently break existing callers.

## 5. Session separation

### Session A — Workflows implementation

Writable repository:

```text
BionicCode/workflows
```

No template-repository implementation files may be changed during this session.

Session A must deliver:

- authoritative reusable doc-metadata engine;
- safe harness and fresh tests;
- package-aware initializer/upgrader;
- generated thin wrapper template/renderer;
- sync ownership plan;
- canonical version authority enforcement;
- exact self-canonical no-op;
- corrected manifest governance;
- canonical links and tamper evidence;
- current authoritative documentation;
- a tested immutable Workflows release candidate SHA.

### Session B — Template caller migration

Writable repository:

```text
BionicCode/template-visual-studio-repository
```

Session B cannot start until the Session A release gate is accepted and records an exact Workflows commit SHA.

Session B must:

- run the approved initializer/upgrade against the template caller;
- install the generated wrapper and package surfaces;
- preserve caller-owned manifest policy;
- switch orchestration to the wrapper;
- prove parity and convergence;
- remove duplicated engine/test files only after proof;
- clean stale automation PR state;
- leave a short pointer to the authoritative Workflows backlog/protocol.

Do not mix Workflows engine changes into Session B. A defect in the shared engine reopens a bounded Workflows pass and produces a new release candidate SHA before migration resumes.

## 6. Ordered roadmap

The order below is mandatory.

### Lifecycle and state authority

Apply the lifecycle and handoff rules in [backlog-workflow-documentation.md](backlog-workflow-documentation.md), the state and evidence rules in [evidence-ledger-documentation.md](evidence-ledger-documentation.md), and the start, stop, and integrity gates in [repository-review-protocol.md](repository-review-protocol.md).

For this recovery, pass-completion checkboxes and the evidence ledger are maintainer-controlled state. They may change only through current user authorization that explicitly permits the exact coordination update. Execution, validation, or self-review alone does not complete a pass or unlock later work. The task-specific execution handoff supplies the literal pre-pass baseline and runtime lease.

### Ordered pass index

This index is navigation, not a second evidence ledger. The status values mirror the authoritative ledger in section 9.

| ID | Title | Mode | Immediate dependency | Status |
|---|---|---|---|---|
| W0 | Adopt authoritative coordination files | coordination | — | Completed |
| W1 | Documentation authority and current-state audit | review-only | W0 | Completed |
| W2 | Stabilize current-state documentation before Codex implementation | implementation | W1 | Pending |
| W2A | Approve workflow role naming and migration map | planning | W2 | Locked |
| W2B | Apply workflow filename and reference migration | implementation | W2A | Locked |
| W3 | Contain broken Workflows self-orchestration | implementation | W2B | Locked |
| W4 | Stabilize the PowerShell acceptance harness | implementation | W3 | Locked |
| W5 | Establish fresh executable baseline | validation-only | W4 | Locked |
| W6 | Approve the reusable workflow and package contract | planning | W5 | Locked |
| W7 | Convert doc-metadata into the authoritative reusable engine | implementation | W6 | Locked |
| W8 | Implement package-aware init/upgrade | implementation | W7 | Locked |
| W9 | Implement one shared sync authority classifier | implementation | W8 | Locked |
| W10 | Make sync execution consume the classifier | implementation | W9 | Locked |
| W11 | Expose the read-only ownership plan | implementation | W10 | Locked |
| W12 | Enforce exclusive canonical version authority | implementation | W11 | Locked |
| W13 | Prove cross-engine convergence in fixtures | validation-only | W12 | Locked |
| W14 | Correct manifest governance | implementation | W13 | Locked |
| W15 | Canonical links | implementation | W14 | Locked |
| W16 | Complete protected-field tamper coverage | implementation | W15 | Locked |
| W17 | Workflows release-candidate certification | validation-only | W16 | Locked |
| T0 | Resolve and quarantine caller documentation | implementation | W17 | Locked |
| T1 | Run package init/upgrade on a migration branch | migration | T0 | Locked |
| T2 | Shared-versus-local parity gate | validation-only | T1 | Locked |
| T3 | Switch orchestration to the thin wrapper | migration | T2 | Locked |
| T4 | Prove live caller convergence | validation-only | T3 | Locked |
| T5 | Remove duplicated caller engine | migration | T4 | Locked |
| T6 | Clean stale automation state | coordination | T5 | Locked |

### Project-specific historical exception

W0 and W1 were accepted before this backlog adopted the normalized pass template. Their original inline specifications intentionally remain historical and are not reopened or rewritten merely because they omit fields introduced later. This presentation exception does not waive ledger integrity or permit accepted historical evidence to be changed or recorded inaccurately.

# Session A — `BionicCode/workflows`

## W0 — Adopt authoritative coordination files

- [x] **Completed**

**Goal:** adopt the authoritative recovery backlog and review protocol, and establish the repository-specific implementation-handoff and protected-control-plane rules.

**Allowed files:**

- `AGENTS.md`
- `repository-maintenance-orchestrator-recovery-backlog.md`
- `repository-review-protocol.md`

**Validation:**

- exactly three files changed;
- changes to `AGENTS.md` are limited to `REPOSITORY SPECIFICS`;
- no competing active roadmap exists in Workflows;
- current state is clearly distinguished from approved future state;
- protected control-plane and maintainer-only status rules are consistent across all three files;
- links and Markdown render correctly;
- `git diff --check`.

**Review gate:** maintainer approves exact three-file diff.

---

## W1 — Documentation authority and current-state audit

- [x] **Completed**

**Mode:** review-only.

**Goal:** inventory every potentially normative Markdown file in Workflows and classify it as:

- current normative guidance;
- current product documentation;
- copied/generated documentation;
- historical evidence;
- planned behavior;
- stale/contradictory;
- non-normative background.

**Required review scope:**

- root `README.md`;
- root `AGENTS.md`, `AGENT_GUARDRAILS.md`, and `DOCUMENTATION.md`;
- nested `AGENTS.md` and `AGENTS.override.md` files;
- `.github/copilot-instructions.md` and `.github/instructions/**/*.instructions.md`;
- workflow documentation;
- doc-metadata documentation tree;
- sync documentation tree;
- schema-linked references;
- examples and templates.

**Output:** dated audit table with file, authority, implementation match, contradictions, and required owning pass.

**Stop condition:** repository HEAD changes.

---

## W2 — Stabilize current-state documentation before Codex implementation

- [ ] **Completed**

**Mode:** implementation (documentation-only).

**Objective:** make the maintainer-approved W1 documentation set accurately describe current repository behavior, clearly separate planned and historical behavior, and remove or quarantine guidance that could cause Codex or a human contributor to implement stale behavior.

**Rationale:** W1 identified potentially normative Markdown whose authority or implementation match must be corrected before semantic workflow work begins. Stabilizing those surfaces first prevents stale documentation from driving later implementation while preserving the approved technical roadmap.

**Dependencies:**

- W1 is accepted, closed, and fully recorded in the evidence ledger;
- the W1 audit result and maintainer-approved W2 allowlist below are the scope authority for this pass;
- a separate authorized W2 execution handoff supplies the exact repository state and execution lease.

**Scope:**

- repository: `BionicCode/workflows`;
- read-only inspection may cover repository content needed to verify current behavior;
- modifications are limited to the exact Markdown paths below.

**Allowed files:**

| Path | W2 write constraint |
|---|---|
| `README.md` | Current-state product and repository documentation only. |
| `AGENTS.md` | `REPOSITORY SPECIFICS` only. |
| `AGENT_GUARDRAILS.md` | Repository-specific overlay only. |
| `DOCUMENTATION.md` | Repository-specific overlay only. |
| `.github/copilot-instructions.md` | Repository-specific overlay only. |
| `.github/instructions/code-review.instructions.md` | Repository-specific overlay only. |
| `.github/instructions/tests.instructions.md` | Repository-specific overlay only. |
| `src/AGENTS.md` | Repository-specific overlay only. |
| `test/AGENTS.md` | Repository-specific overlay only. |
| `.github/scripts/doc-metadata/README.md` | Current-state documentation only; planned behavior must be explicitly labelled. |
| `.github/scripts/doc-metadata/tests/README.md` | Current-state documentation only; planned behavior must be explicitly labelled. |
| `.github/scripts/sync-files-from-manifest/README.md` | Current-state documentation only; planned behavior must be explicitly labelled. |
| `.github/tools/doc-metadata/README.md` | Current-state documentation only; planned behavior must be explicitly labelled. |
| `.github/tools/doc-metadata/api-reference.md` | Current-state documentation only; planned behavior must be explicitly labelled. |
| `.github/tools/doc-metadata/type-reference.md` | Current-state documentation only; planned behavior must be explicitly labelled. |
| `.github/tools/sync-config/README.md` | Current-state documentation only; planned behavior must be explicitly labelled. |

This is the exact maintainer-approved W1 allowlist for W2. Files outside this table are not writable in W2.

**Prohibited files and scope:**

- every path outside the exact allowlist, including this backlog, the evidence-ledger documentation, and the review protocol;
- workflow, script, schema, manifest, installer, executable test, fixture, or package implementation;
- shared copied instruction baselines outside the designated repository-specific overlays;
- new documentation paths or an independently edited copy whose authoritative source requires a coordinated change.

**Required outputs:**

- corrected or quarantined stale and contradictory statements within the allowlist;
- explicit current, planned, historical, copied, and generated labels wherever authority or timing could otherwise be confused;
- human-oriented concepts, callouts, and cross-links needed to understand current behavior without presenting future architecture as implemented;
- an execution report that accounts for every allowlisted path, including paths intentionally left unchanged.

**Required invariants:**

- current-behavior claims match the exact repository state leased to W2;
- planned callable-authority, packaging, ownership, migration, and other future behavior remains explicitly planned;
- copied documentation is not edited independently of its authority;
- shared copied instruction baselines remain unchanged and only repository-specific overlays may vary;
- approved architecture, product behavior, pass order, pass identity, and accepted W0/W1 evidence remain unchanged;
- W2A and every later pass remain `Locked`.

**Non-goals:**

- implementing or changing workflow, script, schema, manifest, installer, package, fixture, or executable test behavior;
- deciding the W2A workflow naming and migration map;
- rewriting shared copied instruction baselines;
- widening the W1 allowlist, creating a new technical roadmap, or extracting specifications into new files;
- completing, closing, unlocking, or activating W2, W2A, or any later pass.

**Acceptance criteria:**

- each of the 16 allowlisted paths is accounted for and any changed statement is supported by current repository evidence;
- reading the applicable allowlisted Markdown cannot reasonably confuse current, planned, historical, copied, or generated behavior;
- instruction-file changes, if any, are confined to the named repository-specific overlays;
- the complete diff is documentation-only, remains inside the exact allowlist, and preserves all required invariants;
- required callouts and links are understandable to a human reader and resolve correctly.

**Validation:**

- compare every current-behavior statement changed by W2 with the exact leased repository implementation;
- account for all 16 allowlisted paths and verify the changed-file set is a subset of that list;
- inspect copied instruction diffs against their repository-specific overlay boundaries;
- validate Markdown structure and relative links for every changed file;
- search changed documentation for unlabelled future behavior and stale current-state claims;
- run `git diff --check`;
- review the complete diff against the W1 audit and this pass contract.

**Stop conditions:**

- a required correction needs a path outside the exact allowlist or a shared copied baseline change;
- current behavior cannot be established from the leased repository state;
- a product, architecture, naming, authority, or migration decision is required;
- documentation and implementation cannot be made accurate without changing executable behavior;
- the leased repository state changes, unrelated worktree changes appear, or another applicable instruction conflicts with this scope.

**Review gate:** the maintainer independently approves the exact documentation diff, the 16-path accounting, current-versus-planned classification, overlay-boundary review, link checks, and complete execution report.

**Follow-up effect:** after W2 is independently accepted, closed, and fully finalized, W2A may become eligible for separate preparation and activation. W2 does not activate or unlock W2A or any later pass.

---

## W2A — Approve workflow role naming and migration map

- [ ] **Completed**

**Mode:** Plan Mode; no repository edits.

**Goal:** approve the complete behavior-preserving workflow filename migration before semantic workflow implementation begins.

**Required output:**

- the binding `orchestrator`, `caller`, and `reusable` role definitions from section 4.9;
- the exact old-to-new filename map;
- a repository-wide inventory of every literal old-path reference;
- the exact W2B file allowlist;
- compatibility treatment for externally referenced old reusable-workflow paths;
- deprecation and eventual removal criteria for compatibility entry points;
- validation and rollback steps.

**Stop conditions:**

- any workflow's architectural role remains ambiguous;
- an external caller cannot be inventoried or protected by compatibility;
- the migration would require a semantic trigger, permission, input/output, job-graph, or script behavior change.

**Review gate:** maintainer approves the filename map, reference inventory, compatibility plan, and exact W2B allowlist.

---

## W2B — Apply workflow filename and reference migration

- [ ] **Completed**

**Goal:** apply the approved W2A filename migration as a behavior-preserving preparation pass before functional workflow implementation.

**Allowed files:** exactly the files approved by W2A. Protected control-plane files remain read-only unless the current task explicitly names and authorizes them.

**Required behavior:**

- rename workflow files to their canonical role-suffixed names;
- update every workflow, script, test, fixture, manifest/template, and documentation reference to the new paths;
- preserve triggers, permissions, inputs, outputs, secrets, conditions, job dependencies, concurrency, and executed scripts;
- retain an explicitly documented compatibility entry point when an existing cross-repository caller still references an old reusable-workflow path;
- add no unrelated cleanup or functional behavior change;
- leave no unexplained stale reference to a retired filename.

**Validation:**

- repository-wide literal-reference search for every old filename;
- YAML parse;
- `actionlint` or equivalent semantic workflow lint;
- caller-to-reusable reference matrix;
- compatibility caller fixture where required;
- Markdown link/reference validation;
- `git diff --check`;
- complete rename-only diff review.

**Stop conditions:**

- a semantic behavior change is required;
- an external caller would break without an unapproved compatibility mechanism;
- the exact W2A allowlist is insufficient.

**Review gate:** maintainer accepts a behavior-preserving filename/reference migration before W3 begins.

---

## W3 — Contain broken Workflows self-orchestration

- [ ] **Completed**

**Goal:** eliminate the missing local sync-workflow call and autonomous source-side schedule.

**Expected file:**

- `.github/workflows/repository-maintenance-orchestrator.yml`

**Required behavior:**

- no call to an absent `.github/workflows/sync-managed-files-caller.yml`;
- no source-side sync broadcast;
- no schedule;
- local self-maintenance only;
- default branch derived from repository context;
- repair-branch recursion guard preserved.

This pass may temporarily retain the current local doc-metadata call until W6 replaces it with the authoritative local reusable path.

**Validation:**

- YAML parse;
- `actionlint` or equivalent;
- exact trigger/job matrix;
- live expected run;
- no zero-job scheduled run.

---

## W4 — Stabilize the PowerShell acceptance harness

- [ ] **Completed**

**Goal:** make tests bounded and deadlock-resistant without changing product assertions.

**Allowed file:**

- `.github/scripts/doc-metadata/tests/Invoke-DocMetadataAcceptanceTests.ps1`

**Required behavior:**

- concurrent stdout/stderr draining;
- finite per-process timeout;
- process-tree termination where supported;
- START/PASS/FAIL output;
- timeout diagnostics;
- cleanup in `finally`;
- high-output deadlock witness;
- intentional timeout witness.

**Validation:**

- PowerShell parser;
- harness self-tests;
- complete suite twice;
- no production file changed.

---

## W5 — Establish fresh executable baseline

- [ ] **Completed**

**Mode:** validation-only.

Required:

```text
PowerShell parser for all doc-metadata scripts
doc-metadata acceptance suite twice
sync Python unit suite
JSON Schema validation
YAML parse
actionlint or equivalent
Markdown relative-link validation
git diff --check
```

Record runtime versions and exact commit.

Any failure becomes a separate bounded pass. Historical green runs do not replace this gate.

---

## W6 — Approve the reusable workflow and package contract

- [ ] **Completed**

**Mode:** Plan Mode.

Must specify:

- canonical role-suffixed workflow filenames and compatibility paths approved by W2A/W2B;
- stable caller inputs, secrets, outputs, and permissions;
- caller/base/head checkout matrix;
- Workflows self-checkout through `job.workflow_repository`/`job.workflow_sha`;
- fork behavior;
- repair branch behavior;
- local Workflows self-call;
- wrapper schema and generated notice;
- literal SHA rendering;
- package file list;
- canonical caller paths;
- init/upgrade/validate commands;
- package version identity;
- manifest structural merge rules;
- conflicts and rollback;
- documentation layout;
- release candidate process.

**Critical decision:** approve one canonical sync configuration path. The current `.github/sync-config` versus `.github/tools/sync-config` mismatch must end here.

---

## W7 — Convert doc-metadata into the authoritative reusable engine

- [ ] **Completed**

**Goal:** make Workflows the only executable engine authority.

**Expected files:**

- `.github/workflows/doc-metadata-reusable.yml`
- `.github/workflows/repository-maintenance-orchestrator.yml` only for final local self-call
- `.github/scripts/doc-metadata/**`
- `.github/tools/doc-metadata/**`
- focused docs and tests required by the public contract

**Required behavior:**

- reusable workflow obtains engine from `job.workflow_repository` and `job.workflow_sha`;
- caller trusted and working trees are separate;
- no caller-local engine script is executed;
- caller `github` context and token authority remain intact;
- permissions cannot be elevated;
- Workflows local self-maintenance calls the same authoritative implementation;
- public interface is closed and documented;
- workflow dispatch behavior is either removed from the reusable engine or explicitly separated into a local top-level caller.

**Validation:**

- full PowerShell suite twice;
- caller checkout fixture matrix;
- fork read-only case;
- same-repository repair case;
- branch/push/manual cases;
- workflow semantic lint;
- live Workflows self-call.

---

## W8 — Implement package-aware init/upgrade

- [ ] **Completed**

**Goal:** install a coherent doc-metadata caller package through an explicit init command.

**Expected surfaces:**

- reusable installer workflow;
- package renderer/installer script;
- wrapper template;
- package tests;
- sync-init path corrections;
- authoritative installation documentation.

**Required installer behavior:**

- `init`, `upgrade`, and `validate-installation`;
- checks out caller and exact Workflows implementation commit;
- renders literal `job.workflow_sha` into wrapper;
- creates one PR;
- preserves caller-owned manifest when present;
- creates default doc manifest only when missing;
- installs matching schema/docs;
- structurally creates or updates approved sync entries;
- preserves unrelated caller sync entries;
- rejects conflicting managed entries;
- idempotent second run is no-op;
- upgrade from SHA A to SHA B changes all package surfaces coherently;
- never copies engine or tests;
- never silently writes directly to protected default branch.

**Important:** the wrapper is installer-managed, not ordinary byte-for-byte sync content. Schema/docs entries must remain tied to the same pinned package SHA.

---

## W9 — Implement one shared sync authority classifier

- [ ] **Completed**

**Goal:** produce neutral ownership/version-authority facts from the same semantics used by sync execution.

**Required facts per expanded target:**

- source repository/ref/path;
- target path;
- lifecycle policy;
- declared managed scope;
- target-exists state when relevant;
- exact-self-canonical state;
- write authority;
- version authority.

**Required lifecycle classification:**

```text
external enforce           -> continuous external authority
self-canonical enforce     -> no-op/current repository authority
seed_once target absent    -> create-if-missing
seed_once target exists    -> no active write authority
disabled                   -> no active write authority
```

The classifier must reuse normalization, source-glob expansion, duplicate detection, and path safety. It must not create a parallel interpretation.

---

## W10 — Make sync execution consume the classifier

- [ ] **Completed**

**Goal:** prevent planner/executor disagreement.

**Required behavior:**

- exact self-canonical operations are no-op;
- same repository but different source/target path remains real sync;
- verify and sync consume classifier facts;
- duplicate/generated-target behavior unchanged unless explicitly approved;
- no write begins before complete plan succeeds.

**Validation:** full sync suite plus exact self/no-op matrix.

---

## W11 — Expose the read-only ownership plan

- [ ] **Completed**

**Goal:** publish a closed, versioned plan for doc-metadata.

**Contract must include:**

- schema version;
- generator repository and commit;
- caller repository and exact target SHA;
- manifest path and digest;
- completeness;
- sorted unique targets;
- neutral authority facts;
- no secrets or source content.

**Failure must be closed for:**

- missing/invalid manifest where plan is required;
- unsupported version;
- wrong caller/SHA/digest;
- duplicate target;
- source tree truncation;
- unavailable private source;
- oversized output;
- incomplete plan.

Plan and actual sync must use the same Workflows commit.

---

## W12 — Enforce exclusive canonical version authority

- [ ] **Completed**

**Goal:** doc-metadata consumes only the ownership-plan contract.

**Required behavior:**

- external `enforce` target: skip entire file;
- self-canonical `enforce`: allow;
- existing `seed_once`: allow;
- missing `seed_once`: reserve;
- disabled: allow normal doc governance;
- stale/missing/invalid required plan: fail before writes;
- separate report category for canonical-source authority;
- no marker parsing in doc-metadata;
- no second blacklist manifest.

**Required documentation:**

- source owns canonical version under external `enforce`;
- local marker content may remain editable while canonical version stays source-owned;
- Git history records local overlay changes;
- no local-overlay version in v1;
- version is not merge priority.

---

## W13 — Prove cross-engine convergence in fixtures

- [ ] **Completed**

Run twice:

```text
ownership plan
doc-metadata Analyze
doc-metadata Update when required
doc-metadata Check
sync verify/sync plan
repeat
```

Witnesses:

- external whole-file enforce;
- external inside/outside-marker enforce;
- exact self-canonical entry;
- existing/missing seed_once;
- disabled;
- unowned document;
- invalid/stale plan.

Second pass must be no-op.

---

## W14 — Correct manifest governance

- [ ] **Completed**

**Goal:** implement include-minus-exclude and remove `documentEligibility`.

Implementation, schema, default manifest, tests, examples, API/type docs, and migration diagnostics are one pass.

Remove broad `**/*.txt`. Explicitly included unprocessable files fail clearly.

---

## W15 — Canonical links

- [ ] **Completed**

Implement and document:

```markdown
> [<b>View Changes</b>](...)
> [<b>View Commit</b>](...)

- Updated: <b>...</b> | Author: <b>...</b> | [<b>View Changes</b>](...)
- Updated: <b>...</b> | Author: <b>...</b> | [<b>View Commit</b>](...)
```

No generated `Changes:` label. No guessed unavailable history.

---

## W16 — Complete protected-field tamper coverage

- [ ] **Completed**

Isolated cases:

- Version;
- Created;
- Updated;
- Author;
- current link;
- generated history/presentation;
- mixed tamper;
- tamper plus body change;
- PR/push/manual;
- authority-skipped file untouched.

Production changes require a failing test witness.

---

## W17 — Workflows release-candidate certification

- [ ] **Completed**

**Goal:** produce the exact immutable SHA allowed for caller migration.

Required:

- all PowerShell and Python suites pass twice where required;
- package init, no-op re-init, and upgrade fixtures;
- generated wrapper YAML/actionlint;
- literal SHA equals release candidate;
- schema/docs/default manifest match engine contract;
- local Workflows self-maintenance passes;
- ownership convergence fixtures pass twice;
- static security and permissions review;
- complete diff review;
- authoritative docs current.

Record:

```text
WORKFLOWS_RELEASE_CANDIDATE_SHA=<40-character SHA>
```

### External-caller limitation

A pure Workflows test cannot prove every cross-repository permission and repair behavior. Session B begins with a non-destructive integration branch and parity gate. If that gate finds a shared-engine defect, migration stops and a bounded Workflows fix produces a new release candidate.

# Session B — `BionicCode/template-visual-studio-repository`

## T0 — Resolve and quarantine caller documentation

- [ ] **Completed**

Review current caller HEAD, old backlog/protocol, copied docs, local engine docs, and open PRs.

Replace the old active full roadmap with:

- a pointer to the authoritative Workflows backlog;
- template-specific migration status only.

No implementation yet.

---

## T1 — Run package init/upgrade on a migration branch

- [ ] **Completed**

Use the exact W17 SHA.

Expected PR changes:

- generated thin wrapper;
- local schema/docs at matching package version;
- preserved or initialized caller doc manifest;
- structurally updated sync manifest entries;
- package metadata/validation surfaces.

No old engine deletion yet.

Validate idempotent second installer run.

---

## T2 — Shared-versus-local parity gate

- [ ] **Completed**

Run old local engine and new shared engine against identical fixtures and repository states without allowing both to publish repairs.

Compare:

- analyze report;
- changed-file set;
- updated bytes;
- diagnostics;
- link map behavior;
- post-check result.

Differences require explicit classification. Unexpected shared-engine differences reopen Workflows.

---

## T3 — Switch orchestration to the thin wrapper

- [ ] **Completed**

**Goal:** make the shared engine authoritative in the caller.

Required:

- top-level orchestrator calls local thin wrapper;
- wrapper pins exact W17 SHA;
- ownership plan precedes doc-metadata;
- sync uses same Workflows SHA;
- no intermediate merge that exposes partial integration;
- PR/push/manual/fork matrix passes.

---

## T4 — Prove live caller convergence

- [ ] **Completed**

Use isolated branches/fixtures and run the complete sequence twice.

No second-pass PR or reversal is allowed.

Do not merge PR #34 or PR #35.

---

## T5 — Remove duplicated caller engine

- [ ] **Completed**

Only after T2–T4 acceptance, remove caller copies of:

- PowerShell engine;
- resolver engine;
- engine acceptance tests;
- full local reusable implementation no longer needed.

Retain:

- thin wrapper;
- caller manifest;
- schema/docs package copies;
- caller orchestration;
- caller-specific documentation.

Preserve old implementation through Git history, not an obsolete-code folder.

---

## T6 — Clean stale automation state

- [ ] **Completed**

After convergence:

- close/supersede PR #34 and PR #35 with preserved evidence;
- regenerate fresh automation evidence;
- verify clean current PRs;
- update evidence ledger.

No automated merge is authorized.

## 7. Deferred post-recovery candidates

F1 through F3 are proposal identifiers outside the admitted recovery roadmap, ordered pass index, and current evidence ledger. They have no current completion status and require a future admission review, formal pass contract, ordering decision, and explicit activation before execution. They do not block the recovery completion definition in section 8 unless a later governance update explicitly promotes them into the roadmap.

### F1 candidate — Single-boundary marker support

Allow one physical marker with virtual BOF/EOF boundary. Requires schema, parser, composition, migration, tests, and human docs.

Do not make recovery depend on it.

### F2 candidate — Hierarchical manifest imports and provenance

Design schema-level policy imports with declaring-repository provenance, cycle detection, depth limits, duplicate conflict handling, and A→B→C diagnostics.

Do not implement raw textual fences inside JSON.

### F3 candidate — Performance and dependency hardening

Only after correctness:

- immutable action references;
- measured checkout depth changes;
- dependency warning remediation;
- plan-size measurement;
- caching only with demonstrated reusable output;
- one optimization per pass.

## 8. Completion definition

Recovery is complete only when:

- Workflows contains one authoritative doc-metadata engine;
- callers contain no copied engine/tests;
- initializer installs a coherent pinned package;
- schema/docs/wrapper share one package identity;
- Workflows remains passive;
- ownership plan and sync share one classifier and commit;
- canonical version authority prevents ping-pong;
- two complete passes converge to no-op;
- manifest governance, links, and tamper behavior match approved contracts;
- documentation is human-readable, current, and structurally complete;
- exact final SHAs and run evidence are recorded;
- stale automation PRs are resolved.

## 9. Evidence ledger

**See [evidence-ledger-documentation.md](evidence-ledger-documentation.md) for details.**

> [!NOTE]
> **Historical W1 bookkeeping arrangement**
>
> W1 predates the finalized activation-commit workflow.
>
> Its execution handoff used
> `3a3fe364028db003bfc89d3a94fd8a9f167d1f35` as the task-supplied pre-pass
> baseline and execution lease.
>
> The W1 branch contained one explicitly approved post-baseline bookkeeping
> commit:
>
> `af639f43688bfd136b1dbdf051cc07bb7c588068`
>
> That commit updated the ledger to record the task-supplied baseline and
> restored the backlog file’s final newline. It was verified as part of W1’s
> start checks, but it was not the W1 pre-pass baseline or pass result.
>
> Beginning with W2, the dedicated `Locked` → `Pending` activation commit on
> the target branch is supplied as the pre-pass baseline, and the pass branch
> is created from exactly that commit. This avoids the historical W1
> bookkeeping arrangement.



| Pass | Status | Pre-pass baseline SHA | Result SHA | PR # | Review-gate closure SHA | Tests/runs | Reviewer |
|---|---|---|---|---|---|---|---|
| W0 | Completed | `a64ef89537304f81466acfcbdd63a187fe74ce51` | `ed8b11288b89a5f0aca2c1551e2d8bdb1606c8a8` | 4 | `f0005ad6a23431bbac4e2e2c6955a6d59a9437cb` | Three-file scope review; Markdown/link checks; `git diff --check` | BionicCode |
| W1 | Completed | `3a3fe364028db003bfc89d3a94fd8a9f167d1f35` | N/A — review-only; no repository change | 8 | `9abed50a87fafb80157cab636fd73de018f3c5ea` | 30/30 tracked Markdown audited; lease, ancestry, merge-base, and bookkeeping diff verified; 20 local targets and 3 anchors resolved; static workflow/script/schema/manifest/example audit; `git diff --check` PASS; PowerShell suite and GitHub Actions not run; sync tests executed 0 tests because `jsonschema` was unavailable | BionicCode |
| W2 | Pending |  |  |  |  |  |  |
| W2A | Locked |  |  |  |  |  |  |
| W2B | Locked |  |  |  |  |  |  |
| W3 | Locked |  |  |  |  |  |  |
| W4 | Locked |  |  |  |  |  |  |
| W5 | Locked |  |  |  |  |  |  |
| W6 | Locked |  |  |  |  |  |  |
| W7 | Locked |  |  |  |  |  |  |
| W8 | Locked |  |  |  |  |  |  |
| W9 | Locked |  |  |  |  |  |  |
| W10 | Locked |  |  |  |  |  |  |
| W11 | Locked |  |  |  |  |  |  |
| W12 | Locked |  |  |  |  |  |  |
| W13 | Locked |  |  |  |  |  |  |
| W14 | Locked |  |  |  |  |  |  |
| W15 | Locked |  |  |  |  |  |  |
| W16 | Locked |  |  |  |  |  |  |
| W17 | Locked |  |  |  |  |  |  |
| T0 | Locked |  |  |  |  |  |  |
| T1 | Locked |  |  |  |  |  |  |
| T2 | Locked |  |  |  |  |  |  |
| T3 | Locked |  |  |  |  |  |  |
| T4 | Locked |  |  |  |  |  |  |
| T5 | Locked |  |  |  |  |  |  |
| T6 | Locked |  |  |  |  |  |  |
