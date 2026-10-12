# 两个检查脚本

只需 Python 3 标准库。在本 Skill 目录运行：

```sh
python scripts/check_content_lock.py baseline.json candidate.json
python scripts/check_layout.py layout.json --width 720 --height 960
```

内容锁检查字节或 JSON 语义；返回码 0 表示相同，1 表示有差异。它不判断事实。

布局输入形如：

```json
{
  "minimum_sizes": {"body": 17},
  "issues": [],
  "blocks": [{"page":1,"role":"body","size":18,"h":56,"allocated_h":70}],
  "text": [{"page":1,"block":"opening","role":"body","size":18,"text":"示例","x":48,"y":210,"w":36,"h":18}]
}
```

坐标统一用左上角起算的 PDF 点。text 应填写真实字形边界；同一 block 内的行间关系由排版源负责。脚本核对字号下限、分配高度、页界和不同 block 的文字重叠，不理解图中的牌面、科学语义或阅读节奏。不要用虚构坐标获得“通过”。

修改版面后重新导出和记录。对源内容的合法修订先说明原因，再更新基线。最终核验应绑定交付 PDF 的哈希。
