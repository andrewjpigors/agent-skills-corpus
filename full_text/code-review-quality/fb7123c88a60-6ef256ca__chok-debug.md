---
name: chok-debug
description: "Systematic debugging skill with root-cause-first methodology, multi-layer diagnostics, and automatic handoff to chok-verify/chok-fix pipeline."
origin: custom
triggers:
  keywords: [버그, 에러, 빌드 실패, 왜 안 되지, 스택 트레이스, TypeError, crash, fail]
  type: process
  model-hint: sonnet
---

# chok-debug — 체계적 디버깅 스킬

근본 원인 분석 → 가설 검증 → 수정 제안 → chok-fix 연동까지의 완전한 디버깅 파이프라인.

## Sources

| 통합 요소 | 원본 | 가져온 핵심 |
|-----------|------|------------|
| 4단계 디버깅 프로세스 | superpowers:systematic-debugging | Root Cause → Pattern → Hypothesis → Fix |
| Iron Law | superpowers:systematic-debugging | 근본 원인 없이 수정 금지 |
| 이슈 타입 분류 | sc:troubleshoot | bug/build/performance/deployment |
| 3회 실패 시 아키텍처 재검토 | superpowers:systematic-debugging | 무한 재시도 방지 |
| chok-fix 연동 | chok-fix | 수정 제안을 자동 전달 |
| chok-verify 연동 | chok-verify | 수정 후 검증 자동 실행 |
| E2E 단계별 분류 | `claudedocs/research_e2e_debug_deep_20260525_205822.md` | liveness → smoke → standard → agentic 7-tier 분류 |
| Recon-then-Action | Playwright Test Agents (MS+Anthropic) | accessibility tree 우선, 실패 시만 스크린샷 |
| PFS Flaky 트리아지 | Probabilistic Flakiness Score | flip+retry+예측불가성 단일 점수, ≥0.7 진짜 버그 (기본 가중치 w1=0.5/w2=0.3/w3=0.2 = chok-debug 자체 설정, `--pfs-weights` 옵션 override 가능) |
| Visual Regression | Argos CI / Playwright `toHaveScreenshot()` | UI 회귀 감지 (opt-in) |
| Production Verification | Dark Canary + Shadow Traffic | prod 1% 점진 롤아웃, 자동 실행 금지 |

## Usage

```
/chok-debug [issue] [--type bug|build|perf|deploy|test] [--trace] [--fix] [--unstuck]
```

### Options

| Option | 설명 | 기본값 |
|--------|------|--------|
| `issue` | 이슈 설명 또는 에러 메시지 | 필수 |
| `--type` | 이슈 유형 (자동 감지 가능) | `auto` |
| `--trace` | 데이터 흐름 역추적 활성화 | `false` |
| `--fix` | 디버깅 완료 후 chok-fix 자동 실행 | `false` |
| `--unstuck` | 가설 3회 실패 시 자동 chok-unstuck 트리거 (사용자 confirm 필수) | `false` |
| `--e2e` | E2E 검증 강제 활성화 (Phase 1.4 풀 커버 모드) | `auto` |
| `--visual-regression` | Argos / Playwright 시각 회귀 비교 (UI 이슈 자동 추천) | `false` |
| `--prod-verify` | Phase 1.9 Production Verification 가이드 출력 | `false` |
| `--screenshot-budget` | E2E 세션당 최대 스크린샷 수 (토큰 폭발 방지) | `3` |

### `--unstuck` 동작

가설 3회 실패 후 (Phase 3 hypothesis exhaustion) 자동 chok-unstuck 발동:

```xml
<unstuck-trigger-flow>
  <step n="1">Phase 3 가설 3회 실패 감지 (실패한 가설 목록 hypothesis_log 누적)</step>
  <step n="2">자동 실행 금지 — `AskUserQuestion` 확인 게이트:
    "가설 3회 실패. chok-unstuck (lateral-thinking 5-persona)로 다른 접근을 발산할까요?"
  </step>
  <step n="3">사용자 yes → chok-unstuck invoke (hypothesis_log를 failed_attempts로 전달)</step>
  <step n="4">chok-unstuck 결과의 selected option을 Phase 3 새 가설로 등록 + Phase 3 재실행</step>
  <step n="5">사용자 no → 표준 "3회 실패 → 아키텍처 재검토" 흐름 유지</step>
</unstuck-trigger-flow>
```

