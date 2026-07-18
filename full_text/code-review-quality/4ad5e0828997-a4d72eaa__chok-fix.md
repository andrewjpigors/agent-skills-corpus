---
name: chok-fix
description: "Intelligent auto-fix skill that resolves issues found by chok-verify or debugging sessions. Uses root-cause analysis, tiered model routing, and iterative fix-verify loops."
origin: custom
triggers:
  keywords: [수정, fix, 고쳐, 자동 수정, 이슈 해결]
  type: execute
  model-hint: sonnet
---

# chok-fix — Intelligent Auto-Fix Skill

디버그/검증 이후 발견된 이슈를 체계적으로 해결하는 스킬.
`/chok-verify --fix`에서 자동 호출되거나, 독립적으로 사용 가능.

## Sources

| 통합 요소 | 원본 | 가져온 핵심 |
|-----------|------|------------|
| 3단계 자동 수정 | Plankton | Format → Lint → Delegate |
| 모델 티어 라우팅 | Plankton | Haiku/Sonnet/Opus 복잡도별 분배 |
| 근본 원인 분석 | sc:pm PDCA | 재시도 금지, Why 먼저 |
| 설정 보호 | Plankton | Config Tamper Guard |
| 자동 반복 검증 | autoresearch | Modify → Verify → Keep/Discard |
| 에이전트 위임 | superpowers | 병렬 서브에이전트 수정 |

## Usage

```
/chok-fix [target] [--tier auto|haiku|sonnet|opus] [--max-rounds 3] [--dry-run]
```

### Arguments

| Arg | 설명 | 기본값 |
|-----|------|--------|
| `target` | 파일, 디렉토리, 또는 `verify-report.json` | `.` (현재 디렉토리) |
| `--tier` | 모델 라우팅 (auto = 복잡도 자동 판단) | `auto` |
| `--max-rounds` | 최대 수정-검증 반복 횟수 | `3` |
| `--dry-run` | 수정하지 않고 계획만 출력 | `false` |

## Core Principle: Root Cause First

```
절대 같은 방법으로 재시도하지 마라.
실패하면 WHY를 먼저 파악하라.
```

### Anti-Patterns (절대 금지)

```
BAD:  에러 발생 → 같은 코드 다시 실행
BAD:  타임아웃 → 대기 시간만 늘림
BAD:  Warning → "일단 넘어가자"
```

### Correct Patterns (필수)

```
GOOD: 에러 발생 → 공식 문서 조사 → 원인 파악 → 다른 방법 시도
GOOD: 타임아웃 → 리소스/네트워크 근본 원인 조사
GOOD: Warning → 왜 발생했는지 조사 → 카테고리 분류 → 조치
```

## Fix Pipeline

### Stage 1: Issue Triage (분류)

chok-verify 결과 또는 수동 이슈를 severity별로 분류한다:

```xml
<issue-triage>
  <severity level="critical" action="즉시 수정">
    <category>Build failures</category>
    <category>Test failures</category>
    <category>Security vulnerabilities (secrets, injection)</category>
    <category>Runtime errors</category>
  </severity>
  <severity level="high" action="PR 전 수정">
    <category>Type errors</category>
    <category>Coverage below 80%</category>
    <category>Missing error handling</category>
  </severity>
  <severity level="medium" action="자동 수정 가능">
    <category>Lint errors</category>
    <category>Format violations</category>
    <category>Unused imports</category>
    <category>console.log / print statements</category>
  </severity>
  <severity level="low" action="정보 제공">
    <category>Lint warnings</category>
    <category>Style suggestions</category>
    <category>Deprecation notices</category>
  </severity>
</issue-triage>
```

### Stage 2: Auto-Fix (Silent)

MEDIUM 이하 이슈를 도구로 자동 수정한다:

```bash
# Format (40-50% 이슈 해결)
# TypeScript/JS
biome check --write . 2>/dev/null || prettier --write . 2>/dev/null

# Python
ruff format . 2>/dev/null
ruff check --fix . 2>/dev/null

# Go
gofmt -w . 2>/dev/null
goimports -w . 2>/dev/null

# Rust
cargo fmt 2>/dev/null
```

### Stage 3: Root Cause Analysis (HIGH/CRITICAL)

HIGH 이상 이슈는 자동 수정하지 않고, 근본 원인을 분석한다:

```markdown
For each issue:

1. IDENTIFY: 어떤 에러인가?
   - 에러 메시지 전문 확인
   - 발생 파일:라인 확인

2. INVESTIGATE: 왜 발생했는가?
   - 관련 코드 컨텍스트 읽기
   - 공식 문서 확인 (context7 MCP 활용)
   - 유사 이슈 검색

3. HYPOTHESIZE: 원인 가설 수립
   - "원인은 [X]이다. 근거: [Y]"
   - "해결책: [Z]. 이유: [W]"

4. FIX: 수정 적용
   - 이전 시도와 다른 방법이어야 한다
   - 최소 변경 원칙 (관련 없는 코드 건드리지 않음)

4.5. SIMPLICITY GATE (Karpathy P2/P3 검증):
   `Read("~/.claude/skills/shared/karpathy-principles.md")`
   수정 적용 전 다음을 자문한다:
   - "이 수정이 근본 원인 해결에 필요한 최소 변경인가?"
   - "수정이 요청 범위를 넘어서지 않는가?"
   - "기존 코드를 불필요하게 리팩토링하지 않았는가?"
   - "시니어 엔지니어가 이 수정을 보고 '과도하다'고 할 것인가?"
   위반 감지 시: 수정 축소 후 재적용 (동일 라운드 내 즉시 처리)

5. VERIFY: 수정 검증
   - 해당 이슈 재현 테스트
   - 회귀 테스트
```

### Stage 4: Tiered Model Routing

이슈 복잡도에 따라 에이전트 모델을 라우팅한다:

| Tier | 모델 | 대상 이슈 | 타임아웃 |
|------|------|----------|---------|
| **haiku** | Haiku 4.5 | 포맷, 임포트 정리, 단순 린트 | 120s |
| **sonnet** | Sonnet 4.6 | 리팩토링, 복잡도, 테스트 추가 | 300s |
| **opus** | Opus 4.7 | 타입 시스템, 아키텍처, 보안 | 600s |

**Auto-routing 기준:**

```xml
<model-tiering>
  <tier name="haiku" model="Haiku 4.5" timeout="120s">
    <target>포맷, 임포트 정리, 단순 린트</target>
    <code-patterns>E1xx, W1xx, F401 (import)</code-patterns>
  </tier>
  <tier name="sonnet" model="Sonnet 4.6" timeout="300s">
    <target>리팩토링, 복잡도, 테스트 추가</target>
    <code-patterns>C901 (complexity), PLR (refactor)</code-patterns>
  </tier>
  <tier name="opus" model="Opus 4.7" timeout="600s">
    <target>타입 시스템, 아키텍처, 보안</target>
    <code-patterns>Type errors, security, architecture</code-patterns>
  </tier>
  <auto-routing>
    <rule condition="simple issues 5 or fewer" action="use current tier" />
    <rule condition="simple issues more than 5" action="upgrade one tier" />
  </auto-routing>
</model-tiering>
```

### Stage 5: Fix-Verify Loop

수정 후 자동 재검증한다 (최대 `--max-rounds` 회):

```
Round 1:
├─ Stage 2: Auto-fix (format, lint)
├─ chok-verify quick → 이슈 확인
├─ 이슈 남아있으면 → Round 2
└─ 이슈 없으면 → Stage 5.5 (regression test mandate)

Round 2:
├─ Stage 3: Root cause analysis
├─ Stage 4: Agent delegation
├─ chok-verify full → 재검증
├─ 이슈 남아있으면 → Round 3
└─ 이슈 없으면 → Stage 5.5

Round 3 (final):
├─ 남은 이슈 상세 보고
├─ 수동 수정 가이드 제공
└─ 자동 수정 포기 사유 설명
```

### Stage 5.5: Regression Test Mandate (행동 변경 수정 시)

**Iron Law 보강**: "수정 없이 fail하던 테스트"가 "수정 후 pass"하는 것을 실제로 검증한다. 단순히 테스트 추가만 하는 것이 아니라 git 시점 비교로 행동 변경을 증명한다.

**적용 대상** (자동 분기):
- 행동 변경 (Type errors가 아닌 logic / runtime / behavioral 수정) → **mandatory**
- Lint/format/import-only 수정 → **면제** (skip)
- Test-only 수정 (테스트 코드만 수정) → **면제** (skip)
- Documentation/comment only → **면제** (skip)

