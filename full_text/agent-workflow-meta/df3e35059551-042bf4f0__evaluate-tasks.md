---
name: evaluate-tasks
description: Deep evaluation of TAU2 task data quality — runs per-task subagents for thorough NL assertion verification, gold action correctness, DB state validity, and policy alignment
argument-hint: [domain] [task_ids or "all"]
---

# Evaluate TAU2 Task Data Quality

Deep-check task definitions against the actual database and domain policy for correctness and consistency. Uses **one subagent per task** for thorough, fresh-context analysis, plus a **cross-task analysis agent** for pattern detection.

**Input:** $ARGUMENTS

Parse for: domain name and optionally specific task IDs (space-separated) or "all".

## Architecture

```
Orchestrator (you)
  ├── Phase 0: Setup — determine paths, task count, discover simulation data
  ├── Phase 1: Quick batch validation — run automated script, catch BROKEN tasks
  ├── Phase 2: Launch subagents — one per task, up to 5 in parallel
  │     ├── task-0 subagent: execute tools, read policy, verify NL, structured verdict
  │     ├── task-1 subagent: ...
  │     └── task-N subagent: ...
  ├── Phase 2.5: Cross-task analysis agent — single agent, receives all verdicts + sim scores
  ├── Phase 3: Merge per-task + cross-task findings, assemble summary
  └── Phase 4: Save report to progress/data_quality/evaluate_{domain}.md
```

## Available Domains

| Domain | Language | Notes |
|--------|----------|-------|
| fns_company | EN + RU | get_tasks() + get_tasks_ru() |
| fns_risk | EN + RU | get_tasks() + get_tasks_ru() |
| hr_kadry | RU only | get_tasks_ru() only |
| it_support | RU only | get_tasks_ru() only |
| legal_contracts | RU only | get_tasks_ru() only |
| telecom_support | RU only | get_tasks_ru() only |
| incident_management | RU only | get_tasks_ru() only |
| medical_reception | RU only | get_tasks_ru() only |
| budget_planning | RU only | get_tasks_ru() only |
| warehouse_logistics | RU only | get_tasks_ru() only |

Russian-only domains raise ValueError on get_tasks() — skip EN/RU parity check for them.

## Free-Text Arguments Reference

These arguments must NEVER be in `compare_args` (they are free-text and differ between agent and gold):

| Domain | Tool | Free-Text Args |
|--------|------|---------------|
| ALL | `transfer_to_human_agents` | `summary` (compare_args MUST be `[]`) |
| hr_kadry | `submit_leave_request` | `reason` |
| it_support | `create_ticket` | `subject`, `description` |
| it_support | `assign_equipment` | `reason` |
| legal_contracts | `request_approval` | `initiator`, `justification` |
| legal_contracts | `register_contract_action` | `reason` |
| telecom_support | `change_tariff` | `reason` |
| fns_company | `flag_company_risk` | `reason` |
| fns_risk | `create_audit_request` | `justification` |
| incident_management | `create_incident` | `title`, `description` |
| incident_management | `update_incident` | `resolution_notes` |
| incident_management | `create_change_request` | `description`, `rollback_plan` |
| medical_reception | `cancel_appointment` | `reason` |
| budget_planning | `create_expense_request` | `description` |
| budget_planning | `approve_expense` | `justification` |
| warehouse_logistics | `create_order` | `customer_name` |

## Phase 0: Setup + Simulation Discovery

1. Determine the domain import path: `tau2.domains.{domain}.environment`
2. Determine task file: `data/tau2/domains/{domain}/ru-tasks_30.json`
3. Determine policy file: `data/tau2/domains/{domain}/ru-policy.md`
4. For bilingual domains (fns_company, fns_risk), also note EN files: `tasks_30.json`, `policy.md`
5. Get the list of task IDs (run quick Python to enumerate)
6. **Discover simulation data** — run this Python script to find available model runs and compute per-task averages.

**Which sims to use:** There are many legacy/duplicate runs in `data/simulations/`. Only use the
**latest run per canonical model slug** from this curated set (strongest signal, comparable configs):

| Slug prefix | Model | Role | Why include |
|-------------|-------|------|-------------|
| `q35-27b-nothink-10t` | Qwen3.5-27B no-think | Strong baseline | Best open-source baseline, ceiling reference |
| `q35-nothink-10t` | Qwen3.5-9B no-think | Target model | Primary model we're improving |
| `dpo-v4-8k-ds` | Q3.5-9B DPO v4 | Trained variant | Shows training effect |
| `gpt-oss-120b_all` | GPT-OSS-120B | Oracle | Strongest model, near-ceiling |
| `sft-v2-r32-all` | Q3.5-9B SFT v2 | Trained variant | SFT baseline |

