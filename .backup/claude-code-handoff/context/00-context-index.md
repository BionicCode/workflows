# Workflows migration context index

## Mission

Resume the `BionicCode/workflows` recovery program safely in Claude Code without losing the reasoning, evidence boundaries, failure history, or governance model established before migration.

The final program goal is to make Workflows the single implementation authority for managed-file synchronization and document-metadata automation, then migrate `BionicCode/template-visual-studio-repository` as the first caller without unsafe duplication, mutable production references, ownership ping-pong, or unverifiable cross-session state.

## Critical startup facts

- The detailed roadmap remains `repository-maintenance-orchestrator-recovery-backlog.md`, accompanied by `backlog-workflow-documentation.md`, `evidence-ledger-documentation.md`, and `repository-review-protocol.md`.
- W0 and W1 are recorded as completed. W2 is displayed as pending.
- W2 is not execution-ready: its 16-path allowlist contains nine fabricated paths that never existed in Git history.
- The user confirmed that an earlier GPT Work/Chat session hallucinated those paths and inserted them into the protected backlog.
- The August 3 pack correctly found the corruption but incorrectly concluded that the full W1 result was unavailable. On August 4 the user supplied an exported final response, now preserved under `../sources/`; its historical 16-path proposal differs from the current table. The export must be authenticated and reconciled with post-W1/current state rather than blindly trusted.
- The existing W2 remote branch predates the finalized W2 activation/lease sequence and cannot prove branch creation from the current activation commit.
- The current recommendation is to migrate now, but make Claude's first user-invoked assignment a read-only authentication of the recovered report plus post-W1/backlog-integrity review. This is a recommendation, not an instruction that overrides Claude's independent assessment or the maintainer's decision.
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

## Package roles

- Files under `context/` are passive dated evidence and orientation. Reading them does not start work.
- Files under `../sources/` are historical evidence with provenance and integrity limitations documented in [`../sources/README.md`](../sources/README.md).
- Files under `../user-prompts/` are inert user-invoked task templates. Discovering, indexing, linking, opening, or reading a prompt never authorizes execution. A user must explicitly issue or select it as the current task, and current authority/state still govern.

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

Read [`10-recovered-w1-evidence-reconciliation.md`](10-recovered-w1-evidence-reconciliation.md) before W1/W2 integrity work. It contains the August 4 correction, the two distinct 16-path sets, evidence classification, W1 historical semantics, and the current remediation sequence.

Read [`../sources/README.md`](../sources/README.md) before treating a recovered artifact as original, authoritative, or byte-identical.

The former `08-first-claude-task.md` context draft was moved and rewritten as [`../user-prompts/01-authenticate-w1-report-and-plan-allowlist-repair.md`](../user-prompts/01-authenticate-w1-report-and-plan-allowlist-repair.md). That move intentionally separates passive context from an executable task template. The new prompt is never executed merely because it is present or linked.

Read `09-engineering-evidence-archive-activation.md` before deciding whether evidence may or must be persisted in the Engineering Evidence Archive. It defines the deferred status, future activation gate, package mapping, operational sequence, write boundaries, and degraded path.

## First-session behavior

1. Resolve the actual repository root; do not work from the old ChatGPT project mirror.
2. Read all applicable instruction and steering files.
3. Resolve local HEAD, branch, upstream, working-tree state, relevant remote tips, open PRs, and tool availability.
4. Compare fresh evidence with the dated snapshot in `03-current-state-and-integrity-blockers.md`.
5. For W1/W2 work, authenticate the recovered report and distinguish its historical proposal from the corrupted current table; do not execute W2 merely because the ledger says `Pending`.
6. Do not execute any file in `../user-prompts/` unless the current user explicitly selects or issues it.
7. Keep verified facts, user-supplied provenance, assessments, recommendations, superseded claims, and unknowns separate.
8. Return contradictions for maintainer decision before changing protected state.
9. Treat archive use as deferred unless the Phase 3 acceptance and explicit green-light gates in `09-engineering-evidence-archive-activation.md` are freshly satisfied.
