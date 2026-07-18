---
name: create-domain
description: Create or modify a TAU2 benchmark domain — generates data model, tools, DB, policy, tasks with configurable complexity and count
argument-hint: [domain_name — description] [--tasks N] [--complexity hard|mixed|easy] [--tasks-only] [--rewrite-tasks] [--api agent=url,model=name user=url,model=name]
---

# Create / Configure TAU2 Domain

Generate a complete TAU2 domain from a description, or modify an existing domain's tasks. Supports configurable task count and complexity.

**Input:** $ARGUMENTS

Parse the input for:
- **domain name** (snake_case) — required
- **description** — domain concept, entities, tools, scenarios
- **--tasks N** — number of tasks to generate (default: 15)
- **--complexity hard|mixed|easy** — task complexity profile (default: hard)
- **--tasks-only** — only generate/rewrite tasks for an existing domain (skip code/DB/policy)
- **--rewrite-tasks** — synonym for --tasks-only, regenerate task file for existing domain
- **--api agent=url,model=name user=url,model=name** — optional: run live task validation after generation

If the input is vague, ask clarifying questions before proceeding.

## Complexity Profiles

### `hard` (default, recommended)
- **NO simple lookups** — every task has 3+ gold actions
- **NO 2-step tasks** — minimum 3 actions, target 4-6
- **Multi-turn**: at least 60% of tasks have 2-3 dialogue turns
- **Required patterns**: tool info reuse, user cross-overs, conditional chains, error recovery
- **Typical distribution** (for 15 tasks):
  - 5 full lifecycle chains (5-6 actions, multi-turn)
  - 4 conditional/branching tasks (4-5 actions, policy decision points)
  - 3 multi-turn with user cross-over (3-5 actions, user changes request mid-flow)
  - 2 error recovery (3-4 actions, first attempt fails, agent adapts)
  - 1 escalation/transfer (3+ actions, policy limit reached)

### `mixed` (balanced)
- Mix of simple and complex tasks
- **Distribution** (for 30 tasks):
  - 6-8 simple (1-2 actions, basic lookup)
  - 10-12 medium (2-3 actions, multi-step)
  - 6-8 hard (4+ actions, write tools, edge cases)
  - 4-6 edge cases (error handling, boundary conditions)

### `easy` (quick validation)
- Mostly simple tasks for testing infrastructure
- 1-2 action tasks, single-turn
- Useful for smoke tests, not benchmarking

## NL Assertion Guidelines

NL assertions should test what ACTION evaluation **cannot** — they must NOT duplicate tool-call verification.

**Good NL assertions** (test communication/reasoning):
- "Агент объяснил клиенту, ПОЧЕМУ заявка отклонена, ссылаясь на правила политики" — tests explanation quality
- "Агент предупредил о возможных последствиях смены тарифа" — tests proactive communication
- "Агент корректно интерпретировал результат сравнения компаний и сообщил уровень риска" — tests reasoning
- "Агент НЕ раскрыл внутренние данные о риск-скоринге клиенту" — tests policy compliance in text

**Bad NL assertions** (duplicate ACTION check):
- "Агент вызвал get_company_info с ИНН 5001234567" — this is exactly what ACTION evaluates
- "Агент создал заявку на аудит" — ACTION already checks create_audit_request was called
- "Агент использовал инструмент compare_companies" — pure tool-call check

**Rule of thumb:** If the assertion can be verified by checking tool call logs alone, it belongs in ACTION, not NL. NL should verify what the agent **said to the user** and **how it reasoned**, not what tools it called.

## Task Design Principles (for `hard` complexity)

### 1. Action Chains
Every tool call result must inform the next step. Example:
```
get_employee_info → discover VIP status → priority boost decision
get_system_info → find dependencies → cascade impact check
check_stock → below min_level → trigger restock flow
```

### 2. Tool Information Reuse
Output from tool A feeds into tool B's arguments or decisions:
- `get_patient_info` returns `insurance_plan_id` → used in `check_insurance_coverage`
- `get_contract_info` returns `amount` → determines `approval_level` in `request_approval`
- `check_stock` returns `available_quantity` → determines if partial fulfillment needed

