#!/usr/bin/env python3
"""Dependency-free structural checks for AY Skills."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
EXPECTED_SKILLS = (
    "ay-work",
    "ay-fix",
    "ay-improve",
    "ay-write",
    "ay-review",
)
FRONTMATTER_RE = re.compile(r"\A---\n(?P<yaml>.*?)\n---\n(?P<body>.*)\Z", re.DOTALL)
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
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

    validate_manifests(root, errors)
    validate_scenarios(root, errors)
    validate_docs(root, errors)
    return errors


def load_json(path: Path, errors: list[str]) -> dict | list | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{path.relative_to(path.parents[1])}: invalid JSON: {error}")
        return None


def validate_manifests(root: Path, errors: list[str]) -> None:
    codex = load_json(root / ".codex-plugin" / "plugin.json", errors)
    claude = load_json(root / ".claude-plugin" / "plugin.json", errors)
    marketplace = load_json(root / ".claude-plugin" / "marketplace.json", errors)
    if not isinstance(codex, dict) or not isinstance(claude, dict):
        return
    for label, manifest in (("codex", codex), ("claude", claude)):
        if manifest.get("name") != "ay-skills":
            errors.append(f"{label} manifest: name must be ay-skills")
        if manifest.get("version") != "0.1.0":
            errors.append(f"{label} manifest: version must be 0.1.0")
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


def validate_scenarios(root: Path, errors: list[str]) -> None:
    scenarios = load_json(root / "tests" / "scenarios.json", errors)
    if not isinstance(scenarios, list):
        return
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
        if skill not in counts:
            errors.append(f"{scenario_id}: invalid expected_skill {skill!r}")
        else:
            counts[str(skill)] += 1
        if scenario.get("first_step") not in {"execute", "investigate", "review", "outline"}:
            errors.append(f"{scenario_id}: invalid first_step")
        if scenario.get("change_gate") not in {
            "already-approved",
            "approval-before-change",
            "read-only",
        }:
            errors.append(f"{scenario_id}: invalid change_gate")
    for name, count in counts.items():
        if count < 4:
            errors.append(f"scenarios: {name} has only {count} cases")


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
