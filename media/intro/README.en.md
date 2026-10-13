# Making Sense Together: a 16-second introduction
[中文](README.md)

The film starts with a question, shows the finished cell guide, then introduces the two independent skills. All three formats keep the complete story. Portrait and square have their own layouts in every scene, including the text, artwork, annotation paths and entrances. English videos use fully English illustrated pages, including their titles, body copy and labels. Chinese videos use the Chinese edition. There is no narration; GIFs loop.

| Format | English | 中文 |
|---|---|---|
| Landscape 16:9 · 960 × 540 | [MP4 · 446 KB](intro.en.mp4) · [GIF](intro.en.gif) · [Poster](poster.en.png) · [Report](report.en.json) | [MP4 · 403 KB](intro.mp4) · [GIF](intro.gif) · [Poster](poster.png) · [Report](report.json) |
| Square 1:1 · 720 × 720 | [MP4 · 416 KB](square/intro.en.mp4) · [GIF](square/intro.en.gif) · [Poster](square/poster.en.png) · [Report](square/report.en.json) | [MP4 · 365 KB](square/intro.mp4) · [GIF](square/intro.gif) · [Poster](square/poster.png) · [Report](square/report.json) |
| Portrait 9:16 · 720 × 1280 | [MP4 · 557 KB](vertical/intro.en.mp4) · [GIF](vertical/intro.en.gif) · [Poster](vertical/poster.en.png) · [Report](vertical/report.en.json) | [MP4 · 519 KB](vertical/intro.mp4) · [GIF](vertical/intro.gif) · [Poster](vertical/poster.png) · [Report](vertical/report.json) |

Each README embeds an 800 × 450 looping GIF across the main reading area. Click the animation to open the MP4. GitHub respects the reader's animated-image autoplay setting. Static covers and full-size PNG posters are also included.

## Story and source

- [English storyboard](story.en.json) · [中文分镜](story.json): complete copy and the three scenes, at 0–5, 5–10 and 10–16 seconds.
- [Layered composition](../../scripts/intro-composition.mjs): layouts, annotation paths, page entrances and step markers for all three canvases.
- [Export script](../../scripts/build_intro.mjs) · [Output settings](formats.json): dimensions, encoding and size budgets.

This uses the maintained successor to the requested [motion-story-skills](https://github.com/NewenergyEric/motion-story-skills): [eric-intro-motion-skill](https://github.com/NewenergyEric/eric-intro-motion-skill) v0.4.0, pinned to `6c761d6e4a6e0ed358178b5d2f1fac339a3361cf`. The custom composition reuses its glyph measurement, PNG renderer and media checks, plus the same repository's social-motion layout audit. Artwork and finished pages come from this project.

## Rebuild

Use Node.js 22+, Git and FFmpeg / ffprobe on PATH. Prepare the pinned runtime from the project root:

```sh
git clone --filter=blob:none --sparse --no-checkout https://github.com/NewenergyEric/eric-intro-motion-skill.git .build/tools/eric-intro-motion-skill
git -C .build/tools/eric-intro-motion-skill sparse-checkout set skills/eric-intro-motion-skill skills/social-motion
git -C .build/tools/eric-intro-motion-skill checkout 6c761d6e4a6e0ed358178b5d2f1fac339a3361cf
npm ci --ignore-scripts --prefix .build/tools/eric-intro-motion-skill/skills/eric-intro-motion-skill
```

Finished sample pages are included. If you edit the English copy, rebuild them first with `python scripts/build_english_examples.py` after installing the project's Python requirements. This preserves the original artwork and typesets the titles, body copy and labels from each example's `content.en.json`.

Choose `wide`, `square` or `vertical`, and `en` or `zh`. For example:

```sh
node scripts/build_intro.mjs --ratio vertical --lang en --preview
node scripts/build_intro.mjs --ratio vertical --lang zh --preview
node scripts/build_intro.mjs --ratio vertical --lang en
node scripts/build_intro.mjs --ratio vertical --lang zh
```

Review the previews before exporting without `--preview`. Skip the download if the pinned runtime is already present, or use `--motion-story ./path-to-repo`. Previews go to `.build/intro-render/<ratio>/<language>`; exports go here or into `square/` or `vertical/`. A full build replaces the selected format and language.

Frames are cached in `.build/intro-frame-cache/`. The key covers storyboards, code, original and resized artwork, font, dependency lockfile, ratio and frame rate; each cached frame is checked by hash. Run the same command after an interruption to resume. An encoded MP4 is reused only when its hash, encoding settings and FFmpeg version match.

## Exports and checks

All MP4s are 24 fps and 384 frames, with H.264 / yuv420p, silent AAC and faststart. CRF 27 varies the bitrate with image complexity. GIFs have 100 frames at 6.25 fps and 48 colors: landscape is 800 × 450, square is 400 × 400, and portrait is 360 × 640. Every file runs for 16 seconds.

The build checks text bounds, overlap and layer overflow on every frame, plus missing glyphs, dimensions, frame counts and size budgets, then fully decodes both video formats. Each directory's `audit.json` and `audit.en.json` records text and independent artwork bounds in all three scenes. Compare the formats with:

```sh
node .build/tools/eric-intro-motion-skill/skills/social-motion/scripts/native-audit.mjs media/intro/audit.en.json media/intro/square/audit.en.json media/intro/vertical/audit.en.json
node .build/tools/eric-intro-motion-skill/skills/social-motion/scripts/native-audit.mjs media/intro/audit.json media/intro/square/audit.json media/intro/vertical/audit.json
```

Reports record source and export hashes. These checks still need visual review of the encoded files. See the [verification record](../../docs/verification.en.md) for this release's scope. Social-platform transcoding and playback after upload were not tested.
