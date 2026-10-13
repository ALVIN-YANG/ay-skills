# Contributing

Read [AGENTS.md](AGENTS.md) before changing a skill. Keep every skill independently installable and preserve the approval contract shared by all `SKILL.md` files.

## Required local checks

```bash
python3 scripts/verify_skills.py
python3 -m unittest discover -s tests -v
python3 scripts/verify_portable_install.py
python3 scripts/package_release.py --output /tmp/ay-skills.tar.gz
python3 scripts/package_release.py --verify /tmp/ay-skills.tar.gz
```

CI covers repository structure, unit tests, standalone installation, and the release archive. These checks do not prove live model routing or behavior.

## Model-backed evaluations

```bash
python3 scripts/run_routing_evals.py --host codex
python3 scripts/run_routing_evals.py --host codex --catalog global
python3 scripts/run_routing_evals.py --host codex --catalog ay-only
python3 scripts/run_routing_evals.py --host claude
python3 scripts/run_behavior_evals.py
python3 scripts/run_journey_evals.py
python3 scripts/run_product_evals.py
python3 scripts/run_product_evals.py --research-mode live
```

These evaluations require authenticated local CLIs and stay outside ordinary CI. They write ignored results under `eval-results/`. Journey failures preserve the workspace and final response; `--recheck-dir` can run the assertions again without another model call.

PNG fixture cases require Pillow. If it is not installed, run the relevant command with `uv run --with pillow` instead of adding Pillow to the project.

Network and authentication failures are reported as infrastructure errors, not skill failures. Record only the model, CLI, catalog, and pass rate actually checked.

For design-handoff changes, freeze the cases before editing skills and run the same cases before and after. Behavior evaluations save the final response and changed outputs under each case's results directory for inspection.

```bash
python3 scripts/run_behavior_evals.py --catalog target --ids architecture-approved-handoff review-design-complete review-design-missing-decisions implement-design-provider-drift implement-precise-edit review-read-only
```

Inspect the actual documents and responses: a fresh reader must reconstruct responsibilities, decisions, rationale, assumptions, and unresolved choices without the author's chat. The complete design has no blockers within its stated exercise scope. The incomplete design leaves retry semantics and concurrent closure unresolved; a reviewer must identify those choices rather than invent them. The provider-drift case must expose the false offline-cache assumption without changing files. The precise edit must still finish directly. Readiness is neither human approval nor executed runtime proof; verdict patterns and unchanged-file assertions alone do not prove review quality.

For writing changes, run the focused cases and inspect actual prose using [the writing rubric](tests/writing-rubric.md). File creation, keyword assertions, and a successful AI review do not prove human comprehension. The fixture catalog retains `human-writing` as an explicit-only alternative; the global catalog reflects the user's actual installation.

```bash
python3 scripts/run_behavior_evals.py --catalog target --ids write-chinese-clarity write-technical-selection write-source-comparison write-english-holdout write-review-only
python3 scripts/run_routing_evals.py --host codex --ids write-chinese-explainer write-chinese-rewrite write-line-edit write-fiction specialist-human-writing specialist-clear-rewrite no-skill-short-answer
```

For product website changes, freeze cases before editing the skill and inspect their saved outputs using [the website rubric](tests/website-rubric.md). Review rendered desktop and mobile pages and actual action targets; artifact assertions alone do not prove visual quality.

```bash
python3 scripts/run_behavior_evals.py --catalog target --ids website-proposal-only website-approved-static-page website-design-only-handoff website-two-visible-directions
python3 scripts/run_routing_evals.py --host codex --ids website-product-homepage website-approved-build website-design-only website-two-directions specialist-frontend specialist-frontend-workspace specialist-oil-ui ui-style-flow specialist-web-audit
```

## Release evidence

Keep `VERSION`, plugin manifests, and the release tag aligned. A source change, successful CI run, pushed tag, published GitHub Release, downloaded archive, and remote install are separate proof layers.

Pushing `v<VERSION>` starts the release workflow. Do not claim the public release until the workflow has published the archive and the downloaded artifact has been verified.
