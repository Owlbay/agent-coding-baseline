# 文档索引

基准仓库自己的文档。这里的内容不进 `project/` 模板，也不会被 `new-project.sh` 拷进新项目。

| 目录 | 内容 |
| --- | --- |
| `references/` | 外部资料的约定摘要。按主题再分一层，一篇来源一份文件。写清来源和许可证，不复制上游源码。要安装的 skill 仍走 `vendor/`。 |

| 主题 | 放什么 |
| --- | --- |
| `references/design/` | 界面、图纸、视觉说明方法 |

| 文档 | 内容 |
| --- | --- |
| [references/design/dimensional-drawing.md](references/design/dimensional-drawing.md) | 组件尺寸图：只画结构、代号与公式、不发明数值 |

新增一份资料时：放到对应主题目录（没有合适主题就新建目录），在上表登记，并在根目录 `THIRD_PARTY_NOTICES.md` 记下许可证。
