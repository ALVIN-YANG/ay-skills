#!/usr/bin/env python3
"""Run multi-step implicit AY workflows in one persistent workspace."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

import run_behavior_evals as behavior


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "tests" / "journey-scenarios.json"
FIXTURES = ROOT / "tests" / "fixtures"


@dataclass(frozen=True)
class JourneyResult:
    journey_id: str
    passed: bool
    detail: str
    error: str = ""
    artifact_dir: str = ""
    infrastructure_error: bool = False


def preserve_failure(root: Path, workspace: Path, destination: Path) -> str:
    destination.mkdir(parents=True, exist_ok=False)
    shutil.copytree(
        workspace,
        destination / "workspace",
        ignore=shutil.ignore_patterns(".agents", ".git", "__pycache__"),
    )
    messages = destination / "final-messages"
    messages.mkdir()
    for output in sorted(root.glob("*.txt")):
        shutil.copy2(output, messages / output.name)
    write_artifact_manifest(destination)
    return str(destination)


def file_hashes(root: Path) -> dict[str, str]:
    return {
        relative: hashlib.sha256(content).hexdigest()
        for relative, content in sorted(behavior.snapshot(root).items())
    }


def write_artifact_manifest(artifact_dir: Path) -> None:
    manifest = {
        "workspace": file_hashes(artifact_dir / "workspace"),
        "final_messages": file_hashes(artifact_dir / "final-messages"),
    }
    artifact_dir.joinpath("artifact-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def verify_artifact_manifest(artifact_dir: Path) -> list[str]:
    path = artifact_dir / "artifact-manifest.json"
    try:
        expected = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"preserved artifact integrity manifest is missing or invalid: {error}"]
    actual = {
        "workspace": file_hashes(artifact_dir / "workspace"),
        "final_messages": file_hashes(artifact_dir / "final-messages"),
    }
    return [] if actual == expected else ["preserved artifacts changed after capture"]


def run_prompt(
    workspace: Path,
    env_root: Path,
    prompt: str,
    output: Path,
    model: str | None,
    timeout: int,
) -> subprocess.CompletedProcess[str]:
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
    command.append(prompt)
    return subprocess.run(
        command,
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
        env=behavior.isolated_codex_env(env_root),
    )


def verify_cross_artifact(scenario: dict[str, object], after: dict[str, bytes]) -> list[str]:
    errors: list[str] = []
    cross = scenario.get("cross_artifact", {})
    if not isinstance(cross, dict):
        return ["cross_artifact must be an object"]
    required = cross.get("required_terms", {})
    if isinstance(required, dict):
        for path, terms in required.items():
            content = after.get(str(path))
            if content is None:
                errors.append(f"{path}: missing from final journey")
                continue
            lowered = content.decode("utf-8", errors="replace").lower()
            missing = [str(term) for term in terms if str(term).lower() not in lowered]
            if missing:
                errors.append(f"{path}: lost journey terms {missing}")
    patterns = cross.get("required_patterns", {})
    if isinstance(patterns, dict):
        for path, expressions in patterns.items():
            content = after.get(str(path))
            if content is None:
                errors.append(f"{path}: missing from final journey pattern checks")
                continue
            text = content.decode("utf-8", errors="replace")
            missing = [
                str(expression)
                for expression in expressions
                if re.search(str(expression), text, re.IGNORECASE | re.DOTALL) is None
            ]
            if missing:
                errors.append(f"{path}: lost journey invariants {missing}")
    forbidden_patterns = cross.get("forbidden_patterns", {})
    if isinstance(forbidden_patterns, dict):
        for path, expressions in forbidden_patterns.items():
            content = after.get(str(path))
            if content is None:
                continue
            text = content.decode("utf-8", errors="replace")
            present = [
                str(expression)
                for expression in expressions
                if re.search(str(expression), text, re.IGNORECASE | re.DOTALL) is not None
            ]
            if present:
                errors.append(f"{path}: introduced journey contradictions {present}")
    forbidden = cross.get("forbidden_terms", {})
    if isinstance(forbidden, dict):
        paths = [str(path) for path in forbidden.get("paths", [])]
        terms = [str(term) for term in forbidden.get("terms", [])]
        for path in paths:
            lowered = after.get(path, b"").decode("utf-8", errors="replace").lower()
            present = [term for term in terms if term.lower() in lowered]
            if present:
                errors.append(f"{path}: introduced forbidden scope {present}")
    return errors


def run_verify_commands(
    workspace: Path, commands: object, timeout: int
) -> list[str]:
    errors: list[str] = []
    if not isinstance(commands, list):
        return ["verify_commands must be a list"]
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
            output = (checked.stderr or checked.stdout)[-1000:].strip()
            errors.append(f"{' '.join(command)} failed: {output}")
    return errors


def run_journey(
    scenario: dict[str, object], model: str | None, timeout: int, failure_root: Path
) -> JourneyResult:
    journey_id = str(scenario["id"])
    with tempfile.TemporaryDirectory(prefix=f"ay-journey-{journey_id}-") as directory:
        root = Path(directory)
        workspace = root / "workspace"
        installed = workspace / ".agents" / "skills"
        installed.mkdir(parents=True)
        behavior.install_catalog(installed, "ay-product", "fixture")

        def failed(
            detail: str, error: str = "", infrastructure_error: bool = False
        ) -> JourneyResult:
            destination = failure_root / journey_id
            artifact_dir = preserve_failure(root, workspace, destination)
            return JourneyResult(
                journey_id, False, detail, error, artifact_dir, infrastructure_error
            )

        fixture_root = (FIXTURES / str(scenario["fixture"])).resolve()
        try:
            fixture_root.relative_to(FIXTURES.resolve())
        except ValueError:
            return failed("invalid fixture path")
        if not fixture_root.is_dir():
            return failed("fixture missing", str(fixture_root))
        shutil.copytree(fixture_root, workspace, dirs_exist_ok=True)

        completed_steps: list[str] = []
        for index, step in enumerate(scenario["steps"], start=1):
            step_id = str(step["id"])
            before = behavior.snapshot(workspace)
            output = root / f"{index:02d}-{step_id}.txt"
            try:
                completed = run_prompt(
                    workspace,
                    root / f"env-{index}",
                    str(step["prompt"]),
                    output,
                    model,
                    timeout,
                )
            except subprocess.TimeoutExpired:
                return failed(f"{step_id} timed out")
            if completed.returncode != 0:
                detail = (completed.stderr or completed.stdout)[-1500:].strip()
                return failed(
                    f"{step_id} command failed",
                    detail,
                    behavior.is_infrastructure_error_text(detail),
                )
            final_message = output.read_text(encoding="utf-8")
            after = behavior.snapshot(workspace)
            assertions = dict(step.get("assert", {}))
            errors = behavior.verify_result(assertions, before, after, final_message)
            if errors:
                error = "; ".join(errors) + f"\nFinal response:\n{final_message[-3000:]}"
                return failed(f"{step_id} failed", error)
            completed_steps.append(step_id)

        after = behavior.snapshot(workspace)
        errors = verify_cross_artifact(scenario, after)
        errors.extend(run_verify_commands(workspace, scenario.get("verify_commands", []), timeout))
        if errors:
            return failed("final verification failed", "; ".join(errors))
        return JourneyResult(journey_id, True, " -> ".join(completed_steps))


def recheck_journey(
    scenario: dict[str, object], artifact_dir: Path, timeout: int
) -> JourneyResult:
    journey_id = str(scenario["id"])
    workspace = artifact_dir / "workspace"
    messages = artifact_dir / "final-messages"
    if not workspace.is_dir() or not messages.is_dir():
        return JourneyResult(
            journey_id,
            False,
            "preserved artifacts are incomplete",
            artifact_dir=str(artifact_dir),
        )
    integrity_errors = verify_artifact_manifest(artifact_dir)
    if integrity_errors:
        return JourneyResult(
            journey_id,
            False,
            "preserved artifact integrity check failed",
            "; ".join(integrity_errors),
            str(artifact_dir),
        )
    review_outputs = sorted(messages.glob("*-review.txt"))
    if not review_outputs:
        return JourneyResult(
            journey_id,
            False,
            "preserved review output is missing",
            artifact_dir=str(artifact_dir),
        )
    state = behavior.snapshot(workspace)
    review = scenario["steps"][-1]
    errors = behavior.verify_result(
        dict(review.get("assert", {})),
        state,
        state,
        review_outputs[-1].read_text(encoding="utf-8"),
    )
    errors.extend(verify_cross_artifact(scenario, state))
    with tempfile.TemporaryDirectory(prefix=f"ay-recheck-{journey_id}-") as directory:
        verification_workspace = Path(directory) / "workspace"
        shutil.copytree(
            workspace,
            verification_workspace,
            ignore=shutil.ignore_patterns(".agents", ".git", "__pycache__"),
        )
        errors.extend(
            run_verify_commands(
                verification_workspace,
                scenario.get("verify_commands", []),
                timeout,
            )
        )
    return JourneyResult(
        journey_id,
        not errors,
        "rechecked preserved final artifacts",
        "; ".join(errors),
        str(artifact_dir),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model")
    parser.add_argument("--parallel", type=int, default=2)
    parser.add_argument("--ids", nargs="+")
    parser.add_argument("--timeout", type=int, default=420)
    parser.add_argument(
        "--recheck-dir",
        type=Path,
        help="Re-run final assertions against a preserved failure run without model calls",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=ROOT / "eval-results" / "journey",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.recheck_dir and shutil.which("codex") is None:
        raise SystemExit("codex CLI is required")
    scenarios = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    if args.ids:
        wanted = set(args.ids)
        scenarios = [scenario for scenario in scenarios if scenario["id"] in wanted]
        missing = wanted - {scenario["id"] for scenario in scenarios}
        if missing:
            raise SystemExit(f"unknown journey ids: {', '.join(sorted(missing))}")
    results: list[JourneyResult] = []
    if args.recheck_dir:
        results = [
            recheck_journey(
                scenario,
                args.recheck_dir.resolve() / str(scenario["id"]),
                args.timeout,
            )
            for scenario in scenarios
        ]
    else:
        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        failure_root = args.results_dir / "failures" / run_id
        with ThreadPoolExecutor(max_workers=args.parallel) as executor:
            futures = [
                executor.submit(run_journey, scenario, args.model, args.timeout, failure_root)
                for scenario in scenarios
            ]
            for future in as_completed(futures):
                results.append(future.result())
    for result in results:
        mark = "PASS" if result.passed else "INFRA" if result.infrastructure_error else "FAIL"
        print(f"{mark} {result.journey_id}: {result.detail}", flush=True)
        if result.error:
            print(f"  {result.error}", flush=True)
    infrastructure = [result for result in results if result.infrastructure_error]
    failures = [
        result for result in results if not result.passed and not result.infrastructure_error
    ]
    args.results_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "host": "codex",
        "model": args.model,
        "mode": "recheck" if args.recheck_dir else "model",
        "passed": sum(result.passed for result in results),
        "failed": len(failures),
        "infrastructure_errors": len(infrastructure),
        "total": len(results),
        "results": [asdict(result) for result in sorted(results, key=lambda item: item.journey_id)],
    }
    result_name = "codex-recheck.json" if args.recheck_dir else "codex.json"
    args.results_dir.joinpath(result_name).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        f"RESULT: {sum(result.passed for result in results)}/{len(results)} passed, "
        f"{len(failures)} failed, {len(infrastructure)} infrastructure errors",
        flush=True,
    )
    return 2 if infrastructure else 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