**검증 로직 (요약)**: mandate는 (1) `pre_fix_commit_sha`에서 신규 회귀 테스트가 **FAIL**함을 git 시점 복원으로 증명하고, (2) 수정 후 동일 테스트가 **PASS**함을 확인하며, (3) 두 검증을 통과해야만 commit을 허용한다. 통과 시 출력에 `<regression-verified>{path, pre_fix_status, post_fix_status}</regression-verified>` 필드를 포함한다.

**전체 verification-steps XML + safety/exemption 규칙 + 통과/실패 출력 예시는 적용 직전 `Read("~/.claude/skills/chok-fix/references/regression-mandate.md")`로 로드하여 step 0~8을 그대로 실행하라.**

**chok-verify와의 인터페이스**: chok-verify pre-pr 모드는 `regression-verified` 필드 부재 시 PR 차단 (단 면제 조건 충족 시 통과).

## Fix Strategies by Issue Type

이슈 타입별(Build / Type / Test / Security / Coverage) 단계별 수정 레시피가 필요하면, 해당 이슈를 수정하기 직전 `Read("~/.claude/skills/chok-fix/references/fix-strategies.md")`로 레시피를 로드하여 그대로 적용하라.

## Config Tamper Guard

수정 과정에서 린터/포맷터 설정을 변경하면 **즉시 롤백**한다:

```bash
# 보호 대상 파일
PROTECTED_FILES=(
    ".eslintrc*" ".prettierrc*" "biome.json"
    ".ruff.toml" "ruff.toml" "pyproject.toml"  # [tool.ruff] 섹션
    "tsconfig.json" ".swiftlint.yml"
    ".golangci.yml" "detekt.yml"
    ".hadolint.yaml" ".shellcheckrc"
)

# 변경 감지 시
echo "WARNING: 린터 설정 변경 감지. 코드를 수정하라, 규칙을 비활성화하지 마라."
git checkout -- [protected-file]
```

## Output Format

### Fix Report

```
╔══════════════════════════════════════════╗
║           CHOK-FIX REPORT               ║
║           Rounds: 2/3                   ║
║           Duration: 45s                 ║
╠══════════════════════════════════════════╣
║                                         ║
║  Auto-Fixed (Silent):                   ║
║    [FORMAT] 5 files reformatted         ║
║    [LINT]   3 unused imports removed    ║
║    [LINT]   2 console.logs removed      ║
║                                         ║
║  Agent-Fixed (Delegated):               ║
║    [TYPE]   Null check added: auth.ts:45║
║    [TEST]   Missing assertion fixed     ║
║                                         ║
║  Remaining (Manual):                    ║
║    [NONE]   All issues resolved         ║
║                                         ║
║  Verification:                          ║
║    Before: 12 issues (2 HIGH, 10 MED)   ║
║    After:  0 issues                     ║
║    Status: ALL CLEAR                    ║
║                                         ║
╚══════════════════════════════════════════╝
```

### XML (chok-verify 연동용)

```xml
<fix-report>
  <rounds type="integer" />
  <max-rounds type="integer" />
  <duration-seconds type="integer" />
  <issues>
    <total-found type="integer" />
    <auto-fixed type="integer" />
    <agent-fixed type="integer" />
    <remaining type="integer" />
  </issues>
  <fixes type="array">
    <fix>
      <phase enum="format|lint|type|test|security" />
      <file type="string" />
      <action type="string" />
      <tier enum="auto|haiku|sonnet|opus" />
      <root-cause type="string" optional="true" />
    </fix>
  </fixes>
  <verification>
    <before critical="integer" high="integer" medium="integer" low="integer" />
    <after critical="integer" high="integer" medium="integer" low="integer" />
  </verification>
  <status enum="all_clear|partial|manual_required|prod_manual_only" />
</fix-report>
```

### chok-debug 입력 처리 규칙 (Phase 1.9 manual_only)

chok-debug XML 출력에 `<prod_verification execution="manual_only">` 포함 시:

```
1. 자동 수정 시도 금지
2. fix-report status = "prod_manual_only"
3. Phase 1.9 가이드 텍스트를 사용자에게 그대로 전달
4. chok-verify로 핸드오프하지 않음 (prod 검증은 별도 도구 영역)
5. 일반 <fix-proposal> 블록은 정상 처리 (개발/스테이징 환경만)

처리 우선순위:
  - <fix-proposal> 있음 → 일반 수정 진행 (Stage 2-5)
  - <prod_verification execution="manual_only"> 추가 있음 → 보고 단계에 prod 가이드 첨부
  - 두 블록 모두 만족 후 chok-verify 호출 (prod 부분은 제외)
```

