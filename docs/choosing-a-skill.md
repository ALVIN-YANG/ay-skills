# Choosing a skill

Choose the primary skill from the work you need delivered. A domain or artifact-specific skill should lead; AY Skills supplies an approval or evidence boundary only where it helps.

## Common product handoff

A typical sequence is:

```text
ay-product → ay-ui → ay-architecture → ay-api → ay-database → ay-implement → ay-integration-docs
```

This is guidance, not a required pipeline. Move architecture earlier when feasibility blocks UI. Skip `ay-integration-docs` unless another client team consumes the changed contract. Use `ay-review` where a read-only consistency check is useful. Every skill can also run alone from approved inputs.

## Common overlaps

| Request | Primary skill |
|---|---|
| Apply a real expert's published framework to an open decision | `ay-expert-lens`; the domain skill still owns a concrete artifact or execution |
| Simulate an expert or celebrity in the first person | A dedicated persona skill; `ay-expert-lens` does not impersonate people |
| Design a new API, event, or message contract | `ay-api` |
| Document an approved or implemented contract for one client and release | `ay-integration-docs` |
| Generate an exhaustive public reference from OpenAPI | A dedicated API reference generator |
| Upload or submit an App Store release, check review state, or recover from rejection | A dedicated App Store release skill |
| Produce truthful store screenshots from a release build | `ay-store-screenshots` |
| Produce and install Apple AppIcon or `.icns` assets | A dedicated Apple icon asset skill when available; `ay-icon` leads an open metaphor and direction |
| Diagnose a failure without a requested repair | A dedicated diagnosis workflow; use `ay-fix` when the repair should also be completed |
| Choose or deepen a module interface or seam | A dedicated codebase-design skill; use `ay-improve` after the boundary is settled |
| Review changes since a commit, branch, or merge base | A dedicated diff-review skill; use `ay-review` across product and delivery artifacts |
| Write natural Chinese long-form prose | A dedicated Chinese writing skill; `ay-write` leads research, English, or illustrated work |

If two skills still appear to overlap, install only the one that owns the immediate deliverable or name it explicitly in the request.
