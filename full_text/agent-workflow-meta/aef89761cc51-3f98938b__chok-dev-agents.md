---
name: chok-dev-agents
description: "개발 팀 에이전트 구성 레이어. 하나의 목표를 독립 subtask로 분해하고 task shape 기반 coordination 패턴(Pipeline/Fan-out/Producer-Reviewer/Supervisor/Hierarchical)으로 팀을 가동한다. 신규 orchestrator/implementer/architect/docs 에이전트 + 기존 chok-supervisor(검토)/chok-verify(QA)/chok-check(보안)/chok-techreview/chok-unstuck 재사용. 병렬 fan-out + worktree 격리 + 예산 가드. 트리거: '개발 팀 만들어', '팀으로 구현', '병렬로 구현', 'chok-dev-agents'."
origin: custom
triggers:
  keywords: [팀, 병렬, 동시 구현, 여러 에이전트, 팀으로 만들어]
  type: execute
  model-hint: sonnet
---

# chok-dev-agents — 개발 팀 에이전트 구성 레이어

하나의 목표를 받아 **전문 에이전트 팀**을 구성하고 결과를 종합한다. 기존 chok-* 순차 파이프라인에 **병렬 팀 구성(fan-out)**을 더하는 메타 오케스트레이터.

## Sources

| 통합 요소 | 원본 | 가져온 핵심 |
|-----------|------|------------|
| orchestrator-worker + 병렬 fan-out | Anthropic multi-agent research system | 요약+아티팩트만 반환 (context 보존), +90.2% vs single |
| 6 coordination 패턴 | revfactory/harness | Pipeline/Fan-out/Expert Pool/Producer-Reviewer/Supervisor/Hierarchical |
| typed role (role/goal/backstory) | CrewAI | role 명세 명확화 (role confusion 방지) |
| supervisor 임계 | LangGraph | 6+ worker일 때만 hierarchical, 이하는 flat |
| 아티팩트 핸드오프 | gstack `~/.gstack/projects/` | 파일 기반 핸드오프 (transcript 아님) |
| 예산 가드 | Anthropic 15× cost finding | max 동시 3 + 반복 cap 3 |

## Usage

```
/chok-dev-agents <goal> [--max-agents N] [--max-rounds N] [--pattern auto|pipeline|fanout|producer-reviewer|supervisor] [--dry-run]
```

| Arg | 설명 | 기본값 |
|-----|------|--------|
| `goal` | 달성할 목표 (자연어) | 필수 |
| `--max-agents` | 최대 동시 subagent 수 (예산 가드) | `3` |
| `--max-rounds` | REVISE 재작업 최대 반복 | `3` |
| `--pattern` | coordination 패턴 강제 (auto = 결정 트리) | `auto` |
| `--dry-run` | 분해 + 패턴 선택만 출력, 실행 안 함 | `false` |
| `--workflow` | [PoC] Phase 3 fan-out을 네이티브 `Workflow parallel()`로 실행 (ultracode opt-in 동시 충족 필요, B1 검토) | `false` |

### Examples

```bash
# 단순 단일 task (핵심 4만, 병렬 안 함)
/chok-dev-agents "로그인 버튼 색상 변경"

# 병렬 fan-out (독립 subtask)
/chok-dev-agents "결제 모듈 Stripe 연동 + 환불 API + 결제 UI + 테스트"

# 복잡 설계 (architect 활성화)
/chok-dev-agents "마이크로서비스 3개 + API gateway 구축"

# 분해만 확인
/chok-dev-agents "전체 인증 리팩토링" --dry-run
```

## 팀 구성 (역할)

| 역할 | 신규/재사용 | agent 정의 | flow 위치 |
|------|-----------|-----------|----------|
| orchestrator | 신규 | `agents/chok-orchestrator.md` | Phase 0,1,7 |
| implementer | 신규 | `agents/chok-implementer.md` | Phase 3,5 |
| architect | 신규(선택) | `agents/chok-architect.md` | Phase 0 (복잡 시) |
| docs | 신규(선택) | `agents/chok-docs.md` | Phase 7 (공개 변경 시) |
| reviewer | 재사용 | chok-supervisor | Phase 4 |
| QA | 재사용 | chok-verify | Phase 6 |
| security | 재사용 | chok-check | Phase 6 (민감 시) |
| techreview | 재사용 | chok-techreview | Phase 2 |
| 막힘 해소 | 재사용 | chok-unstuck | Phase 4 (REJECT) |

