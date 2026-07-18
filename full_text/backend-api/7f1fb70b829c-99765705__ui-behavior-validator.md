---
name: ui-behavior-validator
description: >-
  Detects "everything passes but it doesn't work" defects where unit and
  integration tests pass, docs are current, and code review looks clean,
  yet the running system silently shows zero, null, default, or stale
  values that contradict backend reality. Cross-validates a five-tuple
  contract (DB field → query → API field → UI element → trace manifest)
  against a live system by probing each layer independently, asserting
  agreement, and using MCP-driven trace correlation through Grafana
  Tempo/Loki/Mimir. Supports Ratatui, GTK, and web stacks. Refuses to run
  unless the OTel Collector enforces PII redaction. Outputs schema-
  validated findings.json plus per-contract evidence. Triggers: validate
  the UI, value-flow validation, why does X show zero, metric never
  updates, field is empty but API works, audit Gherkin coverage,
  post-iterate validation, PR review for UI/data changes, post-deploy
  canary, behavior validation.
license: Apache-2.0
metadata:
  version: 2.0.0
  author: skills-repo
  artifacts-root: artifacts/ui-behavior-validator
  consumers: ["/story-creator", "/adr-create", "/iterate"]
required-mcp-servers:
  - { name: grafana,      type: "grafana/mcp-grafana", flags: ["--disable-write"] }
  - { name: tempo-direct, type: "tempo-mcp" }
compatibility: >-
  Requires Rust 1.84+, Python 3.11+, OTel Collector with redaction
  processors, and Tempo 2.x + Loki + Mimir (or SigNoz) reachable from the
  agent host. `mcp-grafana` v0.14+ and `tempo-mcp` must be on
  PATH. Optional: D-Bus for GTK AT-SPI, Chrome/Chromium for web. Hook
  paths assume install at ~/.claude/skills/ui-behavior-validator/.
allowed-tools: >-
  Read Write Edit Glob Grep Bash(cargo*) Bash(python3*) Bash(surreal*)
  Bash(curl*) Bash(jq*) Bash(rg*) Bash(git*) Bash(npx*) Bash(otelcol*)
  Bash(docker*) Agent Skill AskUserQuestion WebFetch WebSearch
---

# UI Behavior Validator

You catch the defect class where every test layer passes but the running
system still lies. The five-tuple contract — DB field → query → API field
→ UI element → trace manifest — turns "did it work?" into an executable
assertion over four independent ground truths plus an observability
witness. When they disagree, you localize the divergence and emit
schema-validated findings that downstream skills consume directly.

## When to Use This Skill

- Right after `/iterate` closes a UI- or data-touching ticket — run contracts tagged `regression`
- During PR review when the diff touches `src/tui/**`, `src/api/**`, `src/db/**`, schema files, `features/**`, or `*.openapi.{json,yaml}` — run contracts tagged `pr-gate`
- Within ten minutes of a deploy marker — run contracts tagged `canary` against the canary URL or staging binary
- Bug-bash sessions — run the full contract set with `--explore` (LLM judge enabled)
- Explicit phrases: "validate the UI", "why does X show zero", "the metric never updates", "the field is empty but the API works", "audit Gherkin coverage", "check the canary", "value-flow validation"

## Quick Start

Arguments: `[--contract <id>] [--target <bin-or-url>] [--api <url>] [--explore] [--force]`

Defaults: discover all `assets/contracts/*.contract.yaml`, target binary
from `Cargo.toml`'s default-run, API at `http://localhost:3030`. Artefacts
land under `artifacts/ui-behavior-validator/<run-id>/`.

The skill walks six phases in strict order. Phase 0 is non-negotiable —
if the foundation's broken, every backend probe lies, so the skill halts
and emits one `INFRASTRUCTURE_GAP` finding instead of running the rest.

