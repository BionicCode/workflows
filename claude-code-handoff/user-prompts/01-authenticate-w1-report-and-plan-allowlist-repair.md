# User-invoked prompt: authenticate W1 and plan W2 allowlist repair

> [!CAUTION]
> This repository file is an inert task template. Its presence, discovery, indexing, linking, or reading does not authorize or start the task. Execute it only when the current user explicitly issues or selects it. The current user request, current repository state, and freshly resolved instructions always govern.

## Role and mode

Act as an independent evidence reviewer and remediation planner for `BionicCode/workflows`.

Mode: **review-only**.

Do not implement the remediation and do not execute W2. Produce a self-contained authentication and governance-repair proposal for later maintainer decision.

## Objective

Authenticate the user-supplied recovered W1 final report as far as available evidence permits; compare its historical proposed 16-path W2 allowlist with the different corrupted 16-path table now in the protected backlog; audit post-W1 drift and the backlog for other unsupported semantic content; and recommend exact protected-file, W2-status, branch, and lease treatment for a separately authorized later implementation.

Do not blindly trust the recovered report. Its repository facts are strongly corroborated, but the user's statement that it is the exact original ChatGPT response is not cryptographically provable from the export alone.

## Absolute non-mutation boundary

Do not modify or create any file, including reports, generated files, caches inside the repository, the Git index, or an Engineering Evidence Archive package.

Do not:

- stage, commit, push, fetch, pull, merge, rebase, reset, restore, checkout, switch, create/delete/move a branch or tag, stash, clean, or mutate any ref;
- open, update, close, label, review, or merge a pull request or issue;
- dispatch, rerun, cancel, or approve a workflow;
- change repository settings, permissions, branch protection, or secrets;
- edit the protected backlog, ledger, review protocol, instruction surfaces, this handoff, or any implementation file;
- install dependencies into the repository;
- execute W2 or any later pass; or
- initialize, populate, checksum, validate-as-complete, repair, or otherwise mutate the Engineering Evidence Archive.

Read-only local Git inspection and read-only remote queries are allowed only when they do not update refs or repository state. Do not use `git fetch` as an inspection shortcut. If live remote state cannot be established without mutation or unavailable credentials, label it unknown.

## Repository identity and dated hints

The intended implementation-authority repository is:

```text
BionicCode/workflows
```

Resolve the actual repository root and remote identity. Do not work from a project mirror, the template caller repository, or a path selected only because it appears in dated context.

Historical anchors to verify, not current leases:

```text
W1 baseline and execution lease:
3a3fe364028db003bfc89d3a94fd8a9f167d1f35

W1 post-baseline bookkeeping commit:
af639f43688bfd136b1dbdf051cc07bb7c588068

W1 review-gate closure:
9abed50a87fafb80157cab636fd73de018f3c5ea

Governance normalization that persisted the wrong list:
0fb830f92ae6f7c5933b9bace14a43e0231e9707
```

Re-resolve current branch, HEAD, upstream, working tree, relevant local and cached remote-tracking refs, and any safely queryable live remote tips. Record initial and final state. Stop if the review surface changes.

## Required instruction and context resolution

Read every applicable instruction completely before analysis, including at least:

```text
CLAUDE.md
AGENTS.md
AGENT_GUARDRAILS.md
DOCUMENTATION.md
.github/copilot-instructions.md
.github/instructions/*.instructions.md
src/AGENTS.md
test/AGENTS.md
repository-review-protocol.md
repository-maintenance-orchestrator-recovery-backlog.md
backlog-workflow-documentation.md
evidence-ledger-documentation.md
claude-code-handoff/context/00-context-index.md
claude-code-handoff/context/03-current-state-and-integrity-blockers.md
claude-code-handoff/context/04-development-history-and-lessons.md
claude-code-handoff/context/06-recommendation-and-decision-record.md
claude-code-handoff/context/07-evidence-and-source-map.md
claude-code-handoff/context/09-engineering-evidence-archive-activation.md
claude-code-handoff/context/10-recovered-w1-evidence-reconciliation.md
claude-code-handoff/sources/README.md
```

