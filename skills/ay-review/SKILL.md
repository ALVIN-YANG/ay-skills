---
name: ay-review
description: Review product, UI, architecture, API, database, implementation, or delivery artifacts for intent, correctness, risk, cross-artifact consistency, and proof. Use when a general audit, review-then-fix, 发布前检查, or check spanning several handoffs is requested. Let a dedicated since-commit or pull-request code-review skill lead branch diffs when installed, and yield to specific security or accessibility review.
---

# AY Review

Find consequential defects without manufacturing noise. Stay read-only unless fixes are explicitly authorized.

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

## Fix the review frame

Identify the comparison point and originating intent. Read repository instructions, current working-tree state, changed files, surrounding callers and consumers, tests, and claims made about the work. When product, UI, architecture, API, or database artifacts exist, trace important behavior across them instead of reviewing each in isolation.

If the target or intended behavior cannot be discovered, ask one focused decision question before claiming spec compliance.

## Review what matters

Check:

- **Intent:** requested behavior, non-goals, missing consumers, scope drift.
- **Consistency:** user journeys, system boundaries, API contracts, data invariants, and implementation agree where they overlap.
- **Correctness:** concrete inputs, states, sequences, boundaries, and failure handling.
- **Risk:** data loss, permissions, security, concurrency, compatibility, migration, rollback, and external effects when relevant.
- **Evidence:** whether tests exercise the changed path and whether source, build, package, install, deployment, runtime, device, or published proof is being conflated.

Every finding must have an exact location or artifact, a triggering state, a real impact, and evidence that existing guards do not prevent it. Read upstream callers and downstream consumers before reporting. Drop vague concerns and style preferences that do not affect the contract.

## Report

Lead with findings ordered by severity. Keep ranges tight and separate blockers from advisory improvements. Then state assumptions and unverified proof surfaces. Zero findings is valid.

Do not apply fixes unless the current request already authorizes them. If it does, follow the approval contract and use the smallest relevant repair or improvement path.
