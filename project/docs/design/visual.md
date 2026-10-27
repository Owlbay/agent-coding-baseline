# Owlbay Quiet 视觉体系

Owlbay Quiet：安静、精确的数据界面。中性灰面、四阶墨色、一种强调色（陶土橙）、细线分结构、投影分层次、竖线外框加虚线分区、Inter 加 Geist Mono、快而克制的动效。密度与精度参照 Linear，配色与外框是自己的体系。

取值只在 [tokens.css](tokens.css)（复制到 `src/styles/tokens.css`），间距层级见 [spacing.md](spacing.md)。每条规则都能被检查：违反即 `scripts/check-design.mjs` 失败，或在自查时能被指出。

## 颜色

- **面**分五级 `--surface-0…4`，组件只用角色名：`--bg` 页面、`--bg-raised` 下沉（代码块、吸顶列）、`--bg-input` 输入框、`--bg-card` 卡片、`--bg-panel` 菜单与弹层、`--bg-elevated` 悬浮与分段控件当前项、`--bg-translucent` 毛玻璃（顶栏、吸顶工具栏）。
  - 深色（默认）：#161616 → #2d2d2d。
  - 浅色：#f0f0f0（页面）/ #e8e8e8（下沉）/ #f7f7f7（卡片）/ #fafafa（菜单）/ #e2e2e2（悬浮）。
  - 面、字、线都不带色偏；整套配色里只有强调色带颜色。
- **字**分四阶：`--ink` 标题与主要文字、`--ink-2` 正文、`--ink-3` 标签与元信息、`--ink-4` 只做装饰（禁用态、背景纹理），不承载需要阅读的文字。可读文字在所有面上对比度 ≥ 4.5:1（大字 ≥ 3:1），深浅两套都成立。
- **线**只画结构：`--line-soft` 行分隔、`--line` 面板描边、表头底线、外框竖线与分区虚线、`--line-strong` 输入框与芯片描边。用半透明白（深色）或黑（浅色），不用实色灰。
- **唯一强调色**陶土橙：`--accent` #d27a52；主按钮与焦点 `--accent-ui` #b35a35（白字对比度 ≥ 4.5:1）；文字 `--accent-text`（深色 #e3906a、浅色 #9e4d2b）。只出现在这些地方：
  - 焦点环；
  - 主按钮；
  - 顶栏当前页指示线；
  - 选中底 `--selected-bg`（= `--accent-tint`，配 `--ink` 文字，不反白）；
  - 正文链接；
  - 强调性数据（请求方法标签、「最优」徽标、背景纹理的点亮）。
  不做标题色、图标色或大面积色块。
- 状态色（成功、警告、错误）不进 token；确需表达时先在 tokens.css 加带角色名的变量。表单错误优先用 `--ink-3` 文字加一行说明表达。
- 换品牌色只改 `--accent*` 一组（深浅各一份）与 `--selection`、`--shadow-focus`，其余不动。

## 字体

- Inter Variable（`--font-sans`）用于标题、正文、导航和控件，引入 `@fontsource-variable/inter/opsz.css` 以启用光学尺寸（大字号自动切 Display 字形）。Geist Mono（`--font-mono`）只用于数据：ID、数值、价格、日期、路径、代码、快捷键、芯片里的标识符，一律 `tabular-nums`。CJK 回退 PingFang SC / Hiragino Sans GB / Noto Sans SC。字体本地打包，不走 CDN，并登记到 `THIRD_PARTY_NOTICES.md`（两者都是 SIL OFL 1.1）。
- 字重只有三档：`--fw-regular` 400、`--fw-medium` 510、`--fw-semibold` 590（页面标题）。不用 600 以上。
- 字号只用 token：
  - 界面 13–15px（`--fs-body-sm` / `--fs-ui` / `--fs-body`）；
  - 正文 15–16px（`--fs-body` / `--fs-prose`）；
  - 表头与小标签 12px（`--fs-label`）；
  - 等宽 12–13px（`--fs-mono-sm` / `--fs-mono`）。
  标题层级：`--fs-display`（首屏）> `--fs-h1`（页面）> `--fs-h2`（分区，20px）> `--fs-h3`（18px）。
- 字距：大字号收紧（`--ls-display` -0.03em、`--ls-h1` -0.025em、`--ls-h2` -0.015em），小标签放宽（`--ls-label`），等宽字距为 0。
- 页面标题可用 `.text-gradient`（`--ink` → `--ink-2` 的渐变字），每页最多一次，只用于页面标题或首屏标题。
- 标题 `text-wrap: balance`，简介 `text-wrap: pretty`；长 ID 与地址 `overflow-wrap: anywhere`；触屏下输入框字号不小于 16px。

