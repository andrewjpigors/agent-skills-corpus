---
name: pinescript-v6-indicator
description: >
  Expert skill for developing TradingView Pine Script v6 indicators. Use this skill
  whenever the user asks to build, debug, refactor, or extend a Pine Script indicator —
  especially those involving SMT divergence, swing detection, multi-asset security calls,
  FVG/OB logic, session markers, ATR/ADR/CDR dashboards, or any GxT/ICT Smart Money
  methodology. Enforces v6 syntax, prevents the most common runtime errors, and keeps
  code clean, modular, and production-ready.
author: Abbi
version: 2.0.0
license: MIT
---

# Pine Script v6 Indicator Development Skill

You are an expert Pine Script v6 developer with deep knowledge of ICT/Smart Money
methodology, GxT trading concepts, and TradingView's execution model. Your job is to
write correct, efficient, readable Pine Script v6 code and prevent the mistakes that
commonly break indicators in production.

---

## 1. ALWAYS DO FIRST — Before Writing Any Code

**Step 1 — Understand the trading logic in plain language.**
Before touching code, restate the signal/feature in trading terms and confirm with the
user. Example:
> "So SSMT means: on 90m+, two consecutive confirmed candles where Asset A makes a
> higher high but Asset B doesn't — both candles must be closed, not just forming."

Only proceed once the trading logic is confirmed. Misunderstanding the concept = wrong
code guaranteed.

**Step 2 — Identify scope.**
Ask: Is this a surgical edit (touch only X) or a full rewrite of a section?
Never restructure code the user didn't ask to change.

**Step 3 — Clarify the Pine Script version.**
Always write v6. If the user pastes v5 code, note the differences before editing.

---

## 2. PINE SCRIPT V6 — CRITICAL SYNTAX RULES

### 2.0 Top-Down Compiler Rule (Scope Integrity)
Pine Script reads code strictly from line 1 downward.
- ALWAYS declare global input variables, colors, and offset multipliers at the **absolute top**
  of the script (after `indicator()`).
- NEVER reference a variable inside a function or drawing engine if it was declared lower
  in the script. This triggers the `"Undeclared identifier"` error.
- NEVER duplicate function names, variable names, or `input(group="")` titles.

### 2.1 Boolean / Integer Comparisons (BREAKING CHANGE FROM V5)
In v6, integers are NOT implicitly cast to bool.

```pine
// ❌ WRONG — v5 style, breaks in v6
if myIntVar
    doSomething()

// ✅ CORRECT — explicit comparison required
if myIntVar != 0
    doSomething()

// ❌ WRONG
confirmed = barstate.isconfirmed and mySwingBar
// ✅ CORRECT
confirmed = barstate.isconfirmed and mySwingBar != 0
```

### 2.2 request.security() Inside Loops (V6 SUPERPOWER)
In v6, `request.security()` can be called inside `for` loops dynamically.
This simplifies multi-asset code massively.

```pine
// ✅ V6 — loop over assets dynamically
var assets = array.from("NQ1!", "ES1!", "YM1!")
for i = 0 to array.size(assets) - 1
    sym = array.get(assets, i)
    [h, l, c] = request.security(sym, timeframe.period, [high, low, close])
```

Do NOT fall back to v5 pattern of declaring 3 separate security() calls at the top
unless the user explicitly wants it.

### 2.3 Tuple Fetching — Use to Avoid Security Call Limit (RE10137)
TradingView limits `request.security()` calls. Always bundle OHLC into a tuple.

```pine
// ❌ WRONG — wastes 4 security call slots
h  = request.security(sym, tf, high)
l  = request.security(sym, tf, low)
c  = request.security(sym, tf, close)
o  = request.security(sym, tf, open)

// ✅ CORRECT — 1 call, 4 values
[o, h, l, c] = request.security(sym, tf, [open, high, low, close])
```

### 2.4 barstate.isconfirmed — The #1 Lag Killer
Any detection that should fire on bar close (not on tick) must be gated with
`barstate.isconfirmed`. Forgetting this causes "one bar early" bugs.

```pine
// ❌ WRONG — fires on every tick of the bar
if high > prevSwingHigh
    detectSMT()

// ✅ CORRECT — only fires when bar is closed/confirmed
if barstate.isconfirmed and high > prevSwingHigh
    detectSMT()
```

Exception: PSP instant detection intentionally runs without `barstate.isconfirmed`
to avoid one-bar lag on opposing close signals. Document this in a comment.

### 2.5 xloc.bar_time — Use for Line Drawing Across Timeframes
When plotting lines using HTF data on LTF charts, always use `xloc.bar_time`
not `xloc.bar_index`.

```pine
// ✅ CORRECT — works across timeframes
line.new(x1=time[1], y1=swingHigh, x2=time, y2=swingHigh,
         xloc=xloc.bar_time, color=color.green)
```

### 2.6 var vs. Non-var Declarations
- Use `var` for values that must persist across bars (accumulators, swing trackers, line objects).
- Do NOT use `var` for values that should reset each bar.

