# Development history and lessons

## 1. Why this history matters

Several current rules look ceremonial when read without context. They were added after concrete failures involving ambiguous baselines, duplicated state, missing durable reports, premature activation, and GPT-generated false repository facts.

This document preserves those causes so Claude can simplify only when the underlying guarantee remains intact.

## 2. Project identity and context migration

The ChatGPT project that carried this work was named approximately `template-visual-studio-repository sync automation`. That name was misleading for the active implementation phase. The actual repository under recovery is `BionicCode/workflows`; `template-visual-studio-repository` is only the first later caller migration.

The user wanted to move from a cloud/project mirror to a local-folder project so the actual repository/worktree could be provided to Work and Codex. The desktop product did not support moving existing chats between projects, so detailed Markdown handoffs became necessary.

Work then paused before W2 while a separate Engineering Evidence Archive was introduced as a durable home for authorized handoffs, execution reports, reviews, and material supporting evidence. Archive use remains deliberately deferred until its Phase 3 migration is accepted and the maintainer explicitly green-lights use. The Claude migration and Workflows backlog repair do not wait for that gate. After valid activation, archive persistence is expected for in-scope durable evidence under the current task, using `09-engineering-evidence-archive-activation.md`; it is not a second backlog or acceptance authority.

## 3. Repository development before the recovery roadmap

### March 2026: reusable workflow repository begins

Relevant Git history:

- initial repository and CI/release/lint workflows;
- reusable `.editorconfig` synchronization;
- first manifest-driven reusable sync workflow (`bb4f7c0...`);
- early workflow-call and trigger corrections.

### May 2026: managed sync becomes a real engine

The sync subsystem gained:

- manifest validation;
- `init`, `validate`, and `sync` behavior;
- source paths and source globs;
- `target_directory` semantics;
- marker-aware whole/outside/inside scopes;
- path-safety and duplicate-target handling;
- atomic planning/write behavior;
- schema and multi-page type documentation;
- caller configuration bootstrap.

The root `AGENTS.md` and documentation conventions were also introduced.

On 2026-05-28, repository maintenance and managed-file orchestration were added. Sync configuration documentation was briefly added and then removed. Document-metadata repair commits and manifests were also present. By the July review, core doc-metadata blobs in Workflows and the template caller were identical, but documentation and caller-specific configuration were not assumed interchangeable.

This history explains why the recovery explicitly says not to rewrite Workflows from scratch: substantial sync and metadata behavior already exists.

## 4. July 13: authoritative recovery control plane (W0)

### Initial roadmap and protocol

Commit `1e2348e947dab8f4e597cb864b488085951d10fa` added:

- the recovery backlog;
- the repository review protocol;
- repository-specific agent rules.

The roadmap separated:

- Workflows engine recovery (W passes);
- template caller migration (T passes);
- protected governance from implementation;
- pass execution from review acceptance.

### Early coordination corrections

Several rapid commits added:

- completion checkboxes;
- maintainer ownership of status/ledger state;
- protected control-plane rules;
- exact W0 scope and review gate;
- an evidence ledger.

W0 was delivered by PR #4. Its result and closure were recorded separately.

### What these corrections taught

The backlog itself was being evolved while work was beginning. Early defects included redundant W2 ledger entries, evolving column semantics, and incomplete W0 closure data. These were corrected before W1 through PRs #5 and #6 and direct coordination commits.

Lesson: a Markdown table that parses is not necessarily a valid state machine. Structural, evidence, status, and timing semantics require review.

## 5. July 13: generic instruction surfaces added before W1

Commit `38ddb8bd7c70ab40617aefee66685d0b3e2c948c` added:

- `AGENT_GUARDRAILS.md`;
- `DOCUMENTATION.md`;
- `.github/copilot-instructions.md`;
- `.github/instructions/dotnet.instructions.md`;
- `.github/instructions/test.instructions.md`;
- `src/AGENTS.md`;
- `test/AGENTS.md`;
- an empty `docs/` placeholder.

The Workflows repository has no .NET source tree; `src/` and `test/` contain only these instruction files. W1 was therefore explicitly told not to presume that generic .NET/testing instruction copies were applicable. Their source, scope, and authority had to be audited.

Lesson: inherited template documentation can look normative while being technically irrelevant to the current repository. Names and polished prose do not prove applicability.

## 6. W1: documentation authority audit

### Activation context

Commit `3a3fe364028db003bfc89d3a94fd8a9f167d1f35` became the task-supplied W1 baseline. It also clarified workflow role terminology and protocol rules.

The existing W1 branch received one approved bookkeeping commit:

```text
af639f43688bfd136b1dbdf051cc07bb7c588068
```

It recorded the task baseline in the ledger and restored a missing final newline. It was not W1 result work.

### W1 assignment

The surviving nine-page PDF handoff required:

- review-only operation;
- exact lease and branch checks;
- systematic enumeration of every tracked Markdown file;
- authority/copy/generated/current/planned/historical classification;
- implementation comparison;
- link, schema, manifest, workflow, script, example, and template tracing;
- a dated 30-row audit table;
- exact owning pass per correction;
- a proposed exact W2 allowlist;
- a final chat report only, with no repository report file.

