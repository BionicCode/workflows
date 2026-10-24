# Current state and integrity blockers

## 1. Status of this document

This assessment began on 2026-08-03 and its checkout facts were revalidated on 2026-08-04. It is deliberately loaded during migration because the repository's nominal W2 state is unsafe to interpret without this context.

The August 3 assessment correctly identified the corrupted W2 table and branch-provenance defect, but its conclusion that the complete W1 response was unavailable is superseded by the August 4 user export. See `10-recovered-w1-evidence-reconciliation.md` and `../sources/README.md`. The export changes the evidence available for review; it does not make W2 executable or authorize a protected correction.

Re-resolve every Git, GitHub, branch, and working-tree fact before acting. Do not convert a stale snapshot into a new execution lease.

## 2. Assessed repository state

### Reconciliation installation baseline - verified 2026-08-04

```text
Path: I:\GitHubRepositories\Workflows
Repository: BionicCode/workflows
Checkout: primary local checkout
Branch: main
HEAD: edff99aa17db08599e68cfce6e57ebc9168797c3
Local main: edff99aa17db08599e68cfce6e57ebc9168797c3
Cached origin/main: edff99aa17db08599e68cfce6e57ebc9168797c3
Working tree before reconciliation edits: clean
```

No fetch or ref mutation was performed. These values are the start state for installing the recovered handoff reconciliation, not a future execution lease. The earlier checkout snapshots below remain dated historical observations.

### Pre-change attached checkout - verified 2026-08-04

```text
Path: I:\ChatGPT And Codex Worktrees\c00e\Workflows
Repository: BionicCode/workflows
Checkout: detached linked worktree
HEAD: 8a2cf838d2511192022acf2eee3d5ba7d7c229f3
Local main: 8a2cf838d2511192022acf2eee3d5ba7d7c229f3
Local main upstream: origin/main
Cached origin/main: 8a2cf838d2511192022acf2eee3d5ba7d7c229f3
Detached-checkout upstream: none
Working tree: clean
```

`git worktree list --porcelain` also resolved the linked primary worktree at
`I:\GitHubRepositories\Workflows`, on local `main` at the same commit. That
primary checkout's read-only status was also clean on `main` with upstream
`origin/main`. The attached checkout is the task workspace and was clean before
this focused documentation update.

Root `CLAUDE.md` and context files `00` through `08` are tracked at the resolved
HEAD. This focused update adds context file `09` in the working tree. The old
condition in which root `CLAUDE.md` was an untracked one-line bridge no longer
describes the resolved baseline or resulting documentation state.

### Preserved 2026-08-03 snapshot - historical, not current

The preceding assessment observed the primary checkout at:

```text
Path: I:\GitHubRepositories\Workflows
Branch: main
Local HEAD: a0743587783b1c16a35b8e3f47d194f942ff3997
Cached origin/main: dfe10c1724ee90120e1b9692bcd8accff50f0042
main was 0 commits ahead and 1 cached commit behind origin/main
no tracked staged changes
no tracked unstaged changes
one untracked file: CLAUDE.md
```

That historical untracked `CLAUDE.md` contained exactly:

```markdown
@AGENTS.md
```

At that time it was a valid minimal Claude Code bridge but not part of a
reproducible repository baseline. Preserve this observation as history; do not
apply its untracked-file handling to the current tracked file.

### Cached remote-tracking state

```text
origin/main: 8a2cf838d2511192022acf2eee3d5ba7d7c229f3
```

The current commit is a merge whose second parent is the former cached
`origin/main` tip `dfe10c1724ee90120e1b9692bcd8accff50f0042`.
That earlier commit changed only `wwith` to `with` in the backlog's
index/ledger synchronization note. Preserve `dfe10c1...` and `a074358...` as
historical Git evidence, not as current checkout tips.

No fetch was performed during either assessment. The 2026-08-03 read-only
`git ls-remote` attempt could not connect to GitHub. The 2026-08-04 value above
is still a cached ref, not a guarantee of current live remote state.

## 3. Nominal pass state