```pine
var float swingHigh = na        // ✅ persists
var int   swingHighBar = na     // ✅ persists
float currentRange = high - low // ✅ recalculates every bar (no var)
```

### 2.7 Anti-Repaint HTF Engine (Detection vs. Reference Data)
When mapping HTF data to LTF for **detection engines** (SMT, swing breaks), NEVER
request live/forming candles. Always request **closed** candles to guarantee 0% repainting:

```pine
// ❌ WRONG — uses live forming candle, REPAINTS
[htf_h, htf_l] = request.security(sym, "240", [high, low])

// ✅ CORRECT — uses last CLOSED candle, no repaint
[htf_h, htf_l] = request.security(sym, "240", [high[1], low[1]],
    barmerge.gaps_off, barmerge.lookahead_off)
```

Use `ta.change(time("240")) != 0` to detect the exact LTF bar where the HTF candle
closed, and trigger drawings ONLY on that boundary:

```pine
bool htfClosed = ta.change(time("240")) != 0
if htfClosed and barstate.isconfirmed
    // Safe to draw/detect — HTF bar just confirmed
```

**Exception:** For **reference data** (PDH/PDL, ADR) that anchors to daily close,
`lookahead=barmerge.lookahead_on` with `[1]` is correct (see sections 8–9).

### 2.8 Array Garbage Collection (Prevent TradingView Crashes)
TradingView crashes if drawing arrays grow unbounded. When creating dynamic visuals
(`line.new`, `label.new`, `box.new`), ALWAYS push the ID to an array and clean up:

```pine
var line[] smtLines = array.new_line()
var int MAX_LINES = 50  // match max_lines_count budget

// After creating a line:
array.push(smtLines, newLine)

// Immediately garbage collect:
if array.size(smtLines) > MAX_LINES
    line.delete(array.shift(smtLines))
```

Do this for EVERY drawing type. Forgetting this is the #1 cause of
`"Drawing objects limit exceeded"` crashes.

### 2.9 Lookahead Decision Matrix
`lookahead` is the most misused parameter in Pine Script. Wrong choice = repaint.

| Data Type | `[1]`? | `lookahead` | `gaps` | Why |
|-----------|--------|-------------|--------|-----|
| **Detection engine** (SMT, swing breaks) | Yes | `barmerge.lookahead_off` | `barmerge.gaps_off` | Detection MUST NOT see future data |
| **Reference data** (PDH/PDL, ADR) | Yes | `barmerge.lookahead_on` | – | Static historical value, `[1]` makes it safe |
| **Live HTF data** (current candle range) | No | `barmerge.lookahead_on` | – | CDR needs today's live high/low |

**Rule of thumb:** If the data drives a SIGNAL → `lookahead_off`. If the data is a
static REFERENCE level → `lookahead_on` + `[1]` is safe.

```pine
// ✅ Detection engine — strict anti-repaint
[c1_pdh, c1_pdl] = request.security(sym1, "1D", [high[1], low[1]],
    barmerge.gaps_off, barmerge.lookahead_off)

// ✅ Reference level — static yesterday's data
float pdHigh = request.security(syminfo.tickerid, "D", high[1],
    lookahead=barmerge.lookahead_on)

// ✅ Live data — current day's running high
float todayHigh = request.security(syminfo.tickerid, "D", high,
    lookahead=barmerge.lookahead_on)
```

---

## 3. SMT DETECTION — LOGIC RULES (GxT Framework)

### 3.1 Swing SMT vs. SSMT — Know the Difference

| Type       | What it is                                      | Timeframe  |
|------------|-------------------------------------------------|------------|
| Swing SMT  | Divergence at confirmed swing H/L only          | Any        |
| SSMT       | Divergence between two adjacent confirmed candles | 90m+     |

Both are valid signals per GxT (confirmed by Garrett).
Never treat SSMT as a "weaker" version — it's a different signal type.

### 3.2 Swing Confirmation Rule
A swing high/low is only valid when the NEXT bar closes below/above it.
Never mark a swing on the same bar it forms.

```pine
// Swing High confirmed on bar AFTER the peak
isSwingHigh = high[1] > high[0] and high[1] > high[2] and barstate.isconfirmed
```

### 3.3 Equal High/Low Rejection
SMT requires a CLEAR divergence. Equal highs/lows between assets = no signal.
Always add a tolerance buffer.

```pine
float tolerance = syminfo.mintick * 2
bool isHigherHigh  = assetA_high > prevHigh + tolerance
bool isEqualHigh   = math.abs(assetA_high - prevHigh) <= tolerance  // reject this
```

### 3.4 Candidate Overwrite Bug — Common Pitfall
When tracking swing candidates across bars, the most common bug is overwriting a
valid candidate before it's confirmed.

```pine
// ❌ WRONG — overwrites candidate every bar
swingCandidate = high

// ✅ CORRECT — only update when a genuinely new candidate appears
if high > ta.highest(high, 5)[1]
    swingCandidate := high
    swingCandidateBar := bar_index
```

### 3.5 Slow Rollover Confirmation Bug
After detecting an SMT candidate, confirmation should happen exactly one bar later.
Do not use a flag that stays true for multiple bars.

