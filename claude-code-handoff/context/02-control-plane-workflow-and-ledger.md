# Control-plane workflow and evidence ledger

## 1. Why the control plane exists

The recovery spans many dependent passes, multiple agents/sessions, two repositories, protected files, live GitHub behavior, and exact rollback boundaries. Earlier work exposed the risk of relying on chat state, branch names, or a vague notion of "the latest commit."

The control plane was introduced to make the work recoverable after interruption and to separate:

- project intent from task authorization;
- stable pass specifications from runtime handoffs;
- implementation from independent review;
- result commits from lifecycle bookkeeping;
- a branch name from an immutable execution lease;
- accepted history from later corrections.

The system is deliberately stricter than a normal issue/PR workflow because later passes depend on independently accepted earlier state and because a wrong authority decision can cause cross-repository writes or automation ping-pong.

## 2. Steering-file responsibilities

### `repository-maintenance-orchestrator-recovery-backlog.md`

Primary responsibility:

- project-specific goal and boundaries;
- approved architecture and decisions;
- confirmed defects and unverified areas;
- ordered W and T passes;
- per-pass scope, outputs, validation, stop conditions, and review gates;
- current pass status and accepted evidence ledger;
- project-specific historical exceptions.

It is the intended authoritative roadmap and project-state record. It does not authorize writes by itself. Its current W2 section is known to contain fabricated paths, so it must be repaired through its governance process rather than silently replaced by this handoff.

### `backlog-workflow-documentation.md`

Primary responsibility:

- reusable end-to-end backlog lifecycle;
- pass admission and sizing;
- roles;
- handoff creation and authorization review;
- explicit execution directive;
- result review and correction loops;
- closure, inter-pass maintenance, interruption recovery, and common anti-patterns.

It intentionally avoids project-specific pass IDs, SHAs, repository names, and technical architecture. Those belong in the backlog.

### `evidence-ledger-documentation.md`

Primary responsibility:

- ledger column meanings;
- `Locked`, `Pending`, and `Completed` semantics;
- allowed transitions;
- activation, execution lease, closure, and post-merge finalization timing;
- SHA role separation;
- fully-finalized row definition;
- start gates and blocking contradictions.

It explains why some fields cannot be populated in the same commit that creates their value.

### `repository-review-protocol.md`

Primary responsibility:

- evidence precedence;
- repository-role classification;
- required state header;
- pass-start and ledger-integrity review;
- review-only, planning, and implementation rules;
- reusable workflow, package, trust, documentation, validation, and test-quality gates;
- protected control-plane files;
- required review output and completion standard.

Current project state and pass order belong in the backlog, not in a competing protocol section.

### `AGENTS.md`, `AGENT_GUARDRAILS.md`, `DOCUMENTATION.md`, and scoped instructions

Primary responsibility:

- repository execution behavior;
- task modes and review expectations;
- protected files;
- validation and completion reporting;
- path-specific engineering/test rules;
- documentation policy.

The root `AGENTS.md` states that only the current user prompt grants Git/GitHub actions and that protected control-plane paths require exact explicit authorization.

## 3. Authority and evidence precedence

The control plane is not a permission system by itself. The intended precedence is:

1. current explicit user authorization;
2. exact repository content at the resolved commit;
3. live workflow evidence tied to that commit;
4. executable parsers/tests tied to that commit;
5. applicable repository instructions;
6. authoritative current product documentation;
7. backlog and review reports;
8. chat history and commit messages.

This ordering prevents a planned Markdown statement or confident prior agent summary from overriding current executable behavior.

## 4. Roles versus products

Roles are responsibilities, not tool names:

- **Maintainer:** owns intent, roadmap, protected state, acceptance, closure, and activation.
- **Backlog designer:** decomposes outcomes, dependencies, scope, gates, and stop conditions.
- **Handoff author:** translates one activated pass into a runtime contract with exact state.
- **Executor:** performs authorized work and reports; does not accept or close its own pass.
- **Reviewer:** independently evaluates evidence; does not silently fix while in review-only mode.
- **Control-plane coordinator:** performs explicitly authorized ledger/backlog changes without altering pass-result content.

ChatGPT Work, Codex, Claude Code, and humans can fill roles. Naming a product does not define whether it is planning, executing, reviewing, or accepting.

## 5. Backlog iteration workflow

### 5.1 Design and admit

A proposed pass must be outcome-oriented, bounded, independently reviewable, correctly ordered, and free of unresolved policy that an implementation agent would otherwise have to invent.

### 5.2 Prepare while locked

Before activation:

- previous pass is fully finalized;
- approved inter-pass maintenance is complete;
- no pass is active;
- decisions and scope are ready;
- a draft handoff is reviewed for fidelity;
- control-plane contradictions are corrected.

### 5.3 Activate and establish lease

The maintainer performs a dedicated `Locked -> Pending` coordination commit on the target branch. That exact commit becomes the pre-pass baseline supplied literally in the execution handoff. The pass branch is created from exactly that commit.

