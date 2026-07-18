---
name: ui-ux-pro-max
description: UI/UX 设计智能。包含 67 种风格、161 个色板、57 组字体配对、25 种图表、16 个技术栈 (React, Next.js, Vue, Svelte, Astro, SwiftUI, React Native, Flutter, Nuxt, Nuxt UI, Tailwind, shadcn/ui, Jetpack Compose, Three.js, Angular, Laravel)。操作 (Actions)：plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check UI/UX code。项目 (Projects)：website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, mobile app, .html, .tsx, .vue, .svelte。元素 (Elements)：button, modal, navbar, sidebar, card, table, form, chart。风格 (Styles)：磨砂玻璃风 (glassmorphism), 黏土拟态 (claymorphism), 极简主义 (minimalism), 粗野主义 (brutalism), 新拟态 (neumorphism), 便当格布局 (bento grid), 暗黑模式 (dark mode), 响应式 (responsive), 拟物风格 (skeuomorphism), 扁平设计 (flat design)。主题 (Topics)：色板 (color palette), 无障碍 (accessibility), 动画 (animation), 布局 (layout), 字体排版 (typography), 字体配对 (font pairing), 间距 (spacing), 悬停 (hover), 阴影 (shadow), 渐变 (gradient)。集成 (Integrations)：用于组件搜索和示例的 shadcn/ui MCP。
---
# UI/UX Pro Max - Design Intelligence

面向 Web 和移动端应用的全面设计指南。包含跨 16 个技术栈的 67 种 UI 风格、161 个色板、57 组字体配对、99 条 UX 指南以及 25 种图表类型。支持基于优先级的推荐和可搜索数据库。

## 适用场景 (When to Apply)

当任务涉及 **UI 结构、视觉设计决策、交互模式或用户体验质量控制** 时，应使用此 Skill。

### 必须使用 (Must Use)

在以下场景中，必须调用此技能：

- 设计新的页面（Landing Page、Dashboard、Admin 后台、SaaS、移动端 App）
- 创建或重构 UI 组件（按钮、弹窗、表单、表格、图表等）
- 选择配色方案、字体系统、间距规范或布局体系
- 审查 UI 代码的用户体验、可访问性 (A11y) 或视觉一致性
- 实现导航结构、过渡动效或响应式布局
- 制定产品级的设计决策（风格偏好、信息层级、品牌调性传达）
- 提升界面的感知质量 (Perceived Quality)、清晰度或易用性

### 推荐使用 (Recommended)

在以下场景中，强烈建议使用此技能：

- 觉得 UI 视觉效果“不够专业”，但具体原因不明确时
- 收到可用性或交互体验方面的改进反馈时
- 项目上线前的 UI 走查与细节调优 (UI Polish)
- 需要多端统一设计（Web / iOS / Android）时
- 构建设计系统 (Design System) 或可复用组件库时

### 无需使用 (Skip)

在以下场景中，无需调用此技能：

- 纯后端业务逻辑开发
- 仅涉及 API 或数据库结构设计
- 与界面呈现完全无关的底层性能调优
- 基础设施搭建或 DevOps 工作
- 纯文本脚本或非视觉类自动化任务

**核心判定准则**：只要任务会影响界面的**视觉呈现（看起来如何）、用户体验（用起来如何）、动效展示（如何运动）或交互逻辑（如何响应）**，即必须调用此技能。

## 按优先级排序的规则类别

*注：本表供开发人员与 AI 查阅，用以明确 1→10 级规则的关注优先级；详细细则请使用 `--domain <Domain>` 命令检索。脚本本身不解析此表。*

| 优先级 | 类别 | 影响度 | 领域 | 关键检查项 (必须满足) | 反面模式 (避免使用) |
|----------|----------|--------|--------|------------------------|------------------------|
| 1 | 无障碍合规性 (Accessibility) | 严重 (CRITICAL) | `ux` | 对比度 4.5:1、Alt 文本、键盘导航、Aria 标签 | 强行移除焦点环、使用无标签的纯图标按钮 |
| 2 | 触控与交互 (Touch & Interaction) | 严重 (CRITICAL) | `ux` | 最小尺寸 44×44px、8px+ 间距、加载状态反馈 | 仅依赖悬停 (hover)、瞬间状态切换 (0ms) |
| 3 | 性能与加载 (Performance) | 高 (HIGH) | `ux` | WebP/AVIF、延迟加载、保留空间 (CLS < 0.1) | 布局抖动、累积布局偏移 (CLS) |
| 4 | 界面风格适配 (Style Selection) | 高 (HIGH) | `style`, `product` | 匹配产品类型、风格一致性、使用 SVG 图标 | 随机混搭扁平与拟物风、使用 Emoji 作为图标 |
| 5 | 布局与响应式 (Layout & Responsive) | 高 (HIGH) | `ux` | 移动优先断点、视口 meta 标签、无水平滚动 | 产生水平滚动条、硬编码 px 容器宽度、禁用缩放 |
| 6 | 排版与色彩 (Typography & Color) | 中 (MEDIUM) | `typography`, `color` | 正文字体 ≥16px、行高 1.5、语义化颜色 Token | 正文字体小于 12px、灰底灰字、在组件中硬编码十六进制颜色值 |
| 7 | 动效与过渡 (Animation) | 中 (MEDIUM) | `ux` | 时长 150–300ms、动效传达意图、空间连续性 | 仅作点缀的冗余动画、对宽/高做过渡、不支持减弱动态效果 (reduced-motion) |
| 8 | 表单与反馈 (Forms & Feedback) | 中 (MEDIUM) | `ux` | 可见标签、就近字段错误提示、渐进式呈现 | 仅使用占位符作标签、错误仅堆叠在顶部、初始展示过多字段 |
| 9 | 导航与层级 (Navigation Patterns) | 高 (HIGH) | `ux` | 可预测的返回、底部导航 ≤5 个、支持深层链接 | 导航项过载、返回行为混乱、缺少深层链接支持 |
| 10 | 图表与数据 (Charts & Data) | 低 (LOW) | `chart` | 图例清晰、悬停工具提示、无障碍色彩区分 | 仅依靠颜色传达数据维度与含义 |

## 快速参考指南

### 1. 无障碍合规性 Accessibility (CRITICAL)

- `color-contrast` —— 普通正文的对比度至少达到 4.5:1（大号文本为 3:1）；设计时可参考 Material Design 规范
- `focus-states` —— 交互元素上必须有清晰可见的焦点环（建议 2–4px，参考 Apple HIG 与 Material Design）
- `alt-text` —— 为具有实际信息含义的图片提供准确且描述性的 `alt` 属性
- `aria-labels` —— 针对仅包含图标的按钮必须提供 `aria-label` 属性；在移动端原生开发中对应 `accessibilityLabel`（参考 Apple HIG）
- `keyboard-nav` —— 键盘 Tab 键切换焦点顺序应与视觉布局顺序一致，提供完整的键盘无障碍通道支持（参考 Apple HIG）
- `form-labels` —— 使用带有 `for` 属性的 `label` 标签与输入框显式关联
- `skip-links` —— 为键盘操作用户提供“跳过至主要内容 (Skip to content)”的快捷导航链接
- `heading-hierarchy` —— 严格遵循 `h1` → `h6` 的阶梯级标题顺序，切勿越级使用
- `color-not-only` —— 绝不能仅通过颜色差异来传达信息（应结合图标或文本补充说明）
- `dynamic-type` —— 完美适配系统级字体缩放，确保文字放大时不会发生布局截断（参考 Apple Dynamic Type 与 Material Design）
- `reduced-motion` —— 适配 `prefers-reduced-motion` 属性，当用户开启减弱动画偏好时，自动简化或禁用非必要动效（参考 Apple Reduced Motion API，MD）
- `voiceover-sr` —— 提供具有明确现实意义的 `accessibilityLabel` 与 `accessibilityHint`，为屏幕阅读器 (VoiceOver) 规划合理的朗读顺序（参考 Apple HIG，MD）
- `escape-routes` —— 在弹窗模态框与多步骤流程中，始终提供清晰的“取消”、“返回”或关闭的物理出口（参考 Apple HIG）
- `keyboard-shortcuts` —— 保留系统默认和辅助技术专用的快捷键，为拖拽等复杂手势提供键盘替代操作（参考 Apple HIG）

