---
Version: 1
Created: 2026-10-13T20:27:23+00:00
Updated: 2026-10-13T20:27:23+00:00
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

# Workflows agent-package migration

## Baseline and conservation

Clean main tracking origin/main; baseline `d820fda78405c924e6fa969221697d08fb59f427`. Shared seven-module bodies were preserved from template partition `257f280e4e79faf7c94314711738c6a790ffe693`, with only approved routing, ownership, link, REVIEW-policy and language-boundary corrections. No external template was edited.

| Legacy file | Baseline worktree SHA256 | Git blob SHA256 |
|---|---|---|
| `AGENTS.md` | `55e860cc960e743f980b8b503f5832400bdb8d1dd2da01cab485cc0ba2246c38` | `9669fa43dba0729778c15215a4bf798341f61e5fac79a04c8a2c6e01a69ed93f` |
| `AGENT_GUARDRAILS.md` | `3df3ae3cc454a407ba6bc93cd63593e9f3b7fba808af2b2296e6ab233813853b` | `632376bc9af8d67081066d30eb29823337e484a6e61402ec4e99dac87e6f21dd` |
| `DOCUMENTATION.md` | `b381187e034d80f785469d05a708223f71330d1fab7baa9a46f707f316181823` | `09d45df6a38ce31a37fe5475b42a720eeff08f319c426b9ee0f6090861941e75` |
| `test/AGENTS.md` | `fa8f414dfa6785f7b481f8d4fa2eadcc35dd4c0c1743f1ba30aa5614f8311c1e` | `a5596a7a299e183043b1c50b81480127f5daf4db508253872e2eae71805b2e46` |
| `CLAUDE.md` | `64f964a6260a5cb06d2c2e96dba133b3c6124afe270a1704ffd898ed8b6da6a2` | `64f964a6260a5cb06d2c2e96dba133b3c6124afe270a1704ffd898ed8b6da6a2` |
| `CLAUDE.local.md` | `5640064bd3ea8790713336cab1fd4d8d3f729dee2eedca0e95c0d6ee664a018d` | `5640064bd3ea8790713336cab1fd4d8d3f729dee2eedca0e95c0d6ee664a018d` |
| `.github/copilot-instructions.md` | `2d174fbb8d913f5518cef8b1d12cb42ca09e803149f19ae9084fe33f626dd988` | `aac05a7a6c7e4139cfd824fe74e728525119b1e726df00d8f023738f65dccd66` |
| `.github/instructions/dotnet.instructions.md` | `50bbbdc2de9e431adc5547076e5ae56f19c2a0a1aa979a98850b62181ea4e741` | `032723c5757b7be3ffc30bb9ee5241f9f36879fb65f2281c78c91ab72da203cc` |
| `.github/instructions/test.instructions.md` | `f40a7bcad500de4ebf1fc05ab4a41242ea52d9600d0b2fabb97e2cda6fc59fc6` | `bdb1140df247b64b5ab130ee95fac753e5554b0c308559e67415e1b1a057b4c5` |

Every group below is identified by its original heading and occurrence. Metadata presentation and empty template placeholders are not policy. Classification is one of shared policy, repository-wide custom policy, path-specific native policy, client-local policy, or superseded routing/duplicates.