### Flaky 신뢰도 검증 (PFS insufficient_data)

chok-debug XML 출력에 `<flaky_suspects classification="insufficient_data">` 포함 시:

```
1. chok-fix 자동 핸드오프 차단
2. fix-report status = "manual_required"
3. 사용자 알림: "PFS 측정 표본 부족 (<10회) — PFS_RUNS=10 이상으로 재측정 후 재시도"
```

## Integration with chok-verify

### Automatic Flow

```
/chok-verify full --fix
    │
    ├─ chok-verify 실행 → 이슈 수집
    ├─ fixable_issues XML 생성
    ├─ chok-fix에 전달
    │   ├─ Stage 1: Triage
    │   ├─ Stage 2: Auto-fix
    │   ├─ Stage 3-4: Root cause + Agent (필요시)
    │   └─ Stage 5: Re-verify
    └─ 최종 chok-verify 리포트 출력
```

### Manual Flow

```
# 특정 파일만 수정
/chok-fix src/auth.ts --tier sonnet

# 드라이런 (수정 계획만 확인)
/chok-fix . --dry-run

# 이전 검증 결과 기반 수정
/chok-fix verify-report.json --max-rounds 5
```

## Learning & Documentation

수정 라운드 종료 시 성공/실패 패턴을 기록하라. 성공·실패 패턴 기록 프로토콜이 필요하면 `Read("~/.claude/skills/chok-fix/references/fix-strategies.md")`의 "Learning & Documentation" 섹션을 로드하여 따르라.

## Stage 6: Retrospective (회고)

수정 파이프라인 종료 후 전체 수정 과정을 종합 회고한다.

회고 프로토콜: Read("~/.claude/skills/shared/retrospective-protocol.md")

### 이 스킬의 평가 관점

| 관점 | 평가 내용 | 만점 |
|------|----------|------|
| **Fix Accuracy** | 수정이 근본 원인을 해결했는가? 새로운 이슈를 만들지 않았는가? | /5 |
| **Model Efficiency** | 모델 티어링이 적절했는가? Auto-fix 비율이 높은가? 불필요한 opus 호출이 없었는가? | /5 |
| **Process Fidelity** | Root cause first 원칙을 지켰는가? 같은 방법으로 재시도하지 않았는가? | /5 |

### 고유 분석: 수정 효율 등급

Auto-fix/Agent-fix/Manual 비율과 라운드 수로 등급을 산정한다:
- **A**: Auto-fix 70%+, 1라운드 완료
- **B**: Auto-fix 50%+, 2라운드 이내 완료
- **C**: Agent-fix 필요, 3라운드 내 완료
- **D**: Manual 잔여 있음

---

## Supervisor Integration (감독관 연동)

감독관 체크포인트 프로토콜: Read("~/.claude/skills/shared/supervisor-checkpoint.md")

### 이 스킬의 체크포인트

| 시점 | 검토 질문 |
|------|----------|
| Stage 1 (Triage) 완료 | "이슈 분류가 정확한가? severity 판정이 타당한가? 놓친 이슈는 없는가?" |
| Stage 3 (Root Cause) 완료 | "근본 원인 분석이 정확한가? 수정 방향이 올바른가? 회귀 위험은 없는가?" |
| Stage 5 (Fix-Verify) 각 라운드 | "수정이 근본 원인을 해결했는가? 새로운 문제를 만들지 않았는가? 린터 설정을 우회하지 않았는가?" |

### 예외 규칙

- Config Tamper 감지 시 감독관 판정 없이 즉시 롤백

## Boundaries

**Will:**
- chok-verify 결과를 입력받아 체계적으로 수정
- 근본 원인 분석 후 수정 (블라인드 재시도 금지)
- 복잡도별 모델 라우팅으로 비용 최적화
- 수정 후 자동 재검증 (fix-verify loop)
- 린터 설정 변경 차단 (Config Tamper Guard)

**Won't:**
- 같은 방법으로 재시도 (반드시 다른 접근)
- 원인 파악 없이 수정 시도
- 린터/포맷터 규칙 비활성화로 이슈 해결
- max-rounds 초과 시 무한 반복
- 보안 이슈를 자동으로만 처리 (사람 검토 필수)
