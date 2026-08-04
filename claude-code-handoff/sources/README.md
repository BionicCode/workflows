# Recovered handoff sources

## Role and authority

This directory preserves selected historical evidence recovered on 2026-08-04 from the user-supplied ChatGPT transfer export. These files are evidence inputs, not current repository instructions, execution leases, task prompts, maintainer acceptance, or automatic write authority. Discovering or reading them authorizes nothing.

The user states that `W1-final-audit-report.txt` is the exported original final response from the W1 ChatGPT task. The hashes below prove identity with the supplied export, not authorship, originality, or historical authenticity. Authenticate that report against the W1 contract, Git objects, baseline tree, and later closure evidence before relying on it as the historical W1 result.

## Supplied package

| Item | Classification | Integrity evidence | Repository treatment |
|---|---|---|---|
| `template-visual-studio-sync-automation-memory-context-dump.zip` | User-supplied transfer package; external input | SHA-256 `0173a3352f6452feae17cae0698fbd48f57d24ddfd8bb037952b10b06bb28c2d`; 12 readable entries; ZIP integrity check found no bad entry | Not vendored as a monolith. Four selected text sources are preserved below. |
| `complete-chatgpt-memory-and-project-context-dump-for-codex.md` | Convenience aggregate of the ZIP's `00` through `06` synthesis documents; external input | SHA-256 `5b17cd6bcc8ad93e2e91bde62cbba2635dba93c7f8689d7e978dca90ad16319e`; each of the seven synthesis documents was found verbatim in the aggregate | Not vendored because it duplicates synthesis prose and is not primary evidence. |
| `sources/W1-execution-handoff.pdf` inside the ZIP | Historical W1 task contract, not the final report | SHA-256 `14b0f7a3bfbe2b7584cdcf961ff49237259b8a652e1923337e4d97e9829d61cc` | Not vendored. It remains an external binary source that a review must verify from the supplied ZIP or another user-authorized copy. |

The filenames above identify external transfer inputs. Their presence on one machine is a dated observation, not a portable path or an instruction to search outside an authorized workspace.

## Vendored files and byte identity

| Vendored file | Evidence classification | ZIP-entry SHA-256 | Installed SHA-256 | Identity result |
|---|---|---|---|---|
| [`W1-final-audit-report.txt`](W1-final-audit-report.txt) | User-supplied exported-original candidate; historical W1 result requiring authentication | `4afa74679b22197a392341750235767e598f74a756e4b0b84cff85e842a69129` | `5e7a9647c416b8e0f3f43b84f56ab9db5b92f06403662a30e011d782b746f0b1` | LF-normalized line-sequence identity; installed copy has one added terminal LF. |
| [`W1-planning-and-handoff.txt`](W1-planning-and-handoff.txt) | Historical planning evidence; contains the later erroneous reconstructed allowlist and an explicit stop-on-discrepancy rule | `018c70188233e01b6377d6e8ac24cf35c623352c1ed57f5be4dd17aff6c3cee4` | `c4576c38299720ca42f1f2e639063822a9849d2b438bfcd67116d8f546f1f75c` | LF-normalized line-sequence identity; installed copy has one added terminal LF. |
| [`backlog-governance-acceptance-review.txt`](backlog-governance-acceptance-review.txt) | Historical acceptance review; useful for reviewed governance structure, but its W2-allowlist acceptance missed source fidelity and is superseded | `63460caabed3ea92704ba364cd111208ec4137f704621b68c50bf08184793f2a` | `545b1fec31a1dc787d877ecfd8ca3c83637ecc9bd376837c821ebb541a2125ec` | LF-normalized line-sequence identity; installed copy has one added terminal LF. |
| [`independent-technical-strategy-review.md`](independent-technical-strategy-review.md) | Historical independent review; later-pass recommendations remain non-binding, while its “activate W2 unchanged” conclusion is superseded | `c4fae94e4e875122b195b9e8b9b1a9c86a49aeaea2eb5cba5100901bb74ee683` | `c4fae94e4e875122b195b9e8b9b1a9c86a49aeaea2eb5cba5100901bb74ee683` | Exact raw-byte match. |

All four ZIP entries are UTF-8 without a byte-order mark and use LF line endings. The first three end immediately after their final text character. The required `apply_patch` installation path added a terminal LF to those files; no body line, line order, Unicode scalar, or other line ending changed. Here, **LF-normalized line-sequence identity** means decoding as UTF-8, normalizing line separators to LF, and comparing the ordered lines while treating EOF after the final line as equivalent to one terminal LF. Both the ZIP-entry and installed hashes are retained so the limitation is visible rather than hidden.

The exact strategy-review source retains its original two-space Markdown hard breaks on header lines 3 through 5. A supplemental new-file whitespace check reports those three lines as trailing whitespace; removing them would break the required raw-byte identity. The installed hashes describe this local checkout immediately after reconciliation. Git reports no path-specific whitespace or line-ending attribute for these files, so later checkout tooling with automatic line-ending conversion may change working-tree bytes; revalidate the raw or normalized identity before relying on a later copy.

## Source precedence

For current action, use this order:

1. current explicit user authorization;
2. freshly resolved repository content and Git/runtime evidence;
3. applicable repository instructions and protected governance;
4. authenticated historical task contracts and accepted durable evidence;
5. this recovered source set;
6. synthesis documents, prior summaries, and commit messages.

Within this recovered set:

- the W1 execution-handoff PDF defines the historical task contract;
- an independently authenticated `W1-final-audit-report.txt` is the best evidence of the historical response and its proposed 16-path allowlist;
- `W1-planning-and-handoff.txt` is a later reconstruction and cannot override the authenticated report;
- the acceptance and strategy reviews remain evidence of what those reviews concluded, not proof that their missed W2-scope conclusion was correct.

No recovered artifact establishes the correct current W2 scope by itself. The protected backlog remains the intended roadmap and state authority, but its current W2 table is factually corrupted and blocked. A current scope requires authentication, post-W1/current-state review, explicit maintainer selection, a separately authorized protected correction, independent review, and a fresh valid execution lease.