1. **Phase 0** — instrumentation audit (mandatory)
2. **Phase 1** — discovery (DB schema, OpenAPI, UI elements, Gherkin, trace topology)
3. **Phase 2** — modeling (five-tuple contracts; hand-authored or inferred)
4. **Phase 3** — probing (MCP-driven, one probe per contract)
5. **Phase 4** — diff and triage (predicate cascade, first match wins)
6. **Phase 5** — reporting (schema-validated findings.json + evidence/)

## Live context (auto-injected at load)

- Repo root:          !`git rev-parse --show-toplevel 2>/dev/null || echo "n/a"`
- Branch:             !`git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "n/a"`
- mcp-grafana on PATH: !`command -v mcp-grafana >/dev/null && echo yes || echo NO`
- tempo-mcp on PATH: !`command -v tempo-mcp >/dev/null && echo yes || echo NO`
- Contracts found:    !`ls assets/contracts/*.contract.yaml 2>/dev/null | wc -l`
- Last run id:        !`ls -1 artifacts/ui-behavior-validator/ 2>/dev/null | tail -1`

## Architecture

```
  Phase 0: audit OTLP reach, ZMQ propagation, gen_ai.* semconv, PII redaction
       │
       ▼
  Phase 1: discover DB/API/UI/Gherkin/trace-topology → discovery.json
       │
       ▼
  Phase 2: load assets/contracts/*.contract.yaml (or infer via model_contracts.py)
       │
       ▼
  Phase 3: per contract, drive system + read four layers + correlate trace
       │           │              │              │              │
       DB probe    API probe      UI probe       sleep N ms     trace probe
       (Surreal)   (HTTP+trace)   (per stack)    (settle)       (Tempo MCP)
       │
       ▼
  Phase 4: predicate cascade — db_absent → api_stub → trace_orphan → ... → judge
       │
       ▼
  Phase 5: findings.json + report.html + evidence/<contract_id>/
```

## Phase 0 — Instrumentation audit (mandatory, hard-refuse on fail)

The audit checks four properties in order. **Any failure halts the skill
and emits one `INFRASTRUCTURE_GAP` finding.** Don't run probes against an
unobserved system — they'd produce false negatives at industrial scale.

| Check | Script | Failure mode |
|---|---|---|
| OTLP reach (synthetic span lands in Tempo within 15s) | `scripts/phase0/audit_otlp_reach.py` | `INFRASTRUCTURE_GAP/no_otlp_reach` |
| W3C traceparent crosses ZMQ DEALER/ROUTER | `scripts/phase0/audit_zmq_propagation.py` | `INFRASTRUCTURE_GAP/zmq_propagation_broken` |
| Rig agent calls emit `gen_ai.*` semconv | `scripts/phase0/audit_rig_semconv.py` | `INFRASTRUCTURE_GAP/rig_uninstrumented` |
| OTel Collector pipeline enforces PII redaction | `scripts/phase0/audit_pii_redaction.py` | `INFRASTRUCTURE_GAP/pii_pipeline_missing` |

Run them in order. The PII check is the hardest and most often missed —
treat the observability backend as a separate trust zone from the
application. An MCP-armed agent can read any attribute on any span;
unredacted spans become a query-time data leak.

See [references/PII_REDACTION_PLAYBOOK.md](references/PII_REDACTION_PLAYBOOK.md)
for the Collector configuration the audit demands and
[references/MCP_SERVER_SETUP.md](references/MCP_SERVER_SETUP.md) for
wiring `mcp-grafana` and `tempo-mcp` before the first audit.

Emit `Phase 0: PASSED (4/4 checks)` or `Phase 0: HALT — <check> failed`.
On halt, stop immediately. Don't proceed to Phase 1.

## Phase 1 — Discovery

With the foundation confirmed, enumerate everything the contracts cross-
reference. Discovery's read-only; subsequent phases work from
`artifacts/ui-behavior-validator/<run-id>/discovery.json`.

