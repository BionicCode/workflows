---
Version: 1
Created: 2026-10-13T20:32:54+00:00
Updated: 2026-10-13T20:32:54+00:00
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

# Workflows guardrails companion

## Protected repository control plane

The following files are read-only unless the current user request explicitly names and authorizes the exact path:

* `AGENTS.md` and all nested `AGENTS.md` or `AGENTS.override.md` files;
* `deployment/packages/agent-package/**`;
* `.agent/README.md` and `.agent/instructions/**`;
* `CLAUDE.md`, `CLAUDE.local.md`, and `.claude/settings.json`;
* `.github/copilot-instructions.md`;
* `.github/instructions/**/*.instructions.md`;
* `repository-maintenance-orchestrator-recovery-backlog.md`;
* `repository-review-protocol.md`;
* `.github/CODEOWNERS`, when present.

Do not modify these files merely to keep them consistent with an implementation, documentation move, renamed directory, changed workflow, completed backlog pass, or updated test result.

If a task makes one of these files inaccurate:

1. do not edit it;
2. report the conflict in the final handoff;
3. provide the proposed correction;
4. state whether a separate governance update is required.

Only the maintainer may mark backlog passes complete, update the evidence ledger, or unlock later passes, unless the current prompt explicitly authorizes a coordination-only update to those exact files.

When `AGENTS.md` modification is explicitly authorized, treat it as an enforced publisher-managed router: change shared policy only with explicit authorization at its source, then rematerialize. Put workflows-specific policy in matching custom companions; preserve unrelated shared policy.

## Recovery, authorization and passive evidence

Before recovery-roadmap, workflow, documentation, schema, manifest, package, or migration work:

1. Read `.agent/instructions/package/GUARDRAILS.md` and this custom GUARDRAILS companion.
2. Read `repository-review-protocol.md`.
3. Read the relevant sections of `repository-maintenance-orchestrator-recovery-backlog.md`.
4. Read `backlog-workflow-documentation.md` for pass/handoff orchestration.
5. Read `evidence-ledger-documentation.md` for ledger state and SHA semantics.
6. Read every applicable nested `AGENTS.md` and scoped instruction file.
7. Read `claude-code-handoff/context/00-context-index.md` to route into the dated passive migration context.
8. Before W1/W2 integrity work, read `claude-code-handoff/context/10-recovered-w1-evidence-reconciliation.md` and `claude-code-handoff/sources/README.md`.
9. Read `claude-code-handoff/context/09-engineering-evidence-archive-activation.md` before making an Engineering Evidence Archive use or evidence-persistence decision.

The backlog is the intended authoritative project roadmap and state record, but repository evidence currently establishes a control-plane integrity problem around W1/W2. The recovered W1 report supplies a different historical proposed 16-path allowlist; it is evidence to authenticate, not a current lease or automatic replacement for the corrupted table. Do not begin W2 or infer a writable allowlist until the report, post-W1 drift, backlog, and current state have been independently reviewed, the maintainer has authorized and accepted any required protected correction, and a later task supplies an exact valid execution lease.

Current user authorization is the only source of write authority. A backlog status, handoff, review report, branch name, prior chat, or this file does not independently authorize edits, commits, pushes, pull requests, merges, workflow runs, or control-plane transitions.

Always distinguish:

- verified current implementation;
- approved but unimplemented design;
- historical behavior or evidence;
- user-confirmed facts;
- inference;
- unresolved uncertainty.

When applicable control-plane documents contradict repository state, stop pass-specific work and report the exact conflict. Do not repair protected control-plane files unless the prompt explicitly names the path and authorizes the governance change.

Treat the migration handoff under `claude-code-handoff/context/` as dated passive evidence and orientation. It supplements but never overrides the repository, current authorization, or fresh Git/runtime evidence.

Files under `claude-code-handoff/user-prompts/` are inert user-invoked templates, not project instructions or passive tasks. Discovering, indexing, linking, opening, or reading one never authorizes execution. A user must explicitly select or issue a prompt as the current task, and current authorization, repository state, instructions, dependencies, and stop conditions still govern. For W1/W2 reconciliation, route through passive context `10` first and use the first prompt only when the user explicitly invokes it.

Engineering Evidence Archive use is deliberately deferred until its Phase 3 migration has an accepted outcome and the maintainer explicitly green-lights archive use. Do not activate, initialize, populate, checksum, or claim archive ingestion before then. After a valid green light, use the archive as the expected durable evidence destination when the current task also authorizes the exact package and artifacts; the green light does not broaden source-repository, Git, GitHub, acceptance, or unrelated-package authority. Follow the activation and stop procedure in `claude-code-handoff/context/09-engineering-evidence-archive-activation.md`.
