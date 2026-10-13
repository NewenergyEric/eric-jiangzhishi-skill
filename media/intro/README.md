# 16 秒仓库介绍

[MP4](intro.mp4) · [GIF](intro.gif) · [静态海报](poster.png) · [分镜 JSON](story.json) · [动画源](../../scripts/build_intro.mjs) · [输出报告](report.json)

视频先说明用途，再展示两页细胞成稿，最后给出太阳系与细胞两个例子。画面使用仓库里的真实插画和页面，没有旁白。GIF 循环播放；不需要动画时可使用静态海报。

三段分别为 0–5 秒、5–10 秒和 10–16 秒。所有可见文案、时间、尺寸和体积上限都写在 story.json；位置与动画写在 build_intro.mjs。

## 实际使用的 Motion Story

采用 [motion-story-skills](https://github.com/NewenergyEric/motion-story-skills) v0.3.0，固定提交 `1c002f5f00c56a05ef03c788bddad673254d101a`。复用其 `renderStory` 编码流程、`textBox` 字形测量与轮廓、PNG 栅格化和 `inspectVideo` 输出检查。为本项目写了一个组合：细胞标注逐渐显现，样页依次展开，制作步骤依次标记。

## 重建

需要 Node.js 22+、Git，以及 PATH 中可用的 FFmpeg / ffprobe。在项目根目录运行：

```sh
git clone https://github.com/NewenergyEric/motion-story-skills.git .build/tools/motion-story-skills
git -C .build/tools/motion-story-skills checkout 1c002f5f00c56a05ef03c788bddad673254d101a
npm ci --prefix .build/tools/motion-story-skills/skills/motion-story
node scripts/build_intro.mjs --preview
node scripts/build_intro.mjs
```

已下载上游仓库时，跳过 clone；也可以用 `--motion-story ./path-to-repo` 指定目录。预览保存在 `.build/intro-render`。完整构建会替换本目录的 MP4、GIF、海报和报告，请先保留需要的旧版本。

MP4 为 960 × 540、24 fps、H.264 / yuv420p，带兼容用的静音 AAC 轨道和 faststart。GIF 为 640 × 360、12.5 fps、96 色。脚本会检查时长、帧数、尺寸与文件体积；MP4 上限 5 MB、GIF 上限 3 MB，超出会报错。实际字节数和 SHA-256 见报告。

文字缺字或溢出会停止渲染。生成后仍需查看实际画面；已做本地抽帧检查，未把各社交平台上传后的显示效果列为验证通过。