`--unstuck` 미지정 시: 표준 3-failure halt (기존 동작 유지). 명시 시에만 자동 unstuck 게이트 활성화.

## The Iron Law

```
근본 원인 조사 없이 수정을 시도하지 마라.
Phase 1을 완료하지 않았으면 수정을 제안할 수 없다.
```

### Karpathy Principles Alignment

Karpathy 원칙 참조: `Read("~/.claude/skills/shared/karpathy-principles.md")`

chok-debug의 Iron Law는 Karpathy P1(Think Before Coding)과 P3(Surgical Changes)에 이미 강하게 정렬되어 있다. 추가 적용:
- Phase 3 가설 수립 시 전제를 명시적으로 기술한다 (P1)
- Phase 4 수정 제안에서 최소 변경 원칙을 검증한다 (P2, P3)

## Phase 0: Pre-flight Check (디버깅 환경 준비)

**Phase 1 시작 전 반드시 실행.** 환경 미확인 상태로 디버깅하면 잘못된 전제로 시간 낭비.

- **Step 0.1 서버 실행 확인**: `curl -s http://localhost:3000/api/auth/session` — 응답 있음=실행 중 / Connection refused=사용자에게 서버 실행 요청 후 중단.
- **Step 0.2 인증 라이브러리 감지**: `package.json`에서 `next-auth`→NextAuth, `firebase/auth`→Firebase, `@supabase/supabase-js`→Supabase Grep.
- **Step 0.3 NextAuth — 테스트 경로 결정** (둘 다 보존):
  - **경로 A (curl 가능)**: `Grep("getToken", app/api OR pages/api)` → 후보 발견 시 `curl -s http://localhost:3000/api/debug/session` → 200+token이면 경로 A 확정 / 404·500이면 경로 B 폴백.
  - **경로 B (브라우저 탭 필수)**: `tabs_context_mcp`로 앱 탭 확인 → `javascript_tool`로 `fetch('/api/auth/session').then(r=>r.json())` → `{user:{...}}`면 로그인 확인 완료 / `{}`·null이면 로그인 요청 후 재개. 한계: curl 직접 호출 불가, 모든 API 테스트는 탭 내 fetch()로만.
- **Step 0.4 결과 기록**: 서버(RUNNING/STOPPED) · 인증(NextAuth/Firebase/Supabase/기타) · 테스트 경로(A debug endpoint / B 브라우저 fetch) · 브라우저 탭(있음/없음) · 로그인 상태(됨/안됨).

---

## Phase 1: Root Cause Investigation (근본 원인 조사)

**어떤 수정도 시도하기 전에 반드시 완료하라.**

- **Step 1.1 에러 메시지 정독**: 에러 메시지·스택 트레이스를 끝까지 읽고 파일:라인·에러 코드 기록, 경고도 무시 금지.
- **Step 1.2 재현 확인**: 일관 재현 가능한가? 정확한 단계는? 간헐적인가? 재현 불가 시 데이터 수집 강화·추측 금지.
- **Step 1.3 최근 변경 확인**: `git log --oneline -10`, `git diff HEAD~3 --stat`, `git diff HEAD~5 -- package.json pyproject.toml go.mod Cargo.toml`.

### Step 1.4: E2E 단계별 검증 — Tier SELECTION (제어 흐름)

**단위 테스트 통과 ≠ 실서버 동작 확인.** mock 기반 테스트는 실제 의존성(LLM, DB 드라이버, gRPC 등) 런타임 에러 미감지.

이슈를 분석해 권장 Tier(1-7)를 결정한다:

```
단순 5xx / NPE / 단일 엔드포인트 실패           → Tier 1-3 (smoke, 빠른 진단)
사용자 플로우 깨짐 / 다단계 인터랙션 / 인증 후 이상 → Tier 4 (Standard E2E)
AI 에이전트 디버깅 / multi-step trajectory 의심   → Tier 5 (Agentic E2E)
UI 깨짐 / 레이아웃 회귀 / 시각적 변경 의심         → Tier 6 (Visual Regression, --visual-regression)
배포 후 prod에서만 발생                          → Tier 7 (--prod-verify → Phase 1.9)
```

> **자동 Tier 선택 금지 규칙 (강제)**: 키워드 매핑은 휴리스틱이므로 100% 신뢰 불가. 아래 `AskUserQuestion` 게이트는 **항상 강제 실행**. `--e2e` 플래그가 명시된 경우에도 Tier 4 vs Tier 5 선택은 사용자 확인 필수.