### 2. 触控体验与交互响应 Touch & Interaction (CRITICAL)

- `touch-target-size` —— 触控目标尺寸最小为 44×44pt (Apple) / 48×48dp (Material)；必要时可通过负外边距或填充将触控热区扩展至视觉边界外
- `touch-spacing` —— 触控目标之间至少保持 8px/8dp 的物理间距，避免误触（参考 Apple HIG，MD）
- `hover-vs-tap` —— 将点击/触控作为第一交互现场；绝不能将关键操作仅绑定在悬停 (Hover) 状态上
- `loading-buttons` —— 在异步操作（如接口请求）执行期间禁用提交按钮，并展示加载中 (Spinner) 或进度状态
- `error-feedback` —— 在校验未通过的表单字段就近位置，显示清晰且具体的错误提示信息
- `cursor-pointer` —— 为 Web 端所有可交互及可点击元素显式声明 `cursor-pointer` 样式
- `gesture-conflicts` —— 避免在容易引发冲突的区域使用水平滑动操作，优先使用主流的垂直滚动
- `tap-delay` —— 使用 `touch-action: manipulation` 消除移动端 Web 浏览器中 300ms 的点击延迟
- `standard-gestures` —— 尊重并一致地使用系统标准手势，切勿重新定义其核心功能（如侧滑返回、双指捏合缩放）（参考 Apple HIG）
- `system-gestures` —— 绝不屏蔽或干扰系统的边缘划动手势（如调出控制中心、手势导航等）（参考 Apple HIG）
- `press-feedback` —— 在用户按压时提供即时的视觉反馈（如水波纹/涟漪效果或状态层变暗，参考 Material Design 状态层设计）
- `haptic-feedback` —— 在操作成功或遇到重要提示时提供精细的振动触觉反馈，但切忌泛滥（参考 Apple HIG）
- `gesture-alternative` —— 绝不依赖手势作为唯一触发手段，关键操作必须提供可见的常规控制按钮
- `safe-area-awareness` —— 主动适配刘海屏 (Notch)、动态岛 (Dynamic Island)、底部手势条等系统边界，将交互按钮放置在安全区域内 (Safe Area)
- `no-precision-required` —— 避免强迫用户在极窄的边缘或过小的像素点上进行高精度点击操作
- `swipe-clarity` —— 凡是支持滑动的操作，必须提供直观的视觉引导或暗示（如箭头、渐变虚化、新手引导）
- `drag-threshold` —— 在触发拖拽行为前设置合理的移动阈值，以避免因手抖或微小位移导致的误触发
- 
### 3. 性能与加载优化 Performance (HIGH)

- `image-optimization` —— 优先使用下一代图片格式 WebP/AVIF，配置响应式图片资源（`srcset`/`sizes`），并懒加载非首屏图片
- `image-dimension` —— 声明图片的宽/高或使用 `aspect-ratio` 属性占位，以避免图片加载时引起布局偏移（CLS 调优）
- `font-loading` —— 声明 `font-display: swap` 或 `optional`，防止因自定义字体未加载导致的正文闪烁或隐形 (FOIT / FOUT)
- `font-preload` —— 仅预加载最核心的字体变体，避免无节制地加载全量字重导致网络阻塞
- `critical-css` —— 抽取并内联首屏关键 CSS 样式，或确保核心样式表尽早加载
- `lazy-loading` - 通过动态导入 (Dynamic Imports) 或路由级分包，懒加载非首屏及较重组件
- `bundle-splitting` —— 实施代码分割 (Code Splitting)（如配合 React Suspense / Next.js dynamic），降低首次加载体积，提升可交互时间 (TTI)
- `third-party-scripts` —— 对第三方脚本应用 `async` 或 `defer` 异步加载，审计并果断移除无用脚本
- `reduce-reflows` —— 避免在同一个执行帧中频繁读取与写入 DOM 属性，合理合并 DOM 操作以减少浏览器重排
- `content-jumping` —— 为异步加载的内容提前保留高度或骨架占位，避免页面出现大范围布局跳动
- `lazy-load-below-fold` —— 对首屏折叠线以下的所有图片和媒体资源显式添加 `loading="lazy"` 属性
- `virtualize-lists` —— 针对长度超过 50 条的数据列表引入虚拟列表 (Virtual List) 机制，优化内存占用与滚动性能
- `main-thread-budget` —— 确保单帧计算量控制在 16ms 内以实现 60fps 流程度；将计算重任分流至主线程外（如 Web Workers）
- `progressive-loading` —— 对于耗时超过 1 秒的操作，使用带有微光动画的骨架屏 (Skeleton Screen) 替代无聊的加载菊花图 (Spinner)（参考 Apple HIG）
- `input-latency` —— 确保触控或滚动的输入响应延迟在 100ms 以内（参考 Material Design 响应度标准）
- `tap-feedback-speed` —— 在用户触碰屏幕后的 100ms 内，界面必须产生即时视觉反馈（参考 Apple HIG）
- `debounce-throttle` —— 对滚动、窗口重置大小、实时搜索等高频触发事件应用防抖 (Debounce) 或节流 (Throttle) 处理
- `offline-support` —— 提供友好的离线状态信息以及核心功能的离线缓存回退方案 (PWA/原生)
- `network-fallback` —— 针对慢速网络环境提供平滑降级模式（如加载低清图、精简复杂动效等）

### 4. 界面风格适配 Style Selection (HIGH)

- `style-match` —— 确保产品 UI 视觉风格与产品类别高度吻合（可运行 `--design-system` 指令获取匹配方案）
- `consistency` —— 确保产品的所有页面在主视觉风格、阴影、圆角和设计系统变量上保持全局一致
- `no-emoji-icons` —— 规范使用现代 SVG 图标（如 Heroicons, Lucide），绝不直接使用系统 Emoji 作为 UI 图标
- `color-palette-from-product` —— 依据产品定位与目标受众精选色板（可使用 `--domain color` 命令查询）
- `effects-match-style` —— 阴影、模糊、圆角和渐变等物理效果必须与整体风格紧密吻合（如 Glassmorphism 配毛玻璃、Brutalism 配粗描边粗阴影等）
- `platform-adaptive` —— 尊重平台的设计惯例（如 SwiftUI 遵循 Apple HIG，Android 遵循 Material Design 3）
- `state-clarity` —— 悬停 (Hover)、聚焦 (Focus)、按压 (Active) 与禁用 (Disabled) 状态必须在视觉上界定分明，同时不偏离整体风格（参考 Material 状态层）
- `elevation-consistent` —— 构建系统化的投影与层级阶梯，不要随机或凭感觉设定阴影属性
- `dark-mode-pairing` —— 同时设计亮/暗两套对比度合规的界面配色，并维持统一的品牌感知与视觉调性
- `icon-style-consistent` —— 在整个应用中规范使用同一种图标样式（粗细、圆角及描边风格），避免随机混用
- `system-controls` —— 优先使用系统原生控件，仅在品牌及定制化场景要求高时才进行高定包装（参考 Apple HIG）
- `blur-purpose` —— 仅在需要引导视觉重心、弱化底层元素时（如模态弹窗、底面板背景）使用模糊效果，切忌滥用为纯装饰（参考 Apple HIG）
- `primary-action` —— 单个屏幕内应有且仅有一个主 CTA 按钮，确保次要操作在视觉表现上处于清晰的从属地位（参考 Apple HIG）

