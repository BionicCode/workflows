# Repository Review Protocol

## 1. Purpose

This protocol defines reusable evidence, review, implementation, documentation, and stop rules for the repository-maintenance program.

Current state, decisions, ordering, and completion status belong only in `repository-maintenance-orchestrator-recovery-backlog.md`.

Neither this protocol nor the backlog authorizes edits. The current user prompt defines write authority.

## 2. Repository authority model

Before work begins, classify every repository as one of:

- **implementation authority** — owns reusable engine, tests, schema, authoritative docs, and package templates;
- **caller** — owns invocation, permissions, local manifests, orchestration, and generated wrapper;
- **canonical content source** — owns distributed file content/version;
- **target** — receives source-to-target content;
- **fixture** — disposable validation context only.

Do not infer authority from repository ancestry or naming. Authority comes from explicit approved configuration.

For the current recovery:

```text
BionicCode/workflows = implementation authority
BionicCode/template-visual-studio-repository = first caller migration
```

## 3. Evidence precedence

Use:

1. current explicit user authorization;
2. exact repository content at resolved commit;
3. live Actions jobs/logs/artifacts tied to that commit;
4. executable parser/tests tied to that commit;
5. applicable AGENTS/guardrails/instructions;
6. authoritative current product documentation;
7. backlog/review reports;
8. chat history and commit messages.

Planned or historical Markdown never overrides current code/runtime evidence.

## 4. Required state header

Record before planning or editing:

- repository full name and role;
- default branch;
- exact current HEAD;
- expected writable base SHA;
- branch/worktree state;
- applicable agent instructions;
- relevant caller/called workflow SHA;
- open PRs and automation branch SHAs;
- runtime/tool availability;
- unavailable credentials or external fixtures.

If a writable base differs from the expected SHA, stop before editing.

## 5. Session isolation

### Workflows session

When the current session is Workflows-only:

- do not edit caller repositories;
- represent caller behavior through fixtures and documented assumptions;
- do not claim complete cross-repository certification without a real external caller run;
- produce an immutable release candidate SHA before caller migration.

### Caller migration session

When the current session is caller-only:

- pin one accepted Workflows SHA;
- do not change Workflows implementation;
- stop and reopen a bounded Workflows pass when the shared engine is defective;
- do not locally patch shared behavior in the caller;
- do not retain two active roadmaps.

## 6. Base-SHA lease

Each pass has an exact base-SHA lease.

Resolve immediately before first edit and final report.

If the base moves:

- do not silently rebase;
- compare intervening changes with assumptions;
- return to Plan Mode when overlap exists;
- require maintainer approval before rebasing otherwise.

Bot branches are volatile evidence, not baselines.

## 7. Task-mode rules

### Review-only

- no file or GitHub-state changes;
- trace real call paths;
- classify findings as confirmed, risk, or unverified;
- state validation limits.

### Plan Mode

Must produce:

- public contract;
- trust model;
- file set;
- state/event/failure matrices;
- schema and migration;
- tests;
- docs;
- stop/rollback conditions;
- independent-merge rule.

Unresolved behavior becomes a maintainer decision.

### Implementation

- edit only explicit allowed files;
- stop instead of expanding scope;
- update implementation, tests, schema, package templates, examples, and focused docs together when the public contract changes;
- review complete diff;
- no push/merge/dispatch/PR mutation unless separately authorized.

## 8. Reusable-workflow rules

For cross-repository reusable workflows:

- definition files must live directly in `.github/workflows`;
- `workflow_call` is required;
- caller jobs use `owner/repo/.github/workflows/file.yml@ref`;
- production callers use a literal full commit SHA unless an explicitly approved immutable-release policy replaces it;
- expressions and contexts are not allowed in `jobs.<job_id>.uses`;
- caller permissions may be maintained or reduced, never elevated;
- called workflow `github` context and token belong to the caller;
- called workflow runners are evaluated in caller context;
- nested workflows must all be accessible;
- concurrency groups in caller and called workflow must not accidentally cancel each other.

### Authoritative implementation checkout

A reusable workflow that executes co-located scripts must check out:

