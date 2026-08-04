# Proposed first Claude Code task: pre-W2 integrity reconstruction

## Handoff state

```text
Proposed for independent review - not approved for repository execution
```

This task is deliberately read-only. It is intended to let Claude independently evaluate the migration recommendation and reconstruct a safe next step. It does not authorize correction of the backlog or execution of W2.

## Objective

Assess whether `BionicCode/workflows` can safely resume at W2. Reconstruct the missing W1 documentation-authority evidence as far as current repository and Git history permit, deeply audit the current recovery backlog for hallucinated or unsupported content, verify W2 lifecycle/branch integrity, and recommend an exact remediation path.

## Operating mode

Review-only. Use Claude Code plan/read-only controls where available.

Do not modify:

- repository files;
- generated files;
- Git index or working tree;
- branches, refs, commits, tags, stashes, or remotes;
- pull requests, issues, reviews, workflow runs, or repository settings;
- backlog statuses, checkboxes, or evidence cells;
- the tracked `CLAUDE.md` or this context package.

Do not install dependencies into the repository or run state-changing validation.

## Repository identity

The authoritative working repository is the local checkout of:

```text
BionicCode/workflows
```

Do not use `template-visual-studio-repository` as the active implementation repository. It is a later caller migration and may be inspected only if the current prompt and available checkout authorize read-only evidence gathering.

## Dated state hints, not leases

The latest read-only assessment on 2026-08-04 observed the attached task worktree:

```text
checkout: detached linked worktree
HEAD: 8a2cf838d2511192022acf2eee3d5ba7d7c229f3
local main: 8a2cf838d2511192022acf2eee3d5ba7d7c229f3
local main upstream: origin/main
cached origin/main: 8a2cf838d2511192022acf2eee3d5ba7d7c229f3
working tree: clean
tracked at the resolved baseline: CLAUDE.md and context files 00 through 08
nominal backlog state: W0/W1 Completed, W2 Pending, later passes Locked
```

Re-resolve all state yourself. These values do not authorize checkout, pull, fetch, branch creation, or W2 work.

The older `a074358...` local-main, `dfe10c1...` cached-upstream, and untracked-`CLAUDE.md` observations are preserved as historical evidence in `03-current-state-and-integrity-blockers.md`; they are not current hints.

## Engineering Evidence Archive boundary

Engineering Evidence Archive use is deferred for this proposed task. Do not create, populate, checksum, validate as complete, or otherwise mutate an archive package. Read `09-engineering-evidence-archive-activation.md` for the future gate and procedure. If this review produces evidence worth retaining, return an archive-ready durable report and an exact pending-ingestion record; do not claim that either was archived.

## Required sources

Read completely where applicable:

```text
CLAUDE.md
AGENTS.md
AGENT_GUARDRAILS.md
DOCUMENTATION.md
.github/copilot-instructions.md
.github/instructions/*.instructions.md
src/AGENTS.md
test/AGENTS.md
repository-maintenance-orchestrator-recovery-backlog.md
backlog-workflow-documentation.md
evidence-ledger-documentation.md
repository-review-protocol.md
claude-code-handoff/context/*.md
```

Inspect implementation, tests, schemas, manifests, workflows, templates, and Git history needed to verify claims. Do not infer behavior from documentation names.

## Established allegation to verify

The maintainer states that an earlier GPT session fabricated nine W2 allowlist paths. The prior assessment found no Git history for any of them. Independently verify:

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

Treat their absence as a backlog-integrity problem, not a request to create them.

## Required work

### 1. Resolve state

Record:

- repository full name and root;
- default branch;
- local branch and HEAD;
- upstream and actual remote tip if safely resolvable;
- ahead/behind relation;
- complete working-tree status;
- relevant local/remote W1 and W2 branch tips;
- open relevant PRs if accessible;
- applicable instructions;
- available/unavailable tools and evidence.

Do not fetch or mutate refs unless a separate current prompt explicitly authorizes it. If live remote state cannot be resolved, label it unknown.

### 2. Validate control-plane consistency

Compare:

- backlog index;
- evidence ledger;
- completion checkboxes;
- backlog pass contracts;
- evidence-ledger rules;
- backlog workflow rules;
- review protocol;
- branch/reflog history;
- current task authorization.

Report every structural, state, evidence, ancestry, commit-separation, or authority contradiction.

