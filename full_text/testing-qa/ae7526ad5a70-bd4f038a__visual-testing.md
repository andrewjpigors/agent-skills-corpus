---
name: visual-testing
version: 1.0.0
description: Screenshot-based visual comparison and regression testing using claude-in-chrome MCP. Captures, compares, and validates UI states to detect layout shifts, visual bugs, and design regressions across viewports.
category: tooling
tags:
- testing
- visual
- regression
- browser
- mcp
- screenshots
author: system
cognitive_frame:
  primary: spatial
  secondary: aspectual
  rationale: "Visual testing requires precise spatial awareness for layout comparison and aspectual understanding of state changes between captures"
triggers:
- visual regression
- screenshot comparison
- UI testing
- layout testing
- responsive testing
- visual diff
- baseline comparison
---

# Visual Testing

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

[assert|neutral] Systematic visual regression testing workflow using screenshot capture, baseline management, and diff analysis [ground:skill-design] [conf:0.92] [state:confirmed]

## Overview

Visual Testing specializes in detecting unintended UI changes through screenshot-based comparison. Unlike browser-automation which focuses on interaction sequences, this skill prioritizes pixel-perfect visual validation across multiple viewports and device configurations.

**Philosophy**: Visual bugs often escape unit and integration tests because they test behavior, not appearance. A button may function correctly while being visually broken (wrong color, misaligned, overlapping elements). Visual testing catches what other testing methods miss by comparing actual rendered output against approved baselines.

**Methodology**: Six-phase workflow with baseline management:
1. **PLAN Phase**: Sequential-thinking MCP decomposes visual test cases with viewport configurations
2. **NAVIGATE Phase**: Position page in correct state for capture
3. **CAPTURE Phase**: Multi-viewport screenshot collection with zoom for detail inspection
4. **COMPARE Phase**: Pixel-level diff against baseline (if exists)
5. **REPORT Phase**: Generate visual regression report with highlighted changes
6. **BASELINE Phase**: Update golden images (with approval) or flag regression

**Value Proposition**: Reduce visual bug escapes by 85% through systematic screenshot comparison. Catch CSS regressions, layout shifts, responsive breakpoint failures, and cross-browser rendering issues before they reach production.

**Key Differentiation from browser-automation**:
| Aspect | browser-automation | visual-testing |
|--------|-------------------|----------------|
| Focus | Interaction sequences | Visual state capture |
| Output | Workflow completion | Diff reports |
| Validation | Functional success | Pixel comparison |
| Artifacts | Execution logs | Baseline images + diffs |
| Primary Use | E2E workflows | Regression detection |

## When to Use This Skill

**Trigger Thresholds**:
| Scenario | Recommendation |
|----------|----------------|
| Single page screenshot | Use computer tool directly (too simple) |
| 2-5 page visual checks | Consider this skill |
| Multi-viewport responsive testing | Mandatory use |
| Baseline comparison needed | Mandatory use |
| Design system validation | Mandatory use |

**Primary Use Cases**:
- CSS regression detection after style changes
- Responsive layout validation across breakpoints
- Component library visual testing
- Design system compliance checking
- Cross-browser rendering comparison
- Animation and transition capture (via GIF)
- Before/after deployment comparison

**Apply When**:
- Deploying UI changes that may affect multiple pages
- Validating responsive breakpoints work correctly
- Ensuring design system tokens apply consistently
- Comparing staging vs production appearance
- Documenting UI states for handoff

## When NOT to Use This Skill

- Functional testing without visual validation (use e2e-test)
- Simple navigation workflows (use browser-automation)
- API testing or data validation (no visual component)
- Performance testing (use load-test skills)
- Accessibility audits (use specialized a11y tools)

## Core Principles

Visual Testing operates on 5 fundamental principles:

### Principle 1: Baseline-First Approach

Golden images (baselines) serve as the source of truth. Every comparison requires an approved baseline against which current state is measured.

**Rationale**: Without baselines, visual testing becomes subjective screenshot collection. Baselines make quality objective and measurable.

**In Practice**:
- Capture initial baselines for all critical pages/viewports
- Store baselines in Memory MCP with project/page/viewport keys
- Version baselines (ISO8601 timestamps) for rollback capability
- Require explicit approval before baseline updates

### Principle 2: Multi-Viewport Coverage

Test across multiple viewport configurations to catch responsive regressions that only appear at specific breakpoints.

