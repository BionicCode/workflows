# Engineering Evidence Archive activation procedure

## 1. Purpose and current status

This document gives a new Claude Code session enough durable procedure to use
the Engineering Evidence Archive after its migration gate is satisfied. It is
orientation and execution guidance, not advance authorization.

> [!CAUTION]
> **Status on 2026-08-04: deferred.** Do not initialize, populate, checksum,
> validate as complete, or claim ingestion of a Workflows evidence package.
> Activation requires both an accepted Engineering Evidence Archive Phase 3
> outcome and an explicit maintainer green light.

The intended future green light may be as short as:

```text
Claude may now use the Engineering Evidence Archive.
```

That statement activates archive availability and the expectation that
qualifying durable evidence will be persisted. It does not replace the current
task. The current task must still provide the source scope, stable backlog-item
identity, artifacts to preserve, and authority for the exact archive package
mutation. This static document never pre-authorizes a future write.

## 2. Status model

### Deferred

Archive use is deferred while any activation prerequisite is unproved. Claude
may prepare an archive-ready report and pending-ingestion record, but must not
write an archive package or say that evidence was archived.

### Activation-ready

The archive is activation-ready only when fresh evidence establishes all of
the following:

1. Phase 3 has a specific accepted outcome, not merely a branch, commit,
   filename, or statement that work was attempted.
2. The accepted Phase 3 result leaves the current schema-v1 project and package
   state valid for the intended operation.
3. The archive checkout, instructions, imports, schemas, pinned dependencies,
   tests, and documented command interfaces can be read and reconciled.
4. The current task identifies the exact source repository, backlog item,
   package scope, artifacts, and permitted archive mutations.
5. The maintainer explicitly gives the archive green light.

### Activated

After all prerequisites and the explicit green light, archive use is expected
for qualifying durable evidence produced or accepted within the current task.
Do not treat persistence as vague cleanup or an optional afterthought. Do not,
however, archive every draft, intermediate chat, or transient command output by
default; apply the selection rules in this document.

The green light does not authorize:

- edits to `BionicCode/workflows` or another source repository;
- execution, review acceptance, maintainer acceptance, source integration, or
  a backlog-state transition;
- staging, commits, pushes, pulls, fetches, merges, rebases, resets, stashes,
  pull requests, workflow dispatches, or other remote changes;
- writes to an unrelated archive project or package; or
- overwrite, repair, normalization, or deletion of existing evidence.

## 3. Repository identities and mandatory re-resolution

The source repository is:

```text
BionicCode/workflows
```

It remains the roadmap and implementation authority. Resolve its actual local
root, remote identity, branch or detached state, HEAD, upstream, working tree,
and current task authorization before using any evidence from it.

The archive repository is:

```text
BionicCode/engineering-evidence-archive
```

The last-known local archive path on 2026-08-04 was:

```text
I:\GitHubRepositories\ChatGPT\EngineeringEvidenceArchive\engineering-evidence-archive
```

The path and every SHA in this handoff are dated hints. At activation, locate
the actual archive checkout and re-resolve its repository identity, branch,
HEAD, upstream, ahead/behind relationship, complete worktree status, applicable
instructions, runtime, dependencies, and current files. Do not select a
checkout or baseline from this path or a remembered SHA alone.

## 4. Authority boundaries

The Workflows authority chain remains:

1. current explicit maintainer authorization;
2. current `BionicCode/workflows` repository and Git evidence;
3. the authoritative Workflows recovery backlog and supporting control-plane
   documents;
4. accepted handoffs, execution reports, and reviews tied to exact state.

The archive is the authority only for its evidence layout, provenance records,
artifact inventory, relationships, and integrity contract. It is not a second:

- Workflows roadmap or backlog;
- execution lease;
- implementation source;
- independent reviewer;
- maintainer acceptance authority; or
- integration record for the source repository without separate source
  evidence.

Keep these dimensions separate:

| Dimension | Authority and meaning |
| --- | --- |
| Archive completeness | Whether the package satisfies the archive contract. |
| Task execution | What the authorized task did or failed to do. |
| Independent review | What an identified reviewer concluded. |
| Maintainer acceptance | What the maintainer explicitly accepted, rejected, or deferred. |
| Source integration | What current source-repository evidence proves was integrated, not integrated, reverted, or remains unknown. |

No value in one dimension proves another. A complete archive may document a
failed task, and an accepted or integrated task may still have an incomplete
archive.

## 5. Authoritative archive sources after activation

Read these from the freshly resolved archive checkout before any archive
mutation:

1. `CLAUDE.md`, including every imported instruction file;
2. root and applicable nested `AGENTS.md` or `AGENTS.override.md` files;
3. `EVIDENCE_TRACKING.md` for normative evidence semantics;
4. `TOOLING.md` for the current schema-v1 operational profile and commands;
5. `schemas/project-metadata-v1.schema.json` and
   `schemas/evidence-manifest-v1.schema.json`;
6. `requirements.txt` and the installed dependency versions;
7. `tests/test_archive_tools.py` and current accepted test evidence;
8. the intended project's `PROJECT.md` and every existing package record that
   affects mapping, collision, supersession, or provenance; and
9. the current Workflows instructions, backlog item, handoff, result, review,
   and maintainer-decision evidence being represented.

Do not infer missing imported content. A missing `@...` import, contradictory
instruction surface, unsupported schema version, unavailable required source,
or ambiguous authority rule is a stop condition. Report the exact missing or
conflicting path and wait for an authorized correction or maintainer decision.

## 6. Canonical Workflows package mapping

Schema version `1` maps the repository exactly as follows:

```text
BionicCode/workflows
-> projects/workflows/
```

A stable Workflows backlog item maps to:

```text
ITEM-ID
-> projects/workflows/backlog-items/ITEM-ID/
```

Preserve the repository name and backlog-item identifier exactly, including
case and suffixes. For example, `W2A` must not become `w2a`. The project record
must preserve the full `BionicCode/workflows` identity.

Before writing, inspect all project mappings. If another owner already maps the
same repository-name directory, if project metadata disagrees with the path,
if case differs, or if the required mapping exception is unresolved, stop with
an owner/name collision. Do not create an owner directory or invent a mapping;
schema-v1 requires an explicit maintainer decision for that case.

Locate an existing item before running the initializer. The initializer has no
force or overwrite mode. An existing, legacy, invalid, conflicting, or
case-colliding project or package is a stop condition, not permission to repair
or replace it.

## 7. Evidence selection and truthful metadata

Persist the durable evidence needed to reconstruct the task and its decisions:

- the authorized handoff or binding scope contract;
- a durable execution or review report;
- independent and acceptance reviews;
- material validation logs, diffs or patches, and supporting attachments;
- explicit maintainer decision or acceptance evidence; and
- a conversation export only when it is materially necessary for provenance
  and the current task authorizes storing it.

Do not archive every draft, scratch note, intermediate chat, repeated output,
or transient diagnostic by default. Prefer the smallest complete evidence set.
Every archived task needs a durable stored report before its package can be
archive-complete; a final chat response alone is insufficient.

For every artifact, record truthfully:

- its allowed role;
- `direct-task` or `later-contextual-or-governance` evidence phase;
- `original`, `exported-original`, `reconstructed`, `derived`, or
  `reference-only` provenance;
- the source and acquisition or reconstruction method;
- known creation, observation, export, or import dates with the event meaning;
- every SHA with its semantic role, such as baseline, lease, result, reviewed,
  or integrated state;
- relationships to other artifacts;
- material limitations and unavailable evidence; and
- unknown and not-applicable states without optimistic defaults.

Do not describe recreated text as original, a branch as an exact commit, an
archive record as acceptance, or missing evidence as if it were observed.

## 8. Payload immutability and corrections

Once a stored artifact has a manifest entry, its payload bytes are immutable.
Never silently edit, normalize, redact, replace, regenerate, or delete those
bytes, even when the artifact is reconstructed or derived.

