# Illustration & layout
**Making Sense Together · 一起读懂**

Skill ID: `knowledge-card-art-direction` · [Instruction entry in Chinese](SKILL.md)

Use this when the content is approved and the pages need attention: better illustrations, clearer type, more varied layouts or a carefully checked PDF. It works independently of the content skill.

## Bring these inputs

Approved copy, sources, output language, page count, viewing size, style references and anything that must stay unchanged.

## How it works

1. Keep one content source and record its hash. If rewriting is allowed, note what changed and why.
2. Plan the reading order before choosing the layout. Let the content determine image size, spacing and the relationship between text and pictures.
3. Use an image-generation tool for the main artwork. Typeset body copy, precise labels, numbers and sources separately.
4. Measure actual glyph bounds and check the text inside its own container. When it does not fit, change the structure or available space before making everything smaller.
5. Export, render and inspect every delivered page. Check the text against the approved content, then hand over the editable files with the finished result.

The [warm-paper preset](assets/style-preset.json) and Chinese [sample one](assets/example-page-01.png) / [sample two](assets/example-page-02.png) are references, not a required brand.

## Try it

> Read this folder's SKILL.md. Use my approved English copy to make a two-page illustrated guide. Keep the wording unless we agree on a change. Follow the supplied style, use icons that help explain the topic, and check the actual exported pages at reading size. Deliver the PDF, editable copy, artwork, prompts and layout source.

## Checks and installation

The [content comparison script](scripts/check_content_lock.py) and [layout checker](scripts/check_layout.py) use only the Python standard library. Their input formats and limits are described in the [check reference in Chinese](references/checks.md). They support visual review; they do not prove that an illustration or explanation is correct.

Copy the entire folder to a skills directory supported by your assistant, or ask it to read SKILL.md directly. Confirm discovery with a small task. This skill does not automatically install dependencies, generate images or publish files.

[Installation details in Chinese](references/installation.md) · [MIT license](LICENSE).