### 3. User Cross-Overs (multi-turn)
User changes the situation mid-conversation:
- "Actually, use a different vendor" (after first vendor rejected)
- "Also book an appointment for next week" (adds second request)
- "The amount should be 300K, not 500K" (corrects earlier info)
- "What if we split this into two orders?" (changes approach)

### 4. Conditional Branching
Agent must choose path based on discovered data:
- Insurance covers specialty → book directly; not covered → suggest alternative
- Budget frozen → refuse new request; budget active but >80% spent → warn + escalate
- Supplier active → create restock; suspended → transfer to manager

### 5. Error Recovery
First attempt fails, agent must adapt:
- Invalid ID → user corrects → retry with valid ID
- Expired referral → user requests urgent type → skip referral requirement
- Dismissed employee → user provides colleague's ID

## Step 0: Plan

Before writing any code, present a brief plan:
1. **Domain name** (snake_case, e.g. `hr_kadry`)
2. **DB entities** — list of 4-8 entity types with ~8-15 records each
3. **Tools** — list of 5-8 tools (mix of READ and WRITE, at least 1 WRITE)
4. **Policy outline** — key decision rules with specific numeric thresholds/criteria
5. **Task plan** — how many tasks, which complexity patterns, expected action count distribution
6. **Language mode** — ask the user: **"Russian only" or "Both languages (RU + EN)"?**
   - **Russian only (default):** Create `ru-policy.md`, `ru-tasks_30.json` only. Do NOT create `tasks_30.json` — it would be a misleading copy. `get_tasks()` should read `ru-tasks_30.json`. Create `policy.md` as EN translation (lightweight, useful for code readers).
   - **Both languages:** Create `ru-policy.md` + `policy.md`, `ru-tasks_30.json` + `tasks_30.json` with real translations.

Wait for user approval before proceeding.

**If `--tasks-only` / `--rewrite-tasks`**: Skip Steps 1-7, 9. Read existing DB + policy + tools, then generate tasks (Step 8) and validate (Step 10, 10.5, 10.5b).

## Step 1: Data Model (`src/tau2/domains/{domain}/data_model.py`)

```python
from __future__ import annotations
from typing import Literal, Optional
from pydantic import BaseModel
from tau2.environment.db import DB
from tau2.utils.utils import get_dict_hash

# Define entity models (all inherit BaseModel)
class Entity1(BaseModel):
    field1: str
    field2: int

# Main DB class (inherit DB, not BaseModel)
class {Domain}DB(DB):
    collection1: dict[str, Entity1]   # keyed by identifier
    collection2: list[Entity2]        # or list
    write_targets: list[WriteEntity]  # starts empty in db.json

    # CRITICAL: Override if WRITE tools have free-text fields
    def get_hash(self) -> str:
        data = self.model_dump()
        for item in data.get("write_targets", []):
            item.pop("free_text_field", None)  # strip free-text
        return get_dict_hash(data)
```

**Rules:**
- Inherit from `DB` (not `BaseModel`) for the main DB class
- Use `dict[str, Model]` for keyed collections (ID → record)
- Use `list[Model]` for append-only collections (write targets, logs)
- Override `get_hash()` if ANY write tool accepts free-text (reason, comment, justification, etc.)
- Write target collections MUST start as empty `[]` in db.json

## Step 2: Tools (`src/tau2/domains/{domain}/tools.py`)

```python
from tau2.domains.{domain}.data_model import {Domain}DB
from tau2.environment.toolkit import ToolKitBase, ToolType, is_tool

class {Domain}Tools(ToolKitBase):
    db: {Domain}DB

    def __init__(self, db: {Domain}DB) -> None:
        super().__init__(db)  # MUST pass db

    @is_tool(ToolType.READ)
    def get_something(self, id: str) -> dict:
        """Docstring in RUSSIAN — this becomes the tool description for the LLM.

        Args:
            id: Описание параметра.

        Returns:
            dict с данными.
        """
        if id not in self.db.collection:
            raise ValueError(f"Не найдено: {id}")
        return self.db.collection[id].model_dump()

    @is_tool(ToolType.WRITE)
    def create_record(self, id: str, value: str, reason: str) -> dict:
        """Write tool — НЕОБРАТИМО.

        Args:
            id: Идентификатор.
            value: Значение.
            reason: Обоснование.
        """
        entry = WriteEntity(id=id, value=value, reason=reason)
        self.db.write_targets.append(entry)
        return {"status": "success", "id": id}
```

