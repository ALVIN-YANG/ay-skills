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

Inspect supplied material and the product or repository. Name the decision: validate, build, narrow, differentiate, or stop. Frame the user, trigger, job, current workaround, consequence, and riskiest hypotheses.

Research only when permitted and decision-relevant. Prefer primary sources. Company pages prove offerings, not demand. Never invent research, traction, quotes, or measurements. Separate facts, inferences, recommendations, and assumptions.

Diagnose observed behavior before redesigning an existing product. Preserve approved choices unless unsafe or impossible. With weak evidence, do not manufacture a PRD.

## Converge with minimal interruption

Find discoverable facts yourself. Ask one compact batch only when a choice changes user, behavior, scope, cost, or risk. Recommend a default and tradeoff.

When direction is open, compare doing nothing, workarounds, products, and substitutes. Derive the switching trigger and wedge instead of listing features.

Choose one user, job, and wedge for a broad concept. Test value, usability, feasibility, viability, ethics, and distribution. Give critical assumptions a test, evidence, and decision rule. No-build is valid.

Read [product modes](references/product-modes.md) when deciding among a new idea, existing-product diagnosis, fixed brief, validation-only proposal, or sensitive product.

## Deliver the product definition

Include only relevant items:

- user, trigger, job, evidence, current alternative, and thesis
- chosen position, switch reason, tradeoffs, goals, and non-goals
- journey, stable terms, states, rules, and traceable requirements
- testable acceptance for relevant empty, cancel, failure, recovery, permission, and safe-default behavior
- measurements with signal, denominator, window, guardrail, and decision rule; never invent targets
- assumptions, tests, risks, dependencies, and open decisions

Do not force sections or hide missing evidence with detail. Distinguish proposals, validated demand, technical proof, and release readiness.

Create files only for a requested handoff. Preserve terms and state names for downstream traceability. Stop before design and implementation unless authorized.

Report the recommendation, evidence, tradeoffs, and what still requires user or technical validation.
