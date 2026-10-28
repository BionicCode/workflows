# Managed Package Platform — Evidence Ledger

This project-owned ledger is the sole mutable authority for pass lifecycle state and accepted execution/review evidence in the default lane. Stable identities, titles, order, dependencies and pass contracts belong to the [project backlog](backlog.md).

Apply all transitions, SHA population, review, finalization and start gates from the installed [evidence-ledger protocol](evidence-ledger-protocol.md), [review protocol](review-protocol.md) and [Backlog Workflow](backlog-workflow.md). This ledger does not independently authorize changes.

One independently governed evidence ledger defines one strictly ordered lifecycle lane. At most one pass may be `Pending` in this lane, and zero pending passes is valid. No additional lane is admitted by the project backlog. Parallel execution would require separately governed ledger state plus backlog-defined paths, authority boundaries, dependencies and integration order; no generic filename is assumed.

> [!IMPORTANT]
> Governance workspace installation and this initialization are not accepted MP pass results. Every admitted pass starts `Locked` with empty evidence cells. A pre-activation handoff and separate authorization, activation, actual execution lease, readiness gate and execution directive are required before pass-specific work.

| Pass | Status | Pre-pass baseline SHA | Result SHA | PR # | Review-gate closure SHA | Tests/runs | Reviewer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MP00 | Locked | | | | | | |
| MP01 | Locked | | | | | | |
| MP02 | Locked | | | | | | |
| MP03 | Locked | | | | | | |
| MP04 | Locked | | | | | | |
| MP05 | Locked | | | | | | |
| MP06 | Locked | | | | | | |
| MP07 | Locked | | | | | | |
| MP08 | Locked | | | | | | |
| MP09 | Locked | | | | | | |
| MP10 | Locked | | | | | | |
| MP11 | Locked | | | | | | |
| MP12 | Locked | | | | | | |
| MP13 | Locked | | | | | | |
| MP14 | Locked | | | | | | |
| MP15 | Locked | | | | | | |
| MP16 | Locked | | | | | | |
| MP17 | Locked | | | | | | |
| MP18 | Locked | | | | | | |
| MP19 | Locked | | | | | | |
| MP20 | Locked | | | | | | |
| MP21 | Locked | | | | | | |
| MP22 | Locked | | | | | | |
| MP23 | Locked | | | | | | |
| MP24 | Locked | | | | | | |
| MP25 | Locked | | | | | | |
| MP26 | Locked | | | | | | |
| MP27 | Locked | | | | | | |
| MP28 | Locked | | | | | | |
| MP29 | Locked | | | | | | |
| MP30 | Locked | | | | | | |
| MP31 | Locked | | | | | | |
| MP32 | Locked | | | | | | |
| MP33 | Locked | | | | | | |
| MP34 | Locked | | | | | | |
| MP35 | Locked | | | | | | |
| MP36 | Locked | | | | | | |

Allowed lifecycle states are `Locked`, `Pending` and `Completed`. Do not duplicate their mutable values in the backlog.

Populate accepted baseline/result/review evidence only at the timing required by the installed protocols. In particular, the baseline cell stays empty at activation; the closure commit cannot contain its own SHA, and closure-SHA/PR fields receive their prescribed delayed finalization. Do not prefill review-only `N/A` values before acceptance.

Completing a pass does not activate its successor. Required predecessor evidence and reachability must be fully finalized before a later pass becomes eligible for its own separately authorized activation.
