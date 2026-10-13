---
Version: 1
Created: 2026-10-13T20:27:25+00:00
Updated: 2026-10-13T20:27:25+00:00
Author: BionicCode
---
<!-- doc-metadata-presentation:start -->
<details>
<summary>Change History</summary>


</details>

---

<br>
<br>
<!-- doc-metadata-presentation:end -->

# Using the agent instruction package

The repository-root [AGENTS router](../../AGENTS.md) selects explicit package/custom
pairs in the order ENGINEERING, IMPLEMENTATION, CODE_REVIEW, DOTNET, TESTING,
GUARDRAILS, DOCUMENTATION. ENGINEERING always applies; all other matching routes
combine, including relevant planning and read-only work. Missing selected modules
stop dependent work. Missing custom companions are normal.

## Customize without mixing ownership

Create a meaningful `custom/<MODULE>.md` for the corresponding `package/<MODULE>.md`.
Read package first, then that exact companion. Companions may add, refine or explicitly
override their matching module, followed by applicable native nested instructions.
System/user instructions and mandatory routing/ownership remain binding. Do not add
empty companions, repository-specific fences to package files, or a parallel framework.
Custom companions and legitimate native/client-local files are independently owned.

## Synchronization and lifecycle

The router, this README, the package subtree and package index are whole-file enforced
while subscribed. Optional Copilot adapters are enforced when selected. REVIEW and
the optional Claude bridge use `seed_once`: existing local content is preserved.
The [review seed/state boundary](../../.agent/REVIEW.md) is independent of formal
review policy in [CODE_REVIEW](package/CODE_REVIEW.md).

Recursive synchronization is additive: newly declared source members are copied,
but removed members, custom companions and unrelated target files are never pruned.
Disabling/removing registration ends upstream ownership without deleting installed
files. Opting out one file within a glob requires non-overlapping declarations;
an overlapping disabled entry is not a per-file override.

An old external manifest stays on its existing sources until separately migrated.
No installer, automatic registration merge, external migration or CI integration is
provided by this passive package. Install dependencies before bridges and the router;
an interrupted installation has no all-or-nothing guarantee.

See the [architecture](package/docs/ARCHITECTURE.md) for the complete consumer contract.
