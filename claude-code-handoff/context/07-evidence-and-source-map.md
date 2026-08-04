# Evidence and source map

## 1. Evidence precedence for this handoff

Use this order when validating the pack:

1. current explicit maintainer authorization;
2. freshly resolved repository content and Git state;
3. live GitHub evidence tied to exact SHAs;
4. executable implementation/tests/schemas/manifests;
5. applicable repository instructions;
6. accepted durable review artifacts;
7. this migration pack;
8. prior chat summaries and commit messages.

The pack intentionally contains user-confirmed provenance that Git cannot prove by itself. Keep that testimony identified rather than turning it into an unexplained repository fact.

## 2. Authoritative repository steering files

### `repository-maintenance-orchestrator-recovery-backlog.md`

Used for:

- project goal;
- reviewed defects;
- approved target architecture;
- W0-W17 and T0-T6 roadmap;
- W1/W2 specifications;
- evidence ledger;
- current nominal statuses.

Known limitation: current W2 scope is corrupted and cannot be executed as written.

### `backlog-workflow-documentation.md`

Used for:

- outcome-oriented pass design;
- roles;
- handoff/execution/review lifecycle;
- correction and inter-pass maintenance rules;
- completed-work follow-up guidance;
- interruption recovery;
- anti-patterns.

Added after W1 and therefore outside the original 30-file audit.

### `evidence-ledger-documentation.md`

Used for:

- status definitions;
- activation/closure/finalization timing;
- SHA semantic roles;
- baseline lease checks;
- fully-finalized rows;
- index/ledger synchronization rule.

Added after W1 and therefore outside the original 30-file audit.

### `repository-review-protocol.md`

Used for:

- repository authority model;
- evidence precedence;
- start/stop gates;
- protected control plane;
- reusable workflow, package, trust, validation, and review rules.

### Instruction surfaces

Used for task behavior and protected scope:

```text
AGENTS.md
AGENT_GUARDRAILS.md
DOCUMENTATION.md
.github/copilot-instructions.md
.github/instructions/dotnet.instructions.md
.github/instructions/test.instructions.md
src/AGENTS.md
test/AGENTS.md
```

Important applicability fact: `src/` and `test/` contain only their AGENTS files in the assessed checkout. Generic .NET instructions should not be presumed relevant to a Python/PowerShell/GitHub Actions repository.

### Deferred Engineering Evidence Archive routing

`09-engineering-evidence-archive-activation.md` is the Workflows-side procedure for future archive use. It does not activate the archive. After activation, the archive's current `CLAUDE.md`, `AGENTS.md`, `EVIDENCE_TRACKING.md`, `TOOLING.md`, `requirements.txt`, versioned schemas, tests, project metadata, and existing package records must be read from a freshly resolved archive checkout. A missing instruction import or material conflict is a stop condition; never invent the missing content.

Read-only revalidation on 2026-08-04 observed:

```text
Archive repository: BionicCode/engineering-evidence-archive
Last-known local path: I:\GitHubRepositories\ChatGPT\EngineeringEvidenceArchive\engineering-evidence-archive
Branch: main
HEAD: e6d98ebc799d3b67e94f0edc531de3746badc6d3
Cached upstream: origin/main at 3125e561b8d42cb746eb4313ffbcf2cb21e55e2c
Divergence: five commits ahead, zero behind
Working tree: clean
```

This is dated evidence, not an activation lease. Phase 3 remains incomplete;
`projects/workflows` and W1 remain legacy pre-contract state. Archive
`CLAUDE.md` still imports the absent
`docs/claude-context/00-core-context.md`, and root `AGENTS.md` still refers to
removed `projects/template-visual-studio-repository` content in its migration
boundary. The current host has Python 3.14.6 but not the pinned `PyYAML`
dependency; read-only repository validation therefore returned exit `2`,
`DEPENDENCY_UNAVAILABLE`, without changing archive state. Re-resolve all of
these conditions after Phase 3 rather than treating them as permanent claims.

## 3. Current implementation anchors

### Workflows

```text
.github/workflows/repository-maintenance.yml
.github/workflows/doc-metadata.yml
.github/workflows/sync-files-from-manifest.yml
```