The active row's baseline cell remains empty during execution. The handoff carries the lease; the ledger records the historical accepted value at closure.

### 5.4 Execute

The executor first verifies:

- repository and branch identity;
- ancestry from the supplied lease;
- every post-baseline commit;
- clean/expected working tree;
- one pending pass and all later passes locked;
- current authorization and writable scope.

The pass stays `Pending` through planning, implementation, validation, review, corrections, and repeated review.

### 5.5 Review and correct

Result review compares the backlog pass, approved handoff, complete result, exact repository state, validation evidence, instructions, and review protocol. Passing tests or an executor self-review is not acceptance.

Corrections inside the same contract remain in the same pass and normally use the same branch/lease. A material scope expansion, new authority domain, unresolved design decision, insufficient allowlist, or separate rollback boundary requires roadmap revision or a new pass.

### 5.6 Close

After independent maintainer acceptance, a coordination-only closure commit records:

- historical pre-pass baseline;
- accepted result SHA, or the exact review-only `N/A` value;
- accepted tests/runs;
- reviewer;
- `Pending -> Completed`;
- checked completion box.

Later passes remain locked. The closure commit does not activate the next pass.

### 5.7 Finalize and maintain

After merge, a later commit records values that could not exist earlier, especially:

- delivering PR number;
- closure commit SHA.

Inter-pass governance/documentation/branch maintenance occurs with zero pending passes when needed. Only after finalization and maintenance is a new pass separately activated.

## 6. Why the ledger table was introduced

The ledger is a compact, immutable correlation layer across passes, handoffs, branches, results, reviews, pull requests, and later recovery.

It addresses specific ambiguity:

- Which exact repository snapshot was the input?
- Which commit contains the actual result rather than bookkeeping?
- Which review evidence was accepted?
- Who accepted it?
- Which commit performed the protected state transition?
- Was the row finalized before later work started?
- Can a future agent reconstruct the pass without the original chat?

Without the ledger, a merge commit, closure commit, branch tip, and result commit can be incorrectly treated as interchangeable.

## 7. Ledger columns and SHA roles

| Column | Meaning | Important timing rule |
|---|---|---|
| `Pass` | Stable ordered identifier | Never reused, duplicated, or silently reordered |
| `Status` | Lifecycle state | Changes only in an authorized transition commit |
| `Pre-pass baseline SHA` | Activation snapshot and execution lease | Established before branch creation; entered in ledger at closure |
| `Result SHA` | Commit containing accepted pass result | Never substitute bookkeeping unless it contains the result |
| `PR #` | Pull request delivering result/closure | Usually known after merge; explicit `N/A` is allowed |
| `Review-gate closure SHA` | Commit marking accepted completion | Cannot contain its own SHA; entered later |
| `Tests/runs` | Accepted validation and review evidence | Recorded at closure |
| `Reviewer` | Acceptance authority | Recorded at closure |

A review-only pass uses:

```text
N/A — review-only; no repository change
```

for its result rather than pretending a coordination commit was the review result.

## 8. State invariants

- At most one pass is `Pending`; zero is valid during maintenance.
- Allowed transitions are only `Locked -> Pending` and `Pending -> Completed`.
- A completed pass does not casually return to pending.
- All later passes remain locked throughout the current lifecycle.
- The execution lease exists before pass branch creation.
- Result and control-plane commits remain distinguishable.
- No commit is required to contain its own SHA.
- The next pass is activated only after the previous row is fully finalized and maintenance is complete.
- The ordered pass index is navigational only, but its displayed status must change in the same commit as the authoritative ledger status.

Any ledger/backlog/index/branch contradiction is a blocking control-plane defect, not a reason to pick whichever value seems most convenient.

## 9. W0/W1 historical exception

W0 and W1 predate the finalized reusable workflow. Their concise historical pass specifications are not rewritten simply to look like later templates.

W1 used:

- task-supplied baseline: `3a3fe364028db003bfc89d3a94fd8a9f167d1f35`;
- one approved post-baseline bookkeeping commit: `af639f43688bfd136b1dbdf051cc07bb7c588068`;
- review-only result: no repository result commit;
- closure commit: `9abed50a87fafb80157cab636fd73de018f3c5ea`;
- delivering PR: #8.

The bookkeeping commit recorded the task baseline and restored a final newline. It was not the W1 baseline or result. Early closure temporarily recorded it incorrectly as the baseline; later governance commits corrected the ledger and documented the exception.

This history is the reason current rules establish the activation commit before branch creation and delay ledger population until closure.

## 10. What Claude must not infer

Do not infer that:

- `Pending` alone means execution may begin;
- an empty pending-row baseline cell is itself an error;
- a branch with the expected name was created from the lease;
- the latest branch tip is the baseline;
- a completed pass should be reopened instead of using an authorized follow-up mechanism;
- the executor may update completion state after tests pass;
- a handoff may broaden a backlog allowlist;
- the backlog's current corrupted W2 scope may be silently repaired in an implementation task.

When state cannot be reconstructed unambiguously, the prescribed response is a maintainer-controlled governance correction before pass-specific work.
