from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    ManifestError,
    default_rules_path,
    default_schema_path,
    emit_output,
    log_error,
    log_info,
    validate_and_normalize_manifest,
    write_normalized_manifest,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate and normalize a sync-files-from-manifest manifest."
    )
    manifest_source = parser.add_mutually_exclusive_group(required=True)
    manifest_source.add_argument("--manifest-json", help="Raw JSON manifest string.")
    manifest_source.add_argument(
        "--manifest-json-env",
        help="Name of an environment variable containing the raw JSON manifest string.",
    )
    manifest_source.add_argument(
        "--manifest-json-file",
        help="Path to a file containing the raw JSON manifest string.",
    )
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
    parser.add_argument(
        "--schema-path",
        default=str(default_schema_path()),
        help="Path to the authoritative JSON Schema bundled with the reusable workflow.",
    )
    parser.add_argument(
        "--rules-path",
        default=str(default_rules_path()),
        help="Path to the declarative semantic rule configuration.",
    )
    return parser.parse_args()


def read_manifest_json(args: argparse.Namespace) -> str:
    if args.manifest_json is not None:
        return args.manifest_json

    if args.manifest_json_env is not None:
        import os

        value = os.getenv(args.manifest_json_env)
        if value is None:
            raise ManifestError(f"Environment variable '{args.manifest_json_env}' is not set.")
        return value

    return Path(args.manifest_json_file).read_text(encoding="utf-8")


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    normalized_manifest_path = Path(args.normalized_manifest_path).resolve()
    manifest_json = read_manifest_json(args)

    entries = validate_and_normalize_manifest(
        manifest_json=manifest_json,
        repo_root=repo_root,
        schema_path=Path(args.schema_path).resolve(),
        rules_path=Path(args.rules_path).resolve(),
    )
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