The backlog index and ledger currently display:

- W0: `Completed`;
- W1: `Completed`;
- W2: `Pending`;
- W2A through W17: `Locked`;
- T0 through T6: `Locked`.

The index and ledger now agree textually. That does not make W2 semantically executable.

### Ledger conflict matrix

| Surface | Textual state | Repository/Git evidence | Integrity conclusion |
|---|---|---|---|
| W1 ledger row | Completed and fully populated | Recorded SHAs resolve; corrected baseline matches the W1 handoff | Structurally finalized |
| W1 evidence description | 30/30 audit completed | The ledger does not contain the detailed audit; an exported response is now vendored as historical evidence, with user-supplied provenance and strong repository corroboration | Accepted history exists; authentication and current-state reconciliation remain required |
| W2 dependency | W1 result plus maintainer-approved allowlist are scope authority | The current list contains nine paths with no Git history; the recovered report contains a different historical proposed list | The current dependency attribution is false; neither list is currently execution-authoritative |
| W2 ledger row | Pending with empty evidence cells | Empty cells are normal while active | Textually valid but not sufficient |
| W2 activation semantics | Pending implies an exact activation lease and branch created from it | The existing W2 branch began at the earlier `82c19aa...` state, before the current activation | Semantic start gate fails |
| Ordered pass index | W2 Pending | It matches the ledger after a separate corrective commit | Mirror is synchronized now, but earlier drift proves duplicated-state risk |

The ledger does not conflict because W2's cells are empty. It conflicts because the semantic facts required by `Pending` cannot be proven and because the pass's declared scope authority is known false. A finalized predecessor row also cannot guarantee that a later GPT edit preserved backlog integrity.

## 4. Confirmed fabricated W2 allowlist

### Established cause

**User-confirmed:** an earlier GPT Work/Chat session fabricated W2 paths and committed them into the protected authoritative backlog. The files were not deleted and are not missing checkout content. They never existed.

**Verified - Git:** `git log --all --follow -- <path>` returned no history for every path below.

### Fabricated paths

```text
.github/instructions/code-review.instructions.md
.github/instructions/tests.instructions.md
.github/scripts/doc-metadata/README.md
.github/scripts/doc-metadata/tests/README.md
.github/scripts/sync-files-from-manifest/README.md
.github/tools/doc-metadata/README.md
.github/tools/doc-metadata/api-reference.md
.github/tools/doc-metadata/type-reference.md
.github/tools/sync-config/README.md
```

The W2 table has 16 entries. Nine are fabricated, leaving only seven literal paths that exist. The W2 acceptance criteria nevertheless require accounting for all 16 and call the table the exact maintainer-approved W1 allowlist.

### Real nearby paths

The following real paths illustrate the mismatch:

```text
.github/instructions/dotnet.instructions.md
.github/instructions/test.instructions.md
.github/scripts/sync-files-from-manifest/documentation/**
.github/tools/doc-metadata/documentation/**
```

These are not declared one-for-one replacements. A current W2 allowlist must be selected from authenticated historical evidence plus current implementation and post-W1 governance evidence. Similar names are insufficient proof of scope.

The recovered W1 response now supplies a historical proposed set containing the real nearby instruction and documentation paths. That set must be authenticated and reviewed against post-W1/current state; it must not be applied as a guessed rename map or automatic current replacement. See `10-recovered-w1-evidence-reconciliation.md` for both complete sets.

## 5. How the fabricated list entered the backlog

Commit `0fb830f92ae6f7c5933b9bace14a43e0231e9707` formalized W2 and introduced the 16-path table. Its commit message described the table as an "accepted 16-path documentation scope."

The fabricated paths appear in that diff even though:

- the W1 audit had systematically enumerated 30 tracked Markdown files;
- none of the nine paths existed in the W1 tree;
- none has history anywhere in the local Git object database;
- actual documentation is organized in `documentation/` trees with different filenames.

The current backlog therefore contains an unsupported attribution: it presents a later GPT-generated list as the maintainer-approved output of W1.