```bash
# DB schema
surreal sql --conn "$SURREAL_URL" --user "$U" --pass "$P" --pretty \
  "INFO FOR DB; INFO FOR TABLE work; INFO FOR TABLE agent; INFO FOR TABLE task"

# API contract
curl -sS http://localhost:3030/api-docs/openapi.json | jq '.'

# UI elements — Ratatui: grep widget render calls
rg --type rust 'Paragraph::new|Cell::from|Span::raw' src/tui/

# Gherkin features
find features/ -name '*.feature' | xargs -I{} basename {} .feature

# Trace topology via MCP
# (these are agent tool calls, not shell — listed for completeness)
# mcp-grafana.list_datasources
# tempo-direct.search_tempo (traceql, last 1h, limit 100)
```

Output: `discovery.json` with the union of `{db_tables[], api_paths[],
ui_elements[], gherkin_scenarios[], known_span_names[], services[]}`.

## Phase 2 — Modeling: the five-tuple contract

Each contract lives at `assets/contracts/<id>.contract.yaml`. See
[references/FIVE_TUPLE_MODEL.md](references/FIVE_TUPLE_MODEL.md) for the
full schema. The example at `assets/contracts/queue_depth.example.contract.yaml`
is the reference shape; copy and adapt.

Skeleton:

```yaml
id: queue_depth
description: "Pending work queue depth shown in TUI metrics panel."

db_field:      { table: work, column: state, where: "state='queued'", type: int }
computation: "SELECT count() FROM work WHERE state='queued' GROUP ALL"
api_field:     { path: /api/v1/metrics, json_pointer: /queue/depth }
ui_element:
  tui: { view: metrics, region: [10,5,20,1], label: "Queued" }

trace_manifest:
  expected_span_names: [http.request, handler.metrics, db.query.work, response.serialize]
  required_attributes:
    - { span: db.query.work, key: db.system, value: surrealdb }
    - { span: handler.metrics, key: noelle.probe.id, present: true }
  forbidden_attributes:
    - { span: handler.metrics, key: noelle.handler.stub, value: true }

bounded_staleness_ms: 15000
inferred: false
```

Hand-authored contracts gate dispatch; `inferred: true` contracts are
suggestions. The `forbidden_attributes` block is what catches teams who
mark stub handlers with `noelle.handler.stub=true` — the marker survives
the refactor, the implementation doesn't.

## Phase 3 — Probing (MCP-driven)

Probing is an agentic loop over contracts, not a hard-coded script. For
each contract, generate a `probe_id` (ULID), inject it into W3C Baggage,
then drive four independent observations. See
[references/PROBING_PROTOCOL.md](references/PROBING_PROTOCOL.md) for
per-stack UI probe mechanics (TUI / GTK / web) and SurrealDB SDK calls.

```
probe_id = ULID()
inject probe_id into Baggage as noelle.probe.id

(1) value_db  = surrealdb.query(contract.computation)
(2) resp      = http_get(contract.api_field.path)
    trace_id  = parse_traceparent(resp.headers)
    value_api = jsonpointer.resolve(resp.body, contract.api_field.json_pointer)
(3) value_ui  = drive_ui(contract.ui_element)  # per stack
(4) sleep(contract.bounded_staleness_ms)        # default 15s, Tempo P99 ingest
(5) trace     = tempo-direct.query_tempo_trace_by_id(trace_id)
    report    = tempo-direct.assert_spans_in_trace(trace_id, expected_span_names)
(6) if report.missing not empty:
      logs = grafana.query_loki_logs('{trace_id="' + trace_id + '"}', t-30s, t+30s)
(7) baseline = grafana.query_prometheus(
      'rate(traces_service_graph_request_failed_total[1m])')
(8) emit evidence/<contract_id>/observations.json with all four layers + report
```

Two design points:

- `tempo-mcp` is custom because `mcp-grafana` routes Tempo access through Sift investigations — wrong abstraction for bounded-staleness probes. The custom binary's about 150 lines of Rust using `rmcp` 1.x. See `scripts/tempo-mcp/` for the source.
- For attribute-search fallback when a trace ID's unavailable, double the staleness window to 60-90s.

## Phase 4 — Diff and triage