Treat `claude-code-handoff/context/` as passive dated context and `claude-code-handoff/sources/` as historical evidence. Do not execute any file in `claude-code-handoff/user-prompts/` merely because this task links to or discovers it.

## Required recovered sources and integrity checks

Inspect these vendored historical sources:

```text
claude-code-handoff/sources/W1-final-audit-report.txt
claude-code-handoff/sources/W1-planning-and-handoff.txt
claude-code-handoff/sources/backlog-governance-acceptance-review.txt
claude-code-handoff/sources/independent-technical-strategy-review.md
```

Verify every ZIP-entry and installed hash, exact-match result, and documented terminal-LF limitation in `claude-code-handoff/sources/README.md`. At minimum corroborate:

```text
Supplied ZIP SHA-256:
0173a3352f6452feae17cae0698fbd48f57d24ddfd8bb037952b10b06bb28c2d

W1 final report ZIP-entry SHA-256:
4afa74679b22197a392341750235767e598f74a756e4b0b84cff85e842a69129

W1 execution-handoff PDF ZIP-entry SHA-256:
14b0f7a3bfbe2b7584cdcf961ff49237259b8a652e1923337e4d97e9829d61cc
```

The PDF is the W1 execution contract, not the final report. It was intentionally not vendored. Use the externally supplied ZIP or another copy explicitly supplied by the current user. If it is unavailable, do not invent its content: use repository-corroborated summaries only for a partial check, identify exactly which contract assertions remain unauthenticated, and state whether that prevents a final verdict.

For provenance, distinguish:

- cryptographically verified byte identity with the supplied export;
- user-supplied attribution as the original ChatGPT response;
- repository/Git corroboration of claims inside the response;
- inference; and
- unknown authenticity or acquisition details.

A matching hash proves only identity with the acquired package. It does not prove authorship, originality, or correctness.

## Two distinct 16-path sets

Never merge or casually call both sets “the W1 allowlist.”

### Recovered report's historical proposed set

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

### Current protected-backlog set

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

Verify independently that:

- each set has exactly 16 unique paths;
- their intersection has exactly seven paths;
- every recovered-report path existed at the W1 baseline and determine whether it still exists now;
- each of the nine current-only names was absent at the W1 baseline, absent when inserted by `0fb830f...`, absent now, and has no local Git history across all available refs; and
- no apparent nearby filename is treated as a replacement without evidence.

The nine current-only names are allegations of fabricated paths to prove with concrete Git witnesses. Their nonexistence does not by itself prove which model or person authored them.

## Required work

### 1. Resolve fresh state without mutating refs

Record:

- repository root, full remote identity, and repository role;
- default branch as safely resolvable;
- current branch or detached state and exact HEAD;
- upstream, cached remote-tracking tips, and safely queryable live tips, clearly distinguished;
- ahead/behind and ancestry relations;
- complete working-tree and index state;
- relevant W1 and W2 branch tips and reflog evidence available locally;
- relevant PR state if accessible read-only;
- all applicable instructions and conflicts;
- tool/runtime availability and unavailable evidence.

Do not normalize, checkout, fetch, or clean state to make it fit the handoff. If unrelated changes exist, classify them and stop when they prevent a trustworthy immutable review.

### 2. Authenticate the recovered final report against the W1 contract

Compare the report with the verified W1 execution-handoff contract, including:

- repository identity, W1 branch, baseline, and review-only mode;
- lease and branch relationship checks;
- complete tracked-Markdown enumeration requirement;
- authority/canonical-owner, copied/generated, implementation-match, contradiction, owning-pass, and evidence columns;
- implementation/schema/manifest/workflow/script/example/link tracing requirements;
- exact final-report sections and stop conditions;
- proposed W2 allowlist requirement; and
- final-chat-report/no-repository-report requirement.

