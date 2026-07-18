---
name: component-testing
description: 组件库测试用例编写指南。当被要求为组件加测试用例、调试测试失败、补响应式/SSR/视觉断言、理解项目测试约定、判断某个维度应该放哪个文件测、或讨论 vitest browser mode / vitest-browser-vue / 测试方法论时应用。涵盖：静态契约、动态契约、视觉 wiring、响应式断点、SSR 水合、暴露方法、插槽、子配置等维度。
metadata:
  version: '1.0.0'
---

# 组件库测试用例编写指南

> **触发场景：** 为新组件搭测试 / 给现有组件加用例 / 调试测试失败 / 视觉契约断言怎么写 / 响应式断点怎么测 / SSR 兼容性怎么验 / 测试文件应该拆几个 / vitest 报错排查 / 跨 wrapper strict mode 冲突 / 暴露方法怎么测 / 插槽怎么测 / 子配置（如 column/option/item）怎么测

## 框架速览

| 层          | 选型                                                                                                                           |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 运行器      | Vitest 4.x（`pnpm test:run` / `pnpm test:ui`）                                                                                 |
| 浏览器      | **Playwright Chromium 真浏览器**（不是 jsdom/happy-dom）                                                                       |
| 渲染        | `vitest-browser-vue` 的 `render()`                                                                                             |
| SSR         | `@vue/server-renderer` 在浏览器里 `renderToString`                                                                             |
| 配置        | [`packages/opendesign/vitest.config.ts`](../../opendesign/vitest.config.ts)                                                    |
| 启动副作用  | [`packages/opendesign/__tests__/setup.ts`](../../opendesign/__tests__/setup.ts) 加载 `dist/index.css` + e.light + e.dark token |
| 共享 helper | [`packages/opendesign/__tests__/_helpers/`](../../opendesign/__tests__/_helpers/) 内含 viewport + ssr + theme + dom            |

**测试 co-located**：每个组件 `src/<comp>/__tests__/` 下放 3 个固定文件。

---

## 共享 helper 索引

所有 helper 位于 [`packages/opendesign/__tests__/_helpers/`](../../opendesign/__tests__/_helpers/)，测试文件通过相对路径导入（如 `import { THEMES } from '../../../__tests__/_helpers/theme'`）。

| 文件                                                             | 导出                                                  | 用途                                                                                                               |
| ---------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| [`viewport.ts`](../../opendesign/__tests__/_helpers/viewport.ts) | `BREAKPOINTS`、`setViewport`、`BreakpointName`        | 5 个断点视口切换，用于 `*.responsive.test.ts`                                                                      |
| [`ssr.ts`](../../opendesign/__tests__/_helpers/ssr.ts)           | `renderSSR`、`ssrThenHydrate`、`spyHydrationErrors`   | SSR 字符串渲染 + hydration 测试，用于 `*.ssr.test.ts`                                                              |
| [`theme.ts`](../../opendesign/__tests__/_helpers/theme.ts)       | `THEMES`、`ThemeName`、`paintThemed`、`isTransparent` | 双主题常量 + 主题挂载 + 透明色判断，用于 `*.index.test.ts` 视觉断言                                                |
| [`dom.ts`](../../opendesign/__tests__/_helpers/dom.ts)           | `flush`、`resolveTokenPx`                             | 异步渲染等待 + CSS 变量 px 值解析，用于 `*.index.test.ts`（exposed 方法）和 `*.responsive.test.ts`（token 链断言） |

---

## 工作流（写测试的标准动作）

```
1. 看组件结构 → src/<comp>/{OComp.vue, types.ts, style/}
2. 按 types.ts prop 顺序，定 *.index.test.ts 静态契约用例数
3. 看 media.scss 决定 *.responsive.test.ts 跑哪些视口
4. SSR 兼容性照搬模板（*.ssr.test.ts）
5. pnpm vitest run src/<comp>/__tests__/   ← 跑通
```

**不允许跳过步骤 1**：测试用例必须按 prop 而非"想到什么测什么"组织，参见 [three-file-structure](./references/three-file-structure.md)。

---

## 三个测试文件职责

| 文件                   | 测什么                                                                                                                                                  | 不测什么                    | 详细                                                            |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- | --------------------------------------------------------------- |
| `*.index.test.ts`      | **5 维度 describe**：静态契约（DOM/class/默认值/单主题视觉语义） + 动态契约（emit/键盘/阻断） + 视觉契约（双主题 token wiring） + 子配置契约 + 插槽契约 | 像素值、响应式断点尺寸、SSR | [three-file-structure.md](./references/three-file-structure.md) |
| `*.responsive.test.ts` | 视口 × size 的尺寸数值（字面 px 精确比对 / token 链变量变化断言 / 级联一致性）                                                                          | 颜色、行为                  | [three-file-structure.md](./references/three-file-structure.md) |
| `*.ssr.test.ts`        | renderToString 不抛 + hydration mismatch（用 `test.fails` 标记已知问题）                                                                                | 视觉、布局                  | [three-file-structure.md](./references/three-file-structure.md) |

---

## 视觉断言策略（关键）

**不硬编码 RGB**。token 调一下就大面积维护。改用 **CSS 变量 wiring 断言**：