### 5. 布局与多端响应式 Layout & Responsive (HIGH)

- `viewport-meta` —— 必须在 HTML 中声明 `<meta name="viewport" content="width=device-width, initial-scale=1">`（切勿限制用户缩放）
- `mobile-first` —— 坚持采用移动端优先 (Mobile-First) 设计思路，然后逐步向上适配平板和桌面端
- `breakpoint-consistency` —— 在整个项目中使用统一的断点体系（例如 `375px` / `768px` / `1024px` / `1440px`）
- `readable-font-size` —— 移动端正文字体最小设为 16px，以防 iOS 浏览器在聚焦输入框时进行强制放大
- `line-length-control` —— 移动端单行限制在 35–60 个字符，桌面端单行字数控制在 60–75 个字符，确保极佳的可读性
- `horizontal-scroll` —— 绝不允许在移动端出现横向滚动条，内容必须在视口内完成自适应与合理折行
- `spacing-scale` —— 采用科学的 4pt/8dp 阶梯级间距缩放规范（参考 Material Design）
- `touch-density` —— 可交互元素之间必须保留足够的物理间距，避免由于排版过于拥挤引起交互误触
- `container-width` —— 在大屏桌面端建立统一的最大容器宽度限制（如 `max-w-6xl` 或 `7xl`），使版面居中聚拢
- `z-index-management` —— 在全局建立统一、成体系的 `z-index` 层级系统（如 `0 / 10 / 20 / 40 / 100 / 1000`）
- `fixed-element-offset` —— 凡是使用固定定位 (`fixed`) 的导航栏或底部悬浮栏，必须为底层内容容器留足相等的安全边距
- `scroll-behavior` —— 尽量避免在页面中使用多重嵌套滚动区域，这会严重干扰和割裂系统主滚动体验
- `viewport-units` —— 在移动端推荐使用动态视口单位 `min-h-dvh` 代替不稳定的 `100vh`，防止视口高度被浏览器地址栏裁剪
- `orientation-support` —— 确保页面在横屏模式下也能维持清晰的视觉层级、合理的间距与完备的可操作性
- `content-priority` —— 移动端必须聚焦核心内容，在折叠面板或次级菜单中收纳次要信息
- `visual-hierarchy` —— 通过巧妙的字号大小、字重、间距与对比度强弱来构建清晰的信息阶梯，而不是只依赖色彩区分

### 6. 排版调性与语义化色彩 Typography & Color (MEDIUM)

- `line-height` —— 网页正文段落推荐使用 1.5 - 1.75 的行高，确保行间距呼吸感
- `line-length` —— 将正文单行长度限制在 65 - 75 个字符以内，以减缓阅读疲劳
- `font-pairing` —— 确保标题字体与正文字体在个性和调性上相辅相成，统一视觉风格
- `font-scale` —— 严格采用系统化的字号阶梯进行排版（如 12, 14, 16, 18, 24, 32, 48px）
- `contrast-readability` —— 选用高对比度的前背景文字色，在亮色背景下应避免使用过淡的灰色字（推荐使用类似 `slate-900` 的深灰色）
- `text-styles-system` —— 主动适配平台的排版预设体系（iOS 的 Dynamic Type 样式 / Material Design 的排版角色）（参考 HIG, MD）
- `weight-hierarchy` —— 利用字重建立明确的信息主次：粗体标题 (600–700)、常规体正文 (400)、中字重标签 (500)（参考 MD）
- `color-semantic` —— 定义规范的语义化颜色 Token（`primary`、`secondary`、`error`、`success`、`surface` 等），严禁在组件中大范围硬编码 `#hex` 颜色值
- `color-dark-mode` —— 暗色模式应使用经过低饱和度或明度微调的颜色变体，而非简单反转，并单独校验对比度（参考 HIG, MD）
- `color-accessible-pairs` —— 确保每一个前景与背景色搭配均符合 WCAG 的 4.5:1 (AA) 或 7:1 (AAA) 对比度合规标准
- `color-not-only-decorative` —— 传达状态的颜色（如表示错误的红色、表示成功的绿色）必须同时辅助图标或文本提示，避免让色弱群体漏掉关键信息
- `truncation-strategy` —— 换行排版优于截断。若必须截断，应辅以省略号，并通过悬停提示或展开按钮呈现完整内容（参考 Apple HIG）
- `letter-spacing` —— 尊重平台默认字距设定，绝不能在阅读性正文中使用过于紧密或松散的字距（参考 HIG, MD）
- `number-tabular` —— 在数据表格、财务金额、倒计时等经常变动的数字场景下，强制启用等宽数字（`tabular-nums`），防止数字变动时布局闪烁
- `whitespace-balance` —— 积极利用留白（白空间）对相关元素进行视觉归组；页面各模块之间应留有足够的呼吸空间

### 7. 动效与平滑过渡 Animation (MEDIUM)

