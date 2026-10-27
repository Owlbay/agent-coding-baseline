# Owlbay Terminal 视觉体系

Owlbay Terminal：安静的索引终端。一块暖近黑底、一组暖灰文字、一种陶土色；结构靠线，不靠色块、阴影或圆角。等宽字承载数据，像在终端里翻一份整齐的索引。范例：Owlbay 个人站（hhdxw.top）与 ModelInfo 重设计之前的版本。另一套风格见 [Owlbay Quiet](quiet.md)，两者怎么选见 [visual.md](visual.md)。

取值只在 [terminal.tokens.css](terminal.tokens.css)（复制为 `src/styles/tokens.css`），间距层级见 [spacing.md](spacing.md)。每条规则都能被检查：违反即 `scripts/check-design.mjs` 失败，或在自查时能被指出。

## 颜色

- 深色默认：底 `--bg` #141413，抬升 `--bg-raised` #1a1a18，面板 `--bg-panel` #1e1d1b；字 `--ink` #faf9f5，次级 `--ink-2` / `--ink-3`。`--ink-4` 只做装饰（字墙暗词、禁用态、滚动条），不承载需要阅读的文字。
- 浅色主题是同一套关系的反相（底 #faf9f5、字 #141413），只替换变量值。
- 线用半透明暖白（浅色为半透明暖黑）：`--line-soft` 行分隔、`--line` 外框与面板描边、`--line-strong` 输入框、标签与关键数据竖线。
- **唯一强调色**陶土橙 `--accent` #d97757（浅色下控件用 `--accent-ui` #c15f3c、文字用 `--accent-text` #b0522f）。只出现在：像素 logo、字墙点亮的词、输入光标、当前位置细线、焦点环、请求方法。不做按钮底、链接色或标题色。
- **选中 = 反白**：`--selected-bg`（= `--ink`）做底，`--selected-ink`（= `--bg`）做字。用于分段控件当前项、搜索结果当前项、菜单当前项、开关的按下态。
- **当前位置 = 陶土色 2px 细线**：顶栏当前页压在底边上。

## 字体

- Geist（`--font-sans`）用于标题、正文、导航、说明；Geist Mono（`--font-mono`）只用于数据：ID、数值、价格、日期、路径、快捷键、角标，一律等宽数字。本地打包（`@fontsource-variable/geist`、`@fontsource-variable/geist-mono`），登记 SIL OFL 1.1。CJK 回退 PingFang SC / Hiragino Sans GB / Noto Sans SC。
- 字重只有 400 / 500；层级靠字号与颜色阶，不靠加粗。
- 字号阶梯：`--fs-display`（首屏）> `--fs-h1`（页面标题）> `--fs-h2`（分区标题）> `--fs-h3`；正文 16px、说明 14px、等宽数据 13px、角标 11px。页面标题始终比分区标题大一级。
- 角标 `.corner`：等宽 11px、500、0.06em 字距、拉丁字母大写；内容放计数或日期，不放区分大小写的路径。
- 快捷键写成等宽方括号 `[H]`，`--ink-3`，触屏不显示。

## 结构

- **零圆角、零阴影**。分开两块东西时画 1px 线（`--line` / `--line-soft` / `--line-strong`）或换一档底色。`border-radius` 与 `box-shadow` 只能是 0 / none，或 token 里同样为 0 / none 的变量。
- **内容页外框** `.page`：左右两条 1px `--line` 实线，与顶栏内容边缘对齐，从顶栏贯穿到页脚；框内左右留白 `--page-pad`（32px，≤640 为 16px）；内容少时页脚贴底。首页不画外框。
- **分区** `SectionFrame`：放在 `.page` 内，顶部一条 4px / 4px 虚线横贯两条竖线；右上计数角标，左下来源角标，右下快照日期角标。分区里已有更醒目的入口（如工具栏）时，标题只给读屏器。
- **一行一条的列表** `.list-row`：52px、`--line-soft` 底线、hover `--hover-row`，组件只定义列布局；表头与行用同一字号，保证 `ch` 列宽对齐。
- **页面标题** `PageHeader`：标题 + 一句简介 + 可选操作；右侧可放关键数据，平板及以下排到下方。
- **宽度**：两侧留白 `max(20px, 4vw)`，超宽屏封顶 2400px；`.page` 的直接子项 `min-width: 0`，宽内容只在自身容器内横向滚动。控件高 44px，搜索框 56px，顶栏 64px（手机 52px）。

## 组件

