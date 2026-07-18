---
name: interflow-video-cut
description: Turn a local talking-head / 口播 video into metadata, transcript, and an AI-composed card-based video where the agent composes cards by cloning styled templates and filling them (designing bespoke only when content needs it), then renders to MP4. Ships with the Interflow AI club sign-off ("Interflow AI 出品"). Use when the user asks for interflow-video-cut, 口播成片, talking-head repurposing, video takeaways, transcript cleanup, or turning a spoken video into a captioned card video.
---

# Interflow Video Cut — 口播成片 Workflow

Interflow Video Cut converts a local video into a card-based composition: the
agent designs the cards (timing + content), assembles one composition HTML, and
renders it to MP4 via `hyperframes`.

**Default authoring mode: clone-and-recompose, not free-design.** Per card, start
from a shipped fragment (`references/styles/<key>.html`); always swap the text +
accent, and **recompose its layout freely to serve the card's point — while
holding the style's DNA fixed** (fonts, theme palette, ornament, spacing scale,
overflow guards). Cloning anchors the quality floor in the style's *tokens*, not
in a frozen arrangement, so adjacent cards need not look identical. Hand-authoring
from a blank file is the **exception**, only when content fits no reference.

## CLI Resolution

`vtake` CLI (`npx -y @notedit/vtake@latest`) handles extract/transcribe;
`hyperframes` (`npx -y hyperframes@latest`) renders. Both auto-download from npm.
`SKILL_DIR` = this skill's dir (host injects it as "Base directory for this
skill: …"); all `references/…` + `scripts/…` paths are relative to it.

## Reference Map — read the right file at the right step

The workflow skeleton is below; the heavy detail lives in `references/`. Clone
from the library, don't reinvent.

**Loading discipline (progressive disclosure — read this first).** Every file
below is **Level 3**: it costs zero tokens until you open it, so open it **only
when you actually branch into its step, and read only the slice you need** — not
the whole file "to be safe." Concretely: (1) **never pre-read** these at the
start of a run; pull each one at the moment its step arrives. (2) When a file is
a catalog/matrix (`DESIGN_INDEX.md`, the resolution tables in
`render-strategy.md`), read **the chosen style's / ratio's row**, not the entire
matrix. (3) On the **fast path** — the user pre-approved a single known preset
(e.g. says "默认 / glass-hud / 直接产") — skip `render-strategy.md` **and**
`DESIGN_INDEX.md` entirely and go straight to that preset's recipe + the one
style fragment it clones. Reading all four heavy refs on every run defeats the
whole point of moving them out of `SKILL.md`.