- `duration-timing` —— 微交互的时长应控制在 150–300ms 之间，较复杂的全屏过渡动效不宜超过 400ms，避开 500ms 以上的拖沓动效
- `transform-performance` —— 动效必须高度关注渲染性能，只对 `transform` 和 `opacity` 应用动画，绝不针对 `width` / `height` / `top` / `left` 等极易引发生长和重排的属性做过渡
- `loading-states` —— 一旦网络请求或渲染耗时预期超过 300ms，必须展示骨架屏或进度条，不能让页面产生卡顿感
- `excessive-motion` —— 保持页面动效克制，单个视口内最多同时对 1-2 个关键元素应用动效，避免过度晃动干扰视线
- `easing` —— 坚持“快入缓出”原则：滑入等进入动画使用 `ease-out`，划出等退出动画使用 `ease-in`；禁止在 UI 过渡中使用生硬的 `linear` 线性过渡
- `motion-meaning` —— 每一个交互动效都应承载明确的设计意图（暗示物理空间关系、状态变更等），切忌为动而动（参考 Apple HIG）
- `state-transition` —— UI 元素的状态改变（如 hover、展开折叠、激活）必须声明平滑过渡，消灭突兀的瞬变
- `continuity` —— 页面或路由切换时，尽量保持空间连续性（如使用共享英雄元素、相同的平移方向等）（参考 Apple HIG）
- `parallax-subtle` —— 视差滚动必须保持极度克制，不仅要完美适配减弱动画设置，更不能对晕动症用户造成困扰（参考 Apple HIG）
- `spring-physics` —— 优先选用基于弹簧物理定律的动效曲线，而非生硬的代码贝塞尔曲线，使交互更具流体质感（参考 Apple HIG 流体动效）
- `exit-faster-than-enter` —— 退出动画快于进入：退出动画应比进入动画更迅速（建议设为进入时长的 60%–70%），使界面交互感觉更加干净利落（参考 MD 动效规范）
- `stagger-sequence` —— 交错动效序列 (Stagger)：将列表/网格项的入场动画进行 30–50ms 的交错延迟，避免生硬地一次性呈现或过慢地依次呈现（参考 MD）
- `shared-element-transition` —— 合理使用共享元素过渡 (Shared Element Transition)，在页面级跳转中维护视觉连续性（参考 MD, HIG）
- `interruptible` —— 动效可中断性：所有动画过渡必须可随时被打断，用户的点击或滑动手势应能立即响应并中止当前动画，决不能形成阻塞
- `no-blocking-animation` —— 绝不能在动画执行期间锁定用户输入，UI 交互层必须保持实时可触控、可交互状态（参考 Apple HIG）
- `fade-crossfade` —— 在同一个区域容器中进行内容替换时，使用交叉淡入淡出 (Crossfade) 进行过渡，防止生硬闪跳（参考 MD）
- `scale-feedback` —— 在点击按钮或可点击卡片时，提供轻微的按压缩放（0.95–1.05）反馈，释放时弹回，丰富交互层次（参考 HIG, MD）
- `gesture-feedback` —— 拖动、滑动和双指缩放操作必须实时跟随用户手指进行高帧率的动效渲染（参考 MD 动效规范）
- `hierarchy-motion` —— 用运动轨迹的方向来隐喻页面层级：由下往上滑入代表深入层级，往下滑出代表返回或关闭（参考 MD）
- `motion-consistency` - 在全局统一定义动画时长 Token 和缓动曲线，让整个系统的动效呼吸节奏保持和谐
- `opacity-threshold` —— 渐隐组件的透明度低于 0.2 时应迅速完全隐藏，不要在尾声拖泥带水
- `modal-motion` —— 模态弹窗或底面板应首选从其触发点（如点击的按钮）发起源头动画（滑入或轻微缩放），这有利于用户心智模型构建（参考 HIG, MD）
- `navigation-direction` —— 前进与后退的切换方向必须保持直觉一致：前进向左滑，后退向右退（参考 Apple HIG）
- `layout-shift-avoid` —— 所有常规动画均不能引发生长式布局重排，严防累积布局偏移 (CLS)

### 8. 表单设计与交互反馈 Forms & Feedback (MEDIUM)

- `input-labels` —— 所有输入控件都必须配备清晰可见的文本标签 (Label)，不要试图只用占位符 (Placeholder) 代替标签
- `error-placement` —— 校验报错提示信息必须紧密呈现在与之相关联的输入框下方或临近区域，避免让用户寻找
- `submit-feedback` —— 提交表单时必须将按钮切换至 Loading 状态并禁用，操作结束后给出明确的成功/失败反馈
- `required-indicators` —— 在必填表单项旁边醒目标注必填符号（如统一使用红色星号 *）
- `empty-states` —— 遇到空列表或空状态时，应呈现富有引导性的空状态页面（包含清晰文案说明 + 主行动按钮），严禁只展示白板
- `toast-dismiss` —— 轻提示 (Toast) 应具有 3–5 秒的自动消失机制，不打断用户操作
- `confirmation-dialogs` —— 执行破坏性操作（如删除、清空）前，必须弹出模态对话框让用户进行二次确认
- `input-helper-text` —— 针对格式复杂的表单，在输入框下方直接说明格式要求或提供帮助文案，不建议将其隐藏在 tooltip 中
- `disabled-states` —— 禁用状态的按钮或表单必须应用半透明淡化 (0.38–0.5)、鼠标禁用手势以及 HTML5 语义化 `disabled` 属性
- `progressive-disclosure` —— 循序渐进地展示复杂选项，避免在一开始塞给用户过多字段导致认知过载（参考 Apple HIG）
- `inline-validation` —— 优先在失去焦点 (`blur`) 时触发就近校验，而不是随用户敲击按键实时报错，防止造成焦虑情绪
- `input-type-keyboard` —— 为输入框声明准确的 HTML5 `type` 类型（如 `email`、`tel`、`number`），以便移动端能唤起最佳的键盘布局
- `password-toggle` —— 密码输入框必须提供显式/隐式的一键切换眼睛图标，供用户检查输入
- `autofill-support` —— 声明 `autocomplete` 或原生平台 `textContentType` 属性，方便用户利用系统凭据进行自动填充
- `undo-support` —— 针对删除或批量移动等破坏性行为，在 Toast 中提供限时撤销 (Undo) 操作，给予用户后悔药（参考 Apple HIG）
- `success-feedback` —— 关键任务完成后提供明确的反馈，如微动画打勾、通知 Toast 或高亮确认，强化完成感（参考 MD）
- `error-recovery` —— 错误报错信息必须给出一条可行性排查路径（重试、修改建议、在线支持链接），不能只报告错误而无法解决
- `multi-step-progress` —— 分步表单必须提供步骤条 (Step Indicator) 以展示进度，并绝对支持安全返回上一步
- `form-autosave` —— 较长的表单输入应在底层进行草稿自动保存，防止因断电、误触或浏览器崩溃导致用户数据彻底丢失
- `sheet-dismiss-confirm` —— 在用户关闭带有未保存更改的底面板或模态弹窗前，必须进行弹窗警告确认，严防误触丢失数据
- `error-clarity` —— 报错文案必须直观、易懂（写明错误原因和解决方法），禁止抛出“参数无效”、“500 Error”等代码级错误
- `field-grouping` —— 逻辑关联的输入项应在视觉或语义上分组合并（使用 `fieldset`、容器或留白区划）（参考 MD）
- `read-only-distinction` —— 只读状态 (Read-Only) 的数据应在视觉上与禁用状态 (Disabled) 进行区分，只读应保持良好的文字对比度
- `focus-management` —— 表单校验失败提交时，自动将焦点移动至第一个未通过校验的输入框中，并唤起键盘（参考 WCAG）
- `error-summary` —— 长表单如果有多处报错，应在表单顶部进行红框汇总提示，并提供链接至报错位置的锚点导航（参考 WCAG）
- `touch-friendly-input` —— 移动端输入框的物理高度不应低于 44px，以确保优良的触控交互体验（参考 Apple HIG）
- `destructive-emphasis` —— 破坏性操作（如删除、注销）应使用明确的警示红，且在空间排列上与主 CTA 保持距离（参考 HIG, MD）
- `toast-accessibility` —— Toast 提示严禁抢夺用户的焦点，在 Web 中声明 `aria-live="polite"` 以供屏幕阅读器播报（参考 WCAG）
- `aria-live-errors` —— 表单报错区域使用 `aria-live="assertive"` 或 `role="alert"`，确保视障用户能实时听到错误播报（参考 WCAG）
- `contrast-feedback` —— 表单成功或错误状态提示的颜色对比度也必须严格满足 4.5:1 的无障碍要求（参考 WCAG, MD）
- `timeout-feedback` —— 一旦网络请求超时，必须展示清晰的超时提示，并配备一键重试机制（参考 MD）

### 9. 导航设计与层级模式 Navigation Patterns (HIGH)