> **AskUserQuestion 게이트 (필수)**: 분석 결과(이슈 타입 · 추천 Tier · 추천 이유 · 예상 시간 · 토큰 비용)를 출력하고 `AskUserQuestion`으로 확인하라 — "smoke (Tier 1-3) 빠른 진단 vs Standard E2E (Tier 4) 풀 커버 — 어느 쪽?"

Tier별 실행 절차(Tier 1-7 bash)·이슈→Tier 매핑 상세·AskUserQuestion 출력 포맷·smoke 필요성 사례·Multi-step Miss 방지(3층 검증)는 진입 직전 반드시 읽어라: `Read("~/.claude/skills/chok-debug/references/phase1-investigation.md")`.

### Step 1.5: 멀티레이어 진단 (--trace 모드)

각 컴포넌트 경계에서 in/out 데이터·설정 전파·레이어 상태를 로깅해 깨지는 지점을 증거로 특정한다. 상세 절차·예시는 실행 직전 읽어라: `Read("~/.claude/skills/chok-debug/references/phase1-investigation.md")`.

### Step 1.6: 브라우저 FE 디버깅 (프론트엔드 이슈 시)

코드만 보지 말고 브라우저에서 직접 확인한다. **Recon-then-Action 원칙 필수** (토큰 폭발 차단): accessibility tree(read_page) 우선 정찰 → 필요 시만 action → screenshot은 실패 시만(budget=3). Locator 우선순위 getByRole > getByLabel > getByText > getByTestId > CSS, `waitForTimeout` 고정 대기 금지. 시각/JS/네트워크/인터랙션/GIF 세부 절차(A~E)·screenshot_budget 예외는 진입 직전 읽어라: `Read("~/.claude/skills/chok-debug/references/phase1-investigation.md")`.

### Step 1.7: 데이터 흐름 역추적

에러가 콜스택 깊은 곳에서 발생할 때: 잘못된 값의 생성 지점·전달자를 원본 소스까지 역추적해 증상이 아닌 원인에서 수정한다. 역추적 상세 절차는 실행 직전 읽어라: `Read("~/.claude/skills/chok-debug/references/phase1-investigation.md")`.

### Step 1.8: Flaky 트리아지 (PFS Scoring) — 자동 핸드오프 규칙 (제어 흐름)

테스트 실패가 진짜 버그인가 환경 노이즈인가? 이진 pass/fail 대신 PFS로 분류한다. `PFS = w1*flip_rate + w2*retry_rate + w3*unpredictability` (기본 w1=0.5/w2=0.3/w3=0.2).

> **PFS≥0.7 자동 핸드오프 규칙 (제어 흐름)**:
> - `PFS ≥ 0.7` + 표본 ≥ 10 + Wilson CI 하한 ≥ 0.5 → **real_bug, chok-fix 자동 핸드오프** (`flaky_suspects[].severity="high"`).
> - `PFS ≥ 0.7` + 표본 < 10 또는 CI 하한 < 0.5 → "측정 부족" 경고, 사용자 확인 강제.
> - `PFS 0.2~0.7` → env_flake, chok-fix 핸드오프 보류(사용자 확인), `severity="medium"`.
> - `PFS < 0.2` → noise, 무시/재시도 정책만 조정, `severity="low"`.

측정 절차(최소 10회 실행 bash)·Wilson 95% CI 계산·False-positive 보호·`<flaky-analysis>` 출력은 실행 직전 읽어라: `Read("~/.claude/skills/chok-debug/references/phase1-investigation.md")`.

### Step 1.9: Production Verification (사용자 확인 필수)

**`--prod-verify` 플래그 시만 활성화.** 자동 실행 금지. `AskUserQuestion`으로 prod 1% 트래픽 노출 동의 후 **가이드만 출력**(실행은 사용자 수동). Dark Canary/Shadow Traffic 단계·안전 규칙·chok-fix downstream 처리(`manual_required`)는 활성화 시 읽어라: `Read("~/.claude/skills/chok-debug/references/phase1-investigation.md")`.

## Phase 2: Pattern Analysis (패턴 분석)

