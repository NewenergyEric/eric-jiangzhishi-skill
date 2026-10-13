# What was checked
[中文](verification.md)

Version 1.2.0 · 2026-10-13. The exact public scope is in [publish-files.json](../publish-files.json).

| Area | Result |
|---|---|
| Name and language | The README, start pages, installation guides, skill overviews and films use Making Sense Together / 一起读懂. Chinese and English link to their matching pages. The two installation IDs are unchanged. |
| Independent skills | Each folder was copied into a fresh temporary location. All 13 / 14 files matched their sources, internal references stayed within the respective skill, and a repeat installation stopped without overwriting. The English overviews do not add extra skills. |
| Existing guides | Both examples still have two pages. Only the project name in PDF document properties changed. All four page renders are byte-identical to version 1.1.0. |
| English reading pages | Both translations were compared paragraph by paragraph with the Chinese, including conditions and caveats. Each language is generated from its own JSON. Checks cover complete reading text, labels, page IDs and paragraph counts. Each translation pins the Chinese source hash. |
| Text and layout | Extracted PDF text matches the Chinese content source. Actual text bounds pass the layout checks, with body text at 17 / 18 pt and labels at 15 pt. Negative controls detect changed or removed content, undersized type, overflow and overlapping text. |
| Start-page logic | Both languages pass checks for skill selection, distinct task prompts, clipboard success and manual-copy fallback, checkbox counts and reset. Public relative links resolve. |
| Videos | Each MP4 is 960 × 540, 24 fps and 384 frames; each GIF is 640 × 360 and 200 frames. All run for 16 seconds. All four files decode completely without errors. |
| Visual review | Fourteen moments from each encoded MP4 were inspected, covering entrances, annotation, holds, both sides of the two cuts and the ending. English identifies the sample pages as Chinese. |
| File sizes | Chinese MP4 / GIF: 1,993,342 / 1,980,375 bytes. English MP4 / GIF: 1,993,348 / 1,994,774 bytes. Each is about 2 MB. |
| Packaging | The allowlist, relative references, PNG metadata, PDF text and metadata, and both languages' media hashes pass. An independently extracted full ZIP passes the audit. With the same dependencies, its rebuilt PDFs and PNGs match byte for byte. The small Skills archive passes internal-link and installation checks. |

Media reports record the engine revision and hashes for runtime inputs, font, artwork, composition, storyboards and exports: [English](../media/intro/report.en.json) · [Chinese](../media/intro/report.json). Release assets include SHA256SUMS.txt.

The README's order was informed by the concrete examples in [bat](https://github.com/sharkdp/bat) and the concise purpose and installation entry in [uv](https://github.com/astral-sh/uv). Their wording was not copied.

## Run the public checks

```sh
python scripts/verify_project.py
python scripts/verify_project.py --staged
python scripts/package_release.py
```

The second command compares staged Git bytes with the publication list. Packaging reads only that list and excludes build caches and unrelated project files.

## Limits

- No biology expert review, target-reader study or all-host skill-discovery test was performed.
- Local HTML access was restricted in the built-in browser. Links and JavaScript logic were checked; actual browser layout and player interaction were not verified.
- Video checks cover full decoding and frames from the encoded files, not social-platform uploads or transcoding.
- Original illustrated PDFs, image titles and embedded labels remain Chinese. English reading pages translate the complete text; there is no separate English illustrated PDF.
- PDF/UA certification and screen-reader testing were not performed. Chosen artwork is included; image generation is not pixel-reproducible, and PDF byte reproducibility across dependency versions was not tested.