```ts
// ❌ 易碎：token 改一下就挂
expect(cs.borderTopColor).toBe('rgb(0, 47, 167)');

// ✅ 稳定：4 态 token 必须互不相同（保证用户能视觉区分状态）
const tokens = new Set([
  cs.getPropertyValue('--btn-color').trim(),
  cs.getPropertyValue('--btn-color-hover').trim(),
  cs.getPropertyValue('--btn-color-active').trim(),
  cs.getPropertyValue('--btn-color-disabled').trim(),
]);
expect(tokens.size).toBe(4);
```

完整断言策略 + variant 承载属性表 + brand 例外 → [visual-contract.md](./references/visual-contract.md)。

### 双主题双跑（关键约定）

**所有读 token / 颜色的 wiring 断言必须在 light + dark 两个主题下都跑**。`data-o-theme` 挂在 wrapper container 上（不是 documentElement），同时给 container 一个 fill1 主题背景，让 UI 面板视觉反差明显：

```ts
import { THEMES, paintThemed } from '../../../__tests__/_helpers/theme';

for (const theme of THEMES) {
  test(`OComp <场景> @${theme} - ...`, async () => {
    const screen = render(OComp, { props: {...} });
    const el = screen.container.querySelector('.o-<comp>') as HTMLElement;
    paintThemed(screen.container, theme, el);
    // 断言不变，token 解析值随主题变
  });
}
```

### 跨主题对比（条件性）

**当两主题确实对该属性使用不同色值时**，可补一条跨主题对比用例：证明 light 和 dark 的实际解析值不同。但**不是所有组件都需要**——如果主题设计对该 token 在 light 和 dark 下使用相同色值（如 OButton 的 primary 系），则不做 light≠dark 断言，token 对应什么色值就是什么色值。

```ts
// 适用于两主题不同色的属性（如 ODataTable header bg）
for (const theme of THEMES) {
  test(`OComp variant=solid @${theme} - bg-color 解析为非透明色`, async () => {
    const screen = render(OComp, { props: { color: 'primary', variant: 'solid' } });
    const el = screen.container.querySelector('.o-<comp>') as HTMLElement;
    paintThemed(screen.container, theme, el);
    expect(isTransparent(getComputedStyle(el).backgroundColor)).toBe(false);
  });
}

test('OComp variant=solid color=primary - light / dark 下 backgroundColor 解析值不同', async () => {
  const lightScreen = render(OComp, { props: { color: 'primary', variant: 'solid' } });
  const darkScreen = render(OComp, { props: { color: 'primary', variant: 'solid' } });
  const elL = lightScreen.container.querySelector('.o-<comp>') as HTMLElement;
  const elD = darkScreen.container.querySelector('.o-<comp>') as HTMLElement;
  paintThemed(lightScreen.container, 'e.light', elL);
  paintThemed(darkScreen.container, 'e.dark', elD);
  expect(getComputedStyle(elL).backgroundColor).not.toBe(getComputedStyle(elD).backgroundColor);
});
```

