# Third-party notices

`vendor/` 下的内容由 `scripts/sync-upstream.py` 从上游原样同步，未做修改；对应提交记录在 `skills.lock.json`。各目录保留上游的 LICENSE（及 NOTICE），并继续受其许可证约束。

## jakubkrehel/skills → `vendor/jakubkrehel-skills/`

- 作者：Jakub Krehel，Copyright (c) 2026 Jakub Krehel
- 来源：https://github.com/jakubkrehel/skills（https://jakub.kr/skills）
- 许可证：MIT，全文见 `vendor/jakubkrehel-skills/LICENSE`
- 用途：UI、可访问性、配色、布局、排版、文案的评审与打磨指引，安装为用户级 skill。

## pbakaus/impeccable → `vendor/impeccable/`

- 来源：https://github.com/pbakaus/impeccable（https://impeccable.style），同步其 `plugin/` 下的 skills、agents、hooks
- 许可证：Apache License 2.0，全文见 `vendor/impeccable/LICENSE`；上游第三方声明见 `vendor/impeccable/NOTICE.md`
- 用途：前端设计与评审 skill、配套子代理，以及 UI 变更检测 hook，安装为项目级 skill。
- 说明：`scripts/install-skills.py` 安装时会把 hooks 中的 `${CLAUDE_PLUGIN_ROOT}` 改写为 `${CLAUDE_PROJECT_DIR}/.claude`，写入目标项目的 settings，`vendor/` 中的文件本身不改动。

## vercel-labs/agent-skills → `vendor/vercel-agent-skills/`

- 作者：Vercel
- 来源：https://github.com/vercel-labs/agent-skills，仅同步 `skills/web-design-guidelines`
- 许可证：MIT。上游仓库没有单独的 LICENSE 文件，许可证声明见其 README 的 License 小节，同步保存在 `vendor/vercel-agent-skills/README.md`
- 用途：按 Vercel Web Interface Guidelines 评审 UI 代码，安装为用户级 skill。该 skill 运行时会从 https://github.com/vercel-labs/web-interface-guidelines （MIT）拉取最新规则，规则本身不入库。

## emilkowalski/skills → `vendor/emilkowalski-skills/`

- 作者：Emil Kowalski，Copyright (c) 2026 Emil Kowalski
- 来源：https://github.com/emilkowalski/skills，只同步动效相关 skill：`animate`、`review-animations`、`improve-animations`、`find-animation-opportunities`、`animation-performance`、`animation-vocabulary`、`animate-expo`、`apple-design`、`emil-design-eng`
- 许可证：MIT，全文见 `vendor/emilkowalski-skills/LICENSE`
- 用途：动效的构建、评审、审计、性能与用语指引，安装为用户级 skill。
- 未同步：`write-swift`、`pick-ui-library`、`prototype`、`mobile-native`、`break-ui`、`ask-sonner`。这些与动效无关，不进入 `vendor/`。

## 参考整理（未同步进 vendor/）

### enesozturk/dimensional-drawing

- 作者：Enes Ozturk，Copyright (c) 2026 Enes Ozturk
- 来源：https://github.com/enesozturk/dimensional-drawing
- 许可证：MIT，全文见上游仓库 LICENSE。本仓库未复制其源码、示例或媒体文件。
- 用途：`docs/references/design/dimensional-drawing.md` 整理组件尺寸图的可复用约定。需要原技能出图时从上游安装，不经过 `scripts/sync-upstream.py`。
