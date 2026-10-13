# 一起读懂
[English](README.md) · **简体中文**

我是一个四岁女孩的爸爸。这两个 AI Skill，起于我想陪她认识世界，却总找不到风格合适的绘本。它们帮我把一个问题和一些资料，做成可以打印、也可以在平板上一起读的知识图文。

[下载 Skill](https://github.com/NewenergyEric/eric-jiangzhishi-skill/releases/latest) · [看案例](#两份完整案例) · [使用说明](docs/getting-started.md)

[![16 秒介绍：从资料到两页图文，展示太阳系和细胞的实际成稿](media/intro/intro.gif)](media/intro/intro.mp4)

16 秒循环预览，约 397 KB，无旁白。点击动图可打开 MP4。

<details>
<summary>查看横屏、方版和竖版的中英文视频</summary>

各版 MP4 为 365–543 KB。三种比例保留完整内容，文字与插画分别排版。

| 比例与尺寸 | 中文 | English |
|---|---|---|
| 横屏 16:9 · 960 × 540 | [MP4 · 403 KB](media/intro/intro.mp4) · [GIF](media/intro/intro.gif) | [MP4 · 430 KB](media/intro/intro.en.mp4) · [GIF](media/intro/intro.en.gif) |
| 方版 1:1 · 720 × 720 | [MP4 · 365 KB](media/intro/square/intro.mp4) · [GIF](media/intro/square/intro.gif) | [MP4 · 406 KB](media/intro/square/intro.en.mp4) · [GIF](media/intro/square/intro.en.gif) |
| 竖版 9:16 · 720 × 1280 | [MP4 · 519 KB](media/intro/vertical/intro.mp4) · [GIF](media/intro/vertical/intro.gif) | [MP4 · 543 KB](media/intro/vertical/intro.en.mp4) · [GIF](media/intro/vertical/intro.en.gif) |

[分镜、海报与源码](media/intro/README.md)。

</details>

## 一个爸爸的小尝试

给女儿找绘本时，我常常觉得差了一点。有的太过卡通，角色和情节抢走了注意力，知识本身反而退到了后面；有的又太正式，还没开始读，就让人有了距离感。

我总觉得，知识本身的逻辑、复杂与深度，就有很强的吸引力。一个细胞怎样运作，一颗行星为什么是这个样子，一个问题又怎样带出另一个问题。慢慢发现、逐渐理解的过程，是一件值得反复体验的事。

我也不希望知识成了束之高阁的书本。它可以是有用的工具、一次动手的尝试、一个有意思的见识，也可以是把事物拆开、看看它如何运作，再重新认识世界的方法。

我没有美术或编辑背景，做这些主要凭直觉：画面亲切一点，解释清楚一点，也给细节和追问留一些空间。目前看来，我的第一位“小用户”接受度还不错。

做好的页面可以打印，也可以放在平板上，当作一张张卡片来读。配合我做的 [eric-intro-motion-skill](https://github.com/NewenergyEric/eric-intro-motion-skill)，还可以让关键元素动起来，多一种观察和理解的方式。

这件事从一个四岁小女孩开始，但我想，这份需要也许属于很多人：我们都希望亲近知识，保留好奇心，也愿意花时间弄明白。让学习有趣一些，也能让我们更容易迈出第一步。

所以，我把这两个 Skill 放在这里，想邀请大家一起试试。欢迎使用，也欢迎[分享你的作品、问题和建议](https://github.com/NewenergyEric/eric-jiangzhishi-skill/issues)。带上一个你想弄明白的问题，让我们一起享受发现的过程。

## 两个 Skill，按手上的内容来选

| 你手上有什么 | 从哪个 Skill 开始 |
|---|---|
| 资料和想法，还没想好怎么讲 | [内容梳理](skills/knowledge-to-friendly-product/SKILL.md)：核对资料、组织解释，继续完成图文 |
| 已经定稿的文字，想改善画面 | [插画排版](skills/knowledge-card-art-direction/SKILL.md)：沿用定稿，完成插画、文字排版、校样和导出 |

第一个也能完成整个小项目；第二个适合直接接手已有内容。它们可以配合，也可以各自安装。目录名仍是 `knowledge-to-friendly-product` 和 `knowledge-card-art-direction`，已有安装方式继续可用。

你提供主题、读者和资料，成稿保留来源；正文、采用图片、生成提示和排版源也一起留下，方便下一次修改。制作新插画需要图像生成工具；读取方法文档不需要 Python。

## 从一个小问题开始

1. 在 [Release](https://github.com/NewenergyEric/eric-jiangzhishi-skill/releases/latest) 下载文件名含 `skills` 的小包并解压。
2. 让支持读取文件的 AI 助手打开所选目录的 `SKILL.md`。长期使用时，把整个目录复制到工具支持的技能目录。
3. 带上资料，交代读者和想做的成品。例如：

> 读取 knowledge-to-friendly-product。用我附的资料，给没有生物学背景的读者做两页细胞介绍。先讲细胞内部怎样工作，再比较动物、植物和细菌。用暖纸手绘风格，标题可以手写，正文要清楚好读。交付 PDF、可编辑文字、插画和来源。

需要辅助复制时，可在完整包中运行 `python scripts/install_skill.py knowledge-to-friendly-product --dest ./my-skills`。目标已有同名目录时，脚本会停止。

[详细步骤](docs/getting-started.md) · [HTML 上手入口](docs/getting-started.html) · [安装检查清单](docs/installation-checklist.md)

## 两份完整案例

| 主题 | 这两页讲什么 | 成稿与过程 |
|---|---|---|
| 太阳系八大行星 | 从地球出发，认识内侧四颗行星和外侧四颗巨行星 | [中文 PDF](examples/solar-system/output/solar-system.pdf) · [中文阅读版](examples/solar-system/read.html) · [English text](examples/solar-system/read.en.html) · [制作过程](examples/solar-system/process.md) |
| 认识细胞 | 看典型动物细胞的内部，再比较叶片细胞和细菌 | [中文 PDF](examples/cells/output/cells.pdf) · [中文阅读版](examples/cells/read.html) · [English text](examples/cells/read.en.html) · [制作过程](examples/cells/process.md) |

每例都是两页，没有额外封面。插画、手写标题和图标由图像模型生成，正文与结构标签单独排版。手写标题是图片素材，改字需要重新生成或换成排版字体。英文阅读版翻译了完整正文；现有 PDF 与插画内的文字保留中文。

## 自己修改案例

文字在各例的 `content.json` 与 `content.en.json`，采用图片在 `art/`，完整生图提示在 `prompts.json`。完整发布包包含这些源文件、开放字体和构建脚本。

```sh
python -m pip install -r requirements.txt
python scripts/build_example.py --case cells
python scripts/build_html.py
python scripts/verify_project.py
```

[视频重建](media/intro/README.md) · [实际检查范围](docs/verification.md) · [公开文件清单](docs/publish-allowlist.md)

方法、代码与本项目可授权的原创内容采用 [MIT](LICENSE)；字体遵循 OFL。AI 生成图像不代表排他版权，第三方来源与依赖见 [许可说明](THIRD_PARTY_NOTICES.md)。
