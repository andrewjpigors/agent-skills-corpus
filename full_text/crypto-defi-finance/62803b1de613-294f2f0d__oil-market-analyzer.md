---
name: oil-market-analyzer
description: Analyzes the oil market for equities traders using the Bouchouev storage-capacity-utilization model, futures curve structure, inventory dynamics, shock classification, and geopolitical risk assessment. Frames market conditions and oil-related equity sub-sector sensitivities (E&P, refiners, midstream, oilfield services, integrated majors) for educational analysis. Use when user says "analyze oil", "oil market", "crude oil", "WTI", "Brent", "oil inventory", "oil spreads", "contango", "backwardation", "oil equities", "energy sector", "oil squeeze", "storage capacity", "OPEC", "oil stocks", or asks about oil market conditions, energy sector positioning, or crude oil prices. Do NOT use for precious metals, natural gas standalone analysis, cryptocurrency, or individualized investment recommendations.
---

# Oil Market Analysis for Equities Traders

## Important Disclaimer

**This skill provides educational oil market analysis frameworks only. It does NOT provide financial advice, investment recommendations, or trading signals. All analysis is probabilistic, not predictive. Users must make their own investment decisions and accept full responsibility for any trades. Past patterns do not guarantee future results. Oil markets are highly volatile and subject to geopolitical shocks that no model can anticipate.**

## Instructions

When the user requests an oil market analysis, follow this structured multi-step workflow. The methodology is grounded in Bouchouev's storage-capacity-utilization framework, which models WTI futures spreads as a financial derivative of the observable state variable: storage capacity utilization. This practical approach bypasses the limitations of the canonical theory of storage (inelastic supply/demand, unobservable demand curves) and focuses on what can be measured and traded.

### Methodology Guardrails

Use the Bouchouev model as a high-value lens for **WTI prompt-spread squeeze risk**, not as a standalone model for the flat price of crude oil, Brent, global oil balances, or equity returns. It is a stylized model, not an econometrically rigorous forecasting system.

Always separate:
- **WTI spread stress:** Cushing utilization, prompt delivery constraints, storage economics, and financial squeeze risk
- **Flat-price regime:** global supply/demand, OPEC+, macro demand, geopolitics, USD/rates, and positioning
- **Equity translation:** company balance sheets, hedge books, cost curves, crack spreads, interest rates, shareholder returns, and technical leadership

When signals conflict, do not smooth them into a single confident verdict. Call out the conflict and lower confidence.

### Step 1: Determine Analysis Scope

Ask the user (if not already clear):
1. **What is the analysis goal?** Market overview, specific equity analysis, sector rotation, or spread-trade context
2. **What timeframe?** Tactical (days-weeks), positional (weeks-months), or strategic (months-quarters)
3. **What oil-related equities are they considering?** E&P, refiners, midstream/pipelines, oilfield services, integrated majors, or ETFs (XLE, OIH, XOP, etc.)
4. **Do they have access to current data?** If so, request: WTI/Brent front-month prices, nearby futures spread (F1-F2), contract month/roll date, Cushing inventory levels, Cushing working capacity and source date, weekly EIA data, OVX, WTI-Brent spread, crack spreads, and any equities or ETFs under review

If the user provides data, incorporate it directly. If not, guide them on where to find it and provide the analytical framework they should apply to that data.

### Step 1A: Data Quality and Scope Gate

Before deriving a signal, state the quality of the input data:
- **Market and benchmark:** WTI or Brent? If WTI, is Cushing the relevant delivery constraint? If Brent, do not over-apply Cushing utilization.
- **Release freshness:** EIA weekly release date, COT report date, OPEC/IEA report dates, and whether any source is stale.
- **Capacity denominator:** Cushing working storage capacity data may be stale or discontinued in public EIA reporting. If capacity is not current, label utilization as approximate.
- **Contract timing:** Prompt-month contract, days to expiry, roll timing, and whether F1-F2 is distorted by expiry mechanics.
- **Equity scope:** Sub-sector, ticker, ETF, and timeframe. Do not infer individual-stock conclusions from macro oil data alone.

### Step 2: Macro Oil Market Context (Forest Before Trees)