| file | what's inside | read at |
|---|---|---|
| `references/DESIGN_INDEX.md` | full style × layout × frame matrix + a decision guide + the 中文风格词库 (中文名 ↔ key) | Step 6 / 7 |
| `references/render-strategy.md` | **Step 7 in full** — the 5-question call (Channel A `AskUserQuestion` + Channel B plain-text), precompute rules, day/night auto-match, canvas/frame/bounds resolution tables, theme palettes, 留白, camera rhythm (运镜), layout compositions, storyboard render contract | Step 7 |
| `references/card-contract.md` | **Step 8 in full** — clone-first steps, the card HTML contract + hard rules, NON-NEGOTIABLE overflow safety, portrait sizing, motion philosophy, the `data-anim` kinds table, and the `card-cta` brand-outro template | Step 8 |
| `references/composition-assembly.md` | **Step 9 reference detail** — GSAP statement cheat sheet, timing validation, video framing reference, HyperFrames QA rules, hard-won gotchas, the fixed card-cta GSAP block | Step 9 |
| `references/composition-shell.html` | the STATIC composition scaffold you `cp` and fill (do NOT retype it) | Step 9 |
| `references/transitions-dev-motion.md` | **transitions.dev motion kit** — 7 ported product-UI component effects (digit-flip / lines-reveal / blur-swap / badge-pop / check-draw / icon-swap / shimmer) + 2 handoffs (page / reveal), the CSS-cubic-bezier→GSAP curve map, required card HTML/CSS hooks, and the **content-driven default-by-content table**. The kit is the default surface for graphic cards (every video shows crafted micro-motion, not plain text). | Step 6 / 8 (any graphic card) |
| `references/impact-motion.md` (+ `impact-motion/playground.html` live demo, `?seek=<sec>` freezes frames) | **impact-motion kit（炸裂族动效）v2** — 12 hard-arrival kinds (type-on / char-scramble / word-slam / shake / light-sweep / stamp + mask-lines / magnetic-assemble / ink-bleed / rgb-split / split-flap / flip-3d) + 4 exit transitions (shatter / blinds / flash-cut / punch) + `slam` beat + `videoPunch` 镜头推近, compiled by `build-timeline.py`, seeded & seek-safe. Contains **SLAM DNA 三铁律**, the **Style × impact 准入矩阵** (incl. 歸藏 clean family + light-theme ink flash), and the **冲击自动分配** signal table. Whole-film budget: **≤3 impact uses**（炸裂，但克制）. | Step 6 (自动分配) / 8 (writing impact cards) |
| `references/card-shots.md` | **卡片分镜库（形状层）** — 7 个整卡多幕编排预设（number-landing / list-cascade / quote-hold / compare-split / mechanism-draw / token-cycle / headline-stack），签名动作 + 槽位契约 + 后 50% 揭示默认，`build-timeline.py` 编译（`scripts/card_shots.py`）。含 **词时触发**（`data-anim-at-word` / 槽 `atWord` / 字符串 `videoPunch`——揭示踩说话人真实词时）与 **direction 导演块**（前铺后冻 / 构图轮换 / 呼吸帧 lint，opt-in）。内容→分镜默认表在文内。 | Step 6 (选分镜/导演块) / 8 (写 shot 卡的 DOM 契约) |
| `references/narrative-progression.md` | **叙事递进编排** — when the transcript *argues / explains* (mechanism, cause→effect, this-vs-that, setup→payoff), 4 arcs (问题→机制→产出 · 分阶段揭示 · 对比递进 · 认知翻转) that sequence cards + stage each card's reveal so motion *carries the logic*. Expressed entirely in `beat`/`transition`/`data-anim`/`zone` — no new visual style. Skip for a flat list of independent takeaways. | Step 6 (sequencing an explainer) |
| `references/editorial-print-montage.md` | the multi-asset montage kit for the `editorial-print` style (5 layout primitives, 3 transitions, asset staging, woven vs standalone modes) | when style = editorial-print |
| `references/styles/*.html` | self-contained style fragments — **clone these**; includes the 炸裂族 (neon-grid-hud / liquid-aurora / holo-iridescent + playground-gallery DNA) | Step 7 / 8 |
| `references/styles/guizang-dna.md` (+ `guizang-clean.css` 组件 + `guizang-checklist.md` 质检) | **简洁排版类·歸藏家族**的 DNA 纪律层（两支柱、字号字重耦合、预设调色板、组件库）。统管 swiss / minimal / terminal / editorial-print / pastel-aura | 选了 clean 家族任一款时（Step 7/8）|
| `references/components/components.md` (+ `components-gallery.html` 渲染 demo / 抬取源) | **视觉素材组件库·高频包**（归藏家族新成员，13 个内容形态：折线/柱/环形/大数字 · 类比/黑盒/等式/光谱/冰山/对照 · 终端/对话/代码）。内容命中某种形态时抬一个组件进卡，质量锁死在规格上。含 content→组件 查表。**仅 clean 家族**，CSS 在 guizang-clean.css | clean 家族卡内容命中结构形态时（Step 6 选形 / Step 8 写卡）|
| `references/layouts/*.html` | layout skeletons (videoBounds + cardBounds, landscape/portrait); neon-grid-hud carries its own window-scene | Step 7 / 9 |
| `references/frames/*.html` | 3 frame chrome fragments (clean / hairline / polaroid) | Step 9 |
| `references/curve-motion/README.md` | **可选视觉增强** — 数学曲线母题，**按用途分流**：氛围底(任意曲线) · 斜字 textPath(**仅开放曲线 `openKeys`**，闭合曲线排字必溢出) · clip 裁图剪影(**仅闭合曲线**) · 采样点布点(任意) + 沿曲线丝滑入场漂移（`curveIn`/`curveBob`）。全闭式 `draw(t)`、确定性 seek 安全；配暗底风格（nebula-glass/glass/spatial/geom），不叠 glass-hud/swiss/minimal。**Step 7 的曲线适配风格会触发一次 curve-intent 条件追问**（见 render-strategy.md「5b」） | Step 7 / 8 / 9（想加高级动态质感时） |

## Workflow

### Interaction contract — 前置一次问全，然后无人值守跑完（ALL channels）

**The user hands you a video to get back a finished film, not to babysit a
pipeline.** So the ONLY moment you ask the user anything is **once, upfront**
(Step 3.5), in a single batched round — ratio / layout / style / 运镜 / card
density. After they answer, you run the
**entire** pipeline (transcribe → correct → storyboard → cards → assemble →
render) **autonomously to a finished MP4, with
no further questions** — so they can walk away and come back to a complete
work. This ordering is **identical on every invocation channel** (手机 CLI,
飞书 bot, desktop) — the channel only changes the question *transport* (native
`AskUserQuestion` vs plain-text), never the *timing*.

Rules:
- **Front-load, don't drip.** Never ask a question mid-pipeline that you could
  have asked in Step 3.5. The old flow asked visual direction at Step 7 (after
  transcribe) — that's the bug this contract fixes. Precompute
  everything askable from the **file alone** (metadata + color analysis) so the
  whole batch fires before any slow/mechanical step.
- **Autonomous = render and deliver, not preview-and-wait.** On the autonomous
  path you self-QA with snapshots (Step 10) and go straight to render (Step 11) —
  the user reviews the **finished MP4** and asks for revisions after. Only drop
  into the interactive preview loop if the user explicitly says they want to
  watch/iterate live.
- **Stop early only for a genuine blocker** (missing file, ASR rate-limit, a
  contradiction in the request) — not for a preference you could have batched.
- If the user *explicitly* pre-answers in their opening message ("竖屏 glass 直接产")
  or says "你看着来/默认", skip Step 3.5's questions and proceed on those + the
  auto-recommendations.

### 1. Check Environment

```bash
npx -y @notedit/vtake@latest doctor
# confirm bundled assets:
ls "<SKILL_DIR>/assets/fonts" "<SKILL_DIR>/assets/vendor/gsap.min.js"
```