- **Step 2.1 작동하는 유사 코드 찾기**: 같은 코드베이스에서 비슷하게 작동하는 코드를 찾아 깨진 것과 차이를 파악.
- **Step 2.2 레퍼런스 대조**: 패턴 구현 시 레퍼런스를 모든 줄까지 완전히 읽고 이해한 후 적용 (대충 훑기 금지).
- **Step 2.3 차이점 식별**: 작동/깨진 것의 모든 차이를 나열, "이건 상관없을 거야" 가정 금지, 사소해도 목록 포함.

## Phase 3: Hypothesis & Testing (가설 검증)

- **Step 3.1 단일 가설 수립**: "원인은 [X]이다. 근거: [Y]" 형태로 명확히 기술 (예: "userId가 null인 상태에서 DB 쿼리 실행 — 근거: Step 1.4 Layer 3 진입 시 userId undefined 확인").
- **Step 3.2 최소 변경으로 테스트**: 가설을 테스트할 가장 작은 변경, 한 번에 하나의 변수만, 동시 수정 금지.
- **Step 3.3 결과 확인**: 성공 → Phase 4 / 실패 → 새 가설 수립 (같은 가설 재시도 금지).
- **Step 3.4 3회 실패 시 아키텍처 재검토**: 3회 이상 실패 시 STOP. 패턴/아키텍처가 근본적으로 올바른가·관성으로 계속하는가·리팩토링 필요한가 확인 후 사용자와 논의.

## Phase 4: Fix Proposal (수정 제안)

- **Step 4.1 실패 테스트 작성**: 버그를 재현하는 가장 간단한 테스트, 가능하면 프레임워크 사용, 실패(RED) 반드시 확인.
- **Step 4.2 수정 제안서 생성**: chok-fix로 전달할 구조화된 `<debug-session>` XML 출력.

> **MANDATORY**: Phase 4 출력 전 반드시 전체 스키마를 읽고 준수하라: `Read("~/.claude/skills/chok-debug/references/output-schema.md")`. 이 파일이 cross-skill 계약(chok-fix·chok-verify 파싱)의 source of truth다.

아래는 **compact 스켈레톤**이다. 실제 출력은 위 output-schema.md의 전체 스키마(모든 optional 필드 포함)를 따라야 한다.

```xml
<debug-session>
  <issue type="string" required="true">이슈 설명</issue>
  <type enum="bug|build|perf|deploy|test|flow|trajectory|visual" />
  <root-cause type="string">근본 원인 설명</root-cause>
  <evidence type="string[]"><item>증거 1</item></evidence>
  <hypothesis type="string">검증된 가설</hypothesis>

  <!-- 필수 블록 -->
  <fix-proposal>
    <files type="string[]" format="파일:라인">
      <file>파일1:라인</file>
    </files>
    <changes type="string">변경 내용 설명</changes>
    <severity enum="critical|high|medium|low" />
    <confidence enum="high|medium|low" />
  </fix-proposal>
  <regression-test type="string">테스트 파일 경로</regression-test>

  <!-- optional metadata 필드 (전체 구조는 output-schema.md 참조):
       e2e-tier, tier-execution, trajectory_evidence,
       intermediate_assertions, flaky_suspects, token_cost,
       visual_regression, prod_verification -->
</debug-session>
```

- **Step 4.3 chok-fix 연동 (--fix 모드)**:

```
/chok-debug "에러 설명" --fix
    ├─ Phase 1-3: 근본 원인 조사 + 가설 검증
    ├─ Phase 4: 수정 제안서 생성
    ├─ /chok-fix (Stage 2 Auto-fix → Stage 3 Root cause fix → Stage 5 Fix-Verify loop)
    └─ /chok-verify quick (최종 검증)
```

## Phase 4.5: User Root Cause Delivery (사용자 원인 전달)

**어떤 경우에도 생략 불가.** `--fix` 자동 실행 여부, 해결 성공/실패 여부와 무관하게 항상 실행.

### 전달 원칙

```
1. "무엇이 잘못됐는가"를 한 문장으로 먼저 말하라
2. 기술 용어보다 영향(impact) 중심으로 설명하라
3. 원인 → 영향 → 수정 → 재발 방지 4단 구조 유지
4. 증거(파일:라인)를 반드시 포함하라
5. 해결 못한 경우에도 "현재까지 파악한 원인"을 전달하라
```

### 출력 포맷