### W1 recorded outcome

The ledger records:

- 30/30 tracked Markdown files audited;
- 20 local targets and 3 anchors resolved;
- static workflow/script/schema/manifest/example audit;
- `git diff --check` passed;
- PowerShell suite and Actions not run;
- sync test command discovered zero tests because `jsonschema` was unavailable.

Closure commit:

```text
9abed50a87fafb80157cab636fd73de018f3c5ea
```

PR #8 merged the closure.

### Evidence persistence mistake

The final W1 report was intentionally kept in chat and was not persisted in the repository or PR #8. The PDF is only the handoff, not the result. That made the report unavailable to the August 3 repository-only recovery even though W1 had occurred.

On August 4 the user supplied an exported candidate original final response, now preserved under `../sources/`. Its 30-row table and historical proposed 16-path set are strongly corroborated by the baseline, but the export's originality remains user-supplied provenance that must be authenticated rather than assumed.

Lesson: "return the report in chat" satisfied the immediate task but failed the long-term interruption-recovery goal. Critical review artifacts must be persisted in an authorized durable location, even when they should not become normative repository documentation.

## 7. W1 ledger baseline mistake and repair

W1 closure initially recorded `af639f4...` as the pre-pass baseline. That confused the approved bookkeeping branch tip with the task's actual execution lease `3a3fe36...`.

Post-W1 governance work:

- corrected the W1 baseline;
- documented the historical bookkeeping arrangement;
- formalized self-reference and delayed ledger population;
- separated result, closure, finalization, and next activation commits.

Important commits include:

```text
33fe38a...  introduce evidence-ledger documentation and backlog-workflow file
2cc9a58...  substantially complete ledger workflow semantics
deb32c2...  add ledger-integrity review to the review protocol
a3d2b9e...  complete reusable backlog workflow documentation
91e8dad...  document W1 historical exception
4f6cb04...  correct W1 baseline
51a5749...  clarify W1 bookkeeping role
```

Lesson: every SHA needs one semantic role, and a commit cannot contain its own final SHA. The handoff must carry the active lease until closure can record it historically.

## 8. Early W2 activation and rollback to maintenance

Commit `82c19aa...` finalized W1's PR/closure fields and marked W2 `Pending`. It also contained several typographical and semantic issues in then-current ledger guidance.

Commit `a32610f...` changed W2 back to `Locked` so governance could be repaired before work.

The remote W2 branch was already created at `82c19aa...`. This is central to the later provenance problem: the branch predates the finalized activation-commit workflow.

Lesson: create branches only after the final prerequisite state and lease rules exist. A later fast-forward cannot retroactively prove a correct branch-creation event.

## 9. Governance normalization and the hallucinated allowlist

The recovered W1 report and the later planning artifact now expose two different 16-path sets. The report's historical proposal names 16 paths that existed at the W1 baseline. `W1-planning-and-handoff.txt` reconstructed a different set with nine nonexistent names, while also warning that the definitive W1 report remained the source of truth and that a discrepancy required a stop.

Commit `0fb830f92ae6f7c5933b9bace14a43e0231e9707`:

- added the concise ordered pass index;
- formalized W2 as a documentation-only implementation pass;
- separated deferred candidates from admitted passes;
- inserted a detailed 16-path W2 allowlist.

The user confirmed that an earlier GPT session fabricated nine of those paths. Git history independently confirms that none ever existed. The governance implementation persisted the erroneous reconstruction; the later acceptance review treated its internally consistent 16-row structure as sufficient, and the strategy review missed path existence.

This is the most important unresolved mistake. The commit described the list as an accepted W1 scope even though the persisted repository contained no W1 audit result capable of supporting that claim.

Lesson: an agent must enumerate and verify exact paths before placing them in an authoritative allowlist. A plausible repository layout is not evidence.

The evidence supports a propagation chain of chat-only W1 result, erroneous reconstruction, governance implementation, acceptance-review miss, strategy-review miss, and later recovery. It does not establish whether the implementation executor received and ignored the definitive report or never had it available.

## 10. July 15: W2 toggles, missed review finding, and index drift

Sequence:

```text
634e63b...  ledger W2 Locked -> Pending
aaf71d3...  W2 Pending -> Locked for a final technical strategy review
298d04c...  W2 Locked -> Pending after that review
fc731de...  ordered pass index separately corrected from Locked to Pending
ae9ec24...  ledger guide requires index/ledger transition in the same commit
a074358...  backlog repeats the synchronization rule
dfe10c1...  corrects "wwith" typo in that note
```

The independent strategy review at `aaf71d3...` verified many architectural claims and recommended `Activate W2 unchanged`. It missed that nine allowlisted paths did not exist.

The review remains useful for later trust, snapshot, packaging, and sequencing questions, but its W2 readiness conclusion is superseded.

Lesson: a broad, sophisticated architecture review can still miss a simple repository-grounding check. Exact path existence and history checks belong in every allowlist review.

## 11. Index/ledger duplication lesson

The ordered pass index was meant only for navigation, while the ledger was the state authority. Because W2 was changed in the ledger first and the index later, the two temporarily contradicted each other.

