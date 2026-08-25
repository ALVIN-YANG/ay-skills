---
name: ay-api
description: Design service and transport contracts before implementation. Use when the primary deliverable is a REST, GraphQL, gRPC, event, webhook, SDK, or internal service interface, including 接口设计, API文档, OpenAPI, 错误码, 鉴权, or 幂等方案. Do not use for system architecture, physical database schemas, generic documentation, or requests primarily asking to implement handlers.
---

# AY API

Turn user and domain actions into a stable contract without exposing storage accidents.

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

## Derive the contract

Inspect available product requirements, UI states, architecture, consumers, existing conventions, and compatibility obligations. Preserve approved domain terms and state outcomes. Map each client action to a domain command, query, event, or stream. Do not begin by turning tables into CRUD endpoints.

Choose REST, GraphQL, gRPC, events, webhooks, or an internal interface from caller needs, ecosystem, latency, coupling, and evolution constraints. Preserve an established protocol unless evidence justifies change. Ask only about an undiscoverable decision that materially changes consumers or compatibility.

Scale the handoff to the actual operations. Omit generic standards and patterns that cannot be traced to a supplied consumer, risk, or compatibility need.

## Specify observable behavior

For each operation define purpose, authorization, input, output, validation, error semantics, and important state transitions. Add idempotency, optimistic concurrency, pagination, filtering, ordering, rate limits, retry, timeout, cancellation, or streaming behavior only where the use case needs them.

Distinguish authentication from authorization and transport errors from domain outcomes. Prevent cross-tenant access and unsafe retries by contract. Keep responses shaped for consumer tasks without leaking internal tables, provider payloads, or secret fields.

Describe compatibility and evolution: additive changes, deprecation, event ordering and delivery, webhook verification, or versioning where relevant. Avoid a versioning scheme or generic envelope without a real compatibility need.

## Check every consumer

Walk approved UI loading, success, empty, partial, error, cancellation, and recovery states against the contract. Check batch and concurrency behavior, realistic payload size, and failure of dependencies. Name any architecture or data invariant that remains unresolved instead of hiding it in the API.

Create `api.md`, OpenAPI, GraphQL schema, protobuf, or examples only when requested or required for an approved handoff. Stop before database schema and implementation unless separately authorized.
