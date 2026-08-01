<div align="center">
  <h1>AY Skills</h1>
  <p><strong>Lightweight, human-approved workflows for advanced AI coding agents.</strong></p>
  <p>
    <a href="https://github.com/ALVIN-YANG/ay-skills/actions/workflows/test.yml"><img src="https://img.shields.io/github/actions/workflow/status/ALVIN-YANG/ay-skills/test.yml?branch=main&style=flat-square&label=tests" alt="Tests"></a>
    <a href="https://github.com/ALVIN-YANG/ay-skills/releases"><img src="https://img.shields.io/github/v/release/ALVIN-YANG/ay-skills?style=flat-square" alt="Release"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="MIT License"></a>
  </p>
  <p><a href="README.zh-CN.md">简体中文</a></p>
</div>

Advanced models usually know how to write code. The harder problem is collaboration: they guess before understanding, turn vague requests into unapproved design decisions, or keep asking after the direction is already clear.

AY Skills gives them one operating contract:

> **Understand the context. Earn direction once. Finish inside the approved boundary. Prove the real outcome.**

<p align="center">
  <img src="assets/ay-skills-map.svg" alt="Choose an AY Skill by primary intent: ay-work for new work, ay-fix for broken behavior, ay-improve for measured improvements, ay-write for illustrated writing, and ay-review for evidence-backed assessment." width="100%">
</p>

## Five independent skills

| Skill | Use it for | What changes |
|---|---|---|
| [`ay-work`](skills/ay-work/SKILL.md) | Product requirements, user scenarios, features, architecture, general changes | Shapes unclear direction, then implements and verifies the approved result |
| [`ay-fix`](skills/ay-fix/SKILL.md) | Bugs, regressions, crashes, flaky tests, unexpected slowness | Proves root cause before the smallest authorized repair |
| [`ay-improve`](skills/ay-improve/SKILL.md) | Refactoring, architecture, performance, maintainability | Requires a real baseline before restructuring |
| [`ay-write`](skills/ay-write/SKILL.md) | Natural technical writing and illustrated articles | Aligns thesis, outline, sources, and useful visuals before drafting |
| [`ay-review`](skills/ay-review/SKILL.md) | Diffs, branches, plans, release readiness | Stays read-only and reports only consequential, evidence-backed findings |

Install one or all five. Each skill is self-contained; none depends on a router or another AY skill.

## Install

Install for Codex and Claude Code with the portable Agent Skills path:

```bash
npx skills@latest add ALVIN-YANG/ay-skills -a codex claude-code -g -y
```

Run the installer without `-y` to select individual skills or a project-local destination:

```bash
npx skills@latest add ALVIN-YANG/ay-skills
```

Claude Code can also install the native plugin:

```text
/plugin marketplace add ALVIN-YANG/ay-skills
/plugin install ay-skills@ay-skills
```

The skills are model-invoked by default. You can still call one explicitly:

```text
Use $ay-work to add an export flow to this app.
Use $ay-fix to diagnose and fix this intermittent test.
Use $ay-improve to simplify this module from a measured baseline.
Use $ay-write to create a practical illustrated article.
Use $ay-review to review this branch without changing files.
```

## One approval, not endless checkpoints

| Request | AY behavior |
|---|---|
| “Change Retry to Try again and run the UI check.” | The instruction is already approval. Inspect, change, verify. |
| “Improve the homepage.” | Inspect first, propose one direction, wait before changing files. |
| “Fix this Bug.” | Diagnose. Repair directly only when the root-cause fix is unique, local, reversible, and behavior-preserving. |
| “Review this branch.” | Read and report. Do not autofix. |
| “Implement the approved plan and push if green.” | Execute and push without asking again unless the approved boundary changes. |

Approval reopens only when new evidence changes product behavior, architecture, data contracts, dependencies, scope, risk, cost, rollback, or external actions. Ordinary implementation decisions remain the agent's job.

## Illustrated writing without tool interviews

`ay-write` proposes the thesis, outline, and visual plan together. After approval, it chooses the medium from the explanatory job and available capabilities:

| Need | Default |
|---|---|
| Precise small diagram | SVG |
| Complex editable architecture | draw.io source plus export |
| Conceptual or hand-drawn explanation | Excalidraw source plus export |
| Quantitative claim | Chart backed by traceable data |
| Cover, scene, or metaphor | Image generation |

It asks about tools only when style or editability changes the result. Installing a plugin, dependency, paid capability, or project runtime still requires approval.

## Deliberately light

- Five skills, no router and no mode labels.
- Every `SKILL.md` is under 150 lines and 500 body words.
- No hooks, telemetry, statusline, bootstrap injection, global rules, automatic commits, or mandatory planning files.
- Portable `SKILL.md` folders are the source of truth for every host.
- Source tests, plugin validation, isolated installs, host behavior, CI, release contents, and remote installs are reported as separate proof layers.

## Compatibility

Codex behavior and both portable installs are tested. Claude Code's native manifest, isolated marketplace install, and five-skill discovery are tested; its live behavior suite is included but requires a reachable Claude API. Other tools that implement the [Agent Skills specification](https://agentskills.io/specification) can consume the same folders, but are not claimed as verified until tested.

## Development

```bash
python3 scripts/verify_skills.py
python3 -m unittest discover -s tests -v
python3 scripts/run_behavior_evals.py --host codex
python3 scripts/run_behavior_evals.py --host claude
```

The behavior suite covers precise changes, vague features, bug approval boundaries, evidence-backed improvement, illustrated writing, read-only review, external actions, and standalone auto-invocation.

## Influences

AY Skills is original work informed by:

- [mattpocock/skills](https://github.com/mattpocock/skills): fact-versus-decision grilling and concise, composable skill design.
- [obra/superpowers](https://github.com/obra/superpowers): root-cause discipline, approval before design-changing work, and evidence before completion claims.
- [tw93/Waza](https://github.com/tw93/Waza): outcome/evidence contracts, scope restraint, project-context extraction, and human prose.

All three are MIT licensed. AY Skills does not copy their skill text or runtime code.

## License

[MIT](LICENSE) © 2026 Alvin Yang
