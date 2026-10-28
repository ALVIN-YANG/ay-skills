---
name: ay-agent-eval
description: Design, audit, and run evaluations of conversational or tool-using agents; improve them within approved scope. Use when comparing prompts, models, tools, workflows, or agent versions, including Agent 评测、badcase 回归、多轮对话评测、评测驱动迭代. Exclude ordinary unit tests, single code reviews, parameter-only model comparisons, and general architecture design.
---

# AY Agent Eval

Establish whether the measurement is trustworthy before accepting an improvement.

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

## Establish comparability

Inspect the implementation, failures, runner, and constraints. Define observable success, protected behavior, acceptable regressions, baseline, data groups, grader version, initial state, authorized changes, budget, and stopping conditions. Reuse agreed criteria; label proposed thresholds and unresolved decisions. Scores cannot override hard constraints.

For protocol design, metric interpretation, or continuous experiments, read [protocol.md](references/protocol.md).

## Validate the measurement

Inspect representative successes, failures, and disputed traces. Check final state and tool actions programmatically; use explicit rubrics and human-labelled examples to calibrate semantic judges. Allow insufficient evidence; self-reported success is not acceptance.

Keep execution failures separate from task judgments. Count planned, attempted, graded, timed-out, cancelled, and missing results; retain original attempts alongside retries. Include failed attempts, tools, and grading in costs. Estimate noise with targeted repetitions.

## Compare and improve

Compare original, best, and candidate versions under one protocol. Reset sessions, memory, caches, loaded configuration, and tool state to equivalent starting conditions. Group related users, conversations, and paraphrases to reduce leakage. Rebaseline when data, environment, or scoring changes; disclose uncontrolled factors.

Use discovery and regression cases for iteration. Holdout feedback used for a fix becomes development evidence; sealed access requires runner enforcement. Fixed-history replay does not prove full-dialogue success, and simulated users do not establish real-user acceptance.

When repair is authorized, test one evidence-backed hypothesis with the smallest scoped change. Check relevant cases and regressions before broader evaluation. Report paired fixes, regressions, and uncertainty by scenario. Promote a candidate only against agreed acceptance criteria; preserve the original and best versions.

## Stop and report

Rediagnose failed hypotheses. Stop at budget limits, unmeasurable gains, repeated offsetting regressions, or material scope changes. Deliver the best supported result and unresolved work; stopping is not success.

Retain configurations, outputs, costs, and redacted evidence. For resumed work, verify current state against the checkpoint. A long-running controller must enforce budgets, acceptance, and evidence preservation; a prompt alone cannot. Reuse available runners, adding one only when implementation is authorized.

Report the decision, gains, regressions, cost, evidence, and limits. Distinguish benchmark success, end-to-end operation, and real-user or device acceptance.
