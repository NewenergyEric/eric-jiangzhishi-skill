# 一起读懂：16 秒介绍
[English](README.en.md)

| 语言 | 视频与预览 | 可编辑内容与检查 |
|---|---|---|
| 中文 | [MP4](intro.mp4) · [GIF](intro.gif) · [海报](poster.png) | [分镜](story.json) · [报告](report.json) |
| English | [MP4](intro.en.mp4) · [GIF](intro.en.gif) · [Poster](poster.en.png) | [Storyboard](story.en.json) · [Report](report.en.json) |

从一个问题开始，展示两页细胞成稿，再介绍「内容梳理」与「插画排版」这两个独立 Skill。画面使用已有插画和真实成稿，无旁白。英文版独立断行和排版，所展示的中文案例有明确标注。GIF 循环播放，也可使用静态海报。

三幕为 0–5 秒、5–10 秒和 10–16 秒。文案、时间与体积上限在两份分镜 JSON 中；分层位置、标注线、翻页和步骤提示在 [动画源](../../scripts/build_intro.mjs) 中。

## 使用的渲染工具

沿用用户指定的 [motion-story-skills](https://github.com/NewenergyEric/motion-story-skills)，本版使用其后续维护项目 [eric-intro-motion-skill](https://github.com/NewenergyEric/eric-intro-motion-skill) v0.4.0，固定提交 `6c761d6e4a6e0ed358178b5d2f1fac339a3361cf`。复用本地编码、字形测量、PNG 栅格化和成品检查，保留本项目自己的插画与组合代码。

## 重建

需要 Node.js 22+、Git，以及 PATH 中可用的 FFmpeg / ffprobe。在项目根目录运行：

```sh
git clone --filter=blob:none --sparse --no-checkout https://github.com/NewenergyEric/eric-intro-motion-skill.git .build/tools/eric-intro-motion-skill
git -C .build/tools/eric-intro-motion-skill sparse-checkout set skills/eric-intro-motion-skill
git -C .build/tools/eric-intro-motion-skill checkout 6c761d6e4a6e0ed358178b5d2f1fac339a3361cf
npm ci --ignore-scripts --prefix .build/tools/eric-intro-motion-skill/skills/eric-intro-motion-skill
node scripts/build_intro.mjs --lang zh --preview
node scripts/build_intro.mjs --lang en --preview
node scripts/build_intro.mjs --lang zh
node scripts/build_intro.mjs --lang en
```

已有该版本引擎时跳过下载；用 `--motion-story ./path-to-repo` 指定另一目录。预览在 `.build/intro-render/zh` 和 `.build/intro-render/en`。完整构建会替换所选语言的媒体和报告。

MP4 为 960 × 540、24 fps、H.264 / yuv420p，带静音 AAC 轨道和 faststart。GIF 为 640 × 360、12.5 fps、96 色。两种语言均为 16 秒；每个 MP4 上限 5 MB，每个 GIF 上限 3 MB。

脚本遇到缺字、文字溢出、尺寸或体积不符会停止。报告保存版本、原图、动画源、分镜、运行时依赖与媒体哈希。核验范围见 [检查记录](../../docs/verification.md)；平台上传后的显示不在本地检查范围内。