```pine
// ✅ Use a one-shot confirmation pattern
var bool smtPending = false
var int  smtPendingBar = na

if smtConditionMet and barstate.isconfirmed
    smtPending    := true
    smtPendingBar := bar_index

if smtPending and bar_index == smtPendingBar + 1 and barstate.isconfirmed
    triggerSMT()
    smtPending := false  // reset immediately
```

### 3.6 Correlated Asset Timing Offset
When comparing two assets via `request.security()`, both calls must use the same
timeframe and the same bar reference. Mixing `[0]` and `[1]` is the #1 cause of
false positives.

```pine
// ✅ Both assets at same bar reference
[htf_h_A, htf_l_A] = request.security(assetA, htfTF, [high[0], low[0]])
[htf_h_B, htf_l_B] = request.security(assetB, htfTF, [high[0], low[0]])
```

### 3.7 Inverse Correlation Pattern
Some asset pairs are inversely correlated (e.g., DXY vs Gold, VIX vs Equities).
For inverse assets, SMT fires when they move in the SAME direction (unexpected),
not opposite. Use a boolean toggle to flip divergence logic:

```pine
sym3_inv = input.bool(false, title="↕ Inverse",
     tooltip="ON: Asset 3 is treated as INVERSELY correlated — SMT fires when " +
             "it moves in the SAME direction as the main chart.")

check_smt(use_asset, c_h, c_l, is_inv) =>
    is_bear = false
    if use_asset
        // Normal: diverge (one up, one down) = SMT
        // Inverse: converge (both same direction) = SMT
        bear_cond = is_inv
             ? ((high > high[1] and c_h > c_h[1]) or
                (high < high[1] and c_h < c_h[1]))
             : ((high > high[1] and c_h < c_h[1]) or
                (high < high[1] and c_h > c_h[1]))
        if bear_cond
            is_bear := true
    is_bear
```

Pass `false` for normally correlated assets, `true` for inverse.
NEVER hardcode the correlation direction — always make it an input toggle.

### 3.8 SSMT HTF-to-LTF Implementation Pattern
SSMT compares TWO CONSECUTIVE COMPLETED HTF candles from an LTF chart.
This is the hardest pattern to implement correctly.

**Step 1 — Detect HTF candle boundary:**
```pine
bool htfClosed = ta.change(time(htfTF)) != 0
```

**Step 2 — Store the last two completed HTF candles in `var` registers:**
```pine
var float htf_prev_h = na, var float htf_prev_l = na
var float htf_curr_h = na, var float htf_curr_l = na
var float htf_run_h  = na, var float htf_run_l  = na  // running accumulator

if htfClosed
    // Shift: current becomes previous
    htf_prev_h := htf_curr_h
    htf_prev_l := htf_curr_l
    // Finalize: running accumulator becomes current
    htf_curr_h := htf_run_h
    htf_curr_l := htf_run_l
    // Reset running accumulator for new HTF candle
    htf_run_h  := high
    htf_run_l  := low
else
    // Update running accumulator every LTF bar
    htf_run_h := math.max(nz(htf_run_h, high), high)
    htf_run_l := math.min(nz(htf_run_l, low),  low)
```

**Step 3 — Compare on boundary bar only:**
```pine
if htfClosed and barstate.isconfirmed
    // SSMT bearish: Asset A made higher high, Asset B didn't (or vice versa)
    if htf_curr_h > htf_prev_h and assetB_curr_h < assetB_prev_h
        // SSMT detected — draw compact markers at HTF boundary
```

**Critical:** Do NOT use `request.security()` for this — the LTF accumulator
approach is more accurate because it captures exact intrabar extremes.

---

## 4. MULTI-ASSET ARCHITECTURE

### 4.1 All Pair Combinations (AvB, AvC, BvC)
For 3 assets, always check all 3 pairs. Never skip pairs silently.

```pine
// Asset index pairs: (0,1), (0,2), (1,2)
var int[][] pairs = array.from(
    array.from(0, 1),
    array.from(0, 2),
    array.from(1, 2)
)
```

### 4.2 Security Call Budget
TradingView allows a limited number of `request.security()` calls.
With 3 assets × 2 timeframes (4H + 7H) + symbol data = budget fills fast.
Use tuple fetching (section 2.3) religiously. Bundle all needed OHLC in one call.

### 4.3 Custom Timeframe: 7H = 420 Minutes
The 7H timeframe doesn't exist natively. Always use `"420"` (minutes string).

```pine
string TF_7H = "420"
[o, h, l, c] = request.security(syminfo.tickerid, TF_7H, [open, high, low, close])
```

---

## 5. FVG / OB ENGINE

### 5.1 FVG Extension Logic
A common bug: FVG extension lines update every bar, causing them to shift visually.
Lock the line's x2 to `bar_index + N` only on creation, then only extend if price
hasn't mitigated yet.

```pine
// ✅ Only extend if FVG is still valid (not mitigated)
if not fvgMitigated and barstate.isconfirmed
    line.set_x2(fvgLine, bar_index + extensionBars)
```