**Rules:**
- Class: `{Domain}Tools(ToolKitBase)`
- Constructor: `super().__init__(db)` — ALWAYS pass db
- Decorator: `@is_tool(ToolType.READ)` or `@is_tool(ToolType.WRITE)`
- Tool docstrings in **Russian** — they ARE the tool descriptions shown to the LLM
- Return `.model_dump()` for read tools, confirmation dict for write tools
- Raise `ValueError` with Russian message for not-found cases
- 5-8 tools total: mostly READ (3-5), 1-2 WRITE, optionally 1 GENERIC (calculate)

## Step 3: Utils (`src/tau2/domains/{domain}/utils.py`)

```python
from tau2.config import DEFAULT_LANGUAGE
from tau2.utils.utils import DATA_DIR

{DOMAIN_UPPER}_DATA_DIR = DATA_DIR / "tau2" / "domains" / "{domain}"
{DOMAIN_UPPER}_DB_PATH = {DOMAIN_UPPER}_DATA_DIR / "db.json"
{DOMAIN_UPPER}_POLICY_PATH = {DOMAIN_UPPER}_DATA_DIR / "policy.md"
{DOMAIN_UPPER}_POLICY_PATH_RU = {DOMAIN_UPPER}_DATA_DIR / "ru-policy.md"
{DOMAIN_UPPER}_TASK_SET_PATH = {DOMAIN_UPPER}_DATA_DIR / "tasks_30.json"
{DOMAIN_UPPER}_TASK_SET_PATH_RU = {DOMAIN_UPPER}_DATA_DIR / "ru-tasks_30.json"

def get_{domain}_policy_path(language: str = None):
    if language is None:
        language = DEFAULT_LANGUAGE
    return {DOMAIN_UPPER}_POLICY_PATH_RU if language == "ru" else {DOMAIN_UPPER}_POLICY_PATH

def get_{domain}_task_set_path(language: str = None):
    if language is None:
        language = DEFAULT_LANGUAGE
    return {DOMAIN_UPPER}_TASK_SET_PATH_RU if language == "ru" else {DOMAIN_UPPER}_TASK_SET_PATH
```

## Step 4: Environment (`src/tau2/domains/{domain}/environment.py`)

```python
import json
from typing import Optional
from tau2.config import DEFAULT_LANGUAGE
from tau2.data_model.tasks import Task
from tau2.domains.{domain}.data_model import {Domain}DB
from tau2.domains.{domain}.tools import {Domain}Tools
from tau2.domains.{domain}.utils import (
    {DOMAIN_UPPER}_DB_PATH, get_{domain}_policy_path,
)
from tau2.environment.environment import Environment

def get_environment(db=None, solo_mode=False, language=None) -> Environment:
    if solo_mode:
        raise ValueError("{domain} domain does not support solo mode")
    if language is None:
        language = DEFAULT_LANGUAGE
    if db is None:
        db = {Domain}DB.load({DOMAIN_UPPER}_DB_PATH)
    tools = {Domain}Tools(db)
    with open(get_{domain}_policy_path(language), "r") as fp:
        policy = fp.read()
    return Environment(domain_name="{domain}", policy=policy, tools=tools)

def get_tasks() -> list[Task]:
    from tau2.domains.{domain}.utils import {DOMAIN_UPPER}_TASK_SET_PATH
    with open({DOMAIN_UPPER}_TASK_SET_PATH, "r") as fp:
        return [Task.model_validate(t) for t in json.load(fp)]

def get_tasks_ru() -> list[Task]:
    from tau2.domains.{domain}.utils import {DOMAIN_UPPER}_TASK_SET_PATH_RU
    with open({DOMAIN_UPPER}_TASK_SET_PATH_RU, "r") as fp:
        return [Task.model_validate(t) for t in json.load(fp)]
```

## Step 5: `__init__.py`

Create empty `src/tau2/domains/{domain}/__init__.py`.