Ignore old slugs like `q3vl8b*`, `OLM*`, `q3vl32b*`, `q3vl4b*` — these are legacy Qwen3-VL runs
with different configs (thinking enabled, different sampling) and are not comparable.

When multiple dirs match the same slug prefix (e.g. `q35-nothink-10t_ru_2026-03-06` and an older one),
take only the **latest by date** (last in sorted order). The script below handles this automatically.

```python
import json, sys, os, re
from collections import defaultdict
sys.path.insert(0, "src")

DOMAIN = "{domain}"
SIMS_DIR = "data/simulations"

# Canonical slug prefixes — only these are loaded
CANONICAL_SLUGS = {
    "q35-27b-nothink-10t",
    "q35-nothink-10t",
    "dpo-v4-8k-ds",
    "gpt-oss-120b_all",
    "sft-v2-r32-all",
}

def get_nl_fraction(ri):
    nl_checks = ri.get("nl_assertions") or []
    if not nl_checks:
        rb = ri.get("reward_breakdown") or {}
        return rb.get("NL_ASSERTION", 1.0)
    return sum(1 for c in nl_checks if c.get("met", False)) / len(nl_checks)

def compute_primary(ri):
    rb = ri.get("reward_breakdown") or {}
    if not rb: return 0.0
    r = 1.0
    if "DB" in rb: r *= 1.0 if rb["DB"] == 1.0 else 0.0
    if "ACTION" in rb: r *= rb["ACTION"]
    r *= get_nl_fraction(ri)
    return r

# Find latest dir per canonical slug
slug_to_latest = {}  # slug -> (dir_name, filepath)
for d in sorted(os.listdir(SIMS_DIR)):
    fp = os.path.join(SIMS_DIR, d, f"{DOMAIN}.json")
    if not os.path.exists(fp):
        continue
    parts = d.split("_ru_")
    if len(parts) < 2:
        continue
    slug = parts[0]
    if slug not in CANONICAL_SLUGS:
        continue
    # sorted() ensures later dates overwrite earlier ones
    slug_to_latest[slug] = (d, fp)

# Scan only latest dirs
task_scores = defaultdict(lambda: defaultdict(list))
task_components = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
slugs_found = set()

for slug, (dirname, fp) in slug_to_latest.items():
    slugs_found.add(slug)
    try:
        with open(fp) as f:
            data = json.load(f)
        for sim in data.get("simulations", []):
            tid = sim.get("task_id")
            ri = sim.get("reward_info") or {}
            rb = ri.get("reward_breakdown") or {}
            if not rb:
                continue
            primary = compute_primary(ri)
            task_scores[tid][slug].append(primary)
            task_components[tid][slug]["action"].append(rb.get("ACTION", 0))
            task_components[tid][slug]["nl_frac"].append(get_nl_fraction(ri))
            task_components[tid][slug]["db"].append(rb.get("DB", 1.0))
    except Exception as e:
        print(f"Error loading {fp}: {e}")

if not slugs_found:
    print("SIM_SUMMARY: NO SIMULATION DATA")
else:
    print(f"SIM_SUMMARY: {len(slugs_found)} models found: {sorted(slugs_found)}")
    print(f"Dirs used: {json.dumps({s: d for s, (d, _) in slug_to_latest.items()}, indent=2)}")
    # Per-task summary as compact JSON
    summary = {}
    for tid in sorted(task_scores.keys()):
        tid_data = {}
        for slug in sorted(slugs_found):
            vals = task_scores[tid].get(slug, [])
            if vals:
                comps = task_components[tid][slug]
                tid_data[slug] = {
                    "primary_avg": round(sum(vals) / len(vals), 3),
                    "pass_rate": round(sum(1 for v in vals if v == 1.0) / len(vals), 3),
                    "action_avg": round(sum(comps["action"]) / len(comps["action"]), 3),
                    "nl_avg": round(sum(comps["nl_frac"]) / len(comps["nl_frac"]), 3),
                    "n": len(vals),
                }
        summary[str(tid)] = tid_data
    print("SIM_JSON_START")
    print(json.dumps(summary, ensure_ascii=False))
    print("SIM_JSON_END")
```

Save the output between `SIM_JSON_START` and `SIM_JSON_END` as `sim_summary_json` for Phase 2.5. If "NO SIMULATION DATA" is printed, set `sim_summary_json = "NO SIMULATION DATA"`.