A correction or better representation is a new artifact with a new id, path,
provenance record, origin description, and digest. Use:

- `derived_from` when the new representation derives from an artifact stored in
  the same package; and
- `supersedes` when the new artifact explicitly corrects or replaces an earlier
  artifact.

Keep the earlier artifact and its provenance. Metadata or index corrections
must remain reviewable in Git and must never conceal a payload rewrite.

## 9. Operational sequence after activation

The commands below matched archive `TOOLING.md` and the CLI parser definitions
at the 2026-08-04 read-only inspection. Re-read current `TOOLING.md` and confirm
the interfaces before using them.

### 9.1 Inspect and locate

From the freshly resolved archive root:

1. Confirm repository identity and expected worktree state.
2. Resolve `BionicCode/workflows` and the exact `ITEM-ID` from the authoritative
   Workflows backlog.
3. Inspect `projects/` for exact-case mapping and owner/name collisions.
4. Locate any existing project and package before planning a write.
5. Inspect for legacy or invalid metadata, transaction locks, candidate or
   rollback stages, unexpected payloads, and unrelated changes.
6. Confirm that the current task authorizes the exact package and artifact set.

Stop rather than normalizing, deleting, moving, or repairing unexpected state.

### 9.2 Preview initialization

For a genuinely absent package, preview the exact paths without writing:

```text
python .github/scripts/init-backlog-item.py --repository BionicCode/workflows --item-id ITEM-ID --dry-run
```

Review the plan against the authorized package. If the package and project
creation paths are authorized and the preview is clean, repeat without
`--dry-run`:

```text
python .github/scripts/init-backlog-item.py --repository BionicCode/workflows --item-id ITEM-ID
```

Optional verified fields such as task title, task mode, default branch, project
title, and archive scope may be supplied only when current evidence establishes
them. Do not invent values merely to fill the skeleton.

### 9.3 Add payloads and manifest records

Within the one authorized package:

1. Preserve the selected artifact bytes in the correct `handoff/`, `reports/`,
   `reviews/`, or `attachments/` directory.
2. Add exactly one manifest entry for every stored payload.
3. Record role, evidence phase, provenance, source, date, media type,
   relationships, limitations, and state evidence truthfully.
4. Keep `sha256: null` for a stored artifact only during the bounded interval
   before the explicit checksum transaction.
5. Update `INDEX.md` so its state dimensions, evidence groups, missing evidence,
   and links accurately mirror the manifest.

Do not add `.gitkeep` files to payload directories. Do not add an unlisted
payload or a fictitious local path for reference-only evidence.

### 9.4 Preview and write checksums

Preview checksum metadata without writing:

```text
python .github/scripts/generate-checksums.py projects/workflows/backlog-items/ITEM-ID --dry-run
```

When the current task authorizes checksum metadata writes for that exact
package, run:

```text
python .github/scripts/generate-checksums.py projects/workflows/backlog-items/ITEM-ID --write
```

The writer fills only missing manifest digests and writes the matching sorted
`SHA256SUMS`; it does not invent artifact entries or overwrite a conflicting
non-null digest. Treat a lock, stage, concurrent change, rollback conflict, or
manifest/checksum split as a stop requiring manual evidence-based inspection.
Never break a lock based only on age or PID.

### 9.5 Validate the package read-only

Validate the exact package:

```text
python .github/scripts/validate-archive.py projects/workflows/backlog-items/ITEM-ID --format text
```

Validation must remain read-only. It must not generate checksums, normalize
YAML, repair metadata, create files, or remove locks. Root validation may be
added when the current archive contract requires it, but package success must
not be used to hide unrelated root invalidity or an unresolved Phase 3 state.

### 9.6 Review the complete result

Review the complete archive diff and confirm:

- only the authorized project/package paths changed;
- payload bytes match the acquired evidence;
- inventory, links, relationships, checksums, dates, SHA roles, provenance,
  limitations, and independent state dimensions are truthful;
- no source-repository or unrelated package state changed;
- package state does not overclaim completeness, review, acceptance, or
  integration; and
