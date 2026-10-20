# Client integration handoffs

Document an approved or implemented contract for one consumer and release. This writing task does not design a new contract or replace a complete public API reference.

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