| Group | Source / heading | Classification | Destination / rationale |
|---|---|---|---|
| G001 | `AGENTS.md` / AGENTS.md (Version 3.2) | shared policy | Preserve in `.agent/instructions/package/ENGINEERING.md`; client duplicates route through thin adapters. |
| G002 | `AGENTS.md` / Guardrail Routing | superseded routing/duplicates | Root `AGENTS.md` preserves scope, read-only mode and explicit additive routing; duplicate policy bodies are in canonical modules. |
| G003 | `AGENTS.md` / Scope and Precedence | superseded routing/duplicates | Root `AGENTS.md` preserves scope, read-only mode and explicit additive routing; duplicate policy bodies are in canonical modules. |
| G004 | `AGENTS.md` / Core Engineering Standards | shared policy | Preserve in `.agent/instructions/package/ENGINEERING.md`; client duplicates route through thin adapters. |
| G005 | `AGENTS.md` / Scope Discovery and Routing | shared policy | Preserve in `.agent/instructions/package/ENGINEERING.md`; client duplicates route through thin adapters. |
| G006 | `AGENTS.md` / Task Modes | superseded routing/duplicates | Root `AGENTS.md` preserves scope, read-only mode and explicit additive routing; duplicate policy bodies are in canonical modules. |
| G007 | `AGENTS.md` / Review-only mode | superseded routing/duplicates | Root `AGENTS.md` preserves scope, read-only mode and explicit additive routing; duplicate policy bodies are in canonical modules. |
| G008 | `AGENTS.md` / Implementation mode | superseded routing/duplicates | Root `AGENTS.md` preserves scope, read-only mode and explicit additive routing; duplicate policy bodies are in canonical modules. |
| G009 | `AGENTS.md` / Planning and Execution | shared policy | Preserve in `.agent/instructions/package/ENGINEERING.md`; client duplicates route through thin adapters. |
| G010 | `AGENTS.md` / File System and Project Structure | shared policy | Preserve in `.agent/instructions/package/ENGINEERING.md`; client duplicates route through thin adapters. |
| G011 | `AGENTS.md` / Validation Expectations | shared policy | Preserve in `.agent/instructions/package/IMPLEMENTATION.md`; client duplicates route through thin adapters. |
| G012 | `AGENTS.md` / Completion and Self-Review Requirements | shared policy | Preserve in `.agent/instructions/package/IMPLEMENTATION.md`; client duplicates route through thin adapters. |
| G013 | `AGENTS.md` / Documentation Is Part of Done | shared policy | Preserve in `.agent/instructions/package/IMPLEMENTATION.md`; client duplicates route through thin adapters. |
| G014 | `AGENTS.md` / Testing Standards | shared policy | Preserve in `.agent/instructions/package/IMPLEMENTATION.md`; client duplicates route through thin adapters. |
| G015 | `AGENTS.md` / Analyzer and Style Compliance | shared policy | Preserve in `.agent/instructions/package/ENGINEERING.md`; client duplicates route through thin adapters. |
| G016 | `AGENTS.md` / Documentation and Comments | shared policy | Preserve in `.agent/instructions/package/DOCUMENTATION.md`; client duplicates route through thin adapters. |
| G017 | `AGENTS.md` / Default Review Mission | shared policy | Preserve in `.agent/instructions/package/CODE_REVIEW.md`; client duplicates route through thin adapters. |
| G018 | `AGENTS.md` / Review Priorities | shared policy | Preserve in `.agent/instructions/package/CODE_REVIEW.md`; client duplicates route through thin adapters. |
| G019 | `AGENTS.md` / Required Review Method | shared policy | Preserve in `.agent/instructions/package/CODE_REVIEW.md`; client duplicates route through thin adapters. |
| G020 | `AGENTS.md` / Review Output Format | shared policy | Preserve in `.agent/instructions/package/CODE_REVIEW.md`; client duplicates route through thin adapters. |
| G021 | `AGENTS.md` / Required Review Sections | shared policy | Preserve in `.agent/instructions/package/CODE_REVIEW.md`; client duplicates route through thin adapters. |
| G022 | `AGENTS.md` / Stop / Uncertainty Rules | shared policy | Preserve in `.agent/instructions/package/CODE_REVIEW.md`; client duplicates route through thin adapters. |
| G023 | `AGENTS.md` / Implementation Completion Report | shared policy | Preserve in `.agent/instructions/package/IMPLEMENTATION.md`; client duplicates route through thin adapters. |
| G024 | `AGENTS.md` / Change and Review Style | shared policy | Preserve in `.agent/instructions/package/ENGINEERING.md`; client duplicates route through thin adapters. |
| G025 | `AGENTS.md` / Commit and Pull Request Guidance | shared policy | Preserve in `.agent/instructions/package/IMPLEMENTATION.md`; client duplicates route through thin adapters. |
| G026 | `AGENTS.md` / Keep This File Focused | shared policy | Preserve in `.agent/instructions/package/GUARDRAILS.md`; client duplicates route through thin adapters. |
| G027 | `AGENTS.md` / Repository Specifics | superseded routing/duplicates | Remove empty template placeholders/markers; retain concrete local facts and handoff/protection policy in meaningful custom companions. |
| G028 | `AGENTS.md` / Implementation-pass review handoff | repository-wide custom policy | Preserve complete handoff, Git authorization and exact-path artifact requirements in custom IMPLEMENTATION. |
| G029 | `AGENTS.md` / Protected repository control plane | repository-wide custom policy | Preserve governance and maintainer-only state rules in custom GUARDRAILS; replace retired path references with exact new surfaces. |
| G030 | `AGENTS.md` / Solution and Structure | repository-wide custom policy | Facts → custom ENGINEERING, TESTING and DOCUMENTATION; remove placeholders rather than invent values. |
| G031 | `AGENTS.md` / Build and Validation | superseded routing/duplicates | Remove empty template placeholders/markers; retain concrete local facts and handoff/protection policy in meaningful custom companions. |
| G032 | `AGENTS.md` / Repository Conventions | superseded routing/duplicates | Remove empty template placeholders/markers; retain concrete local facts and handoff/protection policy in meaningful custom companions. |
| G033 | `AGENTS.md` / Optional Specialized Instruction Files | superseded routing/duplicates | Remove empty template placeholders/markers; retain concrete local facts and handoff/protection policy in meaningful custom companions. |
| G034 | `AGENT_GUARDRAILS.md` / AGENT_GUARDRAILS.md | shared policy | Preserve in `.agent/instructions/package/GUARDRAILS.md`; client duplicates route through thin adapters. |
| G035 | `AGENT_GUARDRAILS.md` / Purpose | shared policy | Preserve in `.agent/instructions/package/GUARDRAILS.md`; client duplicates route through thin adapters. |
| G036 | `AGENT_GUARDRAILS.md` / When to read this file | shared policy | Preserve in `.agent/instructions/package/GUARDRAILS.md`; client duplicates route through thin adapters. |
| G037 | `AGENT_GUARDRAILS.md` / Non-negotiable repository guardrails | shared policy | Preserve in `.agent/instructions/package/GUARDRAILS.md`; client duplicates route through thin adapters. |
| G038 | `AGENT_GUARDRAILS.md` / Protected instruction surfaces | shared policy | Preserve in `.agent/instructions/package/GUARDRAILS.md`; client duplicates route through thin adapters. |
| G039 | `AGENT_GUARDRAILS.md` / Public contract consistency | shared policy | Preserve in `.agent/instructions/package/GUARDRAILS.md`; client duplicates route through thin adapters. |
| G040 | `AGENT_GUARDRAILS.md` / Path, file, and security guardrails | shared policy | Preserve in `.agent/instructions/package/GUARDRAILS.md`; client duplicates route through thin adapters. |
| G041 | `AGENT_GUARDRAILS.md` / Schema and configuration guardrails | shared policy | Preserve in `.agent/instructions/package/GUARDRAILS.md`; client duplicates route through thin adapters. |
| G042 | `AGENT_GUARDRAILS.md` / Build and dependency guardrails | shared policy | Preserve in `.agent/instructions/package/GUARDRAILS.md`; client duplicates route through thin adapters. |
| G043 | `AGENT_GUARDRAILS.md` / Test guardrails | shared policy | Preserve in `.agent/instructions/package/GUARDRAILS.md`; client duplicates route through thin adapters. |
| G044 | `AGENT_GUARDRAILS.md` / Documentation guardrails | shared policy | Preserve in `.agent/instructions/package/GUARDRAILS.md`; client duplicates route through thin adapters. |
| G045 | `AGENT_GUARDRAILS.md` / Completion report checklist | shared policy | Preserve in `.agent/instructions/package/GUARDRAILS.md`; client duplicates route through thin adapters. |
| G046 | `DOCUMENTATION.md` / DOCUMENTATION.md | shared policy | Preserve in `.agent/instructions/package/DOCUMENTATION.md`; client duplicates route through thin adapters. |
| G047 | `DOCUMENTATION.md` / Purpose | shared policy | Preserve in `.agent/instructions/package/DOCUMENTATION.md`; client duplicates route through thin adapters. |
| G048 | `DOCUMENTATION.md` / Documentation layers | shared policy | Preserve in `.agent/instructions/package/DOCUMENTATION.md`; client duplicates route through thin adapters. |
| G049 | `DOCUMENTATION.md` / 1) Source comments inside code | shared policy | Preserve in `.agent/instructions/package/DOCUMENTATION.md`; client duplicates route through thin adapters. |
| G050 | `DOCUMENTATION.md` / 2) XML documentation comments for APIs | shared policy | Preserve in `.agent/instructions/package/DOCUMENTATION.md`; client duplicates route through thin adapters. |
| G051 | `DOCUMENTATION.md` / 3) Markdown documentation files | shared policy | Preserve in `.agent/instructions/package/DOCUMENTATION.md`; client duplicates route through thin adapters. |
| G052 | `DOCUMENTATION.md` / Choosing the right level | shared policy | Preserve in `.agent/instructions/package/DOCUMENTATION.md`; client duplicates route through thin adapters. |
| G053 | `DOCUMENTATION.md` / Documentation is part of done | shared policy | Preserve in `.agent/instructions/package/DOCUMENTATION.md`; client duplicates route through thin adapters. |
| G054 | `test/AGENTS.md` / AGENTS.md | shared policy | Preserve in `.agent/instructions/package/TESTING.md`; client duplicates route through thin adapters. |
| G055 | `test/AGENTS.md` / Purpose | shared policy | Preserve in `.agent/instructions/package/TESTING.md`; client duplicates route through thin adapters. |
| G056 | `test/AGENTS.md` / Test Philosophy | shared policy | Preserve in `.agent/instructions/package/TESTING.md`; client duplicates route through thin adapters. |
| G057 | `test/AGENTS.md` / Test Scope and Failure Discipline | shared policy | Preserve in `.agent/instructions/package/TESTING.md`; client duplicates route through thin adapters. |
| G058 | `test/AGENTS.md` / Independence and Isolation | shared policy | Preserve in `.agent/instructions/package/TESTING.md`; client duplicates route through thin adapters. |
| G059 | `test/AGENTS.md` / Naming Conventions | shared policy | Preserve in `.agent/instructions/package/TESTING.md`; client duplicates route through thin adapters. |
| G060 | `test/AGENTS.md` / Test Structure | shared policy | Preserve in `.agent/instructions/package/TESTING.md`; client duplicates route through thin adapters. |
| G061 | `test/AGENTS.md` / Assertions and Expected Outcomes | shared policy | Preserve in `.agent/instructions/package/TESTING.md`; client duplicates route through thin adapters. |
| G062 | `test/AGENTS.md` / Parameterized Tests and Data | shared policy | Preserve in `.agent/instructions/package/TESTING.md`; client duplicates route through thin adapters. |
| G063 | `test/AGENTS.md` / Test Logic and Readability | shared policy | Preserve in `.agent/instructions/package/TESTING.md`; client duplicates route through thin adapters. |
| G064 | `test/AGENTS.md` / Test Doubles | shared policy | Preserve in `.agent/instructions/package/TESTING.md`; client duplicates route through thin adapters. |
| G065 | `test/AGENTS.md` / Async and Time-Sensitive Tests | shared policy | Generic async/timing rules → TESTING; Task/Task<T>/async void → DOTNET; no language-specific rule is lost. |
| G066 | `test/AGENTS.md` / What Not to Test Directly | shared policy | Preserve in `.agent/instructions/package/TESTING.md`; client duplicates route through thin adapters. |
| G067 | `test/AGENTS.md` / Organization Under `test/` | shared policy | Generic layout rules → TESTING (existing layout first); .NET generated project naming → DOTNET; workflows test roots → custom TESTING. |
| G068 | `test/AGENTS.md` / Validation and Reporting | shared policy | Preserve in `.agent/instructions/package/TESTING.md`; client duplicates route through thin adapters. |
| G069 | `test/AGENTS.md` / Review Priorities for Test Code | shared policy | Preserve in `.agent/instructions/package/TESTING.md`; client duplicates route through thin adapters. |
| G070 | `CLAUDE.md` / Claude Code project routing | repository-wide custom policy | Identity → custom ENGINEERING; every recovery routing, W1/W2 integrity, current-authorization, evidence, passive-context, inert user-prompt and Archive activation group → custom GUARDRAILS. Generic @AGENTS.md import → Claude bridge. |
| G071 | `CLAUDE.local.md` / passive context import | client-local policy | Retain `CLAUDE.local.md` byte-for-byte; its valid @import remains repository-local. |
| G072 | `.github/copilot-instructions.md` / copilot-instructions.md (Version 3.2) | shared policy | Preserve in `.agent/instructions/package/ENGINEERING.md`; client duplicates route through thin adapters. |
| G073 | `.github/copilot-instructions.md` / Scope and Precedence | superseded routing/duplicates | Root `AGENTS.md` preserves scope, read-only mode and explicit additive routing; duplicate policy bodies are in canonical modules. |
| G074 | `.github/copilot-instructions.md` / Core Engineering Standards | shared policy | Preserve in `.agent/instructions/package/ENGINEERING.md`; client duplicates route through thin adapters. |
| G075 | `.github/copilot-instructions.md` / Scope Discovery and Routing | shared policy | Preserve in `.agent/instructions/package/ENGINEERING.md`; client duplicates route through thin adapters. |
| G076 | `.github/copilot-instructions.md` / Task Modes | superseded routing/duplicates | Root `AGENTS.md` preserves scope, read-only mode and explicit additive routing; duplicate policy bodies are in canonical modules. |
| G077 | `.github/copilot-instructions.md` / Review-only mode | superseded routing/duplicates | Root `AGENTS.md` preserves scope, read-only mode and explicit additive routing; duplicate policy bodies are in canonical modules. |
| G078 | `.github/copilot-instructions.md` / Implementation mode | superseded routing/duplicates | Root `AGENTS.md` preserves scope, read-only mode and explicit additive routing; duplicate policy bodies are in canonical modules. |
| G079 | `.github/copilot-instructions.md` / Planning and Execution | shared policy | Preserve in `.agent/instructions/package/ENGINEERING.md`; client duplicates route through thin adapters. |
| G080 | `.github/copilot-instructions.md` / File System and Project Structure | shared policy | Preserve in `.agent/instructions/package/ENGINEERING.md`; client duplicates route through thin adapters. |
| G081 | `.github/copilot-instructions.md` / Validation Expectations | shared policy | Preserve in `.agent/instructions/package/IMPLEMENTATION.md`; client duplicates route through thin adapters. |
| G082 | `.github/copilot-instructions.md` / Completion and Self-Review Requirements | shared policy | Preserve in `.agent/instructions/package/IMPLEMENTATION.md`; client duplicates route through thin adapters. |
| G083 | `.github/copilot-instructions.md` / Documentation Is Part of Done | shared policy | Preserve in `.agent/instructions/package/IMPLEMENTATION.md`; client duplicates route through thin adapters. |
| G084 | `.github/copilot-instructions.md` / Testing Standards | shared policy | Preserve in `.agent/instructions/package/IMPLEMENTATION.md`; client duplicates route through thin adapters. |
| G085 | `.github/copilot-instructions.md` / Analyzer and Style Compliance | shared policy | Preserve in `.agent/instructions/package/ENGINEERING.md`; client duplicates route through thin adapters. |
| G086 | `.github/copilot-instructions.md` / Documentation and Comments | shared policy | Preserve in `.agent/instructions/package/DOCUMENTATION.md`; client duplicates route through thin adapters. |
| G087 | `.github/copilot-instructions.md` / Default Review Mission | shared policy | Preserve in `.agent/instructions/package/CODE_REVIEW.md`; client duplicates route through thin adapters. |
| G088 | `.github/copilot-instructions.md` / Review Priorities | shared policy | Preserve in `.agent/instructions/package/CODE_REVIEW.md`; client duplicates route through thin adapters. |
| G089 | `.github/copilot-instructions.md` / Required Review Method | shared policy | Preserve in `.agent/instructions/package/CODE_REVIEW.md`; client duplicates route through thin adapters. |
| G090 | `.github/copilot-instructions.md` / Review Output Format | shared policy | Preserve in `.agent/instructions/package/CODE_REVIEW.md`; client duplicates route through thin adapters. |
| G091 | `.github/copilot-instructions.md` / Required Review Sections | shared policy | Preserve in `.agent/instructions/package/CODE_REVIEW.md`; client duplicates route through thin adapters. |
| G092 | `.github/copilot-instructions.md` / Stop / Uncertainty Rules | shared policy | Preserve in `.agent/instructions/package/CODE_REVIEW.md`; client duplicates route through thin adapters. |
| G093 | `.github/copilot-instructions.md` / Implementation Completion Report | shared policy | Preserve in `.agent/instructions/package/IMPLEMENTATION.md`; client duplicates route through thin adapters. |
| G094 | `.github/copilot-instructions.md` / Change and Review Style | shared policy | Preserve in `.agent/instructions/package/ENGINEERING.md`; client duplicates route through thin adapters. |
| G095 | `.github/copilot-instructions.md` / Commit and Pull Request Guidance | shared policy | Preserve in `.agent/instructions/package/IMPLEMENTATION.md`; client duplicates route through thin adapters. |
| G096 | `.github/copilot-instructions.md` / Keep This File Focused | shared policy | Preserve in `.agent/instructions/package/GUARDRAILS.md`; client duplicates route through thin adapters. |
| G097 | `.github/copilot-instructions.md` / Repository Specifics | superseded routing/duplicates | Remove empty template placeholders/markers; retain concrete local facts and handoff/protection policy in meaningful custom companions. |
| G098 | `.github/copilot-instructions.md` / Solution and Structure | shared policy | Preserve in `.agent/instructions/package/ENGINEERING.md`; client duplicates route through thin adapters. |
| G099 | `.github/copilot-instructions.md` / Build and Validation | superseded routing/duplicates | Remove empty template placeholders/markers; retain concrete local facts and handoff/protection policy in meaningful custom companions. |
| G100 | `.github/copilot-instructions.md` / Repository Conventions | superseded routing/duplicates | Remove empty template placeholders/markers; retain concrete local facts and handoff/protection policy in meaningful custom companions. |
| G101 | `.github/copilot-instructions.md` / Optional Specialized Instruction Files | superseded routing/duplicates | Remove empty template placeholders/markers; retain concrete local facts and handoff/protection policy in meaningful custom companions. |
| G102 | `.github/instructions/dotnet.instructions.md` / dotnet.instructions.md | shared policy | Preserve in `.agent/instructions/package/DOTNET.md`; client duplicates route through thin adapters. |
| G103 | `.github/instructions/dotnet.instructions.md` / Scope | shared policy | Preserve in `.agent/instructions/package/DOTNET.md`; client duplicates route through thin adapters. |
| G104 | `.github/instructions/dotnet.instructions.md` / Repository contract files | shared policy | Preserve in `.agent/instructions/package/DOTNET.md`; client duplicates route through thin adapters. |
| G105 | `.github/instructions/dotnet.instructions.md` / Command policy | shared policy | Preserve in `.agent/instructions/package/DOTNET.md`; client duplicates route through thin adapters. |
| G106 | `.github/instructions/dotnet.instructions.md` / .editorconfig and analyzer compliance | shared policy | Preserve in `.agent/instructions/package/DOTNET.md`; client duplicates route through thin adapters. |
| G107 | `.github/instructions/dotnet.instructions.md` / Naming and readability expectations | shared policy | Preserve in `.agent/instructions/package/DOTNET.md`; client duplicates route through thin adapters. |
| G108 | `.github/instructions/dotnet.instructions.md` / Design expectations for .NET code | shared policy | Preserve in `.agent/instructions/package/DOTNET.md`; client duplicates route through thin adapters. |
| G109 | `.github/instructions/dotnet.instructions.md` / Documentation expectations | shared policy | Preserve in `.agent/instructions/package/DOTNET.md`; client duplicates route through thin adapters. |
| G110 | `.github/instructions/dotnet.instructions.md` / Test project conventions | shared policy | Preserve in `.agent/instructions/package/DOTNET.md`; client duplicates route through thin adapters. |
| G111 | `.github/instructions/dotnet.instructions.md` / Reporting requirements for implementation tasks | shared policy | Preserve in `.agent/instructions/package/DOTNET.md`; client duplicates route through thin adapters. |