Before analyzing any oil equity, assess the overall oil market environment. This parallels Weinstein's "Forest to Trees" hierarchy, adapted for oil:

1. **Global Oil Regime (Forest):**
   - Is the oil market in surplus (builds), balance, or deficit (draws)?
   - What is OPEC+ doing? (Cutting, holding, or increasing production quotas)
   - Are there active geopolitical risk premiums? (Middle East tensions, sanctions, shipping disruptions)
   - What is the demand trajectory? (Global GDP growth, China demand, seasonal patterns, energy transition pressures)

2. **Futures Curve Structure (Trees):**
   - **Backwardation** (front > deferred): Market is tight, drawing inventories. Bullish for spot, signals supply deficit.
   - **Contango** (front < deferred): Market is oversupplied, building inventories. The spread should roughly equal the cost of storage when in normal contango.
   - **Super contango**: Storage capacity is under stress. Major red flag per Bouchouev's model -- proximity to the upper capacity boundary.
   - **Extreme backwardation**: Potential supply squeeze. Proximity to lower inventory boundary (stock-out risk).

3. **Shock Classification:** Identify the dominant driver before translating oil conditions into equity implications. Use the Kilian-style distinction between:
   - current physical supply shock (production outage or surprise supply)
   - aggregate demand shock (global growth, industrial activity, China/India demand)
   - precautionary/oil-specific demand shock (geopolitical risk premium, uncertainty about future availability)
   - storage squeeze shock (Cushing or other delivery/storage constraint)
   - financial/liquidity shock (forced futures liquidation, ETF/OTC product mechanics, margin stress)

4. **The Equity Sector (Leaves):** Only then assess individual oil equities or sub-sectors.

**CRITICAL:** Oil equities are leveraged bets on oil prices. The macro oil environment dominates individual stock selection. Even the best-managed E&P company will underperform in a collapsing oil price regime.

### Step 3: Storage Capacity Utilization Assessment (The Bouchouev Framework)

This is the core analytical engine. Consult `references/storage-model.md` for the full theoretical framework.

**The State Variable: x(t) = Inventory / Capacity**

Storage capacity utilization is the single most important observable variable for WTI prompt-spread squeeze analysis. It helps assess:
- The probability of extreme price events (squeezes)
- The non-linear behavior of futures spreads
- The risk/reward asymmetry for both long and short positions

Do not treat Cushing utilization as a complete proxy for global crude scarcity. Cushing matters directly for physically delivered WTI futures, but Brent, seaborne crude, Gulf Coast export economics, refinery demand, and alternative storage locations can diverge from Cushing.

**Classify the Current Regime:**

| Utilization Zone | Range | Spread Behavior | Market Regime | Equity Implication |
|-----------------|-------|-----------------|---------------|-------------------|
| Critical Low | < 25% | Extreme backwardation | Supply squeeze risk | Supports E&P sensitivity; pressures crude-input businesses |
| Low | 25-40% | Moderate backwardation | Supply-tight | Supports E&P and activity-sensitive services |
| Normal | 40-70% | Mild contango to mild backwardation | Balanced | Sector-neutral; prioritize relative strength and fundamentals |
| High | 70-85% | Moderate contango | Oversupplied | Pressures E&P; watch storage-linked midstream and refiner cracks |
| Critical High | > 85% | Super contango / tank-top risk | Storage squeeze risk | Pressures E&P and OFS; raises financial/liquidity risk |

These zones are heuristics. Treat them as approximate unless the capacity denominator and spread calibration are current.

**Key Insight (Bouchouev):** The relationship between spreads and inventories is highly non-linear near the boundaries. In the middle range (40-70% utilization), spreads are relatively insensitive to inventory changes. Near either boundary, small changes in inventory can create large spread moves -- the Dirac delta function behavior at the extremes.

**Forward-Looking Adjustment:**

The market does not trade on current inventories alone. It trades on *expected* inventories at the time of futures delivery. Assess:
- The recent slope of inventory builds/draws (momentum in the inventory trajectory)
- Whether the current trajectory, if extrapolated, approaches either capacity boundary
- Seasonal adjustments (refinery maintenance seasons, summer driving season, winter heating demand)

