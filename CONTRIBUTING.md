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

## Release evidence

Keep `VERSION`, plugin manifests, and the release tag aligned. A source change, successful CI run, pushed tag, published GitHub Release, downloaded archive, and remote install are separate proof layers.

Pushing `v<VERSION>` starts the release workflow. Do not claim the public release until the workflow has published the archive and the downloaded artifact has been verified.
