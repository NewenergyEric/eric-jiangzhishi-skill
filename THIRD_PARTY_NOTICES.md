# 许可与素材来源

[English](THIRD_PARTY_NOTICES.en.md)

项目自编的 Skill 方法、模板、代码、说明文字、中英译文与排版源采用 [MIT](LICENSE)。太阳系和细胞插画、图标、手写标题按 MIT 提供本项目能够授予的使用权。生成工具与完整提示记录在各案例的 prompts.json；AI 输出不代表排他版权。

## 字体

`vendor/fonts/NotoSansSC.ttf` 是 Google Fonts 分发的 Noto Sans SC，保持原文件，使用 SIL Open Font License 1.1。原版权与完整许可见 [OFL.txt](vendor/fonts/OFL.txt)，[上游字体](https://github.com/google/fonts/tree/main/ofl/notosanssc)。构建时生成临时字重实例，PDF 嵌入字体子集。手写标题是 PNG 字图，不是新的字体文件。

## 事实来源

NASA、IAU、NHGRI、OpenStax 和东京大学等只用于核对知识事实。正文及英文译文为自行组织的解释，未复制资料中的图片、段落、Logo 或网页。具体主张与链接见 [太阳系来源](examples/solar-system/sources.md) 和 [细胞来源](examples/cells/sources.md)；这些网站的原文与素材仍受各自许可约束。

## 介绍视频

视频沿用 [motion-story-skills](https://github.com/NewenergyEric/motion-story-skills) 工作流，使用其后续维护项目 [eric-intro-motion-skill](https://github.com/NewenergyEric/eric-intro-motion-skill) v0.4.0 的本地渲染、字形排版和媒体检查代码，固定提交为 `6c761d6e4a6e0ed358178b5d2f1fac339a3361cf`。该项目代码采用 MIT，版权为 © 2026 Eric (NewenergyEric)，原许可随上游仓库保留。本仓库通过导入调用，不复制其引擎源码。

本项目自行编写视频分镜与组合代码，使用本仓库已有插画和真实成稿。渲染时读取上游保留 OFL 的 Noto Sans SC 字体；所用 fontkit、resvg-js 由上游锁文件安装，FFmpeg 由用户环境提供，均未打包进本项目。

第三方 Python 库由使用者通过 requirements.txt 安装。公开包不含参考书、个人资料、认证信息或构建缓存。