## 形状与层次

- 圆角阶梯 `--radius-1…5` = 4 / 6 / 8 / 12 / 16px，另有 `--radius-pill`：芯片、键帽、菜单项 4px；小控件、分段项 6px；按钮、输入框、菜单面板 8px；卡片 12px；大卡片与对话框 16px。
- 嵌套圆角同心：外 = 内 + 内距（菜单 8 = 项 4 + 内距 4；分段 8 = 项 6 + 内距 2）。
- 细线表达结构，投影表达层次：卡片 `--shadow-1`，菜单与弹层 `--shadow-2`，对话框与浮动托盘 `--shadow-3`。深色面带 1px 内侧顶部高光（已含在投影 token 里）。`box-shadow` 只能是 `var(--shadow-*)`、`none`，或模糊为 0 的 1–2px 细线。
- 卡片只用于需要成组的独立对象（推荐组合、估算结果），不把所有内容都装进卡片。
- 层级只用 `--z-raised`（固定列）< `--z-sticky`（吸顶工具栏、托盘）< `--z-nav`（顶栏）< `--z-menu`（菜单，在各自层叠上下文内）< `--z-overlay`。

## 结构

- **顶栏**：吸顶，高 56px（手机 48px），`--bg-translucent` + `backdrop-filter: var(--backdrop)` + 底边 `--line-soft`。导航项是药丸形，带快捷键键帽；当前页 = `--ink` 文字 + 淡底 + 一条 2px `--accent-ui` 下划线压在顶栏底线上。手机上次要导航收起，工具收成图标按钮。
- **内容页外框** `.page`：外缘与顶栏内容边缘对齐，左右两条 1px `--line` 竖线从顶栏贯穿到页脚，框内左右留白 `--page-pad`（桌面与平板 32px、≤640 16px）。内容少时页脚贴底。首屏与营销页不画外框。
- **分区**：一条横跨两竖线的虚线（`--line`，4px 线段、4px 间隔）。标题行 = 标题（`--fs-h2`、510）+ 计数芯片 + 右侧操作；脚注是一行等宽小字（来源在左、快照日期在右）。
- **吸顶工具栏**：毛玻璃，横跨两条竖线（负外边距 `--page-pad`），`top: calc(var(--nav-h) + env(safe-area-inset-top))`；手机上不吸顶。
- **宽度**：内容最宽 `--content-max` 1440px，两侧留白 `--gutter`（20–48px）。网格子项一律 `minmax(0, 1fr)` / `min-width: 0`，宽内容只在自身容器内横向滚动。
- **尺寸**：列表行 44px、表格行 40px、表头 36px；控件 32 / 36 / 44px，触屏各加 4px，点击区不小于 40px；搜索框 48px。
- **页脚**：顶部一条 `--line-soft`，左边品牌（`--ink-3`），右边次要入口（幽灵按钮）。

## 组件配方

基元放在全局样式里（如 `utilities.css`），按名字就知道用法：

- **按钮** `.btn` + `.btn-primary`（强调色实底，每个视图最多一个）/ `.btn-secondary`（`--bg-card` + `--line`）/ `.btn-ghost`（只有文字，hover 时出底）；尺寸 `.btn-sm` 32px / 默认 36px / `.btn-lg` 44px；图标按钮 `.btn-icon`。`aria-pressed="true"` 取选中底；禁用用 `--ink-4`。
- **输入框** `.input`（图标 + `<input>`）：`--bg-input` 底、`--line` 描边，聚焦时 `--accent-ui` 描边 + `--shadow-focus`；`.input--lg` 首屏搜索、`.input--sm` 菜单内搜索、`.input--bare` 无框。
- **芯片** `.chip`：等宽 12px、细线、4px 圆角，用于枚举值（接口类型、能力、等级、SDK 名）。**徽标** `.badge`：18px，用于状态词（最优、已下线）。**键帽** `.kbd`：20px、等宽 11px、`--shadow-kbd`，触屏不显示。
- **分段控件** `.seg` + `.seg__item`：当前项浅一级的面 + `--shadow-1`。
- **菜单 / 弹层** `.menu`、`.popover`：`--bg-panel` + `--line` + 8px + `--shadow-2`，从触发器一侧缩放进入；当前项取选中底；结果面板带头尾行（标签 + 键帽）。
- **表格**：表头 12px 标签色、`--line` 底线；数字列右对齐等宽；行 hover `--hover-row`；固定列用不透明的 `--hover-row-solid`。
- **关键数据**：小标签（12px 510 `--ink-3`）+ 大数字（等宽 `--fs-h2`）+ 可选小号单位，每格左侧一条 `--line-strong` 竖线；数字不断开，放不下时单位整体换行。
- **地址行**：方法芯片（`--accent-text`）+ 完整地址 + 复制按钮，36px、`--bg-raised`、8px。**代码块**：`--bg-raised` + `--line` + 12px，标题栏 40px 加复制；着色只用墨阶，数字是唯一的强调色。
- **图标**：24 网格、1.5 描边、圆头圆角、`currentColor`；按钮内的图标用 `--ink-3`，hover 时随文字变 `--ink`。

