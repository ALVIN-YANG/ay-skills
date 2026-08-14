---
name: ay-improve
description: Improve code structure, architecture, maintainability, performance, or developer experience from a measured baseline without scope drift. Use when optimization, refactoring, simplification, cleanup, renaming, or extraction is the primary task, including 重构, 优化性能, 整理代码, or 简化, there is no bug symptom, and no more specific architecture or performance skill applies.
---

# AY Improve

Improve a demonstrated constraint, not an imagined future.

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

## Find the constraint

Inspect the relevant call paths, tests, history, build or runtime measurements, and change patterns. Name the concrete friction: latency, allocation, duplication, coupling, unclear ownership, difficult testing, slow builds, or repeated change cost.

Do not treat aesthetics, file size alone, or a new abstraction as evidence. If no material constraint is found, say so and recommend no change.

## Propose the smallest leverage

Trace every proposed file, dependency, abstraction, and public behavior to the measured constraint. Recommend the smallest option that materially improves it. Include:

- baseline and evidence
- intended improvement and success measure
- affected boundary and behavior that must stay stable
- scope, risk, and relevant alternative
- verification method

Wait for approval before restructuring unless the user's instruction already specifies the exact transformation.

## Implement and compare

Preserve behavior unless the approved proposal says otherwise. Prefer a deep, stable interface over layers of helpers. Avoid speculative extensibility, unrelated cleanup, and dependencies whose cost exceeds the improvement.

Verify the success measure and neighboring behavior. Distinguish measured gains from reasoned expectations. Review the final diff for scope traceability, then report the before/after evidence and remaining tradeoffs.
