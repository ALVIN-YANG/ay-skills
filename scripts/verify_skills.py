#!/usr/bin/env python3
"""Dependency-free structural checks for AY Skills."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = (
    "ay-product",
    "ay-ui",
    "ay-architecture",
    "ay-api",
    "ay-database",
    "ay-implement",
    "ay-fix",
    "ay-audio",
    "ay-improve",
    "ay-write",
    "ay-review",
    "ay-icon",
    "ay-app-store",
)
FRONTMATTER_RE = re.compile(r"\A---\n(?P<yaml>.*?)\n---\n(?P<body>.*)\Z", re.DOTALL)
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
CONTRACT_RE = re.compile(
    r"<!-- ay-contract:start -->\n(?P<contract>.*?)\n<!-- ay-contract:end -->",
    re.DOTALL,
)
LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing or malformed YAML frontmatter")
    fields: dict[str, str] = {}
    for line in match.group("yaml").splitlines():
        if not line.strip():
            continue
        if line.startswith((" ", "\t")) or ":" not in line:
            raise ValueError(f"unsupported frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key or not value or key in fields:
            raise ValueError(f"invalid frontmatter field: {line!r}")
        fields[key] = value
    return fields, match.group("body")


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", text))


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    version_path = root / "VERSION"
    version = version_path.read_text(encoding="utf-8").strip() if version_path.is_file() else ""
    if not SEMVER_RE.fullmatch(version):
        errors.append("VERSION: missing or invalid semantic version")
    skills_root = root / "skills"
    actual = sorted(path.name for path in skills_root.iterdir() if path.is_dir())
    if actual != sorted(EXPECTED_SKILLS):
        errors.append(f"skills: expected {sorted(EXPECTED_SKILLS)}, found {actual}")

    contracts: dict[str, str] = {}
    descriptions: dict[str, str] = {}

    for name in EXPECTED_SKILLS:
        skill_root = skills_root / name
        skill_file = skill_root / "SKILL.md"
        metadata_file = skill_root / "agents" / "openai.yaml"
        if not skill_file.is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue
        if not metadata_file.is_file():
            errors.append(f"{name}: missing agents/openai.yaml")
            continue

        text = skill_file.read_text(encoding="utf-8")
        try:
            fields, body = parse_frontmatter(skill_file)
        except ValueError as error:
            errors.append(f"{name}: {error}")
            continue

        if set(fields) != {"name", "description"}:
            errors.append(f"{name}: frontmatter must contain only name and description")
        if fields.get("name") != name:
            errors.append(f"{name}: frontmatter name mismatch")
        if not NAME_RE.fullmatch(name) or len(name) > 64:
            errors.append(f"{name}: invalid portable skill name")

        description = fields.get("description", "")
        if "Use when" not in description:
            errors.append(f"{name}: description must include concrete 'Use when' triggers")
        if len(description) > 1024:
            errors.append(f"{name}: description exceeds 1024 characters")
        if description in descriptions:
            errors.append(f"{name}: duplicates description from {descriptions[description]}")
        descriptions[description] = name

        line_total = len(text.splitlines())
        if line_total > 150:
            errors.append(f"{name}: {line_total} lines exceeds 150")
        body_words = word_count(body)
        if body_words > 500:
            errors.append(f"{name}: {body_words} body words exceeds 500")
        if "TODO" in text:
            errors.append(f"{name}: contains TODO placeholder")

        contract_match = CONTRACT_RE.search(body)
        if not contract_match:
            errors.append(f"{name}: missing AY approval contract markers")
        else:
            contracts[name] = contract_match.group("contract").strip()

        for target in LINK_RE.findall(body):
            if target.startswith(("http://", "https://", "#")):
                continue
            clean_target = target.split("#", 1)[0]
            resolved = skill_root / clean_target
            if not resolved.is_file():
                errors.append(f"{name}: broken reference {target}")
            if "/" in clean_target and not clean_target.startswith("references/"):
                errors.append(f"{name}: reference must stay one level from SKILL.md: {target}")

        metadata = metadata_file.read_text(encoding="utf-8")
        if f"${name}" not in metadata:
            errors.append(f"{name}: default_prompt must mention ${name}")
        for key in ("display_name:", "short_description:", "default_prompt:"):
            if key not in metadata:
                errors.append(f"{name}: agents/openai.yaml missing {key[:-1]}")
        if "allow_implicit_invocation: false" in metadata:
            errors.append(f"{name}: must remain model-invoked")

    if contracts:
        canonical_name = EXPECTED_SKILLS[0]
        canonical = contracts.get(canonical_name)
        if canonical is None:
            errors.append(f"{canonical_name}: cannot establish canonical approval contract")
        else:
            for name, contract in contracts.items():
                if contract != canonical:
                    errors.append(f"{name}: approval contract drifted from {canonical_name}")

    validate_manifests(root, version, errors)
    validate_scenarios(root, errors)
    validate_ay_only_scenarios(root, errors)
    validate_execution_scenarios(root, errors)
    validate_journey_scenarios(root, errors)
    validate_product_evals(root, errors)
    validate_docs(root, errors)
    return errors


def load_json(path: Path, errors: list[str]) -> dict | list | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{path.relative_to(path.parents[1])}: invalid JSON: {error}")
        return None


def validate_manifests(root: Path, version: str, errors: list[str]) -> None:
    codex = load_json(root / ".codex-plugin" / "plugin.json", errors)
    claude = load_json(root / ".claude-plugin" / "plugin.json", errors)
    marketplace = load_json(root / ".claude-plugin" / "marketplace.json", errors)
    if not isinstance(codex, dict) or not isinstance(claude, dict):
        return
    for label, manifest in (("codex", codex), ("claude", claude)):
        if manifest.get("name") != "ay-skills":
            errors.append(f"{label} manifest: name must be ay-skills")
        if manifest.get("version") != version:
            errors.append(f"{label} manifest: version must match VERSION ({version})")
        if manifest.get("license") != "MIT":
            errors.append(f"{label} manifest: license must be MIT")
    if codex.get("skills") != "./skills/":
        errors.append("codex manifest: skills must point to ./skills/")
    claude_skills = claude.get("skills")
    expected_paths = {f"./skills/{name}" for name in EXPECTED_SKILLS}
    if not isinstance(claude_skills, list) or set(claude_skills) != expected_paths:
        errors.append("claude manifest: skills list does not match canonical skill folders")
    if not isinstance(marketplace, dict) or marketplace.get("name") != "ay-skills":
        errors.append("claude marketplace: missing or invalid name")
    elif not isinstance(marketplace.get("plugins"), list) or not marketplace["plugins"]:
        errors.append("claude marketplace: missing plugin entry")
    else:
        entry = marketplace["plugins"][0]
        if not isinstance(entry, dict):
            errors.append("claude marketplace: plugin entry must be an object")
        elif entry.get("version") != version:
            errors.append(f"claude marketplace: version must match VERSION ({version})")

    if os.environ.get("GITHUB_REF_TYPE") == "tag":
        expected_tag = f"v{version}"
        if os.environ.get("GITHUB_REF_NAME") != expected_tag:
            errors.append(f"release tag must match VERSION ({expected_tag})")


def validate_scenarios(root: Path, errors: list[str]) -> None:
    scenarios = load_json(root / "tests" / "scenarios.json", errors)
    competing = load_json(root / "tests" / "competing-skills.json", errors)
    if not isinstance(scenarios, list) or not isinstance(competing, list):
        return
    competing_names = {
        str(skill.get("name"))
        for skill in competing
        if isinstance(skill, dict) and skill.get("name")
    }
    if len(competing_names) != len(competing):
        errors.append("competing skills: names must be present and unique")
    for skill in competing:
        if not isinstance(skill, dict):
            continue
        name = str(skill.get("name", ""))
        if not NAME_RE.fullmatch(name):
            errors.append(f"competing skills: invalid name {name!r}")
        if not str(skill.get("description", "")).strip():
            errors.append(f"competing skills: {name} is missing a description")
    allowed_skills = set(EXPECTED_SKILLS) | competing_names | {"none"}
    if len(scenarios) < 20:
        errors.append(f"scenarios: expected at least 20, found {len(scenarios)}")
    ids: set[str] = set()
    counts = {name: 0 for name in EXPECTED_SKILLS}
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            errors.append("scenarios: every entry must be an object")
            continue
        scenario_id = str(scenario.get("id", ""))
        if not scenario_id or scenario_id in ids:
            errors.append(f"scenarios: missing or duplicate id {scenario_id!r}")
        ids.add(scenario_id)
        skill = scenario.get("expected_skill")
        if skill not in allowed_skills:
            errors.append(f"{scenario_id}: invalid expected_skill {skill!r}")
        elif skill in counts:
            counts[str(skill)] += 1
        if set(scenario) != {"id", "prompt", "expected_skill"}:
            errors.append(f"{scenario_id}: routing cases need only id, prompt, and expected_skill")
    for name, count in counts.items():
        if count < 4:
            errors.append(f"scenarios: {name} has only {count} cases")
    if not any(scenario.get("expected_skill") == "none" for scenario in scenarios):
        errors.append("scenarios: missing a no-skill routing case")
    if not competing_names.issubset({str(scenario.get("expected_skill")) for scenario in scenarios}):
        errors.append("scenarios: every competing skill needs a routing case")


def validate_ay_only_scenarios(root: Path, errors: list[str]) -> None:
    scenarios = load_json(root / "tests" / "ay-only-scenarios.json", errors)
    if not isinstance(scenarios, list):
        return
    if len(scenarios) < 5:
        errors.append(f"AY-only scenarios: expected at least 5, found {len(scenarios)}")
    ids: set[str] = set()
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            errors.append("AY-only scenarios: every entry must be an object")
            continue
        scenario_id = str(scenario.get("id", ""))
        if not scenario_id or scenario_id in ids:
            errors.append(f"AY-only scenarios: missing or duplicate id {scenario_id!r}")
        ids.add(scenario_id)
        if set(scenario) != {"id", "prompt", "expected_skill"}:
            errors.append(f"{scenario_id}: AY-only routing fields do not match schema")
        if scenario.get("expected_skill") not in EXPECTED_SKILLS:
            errors.append(f"{scenario_id}: fallback must select an AY skill")
        if "$ay-" in str(scenario.get("prompt", "")):
            errors.append(f"{scenario_id}: fallback prompt must use implicit routing")


def validate_patterns(label: str, patterns: object, errors: list[str]) -> None:
    if not isinstance(patterns, list) or any(not isinstance(pattern, str) for pattern in patterns):
        errors.append(f"{label}: regex patterns must be strings in a list")
        return
    for pattern in patterns:
        try:
            re.compile(pattern)
        except re.error as error:
            errors.append(f"{label}: invalid regex {pattern!r}: {error}")


def validate_execution_scenarios(root: Path, errors: list[str]) -> None:
    scenarios = load_json(root / "tests" / "execution-scenarios.json", errors)
    if not isinstance(scenarios, list):
        return
    ids: set[str] = set()
    covered: set[str] = set()
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            errors.append("execution scenarios: every entry must be an object")
            continue
        scenario_id = str(scenario.get("id", ""))
        if not scenario_id or scenario_id in ids:
            errors.append(f"execution scenarios: missing or duplicate id {scenario_id!r}")
        ids.add(scenario_id)
        skill = str(scenario.get("skill", ""))
        if skill not in EXPECTED_SKILLS:
            errors.append(f"{scenario_id}: invalid execution skill {skill!r}")
        covered.add(skill)
        if not isinstance(scenario.get("files"), dict):
            errors.append(f"{scenario_id}: files must be an object")
        if "$ay-" in str(scenario.get("prompt", "")):
            errors.append(f"{scenario_id}: behavior prompt must use implicit routing")
        if not any(
            key in scenario
            for key in (
                "expect_no_changes",
                "expected_files",
                "expected_created",
                "created_all",
                "final_any",
                "final_all",
                "final_none",
                "final_regex",
                "expected_png",
                "expected_svg",
                "verify_commands",
                "reproduce",
            )
        ):
            errors.append(f"{scenario_id}: missing observable assertion")
        created_all = scenario.get("created_all", {})
        if not isinstance(created_all, dict):
            errors.append(f"{scenario_id}: created_all must be an object")
        else:
            for path, terms in created_all.items():
                if not isinstance(terms, list) or not terms:
                    errors.append(f"{scenario_id}: {path} needs created_all terms")
        for field in ("expected_png", "expected_svg"):
            value = scenario.get(field, {})
            if not isinstance(value, dict):
                errors.append(f"{scenario_id}: {field} must be an object")
        if "unchanged_files" in scenario and not isinstance(scenario["unchanged_files"], list):
            errors.append(f"{scenario_id}: unchanged_files must be a list")
        if "final_regex" in scenario:
            validate_patterns(f"{scenario_id}/final_regex", scenario["final_regex"], errors)
        commands = scenario.get("verify_commands", [])
        if not isinstance(commands, list) or any(
            not isinstance(command, list) or not command for command in commands
        ):
            errors.append(f"{scenario_id}: verify_commands must contain argument lists")
        reproduce = scenario.get("reproduce", [])
        if not isinstance(reproduce, list):
            errors.append(f"{scenario_id}: reproduce must be a list")
        else:
            for check in reproduce:
                if not isinstance(check, dict) or set(check) != {"path", "command"}:
                    errors.append(f"{scenario_id}: reproduce checks need only path and command")
                    continue
                if not str(check.get("path", "")).strip():
                    errors.append(f"{scenario_id}: reproduce path is missing")
                command = check.get("command")
                if not isinstance(command, list) or not command:
                    errors.append(f"{scenario_id}: reproduce command must be an argument list")
        fixture = scenario.get("fixture")
        if fixture:
            fixture_path = (root / "tests" / "fixtures" / str(fixture)).resolve()
            try:
                fixture_path.relative_to((root / "tests" / "fixtures").resolve())
            except ValueError:
                errors.append(f"{scenario_id}: fixture escapes tests/fixtures")
            else:
                if not fixture_path.is_dir():
                    errors.append(f"{scenario_id}: fixture does not exist")
    missing = set(EXPECTED_SKILLS) - covered
    if missing:
        errors.append(f"execution scenarios: missing skills {', '.join(sorted(missing))}")


def validate_journey_scenarios(root: Path, errors: list[str]) -> None:
    scenarios = load_json(root / "tests" / "journey-scenarios.json", errors)
    if not isinstance(scenarios, list):
        return
    if len(scenarios) < 3:
        errors.append(f"journey scenarios: expected at least 3, found {len(scenarios)}")
    ids: set[str] = set()
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            errors.append("journey scenarios: every entry must be an object")
            continue
        scenario_id = str(scenario.get("id", ""))
        if not scenario_id or scenario_id in ids:
            errors.append(f"journey scenarios: missing or duplicate id {scenario_id!r}")
        ids.add(scenario_id)
        fixture = root / "tests" / "fixtures" / str(scenario.get("fixture", ""))
        if not fixture.is_dir():
            errors.append(f"{scenario_id}: journey fixture does not exist")
        steps = scenario.get("steps")
        if not isinstance(steps, list) or len(steps) < 4:
            errors.append(f"{scenario_id}: journey needs at least four steps")
            continue
        step_ids: set[str] = set()
        for step in steps:
            if not isinstance(step, dict):
                errors.append(f"{scenario_id}: journey step must be an object")
                continue
            step_id = str(step.get("id", ""))
            if not step_id or step_id in step_ids:
                errors.append(f"{scenario_id}: missing or duplicate step {step_id!r}")
            step_ids.add(step_id)
            if "$ay-" in str(step.get("prompt", "")):
                errors.append(f"{scenario_id}/{step_id}: journey prompt must use implicit routing")
            if not isinstance(step.get("assert"), dict) or not step["assert"]:
                errors.append(f"{scenario_id}/{step_id}: missing observable assertions")
            elif "final_regex" in step["assert"]:
                validate_patterns(
                    f"{scenario_id}/{step_id}/final_regex",
                    step["assert"]["final_regex"],
                    errors,
                )
        cross = scenario.get("cross_artifact")
        if not isinstance(cross, dict) or not isinstance(cross.get("required_terms"), dict):
            errors.append(f"{scenario_id}: cross-artifact required terms are missing")
        elif "required_patterns" not in cross:
            errors.append(f"{scenario_id}: cross-artifact semantic patterns are missing")
        else:
            for field in ("required_patterns", "forbidden_patterns"):
                patterns = cross.get(field, {})
                if not isinstance(patterns, dict):
                    errors.append(f"{scenario_id}: {field} must be an object")
                    continue
                for path, expressions in patterns.items():
                    validate_patterns(f"{scenario_id}/{field}/{path}", expressions, errors)
        review = steps[-1] if steps else {}
        review_assert = review.get("assert", {}) if isinstance(review, dict) else {}
        required_review_patterns = {
            r"(?m)^BLOCKER_COUNT: 0\s*$",
            r"(?m)^CRITICAL_COUNT: 0\s*$",
        }
        review_id = review.get("id") if isinstance(review, dict) else None
        if review_id != "review" or not required_review_patterns.issubset(
            set(review_assert.get("final_regex", []))
        ):
            errors.append(f"{scenario_id}: final review must prove zero blocker and critical counts")
        commands = scenario.get("verify_commands")
        if not isinstance(commands, list) or not commands:
            errors.append(f"{scenario_id}: journey needs executable verification")


def validate_product_evals(root: Path, errors: list[str]) -> None:
    scenarios = load_json(root / "tests" / "product-scenarios.json", errors)
    rubric = load_json(root / "tests" / "product-rubric.json", errors)
    schema = load_json(root / "tests" / "product-eval.schema.json", errors)
    if not isinstance(scenarios, list) or not isinstance(rubric, dict) or not isinstance(schema, dict):
        return
    if len(scenarios) < 12:
        errors.append(f"product scenarios: expected at least 12, found {len(scenarios)}")
    ids: set[str] = set()
    holdouts = 0
    categories: set[str] = set()
    required = {"id", "category", "research_mode", "holdout", "prompt", "files", "criteria"}
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            errors.append("product scenarios: every entry must be an object")
            continue
        scenario_id = str(scenario.get("id", ""))
        if not scenario_id or scenario_id in ids:
            errors.append(f"product scenarios: missing or duplicate id {scenario_id!r}")
        ids.add(scenario_id)
        if set(scenario) != required:
            errors.append(f"{scenario_id}: product scenario fields do not match schema")
        if not isinstance(scenario.get("files"), dict) or not scenario.get("files"):
            errors.append(f"{scenario_id}: product scenario needs supplied files")
        if not isinstance(scenario.get("criteria"), list) or len(scenario.get("criteria", [])) < 2:
            errors.append(f"{scenario_id}: product scenario needs at least two criteria")
        if scenario.get("holdout") is True:
            holdouts += 1
        categories.add(str(scenario.get("category", "")))
        if scenario.get("research_mode") not in {"fixed", "live"}:
            errors.append(f"{scenario_id}: product scenario has invalid research_mode")
    if holdouts < 3:
        errors.append(f"product scenarios: expected at least 3 holdouts, found {holdouts}")
    if len(categories) < 5:
        errors.append("product scenarios: expected at least 5 categories")
    if not {"fixed", "live"}.issubset(
        {str(scenario.get("research_mode")) for scenario in scenarios if isinstance(scenario, dict)}
    ):
        errors.append("product scenarios: fixed and live research modes are both required")

    dimensions = rubric.get("dimensions")
    failures = rubric.get("critical_failures")
    if not isinstance(dimensions, list) or len(dimensions) != 10:
        errors.append("product rubric: expected exactly 10 dimensions")
    elif len({str(item.get("id")) for item in dimensions if isinstance(item, dict)}) != 10:
        errors.append("product rubric: dimension ids must be unique")
    if not isinstance(failures, list) or not failures:
        errors.append("product rubric: critical failures are missing")
    for key in (
        "minimum_median_total",
        "minimum_win_rate",
        "maximum_critical_failures",
        "maximum_average_question_batches",
    ):
        if key not in rubric:
            errors.append(f"product rubric: missing {key}")


def validate_docs(root: Path, errors: list[str]) -> None:
    for filename in ("README.md", "README.zh-CN.md"):
        path = root / filename
        if not path.is_file():
            errors.append(f"docs: missing {filename}")
            continue
        text = path.read_text(encoding="utf-8")
        for name in EXPECTED_SKILLS:
            if name not in text:
                errors.append(f"{filename}: missing {name}")
        if "TODO" in text:
            errors.append(f"{filename}: contains TODO placeholder")
        for command in (
            "scripts/run_routing_evals.py",
            "scripts/run_behavior_evals.py",
            "scripts/run_journey_evals.py",
            "scripts/run_product_evals.py",
            "scripts/verify_portable_install.py",
            "scripts/package_release.py",
        ):
            if command not in text:
                errors.append(f"{filename}: missing {command}")
    if not (root / ".github" / "workflows" / "release.yml").is_file():
        errors.append("docs: release workflow is missing")


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAILED: {len(errors)} validation error(s)")
        return 1
    print(f"OK: {len(EXPECTED_SKILLS)} skills and repository surfaces verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