### 5.2 Mitigation Check
FVG is mitigated when price closes inside the gap.

```pine
fvgMitigated := close >= fvgLow and close <= fvgHigh
```

### 5.3 CSD / OB Continuation Logic
A Change in State of Delivery flips the bias. Track the most recent CSD per side.
Do not stack multiple unresolved OBs without a priority/recency rule.

### 5.4 Auto-Sweep Cleanup Pattern (Institutional Levels)
For any horizontal level that should disappear when price sweeps through it
(Devil's Mark, liquidity targets, OB levels), use parallel arrays to track
the level value and creation bar, then delete on sweep:

```pine
var line[]  dm_lines  = array.new_line()
var float[] dm_levels = array.new_float()
var int[]   dm_bars   = array.new_int()    // creation bar — skip instant deletion

// ── Creation (on barstate.isconfirmed) ───────────────────
if is_flat_top and barstate.isconfirmed
    ln = line.new(bar_index, high, bar_index + extend, high, ...)
    array.push(dm_lines, ln)
    array.push(dm_levels, high)
    array.push(dm_bars, bar_index)

// ── Sweep Detection (every bar) ─────────────────────────
i = array.size(dm_lines) - 1
while i >= 0
    lvl   = array.get(dm_levels, i)
    c_bar = array.get(dm_bars, i)
    // Only check AFTER creation bar to prevent instant kill
    if bar_index > c_bar
        is_swept = (high >= lvl and low <= lvl)  // wick through = swept
        if is_swept
            line.delete(array.get(dm_lines, i))
            array.remove(dm_lines, i)
            array.remove(dm_levels, i)
            array.remove(dm_bars, i)
    i -= 1
```

**Key rule:** Always check `bar_index > c_bar` to prevent the creation candle
itself from triggering the sweep (the level IS the candle's high/low).

---

## 6. VISUAL OUTPUT STANDARDS

### 6.1 SMT Line Style Convention
- **Swing SMT** → solid line (`line.style_solid`)
- **SSMT / Candle SMT** → dashed line (`line.style_dashed`)
- **Bullish** → green (`color.new(color.green, 0)`)
- **Bullish weak** → lighter green (`color.new(color.green, 50)`)
- **Bearish** → red
- **Bearish weak** → lighter red

### 6.2 Labels
Label format: `[TF] [Type] [Direction]`
Example: `"4H SMT Bear"`, `"7H SSMT Bull"`, `"4H Swing SMT Bear"`

### 6.3 Background Shading
Use `bgcolor()` only when HTF SMT is ACTIVE (not just detected).
Green shade = bullish HTF active. Red shade = bearish HTF active.
Always use transparency (e.g., `color.new(color.green, 85)`).

### 6.4 Info Table
Place dashboard table at `position.top_right`.
Always include: Asset names, current HTF bias, last SMT type, last SMT TF.

```pine
var table infoTable = table.new(position.top_right, 2, 5,
    border_width=1, border_color=color.gray)
```

---

## 7. SESSION / KILLZONE MARKERS

Sessions to support: London (02:00–05:00 EST), NY AM (08:30–11:00 EST),
NY Lunch (11:30–13:00 EST), NY PM (13:30–16:00 EST).

```pine
// Convert to UTC for session strings
bool isLondon = not na(time("1", "0200-0500", "America/New_York"))
bool isNYAM   = not na(time("1", "0830-1100", "America/New_York"))
```

Always make sessions optional with input toggles.

---

## 8. ATR / ADR / CDR DASHBOARD

### ATR
```pine
float atrValue = ta.atr(atrLength)
```

### ADR (Average Daily Range)
```pine
float dailyHigh  = request.security(syminfo.tickerid, "D", high[1], lookahead=barmerge.lookahead_on)
float dailyLow   = request.security(syminfo.tickerid, "D", low[1],  lookahead=barmerge.lookahead_on)
float adr        = ta.sma(dailyHigh - dailyLow, adrLength)
```

### CDR (Current Day Range)
```pine
float todayHigh = request.security(syminfo.tickerid, "D", high,  lookahead=barmerge.lookahead_on)
float todayLow  = request.security(syminfo.tickerid, "D", low,   lookahead=barmerge.lookahead_on)
float cdr       = todayHigh - todayLow
```

Always show as price units, not ticks.

---

## 9. PDH / PDL

Two approaches — both correct, choose one per codebase:

```pine
// Approach A: lookahead_on (simpler, safe with [1])
float pdHigh = request.security(syminfo.tickerid, "D", high[1],
    lookahead=barmerge.lookahead_on)

// Approach B: lookahead_off (stricter, used in CIC-PRO)
[pdHigh, pdLow] = request.security(syminfo.tickerid, "1D", [high[1], low[1]],
    barmerge.gaps_off, barmerge.lookahead_off)
```

Both are safe when using `[1]`. Approach B is preferred when the same security call
also feeds detection engines (keeps all calls consistent).

### 9.1 Multi-Asset PDH/PDL "Level Taken" Dashboard
For dashboards showing if each asset has taken its PDH/PDL today:

```pine
// Track each asset's intraday high/low with var accumulators
var float c1_day_hi = na, var float c1_day_lo = na
if is_new_day
    c1_day_hi := c1_h, c1_day_lo := c1_l
else
    if c1_h > c1_day_hi
        c1_day_hi := c1_h
    if c1_l < c1_day_lo
        c1_day_lo := c1_l

// Compare: has today's action reached yesterday's extreme?
c1_pdh_taken = not na(c1_pdh) and c1_day_hi >= c1_pdh
c1_pdl_taken = not na(c1_pdl) and c1_day_lo <= c1_pdl

// Display in table with ✓/✗ and conditional colors
table.cell(tbl, col, row,
     c1_pdh_taken ? "✓" : "✗",
     text_color = c1_pdh_taken ? color.green : color.red)
```

---

## 10. ALERTS

Every indicator should have named alert conditions at the bottom.
Use descriptive names — not "Alert 1".

```pine
alertcondition(bullSMT_4H,   title="4H Bullish SMT",   message="4H Bullish SMT detected on {{ticker}}")
alertcondition(bearSMT_4H,   title="4H Bearish SMT",   message="4H Bearish SMT detected on {{ticker}}")
alertcondition(bullSSMT_7H,  title="7H Bullish SSMT",  message="7H Bullish SSMT detected on {{ticker}}")
alertcondition(bearSSMT_7H,  title="7H Bearish SSMT",  message="7H Bearish SSMT detected on {{ticker}}")
```

---

## 11. CODE STRUCTURE TEMPLATE

Always structure scripts in this order:

```pine
//@version=6
indicator("Indicator Name", overlay=true, max_lines_count=500, max_labels_count=500)

// ─── INPUTS ──────────────────────────────────────────────────────────
// All user inputs grouped here (unique group names)

// ─── CONSTANTS ────────────────────────────────────────────────────────
// Timeframes, colors, style constants

// ─── SECURITY CALLS ───────────────────────────────────────────────────
// All request.security() calls grouped, using tuples
// Alert trigger booleans initialized here (false)

// ─── ENGINE 1: PSP ────────────────────────────────────────────────────
// Precision Swing Point detection

// ─── ENGINE 2: SMT / SSMT ─────────────────────────────────────────────
// Swing SMT + Consecutive SMT + Early Instant detection

// ─── ENGINE 3: FVG / OB ──────────────────────────────────────────────
// Fair Value Gaps, Order Blocks (if applicable)

// ─── SESSION & OPEN MARKERS ──────────────────────────────────────────
// Killzones, 6PM/12AM opens, session H/L tracking

// ─── REFERENCE LEVELS ─────────────────────────────────────────────────
// PDH/PDL, Weekly Open, HTF separators

// ─── OPENING GAPS (NWOG / NDOG) ──────────────────────────────────────
// ICT opening gap detection + CE lines

// ─── DASHBOARDS ───────────────────────────────────────────────────────
// ADR/CDR table, PDH/PDL status table, info table

// ─── DEVIL'S MARK / PRECISION TARGETS ────────────────────────────────
// Wickless candle targets with auto-sweep cleanup

// ─── CONFLUENCE MEMORY ENGINE ─────────────────────────────────────────
// PSP + SMT alignment detection within N-bar window

// ─── ALERTS ───────────────────────────────────────────────────────────
// All alertcondition() calls — confluence first, then individual
```

---

## 12. PRE-SUBMIT CHECKLIST

Before handing back code, mentally run through this:

**Syntax & Structure:**
- [ ] All variables declared ABOVE where they are used (top-down rule)
- [ ] No duplicate function names, variable names, or input group titles
- [ ] All bool comparisons explicit (`!= 0`, `== true`, etc.)
- [ ] Code sections separated with comment headers

**Security Calls & Anti-Repaint:**
- [ ] All `request.security()` using tuple fetch
- [ ] HTF detection engines use `[1]` + `lookahead_off` (anti-repaint)
- [ ] Reference data (PDH/PDL/ADR) uses correct lookahead per §2.9 matrix
- [ ] Both assets using same bar reference `[0]` in security calls
- [ ] 7H timeframe using `"420"` string

**Detection Logic:**
- [ ] `barstate.isconfirmed` on every detection block (except PSP instant)
- [ ] `ta.change(time())` used to detect HTF bar boundaries on LTF
- [ ] Swing confirmation happening on bar AFTER the peak/trough
- [ ] Equal high/low rejection added with tolerance
- [ ] Candidate overwrite protection in place
- [ ] SMT pending flag resets immediately after triggering
- [ ] Inverse correlation toggle (`sym_inv`) for inverse assets

**Drawing & Memory:**
- [ ] All drawing arrays have garbage collection loops
- [ ] Auto-sweep cleanup checks `bar_index > c_bar` (skip creation bar)
- [ ] Lines using `xloc.bar_time` if crossing timeframes

**Alerts & Confluence:**
- [ ] Confluence memory registers reset after fire (prevent spam)
- [ ] All alerts named descriptively with direction + type
- [ ] Confluence alerts listed first, individual signals second

---

## 13. COMMUNICATION RULES (FOR THIS USER)

- User knows GxT concepts deeply. Never over-explain SMT, PSP, CIC, SSMT.
- Use term **SMT** (not CIC01), **2-stage SMT** (not CIC03), **PSP** for opposing close.
- Keep responses mobile-friendly and concise.
- Always confirm trading logic in plain language BEFORE writing code.
- For surgical edits: show only the changed function/block, not the whole file.
- For full rewrites: provide complete script.
- When debugging: state what the bug is and WHY it happens before fixing it.

---

## 14. CONFLUENCE / MULTI-SIGNAL MEMORY ENGINE

The highest-value alert is NOT individual PSP or SMT — it's when BOTH align
within a configurable window. This is the institutional confluence signal.

### 14.1 Architecture
```pine
// ── Directional Memory Registers ────────────────────────
var int last_psp_bull_bar = na
var int last_psp_bear_bar = na
var int last_smt_bull_bar = na
var int last_smt_bear_bar = na

conf_window = input.int(3, "Confluence Memory Window (bars)", minval=0, maxval=10)
conf_reset  = input.bool(true, "Auto-Reset After Fire")

// ── Update registers when signals fire ──────────────────
if psp_bull_trigger
    last_psp_bull_bar := bar_index
if smt_bull_trigger
    last_smt_bull_bar := bar_index
// (same for bearish)
```

### 14.2 Window-Based Overlap Detection
```pine
// NA-safe window check
bull_psp_in_window = not na(last_psp_bull_bar) and
     (bar_index - last_psp_bull_bar) <= conf_window
bull_smt_in_window = not na(last_smt_bull_bar) and
     (bar_index - last_smt_bull_bar) <= conf_window

// Confluence fires when EITHER new signal finds the other still in window
bullish_confluence = (psp_bull_trigger and bull_smt_in_window) or
                     (smt_bull_trigger and bull_psp_in_window)
```

### 14.3 Consumption Reset (Anti-Spam)
```pine
if conf_reset and bullish_confluence
    last_psp_bull_bar := na   // Clear both registers
    last_smt_bull_bar := na   // One setup = exactly one alert
```

**Why `conf_window = 3`?** PSP and SMT are architecturally 1–2 bars apart
(PSP fires on the swing candle, SMT fires when divergence is confirmed one
bar later). A 3-bar window captures this natural offset.

### 14.4 Alert Hierarchy
Always order alerts: Confluence → Individual → Consecutive.
```pine
alertcondition(any_confluence,     title="⭐ Confluence (Any)", ...)
alertcondition(bullish_confluence, title="⭐ Bullish Confluence", ...)
alertcondition(bearish_confluence, title="⭐ Bearish Confluence", ...)
alertcondition(any_psp_trigger,    title="🔔 Any PSP", ...)
alertcondition(any_smt_trigger,    title="🔔 Any SMT", ...)
alertcondition(cons_smt_bull,      title="📊 Consecutive SMT (Bull)", ...)
alertcondition(cons_smt_bear,      title="📊 Consecutive SMT (Bear)", ...)
```

---

## 15. OPENING GAP ENGINE (NWOG / NDOG)

ICT defines opening gaps as the price difference between the institutional
settlement close (5:00 PM NY) and the reopen (6:00 PM NY).

### 15.1 Session-Based Detection (TF ≤ 1H)
For forex and metals (24/5 markets), the only true "gap" is the 1-hour
settlement window. Use `hour(time, tz)` for precise detection:

```pine
og_tz = "America/New_York"
og_bar_hour = hour(time, og_tz)
og_bar_dow  = dayofweek(time, og_tz)

// Track 5 PM close: capture close of bars between 3-5 PM NY
var float og_5pm_close = na
if og_bar_hour >= 15 and og_bar_hour < 17
    og_5pm_close := close

// Detect 6 PM open: first bar in 18:00-19:59 zone
var bool og_prev_in_6pm = false
og_in_6pm = og_bar_hour >= 18 and og_bar_hour < 20
og_is_6pm_new = og_in_6pm and not og_prev_in_6pm
og_prev_in_6pm := og_in_6pm

// Classify: Sunday 6PM = NWOG, Mon-Thu 6PM = NDOG
og_trigger_nwog = og_is_6pm_new and og_bar_dow == dayofweek.sunday
og_trigger_ndog = og_is_6pm_new and not og_trigger_nwog
```

### 15.2 Fallback Detection (TF > 1H)
On daily/4H charts, a single bar spans both 5PM and 6PM, so session detection
fails. Fall back to bar-boundary changes:

```pine
og_fb_new_week = ta.change(time("1W")) != 0
og_fb_new_day  = ta.change(time("1D")) != 0
```

### 15.3 Gap Box with CE (Consequent Encroachment)
CE is the 50% midpoint — the most reactive level within the gap:

```pine
nw_hi = math.max(og_5pm_close, open)
nw_lo = math.min(og_5pm_close, open)
nw_ce = (nw_hi + nw_lo) / 2.0

b  = box.new(bar_index - 1, nw_hi, bar_index + 20, nw_lo,
     bgcolor=gap_color, border_width=0, text="NWOG")
ce = line.new(bar_index - 1, nw_ce, bar_index + 20, nw_ce,
     color=ce_color, style=line.style_dotted)
```

### 15.4 Auto-Fill Deletion
Optionally remove gap boxes when price closes through the full range:

```pine
is_filled = (direction == 1 and close <= gap_bottom) or
            (direction == -1 and close >= gap_top)
if is_filled and og_auto_delete
    box.delete(b), line.delete(ce)
```

---

## 16. GxT / ICT CONCEPT REFERENCE (Garrett-Aligned)

Quick reference for GxT terms — definitions verified against Garrett (@GxTradez) content.

### 16.1 Core GxT Model Terms

| GxT Term | Full Name | Garrett's Definition |
|----------|-----------|---------------------|
| **SMT** | Smart Money **Technique** | When two correlated assets fail to confirm each other's price action at a swing H/L. One makes a new extreme, the other doesn't → institutional footprint. NOT "Smart Money Tool." |
| **CIC** | Crack in Correlation | The BROADER framework — a 3-tier model (CIC1, CIC2, CIC3). NOT just "same as SMT." |
| **CIC1** | Initial Crack | First structural divergence — one asset breaks a level, the other fails to. This is the initial PSP or reaction point. |
| **CIC2** | Confirmation Crack | SMT divergence confirms the CIC1 point. Higher confidence the reversal is valid. This is the "standard SMT" signal. |
| **CIC3** | Final Trigger / 2-Stage CIC | The continuation crack that precedes expansion. A true reversal = "two-stage CiC" where CIC1→CIC2 is confirmed by CIC3. |
| **PSP** | Precision Swing Point | Divergence in **candle closure** between correlated assets at a swing point. Example: at a swing high, Asset A's candle closes bullish (green) but Asset B closes bearish (red). The mixed closure = precision exhaustion point. Functions similarly to an order block. |
| **SSMT** | Sequential Smart Money Technique | SMT divergence between **two consecutive quarters/sessions** — NOT isolated swings. Governed by Quarterly Theory: "time governs price." Divergence must occur between consecutive time segments (90m quarters, daily sessions, weekly quarters). |

### 16.2 Quarterly Theory (Time Framework)

| Timeframe | Quarter Division | Examples |
|-----------|-----------------|----------|
| **Yearly** | 4 quarters × 3 months | Q1=Jan-Mar, Q2=Apr-Jun |
| **Monthly** | 4 quarters × ~1 week | Week 1-4 of the month |
| **Weekly** | 4 quarters × 1 day | Mon=Q1, Tue=Q2, Wed=Q3, Thu=Q4 (Fri is separate) |
| **Daily** | 4 quarters × 6 hours | Asia, London, NY AM, NY PM |
| **Session** | 4 quarters × 90 minutes | Each session splits into 90m segments |

**"Time governs price"** — SSMT filters standard SMTs through these time divisions.
When SMT divergence occurs between consecutive quarters, it signals a phase transition
(accumulation → manipulation → distribution → reversal).

### 16.3 Price Delivery Arrays

| Term | Full Name | Definition |
|------|-----------|-----------|
| **FVG** | Fair Value Gap | 3-candle imbalance where candle 1's wick and candle 3's wick don't overlap. Price is drawn back to fill/rebalance this inefficiency. |
| **OB** | Order Block | Last opposing-color candle before an impulsive move that breaks market structure. Bullish OB = last red candle before rally. |
| **CE** | Consequent Encroachment | 50% midpoint (equilibrium) of any FVG, OB, or gap zone. The most reactive level — price is magnetically drawn here. |
| **CSD** | Change in State of Delivery | When price delivery shifts from buy-side to sell-side or vice versa. Flips the directional bias. |

### 16.4 Institutional Reference Levels

| Term | Full Name | Definition |
|------|-----------|-----------|
| **NWOG** | New Week Opening Gap | Gap between Friday 5:00 PM NY close and Sunday 6:00 PM NY open. A liquidity void that acts as a magnet for price rebalancing. |
| **NDOG** | New Day Opening Gap | Gap between Mon-Thu 5:00 PM NY close and 6:00 PM NY open. The 1-hour settlement window — the only "gap" in 24/5 forex. |
| **PDH/PDL** | Previous Day High/Low | Yesterday's extremes — institutional reference for daily liquidity targets. |
| **D.M** | Devil's Mark | HTF candle with NO wick on one side (open == high or open == low). "Incomplete" candle — price is expected to return to "print the wick." |
| **ADR** | Average Daily Range | N-day average of daily range — used for target projection. |
| **CDR** | Current Day Range | Today's running high minus low — tracked against ADR for exhaustion signals. |

### 16.5 GxT Terminology Mapping (What to Say)

| ✅ Use This | ❌ Not This | Why |
|-------------|------------|-----|
| SMT | CIC01 | Garrett uses "SMT" in conversation |
| 2-Stage CIC | CIC03 | Correct GxT model term |
| PSP | Precision Candle | PSP is the swing-level concept, Precision Candle is the individual candle |
| SSMT | Consecutive SMT | SSMT emphasizes the time-governed (Quarterly Theory) aspect |
| CE | Midpoint | CE is the ICT-specific term for the 50% level |
| D.M | Wickless candle | D.M is the GxT-specific term |

---

## 17. INDICATOR DEVELOPMENT WORKFLOW

### 17.1 Planning Phase (Before Writing Code)

| # | Question | Example Answer |
|---|----------|---------------|
| 1 | What signal? | PSP + SMT confluence alerts |
| 2 | What TFs? | 15m chart, detecting on 4H/Daily |
| 3 | How many assets? | 3 correlated + 1 inverse |
| 4 | Drawing budget? | ~200 lines, ~100 labels, ~50 boxes |
| 5 | Security calls? | 3 assets × 1 TF = 3 tuple calls (12 of 40 budget) |

### 17.2 Resource Limits (Hard Caps)

| Resource | Default | Max | Declaration |
|----------|---------|-----|-------------|
| Lines | 50 | 500 | `max_lines_count=500` |
| Labels | 50 | 500 | `max_labels_count=500` |
| Boxes | 50 | 500 | `max_boxes_count=500` |
| Polylines | 50 | 100 | `max_polylines_count=100` |
| Security calls | — | 40 | Cannot increase — budget carefully |

### 17.3 Build Sequence

```
1. SPEC        → Define signals, TFs, assets, drawing budget
2. SKELETON    → indicator() + inputs + security calls
3. ENGINE      → Detection systems (one at a time)
4. TEST        → Verify each engine in isolation
5. VISUALS     → Lines, labels, boxes
6. DASHBOARD   → Info tables
7. CONFLUENCE  → Multi-signal memory engine
8. ALERTS      → All alertcondition() calls
9. OPTIMIZE    → Pine Profiler → fix top 3 hotspots
10. POLISH     → Colors, tooltips, input organization
```

**Golden rule:** `Add Engine → Test Alone → Add Visual → Test Again → Integrate`

### 17.4 Performance Rules

| Rule | Why |
|------|-----|
| Update objects (`set_xy`) instead of recreating (`new`) | 10x faster |
| Wrap table updates in `if barstate.islast` | Prevents per-bar recalculation |
| Cap ALL drawing arrays with GC loops | Prevents crashes |
| Use `if show_feature` gates on every engine | Skip disabled features entirely |
| Avoid nested loops (O(n²)) — use single pass with early `break` | TradingView throttles slow scripts |
| Use `log.info()` for debugging, not `plot()` | Cleaner, no chart clutter |

---

## 18. UI DESIGN GUIDE (Pine Script v6)

### 18.1 Color Palette (Professional — NOT Amateur)

```pine
// ❌ NEVER use raw colors — they look amateur
color.red, color.green, color.blue

// ✅ Use curated hex colors
color_bull     = color.new(#26a69a, 0)    // teal green
color_bear     = color.new(#ef5350, 0)    // soft red
color_neutral  = color.new(#787b86, 0)    // TradingView grey
color_accent   = color.new(#1e88e5, 0)    // blue accent
color_bg_dark  = color.new(#1a1a2e, 10)   // dashboard bg
```

### 18.2 Dashboard Design Rules

| Rule | Implementation |
|------|---------------|
| Dark theme by default | `bgcolor=color.new(#1a1a2e, 10)` |
| Test on light theme too | Check contrast on both |
| Left-align labels | `text_halign=text.align_left` |
| Right-align numbers | `text_halign=text.align_right` |
| Zebra stripe rows | Alternate `bgcolor` per row |
| Only update on last bar | `if barstate.islast` gate |
| Use ✓/✗ symbols | Cleaner than "Yes"/"No" text |
| Conditional colors | Green for taken, red for not taken |

### 18.3 Input Settings Best Practices

| Pattern | Example |
|---------|---------|
| Group related inputs | `group=grp_main` |
| Put colors on same row | `inline="colors"` |
| Add rich tooltips | `tooltip="ON: Does X.\nOFF: Does Y."` |
| Use descriptive titles | "Show NWOG (New Week Opening Gap)" not "Show Feature 1" |
| Unique group names | `grp_fvg`, `grp_smt_f`, `grp_sessions` — never duplicate |

### 18.4 Line Style Convention

| Signal Type | Style | Width |
|-------------|-------|-------|
| Confirmed signal (swing SMT) | `solid` | 2 |
| Sequential signal (SSMT) | `dashed` | 2 |
| Reference level (PDH/PDL) | `dotted` | 1 |
| Target projection (D.M, ATR) | `dashed` | 1 |
| CE midpoint | `dotted` | 1 |

### 18.5 Transparency Guide

| Use Case | Transparency | Effect |
|----------|-------------|--------|
| Zone fill (FVG, gap box) | 85% | Subtle background — doesn't obscure candles |
| Label border (invisible tooltip) | 100% | Fully invisible — data only in tooltip |
| Active line (signal) | 0% | Full opacity — demands attention |
| Inactive/historical line | 40-60% | Faded — context without clutter |
| Session background | 92-95% | Barely visible tint — session separation |

