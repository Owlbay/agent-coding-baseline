# Third-party notices

收录范围、未收录条目和锁定提交见 [`docs/UPSTREAMS.md`](docs/UPSTREAMS.md)。`vendor/` 下的内容由 `scripts/sync-upstream.py` 从上游原样同步，未做修改。目录是 `vendor/<category>/<upstream-id>/`：每个 skill 只属于一个功能分类，许可证文件放在该上游出现过的每一个分类目录里。作者写在 `skills.json`，对应提交记录在 `skills.lock.json`。各目录继续受其许可证约束。

## jakubkrehel/skills

- 作者：Jakub Krehel，Copyright (c) 2026 Jakub Krehel
- 来源：https://github.com/jakubkrehel/skills（https://jakub.kr/skills）
- 许可证：MIT。全文随分类目录各留一份：`vendor/interface-design/jakubkrehel-skills/LICENSE`、`vendor/accessibility/jakubkrehel-skills/LICENSE`、`vendor/review/jakubkrehel-skills/LICENSE`、`vendor/prototyping/jakubkrehel-skills/LICENSE`
- 用途：安装为用户级 skill。
  - 界面设计：`better-colors`、`better-layout`、`better-typography`、`better-ui`、`better-writing`、`explain-interface`
  - 可访问性：`better-accessibility`
  - 评审与压测：`better-interface`、`interface-review`、`break`
  - 原型与变体：`variant`
- 同步范围：`skills.json` 列出的 skill 目录。上游仓库里的 `build-design`、`state-machine`、`teardown` 不在安装清单中，不进入 `vendor/`。

## pbakaus/impeccable → `vendor/interface-design/impeccable/`

- 作者：Paul Bakaus
- 来源：https://github.com/pbakaus/impeccable（https://impeccable.style），同步其 `plugin/` 下的 skill、agents、hooks
- 许可证：Apache License 2.0，全文见 `vendor/interface-design/impeccable/LICENSE`；上游第三方声明见 `vendor/interface-design/impeccable/NOTICE.md`
- 用途：前端设计与评审 skill、配套子代理，以及 UI 变更检测 hook，安装为项目级 skill。分类是界面设计。
- 说明：`scripts/install-skills.py` 安装时会把 hooks 中的 `${CLAUDE_PLUGIN_ROOT}` 改写为 `${CLAUDE_PROJECT_DIR}/.claude`，写入目标项目的 settings，`vendor/` 中的文件本身不改动。

## vercel-labs/agent-skills → `vendor/review/vercel-agent-skills/`

- 作者：Vercel
- 来源：https://github.com/vercel-labs/agent-skills，仅同步 `skills/web-design-guidelines`
- 许可证：MIT。上游仓库没有单独的 LICENSE 文件，许可证声明见其 README 的 License 小节，同步保存在 `vendor/review/vercel-agent-skills/README.md`
- 用途：按 Vercel Web Interface Guidelines 评审 UI 代码，安装为用户级 skill。分类是评审与压测。该 skill 运行时会从 https://github.com/vercel-labs/web-interface-guidelines （MIT）拉取最新规则，规则本身不入库。

## emilkowalski/skills

- 作者：Emil Kowalski，Copyright (c) 2026 Emil Kowalski
- 来源：https://github.com/emilkowalski/skills
- 许可证：MIT。全文随分类目录各留一份，例如 `vendor/motion/emilkowalski-skills/LICENSE`
- 用途：安装为用户级 skill。
  - 界面设计：`emil-design-eng`
  - 动效：`animate`、`animate-expo`、`animation-performance`、`animation-vocabulary`、`find-animation-opportunities`、`remove-animations`、`improve-animations`、`review-animations`、`apple-design`
  - 移动端：`mobile-native`
  - 评审与压测：`break-ui`
  - 原型与变体：`prototype`
  - 前端库：`pick-ui-library`、`ask-sonner`
  - 语言与工程：`write-swift`
- 未写入 `vendor/` 的根目录文件：`performance-cheatsheet.md`。它不是 skill，其中的动效性能要点已由 `animation-performance` 覆盖。

## 参考整理（未同步进 vendor/）

### enesozturk/dimensional-drawing

- 作者：Enes Ozturk，Copyright (c) 2026 Enes Ozturk
- 来源：https://github.com/enesozturk/dimensional-drawing
- 许可证：MIT，全文见上游仓库 LICENSE。本仓库未复制其源码、示例或媒体文件。
- 用途：`docs/references/interface-design/dimensional-drawing.md` 整理组件尺寸图的可复用约定，主题与界面设计分类对齐。需要原技能出图时从上游安装，不经过 `scripts/sync-upstream.py`。