## 6. W1 administrative completion versus recovered evidence

### What is recorded

The W1 ledger row records:

```text
Pre-pass baseline: 3a3fe364028db003bfc89d3a94fd8a9f167d1f35
Result: N/A — review-only; no repository change
PR: 8
Review-gate closure: 9abed50a87fafb80157cab636fd73de018f3c5ea
Evidence: 30/30 tracked Markdown audited; 20 local targets and 3 anchors resolved;
          static workflow/script/schema/manifest/example audit;
          git diff --check PASS; stated execution limitations
Reviewer: BionicCode
```

The W1 baseline contains exactly 30 tracked Markdown files. The preserved
2026-08-03 cached `dfe10c1...` snapshot contained 32, with
`backlog-workflow-documentation.md` and `evidence-ledger-documentation.md`
added after W1. The revalidated pre-change `8a2cf838...` baseline contains 43;
this focused update adds context file `09` in the working tree. Recount at the
exact reviewed result rather than treating a dated count as a current
allowlist.

### What the recovered export adds

The W1 execution handoff required a dated row for every potentially normative Markdown file, including:

- authority/canonical owner;
- copied/generated relationship;
- implementation match;
- contradictions;
- required owning pass;
- line-level evidence;
- exact proposed W2 allowlist.

The handoff explicitly required this report in the final chat response and prohibited creating a repository report file. The surviving PDF is only the nine-page execution contract, not the final audit.

PR #8 contains the closure commit and a minimal "closing W1" description, but no persisted audit table or review discussion. The August 4 user export now supplies a candidate complete final response under `../sources/W1-final-audit-report.txt`. Its 30-row table, baseline facts, and historical proposed allowlist are strongly corroborated, but its attribution as the exact original response remains user-supplied and requires independent authentication.

### Precise conclusion

W1 is **administratively completed** and should not casually return to `Pending`.

W1's report was **not evidentially portable in the repository/PR at the time of the August 3 assessment**. The recovered export now makes the candidate report portable inside this handoff, without retroactively proving provenance or current scope fitness.

The later W2 allowlist is **known invalid** and cannot serve as a substitute for the recovered historical result.

The recovered historical list is **evidence, not an execution lease**. Authentication, post-W1 review, maintainer selection, protected correction, independent acceptance, and a valid later lease remain necessary.

Do not claim that the W1 audit never occurred. The evidence supports that it was performed and later accepted, and the recovered response provides strong evidence of its output. It does not support the current W2 table's attribution.

## 7. W1 ledger-history correction

W1 closure commit `9abed50...` initially recorded the bookkeeping commit `af639f4...` as the pre-pass baseline. That was inconsistent with the actual task handoff, which used `3a3fe36...`.

Later commits:

- corrected the baseline to `3a3fe36...`;
- documented `af639f4...` as the one approved post-baseline bookkeeping change;
- formalized why the activation SHA belongs in the handoff first and in the ledger only at closure.

The current W1 baseline cell is correct. Preserve the earlier error in history because it explains the current ledger design; do not rewrite it as though the error never happened.

## 8. W2 activation and branch-provenance conflict

### Branch history

The local remote-tracking reflog first recorded the W2 branch at:

```text
82c19aa38cd894b40b2fe833e136731a8017d3a4
```

on 2026-07-14. That was an early attempt to mark W2 pending before the later ledger/activation workflow was finalized.

Subsequent target-branch events included:

```text
634e63b...  W2 Locked -> Pending
aaf71d3...  W2 Pending -> Locked for strategy review
298d04c...  W2 Locked -> Pending again
fc731de...  ordered index corrected to Pending
ae9ec24...  reusable rule added: index must move with ledger
a074358...  backlog repeats the synchronization rule
dfe10c1...  typo-only correction
```

The existing W2 branch was later fast-forwarded. It was not newly created from `298d04c...`, the current pending activation transition.

### Semantic consequence

Under the current ledger workflow, `Pending` means:

