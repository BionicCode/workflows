# Roadmap overview

## 1. Authoritative detailed source

Use these repository files for exact current contracts:

- `repository-maintenance-orchestrator-recovery-backlog.md` - project-specific ordered roadmap, current state, decisions, pass contracts, and evidence ledger;
- `backlog-workflow-documentation.md` - reusable backlog/handoff/execution/review lifecycle;
- `evidence-ledger-documentation.md` - pass states, SHA roles, ledger timing, and invariants;
- `repository-review-protocol.md` - evidence, trust, validation, start/stop, review, and protected-file rules.

This overview intentionally does not duplicate all pass criteria. The backlog is the intended owner of that detail, subject to the current integrity correction.

## 2. Program phases

### Foundation and documentation trust

- **W0:** adopt authoritative coordination files - recorded completed.
- **W1:** audit documentation authority/current state - recorded completed, but detailed result is not portable.
- **W2:** stabilize current-state documentation - displayed pending, currently blocked by corrupt scope and invalid lease/branch provenance.

### Behavior-preserving workflow naming preparation

- **W2A:** plan role-suffixed filename map and compatibility treatment.
- **W2B:** apply rename/reference migration without semantic behavior change.

The separation exists because a reusable workflow path is a public cross-repository contract.

### Restore a trustworthy current baseline

- **W3:** remove broken source-side/self-orchestration behavior and missing workflow call.
- **W4:** make the PowerShell acceptance harness bounded and deadlock-resistant.
- **W5:** establish fresh executable parser/test/schema/YAML/link evidence.

### Approve and build the central reusable package

- **W6:** plan the reusable workflow, trust, caller checkout, wrapper, package, bootstrap, and upgrade contract.
- **W7:** make Workflows the sole executable doc-metadata engine authority.
- **W8:** implement coherent init/upgrade/validate-installation packaging.

### Unify sync and doc-metadata ownership

- **W9:** one shared sync authority classifier.
- **W10:** make sync execution consume that classifier.
- **W11:** expose a closed read-only ownership plan.
- **W12:** make doc-metadata enforce exclusive canonical version authority from the plan.
- **W13:** prove two-pass cross-engine convergence in fixtures.

### Finalize product contract and certify Workflows

- **W14:** replace `documentEligibility`/broad text matching with include-minus-exclude governance.
- **W15:** implement canonical change/commit link presentation.
- **W16:** complete protected-field tamper coverage.
- **W17:** certify one immutable Workflows release-candidate SHA.

An earlier strategy review recommended moving W14 immediately after W5 to avoid building later work against an obsolete manifest contract. This was not yet adopted and should be independently reconsidered during backlog review.

### First caller migration

- **T0:** quarantine/synchronize caller documentation and old roadmap state.
- **T1:** run package init/upgrade on a non-destructive migration branch.
- **T2:** compare shared and local engines for parity.
- **T3:** switch caller orchestration to the thin wrapper.
- **T4:** prove live cross-repository convergence.
- **T5:** remove duplicated caller engine/test copies only after proof.
- **T6:** clean stale automation PR/branch state while preserving evidence.

## 3. Deferred candidates

F1-F3 are proposals, not admitted passes:

- single-boundary marker support;
- hierarchical manifest imports/provenance;
- performance and dependency hardening.

They require future admission, ordering, scope, and explicit activation. They do not currently block recovery.

## 4. Recovery completion definition

At a high level, recovery ends only when:

- Workflows contains one authoritative doc-metadata engine;
- callers no longer contain copied engine/test implementations;
- init/upgrade installs a coherent immutable package;
- wrapper/schema/docs/package identity agree;
- Workflows is passive;
- sync and doc-metadata use one authority plan/classifier and converge;
- manifest governance, links, and tamper behavior match accepted contracts;
- documentation is current and understandable;
- exact final SHAs and run evidence are recorded;
- stale automation state is resolved.

## 5. Immediate roadmap boundary

Do not plan later implementation in detail until the pre-W2 integrity review establishes:

- a trustworthy backlog;
- a real documentation authority map;
- an accepted W2 scope or revised pass structure;
- a valid execution baseline and branch;
- explicit maintainer authorization.

Later pass descriptions remain useful strategic context, not permission to work ahead.