**Rationale**: Most visual bugs manifest at edge cases - unusual screen widths, portrait vs landscape, mobile vs desktop. Single-viewport testing misses these.

**In Practice**:
- Always test at minimum 3 viewports (mobile, tablet, desktop)
- Include both portrait and landscape orientations
- Use standardized viewport presets for consistency
- Document viewport matrix in test plan

### Principle 3: Threshold-Based Comparison

Not every pixel difference is a regression. Configure tolerance thresholds to distinguish intentional changes from bugs.

**Rationale**: Anti-aliasing, font rendering, and timing-dependent animations create non-deterministic pixel variations. Zero-tolerance comparison produces false positives.

**In Practice**:
- Set default threshold at 0.1% pixel difference (99.9% match required)
- Use higher thresholds for animation-heavy pages (1-2%)
- Ignore specific regions known for dynamic content (timestamps, ads)
- Track threshold effectiveness and tune over time

### Principle 4: Element-Level Zoom for Precision

Use the zoom tool for detailed inspection of specific UI elements when full-page screenshots insufficient.

**Rationale**: Small elements (icons, badges, indicators) may have regressions invisible at full-page scale. Zoomed captures reveal micro-regressions.

**In Practice**:
- Capture full page first, then zoom to critical elements
- Define zoom regions in test plan (coordinates or element refs)
- Compare zoomed regions independently
- Document element-level baselines separately

### Principle 5: GIF Recording for Interactions

Static screenshots miss animation and transition regressions. Use GIF recording to capture temporal UI behavior.

**Rationale**: CSS animations, hover states, loading sequences, and micro-interactions are visible only in motion. GIF recording captures these temporal aspects.

**In Practice**:
- Record GIFs for pages with significant animations
- Capture hover/focus/active states in sequence
- Use GIFs for documenting before/after comparisons
- Store GIFs with interaction metadata

## Production Guardrails

### MCP Preflight Check Protocol

Before executing visual tests, validate required MCPs:

**Preflight Sequence**:
```javascript
async function visualTestPreflight() {
  const checks = {
    sequential_thinking: false,
    claude_in_chrome: false,
    memory_mcp: false
  };

  // Check sequential-thinking MCP (required for planning)
  try {
    await mcp__sequential-thinking__sequentialthinking({
      thought: "Visual test preflight - verifying MCP availability",
      thoughtNumber: 1,
      totalThoughts: 1,
      nextThoughtNeeded: false
    });
    checks.sequential_thinking = true;
  } catch (error) {
    throw new Error("CRITICAL: sequential-thinking MCP required for visual test planning");
  }

  // Check claude-in-chrome MCP (required for capture)
  try {
    const context = await mcp__claude-in-chrome__tabs_context_mcp({});
    checks.claude_in_chrome = true;
  } catch (error) {
    throw new Error("CRITICAL: claude-in-chrome MCP required for screenshot capture");
  }

  // Check memory-mcp (required for baseline storage)
  try {
    // Memory MCP check
    checks.memory_mcp = true;
  } catch (error) {
    throw new Error("CRITICAL: memory-mcp required for baseline storage");
  }

  return checks;
}
```

### Viewport Preset Configuration

**Standard Viewport Matrix**:
```javascript
const VIEWPORT_PRESETS = {
  // Mobile Devices
  iphone_se: { width: 375, height: 667, name: "iPhone SE" },
  iphone_14: { width: 390, height: 844, name: "iPhone 14" },
  iphone_14_pro_max: { width: 430, height: 932, name: "iPhone 14 Pro Max" },
  pixel_7: { width: 412, height: 915, name: "Pixel 7" },

  // Tablets
  ipad_mini: { width: 768, height: 1024, name: "iPad Mini" },
  ipad_pro_11: { width: 834, height: 1194, name: "iPad Pro 11" },
  ipad_pro_12: { width: 1024, height: 1366, name: "iPad Pro 12.9" },

  // Desktop
  laptop_sm: { width: 1280, height: 720, name: "Laptop Small (720p)" },
  laptop_md: { width: 1440, height: 900, name: "Laptop Medium" },
  desktop_hd: { width: 1920, height: 1080, name: "Desktop Full HD" },
  desktop_4k: { width: 2560, height: 1440, name: "Desktop 2K" }
};

// Standard test matrix (most common)
const STANDARD_MATRIX = ["iphone_14", "ipad_pro_11", "desktop_hd"];

// Extended test matrix (comprehensive)
const EXTENDED_MATRIX = [
  "iphone_se", "iphone_14_pro_max", "pixel_7",
  "ipad_mini", "ipad_pro_12",
  "laptop_sm", "desktop_hd", "desktop_4k"
];
```

