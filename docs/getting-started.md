# 从一份资料开始

[English](getting-started.en.md)

先下载 [Release](https://github.com/NewenergyEric/eric-jiangzhishi-skill/releases/latest)。完整包带案例、开放字体与构建源；Skills 包只带两个可独立复制的 Skill。解压后在本地打开 [HTML 上手入口](getting-started.html)，或者直接照这份说明操作。

## 选一个入口

资料还需要理解和改写，先用 `skills/knowledge-to-friendly-product/SKILL.md`。文字已经定稿、想改善插画和排版，就用 `skills/knowledge-card-art-direction/SKILL.md`。

让能访问本地文件的 AI 助手读取完整 Skill。若要长期安装，复制整个目录到宿主支持的技能目录；也可使用 `python scripts/install_skill.py knowledge-to-friendly-product --dest ./my-skills`。这个示例只安装到项目下的自选目录，不改全局环境。

## 给出必要输入

说清主题、读者已有知识、阅读场景、资料、载体与页数、想保留的文字、风格参考和不能改的部分。没有真实用户调研可以先写工作假设，不要编造调研结论。

> 用「一起读懂」整理我的资料。读者是【具体情境】，做成【页数和载体】。文字请自然连贯，图像解释关系。保留来源和边界，完成可编辑源与成稿，并说明实际检查范围。

## 看什么才算做完

先核对解释是否准确，再检查画面与标签是不是同一件事。打开真正导出的每一页，看字是否读得清、是否碰图、来源能否找到。收到可编辑文字、提示、采用图片与排版源后，才方便继续改。

制图需要图像模型；PDF 构建需要对应依赖。缺少工具时保留未完成状态。示例展示了两种主题的做法，不保证任何资料都能自动变成好内容。

## 更新或恢复

同名安装目录已存在时先另存旧版，再决定替换。删除时只移走这个 Skill 目录。来源或受众改变后重新核验事实与例子，不只沿用旧图片。

[安装检查清单](installation-checklist.md) · [实际验证](verification.md) · [回到说明](../README.zh-CN.md)
