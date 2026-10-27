# 视觉体系

模板里有两套风格，新项目选一套，选定后删掉另一套的文档与 token 文件。两套共用同一组角色名（`--bg*`、`--ink*`、`--line*`、`--accent*`、`--sp-*`、`--fs-*` 等）、同一份 [间距层级](spacing.md) 和同一个检查脚本 `scripts/check-design.mjs`。

| | [Owlbay Quiet](quiet.md) | [Owlbay Terminal](terminal.md) |
| --- | --- | --- |
| 一句话 | 安静、精确的数据界面 | 安静的索引终端 |
| 底色 | 中性灰，无色偏 | 暖近黑 / 暖白 |
| 强调色 | 陶土橙 #d27a52（按钮 #b35a35） | 陶土橙 #d97757 |
| 字体 | Inter（opsz）+ Geist Mono | Geist + Geist Mono |
| 形状 | 4–16px 同心圆角，分层投影 | 零圆角、零阴影 |
| 选中 | 强调色淡底 + 正文色 | 反白 |
| 共同点 | 竖线外框、虚线分区、等宽数据、陶土橙单一强调色 | 同左 |
| token | [quiet.tokens.css](quiet.tokens.css) | [terminal.tokens.css](terminal.tokens.css) |
| 范例 | ModelInfo 当前版本 | Owlbay 个人站 hhdxw.top |

怎么选：

- 产品型、交互多（筛选、菜单、对比、表单）的应用选 **Quiet**：圆角与投影给出层次，控件更好认。
- 内容型、个人型站点（博客、作品集、索引页）选 **Terminal**：只靠线与等宽字，更有性格，也更轻。

选定后：

1. 把对应的 `*.tokens.css` 复制为 `src/styles/tokens.css`，删掉另一套的 `.md` 与 `.tokens.css`。
2. 在 `AGENTS.md` 里把视觉规范链接指向选定的文档。
3. 按选定文档末尾「套用到新项目」的步骤安装字体、实现基元、接入检查。
