---
Version: 1
Created: 2026-10-13T20:32:55+00:00
Updated: 2026-10-13T20:32:55+00:00
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

# Workflows implementation companion

## Implementation-pass review handoff

For every completed implementation pass defined by `repository-maintenance-orchestrator-recovery-backlog.md`, produce a self-contained review handoff.

The handoff must contain:

* the backlog pass identifier and task goal;
* the exact repository, base branch, base commit SHA, and resulting working-tree or commit state;
* the premises, approved design decisions, and conventions used;
* the implementation summary and rationale;
* externally visible behavior and behavior intentionally left unchanged;
* the complete changed-file list;
* validation commands, runtime versions, and results;
* tests added or changed and the external contract each test proves;
* documentation, schema, manifest, configuration, example, and migration assessment;
* security, permission, trust, ownership, concurrency, idempotence, and rollback review where relevant;
* unverified paths, environment limitations, assumptions, and remaining risks;
* confirmation of whether any stop condition occurred;
* all Git and GitHub actions performed;
* a suggested commit subject and, when useful, an optional commit body;
* the exact next backlog pass unlocked, or an explicit statement that no later pass is unlocked.

Do not stage, commit, push, create or update a pull request, merge, dispatch workflows, or modify repository settings unless the user explicitly authorizes that exact action.

Create or update a repository Markdown handoff file only when the current task explicitly authorizes its path. A backlog requirement alone does not expand the task’s writable file scope.

When no repository handoff file is authorized, return the complete handoff in the final response and state that no persistent handoff artifact was created.

Do not claim completion based solely on passing tests. Review the complete diff against the pass contract, repository instructions, public behavior, documentation, schema, configuration, and stop conditions before declaring the pass complete.