### Managed sync implementation

```text
.github/scripts/sync-files-from-manifest/common.py
.github/scripts/sync-files-from-manifest/init_manifest.py
.github/scripts/sync-files-from-manifest/validate_manifest.py
.github/scripts/sync-files-from-manifest/sync_files.py
.github/scripts/sync-files-from-manifest/marker_scope.py
.github/scripts/sync-files-from-manifest/source_glob.py
.github/scripts/sync-files-from-manifest/schema/**
.github/scripts/sync-files-from-manifest/templates/**
.github/scripts/sync-files-from-manifest/tests/**
```

### Doc-metadata implementation

```text
.github/scripts/doc-metadata/update-doc-metadata.ps1
.github/scripts/doc-metadata/resolve-content-change-links.ps1
.github/scripts/doc-metadata/tests/Invoke-DocMetadataAcceptanceTests.ps1
.github/tools/doc-metadata/doc-metadata-manifest.json
.github/tools/doc-metadata/doc-metadata-manifest.schema.json
```

### Product documentation trees

```text
.github/scripts/sync-files-from-manifest/documentation/**
.github/tools/doc-metadata/documentation/**
README.md
```

## 4. W1 source artifact

The old ChatGPT project mirror contained:

```text
C:\Users\Mobil\.codex\.chatgpt-projects\g-p-6a50cf8284008191800cbfe6d163fb7f\sources\Handoff W1 - W1 Documentation Authority Audit.pdf
```

Verified content:

- nine pages;
- title `W1 Documentation Authority Audit`;
- exact baseline/branch lease;
- review-only constraints;
- required 30-file authority audit method;
- exact final-report structure;
- requirement to propose a W2 allowlist;
- explicit instruction to return the report in chat and not create a repository file.

It does **not** contain the final audit table or findings.

The PDF was text-extracted with `pdfplumber` and rendered with Poppler. Pages 1 and 6 were visually inspected to confirm title, lease content, and audit-table layout.

## 5. Independent strategy review artifact

The old project mirror also contained:

```text
C:\Users\Mobil\.codex\.chatgpt-projects\g-p-6a50cf8284008191800cbfe6d163fb7f\sources\independent-technical-strategy-review(2).md
```

Review date: 2026-07-15.

Useful evidence:

- confirmed current orchestration, caller-engine, harness, and manifest defects;
- supported the central architecture;
- identified trusted-policy, immutable source snapshot, plan attestation, package transaction, bootstrap, action pinning, sequencing, and live-platform gaps.

Known failure:

- concluded W2 could be activated unchanged;
- failed to notice nine nonexistent W2 paths.

Treat later-pass recommendations as review input, not accepted roadmap changes.

## 6. Git evidence anchors

### Initial recovery and W0

```text
1e2348e947dab8f4e597cb864b488085951d10fa  initial backlog/protocol
ed8b11288b89a5f0aca2c1551e2d8bdb1606c8a8  PR #4 merge / W0 result
f0005ad6a23431bbac4e2e2c6955a6d59a9437cb  W0 closure evidence
```

### W1

```text
3a3fe364028db003bfc89d3a94fd8a9f167d1f35  W1 task baseline
af639f43688bfd136b1dbdf051cc07bb7c588068  approved bookkeeping commit
9abed50a87fafb80157cab636fd73de018f3c5ea  W1 closure commit
272ba878960d2666def987c1fbf05893e9f49cbe  PR #8 merge commit
```

### Post-W1 governance

```text
82c19aa38cd894b40b2fe833e136731a8017d3a4  early W2 pending/finalization attempt
a32610f2a408f681db3ae6b1285c2f2b1301f6bd  return W2 to Locked for maintenance
33fe38a8dc897ca0085427e35c5ee06c4a09de53  add ledger/backlog workflow docs
2cc9a58744dde3ce255f868b88e3f52e514d2237  expand ledger semantics
deb32c22e921033c3bfeebd259d53c895fea4ee3  add ledger integrity review
a3d2b9ea6f65a150df41c79e19e8193bff164aca  complete backlog workflow guide
4f6cb042b4fb74b274d0bd2ef43fffa866c54038  correct W1 baseline
51a5749181e2f10c80ccd6b9a37be190ee7444d3  clarify W1 exception
0fb830f92ae6f7c5933b9bace14a43e0231e9707  normalize W2 and add invalid allowlist
```

