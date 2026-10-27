---
Version: 3
Created: 2026-10-13T20:27:23+00:00
Updated: 2026-10-27T21:11:01+00:00
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

# Agent-package publisher maintenance

The authoritative shared source is `deployment/packages/agent-package/` in
`BionicCode/workflows`. The installed workflows package is a derived first consumer.
Edit shared sources, finalize source metadata, then materialize bytes. Keep workflows
policy in installed custom companions. [MIGRATION](MIGRATION.md) records baseline
identity, every legacy policy group, conservation destinations and retirement.

## Approved scope and executable gates

The passive package has exactly seven modules and the approved source/target projection.
The first installation is manual. Installer implementation, registration merging,
external migrations, pruning, CI integration, rule-quality audits, template changes,
publication, Git mutations and recovery-roadmap state transitions are deferred or
separately authorized. Manual materialization is not transactional: keep the old router
until dependencies, local policy and bridges are ready.

Core implementation requires verified Git/protected-file state, Codex native isolation,
legacy policy conservation, schema/projection/lifecycle/sync validation, explicit-path
metadata tests, source/installation suites, installation parity and complete diff review.
Authenticated Claude is not a prerequisite for bounded core implementation or completion.
Claude native compatibility remains a distinct pending gate. No subscription, API key,
personal credential change, personal setting change or further authentication attempt is
part of this implementation.

## Publisher native isolation

Create the publisher-only `deployment/packages/agent-package/AGENTS.override.md` before
the sibling deployable `AGENTS.md`. Codex selects the override at source startup.
Explicit target-path inspection must make the same selection. Source payloads remain
inspectable data, and operative root/module/custom guidance governs source maintenance.
Never include the override in consumer projection.

Preserve existing publisher `.claude/settings.json` keys and unrelated exclusions.
The following exercised merge recipe adds only the two approved source payload paths.
Set `$repositoryRoot` to the verified publisher root before running it.