## Step 6: Database (`data/tau2/domains/{domain}/db.json`)

Create a realistic mock database with:
- **8-15 records per collection** — enough variety for diverse tasks
- **Realistic Russian names/data** — use believable company names, person names, dates
- **Cross-references** — entities should reference each other (e.g. person works at company)
- **Edge cases baked in** — some records with missing data, boundary values, duplicates
- **Write targets start empty**: `"write_targets": []`
- **Use `ensure_ascii=False`** for Cyrillic in JSON

## Step 7: Policy (`data/tau2/domains/{domain}/ru-policy.md`)

Write the agent policy **in Russian**. The policy should focus on **decision rules and criteria** — NOT tool API descriptions (the agent already gets tool schemas via function calling).

Structure:

```markdown
# Политика агента: {Domain Title Russian}

Текущая дата: 2024-12-15.

Вы — {role description Russian}.

## Идентичность и ограничения
- Data source constraints
- What agent can and cannot do

## Правила принятия решений
- Decision rule 1 with SPECIFIC thresholds/criteria (numbers, categories)
- Decision rule 2 with clear conditions
- When to use write tools (preconditions, verification steps)

## Правила взаимодействия
- Communication rules
- What to tell the user, what not to reveal
```

**Critical:** Include specific decision criteria with numeric thresholds — this is what makes tasks testable. The policy must be detailed enough that an LLM can follow it deterministically.

**Do NOT list tool API signatures in the policy** — the agent gets those from OpenAI function schemas. The policy should describe WHEN and WHY to use tools, decision logic, and constraints.

**Language handling:**
- **Russian only mode:** Create `ru-policy.md` (Russian) and `policy.md` (English translation — lightweight, for code readers). No duplication.
- **Both languages mode:** Create `ru-policy.md` (Russian) and `policy.md` (English translation).

## Step 8: Tasks (`data/tau2/domains/{domain}/ru-tasks_30.json`)

Generate tasks using **parallel subagents** for efficiency. Split task generation across 3 agents, each handling a subset of tasks with assigned complexity tiers and entity sets.

### Step 8a: Prepare Task Generation Context

Before launching subagents, prepare the shared context:
1. **Full DB dump** — read db.json to know all available entities and their IDs
2. **Policy text** — read the policy to know decision rules
3. **Tool list** — enumerate all tools with their parameter schemas
4. **Entity allocation** — divide DB entities into 3 non-overlapping sets (one per agent), ensuring each agent has enough entities for its tasks. Some entities may be shared (e.g., lookup-only entities).
5. **Task ID ranges** — assign ranges: Agent 1 gets IDs 0–N1, Agent 2 gets N1+1–N2, Agent 3 gets N2+1–N3

Run this to extract tool schemas:
```python
import json, sys
sys.path.insert(0, "src")
from tau2.domains.{domain}.environment import get_environment

env = get_environment(language='ru')
tools = env.get_tools()
for t in tools:
    schema = t.model_dump() if hasattr(t, 'model_dump') else {"name": t.name}
    print(json.dumps(schema, ensure_ascii=False, indent=2))
```

### Step 8b: Launch Parallel Task Generation Subagents

Launch **3 subagents in parallel** using the Agent tool. Each subagent generates a subset of tasks.

**Subagent prompt template** (fill in `{domain}`, `{db_dump}`, `{policy_text}`, `{tool_schemas}`, `{task_id_range}`, `{complexity_tier}`, `{assigned_entities}`, `{target_count}`, `{free_text_args}`, `{domain_specific_write_preconditions}`):

