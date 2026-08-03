# Migration recommendation and decision record

## 1. Question assessed

Before moving this project to Claude Code, should the current side:

- hand Claude the present repository and let it start W2;
- quickly fix the W2 allowed-files list;
- reopen or complete W1 again so Claude receives a clean W2 start;
- finish all pre-W2 repair before migration;
- or migrate now with a recovery-oriented handoff?

## 2. Non-binding conclusion

The prior Codex assessment recommended:

> Migrate to Claude Code now, but migrate at the pre-W2 recovery boundary rather than presenting W2 as execution-ready.

Claude's first assignment should be a source-grounded, read-only reconstruction of W1 evidence and a full integrity review of the current backlog. Protected corrections, a fresh branch/lease, and actual W2 work should follow only after maintainer review.

This recommendation is intentionally non-binding. Claude should reconstruct the reasoning below, challenge its premises, and offer a safer or simpler alternative if fresh evidence supports one.

## 3. Decision analysis

### Option A: start W2 immediately

Assessment: unsafe.

Reasons:

- nine of 16 allowed paths are fabricated;
- the detailed W1 result is unavailable;
- W2's branch was not created from the current activation commit;
- no valid current execution handoff/lease exists;
- the local and live remote state are not freshly reconciled.

### Option B: replace only the nine paths, then start W2

Assessment: insufficient.

Reasons:

- there is no evidence-backed one-to-one replacement map;
- real documentation trees contain many files omitted from the table;
- a confirmed hallucination in an authoritative source creates a semantic trust problem beyond literal path existence;
- the branch/lease problem would remain;
- the protected backlog requires authorized governance review.

The eventual text diff may be small. Establishing that it is the correct diff is not a minor task.

### Option C: reopen and complete W1 again

Assessment: usually misleading and contrary to current lifecycle rules.

Reasons:

- W1 is recorded completed and accepted;
- current workflow says a completed pass does not casually return to pending;
- the corruption was introduced after W1;
- rewriting W1 history would obscure the later GPT failure.

The missing evidence should be reconstructed, and the post-W1 corruption should be corrected through an explicit maintenance/follow-up/governance mechanism chosen by the maintainer.

Claude should still examine whether the project's current rules require a formal reopening procedure or a new inserted pass. It should not assume the label in advance.

### Option D: finish all remediation in Codex before migration

Assessment: safe but unnecessarily delays the platform migration.

The same read-only audit is suitable as Claude's onboarding task. Performing it in Claude lets the new agent learn the repository from evidence while producing the repair proposal it will later need.

### Option E: migrate now with a pre-W2 recovery handoff

Assessment: recommended.

Benefits:

- does not falsely advertise a clean W2 state;
- preserves W1 history;
- makes Claude prove its repository grounding before implementation;
- avoids duplicating a substantial audit across agents;
- allows the Engineering Evidence Archive work to remain deferred;
- produces a natural decision gate before protected edits.

## 4. Recommended sequence

### Phase A: migration and read-only reconstruction

Claude receives:

- the real local Workflows checkout;
- stable `CLAUDE.md`/`AGENTS.md` instructions;
- this context pack;
- a read-only first task.

It independently verifies:

- local and remote Git state;
- instruction/control-plane precedence;
- W1 baseline and 30-file corpus;
- two post-W1 steering documents;
- every backlog current-state and exact-path claim;
- W2 allowlist and branch provenance;
- the prior recommendation itself.

### Phase B: maintainer decision

The maintainer chooses:

- correction mechanism and pass/state treatment;
- real W2 scope;
- disposition of the old W2 branch;
- whether Claude files/context become tracked;
- which strategy-review recommendations enter the roadmap;
- where reconstructed evidence should be persisted.

### Phase C: authorized control-plane remediation

Only an explicitly authorized task should:

- correct the fabricated allowlist and any other verified backlog defects;
- state that GPT-generated false information was removed;
- preserve accepted W0/W1 history;
- synchronize index/ledger state;
- update related steering semantics only where required;
- receive independent review.

### Phase D: W2 reactivation/readiness

After accepted remediation:

- resolve a clean target baseline;
- resolve the `CLAUDE.md` working-tree decision;
- issue a SHA-pinned W2 handoff;
- create a fresh W2 branch from the exact activation commit, or document a maintainer-approved exception;
- verify ancestry, diff, and working tree;
- start W2.

## 5. Proposed readiness gates before actual W2

All should be true or explicitly waived by the maintainer:

1. Every backlog statement classified as current has repository evidence.
2. Every literal current path exists; planned/historical paths are labelled.
3. The reconstructed W1 authority map is reviewable.
4. The real W2 allowlist names only verified paths and explains each inclusion.
5. Other GPT-introduced backlog changes have been audited.
6. The protected correction is accepted and recorded at an exact commit.
7. Index and ledger agree in the same commit.
8. Local target branch and actual remote state are reconciled.
9. Working-tree exceptions, including `CLAUDE.md`, are explicitly resolved or included in the lease.
10. The W2 branch originates at the accepted activation commit.
11. The execution handoff states exact repository, target, branch, baseline, expected HEAD, allowed/prohibited files, validation, and stop conditions.
12. The current prompt explicitly authorizes W2 execution.

## 6. Engineering Evidence Archive recommendation

Do not block the Claude migration or backlog repair on Engineering Evidence Archive integration.

For now, preserve reliability through:

- exact SHAs;
- explicit evidence labels;
- self-contained Markdown reports;
- complete file inventories;
- recorded limitations;
- maintainer acceptance.

After the reconstruction and correction are accepted, store their final handoff/review artifacts in the archive if that program is ready. The archive should preserve evidence; it should not become a second roadmap authority.

## 7. Conditions that could change the recommendation

Claude should recommend a different sequence if fresh evidence proves, for example:

- the original W1 audit result exists in a recoverable authoritative source;
- a real accepted W2 allowlist exists elsewhere and can be authenticated;
- the remote W2 branch was recreated from a valid activation commit in history unavailable to this assessment;
- current remote state already contains an accepted governance repair;
- the maintainer intentionally established a different reopening or maintenance mechanism;
- keeping migration context outside the repository creates an unacceptable operational risk.

Any changed recommendation should identify the new evidence and explain which prior premise no longer holds.

## 8. Recommended discussion outcome

Claude should return one of these high-level conclusions after its first audit:

- **Proceed with the proposed pre-W2 remediation sequence**;
- **Proceed with a revised remediation sequence**, with exact differences and rationale;
- **W2 can start after bounded normalization**, with proof that every blocker is resolved;
- **Blocked pending maintainer decision or missing evidence**, with exact questions.

It should not merely agree with this document.
