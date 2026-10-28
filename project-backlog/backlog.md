# Managed Package Platform — Project Backlog

## 1. Purpose and authority

Build a generic, registry-driven platform to create, register, install, maintain and execute reusable packages across GitHub repositories. `BionicCode/workflows` owns the shared platform implementation; approved package publishers own their canonical sources, and destination repositories own their local configuration and mutable project state.

This project-owned backlog is the stable authority for pass identities, titles, order, dependencies, scope, outputs, invariants, acceptance criteria and project-specific decisions. The [project evidence ledger](evidence-ledger.md) is the sole mutable authority for lifecycle state, accepted SHAs, PRs, test/run evidence and reviewer state in the default lane.

Reusable authority and lifecycle rules remain in the installed [Backlog Workflow](backlog-workflow.md), [review protocol](review-protocol.md) and [evidence-ledger protocol](evidence-ledger-protocol.md), together with the [repository instructions](../AGENTS.md). This backlog applies those contracts without replacing them.

> [!IMPORTANT]
> A roadmap entry, dependency, package registration, review or file installation grants no write authority. Every later task needs current authorization and the applicable handoff and readiness gates. Initializing this backlog and its ledger is outside the new pass lifecycle and completes or activates no pass.

The five-file `project-backlog/` workspace is already installed. Initialization populates only the two project-owned roadmap/state files; it does not repeat provisioning, install a skill, activate a service, dispatch a workflow or retire an implementation.

The requirement baseline is the maintainer-supplied **Managed Package Platform — Project Backlog** draft, containing MP00–MP34 plus MP04A and MP18A, normalized by the approved initialization plan. Its SHA-256 is `5FE4620F69AF416EA31BA9C39416BE66EE59F58A9B347F03ADA5CF5D91FAEA6F`. The accompanying **Codex Handoff — Managed Package Platform Backlog Initialization Review** is supporting planning material, not an independent authorization.

The roadmap establishes the intended replacement direction for the archived repository-maintenance recovery project. MP00 verifies and records the supersession baseline; runtime cutover and retirement remain separately gated later work. Historical W/T identities and evidence are not new-project results.

## 2. Program outcomes and completion definition

The program must deliver:

- A versioned package model, central registry/catalog, registrar and early `create-package` factory.
- Generic dependency resolution and installation, validation, repair, upgrade and removal infrastructure for both package classes.
- A package-agnostic Composition Runner using one cumulative working tree, a final validation pass and one safely reconciled maintenance PR.
- A single shared document/file ownership capability consumed by Managed File Sync and Document Revisions.
- Standard runtime interfaces implemented through Python and PowerShell, with immutable source provenance and no package-specific business logic in the runner or installer.
- Migrated runtime and asset packages, accepted consumers, current documentation and governed legacy retirement.

Completion is observable when an authorized operator can create and register either package class, install compatible packages into a destination through one coherent proposal, receive a thin runtime caller when needed, obtain one validated cumulative maintenance proposal, safely manage package lifecycle changes and operate without the legacy orchestrator or specialized installers.

All required hosted, security, migration, rollback and convergence evidence must be accepted under the installed review and ledger protocols. Final release declaration follows the required final-pass closure/finalization and explicit release authorization; no result may anticipate its own closure SHA or a release that does not exist.

## 3. Boundaries and non-goals

### In scope

- Shared implementation and preferred canonical package sources in `BionicCode/workflows`.
- Approved package sources at explicit paths in external repositories, including the existing Backlog Workflow and Code Style sources.
- `BionicCode/template-visual-studio-repository` as the first real consumer migration, followed by inventoried adopters including `BionicCode/nextcloud-url-uploader`.
- Package contracts, shared ownership, script runtime composition, administration, installation, lifecycle state, migration, certification, documentation and accepted retirement.
- Read-only historical evidence inspection where needed to establish provenance or preserve existing authority.

### Authority and migration boundaries

Exact source revisions, test repositories, destination branches and writable paths belong in later authorized handoffs. Naming a repository here is not write authority. Separate source-engine corrections from caller migration; do not patch shared behavior independently in a consumer.

Protected instructions, publisher payloads, installed instruction copies and control-plane surfaces retain their current repository protections. MP28 and other future passes need exact protected-path authorization; this initialization does not grant it.

Historical material under `.backup/` remains historical and read-only unless a later task explicitly authorizes a specific disposition. An evidence archive, if integrated later, stores downstream artifacts and does not own backlog, ledger, acceptance or lifecycle state. No archive infrastructure activation is included here.

### Out of scope for the initial release

- Arbitrary package-specific installer GUIs.
- Unrestricted installation hooks or execution of arbitrary unreviewed package code.
- A distributed locking requirement.
- Automatic repository merges or automatic human conflict resolution.
- Transactionally coordinated deployment across multiple destination repositories.
- Unrelated instruction-rule audits, global agent configuration changes or skill installation/activation.

### Deferred decisions

Exact descriptor fields, public filenames, CLI flags, protected-region delimiters, credential names, approved external SHAs and release versions are outputs or runtime inputs of the designated contract passes. They are not invented during initialization. Every dependent implementation must wait for the required accepted decisions.

## 4. Decisions and supporting specifications

The following are approved architectural premises for this roadmap. They describe required future behavior; they do not assert that the replacement platform is already implemented.

### D01 — Canonical sources, identity and approval

Prefer `BionicCode/workflows/deployment/packages/<package-id>/` as the canonical package source location. The registrar and installer must also support approved packages at explicitly specified repository-relative paths in external GitHub repositories.

Approved source identity combines repository, package path and immutable revision. Package identity must survive relocation. Resolve source/configuration/runtime versions coherently and retain provenance through contribution merging and installation state. Registration may inspect metadata but must not implicitly execute package code or copy untrusted workflows into the platform.

### D02 — Package classes and capability dependencies

Class 1 asset packages provide a common descriptor, a package-owned `sync-manifest.json` contribution, payload and documentation. They require no executable service entry point. Their installer resolves compatible Sync/runtime infrastructure, structurally merges contributions, materializes initial assets and maintains provenance/state in one destination proposal.

Class 2 runtime-service packages provide the common descriptor, compatible `execute` and `validate` entry points, declared runtime requirements, inputs, outputs, compatibility, tests and documentation. They may also distribute assets and contributions. A service executing through the Composition Runner does not publish a separate maintenance PR.

Capability libraries such as document ownership are trusted dependencies, not automatically scheduled transformations. MP02/MP06 settle their representation and bootstrap direction without introducing a third top-level package class, meaningless runtime scripts or a Sync bootstrap cycle.

### D03 — Package factory

The early administrative `create-package` workflow defaults to the central repository and `deployment/packages/`. Explicit external repository/path inputs remain supported. Validate identity and paths, require creation confirmation, refuse unrelated-content overwrite, generate class-appropriate structure/docs/fixtures/tests and produce a reviewed PR in the selected source repository.

Generate inert example `execute`/`validate` implementations only for Class 2. Factory execution does not automatically register, install or activate the package and is usable before the final registrar/installer.

### D04 — Runtime execution and publication

Runtime engines use Python/PowerShell execution interfaces. The supported package runtime interface contains no package-specific callable YAML workflows. Central administration workflows, the generic callable composition workflow and thin destination callers remain supported. Existing legacy workflows are compatibility/migration artifacts until accepted removal gates; they do not become new package runtime APIs.

Resolve one coherent context and collect applicable current and historical changes. Execute ordered top-level services on one cumulative working tree; services may call their trusted library dependencies. Record structured outcomes and service changesets. No service publishes during execution.

Freeze the cumulative candidate, run required read-only validators against that same candidate, independently check global ownership and journal integrity, and aggregate structured reports. Reject publication after any required execution, validation, ownership or freshness failure.

After remote-state and authority checks, create or safely reconcile one automation-owned maintenance PR. Never auto-merge into the destination branch or silently overwrite user-modified proposals. Preserve reviewable failure diagnostics and require an unchanged post-merge rerun to be a no-op.

### D05 — Shared ownership

Extract existing Sync ownership behavior before extending it. Maintain one authoritative ownership interpreter shared by Sync and Document Revisions. Cover whole-file source authority, inside/outside markers, globs, marker grammar/malformed input, exclusive service sections, user-editable and non-writable regions, allowed writers, overlaps, canonical projection, incoming/service-generated changes, policy transitions and approved administrator overrides.

Preserve legacy whole-file and marker behavior during extraction. Protected-region exceptions require an explicit approved versioned contract; never silently weaken existing byte-exact whole-file semantics. Ownership authorizes regions/writers; each service validates its own semantic content. Registration cannot unilaterally override established policy.

### D06 — File lifecycle and durable receipts

| Policy | Initial provisioning | Existing target | Missing after provisioning |
| --- | --- | --- | --- |
| `enforce` | Create canonical content | Enforce the approved owned scope | Restore |
| `ensure_exists` | Create | Preserve target-owned content | Restore |
| `seed_once` | Provision once | Preserve target-owned content | Preserve deliberate absence |
| `disabled` | No active provisioning | No active maintenance | No restoration |

True `seed_once` needs durable earlier-provisioning evidence. Payload and receipt changes belong to one coherent installation proposal; a missing file alone does not establish a receipt or authorize reseeding. Preserve deliberate deletion/relocation of consumed true seeds.

Legacy `seed_once` registrations retain equivalent behavior through explicit migration to `ensure_exists` unless individually reclassified with maintainer approval. Installation, synchronization, repair, upgrade, removal and dependency planning share these semantics. MP04 defines ambiguous-history handling without inventing receipts.

Retain additive behavior as the compatibility baseline. Stale managed-asset removal requires proven ownership, complete membership evidence and an approved operation. A target directory alone is not deletion ownership.

### D07 — Document Revisions

Approve protected revision-region identity, authority, format/versioning and migration before implementing conversion. Build and validate migration tooling before integrating live conversion with the consolidated service.

Replace tool-owned YAML front matter with dedicated protected revision regions while preserving unrelated YAML fields/content, lineage, timestamps and revision history. Diagnose tampering and ambiguity, preserve rollback, and distinguish body changes from tool-only or format-only changes. Sync plus Document Revisions must converge after an unchanged maintenance proposal is merged.

### D08 — Package migration and source relocation

MP01 inventories dependencies of moving Backlog Workflow and Code Style canonical distribution sources into `deployment/packages/`. MP02 approves each repository/path authority and compatibility/rollback disposition. Prefer central relocation; retaining an external canonical location requires a documented correctness, dependency, security or feasibility reason.

MP29/MP30 execute those approved decisions. Preserve Backlog Workflow's three managed governance files, two mutable project files, existing ledger/backlog state and separate skill boundary. Preserve Code Style's existing NuGet behavior and verify its actual payload rather than infer it from old examples.

Convert Agent Instructions without losing the instruction partition, source/install ownership, local companions, optional bridges, operational review state or seeded customizations. The generic installer replaces specialized adoption for future consumers after acceptance.

### D09 — Security, snapshots and recovery

Keep installation and runtime privilege boundaries distinct. Validate source-read and destination-write authority independently, approved immutable execution sources, safe repository-relative paths, symlink/junction behavior, argument handling, secret boundaries and workflow-file permissions.

