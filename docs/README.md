# 文档索引

基准仓库自己的文档。这里的内容不进 `project/` 模板，也不会被 `new-project.sh` 拷进新项目。

| 目录 | 内容 |
| --- | --- |
| `references/` | 外部资料的约定摘要。主题目录用和 `vendor/` 相同的分类 id。一篇来源一份文件。写清来源和许可证，不复制上游源码。要安装的 skill 仍走 `vendor/`。 |

分类 id：`interface-design`（界面设计）、`motion`（动效）、`mobile`（移动端）、`accessibility`（可访问性）、`review`（评审与压测）、`prototyping`（原型与变体）、`frontend-libraries`（前端库）、`language`（语言与工程）。目前有资料摘要的是界面设计。

| 主题 | 放什么 |
| --- | --- |
| `references/interface-design/` | 界面设计方面的外部约定，例如尺寸图 |

| 文档 | 内容 |
| --- | --- |
| [references/interface-design/dimensional-drawing.md](references/interface-design/dimensional-drawing.md) | 组件尺寸图：只画结构、代号与公式、不发明数值 |

新增一份资料时：放到对应分类目录（没有目录就按上表的 id 新建），在上表登记，并在根目录 `THIRD_PARTY_NOTICES.md` 记下许可证。
