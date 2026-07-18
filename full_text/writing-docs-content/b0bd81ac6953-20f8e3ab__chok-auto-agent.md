---
name: chok-auto-agent
description: "Autonomous multi-task agent team. /loop chok-auto-agent으로 실행. docs/tasks.md에서 태스크를 읽어 chok-supervisor(PM) → gstack(실행) → chok-debug(검증) → chok-fix(수정) → chok-supervisor(최종확인) 파이프라인을 반복. 방향 이탈 감지 시 태스크 자동 재설계 후 개발 재진입. 토큰 소진 시 상태 저장 후 ScheduleWakeup으로 자동 재개. 모든 태스크 완료까지 루프."
origin: custom
triggers:
  keywords: [자동 실행, loop, 다중 태스크, autonomous]
  type: execute
  model-hint: sonnet
---

# chok-auto-agent — 자율 멀티태스크 에이전트 팀

`/loop chok-auto-agent`로 실행. `docs/tasks.md`의 미완료 태스크를 소진할 때까지 자동 처리.
방향 이탈 감지 시 태스크를 자동 재설계하여 올바른 방향으로 개발을 이어간다.

## 실행 방법

```
/loop chok-auto-agent [--dry-run] [--task-file PATH] [--wait-hours N] [--check-interval N]
```

<options>
  <option flag="--dry-run"        default="false"          description="태스크 목록만 출력, 실행 안 함" />
  <option flag="--task-file"      default="docs/tasks.md"  description="태스크 파일 경로" />
  <option flag="--wait-hours"     default="5"              description="토큰 소진 후 재개까지 대기 시간(시간)" />
  <option flag="--check-interval" default="3"              description="DAC 실행 주기 (완료 태스크 N개마다)" />
</options>

---

## Step 0: Preamble

매 이터레이션 시작 시 반드시 먼저 실행한다.

```bash
STATE_FILE="$HOME/.gstack/chok-auto-agent/state.json"
mkdir -p "$HOME/.gstack/chok-auto-agent"

[ -f "$STATE_FILE" ] && cat "$STATE_FILE" && echo "STATE: RESUME" || echo "STATE: FRESH"
echo "TIMESTAMP: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

TASK_FILE="${TASK_FILE:-docs/tasks.md}"
if [ -f "$TASK_FILE" ]; then
  PENDING=$(grep -c '^\s*- \[ \]' "$TASK_FILE" 2>/dev/null || echo "0")
  echo "TASK_FILE: $TASK_FILE  PENDING_TASKS: $PENDING"
  cat "$TASK_FILE"
else
  echo "TASK_FILE_MISSING: $TASK_FILE"
fi
```

<preamble-routing>
  <route condition="STATE: FRESH"                               action="Step 0c DAC — 베이스라인 캡처 후 Step 1" />
  <route condition="STATE: RESUME AND phase == dac_in_progress" action="Step 0c DAC 재개 — Phase F (조정 액션)부터 재시작" />
  <route condition="STATE: RESUME AND phase == gstack_done"     action="Step 4 (chok-debug) 직행 — post-gstack 컨텍스트 리셋 후 재개" />
  <route condition="STATE: RESUME"                              action="state.json의 current_task + phase부터 재개" />
  <route condition="PENDING_TASKS: 0"                           action="Step 7 — 완료 리포트 후 루프 종료" />
  <route condition="TASK_FILE_MISSING"                          action="에스컬레이션 — 사용자에게 파일 경로 요청 후 중단" />
</preamble-routing>

---

## Step 0c: 방향 정렬 점검 (Direction Alignment Check, DAC)

Preamble 이후, 태스크 선택(Step 1) 이전에 실행한다.
프로젝트 전체 궤적이 최초 목표와 일치하는지 주기적으로 점검한다.
**방향 이탈 감지 시 사용자에게 에스컬레이션하지 않는다. 태스크를 자동 재설계 후 개발을 이어간다.**

### 트리거 조건