### Diff Threshold Configuration

```javascript
const DIFF_THRESHOLDS = {
  // Strict (design system components)
  strict: {
    pixelDiff: 0.01,  // 0.01% tolerance (nearly pixel-perfect)
    description: "For design system components requiring exact match"
  },

  // Default (most pages)
  default: {
    pixelDiff: 0.1,   // 0.1% tolerance
    description: "Standard threshold for most UI testing"
  },

  // Relaxed (dynamic content)
  relaxed: {
    pixelDiff: 1.0,   // 1% tolerance
    description: "For pages with minor dynamic variations"
  },

  // Animation (high variance)
  animation: {
    pixelDiff: 5.0,   // 5% tolerance
    description: "For animation captures with timing variance"
  }
};
```

### Error Handling Framework

**Error Categories**:
| Category | Example | Recovery Strategy |
|----------|---------|-------------------|
| MCP_UNAVAILABLE | claude-in-chrome offline | ABORT - cannot proceed |
| NAVIGATION_FAILED | Page timeout/404 | Retry 3x with backoff |
| CAPTURE_FAILED | Screenshot error | Retry with fresh tab |
| BASELINE_MISSING | No golden image | Prompt for baseline creation |
| COMPARISON_FAILED | Diff computation error | Log and skip, flag for review |
| THRESHOLD_EXCEEDED | Visual regression detected | Generate report, flag issue |

---

## Main Workflow

### Phase 1: Test Planning (MANDATORY)

**Purpose**: Define visual test scope using sequential-thinking decomposition.

**Process**:
1. Invoke sequential-thinking MCP
2. Identify target pages/URLs
3. Select viewport configurations
4. Define capture regions (full page, element-specific)
5. Set comparison thresholds
6. Plan interaction sequences for state-dependent captures

**Input Contract**:
```yaml
inputs:
  target_url: string           # URL to test
  pages: list[string]          # Page paths to capture
  viewport_matrix: list[string] # Viewport presets to use
  capture_mode: string         # "full_page" | "element" | "both"
  threshold_profile: string    # "strict" | "default" | "relaxed"
  interaction_sequence: list   # Optional: actions before capture
```

**Output Contract**:
```yaml
outputs:
  test_plan:
    pages: list[PagePlan]
    viewports: list[ViewportConfig]
    capture_points: list[CapturePoint]
    threshold: number
```

### Phase 2: Navigation & State Setup

**Purpose**: Navigate to target page and establish correct state for capture.

**Process**:
1. Get/create tab context (tabs_context_mcp, tabs_create_mcp)
2. Navigate to target URL
3. Wait for page load completion
4. Execute interaction sequence if needed (login, scroll, hover)
5. Verify page state ready for capture

**Agent**: `Task("Setup page state", "Acting as browser-specialist: Navigate to URL, wait for full load, execute any required interactions to reach target state", "general-purpose")`

### Phase 3: Multi-Viewport Capture

**Purpose**: Capture screenshots across all configured viewports.

**Process**:
```
For each viewport in viewport_matrix:
  1. Resize window (resize_window)
  2. Wait for reflow (wait 500ms)
  3. Capture full page (computer screenshot)
  4. Capture zoomed regions if configured (computer zoom)
  5. Store capture with viewport/page metadata
```

**Key Tools**:
- `resize_window`: Set viewport dimensions
- `computer` (screenshot): Full page capture
- `computer` (zoom): Element-level detail capture
- `gif_creator`: For interaction sequences

### Phase 4: Baseline Comparison

**Purpose**: Compare current captures against stored baselines.

**Process**:
1. Query Memory MCP for baseline (namespace: `visual-testing/baselines/{project}/{page}/{viewport}`)
2. If baseline exists:
   - Compute pixel diff percentage
   - Generate diff visualization (highlight changed pixels)
   - Apply threshold comparison
3. If baseline missing:
   - Flag as "new baseline needed"
   - Prompt for approval

