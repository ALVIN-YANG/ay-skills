#!/usr/bin/env python3
"""Run isolated skill-routing fixtures through Codex or Claude Code."""

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
SCENARIOS = ROOT / "tests" / "scenarios.json"
SCHEMA = ROOT / "tests" / "routing.schema.json"
COMPETING_SKILLS = ROOT / "tests" / "competing-skills.json"


@dataclass(frozen=True)
class Result:
    scenario_id: str
    passed: bool
    expected: str
    actual: str
    reason: str
    error: str = ""


def is_infrastructure_error(result: Result) -> bool:
    lowered = result.error.lower()
    return any(
        marker in lowered
        for marker in ("connectionrefused", "unable to connect to api")
    )


def print_result(result: Result) -> None:
    mark = "PASS" if result.passed else "FAIL"
    print(
        f"{mark} {result.scenario_id}: expected={result.expected} "
        f"actual={result.actual} reason={result.reason}",
        flush=True,
    )
    if result.error:
        print(f"  {result.error}", flush=True)


def make_prompt(scenario: dict[str, object]) -> str:
    return (
        "This is a read-only routing evaluation. Do not inspect files, use tools, or perform "
        "the requested work. Choose the single primary installed skill, or `none` when no skill "
        "fits. Prefer a specific artifact or tool skill over a general workflow. "
        "Return only the required structured response.\n\n"
        f"User request: {scenario['prompt']}"
    )


def install_skill_stub(installed: Path, skill: dict[str, str]) -> None:
    skill_root = installed / skill["name"]
    skill_root.mkdir()
    skill_root.joinpath("SKILL.md").write_text(
        "---\n"
        f"name: {skill['name']}\n"
        f"description: {skill['description']}\n"
        "---\n\n"
        f"Use this skill for {skill['name']} tasks.\n",
        encoding="utf-8",
    )


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


def parse_response(path: Path, host: str) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if host == "claude" and isinstance(data, dict):
        structured = data.get("structured_output")
        if isinstance(structured, dict):
            return structured
        result = data.get("result")
        if isinstance(result, str) and result.strip().startswith("{"):
            return json.loads(result)
    if not isinstance(data, dict):
        raise ValueError("response is not a JSON object")
    return data


def run_scenario(
    scenario: dict[str, object],
    host: str,
    workdir: Path,
    output_dir: Path,
    model: str | None,
    timeout: int,
) -> Result:
    scenario_id = str(scenario["id"])
    output = output_dir / f"{scenario_id}.json"
    prompt = make_prompt(scenario)
    if host == "codex":
        command_env = isolated_codex_env(output_dir.parent / scenario_id)
        command = [
            "codex",
            "exec",
            "--ephemeral",
            "--ignore-user-config",
            "--ignore-rules",
            "--sandbox",
            "read-only",
            "--skip-git-repo-check",
            "--color",
            "never",
            "--output-schema",
            str(SCHEMA),
            "--output-last-message",
            str(output),
            "--cd",
            str(workdir),
        ]
        if model:
            command.extend(["--model", model])
        command.append(prompt)
    else:
        command_env = None
        schema = SCHEMA.read_text(encoding="utf-8")
        command = [
            "claude",
            "--print",
            "--plugin-dir",
            str(ROOT),
            "--tools",
            "",
            "--permission-mode",
            "plan",
            "--no-session-persistence",
            "--output-format",
            "json",
            "--json-schema",
            schema,
        ]
        if model:
            command.extend(["--model", model])
        command.append(prompt)

    try:
        completed = subprocess.run(
            command,
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            env=command_env,
        )
    except subprocess.TimeoutExpired:
        return Result(scenario_id, False, "", "timeout", "", "model timed out")

    if host == "claude" and completed.returncode == 0:
        output.write_text(completed.stdout, encoding="utf-8")
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout)[-1500:].strip()
        return Result(scenario_id, False, "", "error", "", detail)

    try:
        response = parse_response(output, host)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        return Result(scenario_id, False, "", "invalid-json", "", str(error))

    expected = str(scenario["expected_skill"])
    actual = str(response.get("skill"))
    return Result(
        scenario_id,
        actual == expected,
        expected,
        actual,
        str(response.get("reason", "")),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", choices=("codex", "claude"), required=True)
    parser.add_argument("--model")
    parser.add_argument("--parallel", type=int, default=2)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--ids", nargs="+", help="Run only the named scenario ids")
    parser.add_argument("--timeout", type=int, default=240)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.parallel < 1:
        raise SystemExit("--parallel must be positive")
    scenarios = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    if args.ids:
        wanted = set(args.ids)
        scenarios = [scenario for scenario in scenarios if scenario["id"] in wanted]
        missing = wanted - {scenario["id"] for scenario in scenarios}
        if missing:
            raise SystemExit(f"unknown scenario ids: {', '.join(sorted(missing))}")
    if args.limit:
        scenarios = scenarios[: args.limit]

    with tempfile.TemporaryDirectory(prefix="ay-skills-evals-") as directory:
        workdir = Path(directory) / "workspace"
        output_dir = Path(directory) / "output"
        installed = workdir / ".agents" / "skills"
        installed.mkdir(parents=True)
        output_dir.mkdir()
        for skill in ROOT.joinpath("skills").iterdir():
            if skill.is_dir():
                shutil.copytree(skill, installed / skill.name)
        competing_skills = json.loads(COMPETING_SKILLS.read_text(encoding="utf-8"))
        for skill in competing_skills:
            install_skill_stub(installed, skill)

        results: list[Result] = []
        pending = scenarios
        if args.host == "claude" and scenarios:
            preflight = run_scenario(
                scenarios[0],
                args.host,
                workdir,
                output_dir,
                args.model,
                args.timeout,
            )
            results.append(preflight)
            print_result(preflight)
            if is_infrastructure_error(preflight):
                print(
                    "ABORTED: Claude API is unreachable; remaining routing cases were not started",
                    flush=True,
                )
                return 1
            pending = scenarios[1:]

        with ThreadPoolExecutor(max_workers=args.parallel) as executor:
            futures = [
                executor.submit(
                    run_scenario,
                    scenario,
                    args.host,
                    workdir,
                    output_dir,
                    args.model,
                    args.timeout,
                )
                for scenario in pending
            ]
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                print_result(result)

    failures = [result for result in results if not result.passed]
    print(
        f"RESULT: {len(results) - len(failures)}/{len(results)} cases passed on {args.host}",
        flush=True,
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