- a valid activation commit exists;
- the handoff supplies that exact SHA as the lease;
- the pass branch was created from that exact commit;
- ancestry and working-tree checks passed.

The existing branch cannot prove those conditions. Pointing at the same tip as `origin/main` does not repair its creation provenance.

The empty W2 ledger evidence cells are normal for an active pass. The blocker is the invalid or absent runtime lease and branch creation history, combined with the corrupt scope.

## 9. Prior independent strategy review is partly superseded

The 2026-07-15 independent technical strategy review concluded:

```text
Accept with non-blocking recommendations
Activate W2 unchanged
```

It inspected the repository and confirmed many architectural defects, but it did not detect that nine W2 paths were nonexistent. Its conclusion that W2 was safe to activate is therefore superseded by later evidence and the maintainer's confirmation.

The review's later-pass architecture recommendations may still be valuable hypotheses. They must be independently reassessed rather than discarded or adopted wholesale.

## 10. Why the entire current backlog needs review

The nine paths are a confirmed failure witness, not proof that every other statement is wrong. A bounded literal-path scan found no additional obviously unlabelled missing paths beyond those nine; other missing names were explicitly planned, historical, or candidate paths.

That scan cannot detect semantic hallucinations. The deep review should verify:

- every current-state assertion against implementation;
- every pass dependency and ordering claim;
- every exact file/command/test name;
- every ownership and trust premise;
- every current-versus-planned label;
- every accepted historical SHA and its semantic role;
- every claim imported from the independent review;
- whether roadmap recommendations were accepted, rejected, or never decided;
- whether every Markdown file at the exact reviewed state has the correct authority classification;
- whether any real W2-required document is omitted.

## 11. Current blockers before actual W2 execution

1. The authoritative W2 allowlist is known false.
2. The recovered W1 report and historical proposed allowlist are now persisted as handoff evidence, but their exported-original provenance and material claims still need independent authentication.
3. The two post-W1 workflow/ledger guides were never part of the 30-file W1 baseline and need inclusion in a current integrity and scope review.
4. The backlog requires a semantic audit for additional unsupported GPT content.
5. The existing W2 branch does not satisfy current activation provenance.
6. No execution-ready W2 handoff supplies a valid current lease.
7. Live remote state has not been refreshed; cached `origin/main` is not a live-remote guarantee.
8. Protected backlog/ledger corrections require explicit maintainer authorization and independent review.

The earlier local-behind and untracked-`CLAUDE.md` conditions are resolved in
the 2026-08-04 attached checkout and are not current blockers.

## 12. Unresolved questions for Claude and the maintainer

- Should the recovery use an inter-pass governance correction, insert a new bounded recovery pass, or define a formal reopening mechanism?
- Should W2 return to `Locked` during repair, or should the correction be framed as maintenance of the currently pending state?
- After authenticating the historical proposal, should current W2 retain that set, adopt a justified post-W1 revision, or use another governed scope?
- Does W2 remain the right pass after the deep audit, or must it be revised/split?
- What additional backlog statements were introduced by GPT without evidence?
- Should the existing W2 branch be retained as historical evidence, abandoned without deletion, or explicitly superseded by a fresh branch?
- Which non-binding recommendations from the independent strategy review should be admitted into the roadmap?
- Which accepted Engineering Evidence Archive Phase 3 outcome and explicit maintainer green light will satisfy the activation procedure in `09-engineering-evidence-archive-activation.md`?

Do not answer these by convenience. Produce evidence and alternatives for maintainer decision.

## 13. Resolution shape assessed as safest

The prior Codex assessment recommended:

1. migrate to Claude Code now;
2. run a read-only authentication of the recovered W1 report plus post-W1 and full backlog-integrity audit;
3. let the maintainer approve exact corrections;
4. correct the protected backlog and any related control-plane contradictions in a separately authorized task;
5. independently review that correction;
6. establish a fresh, exact W2 baseline, branch, and handoff;
7. start W2 only then.

This is a reasoned recommendation, not a mandatory workflow change. Claude is expected to challenge it where repository evidence supports a safer or simpler alternative.
