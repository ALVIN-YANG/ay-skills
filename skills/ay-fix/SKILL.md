---
name: ay-fix
description: Diagnose and repair bugs, regressions, crashes, hangs, test failures, incorrect behavior, and unexpected slowness through evidence and root cause. Use when something is broken or used to work and this is the primary debugging workflow; keep diagnosis read-only unless the user also asks for a fix. Do not use for planned improvements without a failure symptom.
---

# AY Fix

Prove the cause, then make the smallest authorized repair that prevents recurrence.

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

## Diagnose

1. Capture the exact symptom, expected behavior, environment, and failure layer.
2. Reproduce through the closest available path, or name the missing reproduction condition.
3. Trace backward from the bad output to the earliest incorrect state. Read recent changes and working examples when relevant.
4. Form competing hypotheses and run the smallest discriminating check. Instrument boundaries when observation is missing.
5. Confirm the cause. A plausible smell, correlation, or vanished symptom is not proof.

After a failed hypothesis, collect new evidence before trying another. Do not edit repeatedly in place of diagnosis.

## Decide the repair boundary

If the user asked only to diagnose, stop with the confirmed cause or next discriminating check.

If the user asked to fix, proceed without another checkpoint only when the root-cause repair is unique, local, reversible, and preserves intended behavior. Present a repair proposal first when alternatives change product behavior, architecture, data contracts, dependencies, scope, external state, or material risk.

## Repair and prove

Fix the cause at the narrowest responsible boundary, not its downstream symptom. Add a regression check when a stable behavior seam exists; do not invent hollow tests for untestable surfaces.

Re-run the original reproduction, regression check, and relevant neighbors. Separate environment, harness, source, build, package, deployment, and real-runtime evidence. If the cause remains unproven, say so.

Report the cause, discriminating evidence, repair, proof, and remaining uncertainty.