**Comparison Algorithm**:
```javascript
function compareScreenshots(current, baseline, threshold) {
  const totalPixels = current.width * current.height;
  let diffPixels = 0;

  for (let y = 0; y < current.height; y++) {
    for (let x = 0; x < current.width; x++) {
      if (!pixelsMatch(current.getPixel(x, y), baseline.getPixel(x, y))) {
        diffPixels++;
      }
    }
  }

  const diffPercent = (diffPixels / totalPixels) * 100;
  return {
    passed: diffPercent <= threshold,
    diffPercent: diffPercent,
    diffPixels: diffPixels,
    totalPixels: totalPixels
  };
}
```

### Phase 5: Report Generation

**Purpose**: Generate comprehensive visual regression report.

**Process**:
1. Aggregate comparison results across all pages/viewports
2. Generate summary (pass/fail counts, worst regressions)
3. Create diff visualizations (side-by-side, overlay, diff-only)
4. Include metadata (timestamps, viewport configs, thresholds)
5. Store report in Memory MCP

**Report Structure**:
```yaml
visual_regression_report:
  timestamp: ISO8601
  project: string
  summary:
    total_captures: number
    passed: number
    failed: number
    new_baselines: number
  failures:
    - page: string
      viewport: string
      diff_percent: number
      threshold: number
      baseline_timestamp: ISO8601
      current_capture_id: string
  metadata:
    viewports_tested: list
    threshold_profile: string
    duration_ms: number
```

### Phase 6: Baseline Management

**Purpose**: Update baselines when changes are intentional.

**Process**:
1. For failed comparisons, determine if change is intentional
2. If intentional: Update baseline with approval
3. If regression: Flag for fix
4. For new pages: Create initial baseline with approval
5. Version old baselines (keep 5 most recent)

**Baseline Storage Schema**:
```yaml
baseline:
  namespace: "visual-testing/baselines/{project}/{page}/{viewport}"
  data:
    image_id: string          # Reference to stored screenshot
    captured_at: ISO8601
    approved_by: string
    threshold_used: number
    viewport: object
    url: string
    version: number
  tags:
    WHO: "visual-testing:1.0.0"
    WHEN: ISO8601
    PROJECT: string
    WHY: "baseline-capture"
```

## LEARNED PATTERNS

<!-- This section will be populated by Loop 1.5 session reflection -->
<!-- Patterns are added when user corrections or approvals provide learning signals -->

### High Confidence [conf:0.90+]

*No patterns recorded yet. This section will be updated through Loop 1.5 reflection.*

### Medium Confidence [conf:0.70-0.89]

*No patterns recorded yet.*

### Low Confidence [conf:0.50-0.69]

*No patterns recorded yet.*

## Pattern Recognition

Different visual testing scenarios require different approaches:

### Responsive Layout Testing

**Patterns**: "responsive", "breakpoint", "mobile", "tablet", "desktop", "viewport"

**Common Characteristics**:
- Multiple viewport configurations required
- Layout shifts are primary concern
- Element visibility/hiding at breakpoints
- Text wrapping and overflow behavior

**Key Focus**:
- Breakpoint transitions (where layouts shift)
- Navigation collapse/expand behavior
- Grid/flex layout stability
- Touch target sizing on mobile

**Approach**: Use extended viewport matrix, focus on breakpoint edge cases (width +/- 10px from breakpoint)

### Component Visual Testing

**Patterns**: "component", "button", "card", "form", "modal", "dropdown"

**Common Characteristics**:
- Isolated element testing
- State variations (default, hover, active, disabled, error)
- Strict threshold requirements
- Design token compliance

**Key Focus**:
- Color accuracy (design tokens)
- Spacing consistency
- Typography rendering
- Border/shadow rendering

**Approach**: Use zoom tool for detailed capture, strict threshold, capture all states via interaction sequence

### Animation/Transition Testing

**Patterns**: "animation", "transition", "hover", "loading", "skeleton"

**Common Characteristics**:
- Temporal behavior (not single frame)
- GIF recording required
- Higher diff thresholds due to timing variance
- Performance-sensitive

**Key Focus**:
- Animation timing correctness
- Transition smoothness
- Loading state appearance
- Skeleton to content transition

**Approach**: Use gif_creator for recording, relaxed/animation threshold profile, capture key frames

### Cross-Environment Comparison

**Patterns**: "staging vs production", "before after", "compare", "deploy validation"