- `bottom-nav-limit` —— 底部导航栏 Tab 数量限制在 3-5 个；且必须同时采用“图标+文字标签”的设计，只放图标非常不易用
- `drawer-usage` —— 侧边栏/抽屉导航仅用于收纳次要或低频的导航项，切勿把主流程操作塞入侧栏
- `back-behavior` —— 返回行为必须符合直觉并保持全局连贯，且务必保留先前页面的滚动高度与未提交的表单状态
- `deep-linking` —— 确保核心功能页面均配有唯一的 URL 路径，支持直接通过深层链接 (Deep Link) 进行分享或跳转
- `tab-bar-ios` —— iOS 原生设计：必须将全局一级分类放在屏幕底部的 Tab Bar 中，符合单手持机操作习惯（参考 Apple HIG）
- `top-app-bar-android` —— Android 原生设计：使用顶部应用栏 (Top App Bar) 放置页面标题、返回键与动作入口（参考 Material Design）
- `nav-label-icon` —— 导航入口不能仅设计纯图标，文字标签对减少认知障碍极其关键
- `nav-state-active` —— 处于激活状态的导航项必须有极高辨识度的高亮设计（如主色高亮、字重加粗、动态底划线）
- `nav-hierarchy` —— 严格划分主级导航（底栏/主栏）与次级/辅助级导航（页内标签/设置面板）的视觉权重
- `modal-escape` —— 每一个模态弹窗或底面板都必须有显眼的“关闭”或“取消”键，在移动端还需支持手势下滑关闭（参考 Apple HIG）
- `search-accessible` —— 搜索框应处于极易触达的常驻区（如顶栏或首个 Tab 中）；并提供搜索历史、热门推荐词等辅助录入
- `breadcrumb-web` —— Web 端：当信息层级深度超过 3 级时，必须配置面包屑导航 (Breadcrumbs)，指引用户所在位置
- `state-preservation` —— 点击返回时，页面必须高还原度恢复先前的滚动位置、侧栏筛选条件与已输入的文字（参考 HIG, MD）
- `gesture-nav-support` —— 主动适配系统的滑动手势导航（如 iOS 侧滑返回、Android 边缘预测性返回），避免产生手势拦截冲突
- `tab-badge` —— 谨慎在导航 Tab 上应用徽标红点 (Badge) 进行强打扰，一旦用户点击该模块，红点应立即消除（参考 HIG, MD）
- `overflow-menu` —— 如果操作按钮超出容器宽度，收纳至“更多”溢出菜单中，切勿把按钮挤爆到换行
- `bottom-nav-top-level` —— 底部导航栏仅用于放置应用最顶层的 3-5 个核心入口，决不能在底部导航栏内嵌套次级页面底栏
- `adaptive-navigation` —— 响应式导航：宽屏大屏设备上（≥1024px）优先选用侧边栏或左侧导航轨，移动端则切换至底栏/顶栏
- `back-stack-integrity` —— 确保应用的导航栈完整度，返回操作必须循序渐进，绝不能直接把用户的导航历史清空并丢回首页
- `navigation-consistency` —— 导航栏的设计和位置在所有页面中应保持一致，不能随着页面切换而在顶部、底部、侧边随机变化
- `avoid-mixed-patterns` —— 避免在同一层级混乱地混合使用顶部 Tabs、侧边抽屉与底部 Tab Bar
- `modal-vs-navigation` —— 模态框 (Modal) 绝不能用作主线导航流程；它们的设计初衷是临时打断用户以处理独立事务
- `focus-on-route-change` —— 路由页面切换后，将焦点移至主要容器标题上，使屏幕阅读器能第一时间为盲人播报新页面（参考 WCAG）
- `persistent-nav` —— 关键导航入口在深度页面中依然需要可触及，不要在子任务中将其彻底隐藏或锁死
- `destructive-nav-separation` —— 带有危险性的入口（如注销、删除组织、注销账号）必须在空间上与日常导航大距离隔开
- `empty-nav-state` —— 如果某个导航项由于无权限或无数据暂时无法访问，应显示具体的权限说明或引导流程，不能默默隐藏

### 10. 图表设计与数据可视化 Charts & Data (LOW)

- `chart-type` —— 图表类型与数据结构必须高度契合：时间趋势推荐折线图/面积图，横向对比选用柱状图，占比推荐环形图/饼图
- `color-guidance` —— 必须选择对色盲用户友好的配色方案，绝不能仅通过红、绿两色对比来表达涨跌或数据盈亏
- `data-table` —— 所有的图表页面，均必须提供表格 (Table) 版本的替代呈现，这对屏幕阅读器用户是刚需
- `pattern-texture` —— 对图表使用不同的线条样式（实线、虚线）、纹理填充或形状标记，确保即使没有颜色信息也能轻松阅读
- `legend-visible` —— 图表必须配备直观易读的图例说明，且图例必须紧靠图表主体放置，严禁将其放在首屏线以下
- `tooltip-on-interact` —— 必须支持点击（移动端）或悬停（Web 端）时弹出包含确切数据值的浮窗 (Tooltip)
- `axis-labels` —— 坐标轴标签必须配有明确的物理单位与人性化的刻度划分，移动端避免使用倾斜 45 度或被截断的文字
- `responsive-chart` —— 图表必须具备完整的响应式能力，在小屏设备上可自动精简坐标轴刻度或将柱状图转换为水平条形图
- `empty-data-state` —— 当图表无数据可显示时，必须展示易懂的空状态界面并提供引导（如“暂无数据”+“去创建”），严禁丢出一个空白的坐标轴
- `loading-chart` —— 数据加载中时，使用图表专用的骨架图或微光动画占位，不要给用户展示坏掉的布局
- `animation-optional` —— 数据图表入场动画必须适配减弱动效偏好，确保急需数据的用户能立即获取信息
- `large-dataset` —— 面对 1000+ 的海量数据点时，后台或前端需进行抽样/聚合，并提供下钻 (Drill-Down) 入口，不能直接丢给渲染引擎
- `number-formatting` —— 坐标轴及数值标签上的所有数字、日期、金融金额，均必须进行本地化格式化处理（如 `¥12,500.00`）
- `touch-target-chart` —— 交互式图表元素（如散点图的圆点、饼图扇区）触控热区至少保持 44pt，或在用户手指接近时自动吸附高亮
- `no-pie-overuse` —— 类别超过 5 个时禁止使用饼图或环形图，因为极难阅读对比；应果断切换为水平条形图
- `contrast-data` —— 数据线条/图形块与图表背景的对比度需 ≥3:1，图表内嵌的数据文本标签与背景对比度需 ≥4.5:1
- `legend-interactive` —— 数据系列的图例应设计为可交互式点击，允许用户通过勾选图例来过滤和显示/隐藏对应的数据系列
- `direct-labeling` —— 当数据系列较少时，直接将数值标签标在折线或柱条上，减少用户在图表与图例之间来回移动视线的疲劳
- `tooltip-keyboard` —— 交互图表的浮窗 (Tooltip) 数据必须支持键盘 Focus 唤起，不能让键盘用户摸黑
- `sortable-table` —— 提供替代方案的表格数据必须支持列排序，并使用 `aria-sort` 语义化标签声明当前排序状态
- `axis-readability` —— 坐标轴刻度布局不能过于拥挤；在小屏下必须根据屏幕宽度自动跳过部分刻度，确保不重叠
- `data-density` —— 严格限制单个图表的信息密度以避免认知超载；必要时应合理拆分为多个子图表进行对比
- `trend-emphasis` —— 可视化的核心是凸显数据本身的客观趋势，切忌使用过重的卡片投影或喧宾夺主的背景渐变
- `gridline-subtle` —— 坐标轴辅助网格线必须保持极低的视觉权重（如使用非常淡的 `gray-100` 或 `gray-200`），严防抢夺视线
- `focusable-elements` —— 所有的交互式图表数据点、柱条、扇区，均必须支持键盘焦点 Focus 状态，以兼容辅助技术
- `screen-reader-summary` —— 在图表容器上声明 `aria-label`，用一两句话为视障用户精炼总结当前图表的核心结论或数据趋势
- `error-state-chart` —— 图表请求失败时，必须在图表区域内展示明确的报错提示及“重新加载”按钮，禁止页面崩溃或空白
- `export-option` —— 针对数据敏感的报表系统，提供将图表所含源数据导出为 CSV/Excel 或下载图表为图片/PDF 的快捷操作
- `drill-down-consistency` —— 图表的深度钻取必须提供清晰的面包屑导航，并保障用户能随时安全返回上一层级
- `time-scale-clarity` —— 涉及时间维度的图表，必须在显眼位置标明当前的时间粒度（如日/周/月/季），并提供快速切换 Tab