哪些测试需要双主题、哪些不用 + 完整说明 → [visual-contract.md「双主题」段](./references/visual-contract.md#双主题light--dark双跑)。

---

## 异步渲染等待（flush）

组件使用 `OScroller`、`useElementBounding`、`ResizeObserver` 等异步机制时，需要等待 RAF 稳定后再断言：

```ts
import { flush } from '../../../__tests__/_helpers/dom';

test('ODataTable exposed - selectAll / clearAll 更新 selectedKeys', async () => {
  const tableRef = ref<any>(null);
  const screen = render({
    setup() {
      return () => h(ODataTable as any, { ref: tableRef, data, columns, selection: true });
    },
  });
  await flush(); // ← 必须
  tableRef.value.selectAll();
  await flush(); // ← 每次 DOM 改变后再 flush
  // 断言...
});
```

**何时需要 flush**：

- 组件内部有 `requestAnimationFrame` / `setTimeout` 延迟渲染
- 使用 `OScroller` / `OPopup` 等异步定位组件
- 调用 exposed 方法后 DOM 发生变化

---

## 暴露方法测试

组件通过 `defineExpose` 暴露方法时，用 `ref` 获取组件实例并调用：

```ts
test('ODataTable exposed - selectAll / clearAll 更新 selectedKeys', async () => {
  const tableRef = ref<any>(null);
  const screen = render({
    setup() {
      return () => h(ODataTable as any, { ref: tableRef, data, columns, selection: true });
    },
  });
  await flush();
  expect(tableRef.value).toBeTruthy();

  tableRef.value.selectAll();
  await flush();
  const checked = screen.container.querySelectorAll('tbody .o-table-row-checkbox input:checked');
  expect(checked.length).toBe(data.length);

  tableRef.value.clearAll();
  await flush();
  const checkedAfter = screen.container.querySelectorAll('tbody .o-table-row-checkbox input:checked');
  expect(checkedAfter.length).toBe(0);
});

test('ODataTable exposed - dataColumns / dataColumnMap / groupColumns 暴露正确长度', async () => {
  const tableRef = ref<any>(null);
  render({
    setup() {
      return () => h(ODataTable as any, { ref: tableRef, data, columns });
    },
  });
  await flush();
  expect(tableRef.value.dataColumns.length).toBe(3);
  expect(tableRef.value.dataColumnMap.size).toBeGreaterThanOrEqual(3);
});
```

---

## 响应式视口

5 个断点已封装在 [`__tests__/_helpers/viewport.ts`](../../opendesign/__tests__/_helpers/viewport.ts)，按"适配规则一致"分三大类：

| 视口    | width | 区间      | 类  |
| ------- | ----- | --------- | --- |
| desktop | 1920  | >1680     | 1   |
| laptop  | 1440  | 1201-1680 | 2   |
| pad_h   | 1100  | 841-1200  | 2   |
| pad_v   | 768   | 601-840   | 3   |
| phone   | 375   | 360-600   | 3   |

**用法**：

```ts
import { BREAKPOINTS, setViewport } from '../../../__tests__/_helpers/viewport';

await setViewport('desktop');
```

**跑哪些视口由组件的 `media.scss` 决定**：写了几个 `@include respond(...)` 块就跑哪几个视口（外加 `desktop` 作基准）。不强求 5 个全跑。

### 响应式数值断言策略

| 变量类型         | 断言策略                         | 说明                                                        |
| ---------------- | -------------------------------- | ----------------------------------------------------------- |
| **字面 px 变量** | 矩阵精确比对 `toBeCloseTo(n, 0)` | var.scss / media.scss 直接写 `8px` / `12px` / `16px` 的变量 |
| **token 链变量** | 只断言「跃迁前后值发生变化」     | 值是 `var(--o-*)` 指向 token，最终 px 由主题决定            |
| **级联区间**     | 断言「级联自上游断点值」         | 无专属 media 覆盖的区间                                     |

**字面 px 断言示例**（OButton）：

```ts
for (const bp of Object.keys(EXPECTED) as (keyof typeof EXPECTED)[]) {
  for (const size of ['large', 'medium', 'small'] as SizeKey[]) {
    const exp = EXPECTED[bp][size];
    test(`OButton size=${size} @${bp} - 字号${exp.fontSize}/icon${exp.iconSize}/gap${exp.iconGap}/padX${exp.padX}/高${exp.height}`, async () => {
      await setViewport(bp);
      const screen = render(OButton, { props: { size, icon: OIconAdd }, slots: { default: size } });
      const btn = screen.container.querySelector('.o-btn') as HTMLElement;
      const m = measure(btn);
      expect(m.fontSize).toBeCloseTo(exp.fontSize, 0);
      expect(m.iconSize).toBeCloseTo(exp.iconSize, 0);
      // ...
    });
  }
}
```

**token 链变量断言示例**（ODataTable）：

```ts
import { resolveTokenPx } from '../../../__tests__/_helpers/dom';

// 不硬比对绝对 px。仅在该 size 实际声明覆盖的 respond 块端点验证「跃迁前后值变了」。
test('ODataTable medium - --table-text-size 在 desktop → laptop → pad_v 各跃迁端点值变化', async () => {
  const d = resolveTokenPx(await renderAt('desktop', 'medium'), '--table-text-size');
  const l = resolveTokenPx(await renderAt('laptop', 'medium'), '--table-text-size');
  const pv = resolveTokenPx(await renderAt('pad_v', 'medium'), '--table-text-size');
  expect(d).not.toBe(l); // text1 → tip1
  expect(l).not.toBe(pv); // tip1 → tip2
});
```

**级联一致性断言示例**：

```ts
// pad_v / phone 段 small 未声明专属覆盖，应级联自 pad_h
test('ODataTable small @phone - 无专属覆盖，所有变量值级联自 pad_h', async () => {
  const root = await renderAt('phone', 'small');
  assertMetrics(root, SMALL_STOPS.pad_h); // 与 pad_h 值相同
});
```

完整示例 → [OButton.responsive.test.ts](../../opendesign/src/button/__tests__/OButton.responsive.test.ts) / [ODataTable.responsive.test.ts](../../opendesign/src/data-table/__tests__/ODataTable.responsive.test.ts)。

---

## 命名规范

**格式：`<OComp> <prop / 场景> - <中文描述>`**

| 场景            | 模板                                                                                          |
| --------------- | --------------------------------------------------------------------------------------------- |
| 单 prop（枚举） | `<OComp> <prop> - 各枚举值注入 o-<comp>-{prop} 类`                                            |
| 默认值          | `<OComp> <prop> - 未显式时取默认值 <值>`                                                      |
| 事件            | `<OComp> click - 用户点击时 emit click(MouseEvent)`                                           |
| 状态阻断        | `<OComp> disabled - 用户操作时阻止 emit <事件>`                                               |
| 响应式          | `<OComp> <prop>=<值> @<断点> - <尺寸表现>`                                                    |
| SSR             | `<OComp> SSR <prop>=<值> - <HTML 输出特征>`                                                   |
| 水合            | `<OComp> hydration <prop>=<值> - 无 hydration mismatch 警告`                                  |
| Wiring 矩阵     | `<OComp> <state> wiring @${theme} - N color × M variant 矩阵下 <state> 系 token 与 base 不同` |
| 双主题          | `<OComp> <场景> @${theme} - <断言摘要>`                                                       |
| 跨主题对比      | `<OComp> <prop> - light / dark 下 <token> 解析值不同`                                         |
| **暴露方法**    | `<OComp> exposed - <方法名> <效果>`                                                           |
| **子配置**      | `<OComp> <配置类型>.<字段> - <表现>`（如 column.fixed / option.disabled / item.label）        |
| **插槽**        | `<OComp> slot=<name> - <效果>`                                                                |
| **已知问题**    | 用 `test.fails` 标记，命名同普通用例                                                          |

**禁用**：纯英文描述、`P1`/`P2` 前缀。

### 已知问题标记

组件实现有 bug 但暂不修复时，用 `test.fails` 标记，锁定当前行为：

```ts
// 已知问题：loading=true 时 SSR 与客户端首帧不一致
// 标记为预期失败，待组件侧修复后改回普通断言。归类 L2（组件实现 bug）。
test.fails('ODataTable hydration loading=true - 无 hydration mismatch 警告', async () => {
  const spy = spyHydrationErrors();
  mountedRoot = await ssrThenHydrate(ODataTable, { data: [], columns, loading: true });
  expect(spy.hasHydrationMismatch()).toBe(false);
  spy.restore();
});

// 插槽未实现：types.ts 定义了但模板未渲染
test.fails('ODataTable slot=td_${key} - 替换指定列每一行的单元格内容', async () => {
  // ...
});
```

---

## describe 分组（统一 5 维度范式）

所有组件统一按以下维度拆分 describe，**按组件实际有的维度取**，没有的维度不写空 describe：

| #   | describe 名称                      | 测什么                                     | 适用条件                 |
| --- | ---------------------------------- | ------------------------------------------ | ------------------------ |
| 1   | 静态契约（按 types.ts 属性）       | DOM / class / 默认值 / 单主题视觉语义      | 所有组件必有             |
| 2   | 动态契约（用户交互 → 组件响应）    | emit / 键盘 / disabled 阻断 / exposed 方法 | 有交互的组件（T2+）      |
| 3   | 视觉契约（双主题 light / dark）    | 所有 THEMES 循环的 token wiring 断言       | 有颜色/状态 token 的组件 |
| 4   | 子配置契约（按 <ConfigType> 字段） | column.fixed / option.disabled 等          | 有子配置类型的复杂组件   |
| 5   | 插槽契约（具名插槽）               | slot=default / slot=icon / slot=header 等  | 有具名插槽的组件         |

### 简单组件（如 OButton）：4 个 describe

```ts
describe('静态契约（按 types.ts 属性）', () => {
  /* 每个 prop 一条 — DOM/class/默认值/单主题视觉语义（variant 背景/边框等） */
});
describe('动态契约（用户交互 → 组件响应）', () => {
  /* emit + disabled/loading 阻断 + 键盘 — 不含 THEMES 循环 */
});
describe('视觉契约（双主题 light / dark）', () => {
  /* 每个「视觉承载点」拆为两条用例：
     ① for-theme 循环：证明在 light 和 dark 下 token 都解析为合理值
     ② 跨主题对比：证明 light 和 dark 的实际解析值不同
     承载点示例：
     - solid bg-color：非透明 + light≠dark
     - outline bd-color：可见边框 + light≠dark
     - 4态 token 互不相同（6 color × 2 theme）
     - disabled 文字色切换 + light≠dark
     - hover/active wiring 矩阵（6 color × 3 variant × 2 theme）
     - 状态层级（outline 4态 border-color 两两不同 × 2 theme） */
});
describe('插槽契约（具名插槽）', () => {
  /* slot=default / slot=icon / slot=suffix */
});
```

### 复杂组件（如 ODataTable）：5 个 describe

```ts
describe('静态契约（按 types.ts 属性）', () => {
  /* 每个 prop 一条 */
});
describe('动态契约（用户交互 → 组件响应）', () => {
  /* emit + exposed 方法 */
});
describe('视觉契约（双主题 light / dark）', () => {
  /* 每个「视觉承载点」拆为两条用例：
     ① for-theme 循环：证明在 light 和 dark 下 token 都解析为合理值
     ② 跨主题对比：证明 light 和 dark 的实际解析值不同
     承载点示例：
     - headerStyle=fill：thead bg 非透明 + light≠dark
     - border=all：cell border 可见 + light≠dark
     - stripe：偶数行 gradient + light≠dark
     - loading：旋转动画运行 */
});
describe('子配置契约（按 <配置类型> 字段）', () => {
  /* 如 DataTableColumnT 的 fixed/width/formatter 等 */
});
describe('插槽契约（具名插槽）', () => {
  /* slot=header / slot=th_${key} / slot=empty 等 */
});
```

### 维度归位原则

**视觉契约（双主题）块从静态/动态契约中抽离**：所有 `for (const theme of THEMES)` 循环的断言统一放入「视觉契约」块，静态/动态契约中不出现 THEMES 循环。理由：

1. 静态契约只验 DOM/class/默认值/单主题视觉语义（不含双主题 token wiring）
2. 动态契约只验 emit/行为拦截（不含 hover/active wiring 矩阵）
3. 视觉契约集中管理所有双主题断言，便于主题升级时批量维护

**判断标准**：测试里有 `paintThemed()` 或 `for (const theme of THEMES)` → 归入视觉契约块；只有 `classList.contains` / `getAttribute` / `tagName` / 数值 → 留在静态/动态契约。

**原则**：describe 名称要清楚表达测试维度，不要用"功能测试"、"视觉测试"等模糊命名。

---

## 组件档位（参考用）

按 [`packages/opendesign/CLAUDE.md`](../../opendesign/CLAUDE.md) 的"实现范式"归档，**仅供判断"哪些交互必测"**，不再设最低用例数（数量由 prop 数量自然决定）：

| 档位                      | 特征                              | 关键交互（动态契约必覆盖）                          |
| ------------------------- | --------------------------------- | --------------------------------------------------- |
| **T1** 展示型             | 纯渲染、无 emit、无状态           | 无                                                  |
| **T2** 交互基础           | 有 click/hover 但无状态机         | click + 键盘（Enter/Space）                         |
| **T3** 表单控件（范式 A） | 接入 `useFormField`、有 v-model   | v-model 双向 + clear + formItem 上下文校验触发      |
| **T4** 组合（范式 B）     | Group ↔ Item 通过 provide/inject | 子项触发 group emit、独立使用降级                   |
| **T5** 浮层（范式 C）     | 基于 `OPopup` 派生                | open/close 状态 + outside-click + `ClientOnly` 包裹 |
| **T6** 反馈类             | 命令式 API、异步触发              | 命令式调用 + close 回调 + 多实例 z-index            |
| **T7** 数据展示           | 大数据列表 / 表格 / 树            | 排序/筛选/选中 + 虚拟滚动事件                       |

---

## 新组件接入步骤

以新组件 `OComp` 为例：

1. **定档**：看 `src/<comp>/` 实现对照上表 T1~T7（仅用于判断动态契约必覆盖哪些交互）
2. **建目录**：`src/<comp>/__tests__/`
3. **从已有组件复制骨架**：
   ```bash
   cp -r src/<已有 component>/__tests__ src/<comp>/__tests__
   # 重命名文件并替换内部组件名
   ```
4. **打开 `src/<comp>/types.ts`**，按 prop 顺序一条一条写静态契约用例：
   - 每个 prop 一条 `test()`
   - 一条内集中断言该 prop 的所有视觉表现（class、tag 切换、内部节点、CSS 变量等）
   - 默认值的表现也作为该条用例的一个断言
5. **加动态契约用例**：参照档位关键交互列表
6. **`responsive.test.ts` 视口按 `media.scss` 实际断点定**，不强求 5 个全跑
7. **跑通**：
   ```bash
   pnpm vitest run src/<comp>/__tests__
   ```

---

## 踩坑速查

| 现象                                                                        | 真因 / 解决                                                                                                                                      | 详细                                                  |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------- |
| 同一 test 多次 `render()` 后 `getByText/getByRole` 报 strict mode violation | Playwright Locator 在 body 范围搜，命中 ≥2 元素就 fail。改用 `wrapper.container.querySelector('.o-<comp>')` 从各自根节点取                       | [pitfalls.md](./references/pitfalls.md)               |
| `pnpm test:ui` 面板里 hover 测试红色，CLI 跑过                              | 用户鼠标实际位置可能已悬在 button 上，`before === after === hover 色`。改用 **token wiring 断言** 替代真实事件触发                               | [pitfalls.md](./references/pitfalls.md)               |
| hover 后立刻读 `borderColor` 拿到旧值                                       | `transition: all` 让读取时机不稳定。测试前 `el.style.transition = 'none'`；更稳直接断言 token wiring                                             | [visual-contract.md](./references/visual-contract.md) |
| `:active` 怎么也触发不到                                                    | `userEvent` 无 `pointer/mouse.down` API；`dispatchEvent('mousedown')` 不触发 `:active` 伪类。改用 **active wiring 断言**                         | [visual-contract.md](./references/visual-contract.md) |
| icon prop 传组件时 Vue warn "reactive object"                               | `icon = markRaw(IconComp)` 包一下                                                                                                                | [pitfalls.md](./references/pitfalls.md)               |
| 空 `<svg>` 把按钮撑到 ~300px 宽                                             | SVG 无 width/height 时浏览器默认 300×150。用真实 icon 组件（`OIconAdd` 等）                                                                      | [pitfalls.md](./references/pitfalls.md)               |
| `style.borderRadius` 是空字符串                                             | `round` prop 把值写入 `--<comp>-radius` CSS 变量。断言 `style.getPropertyValue('--<comp>-radius')` 或 `getComputedStyle(el).borderTopLeftRadius` | [pitfalls.md](./references/pitfalls.md)               |
| disabled prop 在 DOM 上找不到 `disabled` 属性                               | opendesign 的 disabled 只用 class + 内部 preventDefault，不透传原生属性。断言 class 而非 attribute                                               | [pitfalls.md](./references/pitfalls.md)               |
| Browser Mode 下样式全没 / Token 报错                                        | `dist/index.css` 缺失。先跑 `pnpm build:style`                                                                                                   | [pitfalls.md](./references/pitfalls.md)               |
| **调用 exposed 方法后断言失败**                                             | DOM 更新需要 RAF。调用后 `await flush()` 再断言                                                                                                  | 见上文「异步渲染等待」                                |
| **OScroller / OPopup 相关组件渲染不稳定**                                   | 异步定位需要 RAF。初始渲染后 `await flush()` 再断言                                                                                              | 见上文「异步渲染等待」                                |
| **token 链变量跨断点值相同（如 radius）**                                   | 当前主题别名指向同 px。跳过该跃迁断言，待主题区分后再补                                                                                          | 见上文「响应式数值断言策略」                          |
| **插槽测试 fail 但 types.ts 有定义**                                        | 模板未实际渲染该 slot。用 `test.fails` 标记，待组件侧补实现                                                                                      | 见上文「已知问题标记」                                |

---

## 命令

```bash
cd packages/opendesign

pnpm test            # watch 模式
pnpm test:run        # 单次运行
pnpm test:ui         # Vitest UI 面板
pnpm test:cov        # 覆盖率

# 单文件
pnpm vitest run --config vitest.config.ts src/<comp>/__tests__/OComp.index.test.ts

# 单用例按名过滤
pnpm test:run -- -t "用例名片段"
```

**首次跑额外步骤**：

```bash
pnpm install
pnpm exec playwright install chromium
pnpm -C packages/opendesign build:style    # 产出 dist/index.css
```

---

## 测试 import 策略

测试直接 import 组件源码，不走构建产物：

```ts
import OComponent from '../OComponent.vue';
```

**好处**：改组件源码立刻能跑测试，不需要先 build。

**代价**：丢掉"测发布产物"的回归信号。如果担心构建产物与源码不一致，可以在 CI 加一次构建产物导出一致性测试。

---

## 覆盖率

### 计算原理

底层等价于 `vitest run --coverage --config vitest.config.ts`，使用 **V8 provider**。V8 在运行测试时，通过 JavaScript 引擎内置的代码执行追踪机制，记录每条语句/分支/函数/行是否被执行过，最终输出「已执行 / 总数」的比值即覆盖率百分比。不同于 Istanbul 的 instrumentation（源码注入探针），V8 provider 无需改写源码，直接利用引擎原生计数，零侵入且与 Browser Mode 真浏览器执行一致。

### 覆盖范围

**计入覆盖率的文件**（`coverage.include`，配置在 [`vitest.config.ts`](../../opendesign/vitest.config.ts)）：

```
src/**/*.{ts,vue}
```

即所有组件源码（`.vue` SFC + `.ts` 逻辑/类型/composable）。

**不计入覆盖率的文件**（`coverage.exclude`）及排除理由：

| 掄除项                   | 理由                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------ |
| `src/**/__tests__/**`    | 测试文件本身不是被测对象，纳入会虚增覆盖率                                           |
| `src/**/__docs__/**`     | 文档交互式 Demo，不是组件运行时逻辑                                                  |
| `src/**/__demo__/**`     | 文档站展示 Demo，同上                                                                |
| `src/**/*.d.ts`          | 纯 TypeScript 类型声明，无运行时代码可执行                                           |
| `src/_virtual/**`        | 自动生成的虚拟入口（统一导出），非手写业务逻辑                                       |
| `src/icon-components/**` | SVG 批量生成的图标组件，数量大但逻辑单一（仅渲染 SVG），不计入可避免覆盖率被图标稀释 |

### 测了什么

覆盖率衡量的是**源码在测试中的执行情况**，对应 3 个测试文件各自覆盖的维度：

| 测试文件               | 覆盖的源码维度                                                                                                                                  | 对覆盖率指标的贡献                                                                             |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `*.index.test.ts`      | 静态契约（按 `types.ts` 每个 prop → DOM 结构 / class 注入 / 默认值 / token wiring）+ 动态契约（用户交互 → emit / disabled 阻断 / exposed 方法） | 覆盖 `<script setup>` 的大部分语句/分支/函数，是 `% Stmts` / `% Branch` / `% Funcs` 的主要来源 |
| `*.responsive.test.ts` | 视口 × size 的尺寸数值（字面 px 精确比对 / token 链跃迁断言）                                                                                   | 覆盖 `media.scss` 对应的响应式条件分支，补充 `% Branch`                                        |
| `*.ssr.test.ts`        | `renderToString` 不抛 + hydration mismatch                                                                                                      | 覆盖 SSR 路径（`<script setup>` 在服务端渲染的执行路径），补充 `% Stmts` / `% Branch`          |

**未被覆盖率反映的维度**（测试验证了但覆盖率数字看不到）→ 见 [框架边界 §10](#10-覆盖率不反映的维度)。

### 覆盖率指标含义

| 指标                | 含义                                | 对组件库的意义                                                        |
| ------------------- | ----------------------------------- | --------------------------------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------ |
| `% Stmts`           | 语句覆盖率：被执行过的语句 / 总语句 | 反映有多少代码行被测试触发执行                                        |
| `% Branch`          | 分支覆盖率：`if`/`else`/三元/`&&`/` |                                                                       | ` 各分支的命中情况 | 反映条件逻辑（如 `if (disabled)` / `if (size === 'large')`）是否被测试覆盖到各个分支 |
| `% Funcs`           | 函数覆盖率：被调用过的函数 / 总函数 | 反映 `defineExpose` 暴露的方法、composable 返回的函数等是否被测试调用 |
| `% Lines`           | 行覆盖率：被执行过的行 / 总行       | 与 `% Stmts` 类似，但以行为单位，更直观对应编辑器行号                 |
| `Uncovered Line #s` | 未被覆盖的行号区间（如 `2-138`）    | 直接定位哪些代码从未被测试触发，是补测试的第一线索                    |

### 产出物

运行 `pnpm test:cov` 后会额外生成 `packages/opendesign/coverage/` 目录（已加入 `.gitignore`），并在终端打印一份文本汇总表。

| 文件/目录                     | 用途                                                                           |
| ----------------------------- | ------------------------------------------------------------------------------ |
| `index.html`                  | HTML 报告入口，浏览器打开可逐文件钻取，未覆盖代码行红色高亮                    |
| `lcov-report/`                | HTML 报告的资源/分文件页面                                                     |
| `lcov.info`                   | 机器可读格式，给 CI（Codecov/Coveralls）或 VSCode 插件（Coverage Gutters）消费 |
| `base.css` / `*.js` / `*.png` | HTML 报告的样式与脚本                                                          |

### 查看方式

1. **VSCode 控制台**：`pnpm test:cov` 运行结束后，终端直接输出汇总表（向上滚动查看）
2. **VSCode 行内显示（推荐）**：装 _Coverage Gutters_ 插件 → 命令面板 `Coverage Gutters: Display Coverage`，读 `coverage/lcov.info` 在编辑器侧边栏显示红/绿条，定位未覆盖行最直观
3. **HTML 报告**：浏览器打开 `packages/opendesign/coverage/index.html`，点击文件名钻取，红色高亮即未覆盖行

---

## CI 集成

CI 配置尚未落地。建议步骤：

1. `pnpm install`
2. `pnpm exec playwright install --with-deps chromium`
3. `pnpm -C packages/opendesign build:style`（产出 `dist/index.css`）
4. `pnpm -C packages/opendesign test:run --browser.headless=true`
5. （可选）`pnpm -C packages/opendesign test:cov` + 上传 `lcov.info` 到 Codecov / Coveralls

---

## 框架边界：本框架不支持的测试类型

本框架定位是**单组件契约 + 视觉 wiring 兜底**。以下测试类型因技术限制或职责划分，不属于本框架的覆盖范围，需要用其他工具/项目补充。

### 1. 像素级视觉回归（截图 diff）

**为什么不支持**：本框架的视觉断言是 CSS 变量 wiring（token 字面值比对 + 4 态互不相同），验证的是「视觉状态可区分」而非「渲染结果与设计稿像素一致」。截图 diff 需要截图 → 逐像素比对 → 差异阈值判定，这个流程与 Vitest Browser Mode 的 DOM 断言模型不兼容。

**替代方案**：Playwright screenshot comparison 或第三方视觉回归平台（Percy / Chromatic / Applitools），在独立 E2E 项目中执行。

### 2. 跨浏览器兼容性（Firefox / WebKit）

**为什么不支持**：`vitest.config.ts` 仅配置 `instances: [{ browser: 'chromium' }]`。Vitest Browser Mode 当前不支持多浏览器并行跑组件测试（Playwright 多浏览器需要 playwright-ct 或独立 E2E 项目）。

**替代方案**：Playwright 多浏览器 E2E 测试（`playwright test --project=firefox --project=webkit`），在独立仓库或 Skill-Test 项目中执行。

### 3. 真实伪类触发后的像素级断言（`:hover` / `:active` / `:focus-visible`）

**为什么不支持**：

| 伪类             | 限制                                                                                                                                                                                                                          |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `:hover`         | vitest-browser UI 模式下用户鼠标位置不可控——可能已悬在目标元素上，`before === after === hover 色`。CLI 模式过但 UI 模式挂，同一段代码行为不一致                                                                               |
| `:active`        | vitest-browser 的 `userEvent` 没有 `pointer/mouse.down` API（按住不释放语义）；`dispatchEvent('mousedown')` 不触发 `:active` 伪类（伪类由浏览器内部管理）；键盘 `{Space}` 仅在 focus 时短暂触发，读 computed style 时机不稳定 |
| `:focus-visible` | 可以用 `userEvent.tab()` 触发，但断言时机不稳定（focus ring 的出现/消失涉及浏览器内部状态机）                                                                                                                                 |

**本框架的替代策略**：用 **token wiring 断言**替代真实伪类触发——断言 `--btn-color-hover` / `--btn-color-active` 的字面值与 `--btn-color` 不同，证明「视觉状态链路已 wire 上」，由设计稿保证 token 解析后的 RGB 正确。像素级的真实切换效果由 E2E 截图回归兜底。

### 4. 页面级集成 / 多组件联动流程

**为什么不支持**：本框架每个 test 只 mount **单个组件**，验证的是该组件自身的契约。多个组件联动（如「填写表单 → 点击提交按钮 → 弹出确认对话框 → 验证结果」）需要页面级上下文，超出单组件测试的职责边界。

**替代方案**：业务方 E2E（Cypress / Playwright test），或文档站 `packages/docs` 的集成测试。

### 5. 动画流畅度 / FPS / 性能指标

**为什么不支持**：本框架可以断言 `animationName !== 'none'`（动画在跑）和 `animationDuration`（时长），但无法验证动画是否流畅（无卡顿）或 FPS 是否达标。性能指标需要在真实负载下长时间采集，与单次 mount + 立即断言的测试模式不匹配。

**替代方案**：Chrome DevTools Performance 面板手动测试，或 Lighthouse / WebPageTest 自动化性能评测。

### 6. 无障碍（a11y）自动化审计

**为什么不支持**：Vitest Browser Mode 没有 axe-core 等无障碍审计工具集成。浏览器环境虽然有 accessibility tree，但 vitest-browser 不提供 `page.accessibility` API（这是 Playwright test 级别的功能，不在 vitest-browser 的 Locator 模型内）。

**替代方案**：Playwright 的 `page.accessibility.snapshot()` + axe-core Playwright 插件，在 E2E 项目中执行。手动测试时用浏览器 a11y 扩展（axe DevTools）。

**本框架已覆盖的 a11y 相关维度**：

- `disabled` 阻断 emit（行为层面的无障碍保障）
- 键盘 Enter / Space 触发 click（键盘可操作）
- tag / href 渲染正确（语义标签）

**已知的 a11y 遗留问题**（不在本框架修复范围）：opendesign 的 `disabled` 仅注入 class + 内部 `preventDefault`，**不透传 HTML 原生 `disabled` 属性**。这意味着 screen reader 无法读出 disabled 状态，键盘 Tab 仍能聚焦。这是 L1 级问题，待组件侧修复后测试也要同步改。

### 7. 触摸事件 / 移动端手势

**为什么不支持**：Vitest Browser Mode 的 Playwright 实例是桌面 Chromium，`userEvent` 只有 click / hover / keyboard / tab，没有 touch / swipe / pinch 等手势 API。即使设置小视口（phone 375px），交互仍是鼠标模拟而非真实触摸。

**替代方案**：Playwright 的 `page.touch()` API（需 Playwright test 模式，不在 vitest-browser 内），或真设备测试（Appium / BrowserStack）。

### 8. 键盘导航完整性（Tab 顺序 / focus trap）

**为什么不支持**：本框架可以验证单个组件内的键盘交互（Enter / Space 触发 click），但无法验证完整的 Tab 顺序——Tab 顺序取决于页面级 DOM 结构和所有可聚焦元素的排列，超出了单组件 mount 的边界。focus trap（如 Modal 内 Tab 不逃出）也需要页面级上下文。

**替代方案**：Playwright test 的 `page.keyboard.press('Tab')` 序列 + `page.accessibility` 检查，在 E2E 项目中执行。

### 9. SEO / meta 标签 / OG 属性

**为什么不支持**：SSR 测试用 `renderToString` 渲染单个组件，产出的是组件片段 HTML，不是完整页面。meta 标签、OG 属性、`<head>` 内容需要在完整页面（Nuxt / Next）上下文中验证。

**替代方案**：文档站 `packages/docs`（Nuxt）的集成测试 + `vue-meta` 验证。

### 10. 覆盖率不反映的维度

以下维度**测试已验证**但**V8 覆盖率数字无法体现**——详细说明见 [覆盖率 → 测了什么](#测了什么)：

| 维度            | 说明                                                                                           |
| --------------- | ---------------------------------------------------------------------------------------------- |
| CSS 变量 wiring | `getPropertyValue('--token')` 比对 token 字面值——CSS 层面的验证，V8 不追踪样式计算             |
| 视觉语义        | outline 有 border / solid 有背景 / text 无背景——断言 `getComputedStyle` 返回值，不涉及源码分支 |
| 响应式 px 数值  | `toBeCloseTo(exp.height, 0)` 精确比对——验证 CSS 渲染结果而非源码执行路径                       |

**核心结论**：覆盖率是代码执行覆盖的度量，不是功能完整性的唯一指标——低覆盖率意味着有代码路径未被测试触发（需要补测试），但高覆盖率不等于所有视觉/交互行为都已验证（视觉维度靠 wiring 断言，不靠覆盖率）。

---

## 测试失败的分类排查（L0~L3）

**不要直接改测试值让它过**，按下表顺序排查：

| Level                    | 现象                                      | 修哪里                                 |
| ------------------------ | ----------------------------------------- | -------------------------------------- |
| **L0** 测试本身错        | 选择器写错、断言期望值与设计稿/Token 不符 | 修 `*.test.ts`                         |
| **L1** 组件 API 设计偏差 | prop 名/类型/默认值不符合预期             | 修 `src/<comp>/types.ts`               |
| **L2** 组件实现 bug      | 渲染/事件/状态机错                        | 先在测试里 reproduce，再修 `OComp.vue` |
| **L3** Skill / 文档错    | 描述的 class/prop 与源码不符              | 同步修文档 + 当前测试                  |

---

## 完整方法论入口

本 skill 包含完整的测试方法论（方法论不再在 `__tests__/README.md` 中重复，该文件只记录文件夹自身的结构和运行方式）。

详细骨架代码与各维度示例见 [references/](./references/)：

- [three-file-structure.md](./references/three-file-structure.md) — 三个文件职责边界 + 骨架代码 + 决策表
- [visual-contract.md](./references/visual-contract.md) — 视觉断言策略 + 双主题 + variant 承载属性
- [pitfalls.md](./references/pitfalls.md) — 踩坑速查（完整版，含排查顺序 L0~L3）

标杆组件测试：

- 简单组件标杆：[packages/opendesign/src/button/**tests**/](../../opendesign/src/button/__tests__/) — 3 文件 / 4 个 describe（静态契约 + 动态契约 + 视觉契约 + 插槽契约） + 响应式 STOPS + token 链 + 级联一致性 + SSR
- 复杂组件标杆：[packages/opendesign/src/data-table/**tests**/](../../opendesign/src/data-table/__tests__/) — 3 文件 / 5 个 describe（含子配置契约、插槽契约） + 暴露方法 + token 链响应式断言

`__tests__/` 目录结构与索引见 [packages/opendesign/**tests**/README.md](../../opendesign/__tests__/README.md)。
