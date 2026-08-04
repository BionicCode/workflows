# Recovered W1 evidence reconciliation

## 1. Status and authority

This is passive context added on 2026-08-04. It corrects a premise in the earlier August 3 migration pack without rewriting that pack as though it had always known about the recovered export.

This file is not a task prompt, execution lease, backlog correction, maintainer decision, or write authorization. The ready-to-use review template lives separately in [`../user-prompts/01-authenticate-w1-report-and-plan-allowlist-repair.md`](../user-prompts/01-authenticate-w1-report-and-plan-allowlist-repair.md) and remains inert until a user explicitly issues it.

The Engineering Evidence Archive activation procedure in [`09-engineering-evidence-archive-activation.md`](09-engineering-evidence-archive-activation.md) remains in force and is not superseded by the recovered web export.

## 2. What changed on August 4

The August 3 handoff correctly established two important current blockers:

- the W2 table in the protected backlog contains nine names that do not exist and have no local Git history; and
- the existing W2 branch does not prove creation from the activation commit required by the later normalized lease workflow.

It incorrectly concluded that the complete W1 final response and historical proposed allowlist were unavailable. On August 4 the user supplied an export containing [`../sources/W1-final-audit-report.txt`](../sources/W1-final-audit-report.txt). Its bytes, evidence classification, and limitations are recorded in [`../sources/README.md`](../sources/README.md).

The export resolves the **availability** gap. It does not cryptographically prove the user's assertion that the file is the exact original ChatGPT response, and it does not decide the correct **current** W2 scope. Authentication and current-state reconciliation remain required.

## 3. The two different 16-path sets

### Historical proposed W1 allowlist from the recovered report

All 16 of these paths existed at W1 baseline `3a3fe364028db003bfc89d3a94fd8a9f167d1f35` and still exist at the 2026-08-04 reconciliation baseline:

```text
.github/copilot-instructions.md
.github/instructions/dotnet.instructions.md
.github/instructions/test.instructions.md
.github/scripts/sync-files-from-manifest/documentation/sync-manifest.md
.github/tools/doc-metadata/documentation/doc-metadata-manifest-api.md
.github/tools/doc-metadata/documentation/doc-metadata-manifest.md
.github/tools/doc-metadata/documentation/types/document-eligibility.md
.github/tools/doc-metadata/documentation/types/manifest-document.md
.github/tools/doc-metadata/documentation/types/report-analysis.md
.github/tools/doc-metadata/documentation/update-doc-metadata.md
AGENTS.md
AGENT_GUARDRAILS.md
DOCUMENTATION.md
README.md
src/AGENTS.md
test/AGENTS.md
```

This is a historical **proposed** W2 allowlist inside the recovered W1 response. It becomes trustworthy evidence of what W1 proposed only after the response is authenticated. Even then, it does not automatically become the current execution-authoritative list.

### Current backlog W2 table

The protected backlog currently states this different 16-path set:

```text
README.md
AGENTS.md
AGENT_GUARDRAILS.md
DOCUMENTATION.md
.github/copilot-instructions.md
.github/instructions/code-review.instructions.md
.github/instructions/tests.instructions.md
src/AGENTS.md
test/AGENTS.md
.github/scripts/doc-metadata/README.md
.github/scripts/doc-metadata/tests/README.md
.github/scripts/sync-files-from-manifest/README.md
.github/tools/doc-metadata/README.md
.github/tools/doc-metadata/api-reference.md
.github/tools/doc-metadata/type-reference.md
.github/tools/sync-config/README.md
```

Exactly seven paths overlap:

```text
README.md
AGENTS.md
AGENT_GUARDRAILS.md
DOCUMENTATION.md
.github/copilot-instructions.md
src/AGENTS.md
test/AGENTS.md
```

The other nine current-backlog names are **fabricated historical claims**: they were already nonexistent when inserted, are absent at the W1 baseline and current reconciliation baseline, and have no history in the local Git object database. Their similarity to real files does not make them rename candidates or authorize creating them.