<dac-triggers>
  <trigger id="baseline"     condition="dac_last_run_at == null"
           description="최초 실행 — 베이스라인 캡처 후 DAC 실행" />
  <trigger id="interval"     condition="dac_task_counter_since_check >= CHECK_INTERVAL"
           description="주기적 점검 — CHECK_INTERVAL = args[--check-interval] ?? state.dac_check_interval ?? 3" />
  <trigger id="reject-rate"  condition="recent_verdicts[-5:].count('REJECT') / 5 > 0.30"
           description="이상 감지 — 최근 5회 감독관 판정 중 REJECT 30% 초과" />
  <trigger id="repeat-issue" condition="recent_issue_types[-2] != null AND recent_issue_types[-2] == recent_issue_types[-1]"
           description="이상 감지 — 동일 이슈 유형이 연속 2개 태스크에서 반복" />
  <skip condition="PENDING_TASKS == 0" description="완료된 태스크가 없으면 DAC 건너뜀" />
</dac-triggers>

### DAC 실행

트리거 조건 충족 시 DAC 모듈을 로드하여 실행한다:
Read("~/.claude/skills/chok-auto-agent/dac-module.md")
로드된 6-Phase 프로세스(A: 목표확정 → B: 궤적추출 → C: 드리프트스코어 → D: WebSearch검증 → E: 판정 → F: 조정)를 따라 실행하고 결과를 state.json에 저장한다.

판정 결과 라우팅:
- ALIGNED (>=8.0) → Step 1
- REORDER (5.5~8.0) → tasks.md 재순서 → Step 1
- CORRECT (3.0~5.5) → 교정 태스크 삽입 → Step 1
- REDESIGN (<3.0) → 태스크 재설계 → Step 2 재진입

---

## Context Management Protocol

Agent 격리 + 모델 라우팅 + 글로벌 제약: Read("~/.claude/skills/chok-auto-agent/agent-prompt-template.md")

**post-gstack 체크포인트**: Step 3 완료 후 조건부 ScheduleWakeup(60) — 상세는 Step 3 참조.

**이터레이션 간 리셋**: Step 7에서 ScheduleWakeup(60)으로 자동 리셋.

---

## Step 1: 태스크 결정

<task-selection>
  <source priority="1">state.json의 current_task (이전 세션에서 중단된 작업)</source>
  <source priority="2">docs/tasks.md의 첫 번째 `- [ ]` 항목</source>
  <format>- [ ] 태스크 설명  ← 선택 대상</format>
  <fallback>태스크 없음 → Step 7</fallback>
</task-selection>

**전제 조건 확인**: 태스크 선택 후, 선행 태스크 완료 여부·필요 파일 존재·의존 모듈 접근 가능 여부를 확인한다. 미충족 시 BLOCKED 마킹 → 다음 태스크로 이동.

### Step 1.5: 모호성 게이트 (Ambiguity Gate, Seed QA)

자율 루프에 underspecified 목표를 투입하면 drift·오작업이 누적된다. Step 2 진입 전, 선택된 태스크가 자율 실행 가능할 만큼 명세되었는지 게이트한다 (Ouroboros `ooo auto` ambiguity≤0.20 패턴 차용).

```xml
<ambiguity-gate threshold="0.20">
  <seed-qa>태스크가 (a) 검증 가능한 완료 기준(acceptance criteria), (b) 대상 파일/모듈 범위, (c) 성공 = 무엇인지를 갖추는가? 셋 다 충족 → ambiguity 낮음.</seed-qa>
  <score>ambiguity = 미충족 항목 수 / 3 (0.00 = 완전 명세, 0.33 = 1개 누락, ...)</score>
  <decision-logic>
    <rule>ambiguity ≤ 0.20 (전부 충족) → PASS, Step 2 진입</rule>
    <rule>ambiguity > 0.20 → bounded repair: 프로젝트 컨텍스트(코드·docs·이전 태스크)에서 누락분 자동 보강 시도, 최대 2회</rule>
    <rule>2회 보강 후에도 미충족 → 자율 진행 금지. 해당 태스크 BLOCKED 마킹 + tasks.md에 사유 기록 → 사용자 에스컬레이션 (defer-ambiguous: 모호한 목표는 사람 판단). 다음 태스크로 이동</rule>
  </decision-logic>
</ambiguity-gate>
```

