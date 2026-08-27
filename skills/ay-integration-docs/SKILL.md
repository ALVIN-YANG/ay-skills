---
name: ay-integration-docs
description: Write concise consumer-specific Markdown handoffs for approved or implemented APIs, events, messages, and release deltas. Use when backend, web, mobile, desktop, or device teams need 接口文档, 消息协议, 联调说明, 客户端升级说明, or 本期接口变更. Do not use to design a new contract, generate an exhaustive public API reference, describe internal implementation, write product release notes, or document unchanged interfaces.
---

# AY Integration Docs

Give one consumer the observable contract it needs.

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

## Select visible scope

Identify the consumer, release or integration, comparison baseline for a delta, and sources of truth. Inspect approved contracts, schemas, diffs, and tests.

Include only operations and messages used by that consumer in scope. A release delta contains only visible additions, changes, deprecations, and removals. Exclude unchanged or unused interfaces, other clients, and internal code, storage, broker topology, or deployment.

Explain only observable business conditions, authorization, validation, state outcomes, compatibility, retry, idempotency, ordering, and client action. Do not explain how the server works. If nothing visible changed, say so without an empty template.

## Required content

Open with a brief introduction naming the consumer, business purpose, scope or baseline, prerequisites, and compatibility result. Omit filler, tutorials, generic standards, and repeated background.

Every documented HTTP operation requires:

- purpose, business condition, method, and path;
- a concrete request example and request-parameter table;
- a successful response example and response-field table.

Tables cover only real fields and state name, location when relevant, type, requiredness, meaning, and constraints.

Keep canonical concept and state names across operations and messages. Show verified source mappings; never silently rename or invent aliases.

Every event or message requires direction, trigger, consumer-visible delivery behavior, a payload example, and a field table. Include reliability behavior only when contractual.

Give a separate response or payload example for each special error requiring distinct handling. End with one error summary table containing every mentioned error's transport or HTTP status, stable code, condition, client action, and retry policy. Add no unsupported generic errors.

Examples must be consistent and contain no secrets or personal data. Never invent fields, codes, constraints, or meaning. Mark unresolved facts as `待确认` and name the missing evidence.

## Verify and deliver

Cross-check names, types, required fields, examples, statuses, and outcomes against the sources. Confirm each in-scope interface has all required examples and tables, each special error appears in the summary, and no internal or out-of-scope name leaked.

Use direct, natural language. Each paragraph adds information. Create or update Markdown only when authorized, and stop before contract or implementation changes unless separately requested.
