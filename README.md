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

AY Skills started with the things that kept bothering me when I worked with AI: product ideas became specs before anyone checked the user or market, screen designs drifted between rounds, backend code began without settled boundaries or contracts, bugs were guessed at, streaming voice glitches were patched without tracing the audio path, refactors had no baseline, reviews changed the code, and releases mixed local, submitted, and live states into one vague claim.

So I turned them into standalone skills. A clear request gets done. If a real product or technical choice is still open, the agent investigates, asks once, and continues inside the boundary you approved.

<p align="center">
  <img src="assets/ay-skills-map.svg" alt="Choose among fourteen AY Skills covering expert lenses, product, UI, architecture, API, database, implementation, debugging, audio, improvement, writing, review, icons, and App Store release." width="100%">
</p>

## Skills

| Skill | Use it when | What it does |
|---|---|---|
| [`ay-product`](skills/ay-product/SKILL.md) | Turning a rough idea into a product direction, MVP, requirement, or PRD | Researches the problem and market, recommends a focused product, and makes assumptions testable |
| [`ay-expert-lens`](skills/ay-expert-lens/SKILL.md) | Asking who understands an open problem best or requesting a real expert's documented perspective | Selects the closest verified framework, applies its decision rules, and separates source, inference, and recommendation |
| [`ay-ui`](skills/ay-ui/SKILL.md) | Choosing visual direction, designing screens, or preparing a UI handoff | Locks one visual contract, iterates through visible screens, and records approved decisions |
| [`ay-architecture`](skills/ay-architecture/SKILL.md) | Designing a new system or subsystem before code | Defines the simplest viable boundaries, ownership, deployment, failure, and evolution model |
| [`ay-api`](skills/ay-api/SKILL.md) | Designing REST, GraphQL, gRPC, service, event, or webhook contracts | Derives stable consumer-facing behavior without mirroring storage tables |
| [`ay-database`](skills/ay-database/SKILL.md) | Choosing a database or designing schemas, indexes, transactions, and migrations | Starts from invariants and access paths, then applies the exact engine's behavior |
| [`ay-implement`](skills/ay-implement/SKILL.md) | Implementing an approved feature, design, or general code change | Preserves settled decisions, makes the smallest complete change, and verifies the result |
| [`ay-fix`](skills/ay-fix/SKILL.md) | Debugging a bug, regression, crash, flaky test, or slowdown | Confirms the cause before making the smallest useful repair |
| [`ay-audio`](skills/ay-audio/SKILL.md) | Building or debugging streaming TTS and voice audio on Apple platforms | Traces provider bytes through the mixer and device, then proves audible playback |
| [`ay-improve`](skills/ay-improve/SKILL.md) | Refactoring or improving performance and maintainability | Establishes a baseline, makes the change, and compares the result |
| [`ay-write`](skills/ay-write/SKILL.md) | Writing or substantially rewriting an article, tutorial, or visual explainer | Produces clear, natural long-form prose without filler |
| [`ay-review`](skills/ay-review/SKILL.md) | Reviewing a diff, branch, plan, or release | Stays read-only and reports consequential issues backed by evidence |
| [`ay-icon`](skills/ay-icon/SKILL.md) | Creating or replacing an App Store, Play Store, or launcher icon | Locks metaphor and style, then generates, inspects, and installs the mark |
| [`ay-app-store`](skills/ay-app-store/SKILL.md) | Creating store screenshots or preparing, submitting, monitoring, and recovering an Apple App Store release | Builds truthful screenshots from the release-build UI, then reconciles code, metadata, commerce, account, and live review state |

Install one or all of them. They do not depend on a router or on each other, and a small change does not have to become a planning exercise.

For a full product, the usual handoff is `ay-product → ay-ui → ay-architecture → ay-api → ay-database → ay-implement`, with `ay-review` checking consistency or implementation when useful. Once a release build exists, `ay-app-store` can turn its real UI into reproducible store screenshots before submission. This is guidance, not a required pipeline: architecture can move earlier when technical feasibility blocks UI, and any skill can run alone from existing approved inputs.

0.8.0 adds `ay-expert-lens` for applying verified expert frameworks to open questions without impersonation or invented quotes. Catalog coexistence routing, artifact and runtime assertions, three end-to-end journeys, standalone install checks, and verified release archives remain separate proof layers.

## Install

List the skills first, then choose interactively:

```bash
npx skills@latest add ALVIN-YANG/ay-skills -l
npx skills@latest add ALVIN-YANG/ay-skills
```