Required:

- `ffmpeg` / `ffprobe` (system)
- `python3` (stdlib only) — for `scripts/auto-style.py`, the auto style-match by video color in Step 7.0
- `<SKILL_DIR>/assets/fonts/*.woff2`, `<SKILL_DIR>/assets/vendor/gsap.min.js` (bundled inside this skill, staged to work dir in Step 9)

Optional:

- `ELEVEN_API_KEY` — set → `vtake transcribe` hits ElevenLabs directly (no rate
  limit). Unset → proxy `https://vtake.app/api/transcribe` (**3 req/min/IP**;
  override via `VTAKE_TRANSCRIBE_ENDPOINT`).

Strongly recommended on macOS for `hyperframes render`:

```bash
export PRODUCER_BROWSER_GPU_MODE=hardware
```

### 2. Create a Work Directory

```bash
VIDEO_PATH="/absolute/path/input.mp4"
WORK_DIR=".interflow-video-work/$(basename "$VIDEO_PATH" | sed 's/\.[^.]*$//')"
mkdir -p "$WORK_DIR"
```

### 3. Extract Audio and Metadata

```bash
npx -y @notedit/vtake@latest extract "$VIDEO_PATH" --out-dir "$WORK_DIR"
```

Outputs: `metadata.json` (duration, width, height, fps) + `audio.mp3`.

### 3.5 Upfront Consultation — ask EVERYTHING here, once (then go autonomous)

**This is the single user-interaction gate.** Everything askable is decidable
from the **file alone** — no transcript needed yet — so ask it all now, before
the slow steps, then run the rest untouched (per the Interaction contract above).

**Precompute first (file-only, cheap):**

```bash
python3 "<SKILL_DIR>/scripts/auto-style.py" "$VIDEO_PATH" --json
# → {"mode","temp","recommend":[...],"recommend_cn":[...]}  → recommendedStyle
```
- `recommendedRatio` from `metadata.json` aspect (≥1.5→16:9 · ≤0.7→9:16 · else 4:5).
  **iPhone `.MOV` caveat:** ffprobe may report a rotated `1920×1080` that displays
  as portrait — check `stream_side_data=rotation` before trusting the aspect.
- `autoCount` from duration × **assumed-medium** density (Step 6 math) — label it
  "约 N 张"; you refine the exact count after the transcript exists. Good enough to ask.

**Then ask ONE batched round** — the 5 visual questions. Use the best channel
(native `AskUserQuestion`; else the plain-text template). The 5 visual questions
+ resolution tables live in
[`references/render-strategy.md`](references/render-strategy.md) (read its question
call now).

Record all 5 answers in working memory: `ratio / layout / style / rhythm /
cardDensity`. These drive Steps 6, 7, 8 — **do not re-ask any
of them later.** (Channels without a native question tool: post the plain-text
batch as one message, parse the reply, proceed. Same timing on every channel.)

> If the user already stated preferences in their opening message, or said
> "默认/auto/你看着来", skip the questions and use those + the auto-recommendations.
> After this gate, you do not pause again until the finished MP4 (Step 12) —
> unless a genuine blocker appears.

### 4. Transcribe (provider-aware: 火山 Seed ASR or ElevenLabs)

Both produce the **same** `transcript.json` shape (`{ segments, words, raw }`, word-
level timestamps in seconds) — the rest of the pipeline doesn't care which ran.

```bash
if [ -n "$VOLC_ASR_API_KEY" ]; then
  # 火山引擎 Seed ASR 2.0 — 中文友好、便宜、词级时间戳。Key 走 env（不进 git）。
  node "$SKILL_DIR/scripts/transcribe.js" --audio "$WORK_DIR/audio.mp3" --out-dir "$WORK_DIR"
else
  # fallback: ElevenLabs via vtake (proxy mode works key-free, 3 req/min/IP)
  npx -y @notedit/vtake@latest transcribe "$WORK_DIR/audio.mp3" --out-dir "$WORK_DIR" --asr elevenlabs
fi
```

Output: `transcript.json` with `{ segments, words, raw }`.

**Two ASR providers, pick by env:**
- **火山 Seed ASR** (`VOLC_ASR_API_KEY` set) — async submit (base64 audio, **no
  public URL needed**); `transcribe.js` resamples to 16k mono first, polls, and
  emits the same shape. Optional: `VOLC_ASR_RESOURCE_ID` (default `volc.seedasr.auc`),
  `VOLC_ASR_MODEL` (default `bigmodel`). Re-convert a saved result without re-
  billing: `node transcribe.js --from-result volcengine_result.json --out-dir "$WORK_DIR"`.
- **ElevenLabs** (no `VOLC_ASR_API_KEY`) — `vtake` proxy mode runs key-free out of
  the box (zero model download) and only hits the rate limit below. There is no
  local/whisper path.

**Rate limiting (proxy mode only — no `ELEVEN_API_KEY`):** the server allows
3 requests per minute per IP. If you see an error starting with
`rate_limited:` or `service_busy:`, do **not** auto-retry — stop and tell
the user how many seconds to wait (the message includes the retry hint),
then resume from this step when they ask again.