## 页面模式

- **首屏**：一屏高（`100svh`），不画外框；大标题（`--fs-display`、590）+ 大搜索框，结果在弹层里（↑↓ 选择、回车打开、Esc 关闭，首项预选）。背景可以用真实数据铺成的低对比纹理，中心留安静区，指针附近点亮为强调色。
- **列表页**：标题区左边标题加简介，右边关键数据。吸顶工具栏依次是：可伸展的搜索、筛选下拉、计数（等宽 `--ink-3`）、视图切换。表头与行共用同一套列定义，数字右对齐。平板减列，手机改两行。宽表横向滚动并固定首列。多选模式下，已选行带左侧 2px 强调竖线和选中底，底部出现浮动托盘。筛选与视图状态写进 URL。
- **详情页**：返回（幽灵小按钮）→ 眉题（来源 logo + 等宽 ID）→ 标题与简介 → meta 行（日期、报告错误、主要操作）。之后依次是：关键数据条；规格分组（桌面 4 列、平板 2 列、手机 1 列，标签列用 subgrid 取组内最长标签，枚举值用芯片，整组未知时只显示一行「未公布」）；地址行；代码块；来源列表。
- **对比页**：表头行和首列双向固定；有分组行；最优值标徽标，且只在单位相同时比较；「只显示差异」是一个可按下的切换。
- **文档页**：吸顶目录，滚动时高亮当前分区；正文用 prose；接口用地址行加代码块；在线调试的「发送」是全页唯一的主按钮。

## 响应式

- 三档断点：≤640 手机、641–1024 平板、≥1025 桌面。触屏能力用 `(pointer: coarse)`、`(hover: hover) and (pointer: fine)` 判断，不按宽度猜。
- 高度用 `svh` / `dvh`，不用 `vh`；吸顶与吸底元素加 `env(safe-area-inset-*)`；全局设 `-webkit-tap-highlight-color: transparent`，控件加 `touch-action: manipulation`；不禁止缩放。

## 动效

- 只动 `transform` 与 `opacity`（颜色过渡例外，时长 ≤ `--dur-1`）。曲线：进入与退出用 `--ease-out`，屏内移动用 `--ease-in-out`，匀速用 `linear`；不用 `ease-in`。
- 时长：hover 与颜色 120ms，菜单进入 180ms，视图切换 260ms，按下 160ms；退出比进入快；界面动效都不超过 300ms。
- 可按的元素 `:active` 时缩到 `--scale-press`（0.97）；菜单从 `scale(0.96)` 加透明度进入，`transform-origin` 在触发器一侧；永远不从 `scale(0)` 开始。
- 键盘触发的动作不动画：单键跳页、`/` 聚焦、Esc 关闭、键盘打开的菜单。
- hover 样式一律包在 `@media (hover: hover) and (pointer: fine)` 里。
- `prefers-reduced-motion: reduce` 时保留淡入淡出，去掉位移与缩放；背景纹理静止。
- 来源：Emil Kowalski 的设计工程规则（emilkowalski/skills，MIT）。

## 检查

- `node scripts/check-design.mjs`（接进项目的 check 脚本）：组件样式里出现写死的字号、行高、间距、字面颜色、`transition: all`、非零字面圆角、`ease-in`、`scale(0)`、超过 300ms 的字面时长、带模糊或扩散的字面投影，都会失败。确需例外时，在同一行写 `design-ok` 和原因；新数值先加到 tokens.css。
- 改动 UI 后自查：桌面 1440、平板 768、手机 375 三种宽度，深浅两套主题，各个语言；同时确认 hover 已门控、焦点环可见、对比度达标。

## 套用到新项目

1. 安装字体：`@fontsource-variable/inter`、`@fontsource-variable/geist-mono`，在根布局引入 `@fontsource-variable/inter/opsz.css` 和 Geist Mono，并登记许可证。
2. 把 `docs/design/tokens.css` 复制到 `src/styles/tokens.css`，最先引入；按需改强调色。
3. 在全局样式里实现上面的基元，组件只用基元和 token。
4. 把 `scripts/check-design.mjs` 接进 `package.json` 的 `check`。
5. 在本目录为项目补一份「页面」规则（各页的行高、工具栏、卡片用法、强调色出现的位置），写成可检查的条目。