- **顶栏**：品牌（像素 logo + 文字）、导航（`[H]` 键帽 + 名称）、次要入口、语言、主题；当前页文字 `--ink` + 陶土色 2px 底线。实底 `--bg`，底边 `--line-soft`；首页底边改虚线，与字墙栅格呼应。手机上次要导航收起。
- **页脚**：左侧品牌（`--ink-3`），右侧次要入口；首页顶边用虚线。
- **按钮**：`.btn-primary` 反白实底（`--ink` 底、`--bg` 字），`.btn-ghost` 1px 描边；都是直角，hover 只换底色与描边。
- **关键数据**：小标签（Geist）+ 大数字（等宽，`--fs-h2`，手机 `--fs-h3`）+ 可选小号单位，每格左侧一条 `--line-strong` 竖线。
- **筛选下拉**：触发器 1px `--line-strong` 描边，显示「标签 当前值」；面板 `--bg-panel` + `--line`，选项带计数，当前项反白；选项多时面板顶部带搜索。
- **地址行**：方法（陶土色）+ 完整地址 + 复制按钮，`--bg-raised` 底；**代码块**：标题栏 + 复制按钮，正文 `--bg-raised`。
- **标签**：接口类型、能力、等级用小方框（`--line-strong` 描边、零圆角、等宽 12px），与模态小图标一致。
- **命令行**（可选，个人站用）：页面底部一条 `guest@site >` 提示符 + 陶土色闪烁光标的输入栏，支持 `/help` 等命令或直接搜索；`--bg-panel` 底、顶边 `--line`。

## 页面模式

- **首页**：一屏，不画外框；顶栏、字墙 hero、页脚。字墙由真实词条（文章标题、模型名）以等宽字铺满，明暗分四级，指针附近点亮为陶土色，点击直达；中央两行标题 + 搜索框（结果面板 `--bg-panel` 底，当前项反白，↑↓ / 回车 / Esc）。触屏时字墙减量调暗，缓慢轮换点亮几个词。
- **列表页**：标题区（左标题 + 简介，右关键数据）+ 分区；分区顶部一行工具栏：搜索框伸展、筛选下拉、右侧「筛选后 / 总数」计数与视图切换，平板及以上吸顶；筛选与视图状态同步到 URL。宽表横向滚动，首列固定，滚动后右缘一条 `--line`。
- **详情页**：关键数据条 + 规格分组（桌面 4 列、平板 2 列、手机 1 列，标签用 Geist `--ink-3`，值用等宽，标签列 subgrid 取最长）；整组未知只显示一行「未公布」；其后是地址行、代码块、来源列表。
- **文章页**（个人站）：窄栏正文，代码块与表格直角细线；目录与元信息用等宽小字。

## 响应式

三档断点：≤640 手机、641–1024 平板、≥1025 桌面。列表行在平板减列、在手机改两行；地址行在手机上地址独占一行、按钮换行铺满；网格子项一律 `minmax(0, 1fr)` / `min-width: 0`。hover 样式包在 `@media (hover: hover)` 里。

## 动效

- 状态过渡 120ms，面板 200ms，视图切换不超过 300ms，缓动 `--ease-out`；不用 `ease-in`，不用 `transition: all`。跨页与主题切换用 View Transitions；筛选只过渡列表区。
- 按钮按下缩到 `--scale-press`（0.97）。键盘触发的动作不动画。
- `prefers-reduced-motion` 下保留淡入淡出，去掉位移与缩放；字墙静止。

## 检查

- `node scripts/check-design.mjs`：组件样式里出现写死的字号、行高、间距、字面颜色、`transition: all`、非零字面圆角、`ease-in`、`scale(0)`、超过 300ms 的字面时长、带模糊的字面投影，都会失败。确需例外时，在同一行写 `design-ok` 和原因；新数值先加到 tokens.css。
- 改动 UI 后自查：桌面 1440、平板 768、手机 375，深浅两套主题，各个语言。

## 套用到新项目

1. 安装字体：`@fontsource-variable/geist`、`@fontsource-variable/geist-mono`，在根布局引入，并登记许可证。
2. 把 `docs/design/terminal.tokens.css` 复制为 `src/styles/tokens.css`，最先引入。
3. 实现 `.page`、`.list-row`、`.corner`、`.btn-primary` / `.btn-ghost`、`SectionFrame`、`PageHeader` 等基元，组件只用基元和 token。
4. 把 `scripts/check-design.mjs` 接进 `package.json` 的 `check`。
5. 在本目录为项目补一份「页面」规则，写成可检查的条目。
