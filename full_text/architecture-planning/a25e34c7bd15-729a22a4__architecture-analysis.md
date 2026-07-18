---
name: architecture-analysis
description: >
  Run risk and design-characteristics analyses over ARCHITECTURE.md documentation.
  Produces date-stamped reports in analysis/ covering ten lenses across two groups:
  HIGH-priority runtime/security — SPOF (single points of failure), Blast Radius
  (downstream cascade impact), Bottleneck (throughput chokepoints), Cost Hotspots
  (Pareto cost concentration), STRIDE (per-trust-boundary security threats);
  Strategic/sustainability — Vendor Lock-in (portability risk and exit cost),
  Latency Budget (per-hop SLO decomposition), Tech Debt/EOL (currency and deprecated tech),
  Coupling (fan-in/fan-out and cycles), Data Sensitivity (PII flow and encryption gaps).
  Each analysis can be requested individually, as a group, or all ten run in parallel.
  A consolidated Security Posture option (analysis 12) merges the STRIDE and Data Sensitivity
  reports into a single reviewer-fillable validation checklist of every security control to
  validate (markdown-only; exportable to a Word worksheet via architecture-docs-export).
  Output: analysis/<TYPE>-<YYYY-MM-DD>.md (default) OR analysis/<TYPE>-<YYYY-MM-DD>.html
  (interactive d3.js report; format is selected at runtime — Step 2.4).
  Requires ARCHITECTURE.md to exist (created by architecture-docs skill).
  Do NOT invoke for compliance contracts (use architecture-compliance),
  peer quality review (use architecture-peer-review), or ADR management (use architecture-definition-record).
---

# Architecture Analysis Skill

## Purpose

This skill produces **risk and design-characteristics analyses** over an architecture's documentation — the kind of assessments that come out of an architecture review meeting, pre-incident review, or release-readiness audit.

It bundles **ten focused analyses** across two groups, each driven by a dedicated spec and a universal sub-agent:

**HIGH-priority (runtime / security risk):**

| # | Analysis | Lens | Output |
|---|----------|------|--------|
| 1 | **SPOF** | Single points of failure → full outage / degradation / operational | `analysis/SPOF-<date>.md` |
| 2 | **Blast Radius** | Per-component downstream cascade impact | `analysis/BLAST-RADIUS-<date>.md` |
| 3 | **Bottleneck** | Throughput chokepoints and capacity headroom | `analysis/BOTTLENECK-<date>.md` |
| 4 | **Cost Hotspots** | Pareto cost concentration and over-provisioning | `analysis/COST-HOTSPOTS-<date>.md` |
| 5 | **STRIDE** | Security threats per trust boundary | `analysis/STRIDE-<date>.md` |

**Strategic / sustainability:**

| # | Analysis | Lens | Output |
|---|----------|------|--------|
| 6 | **Vendor Lock-in** | Portability risk, exit cost, vendor concentration | `analysis/VENDOR-LOCKIN-<date>.md` |
| 7 | **Latency Budget** | Per-hop SLO decomposition, over-budget hops | `analysis/LATENCY-BUDGET-<date>.md` |
| 8 | **Tech Debt / EOL** | Technology currency, deprecated SDKs, ADR debt | `analysis/TECH-DEBT-<date>.md` |
| 9 | **Coupling** | Fan-in/fan-out, instability, cyclical dependencies | `analysis/COUPLING-<date>.md` |
| 10 | **Data Sensitivity** | PII data flows, encryption gaps, retention compliance | `analysis/DATA-SENSITIVITY-<date>.md` |

**Distinct from:**
- `architecture-peer-review` — evaluates *document quality* (structure, completeness, coherence). This skill evaluates *runtime and operational risk*.
- `architecture-compliance` — generates contract adherence documents (10 compliance types). This skill produces architectural risk reports.
- `architecture-traceability` — maps PO Spec use cases to architecture sections. This skill has no dependency on a PO Spec.

---

## When to Invoke This Skill

