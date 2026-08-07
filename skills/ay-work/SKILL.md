---
name: ay-work
description: Shape, implement, and verify product or software changes inside a human-approved boundary. Use when a user requests a new feature, product requirement, user scenario, architecture decision, or general code and file change and no more specific installed skill applies. Do not use for bugs, optimization, long-form writing, review, or specialized artifact and tool work.
---

# AY Work

Turn intent into a verified change. Earn direction once, then finish without ceremony.

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

## Establish context

Read project instructions, working-tree state, relevant code and tests, nearby history, and linked or live documentation when it affects the answer. Separate facts, assumptions, and decisions. Ask for decisions; find facts yourself.

## Decide whether to act

Act directly when the request already fixes the target, result, and acceptance boundary. A small explicit change needs no restated plan.

A request to build an undefined feature approves the goal, not product behavior the agent would have to invent. Shape and get approval for those decisions first.

Otherwise, map the decision tree. Ask the current frontier in one compact batch: only decisions whose prerequisites are settled. Recommend an answer and name the tradeoff for each. Do not ask the user to repeat repository facts.

When decisions are resolved, propose:

- outcome and user-visible behavior
- scope and non-goals
- recommended approach and affected boundaries
- material risks, dependencies, migration, rollback, or external actions
- acceptance evidence

Wait for approval before changing files.

## Execute

Follow repository conventions and make the smallest coherent change. Create specs, tickets, scratch files, or new abstractions only when the user requests them, the repository requires them, or the work genuinely needs a durable handoff.

If a reopen condition appears, stop at a safe point. Show the new evidence, explain how it changes the approved proposal, and recommend the decision. Otherwise continue without another checkpoint.

## Verify and report

Exercise the highest relevant proof surface: source check, test, build, package, install, deployment, production behavior, device, render, or published page. Keep those layers distinct.

Lead with the delivered outcome. State evidence that ran, external actions completed, and any proof surface still unverified.
