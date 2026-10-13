---
Version: 1
Created: 2026-10-13T20:27:24+00:00
Updated: 2026-10-13T20:27:24+00:00
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

# Agent instruction package architecture

## Installed structure and ownership

`AGENTS.md` is the root router. `.agent/README.md` is the index;
`.agent/instructions/README.md` is the adopter landing page. Exactly seven canonical
modules live under `.agent/instructions/package/`: ENGINEERING, IMPLEMENTATION,
CODE_REVIEW, DOTNET, TESTING, GUARDRAILS and DOCUMENTATION. Their optional exact
companions live under `.agent/instructions/custom/`; only meaningful companions exist.
There is no mixed-ownership REPOSITORY file or repository-specific fence in package policy.

The publisher owns shared source files and enforced installed copies. Repository
owners own custom/native/local instructions and operational REVIEW independently.
Generic optional adapters occupy root CLAUDE and the three native Copilot locations.
Publisher discovery configuration and source-maintenance overrides are never deployed.

## Routing and precedence

The [root router](../../../../AGENTS.md) contains complete activation categories and
explicit paths. Routes are additive and ordered ENGINEERING, IMPLEMENTATION,
CODE_REVIEW, DOTNET, TESTING, GUARDRAILS, DOCUMENTATION. Paths resolve from repository
root even for nested startup. Read each selected package module and companion before
dependent work. Missing selected package files are an integrity failure; optional
companions may be absent. Apply package < matching custom < applicable native nested
guidance, subject to higher-priority instructions and mandatory ownership/routing.

Formal review, including `<review>`, is distinct from implementation planning,
analysis and implementation self-review. Relevant .NET/C#/Visual Studio and testing
routes do not depend on directory location. TESTING remains language-independent;
.NET-specific async and test-project rules live in DOTNET.

## Source-to-target declarations

The passive declaration uses schema_version 1, source_to_target, whole_file,
uniqueness_policy none, source_repo BionicCode/workflows and source_ref main.
Every source selector includes deployment/packages/agent-package/.

| Source relative to package | Installed target | Lifecycle |
|---|---|---|
| README.md | .agent/README.md | enforce |
| instruction-package/**/* | .agent/** preserving the subtree | enforce, recursive and hidden files included |
| REVIEW.md | .agent/REVIEW.md | seed_once |
| bridges/claude/CLAUDE.md | CLAUDE.md | optional seed_once |
| bridges/copilot/copilot-instructions.md | .github/copilot-instructions.md | optional enforce |
| bridges/copilot/instructions/dotnet.instructions.md | .github/instructions/dotnet.instructions.md | optional enforce |
| bridges/copilot/instructions/test.instructions.md | .github/instructions/test.instructions.md | optional enforce |
| AGENTS.md | AGENTS.md | enforce; materialize last |

The Claude group is one declaration; the Copilot group is three declarations.
Source and target basenames match the existing engine. Registration is a template
for a future installer, not a complete adopter manifest or active self-registration.

## Lifecycle, compatibility and opt-out

Install index, instruction landing page and package dependencies before entrypoints.
Preserve meaningful legacy policy in local companions before replacing native files.
Preserve an existing operational REVIEW and seeded Claude customizations. Fresh REVIEW
uses the stable empty seed, never publisher findings. CODE_REVIEW and its companion
own identifier allocation and Log maintenance; the mutable document does not own policy.

Whole-file enforced subscription refreshes complete publisher-owned files. Recursive
expansion only adds or updates members; it does not prune missing members or local files.
Removing/disabling registration opts out without deletion. Split a glob into complete,
non-overlapping declarations for individual opt-out. External old manifests must not
be redirected to a dependent router without a separately authorized migration.

Interrupted manual installation is not transactional. Keep the old operative router
until required dependencies exist. A router missing a selected module stops dependent
work. Native client discovery is version/configuration-dependent; static package
validation does not establish client behavior or model compliance.

## Metadata

Finalize metadata at publisher sources before copying bytes to enforced installations.
Do not independently update metadata on installed enforced files. Custom companions
have independent repository metadata ownership. Source REVIEW, operational REVIEW and
the minimal Claude bridges are excluded from automated metadata mutation.