> **Note — this skill is additive only.** It *decorates* a take (cards over
> video); it does NOT 去口水词 / 去气口 / 去废话. It assumes a reasonably clean
> recording. If a raw 口播 has lots of 口水词 / 卡顿 / 重说, those stay in the
> footage and get baked under your cards — clean it first with whatever editor
> you prefer, then feed the cleaned video here. (Automatic rough-cut is no longer
> wired into this pipeline.)

### 5. Correct Transcript

Read `transcript.json` and fix obvious ASR errors:

- Homophones, product names, technical terms, punctuation
- Preserve all `start` / `end` timestamps
- Prefer editing `segments[].text` only
- Edit individual `words[].word` only for clear one-to-one replacements

### 6. Draft a Lightweight Storyboard (in chat)

**No CLI involved.** Read `transcript.json` + `metadata.json` and design
cards directly. `storyboard.json` is an agent-internal planning artifact
— no vtake CLI command consumes it; it exists so you can think clearly
about timing and content before writing each card's HTML. Keep the
shape consistent with the example below so the same outline can drive
the composition you author in Step 9:

```json
{
  "schemaVersion": 3,
  "composition": {
    "fps": 30,
    "width": 1080,
    "height": 1920,
    "durationSeconds": 121.2,
    "layout": "portrait",
    "themeId": "noir",
    "seed": 42,
    "background": { "key": "dark-particles", "accent": "#7aa2ff", "opacity": 0.9 }
  },
  "videoTrack": {
    "sourcePath": "input-video.mp4",
    "startSec": 0,
    "endSec": 121.2,
    "bounds": { "x": 0, "y": 0, "width": 1080, "height": 1920 }
  },
  "subtitles": { "enabled": false },
  "cards": [
    {
      "id": "card-01",
      "intent": "Hook with the speaker's anxious midnight question",
      "startSec": 0.5,
      "endSec": 13.0,
      "accentIndex": 0,
      "zone": "fullscreen",
      "beat": "kinetic",
      "contentHints": {
        "kicker": "AN HONEST QUESTION",
        "title": "晚上 11 点的灵魂提问",
        "detail": "客户六十秒语音：「人民币会升值，我的美金保单是不是亏惨了？」"
      }
    }
  ]
}
```

**Required Card fields:**

| field | type | purpose |
|---|---|---|
| `id` | string | stable id used in card HTML & GSAP selectors |
| `intent` | string | natural-language description; fed to card synthesis |
| `startSec` / `endSec` | number | times in seconds (endSec > startSec) |
| `accentIndex` | 0 \| 1 \| 2 \| 3 \| 4 | which of the 5 theme accent colors this card pulls |
| `zone` | enum (see below) | where on the canvas the card lives |
| `contentHints` | object | free-form bag; agent puts kicker/title/detail/data/quote here |
| `archetype` (optional) | string | free-form label you may attach to remember a card's pattern; absent = free-form, which is the default |
| `beat` (optional) | enum: `settle` \| `cut` \| `hold` \| `kinetic` \| `montage` \| `footage` \| `slam` | **the card's motion = its INTENT** (not a random gesture). `build-timeline.py` picks the whole enter/life/exit by this. Absent = `settle` (calm slip+drift, the legacy default). Assign by what the card means — hook→`kinetic` 或 `slam`（整卡逐块砸落+死静，impact 族、计入 ≤3 预算、卡需 ≥2.5s）, 重锤/严肃→`cut`, 金句/留白→`hold`, 罗列/证据→`montage`, 视频当主角→`footage`. See the beat table in `composition-assembly.md`. |
| `videoPunch` (optional) | (number \| string)[] — 秒（相对卡 start）或**要踩的词** | **说话人爆点瞬间的镜头硬推近**：`#video-wrap` scale 1→1.06 (0.14s power4.out) → 回 1 (0.3s)。字符串条目（如 `["私信"]`）= 从 transcript 词级时间戳解析、推近落在说话人**说出该词的瞬间**。两次间隔 ≥0.5s；一片 ≤2 次；不计入 impact 预算。 |
| `shot` (optional) | `{key, slots, params}` | **卡片分镜预设**（形状层）：一张卡的整段多幕编排由编译器展开——7 个预设（number-landing / list-cascade / quote-hold / compare-split / mechanism-draw / token-cycle / headline-stack），每个带签名动作 + 槽位契约 + 后 50% 揭示默认；槽可 `atWord` 踩词时。声明时接管 enter/life（beat 忽略）；校验失败回落 beat。见 `references/card-shots.md`。留给值得编排的节点（一片 2-4 个），普通卡用 beat。 |
| `transition` (optional) | enum: `cut` \| `fade` \| `slide` \| `wipe` \| `page` \| `reveal` \| `shatter` \| `blinds` \| `flash-cut` \| `punch` | card-to-card handoff (**now live** in `build-timeline.py`): `cut` = hard frame boundary (no slip overlap; set next card's `startSec` = this `endSec`), `wipe` = clip sweep, `fade`/`slide`/absent = the silky slip-up; `page`/`reveal` = transitions.dev handoffs; `shatter`/`blinds`/`flash-cut`/`punch` = impact kit（`flash-cut` is a hard boundary like `cut`; `shatter` needs the card ≥1.6s; ≤3 impact uses per film — see `references/impact-motion.md`）. |
| `styleKey` (optional) | string (a `references/styles/<key>`) | which style fragment to clone this card from. Absent = the film's **primary** style. Set it only on **accent cards** (hero / big-number / outro) to pull a tonally-compatible **sibling** style — see the style-family note in Step 7. Colors stay coherent automatically: every fragment paints from `var(--accent-N)`, so a sibling inherits the theme palette. |
| `componentKey` (optional) | string (a `references/components/<key>`) | which **visual component** this card's content maps to (折线/柱/环形/大数字 · 类比/黑盒/等式/光谱/冰山/对照 · 终端/对话/代码). Set it when the transcript hits a structured shape (a trend, a ratio, an analogy, a dialogue…) — pick via the content→组件 table in `references/components/components.md`. Absent = free-compose (today's default). **clean 家族 only.** |

