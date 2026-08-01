#!/usr/bin/env python3
"""Run AY routing and approval fixtures through Codex or Claude Code."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "tests" / "scenarios.json"
SCHEMA = ROOT / "tests" / "behavior.schema.json"


@dataclass(frozen=True)
class Result:
    scenario_id: str
    passed: bool
    expected: str
    actual: str
    reason: str
    error: str = ""


def make_prompt(scenario: dict[str, object]) -> str:
    return (
        "This is a read-only behavior evaluation. Do not inspect files, use tools, "
        "or perform the requested work. Based on the installed skills, choose the "
        "single primary skill, the first authorized step, and the change approval "
        "gate. Classify the authorization in the user's request as it would apply "
        "to a real task; the evaluation itself being read-only does not remove that "
        "authorization. In first_step, execute means begin an already authorized change; "
        "investigate means gather facts or clarify product behavior before a proposal; "
        "review means assess without changing; outline is only for shaping an article. "
        "Writing or editing an artifact counts as change even when it is not code. "
        "In change_gate, already-approved means file or artifact changes may begin after any "
        "necessary investigation without a separate proposal checkpoint. approval-before-change "
        "means investigation is allowed, but no file or artifact change may begin until the agent "
        "presents its recommended solution or article outline and the user approves it. A broad "
        "goal is not approval for product behavior, architecture, optimization, or article choices "
        "the agent must invent. read-only applies only when the user asks to assess, diagnose, or "
        "explain without requesting any change. "
        "Return only the required structured response.\n\n"
        f"User request: {scenario['prompt']}"
    )


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

    expected = "/".join(
        str(scenario[key]) for key in ("expected_skill", "first_step", "change_gate")
    )
    actual = "/".join(
        str(response.get(key)) for key in ("skill", "first_step", "change_gate")
    )
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

        results: list[Result] = []
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
                for scenario in scenarios
            ]
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                mark = "PASS" if result.passed else "FAIL"
                print(
                    f"{mark} {result.scenario_id}: expected={result.expected} "
                    f"actual={result.actual} reason={result.reason}"
                )
                if result.error:
                    print(f"  {result.error}")

    failures = [result for result in results if not result.passed]
    print(f"RESULT: {len(results) - len(failures)}/{len(results)} cases passed on {args.host}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