> **정본**: 각 신규 역할의 정식 정의는 `agents/{name}.md` (install.sh가 ~/.claude/agents/로 복사). 아래 inline은 빠른 참조 요약 — 정본과 동기 유지.

### Inline Role 요약 (참조용, 정본은 agents/)

```xml
<roles>
  <role name="chok-orchestrator" ref="agents/chok-orchestrator.md" model="opus">
    분해 + 패턴선택 + 종합. transcript 안 읽음 (요약+아티팩트만).
  </role>
  <role name="chok-implementer" ref="agents/chok-implementer.md" model="sonnet">
    scoped task 외과적 구현. worktree 격리. chok-fix 모델 티어링.
  </role>
  <role name="chok-architect" ref="agents/chok-architect.md" model="opus" optional="true">
    컴포넌트 3+ 또는 다층 시스템 시. interface-contract 설계.
  </role>
  <role name="chok-docs" ref="agents/chok-docs.md" model="sonnet" optional="true">
    공개 API 변경 시. 문서 drift 0.
  </role>
</roles>
```

## 7-Phase Flow

### Phase 0: 목표 수신 + 분해 (orchestrator)

목표를 독립 subtask로 분해 + 의존성 그래프 생성.

```
목표 → [T1, T2, T3, ...] + depends_on 그래프
  · 동일 파일 수정 → 직렬 의존
  · 동일 디렉토리 5개+ 변경 → 직렬
  · 독립 → 병렬 가능
```

선택 역할 활성화 판단:
- architect: 신규 컴포넌트 3+ OR 다층 OR 명시 요청
- docs: 공개 API 변경 OR README/CHANGELOG 영향

### Phase 1: 패턴 선택 (결정 트리)

```xml
<pattern-decision-tree>
  <rule condition="subtask 간 의존성 있음" pattern="Pipeline" reason="순서 보장" />
  <rule condition="subtask 독립 + 3개 이하" pattern="Fan-out/Fan-in" reason="병렬+재조합" />
  <rule condition="생성물 품질 불확실" pattern="Producer-Reviewer" reason="생성-비평 분리" />
  <rule condition="scope 모호" pattern="Supervisor" reason="동적 라우팅" />
  <rule condition="worker 6+ AND 다층 도메인" pattern="Hierarchical" reason="LangGraph 임계 초과 시만" />
  <default pattern="Pipeline" reason="가장 단순 + 예측 가능 (Anthropic)" />
</pattern-decision-tree>
```

혼합 가능: `[T1 ∥ T3] → T2 → T4` (병렬 + 직렬 섞기).

### Phase 2: 기술검토 게이트 (선택)

신규 의존성 / 기술 선택 필요 시 → chok-techreview 위임. 4-lens 결과를 implementer 입력에 첨부.

### Phase 3: 병렬 Fan-out (독립 task)

**Pre-flight 안전 확인 (chok-auto Stage 6 로직 상속)**:

```bash
if [ -n "$(git status --porcelain)" ]; then
  echo "⚠ uncommitted 변경 → 병렬 비활성 (SERIAL_ONLY). commit/stash 권장"
  SERIAL_ONLY=true   # 전 task 직렬화 fallback
else
  SERIAL_ONLY=false
fi
```

병렬 가능 시 worktree 생성 + single message multiple Agent calls:

```
WORKTREE_BASE=".claude/worktrees/chok-dev-$(date +%s)"
for task in parallel_tasks (max --max-agents 동시):
  git worktree add -b "chok-dev-${task.id}" "$WORKTREE_BASE/${task.id}" HEAD

# 병렬 dispatch (single message, multiple Agent tool calls)
Agent(subagent_type: "chok-implementer", model: tier, prompt: T1 + worktree_path)
Agent(subagent_type: "chok-implementer", model: tier, prompt: T3 + worktree_path)
```