The extrapolation method: maintain the recent slope of inventory changes forward to the delivery date of the prompt futures contract. If this path approaches a boundary, the market will price in squeeze probabilities well before the event materializes.

### Step 4: Futures Curve Analysis

The futures curve encodes the market's collective expectation of future supply/demand balances, storage economics, risk premium, and carry. Analyze its shape and evolution without treating it as a reliable flat-price forecast.

**Spread Metrics:**
- **F1-F2 Spread (Calendar Spread):** The most liquid and informative for prompt WTI storage stress. Directly modeled as a function of storage capacity utilization when Cushing is the binding location.
- **Term Structure Slope:** Flat, steep, or kinked? A kink (e.g., backwardation in front, contango in deferred) signals a near-term supply issue the market expects to resolve.
- **Time Spread Changes:** Watch the rate of change -- a rapidly steepening contango is a stronger signal than the absolute level.

**Spread Interpretation (from the Bouchouev Model):**
```
S(t,x) = n(y - x_min, tau) - n(y - x_max, tau) - U
```

Where:
- The first term is the probability of a stock-out (upside squeeze) -- drives backwardation
- The second term is the probability of tank-tops (downside squeeze) -- drives contango
- U is the cost of storage
- The net spread reflects the *difference* between these two squeeze probabilities

**Practical Translation:**
- When inventories are low and trending lower, the stock-out probability dominates: spreads tend to move into backwardation. E&P equities often have positive sensitivity, but the equity conclusion still depends on shock type, company hedges, costs, and market trend.
- When inventories are high and trending higher, the tank-top probability dominates: spreads tend to move into contango. Storage and midstream companies may benefit, but E&P equities often face pressure.
- When inventories are mid-range, the spread is approximately the negative cost of storage (normal contango). This is the low-volatility, fair-value regime.

### Step 5: Volatility and Skew Assessment

Oil has a distinctive volatility structure that differs from most commodities. Consult `references/oil-market-indicators.md` for detail.

**Key Properties (from Bouchouev and related commodity volatility literature):**
- **Often negative price-volatility relationship:** Oil volatility frequently rises during sharp downside moves, especially in oversupply, storage-stress, and financial deleveraging regimes. Do not assume this relationship is stable in every supply-disruption regime.
- **Often negative skewness:** The oil price distribution can show strong negative skew. Downside risk is especially important in the post-shale era and in tank-top scenarios.
- **Mean-reverting implied volatility:** Implied volatility often decreases with time to maturity as short-term uncertainty dissipates. The variance of inventory deviations is bounded by the mean-reverting process.

**What This Means for Equities Traders:**
- Oil equity positions carry asymmetric downside risk. Position sizing must account for the fat left tail.
- Periods of low volatility and mid-range prices are *not* safe -- they can rapidly transition to high-volatility drawdowns.
- Protective strategies (stops, hedges, position limits) are more critical in oil equities than in many other sectors.
- The VIX-equivalent for oil (OVX) is a useful additional indicator.

### Step 6: Supply-Side Analysis

Evaluate the supply landscape:

**OPEC+ Dynamics:**
- Current production quotas and compliance levels
- Spare capacity (how much can OPEC ramp if needed?)
- Saudi Arabia's budget breakeven price (their incentive floor)
- Internal OPEC politics and cohesion

**Non-OPEC Supply (primarily U.S. Shale):**
- Rig count trends (Baker Hughes weekly data)
- DUC (Drilled but Uncompleted) wells inventory
- Shale breakeven costs by basin (Permian, Eagle Ford, Bakken)
- Capital discipline vs. growth mode among E&P companies
- Pipeline and takeaway capacity constraints

**Disruption Risk:**
- Geopolitical hotspots (Middle East, Russia/Ukraine, Libya, Venezuela, Nigeria)
- Weather-related risks (Gulf of Mexico hurricanes, extreme cold)
- Sanctions and their enforcement
- Shipping route disruptions (Strait of Hormuz, Red Sea/Suez, Strait of Malacca)

### Step 7: Demand-Side Analysis

Evaluate the demand landscape:

- **China:** Largest incremental demand driver. Track PMI, crude imports, refinery throughput, strategic petroleum reserve activity
- **U.S.:** Gasoline demand (weekly EIA data), jet fuel recovery, petrochemical feedstock demand
- **India:** Growing demand center. Refinery capacity expansion
- **Europe:** Declining structural demand (energy transition), but still significant in absolute terms
- **Seasonal Patterns:** Refinery turnaround season (spring/fall), summer driving season, winter heating demand
- **Structural Headwinds:** EV adoption rates, renewable energy deployment, efficiency gains

### Step 8: Oil Equity Sub-Sector Sensitivity

Map oil market conditions to equity sub-sector sensitivities. Consult `references/oil-equities-framework.md` for detailed sub-sector analysis. Do not present this as a direct recommendation to buy or sell; present it as a regime-based sensitivity map.

| Oil Market Condition | Typical Positive Sensitivity | Rationale |
|---------------------|----------------|-----------|
| Rising prices, backwardation | E&P (upstream) | Direct leverage to flat price. Backwardation rewards production over storage |
| Falling prices, contango | Midstream / Pipelines | Fee-based revenue insulated from commodity price. Contango creates storage revenue |
| Wide crude/product spreads | Refiners | Refining margin (crack spread) expansion. Buy crude cheap, sell products dear |
| High volatility | Integrated majors | Diversified business model dampens swings. Trading desks profit from volatility |
| Rising rig counts | Oilfield services | Activity-driven revenue. Pricing power when rigs are tight |
| Supply disruption | E&P with production in stable regions | Price spike benefits those still producing. Avoid companies in disrupted regions |

**For each sub-sector, apply the Stock-Analyzer technical workflow:**
- Weinstein Stage Analysis (is the sub-sector ETF in Stage 2?)
- Relative strength vs. the broad market AND vs. other energy sub-sectors
- Chart patterns and volume confirmation

Also check sub-sector-specific fundamentals before drawing conclusions:
- **E&P:** hedge book, leverage, breakeven costs, decline rates, basin quality
- **Refiners:** crack spreads, crude slate, RINs exposure, utilization, turnaround schedule
- **Midstream:** volume risk, contract quality, leverage, counterparty exposure, rate sensitivity
- **OFS:** rig/frac activity, capex guidance, pricing power, international vs. North America mix
- **Majors:** integrated mix, trading contribution, capital allocation, dividend coverage

### Step 9: EIA and Key Data Calendar

The weekly EIA report (released Wednesday at 10:30 AM ET) is the most important recurring oil data point. Key components:

- **Crude Oil Inventories:** The headline number. Compare to consensus expectations AND to seasonal norms.
- **Cushing, OK Inventories:** Specifically critical for the Bouchouev model when analyzing WTI. This is the WTI delivery hub. Compute capacity utilization only with a stated capacity denominator and source date.
- **Gasoline and Distillate Inventories:** Proxy for demand strength.
- **Crude Production:** Domestic supply indicator.
- **Refinery Utilization:** How much crude refineries are processing. Low utilization = weak demand or turnaround season.
- **Imports/Exports:** Net trade flows affecting domestic balances.

**API Report:** Released Tuesday evening. Provides an advance estimate before EIA. Market often trades the API surprise.

**Other Key Data:**
- OPEC Monthly Oil Market Report (MOMR)
- IEA Monthly Oil Market Report
- Baker Hughes Rig Count (Friday)
- CFTC Commitments of Traders (Friday) -- lagged positioning categories; useful for crowding context, not a standalone signal
- China customs data (monthly crude imports)

### Step 10: Risk Management for Oil Equities

Oil equities carry commodity-specific risks in addition to normal equity risk. Apply these oil-specific guardrails on top of standard technical-analysis risk management:

**Position Sizing:**
```
Position Size = (Account Size x Risk %) / (Entry Price - Stop Loss Price)
```
- Default risk per trade: 1% of account for single oil equity positions
- Reduce to 0.5% for higher-beta names (small-cap E&P, leveraged ETFs)
- Total oil/energy sector exposure: cap at 15-20% of portfolio
- Correlation risk: oil equities are highly correlated during macro moves. Four "independent" oil stocks may behave as one position in a selloff.