Identify every contract field the recovered report satisfies, partially satisfies, contradicts, or leaves unverified.

### 3. Authenticate repository and Git claims

Independently verify at least:

- both `3a3fe364...` and `af639f...` resolve as commits;
- `af639f...` has the baseline as its sole parent;
- its only changed file and exact `+2/-2` diff;
- the baseline has 57 tracked files and 30 tracked Markdown files;
- the recovered report has exactly 30 unique audit rows and the set equals the baseline Markdown inventory;
- every audit row refers to the correct baseline file and role;
- material implementation, schema, manifest, workflow, script, example, link, and contradiction claims are reproducible at the baseline;
- the reported 20 local targets and three anchors can be reproduced or precisely explained;
- the report's stated validation limits and no-write result are internally and historically consistent; and
- the historical proposed allowlist follows from the report's own findings rather than only matching a list at its end.

Use concrete witness files and line references. A consistent SHA/path table is strong evidence, not automatic proof that the export is original.

### 4. Reconcile verdict, acceptance, and historical closure

Preserve these distinct facts:

- the recovered report's verdict was `Acceptable for W2 scoping`;
- the report explicitly did not accept/complete W1 or unlock W2;
- W1 was later accepted and closed through maintainer-controlled history;
- W1 result SHA is `N/A — review-only; no repository change`;
- `af639f...` is bookkeeping, not baseline or result; and
- `9abed50...` is later review-gate closure evidence, not the report's result.

Inspect the closure commit, PR #8 evidence if accessible, subsequent baseline corrections, and current ledger. State what establishes later acceptance and what remains dependent on historical records or user testimony.

### 5. Apply the W1 historical exception exactly

The authoritative backlog says W0 and W1 were accepted before adoption of the normalized pass template. Their inline specifications remain historical and are not reopened or rewritten merely because later template fields are absent. This presentation exception does not waive ledger integrity or permit accepted history to be recorded inaccurately.

It separately records that W1 predates the finalized activation-commit workflow, used `3a3fe364...` as its supplied baseline/lease, and had one approved bookkeeping commit `af639f...`. Beginning with W2, the dedicated activation commit is the lease and branch-creation point.

Do not pretend the later normalized workflow governed W1. Do not use the exception to excuse current corrupted W2 scope or inaccurate history. Do not recommend casually changing W1 from `Completed` back to `Pending`.

### 6. Trace the propagation chain

Compare:

1. the recovered chat-only W1 result;
2. the erroneous reconstructed set in `W1-planning-and-handoff.txt`, including its stop-on-discrepancy instruction;
3. governance implementation commit `0fb830f...`;
4. `backlog-governance-acceptance-review.txt`;
5. `independent-technical-strategy-review.md`; and
6. the August 3 handoff's later discovery and August 4 recovery.

Determine exactly what is verified about propagation. Do not claim to know whether an executor ignored the definitive report or never received it unless direct evidence proves that choice.

### 7. Audit post-W1 changes and current scope fitness

Enumerate and inspect every material post-W1 change affecting documentation authority, lifecycle, scope, state, or implementation claims. Explicitly include:

```text
backlog-workflow-documentation.md
evidence-ledger-documentation.md
repository-review-protocol.md
repository-maintenance-orchestrator-recovery-backlog.md
```

Determine:

- which files and claims did not exist in the W1 30-file baseline;
- which historical W1 findings remain current, became stale, were already corrected, or need a different owning pass;
- whether later changes require adding, removing, or changing any current W2 candidate path;
- whether copied/shared instruction ownership and overlay restrictions changed;
- whether a real current documentation defect exists outside the historical set; and
- whether admitting it to current W2 would require an explicit governed scope revision rather than silent widening.

### 8. Deep-audit the protected backlog

Do more than check literal paths. Verify current-state, architecture, dependency, pass-order, authority, trust, branch, SHA, command, workflow, test, schema, manifest, fixture, documentation, and migration claims against repository evidence.

