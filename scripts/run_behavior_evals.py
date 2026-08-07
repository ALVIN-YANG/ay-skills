#!/usr/bin/env python3
"""Run black-box Codex tasks and verify observable workspace behavior."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "tests" / "execution-scenarios.json"
IGNORED_SNAPSHOT_PARTS = {".agents", ".git", ".pytest_cache", "__pycache__"}


@dataclass(frozen=True)
class Result:
    scenario_id: str
    passed: bool
    detail: str
    error: str = ""


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

    expected_created = scenario.get("expected_created", {})
    if isinstance(expected_created, dict):
        for path, minimum in expected_created.items():
            content = after.get(str(path))
            if content is None:
                errors.append(f"{path}: was not created")
            elif len(content) < int(minimum):
                errors.append(f"{path}: only {len(content)} characters")

    final_any = scenario.get("final_any", [])
    if isinstance(final_any, list) and final_any:
        lowered = final_message.lower()
        if not any(str(term).lower() in lowered for term in final_any):
            errors.append(f"final response missed all expected terms: {final_any}")

    return errors


def run_scenario(
    scenario: dict[str, object],
    model: str | None,
    timeout: int,
) -> Result:
    scenario_id = str(scenario["id"])
    with tempfile.TemporaryDirectory(prefix=f"ay-behavior-{scenario_id}-") as directory:
        root = Path(directory)
        workspace = root / "workspace"
        output = root / "final.txt"
        installed = workspace / ".agents" / "skills"
        installed.mkdir(parents=True)

        skill_name = str(scenario["skill"])
        shutil.copytree(ROOT / "skills" / skill_name, installed / skill_name)

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
            return Result(scenario_id, False, "command failed", detail)

        try:
            final_message = output.read_text(encoding="utf-8")
            after = snapshot(workspace)
        except OSError as error:
            return Result(scenario_id, False, "could not inspect result", str(error))

        errors = verify_result(scenario, before, after, final_message)
        changes = ", ".join(sorted(changed_paths(before, after))) or "none"
        return Result(scenario_id, not errors, f"changes={changes}", "; ".join(errors))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model")
    parser.add_argument("--parallel", type=int, default=2)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--ids", nargs="+", help="Run only the named scenario ids")
    parser.add_argument("--timeout", type=int, default=300)
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

    results: list[Result] = []
    with ThreadPoolExecutor(max_workers=args.parallel) as executor:
        futures = [
            executor.submit(run_scenario, scenario, args.model, args.timeout)
            for scenario in scenarios
        ]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            mark = "PASS" if result.passed else "FAIL"
            print(f"{mark} {result.scenario_id}: {result.detail}")
            if result.error:
                print(f"  {result.error}")

    failures = [result for result in results if not result.passed]
    print(f"RESULT: {len(results) - len(failures)}/{len(results)} cases passed on codex")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
