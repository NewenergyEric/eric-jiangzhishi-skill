# What was checked
[中文](verification.md)

Version 1.3.0 · 2026-10-13. The exact scope is in [publish-files.json](../publish-files.json). This release changes video formats, encoding and homepage previews. The two skills, example text, reading pages, PDFs and artwork are byte-identical to 1.2.0.

Post-release homepage update (2026-10-13): each README now embeds its existing looping GIF, at 396,725 bytes for Chinese and 414,761 bytes for English, about 80% smaller than the 1.2.0 GIFs. The audit verifies the language-specific embed and infinite-loop setting. Autoplay follows the reader's GitHub settings. The release-time record below and the 1.3.0 release assets are unchanged.

| Area | Result in this release |
|---|---|
| Six MP4s | Chinese and English each have 16:9, 1:1 and 9:16 versions at 960 × 540, 720 × 720 and 720 × 1280. All are 24 fps, 384 frames and 16 seconds. H.264 / yuv420p, silent AAC and faststart checks pass. |
| Six GIFs | Landscape, square and portrait are 480 × 270, 400 × 400 and 360 × 640. All have 100 frames and run for 16 seconds. |
| Full decoding | All six MP4s and six GIFs decode completely without errors. |
| Layout and motion | All 384 frames in every variant pass glyph-bound, text-overlap, step-marker collision and canvas-bound checks. For each language, 14 matching moments across three ratios retain the complete copy and original artwork layers and pass independent re-layout checks in every scene. |
| Encoded frames | Fourteen moments from each MP4 were reviewed, covering entrances, holds, annotation, both sides of both cuts and the ending. Three scenes from each GIF were also checked. English labels the sample pages as Chinese. |
| Homepage media | The Chinese preview changes from a 1,980,375-byte GIF to a 42,649-byte cover; English changes from 1,994,774 to 44,546 bytes. Default preview bytes drop by about 98%. Video opens on click. Actual network loading time was not measured. |
| Language matching | README and HTML start pages link to their language's videos and formats. JavaScript logic checks pass for skill selection, task prompts, clipboard success and fallback, checklist counts and reset. |
| Files and archives | Public files, relative links, PNG metadata, media sources and export hashes pass. Packaging compares every ZIP member with its source. An independently extracted full archive passes the public audit; the Skills archive retains exactly two entries with valid internal links. |

| Format | Language | MP4 bytes | GIF bytes | Cover bytes | Report |
|---|---|---:|---:|---:|---|
| 16:9 | 中文 | 403,028 | 396,725 | 42,649 | [JSON](../media/intro/report.json) |
| 16:9 | English | 429,966 | 414,761 | 44,546 | [JSON](../media/intro/report.en.json) |
| 1:1 | 中文 | 364,842 | 442,994 | 38,787 | [JSON](../media/intro/square/report.json) |
| 1:1 | English | 406,043 | 449,928 | 40,232 | [JSON](../media/intro/square/report.en.json) |
| 9:16 | 中文 | 518,893 | 595,981 | 40,210 | [JSON](../media/intro/vertical/report.json) |
| 9:16 | English | 543,436 | 627,190 | 42,393 | [JSON](../media/intro/vertical/report.en.json) |

Version 1.2.0 verified independent skill installation and overwrite protection, complete bilingual reading text, PDF text and layout, and rebuild identity under the same dependencies. Those files are unchanged here; PDFs were not regenerated. English reading pages contain the complete translations. The illustrated PDFs and text embedded in artwork remain Chinese.

The reports above record runtime, font, original and resized artwork, storyboard, composition and export hashes. Layout reports in each directory retain the full-frame check count and measured bounds at 14 moments. Release assets include SHA256SUMS.txt.

## Run the public checks

```sh
python scripts/verify_project.py
python scripts/verify_project.py --staged
python scripts/package_release.py
```

See the [video instructions](../media/intro/README.en.md) for rebuild and cross-format audit commands. The staged check compares Git bytes against the publication list. Release packages exclude caches and unrelated project files.

## Limits

- Video was fully decoded and encoded frames were reviewed. Browser player interaction, social-platform transcoding and post-upload display were not verified.
- HTML links and JavaScript logic were checked. Built-in browser access restrictions prevented a local browser layout review.
- No biology expert review, target-reader study, all-host skill-discovery test, PDF/UA certification or screen-reader test was performed.
- Chosen artwork is included. Image generation is not pixel-reproducible, and PDF byte reproducibility across dependency versions was not tested.
