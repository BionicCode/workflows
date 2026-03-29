from __future__ import annotations

import argparse
from pathlib import Path

from common import ManifestError, emit_output, log_error, log_info, normalize_manifest, write_normalized_manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate and normalize a sync-files-from-manifest manifest."
    )
    parser.add_argument("--manifest-json", required=True, help="Raw JSON manifest string.")
    parser.add_argument(
        "--repo-root",
        required=True,
        help="Absolute path to the checked-out caller repository.",
    )
    parser.add_argument(
        "--normalized-manifest-path",
        required=True,
        help="Destination path for the normalized manifest JSON file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    normalized_manifest_path = Path(args.normalized_manifest_path).resolve()

    entries = normalize_manifest(args.manifest_json, repo_root)
    write_normalized_manifest(entries, normalized_manifest_path)

    emit_output("normalized_manifest_path", normalized_manifest_path.as_posix())
    emit_output("manifest_entry_count", str(len(entries)))
    log_info(
        f"Validated {len(entries)} manifest entries and wrote normalized manifest to {normalized_manifest_path}."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ManifestError as exc:
        log_error(str(exc))
        raise SystemExit(1) from exc
    except Exception as exc:  # pragma: no cover - defensive guard for workflow logs
        log_error(f"Unexpected manifest validation failure: {exc}")
        raise SystemExit(1) from exc
