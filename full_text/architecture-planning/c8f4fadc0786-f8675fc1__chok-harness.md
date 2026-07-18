---
name: chok-harness
description: "AI agent harness engineering auditor. Scans project harness configuration (CLAUDE.md, hooks, MCP, skills, agents, security, workflow, entropy management, data schema quality, component reusability, agent governance) across 14 dimensions, generates a 0-100% normalized maturity score (raw points kept internal for weighted calculation only, surface output is per-track % normalized (dev shown by default, planning/design opt-in) for trend tracking), detects 16 anti-patterns, and provides actionable improvement recommendations with a phased build roadmap. Uses Socratic clarification when user intent is ambiguous (new harness build/modification direction). Supports 27 Claude Code hook events and 4 handler types (Command, HTTP, Prompt, Agent). Includes an Operational Point Map (27 hooks × common components) and structured data schema validation."
origin: custom
triggers:
  keywords: [하네스, hooks, MCP, 설정 감사, harness, 에이전트 거버넌스]
  type: verify
  model-hint: sonnet
---

# chok-harness — Harness Engineering Auditor

AI 에이전트 하네스 엔지니어링을 14개 차원에서 감사하고, **dev 트랙 0-100% 정규화 점수**로 스코어링한다 (기획/디자인 트랙은 opt-in 독립 정규화). 구체적인 개선안과 구축 로드맵을 생성한다.
스킬 내 데이터 스키마가 AI가 정확히 파싱할 수 있는 구조화된 형식(XML 또는 JSON Schema)인지 검수하고, 필요 시 자동 재작성한다.
27개 운영포인트(hook 이벤트) × 공통 컴포넌트(rules/skills/agents) 매핑 매트릭스를 생성하여, 공용 자산이 실제로 운영 시점에 연결되고 있는지 가시화한다.

> **% 트랙별 단일 기준 근거**: 사용자 노출 점수는 트랙별 단일 정규화(dev/planning/design 각 트랙 내 0-100% 단일, raw+normalized 이중 표기 금지). 트랙 간은 직교 축이라 합산하지 않는다. 기본 감사는 dev 1개만 노출, planning/design은 opt-in. dimension별 가중치는 트랙 내부 계산에만 유지, raw는 `harness-score.json`에서 deprecated read-only.

> **"Agent = Model + Harness"** (Mitchell Hashimoto, 2026) — 같은 모델이라도 하네스 품질에 따라 생산성이 10배 차이난다. LangChain은 하네스만 변경하여 52.8%→66.5% (top-30→top-5)로 개선. Opus는 하네스 교체만으로 순위 33위→5위 상승.

## Usage

```
/chok-harness [--fix] [--json] [--compare] [--dimension <name>] [--track <planning|design>] [--generate-planning [dir]] [--generate-design [dir]]
```

| Flag | Description |
|------|-------------|
| (none) | 전체 14차원 감사 + 스코어 + 제안 + 로드맵 |
| `--fix` | 자동 수정 가능한 항목 즉시 적용 (사용자 확인 후) |
| `--json` | JSON 형식으로 출력 |
| `--compare` | 이전 스캔 결과와 비교 |
| `--dimension <name>` | 특정 차원만 검사 (config, hooks, security, tools, knowledge, agents, workflow, context, testing, entropy, schema, reusability, governance, team-architecture) |
| `--rewrite-xml` | 스킬 내 JSON/markdown 데이터 스키마를 XML로 자동 재작성 |
| `--track <planning\|design>` | 개발 외 서브트랙 감사 (요청 시, 독립 0-100%) |
| `--generate-planning [dir]` | 기획 하네스 생성 (공백만 scaffold, 멱등) |
| `--generate-design [dir]` | 디자인 하네스 생성 (공백만 scaffold, 멱등) |

## Execution Procedure

### Step 0: Argument Parsing

Parse the arguments to determine mode:
- No arguments → full audit
- `--fix` → audit + auto-fix
- `--json` → audit with JSON output
- `--compare` → audit + diff with previous
- `--dimension <name>` → single dimension audit
- `--track planning` / `--track design` → 해당 서브트랙 감사 (독립 정규화, 핵심 14차원과 분리)
- `--generate-planning [dir]` / `--generate-design [dir]` → 생성기 모드 (Phase 2, references/generator-*.md 로드)

