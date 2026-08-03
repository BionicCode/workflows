@AGENTS.md

# Claude Code project routing

This repository is `BionicCode/workflows`. It is the implementation-authority repository for reusable GitHub Actions workflow engines. It is not the `template-visual-studio-repository` caller project.

Before recovery-roadmap, workflow, documentation, schema, manifest, package, or migration work:

1. Read `AGENT_GUARDRAILS.md`.
2. Read `repository-review-protocol.md`.
3. Read the relevant sections of `repository-maintenance-orchestrator-recovery-backlog.md`.
4. Read `backlog-workflow-documentation.md` for pass/handoff orchestration.
5. Read `evidence-ledger-documentation.md` for ledger state and SHA semantics.
6. Read every applicable nested `AGENTS.md` and scoped instruction file.

The backlog is the intended authoritative project roadmap and state record, but repository evidence currently establishes a control-plane integrity problem around W1/W2. Do not begin W2 or infer a writable allowlist until the current task has independently revalidated the backlog and supplied an exact authorized execution lease.

Current user authorization is the only source of write authority. A backlog status, handoff, review report, branch name, prior chat, or this file does not independently authorize edits, commits, pushes, pull requests, merges, workflow runs, or control-plane transitions.

Always distinguish:

- verified current implementation;
- approved but unimplemented design;
- historical behavior or evidence;
- user-confirmed facts;
- inference;
- unresolved uncertainty.

When applicable control-plane documents contradict repository state, stop pass-specific work and report the exact conflict. Do not repair protected control-plane files unless the prompt explicitly names the path and authorizes the governance change.

Treat the migration handoff under `claude-code-handoff/context/` as dated evidence and orientation. It supplements but never overrides the repository, current authorization, or fresh Git/runtime evidence.
