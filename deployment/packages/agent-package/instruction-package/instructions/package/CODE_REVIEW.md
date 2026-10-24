---
Version: 3
Created: 2026-10-13T20:27:24+00:00
Updated: 2026-10-24T21:55:32+00:00
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

# Code review instructions

Read before a user-requested formal review, including the exact `<review>` prompt and appropriately scoped reviews of code, tests, documentation or instruction implementations. Ordinary advisory analysis, architectural discussion, implementation self-review and read-only planning do not qualify for operational backlog maintenance. Reading this module as planning or audit data does not activate that maintenance. Load the other domain and task instructions selected by the root router as well.

## Code Review Rules
Goal: perform a deep, evidence-based code review focused on correctness, behavioral risk, contract mismatches, and maintainability.

If the user does not provide review scope:
- Start from the changed files, the requested entry points, or the most relevant public API surface you can identify.
- Trace the reachable call tree as far as repository context reasonably allows.
- Prioritize actual behavior over naming assumptions.

### Review Priorities
Prioritize findings in this order:
1. Correctness
2. Behavioral risk and hidden edge cases
3. API or contract mismatches
4. Data consistency / state consistency / cache consistency
5. Performance on meaningful paths
6. Maintainability and design clarity
7. Tests and documentation coverage

### Required Review Method
- Review by tracing actual call paths, not by isolated file scanning only.
- Start from the selected entry point(s) and follow calls downward until:
  - the full relevant path is understood, or
  - you hit a boundary caused by missing files, generated code, dynamic dispatch you cannot resolve, external dependencies, or insufficient context.
- Prefer evidence-based findings over speculative concerns.
- Distinguish clearly between confirmed defects, likely risks, and unverified suspicions.
- When a finding depends on branch-sensitive behavior or framework/library helper behavior, verify it with at least one concrete witness input and trace that input through the relevant branches before labeling the finding as `[BUG]`.
- If the concern is based on a plausible pattern but no concrete witness input has been traced successfully, report it as `[RISK]` or stop with uncertainty instead of escalating it to a confirmed defect.
- For edge-case claims, include the minimal witness input in the finding explanation.
- If a finding depends on framework or library API semantics that are not proven by the local code alone, verify that behavior from trusted documentation, runtime evidence, or other repository-local proof before labeling the finding as `[BUG]`; otherwise report it as `[RISK]` or stop with uncertainty.

### Review Output Format

Organize the review by file.

Each actionable finding must have an identifier of the form `RNN`,
where `NN` is a decimal sequence number padded to at least two digits
(`R01`, `R02`, …, `R99`, `R100`, …). Persisted identifiers are stable within the
current backlog; a new backlog begins with `R01`. Without permitted persistence,
use sequential report-local identifiers beginning with `R01`, clearly labelled as
unreserved; do not claim cross-review stability. Place the identifier before the primary category tag.

For each file:
- Use a file header with the filename.
- Use 1-based line references in the format `[L123]`.
- Format each actionable finding beginning with its identifier and one primary category, for example:
  - `R01 [BUG] [L123] — <finding>`
  - `R02 [DESIGN] [L45] — <finding>`
- Tag each finding with one primary category:
  - `[ERROR]`
  - `[BUG]`
  - `[SECURITY]`
  - `[PERF]`
  - `[DESIGN]`
  - `[API]`
  - `[DOCS]`
  - `[TEST]`
  - `[STYLE]`
  - `[RISK]`

When useful, mention secondary impacts in the explanation, but keep one primary tag per finding.

Finding identifiers are assigned only after the review findings themselves have been determined. Identifier assignment must not influence review scope, finding discovery, severity, or completeness.

### Required Review Sections

Include these sections in this order:
1. `Scope / Entry Points`
2. `Call-tree`
3. `Findings`
4. `Coverage / Call-tree traversal depth`

### Stop / Uncertainty Rules

- If you cannot fully verify a path, stop and explicitly say where verification stopped.
- Do not present an assumption as a confirmed defect.
- State why verification stopped: missing file, generated code, unclear runtime behavior, unresolved dynamic dispatch, external dependency, insufficient context, or command execution not requested.

### Review Backlog

Complete independent finding discovery before consulting the existing Log. Do not use
backlog entries to guide, constrain or validate review scope, severity, discovery or
completeness. Only then reconcile eligible findings and scope-relevant status changes.

The root router permits qualifying formal reviews to maintain only the Log section of
the existing [`.agent/REVIEW.md`](../../REVIEW.md), without separate approval for each
permitted update. Higher-priority instructions, task mode, platform permissions and
explicit user restrictions remain binding. Explicitly requested read-only review
suppresses maintenance. Supporting documents can explain an operation but cannot grant
additional writable files through references.