```
You are generating {target_count} benchmark tasks (IDs {task_id_range}) for the {domain} TAU2 domain.
Complexity tier: {complexity_tier}. Return ONLY a valid JSON array of task objects.

## Domain Context

### Database (db.json):
{db_dump}

### Policy:
{policy_text}

### Available Tools:
{tool_schemas}

### Your Assigned Entities (use PRIMARILY these — avoid others to prevent overlap):
{assigned_entities}

### Free-Text Arguments (NEVER include in compare_args):
{free_text_args}

### Write Tool Preconditions:
{domain_specific_write_preconditions}

## Task Schema

Each task must follow this exact schema:
```json
{
    "id": "{task_id}",
    "description": {
        "purpose": "What this task tests (English)",
        "relevant_policies": null,
        "notes": null
    },
    "user_scenario": {
        "persona": null,
        "instructions": {
            "domain": "{domain}",
            "reason_for_call": "Why user is calling (Russian)",
            "known_info": "What user knows (Russian)",
            "unknown_info": null,
            "task_instructions": "Exact user script (Russian)",
            "first_message": "Fixed first user message (Russian) — deterministic, used verbatim",
            "knowledge_boundary": "What user knows and does NOT know (Russian). Always end with: Вы НИКОГДА не предлагаете помощь — вы клиент.",
            "dialogue_scheme": [
                {"turn": 1, "user": "User opening", "expected_agent": "Agent response"},
                {"turn": 2, "user": "Follow-up", "expected_agent": "Agent action"},
                {"turn": 3, "user": "###STOP###", "expected_agent": null}
            ]
        }
    },
    "initial_state": null,
    "evaluation_criteria": {
        "actions": [
            {
                "action_id": "{task_id}_{action_index}",
                "requestor": "assistant",
                "name": "tool_name",
                "arguments": {"param": "value"},
                "compare_args": ["param"]
            }
        ],
        "env_assertions": null,
        "communicate_info": null,
        "nl_assertions": ["Агент должен ... (Russian)"],
        "reward_basis": ["ACTION", "NL_ASSERTION"],
        "user_nl_assertions": ["Пользователь указал ... (Russian)"]
    }
}
```

## Rules

1. **Arguments must reference real DB entities** — verify IDs exist in the DB dump above
2. **action_id format**: "{task_id}_{action_index}" (e.g., "5_0", "5_1")
3. **compare_args**: list params to match exactly. NEVER include free-text args: {free_text_args}
4. **reward_basis**: NO COMMUNICATE. Use:
   - `["ACTION", "NL_ASSERTION"]` for read-only tasks
   - `["ACTION", "DB", "NL_ASSERTION"]` for tasks with write tools
5. **nl_assertions**: 2-4 per task, in Russian
6. **user_nl_assertions**: 2-3 per task, check user simulator followed scenario
7. **first_message**: deterministic, contains entity IDs from known_info
8. **knowledge_boundary**: always end with "Вы НИКОГДА не предлагаете помощь — вы клиент."
9. **Last dialogue turn**: always `"###STOP###"` with `expected_agent: null`

## NL Assertion Guidelines (CRITICAL)

NL assertions must test what ACTION evaluation CANNOT — they must NOT duplicate tool-call verification.

GOOD (test communication/reasoning):
- "Агент объяснил клиенту, ПОЧЕМУ заявка отклонена, ссылаясь на правила политики"
- "Агент предупредил о возможных последствиях смены тарифа"
- "Агент корректно интерпретировал результат и сообщил пользователю итоговое решение"
- "Агент НЕ раскрыл внутренние данные о скоринге клиенту"

BAD (duplicate ACTION check — DO NOT USE):
- "Агент вызвал get_company_info с ИНН 5001234567" — ACTION already checks this
- "Агент создал заявку" — ACTION already checks the write tool was called
- "Агент использовал инструмент X" — pure tool-call check

Rule: If the assertion can be verified by checking tool call logs alone, it belongs in ACTION, not NL.

## Complexity: {complexity_tier}

{complexity_instructions_for_tier}

Return ONLY the JSON array. No markdown, no explanation.
```

**Complexity tier instructions** (include the relevant one in the subagent prompt):

For **easy/medium tier** (Agent 1):
```
Generate tasks with 3-4 gold actions. Focus on:
- Standard lookup → decision → action chains
- Clear-cut policy decisions (no edge cases)
- Single user intent, 2-turn dialogue
```

For **medium/hard tier** (Agent 2):
```
Generate tasks with 4-5 gold actions. Focus on:
- Conditional branching (agent must choose path based on discovered data)
- User cross-overs (user changes request mid-flow, adds to dialogue_scheme)
- Multi-turn dialogue (3+ turns)
```

