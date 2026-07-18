---
name: chok-supervisor
description: "Standalone supervisor skill for on-demand critical review. Implements Anthropic's Evaluator-Optimizer pattern with separated evaluation, 6-dimension scoring (30pts), severity-driven feedback, and multi-layer verification."
origin: custom
triggers:
  keywords: [검토, 리뷰, 코드 품질, 채점, 감독]
  type: verify
  model-hint: sonnet
---

# chok-supervisor — 독립 감독관 스킬

작업 결과물을 비판적으로 검토하고 구체적 피드백을 제공한다.
chok-* 파이프라인 내부 자동 호출 외에, 사용자가 직접 호출할 수 있는 스킬.

## Usage

```
/chok-supervisor [target] [--scope file|module|feature] [--strict] [--consensus]
```

| Arg | 설명 | 기본값 |
|-----|------|--------|
| `target` | 검토 대상 (파일, 디렉토리, "last-commit", 또는 설명) | `git diff` (미커밋 변경) |
| `--scope` | 검토 범위 | `file` |
| `--strict` | 점수 기준 강화 (APPROVED 최소 27점) | `false` |
| `--consensus` | Multi-model 합의 모드 (Codex CLI read-only 호출 + 3-section 출력) | `false` |

### Examples

```bash
# 미커밋 변경사항 전체 검토
/chok-supervisor

# 특정 파일 검토
/chok-supervisor src/auth.ts

# 마지막 커밋 검토
/chok-supervisor last-commit

# 모듈 단위 엄격 검토
/chok-supervisor src/features/chat --scope module --strict

# 작업 설명으로 검토 요청
/chok-supervisor "방금 구현한 인증 미들웨어 검토해줘"
```

## Execution Procedure

### Step 1: 검토 대상 결정

```
target 파싱:
  ├─ 파일/디렉토리 경로 → 해당 파일 읽기
  ├─ "last-commit" → git diff HEAD~1 + git show HEAD
  ├─ 텍스트 설명 → 관련 파일 자동 탐색 (Grep/Glob)
  └─ 빈 입력 → git diff (미커밋 변경)
```

### Step 2: 컨텍스트 수집

```
1. CLAUDE.md, .claude/rules/ 읽기 (프로젝트 규칙)
2. 변경 파일 주변의 기존 코드 패턴 확인
3. 관련 테스트 파일 존재 여부 확인
4. git log --oneline -5 (최근 변경 흐름)
```

### Step 2.5: Karpathy Principles Context

Karpathy 코딩 원칙 로드: `Read("~/.claude/skills/shared/karpathy-principles.md")`

검토 시 4가지 원칙 준수 여부를 기존 6개 차원의 sub-criteria로 평가한다 (별도 차원 추가 아님 — 점수에 가산되지 않음). self-retro 출력의 `[KARPATHY ALIGNMENT]` 박스는 이 sub-criteria의 OK/WARN roll-up이며 7번째 채점 차원이 아니다.

### Step 3: chok-supervisor 에이전트 호출

```
Agent(
  subagent_type: "chok-supervisor",
  prompt: "다음 작업 결과물을 검토하라:
    - 검토 대상: {target_summary}
    - 변경 내용: {diff_or_content}
    - 프로젝트 규칙: {claude_md_rules}
    - 기존 패턴: {existing_patterns}
    6가지 관점으로 채점하고 판정하라."
)
```

### Step 3.5: Multi-Model Consensus (`--consensus` 모드 시)

`--consensus` 플래그가 명시된 경우, Codex CLI(`codex review`)를 read-only sandbox로 추가 호출하여 다중 모델 합의를 산출한다. 단일 모델 편향(blind spot)을 제거.

> **추가 합의원 — Anthropic `advisor()` 툴:** 환경에 네이티브 `advisor()` 툴이 있으면 Codex와 **병렬 합의원**으로 사용한다. advisor()는 전체 transcript를 자동 전달받는 in-loop 상위 모델 리뷰어로, 최종 verdict 직전 호출한다. Codex(외부 sandbox 리뷰) + advisor(in-loop transcript 리뷰)는 상호 보완적 — 둘 다 가능하면 둘 다, advisor만 가능하면 advisor 단독으로 다중 합의 달성. 둘 다 없으면 단독 verdict (degraded mode).

**선결 조건 확인**:

```bash
# Codex CLI 존재 확인 (graceful fallback)
if /usr/bin/which codex >/dev/null 2>&1; then
  CODEX_AVAILABLE=true
else
  CODEX_AVAILABLE=false
  # 사용자에게 알림 후 단독 verdict로 진행 (degraded mode)
fi
```

**호출 형태** (Codex 사용 가능 시):

```bash
# read-only: code 수정 권한 없이 review만 (sandbox flag 필수)
# 90초 timeout: hang 방지 (degraded mode로 자동 폴백)
timeout 90s codex review \
  --sandbox read-only \
  --target "$TARGET_PATH_OR_DIFF" \
  --output-format json \
  > /tmp/codex-review-$$.json 2>/dev/null
CODEX_EXIT=$?
case $CODEX_EXIT in
  0)   CODEX_RESULT="ok" ;;
  124) CODEX_RESULT="timeout" ;;       # timeout(1) returns 124 on SIGTERM
  *)   CODEX_RESULT="failed" ;;
esac
```

**Verdict 정규화 + 병합 알고리즘**:

```xml
<consensus-merge>
  <step n="1">각 reviewer verdict를 정수 매핑: APPROVED=3, REVISE=2, REJECT=1</step>
  <step n="2">최종 verdict = max(stricter) 채택 — 의견 불일치 시 더 엄격한 쪽 우선 (안전성 편향)</step>
  <step n="3">divergence_score = (max - min) / 2 산출
    - 0.0 = 완전 합의 (모두 같은 verdict)
    - 0.5 = 한 단계 차이 (예: APPROVED vs REVISE)
    - 1.0 = 양극단 차이 (APPROVED vs REJECT)
  </step>
  <step n="4">divergence_score ≥ 0.5 시 사용자 게이트 강제 (`AskUserQuestion`) — 의견 양극단 → 사람 판단 필요</step>
  <step n="5">3-section 출력: <consensus>, <divergence>, <chok-supervisor-verdict></step>
  <step n="6">autopilot 적용 여부는 6-gate autopilot rubric으로 별도 판정 (consensus 결과와 독립)</step>
</consensus-merge>
```

**6-gate autopilot 자동결정 rubric** (gstack `autoplan` 패턴 차용):

```xml
<autopilot-rubric>
  <principle name="completeness">issue가 모든 영향 파일을 cover하는가? unhandled 케이스 없는가?</principle>
  <principle name="pattern-match">기존 코드 패턴과 일치하는가? 새 패턴 도입은 정당화 가능한가?</principle>
  <principle name="reversibility">변경이 가역적인가? (lint/format/comment-only OK / DB migration / schema change FAIL)</principle>
  <principle name="prior-user-choice">사용자가 이미 비슷한 선택을 한 적 있는가? memory/feedback에 일관 패턴 있는가?</principle>
  <principle name="defer-ambiguous">모호한 부분은 사용자에게 위임 (자동 결정 보류)</principle>
  <principle name="escalate-security">보안 영향 있으면 무조건 사용자 게이트</principle>

  <decision-logic>
    <rule>6 원칙 모두 PASS + divergence_score &lt; 0.5 → autopilot_allowed = true</rule>
    <rule>1개 이상 FAIL OR divergence_score ≥ 0.5 → autopilot_allowed = false (사용자 게이트)</rule>
    <rule>escalate-security가 trigger되면 다른 원칙 무관하게 사용자 게이트 강제</rule>
  </decision-logic>
</autopilot-rubric>
```

**Degraded mode (Codex 미설치/실패 시)**:

```xml
<degraded-mode>
  <reviewer-priority>codex 부재 시에도 native `advisor()` 툴이 있으면 1차 in-loop 합의원으로 사용 — 완전 단독(solo) verdict는 codex AND advisor 둘 다 없을 때만.</reviewer-priority>
  <output>
    degraded_mode=true
    fallback_reason="codex not installed | codex execution failed | codex timeout"
    consensus_source="advisor() in-loop" (advisor 가능 시) | "solo" (둘 다 없을 때)
    final_verdict={advisor 합의 반영 verdict | chok-supervisor 단독 verdict}
    divergence_score={advisor 사용 시 산출 | null}
    autopilot_allowed=verdict 기반 6-gate autopilot 판정
  </output>
  <user-message>
    "⚠ Codex CLI 없음 → advisor() in-loop 리뷰어로 합의 진행 (advisor도 없으면 단독 verdict).
     Codex 다중 모델 합의를 원하시면: brew install codex / pipx install codex-cli 설치,
     또는 --consensus 플래그 제거하고 단독 모드 사용."
  </user-message>
</degraded-mode>
```

