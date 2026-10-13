# 实际验证记录
[English](verification.en.md)

版本：1.4.0。日期：2026-10-13。范围以 [publish-files.json](../publish-files.json) 为准。本版增加完整英文图文，替换所有英文视频中的样页，并为中英文首页放大循环预览、增加四个本地 SVG 标签。两个 Skill 入口、原中文 PDF 和插画未改动。

| 范围 | 本次结果 |
|---|---|
| 英文图文 | 细胞与太阳系各两页，标题、正文、备注、标注均与完整英文源文一致。PDF 提取文字不含中文；字形边界、缺字和文字重叠检查通过。四张导出样页均已逐页查看。 |
| 语言对应 | 英文阅读版与 HTML 上手页使用英文样页，并链接英文 PDF。三个英文视频报告均记录四张英文 PNG 的来源哈希；中文视频使用中文样页。 |
| 六个 MP4 | 中英文各有 16:9、1:1、9:16 三版，分别为 960 × 540、720 × 720、720 × 1280。均为 24 fps、384 帧、16 秒，H.264 / yuv420p、静音 AAC、faststart。 |
| 六个 GIF | 横屏提升至 800 × 450；方版为 400 × 400，竖版为 360 × 640。均为 100 帧、16 秒，无限循环。 |
| 完整解码 | 六个 MP4 和六个 GIF 都完整解码，无错误。 |
| 排版与动作 | 每版 384 帧均检查实际字形边界、文字重叠、步骤图标碰撞和图层越界。每种语言的三种比例均保留完整文案和原始图层，各幕独立重排检查通过。 |
| 成品画面 | 查看各 MP4 实际编码后的 14 个时刻，覆盖进入、停留、标注、两个转场前后和收尾；另检查各 GIF 的三幕。 |
| 首页预览 | 中英文各用对应语言 GIF，显示宽度设为 960 像素，并由 GitHub 限制在可用正文宽度内。GIF 实际宽度从 480 增至 800 像素。四个本地 SVG 标签说明许可、两个 Skill、双语版本和输出格式。 |
| 文件与打包 | 公开范围、相对链接、PNG 元数据、媒体来源与成品哈希通过检查。打包逐项比较 ZIP 成员和原文件；完整包独立解压后通过公开检查，Skills 小包保留两个独立入口和有效内部链接。 |

| 比例 | 语言 | MP4 字节 | GIF 字节 | 报告 |
|---|---|---:|---:|---|
| 16:9 | 中文 | 403,028 | 942,286 | [JSON](../media/intro/report.json) |
| 16:9 | English | 446,230 | 1,003,355 | [JSON](../media/intro/report.en.json) |
| 1:1 | 中文 | 364,842 | 442,994 | [JSON](../media/intro/square/report.json) |
| 1:1 | English | 415,652 | 455,165 | [JSON](../media/intro/square/report.en.json) |
| 9:16 | 中文 | 518,893 | 595,981 | [JSON](../media/intro/vertical/report.json) |
| 9:16 | English | 557,296 | 650,091 | [JSON](../media/intro/vertical/report.en.json) |

英文样页的排版记录：[细胞](../examples/cells/output/layout.en.json) · [太阳系](../examples/solar-system/output/layout.en.json)，包含实际文字边界、完整正文核对和来源及输出哈希。视频报告记录运行时、字体、插画、分镜、排版代码与媒体哈希。发布附件包括四份 PDF、十二个媒体文件、两个 ZIP 和 `SHA256SUMS.txt`。

1.2.0 已验证两个 Skill 的独立安装与重复安装保护；相关 Skill 和安装脚本未变，本版没有重复安装测试。

## 重新检查

```sh
python scripts/verify_project.py
python scripts/verify_project.py --staged
python scripts/package_release.py
```

重建视频与跨比例检查命令见 [视频说明](../media/intro/README.md)。暂存检查逐文件比较 Git 内容与公开清单；发布包不含缓存和其他项目资料。

## 检查的边界

- 没有测量实际网络加载秒数。GIF 自动播放遵循读者的 GitHub 设置；社交平台转码不在本次检查范围内。
- 已检查 HTML 链接及原有 JavaScript 行为；未新增屏幕阅读器实测或 PDF/UA 认证。
- 未做生物学专家审稿、真实读者试读或所有宿主的 Skill 自动发现测试。
- 图像模型不保证逐像素重现；采用图片已提供，跨依赖版本的 PDF 字节一致性未验证。
