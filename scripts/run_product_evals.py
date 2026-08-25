#!/usr/bin/env python3
"""Blindly compare AY Product with an unskilled Codex baseline."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import shutil
import statistics
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "tests" / "product-scenarios.json"
RUBRIC = ROOT / "tests" / "product-rubric.json"
SCHEMA = ROOT / "tests" / "product-eval.schema.json"
SKILL = ROOT / "skills" / "ay-product"


@dataclass(frozen=True)
class CaseResult:
    run_id: str
    passed: bool
    skilled_score: int = 0
    baseline_score: int = 0
    skilled_winner: bool = False
    tie: bool = False
    skilled_failures: tuple[str, ...] = ()
    skilled_question_batches: int = 0
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


def isolated_codex_env(root: Path) -> dict[str, str]:
    env = os.environ.copy()
    source_home = Path(env.get("CODEX_HOME", Path.home() / ".codex")).expanduser().resolve()
    isolated_home = root / "codex-home"
    isolated_home.mkdir(mode=0o700, parents=True)
    auth = source_home / "auth.json"
    if auth.is_file():
        copied = isolated_home / "auth.json"
        shutil.copy2(auth, copied)
        copied.chmod(0o600)
    env["CODEX_HOME"] = str(isolated_home)
    return env


def write_files(workspace: Path, files: object) -> None:
    if not isinstance(files, dict):
        return
    for relative, content in files.items():
        path = workspace / str(relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(content), encoding="utf-8")


def run_codex(
    workspace: Path,
    output: Path,
    prompt: str,
    home: Path,
    model: str | None,
    timeout: int,
    schema: Path | None = None,
) -> str:
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
        "--output-last-message",
        str(output),
        "--cd",
        str(workspace),
    ]
    if schema:
        command.extend(["--output-schema", str(schema)])
    if model:
        command.extend(["--model", model])
    command.append(prompt)
    completed = subprocess.run(
        command,
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
        env=isolated_codex_env(home),
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout)[-2000:].strip()
        raise RuntimeError(detail or f"codex exited {completed.returncode}")
    return output.read_text(encoding="utf-8")


def blind_order(scenario_id: str, repetition: int) -> bool:
    digest = hashlib.sha256(f"{scenario_id}:{repetition}".encode()).digest()
    return digest[0] % 2 == 0


def evaluation_prompt(
    scenario: dict[str, object],
    rubric: dict[str, object],
    first: str,
    second: str,
) -> str:
    files = scenario.get("files", {})
    return (
        "Act as a strict product-work evaluator. Judge only the two anonymous responses. "
        "Do not infer which one used a skill. Use the rubric literally; longer is not better. "
        "Judge each dimension at the depth relevant to this case. Give full credit when a response "
        "correctly avoids analysis that the approved scope or no-build decision makes irrelevant; "
        "do not reward sections added only to fill the rubric. "
        "A response may score well by recommending validation or no build. List a critical "
        "failure only when the response actually commits it. Count question batches in the "
        "response; a compact group of related questions is one batch. Each dimension score "
        "must use the exact rubric id and total must equal their sum. A response with a critical "
        "failure loses to one without; otherwise the higher total wins and equal totals tie. "
        "Return only the required "
        "structured response.\n\n"
        f"USER REQUEST:\n{scenario['prompt']}\n\n"
        f"SUPPLIED FILES:\n{json.dumps(files, ensure_ascii=False, indent=2)}\n\n"
        f"CASE-SPECIFIC CRITERIA:\n{json.dumps(scenario.get('criteria', []), ensure_ascii=False, indent=2)}\n\n"
        f"SHARED RUBRIC:\n{json.dumps(rubric, ensure_ascii=False, indent=2)}\n\n"
        f"RESPONSE A:\n{first}\n\nRESPONSE B:\n{second}"
    )


def normalize_evaluation(data: dict[str, object], rubric: dict[str, object]) -> list[str]:
    errors: list[str] = []
    expected_ids = [str(item["id"]) for item in rubric["dimensions"]]  # type: ignore[index]
    allowed_failures = {str(item["id"]) for item in rubric["critical_failures"]}  # type: ignore[index]
    for label in ("a", "b"):
        result = data.get(label)
        if not isinstance(result, dict):
            errors.append(f"{label}: missing evaluation")
            continue
        scores = result.get("dimension_scores")
        if not isinstance(scores, list):
            errors.append(f"{label}: missing dimension scores")
            continue
        ids = [str(item.get("id")) for item in scores if isinstance(item, dict)]
        if ids != expected_ids:
            errors.append(f"{label}: dimension ids or order do not match rubric")
        total = sum(int(item.get("score", -100)) for item in scores if isinstance(item, dict))
        result["total"] = total
        failures = result.get("critical_failures")
        if not isinstance(failures, list) or not set(map(str, failures)).issubset(allowed_failures):
            errors.append(f"{label}: unknown critical failure")
    if not errors:
        first = data["a"]  # type: ignore[index]
        second = data["b"]  # type: ignore[index]
        first_failed = bool(first["critical_failures"])  # type: ignore[index]
        second_failed = bool(second["critical_failures"])  # type: ignore[index]
        if first_failed != second_failed:
            expected_winner = "B" if first_failed else "A"
        elif first["total"] > second["total"]:  # type: ignore[index]
            expected_winner = "A"
        elif second["total"] > first["total"]:  # type: ignore[index]
            expected_winner = "B"
        else:
            expected_winner = "tie"
        data["winner"] = expected_winner
    return errors


def run_case(
    scenario: dict[str, object],
    repetition: int,
    rubric: dict[str, object],
    model: str | None,
    judge_model: str | None,
    timeout: int,
    results_dir: Path,
) -> CaseResult:
    scenario_id = str(scenario["id"])
    run_id = f"{scenario_id}-{repetition}"
    try:
        with tempfile.TemporaryDirectory(prefix=f"ay-product-{run_id}-") as directory:
            root = Path(directory)
            skilled_workspace = root / "skilled"
            baseline_workspace = root / "baseline"
            judge_workspace = root / "judge"
            for workspace in (skilled_workspace, baseline_workspace, judge_workspace):
                workspace.mkdir()
            write_files(skilled_workspace, scenario.get("files"))
            write_files(baseline_workspace, scenario.get("files"))
            installed = skilled_workspace / ".agents" / "skills"
            installed.mkdir(parents=True)
            shutil.copytree(SKILL, installed / "ay-product")

            if scenario.get("research_mode") == "fixed":
                research_instruction = (
                    "This is a fixed-source evaluation. Use only the supplied workspace files "
                    "and general reasoning; do not browse or fetch external information. "
                )
            else:
                research_instruction = (
                    "This is a live-research evaluation. Research current public information "
                    "when it materially affects the decision and cite the supporting sources. "
                )
            task_prompt = research_instruction + str(scenario["prompt"])
            skilled = run_codex(
                skilled_workspace,
                root / "skilled.txt",
                task_prompt,
                root / "skilled-home",
                model,
                timeout,
            )
            baseline = run_codex(
                baseline_workspace,
                root / "baseline.txt",
                task_prompt,
                root / "baseline-home",
                model,
                timeout,
            )
            skilled_is_a = blind_order(scenario_id, repetition)
            first, second = (skilled, baseline) if skilled_is_a else (baseline, skilled)
            judged = run_codex(
                judge_workspace,
                root / "judge.json",
                evaluation_prompt(scenario, rubric, first, second),
                root / "judge-home",
                judge_model or model,
                timeout,
                SCHEMA,
            )
            evaluation = json.loads(judged)
            errors = normalize_evaluation(evaluation, rubric)
            if errors:
                return CaseResult(run_id, False, error="; ".join(errors))

            skilled_key = "a" if skilled_is_a else "b"
            baseline_key = "b" if skilled_is_a else "a"
            skilled_eval = evaluation[skilled_key]
            baseline_eval = evaluation[baseline_key]
            winner = str(evaluation["winner"])
            skilled_label = "A" if skilled_is_a else "B"

            artifact = {
                "run_id": run_id,
                "scenario": scenario,
                "skilled": skilled,
                "baseline": baseline,
                "skilled_anonymous_label": skilled_label,
                "evaluation": evaluation,
            }
            results_dir.mkdir(parents=True, exist_ok=True)
            results_dir.joinpath(f"{run_id}.json").write_text(
                json.dumps(artifact, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            return CaseResult(
                run_id,
                True,
                int(skilled_eval["total"]),
                int(baseline_eval["total"]),
                winner == skilled_label,
                winner == "tie",
                tuple(map(str, skilled_eval["critical_failures"])),
                int(skilled_eval["question_batches"]),
            )
    except (OSError, RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        detail = str(error)
        return CaseResult(
            run_id,
            False,
            error=detail,
            infrastructure_error=is_infrastructure_error_text(detail),
        )


def summarize(results: list[CaseResult], rubric: dict[str, object]) -> tuple[dict[str, object], bool]:
    completed = [result for result in results if result.passed]
    infrastructure_runs = [
        result.run_id for result in results if result.infrastructure_error
    ]
    failed_runs = [
        result.run_id
        for result in results
        if not result.passed and not result.infrastructure_error
    ]
    skilled_scores = [result.skilled_score for result in completed]
    baseline_scores = [result.baseline_score for result in completed]
    wins = sum(result.skilled_winner for result in completed)
    ties = sum(result.tie for result in completed)
    effective_win_rate = (wins + 0.5 * ties) / len(completed) if completed else 0.0
    critical_failures = sum(len(result.skilled_failures) for result in completed)
    average_questions = (
        statistics.mean(result.skilled_question_batches for result in completed)
        if completed
        else 0.0
    )
    median_skilled = statistics.median(skilled_scores) if skilled_scores else 0.0
    thresholds = {
        "minimum_median_total": float(rubric["minimum_median_total"]),
        "minimum_win_rate": float(rubric["minimum_win_rate"]),
        "maximum_critical_failures": int(rubric["maximum_critical_failures"]),
        "maximum_average_question_batches": float(
            rubric.get("maximum_average_question_batches", 1.0)
        ),
    }
    passed = bool(completed) and not failed_runs and not infrastructure_runs and all(
        (
            median_skilled >= thresholds["minimum_median_total"],
            effective_win_rate >= thresholds["minimum_win_rate"],
            critical_failures <= thresholds["maximum_critical_failures"],
            average_questions <= thresholds["maximum_average_question_batches"],
        )
    )
    summary = {
        "passed": passed,
        "runs": len(results),
        "completed": len(completed),
        "failed_runs": failed_runs,
        "infrastructure_runs": infrastructure_runs,
        "median_skilled_score": median_skilled,
        "median_baseline_score": statistics.median(baseline_scores) if baseline_scores else 0.0,
        "skilled_wins": wins,
        "ties": ties,
        "effective_win_rate": effective_win_rate,
        "skilled_critical_failures": critical_failures,
        "average_skilled_question_batches": average_questions,
        "thresholds": thresholds,
    }
    return summary, passed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model")
    parser.add_argument("--judge-model")
    parser.add_argument("--parallel", type=int, default=2)
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--ids", nargs="+")
    parser.add_argument("--holdout", choices=("include", "exclude", "only"), default="exclude")
    parser.add_argument(
        "--research-mode", choices=("fixed", "live", "all"), default="fixed"
    )
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--results-dir", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.parallel < 1 or args.repetitions < 1:
        raise SystemExit("--parallel and --repetitions must be positive")
    if shutil.which("codex") is None:
        raise SystemExit("codex CLI is required")
    scenarios = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    rubric = json.loads(RUBRIC.read_text(encoding="utf-8"))
    results_dir = args.results_dir or (
        ROOT / "eval-results" / "product" / f"{args.research_mode}-{args.holdout}"
    )
    if args.holdout != "include":
        wanted_holdout = args.holdout == "only"
        scenarios = [case for case in scenarios if bool(case.get("holdout")) == wanted_holdout]
    if args.research_mode != "all":
        scenarios = [
            case for case in scenarios if case.get("research_mode") == args.research_mode
        ]
    if args.ids:
        wanted = set(args.ids)
        scenarios = [case for case in scenarios if case["id"] in wanted]
        missing = wanted - {case["id"] for case in scenarios}
        if missing:
            raise SystemExit(f"unknown or filtered ids: {', '.join(sorted(missing))}")
    if args.limit:
        scenarios = scenarios[: args.limit]

    results: list[CaseResult] = []
    with ThreadPoolExecutor(max_workers=args.parallel) as executor:
        futures = [
            executor.submit(
                run_case,
                scenario,
                repetition,
                rubric,
                args.model,
                args.judge_model,
                args.timeout,
                results_dir,
            )
            for scenario in scenarios
            for repetition in range(1, args.repetitions + 1)
        ]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            if result.passed:
                verdict = "win" if result.skilled_winner else "tie" if result.tie else "loss"
                print(
                    f"PASS {result.run_id}: skill={result.skilled_score} "
                    f"baseline={result.baseline_score} verdict={verdict} "
                    f"questions={result.skilled_question_batches} "
                    f"critical={len(result.skilled_failures)}"
                )
            else:
                mark = "INFRA" if result.infrastructure_error else "FAIL"
                print(f"{mark} {result.run_id}: {result.error}")

    summary, passed = summarize(results, rubric)
    results_dir.mkdir(parents=True, exist_ok=True)
    results_dir.joinpath("summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 2 if summary["infrastructure_runs"] else 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