- Before a release-readiness review or architecture gate
- During an annual architecture audit
- After a major architectural change (new component, ADR superseded, Redis removed, etc.)
- Pre-incident risk assessment or chaos engineering planning
- User asks: "find my SPOFs", "blast radius analysis", "where are my bottlenecks", "cost analysis of my architecture", "threat model my architecture", "run all analyses"
- Use `/skill architecture-analysis`

**Do NOT invoke for:**
- Document quality review → `architecture-peer-review`
- Compliance contract generation → `architecture-compliance`
- Requirements traceability → `architecture-traceability`
- ADR creation or update → `architecture-definition-record`

---

## Files in This Skill

| File | Purpose |
|------|---------|
| `SKILL.md` | This file — dispatcher, menu, orchestration |
| `analyses/SPOF.md` | Classification rules and report spec for SPOF analysis |
| `analyses/BLAST_RADIUS.md` | Classification rules and report spec for Blast Radius analysis |
| `analyses/BOTTLENECK.md` | Classification rules and report spec for Bottleneck analysis |
| `analyses/COST_HOTSPOTS.md` | Classification rules and report spec for Cost Hotspots analysis |
| `analyses/STRIDE.md` | Classification rules and report spec for STRIDE Threat Model |
| `analyses/VENDOR_LOCKIN.md` | Classification rules and report spec for Vendor Lock-in analysis |
| `analyses/LATENCY_BUDGET.md` | Classification rules and report spec for Latency Budget analysis |
| `analyses/TECH_DEBT.md` | Classification rules and report spec for Tech Debt / EOL analysis |
| `analyses/COUPLING.md` | Classification rules and report spec for Coupling / Fan-out analysis |
| `analyses/DATA_SENSITIVITY.md` | Classification rules and report spec for Data Sensitivity & Flow analysis |
| `analyses/SECURITY_POSTURE.md` | Consolidation spec — merges the STRIDE + Data Sensitivity reports into a reviewer-fillable Security Posture validation checklist (markdown-only) |
| `templates/analysis-report-skeleton.md` | Shared section structure for all Markdown analysis reports |
| `templates/analysis-report-html-skeleton.html` | Shared HTML shell (d3.js v7 + d3-sankey, corporate styling) for the HTML output mode |
| `templates/viz/<analysis_type>.html` | One self-contained d3 viz snippet per analysis type (10 files); inlined into the HTML shell at render time |

---

## Step 0 — Resolve Plugin Directory

Before any workflow, resolve the absolute path to the plugin installation so spec files can be loaded by the sub-agent.

**Step A — Glob (dev/local mode)**:

Glob for: `**/{sa-skills,solutions-architect-skills}/skills/architecture-analysis/SKILL.md`

The brace expansion matches both marketplace installs (`sa-skills/` in `~/.claude/plugins/cache/...`) and local dev clones (historical repo folder `solutions-architect-skills/`). If found, strip `/skills/architecture-analysis/SKILL.md` from the result to get `plugin_dir`.

**Step B — Marketplace fallback**:

If Glob returns nothing, set:
```
plugin_dir = ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace
```

Store `plugin_dir` for use in all agent prompts.

---

## Step 1 — Locate Architecture Document

Search for `ARCHITECTURE.md` at the project root. Determine doc structure:

- **Multi-file**: `ARCHITECTURE.md` exists as a navigation index + `docs/NN-*.md` section files + `docs/components/` per-component files
- **Monolithic**: a single `ARCHITECTURE.md` file containing all sections

If no `ARCHITECTURE.md` is found, abort:
```
❌ No ARCHITECTURE.md found. Use /skill architecture-docs to create one first.
```

Build `doc_files` — an ordered list of absolute file paths to pass to each agent:
1. `ARCHITECTURE.md` (always)
2. `docs/NN-*.md` section files in numeric order (if `docs/` exists)
3. `docs/components/README.md` and `docs/components/**/*.md` in numeric order
4. All `adr/ADR-*.md` files in alphabetic order
5. `compliance-docs/COMPLIANCE_MANIFEST.md` (if present — used for SPOF and STRIDE cross-reference)

---

## Step 2 — Select Analyses (BLOCKING — user must choose)

Present the analysis menu. **Do not default or assume.** If the user says "analyze my architecture" without specifying which, present this menu:

