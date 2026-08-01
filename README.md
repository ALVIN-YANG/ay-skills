<div align="center">
  <h1>AY Skills</h1>
  <p><strong>Understand first. Interrupt less. Finish the job.</strong></p>
  <p>
    <a href="https://github.com/ALVIN-YANG/ay-skills/actions/workflows/test.yml"><img src="https://img.shields.io/github/actions/workflow/status/ALVIN-YANG/ay-skills/test.yml?branch=main&style=flat-square&label=tests" alt="Tests"></a>
    <a href="https://github.com/ALVIN-YANG/ay-skills/releases"><img src="https://img.shields.io/github/v/release/ALVIN-YANG/ay-skills?style=flat-square" alt="Release"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="MIT License"></a>
  </p>
  <p><a href="README.zh-CN.md">简体中文</a></p>
</div>

AY Skills started with five things that kept bothering me when I worked with AI: it began before it understood the request, guessed at bugs, refactored without a baseline, wrote like a manual, and changed code during a review.

So I turned them into five standalone skills. A clear request gets done. If a real product or technical choice is still open, the agent investigates, asks once, and continues inside the boundary you approved.

<p align="center">
  <img src="assets/ay-skills-map.svg" alt="Choose an AY Skill: ay-work for new work, ay-fix for bugs, ay-improve for measured improvements, ay-write for clear visual writing, and ay-review for read-only review." width="100%">
</p>

## Skills

| Skill | Use it when | What it does |
|---|---|---|
| [`ay-work`](skills/ay-work/SKILL.md) | Building a feature or working through an unclear requirement | Clarifies the open choices, then builds and verifies the result |
| [`ay-fix`](skills/ay-fix/SKILL.md) | Debugging a bug, regression, crash, flaky test, or slowdown | Confirms the cause before making the smallest useful repair |
| [`ay-improve`](skills/ay-improve/SKILL.md) | Refactoring or improving performance and maintainability | Establishes a baseline, makes the change, and compares the result |
| [`ay-write`](skills/ay-write/SKILL.md) | Writing, rewriting, or explaining something with useful visuals | Produces clear, natural prose without filler |
| [`ay-review`](skills/ay-review/SKILL.md) | Reviewing a diff, branch, plan, or release | Stays read-only and reports consequential issues backed by evidence |

Install one or all five. They do not depend on a router or on each other, and a small change does not have to become a planning exercise.

## Install

Install all five for Codex and Claude Code:

```bash
npx skills@latest add ALVIN-YANG/ay-skills -a codex claude-code -g -y
```

To choose individual skills or install them in the current project:

```bash
npx skills@latest add ALVIN-YANG/ay-skills
```

Claude Code also supports the native plugin:

```text
/plugin marketplace add ALVIN-YANG/ay-skills
/plugin install ay-skills@ay-skills
```

Skills are picked up automatically when the task matches. You can also name one directly:

```text
Use $ay-work to add an export flow to this app.
Use $ay-fix to diagnose and fix this intermittent test.
Use $ay-improve to simplify this module from a measured baseline.
Use $ay-write to turn these notes into a clear illustrated article.
Use $ay-review to review this branch without changing files.
```

## When it stops to ask

A precise request is already approval: investigate, make the change, and verify it.

The agent stops when it would otherwise have to decide product behavior, architecture, data contracts, dependencies, scope, risk, cost, rollback, or an external action for you. Once you approve the direction, it keeps going unless that boundary changes.

Reviews are the exception: `ay-review` stays read-only unless you ask for fixes.

## Writing with visuals

`ay-write` works out the point, structure, and purpose of each visual before choosing a tool. Small precise diagrams use SVG; editable architecture uses draw.io or Excalidraw; quantitative claims use charts with traceable data; covers and scenes can use image generation.

It only asks when style or editability would change the result, or when a new tool, dependency, paid service, or project runtime is required.

## Small by design

Five skills. No router, modes, hooks, telemetry, statusline, automatic commits, or mandatory planning files. Each skill has one job and can be installed on its own.

AY Skills follows the [Agent Skills specification](https://agentskills.io/specification). Portable installation is tested in Codex and Claude Code, and the Claude Code plugin is tested separately. Other hosts are not claimed until they are verified.

<details>
<summary>Development and verification</summary>

```bash
python3 scripts/verify_skills.py
python3 -m unittest discover -s tests -v
python3 scripts/run_behavior_evals.py --host codex
python3 scripts/run_behavior_evals.py --host claude
```

The behavior suite covers clear changes, vague features, debugging, measured improvement, illustrated writing, read-only review, external actions, and standalone invocation. Live Claude behavior checks require a reachable Claude API.

</details>

## Influences

AY Skills is original work informed by [mattpocock/skills](https://github.com/mattpocock/skills), [Superpowers](https://github.com/obra/superpowers), and [Waza](https://github.com/tw93/Waza): useful questioning, root-cause discipline, and small skills with clear boundaries. It does not copy their skill text or runtime code.

## License

[MIT](LICENSE) © 2026 Alvin Yang
