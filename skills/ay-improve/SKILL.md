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

Inspect the relevant call paths, tests, history, build or runtime measurements, and change patterns. Name the concrete friction: latency, allocation, duplication, coupling, unclear ownership, difficult testing, slow builds, or repeated change cost.

Do not treat aesthetics, file size alone, or a new abstraction as evidence. If no material constraint is found, say so and recommend no change.

## Propose the smallest leverage

After understanding the affected flow, compare solutions in this order:

1. no change or deletion
2. reuse code or configuration already present
3. use the language standard library or native platform
4. use an installed dependency
5. add the smallest new code or dependency

Stop at the first option that fully satisfies the approved behavior. This guides design; it is not code golf. Do not sacrifice stable module boundaries, readability, trust-boundary validation, data-loss protection, security, accessibility, or explicit requirements.

Trace the chosen files, dependencies, abstractions, and behavior to the demonstrated constraint. Include:

- baseline and evidence
- intended improvement and success measure
- affected boundary and behavior that must stay stable
- scope, risk, and relevant alternative
- verification method

For a deliberately limited solution, name its capability ceiling and observable upgrade trigger in an existing proposal or handoff. Do not create a comment or artifact only for this record.

Wait for approval before restructuring unless the user's instruction already specifies the exact transformation.

## Implement and compare

Preserve behavior unless approved otherwise. Prefer a deep, stable interface over helper layers. Treat size, nesting, parameters, and dependency fan-out as signals, not quotas. Split units mixing unrelated responsibilities or dependencies; merge pass-through files and one-use interfaces. Organize packages by domain capability; avoid generic `util`, `common`, `helpers`, or `types` dumping grounds; keep contract names consistent. Avoid speculative extensibility and unrelated cleanup. Changing the system shape still needs an approved proposal.

Verify the success measure and neighboring behavior. Less code or fewer dependencies help only when behavior, safeguards, and checks remain intact. Separate measured gains from expectations; do not claim saved lines, cost, or time without a comparable baseline. Review scope traceability, then report before/after evidence and remaining tradeoffs.
