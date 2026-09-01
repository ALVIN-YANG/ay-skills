# AY Skills

[![Tests](https://img.shields.io/github/actions/workflow/status/ALVIN-YANG/ay-skills/test.yml?branch=main&style=flat-square&label=tests)](https://github.com/ALVIN-YANG/ay-skills/actions/workflows/test.yml)
[![Release](https://img.shields.io/github/v/release/ALVIN-YANG/ay-skills?style=flat-square)](https://github.com/ALVIN-YANG/ay-skills/releases)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)

[简体中文](README.zh-CN.md)

AY Skills is a set of fifteen standalone skills for coding agents. Each skill defines when the agent can proceed, when a decision needs your approval, and what evidence counts as done.

## Quick start

List the skills, then choose what to install:

```bash
npx skills@latest add ALVIN-YANG/ay-skills -l
npx skills@latest add ALVIN-YANG/ay-skills
```

Describe the task normally. The matching skill should load from the request; naming `$ay-implement` or another skill is optional.

```text
Add CSV export to this app and verify the result.
```

## How it behaves

- A precise request runs directly.
- A choice that changes product behavior, architecture, data contracts, dependencies, scope, risk, cost, rollback, or an external action stops for approval.
- Approved work continues inside that boundary and reports the highest proof actually reached.
- Reviews stay read-only unless fixes are requested.

The skills are independent. They do not require a router, shared runtime, modes, hooks, telemetry, automatic commits, or planning files.

## Skills

### Plan and design

| Skill | Use it for |
|---|---|
| [`ay-expert-lens`](skills/ay-expert-lens/SKILL.md) | Apply a real expert's documented framework to an open decision |
| [`ay-product`](skills/ay-product/SKILL.md) | Research a product idea and define a focused, testable direction |
| [`ay-ui`](skills/ay-ui/SKILL.md) | Choose a visual direction, design screens, and prepare a UI handoff |
| [`ay-architecture`](skills/ay-architecture/SKILL.md) | Set system boundaries, ownership, deployment, and failure behavior |
| [`ay-api`](skills/ay-api/SKILL.md) | Design consumer-facing APIs, events, webhooks, and service contracts |
| [`ay-database`](skills/ay-database/SKILL.md) | Design schemas, indexes, transactions, and migrations for the exact engine |

### Build and hand off

| Skill | Use it for |
|---|---|
| [`ay-implement`](skills/ay-implement/SKILL.md) | Implement an approved change and verify the result |
| [`ay-integration-docs`](skills/ay-integration-docs/SKILL.md) | Document only the API and message changes a specific client needs |
| [`ay-fix`](skills/ay-fix/SKILL.md) | Confirm a bug's cause, then make the smallest useful repair |
| [`ay-improve`](skills/ay-improve/SKILL.md) | Refactor or optimize from a measured baseline |
| [`ay-review`](skills/ay-review/SKILL.md) | Review product and delivery artifacts without silently editing them |

### Specialized work

| Skill | Use it for |
|---|---|
| [`ay-audio`](skills/ay-audio/SKILL.md) | Build or debug streaming TTS and voice playback on Apple platforms |
| [`ay-write`](skills/ay-write/SKILL.md) | Write or substantially revise articles, tutorials, and visual explainers |
| [`ay-icon`](skills/ay-icon/SKILL.md) | Design and install store or launcher icons |
| [`ay-store-screenshots`](skills/ay-store-screenshots/SKILL.md) | Produce reproducible App Store screenshots from shipped UI |

See [Choosing a skill](docs/choosing-a-skill.md) for common overlaps and a typical product handoff.

## One example

```text
You: Add offline mode.

AY: I found that the app currently assumes a live connection. I recommend making
cached data read-only offline, showing when it became stale, and leaving queued
writes out of this change. I will check cold launch, reconnect, and stale-data
behavior. Approve this boundary?

You: Approved.

AY: Implemented the approved flow and ran the focused tests. Queued writes remain
out of scope; real-device reconnect behavior is the only unverified surface.
```

## Evidence in this repository

The test suite checks routing, behavior, protected files, reproducible assets, portable installation, release archives, and multi-skill handoffs. The three end-to-end journeys—FieldLog, PairDown, and NextStop—are synthetic fixtures, not claims of user research or production adoption. Their inputs and assertions live in [`tests/journey-scenarios.json`](tests/journey-scenarios.json).

Development commands and the limits of each proof layer are in [CONTRIBUTING.md](CONTRIBUTING.md).

## Other install options

Install all fifteen skills for Codex and Claude Code:

```bash
npx skills@latest add ALVIN-YANG/ay-skills -s '*' -a codex claude-code -g -y
```

<details>
<summary>Claude Code plugin and maintenance commands</summary>

```text
/plugin marketplace add ALVIN-YANG/ay-skills
/plugin install ay-skills@ay-skills
```

```bash
npx skills@latest list -g
npx skills@latest update -g
npx skills@latest remove ay-audio -g
```

</details>

AY Skills follows the [Agent Skills specification](https://agentskills.io/specification). The Codex manifest is for local marketplace testing and a possible future directory submission; this repository does not claim a public Codex plugin listing.

## Acknowledgements and license

The project is original work informed by several agent-skill and app-delivery projects. The exact sources, licenses, and boundaries are recorded in [docs/influences.md](docs/influences.md).

[MIT](LICENSE) © 2026 Alvin Yang
