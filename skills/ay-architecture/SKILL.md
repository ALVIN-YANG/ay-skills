---
name: ay-architecture
description: Design a system or subsystem before implementation. Use when the primary deliverable is architecture, module boundaries, data ownership, integration, deployment shape, quality attributes, or an architecture.md proposal, including 技术架构, 后端架构, 系统拆分, or 单体还是微服务. Do not use for routine implementation, refactoring an existing codebase without a design deliverable, endpoint details, or physical database schemas.
---

# AY Architecture

Choose the simplest system shape that satisfies the product and its real constraints.

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

## Read the system from its use

Inspect available requirements, approved UI flows, current code and infrastructure, team constraints, traffic shape, data sensitivity, budget, compliance, and operational expectations. Preserve upstream domain terms and trace each important state through latency, permissions, offline behavior, failure, cancellation, and recovery. Architecture may precede UI only when a feasibility or risk decision blocks useful interface design.

Separate known constraints from estimates and preferences. Ask only about a choice that changes the system shape and cannot be discovered. Recommend a default with its tradeoff.

## Define boundaries before technologies

Derive system context, responsibilities, module seams, data ownership, trust boundaries, external adapters, and synchronous or asynchronous flows. For each boundary, state what it hides, who owns it, and what failure crosses it.

Prefer a modular monolith and existing infrastructure unless scale, isolation, ownership, deployment, or reliability evidence justifies another shape. Do not default to microservices, Clean Architecture, event sourcing, queues, caches, or extra abstraction layers. Compare alternatives only where the decision is material.

Select store categories, protocols, and deployment units at this level, but leave endpoint payloads and physical tables to their own design work.

## Make the proposal testable

Describe quality attributes with scenarios and observable limits: availability, latency, throughput, consistency, privacy, recovery, cost, and operability only where relevant. Include failure containment, migration or evolution path, risks, rejected options, and the cheapest validation for uncertain assumptions.

Create `architecture.md`, an ADR, or diagrams only when requested or needed for an approved handoff. Stop before API detail, database schema, and implementation unless separately authorized.