```markdown
## 문제 원인 요약

**한줄 요약**:
  {비기술적 언어로 한 문장 원인}

**상세 원인**:
  {기술적 근본 원인, 파일:라인 포함}

**영향 범위**:
  {어떤 기능/사용자에게 영향을 미쳤는가}

**수정 내용**:
  {무엇을 어떻게 고쳤는가}
  {미해결 시 → "현재 파악 범위와 한계"}

**재발 방지**:
  {같은 문제가 다시 생기지 않으려면}
```

작성된 출력 예시는 필요 시 읽어라: `Read("~/.claude/skills/chok-debug/references/issue-type-strategies.md")`.

---

## Issue Type별 디버깅 전략

Bug / Build / Performance / Deploy / Test 5개 타입별 단계별 전략은 이슈 타입 확정 시 읽어라: `Read("~/.claude/skills/chok-debug/references/issue-type-strategies.md")`. (같은 파일에 Phase 4.5 출력 예시·Debug Report 예시 포함.)

## Red Flags — 즉시 중단하고 Phase 1로 돌아가라

이런 생각이 들면 **프로세스를 위반**하고 있다:

| 위험 신호 | 해야 할 일 |
|-----------|-----------|
| "일단 이것만 바꿔보자" | STOP → Phase 1 |
| "아마 이거일 거야" | STOP → 증거 수집 |
| "빨리 고쳐야 해" | 체계적 디버깅이 더 빠르다 |
| "테스트는 나중에" | 테스트 먼저 작성 |
| "여러 개 한꺼번에 고치자" | 한 번에 하나만 |
| "레퍼런스 대충 봤어" | 전부 읽어라 |
| "한 번만 더 시도" (2회 실패 후) | 3회 규칙 확인 |
| "이건 간단한 문제야" | 간단한 버그에도 근본 원인이 있다 |

## Output Format

Debug Report 작성 시 포맷·예시는 읽어라: `Read("~/.claude/skills/chok-debug/references/issue-type-strategies.md")`. 리포트 헤더에는 Type · Duration · E2E Tier Used · Token Cost를 포함하고, Issue / Root Cause / Evidence / Flaky Analysis / Fix Proposal / Regression Test / Next 섹션을 채운다.

## Phase 5: Retrospective (회고)

디버깅 세션 종료 후 전체 과정을 종합 회고한다. **해결 성공/실패/아키텍처 재검토 모든 경우에 실행한다.**

회고 프로토콜: `Read("~/.claude/skills/shared/retrospective-protocol.md")`

### 이 스킬의 평가 관점

| 관점 | 평가 내용 | 만점 |
|------|----------|------|
| **Diagnostic Accuracy** | 근본 원인을 정확히 찾았는가? 가설 몇 번 만에 적중했는가? 오진이 있었는가? | /5 |
| **Process Fidelity** | Iron Law를 지켰는가? Phase 순서를 건너뛰지 않았는가? Red Flag 위반이 있었는가? | /5 |
| **Efficiency** | 가설 시도 횟수가 적절했는가? 불필요한 조사가 있었는가? | /5 |

### 고유 분석: 가설 히스토리

가설 적중률 = 최종 정답 가설 순번 / 총 시도 수. 첫 가설 정답 여부, 기각 가설의 정보 가치, 패턴 반복 여부, 아키텍처 재검토 진입 여부를 분석한다.

---

## 전체 파이프라인: chok-debug → chok-fix → chok-verify

