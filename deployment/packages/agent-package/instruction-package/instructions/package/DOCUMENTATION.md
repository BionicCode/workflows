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

# Documentation instructions

Read for documentation, comments, examples, instruction Markdown, or behavior changes that require documentation. These portable rules combine with the other files selected by the root router.

## Documentation and Comments
- Add meaningful code comments where names alone are not enough to explain intent, invariants, trade-offs, caveats, failure modes, unsupported scenarios, or non-obvious behavior.
- Prefer improving structure and naming before adding explanatory comments that compensate for avoidably unclear code.
- Do not add comments that merely restate the code.
- Use language-native API documentation comments for public or externally consumed APIs when the repository already uses them, or when you introduce or significantly change public surface area.
- Use correct documentation syntax and language-aware markup where supported.
- If a change introduces non-obvious API usage, data structures, workflow expectations, or extension points, add or update a small Markdown document in the repository's preferred documentation location as described in the [File System and Project Structure](ENGINEERING.md#file-system-and-project-structure) section.
- Keep documentation aligned with implemented behavior; stale documentation is a defect.

Follow the detailed documentation rules below.

## Purpose
This file defines repository documentation expectations for Codex and human contributors.

Documentation is part of the implementation. When behavior, public surface, or important design intent changes, update the relevant documentation in the same change.

---

## Documentation layers
Use the smallest documentation layer that fully explains the change:

1. **Source comments** for non-obvious implementation intent.
2. **Language-native API documentation** for API surface.
3. **Markdown documentation** for consumer guidance, data structures, workflows, behavior notes, and examples. Follow the established documentation layout; otherwise use the top-level `docs/` directory in the repository root. You can create a subfolder if appropriate. Governance instructions, local configuration, and agent bridges keep their established root, `.agent/`, and `.github/` locations.

Do not push everything into one layer.

---

## 1) Source comments inside code
Use the language-native source-comment syntax deliberately and only when the code would otherwise hide important intent.

Add source comments for:
- design rationale,
- invariants that must remain true,
- algorithm behavior that is not obvious from the code shape,
- performance-sensitive trade-offs,
- protocol or format quirks,
- caveats and limitations,
- deliberately unsupported scenarios,
- edge-case handling,
- risk boundaries or failure modes,
- and why a seemingly strange implementation is necessary.

Do **not** add comments that merely narrate obvious syntax or restate a good symbol name.

Comment style:
- Follow the language and repository comment-style conventions.
- Place the comment on its own line above the relevant code.
- Start with an uppercase letter.
- Keep comments concise but meaningful.
- When a limitation matters to callers or maintainers, state it explicitly.

Use `TODO`, `HACK`, or similar markers only when necessary, and include concrete context.

---

## 2) Language-native API documentation
Document public and externally consumed APIs using the language-native documentation
conventions, including protected or extension-oriented members on which callers depend.
Update documentation for new APIs and changes to public behavior, nullability, exceptions,
units, ordering guarantees or mutation semantics.

Use meaningful summaries and complete sentences. Explain non-trivial parameters, return
values, meaningful exceptions, invariants and caveats. Include examples when they materially
help callers; document performance, mutability, threading and format constraints when relevant.
Use language-aware references and markup where supported, following repository conventions.
Applicable .NET XML syntax and requirements belong in [DOTNET](DOTNET.md#documentation-expectations).

Avoid weak summaries such as "Gets or sets the value", "Initializes a new instance" without
explaining the type, or "Does processing". Keep documentation diagnostics warning-free when
the repository enables them.

---

## 3) Markdown documentation files
Add or update a small Markdown document when source comments and native API documentation are not enough for a consumer or maintainer to understand how to use the API or data model.

Typical triggers:
- a new library surface,
- a new workflow,
- non-obvious data structures,
- serialization or file-format behavior,
- mapping rules,
- extension points,
- or behavior that benefits from short examples.

A Markdown doc should usually include:
- purpose,
- where the entry points are,
- important types or data structures,
- key invariants or assumptions,
- usage examples,
- caveats or unsupported cases,
- and versioning or compatibility notes when relevant.

Keep it small and practical. Favor one focused document over a vague wall of text.

Suggested outline:

```md
# Feature or API name

## Purpose

## Entry points

## Data model / important types

## Usage examples

## Guarantees and caveats

## Limitations / unsupported scenarios
```

---

## Choosing the right level
Use this rule of thumb:
- **Would a maintainer misunderstand why the code looks this way?** Add a source comment.
- **Would a caller misunderstand how to use the API?** Add or update language-native API documentation.
- **Would a consumer need a bigger-picture explanation or example?** Add or update Markdown docs.

Often the correct answer is more than one layer.

---

## Documentation is part of done
For implementation tasks, documentation is part of done when relevant.

Before finishing, verify:
- comments explain non-obvious intent rather than narrate syntax,
- public APIs changed by the task have appropriate language-native documentation,
- keywords and code symbols use language-aware references and markup where supported,
- Markdown docs are updated when consumers need examples or data-model explanation,
- and no stale comments remain that contradict the implementation.