```
═══════════════════════════════════════════════════════════
Architecture Analysis — choose analyses to run:
═══════════════════════════════════════════════════════════

  HIGH-priority (runtime / security risk):
   1. SPOF             (Single Points of Failure)        1 agent
      Critical, Degradation, and Operational failure modes with Heat Map

   2. Blast Radius     (Downstream cascade impact)       1 agent
      Per-component fan-out, cascade severity, bulkhead assessment

   3. Bottleneck       (Throughput chokepoints)          1 agent
      Serial chokepoints, connection saturation, capacity headroom

   4. Cost Hotspots    (Cost concentration)              1 agent
      Pareto cost ranking, over-provisioning candidates, vendor lock-in cost

   5. STRIDE           (Security threats per boundary)   1 agent
      Per-trust-boundary STRIDE matrix, high-priority threats

  Strategic / sustainability:
   6. Vendor Lock-in   (Portability risk, exit cost)     1 agent
      L1/L2/L3 lock tiers, vendor concentration, exit cost ranking

   7. Latency Budget   (Per-hop SLO decomposition)       1 agent
      Per-flow budget breakdown, over-budget hops, tail-latency variance

   8. Tech Debt / EOL  (Currency, deprecated tech)       1 agent
      EOL hotlist, deprecated SDKs, unimplemented ADR replacements

   9. Coupling         (Fan-in/fan-out, cycles)          1 agent
      Critical hubs, volatile leaves, god objects, cyclical dependencies

  10. Data Sensitivity (PII flow, encryption gaps)       1 agent
      Data inventory, encryption/retention gaps, sensitive flow map

  11. All ten (parallel)                                  10 agents

  Consolidated (security):
  12. Security Posture (validation checklist)             1 agent
      Merges STRIDE (5) + Data Sensitivity (10) into one reviewer-fillable
      checklist of every security control to validate. Markdown-only.
      Requires the STRIDE and Data Sensitivity reports — runs them first if absent.

═══════════════════════════════════════════════════════════
Selection (e.g. "1", "1,3,5", "6-10", "12", or "all"):
```

**Parse user selection:**
- `all` or `11` → run analyses 1–10
- `1-5` → run only the HIGH-priority group (analyses 1–5)
- `6-10` → run only the Strategic group (analyses 6–10)
- `12` → run the **Security Posture** consolidation (see Step 2.6 — it depends on analyses 5 and 10)
- Comma-separated numbers → run only those analyses
- Single number → run one analysis

**Security Posture dependency**: whenever `12` is in the selection, analyses **5 (STRIDE)**
and **10 (Data Sensitivity)** must have produced reports first. See Step 2.6 for how the
orchestrator satisfies this (consume existing reports, or schedule 5 + 10 ahead of 12).

---

## Step 2.4 — Select Output Format (BLOCKING — user must choose)

After the analysis selection above, present the output format menu. **Do not assume.** The choice applies to **every** analysis dispatched in this run.

```
═══════════════════════════════════════════════════════════
Output format:
═══════════════════════════════════════════════════════════
   1. Markdown   analysis/<TYPE>-<date>.md
      Plain text, grep-friendly, default. ASCII heat maps / pipe tables.

   2. HTML       analysis/<TYPE>-<date>.html
      Interactive corporate-grade report rendered with d3.js v7
      (heat maps, dependency networks, Pareto charts, Sankey, chord, …).
      Loads d3.js from the jsDelivr CDN (cdn.jsdelivr.net) — internet required
      to view the visualisations. Tables/text render fine offline.

Selection (1 or 2):
═══════════════════════════════════════════════════════════
```

**Parse user selection:**
- `1` or `markdown` or `md` → `output_format = "markdown"`
- `2` or `html` → `output_format = "html"`

Store `output_format` for use in Step 3 agent prompts. If anything else is entered, re-prompt — do not default silently.

**Security Posture is markdown-only**: analysis 12 has no HTML/d3 viz mode (it is a
worksheet, not a visualization). If the user selected `12` *and* chose HTML, run analysis 12
in markdown regardless and tell the user: "Security Posture is a validation checklist —
exported as markdown; the HTML format applies to the other selected analyses." Any
non-consolidation analyses in the same run still honor the chosen format.

