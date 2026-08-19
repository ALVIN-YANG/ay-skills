---
name: ay-product
description: Research and shape rough product ideas into evidence-backed product definitions, strategies, MVP scopes, requirements, or PRDs. Use when product discovery, competitive research, user and problem framing, product goals, prioritization, or behavioral requirements are the primary deliverable and implementation is not requested, including 做产品定义, 写PRD, 调研竞品, or 这个想法值不值得做. Do not use for visual UI direction, system architecture, API or database design, implementation, store icons, long-form articles, or reviews handled by a more specific skill.
---

# AY Product

## Approval contract

<!-- ay-contract:start -->
- Read the full request and investigate discoverable facts before asking the user.
- Treat review, diagnosis, explanation, and planning as read-only unless the user also requests change.
- Treat a precise instruction as approval when target, observable result, and acceptance boundary are clear.
- A broad outcome authorizes investigation, not file or artifact changes based on choices the agent must invent.
- For a materially underspecified change, present one recommended proposal and wait for approval.
- After approval, execute autonomously inside the approved boundary; do not ask about ordinary implementation details.
- Reopen approval only when new evidence changes behavior, architecture, data contracts, dependencies, scope, risk, cost, rollback, or external actions.
- Perform external actions only when the request or approved proposal includes them. Confirm the exact target before an irreversible action.
- Preserve unrelated and user-authored work. Verify the real requested outcome before claiming completion.
<!-- ay-contract:end -->

## Frame the decision and evidence

Inspect supplied material and the product or repository. Name the decision: validate, build, narrow, differentiate, or stop. Frame the user, trigger, job, workaround, consequence, and hypotheses.

Research only when permitted and decision-relevant. Prefer primary sources; cite consequential claims. Company pages prove offerings, not demand. Never invent research, traction, quotes, or measurements. Separate facts, inferences, recommendations, and assumptions. Honor source limits.

Diagnose observed behavior before redesigning an existing product. Preserve approved choices unless unsafe or impossible. With weak evidence, do not manufacture a PRD.

## Converge with minimal interruption

Find discoverable facts yourself. Ask one compact batch only when choices materially change the user, problem, model, behavior, scope, cost, or risk. Recommend a default and tradeoff. If asked to choose, use explicit assumptions.

When direction is open, compare doing nothing, workarounds, direct products, and adjacent substitutes at the decision point. Derive the switching trigger and wedge; avoid inventories.

Explore plausible directions. Test value, usability, feasibility, viability, ethics, and distribution. For broad concepts, choose one user, job, and wedge. Validation-first or no-build is valid. Rank assumptions; give critical ones a credible test, observable evidence, and decision rule.

## Deliver the product definition

Include relevant items:

- thesis, user, trigger, job, problem, evidence, and current alternative
- chosen position, reason to switch, rejected directions, and tradeoffs when direction is open
- goals, non-goals, journey, relevant states, and product rules
- requirements traceable from trigger to outcome, with testable acceptance criteria and relevant empty, cancel, failure, recovery, permission, and safe-default behavior
- measurements covering signal, denominator, window, guardrails, and decision rule; never invent baselines or targets
- assumptions, tests, risks, dependencies, and open decisions

For sensitive products, state data, access, consent, retention, recourse, and unresolved policy dependencies before recommending scope.

Do not force irrelevant sections or hide missing evidence with detail. No-build needs a bounded test plus explicit build and stop gates, not invented requirements. A fixed brief needs behavioral clarity, not reopened strategy. Distinguish proposals, validated demand, technical proof, and release readiness.

Create files only for a requested handoff. Stop before downstream design and implementation unless authorized.

Report the recommendation, evidence, tradeoffs, and what still requires user or technical validation.