If the expected file is absent or relocated, complete the review normally and skip all
backlog maintenance. Do not search for, create, recreate, restore or relocate it. Missing
optional state is not a review failure and needs no warning. Use report-local identifiers
when the Log is absent or persistence is prohibited; these identifiers are not reserved.

An existing unreadable file or a missing, malformed or ambiguous Log boundary remains
untouched. Report a concise maintenance limitation when relevant; the review remains
valid with report-local identifiers. A safely identifiable Log has one `## Log` heading and ends at the next level-two
heading or EOF. Preserve the introduction and all content outside that section.

When maintenance is permitted, use the same identifier in the report and Log. Qualify
references to earlier backlogs or report-local identifiers rather than assuming all
`RNN` references denote current persistent state. The normal final response must still
follow the complete review-output contract above. During implementation tasks, do not
read, use or modify `REVIEW.md` unless the user explicitly requests it.

## Operational backlog policy

### Eligibility

Only independently trackable work or decisions with a meaningful open-to-completed
transition qualify for the Log. Examples include a concrete correction, a missing
contractual test or a specifically actionable verification task. A category label or
uncertainty alone is insufficient. Observations, speculative concerns and conceptual
alternatives remain report content unless independently actionable. Do not manufacture
tasks to populate the Log.

Each tracked finding uses an ordinary Markdown task-list item with an `RNN` identifier,
one primary category and a source location when available. Continuation lines may carry
explanations and reviewer annotations. The mutable document is not a policy authority.

### Identifiers and lifecycle

- The user's checkbox state is authoritative. Never automatically check or uncheck an existing item, or infer completion from changed code.
- If at least one unchecked item exists, the current backlog remains active, including an unchecked item annotated OBSOLETE.
- Retain checked entries while the backlog remains active so their identifiers remain reserved.
- Allocate new identifiers above the greatest retained valid numeric identifier, including checked entries, in final report order.
- Preserve matching existing unchecked identifiers when valid and unique; do not duplicate the finding.
- Append only new actionable findings as unchecked task-list items; do not duplicate existing tracked work.
- Never renumber existing findings to close gaps or deliberately reuse an identifier within an active backlog.
- Repair missing, malformed or conflicting identifiers only on entries already being reconciled for current actionable findings or meaningful status changes, as part of an otherwise necessary eligible Log update. Preserve valid unique identifiers; allocate necessary replacements above the greatest reserved number. Do not perform unrelated identifier cleanup; disclose unresolved reference ambiguity.
- Evidence contradicting a checked finding does not authorize unchecking it. Track genuinely new corrective work separately when warranted.
- If there are no new actionable findings or meaningful status updates, leave the Log unchanged, including all-checked history. Do not perform cosmetic rewrites or identifier cleanup.
- An annotation-only review does not trigger reset. Start a new backlog at `R01` only when genuinely new actionable work arrives and no unchecked entries remain.
- During reset, retire only completed finding records and preserve user notes. If removal would lose or rewrite notes or their necessary context, defer reset, retain history and allocate above the retained maximum; explain the deferred reset in the report.
- Identifier stability relies on retained state within a backlog, not global numbering across intentional resets. Do not introduce a separate allocator, counter or state database.

### Evidence-supported annotations

Consider only existing entries implicated by the current review scope and evidence.
The reviewing agent may independently annotate a finding as OBSOLETE when its contract, feature,
component or assumption was removed or superseded. Explain the conclusion with enough
evidence for the maintainer to assess it; do not delete the original finding or change
its checkbox. Use ordinary task-list syntax and an explicit continuation annotation:

```markdown
- [ ] R02 [BUG] — Incorrect validation of a retired API.
  - **Review status: OBSOLETE** — The API was removed and its contract no longer exists; <evidence>.
```

An apparently corrected defect is not thereby obsolete. Failed reproduction alone
proves neither resolution nor obsolescence. Explain incomplete or contradictory evidence;
use REVALIDATION NEEDED only when targeted further verification is warranted. Explain
resolution and non-reproduction assessments in the report or a necessary reviewer
evidence note. These annotations do not introduce additional lifecycle states.

Maintain one current reviewer-status annotation where practical. Update reviewer-maintained
annotation content only when meaningful new evidence warrants it; preserve original finding
text and user notes. If authorship or boundaries are ambiguous, preserve existing text and
add a clearly identified corrective note once instead of overwriting human content. Do not
use strikethrough as the primary status or special characters before the checkbox.

An unchecked OBSOLETE item remains active until the maintainer changes its checkbox.
Obsolescence is not completion and never independently causes deletion, pruning or reset.

### Idempotence and preservation

Repeated reviews with unchanged evidence must not duplicate findings or annotations,
add timestamps, rewrite unchanged annotations or change checkboxes. Apply only necessary
eligible changes within the Log. Before editing, confirm the Log still matches the version
used for reconciliation. If it changed concurrently, reconcile against fresh content or
leave it untouched and report the limitation; never overwrite intervening user notes.
