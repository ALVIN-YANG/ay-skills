# Visual decisions

Choose a visual only when it explains structure, sequence, comparison, data, mechanism, scale, or atmosphere better than prose.

| Explanatory job | Default medium | Deliverable |
|---|---|---|
| Precise small diagram, icon, or annotated mechanism | SVG | Editable `.svg`, responsive sizing, useful title or alt text |
| Complex editable architecture, relationship map, or flow | draw.io | `.drawio` source plus SVG or PNG export |
| Conceptual sketch, journey, or informal mental model | Excalidraw | `.excalidraw` source plus SVG or PNG export |
| Quantitative comparison or trend | Chart from traceable data | Source data or code plus web-ready export |
| Cover, scene, metaphor, or atmosphere | Image generation | Optimized WebP or PNG plus generation intent and alt text |

Do not use image generation for text-heavy architecture or exact diagrams. Do not use a formal diagram when a small table or two sentences communicate faster.

## Plan

For each proposed figure, state:

1. the reader question it answers
2. the information or source behind it
3. the chosen medium
4. whether editability matters
5. where it belongs in the article

For a clearly authorized article, make these decisions while drafting. Include them in a proposal only when a visual changes scope, cost, or a consequential design choice. Do not require a separate outline approval or ask the user to choose a drawing tool without a real tradeoff.

## Produce

Inspect available capabilities first. Use an existing suitable capability within the approved scope, preserving project conventions such as build-time Mermaid or existing SVG assets. If the required medium is unavailable, prefer an equivalent native format; request approval when installation, paid use, or a new runtime is necessary.

Keep labels short and readable. Preserve source files, export at an appropriate web size, use stable descriptive filenames, and verify the rendered result in its destination. Cite external data and respect asset licenses.

Delete any figure that merely repeats nearby prose or adds generic decoration.