```yaml
repository: ${{ job.workflow_repository }}
ref: ${{ job.workflow_sha }}
```

Do not assume the default checkout contains called-workflow implementation files.

### Caller checkouts

Keep separate paths for:

- implementation;
- trusted caller base/default state;
- caller working PR head or branch state.

Never execute code from an untrusted PR head.

## 9. Generated thin-wrapper rules

The thin wrapper is generated dependency metadata, not engine code.

It must:

- contain no implementation logic;
- contain a generated-file notice;
- contain a literal immutable Workflows ref;
- forward only documented inputs/secrets;
- be validated with YAML and GitHub Actions semantic lint;
- be updated only by init/upgrade;
- fail installation validation when its pin disagrees with package identity.

Because `uses:` cannot use expressions, do not model the wrapper as an ordinary byte-for-byte sync source with dynamic SHA substitution.

## 10. Package initialization and upgrade

A package installer must be:

- explicit;
- idempotent;
- reviewable through one PR;
- all-or-nothing for package surfaces;
- non-destructive to caller-owned configuration;
- version-consistent.

Required commands:

```text
init
upgrade
validate-installation
```

Required tests:

- empty caller;
- existing sync manifest;
- existing doc manifest;
- exact no-op rerun;
- upgrade A→B;
- conflicting wrapper;
- conflicting managed sync entry;
- malformed caller manifest;
- protected workflow path;
- default branch with slash/non-main name;
- Unicode/path safety;
- partial write rollback;
- stale package identity.

### Structural manifest edits

Never modify JSON manifests with blind text insertion.

- parse and validate;
- preserve unrelated entries;
- normalize exact managed identities;
- reject ambiguous/conflicting entries;
- emit deterministic formatting;
- validate result before write.

### Package coherence

The following must identify one engine version:

- wrapper pin;
- schema copy;
- authoritative documentation copy;
- package metadata;
- managed source refs.

Do not auto-update docs/schema beyond the pinned engine.

## 11. Sync/doc-metadata coupling boundary

Only sync interprets:

- sync manifest;
- source glob expansion;
- lifecycle;
- marker scopes;
- exact self-canonical state;
- write/version authority.

Doc-metadata consumes only a closed ownership-plan contract.

A sync internal refactor is not a doc-metadata breaking change unless the plan schema or semantics change.

Plan breaking changes require:

- schema-version increment;
- compatibility/migration rule;
- tests;
- caller docs;
- wrapper/package compatibility review.

## 12. Canonical version-authority review

Verify:

- external `enforce` skips target doc-metadata entirely;
- exact self-canonical `enforce` remains locally governable;
- existing `seed_once` is locally governable;
- missing `seed_once` is reserved;
- disabled is locally governable;
- invalid required plan causes no writes;
- local marker edits do not mutate canonical source version;
- no blacklist duplicates sync authority;
- diagnostics identify source authority.

`Version` must never be used to choose a content winner.

## 13. Documentation quality gate

Documentation is a required product surface.

Every behavior pass must review:

- workflow overview;
- manifest tutorial;
- API reference;
- type/property reference;
- schema;
- examples/templates;
- migration/troubleshooting;
- architecture decisions.

Documentation must:

- explain concepts before internals;
- identify current versus planned behavior;
- use callouts where useful;
- include valid and invalid examples;
- explain caveats and ownership;
- avoid stale implementation history in user-facing guides;
- link between overview, tutorial, API, and type pages;
- match exact schema/property names;
- be reviewed for human comprehension, not only factual completeness.

A pass is incomplete when code/tests pass but docs/schema/examples disagree.

## 14. Validation layers

### Layer A — text/syntax

- `git diff --check`;
- JSON parse;
- JSON Schema validation;
- YAML 1.2-safe parse;
- PowerShell parser;
- Python compile/import;
- Markdown link check.

### Layer B — semantic static tooling

- `actionlint` or equivalent;
- language lint/type checks;
- closed-schema tests;
- permission/trigger matrix.

Plain YAML parsing is not Actions semantic validation.

### Layer C — executable unit/acceptance

Record exact command, runtime version, commit, timeout, skipped cases, and result.