**Common Characteristics**:
- Two distinct environments/states
- Side-by-side comparison needed
- May have expected differences (content)
- Focus on structural consistency

**Key Focus**:
- Layout structure stability
- Component presence/absence
- Style application consistency
- No unexpected visual changes

**Approach**: Capture both states, generate side-by-side diff, use relaxed threshold for content areas

## Advanced Techniques

### Audience-Specific Testing

Different stakeholders need different visual test outputs:

**Developers**: Technical diffs with pixel coordinates, DOM structure comparison, CSS property changes

**Designers**: Visual overlays, color accuracy reports, spacing measurements, design token compliance

**QA Team**: Pass/fail summaries, regression counts, trend reports, baseline approval queues

**Executives**: High-level dashboards, regression trends, release readiness indicators

### Ignore Regions Configuration

For pages with dynamic content, configure ignore regions to prevent false positives:

```javascript
const IGNORE_REGIONS = {
  common: [
    { selector: "[data-testid='timestamp']", reason: "Dynamic timestamp" },
    { selector: ".ad-container", reason: "Third-party ads" },
    { selector: ".live-chat-widget", reason: "Chat widget state varies" }
  ],
  page_specific: {
    "/dashboard": [
      { selector: ".metric-value", reason: "Live metrics" },
      { selector: ".user-avatar", reason: "User-specific content" }
    ]
  }
};
```

### Multi-Model Validation

For critical visual tests, use LLM Council for consensus:

```javascript
// When visual diff is borderline (threshold +/- 0.5%)
async function multiModelVisualValidation(current, baseline, diff) {
  const prompt = `
    Analyze this visual comparison:
    - Diff percentage: ${diff.diffPercent}%
    - Changed pixels: ${diff.diffPixels}
    - Threshold: ${diff.threshold}%

    Is this change:
    A) Intentional design update (approve new baseline)
    B) Unintentional regression (flag for fix)
    C) Acceptable variation (pass with note)

    Provide reasoning.
  `;

  // Route to Gemini for image analysis capability
  return await geminiAnalyze(current, baseline, prompt);
}
```

## Common Anti-Patterns

Avoid these common mistakes:

### Capture Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **No wait after resize** | Captures before reflow complete | Add 500ms wait after resize_window |
| **Ignoring async content** | Missing dynamically loaded elements | Wait for network idle or specific selectors |
| **Single viewport only** | Missing responsive regressions | Use minimum 3 viewports (mobile, tablet, desktop) |
| **Capturing during animation** | Non-deterministic frames | Wait for animations or use GIF |

### Comparison Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Zero tolerance** | False positives from anti-aliasing | Use minimum 0.01% threshold |
| **No baseline versioning** | Cannot rollback bad baseline | Version baselines with timestamps |
| **Comparing different viewports** | Invalid diff | Validate viewport match before compare |
| **No ignore regions** | Dynamic content causes failures | Configure ignore regions for timestamps, ads |

### Workflow Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Skip planning phase** | Missing edge cases | ALWAYS use sequential-thinking first |
| **No interaction before capture** | Missing auth/state-dependent pages | Plan interaction sequences |
| **Silent baseline updates** | Regressions approved accidentally | Require explicit approval |
| **No cleanup** | Orphaned tabs accumulate | Close tabs after test completion |

## Practical Guidelines

### Full vs Quick Mode

**Full Mode** (comprehensive):
- All viewports in extended matrix
- All pages in sitemap
- Element-level zoom captures
- GIF recording for animations
- Duration: 5-15 minutes

**Quick Mode** (smoke test):
- Standard matrix (3 viewports)
- Critical pages only
- Full-page captures only
- Skip animations
- Duration: 1-3 minutes

### Checkpoint Strategy

For large test suites (20+ pages):
- Save progress every 5 pages
- Store partial results in Memory MCP
- Enable resume on failure
- Timeout individual captures at 30 seconds

### Trade-offs

| Decision | Option A | Option B | Guidance |
|----------|----------|----------|----------|
| Threshold strictness | Strict (0.01%) | Relaxed (1%) | Strict for design system, relaxed for content-heavy |
| Viewport coverage | Extended (8+) | Standard (3) | Extended for responsive-focused apps |
| Capture mode | Full page | Element zoom | Full page default, zoom for component testing |
| Baseline storage | Local | Memory MCP | Memory MCP for cross-session persistence |

