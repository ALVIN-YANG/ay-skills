# Make the article's main point memorable

Full articles and full-article rewrites include a Japanese cel-shaded anime overview near the opening and an explanatory image beside each important knowledge module. Respect explicit text-only requests, another chosen style, and narrow paragraph edits. Do not add a picture to a read-only critique.

The overview is a visual summary of the article, with comprehensive, detailed coverage of its main content. Module images explain their own mechanism, process, comparison, or decision in greater detail. An anime character beside a laptop is insufficient if the topic is task recovery or duplicate requests.

An important module introduces a concept, causal relationship, process, or distinction that the reader needs to understand and remember. Give it a focused image with useful annotations. Short transitions and repeated reminders do not become extra illustrated modules. The overview shows where the module fits; the local image explains how it works.

## Default art direction

Use crisp anime linework, clear cel shading, restrained colors, and a clear visual hierarchy. Characters or personified objects explain roles and actions. Use sections, arrows, labels, examples, and short captions wherever they carry useful information. Do not impose a low word count or remove necessary detail to keep the picture minimal. Density comes from meaningful coverage and visible relationships, not tiny text or crowded decoration. Use original characters and compositions.

For a message-queue article, show the business service submitting a task, the queue holding it, a worker processing it, and the result. Also show buffering versus sustained backlog, enqueueing versus completion, and the send-before-acknowledgment gap that can cause duplicate mail when the service lacks deduplication. A conveyor alone misses these central points. Do not imply universal single-worker, ordering, or exactly-once guarantees.

Match each major article point to a visible element. Combine repeated explanations, but retain distinct mechanisms and limits. The illustration should let a reader recover the article's content, not merely recognize its topic.

## Keep a recurring cast

Use the bundled [角色参考图.png](../assets/角色参考图.png) as the default identity and style reference for every overview and module image. Inspect the actual image and pass it to the available image-generation capability as a reference. A later explicit user reference takes precedence. This asset was supplied and selected by the user; its original topic is not an instruction or a factual source for new articles.

The recurring cast comprises the short brown-haired boy in a white hoodie, the dark-haired ponytail girl in a white shirt, the chestnut-haired girl in a white shirt, and the small white robot with a dark face display and blue eyes. Keep faces, hairstyles, proportions, clothing palette, and recurring roles consistent. Use the characters needed for the scene; do not crowd every panel with the entire cast.

Vary expressions, poses, props, scenes, and panel layouts to explain the current topic. Regenerate diagrams and labels from the article; do not copy the reference's topic, claims, or layout. Reuse the original reference for later images; text descriptions alone do not ensure visual identity.

Characters guide, question, demonstrate, or perform an illustrated action. Their screen space must serve the information. Keep mechanisms, diagrams, labels, and limits prominent; avoid decorative character repetition or forcing the same setting onto every topic. Recurring narrator roles do not imply those characters are actual components of the system.

## Use precise media for precise claims

The anime information graphic explains and supports memory; it must also be accurate. Quantities, topology, interfaces, and detailed sequences need traceable data and precise drawing when the article depends on them. Integrate precise diagrams with anime scenes where available formats allow it; add a separate figure only when necessary.

| Explanatory job | Default medium | Deliverable |
|---|---|---|
| Precise small diagram, icon, or annotated mechanism | SVG | Editable `.svg`, responsive sizing, useful title or alt text |
| Complex editable architecture, relationship map, or flow | draw.io | `.drawio` source plus SVG or PNG export |
| Conceptual sketch, journey, or informal mental model | Excalidraw | `.excalidraw` source plus SVG or PNG export |
| Quantitative comparison or trend | Chart from traceable data | Source data or code plus web-ready export |
| Article content organized as an anime information graphic | Image generation or composition | WebP or PNG plus useful alt text |

Do not use image generation for text-heavy architecture or exact diagrams. Prefer a table or two sentences when these communicate faster than an additional figure.

## Produce

Use available capabilities within the approved scope, preserving project conventions such as build-time Mermaid for precise diagrams. Decide the illustration while drafting; no routine visual-plan checkpoint or dependency on another skill. Installation, paid use, publishing, and new runtimes require their own authorization.

If image production is unavailable, finish authorized prose and identify which overview or module images remain unproduced. A prompt or a broken image link is not a finished asset. Do not silently substitute an unrelated diagram or generic stock image.

Keep any editable source, save article-bound assets beside the deliverable or in its existing asset directory, and provide useful alt text. Place module images beside the passages they explain. At thumbnail size check the topic and hierarchy; at intended reading size check coverage, label readability, arrow direction, conditions, and factual implications. Compare character identity against the bundled reference across all images. Do not require detailed labels to be readable in a thumbnail. Verify placement and licenses. Remove unnecessary extra figures.