Run the predicate cascade in order. **First match wins.** Subsequent
matches go into evidence but not the primary diagnosis. See
[references/TRIAGE_TAXONOMY.md](references/TRIAGE_TAXONOMY.md) for the
full predicate definitions, localisation heuristics, and flakiness
handling (3× retry policy with widened windows).

| Order | Predicate | Category | Diagnosis |
|---|---|---|---|
| 1 | `db_absent` | `SUSPECT_NO_DATA` | DB query returned 0 rows; environment issue, not a bug |
| 2 | `api_stub` | `BUG_API_STUB` | Response hash identical across N≥5 varied DB inputs |
| 3 | `api_default` | `BUG_SERIALIZER` or `BUG_BINDING` | API matches OpenAPI default while DB has non-default |
| 4 | `api_schema_mismatch` | `BUG_SCHEMA_DRIFT` | Response fails `jsonschema` validation against OpenAPI |
| 5 | `trace_orphan` | `BUG_NO_WORK` | API responded but `db.query.work` span absent — API lied |
| 6 | `trace_dropped` | `BUG_RESPONSE_PATH` | Backend spans exist but API field is default |
| 7 | `ui_unrendered` | `BUG_UI_BINDING` | UI element absent from rendered tree |
| 8 | `ui_default` | `BUG_TUI_BINDING` or `BUG_FORMATTING` | UI shows default/zero while API value is non-default |
| 9 | `ui_stale` | `BUG_RACE_CONDITION` or `BUG_CACHE` | UI shows older value than API across 3 retries with 3× staleness budget |
| 10 | `forbidden_attribute_present` | `BUG_KNOWN_STUB` | `noelle.handler.stub=true` (or similar) appears in trace |
| 11 | `llm_judge` (fallback) | `JUDGE_<category>` | None fired; LLM compares four-layer observations to Gherkin scenario |

Never gate CI on `llm_judge` alone — record `judge_confidence` and
treat as advisory. Each finding gets a localisation (file:line via
rust-analyzer, with confidence) and a minimal reproducer.

## Phase 5 — Reporting

Three artefacts per run:

- `findings.json` — schema-validated against `assets/findings.schema.json`. The downstream handoff currency.
- `report.html` — human-readable summary with embedded screenshots and trace links.
- `evidence/<contract_id>/` — `db.json`, `api.json`, `ui.{txt|png|html}`, `trace.json`, `logs.json`, `observations.json`, `reproducer.sh`.

The schema's append-only and run directories are immutable. Downstream
skills consume findings against `findings.schema.json` and never parse
the HTML. See [references/EVIDENCE_SCHEMA.md](references/EVIDENCE_SCHEMA.md)
for the complete finding-record shape and downstream consumer contracts.

Print one line on completion:
`RUN=artifacts/ui-behavior-validator/<run-id>` and exit 0 (success) or
1 (findings present at severity ≥ high).

## Idempotency

- **Run ID**: `<ISO-8601>-<git-sha>-<contract-set-hash>`
- **Caching**: same target + contract-set + git SHA returns the cached run unless `--force`
- **Reproducibility**: pinned tool versions in `compatibility:`, all probes seeded, viewport 1440×900, `TZ=UTC`, `LC_ALL=C`
- **Append-only**: never edit a prior run directory; cut a new one

## Downstream integration

Three consumer skills read `findings.json` against the schema:

- `/story-creator` — groups recurring `BUG_NO_WORK` and `BUG_UI_BINDING` by `contract_id`, emits Gherkin scenarios from the four-tuple plus trace manifest
- `/adr-create` — aggregates category distributions across the last N runs and proposes ADRs (e.g., recurring `BUG_API_STUB` justifies "no handler returns a literal")
- `/iterate` — reads the top-severity blocker, executes the reproducer, opens `localization.file:line`, applies a fix, re-invokes this skill with `--contract <id> --force`, confirms resolution before opening a PR

PII gating applies downstream: findings whose evidence contains attributes
flagged by the redaction pipeline as suspect block `/story-creator` from
including raw evidence in a Gherkin scenario. The scenario gets a
sanitised abstraction; raw evidence stays in the run directory behind ACL.