Install a product-and-design set:

```bash
npx skills@latest add ALVIN-YANG/ay-skills -s ay-product ay-ui ay-architecture ay-review -a codex claude-code -g -y
```

Install the full-stack delivery set:

```bash
npx skills@latest add ALVIN-YANG/ay-skills -s ay-product ay-ui ay-architecture ay-api ay-database ay-implement ay-review -a codex claude-code -g -y
```

Install all fourteen only when that is what you want:

```bash
npx skills@latest add ALVIN-YANG/ay-skills -s '*' -a codex claude-code -g -y
```

Claude Code also supports the native plugin:

```text
/plugin marketplace add ALVIN-YANG/ay-skills
/plugin install ay-skills@ay-skills
```

Inspect, update, or remove global skills:

```bash
npx skills@latest list -g
npx skills@latest update -g
npx skills@latest remove ay-audio -g
```

Describe the task in ordinary language. The matching skill should fire on its own. Naming `$ay-implement` or another skill is optional, only when you want to force one.

```text
Research this idea and define a focused, testable MVP.
Choose the real expert whose documented framework best fits this open decision, then apply it.
Design the approved product screens one at a time, then prepare design.md.
Design the system architecture, API contract, and database schema before code.
Add an export flow to this app.
Diagnose and fix this intermittent test.
Diagnose why this macOS streaming TTS crackles and fix the proven audio boundary.
Simplify this module from a measured baseline.
Turn these notes into a clear illustrated article.
Review this branch without changing files.
Redesign this app's store icon and install the asset set.
Create reproducible Mac App Store screenshots from the current release build.
Prepare this iOS app for App Review and submit the verified version.
```

## A short example

```text
You: Add offline mode.

AY: The app currently assumes a live connection. I recommend read-only cached data
offline, a visible stale-data state, and queued writes as a non-goal for this change.
I will verify cold launch, reconnect, and stale-data behavior. Approve this boundary?

You: Approved.

AY: Implemented the approved flow and ran the focused tests. Queued writes remain out
of scope; real-device reconnect behavior is the only unverified surface.
```

## Use with other skills

AY Skills can sit beside specific artifact and tool skills such as frontend design, PDF, spreadsheet, or accessibility workflows. The specific skill should lead; AY supplies the approval and evidence boundary when useful.

Choose the primary skill from the deliverable when responsibilities overlap:

| Request | Primary when both are installed |
|---|---|
| Open-ended decision explicitly asking for a real expert framework | `ay-expert-lens`; a domain skill still owns any concrete artifact or execution |
| First-person expert or celebrity simulation | A dedicated persona or Best Minds skill; `ay-expert-lens` does not impersonate the person |
| General App Store preparation, submission, or rejection recovery | A dedicated App Store release skill; `ay-app-store` leads real-UI screenshot generation |
| Apple AppIcon or `.icns` production and installation | A dedicated Apple icon asset skill; `ay-icon` leads an open metaphor and direction |
| Prose-only natural Chinese long-form writing | A dedicated Chinese writing skill; `ay-write` leads research, English, or illustrated articles |
| Diagnosis without a requested repair | A dedicated diagnosis workflow; use `ay-fix` when the repair should be completed |
| Choosing or deepening a module interface or seam | A dedicated codebase-design skill; use `ay-improve` after the refactor boundary is settled |
| Code review since a commit or branch | A dedicated code-review skill; use `ay-review` across product, design, architecture, and implementation |

If the boundary is still ambiguous, install one workflow at project scope or explicitly name `$skill-name`.

## Three realistic handoff journeys

The repository carries the same product material through consecutive stages instead of letting every skill write an unrelated document:

- FieldLog: product, real SVG screen, modular monolith, API, PostgreSQL, executable implementation, and cross-artifact review.
- PairDown: local macOS product, screen, architecture, SQLite, no-auto-delete implementation, and review.
- NextStop: account-free transit product, offline and permission states, screen, architecture, API, executable implementation, and review.

These are synthetic evaluation fixtures, not user-research or production-success claims. See [`tests/journey-scenarios.json`](tests/journey-scenarios.json).

## When it stops to ask

A precise request is already approval: investigate, make the change, and verify it.

The agent stops when it would otherwise have to decide product behavior, architecture, data contracts, dependencies, scope, risk, cost, rollback, or an external action for you. Once you approve the direction, it keeps going unless that boundary changes.