DAC(Step 0c, 궤적 드리프트)와 역할 분리: DAC는 **누적 방향 이탈**을, 본 게이트는 **개별 태스크 진입 적격성**을 본다.

---

## Step 2: PM 착수 검토 — chok-supervisor

> **[Agent 격리]** chok-supervisor를 Agent() 도구로 실행한다. 부모 컨텍스트에는 VERDICT 요약만 수신한다.

```
Agent(
  subagent_type : "chok-supervisor",
  model         : "sonnet",
  prompt        : """
    태스크: {현재 태스크 설명}
    state 위치: ~/.gstack/chok-auto-agent/state.json

    이것은 구조화된 판정 작업이다. 간결하게 분석하고 VERDICT를 빠르게 도출하라.
    착수 검토(pre-review)를 실행하라. 범위 확인, 접근법 검토, 위험 식별.
    결과를 200자 이내로 요약하고 첫 줄에 다음 형식으로 출력:
    VERDICT: APPROVED | REVISE | REJECT
    REASON: (한 줄)
    RISKS: (핵심 위험 1–2개, 없으면 NONE)
  """
)
```

<decision-tree step="2" name="supervisor-pre">
  <verdict result="APPROVED"                   action="Step 3 진행" />
  <verdict result="REVISE"  max-retries="2"    action="피드백 반영 후 이 단계 재실행" />
  <verdict result="REJECT"                     action="BLOCKED 마킹 → 상태 저장 → Step 1 (다음 태스크)" />
</decision-tree>

state-schema.md 참조 — save: current_task, phase=supervisor_pre, session_start, completed_tasks, blocked_tasks

---

## Step 3: 실행 — gstack 또는 chok-dev-agents

> **[Agent 격리]** 실행기를 Agent() 도구로 실행한다. 빌드·테스트 로그가 가장 많은 컨텍스트를 생성하므로 격리가 필수다.

### 실행기 선택 (병렬 분해 가능 시 chok-dev-agents 위임)

```xml
<executor-selection>
  <rule condition="현재 task가 독립 subtask 2+ 로 분해 가능 (FE+BE, 다중 컴포넌트 등)"
        executor="chok-dev-agents" reason="병렬 fan-out 이득" />
  <rule condition="단일 파일/단순 변경" executor="gstack" reason="팀 오버헤드 회피 (기존 sequential 유지)" />
  <default executor="gstack" />
</executor-selection>
```

**chok-dev-agents 위임 시 (state 격리)**:

```
Agent(
  subagent_type : "chok-dev-agents",
  model         : "opus",
  prompt        : """
    목표: {현재 태스크 설명}
    mode: build-step
    ★ state 격리: 너의 run은 ~/.gstack/chok-dev-agents/{run_id}/state.json 사용.
       chok-auto-agent state.json(~/.gstack/chok-auto-agent/)는 건드리지 마라.
    완료 후 200자 요약 + run_id 반환. 첫 줄:
    VERDICT: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
    SUMMARY: (한 줄)
    RUN_ID: {timestamp}-{task_hash[:8]}
  """
)
```

chok-auto-agent는 반환된 요약 + run_id 참조만 자신의 state에 기록 (중첩 state 충돌 방지).

**gstack 실행 시 (기존 단순 경로)**:

```
Agent(
  subagent_type : "gstack",
  model         : "opus",
  prompt        : """
    태스크: {현재 태스크 설명}
    state 위치: ~/.gstack/chok-auto-agent/state.json

    태스크를 구현하라. 완료 후 결과를 200자 이내로 요약하고 첫 줄에 다음 형식으로 출력:
    VERDICT: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
    SUMMARY: (한 줄 — 무엇을 했는지)
    CONCERNS: (DONE_WITH_CONCERNS인 경우만 — 핵심 우려사항 1–2개, 없으면 NONE)
  """
)
```