- every performed or unavailable validation is reported exactly.

Git or GitHub publication is a separate action. If the current task does not
authorize it, leave the reviewed archive changes uncommitted and report that
state.

## 10. Checksums, validation, and exit taxonomy

Checksum generation and validation are different operations:

| Operation | May write? | Meaning |
| --- | --- | --- |
| Checksum `--dry-run` | No | Previews digest/metadata changes and consistency checks. |
| Checksum `--write` | Yes, only when authorized | Writes missing manifest digests and `SHA256SUMS` through the guarded transaction. |
| Archive validation | Never | Recomputes and compares structure, inventory, links, relationships, state, and digests without repair. |

All current archive CLIs use:

| Exit | Meaning and required response |
| --- | --- |
| `0` | Requested operation completed. For validation, all performed checks passed; warnings may remain. |
| `1` | Input or archive state is invalid, conflicting, or unsafe for the requested operation. Correct only through separately authorized work; do not claim validation. |
| `2` | Operation or validation could not complete safely because of unavailable tooling/schema, unreadable data, unsupported version, concurrency, or transaction failure. Report validation-incomplete; this takes precedence when invalidity also exists. |
| `64` | CLI misuse. Correct the invocation; no archive conclusion follows. |

Checksum agreement proves that current bytes match current metadata. It does
not prove that both were never rewritten historically. Review Git history when
historical immutability matters. A validator exit `0` proves the automated
checks it performs, not semantic completeness of a human report.

## 11. Cross-repository and write boundaries

Archive activation never expands the current source task. In particular:

- archive writes do not authorize Workflows edits;
- Workflows edits do not automatically authorize archive writes;
- archive validation does not authorize checksum generation or repair;
- archive completion does not close a Workflows pass or update its ledger;
- a read-only source review may produce archive evidence only when current user
  authorization also covers mutation of the exact archive package; and
- one authorized package does not authorize another project, item, correction,
  supersession chain, or coordination record.

Keep source-repository and archive diffs, reports, and Git actions separately
accounted. Never mix a source implementation mutation into an evidence-ingestion
operation merely because both concern the same backlog item.

## 12. Phase 3 activation gate

Do not infer Phase 3 readiness from the existence of `PROJECT.md`, a manifest,
a `schema_version: 1` scalar, a branch name, a commit message, or the phrase
"Phase 3 complete." Verify the accepted result against the current archive
contract.

At minimum, establish that:

1. maintainer evidence identifies the exact accepted Phase 3 result;
2. `projects/workflows/PROJECT.md` uses the current project-metadata schema;
3. the W1 package and any migrated project metadata use the current manifest
   schema and no longer rely on legacy placeholders or `.gitkeep` payloads;
4. stored payloads, inventory, links, checksums, roles, provenance,
   relationships, durable report, and state dimensions are valid and truthful;
5. the pinned runtime dependencies and supported interpreter are available;
6. current accepted test evidence covers the tool state being used;
7. package and required root validation complete with the expected results;
8. all Claude/agent instruction imports exist and material instruction conflicts
   are resolved; and
9. the intended checkout and package scope are clean or contain only explicitly
   expected changes.

### Dated blockers observed on 2026-08-04

The read-only inspection for this handoff found:

- archive `main` at `e6d98ebc799d3b67e94f0edc531de3746badc6d3`,
  clean and five commits ahead of cached `origin/main`; no fetch established
  current live remote state;
- Phase 3 still described as future work in `EVIDENCE_TRACKING.md`, `TOOLING.md`,
  and `README.md`;
- `projects/workflows` still using legacy `owner.yaml` and `PROJECT.yaml` rather
  than schema-v1 `PROJECT.md`;
- W1 still using the pre-contract manifest, absent referenced payloads,
  `.gitkeep` payloads, and an empty checksum file;
- archive `CLAUDE.md` importing the missing
  `docs/claude-context/00-core-context.md`;
- archive `AGENTS.md` referring to removed
  `projects/template-visual-studio-repository` content in its current migration
  boundary; and
