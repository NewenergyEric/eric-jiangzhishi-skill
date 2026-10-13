# What was checked
[中文](verification.md)

Version 1.4.0 · 2026-10-13. The exact scope is in [publish-files.json](../publish-files.json). This release adds complete English illustrated editions, uses them in all English videos, and gives both READMEs a larger looping preview and four local SVG labels. The two skill entries and the original Chinese PDFs and illustrations are unchanged.

| Area | Result in this release |
|---|---|
| English illustrated pages | Two pages each for cells and the solar system. All titles, body copy, notes and labels match the complete English source text. PDF extraction contains no Chinese text; glyph bounds, missing glyphs and text overlap checks pass. All four exported pages were visually reviewed. |
| Language matching | English reading pages and the HTML start page use English page images and link to English PDFs. All three English video reports identify the four English page PNGs by hash. Chinese videos use the Chinese pages. |
| Six MP4s | Chinese and English each have 16:9, 1:1 and 9:16 versions at 960 × 540, 720 × 720 and 720 × 1280. All are 24 fps, 384 frames and 16 seconds, with H.264 / yuv420p, silent AAC and faststart. |
| Six GIFs | Landscape is now 800 × 450; square is 400 × 400 and portrait is 360 × 640. All have 100 frames, run for 16 seconds and loop indefinitely. |
| Full decoding | All six MP4s and six GIFs decode completely without errors. |
| Layout and motion | All 384 frames of every variant pass glyph-bound, text-overlap, step-marker collision and canvas-bound checks. Each language's three ratios retain the complete copy and original artwork layers, with independent layouts in every scene. |
| Encoded frames | Fourteen moments from each MP4 were reviewed, covering entrances, holds, annotation, both sides of both cuts and the ending. Three scenes from each GIF were also checked. |
| README previews | Both READMEs use their own language's GIF, with a 960-pixel display width that GitHub limits to the available reading area. The actual GIF width increased from 480 to 800 pixels. Four self-contained SVG labels describe the license, two skills, languages and output formats. |
| Files and archives | Public-file scope, relative links, PNG metadata, media source hashes and output hashes pass. Packaging compares every ZIP member with its source. The independently extracted full archive passes the public audit; the Skills archive retains exactly two entries with valid internal links. |

| Format | Language | MP4 bytes | GIF bytes | Report |
|---|---|---:|---:|---|
| 16:9 | 中文 | 403,028 | 942,286 | [JSON](../media/intro/report.json) |
| 16:9 | English | 446,230 | 1,003,355 | [JSON](../media/intro/report.en.json) |
| 1:1 | 中文 | 364,842 | 442,994 | [JSON](../media/intro/square/report.json) |
| 1:1 | English | 415,652 | 455,165 | [JSON](../media/intro/square/report.en.json) |
| 9:16 | 中文 | 518,893 | 595,981 | [JSON](../media/intro/vertical/report.json) |
| 9:16 | English | 557,296 | 650,091 | [JSON](../media/intro/vertical/report.en.json) |

English page layout records: [cells](../examples/cells/output/layout.en.json) · [solar system](../examples/solar-system/output/layout.en.json). They include measured text bounds, complete-copy checks and source/output hashes. Video reports record runtime, font, artwork, storyboard, composition and export hashes. The release includes four PDFs, twelve media files, two ZIPs and `SHA256SUMS.txt`.

Version 1.2.0 verified independent skill installation and overwrite protection. Those skill files and the installer are unchanged; this release does not repeat the installation tests.

## Run the public checks

```sh
python scripts/verify_project.py
python scripts/verify_project.py --staged
python scripts/package_release.py
```

See the [video instructions](../media/intro/README.en.md) for rebuild and cross-format audit commands. The staged check compares Git bytes against the publication list. Release packages exclude caches and unrelated project files.

## Limits

- Actual network loading time was not measured. GIF autoplay follows the reader's GitHub settings. Social-platform transcoding is outside this release's checks.
- HTML links and existing JavaScript behavior were checked; there was no new screen-reader test or PDF/UA certification.
- No biology expert review, target-reader study or all-host skill-discovery test was performed.
- Chosen artwork is included. Image generation is not pixel-reproducible, and PDF byte reproducibility across dependency versions was not tested.