<!-- acceptance:claude-settings-merge:start -->
```powershell
$settingsPath = Join-Path $repositoryRoot '.claude/settings.json'
$settings = if (Test-Path -LiteralPath $settingsPath) {
    Get-Content -LiteralPath $settingsPath -Raw | ConvertFrom-Json -AsHashtable
} else { @{} }
if (-not $settings.ContainsKey('claudeMdExcludes')) { $settings.claudeMdExcludes = @() }
if ($settings.claudeMdExcludes -isnot [System.Collections.IList]) {
    throw 'claudeMdExcludes must be an array; preserve and resolve invalid existing configuration.'
}
$requiredExclusions = @(
    '**/deployment/packages/agent-package/AGENTS.md'
    '**/deployment/packages/agent-package/bridges/claude/CLAUDE.md'
)
foreach ($pattern in $requiredExclusions) {
    if ($settings.claudeMdExcludes -cnotcontains $pattern) {
        $settings.claudeMdExcludes = @($settings.claudeMdExcludes) + $pattern
    }
}
[void][System.IO.Directory]::CreateDirectory((Split-Path -Parent $settingsPath))
[System.IO.File]::WriteAllText($settingsPath, ($settings | ConvertTo-Json -Depth 100) + "`n", [System.Text.UTF8Encoding]::new($false))
```
<!-- acceptance:claude-settings-merge:end -->

Do not suppress installed root AGENTS/CLAUDE, custom companions or other repository
instructions. Publisher settings are not distributed. Both minimal Claude bridges
retain the real `@AGENTS.md` import. The configuration is provisional: documented
support is not proof of effective native behavior in every context.
[Claude memory and Project instructions](https://code.claude.com/docs/en/memory),
[Codex discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md), and
[Copilot path frontmatter](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
describe the client contracts used here.

## Registration and ordering

`deployment/packages/agent-package/configuration/sync-manifest-template.json` contains
declarations against the existing schema. Required entries are index, recursive
instruction subtree, REVIEW seed and root router. Optional Claude is the one-entry
seed_once group; optional Copilot is the three-entry enforce group. Selecting a group
means retaining all its entries; the existing schema has no package/optional-group field.
The declaration is not an installer or a complete adopter manifest.

Every selector includes the full package source prefix, source_repo BionicCode/workflows,
source_ref main, source_to_target, whole_file and uniqueness_policy none. The instruction
glob includes recursive and hidden-file expansion. It is additive and never prunes custom,
operational or unrelated files. Opt-out does not delete installed files. A single-file
glob opt-out needs non-overlapping declarations. Old external manifests are unchanged.

For the first migration, preserve legacy local content before replacing existing Claude
and Copilot bridges. Later seed_once sync preserves existing Claude customizations and
operational REVIEW. Do not seed from a live publisher Log.

## Explicit metadata mutation

Use the one existing `.github/tools/doc-metadata/doc-metadata-manifest.json`.
The following source/maintenance path construction and real string-array invocation are
exercised by the acceptance fixture. Run from the verified workflows repository root.
Every mutating updater call must select actual, existing, unique, nonempty filenames.
Do not pass globs to `-Path` or fall back to staged/implicit discovery.

<!-- acceptance:source-metadata-update:start -->
```powershell
$sourcePrefix = 'deployment/packages/agent-package/'
[string[]] $metadataPaths = @(
    $sourcePrefix + 'AGENTS.md'
    $sourcePrefix + 'AGENTS.override.md'
    $sourcePrefix + 'README.md'
    $sourcePrefix + 'instruction-package/instructions/README.md'
    $sourcePrefix + 'instruction-package/instructions/package/docs/ARCHITECTURE.md'
    $sourcePrefix + 'bridges/copilot/copilot-instructions.md'
    $sourcePrefix + 'bridges/copilot/instructions/dotnet.instructions.md'
    $sourcePrefix + 'bridges/copilot/instructions/test.instructions.md'
    '.github/tools/agent-package/README.md'
    '.github/tools/agent-package/MIGRATION.md'
)
foreach ($module in @('ENGINEERING','IMPLEMENTATION','CODE_REVIEW','DOTNET','TESTING','GUARDRAILS','DOCUMENTATION')) {
    $metadataPaths += $sourcePrefix + 'instruction-package/instructions/package/' + $module + '.md'
}
if ($metadataPaths.Count -eq 0 -or @($metadataPaths | Select-Object -Unique).Count -ne $metadataPaths.Count) {
    throw 'Invalid metadata inventory.'
}
foreach ($path in $metadataPaths) {
    if ($path -match '[*?\[]' -or -not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Invalid explicit path: $path" }
    if (-not ($path.StartsWith($sourcePrefix) -or $path.StartsWith('.github/tools/agent-package/'))) { throw "Invalid metadata ownership: $path" }
}
& ./.github/scripts/doc-metadata/update-doc-metadata.ps1 `
    -Mode Update -Root . `
    -ManifestPath .github/tools/doc-metadata/doc-metadata-manifest.json `
    -Path $metadataPaths
if ($LASTEXITCODE -ne 0) { throw 'Source metadata update failed.' }
```
<!-- acceptance:source-metadata-update:end -->

The repository-owned companions in this installation are ENGINEERING, TESTING,
GUARDRAILS and DOCUMENTATION. Initialize or update them through this separate explicit
batch; IMPLEMENTATION, CODE_REVIEW and DOTNET companions are intentionally absent.

<!-- acceptance:custom-metadata-update:start -->
```powershell
[string[]] $metadataPaths = @(
    '.agent/instructions/custom/ENGINEERING.md'
    '.agent/instructions/custom/TESTING.md'
    '.agent/instructions/custom/GUARDRAILS.md'
    '.agent/instructions/custom/DOCUMENTATION.md'
)
if ($metadataPaths.Count -eq 0 -or @($metadataPaths | Select-Object -Unique).Count -ne $metadataPaths.Count) { throw 'Invalid custom inventory.' }
foreach ($path in $metadataPaths) {
    if (-not $path.StartsWith('.agent/instructions/custom/') -or $path -match '[*?\[]' -or -not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Invalid custom path: $path" }
}
& ./.github/scripts/doc-metadata/update-doc-metadata.ps1 `
    -Mode Update -Root . `
    -ManifestPath .github/tools/doc-metadata/doc-metadata-manifest.json `
    -Path $metadataPaths
if ($LASTEXITCODE -ne 0) { throw 'Custom metadata update failed.' }
```
<!-- acceptance:custom-metadata-update:end -->

Source REVIEW, operational REVIEW and minimal source/installed Claude bridges are
excluded. Installed enforced router, READMEs, modules, architecture and Copilot files
receive source metadata byte-for-byte and are excluded from independent mutation.
Non-managed YAML fields such as Copilot applyTo must survive source updates.

The existing updater treats any YAML frontmatter block as metadata. A new Copilot
document containing only applyTo is rejected as incomplete metadata when no committed
timestamps exist. Author these new source files with valid initial Version, Created,
Updated and Author fields alongside applyTo, using the actual UTC metadata-initialization
time and publisher identity. Then run the explicit updater batch above for presentation
and validation. Do not weaken the engine or discard non-managed fields. Acceptance
also exercises its rejection of incomplete frontmatter without unrelated writes.

## Manual materialization

After source metadata validation, copy README → .agent/README; instruction-package
members → .agent preserving their subtree. Create/update meaningful repository-owned
custom companions independently. Preserve existing .agent/REVIEW or initialize from
the empty seed. Preserve local/client content, then materialize the selected bridges.
Install root AGENTS last after required modules exist. Keep CLAUDE.local byte-for-byte.
Rematerialize whole bytes after any source correction. Never independently repair an
enforced installation. Verify conservation before retiring legacy files.

The current manual workflows installation includes the root Claude bridge and all
three Copilot adapters. Its four local companions are repository-owned extensions
outside the package synchronization projection. The installed Claude bridge retains
the package seed; native Claude compatibility remains subject to the separate gate below.

## Repeatable core acceptance

Required runtimes are Python with the existing sync tool's jsonschema>=4,<5 dependency,
Git and PowerShell 7. Use an isolated environment and the existing
`.github/scripts/sync-files-from-manifest/requirements.txt`. Missing required
dependencies fail; required tests never silently skip. If pwsh is not on PATH, set
AGENT_PACKAGE_PWSH to an existing PowerShell 7 executable for this process.

Run from workflows repository root after package, bridge, declaration, source-metadata
or rematerialization changes:

```powershell
python -B -m unittest discover -s .github/scripts/agent-package/tests -p "test_*.py"
```

The command checks real source/installation contracts and uses the existing sync and
metadata implementations in disposable fixtures. Installed checks are read-only.
It covers restored routing triggers, projection, drift, seeds, ownership, migration,
links, settings merge/matching, lifecycle, opt-out, old manifests, partial states and
explicit metadata with unrelated staged content. It does not prove native-client or
model behavior. This is a local maintenance requirement, not installed CI integration.

Codex preflight: 0.153.4; isolated root, source and source-descendant startup. Actual
saved session instruction messages showed root guidance at all locations, the override
at the two nested locations, and no source payload sentinel. Native module-read attempts
in the earlier read-only probe were denied by its tool policy; those attempts are not
passing routing evidence. Installed native routing and root-started explicit source
inspection must be checked separately before core completion.

Implementation validation: the required unittest invocation passed all 45 tests on
2026-10-13 using isolated Python 3.12.14, jsonschema 4.26.0 and PowerShell 7. The gate
includes actual source/installation parity and the unchanged metadata/sync engines.
The disposable owned-metadata Check passed; unrelated repository-wide failures remain
separate below. Git diff --check passed. No application build/restore or CI run applies
to this passive package change.

Installed Codex 0.153.4 acceptance used `codex exec --approve-for-me
--ignore-user-config --json --cd <startup-directory> --output-last-message <scratch-file>`
with explicit read-only prompts. Working directories were the workflows repository
root, deployment/packages/agent-package, and its
instruction-package/instructions/package descendant. Supported automatic approval
review was required for legitimate file reads in this environment; the earlier
--ask-for-approval never attempts were denied by command policy and remain recorded.
No execution-policy rule or personal setting was changed or bypassed.

Actual saved session user instruction messages contained the root router once in all
three sessions and the publisher override once at both nested starts. The independent
sentinel preflight proved same-directory source-payload suppression. Actual successful
tool results established all five selected package/custom pairs for implementation
planning, testing, guardrails and documentation; complete outputs were reread after
truncation. Root-started explicit target inspection selected the source override and
did not read the suppressed sibling as instructions. No formal CODE_REVIEW or
operational Log access occurred. This is scoped native evidence, not a model-compliance
guarantee. Hashes and file membership for all 118 existing tracked/untracked repository
files were unchanged across the native probes.

Native session evidence identifiers: root 01a1370a-5f6c-7ed2-87db-e0a448fb577e,
source 01a1370c-b158-7b01-b2c3-9227d7cb856b, descendant
01a1370d-46e4-7d90-9a61-21fe5f8c75e0. Saved tool outputs and loading audit are in the
implementation's disposable preflight artifacts. Claude compatibility remains pending;
none of these Codex results substitute for the deferred Claude gate.

The existing updater's read-only Check mode checks the whole governed repository even
when -Path is supplied; -Path restricts mutating Update. During implementation the
repository-wide Check reported four pre-existing missing-metadata failures in the
sync tool requirements.txt and the three historical handoff sources
backlog-governance-acceptance-review.txt, W1-final-audit-report.txt and
W1-planning-and-handoff.txt. These unrelated files are preserved. The contract gate
copies the actual owned source/maintenance/custom documents into a disposable fixture
and runs the unchanged Checker there; it does not introduce another repository config.

## Claude compatibility: pending and source maintenance unsupported/unverified

Claude 2.1.292 was available through the updated Windows PATH; the running parent
process retained its old PATH, so the standalone WinGet executable was used directly.
Inference authentication was unavailable. No authenticated acceptance session ran.

The following are actual native instruction-loading observations from unauthenticated
local `/context` commands, not static simulations or model claims. Each returned
local_command=context, duration_api_ms=0 and num_turns=0. They do not constitute
authenticated client acceptance and must not be dismissed as authentication failures.

The fixture was a disposable Git repository with root CLAUDE importing root AGENTS,
an installed module/custom tree, the two source payloads and the publisher override.
Only the root `.claude/settings.json` contained the two exclusions. Session `--settings`
files selected the default or combined mode without copying root exclusions into them.

| Mode / startup | Root AGENTS | Root CLAUDE | Source AGENTS | Source CLAUDE | Observation |
|---|---|---|---|---|---|
| default / root | yes | yes | no | no | startup case passed only |
| default / package source | no | yes | no | no | root guidance missing |
| default / source Claude directory | no | yes | no | yes | root guidance missing; source bridge loaded |
| default / package descendant | no | yes | no | no | root guidance missing |
| combined / root | yes | yes | no | no | startup case passed only |
| combined / package source | yes | yes | yes | no | source router loaded |
| combined / source Claude directory | yes | yes | yes | yes | both source payloads loaded |
| combined / package descendant | yes | yes | yes | no | source router loaded |

Claude never loaded the Codex override. Nested debug output attempted project settings
at the startup directory's .claude/settings.json rather than demonstrating application
of the root exclusions. This is an observed discrepancy, not a proven causal diagnosis.
Earlier 2.1.296 bundled-client probes also exposed nested failures. Explicitly forwarding
exclusions suppressed source AGENTS in a combined nested probe, but did not establish
root AGENTS import in default nested probes; it is not a complete verified workaround.

Reproduction uses the actual CLI with the fixture's selected startup directory:

```powershell
claude -p /context --permission-mode plan --permission-prompts none --tools Read `
    --strict-mcp-config --setting-sources project,local --settings $modeSettings `
    --no-session-persistence --output-format json --debug-file $debugLog
```

For 2.1.292, $modeSettings contains only
`{"pluginConfigs":{"cc-plugin-agents-md@builtin":{"options":{"instructionFiles":"claude-md-or-agents-md"}}}}`
or the combined value `claude-md-and-agents-md`. Saved reproduction artifacts were
`claude-standalone-<mode>-<location>-result.json`, corresponding debug logs and
`claude-standalone-startup-evidence.json` in the disposable preflight directory.

Do not treat root startup as proof of complete isolation: source-file access may
discover nested instructions later. Until resolved, maintain publisher package sources
with Codex or another independently validated workflow. No root-only launch workaround
or alternative architecture has been adopted.

## Deferred authenticated Claude acceptance gate

Before declaring affected Claude contexts fully compatible, record version,
authentication availability, actual effective settings/mode, startup directory and
observable native loading for all supported combinations:

1. Workflows root startup and installed CLAUDE with its unchanged @AGENTS.md import.
2. Package source root, source Claude directory and deeper source startup locations.
3. Source-file access from a root-started session, including both source entrypoints.
4. Both claude-md-or-agents-md and claude-md-and-agents-md modes where supported.
5. Suppression of both source payloads while installed root guidance remains effective.
6. Preservation of unrelated project instructions, custom companions and CLAUDE.local.
7. Resolution or an explicitly documented compatibility restriction for every observed
   nested failure; unsupported contexts must be reported, not marked passed.

Use supported isolated/session settings without changing personal/machine settings.
Distinguish automatic activation from explicit data reads and avoid relying only on
model self-report. Static JSON, glob matching and unauthenticated `/context` observations
cannot satisfy authenticated acceptance. Report core implementation pass/fail separately
from Claude native compatibility pending.