**Oil-Specific Risk Factors:**
- **Weekend/overnight gap risk:** Geopolitical events do not respect market hours. Oil can gap 5-10% on a weekend.
- **OPEC announcement risk:** Production decisions can instantly reprice the entire sector.
- **Inventory report risk:** Wednesday EIA releases cause regular intra-day volatility spikes.
- **Regulatory/political risk:** Windfall profit taxes, drilling bans, export restrictions, sanctions changes.

**Hedge Considerations:**
- Using oil put options or short futures as portfolio hedges for concentrated oil equity positions
- Calendar spread trades in futures as a supplement to equity positioning
- Cross-hedging between correlated sub-sectors

### Step 11: Synthesize and Deliver Verdict

Combine all findings into a structured assessment:

```
## Oil Market Analysis

**Date:** [date]
**Analysis Type:** [overview / sector / specific equity]
**Timeframe:** [tactical / positional / strategic]

### Macro Oil Regime
- Supply/demand balance: [surplus / balanced / deficit]
- OPEC+ stance: [cutting / holding / increasing]
- Geopolitical risk premium: [low / moderate / elevated / high]
- Demand trajectory: [contracting / flat / growing]

### Data Quality and Scope
- Benchmark: [WTI / Brent / both]
- Key release dates: [EIA / COT / OPEC / IEA]
- Contract timing: [prompt month, days to expiry, roll risk]
- Capacity denominator: [current / stale / unavailable; source date]
- Confidence adjustment: [what data gaps lower confidence]

### Dominant Shock Classification
- Primary driver: [physical supply / aggregate demand / precautionary demand / storage squeeze / financial-liquidity]
- Evidence: [why]
- Equity translation caveat: [how this shock type changes sub-sector read-through]

### Storage Capacity Utilization (Bouchouev Framework)
- Cushing utilization: [X%] -- Zone: [critical low / low / normal / high / critical high]
- Inventory trajectory: [building / stable / drawing]
- Forward-projected utilization at prompt delivery: [X%]
- Dominant squeeze probability: [upside (stock-out) / neutral / downside (tank-top)]

### Futures Curve Structure
- F1-F2 spread: [$X/bbl] -- [backwardation / flat / contango / super contango]
- Term structure shape: [description]
- Spread trend: [steepening / stable / flattening]

### Volatility Environment
- OVX level: [X] -- [low / normal / elevated / extreme]
- Price-vol correlation: [confirming negative relationship / diverging]
- Skew assessment: [normal / elevated downside risk / elevated upside risk]

### Supply Assessment
- OPEC+ compliance and spare capacity: [description]
- U.S. shale activity: [growing / flat / declining]
- Disruption risk: [low / moderate / high]

### Demand Assessment
- Global demand momentum: [weakening / stable / strengthening]
- Key regional drivers: [description]
- Seasonal positioning: [where in the annual cycle]

### Equity Sub-Sector Sensitivity
| Sub-Sector | Regime Tilt | Rationale |
|-----------|----------------|-----------|
| E&P | [positive / neutral / negative sensitivity] | [reason] |
| Refiners | [positive / neutral / negative sensitivity] | [reason] |
| Midstream | [positive / neutral / negative sensitivity] | [reason] |
| Oilfield Services | [positive / neutral / negative sensitivity] | [reason] |
| Integrated Majors | [positive / neutral / negative sensitivity] | [reason] |

### Signal Conflict Check
- Confirming signals: [curve / inventories / cracks / WTI-Brent / OVX / COT / relative strength]
- Conflicting signals: [what disagrees]
- Confidence: [high / medium / low] because [reason]

### Key Levels (WTI)
- Support: [price levels]
- Resistance: [price levels]
- Breakeven zone for shale: [$X-$Y/bbl]

### Risk Parameters
- Primary risk factor: [description]
- Position sizing guidance: [description]
- Portfolio oil-sector allocation: [risk framing, not individualized advice]

### Overall Assessment
[2-4 sentence synthesis: bullish/neutral/bearish regime read for the oil complex, which sub-sectors have positive or negative sensitivity,
primary catalysts to watch, key risks, confidence level, and the Bouchouev model's current signal regarding WTI spread squeeze probabilities.]
```

## Guiding Principles

These axioms apply across all oil market analysis:

1. **Storage capacity utilization is the primary state variable for WTI prompt-spread squeeze risk** -- not for all crude prices or all oil equities. The ratio of inventory to capacity helps determine the probability of extreme WTI delivery events and non-linear spread behavior (Bouchouev).
2. **The market trades on expected future inventories, not current ones** -- spreads reflect what the market believes inventories will be at delivery, not what they are today. Follow the inventory trajectory, not the snapshot.
3. **Non-linearity dominates at the boundaries** -- in the middle of the capacity range, spreads are boring. Near either boundary (stock-out or tank-top), small changes in inventory produce massive price moves. This is where the opportunity AND the danger lies.
4. **Oil volatility often rises during downside moves, but the relationship is regime-dependent** -- oil often follows "up the stairs, down the elevator," yet supply disruptions can create different volatility behavior. Position sizing must account for fat-tail risk and unstable correlations.
5. **Financial market structure matters as much as physical fundamentals** -- the April 2020 negative price event was a financial squeeze, not a physical one. Understand who is holding positions and what will force them to liquidate.
6. **Oil is an investment asset, not just a commodity** -- financialization means oil's price is driven by portfolio flows, hedging demand, and roll yield in addition to physical supply and demand.
7. **Mean reversion is the long-term anchor** -- inventories mean-revert, spreads mean-revert, and prices tend toward the marginal cost of production. Bet with mean reversion over longer horizons, but respect momentum over shorter ones.
8. **Respect the carry trade** -- contango should approximate storage cost. When it substantially exceeds storage cost, the market is pricing in capacity-boundary risk. When backwardation substantially exceeds financing benefit, the market is pricing in stock-out risk.
9. **Classify the shock before mapping equities** -- a price move driven by global demand, precautionary demand, storage stress, or financial liquidation can have different equity implications.
10. **OPEC is a political actor, not an economic optimizer** -- never assume rational economic behavior from a cartel. Model OPEC as a source of regime changes, not smooth adjustments.
11. **Capital preservation first** -- oil markets can move against you faster and further than almost any other major market. The first loss is the best loss.

## Help

When the user asks for help (e.g., "help", "what can you do", "how does this work", "/oil-market-analyzer help"), respond with the following:

```
## Oil Market Analyzer -- Help

A comprehensive oil market analysis skill combining the Bouchouev
storage-capacity-utilization model with shock classification, technical
analysis, supply/demand fundamentals, and equity sub-sector sensitivity.

### What I Can Do

| Command / Request | What Happens |
|-------------------|-------------|
| "Analyze oil market" | Full analysis: data quality, macro regime, shock classification, storage utilization, curve structure, volatility, supply, demand, equity sensitivity, risk parameters, and verdict |
| "What's the oil curve doing?" | Futures curve structure analysis: spread levels, shape, and what they signal about inventory expectations |
| "Storage utilization?" | Bouchouev framework assessment: current utilization zone, squeeze probabilities, and non-linear risk |
| "Which oil stocks to buy?" | Educational sub-sector sensitivity map based on current oil market regime; not individualized investment advice |
| "Oil risk assessment" | Volatility environment, skew, geopolitical risks, and position sizing guidance |
| "Explain [oil concept]" | Educational deep-dive on contango, backwardation, the squeeze model, carry trade, etc. |
| "Cushing inventory analysis" | Detailed assessment of Cushing storage capacity utilization and its implications |
| "OPEC analysis" | Production quotas, compliance, spare capacity, and likely policy direction |
| "How do EIA numbers affect stocks?" | Framework for trading oil equities around the weekly inventory report |

### Core Methodology

- **Bouchouev Storage Model** -- Storage capacity utilization as the primary state variable for WTI prompt-spread squeeze risk; futures spreads as a derivative of inventories/capacity
- **Shock Classification** -- Distinguishing physical supply, aggregate demand, precautionary demand, storage squeeze, and financial/liquidity shocks before mapping equities
- **Futures Curve Analysis** -- Contango/backwardation structure, time spreads, squeeze probabilities
- **Supply/Demand Fundamentals** -- OPEC+, U.S. shale, global demand drivers, seasonal patterns
- **Oil Equity Sub-Sector Mapping** -- Translating oil market conditions into equity sensitivities across E&P, refiners, midstream, oilfield services, and integrated majors
- **Technical Analysis Integration** -- Weinstein Stage Analysis and Minervini Trend Template applied to energy sector ETFs and individual oil equities

### Analysis Workflow

- Step 1: Determine scope (goal, timeframe, equities of interest)
- Step 1A: Check data quality, source freshness, benchmark, and contract timing
- Step 2: Macro oil market context and shock classification
- Step 3: Storage capacity utilization assessment (Bouchouev framework)
- Step 4: Futures curve analysis (spreads, term structure)
- Step 5: Volatility and skew assessment
- Step 6: Supply-side analysis (OPEC+, shale, disruption risk)
- Step 7: Demand-side analysis (China, U.S., seasonal)
- Step 8: Oil equity sub-sector sensitivity
- Step 9: EIA and key data calendar
- Step 10: Risk management for oil equities
- Step 11: Synthesize verdict with a signal conflict check

### Key Data Sources

- EIA Weekly Petroleum Status Report (Wednesday 10:30 AM ET)
- API Weekly Statistical Bulletin (Tuesday evening)
- Baker Hughes Rig Count (Friday)
- CFTC Commitments of Traders (Friday)
- OPEC Monthly Oil Market Report
- IEA Monthly Oil Market Report

### Quick Start

Just say: **"Analyze the oil market"** and I'll walk through the full
workflow. Or ask about a specific aspect like **"What's Cushing
utilization telling us?"**

### Reference Docs

For deep dives, I can consult:
- `references/storage-model.md` -- Bouchouev's capacity-utilization framework, squeeze model math, mean reversion
- `references/oil-equities-framework.md` -- Sub-sector analysis, regime-equity mapping, individual stock factors
- `references/oil-market-indicators.md` -- Data sources, seasonal patterns, volatility structure, positioning data

### Disclaimer

This skill provides educational analysis only. It is NOT financial
advice. All analysis is probabilistic. You are responsible for your
own investment decisions.
```