A spawned-process suite counts only when output is fully drained and processes are bounded.

### Layer D — package fixtures

Run init, no-op init, upgrade, conflict, rollback, and validation fixtures against clean temporary caller trees.

### Layer E — live Actions

Inspect run/attempt, caller and called workflow SHA, checkout identities, permissions, jobs, logs, outputs, artifacts, branch/PR result.

### Layer F — cross-repository certification

Use a real external caller. A same-repository self-call is necessary but not sufficient to prove external access and caller repair behavior.

### Layer G — convergence

Run the complete engine sequence twice. The second pass must be no-op.

## 15. Test-harness requirements

Child-process harnesses must:

- drain stdout/stderr concurrently;
- use finite timeouts;
- terminate timed-out process trees where supported;
- report command, timeout, exit code, and captured output;
- emit START before blocking;
- clean temporary repositories in `finally`;
- avoid sleep-based synchronization where deterministic signaling exists.

## 16. Test-quality review

Inspect whether tests:

- prove public behavior;
- include positive/negative/boundary/failure cases;
- cover false positives and false negatives;
- use non-governed unrelated fixtures;
- preserve no-write-on-failure;
- prove idempotence;
- prove package coherence;
- prove exact SHA pinning;
- prove authority/lifecycle matrix;
- localize hangs;
- avoid weakening assertions to current broken output.

An unrelated defect unlocks a separate pass; it does not expand the current pass.

## 17. Security and trust review

For every workflow/package pass, review:

- minimum permissions;
- caller versus implementation token authority;
- fork behavior;
- trusted/untrusted checkout;
- secrets propagation;
- script injection;
- mutable action references;
- workflow-file write permissions;
- `GITHUB_TOKEN` follow-up trigger limitations;
- branch protection;
- force-with-lease behavior;
- path traversal/symlinks;
- UTF-8 and newline assumptions;
- partial writes and rollback;
- concurrency and stale-run races;
- dependency pinning.

## 18. Required review output

Return:

1. Verdict.
2. Resolved repositories, roles, branches, and SHAs.
3. Scope check.
4. Contract check.
5. Findings with file/line and classification.
6. Validation commands, versions, runs, results, and limitations.
7. Test-quality assessment.
8. Documentation/schema/package assessment.
9. Trust/security assessment.
10. Diff self-review.
11. Stop-condition check.
12. Files changed.
13. GitHub state changed.
14. Exact next unlocked pass.

## 19. Completion standard

A pass completes only when:

- exact base and result SHAs are recorded;
- scope is exact;
- public contract is satisfied;
- required tests and semantic validation pass;
- package/schema/docs/examples agree;
- trust and ownership are reviewed;
- no stop condition occurred;
- maintainer accepts the review gate;
- backlog evidence ledger is updated.

Unavailable evidence remains explicitly unverified.

## 20. Protected control-plane files

The following files are read-only by default because they define agent behavior, review authority, repository policy, or roadmap state:

* root and nested `AGENTS.md`;
* root and nested `AGENTS.override.md`;
* `AGENT_GUARDRAILS.md`;
* `.github/copilot-instructions.md`;
* `.github/instructions/**/*.instructions.md`;
* root `DOCUMENTATION.md` when it defines mandatory documentation policy;
* `repository-maintenance-orchestrator-recovery-backlog.md`;
* `repository-review-protocol.md`;
* `.github/CODEOWNERS`, when present.

A task may modify one of these files only when the current user prompt:

1. names the exact file path;
2. explicitly authorizes that file to be changed;
3. states the intended governance or coordination change.

Broad instructions such as “update documentation,” “update all references,” “keep documentation consistent,” or “complete the backlog pass” do not authorize modification of protected control-plane files.

When implementation makes a protected file inaccurate, the agent must:

* leave the protected file unchanged;
* report the exact inconsistency;
* identify the affected path and section;
* propose the required wording in the final handoff;
* stop if continuing would make repository instructions materially contradictory.

Backlog checkboxes, evidence records, pass statuses, and pass unlocking remain maintainer-controlled even when the implementation itself is complete.