## Phase 1: Quick Batch Validation

Run this Python script for ALL tasks at once. This catches BROKEN tasks (gold actions fail) quickly. Adapt `DOMAIN` and `TASK_IDS`.

```python
import json, sys, re
sys.path.insert(0, "src")

DOMAIN = "{domain}"
TASK_IDS = [{task_ids}]  # list of ints, or computed from get_tasks_ru()

from tau2.domains.{domain}.environment import get_environment, get_tasks_ru

FREE_TEXT_ARGS = {
    "transfer_to_human_agents": {"summary"},
    "submit_leave_request": {"reason"},
    "create_ticket": {"subject", "description"},
    "assign_equipment": {"reason"},
    "request_approval": {"initiator", "justification"},
    "register_contract_action": {"reason"},
    "change_tariff": {"reason"},
    "flag_company_risk": {"reason"},
    "create_audit_request": {"justification"},
    "create_incident": {"description"},
    "update_incident": {"resolution_notes"},
    "create_change_request": {"description", "rollback_plan"},
    "cancel_appointment": {"reason"},
    "create_expense_request": {"description"},
    "approve_expense": {"justification"},
    "create_order": {"customer_name"},
}

tasks = get_tasks_ru()
task_map = {t.id: t for t in tasks}

broken = []
ok = []

for tid in TASK_IDS:
    task = task_map[tid]
    actions = task.evaluation_criteria.actions
    env = get_environment(language='ru')
    tools_dict = {t.name: t for t in env.get_tools()}
    failed = False
    for i, action in enumerate(actions):
        try:
            tools_dict[action.name](**action.arguments)
        except Exception as e:
            print(f"Task {tid}: Action {i} {action.name}({action.arguments}) FAILED: {e}")
            failed = True
    if failed:
        broken.append(tid)
        print(f"Task {tid}: **BROKEN**")
    else:
        ok.append(tid)
        print(f"Task {tid}: actions OK ({len(actions)} actions)")

print(f"\nBROKEN: {broken}")
print(f"OK (need deep review): {ok}")
```

Record `broken` task IDs — these are BROKEN verdict, no subagent needed.
Record `ok` task IDs — these go to Phase 2.

## Phase 2: Deep Per-Task Audit (Subagents)

For each task in the `ok` list, launch a subagent using the **Agent tool** with `subagent_type: "general-purpose"`.

**Launch up to 5 subagents in parallel.** If more than 5 tasks, wait for the first batch to complete, then launch the next batch.

### Subagent Prompt Template

Use this exact template, filling in `{domain}`, `{task_id}`, `{policy_path}`, `{task_file_path}`, and `{domain_specific_checks}`:

```
You are auditing Task {task_id} in the {domain} TAU2 benchmark domain.
Your job: execute the gold actions, verify every NL assertion against actual tool results, check data logic against policy, and return a structured verdict.

Do NOT write any files. Just analyze and return your verdict as text output.

## Step 1: Execute Gold Actions and Capture Results

Run this Python script with Bash:

```python
import json, sys, re
sys.path.insert(0, "src")

from tau2.domains.{domain}.environment import get_environment, get_tasks_ru

FREE_TEXT_ARGS = {
    "transfer_to_human_agents": {"summary"},
    "submit_leave_request": {"reason"},
    "create_ticket": {"subject", "description"},
    "assign_equipment": {"reason"},
    "request_approval": {"initiator", "justification"},
    "register_contract_action": {"reason"},
    "change_tariff": {"reason"},
    "flag_company_risk": {"reason"},
    "create_audit_request": {"justification"},
    "create_incident": {"description"},
    "update_incident": {"resolution_notes"},
    "create_change_request": {"description", "rollback_plan"},
    "cancel_appointment": {"reason"},
    "create_expense_request": {"description"},
    "approve_expense": {"justification"},
    "create_order": {"customer_name"},
}

tasks = get_tasks_ru()
task = [t for t in tasks if t.id == {task_id}][0]
actions = task.evaluation_criteria.actions
reward_basis = task.evaluation_criteria.reward_basis
nl_assertions = task.evaluation_criteria.nl_assertions or []
user_nl = task.evaluation_criteria.user_nl_assertions or []

print("=== TASK INFO ===")
print(f"Task {task_id}: {str(task.description)[:100]}")
print(f"Actions: {len(actions)} ({', '.join(a.name for a in actions)})")
print(f"Reward basis: {reward_basis}")
print(f"NL assertions ({len(nl_assertions)}):")
for i, nl in enumerate(nl_assertions):
    print(f"  [{i}] {nl}")