**Composition-level `background` (optional)** — a moving atmosphere layer behind the
cards / above the video. `{ key, accent, opacity }`; `key` ∈ backgrounds 库
(`dark-particles` / `starfield` / `aurora` / `grid-hud` / `mesh-gradient`) 或
`curve:<曲线>`（曲线**氛围底**——氛围归这层，不是前景斜字）。`build-timeline.py` 自动注入
`<canvas>` + `draw(t)` 钩子（Step 9 记得 `cp` `backgrounds.js` + `curve-atmosphere.js` 进
`vendor/`）。选择在 Step 7「背景层」问题里决定（见 render-strategy.md）。全闭式 `draw(t)`、
seek 安全。

**Five `zone` values** (resolve to card-host pixel bounds in Step 9; full bounds
table in `references/composition-assembly.md`): `fullscreen` (whole canvas —
hero / big numbers) · `whiteboard-area` (40px inset or portrait bottom-45% —
dense data) · `lower-third` (bottom 30% — annotate over video) · `side-panel`
(landscape right-42% / portrait bottom-40% — data beside video) · `video-overlay`
(full canvas, mostly-transparent card — overlay on full-bleed video). Video
bounds are set **once** (`videoTrack.bounds`); "moving" video between cards =
GSAP tweens on `#video-wrap` (Step 9).

**冲击自动分配（pipeline 全自动 — drafting 时执行，用户不手选）。** 扫描修正后的
transcript，命中信号就自动分配 impact，按优先级取**最强 ≤3 个**（预算硬约束，
超了 build-timeline.py 会 WARN），其余一律回落 transitions.dev 丝滑 kit：
① **认知翻转**（"但其实/真相是/大家都错了"）→ break 卡 `transition: shatter` +
下一张 `word-slam` 立新观点（优先级最高）；② **开场 hook / 全片最强主张** →
`beat: "slam"`；③ **情绪爆点 / 章节硬切** → `flash-cut` 或 `punch` + 可选
`videoPunch` 踩在重音音节上；④ **命令 / 代码 / 工具名** → `type-on`。
完整信号表 + Style × impact 准入矩阵（歸藏 clean 家族哪些慎用）见
[`references/impact-motion.md`](references/impact-motion.md)。

**No prescribed roles or arc** — cards emerge from what the video says (all
quotes, all data, open on a number or a story; let the transcript drive).
**But when the transcript *argues or explains*** (a mechanism, cause→effect,
this-vs-that, setup→payoff — you can say "first… which causes… which is why… so…"
across the cards), reach for [`references/narrative-progression.md`](references/narrative-progression.md):
4 arcs that sequence the cards + stage each card's reveal so motion carries the
logic, all in `beat`/`transition`/`data-anim` (no new style). Skip it for a flat
list of independent takeaways — those stay平铺.

