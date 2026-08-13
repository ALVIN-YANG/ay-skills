# AY Skills contributor rules

AY Skills gives coding agents a human-approved boundary, then gets out of their way.

- Keep each `SKILL.md` under 150 lines and 500 words.
- Assume the model is capable. Add only rules that change behavior or protect authorization.
- Keep all six skills independently installable; do not create runtime dependencies between them.
- Preserve the approval contract markers and identical contract text in every skill.
- Put only `name` and `description` in skill frontmatter. Put Codex UI metadata in `agents/openai.yaml`.
- Use one-level progressive disclosure. Add a reference or script only after repeated need is demonstrated.
- Do not add routers, mode labels, hooks, telemetry, global rules, automatic commits, or mandatory artifacts.
- Treat upstream projects as inspiration. Do not copy their skill text or code without attribution and license review.
- Run `python3 scripts/verify_skills.py` and `python3 -m unittest discover -s tests -v` before committing.
- Verify portable install, Codex behavior, Claude behavior, CI, release contents, and remote install as separate layers.
- Keep `VERSION`, plugin manifests, and release tags aligned.