For **hard/edge tier** (Agent 3):
```
Generate tasks with 5-6 gold actions. Focus on:
- Full lifecycle chains (lookup → verify → decide → act → confirm)
- Error recovery (first attempt fails, agent adapts)
- Policy edge cases (boundary conditions, multiple criteria)
- Escalation/transfer scenarios
```

### Step 8c: Merge Task Outputs

After all 3 subagents return:
1. Parse JSON arrays from each subagent
2. Verify task IDs don't conflict
3. Renumber action_ids if needed (`{task_id}_{action_index}`)
4. Concatenate into single array
5. Write to `data/tau2/domains/{domain}/ru-tasks_30.json` with `ensure_ascii=False`

## Step 9: Register Domain

### 9a. `src/tau2/registry.py`

Add imports at top (after existing fns_risk imports):
```python
from tau2.domains.{domain}.environment import \
    get_environment as {domain}_domain_get_environment
from tau2.domains.{domain}.environment import \
    get_tasks as {domain}_domain_get_tasks
from tau2.domains.{domain}.environment import \
    get_tasks_ru as {domain}_domain_get_tasks_ru
```

Add registration (after existing fns_risk registration):
```python
registry.register_domain({domain}_domain_get_environment, "{domain}")
registry.register_tasks({domain}_domain_get_tasks, "{domain}")
registry.register_tasks({domain}_domain_get_tasks_ru, "{domain}_ru")
```

### 9b. `src/tau2/evaluator/evaluator_nl_assertions.py`

Add import:
```python
from tau2.domains.{domain}.utils import get_{domain}_policy_path
```

Add to `get_domain_policy()` dict:
```python
"{domain}": get_{domain}_policy_path,
```

## Step 10: Validate

Run these checks (fix any errors before finishing):

```bash
# 1. Import test
PYTHONPATH=src:$PYTHONPATH python -c "
from tau2.domains.{domain}.environment import get_environment, get_tasks, get_tasks_ru
env = get_environment(language='ru')
print(f'Domain: {env.domain_name}')
print(f'Tools: {[t.name for t in env.get_tools()]}')
print(f'Policy: {len(env.policy)} chars')
tasks = get_tasks_ru()
print(f'Tasks: {len(tasks)}')
"

# 2. DB round-trip
PYTHONPATH=src:$PYTHONPATH python -c "
from tau2.domains.{domain}.data_model import {Domain}DB
from tau2.domains.{domain}.utils import {DOMAIN_UPPER}_DB_PATH
db = {Domain}DB.load({DOMAIN_UPPER}_DB_PATH)
h1 = db.get_hash()
db2 = {Domain}DB.load({DOMAIN_UPPER}_DB_PATH)
h2 = db2.get_hash()
assert h1 == h2, 'Hash mismatch!'
print(f'DB hash: {h1[:16]}... (stable)')
print(f'Collections: { {k: len(v) if isinstance(v, (list, dict)) else 1 for k, v in db.model_dump().items()} }')
"

# 3. Tool execution test
PYTHONPATH=src:$PYTHONPATH python -c "
from tau2.domains.{domain}.environment import get_environment
env = get_environment(language='ru')
tools_dict = {t.name: t for t in env.get_tools()}
for name, tool in tools_dict.items():
    print(f'Tool: {name} — {tool.tool_type}')
"

# 4. Task validation
PYTHONPATH=src:$PYTHONPATH python -c "
from tau2.domains.{domain}.environment import get_tasks_ru
tasks = get_tasks_ru()
for t in tasks:
    assert t.evaluation_criteria.nl_assertions, f'Task {t.id}: no nl_assertions'
    for a in (t.evaluation_criteria.actions or []):
        assert a.compare_args, f'Task {t.id} action {a.action_id}: no compare_args'
    print(f'Task {t.id}: {len(t.evaluation_criteria.actions or [])} actions, {len(t.evaluation_criteria.nl_assertions)} NL assertions — OK')
print(f'All {len(tasks)} tasks valid.')
"

# 5. Registry test
PYTHONPATH=src:$PYTHONPATH python -c "
from tau2.registry import registry
info = registry.get_info()
assert '{domain}' in info.domains, 'Domain not registered!'
assert '{domain}_ru' in info.task_sets, 'RU tasks not registered!'
print(f'Registry OK: {info.domains}')
"
```

