from __future__ import annotations

from dataclasses import dataclass

from common import ManifestEntry, ManifestError


MANAGED_SCOPE_INSIDE_MARKERS = "inside_markers"
MANAGED_SCOPE_OUTSIDE_MARKERS = "outside_markers"


@dataclass(frozen=True)
class TextSlice:
    start: int
    end: int
    text: str


@dataclass(frozen=True)
class MarkerBlock:
    index: int
    start_delimiter: TextSlice
    inner: TextSlice
    end_delimiter: TextSlice


@dataclass(frozen=True)
class ParsedMarkerContent:
    role: str
    text: str
    outside_segments: list[TextSlice]
    blocks: list[MarkerBlock]


def is_marker_scope(entry: ManifestEntry) -> bool:
    return entry.managed_scope in {MANAGED_SCOPE_INSIDE_MARKERS, MANAGED_SCOPE_OUTSIDE_MARKERS}


def _marker_error(
    entry: ManifestEntry,
    role: str,
    message: str,
    occurrence_index: int | None = None,
) -> ManifestError:
    occurrence = ""
    if occurrence_index is not None:
        occurrence = f" at marker occurrence {occurrence_index}"
    return ManifestError(
        f"{entry.describe()} marker parse error in {role} content for target_path "
        f"'{entry.target_path}' with managed_scope '{entry.managed_scope}'{occurrence}: {message}"
    )


def _require_markers(entry: ManifestEntry) -> tuple[str, str]:
    if entry.markers is None:
        raise ManifestError(f"{entry.describe()} requires markers for managed_scope '{entry.managed_scope}'.")
    return entry.markers.start, entry.markers.end


def decode_marker_bytes(content: bytes, entry: ManifestEntry, role: str) -> str:
    try:
        return content.decode(encoding="utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ManifestError(
            f"{entry.describe()} cannot decode {role} content for target_path '{entry.target_path}' "
            f"with managed_scope '{entry.managed_scope}' as strict UTF-8: {exc}."
        ) from exc


def encode_marker_text(content: str, entry: ManifestEntry) -> bytes:
    try:
        return content.encode(encoding="utf-8", errors="strict")
    except UnicodeEncodeError as exc:
        raise ManifestError(
            f"{entry.describe()} cannot encode composed marker-scoped content for target_path "
            f"'{entry.target_path}' with managed_scope '{entry.managed_scope}' as strict UTF-8: {exc}."
        ) from exc


def parse_marker_text(text: str, entry: ManifestEntry, role: str) -> ParsedMarkerContent:
    start_marker, end_marker = _require_markers(entry)
    position = 0
    outside_start = 0
    outside_segments: list[TextSlice] = []
    blocks: list[MarkerBlock] = []

    while position < len(text):
        next_start = text.find(start_marker, position)
        next_end = text.find(end_marker, position)
        next_occurrence = len(blocks) + 1

        if next_end != -1 and (next_start == -1 or next_end < next_start):
            raise _marker_error(
                entry,
                role,
                "found an end marker before a matching start marker.",
                next_occurrence,
            )

        if next_start == -1:
            break

        outside_segments.append(
            TextSlice(outside_start, next_start, text[outside_start:next_start])
        )

        start_begin = next_start
        start_end = start_begin + len(start_marker)
        end_begin = text.find(end_marker, start_end)
        if end_begin == -1:
            raise _marker_error(entry, role, "found a start marker without a matching end marker.", next_occurrence)

        nested_start = text.find(start_marker, start_end)
        if nested_start != -1 and nested_start < end_begin:
            raise _marker_error(
                entry,
                role,
                "found a nested start marker before the matching end marker.",
                next_occurrence,
            )

        end_end = end_begin + len(end_marker)
        blocks.append(
            MarkerBlock(
                index=next_occurrence,
                start_delimiter=TextSlice(start_begin, start_end, text[start_begin:start_end]),
                inner=TextSlice(start_end, end_begin, text[start_end:end_begin]),
                end_delimiter=TextSlice(end_begin, end_end, text[end_begin:end_end]),
            )
        )
        position = end_end
        outside_start = end_end

    outside_segments.append(TextSlice(outside_start, len(text), text[outside_start:]))

    if not blocks:
        raise _marker_error(entry, role, "found no exact marker blocks.", 1)

    return ParsedMarkerContent(
        role=role,
        text=text,
        outside_segments=outside_segments,
        blocks=blocks,
    )


def parse_marker_bytes(content: bytes, entry: ManifestEntry, role: str) -> ParsedMarkerContent:
    return parse_marker_text(decode_marker_bytes(content, entry, role), entry, role)


def validate_source_marker_blocks(source_bytes: bytes, entry: ManifestEntry) -> None:
    parse_marker_bytes(source_bytes, entry, "source")


def _assert_matching_block_counts(
    source: ParsedMarkerContent,
    target: ParsedMarkerContent,
    entry: ManifestEntry,
) -> None:
    if len(source.blocks) != len(target.blocks):
        raise ManifestError(
            f"{entry.describe()} marker block count mismatch for target_path '{entry.target_path}' "
            f"with managed_scope '{entry.managed_scope}': source has {len(source.blocks)} block(s), "
            f"target has {len(target.blocks)} block(s)."
        )


def compose_marker_scoped_text(
    source: ParsedMarkerContent,
    target: ParsedMarkerContent,
    entry: ManifestEntry,
) -> str:
    _assert_matching_block_counts(source, target, entry)

    pieces: list[str] = []
    if entry.managed_scope == MANAGED_SCOPE_INSIDE_MARKERS:
        for block_index, source_block in enumerate(source.blocks):
            target_block = target.blocks[block_index]
            pieces.append(target.outside_segments[block_index].text)
            pieces.append(target_block.start_delimiter.text)
            pieces.append(source_block.inner.text)
            pieces.append(target_block.end_delimiter.text)
        pieces.append(target.outside_segments[-1].text)
        return "".join(pieces)

    if entry.managed_scope == MANAGED_SCOPE_OUTSIDE_MARKERS:
        for block_index, target_block in enumerate(target.blocks):
            pieces.append(source.outside_segments[block_index].text)
            pieces.append(target_block.start_delimiter.text)
            pieces.append(target_block.inner.text)
            pieces.append(target_block.end_delimiter.text)
        pieces.append(source.outside_segments[-1].text)
        return "".join(pieces)

    raise ManifestError(f"{entry.describe()} does not use a marker-scoped managed_scope.")


def compose_marker_scoped_bytes(source_bytes: bytes, target_bytes: bytes, entry: ManifestEntry) -> bytes:
    source = parse_marker_bytes(source_bytes, entry, "source")
    target = parse_marker_bytes(target_bytes, entry, "target")
    return encode_marker_text(compose_marker_scoped_text(source, target, entry), entry)
