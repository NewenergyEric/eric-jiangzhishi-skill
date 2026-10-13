<h1 align="center">Making Sense Together</h1>

<p align="center"><strong>A good “why?” is worth exploring together.</strong><br>Two AI skills for turning your sources into clear, inviting illustrated guides.</p>

<p align="center">
  <a href="LICENSE"><img src="media/badges/license.svg" alt="License: MIT" height="30"></a>
  <a href="#two-skills-start-with-what-you-have"><img src="media/badges/skills.svg" alt="Two independent skills" height="30"></a>
  <a href="README.zh-CN.md"><img src="media/badges/languages.svg" alt="English and Chinese editions" height="30"></a>
  <a href="#two-complete-examples"><img src="media/badges/formats.svg" alt="PDF, MP4 and GIF" height="30"></a>
</p>

<p align="center"><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a> · <a href="https://github.com/NewenergyEric/eric-jiangzhishi-skill/releases/latest">Download the skills</a> · <a href="#two-complete-examples">Explore the guides</a> · <a href="docs/getting-started.en.md">Get started</a></p>

<p align="center"><a href="media/intro/intro.en.mp4"><img src="media/intro/intro.en.gif" alt="A 16-second introduction with fully English cell and solar-system pages" width="960"></a></p>

<p align="center"><sub>16-second loop · English pages throughout · Click for the MP4</sub></p>

<details>
<summary>Landscape, square and portrait videos in English and Chinese</summary>

All MP4s are 365–557 KB. Each format keeps the complete story, with its own text and illustration layout.

| Format | English | 中文 |
|---|---|---|
| Landscape 16:9 · 960 × 540 | [MP4 · 446 KB](media/intro/intro.en.mp4) · [GIF](media/intro/intro.en.gif) | [MP4 · 403 KB](media/intro/intro.mp4) · [GIF](media/intro/intro.gif) |
| Square 1:1 · 720 × 720 | [MP4 · 416 KB](media/intro/square/intro.en.mp4) · [GIF](media/intro/square/intro.en.gif) | [MP4 · 365 KB](media/intro/square/intro.mp4) · [GIF](media/intro/square/intro.gif) |
| Portrait 9:16 · 720 × 1280 | [MP4 · 557 KB](media/intro/vertical/intro.en.mp4) · [GIF](media/intro/vertical/intro.en.gif) | [MP4 · 519 KB](media/intro/vertical/intro.mp4) · [GIF](media/intro/vertical/intro.gif) |

[Storyboard, posters and source](media/intro/README.en.md).

</details>

## A small experiment from a dad

I'm a dad trying to explain the world to my four-year-old daughter. These two AI skills grew out of a search for picture books that felt right for us. They help me turn a question and a few sources into an illustrated guide we can print or read together on a tablet.

When I looked for picture books to help me explain things, I kept coming up against the same gap. Some leaned so heavily on cartoon characters and little stories that the subject slipped into the background. Others felt formal and distant before we'd even started reading.

I find the logic, complexity and depth of a subject fascinating in their own right. How does a cell work? Why is a planet the way it is? How does one question lead to another? The slow process of discovering and understanding something is an experience worth coming back to, again and again.

I don't want knowledge to end up out of reach on a high shelf. It can be a useful tool, something to try, an unexpected observation, or a way to take things apart and understand how the world works.

I have no background in art or editing, so I've been following my intuition: welcoming pictures, clear explanations, and room for detail and more questions. So far, my first little "user" seems happy with the results.