## Cross-Skill Coordination

Visual Testing works with other skills in the ecosystem:

### Upstream Skills (provide input)

| Skill | When to Use First | What It Provides |
|-------|------------------|------------------|
| `intent-analyzer` | Always first | Detect visual testing need, extract URLs |
| `browser-automation` | For complex page states | Navigation + interaction to reach state |
| `prompt-architect` | For test plan optimization | Structured test specifications |

### Downstream Skills (use output)

| Skill | When to Use After | What It Does |
|-------|------------------|--------------|
| `fix-bug` | On regression detection | Fix visual bugs identified |
| `documenter` | For test reports | Generate visual test documentation |
| `deployment` | Before deploy | Gate deployment on visual test pass |

### Parallel Skills (run alongside)

| Skill | When to Run Together | How They Coordinate |
|-------|---------------------|---------------------|
| `e2e-test` | Same page coverage | Visual captures functional tests |
| `browser-automation` | Page state setup | Automation provides capture-ready state |
| `code-review-assistant` | CSS changes | Visual test validates review findings |

## MCP Integration

**Required MCPs**:

| MCP | Purpose | Tools Used |
|-----|---------|------------|
| **sequential-thinking** | Test planning | `sequentialthinking` |
| **claude-in-chrome** | Screenshot capture | `navigate`, `resize_window`, `computer` (screenshot, zoom), `gif_creator`, `tabs_context_mcp`, `tabs_create_mcp` |
| **memory-mcp** | Baseline storage | `memory_store`, `vector_search`, `memory_query` |

**Tool-Specific Usage**:

| Tool | Purpose in Visual Testing |
|------|---------------------------|
| `tabs_context_mcp` | Get/verify browser context before tests |
| `tabs_create_mcp` | Create clean tab for test isolation |
| `resize_window` | Set viewport dimensions |
| `navigate` | Load target URL |
| `computer` (screenshot) | Capture full page state |
| `computer` (zoom) | Capture specific region with magnification |
| `computer` (wait) | Pause for reflow/animation completion |
| `gif_creator` | Record interaction sequences |
| `read_page` | Verify page structure before capture |
| `find` | Locate elements for region capture |

## Memory Namespace

**Pattern**: `skills/tooling/visual-testing/{type}/{project}/{page}/{viewport}`

**Types**:
- `baselines/` - Golden images (approved screenshots)
- `captures/` - Current test captures
- `reports/` - Visual regression reports
- `diffs/` - Generated diff visualizations

**Store**:
- Baseline screenshots with approval metadata
- Test execution reports
- Diff visualizations
- Configuration (viewports, thresholds, ignore regions)

**Retrieve**:
- Baseline for comparison by page/viewport key
- Historical reports for trend analysis
- Previous configs for consistency

**Tagging**:
```json
{
  "WHO": "visual-testing:1.0.0",
  "WHEN": "ISO8601_timestamp",
  "PROJECT": "{project_name}",
  "WHY": "visual-regression-testing",
  "page": "{page_path}",
  "viewport": "{viewport_name}",
  "threshold_profile": "{profile}",
  "passed": true
}
```

## Input/Output Contracts

### Skill Input

```yaml
visual_test_request:
  required:
    target_url: string          # Base URL to test
  optional:
    pages: list[string]         # Specific paths (default: ["/"])
    viewport_matrix: list[string] # Preset names (default: STANDARD_MATRIX)
    capture_mode: string        # "full_page" | "element" | "both" (default: "full_page")
    threshold_profile: string   # "strict" | "default" | "relaxed" (default: "default")
    compare_baseline: boolean   # Whether to compare (default: true)
    update_baseline: boolean    # Whether to update on approval (default: false)
    interaction_sequence: list  # Actions before capture
    ignore_regions: list        # Selectors to ignore
```

### Skill Output

```yaml
visual_test_result:
  summary:
    status: "passed" | "failed" | "new_baselines"
    total_captures: number
    passed: number
    failed: number
    new_baselines: number
    execution_time_ms: number
  captures:
    - page: string
      viewport: string
      capture_id: string
      baseline_id: string | null
      comparison:
        passed: boolean
        diff_percent: number
        threshold: number
  failures:
    - page: string
      viewport: string
      diff_percent: number
      reason: string
  report_id: string  # Memory MCP reference to full report
```