The central repository token is not assumed to authorize arbitrary targets; see the [GitHub token documentation](https://docs.github.com/en/actions/concepts/security/github_token). MP07 supplies deployment-matched feasibility evidence before privileged infrastructure is accepted.

Immutable inputs, optimistic concurrency, historical changed-path accounting and recovery precede accepted publication. Failed, canceled or superseded runs must not lose outstanding work or corrupt proposals. Do not infer exclusive worktree/lane access from an execution lease.

### D10 — Compatibility, retirement and documentation

Provide a complete old-to-new reference map, compatibility direction and removal gate for public path/contract migrations. Preserve operative entry points until dependencies and replacements exist. Migrate consumers only after replacement packages and installation infrastructure are accepted.

Remove obsolete orchestrators, duplicate engines, installers and deprecated artifacts only after replacement certification and rollback review. Every implementation/migration pass delivers affected documentation, examples, tests and migration guidance in the same reviewed change. The final documentation pass completes integration guidance rather than deferring earlier documentation obligations.

### D11 — Evidence categories and current implementation

Keep current implementation, approved future behavior, historical records and unresolved design outputs distinct. Static schema/text checks and local fixtures do not establish hosted integration, native client behavior or broad deployed reliability.

Current extraction evidence is the [Sync implementation](../.github/scripts/sync-files-from-manifest/sync_files.py), its [marker handling](../.github/scripts/sync-files-from-manifest/marker_scope.py) and [documented legacy lifecycle](../.github/scripts/sync-files-from-manifest/documentation/types/lifecycle-policy.md). Current legacy `seed_once` restores missing targets and verifies presence; true seed-and-forget is future work here.

The [metadata implementation](../.github/scripts/doc-metadata/update-doc-metadata.ps1) already supports YAML front matter and comment blocks; selecting comment syntax alone does not implement shared protected ownership or convergence.

At initialization review, the [legacy orchestrator](../.github/workflows/repository-maintenance.yml) references an absent `.github/workflows/sync-managed-files.yml`. This is a static inventory lead, not an observed hosted result. MP01 must revalidate it against its own execution context; this initialization does not repair it.

Historical-only references include the [archived recovery roadmap](../.backup/repository-maintenance-orchestrator-recovery-backlog.md), [archived review protocol](../.backup/repository-review-protocol.md) and [historical ledger notes](../.backup/evidence-ledger-documentation.md). These links do not activate archived instructions or transfer accepted results into the new ledger.

### Planned supporting specifications and requirement coverage

| Required capability | Owning output and implementation consumers |
| --- | --- |
| Architecture, trust and source-location authority | MP02 decision set; applied by all later passes, including MP29 and MP30 |
| Ownership, marker and protected revision-region specification | MP03; extracted/implemented in MP10/MP11 and consumed by MP18/MP26/MP27 |
| Lifecycle, receipt and legacy migration specification | MP04; implemented consistently by MP18 and MP21–MP24 |
| Service context, result, runtime and adapter specification | MP05; feasibility/prototype evidence in MP07/MP08 and production adapters in MP12 |
| Package/layout/dependency/registration schemas | MP06; materialized by MP09 and consumed by MP19–MP24 |
| Factory and central/external package authoring | MP09 |
| Cumulative execution, attribution, immutable inputs and publication | MP08 and MP12–MP17 |
| Registry/catalog, registrar and installation lifecycle | MP19–MP25 |
| Sync and Document Revisions consolidation | MP18 and MP26/MP27 |
| Asset package conversion and canonical-source migration | MP28–MP30 |
| First consumer and remaining adopter migration | MP31/MP32 |
| Hosted security, race/recovery and convergence certification | MP07, MP25 and MP33 |
| Operator/author documentation and accepted retirement/release | Documentation in every affected pass; MP34–MP36 integration and closure |

These are planned outputs of their owning passes, not links to specifications that already exist. Exact public names, approved revisions and execution commands are settled through those passes and later handoffs.

## 5. Dependency and milestone model

Use one strictly ordered default lane, governed by [evidence-ledger.md](evidence-ledger.md). No additional lanes or ledger paths are admitted. Follow the installed protocols for state transitions, predecessor finalization, reachability and shared-worktree coordination instead of redefining them here.

Every pass after MP00 depends on its immediately preceding row being fully finalized as well as all explicit technical dependencies. The index and each formal specification expand dependencies into exact final IDs. Acceptance/finalization only establish eligibility; activation remains a separate authorized action.

Milestones are: governance/contracts/feasibility (MP00–MP07); prototype, early factory and runtime foundations (MP08–MP18); administration/installation certification (MP19–MP25); package migrations (MP26–MP30); and consumers, full certification, documentation, retirement and final authority (MP31–MP36).

Important ordering gates:

- MP01 informs MP02 source relocation decisions; MP29/MP30 execute them.
- MP03/MP04/MP05/MP06 establish contracts before dependent production implementation.
- MP07/MP08 establish feasibility and a bounded prototype before substantial infrastructure investment.
- MP10 extracts existing ownership; MP11 extends that same authority.
- MP14 snapshot/concurrency controls and MP15 validation precede accepted MP16 publication.
- MP18 provides production Sync before installer bootstrap and MP25 certification.
- MP26 validates inert migration tooling before MP27 integrates live-capable Document Revisions.
- Replacement packages precede MP31/MP32 consumer migration; certification and rollback review precede MP35 retirement.
- MP36's own closure/finalization precede an explicitly authorized final release declaration.

## 6. Ordered pass index

This index records stable identity, outcome, mode and dependencies. Lifecycle and accepted evidence belong only to the ledger.

| Pass | Outcome | Mode | Dependencies |
| --- | --- | --- | --- |
| [MP00](#mp00) | Establish the project charter and supersession baseline | coordination | Approved initialization |
| [MP01](#mp01) | Inventory legacy code, packages, consumers and evidence | review-only | MP00 |
| [MP02](#mp02) | Approve platform architecture and trust boundaries | planning | MP01 |
| [MP03](#mp03) | Approve shared ownership and protected revision-region contracts | planning | MP02 |
| [MP04](#mp04) | Approve lifecycle semantics and legacy migration | planning | MP02, MP03 |
| [MP05](#mp05) | Define the service API and Python/PowerShell adapter contracts | planning | MP02, MP03, MP04 |
| [MP06](#mp06) | Define package and registration schemas | planning | MP02, MP03, MP04, MP05 |
| [MP07](#mp07) | Validate security and execution feasibility | validation-only | MP05, MP06 |
| [MP08](#mp08) | Prove cumulative composition with disposable services | implementation | MP03, MP05, MP07 |
| [MP09](#mp09) | Deliver the central and external package factory | implementation | MP06, MP07, MP08 |
| [MP10](#mp10) | Extract the existing document ownership capability | implementation | MP01, MP03, MP06, MP09 |
| [MP11](#mp11) | Implement the shared ownership-policy extensions | implementation | MP03, MP10 |
| [MP12](#mp12) | Deliver generic service loading and execution | implementation | MP05, MP06, MP11 |
| [MP13](#mp13) | Deliver service changeset attribution | implementation | MP12 |
| [MP14](#mp14) | Deliver immutable snapshots and historical change reconciliation | implementation | MP12, MP13 |
| [MP15](#mp15) | Deliver final candidate validation | implementation | MP11, MP13, MP14 |
| [MP16](#mp16) | Deliver one-PR publication and safe reconciliation | implementation | MP14, MP15 |
| [MP17](#mp17) | Deliver central composition and the destination caller | implementation | MP12, MP15, MP16 |
| [MP18](#mp18) | Consolidate Managed File Sync as a standard runtime package | migration | MP04, MP10, MP11, MP12, MP14, MP15, MP17 |
| [MP19](#mp19) | Deliver the trusted registry and package catalog | implementation | MP06, MP07, MP18 |
| [MP20](#mp20) | Deliver registrar administration | implementation | MP19 |
| [MP21](#mp21) | Deliver dependency resolution and installation planning | implementation | MP04, MP06, MP19, MP20 |
| [MP22](#mp22) | Deliver manifest merging and initial asset materialization | implementation | MP04, MP11, MP18, MP21 |
| [MP23](#mp23) | Deliver the generic installer | implementation | MP17, MP18, MP20, MP21, MP22 |
| [MP24](#mp24) | Deliver package validation, repair, upgrade and uninstall planning | implementation | MP04, MP23 |
| [MP25](#mp25) | Certify package administration and installation | validation-only | MP20, MP23, MP24 |
| [MP26](#mp26) | Deliver protected revision migration tooling | implementation | MP03, MP11, MP18, MP25 |
| [MP27](#mp27) | Consolidate Document Revisions and integrate protected-region migration | migration | MP05, MP11, MP14, MP15, MP17, MP18, MP26 |
| [MP28](#mp28) | Migrate Agent Instructions to the asset-package contract | migration | MP04, MP06, MP18, MP22, MP23, MP24, MP25, MP27 |
| [MP29](#mp29) | Migrate Backlog Workflow using its approved source-location decision | migration | MP02, MP04, MP06, MP18, MP22, MP23, MP24, MP25, MP28 |
| [MP30](#mp30) | Migrate Code Style using its approved source-location decision | migration | MP02, MP04, MP06, MP18, MP22, MP23, MP24, MP25, MP29 |
| [MP31](#mp31) | Migrate the Visual Studio template consumer | migration | MP25, MP27, MP28, MP29, MP30 |
| [MP32](#mp32) | Migrate remaining adopters | migration | MP31 |
| [MP33](#mp33) | Certify the complete platform | validation-only | MP25, MP27, MP28, MP29, MP30, MP31, MP32 |
| [MP34](#mp34) | Complete operator and author documentation | implementation | MP33 |
| [MP35](#mp35) | Cut over and retire accepted legacy components | migration | MP31, MP32, MP33, MP34 |
| [MP36](#mp36) | Finalize historical evidence and release authority | coordination | MP35 |

## 7. Pass specifications

### Common pass requirements

Each specification below contains its required fields explicitly. Exact writable files, branch topology, repository revisions, execution commands, test destinations and credentials are finalized in the later authorized handoff; this roadmap grants none of those permissions.

- Apply D01–D11 and the installed workflow/review/ledger protocols without weakening them.
- Keep result, lifecycle closure, post-merge finalization and successor activation responsibilities distinct.
- Maintain tests and current documentation together for implementation/migration; planning/review/validation passes produce inspectable written evidence.
- Exercise public contracts and failure preservation rather than only implementation-shaped or phrase-based checks.
- Stop affected work on conflicting authority, missing prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or necessary out-of-scope changes.
- A merge must preserve operative callers and accepted commit identities. Do not enable incomplete replacement behavior.

The draft-to-final map below preserves every provisional identity. From admission onward, final identities are stable and must not be silently renumbered or reused.

| Draft pass | Final pass |
| --- | --- |
| MP00 | MP00 |
| MP01 | MP01 |
| MP02 | MP02 |
| MP05 | MP03 |
| MP06 | MP04 |
| MP03 | MP05 |
| MP04 | MP06 |
| MP07 | MP07 |
| MP08 | MP08 |
| MP04A | MP09 |
| MP22 | MP10 |
| MP09 | MP11 |
| MP10 | MP12 |
| MP11 | MP13 |
| MP14 | MP14 |
| MP12 | MP15 |
| MP13 | MP16 |
| MP15 | MP17 |
| MP23 | MP18 |
| MP16 | MP19 |
| MP17 | MP20 |
| MP18 | MP21 |
| MP18A | MP22 |
| MP19 | MP23 |
| MP20 | MP24 |
| MP21 | MP25 |
| MP25 | MP26 |
| MP24 | MP27 |
| MP26 | MP28 |
| MP27 | MP29 |
| MP28 | MP30 |
| MP29 | MP31 |
| MP30 | MP32 |
| MP31 | MP33 |
| MP32 | MP34 |
| MP33 | MP35 |
| MP34 | MP36 |

<a id="mp00"></a>

### MP00 — Establish the project charter and supersession baseline

**Identifier:**

`MP00`

**Title:**

Establish the project charter and supersession baseline

**Mode:**

coordination

**Objective:**

Record the project charter, approved architectural premises, repository authority boundaries and explicit relationship to the archived recovery project.

**Rationale:**

Admission establishes the roadmap; a separate first governed pass must verify the supersession baseline before inventory and implementation preparation.

**Dependencies:**

- Approved initialization/admission of this roadmap and ledger; there is no predecessor MP pass.

**Scope:**

- Repositories: BionicCode/workflows; historical source repositories and records are read-only evidence.
- Allowed surfaces: Explicitly authorized project governance records, charter/decision notes and reference analysis.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- A durable charter and supersession record identifying retained historical evidence and the intended replacement direction.
- A verified governance/reference baseline matching the admitted backlog and ledger identities.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Prior installation supplies no MP00 result or completion evidence; initialization does not retroactively authorize this pass.
- Historical W/T evidence remains historical and cannot be imported as an MP result.

**Non-goals:**

- Repeat workspace provisioning, perform implementation inventory, change reusable protocols, activate later work or retire automation.

**Acceptance criteria:**

- The existing five-file governance workspace is verified without reinstallation; historical records remain preserved.
- Competing active governance references are reconciled within authorization or reported as blockers; roadmap and ledger identity/order agree.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Inspect the five installed files, root instruction routes and links to historical records; record exact reviewed context.
- Check identity/order correlation and the governance-only diff; distinguish current authority from historical W/T records.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Project charter/supersession and authority references only; no new executable API.

**Documentation impact:**

Produce the accepted written governance/review/validation evidence appropriate to this pass without silently changing implementation.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Competing active authority remains unresolved, or reconciliation requires an unauthorized protected-reference change.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP01` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp01"></a>

### MP01 — Inventory legacy code, packages, consumers and evidence

**Identifier:**

`MP01`

**Title:**

Inventory legacy code, packages, consumers and evidence

**Mode:**

review-only

**Objective:**

Classify meaningful workflows, scripts, schemas, manifests, documentation, tests, package payloads, callers, releases and evidence as reuse, extract, refactor, migrate, archive or retire.

**Rationale:**

Architecture and source-location decisions need a traced artifact/consumer inventory before fixing migration and retirement boundaries.

**Dependencies:**

- `MP00` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows, BionicCode/backlog-driven-engineering-workflow, BionicCode/bioniccode-code-style, named consumers and relevant historical records; all read-only.
- Allowed surfaces: Read-only artifact, literal-reference, call-path, source-access and canonical/generated-copy inspection; written review output.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- An artifact/consumer classification and real call/reference map with provenance and explicit unverified items.
- Backlog Workflow relocation dependencies, actual Code Style payload/NuGet integration and migration/access constraints.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Reviewed artifacts, archives, Git state, lifecycle state and external repositories remain unchanged.

**Non-goals:**

- Implement corrections, initialize archives, accept historical work as new results or change package authorities.

**Acceptance criteria:**

- Every meaningful inspected artifact has an evidence-backed classification and ownership; inaccessible material remains explicitly unverified.
- The legacy orchestrator's absent workflow reference is revalidated against this pass context; active consumers and release/source dependencies are identified.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Trace actual invocations, package projections, release references and consumer dependency paths rather than infer behavior from names.
- Cross-check canonical/generated boundaries and source access; report coverage, gaps and proposed bounded follow-up surfaces.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Documentation impact:**

Produce the accepted written governance/review/validation evidence appropriate to this pass without silently changing implementation.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Required evidence is unavailable or contradictory; do not guess a classification or mutate artifacts to make the inventory complete.

**Review gate:**

Independent inventory review checks provenance, coverage, classifications and uncertainty; maintainer acceptance is required.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP02` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp02"></a>

### MP02 — Approve platform architecture and trust boundaries

**Identifier:**

`MP02`

**Title:**

Approve platform architecture and trust boundaries

**Mode:**

planning

**Objective:**

Approve the bounded platform architecture, trust/privilege boundaries and canonical-source dispositions using MP01 evidence.

**Rationale:**

Shared ownership, lifecycle, API and package contracts need one coherent architectural baseline before detailed design or production implementation.

**Dependencies:**

- `MP01` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows design authority; external sources and consumers are evidence inputs, not authorized mutation targets.
- Allowed surfaces: Architecture/trust decision artifacts, requirement traceability and bounded design/feasibility analysis.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- An independently reviewed decision set for package classes, capability dependencies, administrative/runtime separation, cumulative PRs, source approval, credentials and compatibility.
- An explicit repository/path authority, compatibility/rollback disposition and central-relocation decision for Backlog Workflow and Code Style.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Preserve the agreed project boundaries, two package classes, external-source capability and no-auto-merge model.

**Non-goals:**

- Redesign unrelated instruction/governance systems, deploy services or move canonical sources during this planning pass.

**Acceptance criteria:**

- All retained project requirements map to the architecture; dependency and privilege boundaries have a feasible bootstrap direction.
- Central relocation is preferred; any external canonical exception has a concrete correctness, dependency, security or feasibility reason.
- The package catalog is distinguished from ownership-policy claims; no third top-level package class or meaningless runtime workaround is introduced.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Review the architecture against the inventory, requirement coverage, trust boundaries, source ownership and rollback cases.
- Review both source-location decisions and the dependency/bootstrap model independently before dependent implementation.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Architecture constraints and source/capability authority; detailed versioned interfaces are subsequent contract outputs.

**Trust and security constraints:**

Approve the source-read, destination-write, code-execution and publication trust model without assuming cross-repository token authority.

**Rollback:**

Approve source-location compatibility/removal and rollback direction before migration.

**Documentation impact:**

Produce accepted written contracts, rationale, examples and bounded fixture/evidence requirements; production materialization remains in the named implementation passes.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Authority, a bootstrap cycle or a material scope change remains unresolved.

**Review gate:**

Independent architectural review must accept requirement coverage, authority, trust, dependency feasibility and source-location decisions; maintainer acceptance is required.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP03` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp03"></a>

### MP03 — Approve shared ownership and protected revision-region contracts

**Identifier:**

`MP03`

**Title:**

Approve shared ownership and protected revision-region contracts

**Mode:**

planning

**Objective:**

Specify versioned ownership, markers, writer/region claims and protected revision regions interoperable with Python and PowerShell.

**Rationale:**

Extraction, ownership extensions and document conversion must share one accepted policy and format before implementation.

**Dependencies:**

- `MP02` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows design authority; existing Sync and metadata implementations are read-only extraction/migration evidence.
- Allowed surfaces: Ownership/marker/region specifications, authority matrices, interoperability contracts and migration/rollback design fixtures.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- A versioned ownership policy, marker grammar, writer/region matrix, overlap/conflict rules and Python/PowerShell interoperability contract.
- Protected revision-region identity, content authority, format/versioning, canonical projection exceptions and malformed/conflicting-claim behavior.
- A migration contract for proven tool-owned front matter that preserves unrelated YAML content and defines rollback.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- One authoritative ownership interpreter; no unilateral registration bypass of existing claims.

**Non-goals:**

- Implement the production interpreter, convert live documents or invent an additional package class.

**Acceptance criteria:**

- Whole-file, inside/outside markers, globs, user-editable, non-writable and exclusive-service cases have explicit authority and failure behavior.
- Legacy whole-file/marker semantics remain explicit; new protected exceptions are approved/versioned and cannot silently weaken byte-exact enforcement.
- Ownership authorization is distinct from domain semantics and shared by both initial service runtimes.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Independently review positive/negative writer, overlap, missing/malformed delimiter and policy-transition matrices.
- Review canonical-content plus service-region examples, migration ambiguity and cross-language calls against actual legacy evidence.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Planned versioned ownership/marker/protected-region and interoperability contracts.

**Trust and security constraints:**

Define explicit writer authority, non-writable regions and approved policy overrides; ambiguous authority fails closed.

**Migration and compatibility:**

Document the exact legacy-to-versioned-policy preservation and protected-region migration boundary.

**Rollback:**

Specify reversal and preservation obligations for revision-format migration before conversion tooling.

**Documentation impact:**

Produce accepted written contracts, rationale, examples and bounded fixture/evidence requirements; production materialization remains in the named implementation passes.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- A proposed exception silently changes legacy semantics, depends on independent interpreters or cannot distinguish tool-owned from unrelated front matter.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP04` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp04"></a>

### MP04 — Approve lifecycle semantics and legacy migration

**Identifier:**

`MP04`

**Title:**

Approve lifecycle semantics and legacy migration

**Mode:**

planning

**Objective:**

Specify enforce, ensure_exists, true seed_once and disabled consistently with durable provisioning evidence and safe legacy migration.

**Rationale:**

Sync and package lifecycle operations must consume one accepted state model before implementing receipts, bootstrap or removal.

**Dependencies:**

- `MP02` — accepted and fully finalized under the installed protocols.
- `MP03` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows lifecycle design authority; existing source/consumer state is read-only evidence.
- Allowed surfaces: Lifecycle/receipt identity, durability, deletion/relocation, upgrade/removal and legacy migration specifications.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- A four-policy contract and durable receipt identity/provisioning rules covering installation, Sync, repair, upgrade, removal and dependency planning.
- An explicit legacy seed_once-to-ensure_exists migration and individually approved true-seed reclassification procedure.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- No inferred deletion ownership from directory membership; additive compatibility remains the baseline.

**Non-goals:**

- Implement storage/operations, silently relabel current registrations or recover lost project data from empty seed templates.

**Acceptance criteria:**

- Unprovisioned items are distinguishable from consumed provisioning history; ambiguous legacy evidence has an explicit safe outcome.
- Missing files alone do not fabricate receipts or reseeding permission; deliberate consumed-seed deletion/relocation and target-owned content are preserved.
- Payload/receipt coherence, reruns, opt-out, stale asset membership and dependency preservation are specified.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Independently review first/missing/existing provisioning, consumed seed, rename/deletion, failed install, rerun, opt-out, upgrade and uninstall scenarios.
- Check backward compatibility with the inspected legacy seed-and-require-presence implementation and explicit reclassification authority.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Planned versioned lifecycle, receipt and migration contracts.

**Migration and compatibility:**

Existing legacy seed_once keeps equivalent ensure_exists behavior unless individually reclassified.

**Rollback:**

Define recovery from failed provisioning and migration without losing consumed-seed history or target-owned data.

**Documentation impact:**

Produce accepted written contracts, rationale, examples and bounded fixture/evidence requirements; production materialization remains in the named implementation passes.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- A rule would silently reseed deleted state, erase receipt history or change legacy behavior without approval.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP05` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp05"></a>

### MP05 — Define the service API and Python/PowerShell adapter contracts

**Identifier:**

`MP05`

**Title:**

Define the service API and Python/PowerShell adapter contracts

**Mode:**

planning

**Objective:**

Approve execution context, result/report schemas, runtime/adapter behavior, bounded execution and validation purity for both initial languages.

**Rationale:**

Feasibility, prototype and production loading need a common service contract before generic execution is implemented.

**Dependencies:**

- `MP02` — accepted and fully finalized under the installed protocols.
- `MP03` — accepted and fully finalized under the installed protocols.
- `MP04` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows service-contract design authority and explicitly approved disposable reference fixtures.
- Allowed surfaces: Written service schemas/specifications, adapter contracts, reference fixtures and bounded feasibility evidence; no production executor.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- The approved context/result/report/error contracts with source/candidate identities, configuration, ordering, ownership and attribution inputs.
- Python and PowerShell adapter/runtime requirements, argument handling, execution bounds, diagnostics and read-only validation behavior.
- Reference fixtures for successful, unchanged, failed and invalid-result cases; production adapters are materialized in MP12.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Content-only packages require no executable stub; service execution does not publish maintenance proposals.

**Non-goals:**

- Build a production loader/publisher, finalize unrelated package fields or execute unapproved source code.

**Acceptance criteria:**

- Both languages express the same required outcomes and preserve context/provenance semantics without package-specific central behavior.
- Validation purity and report placement are explicit; required execution does not depend on package-specific callable YAML.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Review schema/contract fixtures for both languages and success/no-op/failure/invalid-result boundaries.
- Record the evidence needed for MP07/MP08 and check non-ASCII/path, argument, timeout and diagnostic cases where relevant.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Planned versioned service context/result/report and Python/PowerShell adapter contracts.

**Trust and security constraints:**

Bind approved source identity and bounded invocation/argument handling; define credential exposure and validation purity limits.

**Required fixtures:**

Reference services/requests/results for both supported languages, exercised only within an authorized bounded fixture context.

**Documentation impact:**

Produce accepted written contracts, rationale, examples and bounded fixture/evidence requirements; production materialization remains in the named implementation passes.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Domain behavior leaks into the generic API, required semantics differ by language or validation requires candidate mutation.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP06` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp06"></a>

### MP06 — Define package and registration schemas

**Identifier:**

`MP06`

**Title:**

Define package and registration schemas

**Mode:**

planning

**Objective:**

Approve package layouts, descriptor/contribution/dependency schemas and registration identity for both package classes and source topologies.

**Rationale:**

The factory and administrative plane need accepted names, compatibility and dependency shapes before materializing production schemas.

**Dependencies:**

- `MP02` — accepted and fully finalized under the installed protocols.
- `MP03` — accepted and fully finalized under the installed protocols.
- `MP04` — accepted and fully finalized under the installed protocols.
- `MP05` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows package-contract design authority; representative central/external package fixtures are bounded evidence.
- Allowed surfaces: Written versioned package/layout/registration schemas, compatibility definitions and representative fixture validation.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- Approved common descriptors/layouts, contribution format, dependency/capability representation, asset mappings, runtime references and lifecycle provenance.
- Source identity and approval contracts for central/external roots and immutable revisions, with exact public names selected from the illustrative draft layout.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Package identities/provenance survive contribution merging and source relocation; adding a package requires no central business logic.

**Non-goals:**

- Implement the final registry/installer or silently freeze illustrative filenames before this contract is accepted.

**Acceptance criteria:**

- Representative Class 1 and Class 2 fixtures validate; malformed, incompatible and unsafe forms fail.
- Class 1 has no mandatory executable stub; capability representation creates neither a third top-level class nor a Sync bootstrap cycle.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Validate representative central/external asset/runtime contract fixtures, malformed input, invalid paths/revisions, incompatible dependencies and class-specific requirements.
- Review schema/runtime validation alignment, compatibility/migration rules and descriptor-to-installation closure requirements.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Planned versioned package/layout, contribution, dependency and registration schemas; MP09 materializes approved schemas.

**Trust and security constraints:**

Explicit source approval, immutable references, safe relative paths and no implicit code execution.

**Migration and compatibility:**

Specify version compatibility, invalid combinations and migration behavior for breaking public-format changes.

**Required fixtures:**

Representative asset/runtime packages at central and explicit external roots, including invalid variants.

**Documentation impact:**

Produce accepted written contracts, rationale, examples and bounded fixture/evidence requirements; production materialization remains in the named implementation passes.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- The model creates a bootstrap cycle, automatically schedules all libraries or requires unapproved source execution during registration.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP07` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp07"></a>

### MP07 — Validate security and execution feasibility

**Identifier:**

`MP07`

**Title:**

Validate security and execution feasibility

**Mode:**

validation-only

**Objective:**

Establish deployment-matched feasibility evidence for the accepted threat model and service/package contracts.

**Rationale:**

Privilege, source access and runtime restrictions must be proven before accepting privileged production infrastructure.

**Dependencies:**

- `MP05` — accepted and fully finalized under the installed protocols.
- `MP06` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows and exact approved disposable fixture/test repositories; no production destination mutation.
- Allowed surfaces: Execution of authorized bounded reference fixtures and written security/access/recovery evidence; implementation contracts remain fixed.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- Evidence for trusted source execution, private source reads, destination writes, workflow-file handling, runtime support and recovery.
- Exact source revisions/environments, credential authority boundaries and explicit unavailable or inconclusive cases.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Use only approved immutable code and targets; acceptance requires evidence tied to exact tested context.

**Non-goals:**

- Deploy to real consumers, expand credentials, implement production infrastructure or treat static syntax checks as hosted proof.

**Acceptance criteria:**

- Necessary cross-repository boundaries and both initial runtimes are demonstrated against MP02/MP05/MP06.
- Central repository token authority is not presumed to extend to arbitrary targets; missing access never counts as success.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Exercise approved reference fixtures using Python and PowerShell and the real hosted boundaries that local checks cannot prove.
- Inspect permissions, trust/checkouts, injection/path controls, source immutability, workflow-file writes and recovery diagnostics.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Trust and security constraints:**

Validate source-read and destination-write authority separately, privilege boundaries and trusted execution assumptions.

**Required fixtures:**

MP05/MP06 reference artifacts and explicitly approved hosted test repositories with known revisions.

**Documentation impact:**

Produce the accepted written governance/review/validation evidence appropriate to this pass without silently changing implementation.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Required authorization, credentials, platform access or credible evidence is absent; report the exact blocker/inconclusive result.

**Review gate:**

Independent security/feasibility review checks observed evidence and limitations against the threat model; maintainer acceptance is required.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP08` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp08"></a>

### MP08 — Prove cumulative composition with disposable services

**Identifier:**

`MP08`

**Title:**

Prove cumulative composition with disposable services

**Mode:**

implementation

**Objective:**

Deliver a minimal toy-service prototype demonstrating the agreed cumulative composition topology.

**Rationale:**

A bounded end-to-end slice reduces risk before the early factory and major production runtime investment.

**Dependencies:**

- `MP03` — accepted and fully finalized under the installed protocols.
- `MP05` — accepted and fully finalized under the installed protocols.
- `MP07` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows prototype/test artifacts and explicitly approved disposable fixture environments.
- Allowed surfaces: Toy executable services, prototype composition/validation harness, fixtures, tests and explanatory documentation.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- A reproducible shared-tree prototype with ordered transformations, frozen-candidate validation and structured failure/no-op examples.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- No package-specific central business logic, automatic merge or publication during service execution.

**Non-goals:**

- Promote toy services/policy directly to production or expand into the final runtime before prototype acceptance.

**Acceptance criteria:**

- One working tree is shared; required failure and ownership conflict reject publication; an unchanged rerun is a no-op.
- Prototype policy fixtures remain clearly non-production and do not create a competing ownership authority.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Exercise two ordered transformations, validators on the final tree, required execution/validation failure, conflict rejection and a repeated unchanged run.
- Inspect actual candidate changes and reports rather than relying on service success claims.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

A proof implementation of the accepted service/ownership contracts, not a new parallel API.

**Trust and security constraints:**

Apply D01/D09: approved immutable sources, exact destination/write authority, safe paths/arguments and no unapproved execution or credential exposure.

**Required fixtures:**

Disposable Python/PowerShell toy services, conflict/failure inputs and deterministic candidate comparisons.

**Rollback:**

Preserve a coherent accepted baseline/operative caller and target-owned state. Validate failure preservation and the applicable approved recovery path before enabling replacement behavior.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Prototype artifacts remain inert and cannot replace an operative consumer caller.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- The slice requires a different topology, unexplained authority or a second production policy interpreter.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP09` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp09"></a>

### MP09 — Deliver the central and external package factory

**Identifier:**

`MP09`

**Title:**

Deliver the central and external package factory

**Mode:**

implementation

**Objective:**

Implement create-package with approved production schemas, class-specific templates and PR-only central/external source authoring.

**Rationale:**

Accepted contracts and prototype evidence permit early package authoring before the final registrar and installer exist.

**Dependencies:**

- `MP06` — accepted and fully finalized under the installed protocols.
- `MP07` — accepted and fully finalized under the installed protocols.
- `MP08` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows administrative implementation; exact separately approved source/test repositories for generated PRs.
- Allowed surfaces: Factory workflow/engine, schema materialization, class templates, documentation, fixtures and tests.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- A default-central factory supporting explicit external repository/path, class selection and creation confirmation.
- Generated descriptors, class-appropriate payload/contribution/runtime examples, documentation, fixtures and tests delivered through a reviewed source PR.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Only Class 2 receives inert execute/validate examples; approved contracts remain the schema authority.

**Non-goals:**

- Create package-specific runtime workflows, implement the final installer or merge generated PRs automatically.

**Acceptance criteria:**

- Both classes are generated and validate against the approved schemas in central-default and external-path tests.
- Unrelated existing content is never overwritten; creation does not implicitly register, install or activate a package.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Exercise both classes and source topologies, unsafe paths, invalid identities, false/missing confirmation, existing content and generated descriptor/schema validation.
- Verify hosted PR provenance and the exact generated diff in the approved test source repository.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

create-package inputs/defaults, approved schemas, generated package layout and author documentation.

**Trust and security constraints:**

Approved source-write authority, explicit confirmation, safe relative paths and no implicit package execution/registration.

**Required fixtures:**

Class 1/Class 2 generation in the central-default fixture and an explicit external test repository/path.

**Rollback:**

Failed planning writes nothing; failed generation/publication preserves unrelated source state and reports recoverable proposal identity.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Creation exceeds source authority, overwrites unrelated content or requires automatic registration/activation.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP10` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp10"></a>

### MP10 — Extract the existing document ownership capability

**Identifier:**

`MP10`

**Title:**

Extract the existing document ownership capability

**Mode:**

implementation

**Objective:**

Extract document-guard as the reusable authoritative capability while preserving existing Sync ownership behavior.

**Rationale:**

Production ownership extensions must build on one conserved implementation rather than precede or duplicate its extraction.

**Dependencies:**

- `MP01` — accepted and fully finalized under the installed protocols.
- `MP03` — accepted and fully finalized under the installed protocols.
- `MP06` — accepted and fully finalized under the installed protocols.
- `MP09` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows existing Sync implementation and the approved document-guard package root.
- Allowed surfaces: Shared capability source/metadata/API, equivalence fixtures, tests/docs and compatibility delegation required by active legacy invocations.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- The reusable document-guard capability with package metadata, supported API, tests and documentation.
- A verified delegation/reference map ensuring active legacy calls use the extracted authority where necessary.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- MP11 alone owns the approved semantic extensions; extraction preserves legacy whole-file/marker semantics.

**Non-goals:**

- Implement the new policy model prematurely, migrate consumers or remove still-operative entry points.

**Acceptance criteria:**

- Existing whole-file, marker, malformed-input and effective whole-file fallback behavior is conserved.
- One interpreter remains authoritative and all operative legacy invocations continue resolving.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Compare legacy and extracted behavior on successful/invalid marker cases, byte-exact whole files, missing source delimiters, newline/UTF-8 boundaries and diagnostics.
- Trace every affected import/invocation and run focused equivalence/compatibility checks in disposable environments.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

The standalone ownership capability/API and its package metadata; preserved compatibility delegates where required.

**Trust and security constraints:**

Apply D01/D09: approved immutable sources, exact destination/write authority, safe paths/arguments and no unapproved execution or credential exposure.

**Migration and compatibility:**

Preserve old invocation behavior until separately migrated and prove source-to-delegate reference closure.

**Rollback:**

Retain a coherent supported legacy invocation path; do not require downstream local interpreter patches.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Extraction changes semantics, leaves a second interpreter or breaks an active legacy call.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP11` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp11"></a>

### MP11 — Implement the shared ownership-policy extensions

**Identifier:**

`MP11`

**Title:**

Implement the shared ownership-policy extensions

**Mode:**

implementation

**Objective:**

Implement the approved versioned claim parser, authorization, protected regions, overlap detection and policy diagnostics on document-guard.

**Rationale:**

The generic runtime and both domain services require the new policy matrix after conserved extraction is accepted.

**Dependencies:**

- `MP03` — accepted and fully finalized under the installed protocols.
- `MP10` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows document-guard capability and focused interoperability/contract tests.
- Allowed surfaces: The sole shared ownership implementation, policy-claim registry parser, diagnostics, tests and documentation.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- Approved writer/region authorization, exclusive/user/non-writable scopes, protected exceptions, policy transitions and conflict handling.
- A supported consumption path for both Python and PowerShell services.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Ownership authorizes regions/writers; services retain their separate semantic validation responsibility.

**Non-goals:**

- Implement a second package catalog or embed service-specific revision logic in ownership policy.

**Acceptance criteria:**

- Allowed/forbidden writer, overlapping claim, malformed marker and invalid-transition cases fail or succeed as specified.
- Canonical projection preserves approved exceptions without silent legacy weakening; registration cannot self-authorize protected writes.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Execute the accepted scope/overlap/authority matrix including incoming and service-generated changes.
- Verify both language adapters consume the same interpreter and exercise fail-closed diagnostics and approved policy overrides.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

The versioned ownership-claim contract, diagnostics and supported cross-language capability invocation.

**Trust and security constraints:**

Validate explicit writer identities, exclusive/non-writable regions and authorized policy transitions/overrides.

**Migration and compatibility:**

Keep legacy policy behavior unless the accepted versioned migration explicitly changes it.

**Rollback:**

Preserve a coherent accepted baseline/operative caller and target-owned state. Validate failure preservation and the applicable approved recovery path before enabling replacement behavior.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- A package bypasses existing policy, an exception silently weakens authority or another interpreter is required.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP12` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp12"></a>

### MP12 — Deliver generic service loading and execution

**Identifier:**

`MP12`

**Title:**

Deliver generic service loading and execution

**Mode:**

implementation

**Objective:**

Implement production adapters, service loading, execution context, compatibility and top-level ordering from the accepted contracts.

**Rationale:**

Attribution and cumulative validation need real generic execution consuming accepted schemas and shared policy.

**Dependencies:**

- `MP05` — accepted and fully finalized under the installed protocols.
- `MP06` — accepted and fully finalized under the installed protocols.
- `MP11` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows generic runtime, adapters, loader and test/documentation artifacts.
- Allowed surfaces: Approved source loading, Python/PowerShell adapters, context/result handling, dependency ordering and bounded execution.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- The production loader/executor/adapters with compatibility checks, top-level ordering, structured outcomes, tests and docs.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Services execute on the supplied coherent context, call trusted libraries and never independently publish maintenance proposals.

**Non-goals:**

- Implement the publisher, bypass source approval or revive package-specific callable YAML interfaces.

**Acceptance criteria:**

- Approved pinned Python and PowerShell services execute the same contract; cycles, missing dependencies, invalid entry points and invalid results fail.
- Adding a compatible package requires no package identity or business logic in the central loader/executor.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Run language contract fixtures plus ordering, dependency, compatibility, timeout/argument and malformed-result cases.
- Inspect trusted source resolution and prove service execution has no independent PR-publication path.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Production materialization of the MP05/MP06 service/adaptor/loading contracts.

**Trust and security constraints:**

Approved immutable execution sources, bounded invocation, safe arguments and explicit credential exposure.

**Required fixtures:**

Both runtime languages plus cyclic/missing/incompatible dependency and invalid entry/result cases.

**Rollback:**

Preserve a coherent accepted baseline/operative caller and target-owned state. Validate failure preservation and the applicable approved recovery path before enabling replacement behavior.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Loading requires package-specific central logic, unapproved code or an unsupported invocation/validation assumption.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP13` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp13"></a>

### MP13 — Deliver service changeset attribution

**Identifier:**

`MP13`

**Title:**

Deliver service changeset attribution

**Mode:**

implementation

**Objective:**

Implement a structured execution journal correlating services, candidate snapshots, changes and errors.

**Rationale:**

Final validation and historical reconciliation need evidence linking observed changes to real execution without invented attribution.

**Dependencies:**

- `MP12` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows generic runtime/journal implementation and focused fixtures/docs.
- Allowed surfaces: Per-service change capture, snapshot/result correlation, diagnostics and journal integrity behavior.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- A structured journal of services, snapshots, changed paths, results and errors with tests and documentation.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Uncertainty is preserved; journal metadata cannot independently authorize content changes or publication.

**Non-goals:**

- Infer causation without evidence, replace global ownership validation or publish proposals.

**Acceptance criteria:**

- Pre-existing and service-introduced changes are distinguishable where evidence permits, and limitations remain explicit.
- Failed/partial service execution, candidate changes and inconsistent journal records have defined diagnostics.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Compare real before/after candidate states and journal records for success, no-op, failure and partial execution.
- Exercise ambiguous attribution and tampered/inconsistent records; require evidence-backed correlation rather than success labels.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Versioned structured changeset/journal and error-correlation outputs consistent with MP05.

**Trust and security constraints:**

Journal integrity and provenance must survive candidate/service failures without granting new authority.

**Rollback:**

Preserve a coherent accepted baseline/operative caller and target-owned state. Validate failure preservation and the applicable approved recovery path before enabling replacement behavior.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Attribution would be fabricated or the journal cannot be reconciled with the actual candidate.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP14` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp14"></a>

### MP14 — Deliver immutable snapshots and historical change reconciliation

**Identifier:**

`MP14`

**Title:**

Deliver immutable snapshots and historical change reconciliation

**Mode:**

implementation

**Objective:**

Implement coherent source/configuration/runtime snapshots, historical changed-path selection, freshness, optimistic concurrency and recovery.

**Rationale:**

Accepted validation and publication must not depend on mutable or incomplete inputs or forget outstanding historical changes.

**Dependencies:**

- `MP12` — accepted and fully finalized under the installed protocols.
- `MP13` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows generic context/history/concurrency implementation and approved disposable remote-state fixtures.
- Allowed surfaces: Input resolution/identity, history accounting/checkpoint behavior, freshness checks, retry/recovery and diagnostics.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- Immutable context/source/configuration identities and historical selection integrated with service context/journal.
- Optimistic concurrency, freshness rejection and recovery behavior with failure/race tests and operator guidance.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Do not acknowledge away outstanding work on an unsuccessful/superseded operation or infer mutual exclusion from a lease.

**Non-goals:**

- Introduce a distributed locking requirement or accept the publisher before freshness/recovery controls exist.

**Acceptance criteria:**

- Missed changes remain discoverable after failed, canceled and superseded runs; retries recover without losing work.
- Stale runs cannot corrupt proposals; incomplete history or inconsistent source identities cannot silently yield a partial successful transaction.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Exercise historical dirty paths, cancellation/failure/supersession, unavailable history, source changes, concurrent runs and stale remote branch/proposal state.
- Verify retry accounting and candidate/context identities before accepting any publication assumptions.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Snapshot/history-selection, freshness and recovery state contracts consumed by validation/publication.

**Trust and security constraints:**

Apply D01/D09: approved immutable sources, exact destination/write authority, safe paths/arguments and no unapproved execution or credential exposure.

**Migration and compatibility:**

Define recovery/migration of existing historical accounting without silently discarding pending work.

**Rollback:**

Failures and retries preserve outstanding work and previously reviewed proposals; stale state fails before unsafe publication.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Required history is unavailable, identities disagree or remote state invalidates the expected publication context.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP15` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp15"></a>

### MP15 — Deliver final candidate validation

**Identifier:**

`MP15`

**Title:**

Deliver final candidate validation

**Mode:**

implementation

**Objective:**

Implement candidate freeze, required read-only validators, global ownership/journal checks and structured validation aggregation.

**Rationale:**

The publisher must operate only on one successfully validated cumulative candidate with an authenticated identity.

**Dependencies:**

- `MP11` — accepted and fully finalized under the installed protocols.
- `MP13` — accepted and fully finalized under the installed protocols.
- `MP14` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows generic validation gate and focused service/candidate fixtures.
- Allowed surfaces: Candidate identity/freeze, validator orchestration, purity/mutation checks, ownership/journal integrity and result aggregation.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- A final immutable-candidate gate rejecting any required execution, validation, ownership, journal or unauthorized-mutation failure.
- Read-only validator/report handling, tests and diagnostics tied to the exact candidate.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- No cumulative content mutation occurs after the final validated candidate is fixed; reports retain usable failure evidence.

**Non-goals:**

- Repair content inside validation, publish invalid candidates or substitute only syntax checks for required semantic validation.

**Acceptance criteria:**

- All validators assess the same cumulative candidate; disallowed service/validator mutations are rejected.
- Any required failure prevents publication; report outputs do not accidentally modify candidate content.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Exercise required validator failure, invalid reports, ownership/journal mismatches, validator writes and a changing candidate.
- Inspect actual candidate identity/tree and report placement; distinguish observed mutation detection from stronger purity claims.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Final candidate identity and aggregated validation/publication-eligibility outputs.

**Trust and security constraints:**

Enforce approved writer boundaries and the accepted validator-purity model; do not overstate what mutation detection proves.

**Rollback:**

Preserve a coherent accepted baseline/operative caller and target-owned state. Validate failure preservation and the applicable approved recovery path before enabling replacement behavior.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- The validated identity cannot be tied to the proposed tree or the required validation-purity boundary cannot be supported.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP16` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp16"></a>

### MP16 — Deliver one-PR publication and safe reconciliation

**Identifier:**

`MP16`

**Title:**

Deliver one-PR publication and safe reconciliation

**Mode:**

implementation

**Objective:**

Implement safe creation/reconciliation of one maintenance proposal from the validated candidate.

**Rationale:**

The hosted composition workflow needs publication with optimistic freshness and user-proposal protection already established.

**Dependencies:**

- `MP14` — accepted and fully finalized under the installed protocols.
- `MP15` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows publisher and exact approved disposable destination/proposal fixtures.
- Allowed surfaces: Proposal identity, branch/API freshness, cumulative diff publication, no-op/update behavior and diagnostics.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- A one-PR publisher with reviewable candidate provenance, safe update/reconciliation and tests/operator documentation.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- One cumulative maintenance proposal; services never publish independently and target branches are never auto-merged.

**Non-goals:**

- Force through user conflicts, bypass validation/freshness or coordinate transactions across multiple destination repositories.

**Acceptance criteria:**

- No auto-merge, duplicate uncontrolled proposal, stale overwrite or publication after required failure occurs.
- User-modified proposals are preserved; proposal ownership and expected remote identities are verified before updates.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Exercise first publication, rerun, no-op, existing proposal, user modifications, stale branch and concurrent updates.
- Verify the actual remote proposal/tree corresponds to the accepted candidate and invalid runs publish nothing.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Maintenance proposal identity, publication/reconciliation inputs/outputs and diagnostics.

**Trust and security constraints:**

Use only authorized destination credentials and verify Git/API state before proposal mutation.

**Rollback:**

Preserve the prior reviewed/user-modified proposal on failure; document safe retry and conflict handling.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Proposal ownership, authorization or expected remote state is ambiguous or changes before a consequential update.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP17` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp17"></a>

### MP17 — Deliver central composition and the destination caller

**Identifier:**

`MP17`

**Title:**

Deliver central composition and the destination caller

**Mode:**

implementation

**Objective:**

Deliver the generic callable composition workflow and a minimal pinned destination caller.

**Rationale:**

Production package consolidation and installation require a proven hosted entry point for the accepted generic runtime.

**Dependencies:**

- `MP12` — accepted and fully finalized under the installed protocols.
- `MP15` — accepted and fully finalized under the installed protocols.
- `MP16` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows central workflow and exact approved disposable destination caller repository.
- Allowed surfaces: Generic workflow/caller wiring, runtime inputs/outputs/permissions, integration fixtures and documentation.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- The central composition workflow and thin destination caller invoking pinned central implementation without engine duplication.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Central workflow/caller wiring preserves the generic script runtime and no-auto-merge model.

**Non-goals:**

- Migrate real adopters, enable incomplete package replacements or expose per-package callable execution workflows.

**Acceptance criteria:**

- A hosted fixture exercises execution, final validation and publication together with the accepted permissions/context.
- No package-specific runtime YAML API or production consumer migration is introduced.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Invoke the pinned central engine from a real approved hosted fixture and verify context, outputs, candidate and PR behavior.
- Inspect caller thinness, source provenance and failure propagation through the complete workflow boundary.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Generic callable composition workflow and minimal destination caller contract.

**Trust and security constraints:**

Verify hosted source access, caller permissions and credential propagation against MP07 evidence.

**Required fixtures:**

An approved hosted consumer fixture tied to exact central and destination revisions.

**Rollback:**

Preserve a coherent accepted baseline/operative caller and target-owned state. Validate failure preservation and the applicable approved recovery path before enabling replacement behavior.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- The caller needs copied engine logic, package-specific workflow behavior or unsupported access/permission assumptions.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP18` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp18"></a>

### MP18 — Consolidate Managed File Sync as a standard runtime package

**Identifier:**

`MP18`

**Title:**

Consolidate Managed File Sync as a standard runtime package

**Mode:**

migration

**Objective:**

Consolidate production Sync into one standard package with execute/validate, shared ownership, immutable projection and approved lifecycle behavior.

**Rationale:**

The generic installer must bootstrap a real compatible Sync package rather than certify only a toy placeholder before production conversion.

**Dependencies:**

- `MP04` — accepted and fully finalized under the installed protocols.
- `MP10` — accepted and fully finalized under the installed protocols.
- `MP11` — accepted and fully finalized under the installed protocols.
- `MP12` — accepted and fully finalized under the installed protocols.
- `MP14` — accepted and fully finalized under the installed protocols.
- `MP15` — accepted and fully finalized under the installed protocols.
- `MP17` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows existing Sync responsibilities and its MP02/MP06-approved package root; external callers remain compatibility evidence.
- Allowed surfaces: Sync source/schema/docs/tests consolidation, service entry points, lifecycle/receipt integration and necessary legacy delegates/references.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- A self-contained production Sync package consuming the shared ownership authority and standard script service contract.
- Immutable projection, approved lifecycle/receipt behavior, compatibility mapping, focused tests and complete module/migration documentation.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Real production Sync is available before installer certification; generic execution does not publish a separate Sync PR.

**Non-goals:**

- Migrate production consumers, delete active legacy entry points or add a supported package-specific callable YAML wrapper.

**Acceptance criteria:**

- Projection, markers, globs, lifecycle behavior and unchanged reruns satisfy the approved contracts.
- Malformed/incomplete sources and planning failures preserve destination state; active legacy calls remain coherent until migration.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Run focused projection/marker/glob/lifecycle fixtures, receipt and failure-preservation scenarios, source completeness and convergence checks.
- Trace old/new imports, workflow invocations, schemas, configuration and documentation; verify no second interpreter or new per-package callable workflow.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Standard Sync descriptor, service/context contract, projection/lifecycle inputs and compatible legacy invocation boundaries.

**Trust and security constraints:**

Apply D01/D09: approved immutable sources, exact destination/write authority, safe paths/arguments and no unapproved execution or credential exposure.

**Migration and compatibility:**

Preserve operative callers/delegation until accepted migration/removal; explicitly migrate legacy seed semantics.

**Rollback:**

Retain a coherent invocation and configuration rollback path preserving user data and durable seed history.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Consolidation breaks an active caller, duplicates ownership, loses state or needs an unapproved public-contract change.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP19` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp19"></a>

### MP19 — Deliver the trusted registry and package catalog

**Identifier:**

`MP19`

**Title:**

Deliver the trusted registry and package catalog

**Mode:**

implementation

**Objective:**

Implement deterministic approved package/version discovery and immutable source resolution for central and external package roots.

**Rationale:**

Registrar and installation planning need a trusted catalog preserving identities, compatibility and source provenance.

**Dependencies:**

- `MP06` — accepted and fully finalized under the installed protocols.
- `MP07` — accepted and fully finalized under the installed protocols.
- `MP18` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows registry/catalog/resolution implementation and approved read-only source fixtures.
- Allowed surfaces: Registry/catalog parsing, identity/version/approval checks, source resolution, diagnostics, tests and documentation.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- The trusted package/version catalog and deterministic resolver supporting both preferred central and explicit external paths.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- The package catalog is separate from policy claims; package identity survives source relocation.

**Non-goals:**

- Install packages, grant ownership through registration or constrain all approved sources to the central path.

**Acceptance criteria:**

- Duplicate identities, unsafe paths, incompatible versions, unapproved revisions, unavailable sources and inconsistent provenance are rejected.
- Registration/resolution does not implicitly execute package code or substitute moving content for the approved revision.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Exercise central/external sources, duplicate/incompatible/unapproved entries, unavailable/private reads and immutable resolution.
- Verify provenance coherence, safe paths and deterministic results against the accepted registration schema.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Approved registry/catalog and source/version resolution contracts from MP06.

**Trust and security constraints:**

Authenticate source identity/approval, path safety and immutable content without evaluating untrusted package code.

**Rollback:**

Preserve a coherent accepted baseline/operative caller and target-owned state. Validate failure preservation and the applicable approved recovery path before enabling replacement behavior.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Data causes unapproved execution, a source cannot be authenticated or a mutable revision is silently substituted.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP20` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp20"></a>

### MP20 — Deliver registrar administration

**Identifier:**

`MP20`

**Title:**

Deliver registrar administration

**Mode:**

implementation

**Objective:**

Implement reviewable registration, revision update and retirement administration maintaining the approved registry/catalog.

**Rationale:**

The dependency planner and hosted certification need a supported, deterministic administrative path for catalog changes.

**Dependencies:**

- `MP19` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows registrar/control-plane implementation and exact approved registration/test sources.
- Allowed surfaces: Administrative workflows/engine, reviewed catalog updates, approval validation, diagnostics, tests and docs.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- Registrar workflows for new registration, approved revision updates and retirement with deterministic reviewable changes.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Administrative registration is distinct from installation and runtime privileges.

**Non-goals:**

- Merge changes automatically, execute unreviewed package code or silently remove installed packages.

**Acceptance criteria:**

- Catalog changes preserve source/version identity and approval; duplicate/invalid requests are rejected.
- Registration and retirement do not independently activate services or uninstall existing consumers.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Exercise new/update/duplicate/invalid-source/retirement requests and compare exact registry/catalog diffs.
- Verify approvals, provenance, deterministic output and hosted administrative boundaries where required.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Registrar administrative inputs, reviewed catalog outputs and retirement semantics.

**Trust and security constraints:**

Separate catalog-write authority from source-read and destination-install authority.

**Rollback:**

Rejected/failed requests preserve the prior catalog; accepted revision/retirement changes remain reviewable and recoverable.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- A request exceeds catalog/source authority, bypasses existing ownership or implicitly changes consumer activation/install state.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP21` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp21"></a>

### MP21 — Deliver dependency resolution and installation planning

**Identifier:**

`MP21`

**Title:**

Deliver dependency resolution and installation planning

**Mode:**

implementation

**Objective:**

Implement complete dependency/payload closure, compatibility and ownership analysis for both package classes before writes.

**Rationale:**

Materialization and installation require a valid full plan including real Sync/runtime bootstrap and existing destination state.

**Dependencies:**

- `MP04` — accepted and fully finalized under the installed protocols.
- `MP06` — accepted and fully finalized under the installed protocols.
- `MP19` — accepted and fully finalized under the installed protocols.
- `MP20` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows dependency/planning implementation and read-only/disposable destination fixtures.
- Allowed surfaces: Dependency solver, capability/runtime resolution, payload planning, conflict analysis, diagnostics, tests and documentation.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- A generic installation planner resolving both classes, required Sync/runtime infrastructure, dependencies, payloads and conflicts.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Planning performs no writes and treats capability dependencies separately from scheduled services.

**Non-goals:**

- Apply payloads, overwrite manifests or solve a bootstrap problem with no-op service stubs.

**Acceptance criteria:**

- Shared, missing/incompatible and cyclic dependencies have explicit outcomes; complete source/payload closure precedes any write.
- Existing destination ownership/state and source approvals are preserved and no package-specific central business logic is required.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Exercise empty/existing destination plans, shared providers, missing/incompatible dependencies, cycles and Sync/runtime bootstrap.
- Verify source completeness, ownership conflicts and failure-before-write on incomplete/ambiguous plans.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Versioned dependency and complete installation-plan contracts derived from MP04/MP06.

**Trust and security constraints:**

Resolve only approved immutable sources and validate the complete authority/path plan before writes.

**Rollback:**

Preserve a coherent accepted baseline/operative caller and target-owned state. Validate failure preservation and the applicable approved recovery path before enabling replacement behavior.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- The plan is incomplete, cyclic, incompatible or ownership-conflicting; do not proceed to materialization.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP22` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp22"></a>

### MP22 — Deliver manifest merging and initial asset materialization

**Identifier:**

`MP22`

**Title:**

Deliver manifest merging and initial asset materialization

**Mode:**

implementation

**Objective:**

Implement structural contribution merging, provenance-preserving managed identities and safe initial payload/receipt materialization.

**Rationale:**

Installer bootstrap must materialize the accepted plan before installed Sync exists while reusing approved projection and ownership semantics.

**Dependencies:**

- `MP04` — accepted and fully finalized under the installed protocols.
- `MP11` — accepted and fully finalized under the installed protocols.
- `MP18` — accepted and fully finalized under the installed protocols.
- `MP21` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows merger/materializer implementation with disposable manifests, destinations and immutable source fixtures.
- Allowed surfaces: Structured contribution merge, initial projection/receipts, shared capability reuse, preservation/idempotence tests and docs.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- A generic structural sync-manifest merger and bootstrap materializer preserving package identity/provenance.
- Coherent first-provisioning/receipt handling using the approved projection/ownership authorities.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Contributions do not authorize overwriting the caller's whole manifest; true seeds preserve consumed history.

**Non-goals:**

- Assume Sync is installed already, blindly text-insert configuration or prune files by directory membership.

**Acceptance criteria:**

- Unrelated manifest entries and target-owned content are preserved; duplicates, conflicts and malformed input fail.
- Initial seeds and receipts are coherent, reruns are idempotent and planning failures perform no writes.
- Bootstrap works without preinstalled Sync and creates no divergent projection/ownership interpreter.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Exercise missing/existing manifests, unrelated entries, duplicate identities/targets, malformed sources, receipt/seed boundaries and reruns.
- Inspect full output/state after failure and verify immutable source projection and exact preservation of user-owned data.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Structural contribution merge and initial materialization/receipt behavior.

**Trust and security constraints:**

Apply D01/D09: approved immutable sources, exact destination/write authority, safe paths/arguments and no unapproved execution or credential exposure.

**Migration and compatibility:**

Preserve unrelated existing entries and accepted lifecycle semantics; migrate conflicting old registrations only explicitly.

**Rollback:**

Validate the whole plan before writes and preserve coupled target content/state on failure.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Ownership is ambiguous, complete source projection is unavailable or reuse would require a second divergent interpreter.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP23` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp23"></a>

### MP23 — Deliver the generic installer

**Identifier:**

`MP23`

**Title:**

Deliver the generic installer

**Mode:**

implementation

**Objective:**

Implement PR-only installation into an explicitly selected destination with complete payload, dependencies, state and caller wiring.

**Rationale:**

Accepted planning/materialization and production Sync permit coherent central installation without specialized adopter installers.

**Dependencies:**

- `MP17` — accepted and fully finalized under the installed protocols.
- `MP18` — accepted and fully finalized under the installed protocols.
- `MP20` — accepted and fully finalized under the installed protocols.
- `MP21` — accepted and fully finalized under the installed protocols.
- `MP22` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows installer and exact separately authorized disposable destination/source repositories.
- Allowed surfaces: Central installer workflow/engine, dependency/bootstrap integration, coherent destination proposal and diagnostics/tests/docs.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- The generic installer producing one reviewed destination PR containing required payload, dependencies, merged configuration, receipts and runtime caller changes.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Installation and runtime execution remain separate privilege boundaries; no adopter-side specialized bootstrap dependency is required.

**Non-goals:**

- Merge installation PRs, modify repository settings/secrets or coordinate multi-target transactions.

**Acceptance criteria:**

- Empty/existing repositories and production Sync plus an asset package install through one coherent proposal.
- Private approved sources, reruns and changed destination state preserve provenance and user-owned content; no automatic merge occurs.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Exercise empty/existing destination, Sync bootstrap, asset/runtime combinations, private source access, rerun and stale target cases.
- Verify actual proposal closure, ownership, receipt coherence, candidate validation and no partial or unauthorized destination delivery.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Generic installer inputs, destination plan/proposal outputs and supported bootstrap contract.

**Trust and security constraints:**

Explicit destination identity/authority, approved source reads and safe workflow/configuration writes.

**Required fixtures:**

Approved hosted empty/existing destinations and production Sync plus representative Class 1/Class 2 packages.

**Rollback:**

Coupled installation changes remain one coherent proposal; failed preparation/publication preserves target-owned state and prior proposals.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Closure is partial, authorization/source access is missing, ownership conflicts or destination state becomes stale.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP24` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp24"></a>

### MP24 — Deliver package validation, repair, upgrade and uninstall planning

**Identifier:**

`MP24`

**Title:**

Deliver package validation, repair, upgrade and uninstall planning

**Mode:**

implementation

**Objective:**

Implement consistent package lifecycle operations with reviewable plans and supported execution paths.

**Rationale:**

Administrative certification needs safe operation after initial installation, including preserved dependencies and consumed seed history.

**Dependencies:**

- `MP04` — accepted and fully finalized under the installed protocols.
- `MP23` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows lifecycle administration and explicitly approved disposable installed-destination fixtures.
- Allowed surfaces: Validation/repair/upgrade/removal plans and execution boundaries, state compatibility, diagnostics, tests and operator docs.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- Generic Validate, Repair, Upgrade and uninstall/removal planning with approved lifecycle execution paths.
- Ownership-proven stale asset handling, dependency preservation and durable receipt retention.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Lifecycle semantics match installation/Sync; removal does not silently claim or destroy target-owned content.

**Non-goals:**

- Unrestricted uninstall hooks, automatic data deletion or implicit reseeding during repair/upgrade.

**Acceptance criteria:**

- Dependent packages, user-owned content and consumed true seeds remain protected across version change, opt-out and removal.
- Missing files and repeated operations follow the four-policy contract; stale asset deletion requires complete ownership/membership evidence.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Exercise upgrades, missing/existing files, opt-out, retained receipts, shared dependencies, stale assets and reruns.
- Verify conflict/malformed/incomplete plan preservation and that true seeds never reappear without explicit authorization.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Validate/Repair/Upgrade/uninstall planning and approved lifecycle operation contracts.

**Trust and security constraints:**

Apply D01/D09: approved immutable sources, exact destination/write authority, safe paths/arguments and no unapproved execution or credential exposure.

**Migration and compatibility:**

Retain receipt/state identity through upgrades, opt-out and source relocation; preserve backward-compatible legacy mapping.

**Rollback:**

Require recoverable lifecycle plans and preserve user content/receipt history on failed or rejected changes.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Removal infers ownership from a directory, erases seed history or breaks a preserved dependency.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP25` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp25"></a>

### MP25 — Certify package administration and installation

**Identifier:**

`MP25`

**Title:**

Certify package administration and installation

**Mode:**

validation-only

**Objective:**

Establish hosted evidence for registrar through catalog, planner, installer and consumer operation.

**Rationale:**

Real platform access and production Sync bootstrap must be certified before migrating existing package authorities and consumers.

**Dependencies:**

- `MP20` — accepted and fully finalized under the installed protocols.
- `MP23` — accepted and fully finalized under the installed protocols.
- `MP24` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: Exact approved hosted source/destination fixtures; BionicCode/workflows implementation is fixed during validation.
- Allowed surfaces: Hosted acceptance runs, proposal inspection, boundary verification and written certification with exact revisions.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- Reproducible hosted administrative/install evidence for both classes, central/external sources and real Sync bootstrap.
- Security, conflict, rerun and representative recovery results with explicit limitations.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Certification records observed scope and uncertainty without changing implementation or activating real consumers.

**Non-goals:**

- Patch shared implementation during validation, merge test proposals automatically or claim full migrated-platform certification prematurely.

**Acceptance criteria:**

- Registrar-to-consumer behavior is demonstrated in GitHub Actions at matching source/target revisions.
- Local-only fixtures do not substitute for hosted access/integration and required failures are not reported as passes.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Run the accepted hosted matrix for source topology, class, bootstrap, privilege, conflict, rerun and recovery cases.
- Inspect actual PR/destination closure, permissions, immutable sources and lifecycle outcomes; correlate logs/reports to exact versions.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Required fixtures:**

Approved hosted source/destination fixtures for both classes and production Sync.

**Documentation impact:**

Produce the accepted written governance/review/validation evidence appropriate to this pass without silently changing implementation.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Evidence is missing/inconclusive/mismatched or an implementation defect requires correction beyond validation scope.

**Review gate:**

Independent administrative/security integration review verifies hosted artifacts and limitations; maintainer acceptance is required.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP26` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp26"></a>

### MP26 — Deliver protected revision migration tooling

**Identifier:**

`MP26`

**Title:**

Deliver protected revision migration tooling

**Mode:**

implementation

**Objective:**

Implement the approved protected revision format, converter, compatibility handling and rollback tooling without live conversion.

**Rationale:**

The consolidated Document Revisions service needs independently validated migration support before consuming legacy documents.

**Dependencies:**

- `MP03` — accepted and fully finalized under the installed protocols.
- `MP11` — accepted and fully finalized under the installed protocols.
- `MP18` — accepted and fully finalized under the installed protocols.
- `MP25` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows future Document Revisions package and disposable document/ownership fixtures.
- Allowed surfaces: Format implementation, converter, migration/rollback support, compatibility fixtures, tests and documentation.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- The MP03 format implementation and converter preserving proven tool-owned metadata, unrelated YAML content, lineage and history.
- Malformed/ambiguous input diagnostics, reversible migration guidance and shared-ownership fixtures.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Use the approved format/policy and one ownership authority; migration tooling stays inert until integration/cutover is accepted.

**Non-goals:**

- Enable live conversion, publish repair PRs or independently redesign protected-region/lineage policy.

**Acceptance criteria:**

- Only proven tool-owned metadata is migrated; unrelated fields/content and history are preserved.
- Repeated conversion is a no-op, rollback is validated and format-only conversion is not treated as a new body revision.
- No live document is converted while only an incompatible legacy writer is available.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Exercise legacy formats, unrelated YAML fields, ambiguous ownership, malformed input, newline/encoding boundaries, repeated conversion and rollback.
- Inspect bytes/semantic content and shared ownership outcomes on disposable fixtures, including no-write-on-failure.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Approved protected revision format and conversion/compatibility interface consumed by MP27.

**Trust and security constraints:**

Apply D01/D09: approved immutable sources, exact destination/write authority, safe paths/arguments and no unapproved execution or credential exposure.

**Migration and compatibility:**

Preserve unrelated YAML front matter, legacy lineage/history and explicitly supported old formats; reject ambiguous ownership.

**Required fixtures:**

Disposable mixed/legacy/protected documents with unrelated front matter, malformed/tampered input and rollback expectations.

**Rollback:**

Prove reversible conversion and failure preservation before any compatible service is enabled.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Tooling may merge independently only while inert for live documents and compatible with the existing active writer.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Metadata ownership cannot be proven, conversion loses unrelated state or live conversion would precede compatible execution.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP27` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp27"></a>

### MP27 — Consolidate Document Revisions and integrate protected-region migration

**Identifier:**

`MP27`

**Title:**

Consolidate Document Revisions and integrate protected-region migration

**Mode:**

migration

**Objective:**

Deliver a self-contained Document Revisions runtime package integrating the standard service contract, shared ownership and accepted conversion tooling.

**Rationale:**

Asset/consumer migrations need an accepted live-capable service that preserves revision history and converges with Sync.

**Dependencies:**

- `MP05` — accepted and fully finalized under the installed protocols.
- `MP11` — accepted and fully finalized under the installed protocols.
- `MP14` — accepted and fully finalized under the installed protocols.
- `MP15` — accepted and fully finalized under the installed protocols.
- `MP17` — accepted and fully finalized under the installed protocols.
- `MP18` — accepted and fully finalized under the installed protocols.
- `MP26` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows metadata responsibilities and approved Document Revisions package root; approved disposable service/consumer fixtures.
- Allowed surfaces: Source/schema/docs/tests consolidation, execute/validate integration, migration/lineage/history behavior and necessary legacy compatibility references.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- The standard runtime package with execute/validate, MP26 conversion, ownership integration, diagnostics and current docs.
- Validated revision lineage, timestamps/history, tamper handling and post-merge fixed-point behavior without a separate metadata PR publisher.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- One shared ownership interpreter and one cumulative publication; versioning semantics do not repeatedly increment an unchanged proposal.

**Non-goals:**

- Migrate real consumers before readiness or remove operative legacy paths without their acceptance gate.

**Acceptance criteria:**

- Sync and Document Revisions operate under one ownership model and cumulative candidate; no service overwrites another exclusive region.
- An unchanged merged maintenance proposal yields a no-op rerun, stable revision/timestamps/history and correct tamper diagnostics.
- Necessary legacy compatibility remains until accepted consumer cutover; live conversion requires compatible authorized execution.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Run both services together on body changes, metadata-only/format-only changes, legacy conversion, tampering and unrelated YAML preservation.
- Exercise the post-merge unchanged scenario, final read-only validation, history/lineage integrity and old/new invocation reference closure.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Standard Document Revisions descriptor, execution/validation API and approved protected-format migration contract.

**Trust and security constraints:**

Apply D01/D09: approved immutable sources, exact destination/write authority, safe paths/arguments and no unapproved execution or credential exposure.

**Migration and compatibility:**

Preserve necessary legacy invocation/configuration compatibility and unrelated front matter until governed cutover.

**Required fixtures:**

Combined Sync/Document Revisions candidates, legacy/mixed YAML, tamper cases and post-merge unchanged histories.

**Rollback:**

Preserve document/history integrity and the approved compatible invocation rollback path.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- The service publishes its own repair PR, changes another owner's exclusive content or converts live data before compatible authorized execution.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP28` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp28"></a>

### MP28 — Migrate Agent Instructions to the asset-package contract

**Identifier:**

`MP28`

**Title:**

Migrate Agent Instructions to the asset-package contract

**Mode:**

migration

**Objective:**

Convert the existing Agent Instructions source, contribution and payload to the standard Class 1 contract and generic installation path.

**Rationale:**

Accepted runtime/installation foundations permit migration of the protected publisher package without losing its ownership partition.

**Dependencies:**

- `MP04` — accepted and fully finalized under the installed protocols.
- `MP06` — accepted and fully finalized under the installed protocols.
- `MP18` — accepted and fully finalized under the installed protocols.
- `MP22` — accepted and fully finalized under the installed protocols.
- `MP23` — accepted and fully finalized under the installed protocols.
- `MP24` — accepted and fully finalized under the installed protocols.
- `MP25` — accepted and fully finalized under the installed protocols.
- `MP27` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows authoritative agent-package source and only exact separately authorized derived installations/fixtures.
- Allowed surfaces: Approved descriptor/contribution/payload and necessary source/install references, tests and docs; protected paths require exact handoff authorization.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- The standard asset package with complete payload closure, approved lifecycle declarations and generic-installation evidence.
- Preserved instruction partition, source/install ownership, local companions, bridges, review state and seeded customizations.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Keep the instruction partition and publisher/custom/native boundaries; no backlog hooks or rule-quality redesign is added incidentally.

**Non-goals:**

- Change global agent configuration, install skills, rewrite unrelated rules or copy live review findings into a seed.

**Acceptance criteria:**

- Complete instruction payload and generic installation work without a specialized installer.
- Enforced publisher files, optional groups and true-seed state follow approved policies without overwriting repository-owned content.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Exercise fresh install and existing installation migration, complete projection, optional groups, source/install consistency and preserved local/seed bytes.
- Inspect exact protected-path authority, reference closure and absence of incidental rule/skill/global-config changes.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Standard asset descriptor/contribution and supported instruction-package installation/migration contract.

**Trust and security constraints:**

Apply D01/D09: approved immutable sources, exact destination/write authority, safe paths/arguments and no unapproved execution or credential exposure.

**Migration and compatibility:**

Preserve source/install ownership, optional bridges, existing local companions and operational/seeded content.

**Rollback:**

Recover the prior operative instruction routing without discarding repository-owned customizations or review state.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Protected source/installed paths lack exact authorization or the migration would overwrite local instructions/review/customized seed state.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP29` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp29"></a>

### MP29 — Migrate Backlog Workflow using its approved source-location decision

**Identifier:**

`MP29`

**Title:**

Migrate Backlog Workflow using its approved source-location decision

**Mode:**

migration

**Objective:**

Convert Backlog Workflow to the standard asset contract at its MP02-approved canonical location.

**Rationale:**

Source relocation/compatibility is decided before migration; accepted generic installation can then replace specialized adoption safely.

**Dependencies:**

- `MP02` — accepted and fully finalized under the installed protocols.
- `MP04` — accepted and fully finalized under the installed protocols.
- `MP06` — accepted and fully finalized under the installed protocols.
- `MP18` — accepted and fully finalized under the installed protocols.
- `MP22` — accepted and fully finalized under the installed protocols.
- `MP23` — accepted and fully finalized under the installed protocols.
- `MP24` — accepted and fully finalized under the installed protocols.
- `MP25` — accepted and fully finalized under the installed protocols.
- `MP28` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: The MP02-approved Backlog Workflow source repository/path, required approved catalog references and disposable/adopter fixtures explicitly authorized later.
- Allowed surfaces: Package descriptor/contribution/payload, source/release reference migration, compatibility, tests and docs; existing live project state remains protected.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- The standard asset package and updated source/provenance/release references at the approved central or justified external authority.
- New-install and existing-adopter migration evidence preserving the five-file governance projection and separate skill boundary.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Provisioning, skill installation and pass activation remain separate; installed project state is project-owned.

**Non-goals:**

- Repeat this project's governance installation, initialize/complete passes or retire specialized adoption before acceptance.

**Acceptance criteria:**

- Exactly three managed protocol files and two mutable project files retain their intended authority; existing backlog/ledger bytes are not reseeded.
- The source-location decision is executed with compatibility/rollback evidence and generic installation succeeds.
- Specialized adoption retirement remains gated; no global skill installation/activation is implied.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Check the approved source map, immutable/release references, new installation and existing populated/consumed-seed migration.
- Verify three-managed/two-mutable ownership, historical ledger preservation, skill exclusion/boundary and all relevant literal references.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Standard Backlog Workflow asset descriptor, contribution, approved source paths/references and migration guidance.

**Trust and security constraints:**

Apply D01/D09: approved immutable sources, exact destination/write authority, safe paths/arguments and no unapproved execution or credential exposure.

**Migration and compatibility:**

Preserve five-file projection, mutable state, skill boundary and approved release/source compatibility during relocation.

**Rollback:**

Restore compatible source/caller references while preserving populated backlog/ledger and durable seed history.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Relocation authority is unresolved, live project state would be reseeded or unapproved skill behavior/source authority changes are needed.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP30` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp30"></a>

### MP30 — Migrate Code Style using its approved source-location decision

**Identifier:**

`MP30`

**Title:**

Migrate Code Style using its approved source-location decision

**Mode:**

migration

**Objective:**

Convert Code Style's GitHub distribution to the standard Class 1 contract at the MP02-approved source location.

**Rationale:**

The inventoried payload and approved relocation decision permit generic distribution without accidentally changing existing NuGet behavior.

**Dependencies:**

- `MP02` — accepted and fully finalized under the installed protocols.
- `MP04` — accepted and fully finalized under the installed protocols.
- `MP06` — accepted and fully finalized under the installed protocols.
- `MP18` — accepted and fully finalized under the installed protocols.
- `MP22` — accepted and fully finalized under the installed protocols.
- `MP23` — accepted and fully finalized under the installed protocols.
- `MP24` — accepted and fully finalized under the installed protocols.
- `MP25` — accepted and fully finalized under the installed protocols.
- `MP29` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: The approved Code Style source repository/path, required catalog/reference surfaces and explicitly authorized disposable distribution/build fixtures.
- Allowed surfaces: GitHub asset descriptor/contribution/payload, file lifecycle declarations, source mapping, necessary references, tests and documentation.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- The standard GitHub-distribution asset package with explicit lifecycle for the approved .editorconfig and Directory.Build.props payload.
- Approved canonical source mapping and migration/compatibility evidence preserving existing NuGet integration.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Keep one approved canonical distribution authority and preserve unrelated package/build behavior.

**Non-goals:**

- Redesign style rules, silently replace NuGet packaging or invent an unverified payload.

**Acceptance criteria:**

- The actual approved payload is verified rather than inferred from old examples and distribution tests pass.
- Relocation creates no independently edited canonical copies and does not accidentally change NuGet behavior.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Check MP01 payload/build/package evidence against MP02 source mapping; exercise fresh and existing generic distribution.
- Verify per-file lifecycle, NuGet references/integration, source closure and relevant public compatibility cases.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Standard Code Style GitHub asset package, lifecycle declarations and approved source/migration references.

**Trust and security constraints:**

Apply D01/D09: approved immutable sources, exact destination/write authority, safe paths/arguments and no unapproved execution or credential exposure.

**Migration and compatibility:**

Preserve existing NuGet behavior; source relocation and any necessary reference updates follow MP02's accepted disposition.

**Rollback:**

Restore compatible distribution/build references without losing consumer-owned settings or creating dual canonical authorities.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Payload identity, relocation authority, build/package references or NuGet compatibility cannot be established.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP31` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp31"></a>

### MP31 — Migrate the Visual Studio template consumer

**Identifier:**

`MP31`

**Title:**

Migrate the Visual Studio template consumer

**Mode:**

migration

**Objective:**

Install the accepted replacement package set and caller configuration in BionicCode/template-visual-studio-repository.

**Rationale:**

The first real consumer migration follows accepted package/installation capability and provides the model for other adopters.

**Dependencies:**

- `MP25` — accepted and fully finalized under the installed protocols.
- `MP27` — accepted and fully finalized under the installed protocols.
- `MP28` — accepted and fully finalized under the installed protocols.
- `MP29` — accepted and fully finalized under the installed protocols.
- `MP30` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/template-visual-studio-repository only at its exact separately authorized revision; shared platform sources are read-only during caller migration.
- Allowed surfaces: Required generic installation/caller configuration, proven legacy duplication cleanup, migration checks and consumer documentation.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- An accepted required-package installation and compatible caller wiring preserving unrelated source/template and project-owned state.
- A verified old/new reference map, consumer behavior and rollback evidence.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Shared implementation defects are corrected in their source authority; no local engine fork is introduced.

**Non-goals:**

- Patch the shared platform inside the consumer, redesign the template or clean unrelated source files.

**Acceptance criteria:**

- Legacy duplicated callers/scripts/configs are removed only after required replacement installation is available.
- Consumer operation, source access and package projections are valid; unrelated content and mutable/local state are preserved.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Verify generic installer output, required dependencies, complete projection, operative caller, convergence and exact consumer revision.
- Inspect removal/reference closure, retained user/template content and the accepted rollback scenario.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

The first consumer's supported replacement package/caller configuration and migration boundary.

**Trust and security constraints:**

Apply D01/D09: approved immutable sources, exact destination/write authority, safe paths/arguments and no unapproved execution or credential exposure.

**Migration and compatibility:**

Preserve repository-owned template/source/state and keep operative compatibility until replacement is accepted.

**Rollback:**

Validate a consumer-specific rollback restoring compatible callers/configuration without overwriting project state.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Required replacements are unavailable, shared defects require source correction or consumer state/authority differs from the handoff.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP32` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp32"></a>

### MP32 — Migrate remaining adopters

**Identifier:**

`MP32`

**Title:**

Migrate remaining adopters

**Mode:**

migration

**Objective:**

Perform governed migrations for MP01's remaining adopter inventory, including BionicCode/nextcloud-url-uploader.

**Rationale:**

The accepted first consumer provides a proven migration pattern while each remaining repository retains independent authority/evidence.

**Dependencies:**

- `MP31` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: Each exact separately authorized adopter repository/revision from the inventory; shared implementation remains read-only.
- Allowed surfaces: Adopter-specific package/caller changes, accepted legacy cleanup, validation, rollback and migration documentation.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- An evidence-backed migration record and coherent replacement package/caller state for each authorized adopter.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- No silent cross-repository scope expansion, broken dependencies or local shared-engine forks.

**Non-goals:**

- Coordinate atomic deployment across adopters or treat one repository's acceptance as evidence for every other repository.

**Acceptance criteria:**

- Source access, dependency closure, projection and runtime behavior are valid for each adopter.
- Project-owned state and unrelated content remain preserved; repository authorization/evidence are kept distinct.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Repeat the applicable first-consumer checks at each exact revision, including private reads, convergence and rollback.
- Compare actual changed paths against each authorized adopter scope and inspect preserved project/seed content.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Adopter-specific accepted package/caller migration contracts.

**Trust and security constraints:**

Apply D01/D09: approved immutable sources, exact destination/write authority, safe paths/arguments and no unapproved execution or credential exposure.

**Migration and compatibility:**

Retain required source/caller compatibility until each adopter's replacement is verified.

**Rollback:**

Define and validate per-adopter recovery without discarding project data or durable provisioning history.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- An adopter needs an unapproved shared-engine workaround, additional authority or an unsupported migration assumption.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP33` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp33"></a>

### MP33 — Certify the complete platform

**Identifier:**

`MP33`

**Title:**

Certify the complete platform

**Mode:**

validation-only

**Objective:**

Establish reproducible hosted acceptance evidence for the migrated package set and real consumer boundaries.

**Rationale:**

Final documentation and retirement depend on whole-platform security, recovery, lifecycle and convergence evidence beyond component tests.

**Dependencies:**

- `MP25` — accepted and fully finalized under the installed protocols.
- `MP27` — accepted and fully finalized under the installed protocols.
- `MP28` — accepted and fully finalized under the installed protocols.
- `MP29` — accepted and fully finalized under the installed protocols.
- `MP30` — accepted and fully finalized under the installed protocols.
- `MP31` — accepted and fully finalized under the installed protocols.
- `MP32` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: Accepted platform/package revisions and exact approved hosted source/consumer/test repositories; implementation stays fixed during certification.
- Allowed surfaces: Full hosted acceptance matrix, evidence correlation, limitation analysis and written certification.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- Observed evidence for multi-service composition, ownership, races, cancellation/failure recovery, proposal lifecycle, upgrades and all lifecycle modes.
- Cross-repository source access, security and post-merge convergence evidence tied to exact tested revisions.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Aggregate success labels, static phrase tests and prepared fixtures alone do not establish full deployed behavior.

**Non-goals:**

- Patch implementation during validation or declare unsupported cases certified.

**Acceptance criteria:**

- Required scenarios have reproducible accepted results at matching versions; missing/inconclusive evidence is explicit.
- Real external boundaries are exercised where local fixtures cannot prove access or integration.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Execute the accepted complete matrix and inspect actual candidate/PR, remote state, receipt, history and recovery outcomes.
- Check positive/negative controls, post-merge no-op, privilege isolation and preserved target-owned content across migrated packages/consumers.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Required fixtures:**

Exact approved hosted multi-service, lifecycle, source-access, failure/race and consumer fixtures.

**Documentation impact:**

Produce the accepted written governance/review/validation evidence appropriate to this pass without silently changing implementation.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Evidence is missing, inconclusive, revision-mismatched or exposes a defect requiring an authorized source correction.

**Review gate:**

Independent full-platform/security review verifies executable and hosted evidence plus residual limitations; maintainer acceptance is required.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP34` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp34"></a>

### MP34 — Complete operator and author documentation

**Identifier:**

`MP34`

**Title:**

Complete operator and author documentation

**Mode:**

implementation

**Objective:**

Complete integrated operator, package-author, service-author and migration guidance matching the accepted platform.

**Rationale:**

Release and retirement need usable end-to-end guidance while earlier implementation passes have already documented their own contracts.

**Dependencies:**

- `MP33` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows and only explicitly authorized package/consumer documentation surfaces.
- Allowed surfaces: Integrated guides, examples, schema/API references, permissions, diagnostics, troubleshooting and migration instructions.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- Reviewed operator/package-author/service-author/migration documentation aligned with actual accepted interfaces and behavior.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- Documentation is a product contract and must not claim unobserved certification or obsolete behavior.

**Non-goals:**

- Defer missing earlier docs to this pass as a substitute for complete earlier results or silently change implementation.

**Acceptance criteria:**

- Examples and workflow recipes are usable, current and consistent with schemas, permissions, lifecycle and diagnostics.
- Earlier module documentation obligations remain satisfied; unsupported/deferred behavior is labeled accurately.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Exercise documented examples/workflows against supported interfaces in authorized fixtures.
- Check local links/anchors, public names, defaults, source provenance, migration/rollback instructions and troubleshooting against runtime evidence.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Integrated operator/author examples and references documenting accepted public interfaces.

**Trust and security constraints:**

Apply D01/D09: approved immutable sources, exact destination/write authority, safe paths/arguments and no unapproved execution or credential exposure.

**Migration and compatibility:**

Describe exact supported migrations, retained legacy names/removal gates and limitations.

**Rollback:**

Preserve a coherent accepted baseline/operative caller and target-owned state. Validate failure preservation and the applicable approved recovery path before enabling replacement behavior.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Documentation requires unsupported behavior, hidden implementation changes or unauthorized protected-file edits.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP35` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp35"></a>

### MP35 — Cut over and retire accepted legacy components

**Identifier:**

`MP35`

**Title:**

Cut over and retire accepted legacy components

**Mode:**

migration

**Objective:**

Perform the approved replacement cutover and exact legacy retirement set after certification and rollback review.

**Rationale:**

Only accepted replacement coverage and migrated consumers permit removal of obsolete orchestrators, duplicate engines and installers.

**Dependencies:**

- `MP31` — accepted and fully finalized under the installed protocols.
- `MP32` — accepted and fully finalized under the installed protocols.
- `MP33` — accepted and fully finalized under the installed protocols.
- `MP34` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows and only exact separately authorized source/consumer retirement surfaces; historical evidence is preserved.
- Allowed surfaces: Approved cutover/removal map, obsolete implementation/reference cleanup, rollback checks and updated docs.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- The accepted cutover and removal of proven obsolete orchestrator, duplicate engine, specialized installer and deprecated artifacts.
- Verified replacement coverage, reference closure, preserved historical evidence and accepted rollback/removal evidence.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- No component is deleted merely because its replacement is planned; no incidental archive destruction.

**Non-goals:**

- Broad cleanup of unrelated artifacts, rewrite accepted history or retire compatibility before its accepted gate.

**Acceptance criteria:**

- No active consumer depends on the retired surface; required replacements and migrations are certified.
- Historical evidence remains preserved and all relevant invocation/configuration/documentation references remain coherent.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Reconcile the exact retirement set with the inventory and current consumer/reference evidence before deletion.
- Verify post-cutover operation/convergence, rollback assumptions, preserved history and absence of unexplained stale live references.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Accepted legacy deprecation/removal and replacement cutover contract.

**Trust and security constraints:**

Apply D01/D09: approved immutable sources, exact destination/write authority, safe paths/arguments and no unapproved execution or credential exposure.

**Migration and compatibility:**

Prove all active consumers have a supported replacement before removing compatibility.

**Rollback:**

Review and validate the exact rollback/removal path before destructive retirement actions.

**Documentation impact:**

Update affected module/API/schema/usage examples, diagnostics, security and compatibility/migration documentation in the same reviewed change; include suitable tests.

**Independent-merge rule:**

Merge only a coherent result that leaves operative callers valid and preserves accepted identities. Do not enable incomplete replacements or remove compatibility before its accepted gate.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Active consumers, unresolved replacement defects, missing rollback evidence or changed authority remain.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

After acceptance, required integration/reachability and full ledger finalization, `MP36` becomes eligible for preparation and separately authorized activation, subject to all of its dependencies. No activation is automatic.

<a id="mp36"></a>

### MP36 — Finalize historical evidence and release authority

**Identifier:**

`MP36`

**Title:**

Finalize historical evidence and release authority

**Mode:**

coordination

**Objective:**

Reconcile final historical disposition, accepted evidence and immutable release-readiness authority.

**Rationale:**

Project completion needs complete accepted provenance without circular self-reference or an invented release declaration.

**Dependencies:**

- `MP35` — accepted and fully finalized under the installed protocols.

**Scope:**

- Repositories: BionicCode/workflows explicitly authorized project control-plane/release-readiness records; historical records remain preserved.
- Allowed surfaces: Historical disposition records, ledger reconciliation and release-readiness coordination; no implementation changes.
- Prohibited surfaces: unrelated implementation or consumer state; other pass results; protected paths without exact authorization; historical archives except explicitly permitted read-only evidence or separately authorized disposition.

**Required outputs:**

- A historical disposition record, final evidence reconciliation and release-readiness authority referencing actual accepted identities.
- Release-readiness instructions for a separately authorized declaration after this pass's own closure and delayed finalization; the actual declaration is a later program-completion action, not a pre-closure pass output.

**Required invariants:**

- Apply D01–D11 and the installed workflow/review/ledger authority; preserve unrelated and target-owned content. This contract grants no write, Git/GitHub, activation or release authority.
- No commit is required to contain its own SHA; final release and completion claims use actual evidence only.

**Non-goals:**

- Modify implementation, destroy historical records, bypass closure timing or publish a release without explicit authorization.

**Acceptance criteria:**

- Predecessor finalization/reachability and immutable release inputs are verified; historical evidence remains attributable.
- This pass follows normal closure/finalization; no future closure SHA, PR, reviewer, test or release evidence is anticipated.
- The complete result and relevant evidence are independently reviewed and accepted by the maintainer; no stop condition remains unresolved.

**Validation:**

- Audit accepted identities, PR/run/reviewer evidence and target-history reachability under the installed ledger protocol.
- Verify historical disposition/source references and immutable release inputs; review the post-finalization release-declaration procedure without claiming that the declaration has already executed.
- Record actual commands/checks, revisions, environments, outcomes, skipped/unavailable cases and limits; future CLI/format names are not invented by initialization.

**Public contract:**

Final project evidence/disposition and release-readiness authority; no new runtime API.

**Documentation impact:**

Produce the accepted written governance/review/validation evidence appropriate to this pass without silently changing implementation.

**Stop conditions:**

- Stop affected work on conflicting authority, missing/unfinalized prerequisites, ambiguous ownership/state, unavailable approved sources, stale execution context or required changes outside the current authorization.
- Required evidence/reachability is incomplete, release inputs are not immutable or release declaration would precede its authority/finalization.

**Review gate:**

Independent result review checks the complete contract, exact authorized scope, provenance, validation and applicable tests/documentation/compatibility. Maintainer acceptance is required; the executor is not the sole acceptance authority.

**Follow-up effect:**

No successor is admitted. Complete this pass's own normal closure and delayed finalization before an explicitly authorized final release declaration and project-completion assessment under section 2.

## 8. Project-specific exceptions

No new project-specific exception is introduced by initialization. Historical exceptions remain in their historical records and do not silently redefine this project's workflow.

The governance workspace installation is a satisfied prerequisite, not a new-project pass result. This boundary is not an exception to the normal pass lifecycle. Future exceptions require explicit governance review and approval in their owning artifact without weakening the reusable protocols.

## 9. Backlog maintenance rules

- Preserve admitted identities and accepted history. Add bounded follow-up work for later defects; do not silently renumber or reuse a final ID.
- Review changes to order, dependencies, scope, acceptance criteria or architecture through explicit governance. Reconcile ledger identities without copying mutable state into this backlog.
- Re-review a prepared/active handoff when its owning contract changes materially.
- Keep current, approved future, historical, deferred and unresolved behavior distinguishable.
- Preserve the complete draft-to-final mapping and requirement coverage when refining the roadmap.
- Complete each contract's prerequisite decisions before its dependent implementation; do not invent missing schema, delimiter, credential, revision or release values.
- Keep three publisher-managed protocol files unchanged during project-owned initialization/maintenance unless separately authorized at their source authority.
- Repeated initialization preserves populated project content: identical accepted content is a no-op; different populated content requires reconciliation, never blind replacement.
- Preserve archives, local customizations and unrelated worktree state; do not activate archive infrastructure or global skills incidentally.
- Do not infer write authority, execution readiness or automatic activation from this backlog, a dependency, a registration or a review.