We can print the pages or read them as cards on a tablet. With my [eric-intro-motion-skill](https://github.com/NewenergyEric/eric-intro-motion-skill), key elements can move too, giving us another way to look at an idea and understand it.

This began with one four-year-old girl, but I think many of us want something similar: to feel at home with knowledge, stay curious, and take the time to figure things out. A little enjoyment can make it easier to take that first step into an unfamiliar subject.

I'm sharing these two skills so we can explore this together. Try them, and [share what you make, what puzzles you, or what you'd change](https://github.com/NewenergyEric/eric-jiangzhishi-skill/issues). Bring a question you're curious about. Let's enjoy finding things out.

## Two skills. Start with what you have.

| What you have | Which skill to use |
|---|---|
| Sources and an idea that still need explaining | [Content & explanation](skills/knowledge-to-friendly-product/README.en.md): check the sources, shape the explanation and carry it through to a finished guide |
| Approved copy that needs illustration and layout | [Illustration & layout](skills/knowledge-card-art-direction/README.en.md): keep the content, make the artwork, lay out the pages and proof the export |

The first skill can handle a small project from start to finish. The second can pick up where your writing is already done. Install either or both. Their stable folder names are `knowledge-to-friendly-product` and `knowledge-card-art-direction`.

Bring a topic, an audience and your sources. Keep the finished guide, editable copy, chosen images, generation prompts and layout source. New illustrations require an image-generation tool; reading the skill instructions requires no Python setup.

## Try a small topic

1. Download the archive with `skills` in its filename from [Releases](https://github.com/NewenergyEric/eric-jiangzhishi-skill/releases/latest).
2. Ask an AI assistant with file access to read the chosen folder's `SKILL.md`. For regular use, copy the whole folder into your tool's supported skills directory.
3. Give it the sources, intended reader and output you want. For example:

> Read knowledge-to-friendly-product. Use my attached sources to make a two-page introduction to cells for a reader with no biology background. First explain how the parts of a cell work together, then compare animal, plant and bacterial cells. Write in English. Use warm paper and hand-drawn illustrations, with playful titles and clear body text. Deliver the PDF, editable copy, artwork and sources.

The full package also includes a copy helper: `python scripts/install_skill.py knowledge-to-friendly-product --dest ./my-skills`. It stops if that destination already contains the skill.

[Detailed steps](docs/getting-started.en.md) · [HTML start page](docs/getting-started.en.html) · [Installation checklist](docs/installation-checklist.en.md)

## Two complete examples

| Topic | What the two pages explain | Read and explore |
|---|---|---|
| The eight planets | Start on Earth, visit the four rocky planets, then the four outer giants | [English PDF](examples/solar-system/output/solar-system.en.pdf) · [Reading version](examples/solar-system/read.en.html) · [Chinese PDF](examples/solar-system/output/solar-system.pdf) |
| Getting to know cells | Look inside a typical animal cell, then compare a leaf cell and a bacterium | [English PDF](examples/cells/output/cells.en.pdf) · [Reading version](examples/cells/read.en.html) · [Chinese PDF](examples/cells/output/cells.pdf) |

Each example has two complete illustrated pages in each language, ready to print or read on a tablet. The English PDFs, reading pages and videos all use English titles, body copy and labels. Both editions reuse the original illustrations and icons; text is typeset separately. Chinese titles use generated lettering, while English titles use the open Caveat handwriting font.

## Make it your own

Edit `content.json` or `content.en.json` in an example folder. Chosen artwork is in `art/`; full image prompts are in `prompts.json`. The full release includes these files, the open font and build scripts.

```sh
python -m pip install -r requirements.txt
python scripts/build_example.py --case cells
python scripts/build_english_examples.py
python scripts/build_html.py
python scripts/verify_project.py
```

The first PDF command rebuilds the Chinese cell guide. The English command rebuilds both English guides; the HTML command rebuilds both reading languages. Chinese handwritten titles are image assets. English titles remain editable text.

[Rebuild the videos](media/intro/README.en.md) · [What was checked](docs/verification.en.md) · [Publication file list](publish-files.json)

Methods, code and the original material this project can license use [MIT](LICENSE). The font uses the OFL. AI-generated images do not imply exclusive copyright. See [licenses and sources](THIRD_PARTY_NOTICES.en.md).