`ay-product` investigates discoverable product and market facts itself, asks only about decisions that materially change the direction, and stops before UI, architecture, and implementation. The design skills preserve the same rule: they produce approved contracts, while `ay-implement` owns code.

Reviews are the exception: `ay-review` stays read-only unless you ask for fixes.

## Writing with visuals

`ay-write` works out the point, structure, and purpose of each visual before choosing a tool. Small precise diagrams use SVG; editable architecture uses draw.io or Excalidraw; quantitative claims use charts with traceable data; covers and scenes can use image generation.

It only asks when style or editability would change the result, or when a new tool, dependency, paid service, or project runtime is required.

## Small by design

Fourteen skills. No router, modes, hooks, telemetry, statusline, automatic commits, or mandatory planning files. Each skill has one job and can be installed on its own.

AY Skills follows the [Agent Skills specification](https://agentskills.io/specification). Portable installation, live Codex and Claude routing, the native Claude Code plugin, CI, release contents, and remote installation are separate verification layers; support is claimed only for layers actually checked before a release. The Codex manifest targets local marketplace testing and future directory submission, not a currently public Codex plugin listing.

<details>
<summary>Development and verification</summary>

```bash
python3 scripts/verify_skills.py
python3 -m unittest discover -s tests -v
python3 scripts/verify_portable_install.py
python3 scripts/package_release.py --output /tmp/ay-skills.tar.gz
python3 scripts/package_release.py --verify /tmp/ay-skills.tar.gz
python3 scripts/run_routing_evals.py --host codex
python3 scripts/run_routing_evals.py --host codex --catalog global
python3 scripts/run_routing_evals.py --host codex --catalog ay-only
python3 scripts/run_routing_evals.py --host claude
python3 scripts/run_behavior_evals.py
python3 scripts/run_journey_evals.py
python3 scripts/run_product_evals.py
python3 scripts/run_product_evals.py --research-mode live
```

CI runs structural, unit, standalone-install, and release-archive checks. Routing can use the reproducible competitor fixture, the current global Codex catalog, or AY alone to prove standalone fallbacks. Codex behavior cases install AY beside fixture competitors, never name the target skill in the prompt, and assert files, PNGs, SVGs, protected tests, reproducible generated assets, and executable results. Journey cases keep one workspace across handoffs and require semantic invariants plus a zero-blocker final review. Product evaluation retains fixed cases, holdouts, and one rubric; live market research runs separately.

Model-backed evaluations require local authenticated CLIs and stay outside ordinary CI. PNG fixture cases also require Pillow; run them through `uv run --with pillow` when it is not already available, without adding it to the project. Evaluations write ignored results under `eval-results/`; journey failures preserve the workspace and final messages, and `--recheck-dir` can re-run final assertions without another model call. Network failures are reported separately as `INFRA`, not skill failures. Release notes should record only the model, CLI, catalog, and pass rate actually checked for that version. Pushing a `v<VERSION>` tag builds, publishes, downloads, and re-verifies the GitHub Release, so source version, tag, and public release remain distinct states.

</details>

## Influences

AY Skills is original work informed by [Superpowers](https://github.com/obra/superpowers), [Anthropic Skills](https://github.com/anthropics/skills), [wshobson/agents](https://github.com/wshobson/agents), [PM Skills](https://github.com/phuryn/pm-skills), [awesome-copilot](https://github.com/github/awesome-copilot), [claude-skills](https://github.com/alirezarezvani/claude-skills), [mattpocock/skills](https://github.com/mattpocock/skills), and [Waza](https://github.com/tw93/Waza). The useful ideas are approval before implementation, distinctive and consistent UI direction, separate architecture/API/database responsibilities, engine-specific storage design, evidence-first discovery, and small skill boundaries.

The store screenshot workflow is additionally informed by [store-screenshot-mockups](https://github.com/iamngoni/store-screenshot-mockups), [app-store-screenshots](https://github.com/ParthJadhav/app-store-screenshots), and [Shotsmith](https://github.com/gyugyu86/app-store-screenshot-studio): preserve the real shipped UI, make the deck reproducible, render at exact dimensions, and verify exported files. AY does not copy their skill text or runtime code, and intentionally leaves out mandatory modes, documents, commits, and architecture patterns.

The question-relative expert selection in `ay-expert-lens` was prompted by [Best Minds](https://github.com/Agentchengfeng/best-minds) (MIT). AY uses an original, narrower workflow: apply verifiable published frameworks, distinguish source from inference, and never impersonate the person or invent what they would say.

## License

[MIT](LICENSE) © 2026 Alvin Yang