### Step 4: 결과 출력

감독관 에이전트의 리포트를 사용자에게 표시한다.

**`--consensus` 모드 4-필드 출력 형식**:

```xml
<consensus-output>
  <consensus_verdict>{normalized verdict — max of all reviewers}</consensus_verdict>
  <divergence>
    <chok_supervisor verdict="APPROVED" score="27/30">{evidence list}</chok_supervisor>
    <codex verdict="REVISE" score="N/A">{codex's findings}</codex>
    <divergence_score>0.5</divergence_score>
  </divergence>
  <autopilot_decisions>
    <principle name="completeness" pass="true" />
    <principle name="pattern-match" pass="true" />
    <principle name="reversibility" pass="true" />
    <principle name="prior-user-choice" pass="true" />
    <principle name="defer-ambiguous" pass="true" />
    <principle name="escalate-security" pass="true" />
    <allowed>true</allowed>
  </autopilot_decisions>
  <escalations>
    <user_gate required="false" reason="divergence_score &lt; 0.5 AND all principles pass" />
    <!-- OR if required=true: -->
    <!-- <user_gate required="true" reason="divergence_score=0.5: chok-supervisor APPROVED but Codex REVISE — 의견 불일치, 사람 판단 필요" /> -->
  </escalations>
</consensus-output>
```

## Input Schema (chok-debug / chok-fix 핸드오프)

chok-supervisor가 다른 chok-* 스킬에서 호출될 때, 입력 컨텍스트에 다음 8 XML 필드가 포함될 수 있다. 각 필드는 **silent-drop 금지** — 미인식 필드라도 schema_validation_error 로깅 후 진행.

```xml
<chok-supervisor-input-schema source="cross-skill" optional="true">
  <!-- chok-debug Phase 4 XML fields (cross-skill propagation) -->
  <e2e-tier value="1-7" recommendation="smoke|standard|agentic|visual|prod" />
  <tier-execution>
    <tier_executed type="csv-int" />
    <tier_skipped reason="string" />
    <user_confirmed type="boolean" />
  </tier-execution>
  <trajectory_evidence>
    <url_sequence type="array" />
    <interaction_sequence type="array" />
  </trajectory_evidence>
  <intermediate_assertions type="array" />
  <flaky-analysis>
    <pfs type="float" min="0" max="1" />
    <classification enum="real_bug|env_flake|noise|insufficient_data" />
    <wilson_ci_lower type="float" />
    <sample_size type="integer" />
  </flaky-analysis>
  <visual-regression enum="enabled|disabled|tier_fallback" baseline="string" />
  <prod_verification execution="manual_only" />
  <test_as_bug_assessment>
    <verdict enum="code_bug|test_bug|inconclusive" />
    <evidence type="array" />
    <asks_user type="boolean" />
  </test_as_bug_assessment>
</chok-supervisor-input-schema>
```

**활용**: 검토 대상 평가 시 위 필드를 6차원 점수 계산의 evidence로 사용:
- `flaky-analysis.classification=test_bug` → Direction 점수에서 "테스트 자체 오류 인지 여부" 가산
- `prod_verification.execution=manual_only` → Regression 점수에서 "prod 자동 변경 금지 준수" 가산
- `trajectory_evidence` 미비 (Tier ≥ 4인데 비어있음) → Correctness 점수 감산

**미인식 필드 처리**:

```
For each XML field in input not matching schema:
  log: "[schema_validation_error] Unknown field '{name}' in chok-supervisor input. Continuing with known fields only."
  → 처리 계속 (silent drop 안 함, 에러 로깅만)
```

## 6-Dimension Scoring (에이전트 정의 참조)

