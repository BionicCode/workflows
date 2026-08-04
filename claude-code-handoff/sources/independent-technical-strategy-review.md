# Independent Technical Strategy Review — Recovery Backlog

Review date: 2026-07-15  
Target: BionicCode/workflows, repository-maintenance-orchestrator-recovery-backlog.md  
Caller: BionicCode/template-visual-studio-repository  
Review mode: read-only technical and architectural review

## 1. Verdict

**Accept with non-blocking recommendations**

The strategy is coherent enough to activate W2 unchanged. W2 is a documentation-only current-state pass and none of the findings below makes that work unsafe or materially wasteful.

Several recommendations are nevertheless mandatory gates before the affected later passes. The roadmap should bind every ownership decision to an immutable source snapshot, define trusted policy provenance and plan transport before W7/W9–W12, and move W14 ahead of W6 to avoid implementing and packaging an intentionally obsolete manifest contract.

## 2. Resolved state and evidence

| Item | Resolved state |
|---|---|
| Workflows repository | Public; default branch main; final recheck HEAD aaf71d3840f52aa94b9976cb2e69e96d9e44b2d9, exactly the review lease. |
| Backlog | Blob 5b07641f5e5cd80ec8fddbfc751131ad3e2986a0 at the leased commit. W0 and W1 are Completed; W2 through T6 are Locked. |
| Caller repository | Public; default branch main; final recheck HEAD dd569d77b46e0198185958cda865118b8508b7d6. |
| Existing caller automation | PR 34 remains open and now has 11 changed files; PR 35 remains open with four changed files. This is newer live state than the backlog’s earlier PR 34 snapshot, but it does not invalidate the strategy because T6 explicitly owns stale automation cleanup. |
| Instructions | Root AGENTS.md, AGENT_GUARDRAILS.md, .github/copilot-instructions.md, backlog-workflow-documentation.md, evidence-ledger-documentation.md, and repository-review-protocol.md were inspected. The review stayed outside all locked implementation-pass scopes. |
| Technical surfaces | The maintenance and reusable workflows, caller wrappers, initializer, sync and metadata engines, schemas, manifests, tests, and relevant documentation were inspected at the resolved commits. |
| Execution evidence | No tests, builds, formatters, workflow dispatches, or GitHub Actions runs were started, as required for this review. Local gh, pwsh, dotnet, actionlint, and shellcheck were unavailable. Python, git, jq, pdfinfo, and pdftoppm were available. No repository checkout, private-source fixture, repository settings, branch-protection data, or cross-repository credential was available. |