print(f"User NL assertions ({len(user_nl)}):")
for i, nl in enumerate(user_nl):
    print(f"  [{i}] {nl}")

# User scenario
instr = task.user_scenario.instructions
print(f"\n=== USER SCENARIO ===")
if hasattr(instr, 'reason_for_call'):
    print(f"Reason: {instr.reason_for_call}")
if hasattr(instr, 'known_info'):
    print(f"Known info: {json.dumps(instr.known_info, ensure_ascii=False, default=str)}")
if hasattr(instr, 'task_instructions'):
    print(f"Instructions: {instr.task_instructions}")
if hasattr(instr, 'first_message') and instr.first_message:
    print(f"First message: {instr.first_message}")
if hasattr(instr, 'knowledge_boundary') and instr.knowledge_boundary:
    print(f"Knowledge boundary: {instr.knowledge_boundary}")
if hasattr(instr, 'dialogue_scheme') and instr.dialogue_scheme:
    print(f"Dialogue scheme ({len(instr.dialogue_scheme)} turns):")
    for s in instr.dialogue_scheme:
        print(f"  Turn {s.get('turn', '?')}: user={s.get('user', '')[:80]}")
        print(f"    expected_agent: {s.get('expected_agent', '')[:80]}")

# Execute gold actions on fresh DB
print(f"\n=== GOLD ACTION RESULTS ===")
env = get_environment(language='ru')
tools_dict = {t.name: t for t in env.get_tools()}
results = []
for i, action in enumerate(actions):
    try:
        result = tools_dict[action.name](**action.arguments)
        results.append(result)
        result_str = json.dumps(result, ensure_ascii=False, default=str)
        print(f"\nAction {i}: {action.name}({json.dumps(action.arguments, ensure_ascii=False)})")
        print(f"  compare_args: {action.compare_args}")
        print(f"  Result: {result_str[:500]}")
    except Exception as e:
        results.append(f"ERROR: {e}")
        print(f"\nAction {i}: {action.name}({action.arguments}) -> ERROR: {e}")

# DB hash check for write tasks
has_write = any(a.name in FREE_TEXT_ARGS or a.name.startswith(('create_', 'update_', 'submit_', 'approve_', 'cancel_', 'reserve_', 'flag_', 'book_', 'register_', 'change_')) for a in actions)
print(f"\n=== DB STATE ===")
print(f"Has write actions: {has_write}")
if has_write:
    env1 = get_environment(language='ru')
    t1 = {t.name: t for t in env1.get_tools()}
    h_before = env1.tools.db.get_hash()
    for a in actions:
        t1[a.name](**a.arguments)
    h_after = env1.tools.db.get_hash()
    print(f"Hash before: {h_before[:16]}...")
    print(f"Hash after:  {h_after[:16]}...")
    print(f"Changed: {h_before != h_after}")
    if h_before != h_after:
        # Test free-text exclusion
        env2 = get_environment(language='ru')
        t2 = {t.name: t for t in env2.get_tools()}
        for a in actions:
            args2 = dict(a.arguments)
            ft = FREE_TEXT_ARGS.get(a.name, set())
            for k in ft:
                if k in args2:
                    args2[k] = "FREETEXT_TEST_" + args2[k][::-1]
            t2[a.name](**args2)
        h_alt = env2.tools.db.get_hash()
        print(f"Free-text invariant: {h_after == h_alt}")
        if h_after != h_alt:
            print("WARNING: DB hash changes with different free-text! Check get_hash() override.")

# compare_args check
print(f"\n=== COMPARE_ARGS CHECK ===")
for i, action in enumerate(actions):
    ca = action.compare_args
    free = FREE_TEXT_ARGS.get(action.name, set())
    issues = []
    if ca is None and (free & set(action.arguments.keys())):
        issues.append(f"compare_args=null but has free-text args {free & set(action.arguments.keys())}")
    if isinstance(ca, list):
        for arg in ca:
            if arg not in action.arguments:
                issues.append(f"compare_args lists '{arg}' not in arguments")
        if free & set(ca):
            issues.append(f"compare_args includes free-text: {free & set(ca)}")
    if action.name == "transfer_to_human_agents" and ca != []:
        issues.append(f"transfer_to_human_agents compare_args must be [] but is {ca}")
    status = "WARN: " + "; ".join(issues) if issues else "OK"
    print(f"  Action {i} ({action.name}): {status}")