### Step 0.5: Intent Clarification (Socratic) — 조건부 발동

새 하네스 구축이나 수정 방향이 모호할 때 권고/수정이 사용자 의도와 어긋나지 않도록 사전 의도 파악.

**발동 조건** (모두 자동 평가):

```xml
<trigger-conditions logic="OR">
  <cond name="ambiguous-fix">--fix flag AND auto-fixable items count >= 3</cond>
  <cond name="new-project">no .claude/harness-score.json (first audit on this project)</cond>
  <cond name="broad-recommend">no --dimension AND no --json (full audit + recommendation path)</cond>
  <cond name="track-intent">--track or --generate-* flag present AND 대상 트랙 산출물 부재 (생성 권고 분기 필요)</cond>
</trigger-conditions>
```

**비발동 조건**:

```xml
<skip-conditions logic="OR">
  <cond>--json (automation/CI context — no human in loop)</cond>
  <cond>--compare (intent already fixed in previous run)</cond>
  <cond>--dimension &lt;name&gt; (user narrowed scope = intent declared)</cond>
  <cond>--rewrite-xml (mechanical transformation, no judgment)</cond>
</skip-conditions>
```

**문답 프로토콜** — AskUserQuestion 1회, 5초 안에 답 가능한 closed/semi-open 형식:

```xml
<question id="audit-purpose" max-options="4">
  <prompt>이 감사의 목적은?</prompt>
  <option key="diagnose">현재 점수 진단만 (보고서만 필요)</option>
  <option key="prioritize">다음 스프린트 개선 우선순위 결정</option>
  <option key="design">신규 하네스 설계 (현재 점수 낮음)</option>
  <option key="standardize">팀 전체 표준화 (다른 프로젝트 비교)</option>
</question>
```

**응답별 동작**:

| 응답 | Step 4 권고 톤 | 추가 동작 |
|------|--------------|----------|
| diagnose | 점수만 출력, 권고 최소화 | Step 4 권고안 생략, 보고서로 종료 |
| prioritize | 시간/노력 대비 ROI 순 정렬 | Step 4-B 우선순위 가중치 질문 발동 |
| design | `/harness` (revfactory) 위임 권고 강조 | D6/D7 도메인 적합성 질문 발동 |
| standardize | 다른 프로젝트 score.json 비교 권고 | `--compare` 실행 안내 |

`AskUserQuestion` 미응답/타임아웃 → "prioritize" 기본값 (가장 안전한 fallback).

**트랙 의도 질문** — `track-intent` 조건 발동 시 추가 질문:

> `track-purpose`는 trigger-conditions의 track-intent cond가 발동했을 때만 노출한다 (when 속성 = 노출 조건).

```xml
<question id="track-purpose" max-options="3" when="--track or --generate-* present">
  <prompt>기획/디자인 하네스 작업 목적은?</prompt>
  <option key="audit-only">현재 기획/디자인 하네스 점수 진단만</option>
  <option key="generate">공백을 채워 기획/디자인 하네스 생성</option>
  <option key="both">진단 후 공백이면 생성까지</option>
</question>
```

**track-purpose 응답별 동작**:

| 응답 | 동작 |
|------|------|
| audit-only | 해당 트랙 감사 후 종료 (생성기 진입 안 함) |
| generate | Phase 2 생성기(`--generate-*`)로 바로 진행 |
| both | 감사 먼저 → 공백 발견 시 생성기 진입 |

미응답 → `audit-only` (안전 fallback).

### Step 1: Project Discovery

Scan these locations to build the project profile:

```
Global paths:
  ~/.claude/CLAUDE.md
  ~/.claude/settings.json
  ~/.claude/settings.local.json
  ~/.claude/rules/
  ~/.claude/skills/
  ~/.claude/agents/
  ~/.claude/commands/
  ~/.claude/teams/
  ~/.claude/plugins/
  ~/.claude/scheduled-tasks/
  ~/.mcp.json

Project paths (from working directory):
  ./CLAUDE.md or .claude/CLAUDE.md
  ./.claude/settings.json
  ./.claude/settings.local.json
  ./.claude/rules/
  ./.claude/skills/
  ./.claude/agents/
  ./.claude/commands/
  ./.claude/plugins/          # Plugin hooks/hooks.json
  ./.claude/scheduled-tasks/  # Scheduled task definitions
  ./.claude/launch.json       # Dev server configurations
  ./.mcp.json
  ./.gitignore
  ./.env.example or .env.local
  ./.github/workflows/
  ./AGENTS.md

  # 기획 트랙 (--track planning / --generate-planning 시에만 스캔)
  ./docs/planning/
  ./spec.md or ./docs/spec*.md
  ./.claude/skills/**/{split-requirements,sequence-diagram,user-flow,logic-check}*
  docs/planning/commands/{split-requirements,sequence-diagram,user-flow,logic-check}*  (기본; 커스텀은 tracks.planning.path/commands/)
  # 디자인 트랙 (--track design / --generate-design 시에만 스캔)
  ./docs/design/
  ./tokens.* or ./theme.* or ./docs/design/tokens*

  # 라운드트립: 커스텀 target-dir은 .claude/harness-score.json의 tracks.<track>.path에서 읽어 스캔

Settings file hierarchy (highest to lowest precedence):
  1. Managed policy (org-wide admin)
  2. ~/.claude/settings.json (user global)
  3. .claude/settings.json (project, shareable)
  4. .claude/settings.local.json (project, gitignored)
  5. Plugin hooks/hooks.json
  6. Skill/Agent YAML frontmatter
```

Use `Glob` and `Read` tools to check existence and content of each path. Record findings as a checklist.

### Step 2: Dimension Scoring

Score each of the 14 dimensions. For each item, check the condition and award points if met.

각 차원의 채점 항목(`<item>`) 전문: Read("~/.claude/skills/chok-harness/references/dimensions.md")

아래는 차원 인덱스(이름 + 만점 + 가중치 주석)와 각 차원의 채점 맥락을 정하는 prose note이다. 실제 `<item>` 채점 조건은 위 references/dimensions.md에 보관되어 있으니, 점수 산정 시 해당 파일을 로드하여 적용한다.

| Dimension | Max Points |
|-----------|-----------|
| D1: Configuration Quality | 12 (raw / 10% normalized) |
| D2: Hook Coverage | 12 (was 15 — zero-sum 재분배 by D14 신설) |
| D3: Security Posture | 12 |
| D4: Tool Integration | 8 |
| D5: Knowledge System | 8 |
| D6: Agent Architecture | 10 |
| D7: Workflow Automation | 10 |
| D8: Context Management | 8 |
| D9: Testing & Feedback | 8 |
| D10: Entropy Management | 6 |
| D11: Data Schema Quality | 5 (was 7 — zero-sum 재분배 by D14 신설) |
| D12: Component Reusability | 8 |
| D13: Agent Governance | 8 |
| D14: Agent Team Architecture | 5 (신규 — revfactory/harness 6-phase + 6-pattern) |

#### 서브트랙 (on-demand, 핵심 14차원과 분리 채점)

| 트랙 | raw | 채점 ref | 발동 |
|------|-----|----------|------|
| planning | 20 | `references/dimensions-planning.md` | `--track planning` / `--generate-planning` |
| design | 14 | `references/dimensions-design.md` | `--track design` / `--generate-design` |

서브트랙은 자체 raw → 독립 0-100% 정규화. 핵심 14차원 점수에 합산하지 않는다 (트랙별 단일 정규화).

#### Dimension 1: Configuration Quality (12 points raw / 10% normalized)

기본 구조 점검(7개 item × 합계 12점)에 더하여 CLAUDE.md 자체의 품질을 claude-md-improver 6-차원 평가(100pt → A-F)로 보조 출력한다. 6-차원 평가는 D1 raw 점수에 영향을 주지 않으며(가중치는 12pt 그대로 유지), companion field로 `claude_md_grade`를 추가 출력하여 정밀 진단을 가능케 한다.

