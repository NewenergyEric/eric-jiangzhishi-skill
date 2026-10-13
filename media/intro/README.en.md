# Making Sense Together: a 16-second introduction
[中文](README.md)

| Language | Watch or preview | Editable content and checks |
|---|---|---|
| English | [MP4](intro.en.mp4) · [GIF](intro.en.gif) · [Poster](poster.en.png) | [Storyboard](story.en.json) · [Report](report.en.json) |
| 中文 | [MP4](intro.mp4) · [GIF](intro.gif) · [Poster](poster.png) | [Storyboard](story.json) · [Report](report.json) |

The film starts with a question, shows the finished cell guide, then introduces the two independent skills. It uses the actual project illustrations and pages, without narration. English has its own line breaks and type layout. The sample pages are the original Chinese editions and are labeled as such.

The three scenes run from 0–5, 5–10 and 10–16 seconds. Copy, timing and size budgets live in the storyboard JSON files. Layer positions and animation are in [build_intro.mjs](../../scripts/build_intro.mjs).

## Renderer

This continues the requested [motion-story-skills](https://github.com/NewenergyEric/motion-story-skills) workflow using its maintained successor, [eric-intro-motion-skill](https://github.com/NewenergyEric/eric-intro-motion-skill) v0.4.0, pinned to `6c761d6e4a6e0ed358178b5d2f1fac339a3361cf`. The custom composition reuses its local encoder, glyph measurement, PNG rendering and media checks.

## Rebuild

Use Node.js 22+, Git and FFmpeg / ffprobe on PATH. From the project root:

```sh
git clone --filter=blob:none --sparse --no-checkout https://github.com/NewenergyEric/eric-intro-motion-skill.git .build/tools/eric-intro-motion-skill
git -C .build/tools/eric-intro-motion-skill sparse-checkout set skills/eric-intro-motion-skill
git -C .build/tools/eric-intro-motion-skill checkout 6c761d6e4a6e0ed358178b5d2f1fac339a3361cf
npm ci --ignore-scripts --prefix .build/tools/eric-intro-motion-skill/skills/eric-intro-motion-skill
node scripts/build_intro.mjs --lang en --preview
node scripts/build_intro.mjs --lang zh --preview
node scripts/build_intro.mjs --lang en
node scripts/build_intro.mjs --lang zh
```

Skip the download if you already have that engine revision, or point to it with `--motion-story ./path-to-repo`. Preview frames go to `.build/intro-render/en` and `.build/intro-render/zh`. A full build replaces the selected language's media and report.

Each MP4 is 960 × 540 at 24 fps, with H.264 / yuv420p, silent AAC and faststart. Each looping GIF is 640 × 360 at 12.5 fps with 96 colors. Both languages run for 16 seconds. The per-file budgets are 5 MB for MP4 and 3 MB for GIF.

The build stops on missing glyphs, text overflow, incorrect geometry or an exceeded size budget. Reports record the source revision and hashes of artwork, composition code, storyboards, runtime inputs and exports. See the [verification record](../../docs/verification.en.md) for actual checks and their limits.
