# Make the article's main point memorable

Full explanatory articles and their full rewrites include a photorealistic information graphic near the opening and an explanatory image beside each important knowledge module. Interview answers, FAQ and reference entries, procedures, narrow edits, fiction, and social content do not inherit this requirement; illustrate them only when requested or when a figure materially helps the task. A social article follows its requested format even when it explains a technical subject. Respect explicit text-only requests and another chosen style. Do not add a picture to a read-only critique.

The overview is a visual summary of the article, with comprehensive, detailed coverage of its main content. Module images explain their own mechanism, process, comparison, or decision in greater detail. A character beside a laptop is insufficient if the topic is task recovery or duplicate requests.

An important module introduces a concept, causal relationship, process, or distinction that the reader needs to understand and remember. Give it a focused image with useful annotations. Short transitions and repeated reminders do not become extra illustrated modules. The overview shows where the module fits; the local image explains how it works.

## Default art direction

Use cinematic live-action realism: adult Chinese faces, natural skin grain and hair, detailed physical fabrics and accessories, and directional soft light with believable shadows. Avoid anime proportions, plastic skin, and CGI-doll rendering. Keep diagram text sharp even when the photographic background has depth of field. Combine the photographic characters with readable diagrams and a restrained palette; keep backgrounds subordinate to the explanation. Characters or personified objects explain roles and actions. Use sections, arrows, labels, examples, and short captions wherever they carry useful information. Do not remove necessary detail to keep the picture minimal. Density comes from meaningful coverage and visible relationships, not tiny text or crowded decoration. Create a composition for the current subject.

For a message-queue article, show the business service submitting a task, the queue holding it, a worker processing it, and the result. Also show buffering versus sustained backlog, enqueueing versus completion, and the send-before-acknowledgment gap that can cause duplicate mail when the service lacks deduplication. A conveyor alone misses these central points. Do not imply universal single-worker, ordering, or exactly-once guarantees.

Match each major article point to a visible element. Combine repeated explanations, but retain distinct mechanisms and limits. The illustration should let a reader recover the article's content, not merely recognize its topic.

## Keep a recurring cast

Choose the needed characters from these eight bundled portraits. Inspect their actual images and pass those files to the image-generation capability as identity and style references. A later explicit user reference takes precedence. The white portrait backdrop establishes the reference, not a required setting for every article.

| Character | Identity reference |
|---|---|
| DeepSeek / 鲸鱼娘 | [deepseek.png](../assets/characters/deepseek.png): blue waves, fin ears, navy maid dress, whale tail |
| ChatGPT娘 | [chatgpt.png](../assets/characters/chatgpt.png): white hair, horns, pearly gown, dragon wings and tail |
| Claude娘 | [claude.png](../assets/characters/claude.png): copper hair, ivory-orange-black scholar gown, book |
| Gemini娘 | [gemini.png](../assets/characters/gemini.png): blue-violet hair, cat ears and tail, star ornaments |
| GLM娘 | [glm.png](../assets/characters/glm.png): black hair, black-white scholar gown, Z ornaments, black book |
| Grok娘 | [grok.png](../assets/characters/grok.png): blonde twin tails, black-burgundy gown, gold-edged axe |
| Kimi娘 | [kimi.png](../assets/characters/kimi.png): silver curls, moon and music ornaments, piano-key skirt |
| Qwen娘 | [qwen.png](../assets/characters/qwen.png): blue braid, blue-white Chinese-inspired robe, folding fan |

These user-selected AI-generated portraits interpret fan designs from [蓝色大肥鱼档案馆](https://fisharchive.cc/characters). They establish visual identities, not factual claims about the models or sources for new articles. Keep faces, hairstyles, proportions, clothing palettes, and recurring roles consistent. Use the characters needed for the scene; do not crowd every panel with the entire cast.

Vary expressions, poses, props, scenes, and panel layouts to explain the current topic. Favor approachable, playful adult expressions when appropriate; give presenters distinct actions such as sorting, checking, reading, or celebrating a result, rather than repeating a pointing pose. Preserve realistic proportions and identity. Regenerate diagrams and labels from the article; do not copy the reference's topic, claims, or layout. Reuse the original reference for later images; text descriptions alone do not ensure visual identity.

Characters guide, question, demonstrate, or perform an illustrated action. Their screen space must serve the information. Keep mechanisms, diagrams, labels, and limits prominent; avoid decorative character repetition or forcing the same setting onto every topic. Recurring narrator roles do not imply those characters are actual components of the system.

## Use precise media for precise claims

The information graphic explains and supports memory; it must also be accurate. Quantities, topology, interfaces, and detailed sequences need traceable data and precise drawing when the article depends on them. Integrate precise diagrams with photographic characters where available formats allow it; add a separate figure only when necessary.

| Explanatory job | Default medium | Deliverable |
|---|---|---|
| Precise small diagram, icon, or annotated mechanism | SVG | Editable `.svg`, responsive sizing, useful title or alt text |
| Complex editable architecture, relationship map, or flow | draw.io | `.drawio` source plus SVG or PNG export |
| Conceptual sketch, journey, or informal mental model | Excalidraw | `.excalidraw` source plus SVG or PNG export |
| Quantitative comparison or trend | Chart from traceable data | Source data or code plus web-ready export |
| Article content organized as a photorealistic information graphic | Image generation or composition | WebP or PNG plus useful alt text |

Do not use image generation for text-heavy architecture or exact diagrams. Prefer a table or two sentences when these communicate faster than an additional figure.

## Produce

Use available capabilities within the approved scope, preserving project conventions such as build-time Mermaid for precise diagrams. Decide the illustration while drafting; no routine visual-plan checkpoint or dependency on another skill. Installation, paid use, publishing, and new runtimes require their own authorization.

If image production is unavailable, finish authorized prose and identify which overview or module images remain unproduced. A prompt or a broken image link is not a finished asset. Do not silently substitute an unrelated diagram or generic stock image.

Keep any editable source, save article-bound assets beside the deliverable or in its existing asset directory, and provide useful alt text. Place module images beside the passages they explain. At thumbnail size check the topic and hierarchy; at intended reading size check coverage, label readability, arrow direction, conditions, and factual implications. Compare character identity against the bundled reference across all images. Do not require detailed labels to be readable in a thumbnail. Verify placement and licenses. Remove unnecessary extra figures.
