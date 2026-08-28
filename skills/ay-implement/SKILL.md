---
name: ay-implement
description: Implement and verify an approved product or software change inside a human-approved boundary. Use when the user asks to add a feature, implement an approved design, change product behavior, or make a general code change, including 加功能, 实现, 做一下, 落地, or 改代码, and no more specific implementation skill applies. Do not use for product discovery, UI or architecture design-only work, bugs, optimization, long-form writing, review, store icons, or other specialized artifact work.
---

# AY Implement

Turn approved intent and design into a verified change without reopening settled decisions.

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

## Establish the implementation contract

Read project instructions, working-tree state, relevant code and tests, nearby history, and approved product, UI, architecture, API, or database artifacts that exist. Trace the requested behavior from entry point through affected consumers. Preserve stable terms, states, authorization, failure behavior, and data invariants across those handoffs. Separate settled decisions, discoverable facts, and unresolved choices.

Act directly when the request or approved artifact fixes the target, observable result, and acceptance boundary. A small explicit change needs no restated plan.

If implementation would require inventing material product behavior, system shape, data contract, dependency, migration, or external action, present one recommended proposal and wait. Do not recreate a full discovery process inside this skill. Ask only about the current decision that cannot be discovered.

## Implement coherently

Make the smallest complete change within repository conventions. Preserve behavior outside the approved boundary. Keep tests, configuration, generated artifacts, and migrations coherent.

Organize code around cohesive responsibilities. Keep a function at one abstraction level and a file or package centered on a recognizable domain capability. Split mixed change reasons, lifecycles, dependencies, or side effects; keep code together when separation creates pass-through files or one-use interfaces. Avoid generic `util`, `common`, `helpers`, or `types` dumping grounds. Keep public surfaces small and names consistent with approved domain terms.

Add artifacts, abstractions, or dependencies only when requested, repository-required, or needed. Do not translate every upstream artifact mechanically.

If new evidence triggers the approval contract, stop at a safe point, show how it changes the agreed result, and recommend the next decision. Otherwise continue without another checkpoint.

## Verify the delivered result

Exercise the highest relevant proof surface: source check, test, build, package, install, migration rehearsal, deployment, runtime, device, render, or published page. A sentinel edit or keyword-bearing file does not prove a feature. Trace important acceptance criteria and upstream states to executed evidence. Keep proof layers distinct.

Lead with the delivered outcome. State what was verified, external actions completed, and any proof surface still unverified.
