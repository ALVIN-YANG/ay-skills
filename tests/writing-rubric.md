# Writing checks beyond file creation

The execution cases check whether the requested file was produced and protected inputs stayed unchanged. They do not score readability. Use the raw notes and intended reader below for a separate review of the actual output; do not show this rubric to the drafting agent as its user brief.

## Chinese explanation

Case `write-chinese-clarity` uses `fixtures/writing-clarity/notes.md`.

A reader should be able to explain, from the article alone:

- What must survive a process exit, and what step follows the uploaded CSV?
- Why does a timed-out email request leave an unknown result?
- Given this mail service's actual limitations, why is automatic retry unsafe?

Reject invented result-query APIs, invented idempotency support, claims of database-failover validation, author experience, or measured improvements absent from the notes. Check that unfamiliar names follow or accompany an explanation, and that the opening answers the recovery question before cataloguing frameworks.

## English transfer case

Case `write-english-holdout` uses a different subject and language, outside the skill's Chinese rewrite examples.

The output must preserve 200 attempts and twelve initial timeouts, distinguish timeout from confirmed failure, explain reusing the operation ID, and restrict the tested guarantee to the stated server. Check whether a non-specialist could understand the duplicate-upload risk without already knowing idempotency.

## Genre and scope checks

Use a short fiction request to confirm that invented events are allowed and an explanatory conclusion is not imposed. Use `write-review-only` to confirm that a critique does not mutate the draft. A precise paragraph rewrite should retain requested structure and must not grow into an article, visual plan, or publishing task.

## Record and iterate

For each run record the CLI/model when known, skill revision, raw input, actual output, and specific passages that helped or blocked understanding. Report factual preservation, task scope, and explanation quality separately. AI review is a preliminary judgment, not representative human testing.

When a reader objects, preserve the original passage and the proposed correction as a candidate case. Only mark wording as user-approved after actual confirmation. Recheck another subject before turning feedback into a general instruction; do not reward uniform punctuation, arbitrary sentence lengths, or the presence of a preferred heading.
