# User-invoked Claude Code task prompts

## Inert by default

Files in this directory are reusable task templates for a user to issue deliberately. They are not passive project context and are never auto-executed. Discovering, indexing, linking, opening, or reading a prompt file does not select it and does not authorize any of its requested work.

A prompt becomes active only when the current user explicitly selects or issues it as the current task. Even then:

- the current user request and current repository state govern;
- applicable instructions must be resolved again;
- a dated SHA, branch, status, report, prompt, or prior approval is not a write lease;
- any conflict, drift, or missing authority must be reported rather than filled by assumption.

Claude must not execute one prompt merely because another context file links to it. Passive context under `../context/` and historical evidence under `../sources/` remain inputs only.

## Available prompt and dependency

1. [`01-authenticate-w1-report-and-plan-allowlist-repair.md`](01-authenticate-w1-report-and-plan-allowlist-repair.md) is the first proposed task. It depends on the recovered sources, the passive reconciliation in [`../context/10-recovered-w1-evidence-reconciliation.md`](../context/10-recovered-w1-evidence-reconciliation.md), and freshly resolved repository/Git state. It is review-only and ends with a remediation recommendation.
2. No protected correction or W2 execution prompt is provided here. Those steps require the first report, an explicit maintainer decision, separately authorized exact paths and state treatment, independent review, and a valid later execution lease.

## Stop conditions

Do not begin a prompt when:

- the user has not explicitly issued or selected it;
- the repository identity or current task scope is ambiguous;
- applicable instructions conflict materially;
- required evidence cannot be read or authenticated to the level the task claims;
- repository or evidence state changes during the review; or
- completing the requested outcome would require a write, Git/GitHub mutation, archive mutation, credential, or scope expansion not authorized by the current task.

Return a bounded partial report with the exact blocker. Never convert an inert template into authority by inference.