## 使用说明 (How to Use)

请使用下方提供的 CLI 命令行工具，来检索特定的设计领域规则。

## 开发前提条件 (Prerequisites)

检查开发环境是否已安装 Python 3.x：

```bash
python3 --version || python --version
```

如果未安装 Python，请根据您的操作系统执行相应命令安装：

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3
```

**Windows:**
```powershell
winget install Python.Python.3.12
```

---

## 使用指南 (How to Use)

在以下业务开发场景中，可直接调用此技能：

| 场景 (Scenario) | 触发示例 (Trigger Examples) | 推荐起点 (Start From) |
|----------|-----------------|------------|
| **全新项目 / 页面开发** | "做一个 landing page"、"Build a dashboard" | 步骤 1 → 步骤 2（生成设计系统） |
| **新组件设计与还原** | "Create a pricing card"、"Add a modal" | 步骤 3（专项检索：style, ux） |
| **风格定义 / 调性设计 / 字体配对** | "What style fits a fintech app?"、"推荐配色" | 步骤 2（生成设计系统） |
| **UI 走查与无障碍审查** | "Review this page for UX issues"、"检查无障碍" | 上方的快速参考指南 (Quick Reference) |
| **UI 还原度缺陷及交互异常修复** | "Button hover is broken"、"Layout shifts on load" | 快速参考指南 → 匹配章节调优 |
| **体验升级与性能优化** | "Make this faster"、"Improve mobile experience" | 步骤 3（专项检索：ux, react） |
| **适配暗黑模式** | "Add dark mode support" | 步骤 3（专项检索：style "dark mode"） |
| **引入图表与数据可视化** | "Add an analytics dashboard chart" | 步骤 3（专项检索：chart） |
| **特定技术栈的最佳开发实践** | "React performance tips" | 步骤 4（框架指令检索） |

请遵循以下标准开发流：

### 步骤 1：深入分析用户需求

从用户请求中精准提取以下决策因子：
- **产品定位/类型**：娱乐社交（社交、视频、音乐、游戏）、生产力工具（扫描仪、编辑器、转换器）、效率协作（任务管理、笔记、日历）或复合型平台
- **目标受众画像**：C 端消费者用户；考虑年龄段、使用场景（通勤、闲暇、工作）
- **风格关键词**：活泼趣味 (playful)、动感活力 (vibrant)、极致极简 (minimal)、暗黑 OLED (dark mode)、内容优先 (content-first)、沉浸式 (immersive) 等
- **框架技术栈**：确认当前项目所采用的框架与技术栈

### 步骤 2：生成设计系统规范（核心前置步骤，必须执行）

**请务必首先执行 `--design-system` 命令**，以获取包含严密推理逻辑的完整设计系统方案：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

底层执行逻辑：
1. **多维度并行检索**：并行检索产品定位 (product)、UI 风格 (style)、色彩搭配 (color)、布局模式 (landing) 以及字体排版 (typography) 数据库
2. **智能规则推理**：基于 `ui-reasoning.csv` 决策模型，智能匹配并输出最佳方案
3. **输出标准化设计系统**：提供版式布局、视觉风格、色板、字体调性及动效交互说明
4. **输出反模式避坑清单**：列出当前行业需规避的交互/视觉雷区

**示例：**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### 步骤 2b：持久化设计系统（全局主配置 + 页面覆盖模式）

若需保存生成的配置以支持跨会话的**层级上下文检索**，请追加 `--persist` 参数：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

这将在项目根目录下自动创建：
- `design-system/MASTER.md` —— 全局唯一事实来源 (Single Source of Truth，包含全局通用规范)
- `design-system/pages/` —— 存放特定页面覆盖规则的文件夹

**生成特定页面覆盖规则示例：**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"
```

这还会额外创建：
- `design-system/pages/dashboard.md` —— 仅针对仪表盘页面的局部覆盖规范（只声明偏离 Master 的差异部分）

**层级上下文检索机制：**
1. AI 在构建特定页面（如 Checkout）时，会首先检索 `design-system/pages/checkout.md` 是否存在
2. 如果该页面配置文件存在，其局部规则将**覆盖 (override)** 全局 `MASTER.md` 的设定
3. 若不存在特定页面配置文件，则默认以 `design-system/MASTER.md` 为全局唯一依据

**上下文感知检索提示词模板 (Context-Aware Prompt)：**
```
I am building the [Page Name] page. Please read design-system/MASTER.md.
Also check if design-system/pages/[page-name].md exists.
If the page file exists, prioritize its rules.
If not, use the Master rules exclusively.
Now, generate the code...
```

### 步骤 3：补充性细节检索（按需执行）

在设计系统大框架下，若需针对特定交互细节进行微调，可运行以下命令检索：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**补充检索场景：**

| 需求 | 检索领域 (Domain) | 示例 (Example) |
|------|--------|---------|
| 产品原型与排版模式 | `product` | `--domain product "entertainment social"` |
| 视觉风格深度检索 | `style` | `--domain style "glassmorphism dark"` |
| 配色/色板精选 | `color` | `--domain color "entertainment vibrant"` |
| 字体组合/字体配对 | `typography` | `--domain typography "playful modern"` |
| 图表展现与库推荐 | `chart` | `--domain chart "real-time dashboard"` |
| UX 交互与无障碍合规 | `ux` | `--domain ux "animation accessibility"` |
| 落地页布局与 CTA 策略 | `landing` | `--domain landing "hero social-proof"` |
| 开发框架性能调优 | `react` | `--domain react "rerender memo list"` |
| 平台交互规范 (iOS/Android) | `web` | `--domain web "accessibilityLabel touch safe-areas"` |
| AI 提示词与核心变量 | `prompt` | `--domain prompt "minimalism"` |

### 步骤 4：特定技术栈规范适配