```xml
<scoring-dimensions total-max="30">
  <dimension name="Direction" max="5">
    <evaluates>요구사항 일치, scope creep</evaluates>
    <sub-criterion name="karpathy-P1">전제가 명시적으로 기술되었는가? 대안이 제시되었는가?</sub-criterion>
  </dimension>
  <dimension name="Correctness" max="5">
    <evaluates>로직 결함, 엣지 케이스</evaluates>
  </dimension>
  <dimension name="Quality" max="5">
    <evaluates>컨벤션, 보안, 성능, 테스트</evaluates>
    <sub-criterion name="karpathy-P2">최소 코드 원칙 준수 — 불필요한 추상화/기능 없는가?</sub-criterion>
  </dimension>
  <dimension name="Architecture" max="5">
    <evaluates>패턴 일관성, 의존성</evaluates>
  </dimension>
  <dimension name="Completeness" max="5">
    <evaluates>요구사항 커버리지, 에러 처리</evaluates>
    <sub-criterion name="karpathy-P4">성공 기준이 정의되고 검증되었는가?</sub-criterion>
  </dimension>
  <dimension name="Regression" max="5">
    <evaluates>부작용, 파급 효과</evaluates>
    <sub-criterion name="karpathy-P3">변경 범위가 요청에 한정되는가? 인접 코드 불필요 수정 없는가?</sub-criterion>
  </dimension>
</scoring-dimensions>
```

### 판정 기준

**Severity 정의 (앵커)** — 판정은 점수(score) × severity 2-요인 함수다:
- **must-fix**: 배포 차단 / 계약 위반 / 회귀 / 로직 결함. 반드시 수정.
- **should-fix**: 품질·가독성·유지보수 권고. 다수면 누적 위험.
- **could-fix**: 선택적 개선. 단독으로는 verdict에 영향 없음.

**판정 함수 (소진적·비겹침)** — 모든 (score, must-fix, should-fix) 조합이 정확히 하나의 verdict로 해소된다:

```xml
<judgment-criteria note="아래를 위에서 아래로 평가, 첫 매칭 채택">
  <verdict result="REJECT" when="score 0-14" action="사용자 에스컬레이션" />
  <verdict result="REVISE" when="must-fix ≥ 1" reason="must-fix는 점수 무관 차단 (score 0-14이면 위 REJECT 우선)" />
  <verdict result="REVISE" when="should-fix ≥ 3" reason="should-fix 다수는 score ≥20이어도 REVISE로 cap" />
  <verdict result="APPROVED" when="score 25-30, must-fix=0, should-fix≤2" />
  <verdict result="APPROVED" when="score 20-24, must-fix=0, should-fix≤2" note="should/could-fix는 suggestions로 첨부" />
  <verdict result="REVISE" when="score 15-19, must-fix=0" reason="fall-through 구멍 폐쇄 — 낮은 점수는 must-fix 없어도 REVISE" />
</judgment-criteria>
```

**Worked examples (회귀 lock)**:

| score | must | should | → verdict | 근거 |
|-------|------|--------|-----------|------|
| 28 | 0 | 1 | APPROVED | 높은 점수, 이슈 경미 |
| 22 | 0 | 1 | APPROVED | suggestions 첨부 |
| 22 | 0 | 4 | REVISE | should-fix 다수 cap |
| 22 | 1 | 0 | REVISE | must-fix 차단 |
| 16 | 0 | 0 | REVISE | 점수 15-19 (구멍 폐쇄) |
| 12 | * | * | REJECT | 점수 0-14 |

## Integration with chok-* Pipeline

이 스킬은 독립 호출용이다. 파이프라인 내부 자동 호출은 각 chok 스킬의 "Supervisor Integration" 섹션에 정의되어 있다:

- **chok-auto**: Stage 1, 3, 5, 6, 8 완료 후 자동 호출 + Stage 10 회고 검토
- **chok-debug**: Phase 1, 3, 4 완료 후 자동 호출 + Phase 5 회고 검토
- **chok-fix**: Stage 1, 3, 5 완료 후 자동 호출 + Stage 6 회고 검토
- **chok-verify**: 전체 검증 완료 후 메타 검토 + Phase 11 회고 검토
- **chok-harness**: Step 3, 4, --fix 후 자동 호출 + Step 8 회고 검토

## Self-Retrospective (자기 회고)

감독관 자신의 평가 품질을 메타 회고한다. **다른 chok 스킬의 회고 단계 검토 시에도 이 섹션이 적용된다.**

> 출처: Anthropic Evaluator-Optimizer (separated evaluation anti-leniency), Multi-Agent Debate (adversarial verification), Datagrid Tip #6 (reflection-safe architecture with rotating reward models)

### 자기 회고 트리거

```markdown
다음 조건에서 자기 회고를 실행한다:
  1. 세션 내에서 3회 이상 APPROVED를 연속 판정했을 때 (관대함 편향 의심)
  2. REVISE 후 재검토에서 같은 이슈가 반복될 때 (피드백 품질 의심)
  3. 사용자가 감독관 판정을 뒤집었을 때 (판정 정확도 문제)
  4. 독립 호출(/chok-supervisor) 완료 시 (항상)
```