# Reward basis check
print(f"\n=== REWARD BASIS CHECK ===")
rb = reward_basis
if has_write and "DB" not in rb: print("WARN: write actions but DB not in reward_basis")
if actions and "ACTION" not in rb: print("WARN: has actions but ACTION not in reward_basis")
if nl_assertions and "NL_ASSERTION" not in rb: print("WARN: has nl_assertions but NL_ASSERTION not in reward_basis")
if "COMMUNICATE" in rb: print("WARN: COMMUNICATE in reward_basis (deprecated)")
if "DB" in rb and not has_write: print("INFO: DB in reward_basis but no write actions (harmless)")
if not any([has_write and "DB" not in rb, actions and "ACTION" not in rb, nl_assertions and "NL_ASSERTION" not in rb, "COMMUNICATE" in rb]):
    print("OK — reward_basis consistent")

# Complexity
print(f"\n=== COMPLEXITY ===")
scheme_turns = 0
if hasattr(instr, 'dialogue_scheme') and instr.dialogue_scheme:
    scheme_turns = len([s for s in instr.dialogue_scheme if s.get('user') != '###STOP###'])
print(f"Actions: {len(actions)}, Dialogue turns: {scheme_turns}")

# Extract entities for structured output
print(f"\n=== ENTITIES ===")
for i, action in enumerate(actions):
    for k, v in action.arguments.items():
        if isinstance(v, str) and (k.endswith('_id') or k in ('inn', 'inn1', 'inn2', 'employee_id', 'subscriber_id', 'contract_id', 'ticket_id')):
            print(f"  Action {i} ({action.name}): {k}={v}")
```

## Step 2: Read the Domain Policy

Read the policy file at: {policy_path}
Focus on rules relevant to this task's actions (look at the tool names from Step 1).

## Step 3: Verify Each NL Assertion

For EACH NL assertion from Step 1 output, verify:

1. **Data accuracy**: Does the assertion reference specific numbers, IDs, dates, or statuses? Cross-check against the actual tool results from Step 1. If the assertion says "balance is 5000" but the tool returned 3000, that's a FAIL.

2. **Derivability**: Can the agent derive this information from the tool results? If the assertion references data that no tool returns, it's unverifiable — mark WARN.

3. **User scenario alignment**: Does the user scenario actually ask for this info? If the assertion expects the agent to volunteer information the user didn't request, mark WARN (agent may not say it unprompted).

4. **Policy consistency**: Does the assertion align with the domain policy? If the policy says "refuse if X" and the assertion says "agent approved", check if condition X is met.

5. **Contradiction check**: Does any assertion contradict another assertion or the gold actions? E.g., "agent refused the request" but gold actions include a write tool.

6. **NL-duplicates-ACTION check**: Flag NL assertions that merely restate tool calls. If the assertion can be verified by checking tool call logs alone (e.g., "Агент вызвал get_company_info с ИНН 5001234567" or "Агент создал заявку на аудит"), it belongs in ACTION evaluation, not NL. Good NL assertions test what the agent **said to the user** (explanation quality, warnings, reasoning) and **how it reasoned**, not what tools it called.

For each assertion, classify:
- `verified=yes` — assertion is accurate and testable via agent communication
- `verified=partial` — some concerns but broadly correct
- `verified=no` — factual error, unverifiable, or duplicates ACTION check
- Provide a 1-word `topic` (e.g., "balance", "risk_level", "refusal", "warning")
- Note any `concerns` as brief text

## Step 4: Check User Scenario Consistency

Verify:
- `known_info` references valid entities in the DB (check against tool results)
- `task_instructions` flow matches the gold action sequence
- `first_message` (if present) matches the intent and entity IDs
- `dialogue_scheme` (if present): each turn logically leads to the next gold action
- `knowledge_boundary` (if present): doesn't leak info the user shouldn't know

## Step 5: Domain-Specific Data Logic

{domain_specific_checks}

## Step 6: Output Your Verdict

Return EXACTLY this format:

```
TASK_ID: {task_id}
ACTIONS: {count} ({tool_names})
ENTITIES_USED:
- {entity_id} | role={primary|secondary|write_target} | expected_outcome={description}
NL_SUMMARY:
- [0] topic={word} | verified={yes|no|partial} | concerns={text or "none"}
- [1] topic={word} | verified={yes|no|partial} | concerns={text or "none"}
ACTION_CHAIN: tool1 -> tool2 -> tool3
CHECKS:
[CHECK 1] Gold actions: OK / FAIL
[CHECK 2] NL assertions: OK / WARN / FAIL — {details for each problematic assertion}
[CHECK 3] compare_args: OK / WARN / FAIL — {details}
[CHECK 4] Write preconditions: OK / FAIL / N/A — {details}
[CHECK 5] DB state: OK / FAIL / N/A — {details}
[CHECK 6] Reward basis: OK / WARN — {details}
[CHECK 7] User scenario: OK / WARN — {details}
[CHECK 8] NL-duplicates-ACTION: OK / WARN — {count} of {total} NL assertions merely restate tool calls
[CHECK 9] Data logic: OK / WARN / FAIL — {details}
VERDICT: PASS / REVIEW NEEDED / BROKEN
ISSUES: {one-line summary per issue, or "none"}
```

Rules for verdict:
- BROKEN: gold actions fail (CHECK 1), or DB state wrong (CHECK 5 FAIL), or critical data logic error (CHECK 9 FAIL)
- REVIEW NEEDED: any WARN or non-critical FAIL in checks 2-9
- PASS: all checks OK or N/A
```

