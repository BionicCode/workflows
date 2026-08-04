# Workflows migration context index

## Mission

Resume the `BionicCode/workflows` recovery program safely in Claude Code without losing the reasoning, evidence boundaries, failure history, or governance model established before migration.

The final program goal is to make Workflows the single implementation authority for managed-file synchronization and document-metadata automation, then migrate `BionicCode/template-visual-studio-repository` as the first caller without unsafe duplication, mutable production references, ownership ping-pong, or unverifiable cross-session state.

## Critical startup facts

- The detailed roadmap remains `repository-maintenance-orchestrator-recovery-backlog.md`, accompanied by `backlog-workflow-documentation.md`, `evidence-ledger-documentation.md`, and `repository-review-protocol.md`.
- W0 and W1 are recorded as completed. W2 is displayed as pending.
- W2 is not execution-ready: its 16-path allowlist contains nine fabricated paths that never existed in Git history.
- The user confirmed that an earlier GPT Work/Chat session hallucinated those paths and inserted them into the protected backlog.
- The full W1 audit result was returned in chat and is not persisted in the repository or PR #8. Only the W1 execution-handoff PDF survives outside the repository.
- The existing W2 remote branch predates the finalized W2 activation/lease sequence and cannot prove branch creation from the current activation commit.
- The current recommendation is to migrate now, but make Claude's first assignment a read-only pre-W2 evidence reconstruction and backlog-integrity review. This is a recommendation, not an instruction that overrides Claude's independent assessment or the maintainer's decision.
- Engineering Evidence Archive use is deliberately deferred until an accepted Phase 3 outcome and an explicit maintainer green light. Once validly activated, archive use is expected for in-scope durable evidence under the current task; it never becomes a second roadmap, execution lease, or acceptance authority. See `09-engineering-evidence-archive-activation.md`.

## Authority boundary

This context package is a dated migration artifact. It does not:

- replace the backlog;
- repair the ledger;
- authorize writes;
- activate, complete, reopen, or insert a pass;
- establish a pre-pass baseline;
- approve the current recommendation.

When this package and repository evidence differ, report the difference and prefer current explicit authorization plus verified repository/runtime evidence. A protected backlog correction requires a maintainer-authorized governance task.

## Evidence labels used in this package

- **Verified - repository:** observed directly in current files.
- **Verified - Git:** observed in commits, trees, refs, or reflogs.
- **Verified - external:** observed in a linked PR or official product documentation.
- **User-confirmed:** explicitly supplied by the maintainer; preserve it, but identify it as user testimony when repository evidence alone cannot prove motive or authorship.
- **Assessment:** a reasoned conclusion from the evidence, open to independent review.
- **Unknown:** not recoverable from current evidence; do not fill the gap by guessing.

## Topic routing

Read `01-project-purpose-and-architecture.md` when the task concerns:

- overall goals;
- current versus target implementation;
- repository roles;
- reusable workflow design;
- package/init/upgrade design;
- sync/doc-metadata ownership and convergence.

Read `02-control-plane-workflow-and-ledger.md` when the task concerns:

- backlog iterations;
- pass activation or closure;
- handoffs, reviews, or correction loops;
- evidence ledger fields;
- branch baselines and execution leases;
- protected control-plane changes.

Read `03-current-state-and-integrity-blockers.md` before any W2-related work.

Read `04-development-history-and-lessons.md` when a current structure or rule seems unnecessarily complicated. Many controls were added in response to concrete coordination failures.

Read `05-roadmap-overview.md` for program sequencing, then use the authoritative backlog for detailed pass contracts.

Read `06-recommendation-and-decision-record.md` before discussing whether to repair state before or after the Claude migration.

Read `07-evidence-and-source-map.md` before repeating a historical claim or treating an inference as confirmed.

Use `08-first-claude-task.md` as the proposed first read-only assignment.

Read `09-engineering-evidence-archive-activation.md` before deciding whether evidence may or must be persisted in the Engineering Evidence Archive. It defines the deferred status, future activation gate, package mapping, operational sequence, write boundaries, and degraded path.

## First-session behavior

1. Resolve the actual repository root; do not work from the old ChatGPT project mirror.
2. Read all applicable instruction and steering files.
3. Resolve local HEAD, branch, upstream, working-tree state, relevant remote tips, open PRs, and tool availability.
4. Compare fresh evidence with the dated snapshot in `03-current-state-and-integrity-blockers.md`.
5. Do not execute W2 merely because the ledger says `Pending`.
6. Keep verified facts, assessments, recommendations, and unknowns separate.
7. Return contradictions for maintainer decision before changing protected state.
8. Treat archive use as deferred unless the Phase 3 acceptance and explicit green-light gates in `09-engineering-evidence-archive-activation.md` are freshly satisfied.
