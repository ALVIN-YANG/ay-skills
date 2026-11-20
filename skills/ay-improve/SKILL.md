---
name: ay-improve
description: Improve an existing codebase's structure, maintainability, performance, or developer experience from a measured baseline without scope drift. Use when refactoring, optimization, simplification, cleanup, renaming, or extraction is the primary task, including 重构, 优化性能, 整理代码, or 简化, and there is no bug symptom. Let a dedicated module-design skill lead when the interface or seam itself is unresolved. Do not use for greenfield architecture or design-only work.
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

Inspect relevant call paths, tests, history, measurements, and change patterns. Name concrete friction: latency, duplication, coupling, unclear ownership, difficult testing, slow builds, repeated change cost, or wasted agent exploration.

Do not treat aesthetics, file size alone, or a new abstraction as evidence. If no material constraint exists, recommend no change.

For agent context hygiene, demonstrate wrong or wasted exploration from current code, instructions, documents, or tools. Prefer deleting stale or duplicate material, restoring one responsible source, and narrowing overlapping tools. Keep only project-specific rules and pointers in instruction files. Do not create indexes, hooks, or mandatory documents; current code, tests, and history remain the facts.

## Propose the smallest leverage

After understanding the affected flow, choose the first sufficient option:

1. no change or deletion
2. reuse existing code or configuration
3. use the standard library or native platform
4. use an installed dependency
5. add the smallest new code or dependency

Do not sacrifice stable boundaries, readability, validation, data protection, security, accessibility, or requirements. Tie the proposal to the demonstrated constraint with:

- baseline and evidence
- intended improvement and success measure
- affected boundary and protected behavior
- scope, risk, and relevant alternative
- verification method

For a deliberately limited solution, name its capability ceiling and observable upgrade trigger in an existing proposal or handoff. Do not create an artifact only for this record.

Wait for approval before restructuring unless the user specified the exact transformation.

## Implement and compare

Preserve approved behavior. Prefer a deep, stable interface over helper layers. Treat size, nesting, parameters, and fan-out as signals, not quotas. Split unrelated responsibilities; merge pass-through files and one-use interfaces. Organize packages by domain capability, avoid generic dumping grounds, and keep contract names consistent. Avoid speculative extensibility, unrelated cleanup, or unapproved system-shape changes.

Verify the success measure and neighboring behavior. Fewer lines or dependencies help only when behavior, safeguards, and checks remain intact. Separate measured gains from expectations. Report before/after evidence and remaining tradeoffs.
