from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    ManifestError,
    default_schema_path,
    default_template_path,
    emit_output,
    log_error,
    log_info,
)


CALLER_CONFIG_DIR = Path(".github/sync-config")
CALLER_SCHEMA_NAME = "sync-manifest.schema.json"
CALLER_MANIFEST_NAME = "sync-manifest.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize caller-owned managed-file sync configuration.")
    parser.add_argument(
        "--repo-root",
        required=True,
        help="Absolute path to the checked-out caller repository.",
    )
    parser.add_argument(
        "--schema-source",
        default=str(default_schema_path()),
        help="Authoritative schema file bundled with the reusable workflow.",
    )
    parser.add_argument(
        "--template-source",
        default=str(default_template_path()),
        help="Starter manifest template bundled with the reusable workflow.",
    )
    return parser.parse_args()


def read_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as exc:
        raise ManifestError(f"Unable to read '{path}': {exc}.") from exc


def write_if_changed(destination: Path, content: bytes) -> bool:
    if destination.exists() and destination.read_bytes() == content:
        return False

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    return True


def build_pr_body(changed_paths: list[str], manifest_created: bool) -> str:
    lines = [
        "Initialize managed-file sync configuration.",
        "",
        "Changed files:",
    ]
    lines.extend(f"- `{path}`" for path in changed_paths)

    if manifest_created:
        lines.extend(
            [
                "",
                "The starter manifest is intentionally minimal. "
                "Edit `.github/sync-config/sync-manifest.json` in the template repository "
                "to define the real managed-file defaults inherited by descendant repositories.",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "The existing caller-owned manifest was preserved and not overwritten.",
            ]
        )

    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    schema_source = Path(args.schema_source).resolve()
    template_source = Path(args.template_source).resolve()

    config_dir = repo_root / CALLER_CONFIG_DIR
    schema_destination = config_dir / CALLER_SCHEMA_NAME
    manifest_destination = config_dir / CALLER_MANIFEST_NAME

    changed_paths: list[str] = []
    schema_content = read_bytes(schema_source)
    template_content = read_bytes(template_source)

    if write_if_changed(schema_destination, schema_content):
        changed_paths.append((CALLER_CONFIG_DIR / CALLER_SCHEMA_NAME).as_posix())
        log_info(f"Created or updated caller schema at '{schema_destination}'.")
    else:
        log_info(f"Caller schema is already current at '{schema_destination}'.")

    manifest_created = False
    if manifest_destination.exists():
        log_info(f"Caller manifest already exists at '{manifest_destination}'; preserving it.")
    else:
        if write_if_changed(manifest_destination, template_content):
            changed_paths.append((CALLER_CONFIG_DIR / CALLER_MANIFEST_NAME).as_posix())
            manifest_created = True
            log_info(f"Created starter caller manifest at '{manifest_destination}'.")

    emit_output("changed", "true" if changed_paths else "false")
    emit_output("changed_count", str(len(changed_paths)))
    emit_output("changed_paths", "\n".join(changed_paths))
    emit_output("pull_request_body", build_pr_body(changed_paths, manifest_created))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ManifestError as exc:
        log_error(str(exc))
        raise SystemExit(1) from exc
    except Exception as exc:  # pragma: no cover - defensive guard for workflow logs
        log_error(f"Unexpected manifest initialization failure: {exc}")
        raise SystemExit(1) from exc
