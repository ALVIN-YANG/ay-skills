#!/usr/bin/env python3
"""Build and verify a deterministic AY Skills release archive."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile


ROOT = Path(__file__).resolve().parents[1]
TOP_LEVEL = (
    "LICENSE",
    "README.md",
    "README.zh-CN.md",
    "VERSION",
)
TREES = (".claude-plugin", ".codex-plugin", "assets", "skills")
IGNORED_PARTS = {".DS_Store", "__pycache__"}


def release_files(root: Path = ROOT) -> list[Path]:
    files = [root / name for name in TOP_LEVEL]
    for tree in TREES:
        files.extend(path for path in (root / tree).rglob("*") if path.is_file())
    return sorted(
        (path for path in files if not any(part in IGNORED_PARTS for part in path.parts)),
        key=lambda path: path.relative_to(root).as_posix(),
    )


def manifest(root: Path = ROOT) -> dict[str, object]:
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    files = {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in release_files(root)
    }
    skills = sorted(path.parent.name for path in (root / "skills").glob("*/SKILL.md"))
    return {"version": version, "skills": skills, "files": files}


def tar_info(name: str, data: bytes, mode: int = 0o644) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.size = len(data)
    info.mode = mode
    info.mtime = 0
    info.uid = info.gid = 0
    info.uname = info.gname = ""
    return info


def build_archive(
    output: Path,
    root: Path = ROOT,
    content_overrides: dict[str, bytes] | None = None,
) -> Path:
    release_manifest = manifest(root)
    prefix = f"ay-skills-{release_manifest['version']}"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as archive:
                for path in release_files(root):
                    relative = path.relative_to(root).as_posix()
                    data = (content_overrides or {}).get(relative, path.read_bytes())
                    mode = 0o755 if path.suffix == ".py" and data.startswith(b"#!") else 0o644
                    archive.addfile(tar_info(f"{prefix}/{relative}", data, mode), io.BytesIO(data))
                data = (json.dumps(release_manifest, indent=2, sort_keys=True) + "\n").encode()
                archive.addfile(
                    tar_info(f"{prefix}/release-manifest.json", data), io.BytesIO(data)
                )
    return output


def verify_archive(archive_path: Path, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    expected = manifest(root)
    prefix = f"ay-skills-{expected['version']}"
    try:
        with tarfile.open(archive_path, "r:gz") as archive:
            members = {member.name: member for member in archive.getmembers() if member.isfile()}
            manifest_name = f"{prefix}/release-manifest.json"
            member = members.get(manifest_name)
            if member is None:
                return ["release-manifest.json is missing"]
            extracted = archive.extractfile(member)
            actual = json.load(extracted) if extracted else None
    except (OSError, tarfile.TarError, json.JSONDecodeError) as error:
        return [f"archive could not be read: {error}"]

    if actual != expected:
        errors.append("release manifest does not match the checkout")
    expected_files = expected["files"]
    if not isinstance(expected_files, dict):
        return ["checkout release manifest has invalid file hashes"]
    expected_names = {f"{prefix}/{path}" for path in expected_files}
    expected_names.add(f"{prefix}/release-manifest.json")
    actual_names = set(members)
    if actual_names != expected_names:
        missing = sorted(expected_names - actual_names)
        extra = sorted(actual_names - expected_names)
        if missing:
            errors.append(f"archive is missing: {', '.join(missing)}")
        if extra:
            errors.append(f"archive has unexpected files: {', '.join(extra)}")
    for skill in expected["skills"]:
        if f"{prefix}/skills/{skill}/SKILL.md" not in actual_names:
            errors.append(f"archive is missing skill {skill}")
    try:
        with tarfile.open(archive_path, "r:gz") as archive:
            for relative, expected_hash in expected_files.items():
                member = archive.getmember(f"{prefix}/{relative}")
                extracted = archive.extractfile(member)
                if extracted is None:
                    errors.append(f"archive member cannot be read: {relative}")
                    continue
                actual_hash = hashlib.sha256(extracted.read()).hexdigest()
                if actual_hash != expected_hash:
                    errors.append(f"archive member hash mismatch: {relative}")
    except (KeyError, OSError, tarfile.TarError) as error:
        errors.append(f"archive content verification failed: {error}")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--output", type=Path)
    group.add_argument("--verify", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.output:
        path = build_archive(args.output.resolve())
        print(f"OK: built {path}")
        return 0
    errors = verify_archive(args.verify.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: verified {args.verify.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