**Card boundaries — one intent per card** ("let the transcript drive" ≠ "cut
anywhere"). A boundary belongs where the speaker *pivots to a new idea*; a card
spans the stretch between two boundaries. Signals: **topic shift** ("…now here's
what works" = new card) · **argument unit** (a setup→proof→payoff >~20s = 2–3
cards, one per move) · **distinct claim/number/comparison** (each its own card,
no 4-facts data-dump) · **emphasis/repetition** (repeated phrase / "the key
point" = its own beat) · **shot change** (face→screen-share→prop). The math
below sets *how many*; these set *where*. Disagree → trust the intents; never
split one idea or fuse two to hit a number.

**How many takeaways? — auto-infer from duration + density.** No fixed
upper limit. Floor is fixed: **minimum 5 cards**.

**Step 1 — base pace by duration** (natural sec/card for medium density):

| video duration | base pace (sec per card) |
|---|---|
| < 60s (short reel) | **6–8s** |
| 60s – 3 min | **8–12s** |
| 3 – 10 min | **12–20s** |
| 10 – 30 min | **20–35s** |
| > 30 min | **30–60s** |

**Step 2 — density multiplier:** High density (many numbers / distinct claims / staccato) **× 0.7** · Medium (mixed data + narrative) **× 1.0** · Low (slow narrative, one idea over many sentences) **× 1.4**.

**Step 3 — compute:**

```
cardCount = max(5, round(videoSec / (basePace × densityMultiplier)))
```

Always sanity-check against content: the math gives a starting count, but the
actual intents decide the final count.

**Speaker presence — keep the talking head on screen** (unless the user wants a
faceless explainer): cards annotate, they don't replace. Default = full-bleed/
large-PIP speaker on opening + closing cards, ≥ small PIP/side-panel where the
speaker makes a personal point; data-heavy cards can go full-card briefly.

**Distill, don't transcribe — a card is information design.** The #1 failure is
pasting a spoken sentence onto a card; a headline is a *rewrite* (same meaning,
⅓ the words, point surfaced). Gate every card: (1) **one intent, one sentence**
— can't → split; (2) **headline ≠ quote** — ~14-char title, demote the
explanation to a small detail line; (3) **no two cards make the same point** —
merge/reframe overlaps; (4) **shape follows content** — comparison→two-column,
number→big figure+label, list→stacked rows, quote→large centered. Reject &
rewrite if: `title` > ~14 中文字, `detail` is a verbatim clause, or the card is
"the next sentence" not "the next idea".

**Final card — append a customizable brand outro (`card-cta`).** After all
content cards, append one `fullscreen` outro card (`contentHints`: `recap` +
`purpose`) and extend `composition.durationSeconds` by ~3.5s to match its
`endSec`. Lead with a **recap / payoff line rewritten from what the video said**
(the earned content beat, not a logo flash) + a one-line **purpose / 延伸** under
the wordmark. **Re-theme it to the composition's style** (reuse `--bg`/`--ink`/
`--accent-0`, swap mark/wordmark/tagline; keep the entrance choreography) — a
clashing fixed outro is a defect. Ships the Interflow club sign-off (`Interflow`
+ `Interflow AI 出品`); for an outside creator swap/drop the brand, no hard-sell
CTA, **strip AI-jargon** (赋能/闭环/leverage…). Full template + JSON + entrance
choreography: `references/card-contract.md`.

### 7. Resolve Render Strategy (from the Step 3.5 answers — do NOT ask again)

The visual system — ratio / layout / style / 运镜 / density — was **already chosen
by the user in Step 3.5**. This step is pure **resolution**: turn those stored
answers into concrete canvas size, frame, theme palette, and per-card bounds. No
questions here (front-load contract).

What this step does with the stored answers:
- **Resolve canvas** from `ratio` (16:9→1920×1080 `landscape` · 9:16→1080×1920
  `portrait` · 4:5→1080×1350 `portrait`).
- **Map `style` → a specific style key** and **auto-pick the frame** from the
  layout × style matrix; **resolve `rhythm`** (fixed vs dynamic videoBounds).
- **Refine `cardCount`**: in 3.5 you used assumed-medium density for the "约 N"
  label; now the transcript exists, so apply the real density multiplier (Step 6)
  and let the actual intents set the final count.
- **Conditional follow-up already handled in 3.5:** if `style` ∈ {glass /
  nebula-glass / spatial / geom}, the curve-foreground (5b) and dark-background
  (5c) micro-questions fire as part of the upfront gate (the user is still there
  right after picking style) — not here. By Step 7 they're already answered.

**→ The full resolution detail — the canvas / frame / bounds tables, theme
palettes, day/night style map, 留白, camera rhythm, the storyboard render
contract, AND (for reference) the original question call + plain-text fallback —
is in [`references/render-strategy.md`](references/render-strategy.md).** Read
only the slice for your resolved ratio/style. (Its "ask" machinery is what Step
3.5 invokes; here you read the **resolution tables**.)

State back what's locked in one sentence (ratio + canvas size, layout, primary
style + any sibling accent styles, frame, final cardCount, rhythm), then proceed.

### 8. Write Each Card's HTML

**Clone-first (the default).** For each card:

1. `cp "$SKILL_DIR/references/styles/<styleKey>.html" "$WORK_DIR/public/cards/<card-id>.html"` — `<styleKey>` is the card's `styleKey` if set, else the film's **primary** style (see the style-family note in Step 7: most cards use the primary; accent cards may pull a tonally-compatible sibling).
2. Rename the fragment's `data-card-id="ref-<key>"` to this card's `<card-id>` (update the scoped `<style>` selectors + element ids).
3. Swap the placeholder copy for this card's real `contentHints`, set the accent to the card's `accentIndex`.
4. **Compose, don't just fill — but hold the style's DNA.** The floor is the style's design tokens (fonts, theme palette / `var(--accent-N)`, ornament, spacing scale) + the overflow guards — keep those fixed. Within that envelope you're free to **recompose the fragment to serve this card's point**: promote/demote emphasis, switch stacked ↔ two-column, move the panel (bottom / centered / side), drop an unused slot, let shape follow content. Two adjacent cards should NOT be structurally identical when their content differs. Off-limits: re-picking fonts, off-theme color, foreign ornament, breaking overflow safety. Over a talking head, keep the speaker's face clear (a deliberate full-dim statement beat is the rare exception). Full guidance in `references/card-contract.md`.

Authoring a fragment from a blank file is the **exception**. Animations are
**declared, not coded** — use `data-anim-*` attributes only; never write
`<script>` in a card. The composition `index.html` is the only place a
`<script>` (the GSAP block) lives.

**Give each graphic card ONE crafted motion moment (transitions.dev kit — the
default, not optional).** A card that's just static text on video is the failure
this is here to fix. As you fill each card, reach for the **content-matched**
component effect: a number → `digit-flip`, a list → `lines-reveal`, an emphasis
word → `blur-swap`/`shimmer`, a chip → `badge-pop`, a ✓ → `check-draw`, a
this→that swap → `icon-swap`; topic shifts between cards → `page`/`reveal`
handoffs. Add the right `<span class="digit">` / `.line` / `.icon-from` hooks the
effect needs (see the kit). **One** effect per card + its beat — never stack
three (恰到好处). Talking-head/face-is-the-point cards may stay calm; the kit
serves the *graphic* cards. Full default-by-content table + required HTML/CSS per
kind + the curve map: [`references/transitions-dev-motion.md`](references/transitions-dev-motion.md).