Fix ALL validation errors before declaring the domain complete.

## Step 10.5: Cross-Task Validation (Automated)

After task generation and basic validation, run this automated cross-task check. No LLM needed — pure Python, runs in <1 second.

```python
import json, sys
from collections import Counter, defaultdict
sys.path.insert(0, "src")
from tau2.domains.{domain}.environment import get_tasks_ru, get_environment

tasks = get_tasks_ru()
env = get_environment(language='ru')
all_tool_names = [t.name for t in env.get_tools()]
db = env.tools.db.model_dump()

issues = []

# 1. Entity coverage — find DB entities never referenced in any task
used_entities = set()
entity_counter = Counter()
for t in tasks:
    for a in t.evaluation_criteria.actions:
        for k, v in a.arguments.items():
            if isinstance(v, str):
                used_entities.add(v)
                entity_counter[v] += 1

for collection_name, collection in db.items():
    if isinstance(collection, dict):
        for key in collection:
            if key not in used_entities:
                issues.append(f"COVERAGE: DB entity {collection_name}.{key} never referenced in any task")

# 2. Overused entities (>25% of tasks)
for entity, count in entity_counter.most_common():
    pct = count / len(tasks)
    if pct > 0.25:
        issues.append(f"OVERUSE: Entity '{entity}' used in {count}/{len(tasks)} tasks ({pct:.0%})")

# 3. Duplicate action chains (3+ tasks with identical tool sequence)
chain_counter = defaultdict(list)
for t in tasks:
    chain = " -> ".join(a.name for a in t.evaluation_criteria.actions)
    chain_counter[chain].append(t.id)
for chain, tids in chain_counter.items():
    if len(tids) >= 3:
        issues.append(f"DUPLICATE_CHAIN: {len(tids)} tasks with identical chain '{chain}': {tids}")

# 4. Duplicate NL assertion text across tasks
nl_texts = defaultdict(list)
for t in tasks:
    for nl in (t.evaluation_criteria.nl_assertions or []):
        nl_norm = nl.strip().lower()
        nl_texts[nl_norm].append(t.id)
for text, tids in nl_texts.items():
    if len(tids) >= 2:
        issues.append(f"DUPLICATE_NL: NL assertion appears in {len(tids)} tasks ({tids}): '{text[:80]}...'")

# 5. NL assertions that duplicate ACTION checks
action_dup_count = 0
action_dup_total = 0
action_keywords = ['вызвал', 'использовал инструмент', 'вызвала', 'использовала функцию']
for t in tasks:
    for nl in (t.evaluation_criteria.nl_assertions or []):
        action_dup_total += 1
        nl_lower = nl.lower()
        tool_names_in_nl = [tn for tn in all_tool_names if tn in nl_lower]
        if tool_names_in_nl and any(kw in nl_lower for kw in action_keywords):
            action_dup_count += 1
            issues.append(f"NL_DUPS_ACTION: Task {t.id} NL assertion restates tool call: '{nl[:80]}...'")
if action_dup_total > 0 and action_dup_count / action_dup_total > 0.3:
    issues.append(f"NL_DUPS_ACTION_SYSTEMATIC: {action_dup_count}/{action_dup_total} NL assertions duplicate ACTION checks")

# Summary
if issues:
    print(f"CROSS-TASK VALIDATION: {len(issues)} issues found")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("CROSS-TASK VALIDATION: all checks passed")
```

**If issues are found:** Fix them before proceeding. Common fixes:
- COVERAGE: Add a task using the unused entity
- OVERUSE: Redistribute tasks to use different entities
- DUPLICATE_CHAIN: Differentiate tasks (add branches, different outcomes)
- DUPLICATE_NL: Rewrite NL assertions to be task-specific
- NL_DUPS_ACTION: Rewrite to test communication quality instead of tool calls

## Step 10.5b: Interactive API Testing (Optional)

**Only if `--api` flag is provided.** Parse the flag for agent and user endpoints:
```
--api agent=http://host:port/v1,model=model_name user=http://host:port/v1,model=model_name
```

For each generated task, run a mini-simulation to verify the task is solvable and non-trivial:

```bash
# Set up environment for tau2 run
export OPENAI_API_KEY=dummy
export OPENAI_BASE_URL={user_url}
export OPENAI_API_KEY_ASSISTANT=dummy
export OPENAI_BASE_URL_ASSISTANT={agent_url}
export NO_PROXY={agent_host},{user_host}
export no_proxy={agent_host},{user_host}

# Run single task
PYTHONPATH=src:$PYTHONPATH python -m tau2.cli run \
    --domain {domain} --language ru \
    --agent-llm {agent_model} --user-llm {user_model} \
    --user scripted_user \
    --task-ids {task_id} \
    --num-trials 1 --max-steps 30 --max-concurrency 1 \
    --save-to data/simulations/create_domain_test_{domain}
```

Run tasks sequentially (or up to 3-5 concurrent). After each task completes, check the result:

```python
import json
with open("data/simulations/create_domain_test_{domain}/{domain}.json") as f:
    data = json.load(f)

for sim in data["simulations"]:
    tid = sim["task_id"]
    ri = sim.get("reward_info", {})
    rb = ri.get("reward_breakdown", {})
    reward = ri.get("reward", 0)
    action = rb.get("ACTION", 0)
    nl_checks = ri.get("nl_assertions", [])
    nl_frac = sum(1 for c in nl_checks if c.get("met")) / len(nl_checks) if nl_checks else 1.0

    flags = []
    if reward == 0 and action == 0:
        flags.append("AGENT_FAILED — may be too hard or broken")
    if reward == 1.0 and action == 1.0 and nl_frac == 1.0:
        flags.append("TRIVIAL — agent passed perfectly on first try")
    if nl_frac == 1.0 and action < 1.0:
        flags.append("NL_HALLUCINATION — NL passed but action failed")
    if not nl_checks:
        flags.append("NO_NL_CHECKS — NL assertions not evaluated")

    status = " | ".join(flags) if flags else "OK"
    print(f"Task {tid}: reward={reward} action={action} nl={nl_frac:.2f} — {status}")
```

**Interpretation:**
- **AGENT_FAILED**: Task may be too hard, ambiguous, or broken. Review gold actions and policy.
- **TRIVIAL** (for `hard` complexity): Task may be too easy. Consider adding complexity.
- **NL_HALLUCINATION**: NL assertions may be too vague — tighten them.
- **OK**: Task works as intended.

**If `--api` is not provided:** Skip this step entirely (pure structural validation only).

## Step 11: Finalize

After all validation passes:

1. Report summary: task count, complexity distribution, action count stats, entity coverage
2. List any remaining warnings from Step 10.5
3. **Pointer to deep evaluation:** "For deep cross-task analysis including NL verification and simulation-aware scoring, run `/evaluate-tasks {domain}` after the domain stabilizes."

## Checklist

Before finishing, verify:
- [ ] `src/tau2/domains/{domain}/` — all 5 Python files created (skip if `--tasks-only`)
- [ ] `data/tau2/domains/{domain}/` — db.json, policy.md, ru-policy.md, ru-tasks_30.json
- [ ] Task count matches `--tasks N` parameter (default 15)
- [ ] Complexity profile enforced:
  - `hard`: ALL tasks 3+ actions, 60%+ multi-turn, tool info reuse, user cross-overs
  - `mixed`: proper distribution across simple/medium/hard/edge
  - `easy`: simple tasks for smoke testing
- [ ] All task arguments reference valid DB entities — **execute gold actions against DB to verify**
- [ ] Write tools have `compare_args` set and `get_hash()` excludes free-text
- [ ] Domain registered in registry.py (skip if `--tasks-only`)
- [ ] Domain added to evaluator_nl_assertions.py `get_domain_policy()` (skip if `--tasks-only`)
- [ ] All validation checks pass (Step 10)
- [ ] Cross-task validation passes (Step 10.5) — no duplicate chains, no overused entities
- [ ] NL assertions do NOT duplicate ACTION checks (test communication quality, not tool calls)
- [ ] `reward_basis` does NOT include COMMUNICATE
- [ ] Policy does NOT duplicate tool API signatures
- [ ] For `hard` complexity: verify action count distribution (no tasks with <3 actions)