Rules were added requiring every status transition to update both in the same coordination commit.

Lesson: duplicated state is hazardous even when one copy is labelled non-authoritative. If a navigational mirror is retained, automatic or same-commit consistency checks are essential.

## 12. Pause for evidence-archive work

The project stopped before real W2 implementation. The user explored an Engineering Evidence Archive so future handoffs, review reports, and accepted evidence would survive project/chat migration. Recovering the W1 export on August 4 reduces one immediate evidence gap but reinforces the need for durable, provenance-aware storage.

That work was motivated directly by the then-unavailable W1 result and the broader goal of evidence-led development. Recovering the export later does not remove the persistence lesson. Archive activation is not a prerequisite for repairing the Workflows backlog. The current decision is to keep archive integration deferred, use a SHA-pinned Claude handoff now, and retain archive-ready reports plus exact pending-ingestion records until Phase 3 is accepted and the maintainer gives the explicit green light.

Deferral does not make later use vague or optional. After a valid activation, Claude should follow `09-engineering-evidence-archive-activation.md` and persist qualifying durable evidence when the current task authorizes the exact package and artifacts. The activation does not authorize Workflows edits, Git/GitHub actions, unrelated archive packages, technical acceptance, maintainer acceptance, or source integration.

## 13. 2026-08-02/03 migration assessment

The historical 2026-08-02/03 migration assessment re-resolved the local
Workflows checkout and found the following at that time:

- local `main` at `a074358...`;
- cached `origin/main` at `dfe10c1...`;
- one untracked `CLAUDE.md` containing `@AGENTS.md`;
- no tracked worktree changes;
- W2 branch cached at the same remote tip as `origin/main`;
- W1 branch at `9abed50...`;
- the nine nonexistent allowlist paths;
- no full W1 report in the repository or PR #8 at that time;
- W2 branch reflog beginning at pre-normalization commit `82c19aa...`.

These are preserved historical observations, not current checkout hints. The
2026-08-04 pre-change checkout facts are recorded in
`03-current-state-and-integrity-blockers.md`.

The user explicitly reminded the agent that the allowlist was hallucinated. That correction changed the blocker analysis from "missing files" to "corrupted authoritative backlog."

On August 4, after that repository-side pack was prepared, the user supplied the recovered final-response export. This later evidence supersedes only the premise that the W1 response and historical proposed list are unavailable. It does not supersede the corruption, branch-provenance, current-authorization, or archive-activation boundaries.

Lesson: preserve user corrections prominently. Repeating an invalid list without its provenance can cause both the user and the next agent to forget that the defect is GPT-generated, not a repository omission.

## 14. Mistake/correction ledger

| Mistake or risk | Correction already made | Remaining work |
|---|---|---|
| Vague/duplicated pass state | Ledger and normalized lifecycle introduced | Automate structural checks later if useful |
| Executor could be confused with acceptance authority | Maintainer-only closure/activation rules | Preserve role separation in Claude tasks |
| Bookkeeping commit confused with W1 baseline | Baseline corrected; historical exception documented | Keep exact SHA roles in new handoffs |
| Commit self-reference timing unclear | Delayed population and distinct finalization defined | Follow it consistently |
| W2 activated before maintenance finished | Temporarily returned to Locked | Current pending state still needs semantic repair |
| Index and ledger status diverged | Same-commit synchronization rule added | Consider one generated view or validation |
| W1 report lived only in chat | User export is vendored as non-normative historical evidence with hashes and provenance limits | Authenticate it; persist any later accepted evidence through an authorized durable process |
| GPT invented nine W2 paths | Cause now documented; Git history checked; historical W1 proposal recovered | Authenticate the report, deep-audit current state, and replace the list only through authorized governance |
| Strategy review missed basic path validity | Conclusion marked superseded | Retain useful later recommendations only after revalidation |
| W2 branch predates current lease rules | Defect identified | Establish fresh branch/lease or approved exception |
| Generic .NET instructions appear in non-.NET repo | W1 was tasked to classify them | Authenticate the recovered authority finding and review current scope |
| Product names used as workflow roles | Reusable workflow docs define roles | State role explicitly in every Claude task |

## 15. Durable lessons for Claude

1. Inspect real implementation, tests, schemas, manifests, and Git history before trusting Markdown.
2. Verify every exact path in an allowlist, including whether it ever existed.
3. Preserve user-confirmed corrections and distinguish them from inference.
4. Do not rewrite accepted history to hide a later defect.
5. Do not treat completion, merge, result, closure, and activation commits as interchangeable.
6. Do not activate the next pass as part of closing the current one.
7. Keep current and future behavior visibly separate.
8. Persist accepted review evidence somewhere durable and authorized.
9. A branch at the right tip can still have invalid creation provenance.
10. Sophisticated analysis does not replace simple structural checks.
11. When the authoritative source is corrupt, repair its integrity; do not silently create a competing authority.
12. Reassess recommendations independently when their premises were later disproved.
13. A recovered export can resolve availability without proving originality; preserve its hashes and provenance, then authenticate material claims against repository evidence.