**结构化内容 → 抬一个视觉组件 (clean 家族).** When a card's content hits a
structured shape — a trend, a ratio breakdown, a single hero number, an analogy
(X≈Y), a black-box, an A+B=C equation, a spectrum, an iceberg, a two-way
comparison, or a terminal/chat/code mock — don't free-design it: pick the
component via the content→组件 table in
[`references/components/components.md`](references/components/components.md), copy
its `<!-- COMP:<key> -->` block from `components-gallery.html`, fill real content,
and scope its `guizang-clean.css` classes into the card (same as cloning a clean
fragment). These are 归藏-family members — they already encode the 字号字重 +
间距 discipline, so **don't hand-tweak their font/spacing values**. clean 家族 only.

**简洁排版类·歸藏家族 cards** (swiss / minimal / terminal / editorial-print /
pastel-aura): before composing, read
[`references/styles/guizang-dna.md`](references/styles/guizang-dna.md) — these
share one DNA (字号字重耦合 + 预设调色板 + 组件库 `guizang-clean.css`)。配色只能取
预设表（禁自定义 hex，accent 经 `--accent`），组件用 `.stat-card`/`.callout`/
`.pipeline`/`.timeline-v`/`.bar-chart`/`.kicker`/`.meta`/`.mark`，一片一支柱永不混。
写完每张 clean 卡跑一遍校验：

```bash
node "$SKILL_DIR/scripts/validate-clean-card.mjs" "$WORK_DIR/public/cards/<card-id>.html"
```

应 PASS（无 hard fail）；交付前对照 [`guizang-checklist.md`](references/styles/guizang-checklist.md) 过 P0。

**→ The complete Step 8 — the card HTML contract + hard rules (lint), the
canvas-atmosphere exception, NON-NEGOTIABLE overflow safety, portrait
mobile-first sizing, the silky motion philosophy, the full `data-anim` kinds
table, and the `card-cta` brand-outro template — is in
[`references/card-contract.md`](references/card-contract.md). Read it **once
before your first card** — the **overflow safety + contract hard-rules are
mandatory**; the `data-anim` table and the `card-cta` template are lookups, jump
to them only when you actually need them (don't re-read the whole file per
card).**

### 9. Assemble the Composition HTML

Stage the assets and write `$WORK_DIR/public/index.html`:

```bash
# SKILL_DIR is injected by the host ("Base directory for this skill: …")
SKILL_DIR="<SKILL_DIR>"

mkdir -p "$WORK_DIR/public/fonts" "$WORK_DIR/public/vendor" "$WORK_DIR/public/cards"
cp -n "$SKILL_DIR/assets/fonts/"*            "$WORK_DIR/public/fonts/"
cp -n "$SKILL_DIR/assets/vendor/gsap.min.js" "$WORK_DIR/public/vendor/"
# if storyboard.composition.background is set, stage the background-layer libs
# (build-timeline.py injects the <canvas> + draw(t) hook automatically):
cp -n "$SKILL_DIR/references/backgrounds/backgrounds.js"        "$WORK_DIR/public/vendor/"
cp -n "$SKILL_DIR/references/curve-motion/curve-atmosphere.js"  "$WORK_DIR/public/vendor/"
# copy the STATIC composition shell — do NOT retype it
cp "$SKILL_DIR/references/composition-shell.html" "$WORK_DIR/public/index.html"
# stage the input video so the composition can reference it by relative path
ln -f "$VIDEO_PATH" "$WORK_DIR/public/input-video.mp4" 2>/dev/null \
  || cp "$VIDEO_PATH" "$WORK_DIR/public/input-video.mp4"
```

**Then fill the shell — do not regenerate it.** `index.html` is the copied
`composition-shell.html` (already has `#stage` / `#video-wrap` / card-host
structure + `@font-face` + GSAP runtime). Edit only these slots:

1. **The 6 `{{...}}` tokens** at the top: `{{BG}}` `{{TEXT}}` `{{ACCENT_0..4}}`
   (from the chosen `themeId` palette), `{{DURATION}}` (= `composition.durationSeconds`),
   `{{FPS}}`, `{{WIDTH}}`, `{{HEIGHT}}`. The tokens appear in a few places each —
   a `sed` pass replaces all at once, e.g.
   `sed -i '' -e 's/{{DURATION}}/121.2/g' -e 's/{{FPS}}/30/g' … "$WORK_DIR/public/index.html"`.
   (`sed -i ''` is macOS/BSD; on Linux use `sed -i` with no `''`.)
