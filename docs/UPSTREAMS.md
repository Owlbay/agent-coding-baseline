# 上游清单

本文件由 `scripts/render-upstreams.py` 根据 `skills.json` 和 `skills.lock.json` 生成。不要手改。改清单或锁定提交后运行 `python3 scripts/render-upstreams.py`。`scripts/check.sh` 会核对本文件与这两份 JSON 一致。

## 已同步的上游

这些上游由 `scripts/sync-upstream.py` 写入 `vendor/<category>/<upstream-id>/`。作者、许可证、分类和未收录路径以 `skills.json` 为准，锁定提交以 `skills.lock.json` 为准。

### jakubkrehel/skills

- 清单 id：`jakubkrehel-skills`
- 仓库：https://github.com/jakubkrehel/skills
- 主页：https://jakub.kr/skills
- 作者：Jakub Krehel
- 许可证：MIT（文件 `LICENSE`）
- 安装范围：用户级，安装到 `~/.claude/skills/<name>/`
- 锁定提交：[`592aedc`](https://github.com/jakubkrehel/skills/commit/592aedc44d7d5b3e29740984252902f3e5402a1c)（`592aedc44d7d5b3e29740984252902f3e5402a1c`）
- 上游提交时间：2026-10-25T09:26:16-04:00
- 同步时间：2026-10-28T18:14:05+00:00

| Skill | 分类 |
| --- | --- |
| `better-colors` | 界面设计（`interface-design`） |
| `better-layout` | 界面设计（`interface-design`） |
| `better-typography` | 界面设计（`interface-design`） |
| `better-ui` | 界面设计（`interface-design`） |
| `better-writing` | 界面设计（`interface-design`） |
| `explain-interface` | 界面设计（`interface-design`） |
| `better-accessibility` | 可访问性（`accessibility`） |
| `better-interface` | 评审与压测（`review`） |
| `interface-review` | 评审与压测（`review`） |
| `break` | 评审与压测（`review`） |
| `variant` | 原型与变体（`prototyping`） |

#### 未收录

| 路径 | 原因 |
| --- | --- |
| `skills/build-design` | 从 Figma 或设计图还原界面。不在安装清单里，不同步。 |
| `skills/state-machine` | 把组件的每个状态铺在临时页上。不在安装清单里，不同步。 |
| `skills/teardown` | 为实物或界面层次做技术插图。不在安装清单里，不同步。 |

### pbakaus/impeccable

- 清单 id：`impeccable`
- 仓库：https://github.com/pbakaus/impeccable
- 主页：https://impeccable.style
- 作者：Paul Bakaus
- 许可证：Apache-2.0（文件 `LICENSE`）
- 安装范围：项目级，安装到目标项目的 `.claude/`
- 锁定提交：[`df3a4ab`](https://github.com/pbakaus/impeccable/commit/df3a4abe7d0840d5f60324812c432e00b66a4e75)（`df3a4abe7d0840d5f60324812c432e00b66a4e75`）
- 上游提交时间：2026-10-30T10:16:26+00:00
- 同步时间：2026-10-31T04:41:04+00:00

| Skill | 分类 |
| --- | --- |
| `impeccable` | 界面设计（`interface-design`） |

#### 未收录

无。

### vercel-labs/agent-skills

- 清单 id：`vercel-agent-skills`
- 仓库：https://github.com/vercel-labs/agent-skills
- 作者：Vercel
- 许可证：MIT（文件 `README.md`）
- 许可证说明：上游无 LICENSE 文件，许可证声明在 README.md 的 License 小节
- 安装范围：用户级，安装到 `~/.claude/skills/<name>/`
- 锁定提交：[`1a2c79d`](https://github.com/vercel-labs/agent-skills/commit/1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62)（`1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62`）
- 上游提交时间：2026-10-27T14:40:02-07:00
- 同步时间：2026-10-28T18:14:07+00:00

| Skill | 分类 |
| --- | --- |
| `web-design-guidelines` | 评审与压测（`review`） |

#### 未收录

无。

### emilkowalski/skills

- 清单 id：`emilkowalski-skills`
- 仓库：https://github.com/emilkowalski/skills
- 作者：Emil Kowalski
- 许可证：MIT（文件 `LICENSE`）
- 安装范围：用户级，安装到 `~/.claude/skills/<name>/`
- 锁定提交：[`a81dbca`](https://github.com/emilkowalski/skills/commit/a81dbca07f2217b7103e510c0f13f8d5b017afc9)（`a81dbca07f2217b7103e510c0f13f8d5b017afc9`）
- 上游提交时间：2026-10-28T19:25:28+01:00
- 同步时间：2026-10-31T04:41:04+00:00

| Skill | 分类 |
| --- | --- |
| `emil-design-eng` | 界面设计（`interface-design`） |
| `animate` | 动效（`motion`） |
| `animate-expo` | 动效（`motion`） |
| `animation-performance` | 动效（`motion`） |
| `animation-vocabulary` | 动效（`motion`） |
| `find-animation-opportunities` | 动效（`motion`） |
| `remove-animations` | 动效（`motion`） |
| `improve-animations` | 动效（`motion`） |
| `review-animations` | 动效（`motion`） |
| `apple-design` | 动效（`motion`） |
| `mobile-native` | 移动端（`mobile`） |
| `break-ui` | 评审与压测（`review`） |
| `prototype` | 原型与变体（`prototyping`） |
| `pick-ui-library` | 前端库（`frontend-libraries`） |
| `ask-sonner` | 前端库（`frontend-libraries`） |
| `write-swift` | 语言与工程（`language`） |

#### 未收录

| 路径 | 原因 |
| --- | --- |
| `performance-cheatsheet.md` | 不是 skill。其中的动效性能要点已由 animation-performance 覆盖。 |

## 参考整理

这些资料不进 `vendor/`，不锁定提交，不由 `scripts/sync-upstream.py` 安装。

### dimensional-drawing

- 仓库：https://github.com/enesozturk/dimensional-drawing
- 作者：Enes Ozturk
- 许可证：MIT
- 本仓库文档：`docs/references/interface-design/dimensional-drawing.md`
- 说明：组件尺寸图的可复用约定。不复制上游源码，不经 scripts/sync-upstream.py 安装，也不锁定提交。
