# agent-coding-baseline

Agent 编程（Claude Code / Codex）的个人基准仓库：统一个人偏好、commit 规范、项目模板和常用第三方 skill，让每个新项目从同一套规范起步。

## 收录内容

| 内容 | 来源 | 安装位置 |
| --- | --- | --- |
| 个人偏好 | `user/claude/CLAUDE.md`、`user/codex/AGENTS.md` | `~/.claude/`、`~/.codex/` |
| UI 视觉体系：Owlbay Quiet / Owlbay Terminal 两套风格与 token 模板 | `project/docs/design/visual.md`、`quiet.*`、`terminal.*` | 新项目 `docs/design/` |
| UI 间距层级规范 | `project/docs/design/spacing.md` | 新项目 `docs/design/` |
| 设计约束检查 | `project/scripts/check-design.mjs` | 新项目 `scripts/` |
| commit 规范（`/commit`） | `user/claude/commands/commit.md` | `~/.claude/commands/` |
| 组件尺寸图约定（摘要，不含上游源码） | [enesozturk/dimensional-drawing](https://github.com/enesozturk/dimensional-drawing)（MIT） | 不安装；见 [`docs/references/interface-design/dimensional-drawing.md`](docs/references/interface-design/dimensional-drawing.md) |

第三方 skill 按功能放在 `vendor/<category>/<upstream-id>/`。每个 skill 只进一个分类。作者、许可证、未收录路径在 `skills.json`，锁定的提交在 `skills.lock.json`，可读的汇总在 [`docs/UPSTREAMS.md`](docs/UPSTREAMS.md)。许可证文件跟在对应的上游目录里。

安装时去掉分类层：用户级 skill 装到 `~/.claude/skills/<name>/`，项目级 skill 装到目标项目的 `.claude/`。

### 界面设计

布局、配色、排版、表面、文案，以及整页界面的打磨。

| Skill | 来源 | 用途 | 安装 |
| --- | --- | --- | --- |
| better-colors | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | 生成调色板、命名语义 token、换算色值并检查对比度 | 用户级 |
| better-layout | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | 处理分组、对齐、阅读顺序和响应式结构 | 用户级 |
| better-typography | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | 处理字级、字距、字体特性、换行和标点 | 用户级 |
| better-ui | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | 给出圆角、阴影、图标状态和界面动效的具体数值 | 用户级 |
| better-writing | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | 写并检查标签、错误、空状态和确认文案 | 用户级 |
| explain-interface | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | 根据网址或截图说明界面、视觉效果或动效是怎么做出来的 | 用户级 |
| emil-design-eng | [emilkowalski/skills](https://github.com/emilkowalski/skills) | Emil 的界面打磨、组件取舍和动效判断 | 用户级 |
| impeccable | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | 设计、改版、打磨或评审前端界面，并带上 agents 与 hook | 项目级 |

### 动效

动效的实现、评审、审计、性能、用语，以及手势与弹簧。`animate-expo` 写的是 React Native / Expo 上的动效，和下面「移动端」里让网页少一点浏览器感的 `mobile-native` 各做一件事。

| Skill | 来源 | 用途 | 安装 |
| --- | --- | --- | --- |
| animate | [emilkowalski/skills](https://github.com/emilkowalski/skills) | 从零实现一段 web 动效，并决定要不要动 | 用户级 |
| animate-expo | [emilkowalski/skills](https://github.com/emilkowalski/skills) | 用 Reanimated 等为 Expo / React Native 实现动效和手势 | 用户级 |
| animation-performance | [emilkowalski/skills](https://github.com/emilkowalski/skills) | 把掉帧的动效收进帧预算 | 用户级 |
| animation-vocabulary | [emilkowalski/skills](https://github.com/emilkowalski/skills) | 把口头描述的动效换成准确说法 | 用户级 |
| find-animation-opportunities | [emilkowalski/skills](https://github.com/emilkowalski/skills) | 找出该加动效的地方，并否掉不该加的 | 用户级 |
| remove-animations | [emilkowalski/skills](https://github.com/emilkowalski/skills) | 找出不该留下的动效并删掉，只做减法 | 用户级 |
| improve-animations | [emilkowalski/skills](https://github.com/emilkowalski/skills) | 审计整个代码库的动效，给出可执行的修改计划 | 用户级 |
| review-animations | [emilkowalski/skills](https://github.com/emilkowalski/skills) | 按严格标准评审已有动效 | 用户级 |
| apple-design | [emilkowalski/skills](https://github.com/emilkowalski/skills) | 把 Apple 的手势、弹簧和可打断动效原则用到 web | 用户级 |

### 移动端

| Skill | 来源 | 用途 | 安装 |
| --- | --- | --- | --- |
| mobile-native | [emilkowalski/skills](https://github.com/emilkowalski/skills) | 处理手机网页上的粘滞悬停、点击高亮、100vh、输入框缩放和安全区 | 用户级 |

### 可访问性

| Skill | 来源 | 用途 | 安装 |
| --- | --- | --- | --- |
| better-accessibility | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | 按 WCAG 2.2 检查键盘、焦点、ARIA、表单、读屏和缩放 | 用户级 |

### 评审与压测

`break` 把组件放上临时页，铺开它会遇到的场景。`break-ui` 用真实的最坏数据去压同一块界面。名称不同，两份都收录。

| Skill | 来源 | 用途 | 安装 |
| --- | --- | --- | --- |
| better-interface | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | 从无障碍、布局、文案、排版、配色和 UI 打磨给出一份排序后的评审 | 用户级 |
| interface-review | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | 评审分支或未提交改动引入的界面问题 | 用户级 |
| web-design-guidelines | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | 按 Vercel Web Interface Guidelines 评审 UI 代码 | 用户级 |
| break | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | 在临时页上用组件会遇到的各种场景做压测 | 用户级 |
| break-ui | [emilkowalski/skills](https://github.com/emilkowalski/skills) | 用真实的最坏数据压测界面，并标出坏掉的地方 | 用户级 |

### 原型与变体

`variant` 留在真实页面上做变体。`prototype` 在隔离的原型面上发散，选定后再合进产品。名称不同，两份都收录。

| Skill | 来源 | 用途 | 安装 |
| --- | --- | --- | --- |
| variant | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | 在真实页面上做多个有明确差异的变体，再挑一个 | 用户级 |
| prototype | [emilkowalski/skills](https://github.com/emilkowalski/skills) | 在隔离的原型面上做几个不同方向，用切换器挑选后再合进产品 | 用户级 |

### 前端库

| Skill | 来源 | 用途 | 安装 |
| --- | --- | --- | --- |
| pick-ui-library | [emilkowalski/skills](https://github.com/emilkowalski/skills) | 按 Emil 的清单为当前任务选前端库 | 用户级 |
| ask-sonner | [emilkowalski/skills](https://github.com/emilkowalski/skills) | 安装、样式化和排查 Sonner toast | 用户级 |

### 语言与工程

| Skill | 来源 | 用途 | 安装 |
| --- | --- | --- | --- |
| write-swift | [emilkowalski/skills](https://github.com/emilkowalski/skills) | 写现代 Swift：值类型、Swift 6 并发、泛型、性能和 Swift Testing | 用户级 |

## 结构

```text
agent-coding-baseline/
├── user/                    # 个人级配置（自己维护）
├── project/                 # 新项目模板：AGENTS.md、CLAUDE.md、.claude/、docs/、编辑器与 git 配置
├── docs/                    # 基准仓库文档，不进项目模板
│   ├── README.md            # 子目录索引：各目录放什么、新资料登记在哪
│   ├── UPSTREAMS.md         # 上游清单，由 render-upstreams.py 生成
│   └── references/          # 外部资料的约定摘要，主题 id 与 vendor 分类一致
│       └── interface-design/
│           └── dimensional-drawing.md
├── vendor/                  # 只由 sync-upstream.py 写入：vendor/<category>/<upstream-id>/
│   ├── interface-design/
│   │   ├── emilkowalski-skills/    # emil-design-eng
│   │   ├── impeccable/             # impeccable，以及 agents、hooks、LICENSE、NOTICE
│   │   └── jakubkrehel-skills/     # better-colors、better-layout、better-typography、better-ui、better-writing、explain-interface
│   ├── motion/
│   │   └── emilkowalski-skills/    # animate、animate-expo、animation-performance、animation-vocabulary、apple-design、find-animation-opportunities、improve-animations、remove-animations、review-animations
│   ├── mobile/
│   │   └── emilkowalski-skills/    # mobile-native
│   ├── accessibility/
│   │   └── jakubkrehel-skills/     # better-accessibility
│   ├── review/
│   │   ├── emilkowalski-skills/    # break-ui
│   │   ├── jakubkrehel-skills/     # better-interface、break、interface-review
│   │   └── vercel-agent-skills/    # web-design-guidelines；许可证在 README.md
│   ├── prototyping/
│   │   ├── emilkowalski-skills/    # prototype
│   │   └── jakubkrehel-skills/     # variant
│   ├── frontend-libraries/
│   │   └── emilkowalski-skills/    # ask-sonner、pick-ui-library
│   └── language/
│       └── emilkowalski-skills/    # write-swift
├── skills.json              # 上游清单：仓库、许可证、分类、同步路径、安装范围
├── skills.lock.json         # 当前同步到的上游提交
├── .github/workflows/
│   ├── upstream-update.yml  # 每周一 01:00 UTC 拉上游；有变化则开 PR，不合并
│   └── check.yml            # push / PR 时跑 scripts/check.sh
└── scripts/
    ├── sync-upstream.py     # 同步 vendor/；--check 只看有无更新；--report 列出新 skill
    ├── render-upstreams.py  # 用 skills.json 和 skills.lock.json 生成 docs/UPSTREAMS.md
    ├── upstream-pr.py       # 有变化时开或更新同一个上游 PR
    ├── install-skills.py    # user：装到 ~/.claude/skills/<name>；project <目录>：装 skill/agents 并合并 hooks
    ├── new-project.sh       # 拷模板到目标目录（不覆盖已有文件）；--skills 顺带装项目级 skill
    ├── sync-user.sh         # user/ ↔ 本机：默认看差异，--apply 写入（自动 .bak），--pull 拉回
    └── check.sh             # 语法、JSON、vendor 与清单一致性、本机配置漂移
```

同一上游跨多个分类时，每个分类目录里都有一份该上游的许可证文件。

## 常用操作

新项目套用模板并安装项目级 skill：

```bash
scripts/new-project.sh ~/Projects/xxx/my-app --skills
```

把最新的用户级 skill 装到本机：

```bash
scripts/install-skills.py user
```

本机改了 `/commit` 或个人偏好后拉回仓库：

```bash
scripts/sync-user.sh --pull
```

手动检查上游是否有更新：

```bash
scripts/sync-upstream.py --check
```

## 约定

- 个人语言、工作偏好、模型参数只放 `user/`；`project/` 只放能随项目共享的约定。`project/docs/design/` 是新项目模板里的界面风格，路径保持 `docs/design/`，不跟着 skill 分类改名。
- `vendor/` 只由同步脚本写入。每个 skill 在 `skills.json` 里有一个 `category`，同步到 `vendor/<category>/<upstream-id>/skills/<name>/`。新增上游时同时更新 `skills.json`、`docs/UPSTREAMS.md`（跑 `scripts/render-upstreams.py`）和 `THIRD_PARTY_NOTICES.md`。明确不收录的路径写在该上游的 `excluded`。
- 每周一 01:00 UTC，`.github/workflows/upstream-update.yml` 拉取上游。有变化就开或更新 `upstream-sync` 上的同一个 PR，不自动合并。新 skill 只在 PR 里提示。
- 用户级 skill 安装到 `~/.claude/skills/<name>/`，项目级 skill 安装到目标项目的 `.claude/`。安装路径不带分类名。
- `docs/` 是基准仓库自己的文档，不进项目模板。外部资料的约定摘要放 `docs/references/<category>/`，分类 id 与 `vendor/` 相同，一篇来源一份文件，写清来源和许可证，不复制上游源码；新增时登记到 `docs/README.md` 和 `THIRD_PARTY_NOTICES.md`。要安装的 skill 仍走 `vendor/`。
- 项目里的 `.claude/skills/`、`.claude/agents/` 不入库（模板 `.gitignore` 已忽略），需要时从本仓库重装。
- 提交前跑 `scripts/check.sh`。