## Retirement and control-plane boundaries

`AGENT_GUARDRAILS.md`, root `DOCUMENTATION.md` and generic `test/AGENTS.md` are retired only after destination verification. `src/AGENTS.md` was absent and is not recreated. Root/native bridges are replaced after policy preservation. No empty custom CODE_REVIEW or DOTNET file is created.

Only operative instruction links, authority/path descriptions and current protected instruction lists change in the recovery backlog and review protocol. Historical pass allowlists, lifecycle states, checkboxes, evidence, SHAs, ordering, commitments and protocol behavior are preserved. Passive historical context retains historical names. Operational `.agent/REVIEW.md` is separate from these control-plane documents.

No installer, manifest merge, external migration, pruning, CI integration, rule-quality audit, evidence ingestion, publication or Git state transition is performed. Claude native compatibility remains pending as recorded in the publisher maintenance README.

## Conservation verification before retirement

Literal comparison of legacy directive bullets against the shared modules, router and
custom companions identified 20 differences. Scope/precedence and read-only mode are
preserved in the new router, including static inspection, real call tracing and the
prohibition on weakening correctness/review/validation. Repository-specific section
fences and placeholder references are replaced by physical custom ownership. Obsolete
src/test/guardrails/documentation routing points to the new modules and thin adapters.
The root/test default yields to the verified workflows tool-owned test layout. No
meaningful directive was dropped through these ownership/routing corrections.