- Python 3.14.6 available, but pinned `PyYAML` unavailable; the read-only root
  validator returned exit `2` with `DEPENDENCY_UNAVAILABLE` and left no cache,
  lock, stage, or worktree change.

These are dated observations, not permanent claims. Recheck them after Phase 3
and record only the conditions that still exist.

## 13. Activation checklist

Before the first archive mutation after the green light, confirm every item:

- [ ] The maintainer explicitly green-lit Engineering Evidence Archive use.
- [ ] An exact accepted Phase 3 outcome was identified and verified.
- [ ] The current task authorizes the exact archive project, package, artifacts,
      and required metadata/checksum writes.
- [ ] The actual archive root, identity, branch/HEAD, upstream, worktree, and
      source repository state were freshly resolved.
- [ ] `CLAUDE.md`, all imports, applicable agent instructions, evidence contract,
      tooling specification, schemas, requirements, tests, project metadata,
      and relevant package records were read and agree.
- [ ] Pinned dependencies and required validation are available, or the task is
      taking the degraded path without claiming ingestion.
- [ ] `BionicCode/workflows` maps exactly to `projects/workflows`, and the exact
      `ITEM-ID` maps without collision or case change.
- [ ] No legacy, invalid, unexpected existing, locked, staged, indirect, or
      unrelated state blocks the operation.
- [ ] The artifact set, roles, evidence phases, provenance, sources, dates, SHA
      meanings, relationships, limitations, and unknowns are established.
- [ ] Dry-run, write, checksum, validation, diff review, and reporting boundaries
      are understood and authorized.

When these checks pass, the one-sentence green light plus the current task is
operationally sufficient. Do not ask the maintainer to restate this design.

## 14. Stop checklist

Stop archive mutation and return the exact evidence when any of these occurs:

- the green light or accepted Phase 3 outcome is absent or ambiguous;
- the current task does not cover the exact archive package mutation;
- the repository identity, root, mapping, case, owner, item id, or source scope
  differs from expectation;
- an instruction import is missing or governing sources conflict;
- the schema/tool version is unsupported or required dependencies/tests are
  unavailable for the claimed operation;
- the project or package is legacy, invalid, unexpectedly existing, colliding,
  indirect, locked, concurrently changed, or contains unexplained state;
- an operation would overwrite, normalize, delete, or silently rewrite evidence;
- artifact originality, source, date, SHA meaning, authority, relationship, or
  limitation cannot be represented truthfully;
- initializer or checksum dry-run reports unexpected paths or changes;
- an archive CLI returns exit `1`, `2`, or `64` and the condition is not resolved
  within separately authorized scope;
- validation would write or repair;
- source or archive state changes during the operation; or
- the requested archive claim would imply execution, review, acceptance,
  integration, or completeness not established by separate evidence.

## 15. Degraded path and pending ingestion

If archive access, instruction imports, tooling, dependencies, validation, or
write authority is unavailable, preserve the evidence in the current task's
authorized output and return an archive-ready report. Do not create a repository
file merely to hold it unless the current task authorizes that path.

Include this pending-ingestion record:

```text
Archive status: NOT ARCHIVED
Source repository: BionicCode/workflows
Backlog item: <exact ITEM-ID>
Intended package: projects/workflows/backlog-items/<exact ITEM-ID>/
Artifact set: <ids, intended paths, roles, evidence phases, provenance, sources>
Repository state: <dated SHA values with each semantic meaning>
Dates and limitations: <known events, unknowns, unavailable evidence>
Checksums: NOT GENERATED | GENERATED BUT NOT VALIDATED | <truthful state>
Validation: NOT RUN | INCOMPLETE (exit 2, exact code) | INVALID (exit 1, exact code)
Blocking condition: <exact access, instruction, dependency, schema, state, or authority blocker>
Required next action: <smallest authorized action needed before ingestion>
```

Preserve payload bytes and acquisition details so later ingestion can classify
them accurately. A pending record is not an archive package, checksum proof,
validation result, acceptance decision, or integration record.