## Common User Requests and How to Handle Them

**"What's happening with oil?"** -- Run Steps 2-5 for a quick macro overview. Provide curve structure and utilization zone. Then ask if they want the full equity sensitivity analysis.

**"Should I buy oil stocks?"** -- Run the full workflow. Never give a simple yes/no. Map the macro regime to sub-sector sensitivities, state the data gaps, and remind the user this is educational analysis rather than individualized advice.

**"Why are oil prices falling/rising?"** -- Focus on Steps 2, 3, 6, and 7. Identify whether the move is driven by supply (OPEC, disruptions), demand (macro slowdown, seasonal), or financial factors (positioning, roll). Contextualize using the Bouchouev framework.

**"What do the inventories mean?"** -- Focus on Step 3 (storage capacity utilization). Explain the non-linear relationship between inventories and spreads. Emphasize that absolute inventory levels matter less than utilization rate and trajectory.

**"Contango/backwardation -- what does it mean for stocks?"** -- Focus on Step 4 (curve analysis) and Step 8 (sub-sector mapping). Explain how each sub-sector tends to benefit or suffer under different curve structures, then check for contradicting signals from crack spreads, WTI-Brent, OVX, and relative strength.

**"What's the risk in oil right now?"** -- Focus on Steps 5 and 10. Assess volatility, skew, squeeze probabilities, and geopolitical tail risks. Provide position sizing guidance.

**"Help" / "What can you do?"** -- Display the help output defined in the Help section above.

## Performance Notes

- Take your time to do this thoroughly
- Quality is more important than speed
- Never skip the macro oil context step -- it dominates individual equity selection
- Always frame findings in terms of the Bouchouev capacity-utilization model where relevant, but label it specifically as a WTI prompt-spread squeeze framework
- Remember the user is an equities trader -- translate oil market analysis into equity sub-sector sensitivity, not direct trade recommendations
- Always include the disclaimer that this is educational analysis, not financial advice
- When the user provides current data, compute derived metrics (utilization rate, spread ratios) and classify into the framework's zones; state the source date and uncertainty of the capacity denominator
- If the user lacks data, clearly state what data they need and where to find it before applying the framework
- If signals conflict, explicitly identify the conflict and reduce confidence rather than forcing a single conclusion