检索针对特定框架底层实现的高质量代码模板与性能建议：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack <stack>
```

---

## 快捷检索参考表

### 检索领域 (Domains)

| 领域 (Domain) | 用途 | 示例关键词 |
|--------|---------|------------------|
| `product` | 产品类型模式推荐建议 | SaaS, e-commerce, portfolio, healthcare, beauty, service |
| `style` | UI 设计风格、颜色、特效特征 | glassmorphism, minimalism, dark mode, brutalism |
| `typography` | 经典字体搭配、Google Fonts 导入推荐 | elegant, playful, professional, modern |
| `color` | 匹配行业受众的产品色板推荐 | saas, ecommerce, healthcare, beauty, fintech, service |
| `landing` | 落地页页面结构与 CTA 转化策略 | hero, hero-centric, testimonial, pricing, social-proof |
| `chart` | 推荐的数据图表类型与可视化图表库 | trend, comparison, timeline, funnel, pie |
| `ux` | 交互设计优秀实践与反模式防坑指南 | animation, accessibility, z-index, loading |
| `react` | React 生态框架的前端渲染性能调优 | waterfall, bundle, suspense, memo, rerender, cache |
| `web` | 主流端平台设计与无障碍接口规范 | accessibilityLabel, touch targets, safe areas, Dynamic Type |
| `prompt` | 生成特定风格视觉的 AI 绘图提示词 | (style name) |

---

## 标准工作流实战演练

**用户请求**："帮我设计一个 AI 搜索首页"

### 步骤 1：分析需求
- 产品定位：工具类（AI 智能搜索终端）
- 目标受众：追求极致效率、即用即走的 C 端用户
- 风格关键词：前沿、极简、内容优先、暗色模式
- 技术栈：根据项目配置或默认使用 HTML + Tailwind

### 步骤 2：生成设计系统规范（核心前置步骤，必须执行）

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "AI search tool modern minimal" --design-system -p "AI Search"
```

**输出**：获得一份量身定制的设计系统方案，包含推荐布局、视觉风格特征、语义配色、字体排版、核心交互动效以及避坑指南。

### 步骤 3：补充性细节检索（按需执行）

```bash
# 检索极简与纯黑 OLED 模式的设计规范细节
python3 skills/ui-ux-pro-max/scripts/search.py "minimalism dark mode" --domain style

# 检索关于搜索过渡和加载状态的 UX 优秀动效实践
python3 skills/ui-ux-pro-max/scripts/search.py "search loading animation" --domain ux
```

### 步骤 4：特定开发框架的规范检索

```bash
# 检索特定技术栈下的输入性能与列表渲染最佳实践
python3 skills/ui-ux-pro-max/scripts/search.py "input performance" --stack react
```

**最后阶段**：将设计系统规范与检索出的最佳交互细节融会贯通，产出高质量前端代码。

---

## 输出格式 (Output Formats)

`--design-system` 命令行标志支持以下两种输出格式：

```bash
# ASCII 艺术框（默认）- 最适合终端显示与命令行直观阅读
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown 格式 - 格式更规整，最适合保存为文档记录或传给 AI 上下文
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown
```

---

## 高阶开发与提问技巧

### 提问与检索策略

- **使用多维度复合关键词** —— 结合“产品类别 + 垂直行业 + 视觉基调 + 信息密度”进行检索，例如：`"entertainment social vibrant content-dense"`，而不是随意地检索一个 `"app"`
- **横向测试相似关键词** —— `"playful neon"` → `"vibrant dark"` → `"content-first minimal"`
- **采用漏斗式分析** —— 首先运行 `--design-system` 构建底层规范，随后用 `--domain` 深入研究有疑问的局部维度
- **明确绑定技术栈** —— 检索时追加 `--stack <stack_name>`，以获取针对该框架最优雅的组件封装与渲染逻辑

### 常见设计/交互痛点排查与方案

| 问题 | 解决方案 |
|---------|------------|
| **视觉失焦（风格或配色拿捏不准）** | 尝试微调检索关键词重新运行 `--design-system` 进行设计推演 |
| **暗黑模式文本对比度不合规** | 参阅快速参考指南第 1 节：`color-dark-mode` + `color-accessible-pairs` 优化明度 |
| **动画与交互手感生硬** | 参阅快速参考指南第 7 节：`spring-physics` + `easing` + `exit-faster-than-enter` 曲线 |
| **表单填报交互繁琐、报错不友好** | 参阅快速参考指南第 8 节：`inline-validation` + `error-clarity` + `focus-management` 重构 |
| **导航路径混乱、返回状态丢失** | 参阅快速参考指南第 9 节：`nav-hierarchy` + `bottom-nav-limit` + `back-behavior` 保留现场 |
| **移动端小屏布局拥挤或溢出** | 参阅快速参考指南第 5 节：`mobile-first` + `breakpoint-consistency` 优雅折行 |
| **列表滚动掉帧或交互响应迟钝** | 参阅快速参考指南第 3 节：`virtualize-lists` + `main-thread-budget` + `debounce-throttle` 优化 |

### 上线前 UX 质量走查清单 (Pre-delivery Checklist)

- 在具体实现前，建议检索 `--domain ux "animation accessibility z-index loading"` 作为防错预走查
- 交付前，务必严格核对快速参考指南的 **§1–§3** 章节（CRITICAL & HIGH 级别），这是产品可用性的底线
- 至少在 375px（移动端黄金分辨率）和横屏设备下进行界面极限测试
- 开启系统 **减弱动画 (reduced-motion)** 以及 **系统字体最大字号 (Dynamic Type)**，验证布局是否错乱或被截断
- 亮/暗色模式下的前背景色对比度必须使用专业对比度工具双向校验，不要凭主观推测
- 交互按钮的物理热区面积至少达 44pt，且操作入口在系统级边缘（如状态栏/手势条）绝无重合或干扰

---

## 高质量 UI 开发通用铁律

以下是极易被忽略、但会导致界面显得极其廉价和不专业的细节硬伤：

### 图标与视觉资产规范

- 默认图标库使用 **Phosphor (`@phosphor-icons/react`)**。`src/ui-ux-pro-max/data/icons.csv` 中列出的只是常用推荐图标，不是完整集合。
- 当推荐表中找不到合适的图标时：
  - **优先继续从 Phosphor 的完整图标集中选择任何语义更贴切的图标**；
  - 如果 Phosphor 也没有理想选项，可以使用 **Heroicons (`@heroicons/react`)** 作为备选，注意保持风格一致（线性/填充、笔画粗细、圆角风格）。