The nine historical-report-only paths are real. They are not a guessed one-for-one rename map. A governed review must determine whether the authenticated historical set remains appropriate after post-W1 changes or whether current W2 needs a deliberately revised scope.

## 4. Evidence classification

### Verified from repository and local Git

- Baseline `3a3fe364028db003bfc89d3a94fd8a9f167d1f35` and bookkeeping commit `af639f43688bfd136b1dbdf051cc07bb7c588068` exist.
- The bookkeeping commit's sole parent is the baseline. Its only diff is `repository-maintenance-orchestrator-recovery-backlog.md`, with two insertions and two deletions.
- The baseline contains 57 tracked files and exactly 30 tracked Markdown files.
- The recovered report contains exactly 30 unique audit-table paths, equal as a set to the baseline Markdown inventory.
- Both 16-path sets contain 16 unique paths and overlap in exactly seven paths.
- Every historical-report allowlist path existed at the baseline and at the reconciliation baseline.
- Every current-only fabricated name is absent from those trees and has no local Git history.
- The current backlog records W0 and W1 `Completed`, W2 `Pending`, and later passes `Locked`; it also contains the corrupted table.
- The authoritative backlog records the W0/W1 presentation exception and the separate W1 bookkeeping arrangement described below.

### User-supplied provenance

- The user identifies the recovered final report as the exported exact original W1 ChatGPT response.
- The user identifies the nine false current-backlog paths as GPT-fabricated, not deleted or renamed files.

The supplied ZIP and vendored-source hashes preserve the acquired bytes. They do not identify the authoring model or prove that the exported response was not altered before acquisition.

### Strongly corroborated but still requiring task-level authentication

- The recovered report's verdict, baseline, branch relationship, 30-row inventory, proposed allowlist, and described W1 limitations align with repository and ledger facts checked during this reconciliation.
- The report appears internally consistent with the surviving W1 execution contract and later closure history.

A later independent task must still test material line-level claims, the execution-contract match, the reported 20 local targets and three anchors, and the historical acceptance chain before treating the export as authenticated.

### Superseded conclusions

- “The full W1 result and original proposed allowlist are unavailable.” Availability is now superseded by the recovered export.
- The governance acceptance review's conclusion that the persisted W2 table faithfully supplied the exact W1 scope is superseded.
- The strategy review's recommendation to activate W2 unchanged is superseded by the confirmed path corruption.

### Still unknown

- Whether independent authentication can establish the export as the original W1 response beyond the user's provenance statement and repository corroboration.
- Whether all recovered report findings remain correct after post-W1 changes.
- Whether current W2 should use the historical 16 paths unchanged, use a reviewed revision, or be replaced by another governed scope mechanism.
- Whether the backlog contains other unsupported semantic content that cannot be found by literal path checks.
- Current live remote state when it cannot be resolved without mutating refs or relying on stale cached observations.

## 5. Exact W1 historical semantics

The recovered report's verdict was:

```text
Acceptable for W2 scoping
```

The report explicitly said that this verdict did **not** accept or complete W1 and did not unlock W2. Later maintainer-controlled closure and ledger history record W1 as accepted and completed. Do not transfer the later closure backward into the report's own verdict.

W1 used this historical arrangement:

- task-supplied pre-pass baseline and execution lease: `3a3fe364028db003bfc89d3a94fd8a9f167d1f35`;
- explicitly approved post-baseline bookkeeping commit: `af639f43688bfd136b1dbdf051cc07bb7c588068`;
- pass result SHA: `N/A — review-only; no repository change`;
- later review-gate closure SHA: `9abed50a87fafb80157cab636fd73de018f3c5ea`;
- recorded inventory: 30 of 30 tracked Markdown files;
- reported evidence: 20 local targets and three anchors resolved, static workflow/script/schema/manifest/example audit, and `git diff --check` passing, with stated execution limitations.