<decision-tree step="3" name="gstack-run">
  <verdict result="DONE"               action="context-checkpoint 평가 → Step 4 진행" />
  <verdict result="DONE_WITH_CONCERNS" action="context-checkpoint 평가 → Step 4 진행 (concerns 포함하여 검증)" />
  <verdict result="BLOCKED"            action="Step 4 디버그 생략 → Step 5 (chok-fix 직행)" />
  <verdict result="NEEDS_CONTEXT"      action="Step 4 디버그 생략 → Step 5 (chok-fix 직행)" />
</decision-tree>

> **[Context Checkpoint]** `post-gstack` 체크포인트 조건을 평가한다.
> 조건 충족 시: `state.phase = "gstack_done"` 저장 → `ScheduleWakeup(60)` → Step 0 RESUME에서 Step 4 재개.
> 조건 미충족 시: 즉시 Step 4 진행.

state-schema.md 참조 — save: phase=gstack_running→gstack_done/debug_fix, gstack_outcome, gstack_summary

---

## Step 4: 검증 — chok-debug

> **[Agent 격리]** chok-debug를 Agent() 도구로 실행한다.

```
Agent(
  subagent_type : "chok-debug",
  model         : "sonnet",
  prompt        : """
    태스크: {현재 태스크 설명}
    gstack 결과 요약: {state.gstack_summary}
    state 위치: ~/.gstack/chok-auto-agent/state.json

    이것은 빠른 검증 작업이다. gstack 결과 요약을 기반으로 빌드/테스트 상태만 확인하라.
    전체 코드베이스 탐색 불필요. 결과 기반 판정에 집중.
    결과를 200자 이내로 요약하고 첫 줄에 다음 형식으로 출력:
    VERDICT: NO_ISSUES | ISSUES_FOUND
    ISSUES: (발견된 이슈 목록, 없으면 NONE)
    ISSUE_TYPE: (이슈 유형 분류 — architecture/logic/test/style, 없으면 NONE)
  """
)
```

<decision-tree step="4" name="debug">
  <verdict result="NO_ISSUES"    action="Step 5 진행" />
  <verdict result="ISSUES_FOUND" action="Step 4a (chok-fix) 실행" />
</decision-tree>

### Step 4a: 수정 — chok-fix

> **[Agent 격리]** chok-fix를 Agent() 도구로 실행한다.

```
Agent(
  subagent_type : "chok-fix",
  model         : "sonnet",
  prompt        : """
    태스크: {현재 태스크 설명}
    수정할 이슈: {chok-debug ISSUES 내용}
    state 위치: ~/.gstack/chok-auto-agent/state.json

    이것은 집중 수정 작업이다. 이슈 목록에 명시된 항목만 수정하라. 범위를 벗어난 개선 시도 금지.
    최대 3라운드. 결과를 200자 이내로 요약하고 첫 줄에 다음 형식으로 출력:
    VERDICT: FIXED | FAILED
    SUMMARY: (무엇을 수정했는지 한 줄)
  """
  max-rounds : 3
)
```

<decision-tree step="4a" name="fix">
  <verdict result="FIXED"  action="Step 4 재실행 (검증 재확인)" />
  <verdict result="FAILED" action="이슈 기록 후 Step 5 진행" />
</decision-tree>

state-schema.md 참조 — save: phase=debug_fix, debug_issues, fix_applied, recent_issue_types

---

## Step 5: 최종 검토 — chok-supervisor

> **[Agent 격리]** chok-supervisor를 Agent() 도구로 실행한다. 부모 컨텍스트에는 VERDICT 요약만 수신한다.