### 3-Dimension 자기 평가

```xml
<self-evaluation-dimensions total-max="15">
  <dimension name="Judgment Accuracy" max="5">
    <evaluates>판정이 정확했는가? 사용자가 뒤집은 판정이 있는가? 증거 없이 판정하지 않았는가?</evaluates>
  </dimension>
  <dimension name="Leniency Balance" max="5">
    <evaluates>관대함 편향(항상 APPROVED)이 있는가? 과잉 엄격(불필요한 REVISE)이 있는가? APPROVED:REVISE 비율이 적절한가?</evaluates>
  </dimension>
  <dimension name="Feedback Quality" max="5">
    <evaluates>REVISE 시 피드백이 구체적이었는가? 작업 에이전트가 피드백만으로 수정할 수 있었는가? 파일:라인 증거가 포함되었는가?</evaluates>
  </dimension>
</self-evaluation-dimensions>
```

### 관대함 편향 감지 (Leniency Bias Detection)

```markdown
경고 신호:
  - 연속 APPROVED 3회+ → "자동 승인 모드에 빠지지 않았는가?"
  - REVISE 비율 < 10% → "모든 산출물이 정말 그렇게 좋았는가?"
  - must-fix 이슈 0건 연속 5회+ → "기준이 너무 낮지 않은가?"

교정 행동:
  - 다음 검토에서 의도적으로 더 엄격한 기준 적용
  - 가장 최근 APPROVED 3건 중 1건을 무작위 재검토
  - "이 코드를 내가 직접 작성했다면 이 품질에 만족하겠는가?" 자문
```

### 회고 결과 활용

```markdown
자기 회고 결과는 다른 chok 스킬의 회고에 통합된다:

chok-auto Stage 10 → 감독관 자기 회고 포함:
  "이 파이프라인에서 감독관 개입이 적절했는가?"

chok-debug Phase 5 → 감독관 자기 회고 포함:
  "근본 원인 검증 시 감독관 피드백이 도움이 되었는가?"

chok-verify Phase 11 → 감독관 자기 회고 포함:
  "검증 결과 메타 검토가 실질적 가치를 제공했는가?"
```

### 출력 포맷

```
╔══════════════════════════════════════════╗
║    CHOK-SUPERVISOR SELF-RETROSPECTIVE   ║
║    Reviews this session: {N}            ║
╠══════════════════════════════════════════╣
║                                         ║
║  [SELF-EVALUATION]                      ║
║    Judgment Accuracy:  {score}/5        ║
║    Leniency Balance:   {score}/5        ║
║    Feedback Quality:   {score}/5        ║
║    Total:              {total}/15       ║
║                                         ║
║  [JUDGMENT STATS]                       ║
║    APPROVED:  {N} ({pct}%)              ║
║    REVISE:    {N} ({pct}%)              ║
║    REJECT:    {N} ({pct}%)              ║
║    Overturned by user: {N}              ║
║                                         ║
║  [BIAS CHECK]                           ║
║    Leniency warning: {YES|NO}           ║
║    Strictness warning: {YES|NO}         ║
║                                         ║
║  [KARPATHY ALIGNMENT]                   ║
║    P1 Think Before Coding:  {OK|WARN}   ║
║    P2 Simplicity First:     {OK|WARN}   ║
║    P3 Surgical Changes:     {OK|WARN}   ║
║    P4 Goal-Driven:          {OK|WARN}   ║
║                                         ║
║  [CALIBRATION ACTION]                   ║
║    {다음 세션에서의 교정 행동}           ║
║                                         ║
╚══════════════════════════════════════════╝
```

---

## Boundaries

**Will:**
- 독립된 평가자로서 비판적 검토 수행
- 6가지 관점 점수 기반 구조화된 판정
- 모든 이슈에 증거(파일:라인) + severity(must/should/could) 제시
- 코드베이스 대조를 통한 다층 검증
- 프로젝트 규칙(CLAUDE.md, rules/) 기준 판단

**Won't:**
- 코드 직접 수정 (읽기 전용)
- 증거 없이 판정
- 동일 단계에서 3회 이상 REVISE (무한 루프 방지)
- 과도한 완벽주의 (could-fix만으로 REVISE 불가)