| 规范准则 (Rule) | 优秀实践 (Do) | 应规避的反模式 (Avoid) | 核心设计考量 (Why It Matters) |
|------|----------|--------|----------------|
| **禁止将 Emoji 用于结构化图标** | 统一使用高阶矢量图标（如 Phosphor、Heroicons 或平台专有矢量图标库）。 | 在侧边栏导航、设置表单或重要交互控件中胡乱堆叠 Emoji（如 🎨 🚀 ⚙️）。 | Emoji 极其依赖客户端系统预装字库，渲染效果千差万别且无法被设计 Token 所控制。 |
| **纯矢量化资产原则** | 全量使用可无限缩放、完美兼容主题切换的 SVG 图标或平台级矢量 XML 格式。 | 使用 PNG、JPG 等拉伸时会产生锯齿、模糊且无法变色的位图图标。 | 确保在高分视网膜屏幕下的极致清晰度，以及无缝切换亮/暗主题的能力。 |
| **按压状态过渡稳定性** | 点击/按压态仅使用颜色深浅、不透明度 (Opacity) 或投影高度 (Elevation) 的过渡，绝对不改变组件本身的边框物理大小。 | 在按压或悬停时，使用会改变物理宽高、导致周围元素被挤压或抖动的形变 (Layout Shift)。 | 避免造成交互过程中的页面视觉抖动，保障移动端交互的极其平滑，提升感知质量。 |
| **品牌资产规范使用** | 统一使用官方矢量品牌资产，严格遵循其标志安全边界与配色指南。 | 主观臆断或手动绘制 Logo、未经授权随意为品牌图标重新配色或强行拉伸比例。 | 确保品牌呈现的严肃与规范，防范法务纠纷及合规性风险。 |
| **图标尺寸系统化** | 将图标高度与宽度抽象并定义为统一的设计 Token（如 `icon-sm`、`icon-md`=24px、`icon-lg`）。 | 在同一界面中随意混用 18px、21px、25px、29px 等混乱的任意像素尺寸。 | 维持产品设计系统的整体韵律感，建立严谨的视觉阶梯。 |
| **图标描边线宽一致性** | 在同一个视觉信息层级内，所有图标必须采用相同的线宽描边（如统一使用 1.5px 或 2px）。 | 随意拼凑不同线宽、粗细交织的图标集合。 | 描边粗细不一会严重割裂页面的精致度，降低产品的整体品质感。 |
| **图标填充/线性风格纯净度** | 在同一视觉层级或同一组功能区（如底部 Tab 栏）内，必须统一使用同一种图标风格（要么全部线性，要么全部填充）。 | 在同一功能区域内，随性混用填充型与线性图标（如首页是线性，搜索页是填充）。 | 维护图标系统的整体调性与视觉规律性。 |
| **触控热区最小面积限制** | 确保可交互按钮物理热区面积至少达 44×44pt；如果图标视觉过小，必须使用负外边距或 hitSlop 属性扩大实际热区。 | 使用直接暴露的小图标而未做任何热区扩展，导致用户反复点击失败。 | 保障不同手部尺寸用户在运动、颠簸场景下的触碰成功率，满足 A11y 规范。 |
| **图标文字基线精准对齐** | 图标必须与同级排版的文本基线（Baseline）或中心线严格对齐，并保持统一的水平外边距。 | 图标高度偏高或偏低，产生杂乱无章的视错觉。 | 细微的视觉失衡是摧毁高级感的主要元凶，必须做到像素级严谨对齐。 |
| **图形对比度无障碍审查** | 遵循 WCAG 对比度底线：常规功能图标对比度 ≥4.5:1，大型图形化装饰性符号对比度 ≥3:1。 | 采用过淡的灰色图标，导致在阳光直射下完全看不清。 | 确保在各种极端照度和不同设备屏幕上的卓越可读性。 |

### 主流端交互规范原则

| 规范法则 (Rule) | 正面实践 (Do) | 反面模式 (Don't) |
|------|----|----- |
| **即时触控反馈 (Tap feedback)** | 必须在触控后的 80–150ms 内给出明确的涟漪、明度微调或透明度过渡等响应 | 点击后界面如一潭死水，无任何视觉或动效响应 |
| **动效时间把控 (Animation timing)** | 微交互时长限定在 150–300ms 左右，且必须配置符合物理特性的非线性曲线 | 动效瞬间硬切 (0ms) 或采用超过 500ms 的沉重拖沓动画 |
| **朗读焦点顺序 (Accessibility focus)** | 确保屏幕阅读器 (Screen Reader) 的焦点流向与页面视觉布局顺序绝对匹配 | 焦点焦点随意跳动或将无关的装饰元素朗读给视障用户 |
| **禁用态状态表达** | 应用淡化透明度、鼠标禁用标识，并通过 `disabled` 属性禁止一切点击触发 | 按钮看起来依然可用但点击后无任何反应，使用户困惑是否发生卡顿 |
| **扩大最小交互区域** | 确保移动端触控目标热区宽与高均 ≥44pt，对微小图标通过属性扩充交互热区 | 使用过小的像素点，逼迫用户像做外科手术一样精准点击 |
| **规避多重手势冲突** | 每一个物理区域仅设计一种主流手势操作，防止嵌套滚动或边缘划动手势拦截系统手势 | 在支持滑动的卡片组件内，强行嵌入横向滚动的次级数据列表 |
| **无障碍语义声明** | 规范使用原生交互控件（如 Button、Pressable），配置准确的 accessibility role 角色 | 随意使用普通的无语义容器（如 Div、View）来包裹关键交互入口 |

### 亮/暗色模式对比度调优

| 规范法则 (Rule) | 正面实践 (Do) | 反面模式 (Don't) |
|------|----|----- |
| **卡片/卡板层级感 (Surface readability)** | 善用投影高度、高光边框或微弱明度差将卡片面板与底层背景界定分明 | 卡片完全融入背景，导致页面沦为平铺直叙的一张白板 |
| **浅色模式文本易读性** | 确保浅色主题下的正文段落与背景的对比度 ≥4.5:1 | 在白底上使用过淡的浅灰色文字，伤害视力 |
| **暗黑模式文本易读性** | 确保深色主题下主要文本对比度 ≥4.5:1，次要说明文字对比度 ≥3:1 | 暗色主题下的文本对比度不足，导致文字几乎隐形 |
| **边框与分割线辨识度** | 确保分割线和细边框在浅色与暗色主题下均有匹配的明暗度对比 | 只针对默认主题调优，在暗黑模式下边框彻底消失 |
| **交互状态双向适配** | 针对亮/暗两套主题，均设计高水准的 hover、focus、disabled 及 active 交互态 | 仅针对其中一个主题优化了状态，导致另一主题下交互态难以辨认 |
| **Token 化色彩管理** | 在文字、背景和边框上全量引入语义化色彩 Token，实现主题一键切换 | 在组件样式中大量写死 Hex 颜色，使得主题适配维护成本巨大 |
| **半透明遮罩对比调优** | 模态弹窗的底层 Scrim 半透明度应设在 40%–60% 之间，以提供充足的前景聚焦力 | 遮罩过淡导致底层内容与弹窗文本发生视觉打架，严重干扰阅读 |

### 布局与间距节奏规范

| 规范法则 (Rule) | 正面实践 (Do) | 反面模式 (Don't) |
|------|----|----- |
| **安全区域对齐 (Safe-area)** | 针对页眉、底栏及全局悬浮 CTA 栏，强制注入顶部与底部安全区域 padding | 悬浮底栏把刘海屏或系统底部手势条死死挡住，阻断操作 |
| **避开系统交互热区** | 为系统状态栏和导航指示条预留充足的高度避让，严防手势冲突 | 让可交互的按钮与系统自带的手势滑轨边缘重叠，触发误触 |
| **统一多端限制宽度** | 依据设备屏幕尺寸，采用预设的最大安全内容容器宽度（如大屏 PC 限制在 1200px 左右） | 页面布局在宽屏下无限延伸扩展，导致视觉重心涣散 |
| **4/8pt 间距韵律系统** | 内边距、外边距、网格空隙等，一律采用统一的 4/8/16/24/32/48px 等阶梯节奏 | 随心所欲使用 7px、13px、19px、31px 等无规律的间距数值 |
| **控制段落最大排版宽度** | 在宽屏平板及 PC 上，限制单行文字最大排版宽度，保证视线移动舒适 | 段落文字横跨整屏，导致用户每读完一行都需要长距离移动眼球寻找下一行 |
| **垂直间距分明层级** | 页面各区块之间使用鲜明的、拉开差距的垂直间距（如 24px/48px/64px） | 区块区块之间没有清晰的空隙，使页面显得局促而杂乱 |
| **响应式水平槽宽** | 随着设备屏幕宽度增加，按比例增加两侧的水平页面边距 (Page Gutters) | 在平板和移动端上都顽固使用相同极窄的 12px 边距 |
| **底部滚动安全占位** | 凡是页面底部有固定粘性底栏时，必须为列表容器最底端提供相等的 Padding 占位 | 用户滑动到列表最底部时，最后一个条目被粘性底栏永久遮挡 |