Evidence anchors: [leased backlog](https://github.com/BionicCode/workflows/blob/aaf71d3840f52aa94b9976cb2e69e96d9e44b2d9/repository-maintenance-orchestrator-recovery-backlog.md), [Workflows lease commit](https://github.com/BionicCode/workflows/commit/aaf71d3840f52aa94b9976cb2e69e96d9e44b2d9), [caller baseline](https://github.com/BionicCode/template-visual-studio-repository/commit/dd569d77b46e0198185958cda865118b8508b7d6), [caller PR 34](https://github.com/BionicCode/template-visual-studio-repository/pull/34), and [caller PR 35](https://github.com/BionicCode/template-visual-studio-repository/pull/35).

The backlog’s diagnosed defects are supported by current code. In particular:

- The current metadata workflow executes the caller repository’s trusted copy of the engine rather than a Workflows-owned engine: [doc-metadata.yml](https://github.com/BionicCode/workflows/blob/aaf71d3840f52aa94b9976cb2e69e96d9e44b2d9/.github/workflows/doc-metadata.yml).
- The Workflows maintenance orchestrator schedules work, hardcodes main/master metadata calls, and references a local sync workflow that is absent in Workflows: [repository-maintenance.yml](https://github.com/BionicCode/workflows/blob/aaf71d3840f52aa94b9976cb2e69e96d9e44b2d9/.github/workflows/repository-maintenance.yml).
- The current acceptance harness reads stdout and stderr sequentially and waits without a timeout, creating the stated deadlock/hang risk: [Invoke-DocMetadataAcceptanceTests.ps1](https://github.com/BionicCode/workflows/blob/aaf71d3840f52aa94b9976cb2e69e96d9e44b2d9/.github/scripts/doc-metadata/tests/Invoke-DocMetadataAcceptanceTests.ps1).
- The active engine and metadata manifest still implement documentEligibility and broad text matching, supporting the W14 diagnosis: [update-doc-metadata.ps1](https://github.com/BionicCode/workflows/blob/aaf71d3840f52aa94b9976cb2e69e96d9e44b2d9/.github/scripts/doc-metadata/update-doc-metadata.ps1) and [doc-metadata-manifest.json](https://github.com/BionicCode/workflows/blob/aaf71d3840f52aa94b9976cb2e69e96d9e44b2d9/.github/tools/doc-metadata/doc-metadata-manifest.json).

## 3. Architecture assessment

### Feasibility and authority

The central architecture is sound:

- Workflows becomes implementation authority for the metadata engine and shared ownership classifier.
- Callers retain orchestration, permissions, manifests, package identity, and a thin literal-SHA wrapper.
- Engine, trusted-caller, and working-caller checkouts are separated.
- Duplicate caller engines and tests remain until parity and live convergence are proven.
- Version authority is expressed as explicit enforce, seed-once, disabled, and self-canonical behavior rather than inferred from file presence.

GitHub officially exposes job.workflow_repository and job.workflow_sha and documents checking out the repository that supplied a reusable workflow. This makes the proposed self-checkout technically viable on GitHub.com. A reusable workflow reference in jobs.<job_id>.uses cannot use contexts or expressions, so generating a caller wrapper with a literal full SHA is also the right boundary. GitHub states that a full commit SHA is the only immutable action reference. [Contexts reference](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts), [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use).

Nested reusable workflows cannot elevate GITHUB_TOKEN permissions, which supports the proposed caller-owned permission boundary. Accessibility still depends on repository Actions settings and every workflow in the call chain being accessible, so W17 cannot certify live caller integration by static Workflows tests alone. [Reusable workflow permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations), [repository Actions settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository).

### Trust boundaries

The separate trusted and working caller checkouts are appropriate, but the roadmap does not yet say which checkout supplies policy. The current engine reads its metadata manifest from the working tree. If the reusable implementation preserves that behavior without an explicit decision, a pull request can alter the policy used to assess itself, including authority classifications and eligibility. W6 must choose and document one model:

1. enforce trusted-base policy while independently validating proposed working policy; or
2. intentionally accept working policy, with explicit threat analysis and diagnostics.

The first model is safer and is the recommendation.

Fork pull requests should continue to be validation-only. GitHub gives fork-origin pull_request workflows a read-only token and withholds secrets by default; repair must remain an explicit same-repository path with least privilege. [Fork pull-request security](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target).

### Version authority and convergence

The proposed authority table correctly prevents ordinary ping-pong:

- external enforce: sync owns content and metadata skips the entire file;
- exact self-canonical: metadata may update; sync is a no-op;
- seed-once existing: caller owns subsequent content;
- disabled: neither engine enforces.

The unresolved issue is snapshot identity. Current sync manifests commonly reference mutable main branches, and the current sync engine can enumerate and fetch source data through separate requests by that mutable ref. The roadmap says classifier, plan, and sync must use the same Workflows implementation SHA, but that does not guarantee that they observe the same source repository commit. A source move between planning, metadata, and synchronization can change the target set or authority and defeat convergence.

Each source repository/ref must therefore be resolved once to an immutable commit SHA. The ownership plan must carry those SHAs, the caller base/head identities, the trusted policy digest, and its own schema/version/digest. Both consumers must use that same attested plan or fail closed.

### Packaging and migration

The package boundary is sensible: thin wrapper, manifest, schema, documentation, package metadata, and sync entries; no copied engine or test suite. Init/upgrade/validate-installation is a coherent command model, and delaying caller-engine deletion until after T4 is a strong rollback design.

Before implementation, W6/W8 still need explicit contracts for:

- first-install bootstrap at the exact W17 SHA;
- downgrade behavior;
- staging, validation, and atomic promotion of the complete package;
- concurrent runs, stale automation branches, and force-with-lease behavior;
- partial-failure recovery and structural merge conflicts;
- action/dependency provenance in write-capable jobs.

The current write-capable workflows use mutable major-version action tags, including a third-party pull-request action. Action pinning is currently deferred to F3, but immutable references for the release-candidate write path are a correctness and supply-chain requirement, not merely a performance hardening item.

### Sequencing

The pass graph is generally well decomposed and preserves reviewable rollback points. One ordering correction will reduce rework: move W14 immediately after W5. Otherwise W7, W8, and W13 implement, package, and integrate-test the documentEligibility contract only for W14 to remove it afterward.

W13 remains useful after the move; it is the first full local cross-engine convergence gate. W17 remains distinct as release-candidate certification. T2 and T4 remain distinct because parity and live GitHub integration answer different questions.

The architecture should be documented as GitHub.com-only unless a GHES alternative is designed, because job.workflow_repository and job.workflow_sha are not available on GitHub Enterprise Server.

## 4. Goal-to-pass matrix

| Goal | Owning passes | Validation/exit evidence | Assessment |
|---|---|---|---|
| One authoritative metadata engine | W6–W8; T3–T5 | W7 tests, W17 certification, T2 parity, T4 convergence, T5 reference scan | Covered; duplication is intentionally retained until rollback is safe. |
| Trustworthy caller integration | W6–W8; T1–T4 | exact-SHA checks, fork/same-repo tests, live caller runs | Covered, subject to trusted-policy and live-settings clarifications. |
| Coherent init/upgrade | W6, W8, T1 | fresh install, upgrade, idempotence, conflict and rollback tests | Covered in concept; bootstrap, downgrade, concurrency, and atomicity must be explicit. |
| Correct ownership interaction | W9–W13; T3–T4 | classifier matrices, attested plan tests, cross-engine fixtures | Covered after adding immutable source and target identities. |
| Stable version authority/no ping-pong | W9–W13; T3–T4 | two complete no-op passes and negative authority tests | Authority table is sound; mutable source snapshots are the current gap. |
| Manifest governance | W14, then W6–W8/W13 | schema, engine, package, docs, and fixture tests | Covered, but W14 should precede W6. |
| Safe package governance | W6, W8, W17, T1 | identity, merge, tamper, transaction, install/upgrade evidence | Covered after adding supply-chain and transaction criteria. |
| Remove duplicated caller engine/tests | T3–T5 | parity, live convergence, deletion/reference scan | Correctly delayed and independently reviewable. |
| Reviewable migration and rollback | W17, T0–T6 | exact SHAs, branch/PR ledger, live gates, stale-state cleanup | Strong overall; bootstrap and shared-defect restart protocol need precision. |
| Naming/compatibility migration | W2A–W2B, W6–W8, T3–T5 | compatibility inventory and reference tests | Correctly isolated from behavior changes. |

## 5. Pass-by-pass recommendations

| Pass | Scope/position assessment | Recommendation |
|---|---|---|
| W2 | Correctly scoped and positioned; documentation-only. | Activate unchanged. Describe unresolved runtime contracts as unresolved rather than choosing them. |
| W2A | Correctly isolates naming design. | Include every currently callable public path, caller @main reference, compatibility lifetime, and bootstrap alias in the migration inventory. |
| W2B | Correct behavior-preserving migration. | Retain; require compatibility/reference tests and prohibit semantic changes. |
| W3 | Correctly restores Workflows passivity. | Retain; change the sentence saying W6 replaces the local metadata call to W7, because W6 is planning-only. |
| W4 | Correctly isolated reliability fix. | Retain; add failing deadlock and timeout witnesses before the fix and preserve complete stdout/stderr diagnostics. |
| W5 | Necessary executable baseline. | Retain; record discovered suites, dependency versions, skips, and unavailable tools rather than equating zero discovered tests with success. |
| W6 | Broad but appropriately architectural. | Make W14 a prerequisite; add the immutable snapshot, trusted-policy, plan-transport, bootstrap, transaction, downgrade, concurrency, permissions, and action-provenance decisions. |
| W7 | Correct implementation authority boundary. | Retain after the expanded W6 contract; test exact self-checkout identity, untrusted policy changes, forks, reduced permissions, and concurrency-group behavior. |
| W8 | Coherent independently mergeable package pass. | Retain; stage and validate the whole package before promotion, fail closed on partial updates, and implement explicit downgrade/concurrency/bootstrap rules. |
| W9 | Correct single-classifier foundation. | Add target repository/ref/SHA and resolved source commit SHA per source; normalize branches, tags, and SHAs; add source-movement tests. |
| W10 | Correct sync consumer migration. | Consume the resolved snapshot and plan identity, not merely the same classifier code; fail on missing/stale identity. |
| W11 | Correct read-only planning boundary. | Define a versioned plan schema, digest, size limit, and transport. Publish a single attested plan for both consumers. |
| W12 | Correct metadata consumer migration. | Enforce trusted plan provenance; reject forged, stale, wrong-base/head, wrong-source, and digest-mismatched plans without writes. |
| W13 | Necessary cross-engine integration checkpoint. | Retain after W12 and after the moved W14; run twice and add an adversarial source-ref-moves-between-phases fixture. |
| W14 | Correct scope, currently too late. | Move intact to immediately after W5 so all later design, packaging, and convergence work uses the final manifest contract. |
| W15 | Correct canonicalization pass. | Retain; add failing witnesses for noncanonical links and prove no unrelated content churn. |
| W16 | Correctly isolated tamper semantics. | Retain; prove externally owned files are skipped rather than repaired and diagnostics identify the governing source. |
| W17 | Correct release-candidate gate. | Retain; add immutable action references for the release path, attested-plan tests, fresh bootstrap, upgrade/downgrade, partial-failure, and supported-platform evidence. |
| T0 | Correct caller quarantine. | Retain; ensure open automation PRs are recorded but not closed or merged. |
| T1 | Correct first non-destructive caller step. | Define how an exact W17 installer is invoked before the pinned wrapper exists; record branch, PR, package identity, rollback, and observed job.workflow_sha. |
| T2 | Correct parity checkpoint. | Define an approved intentional-delta allowlist; any other difference reopens Workflows work. Do not repair the caller here. |
| T3 | Correct orchestration switch. | Require metadata and sync to consume the same plan digest and source snapshots; keep exact reusable-workflow pins and an atomic rollback commit. |
| T4 | Necessary live integration gate. | Exercise repository settings, permissions, fork/same-repo paths, concurrency, source-ref movement, repair PR behavior, and two complete convergence cycles. |
| T5 | Correctly delayed duplicate deletion. | Retain; record a reversible commit and verify no workflow, documentation, manifest, or test reference points to the deleted engine. |
| T6 | Correct final coordination/cleanup pass. | Retain; close or supersede PRs 34/35 only after T4/T5 evidence, preserve their evidence, and require explicit write authorization for each coordination action. |

## 6. Missing and unnecessary work

No new full pass is required. The missing work fits as bounded contract or exit-criterion additions:

1. Immutable source snapshot and target identity in W6/W9–W13/T3–T4.
2. Trusted policy provenance in W6/W7/W12.
3. Versioned ownership-plan transport and attestation in W6/W11/W12.
4. Exact-W17 bootstrap in W6/W8/T1.
5. Transactional install/upgrade, downgrade, concurrency, and partial-failure semantics in W6/W8/W17/T1.
6. Immutable action references for release/write-capable paths in W6/W17.
7. GitHub.com support boundary and live repository-settings evidence in W6/W17/T4.
8. Expected parity deltas, explicit rollback commits, and a new bounded Workflows follow-up pass when caller migration discovers a shared defect.

The only materially unnecessary work in the present order is implementing and testing the old documentEligibility contract through W7/W8/W13 before deleting it in W14. Moving W14 after W5 removes that waste. W13, W17, T2, and T4 are not duplicates: respectively they establish local convergence, release certification, caller parity, and live platform behavior.

## 7. Blocking findings

None.

No finding makes it unsafe or materially wasteful to begin W2. The unresolved items become blocking only at their stated later gates:

- W6 must not close without the trust, snapshot, transport, bootstrap, and package-lifecycle decisions.
- W7/W9 implementation must not start against an ambiguous policy or mutable-source contract.
- W17 must not certify a write-capable release candidate without immutable dependency references and executable install/upgrade evidence.
- T1/T3 must not switch the caller until exact-SHA bootstrap and shared-plan identity are proven.

## 8. Small exact roadmap changes

Apply these bounded edits; do not rewrite the roadmap:

1. Move W14, unchanged in scope, to immediately after W5 and make it a prerequisite of W6.
2. Under W6, add: “Define trusted-policy provenance. Enforcement uses the trusted base policy; proposed working-tree policy is validated separately and cannot weaken the current run.”
3. Under W6/W9, add: “Resolve every source repository/ref once to a full commit SHA and record target repository/ref/SHA, caller base/head SHA, trusted-policy digest, package identity, generator workflow SHA, plan schema version, and plan digest.”
4. Under W10–W12, replace “same classifier and commit” with: “consume the same attested ownership plan and immutable source snapshots, or fail closed; independent recomputation is permitted only when the resulting canonical plan digest is identical.”
5. Under W11, add an explicit plan transport, size limit, canonical serialization, retention, and rejection behavior. GitHub job outputs are limited, so the design must not assume an unbounded cross-job value. [Workflow output limits](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).
6. Under W6/W8/T1, add: “Define first-install bootstrap that verifies the running reusable workflow’s job.workflow_sha equals the approved W17 SHA before rendering the literal-SHA caller wrapper.” Account for workflow_dispatch requiring the workflow file on the default branch. [Manual workflow runs](https://docs.github.com/actions/managing-workflow-runs/manually-running-a-workflow).
7. Under W8/W17, add package-wide staging/validation/atomic promotion, explicit downgrade policy, concurrent-run/stale-branch behavior, and partial-failure tests.
8. Promote immutable action references for W7/W8/W17/T1–T4 write-capable paths from deferred F3 into the W17 release criteria.
9. Under T2, add an approved intentional-delta allowlist; unexpected differences stop caller work.
10. Under T3/T4, require the metadata and sync jobs to prove the same plan digest and source SHAs, plus a negative source-movement/concurrency test. GitHub concurrency does not guarantee ordering, so correctness must not depend on queue order. [Concurrency behavior](https://docs.github.com/actions/writing-workflows/choosing-what-your-workflow-does/control-the-concurrency-of-workflows-and-jobs).
11. Replace the instruction to “reopen” a completed Workflows pass on a caller-discovered shared defect with: “stop caller work, admit and activate a new bounded Workflows follow-up pass, produce a new release candidate, then discard or rebase the caller migration branch and repeat T1/T2.” This preserves the ledger rule that completed passes do not return to Pending.
12. In W3, change the W6 replacement reference to W7.

## 9. Final recommendation

**Activate W2 unchanged.**

After W2, apply the bounded roadmap edits above before W6 is activated. Keep all other passes locked and preserve the one-pass-at-a-time lease model. This gives the team a safe W2 start without allowing later implementation to inherit ambiguous trust or snapshot contracts.

No Git or GitHub write was performed. No branch, commit, pull request, issue, review, workflow run, repository setting, or attached file was changed.
