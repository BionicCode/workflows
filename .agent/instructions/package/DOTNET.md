---
Version: 2
Created: 2026-10-13T20:27:24+00:00
Updated: 2026-10-24T21:52:05+00:00
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

# .NET and Visual Studio instructions

## Scope

These instructions apply to .NET / Visual Studio code, projects, solutions, SDKs, MSBuild, packages, analyzers, and their validation, regardless of the current working directory. The root router loads them explicitly. User instructions and the root precedence rules apply. Established repository layout and concrete local configuration take precedence over the template defaults below.

## Repository contract files
Before planning, editing, or validating .NET code, inspect the repository files that can change effective build, analysis, test, packaging, and language behavior.

Check these when present:
- `/.editorconfig`
- `/Directory.Build.props`
- `/Directory.Build.targets`
- `/Directory.Packages.props`
- `/global.json`
- relevant `*.sln`, `*.csproj`, `*.props`, `*.targets`, and repository build/test scripts

Do not assume project files tell the full story when shared repository-level configuration exists.

Important:
- Treat `Directory.Build.props` and `Directory.Build.targets` as part of the effective project definition.
- If repository-level settings conflict with local assumptions, follow the effective repository configuration instead of generic .NET defaults.

---

## Command policy
Prefer repository-local or task-local scope over whole-repo commands when possible.
Prefer repository-provided scripts or wrappers when they are the documented validation path.

These commands do not authorize builds, tests, or formatters in review-only or planning-only work.

Typical .NET command sequence:

```bash
# If restore is required
 dotnet restore <solution-or-project>

# Verify style/analyzer compliance without applying fixes
 dotnet format <solution-or-project> --no-restore --verify-no-changes

# If necessary, repair only authorized changes and repeat verification above.

# Build the test project or containing solution, including its dependencies
 dotnet build <test-project-or-containing-solution> --no-restore

# Smallest relevant test scope, after that scope has been built
 dotnet test <test-project-or-containing-solution> --no-build

# After any later formatter/analyzer mutation, repeat affected build/test checks.
```

Rules:
- Verification-only formatting is sufficient when no repair is needed. Do not mutate files merely because an implementation task occurred.
- Apply formatter or analyzer fixes only when necessary within authorized implementation scope. Protect unrelated files and unrelated dirty hunks; file filters alone do not protect dirty hunks within included files.
- Fix task-caused diagnostics; verification is not permission to ignore them. Evidence-supported unrelated failures do not authorize broad cleanup.
- Rebuild and rerun affected validation after any formatter or analyzer mutation so results describe the final source state.
- If `--no-restore` fails because restore has not yet happened, run restore once and continue.
- If tests fail, do not stop at the first red run. Investigate, fix, and rerun the smallest relevant build/test scope until the targeted tests pass or a concrete blocker prevents further progress.
- Treat red tests caused by your changes as part of the task, not as optional follow-up work.
- If a test is broken for reasons unrelated to your change, identify the evidence clearly and continue validating the remaining relevant scope where possible.
- If the repo uses a different validation entry point, such as scripts, CI wrappers, `Makefile` targets, or PowerShell helpers, prefer that path and mention it in the report.
- Never finish an implementation task while knowingly leaving newly introduced analyzer/style violations unresolved unless the user explicitly allows it.
- Never finish an implementation task while knowingly leaving newly failing relevant tests unresolved unless the user explicitly allows it or you have hit a concrete blocker that you report.

---

## .editorconfig and analyzer compliance
Treat `.editorconfig`, analyzer configuration, and project analysis settings as part of the repository contract.

For .NET repositories:
- Assume `.editorconfig` is authoritative for whitespace, code style, naming, and analyzer configuration.
- Respect warnings and errors from SDK analyzers and any repository-installed analyzers.
- Prefer fixing the code over suppressing the diagnostic.
- If a violation appears to be a false positive, document it and use the narrowest justified suppression only if the user allows repository rule exceptions.

Important:
- Command-line `dotnet build` does not automatically enforce all IDE code-style diagnostics unless the project enables build enforcement for code-style analysis.
- Therefore, for implementation tasks, do not rely on build alone to prove `.editorconfig` compliance. Use the established repository validation path, or `dotnet format --verify-no-changes`, with necessary repairs constrained by the command policy above.
- If the repository expects IDE-style rules to fail on build, honor project-level enforcement such as `EnforceCodeStyleInBuild`, `TreatWarningsAsErrors`, `AnalysisLevel`, and related settings when they are configured in shared props/targets files.

---

## Naming and readability expectations
Follow `.editorconfig` naming rules exactly, but do not stop there.

Also apply these readability rules:
- Prefer intention-revealing names for types, members, locals, parameters, lambda parameters, and type parameters.
- Avoid cryptic or low-information abbreviations when a descriptive name materially improves readability.
- Prefer names such as `count`, `index`, `file`, `directory`, `entry`, `item`, `message`, `result`, or `cancellationToken` over names such as `cnt`, `idx`, `f`, `dir`, `e`, `x`, `msg`, or `ct` unless the shorter form is a well-established domain term.
- Name lambda parameters after the role or item being processed so readers do not need to inspect surrounding types just to infer what is being enumerated.
- Use comments to explain intent, invariants, caveats, or trade-offs, not to compensate for poor naming.
- Improve names, structure, or method extraction before adding explanatory comments for code that is only hard to read because the naming is weak.