```
문제 발견
    │
    ▼
/chok-debug "에러 설명" --type bug --fix
    │
    ├─ Phase 0: Pre-flight Check
    │   ├─ 서버 실행 확인
    │   ├─ 인증 라이브러리 감지
    │   └─ 테스트 경로 확정 (A: debug endpoint / B: 브라우저 fetch)
    │
    ├─ Phase 1: Root Cause Investigation
    │   ├─ 1.1~1.3: 에러 메시지/재현/최근 변경
    │   ├─ 1.4: E2E Tiered Check (Tier 1-7)
    │   │   └─ smoke vs full → AskUserQuestion
    │   ├─ 1.5: 멀티레이어 진단 (--trace)
    │   ├─ 1.6: 브라우저 FE 디버깅 (Recon-then-Action, budget=3)
    │   ├─ 1.7: 데이터 흐름 역추적
    │   ├─ 1.8: Flaky 트리아지 (PFS, ≥0.7 자동 → chok-fix)
    │   └─ 1.9: Production Verification (--prod-verify, 사용자 확인 필수)
    │
    ├─ Phase 2: Pattern Analysis
    │   ├─ 유사 작동 코드 찾기
    │   └─ 차이점 식별
    │
    ├─ Phase 3: Hypothesis Testing
    │   ├─ 가설 수립 + 최소 테스트
    │   └─ 3회 실패 → 아키텍처 재검토
    │
    ├─ Phase 4: Fix Proposal → XML 생성
    │
    ├─ Phase 4.5: User Root Cause Delivery ← 항상 실행
    │   └─ 한줄 요약 + 원인 + 영향 + 수정 + 재발 방지
    │
    ▼
/chok-fix (자동 호출)
    │
    ├─ Stage 1: Triage (수정 제안 분류)
    ├─ Stage 2: Auto-fix (format/lint)
    ├─ Stage 3: Root cause fix (에이전트 위임)
    └─ Stage 5: Fix-Verify loop
    │
    ▼
/chok-verify quick (자동 호출)
    │
    ├─ Build: PASS
    ├─ Types: PASS
    ├─ Tests: PASS
    └─ Overall: READY
    │
    ▼
문제 해결 완료
```

## Supervisor Integration (감독관 연동)

감독관 체크포인트 프로토콜: `Read("~/.claude/skills/shared/supervisor-checkpoint.md")`

### 이 스킬의 체크포인트

| 시점 | 검토 질문 |
|------|----------|
| Phase 1 완료 | "근본 원인 조사가 충분한가? 증거가 타당한가? 다른 가능성을 놓치고 있지 않은가?" |
| Phase 3 완료 | "가설이 증거에 기반하는가? 최소 변경 원칙을 지키는가? 다른 가설이 더 유력하지 않은가?" |
| Phase 4 완료 | "수정 제안이 근본 원인을 해결하는가? 회귀 위험은 없는가? 테스트가 충분한가?" |

### In-Loop Advisor (Anthropic advisor() tool)

근본 원인 확정(Phase 1) 직전 + 수정 제안(Phase 4) 직전에 네이티브 `advisor()` 툴을 호출한다. advisor()는 전체 transcript(조사 과정·증거·가설)를 자동 전달받는 in-loop 상위 모델 리뷰어 — 가설을 commit 하기 전 잘못된 root-cause 방향을 잡는다.

- **호출 시점:** 가설 확정 전(Phase 1 종료), 수정안 commit 전(Phase 4 종료)
- **사용 가능 시:** `advisor()` 툴 존재 시만. 없으면 skip (감독관 게이트로 폴백)
- **충돌 처리:** advisor가 다른 root-cause 지적 + 본인이 재현 증거 보유 → silent switch 금지, advisor() 재호출로 근거 대조

## Boundaries

**Will:**
- 근본 원인 조사를 수정 시도 전에 반드시 수행
- 멀티레이어 진단으로 실패 지점 정확히 특정
- 가설-검증 사이클로 과학적 디버깅
- 3회 실패 시 아키텍처 재검토 강제
- chok-fix/chok-verify와 연동하여 수정-검증 자동화
- 구조화된 수정 제안서(XML) 생성
- E2E 7-tier 분류로 smoke vs 풀 커버 자동 추천 + 사용자 확인
- Recon-then-Action으로 토큰 폭발 차단 (screenshot_budget=3)
- PFS ≥0.7 시 chok-fix 자동 핸드오프, 0.2-0.7은 사용자 확인
- Multi-step Miss 방지 (trajectory + intermediate assertions)
- Tier 6 (Visual Regression) UI 이슈 시 자동 추천, 사용자 확인 후 활성화

**Won't:**
- 근본 원인 없이 수정 시도 (추측 금지)
- 같은 방법 재시도 (새로운 가설 필수)
- 여러 수정을 동시에 적용 (한 번에 하나)
- 3회 이상 실패 후 추가 시도 (아키텍처 논의 필수)
- 테스트 없이 수정 완료 선언
- prod 명령 직접 실행 (Phase 1.9는 가이드 출력만, 실행은 사용자 수동)
- 사용자 확인 없이 시각 회귀/agentic E2E/prod 검증 활성화
- screenshot_budget 초과 시 무단 추가 캡처
- waitForTimeout 고정 대기 가이드 제공 (auto-wait/expect.poll만 사용)