```
Agent(
  subagent_type : "chok-supervisor",
  model         : "sonnet",
  prompt        : """
    태스크: {현재 태스크 설명}
    gstack 결과: {state.gstack_summary}
    state 위치: ~/.gstack/chok-auto-agent/state.json

    이것은 최종 판정 작업이다. 마지막 커밋 diff만 검토하라. 전체 프로젝트 탐색 불필요.
    최종 검토(--strict)를 실행하라. 마지막 커밋 기준으로 높은 품질 기준 적용.
    VERDICT + SCORE를 빠르게 도출하라. 결과를 200자 이내로 요약하고 첫 줄에 다음 형식으로 출력:
    VERDICT: APPROVED | REVISE | REJECT
    SCORE: (0–30)
    REASON: (한 줄)
  """
)
```

<decision-tree step="5" name="supervisor-final">
  <verdict result="APPROVED" min-score="20"               action="Step 6 (커밋 & 완료)" />
  <verdict result="REVISE"   max-retries="2"              action="chok-fix 반영 후 이 단계 재실행" />
  <verdict result="REJECT"                                action="MANUAL_REQUIRED 태그 → 리포트 기록 → Step 1 (다음 태스크)" />
</decision-tree>

state-schema.md 참조 — save: phase=supervisor_final, supervisor_score, verdict, recent_verdicts

---

## Step 6: 완료 처리

```bash
# docs/tasks.md: "- [ ] 태스크명" → "- [x] 태스크명"
git add -A
git commit -m "feat: [chok-auto-agent] 태스크 완료: {태스크명}"
```

state-schema.md 참조 — save: current_task=null, phase=idle, completed_tasks(append), last_completed_at, dac_task_counter_since_check(+1)

---

## Step 6a: 회고 & 웹 검색 기반 개선

<retrospective>
  <web-search condition="dac_task_counter_since_check % 2 == 0 OR gstack_outcome == DONE_WITH_CONCERNS">
    <query>best practices for [구현한 기능/패턴] {current_year}</query>
    <query>[사용한 라이브러리] latest patterns performance</query>
  </web-search>
  <no-search-fallback>WebSearch 생략 — 로컬 코드 패턴과 CLAUDE.md 기준으로만 회고 실행.</no-search-fallback>

  <extract-checks>더 나은 패턴, 보안 취약점, 성능 개선 방법 확인</extract-checks>

  <improvement-routing>
    즉시 적용 가능 → 다음 태스크에 반영 / 스킬 개선 → docs/improvements.md / 컨벤션 변경 → CLAUDE.md 업데이트
  </improvement-routing>

  <learning-log>
    ~/.claude/skills/gstack/bin/gstack-learnings-log
      '{"skill":"chok-auto-agent","type":"operational","key":"TASK_KEY",
        "insight":"DESCRIPTION","confidence":4,"source":"observed"}'
  </learning-log>
</retrospective>

---

## Step 7: 루프 제어

<loop-control>
  <route condition="PENDING_TASKS > 0">
    ScheduleWakeup(delaySeconds=60, prompt="&lt;&lt;autonomous-loop-dynamic&gt;&gt;", reason="다음 태스크 실행")
  </route>
  <route condition="PENDING_TASKS == 0">
    최종 완료 리포트 출력 → ScheduleWakeup 호출 없이 루프 종료
  </route>
</loop-control>

완료 리포트: 완료/차단/재설계/재설계실패 태스크 수, DAC 실행 횟수+평균 점수, 총 소요 시간, 개선 건수를 표 형식으로 출력.

---

## 토큰 소진 처리

