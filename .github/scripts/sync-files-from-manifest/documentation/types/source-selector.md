# SourceSelector

`SourceSelector` is the source-selection field group on [`ManifestEntry`](manifest-entry.md).

## Placement

| Property | Value |
|---|---|
| Placement | Entry field group |
| Valid parent | [`ManifestEntry`](manifest-entry.md) |
| Parent properties | `source_path`, `source_glob`, `glob` |

## Attributes

| Attribute | Required | Type | Description |
|---|---:|---|---|
| `source_path` | Conditional | [`RepoRelativeFilePath`](repo-relative-file-path.md) | Exact source file path. Required when `source_glob` is absent. Wildcards are not interpreted. |
| `source_glob` | Conditional | string | Repository-relative POSIX glob pattern. Required when `source_path` is absent. |
| `glob` | No | object | Options for `source_glob`. Forbidden for exact `source_path` entries. |
| `glob.recursive` | No | boolean | Defaults to `false`. Allows `**` as zero or more complete path segments when `true`. |
| `glob.include_hidden` | No | boolean | Defaults to `false`. Allows wildcard segments to match dot-prefixed path segments broadly when `true`. |

## `source_path`

`source_path` selects exactly one source file. It remains exact-file only. Wildcards are not interpreted in `source_path`; use `source_glob` for patterns.

## `source_glob`

`source_glob` selects many source files and expands them into exact-file sync operations before verify or sync planning.

Rules:

- Exactly one of `source_path` or `source_glob` is required.
- `source_glob` must be repository-relative and use `/` separators.
- `source_glob` must contain at least one glob metacharacter: `*`, `?`, or `[`.
- `source_glob` without metacharacters is rejected; use `source_path` for exact-file sync.
- `target_path` must end with `/` for `source_glob` entries.
- Relative layout below the glob base directory is preserved.
- Unmatched target files are not deleted.

`*`, `?`, and character classes match within a single path segment. `**` is allowed only when `glob.recursive` is `true`, and it matches zero or more complete path segments.

## Hidden Matching

- `glob.include_hidden: false` prevents wildcard segments from implicitly matching dot-prefixed path segments.
- Explicitly named dot segments such as `.github` are allowed.
- A pattern segment starting with `.` may match dot-prefixed names for that segment only.
- `glob.include_hidden: true` broadly allows wildcard segments to match hidden path segments.

Examples:

- `.github/scripts/**/*.md` is allowed with `include_hidden: false` because `.github` is explicit.
- `**/*.md` does not traverse `.github` when `include_hidden: false`.
- `docs/*.md` does not match `docs/.hidden.md` when `include_hidden: false`.
- `docs/.*.md` may match dot-prefixed files in `docs`.

## Matching Caveat

`*.*` only matches names containing a dot. Use `*` for all files, `*.md` for Markdown files, and `**/*.md` with `glob.recursive: true` for recursive Markdown sync.