★ **Worktree 실행 계약 (절대경로 규율 — supervisor MF#1)**: subagent의 Bash cwd는 호출마다 리셋되므로 `cd`로 worktree에 고정 불가. 따라서:

```xml
<worktree-execution-contract>
  <rule>orchestrator가 각 implementer 프롬프트에 worktree 절대경로 `$WORKTREE_BASE/{task_id}` 전달</rule>
  <rule>implementer의 모든 Read/Edit/Write는 worktree 절대경로 prefix 사용 (상대경로 금지)</rule>
  <rule>implementer의 모든 Bash 명령은 `cd "$WORKTREE_PATH" && {cmd}` 형태로 self-prefix (cwd 의존 금지)</rule>
  <rule>worktree 미지원 환경(예: cwd 핸드오프 불가) → Phase 3 SERIAL_ONLY fallback (병렬 포기)</rule>
</worktree-execution-contract>
```

각 subagent: scoped tools + 모델 티어링 + `~/.gstack/chok-dev-agents/{run_id}/{task_id}.md` 아티팩트 기록. 반환: 200자 요약 + 아티팩트 경로 (transcript 아님).

#### [PoC] 네이티브 `Workflow` parallel() 경로 (opt-in, B1 검토)

> **실험적.** Dynamic Workflows가 research preview라 기본 OFF. `--workflow` 플래그 + 사용자 ultracode opt-in 동시 충족 시만 활성. 미충족 시 위 수제 Agent() 방식이 정본.

기존 수제 fan-out 대비 이득: journaled resume(중단 후 캐시 재개), `isolation:'worktree'` 네이티브(수제 `git worktree add` 계약 불필요), `budget.remaining()` 가드.

```js
// Phase 3 단일 단계만 교체 (Phase 4 reviewer 게이트는 기존 유지)
const results = await parallel(
  parallel_tasks.map(t => () =>
    agent(t.prompt, {
      label: `impl:${t.id}`,
      phase: 'Fan-out',
      isolation: 'worktree',        // 수제 worktree-execution-contract 대체
      agentType: 'chok-implementer',
      model: t.tier
    })
  )
)  // barrier: 전 task 완료 후 Phase 4로
const artifacts = results.filter(Boolean)  // skip된 agent 제거
```

**A/B 비교 측정 항목** (PoC 평가 기준):

| 지표 | 수제 Agent() | Workflow parallel() |
|------|-------------|---------------------|
| wall-clock (동일 N task) | baseline | 측정 |
| 중단 후 재개 가능 | ✗ (수동 재실행) | ✓ (resumeFromRunId) |
| worktree 계약 코드량 | ~6 rule | 0 (isolation 내장) |
| token (orchestration overhead) | baseline | 측정 |

> **제약:** `workflow()` 중첩 1-level만 → Hierarchical 패턴(에이전트가 다시 팀 구성)은 이 경로로 매핑 불가, 수제 방식 유지. opt-in 정책(ultracode 수신 방법)은 GA 전환 시 재확정.

### Phase 4: Reviewer 게이트 (필수, 각 산출물)

```xml
<reviewer-gate>
  <invoke>chok-supervisor --consensus</invoke>
  <verdict-routing>
    <APPROVED>다음 단계</APPROVED>
    <REVISE max-rounds="3">
      동일 worktree 재사용 (누적 컨텍스트) + supervisor 피드백을 implementer 입력에 첨부.
      3회 초과 → REJECT로 승격.
    </REVISE>
    <REJECT>
      chok-unstuck 발동. ★ chok-unstuck user-gate 필수 surfacing:
      자율 flow라도 AskUserQuestion confirm (no-stop 예외).
      사용자 거부 → MANUAL_REQUIRED 태그 에스컬레이션.
    </REJECT>
  </verdict-routing>
</reviewer-gate>
```

### Phase 5: 직렬 Pipeline (의존 task)

의존 task를 순서대로 실행 (선행 task 머지 후). Merge 전 `git diff --name-only`로 충돌 사전 검출 → 충돌 시 자동 직렬 재실행 (chok-auto Stage 6 로직).

### Phase 6: QA 게이트 (전체 통합 후)

```xml
<qa-gate>
  <invoke>chok-verify pre-pr</invoke>  <!-- 빌드/타입/린트/테스트/E2E/보안 -->
  <drift-check contract="chok-verify Phase 11.5">
    drift_score > 0.3 → chok-supervisor escalation (자기 재조정 아님)
    goal source 없음 → AskUserQuestion, 거부 시 abort
  </drift-check>
  <security condition="민감 영역">chok-check 추가 위임 (OWASP 5-lens)</security>
</qa-gate>
```

### Phase 7: 종합 + 회고 (orchestrator)

- 모든 아티팩트 읽고 종합 리포트 (transcript 아님)
- docs 활성화 시 → chok-docs 문서 동기화
- retrospective-protocol 3차원 회고
- chok-trendsync에 결과 기록 (튜닝, 선택)

## 핸드오프 계약

```xml
<handoff-contract>
  <subagent-returns>
    <summary max-chars="200" />
    <verdict>PASS|FAIL|BLOCKED</verdict>
    <artifact-path>~/.gstack/chok-dev-agents/{run_id}/{task_id}.md</artifact-path>
  </subagent-returns>
  <orchestrator-reads>아티팩트 파일만 (transcript 읽기 금지 = context pollution 방지)</orchestrator-reads>
  <state>~/.gstack/chok-dev-agents/{run_id}/state.json (run_id = {timestamp}-{task_hash[:8]})</state>
</handoff-contract>
```

## 예산 가드 (15× 비용 방지)

```xml
<budget-guard>
  <max-concurrent-agents default="3" enforcing="true" />
  <max-rounds default="3" enforcing="true" />
  <value-gate>단순 task (단일 파일/단일 컴포넌트) → 단일 에이전트 fallback (팀 미동원)</value-gate>

  <!-- supervisor MF#3: advisory → enforcing 비용 게이트 -->
  <pre-flight-cost-estimate>
    추정 비용 배수 = (활성 에이전트 수) × (예상 평균 라운드) × (모델 가중치: opus=3, sonnet=1, haiku=0.3)
    예: implementer(opus) 3 동시 × 2 라운드 = 3 × 2 × 3 = 18× 기준 단위
  </pre-flight-cost-estimate>
  <hard-gate>
    추정 배수 > 10× → 실행 전 `AskUserQuestion` 필수:
      "예상 비용 ~{N}× (단일 챗 대비). 진행 / 에이전트 수 축소 / 단일 에이전트 fallback?"
    추정 배수 ≤ 10× → 경고만 출력하고 진행
  </hard-gate>
  <cost-warning>multi-agent ~15× 단일 챗 (Anthropic finding) → 고가치 작업만</cost-warning>
</budget-guard>
```

## chok-auto-agent 통합

```xml
<integration>
  <standalone>/chok-dev-agents "목표" — 단일 목표 팀 spawn 후 종료</standalone>
  <as-build-step>
    chok-auto-agent Step 3에서 gstack 대신 위임 (병렬 분해 가능한 task일 때만).
    단순 task는 기존 sequential 유지.
  </as-build-step>
  <state-isolation>
    chok-auto-agent: ~/.gstack/chok-auto-agent/state.json (loop)
    chok-dev-agents: ~/.gstack/chok-dev-agents/{run_id}/state.json (run 격리)
    chok-auto-agent는 chok-dev-agents 반환 요약 + run_id 참조만 기록.
  </state-isolation>
</integration>
```

## Boundaries

**Will:**
- 목표 분해 + 패턴 선택 + 병렬 fan-out + 종합
- 신규 역할(orchestrator/implementer/architect/docs) + 기존 스킬 게이트 재사용
- 아티팩트 기반 핸드오프 (context 보존)
- 예산 가드 (max 동시/반복)

**Won't:**
- task-loop (docs/tasks.md 소진) — chok-auto-agent 책임
- transcript 직접 읽기 (요약+아티팩트만)
- 단순 task에 팀 과동원 (단일 에이전트 fallback)
- 사용자 확인 없이 chok-unstuck 자동 적용 (user-gate 필수)

## Retrospective (Phase 7)

3-Dimension 평가:

| 관점 | 평가 내용 |
|------|----------|
| Decomposition Quality | subtask 분해가 적절했나? 과분해/미분해 없었나? |
| Pattern Fit | 선택한 coordination 패턴이 task shape에 맞았나? |
| Team Efficiency | 병렬화로 실제 시간/비용 이득? 예산 가드 적절했나? |

저장: `[PATTERN]` 자주 맞는 패턴-task 매칭, `[GOTCHA]` 잘못된 분해/병렬화 사례.