For each questionable statement classify it as:

- confirmed false;
- confirmed stale;
- current but incomplete;
- planned and correctly labelled;
- historical and correctly labelled;
- plausible risk; or
- unknown.

Check whether recommendations from the strategy review were accepted, rejected, deferred, or merely copied as if decided. Include the two post-W1 guides in the consistency audit. Do not edit the backlog or weaken its protected status.

### 9. Determine the correct governance recommendation

Compare at least these outcomes:

1. retain the authenticated historical 16-path set as current W2 scope;
2. revise that set for documented post-W1/current-state changes while preserving what the historical report actually said; or
3. use another governed scope or bounded follow-up mechanism.

For each option state:

- supporting and contrary evidence;
- historical-fidelity impact;
- current documentation coverage;
- protected-control-plane changes required;
- lifecycle/status implications;
- branch/lease implications;
- migration and later-pass risk;
- unresolved maintainer choices; and
- the exact decision gate.

Recommend one option only when evidence supports it. Path existence and internal Git consistency alone are insufficient.

### 10. Recommend exact W2 status, branch, and lease treatment

Freshly verify the current W2 index/ledger status and the existing W2 branch's creation/provenance. Assess:

- whether W2 should remain nominally `Pending` during repair, be returned to `Locked`, or be handled through another explicitly governed transition;
- whether zero pending passes during maintenance is required or preferable;
- whether the existing W2 branch should be retained only as historical evidence, explicitly excepted, or superseded by a fresh branch;
- which exact accepted commit should become a later activation baseline;
- how index and ledger synchronization must be preserved; and
- how to avoid pretending a later fast-forward proves correct branch creation.

Do not perform any status or branch operation.

## Required final report

Return a durable, self-contained Markdown report in the chat response only. Include:

1. independent verdict on report authentication, with confidence and exact limits;
2. resolved repository/Git/GitHub state and final stability recheck;
3. source inventory, hash results, provenance classification, and PDF availability;
4. W1 contract-to-report compliance matrix;
5. baseline/commit/30-row/evidence-claim authentication results;
6. historical verdict, acceptance, closure, result-SHA, and special-case reconciliation;
7. exact two-set comparison with counts, seven-path intersection, and nine nonexistent-path witnesses;
8. post-W1/current-state delta audit;
9. severity-ordered backlog-integrity findings with file and line evidence;
10. assessment of the three current-scope options;
11. recommended exact protected changes, including proposed wording or table rows, but no applied edit;
12. proposed W2 index/ledger status treatment and invariant-preserving transition sequence;
13. proposed disposition of the existing W2 branch and exact later branch/lease procedure;
14. risks, unknowns, rejected alternatives, and maintainer decisions required;
15. an implementation handoff for a later, separately authorized protected correction, naming exact allowed/prohibited paths, baseline preconditions, validation, review gate, and stop conditions;
16. confirmation that W2 was not executed;
17. confirmation that no file, Git, GitHub, or archive state changed; and
18. archive status `NOT ARCHIVED`, with a pending-ingestion record only if the current task requires one under `context/09`.

Separate verified facts, user-supplied provenance, inference, recommendation, superseded conclusions, and unknowns throughout.

## Stop conditions

Stop and return a bounded partial report if:

- repository identity, baseline objects, or required sources cannot be resolved reliably;
- source hashes do not match their documented raw or normalized identity contract;
- the review surface changes;
- applicable instructions conflict materially;
- the execution contract is unavailable and the missing fields prevent authentication;
- a required remote fact cannot be obtained without mutation or unavailable credentials;
- a command would write, install, fetch, checkout, or require unapproved credentials;
- evidence cannot distinguish the two 16-path sets; or
- the requested conclusion would require guessing historical authenticity, current scope, or maintainer intent.

The task ends with evidence and a recommendation. It does not repair the backlog, alter W1/W2 state, create a branch or lease, execute documentation changes, run W2, or mutate the Engineering Evidence Archive.