---

## Design expectations for .NET code
In addition to repository-wide engineering rules:
- Prefer cohesive types with clear responsibilities.
- Apply single-responsibility thinking when adding or refactoring classes and methods.
- Keep public APIs explicit and unsurprising.
- Avoid leaking infrastructure, UI, serialization, SDK, or persistence concerns across boundaries unless the repository design clearly requires it.
- Prefer constructor injection and explicit dependencies over hidden global state when the repository uses dependency injection.
- Keep extension methods, helpers, and utility classes narrowly scoped and domain-appropriate; do not use them to hide poor design.

---

## Documentation expectations
Follow [DOCUMENTATION](DOCUMENTATION.md) for language-neutral source comments, API
contract details, consumer guidance and stale-documentation safeguards. The language-specific
syntax and XML requirements below apply to relevant .NET APIs.

### C# source comments
For C# code, prefer single-line `//` comments over block comments when appropriate.
Use comments for non-obvious intent rather than restating syntax. These examples
illustrate comment quality, not verified behavior of the adopting repository.

Bad:
```csharp
// Checks if the sequence is empty.
if (!items.Any())
{
    ...
}
```

Good:
```csharp
// Materialize once because upstream enumeration is stateful and may read from a forward-only FIT stream.
var records = source.ToList();
```

Good:
```csharp
// Keep the original field order because downstream CSV consumers compare columns positionally.
```

Use contextual TODO/HACK markers rather than unexplained placeholders.

Better:
```csharp
// TODO: Preserve developer field units once the SDK decoder exposes the original scale metadata.
```

Worse:
```csharp
// TODO: Fix this.
```

### XML documentation comments for applicable .NET APIs
For languages supporting .NET XML documentation comments, document public types and public members at a minimum. Also document protected or extension-oriented members when callers are expected to depend on them.

When XML docs are required:
- new public classes, records, structs, interfaces, enums, and delegates,
- new public constructors, methods, properties, events, and fields,
- changed public behavior,
- changed nullability, exception behavior, units, ordering guarantees, or mutation semantics.

Minimum XML documentation quality:
- Every documented API should have a clear `<summary>`.
- Use complete sentences.
- Document each parameter with `<param>` when parameters are non-trivial or behavior depends on them.
- Use `<returns>` for methods and properties where the return meaning is not already obvious.
- Use `<exception>` for meaningful documented exceptions.
- Use `<remarks>` for caveats, ordering guarantees, performance notes, mutability, threading, or format constraints.
- Use `<example>` when a short usage snippet materially helps consumers.

Prefer semantic XML tags over plain text:
- Use `<see cref="T:Namespace.TypeName"/>` or `<see cref="MemberName"/>` for code references.
- Use `<paramref name="value"/>` for parameter references.
- Use `<typeparamref name="T"/>` for generic type parameters.
- Use `<c>` for inline code and `<code>` for multi-line code.
- Use `<see langword="null"/>`, `<see langword="true"/>`, and similar language keywords instead of quoted plain text where appropriate.

Examples:

```csharp
/// <summary>
/// Tries to locate the session message that best represents the completed activity.
/// </summary>
/// <param name="messages">The decoded FIT messages in source order.</param>
/// <returns>
/// The selected session message, or <see langword="null"/> when the FIT file does not contain session data.
/// </returns>
/// <remarks>
/// When multiple session messages are present, the implementation currently prefers the last complete message.
/// This matches Garmin export behavior observed in the repository test data but may require revision for multi-sport activities.
/// </remarks>
public static SessionMesg? TryGetPrimarySession(IReadOnlyList<Mesg> messages)
```

```csharp
/// <summary>
/// Gets the average speed in meters per second.
/// </summary>
/// <remarks>
/// The value is the decoded FIT session field value before any user-facing unit conversion.
/// </remarks>
public double AverageSpeedMetersPerSecond { get; }
```

Avoid weak summaries such as:
- “Gets or sets the value.”
- “Initializes a new instance.” without saying what the type represents.
- “Does processing.”

If the repository enables XML documentation file generation, keep public XML docs warning-free.

---

## Test project conventions
When adding or generating new automated tests for this repository:
- place test projects under `/test` at repository root,
- create `/test` if it does not already exist,
- and name generated unit test projects `<SolutionName>.Tests` unless the repository already defines a stricter convention.

---

## Reporting requirements for implementation tasks
When you changed code, report:
- what you changed,
- which commands you ran,
- whether build passed,
- whether tests passed,
- whether formatting/analyzer verification passed,
- whether documentation was updated and at what level,
- and any remaining warnings/errors or blockers with a reason.

## .NET asynchronous tests
- Prefer `Task` and `Task<T>`-based test flows; avoid `async void` in test code except where the framework explicitly requires it.
- Name generated unit test projects `<SolutionName>.Tests` unless the repository defines a more specific test-project naming convention.