#### Dimension 2: Hook Coverage (12 points, was 15 — zero-sum 재분배 by D14 신설)

Read `settings.json` (both global and project) and inspect the `hooks` object.

> Claude Code now supports **27 hook events** across 8 categories and **4 handler types** (Command, HTTP, Prompt, Agent).
>
> **27 Hook Events**: SessionStart, SessionEnd, InstructionsLoaded, UserPromptSubmit, PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest, PermissionDenied, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, Stop, StopFailure, TeammateIdle, Elicitation, ElicitationResult, WorktreeCreate, WorktreeRemove, ConfigChange, CwdChanged, FileChanged, Notification, PreCompact, PostCompact, MessageDisplay
>
> **4 Handler Types**: Command (shell script, exit codes control flow), HTTP (POST to endpoint, supports `headers` with `allowedEnvVars`), Prompt (single-turn LLM evaluation), Agent (spawns subagent with tool access)
>
> **Key Config Options**: `async: true` (background execution), `asyncRewake: true` (wake on exit code 2), `if` field (permission-rule filter), `once: true` (run once per session), `statusMessage` (custom spinner text), `disableAllHooks: true` (global disable)
>
> **Hook Return-Field Capabilities (CC 2.1.x, CHANGELOG-verified)**: `reloadSkills: true` (SessionStart return — re-scan skill dirs, v2.1.152); `hookSpecificOutput.additionalContext` (Stop/SubagentStop return — feed text back, keep turn going, v2.1.163); `args: string[]` (hook exec-form — spawn without shell, v2.1.139); `terminalSequence` (hook JSON output — desktop notifications/titles/bells, v2.1.141). `MessageDisplay` (v2.1.152) transforms or hides assistant message text as displayed. Stop/SubagentStop hook **input** now includes `background_tasks` and `session_crons` fields (v2.1.145).
>
> **Self-hosted runner lifecycle**: `post-session` hook (v2.1.169) runs after the session ends and before the workspace is deleted — for snapshotting uncommitted work or exporting logs. This is a runner lifecycle hook, distinct from the 27 settings.json hook events above.
>
> **Exit Code Semantics**: 0=success, 2=blocking error (blocks PreToolUse, denies PermissionRequest), other=non-blocking
>
> **Permission Decisions** (PreToolUse): `deny` > `defer` > `ask` > `allow`. `defer` (v2.1.89+) pauses at tool call for headless integrations.

#### Dimension 3: Security Posture (12 points)

#### Dimension 4: Tool Integration (8 points)

#### Dimension 5: Knowledge System (8 points)

> Progressive disclosure pattern (HumanLayer): Knowledge/tools activated only when needed, preventing premature context consumption.

> **agentskills.io spec conformance + supply-chain provenance**: optional `compatibility` field (≤500 chars — declares product/system-package/network needs), experimental `allowed-tools` (space-separated pre-approved list), name rules (1–64 chars, no consecutive `--`, must match parent dir); `skills-ref validate ./skill` checks conformance. Supply-chain: `gh skill install` (gh v2.90.0+) writes provenance (repo / git-ref / tree-SHA) into SKILL.md frontmatter — prefer provenance-tracked installs over untracked copies. (Non-scored guidance; Knowledge dimension is budget-full at 8/8.)

> **SKILL.md 길이 감사 (비점수 flag)**: 공식 한계는 **본문 < 500줄**. 감사 시 `wc -l skills/*/SKILL.md`로 초과 스킬을 flag하고 progressive-disclosure(references/ 분리)를 권고한다. 작성/리팩토링 규약은 `Read("~/.claude/skills/shared/skill-authoring-rules.md")` 참조. >500줄 = progressive-disclosure 위반 → 컨텍스트 bloat 안티패턴.

#### Dimension 6: Agent Architecture (10 points)

#### Dimension 7: Workflow Automation (10 points)

#### Dimension 8: Context Management (8 points)

#### Dimension 9: Testing & Feedback (8 points)

#### Dimension 10: Entropy Management (6 points)