---

## Step 2.6 — Security Posture dependency resolution (only when analysis 12 is selected)

Security Posture (`security-posture`) is a **consolidation** — it reads the `STRIDE` and
`Data Sensitivity` reports rather than the architecture docs. Before dispatching it:

1. **Locate the source reports** — glob `analysis/STRIDE-*.md` and
   `analysis/DATA-SENSITIVITY-*.md`; pick the most recent date for each.
2. **Satisfy missing sources**:
   - If the user also selected 5 and/or 10 in this run, let those run first (Step 3 dispatches
     all non-consolidation analyses before the consolidation batch); use their fresh outputs.
   - If a source report is **not** selected and **not** found on disk, **add that analysis to
     this run** (STRIDE and/or Data Sensitivity, markdown) so it executes ahead of 12, and
     tell the user: "Security Posture requires the <STRIDE|Data Sensitivity> report — running
     it first."
   - If a source report is **not** selected but **already exists** on disk (any prior date),
     consume the most recent on-disk file as-is (do not re-run it).
3. **Record the resolved source paths** for the Step 3 dispatch of analysis 12.

Always dispatch `security-posture` **last** — after STRIDE and Data Sensitivity have written
their reports in this run (or after confirming the on-disk files exist).

---

## Step 2.5 — Per-analysis explorer findings fan-out (v3.16.0+)

Spawn `sa-skills:architecture-explorer` **once per selected analysis** in findings mode. Each call passes a hardcoded vocabulary `query` lifted from the analysis's spec ("Evidence Extraction Priority" table + rule examples). The explorer emits an `EXPLORE_FINDINGS` block listing the matched files with line-level matches, headings, and 3–5-line excerpts — pre-located evidence the analysis agent reads in step.

**Exclude `security-posture` from this fan-out.** It does not read architecture docs — its
inputs are the STRIDE + Data Sensitivity reports resolved in Step 2.6. Do not spawn an
explorer for analysis 12.

**Per-analysis vocabulary** (joined as a comma-separated string for the `query` parameter):

| Analysis | Vocabulary |
|----------|------------|
| `spof` | single point of failure, failover, redundancy, HA, multi-region, multi-AZ, active-active, circuit breaker |
| `blast-radius` | downstream, dependency, cascade, fan-out, retry, timeout, bulkhead |
| `bottleneck` | throughput, capacity, headroom, queue, backpressure, p99, saturation |
| `cost-hotspots` | cost, pricing, instance, GB-month, reserved, spot, FinOps, billing |
| `stride` | trust boundary, authentication, authorization, mTLS, encryption, audit, RBAC, threat |
| `vendor-lockin` | vendor, proprietary, portability, exit, migration, lock-in, managed service |
| `latency-budget` | latency, p95, p99, SLO, hop, budget, end-to-end |
| `tech-debt` | EOL, end of life, deprecated, legacy, version, sunset, upgrade |
| `coupling` | coupling, fan-in, fan-out, instability, cycle, dependency direction |
| `data-sensitivity` | PII, encryption at rest, encryption in transit, retention, GDPR, data classification |

**Per-analysis spawn**:
```
Task(sa-skills:architecture-explorer)
prompt:
  project_root: <dirname(architecture_file)>
  query: <vocabulary[type] joined as ", ">
  caller: orchestrator-analysis
```