### Domain-Specific Checks Reference

Include the relevant block in `{domain_specific_checks}` based on the domain:

**incident_management:**
- Verify incident exists and has expected status/priority before updates
- Check that priority escalation follows severity rules in policy
- Verify SLA timers: P1=1h, P2=4h, P3=8h, P4=24h (if assertions reference SLA)
- For change requests: verify the linked incident exists
- For reassignment: verify the target team/specialist exists in DB

**medical_reception:**
- Verify doctor exists and has the right specialization for the appointment type
- Check schedule conflicts: no double-booking same doctor at same time
- Verify patient exists in DB before any actions
- For cancellations: verify appointment exists and is in cancellable state
- For rescheduling: verify new slot is available

**budget_planning:**
- Verify budget exists and has sufficient remaining amount for expense
- Check approval chain: amounts > threshold require senior approval (per policy)
- Verify department budget limits (monthly/quarterly)
- For transfers: verify both source and destination budgets exist
- Cross-check amounts: expense amount + already spent <= budget limit

**warehouse_logistics:**
- Verify product exists and has sufficient stock for order
- Check warehouse capacity limits (if assertions reference capacity)
- For transfers: verify both source and destination warehouses exist
- Verify order status transitions are valid (created→confirmed→shipped→delivered)
- Check minimum stock alerts: current_stock < min_threshold triggers alert

**hr_kadry:**
- Annual leave: verify `annual_days_remaining >= requested_days` (via `get_leave_balance`)
- Department load: verify % on leave < 30% (via `get_department_info`)
- Probation: verify employee status and `probation_end` vs 2024-12-15
- 14-day rule: check for existing 14+ day leave in the year
- Sick pay: experience_years → 60% (<5y), 80% (5-8y), 100% (8+y)
- Dismissed employees: cannot submit ANY leave
- Overlapping leave: check `leave_history` for active entries overlapping dates

**it_support:**
- Employee status: verify `status != "dismissed"`
- Duplicate ticket: check for existing open ticket with same category
- Equipment limits: regular (1 laptop, 2 monitors), VIP (1 laptop, 3 monitors)
- Software licenses: `used_licenses < total_licenses` and `expiry_date >= "2024-12-15"`
- Equipment availability: verify equipment type available with status "available"
- VIP priority boost: P4→P3, P3→P2, P2→P1, P1→P1

**legal_contracts:**
- Contract status matches expected for the operation
- Counterparty status (active/blocked/under_review)
- Signatory: authority_end >= 2024-12-15, max_amount >= contract.amount, allowed_types includes contract type
- Confidentiality: confidential → hide amounts; strictly_confidential → transfer to senior counsel
- Payment status: overdue payments match premise

**telecom_support:**
- Subscriber status matches premise (active/blocked/suspended)
- Tariff cooldown: days since last_tariff_change >= 30 (current date 2024-12-15)
- Tariff availability: exists and available == true
- Balance/debt: account balance matches expected
- Package counters: exhaustion matches premise

**fns_risk:**
- compare_companies must precede create_audit_request
- audit_type: risk_score >= 70 → "field"; 50-69 → "desk"; < 50 → NO audit
- audit inn = old company (inn1) from compare_companies

**fns_company:**
- flag_company_risk: verify risk_level per policy decision table
- "high": liquidation/bankruptcy + related, OR bankruptcy + FNS creditor, OR 3+ factors
- "medium-high": mass director (4+) + revenue decline > 50%
- "medium": defendant in large lawsuits only
- "low": minor isolated factors

### EN/RU Parity (Check 8)

**Only for bilingual domains** (fns_company, fns_risk). The orchestrator handles this directly (not subagents) by comparing task files:

```python
import json, sys
sys.path.insert(0, "src")
from tau2.domains.{domain}.environment import get_tasks, get_tasks_ru

en_tasks = {t.id: t for t in get_tasks()}
ru_tasks = {t.id: t for t in get_tasks_ru()}

for tid in sorted(set(en_tasks) | set(ru_tasks)):
    issues = []
    if tid not in en_tasks: issues.append("missing EN")
    if tid not in ru_tasks: issues.append("missing RU")
    if tid in en_tasks and tid in ru_tasks:
        en, ru = en_tasks[tid], ru_tasks[tid]
        en_a = [(a.name, a.arguments, a.compare_args) for a in en.evaluation_criteria.actions]
        ru_a = [(a.name, a.arguments, a.compare_args) for a in ru.evaluation_criteria.actions]
        if en_a != ru_a: issues.append("actions differ")
        if en.evaluation_criteria.reward_basis != ru.evaluation_criteria.reward_basis: issues.append("reward_basis differs")
        en_nl = len(en.evaluation_criteria.nl_assertions or [])
        ru_nl = len(ru.evaluation_criteria.nl_assertions or [])
        if en_nl != ru_nl: issues.append(f"nl_assertions count: EN={en_nl} RU={ru_nl}")
    if issues:
        print(f"Task {tid}: {', '.join(issues)}")
    else:
        print(f"Task {tid}: OK")
```

## Phase 2.5: Cross-Task Analysis

After ALL Phase 2 subagents complete, launch a **single** cross-task analysis agent. This agent receives all per-task verdict blocks and the simulation summary, and performs pattern analysis that per-task agents cannot do individually.

### Cross-Task Agent Prompt

```
You are performing cross-task analysis for the {domain} TAU2 benchmark domain.
You receive structured verdicts from per-task audits and optional simulation scores.
Your job: find cross-task patterns, contradictions, and quality issues that individual task audits cannot detect.

Do NOT write any files. Return your analysis as text output.

## Input Data

### Per-Task Verdicts (from Phase 2)

{all_verdict_blocks_concatenated}

### Simulation Scores

{sim_summary_json}

## Analysis 1: Entity Consistency

Check across all ENTITIES_USED blocks:
1. **Contradicting outcomes**: Same entity appears in multiple tasks with contradicting expected_outcome (e.g., entity X is "approved" in task 5 but "rejected" in task 12 under similar conditions)
2. **Overused entities**: Any entity appearing in >25% of tasks — flag as over-concentrated
3. **Never-referenced DB entities**: Run this to find DB entities not appearing in any task:

```python
import json, sys
sys.path.insert(0, "src")
from tau2.domains.{domain}.environment import get_environment, get_tasks_ru

env = get_environment(language='ru')
db = env.tools.db.model_dump()
tasks = get_tasks_ru()

# Collect all entity IDs used in tasks
used_entities = set()
for t in tasks:
    for a in t.evaluation_criteria.actions:
        for k, v in a.arguments.items():
            if isinstance(v, str):
                used_entities.add(v)

# Check each DB collection
print("=== UNUSED DB ENTITIES ===")
for collection_name, collection in db.items():
    if isinstance(collection, dict):
        for key in collection:
            if key not in used_entities:
                print(f"  {collection_name}.{key}: never referenced in any task")
    elif isinstance(collection, list) and collection:
        for i, item in enumerate(collection):
            if isinstance(item, dict):
                for k, v in item.items():
                    if k.endswith('_id') or k == 'inn':
                        if str(v) not in used_entities:
                            print(f"  {collection_name}[{i}].{k}={v}: never referenced")
```

## Analysis 2: NL Assertion Cross-Check

Check across all NL_SUMMARY blocks:
1. **Contradicting assertions**: Two tasks assert opposite things about the same entity or policy rule
2. **Duplicate assertion text**: Nearly identical NL assertion wording across tasks (copy-paste smell)
3. **NL-duplicates-ACTION prevalence**: Count how many tasks have CHECK 8 WARN — if >30% of tasks have NL assertions that duplicate ACTION checks, flag as systematic issue

## Analysis 3: Simulation Scoring (skip if "NO SIMULATION DATA")

Using the sim_summary_json, identify:
1. **Trivial tasks**: primary_avg == 1.0 across ALL models — too easy, no discriminative value
2. **Broken tasks**: primary_avg == 0.0 across ALL models — likely task bug or impossible task
3. **NL=1 + ACTION<1 suspects**: nl_avg == 1.0 but action_avg < 1.0 for any model — possible NL assertion hallucination (judge says "pass" when agent didn't complete the task)
4. **High-variance tasks**: Same model, pass_rate between 0.2-0.8 — unstable tasks, may depend on random LLM behavior
5. **Model-discriminating tasks**: Large spread between best and worst model — high benchmark value

## Analysis 4: Action Pattern Clustering

Using all ACTION_CHAIN lines:
1. **Duplicate chains**: 3+ tasks with identical tool sequence — over-tested pattern
2. **Over-tested patterns**: >25% of tasks use the same 2-tool prefix
3. **Singletons**: Tasks with unique tool combinations — ensure these aren't accidental outliers
4. **Missing patterns**: Common tool combinations from the domain that no task exercises

## Output Format

Return EXACTLY this format:

```
CROSS-TASK ANALYSIS: {domain}

