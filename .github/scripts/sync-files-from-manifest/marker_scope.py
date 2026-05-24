from __future__ import annotations

from dataclasses import dataclass

from common import ManifestEntry, ManifestError


MANAGED_SCOPE_INSIDE_MARKERS = "inside_markers"
MANAGED_SCOPE_OUTSIDE_MARKERS = "outside_markers"
INSIDE_TARGET_MARKERS_REQUIRED_MESSAGE = (
    "inside_markers requires target marker blocks because source-owned content inside the markers must be enforced."
)
OUTSIDE_PARTIAL_MARKERS_MESSAGE = (
    "Target contains a partial set of marker blocks. Either keep all source-defined marker blocks, "
    "remove all target-owned marker blocks, or add marker IDs in a future manifest version."
)


@dataclass(frozen=True)
class TextSlice:
    start: int
    end: int
    text: str


@dataclass(frozen=True)
class TextLocation:
    line: int
    column: int
    offset: int


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


def text_location(text: str, offset: int) -> TextLocation:
    """Return 1-based line/column for a decoded-text character offset.

    Column is a Unicode code-point index within the line, not a visual display
    column and not a UTF-16 column. CRLF, bare LF, and bare CR each count as one
    newline sequence.
    """
    bounded_offset = max(0, min(offset, len(text)))
    line = 1
    column = 1
    position = 0

    while position < bounded_offset:
        character = text[position]
        if character == "\r":
            if position + 1 < len(text) and text[position + 1] == "\n":
                position += 2
            else:
                position += 1
            line += 1
            column = 1
            continue
        if character == "\n":
            position += 1
            line += 1
            column = 1
            continue

        position += 1
        column += 1

    return TextLocation(line=line, column=column, offset=offset)


def format_text_location(text: str, offset: int) -> str:
    location = text_location(text, offset)
    return f"line {location.line}, column {location.column}, char offset {location.offset}"


def format_block_start_locations(role: str, parsed: ParsedMarkerContent) -> str:
    if not parsed.blocks:
        return f"{role} marker block starts: none"
    locations = ", ".join(
        f"#{block.index} at {format_text_location(parsed.text, block.start_delimiter.start)}"
        for block in parsed.blocks
    )
    return f"{role} marker block starts: {locations}"


def _marker_error(
    entry: ManifestEntry,
    role: str,
    message: str,
    occurrence_index: int | None = None,
    *,
    text: str | None = None,
    offset: int | None = None,
    expected_start_marker: str | None = None,
    expected_end_marker: str | None = None,
) -> ManifestError:
    occurrence = ""
    if occurrence_index is not None:
        occurrence = f" at marker occurrence {occurrence_index}"
    location = ""
    if text is not None and offset is not None:
        location = f" at {format_text_location(text, offset)}"
    expected = ""
    if expected_start_marker is not None and expected_end_marker is not None:
        expected = (
            f" Searched {role} content for exact start marker {expected_start_marker!r} "
            f"and exact end marker {expected_end_marker!r}; content length is "
            f"{len(text) if text is not None else 0} character(s)."
        )
    return ManifestError(
        f"{entry.describe()} marker parse error in {role} content for target_path "
        f"'{entry.target_path}' with managed_scope '{entry.managed_scope}'{occurrence}"
        f"{location}: {message}{expected}"
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
            f"with managed_scope '{entry.managed_scope}' as strict UTF-8 at byte offset "
            f"{exc.start}..{exc.end}: {exc}."
        ) from exc


def encode_marker_text(content: str, entry: ManifestEntry) -> bytes:
    try:
        return content.encode(encoding="utf-8", errors="strict")
    except UnicodeEncodeError as exc:
        raise ManifestError(
            f"{entry.describe()} cannot encode composed marker-scoped content for target_path "
            f"'{entry.target_path}' with managed_scope '{entry.managed_scope}' as strict UTF-8: {exc}."
        ) from exc


def parse_marker_text(
    text: str,
    entry: ManifestEntry,
    role: str,
    *,
    require_blocks: bool = True,
) -> ParsedMarkerContent:
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
                text=text,
                offset=next_end,
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
            raise _marker_error(
                entry,
                role,
                "found a start marker without a matching end marker.",
                next_occurrence,
                text=text,
                offset=start_begin,
            )

        nested_start = text.find(start_marker, start_end)
        if nested_start != -1 and nested_start < end_begin:
            raise _marker_error(
                entry,
                role,
                "found a nested start marker before the matching end marker.",
                next_occurrence,
                text=text,
                offset=nested_start,
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

    if require_blocks and not blocks:
        message = "found no exact marker blocks."
        if role == "target" and entry.managed_scope == MANAGED_SCOPE_INSIDE_MARKERS:
            message = INSIDE_TARGET_MARKERS_REQUIRED_MESSAGE
        raise _marker_error(
            entry,
            role,
            message,
            1,
            text=text,
            expected_start_marker=start_marker,
            expected_end_marker=end_marker,
        )

    return ParsedMarkerContent(
        role=role,
        text=text,
        outside_segments=outside_segments,
        blocks=blocks,
    )


def parse_marker_bytes(
    content: bytes,
    entry: ManifestEntry,
    role: str,
    *,
    require_blocks: bool = True,
) -> ParsedMarkerContent:
    return parse_marker_text(decode_marker_bytes(content, entry, role), entry, role, require_blocks=require_blocks)


def validate_source_marker_blocks(source_bytes: bytes, entry: ManifestEntry) -> None:
    parse_marker_bytes(source_bytes, entry, "source")


def _assert_matching_block_counts(
    source: ParsedMarkerContent,
    target: ParsedMarkerContent,
    entry: ManifestEntry,
) -> None:
    if len(source.blocks) == len(target.blocks):
        return

    if entry.managed_scope == MANAGED_SCOPE_OUTSIDE_MARKERS and not target.blocks:
        return

    if entry.managed_scope == MANAGED_SCOPE_INSIDE_MARKERS:
        raise ManifestError(
            f"{entry.describe()} marker block count mismatch for target_path '{entry.target_path}' "
            f"with managed_scope '{entry.managed_scope}': source has {len(source.blocks)} block(s), "
            f"target has {len(target.blocks)} block(s). "
            f"{format_block_start_locations('source', source)}; "
            f"{format_block_start_locations('target', target)}. "
            f"{INSIDE_TARGET_MARKERS_REQUIRED_MESSAGE}"
        )

    raise ManifestError(
        f"{entry.describe()} marker block count mismatch for target_path '{entry.target_path}' "
        f"with managed_scope '{entry.managed_scope}': source has {len(source.blocks)} block(s), "
        f"target has {len(target.blocks)} block(s). "
        f"{format_block_start_locations('source', source)}; "
        f"{format_block_start_locations('target', target)}. "
        f"{OUTSIDE_PARTIAL_MARKERS_MESSAGE}"
    )


def compose_source_outside_projection(source: ParsedMarkerContent) -> str:
    return "".join(segment.text for segment in source.outside_segments)


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
        if not target.blocks:
            return compose_source_outside_projection(source)

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
    target = parse_marker_bytes(
        target_bytes,
        entry,
        "target",
        require_blocks=entry.managed_scope != MANAGED_SCOPE_OUTSIDE_MARKERS,
    )
    return encode_marker_text(compose_marker_scoped_text(source, target, entry), entry)