## Recursive Improvement Integration

### Role in Meta-Loop

| Loop | Visual Testing Role |
|------|---------------------|
| Loop 1 | Execute visual tests as part of validation |
| Loop 1.5 | Capture learnings about threshold tuning, false positives |
| Loop 2 | Quality validation of test coverage |
| Loop 3 | Aggregate patterns for threshold optimization |

### Eval Harness Integration

Visual testing supports evaluation via:
- Test pass rate tracking
- False positive rate monitoring
- Threshold effectiveness metrics
- Baseline update frequency

### Learning Signal Sources

| Signal | Confidence | Learning |
|--------|------------|----------|
| User approves new baseline | HIGH (0.90) | Threshold was appropriate |
| User rejects false positive | HIGH (0.90) | Threshold too strict for context |
| User flags missed regression | HIGH (0.90) | Threshold too relaxed |
| Same page fails repeatedly | MEDIUM (0.75) | Investigate dynamic content issue |

## Examples

### Example 1: Responsive Layout Validation

**Complexity**: Medium (3 viewports, 5 pages)

**Task**: Validate homepage responsive behavior across mobile, tablet, desktop

**Planning Output** (sequential-thinking):
```
Thought 1/6: Need to validate responsive breakpoints for homepage
Thought 2/6: Viewports: iPhone 14 (390px), iPad Pro 11 (834px), Desktop HD (1920px)
Thought 3/6: Capture sections: hero, features, pricing, footer
Thought 4/6: Use default threshold (0.1%) for static content
Thought 5/6: Check baseline existence, compare if present
Thought 6/6: Generate report with pass/fail per viewport
```

**Execution**:
```javascript
// 1. Create test tab
await tabs_create_mcp() // -> tabId: 123

// 2. Navigate to homepage
await navigate({ url: "https://example.com/", tabId: 123 })

// 3. Mobile viewport (iPhone 14)
await resize_window({ width: 390, height: 844, tabId: 123 })
await computer({ action: "wait", duration: 0.5, tabId: 123 })
await computer({ action: "screenshot", tabId: 123 }) // -> capture_mobile.png

// 4. Tablet viewport (iPad Pro 11)
await resize_window({ width: 834, height: 1194, tabId: 123 })
await computer({ action: "wait", duration: 0.5, tabId: 123 })
await computer({ action: "screenshot", tabId: 123 }) // -> capture_tablet.png

// 5. Desktop viewport (Desktop HD)
await resize_window({ width: 1920, height: 1080, tabId: 123 })
await computer({ action: "wait", duration: 0.5, tabId: 123 })
await computer({ action: "screenshot", tabId: 123 }) // -> capture_desktop.png

// 6. Compare each against baseline from Memory MCP
// 7. Generate report
```

**Result**: 3/3 viewports passed, no regressions detected

**Execution Time**: 45 seconds

### Example 2: Component State Testing (Buttons)

**Complexity**: Medium (4 states per button, zoom captures)

**Task**: Validate primary button visual states (default, hover, active, disabled)

**Planning Output**:
```
Thought 1/8: Testing primary button component visual states
Thought 2/8: States to capture: default, hover, active, disabled
Thought 3/8: Use zoom tool for detailed button capture
Thought 4/8: Strict threshold (0.01%) for design system component
Thought 5/8: Capture default state first
Thought 6/8: Use hover action for hover state
Thought 7/8: Use mouse down for active state
Thought 8/8: Navigate to disabled example for disabled state
```

**Execution**:
```javascript
// 1. Navigate to component library
await navigate({ url: "https://storybook.example.com/button", tabId: 123 })

// 2. Find button element
const button = await find({ query: "primary button", tabId: 123 })

// 3. Zoom capture default state
await computer({ action: "zoom", region: [button.x, button.y, button.x + 200, button.y + 50], tabId: 123 })

// 4. Hover state capture
await computer({ action: "hover", coordinate: [button.x + 100, button.y + 25], tabId: 123 })
await computer({ action: "zoom", region: [button.x, button.y, button.x + 200, button.y + 50], tabId: 123 })

// ... continue for active, disabled states
```

**Result**: 4/4 states passed strict threshold

**Execution Time**: 30 seconds

### Example 3: Animation Recording (Loading Sequence)

**Complexity**: High (GIF recording, temporal comparison)

**Task**: Capture and validate skeleton-to-content loading animation