<token-exhaustion>
  <detection>
    <signal>Rate limit 에러 발생</signal>
    <signal>session_start 기준 4시간 이상 경과 (예방적)</signal>
    <signal>응답 급격히 저하 (컨텍스트 한계)</signal>
  </detection>

  <procedure>
    <step order="1">현재 state.json에 즉시 저장 (token_exhausted_at 포함)</step>
    <step order="2">
      재개 메시지 출력:
      "토큰 소진 감지. {wait_hours}시간 후 자동 재개.
       현재: {current_task} (phase: {phase})
       저장: ~/.gstack/chok-auto-agent/state.json"
    </step>
    <step order="3">
      ScheduleWakeup 체인 (최대 5회 × 3600s = 5시간):
        ScheduleWakeup(3600, "&lt;&lt;autonomous-loop-dynamic&gt;&gt;", "토큰 재충전 대기 N/5")
    </step>
    <step order="4">
      재시작 시 토큰 가용성 확인:
        ELAPSED = now - token_exhausted_at
        ELAPSED &lt; 18000s → 잔여 대기: ScheduleWakeup(min(3600, 18000-ELAPSED))
        ELAPSED ≥ 18000s → TOKEN_READY: Step 0 RESUME로 재개
    </step>
  </procedure>
</token-exhaustion>

---

## 상태 파일 스키마

`~/.gstack/chok-auto-agent/state.json` (v1.2).
상태 저장 시 필드 구조가 불확실하면 반드시 Read("~/.claude/skills/chok-auto-agent/state-schema.md")로 스키마를 확인하라.
핵심 필드: version, phase(idle|dac_in_progress|supervisor_pre|gstack_running|gstack_done|debug_fix|supervisor_final), current_task, gstack_summary, completed_tasks, blocked_tasks, dac_* 필드.

---

## No-Stop 원칙

<no-stop-rules>
  <rule>각 단계 완료 후 사용자에게 확인 요청하지 않는다</rule>
  <rule>감독관 REVISE 피드백은 자동으로 반영한다</rule>
  <rule>chok-fix 실패 시 MANUAL 태그 부착 후 다음 태스크로 진행한다</rule>
  <rule>방향 이탈 감지 시 자동으로 태스크를 재설계하고 개발을 이어간다. 루프를 중단하지 않는다</rule>
  <rule>REDESIGN 2회 실패 시 REDESIGN_FAILED 마킹 후 다음 태스크로 진행한다</rule>
  <rule>모든 결정은 자동으로 내린다. 최종 리포트에서 전체 결과를 한번에 보고한다</rule>
</no-stop-rules>

<escalation-triggers>
  <trigger>감독관 REJECT 2회 연속 (자동 처리 불가)</trigger>
  <trigger>보안 취약점 CRITICAL 등급 발견</trigger>
  <trigger>docs/tasks.md 파일 자체가 존재하지 않음</trigger>
</escalation-triggers>

---

## 파이프라인 흐름

Step0(Preamble) → Step0c(DAC, 조건부) → Step1(태스크 결정)
→ Step2(supervisor 착수검토, sonnet) → Step3(gstack 실행, opus) → [checkpoint]
→ Step4(debug 검증, sonnet) → [Step4a fix, sonnet] → Step5(supervisor 최종검토, sonnet)
→ Step6(커밋) → Step6a(회고) → Step7(루프/종료)
토큰 소진 시: 상태 저장 → ScheduleWakeup(3600) 체인 (최대 5회)

---

## Boundaries

<boundaries>
  <will>docs/tasks.md의 미완료 태스크를 자동으로 소진</will>
  <will>supervisor → gstack → debug/fix → supervisor 4단계 파이프라인 실행</will>
  <will>N개 태스크마다 전체 방향 정렬 자동 점검 (DAC)</will>
  <will>방향 이탈 감지 시 태스크를 자동 재분석하여 올바른 방향으로 재설계 후 개발 진행</will>
  <will>토큰 소진 시 상태 저장 + ScheduleWakeup 체인으로 자동 재개</will>
  <will>각 태스크 완료 후 웹 검색 기반 회고 및 스킬/문서 개선</will>
  <will>모든 결과를 최종 리포트에 종합</will>

  <wont>사용자에게 중간 확인 요청</wont>
  <wont>방향 이탈을 이유로 루프를 중단하거나 사용자에게 확인 요청</wont>
  <wont>실패한 태스크에서 무한 재시도</wont>
  <wont>보안 취약점 CRITICAL 이슈 자동 배포</wont>
  <wont>docs/tasks.md 없이 가상 태스크 생성</wont>
</boundaries>