Legacy Claude recovery clauses are preserved verbatim in custom GUARDRAILS except
the retired guardrails reference, which now names its canonical module and matching
companion. The identity paragraph is preserved in custom ENGINEERING; the local
passive import is preserved byte-for-byte. No roadmap status or evidence is inferred.

## Complete migration change inventory

The first implementation changes the following 50 surfaces. Source payloads and installed copies are separate artifacts; local companions and operational state are independently owned.

| Change | Repository-relative path |
|---|---|
| modified | `.github/copilot-instructions.md` |
| modified | `.github/instructions/dotnet.instructions.md` |
| modified | `.github/instructions/test.instructions.md` |
| modified | `.github/tools/doc-metadata/doc-metadata-manifest.json` |
| modified | `AGENTS.md` |
| deleted | `AGENT_GUARDRAILS.md` |
| modified | `CLAUDE.md` |
| deleted | `DOCUMENTATION.md` |
| modified | `repository-maintenance-orchestrator-recovery-backlog.md` |
| modified | `repository-review-protocol.md` |
| deleted | `test/AGENTS.md` |
| added | `.agent/README.md` |
| added | `.agent/REVIEW.md` |
| added | `.agent/instructions/README.md` |
| added | `.agent/instructions/custom/DOCUMENTATION.md` |
| added | `.agent/instructions/custom/ENGINEERING.md` |
| added | `.agent/instructions/custom/GUARDRAILS.md` |
| added | `.agent/instructions/custom/IMPLEMENTATION.md` |
| added | `.agent/instructions/custom/TESTING.md` |
| added | `.agent/instructions/package/CODE_REVIEW.md` |
| added | `.agent/instructions/package/DOCUMENTATION.md` |
| added | `.agent/instructions/package/DOTNET.md` |
| added | `.agent/instructions/package/ENGINEERING.md` |
| added | `.agent/instructions/package/GUARDRAILS.md` |
| added | `.agent/instructions/package/IMPLEMENTATION.md` |
| added | `.agent/instructions/package/TESTING.md` |
| added | `.agent/instructions/package/docs/ARCHITECTURE.md` |
| added | `.claude/settings.json` |
| added | `.github/scripts/agent-package/tests/test_agent_package_installation_contract.py` |
| added | `.github/scripts/agent-package/tests/test_agent_package_source_contract.py` |
| added | `.github/tools/agent-package/MIGRATION.md` |
| added | `.github/tools/agent-package/README.md` |
| added | `deployment/packages/agent-package/AGENTS.md` |
| added | `deployment/packages/agent-package/AGENTS.override.md` |
| added | `deployment/packages/agent-package/README.md` |
| added | `deployment/packages/agent-package/REVIEW.md` |
| added | `deployment/packages/agent-package/bridges/claude/CLAUDE.md` |
| added | `deployment/packages/agent-package/bridges/copilot/copilot-instructions.md` |
| added | `deployment/packages/agent-package/bridges/copilot/instructions/dotnet.instructions.md` |
| added | `deployment/packages/agent-package/bridges/copilot/instructions/test.instructions.md` |
| added | `deployment/packages/agent-package/configuration/sync-manifest-template.json` |
| added | `deployment/packages/agent-package/instruction-package/instructions/README.md` |
| added | `deployment/packages/agent-package/instruction-package/instructions/package/CODE_REVIEW.md` |
| added | `deployment/packages/agent-package/instruction-package/instructions/package/DOCUMENTATION.md` |
| added | `deployment/packages/agent-package/instruction-package/instructions/package/DOTNET.md` |
| added | `deployment/packages/agent-package/instruction-package/instructions/package/ENGINEERING.md` |
| added | `deployment/packages/agent-package/instruction-package/instructions/package/GUARDRAILS.md` |
| added | `deployment/packages/agent-package/instruction-package/instructions/package/IMPLEMENTATION.md` |
| added | `deployment/packages/agent-package/instruction-package/instructions/package/TESTING.md` |
| added | `deployment/packages/agent-package/instruction-package/instructions/package/docs/ARCHITECTURE.md` |

CLAUDE.local.md remains byte-for-byte unchanged. No implementation handoff file, Git commit, push, PR, external adopter change or roadmap transition was created.
