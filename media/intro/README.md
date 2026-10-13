# 一起读懂：16 秒介绍
[English](README.en.md)

从一个问题开始，展示两页细胞成稿，再介绍「内容梳理」与「插画排版」两个独立 Skill。三种比例都保留这三幕；竖版与方版逐幕重新安排了文字、插画、标注线和动作。英文独立断行，所展示的中文案例有明确标注。视频无旁白，GIF 循环播放。

| 比例与尺寸 | 中文 | English |
|---|---|---|
| 横屏 16:9 · 960 × 540 | [MP4 · 403 KB](intro.mp4) · [GIF](intro.gif) · [海报](poster.png) · [报告](report.json) | [MP4 · 430 KB](intro.en.mp4) · [GIF](intro.en.gif) · [海报](poster.en.png) · [报告](report.en.json) |
| 方版 1:1 · 720 × 720 | [MP4 · 365 KB](square/intro.mp4) · [GIF](square/intro.gif) · [海报](square/poster.png) · [报告](square/report.json) | [MP4 · 406 KB](square/intro.en.mp4) · [GIF](square/intro.en.gif) · [海报](square/poster.en.png) · [报告](square/report.en.json) |
| 竖版 9:16 · 720 × 1280 | [MP4 · 519 KB](vertical/intro.mp4) · [GIF](vertical/intro.gif) · [海报](vertical/poster.png) · [报告](vertical/report.json) | [MP4 · 543 KB](vertical/intro.en.mp4) · [GIF](vertical/intro.en.gif) · [海报](vertical/poster.en.png) · [报告](vertical/report.en.json) |

首页使用约 43–45 KB 的静态封面，点击后再打开 MP4。GIF 是可下载的动画预览，不随 README 自动加载。完整 PNG 海报也随包提供。

## 内容与源码

- [中文分镜](story.json) · [English storyboard](story.en.json)：完整文案与三幕时间，分别为 0–5、5–10、10–16 秒。
- [分层动画](../../scripts/intro-composition.mjs)：三种画布的排版、标注线、样页展开和步骤提示。
- [导出脚本](../../scripts/build_intro.mjs) · [输出设置](formats.json)：分辨率、编码与文件体积上限。

使用用户指定的 [motion-story-skills](https://github.com/NewenergyEric/motion-story-skills) 的后续维护项目 [eric-intro-motion-skill](https://github.com/NewenergyEric/eric-intro-motion-skill) v0.4.0，固定提交 `6c761d6e4a6e0ed358178b5d2f1fac339a3361cf`。复用字形测量、PNG 栅格化、媒体检查和同仓库 social-motion 的原生布局检查；画面来自本项目已有插画与成稿。

## 重建

需要 Node.js 22+、Git，以及 PATH 中可用的 FFmpeg / ffprobe。先在项目根目录准备固定版本的运行时：

```sh
git clone --filter=blob:none --sparse --no-checkout https://github.com/NewenergyEric/eric-intro-motion-skill.git .build/tools/eric-intro-motion-skill
git -C .build/tools/eric-intro-motion-skill sparse-checkout set skills/eric-intro-motion-skill skills/social-motion
git -C .build/tools/eric-intro-motion-skill checkout 6c761d6e4a6e0ed358178b5d2f1fac339a3361cf
npm ci --ignore-scripts --prefix .build/tools/eric-intro-motion-skill/skills/eric-intro-motion-skill
```

选择比例 `wide`、`square` 或 `vertical`，以及语言 `zh` 或 `en`。例如：

```sh
node scripts/build_intro.mjs --ratio vertical --lang zh --preview
node scripts/build_intro.mjs --ratio vertical --lang en --preview
node scripts/build_intro.mjs --ratio vertical --lang zh
node scripts/build_intro.mjs --ratio vertical --lang en
```

先检查预览，再去掉 `--preview` 导出。已有运行时可跳过下载，或通过 `--motion-story ./path-to-repo` 指定。预览在 `.build/intro-render/<ratio>/<language>`；导出到本目录或对应的 `square/`、`vertical/`。完整构建替换所选比例与语言的成品。

渲染帧缓存在 `.build/intro-frame-cache/`。缓存键包含分镜、代码、原图与实际使用的缩放图、字体、依赖锁文件、比例和帧率；逐帧核对哈希。中断后重复同一命令即可复用完整帧。成品命中时还会校验编码参数、FFmpeg 版本和 MP4 哈希。

## 输出与检查

所有 MP4 都是 24 fps、384 帧、H.264 / yuv420p、静音 AAC 和 faststart；使用 CRF 27，按画面复杂度分配码率。GIF 为 6.25 fps、100 帧、48 色，横屏 / 方版 / 竖版分别为 480 × 270、400 × 400、360 × 640。每个文件都是完整 16 秒。

构建逐帧检查实际字形边界、文字重叠、图层越界，以及缺字、尺寸、帧数和体积，并完整解码 MP4 与 GIF。每个目录的 `audit.json` 和 `audit.en.json` 记录三幕的文字与独立图层边界，可对照三种比例：

```sh
node .build/tools/eric-intro-motion-skill/skills/social-motion/scripts/native-audit.mjs media/intro/audit.json media/intro/square/audit.json media/intro/vertical/audit.json
node .build/tools/eric-intro-motion-skill/skills/social-motion/scripts/native-audit.mjs media/intro/audit.en.json media/intro/square/audit.en.json media/intro/vertical/audit.en.json
```

报告保存源文件与成品哈希。机器检查之外还需看实际编码画面；本次检查范围见 [验证记录](../../docs/verification.md)。未验证社交平台转码或上传后的播放表现。
