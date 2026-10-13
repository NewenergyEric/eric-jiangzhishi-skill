# Licenses and sources
[中文](THIRD_PARTY_NOTICES.md)

The skill methods, templates, code, project copy, translations and layout source use the [MIT license](LICENSE). The same license covers the rights this project can grant in the solar-system and cell illustrations, icons and handwritten titles. AI-generated output does not imply exclusive copyright. Each example's prompts.json records its image tool and complete prompts.

## Font

`vendor/fonts/NotoSansSC.ttf` is the original Noto Sans SC file distributed by Google Fonts, under the SIL Open Font License 1.1. See the unchanged attribution in [OFL.txt](vendor/fonts/OFL.txt) and the [upstream font](https://github.com/google/fonts/tree/main/ofl/notosanssc). PDF builds make temporary weight instances and embed subsets. Handwritten titles are PNG images, not a new font.

## Factual sources

NASA, the IAU, NHGRI, OpenStax and the University of Tokyo were consulted for facts. The explanations and their English translations are written for this project; no source illustrations, paragraphs, logos or pages are reproduced. Claim-to-source links are in the [solar-system notes](examples/solar-system/sources.md) and [cell notes](examples/cells/sources.md), in Chinese. Original material on those sites keeps its own license.

## Introduction videos

The films use local rendering, glyph layout and media checks from [eric-intro-motion-skill](https://github.com/NewenergyEric/eric-intro-motion-skill) v0.4.0 at commit `6c761d6e4a6e0ed358178b5d2f1fac339a3361cf`, the maintained successor to [motion-story-skills](https://github.com/NewenergyEric/motion-story-skills). Its code is MIT, © 2026 Eric (NewenergyEric). This project imports the runtime from its separately obtained repository; it does not redistribute the engine source.

The storyboards and custom composition use this project's own artwork and finished pages. The renderer uses its OFL-licensed Noto Sans SC font and its locked fontkit / resvg-js dependencies. FFmpeg is supplied by the user's environment. Those runtimes are not bundled here.

Python dependencies are installed from requirements.txt. The public package excludes reference books, private material, authentication data and build caches.