### W2 state sequence

```text
634e63b9a2d577af6eb63ac0a9e3e80d013cbca5  W2 Pending
aaf71d3840f52aa94b9976cb2e69e96d9e44b2d9  W2 Locked for review
298d04ced734a1a3fd8e406054c810885334fe75  W2 Pending again
fc731de4a206a2a8ce020af9f1c740c0946a55fd  index synchronized to Pending
ae9ec24ee4a7326e850d1c48a13072139b1a3c71  workflow synchronization rule
a0743587783b1c16a35b8e3f47d194f942ff3997  backlog synchronization rule
dfe10c1724ee90120e1b9692bcd8accff50f0042  typo-only follow-up
```

## 7. Markdown inventory evidence

At W1 baseline `3a3fe36...`:

```text
30 tracked Markdown files
```

At the preserved 2026-08-03 cached snapshot `dfe10c1...`:

```text
32 tracked Markdown files
```

At the revalidated pre-change HEAD `8a2cf838...` on 2026-08-04:

```text
43 tracked Markdown files
```

This handoff update adds `09-engineering-evidence-archive-activation.md` to the
working tree. Recount at the exact reviewed result rather than treating either
historical count as a future invariant.

Added after W1:

```text
backlog-workflow-documentation.md
evidence-ledger-documentation.md
```

No tracked Markdown path from the W1 baseline was removed.

## 8. Fabricated-path verification

For each of the nine paths listed in `03-current-state-and-integrity-blockers.md`, local Git history was queried across all refs with path following. Every query returned no commit.

This independently supports the user's statement that they never existed. It does not by itself identify which model/session authored them; that attribution is user-confirmed.

## 9. External evidence

- PR #8: `https://github.com/BionicCode/workflows/pull/8`
- Claude Code project memory/import behavior: `https://code.claude.com/docs/en/memory`

The PR was inspected read-only and did not expose the missing W1 audit.

## 10. Verification limitations

- No fresh `git fetch` or `pull` was performed.
- The 2026-08-03 direct `git ls-remote` attempt could not connect to GitHub; live remote state remains unknown.
- Local and cached refs were re-resolved on 2026-08-04 but remain cached evidence.
- No Workflows build, executable test suite, formatter, or workflow was run; this focused handoff update uses documentation, link, SHA, and diff checks only.
- No template-caller checkout was revalidated in the current migration task.
- No live Actions settings, branch protection, credentials, or private-source fixtures were inspected.
- The full W1 result is unknown.
- The exact earlier GPT session that generated each backlog sentence is not mechanically recoverable from Git.
- A bounded path scan cannot establish semantic backlog integrity.
- The Codex memory registry contained no Workflows-specific entry; this pack relies on repository evidence, supplied project artifacts, current conversation context, and the maintainer's correction.
- The 2026-08-04 archive validator attempt could not proceed beyond its dependency bootstrap because the pinned runtime dependencies are not installed on this host; the archive test suite was not run.

## 11. Claims that remain assessments

These should be independently reviewed:

- migrating now is preferable to repairing everything before migration;
- a read-only pre-W2 audit is the best Claude onboarding task;
- W1 should remain closed while its evidence is reconstructed;
- a fresh W2 branch is safer than reusing the existing branch;
- the exact future Engineering Evidence Archive activation prerequisites have been satisfied when the maintainer gives the green light;
- the backlog's obvious missing-path blast radius may be limited to the known nine;
- strategy-review recommendations remain useful despite its W2 miss.

The current archive deferral is explicit maintainer direction, not one of these assessments. The future readiness facts must still be verified at activation time.

## 12. Revalidation checklist for Claude

Before repeating a handoff claim:

1. resolve current local HEAD and worktree;
2. resolve actual remote tips without mutating state unless authorized;
3. verify the cited commit exists and inspect its diff;
4. inspect the current file rather than relying on this summary;
5. classify the claim as current, historical, planned, user-confirmed, inferred, or unknown;
6. report any drift from the latest dated snapshot in this file.
