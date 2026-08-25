#!/usr/bin/env python3
"""Verify that every skill works as a standalone copied folder."""

from __future__ import annotations

from pathlib import Path
import py_compile
import re
import shutil
import tempfile


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def local_links(markdown: Path) -> list[Path]:
    targets: list[Path] = []
    for target in LINK_RE.findall(markdown.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "#")):
            continue
        targets.append(markdown.parent / target.split("#", 1)[0])
    return targets


def verify_skill(skill: Path) -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix=f"portable-{skill.name}-") as directory:
        copied = Path(directory) / skill.name
        shutil.copytree(skill, copied)
        for markdown in copied.rglob("*.md"):
            for target in local_links(markdown):
                try:
                    target.resolve().relative_to(copied.resolve())
                except ValueError:
                    errors.append(f"{skill.name}: link escapes skill folder: {target}")
                    continue
                if not target.is_file():
                    errors.append(f"{skill.name}: broken local link: {target.relative_to(copied)}")
        for script in copied.rglob("*.py"):
            try:
                py_compile.compile(str(script), doraise=True)
            except py_compile.PyCompileError as error:
                errors.append(f"{skill.name}: script does not compile: {error}")
    return errors


def main() -> int:
    errors: list[str] = []
    skills = sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir())
    for skill in skills:
        errors.extend(verify_skill(skill))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {len(skills)} standalone skills verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