### 3. Reconstruct W1 evidence

At minimum:

- resolve W1 baseline `3a3fe364028db003bfc89d3a94fd8a9f167d1f35`;
- enumerate its 30 tracked Markdown files;
- enumerate current tracked Markdown and identify post-W1 additions;
- classify every current document by role, canonical owner, copied/generated relationship, implementation match, contradictions, and likely owning pass;
- validate local links/anchors and exact current path claims;
- compare current implementation where needed;
- identify what cannot be reconstructed without the original final report.

Do not fabricate the original W1 conclusions. Produce a new dated reconstruction and distinguish it from the historical accepted result.

### 4. Deep-audit the backlog

Do more than path existence checks. Verify:

- current-state defect claims;
- approved-versus-proposed architecture labels;
- pass dependencies and order;
- exact file, command, workflow, test, schema, and manifest names;
- status/ledger SHA semantics;
- user/agent authority boundaries;
- future filenames labelled as future;
- every recommendation imported or omitted from the independent strategy review;
- contradictions with `backlog-workflow-documentation.md` and `evidence-ledger-documentation.md`;
- whether any real required documentation is absent from W2 scope;
- whether any other GPT artifact is unsupported.

For each suspected problem, classify:

- confirmed false;
- confirmed stale;
- current but incomplete;
- planned and correctly labelled;
- historical and correctly labelled;
- plausible risk;
- unknown.

### 5. Propose a real W2 scope

Produce an evidence-backed candidate allowlist. For every candidate path state:

- why it belongs in W2;
- exact current defect;
- minimum correction;
- authority/copy/generated status;
- implementation evidence;
- risk of conflicting with a later behavior pass;
- whether a protected overlay boundary applies.

Also list audited files that should intentionally remain unchanged.

Do not edit any proposed file.

### 6. Evaluate lifecycle repair options

Assess at least:

- inter-pass governance repair with zero pending passes;
- revision of the current W2 contract while preserving W1 history;
- insertion of a bounded recovery/evidence-reconstruction pass;
- formal reopening procedure, if justified;
- reuse of the existing W2 branch under an explicit exception;
- a fresh W2 activation commit and branch.

Explain which option best preserves current invariants and why. Do not assume the prior Codex recommendation is correct.

### 7. Review later strategic recommendations

Briefly classify the independent strategy review's unresolved proposals as:

- still supported and should be added before its owning pass;
- useful but needs further planning;
- obsolete or already covered;
- contradicted;
- not yet assessable.

Pay particular attention to trusted policy, immutable source snapshots, ownership-plan attestation/transport, package atomicity/downgrade/concurrency, action pinning, W14 ordering, W3's W6/W7 reference, and completed-pass follow-up semantics.

## Required final report

Return a self-contained Markdown report with:

1. independent verdict;
2. resolved state and limitations;
3. authority/control-plane consistency matrix;
4. W1 reconstruction coverage and dated authority table;
5. confirmed backlog defects, severity ordered;
6. hallucinated-path verification;
7. proposed real W2 allowlist with evidence;
8. W2 branch/lease assessment;
9. later-roadmap recommendation review;
10. comparison of remediation options;
11. recommended next sequence and decision gates;
12. exact protected changes that would require later authorization;
13. unresolved maintainer questions;
14. confirmation that no file/Git/GitHub state changed;
15. archive status (`not archived`) and, when useful, the exact pending-ingestion record required by `09-engineering-evidence-archive-activation.md`.

Clearly separate:

- verified facts;
- user-confirmed provenance;
- assessment;
- recommendation;
- unknowns.

## Stop conditions

Stop and return a partial report if:

- the repository changes during review;
- required content cannot be read reliably;
- remote state moves during a leased observation;
- a command would require a write or credential not authorized;
- the supposed Workflows checkout is not the actual repository;
- applicable instructions materially conflict and cannot be reconciled read-only.

Do not stop merely because the original W1 report is missing. Reconstruct what can be proven and state the exact evidence gap.

## Expected decision boundary

This first task ends with analysis and a recommendation. It must not:

- correct the backlog;
- complete/reopen W1;
- activate/deactivate W2;
- create a new pass;
- create or reset a branch;
- implement documentation changes;
- commit the Claude context pack;
- initialize, populate, checksum, or otherwise mutate an Engineering Evidence Archive package.

The maintainer will separately decide and authorize any remediation.