## Common pitfalls (refuse to skip these)

- Don't skip Phase 0 — backend probes lie when the foundation lies
- Don't sample once — stub responses fingerprint identical, so vary inputs N≥5 times before declaring `api_stub`
- Don't trust `networkidle` for streaming endpoints — gate on trace-ID arrival instead
- Don't fail on a single flaky step — retry 3× per the flakiness section in `TRIAGE_TAXONOMY.md`
- Don't query MCP servers against unredacted backends — refuse, emit `INFRASTRUCTURE_GAP/pii_pipeline_missing`, halt
- Don't parse the HTML report from a downstream skill — read `findings.json` against the schema
- Correlate by trace ID, never by timestamp; capture buffer-cell colour separately from text for Ratatui

## Forbidden actions

- **Running Phase 1+ when Phase 0 failed.** Hard refusal. The skill emits one `INFRASTRUCTURE_GAP` finding and exits.
- **Querying any MCP backend before the PII audit passes.** The skill won't help exfiltrate unredacted attributes through trace queries.
- **Gating CI on `llm_judge` output alone.** Record the confidence, treat as advisory; deterministic predicates gate, judges advise.
- **Editing a prior run directory.** Cut a new run; the artefact root's append-only.
- **Claiming "the UI works" without trace correlation.** Without the trace manifest, you've validated three layers, not four.
- **Inferring contracts then treating them as gates.** `inferred: true` contracts are suggestions until a human reviews and flips the flag.

## Forbidden phrases (refuse unless followed by cited evidence)

- "Everything looks fine" — say "Predicates 1-10 didn't fire; `llm_judge` confidence: 0.NN against scenario `<id>`."
- "The UI matches the API" — say "UI cell `<region>` text `<value>`; API `<path>` value `<value>`; trace contains `<span_names>` — all four observations agree."
- "No issues found" — say "<n> contracts probed, 0 findings at severity ≥ high; <m> low/info findings recorded."
- "The trace looks healthy" — say "trace `<id>` contains spans `<list>`; manifest required `<list>`; missing: `<list>`."

## Writing Style

Apply `natural-writing-style` to all findings prose, HTML report copy,
and Gherkin handoffs.

Findings output must:

- Quote exact values, span names, and trace IDs — never paraphrase observations
- Cite the predicate that fired (and which predicates fired afterwards) by name
- Name the localisation file:line with the confidence score the tool returned
- Embed the minimal reproducer as a copy-pasteable shell line

## References

- Five-tuple contract schema and inference rules: [references/FIVE_TUPLE_MODEL.md](references/FIVE_TUPLE_MODEL.md)
- Trace manifest authoring (expected / required / forbidden attribute shapes): [references/TRACE_MANIFEST_GUIDE.md](references/TRACE_MANIFEST_GUIDE.md)
- Per-stack probe mechanics (Ratatui / GTK / web / SurrealDB): [references/PROBING_PROTOCOL.md](references/PROBING_PROTOCOL.md)
- MCP server setup (mcp-grafana + tempo-mcp wiring): [references/MCP_SERVER_SETUP.md](references/MCP_SERVER_SETUP.md)
- PII redaction playbook (the Collector config Phase 0 demands): [references/PII_REDACTION_PLAYBOOK.md](references/PII_REDACTION_PLAYBOOK.md)
- Triage taxonomy + flakiness retry policy: [references/TRIAGE_TAXONOMY.md](references/TRIAGE_TAXONOMY.md)
- Evidence schema and downstream consumer contracts: [references/EVIDENCE_SCHEMA.md](references/EVIDENCE_SCHEMA.md)

## Companion skills

- `/story-creator` — consumes `BUG_NO_WORK` and `BUG_UI_BINDING` findings to draft Gherkin scenarios
- `/adr-create` — consumes category distributions to propose architectural decisions
- `/iterate` — consumes top-severity blockers, applies fixes, re-invokes for confirmation
- `/threat-model-review` — invoked when Phase 0's PII redaction check fails (the redaction gap's a security concern, not a wiring concern)