The `caller` field is a contract anchor (see the explorer's Input Parameters): it does not change the explorer's output, but it gives the haiku a structured signal that a string-scanning orchestrator is reading the result, reducing the chance of prose drift.

**Batching**: dispatch in **parallel batches of 4 per message** to keep the explorer fan-out cost-bounded while preserving wall-clock parallelism. After each batch returns, collect the results before sending the next.

Collect each analysis's `EXPLORE_FINDINGS` block keyed by analysis type:

```
findings_by_analysis = {
  "spof":             "<EXPLORE_FINDINGS YAML body>",
  "stride":           "<EXPLORE_FINDINGS YAML body>",
  ...
}
```

**Build the FILES list per analysis** as `union(base_files[type], findings.files[*].file)` — base is the always-read floor that guarantees domain coverage even when no findings match; findings adds where evidence actually lives. The base sets:

| Analysis | Base FILES (always) |
|----------|---------------------|
| `spof` | ARCHITECTURE.md, docs/03-architecture-layers.md, docs/components/README.md |
| `blast-radius` | ARCHITECTURE.md, docs/04-data-flow-patterns.md, docs/05-integration-points.md, docs/components/README.md |
| `bottleneck` | ARCHITECTURE.md, docs/08-scalability-and-performance.md, docs/04-data-flow-patterns.md, docs/components/README.md |
| `cost-hotspots` | ARCHITECTURE.md, docs/06-technology-stack.md, docs/09-operational-considerations.md |
| `stride` | ARCHITECTURE.md, docs/07-security-architecture.md, docs/05-integration-points.md, docs/components/README.md |
| `vendor-lockin` | ARCHITECTURE.md, docs/06-technology-stack.md, docs/03-architecture-layers.md |
| `latency-budget` | ARCHITECTURE.md, docs/04-data-flow-patterns.md, docs/08-scalability-and-performance.md |
| `tech-debt` | ARCHITECTURE.md, docs/06-technology-stack.md, docs/03-architecture-layers.md |
| `coupling` | ARCHITECTURE.md, docs/05-integration-points.md, docs/components/README.md |
| `data-sensitivity` | ARCHITECTURE.md, docs/07-security-architecture.md, docs/05-integration-points.md, docs/04-data-flow-patterns.md |

**Malformed-output detection + retry-once** (v3.22.1+): for each explorer reply, check whether the literal token `EXPLORE_FINDINGS:` appears at the start of any line. If absent (the agent returned synthesis prose), spawn **one** retry of the same explorer call with the same `query`, prepending this corrective line to the prompt:

```
Your previous reply did not contain a literal `EXPLORE_FINDINGS:` line followed by a fenced YAML block. Re-run findings mode and obey the Output contract section: first character of your reply must be `E`; exactly one ```yaml ... ``` fence; no prose outside the fence except the optional "no matches" note.
```

The retry is a fresh Task() invocation, capped at 1 per analysis (no exponential backoff). If the retry still lacks `EXPLORE_FINDINGS:`, treat that analysis's call as `FAILED` for the degraded-mode rule below.

**Degraded mode** (fail-open): if any explorer call returns `status: FAILED`, has empty `files[]`, or fails the malformed-output check above (including after the single retry), fall back to that analysis's base FILES table only (plus the universal `doc_files` from Step 1 if the failure is universal). The analysis still runs.

---

## Step 3 — Spawn Analysis Agents (Parallel)

For each selected analysis, determine:
- `analysis_type` — one of: `spof`, `blast-radius`, `bottleneck`, `cost-hotspots`, `stride`, `vendor-lockin`, `latency-budget`, `tech-debt`, `coupling`, `data-sensitivity`
- `spec_path` — `{plugin_dir}/skills/architecture-analysis/analyses/<SPEC_FILE>.md`
- `skeleton_path` — `{plugin_dir}/skills/architecture-analysis/templates/analysis-report-skeleton.md` (always passed; agent ignores when format is HTML)
- `output_path` — `analysis/<TYPE>-<YYYY-MM-DD>.<ext>` where `<ext>` is `md` when `output_format == "markdown"` and `html` when `output_format == "html"` (and `<TYPE>` is uppercase with hyphens matching the file convention below)
- **HTML mode only** (when `output_format == "html"`):
  - `html_skeleton_path` — `{plugin_dir}/skills/architecture-analysis/templates/analysis-report-html-skeleton.html`
  - `viz_template_path` — `{plugin_dir}/skills/architecture-analysis/templates/viz/<analysis_type>.html`

| Analysis | `analysis_type` | Spec file | Output filename |
|----------|----------------|-----------|-----------------|
| SPOF | `spof` | `SPOF.md` | `SPOF-<date>.md` |
| Blast Radius | `blast-radius` | `BLAST_RADIUS.md` | `BLAST-RADIUS-<date>.md` |
| Bottleneck | `bottleneck` | `BOTTLENECK.md` | `BOTTLENECK-<date>.md` |
| Cost Hotspots | `cost-hotspots` | `COST_HOTSPOTS.md` | `COST-HOTSPOTS-<date>.md` |
| STRIDE | `stride` | `STRIDE.md` | `STRIDE-<date>.md` |
| Vendor Lock-in | `vendor-lockin` | `VENDOR_LOCKIN.md` | `VENDOR-LOCKIN-<date>.md` |
| Latency Budget | `latency-budget` | `LATENCY_BUDGET.md` | `LATENCY-BUDGET-<date>.md` |
| Tech Debt / EOL | `tech-debt` | `TECH_DEBT.md` | `TECH-DEBT-<date>.md` |
| Coupling | `coupling` | `COUPLING.md` | `COUPLING-<date>.md` |
| Data Sensitivity | `data-sensitivity` | `DATA_SENSITIVITY.md` | `DATA-SENSITIVITY-<date>.md` |
| Security Posture | `security-posture` | `SECURITY_POSTURE.md` | `SECURITY-POSTURE-<date>.md` (markdown-only) |

**Security Posture dispatch (consolidation — analysis 12)**: dispatch it **last**, in its own
final batch, after STRIDE and Data Sensitivity have written their reports this run (or after
confirming on-disk reports per Step 2.6). It is **always** markdown (`output_format=markdown`,
`.md` extension) and is **never** given `html_skeleton_path` / `viz_template_path`. Its FILES
list is **not** built from an explorer call; instead set it explicitly to:

```
FILES:
<absolute path to the resolved analysis/STRIDE-<date>.md>
<absolute path to the resolved analysis/DATA-SENSITIVITY-<date>.md>
<absolute path to ARCHITECTURE.md>
<absolute path to docs/components/README.md (if present)>
```

(Paths resolved in Step 2.6. If one primary report is absent, omit its line — the spec's
missing-source rule renders the gap. ARCHITECTURE.md is included only so the agent can read
the solution name / version for the report header.)

**Ensure `analysis/` directory exists** (cross-platform Bun helper — replaces `mkdir -p analysis`):
```bash
bun [plugin_dir]/scripts/ensure-dir.ts analysis
```

Issue Task() calls in **batches of 2 per message** (strict parallel barrier).

**Batching rule**: dispatch exactly **2 Task() calls per message**. After sending a batch, wait for BOTH agents to write their output files before sending the next batch. Do not start batch N+1 until every Task() in batch N has returned. If any analysis agent in a batch fails, record the failure and continue with the next batch (do not retry inline; failures are collected and reported at the end). This caps peak parallelism at 2 and gives the orchestrator a chance to observe early failures before dispatching the remaining batches. For all 10 analyses this is 5 batches; when the user picks a subset, round up (e.g., 3 = 2 batches of 2+1).

Each call (markdown mode):

```
subagent_type: sa-skills:architecture-analysis-agent

Prompt:
analysis_type: <type>
output_format: markdown
spec_path: <absolute path to spec .md file>
skeleton_path: <absolute path to analysis-report-skeleton.md>
output_path: <absolute path to output .md file>
today: <YYYY-MM-DD>

FILES:
<absolute path 1 — ARCHITECTURE.md>
<absolute path 2 — docs/01-system-overview.md>
...
<absolute path N — last file>
```

Each call (HTML mode — adds three lines):

```
subagent_type: sa-skills:architecture-analysis-agent

Prompt:
analysis_type: <type>
output_format: html
spec_path: <absolute path to spec .md file>
skeleton_path: <absolute path to analysis-report-skeleton.md>
html_skeleton_path: <absolute path to analysis-report-html-skeleton.html>
viz_template_path: <absolute path to templates/viz/<analysis_type>.html>
output_path: <absolute path to output .html file>
today: <YYYY-MM-DD>

FILES:
<absolute path 1 — ARCHITECTURE.md>
...
```

**File selection (v3.16.0+)**: the FILES list is `union(base_files[type], findings_by_analysis[type].files[*].file)` — the per-analysis base set from Step 2.5 (always-read floor) unioned with the files surfaced by that analysis's findings call. Typical list size: 5–10 paths per analysis instead of the full corpus. Order: base files first (in the order listed), then any additional findings files.

If Step 2.5 reported `status: FAILED` or empty `files[]` for a given analysis, that analysis's FILES list collapses to its base set only. If the explorer was unreachable for the entire run, fall back to the universal `doc_files` from Step 1 for every analysis. The agent runs identically; just without the trim.

Set each `description` to `"<Analysis Name> analysis"` (e.g., `"SPOF analysis"`).

**[BARRIER — wait for the current batch to complete before dispatching the next batch, and wait for the final batch before proceeding to Step 4]**

---

## Step 4 — Collect Results and Report

After all agents return, collect each agent's one-line summary.

**Check for failures**: if any agent failed to produce an output file, report:
```
⚠️ <Analysis Name> agent failed — <error summary>
   You can re-run this analysis by selecting option <N> again.
```

**Print completion summary** — file extension is `.md` when `output_format == "markdown"` and `.html` when `output_format == "html"` (same one-line summary content either way):

```
═══════════════════════════════════════════════════════════
✅ Architecture Analysis Complete  (format: <markdown|html>)
═══════════════════════════════════════════════════════════

  HIGH-priority analyses:
  analysis/SPOF-2026-04-16.<ext>              6 critical · 5 degradation · 3 operational
  analysis/BLAST-RADIUS-2026-04-16.<ext>      3 high-blast · 4 isolated components
  analysis/BOTTLENECK-2026-04-16.<ext>        4 chokepoints · top: API Gateway (fan-in ×8)
  analysis/COST-HOTSPOTS-2026-04-16.<ext>     top hotspot: Confluent Kafka ($2,100/mo)
  analysis/STRIDE-2026-04-16.<ext>            8 high · 5 medium · 3 low priority threats

  Strategic / sustainability analyses:
  analysis/VENDOR-LOCKIN-2026-04-16.<ext>     5 L1-locked · 3 L2-lock-prone · Azure 68% concentration
  analysis/LATENCY-BUDGET-2026-04-16.<ext>    2 flows over budget · top offender: Auth0 (+140ms)
  analysis/TECH-DEBT-2026-04-16.<ext>         1 EOL-now · 2 EOL-≤6mo · 3 deprecated SDKs
  analysis/COUPLING-2026-04-16.<ext>          2 critical hubs · 1 god object · 0 cycles
  analysis/DATA-SENSITIVITY-2026-04-16.<ext>  3 G1 encryption gaps · 1 G3 retention breach

  Consolidated (when analysis 12 was selected):
  analysis/SECURITY-POSTURE-2026-04-16.md     42 checks · 31 documented · 11 gaps (4 high)

═══════════════════════════════════════════════════════════
Next steps:
  • Review reports in analysis/ — each finding includes source citations
  • Address Documentation Gaps entries to improve future analysis accuracy
  • Export the Security Posture checklist to Word: /skill architecture-docs-export
    (select Security Posture mode — produces a reviewer-fillable .docx)
  • Export any other analysis to Word: /skill architecture-docs-export  (select Compliance
    Contract mode on the analysis .md file — Word export is Markdown-only)
═══════════════════════════════════════════════════════════
```

**When `output_format == "html"`**, append the following block before the context-reclaim hint:

```
💡 Open any report in your browser to explore the d3 visualisations:
     open analysis/SPOF-<date>.html        (macOS)
     xdg-open analysis/SPOF-<date>.html    (Linux)
     start analysis/SPOF-<date>.html       (Windows)

   The HTML reports load d3.js from the jsDelivr CDN — internet is required
   to render the charts. Tables, summaries, recommendations, and citations
   render fine offline; only the interactive viz needs the CDN.
```

**After printing the completion summary above, always append the following user-visible context-reclaim hint** (verbatim, as the final lines of the skill's output):

```
💡 Tip: all analysis reports are written to `analysis/`. To reclaim context from the analysis-agent responses before your next task, run:
    /compact
```

---

## Documentation Fidelity Rule

Every finding in every analysis report MUST cite the source file and section it was derived from (e.g., `(source: docs/08-scalability-and-performance.md — Section "HPA Configuration")`). Agents must NOT invent components, costs, trust boundaries, or risks not present in the architecture documentation. Where required data is absent, the finding is marked `[NOT DOCUMENTED — add to <source-file>]` and listed in a **Documentation Gaps** section at the report footer.

---

## Output Location

All analysis reports are written to `analysis/` at the project root. Files are date-stamped — re-running the same analysis on the same day with the same format overwrites the existing file; re-running on a new date creates a new file, preserving history. Re-running the same date with a different format produces a sibling file with the other extension (`.md` and `.html` can coexist).

```
analysis/
├── SPOF-2026-04-16.md            (or .html — chosen at Step 2.4)
├── BLAST-RADIUS-2026-04-16.md
├── BOTTLENECK-2026-04-16.md
├── COST-HOTSPOTS-2026-04-16.md
├── STRIDE-2026-04-16.md
├── VENDOR-LOCKIN-2026-04-16.md
├── LATENCY-BUDGET-2026-04-16.md
├── TECH-DEBT-2026-04-16.md
├── COUPLING-2026-04-16.md
├── DATA-SENSITIVITY-2026-04-16.md
└── SECURITY-POSTURE-2026-04-16.md   (consolidation of STRIDE + Data Sensitivity — markdown-only)
```

### HTML format notes

- HTML reports are **self-contained single files** — no sibling assets, no build step. Just open in a browser.
- d3.js v7 and d3-sankey are loaded from the jsDelivr CDN (`https://cdn.jsdelivr.net/npm/...`). **No internet** → tables and prose still render, but the viz `<div>` falls back to "Visualization unavailable without d3.js." A user-visible banner makes the fallback explicit.
- HTML mode is intended for socialisation with non-engineering stakeholders (architects, security, finance). Markdown mode remains the default for in-repo review, grep, and Word export via `architecture-docs-export`.
- The HTML and Markdown reports contain the **same findings** — no information is invented for the viz that isn't also in the findings tables.
- **Spec sections defined as ASCII heat maps, ASCII bar charts, ASCII histograms, or Mermaid diagrams are OMITTED in HTML mode** — the per-analysis d3 viz is the canonical HTML rendering of that content (see the agent's Phase 5b.0 omission table). Markdown mode renders the spec's ASCII / Mermaid blocks unchanged. Cascade scenarios (`blast-radius`) and cycle subgraphs (`coupling`) and per-flow sequence diagrams (`data-sensitivity`) are surfaced in HTML mode as HTML tables, not as hand-coded SVG.

---

## Prerequisites

- `ARCHITECTURE.md` created by `/skill architecture-docs`
- `docs/` directory with section files (multi-file architecture recommended for richer analysis)
- `docs/components/` with per-component files (required for Blast Radius and Bottleneck analysis)
- `compliance-docs/` (optional — used by SPOF and STRIDE for cross-reference enrichment)
- ADR files in `adr/` (optional — used to surface risk decisions)

---

## Permissions Required

Add to your project's `.claude/settings.json`:

```json
"Write(analysis/*)",
"Read(analysis/*)",
"Bash(mkdir *)",
"Agent(sa-skills:architecture-analysis-agent)",
"WebSearch"
```

**`WebSearch` is required for the Tech Debt / EOL analysis.** The agent uses it to validate documented EOL dates against vendor product-lifecycle pages (`endoflife.date`, `learn.microsoft.com/lifecycle`, `nodejs.org`, etc.) — see `analyses/TECH_DEBT.md` § "EOL Validation Protocol". Other analyses (SPOF, Blast Radius, Bottleneck, Cost, STRIDE, Vendor Lock-in, Latency Budget, Coupling, Data Sensitivity) do not call WebSearch. If `WebSearch` is omitted, the Tech Debt analysis still completes but produces a `WebSearch unavailable` notice and may report stale EOL data.