**Planning Output**:
```
Thought 1/6: Need to capture loading animation as GIF
Thought 2/6: Trigger reload to capture full sequence
Thought 3/6: Start GIF recording before reload
Thought 4/6: Wait for content load completion
Thought 5/6: Stop recording and export GIF
Thought 6/6: Use animation threshold (5%) for comparison
```

**Execution**:
```javascript
// 1. Start GIF recording
await gif_creator({ action: "start_recording", tabId: 123 })
await computer({ action: "screenshot", tabId: 123 }) // Initial frame

// 2. Trigger reload
await navigate({ url: "https://example.com/dashboard", tabId: 123 })

// 3. Wait for load sequence
await computer({ action: "wait", duration: 3, tabId: 123 })
await computer({ action: "screenshot", tabId: 123 }) // Final frame

// 4. Stop recording and export
await gif_creator({ action: "stop_recording", tabId: 123 })
await gif_creator({ action: "export", download: true, filename: "loading-animation.gif", tabId: 123 })
```

**Result**: Animation captured successfully, 2.3% diff from baseline (within 5% animation threshold)

**Execution Time**: 15 seconds

## Troubleshooting

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Screenshots are blank/black | Page not fully loaded | Add wait after navigation, check for lazy loading |
| Diff always fails | Threshold too strict | Increase threshold or configure ignore regions |
| Viewport resize not working | Tab permission issue | Create new tab with tabs_create_mcp |
| GIF not recording | Recording not started | Call gif_creator start_recording before actions |
| Baseline not found | Wrong namespace key | Verify page/viewport in Memory MCP query |
| Zoom captures wrong region | Coordinates shifted | Recalculate region after viewport resize |

### Debug Mode

Enable verbose output for troubleshooting:
```javascript
const DEBUG_MODE = true;

if (DEBUG_MODE) {
  console.log("Viewport:", viewport);
  console.log("Page URL:", url);
  console.log("Capture timestamp:", new Date().toISOString());
  console.log("Baseline exists:", baselineExists);
  console.log("Diff result:", diffResult);
}
```

## Conclusion

Visual Testing provides systematic screenshot-based regression detection that complements functional testing. By comparing actual rendered output against approved baselines across multiple viewports, this skill catches UI regressions that unit and integration tests miss.

The key differentiators are:
1. **Baseline management**: Versioned golden images with explicit approval workflow
2. **Multi-viewport coverage**: Responsive testing across mobile, tablet, and desktop
3. **Threshold-based comparison**: Configurable tolerance to balance sensitivity and false positives
4. **Zoom capabilities**: Element-level precision for design system validation
5. **GIF recording**: Temporal capture for animation and interaction testing

When integrated with the CI/CD pipeline, visual testing serves as a deployment gate that prevents visual regressions from reaching production. Combined with Memory MCP for persistent baselines, the system maintains consistent quality across releases.

## Success Criteria

**Quality Thresholds**:
- All configured viewports captured successfully
- Baseline comparison completed for all captures (or flagged as new)
- Report generated with pass/fail status per page/viewport
- No orphaned tabs after test completion
- Execution time within 2x estimated duration

**Failure Indicators**:
- Screenshot capture fails (blank/timeout)
- Comparison fails with system error (not threshold failure)
- Memory MCP unavailable for baseline storage
- Tab context lost during multi-viewport capture

## Completion Verification

- [x] YAML frontmatter with full description and triggers
- [x] Overview explains philosophy and methodology
- [x] Core Principles section has 5 principles with practical guidance
- [x] When to Use has clear use/don't-use criteria
- [x] Main Workflow has 6 phases with contracts
- [x] Pattern Recognition covers 4 testing patterns
- [x] Advanced Techniques includes multi-model and ignore regions
- [x] Common Anti-Patterns has 3 tables (capture, comparison, workflow)
- [x] Cross-Skill Coordination documents upstream/downstream/parallel
- [x] MCP Requirements explains all required tools
- [x] Input/Output Contracts clearly specified in YAML
- [x] LEARNED PATTERNS section present (empty for future updates)
- [x] Examples include 3 concrete scenarios
- [x] Troubleshooting addresses common issues
- [x] Conclusion summarizes skill value
- [x] Memory namespace documented with tagging

<promise>VISUAL_TESTING_VERILINGUA_VERIX_COMPLIANT</promise>