> Source: NxCode, OpenAI, Anthropic, Philipp Schmid all emphasize "periodic garbage collection" for agent-generated entropy. Philipp Schmid's "Build to Delete" philosophy: harness components must be modular enough to remove as models improve. Martin Fowler's **Feedforward/Feedback** control model: Guides (anticipate behavior) + Sensors (observe and correct). Philipp Schmid: competitive advantage is not the prompt — it is the **trajectories your harness captures** (structured failure logging as training flywheel). Manus refactored their harness 5 times in 6 months; Vercel removed 80% of agent tools to improve efficiency.

#### Dimension 11: Data Schema Quality (5 points, was 7 — zero-sum 재분배 by D14 신설)

> AI 에이전트가 스킬 내 데이터 계약(output schema, severity table, routing rule 등)을 정확히 파싱하려면 구조화된 형식(XML 또는 JSON Schema)이 비구조 markdown table보다 우월하다. 이 차원은 스킬 파일들의 데이터 스키마가 AI-optimized 구조화 형식으로 정의되어 있는지 평가한다.

#### Dimension 12: Component Reusability (8 points)

> 출처: DRY(Don't Repeat Yourself), Martin Fowler Feedforward/Feedback control model, Philipp Schmid "Build to Delete"(모듈성이 삭제 가능성을 만든다), Vercel(80% 도구 제거로 효율 개선), Manus(6개월간 하네스 5회 리팩터링).
>
> 이 차원은 "하네스 자산이 공통 기반(common base)으로 추출되어 운영포인트(hook 이벤트, 명령 진입점, agent 체인)에서 반복 없이 재사용되는가"를 평가한다. 단순 존재 여부가 아닌 **(a) 계층 구조(공통 vs 특화), (b) 운영 시점 연결, (c) 설계/구조 정리(카탈로그·명명 규약·인터페이스 계약 문서화)** 세 가지를 측정한다.

#### Dimension 13: Agent Governance (8 points)

> 출처: Gravitee "State of AI Agent Security", Kiteworks "AI Agent Data Governance", Bessemer "Securing AI Agents", MCP Roadmap (OAuth 2.1), EU AI Act. 업계 조사에 따르면 63%의 조직이 agent 목적 제한 불가, 60%가 오작동 agent 종료 불가, 33%가 감사 추적 없음. Agent를 독립적인 identity bearer로 관리하고, 최소 권한 원칙을 적용하며, 모든 행동을 추적 가능하게 만드는 거버넌스 체계가 필수다.

> **Tool-scope governance (CC 2.1.x, CHANGELOG-verified)**: skills/commands can set `disallowed-tools` frontmatter (v2.1.152 — removes tools from the model while the skill is active); the `skillOverrides` setting (v2.1.129) supports `off` (hide from model and `/`) and `user-invocable-only` (hide from model only). Both serve least-privilege — audit whether high-blast-radius skills declare them.

#### Dimension 14: Agent Team Architecture (5 points, 신규 — revfactory/harness 6-phase + 6-pattern)

> 출처: revfactory/harness — agent-team factory tool. 6-phase 워크플로(Domain Analysis → Architecture Design → Agent Definition Generation → Skill Generation → Integration & Orchestration → Validation & Testing) + 6 패턴(Pipeline / Fan-out / Expert Pool / Producer-Reviewer / Supervisor / Hierarchical Delegation). 본 차원은 zero-sum 재분배로 신설 (D2 15→12, D11 7→5에서 -5 흡수, raw 인플레 없음). +60% avg quality, 15/15 win-rate (revfactory 보고).

### Step 2.5: Anti-Pattern Detection (Bonus Warnings)

Read("~/.claude/skills/chok-harness/anti-patterns.xml") 을 로드하여 16개 안티패턴 정의를 적용한다. 안티패턴 경고는 보고서에서 권고안 BEFORE에 별도 섹션으로 표시한다.

### Step 2.6: Operational Point Map (운영포인트 매핑)

Read("~/.claude/skills/chok-harness/ops-map-template.xml") 을 로드하여 27개 운영포인트 매핑 절차, 매트릭스 템플릿, 보고서 포맷, 우선순위 운영포인트를 적용한다.

### Step 2.7: Priority Inquiry (Step 0.5 응답이 `prioritize`일 때만)

Step 0.5에서 사용자가 `prioritize`를 선택한 경우, scoring-output.md 위임 전 권고 우선순위 가중치를 1회 수집한다.

```xml
<question id="priority-weights" max-options="4">
  <prompt>개선 우선순위는?</prompt>
  <option key="security-first">보안/거버넌스 우선 (D3, D13)</option>
  <option key="velocity-first">자동화/워크플로 우선 (D2, D7)</option>
  <option key="quality-first">테스트/엔트로피 우선 (D9, D10)</option>
  <option key="balanced">균형 — 점수 차이 큰 순</option>
</question>
```

응답은 scoring-output.md 호출 시 `priority_mode={key}` 인자로 전달. 미응답 → `balanced` 기본값.

Read("~/.claude/skills/chok-harness/scoring-output.md") 을 로드하여 Steps 3-7 (스코어 계산, 권고안 생성, 로드맵, 출력 보고서, 결과 저장)을 실행한다.

## 모드별 실행 절차 (--fix / --compare / --dimension / --rewrite-xml)

각 모드 상세 절차: `Read("~/.claude/skills/chok-harness/references/modes.md")`

## 생성기 모드 (--generate-planning / --generate-design)

감사기 → 감사+생성기 확장 (chok-loop audit|generate 패턴). 멱등 — 감사로 공백만 식별해 채운다.

- `--generate-planning [dir]` → `Read("~/.claude/skills/chok-harness/references/generator-planning.md")` 절차 적용
- `--generate-design [dir]` → `Read("~/.claude/skills/chok-harness/references/generator-design.md")` 절차 적용

전제: 생성 전 개발 하네스 감사로 토대 확인 (개발>기획>디자인). 생성은 사용자 확인 게이트 후. target-dir은 `tracks.<track>.path`에 저장 (라운드트립).

## Step 8: Retrospective (회고)

감사 완료 후 감사 과정 자체의 품질과 권고안의 실효성을 종합 회고한다.

회고 프로토콜: Read("~/.claude/skills/shared/retrospective-protocol.md")

### 이 스킬의 평가 관점

| 관점 | 평가 내용 | 만점 |
|------|----------|------|
| **Audit Fairness** | 점수 산정이 공정했는가? 과대/과소 평가된 항목이 있는가? | /5 |
| **Recommendation Viability** | 권고안이 실행 가능한가? 우선순위가 프로젝트 상황에 맞는가? | /5 |
| **Trend Analysis** | 이전 감사 대비 개선되었는가? 퇴보한 차원이 있는가? | /5 |

### 고유 분석: 점수 변동 트렌드

이전 스캔 결과(.claude/harness-score.json)가 있으면 총점 변화, 개선/퇴보 차원, 변동 없는 차원을 분석한다. 첫 감사이면 트렌드 분석을 건너뛴다.

---

## Supervisor Integration (감독관 연동)

감독관 체크포인트 프로토콜: Read("~/.claude/skills/shared/supervisor-checkpoint.md")

### 이 스킬의 체크포인트

| 시점 | 검토 질문 |
|------|----------|
| Step 3 (스코어 계산) 완료 | "점수 산정이 공정한가? 누락된 차원이 있는가? 과대/과소 평가된 항목이 있는가?" |
| Step 4 (권고안 생성) 완료 | "권고안이 실행 가능한가? 우선순위가 타당한가? 프로젝트 상황에 맞는가?" |
| --fix 적용 후 | "자동 수정이 올바르게 적용되었는가? 의도하지 않은 변경이 있는가?" |

### REVISE 제한 오버라이드

- 감사 결과: 최대 **1회** REVISE
- --fix 적용: 최대 **1회** REVISE

## Reference Sources

전체 인용 출처 목록(Core / Community / Hooks / Governance / MCP / Maturity / Generator Patterns): Read("~/.claude/skills/chok-harness/references/sources.md")