The bookkeeping commit was verified during W1 but was neither the execution baseline nor the result. W1 was executed and later accepted before the normalized reusable backlog/ledger workflow existed.

The authoritative backlog therefore preserves two compatible exceptions:

1. W0 and W1's original inline specifications remain historical and are not reopened or rewritten merely because they omit fields added by the later normalized pass template. This presentation exception does not waive ledger integrity or permit inaccurate historical evidence.
2. Beginning with W2, the dedicated `Locked` to `Pending` activation commit becomes the lease and exact branch-creation point; that later rule must not be retroactively pretended to have governed W1's bookkeeping arrangement.

## 6. Propagation chain

The available evidence supports this chronology:

1. **Chat-only result:** W1 produced a final response with a 30-file audit and historical 16-path proposal, but the task deliberately returned it in chat rather than a repository report.
2. **Erroneous reconstruction:** [`../sources/W1-planning-and-handoff.txt`](../sources/W1-planning-and-handoff.txt) later reconstructed a different 16-path list. It also said the definitive W1 report remained the source of truth and required stopping if the evidence differed.
3. **Governance implementation:** commit `0fb830f92ae6f7c5933b9bace14a43e0231e9707` persisted the reconstructed list as though it were the accepted exact W1 scope.
4. **Acceptance-review miss:** [`../sources/backlog-governance-acceptance-review.txt`](../sources/backlog-governance-acceptance-review.txt) accepted the normalized structure and the wrong table without establishing source fidelity or path history.
5. **Strategy-review miss:** [`../sources/independent-technical-strategy-review.md`](../sources/independent-technical-strategy-review.md) deeply reviewed architecture but recommended activating W2 unchanged without detecting the nonexistent names.
6. **Later recovery:** the August 3 Claude handoff independently identified the corrupt table and branch-provenance defect but could not find the final report in the repository or PR. The August 4 user export then supplied the candidate final response and superseded only the “unavailable” premise.

It is verified that the planning artifact carried the wrong list and that the implementation/reviews propagated or accepted it. Whether an executor received and ignored the definitive report, or never had it available, is unknown and must not be asserted as observed motive or behavior.

## 7. Current authority and blocked state

The backlog remains the intended maintainer-controlled roadmap and state record. Creating a competing current allowlist in this context would weaken that authority. At the same time, its W2 scope attribution is demonstrably corrupt, so the table cannot safely govern execution as written.

No allowlist is currently execution-authoritative:

- the current backlog table is protected but factually invalid;
- the recovered historical list is evidence of an earlier proposal, not a current lease;
- path validity and Git consistency do not prove historical authenticity or current scope fitness;
- W2's nominal `Pending` label cannot overcome corrupt scope, missing current authorization, or invalid branch/lease provenance.

The recovered report is evidence to authenticate. It is not permission to edit the backlog, change W2 status, reuse or recreate a branch, execute W2, or mutate the Engineering Evidence Archive.

## 8. Recommended sequence

1. A user explicitly issues the inert first review prompt.
2. The reviewer freshly resolves instructions, repository/Git/GitHub state, source hashes, and evidence availability without mutating refs.
3. The reviewer authenticates the recovered report against the W1 contract, baseline tree, commit relationship, 30-row table, material evidence claims, and later closure.
4. The reviewer compares the two sets, audits post-W1 changes including `backlog-workflow-documentation.md` and `evidence-ledger-documentation.md`, and deeply reviews the backlog for other unsupported content.
5. The reviewer recommends whether current W2 should retain the authenticated historical set, adopt a justified revision, or use another governed scope; it also proposes exact status, protected-file, branch, and lease treatment.
6. The maintainer selects and explicitly authorizes an exact protected correction in a separate task.
7. An independent review authenticates the correction and preserved W0/W1 history.
8. Only after accepted remediation should a fresh exact W2 activation/lease and branch, or a documented maintainer-approved exception, be established.
9. W2 begins only under a separate explicit execution task.

Until then, the correct state is evidence reconciliation and remediation planning—not W2 execution.
