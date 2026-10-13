# 把知识讲给人听

两套 AI Skill，帮你把资料做成容易读懂的知识图文。适合科普文章、课堂讲义和两页小册子。

[下载 Skill](https://github.com/NewenergyEric/eric-jiangzhishi-skill/releases/latest) · [看案例](#两份完整案例) · [使用说明](docs/getting-started.md)

[![16 秒介绍：从资料到两页图文，展示太阳系和细胞的实际成稿](media/intro/intro.gif)](media/intro/intro.mp4)

16 秒，无旁白。[MP4 · 1.99 MB](media/intro/intro.mp4) · GIF 2.02 MB · [静态预览](media/intro/poster.png) · [视频分镜与源码](media/intro/README.md)

## 它能帮你做什么

你提供主题、读者和资料，助手按 Skill 核实内容、写正文，再做插画与排版。成稿保留来源；正文、图片、生成提示和排版源也一起留下，方便继续改。

| 你手上有什么 | 从哪个 Skill 开始 |
|---|---|
| 资料和想法，还没想好怎么讲 | [把知识讲给人听](skills/knowledge-to-friendly-product/SKILL.md)：理解资料、组织解释、完成图文 |
| 已经定稿的文字，想改善画面 | [知识卡包美术与排版](skills/knowledge-card-art-direction/SKILL.md)：插画、中文排版、校样和导出 |

两个 Skill 可以单独使用。制作新插画需要可用的图像生成工具；读取方法文档不需要安装 Python。

## 开始使用

1. 在 [Release](https://github.com/NewenergyEric/eric-jiangzhishi-skill/releases/latest) 下载文件名含 `skills` 的小包并解压。
2. 让支持读取文件的 AI 助手打开所需目录中的 `SKILL.md`。长期使用时，把整个目录复制到所用工具的技能目录。
3. 带上资料，给它一个具体任务。例如：

> 读取 knowledge-to-friendly-product。用我附的资料，给没有生物学背景的读者做两页细胞介绍。先讲细胞内部怎样工作，再比较动物、植物和细菌。用暖纸手绘风格，标题可以手写，正文要清楚好读。交付 PDF、可编辑文字、插画和来源。

需要辅助复制时，可以运行 `python scripts/install_skill.py knowledge-to-friendly-product --dest ./my-skills`。目标已有同名目录时，脚本会停止。

[详细步骤](docs/getting-started.md) · [HTML 上手入口](docs/getting-started.html) · [安装检查清单](docs/installation-checklist.md)

## 两份完整案例

| 主题 | 这两页讲什么 | 成稿与过程 |
|---|---|---|
| 太阳系八大行星 | 从地球出发，依次认识内侧四颗行星和外侧四颗巨行星 | [PDF](examples/solar-system/output/solar-system.pdf) · [文字版](examples/solar-system/read.html) · [制作过程](examples/solar-system/process.md) |
| 认识细胞 | 看典型动物细胞的内部，再比较叶片细胞和细菌 | [PDF](examples/cells/output/cells.pdf) · [文字版](examples/cells/read.html) · [制作过程](examples/cells/process.md) |

每例都是两页，没有额外封面。插画、手写标题和图标由图像模型生成，准确正文与结构标签单独排版。标题是图片素材，改字需要重新生成或换成排版字体。

## 自己修改案例

文字放在各案例的 `content.json`，采用图片在 `art/`，完整生图提示在 `prompts.json`。完整发布包包含这些源文件、开放字体和 PDF 构建脚本。

```sh
python -m pip install -r requirements.txt
python scripts/build_example.py --case cells
python scripts/build_example.py --case solar-system
python scripts/build_html.py
python scripts/verify_project.py
```

构建使用包内图片，不会调用生图 API。介绍视频使用 [Motion Story](https://github.com/NewenergyEric/motion-story-skills) 渲染，[重建方法](media/intro/README.md)另列。

两份 PDF 已检查页数、文字一致性和实际页面；发布包做了解压、重建和安装复制检查。详细结果与未测项见 [验证记录](docs/verification.md)。

方法、代码与原创内容使用 [MIT](LICENSE)，字体保留 OFL。素材来源和生成图像说明见 [许可说明](THIRD_PARTY_NOTICES.md)。