=== ENTITY CONSISTENCY ===
Contradictions: {count}
{list each: "entity X: task A expects {outcome1}, task B expects {outcome2}"}
Overused (>25%): {entity}: {count}/{total} tasks
Never-referenced DB entities: {count}
{list each}

=== NL CROSS-CHECK ===
Contradicting assertions: {count}
{list each pair}
Duplicate assertion text: {count} pairs
{list each pair with task IDs}
NL-duplicates-ACTION: {count}/{total} tasks flagged (CHECK 8 WARN)
{if >30%: "SYSTEMATIC ISSUE: majority of NL assertions duplicate ACTION checks"}

=== SIMULATION SCORING ===
{or "NO SIMULATION DATA — skipped"}
Trivial (all-pass): {task_ids}
Broken (all-fail): {task_ids}
NL=1+ACTION<1 suspects: {task_ids with details}
High-variance: {task_ids with model and pass_rate}
Best discriminators: {task_ids with spread}

=== ACTION PATTERNS ===
Duplicate chains: {groups}
Over-tested prefixes: {prefix}: {count} tasks
Singletons: {task_ids}
Missing patterns: {suggested tool combinations}

=== RECOMMENDATIONS ===
1. {actionable recommendation}
2. {actionable recommendation}
...
```
```

Launch this as a single subagent with `model: "sonnet"`.

## Phase 3: Collect and Merge Verdicts

After Phase 2 and Phase 2.5 complete:
1. Parse each per-task subagent's verdict (look for the `TASK_ID:` block)
2. Parse the cross-task analysis (look for the `CROSS-TASK ANALYSIS:` block)
3. Categorize per-task: BROKEN / REVIEW NEEDED / PASS
4. Build summary table
5. Merge cross-task findings into the report

## Phase 4: Save Report

Save to `progress/data_quality/evaluate_{domain}.md`:

```markdown
# {Domain} Domain: Task Evaluation Report

**Date:** YYYY-MM-DD
**Tasks:** {total_count}
**Simulation data:** {model_count} models or "none available"

## Summary

| Severity | Count | Tasks |
|----------|-------|-------|
| BROKEN | N | task IDs |
| REVIEW NEEDED | N | task IDs |
| PASS | N | task IDs |

## Per-Task Issues

### Task {id} — {one-line summary}
- {detailed description from subagent verdict}
- **Fix**: {suggested fix}

## Cross-Task Analysis

### Entity Consistency
{from Phase 2.5 — contradictions, overused entities, never-referenced}

### NL Assertion Cross-Check
{from Phase 2.5 — contradictions, duplicates, NL-duplicates-ACTION prevalence}

### Simulation Scoring
{from Phase 2.5 — trivial, broken, NL hallucination suspects, high-variance, discriminators}
{or "No simulation data available for this domain."}

### Action Pattern Clusters
{from Phase 2.5 — duplicate chains, over-tested, singletons, missing patterns}

### Cross-Task Recommendations
{numbered list from Phase 2.5}

## Notes
{any cross-cutting observations from the orchestrator}
```

## Important

- Always reload a FRESH DB for each task (write tools are irreversible)
- Execute tools in the order specified in `actions` list
- The subagent prompt must be SELF-CONTAINED — include all domain-specific checks inline
- Each subagent should do its own tool execution (not rely on orchestrator's Phase 1)
- Phase 1 is only for quick BROKEN detection — Phase 2 subagents do the real work
- Phase 2.5 MUST wait for all Phase 2 subagents to complete (it needs their verdicts as input)
- Launch subagents with `model: "sonnet"` for cost efficiency (they don't need opus for mechanical checking)
- For EN/RU parity (Check 8), the orchestrator runs the comparison directly
- The structured verdict format (TASK_ID, ENTITIES_USED, NL_SUMMARY, ACTION_CHAIN) is critical for Phase 2.5 — ensure subagent prompts include the exact format
