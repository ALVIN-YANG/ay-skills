#!/usr/bin/env python3
"""Run black-box Codex tasks and verify observable workspace behavior."""

from __future__ import annotations

import argparse
import binascii
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zlib


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "tests" / "execution-scenarios.json"
COMPETING_SKILLS = ROOT / "tests" / "competing-skills.json"
FIXTURES = ROOT / "tests" / "fixtures"
IGNORED_SNAPSHOT_PARTS = {".agents", ".git", ".pytest_cache", "__pycache__"}


@dataclass(frozen=True)
class Result:
    scenario_id: str
    passed: bool
    detail: str
    error: str = ""
    infrastructure_error: bool = False


def is_infrastructure_error_text(text: str) -> bool:
    lowered = text.lower()
    return any(
        marker in lowered
        for marker in (
            "connectionrefused",
            "unable to connect to api",
            "failed to lookup address information",
            "stream disconnected before completion",
            "error sending request for url",
        )
    )


def snapshot(workspace: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for path in workspace.rglob("*"):
        relative = path.relative_to(workspace)
        if not path.is_file() or any(part in IGNORED_SNAPSHOT_PARTS for part in relative.parts):
            continue
        files[relative.as_posix()] = path.read_bytes()
    return files


def changed_paths(before: dict[str, bytes], after: dict[str, bytes]) -> set[str]:
    return {
        path
        for path in before.keys() | after.keys()
        if before.get(path) != after.get(path)
    }


def isolated_codex_env(root: Path) -> dict[str, str]:
    env = os.environ.copy()
    source_home = Path(env.get("CODEX_HOME", Path.home() / ".codex")).expanduser().resolve()
    isolated_home = root / "codex-home"
    isolated_home.mkdir(mode=0o700, parents=True)
    auth = source_home / "auth.json"
    if auth.is_file():
        isolated_auth = isolated_home / "auth.json"
        shutil.copy2(auth, isolated_auth)
        isolated_auth.chmod(0o600)
    env["CODEX_HOME"] = str(isolated_home)
    return env


def install_skill_stub(installed: Path, skill: dict[str, str]) -> None:
    skill_root = installed / skill["name"]
    if skill_root.exists():
        return
    skill_root.mkdir()
    skill_root.joinpath("SKILL.md").write_text(
        "---\n"
        f"name: {skill['name']}\n"
        f"description: {skill['description']}\n"
        "---\n\n"
        f"Use this skill for {skill['name']} tasks.\n",
        encoding="utf-8",
    )


def install_catalog(installed: Path, target_skill: str, catalog: str) -> None:
    names = [target_skill]
    if catalog == "fixture":
        names = sorted(path.name for path in (ROOT / "skills").iterdir() if path.is_dir())
    for name in names:
        shutil.copytree(ROOT / "skills" / name, installed / name)
    if catalog == "fixture":
        competing = json.loads(COMPETING_SKILLS.read_text(encoding="utf-8"))
        for skill in competing:
            install_skill_stub(installed, skill)


def png_metadata(data: bytes) -> tuple[int, int, bool]:
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("not a PNG")
    offset = 8
    width = height = bit_depth = color_type = None
    has_transparency = False
    compressed_parts: list[bytes] = []
    saw_iend = False
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        payload = data[offset + 8 : offset + 8 + length]
        crc_offset = offset + 8 + length
        if len(payload) != length or crc_offset + 4 > len(data):
            raise ValueError("truncated PNG chunk")
        expected_crc = struct.unpack(">I", data[crc_offset : crc_offset + 4])[0]
        actual_crc = binascii.crc32(chunk_type + payload) & 0xFFFFFFFF
        if actual_crc != expected_crc:
            raise ValueError(f"invalid {chunk_type.decode(errors='replace')} CRC")
        if chunk_type == b"IHDR":
            if length != 13 or width is not None or offset != 8:
                raise ValueError("invalid IHDR")
            width, height = struct.unpack(">II", payload[:8])
            bit_depth = payload[8]
            color_type = payload[9]
            if payload[10:13] != b"\x00\x00\x00":
                raise ValueError("unsupported PNG compression, filter, or interlace")
        elif chunk_type == b"IDAT":
            compressed_parts.append(payload)
        elif chunk_type == b"tRNS":
            has_transparency = True
        offset += 12 + length
        if chunk_type == b"IEND":
            if length != 0:
                raise ValueError("invalid IEND")
            saw_iend = True
            break
    if not saw_iend or offset != len(data):
        raise ValueError("missing or trailing IEND data")
    if width is None or height is None or bit_depth is None or color_type is None:
        raise ValueError("missing IHDR")
    if width < 1 or height < 1 or not compressed_parts:
        raise ValueError("missing image data")
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(color_type)
    if channels is None or bit_depth not in {1, 2, 4, 8, 16}:
        raise ValueError("unsupported PNG color format")
    try:
        decoded = zlib.decompress(b"".join(compressed_parts))
    except zlib.error as error:
        raise ValueError(f"invalid PNG image data: {error}") from error
    row_bytes = (width * channels * bit_depth + 7) // 8
    expected_size = height * (row_bytes + 1)
    if len(decoded) != expected_size:
        raise ValueError("decoded PNG data has the wrong size")
    if any(decoded[row * (row_bytes + 1)] > 4 for row in range(height)):
        raise ValueError("invalid PNG row filter")
    return width, height, has_transparency or color_type in {4, 6}


def numeric_dimension(value: str | None) -> int | None:
    if value is None:
        return None
    match = re.fullmatch(r"\s*(\d+)(?:px)?\s*", value)
    return int(match.group(1)) if match else None


def svg_visible_content(root: ET.Element) -> tuple[str, int]:
    text_parts: list[str] = []
    renderable = 0
    hidden_containers = {"defs", "style", "script", "metadata", "title", "desc"}
    renderable_tags = {"circle", "ellipse", "image", "line", "path", "polygon", "polyline", "rect", "text", "use"}

    def visit(element: ET.Element, hidden: bool = False) -> None:
        nonlocal renderable
        tag = element.tag.rsplit("}", 1)[-1] if isinstance(element.tag, str) else ""
        hidden = hidden or tag in hidden_containers
        if not hidden and tag in renderable_tags:
            renderable += 1
        if not hidden and tag == "text":
            text_parts.extend(element.itertext())
            return
        for child in element:
            visit(child, hidden)

    visit(root)
    return " ".join(text_parts), renderable


def verify_result(
    scenario: dict[str, object],
    before: dict[str, bytes],
    after: dict[str, bytes],
    final_message: str,
) -> list[str]:
    errors: list[str] = []
    changes = changed_paths(before, after)

    if scenario.get("expect_no_changes") and changes:
        errors.append(f"unexpected changes: {', '.join(sorted(changes))}")

    expected_files = scenario.get("expected_files", {})
    if isinstance(expected_files, dict):
        for path, expected in expected_files.items():
            if after.get(str(path)) != str(expected).encode("utf-8"):
                errors.append(f"{path}: content did not match")
        if expected_files and not scenario.get("allow_extra_changes", True):
            extras = changes - {str(path) for path in expected_files}
            if extras:
                errors.append(f"extra changes: {', '.join(sorted(extras))}")

    unchanged_files = scenario.get("unchanged_files", [])
    if isinstance(unchanged_files, list):
        for path in unchanged_files:
            if before.get(str(path)) != after.get(str(path)):
                errors.append(f"{path}: must remain unchanged")

    expected_created = scenario.get("expected_created", {})
    if isinstance(expected_created, dict):
        for path, minimum in expected_created.items():
            content = after.get(str(path))
            if content is None:
                errors.append(f"{path}: was not created")
            elif len(content) < int(minimum):
                errors.append(f"{path}: only {len(content)} characters")

    created_all = scenario.get("created_all", {})
    if isinstance(created_all, dict):
        for path, terms in created_all.items():
            content = after.get(str(path))
            if content is None:
                errors.append(f"{path}: was not created for content checks")
                continue
            lowered = content.decode("utf-8", errors="replace").lower()
            missing = [str(term) for term in terms if str(term).lower() not in lowered]
            if missing:
                errors.append(f"{path}: missed expected content terms: {missing}")

    created_none = scenario.get("created_none", {})
    if isinstance(created_none, dict):
        for path, terms in created_none.items():
            content = after.get(str(path))
            if content is None:
                errors.append(f"{path}: was not created for forbidden content checks")
                continue
            lowered = content.decode("utf-8", errors="replace").lower()
            present = [str(term) for term in terms if str(term).lower() in lowered]
            if present:
                errors.append(f"{path}: included forbidden content terms: {present}")

    expected_png = scenario.get("expected_png", {})
    if isinstance(expected_png, dict):
        for path, expectation in expected_png.items():
            content = after.get(str(path))
            if content is None:
                errors.append(f"{path}: PNG was not created")
                continue
            try:
                width, height, alpha = png_metadata(content)
            except ValueError as error:
                errors.append(f"{path}: {error}")
                continue
            if isinstance(expectation, dict):
                if width != expectation.get("width") or height != expectation.get("height"):
                    errors.append(f"{path}: expected {expectation.get('width')}x{expectation.get('height')}, found {width}x{height}")
                if "alpha" in expectation and alpha is not expectation.get("alpha"):
                    errors.append(f"{path}: alpha={alpha}, expected {expectation.get('alpha')}")

    expected_svg = scenario.get("expected_svg", {})
    if isinstance(expected_svg, dict):
        for path, expectation in expected_svg.items():
            content = after.get(str(path))
            if content is None:
                errors.append(f"{path}: SVG was not created")
                continue
            try:
                root = ET.fromstring(content)
            except ET.ParseError as error:
                errors.append(f"{path}: invalid SVG: {error}")
                continue
            if not root.tag.endswith("svg"):
                errors.append(f"{path}: root element is not svg")
                continue
            if isinstance(expectation, dict):
                width = numeric_dimension(root.attrib.get("width"))
                height = numeric_dimension(root.attrib.get("height"))
                if width != expectation.get("width") or height != expectation.get("height"):
                    errors.append(f"{path}: expected {expectation.get('width')}x{expectation.get('height')}, found {width}x{height}")
                visible_text, renderable = svg_visible_content(root)
                if renderable == 0:
                    errors.append(f"{path}: has no renderable elements")
                lowered = visible_text.lower()
                missing = [str(term) for term in expectation.get("contains", []) if str(term).lower() not in lowered]
                if missing:
                    errors.append(f"{path}: missed visible terms: {missing}")

    final_any = scenario.get("final_any", [])
    if isinstance(final_any, list) and final_any:
        lowered = final_message.lower()
        if not any(str(term).lower() in lowered for term in final_any):
            errors.append(f"final response missed all expected terms: {final_any}")

    final_all = scenario.get("final_all", [])
    if isinstance(final_all, list) and final_all:
        lowered = final_message.lower()
        missing = [str(term) for term in final_all if str(term).lower() not in lowered]
        if missing:
            errors.append(f"final response missed expected terms: {missing}")

    final_none = scenario.get("final_none", [])
    if isinstance(final_none, list) and final_none:
        lowered = final_message.lower()
        present = [str(term) for term in final_none if str(term).lower() in lowered]
        if present:
            errors.append(f"final response included forbidden terms: {present}")

    final_regex = scenario.get("final_regex", [])
    if isinstance(final_regex, list):
        for pattern in final_regex:
            if re.search(str(pattern), final_message) is None:
                errors.append(f"final response missed required pattern: {pattern}")

    return errors


def verify_reproducible_outputs(
    workspace: Path,
    after: dict[str, bytes],
    checks: object,
    timeout: int,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(checks, list):
        return ["reproduce must be a list"]
    for check in checks:
        if not isinstance(check, dict):
            errors.append("invalid reproduce check")
            continue
        path = str(check.get("path", ""))
        command = check.get("command")
        if not path or not isinstance(command, list) or not command:
            errors.append("reproduce check needs path and command arguments")
            continue
        actual = after.get(path)
        if actual is None:
            errors.append(f"{path}: cannot reproduce missing output")
            continue
        with tempfile.TemporaryDirectory(prefix="ay-reproduce-") as directory:
            copied = Path(directory) / "workspace"
            shutil.copytree(
                workspace,
                copied,
                ignore=shutil.ignore_patterns(".agents", ".git", "__pycache__"),
            )
            reproduced = copied / path
            try:
                reproduced.resolve().relative_to(copied.resolve())
            except ValueError:
                errors.append(f"{path}: reproduction output escapes workspace")
                continue
            if reproduced.is_file():
                reproduced.unlink()
            completed = subprocess.run(
                [str(part) for part in command],
                cwd=copied,
                capture_output=True,
                text=True,
                timeout=min(timeout, 120),
                check=False,
            )
            if completed.returncode != 0:
                output = (completed.stderr or completed.stdout)[-800:].strip()
                errors.append(f"{path}: reproduction command failed: {output}")
                continue
            if not reproduced.is_file():
                errors.append(f"{path}: reproduction command did not create output")
            elif reproduced.read_bytes() != actual:
                errors.append(f"{path}: output differs from clean reproduction")
    return errors


def run_scenario(
    scenario: dict[str, object],
    model: str | None,
    timeout: int,
    catalog: str,
) -> Result:
    scenario_id = str(scenario["id"])
    with tempfile.TemporaryDirectory(
        prefix=f"ay-behavior-{scenario_id}-", ignore_cleanup_errors=True
    ) as directory:
        root = Path(directory)
        workspace = root / "workspace"
        output = root / "final.txt"
        installed = workspace / ".agents" / "skills"
        installed.mkdir(parents=True)

        skill_name = str(scenario["skill"])
        install_catalog(installed, skill_name, catalog)

        fixture = scenario.get("fixture")
        if fixture:
            fixture_root = (FIXTURES / str(fixture)).resolve()
            fixture_root.relative_to(FIXTURES.resolve())
            if not fixture_root.is_dir():
                return Result(scenario_id, False, "fixture missing", str(fixture_root))
            shutil.copytree(fixture_root, workspace, dirs_exist_ok=True)

        files = scenario.get("files", {})
        if isinstance(files, dict):
            for relative, content in files.items():
                path = workspace / str(relative)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(str(content), encoding="utf-8")

        before = snapshot(workspace)
        command = [
            "codex",
            "exec",
            "--ephemeral",
            "--ignore-user-config",
            "--ignore-rules",
            "--sandbox",
            "workspace-write",
            "--skip-git-repo-check",
            "--color",
            "never",
            "--output-last-message",
            str(output),
            "--cd",
            str(workspace),
        ]
        if model:
            command.extend(["--model", model])
        command.append(str(scenario["prompt"]))

        try:
            completed = subprocess.run(
                command,
                cwd=workspace,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
                env=isolated_codex_env(root),
            )
        except subprocess.TimeoutExpired:
            return Result(scenario_id, False, "timeout", "model timed out")

        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout)[-1500:].strip()
            return Result(
                scenario_id,
                False,
                "command failed",
                detail,
                is_infrastructure_error_text(detail),
            )

        try:
            final_message = output.read_text(encoding="utf-8")
            after = snapshot(workspace)
        except OSError as error:
            return Result(scenario_id, False, "could not inspect result", str(error))

        errors = verify_result(scenario, before, after, final_message)
        errors.extend(
            verify_reproducible_outputs(
                workspace,
                after,
                scenario.get("reproduce", []),
                timeout,
            )
        )
        commands = scenario.get("verify_commands", [])
        if isinstance(commands, list):
            for command in commands:
                if not isinstance(command, list) or not command:
                    errors.append("invalid verify command")
                    continue
                checked = subprocess.run(
                    [str(part) for part in command],
                    cwd=workspace,
                    capture_output=True,
                    text=True,
                    timeout=min(timeout, 120),
                    check=False,
                )
                if checked.returncode != 0:
                    output_text = (checked.stderr or checked.stdout)[-800:].strip()
                    errors.append(f"verify command failed: {' '.join(command)}: {output_text}")
        changes = ", ".join(sorted(changed_paths(before, after))) or "none"
        return Result(scenario_id, not errors, f"changes={changes}", "; ".join(errors))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model")
    parser.add_argument("--catalog", choices=("fixture", "target"), default="fixture")
    parser.add_argument("--parallel", type=int, default=2)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--ids", nargs="+", help="Run only the named scenario ids")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=ROOT / "eval-results" / "behavior",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.parallel < 1:
        raise SystemExit("--parallel must be positive")
    if shutil.which("codex") is None:
        raise SystemExit("codex CLI is required")

    scenarios = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    if args.ids:
        wanted = set(args.ids)
        scenarios = [scenario for scenario in scenarios if scenario["id"] in wanted]
        missing = wanted - {scenario["id"] for scenario in scenarios}
        if missing:
            raise SystemExit(f"unknown scenario ids: {', '.join(sorted(missing))}")
    if args.limit:
        scenarios = scenarios[: args.limit]
    if any(scenario.get("expected_png") for scenario in scenarios):
        if importlib.util.find_spec("PIL") is None:
            raise SystemExit(
                "Pillow is required only for PNG fixture evals; run with "
                "`uv run --with pillow python scripts/run_behavior_evals.py`"
            )

    results: list[Result] = []
    with ThreadPoolExecutor(max_workers=args.parallel) as executor:
        futures = [
            executor.submit(run_scenario, scenario, args.model, args.timeout, args.catalog)
            for scenario in scenarios
        ]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            mark = "PASS" if result.passed else "INFRA" if result.infrastructure_error else "FAIL"
            print(f"{mark} {result.scenario_id}: {result.detail}", flush=True)
            if result.error:
                print(f"  {result.error}", flush=True)

    infrastructure = [result for result in results if result.infrastructure_error]
    failures = [
        result for result in results if not result.passed and not result.infrastructure_error
    ]
    args.results_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "host": "codex",
        "catalog": args.catalog,
        "model": args.model,
        "passed": sum(result.passed for result in results),
        "failed": len(failures),
        "infrastructure_errors": len(infrastructure),
        "total": len(results),
        "results": [asdict(result) for result in sorted(results, key=lambda item: item.scenario_id)],
    }
    args.results_dir.joinpath(f"codex-{args.catalog}.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        f"RESULT: {sum(result.passed for result in results)}/{len(results)} passed, "
        f"{len(failures)} failed, {len(infrastructure)} infrastructure errors on codex",
        flush=True,
    )
    return 2 if infrastructure else 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