2. **`.video-wrapper` initial `left/top/width/height`** — set to card-01's layout bounds.
3. **The two `INJECT-*` markers** — **do NOT hand-author these.** Run the
   generator; it reads `storyboard.json` + `public/cards/*.html` and fills both
   the card-host divs and the full GSAP timeline (enter / drift / exit, with
   `data-anim` attributes compiled via the cheat sheet, times quantized,
   `data-track-index` increasing, drift repeats finite):

   ```bash
   python3 "$SKILL_DIR/scripts/build-timeline.py" --work "$WORK_DIR"   # add --slip 0.55 to tune
   ```

   **Idempotent** — re-run after editing any card / the storyboard; it re-injects
   between its `BEGIN/END` sentinels. Run it AFTER Step 8 (cards exist) and AFTER
   the `sed` fill; read its stderr timing warnings. What it leaves to you:
   **`#video-wrap` reframes** for dynamic (起伏运镜) rhythm — add
   `"videoBounds": {left,top,width,height}` (+ optional `"videoClass": "video-wrapper pip"`)
   to a card in `storyboard.json` and it emits the reframe tween at that card's
   slip; cards without `videoBounds` keep the video put (calm default).

> **Hand-authoring the timeline is the exception** — only for a one-off motion the
> cheat sheet can't express (then stop re-running the script, it overwrites). Else
> declare motion as `data-anim-*` (Step 8) and let the generator compile it.

**→ The Step 9 reference detail — the GSAP statement cheat sheet, card-timing
validation (overlap is intentional), the video framing reference per layout, the
HyperFrames layout/animation QA rules, the hard-won gotchas (read before
assembling), and the fixed card-cta GSAP block — is in
[`references/composition-assembly.md`](references/composition-assembly.md).**

### 10. QA — autonomous-default: snapshot self-QA → render → deliver

**Default (autonomous path): do NOT open the interactive preview or wait for
approval.** The user front-loaded their choices in Step 3.5 and walked away to
get a finished film. So self-QA with **single-frame snapshots** (cheap — one per
card moment), fix any overflow/placement issues you see, then go straight to
Step 11 (render) and deliver the MP4. The user reviews the **finished work** and
asks for revisions after — that's when you iterate.

```bash
cd "$WORK_DIR"
# self-QA: one snapshot per card beat (cheap; NOT a render)
npx hyperframes snapshot public --at 5 --describe false   # writes public/snapshots/frame-…png
```

**Interactive path (only if the user explicitly asked to watch/iterate live):**
start the live studio and share the URL — it opens instantly, plays/scrubs in
real time, and **hot-reloads on every edit**.

```bash
cd "$WORK_DIR"
npx hyperframes preview public --no-open
# prints e.g. "Studio  http://localhost:3002" (auto-picks the next free
# port if taken). Share that URL with the user.
```

Interactive loop (only when the user opted to watch live):

1. Assemble / edit the composition (Step 9).
2. Run `hyperframes preview` (once — it stays up and hot-reloads).
   Give the user the `localhost` URL.
3. User reviews in the browser → requests changes → you edit the HTML →
   user just refreshes / re-scrubs. No render in this loop.
4. **Only when the user explicitly approves** do you move to Step 11
   (render). Do not render proactively just to "check" — snapshots
   (`hyperframes snapshot`) cover your own static QA without a full render.

> **Autonomous default does the opposite:** no preview server, no waiting —
> snapshot-QA then render directly (the user is away). Use the interactive loop
> ONLY when they said they want to iterate live.

For YOUR OWN spot-checks during building, use single-frame snapshots
(cheap), not renders:

```bash
npx hyperframes snapshot public --at 5 --describe false   # writes public/snapshots/frame-…png
```

> Pass `--describe false` to silence the built-in Gemini QA (prints
> `GEMINI_API_KEY not set, skipping` otherwise). Frames write to the **real**
> path `public/snapshots/frame-*.png` (not `snap-*.png`). Under zsh an unmatched
> glob hard-errors (`nomatch` → exit 1) — guard loops with `setopt +o nomatch`.

Manage preview servers: `hyperframes preview --list` /
`hyperframes preview --kill-all`.

> Headless / cron runs (no desktop): skip the interactive preview and go
> straight to Step 11, using snapshots for QA.

### 11. Render to MP4 (autonomous default — render once snapshots pass; or after live approval)

```bash
cd "$WORK_DIR"
PRODUCER_BROWSER_GPU_MODE=hardware npx hyperframes render public \
  -o output.mp4 \
  --fps 60   # 60 for spring/motion-heavy comps — matches the live preview's fluidity
```

> **Render at `--fps 60`, not 30.** The live `preview` plays via the browser's
> rAF (~60fps) so spring/`back.*` overshoot looks buttery; a 30fps render samples
> the same motion at half the temporal resolution and the springs read as
> slightly stepped — the #1 reason "the MP4 feels stiffer than the preview". The
> easing is identical; only the sampling differs. Use 30 only for static/calm
> talking-head cuts where file size matters.

`hyperframes render <dir>` reads `<dir>/index.html` and produces the MP4.
The flag `PRODUCER_BROWSER_GPU_MODE=hardware` (or `--browser-gpu`) is
strongly recommended on macOS — software-only Chrome rendering times out
on most laptops.

For a sanity check before the full render, capture a single frame at a
specific timestamp:

```bash
npx hyperframes snapshot public --at 5 --out snapshot-5s.png --describe false
```

### 12. Report Results

Tell the user: work dir path · key artifacts (`storyboard.json`,
`public/cards/*.html`, `public/index.html`, `output.mp4`) · ASR provider · card
count + how you chose them (1 sentence) · any missing keys / quality caveats.
Don't delete the work directory unless asked.
