---
name: chok-verify
description: "All-in-one meta verification skill combining 5 verification patterns: pipeline execution, discipline enforcement, eval metrics, language auto-detection, and mode-based verification depth."
origin: custom
triggers:
  keywords: [검증, verify, 빌드, 린트, 테스트, pre-commit, pre-pr]
  type: verify
  model-hint: sonnet
---

# chok-verify — All-in-One Meta Verification Skill

5개 검증 스킬의 장점을 통합한 올인원 메타 검증 스킬.

## Sources

| 통합 요소 | 원본 스킬 | 가져온 핵심 |
|-----------|-----------|------------|
| 실행 파이프라인 | verification-loop | 6단계 순차 검증 |
| 자기기만 방지 | superpowers:verification-before-completion | Iron Law: 증거 없이 주장 금지 |
| 모드 분리 | verify | quick / full / pre-commit / pre-pr |
| pass@k 메트릭 | eval-harness | 신뢰성 정량 측정 |
| 언어 자동감지 | quality-gate + plankton | 프로젝트 타입별 도구 자동 선택 |
| 설정 보호 | plankton | Config Tamper Guard |

## Usage

```
/chok-verify [mode] [--fix] [--json] [--strict] [--affected-only]
```

### Modes

| Mode | 범위 | 소요 시간 | 용도 |
|------|------|----------|------|
| `quick` | Build + Type | ~10s | 빠른 확인 |
| `full` | 8단계 전체 (기본값) | ~60s | 일반 검증 |
| `pre-commit` | Build + Type + Lint + Secrets | ~20s | 커밋 전 |
| `pre-pr` | 8단계 + Eval + Requirements | ~120s | PR 전 완전 검증 |

### Options

- `--fix`: 발견된 이슈를 `/chok-fix`로 자동 전달
- `--json`: 머신 리더블 JSON 출력
- `--strict`: 경고도 실패로 처리
- `--affected-only`: 변경된 파일에 영향받는 테스트만 실행 (gstack diff-based test selection 패턴)

## The Iron Law (from superpowers:verification-before-completion)

```
증거 없이 완료를 주장하지 마라.
검증 명령을 이 메시지에서 실행하지 않았으면, 통과한다고 주장할 수 없다.
```

### 자기기만 감지 (Red Flags)

이런 표현이 나오면 **즉시 중단**하고 검증을 실행하라:

| 금지 표현 | 해야 할 일 |
|-----------|-----------|
| "아마 될 거야" | 검증 명령 실행 |
| "확신해" | 확신 ≠ 증거 |
| "이번만" | 예외 없음 |
| "린터 통과했으니" | 린터 ≠ 빌드 ≠ 테스트 |
| "에이전트가 성공이라고 했어" | 독립적으로 검증 |

### Anti-Gaming Verdict (from Ouroboros v0.41 Verdict Envelope)

PASS/FAIL/CRITICAL/SKIP 외에, **증거 자체가 신뢰 불가**인 경우를 별도 verdict로 분리한다. 통과 주장을 게임하는 두 가지 패턴을 차단:

| Verdict | Trigger | Action |
|---------|---------|--------|
| `EVIDENCE_FORM_MISMATCH` | 테스트/빌드 출력이 잘려서 PASS/FAIL 판정 불가 (예: `\| tail`·`\| head`로 마스킹, 요약만 있고 결과 라인 없음) | 출력 절단 제거하고 재실행. 판정 라인(테스트 수·exit code) 직접 확인 |
| `FABRICATION_SUSPECTED` | 재현 가능한 증거 없이 통과 주장 (로그·exit code·diff 부재, "성공했음"만 존재) | 즉시 중단. 명령 원본 출력 요구. 에이전트 보고면 독립 재실행 |

> ⚠️ **Self-trap 주의:** 본 스킬의 Phase 2-6도 `2>&1 | tail -50` / `| head -50`을 사용한다. 최종 PASS verdict 직전에는 **판정에 필요한 라인(테스트 합계·exit status)**이 절단 구간에 포함됐는지 확인하라. 포함됐으면 절단 없이 재실행 → `EVIDENCE_FORM_MISMATCH` 자가 적용.

## Phase 1: Language & Environment Detection

프로젝트 루트를 스캔하여 언어/프레임워크를 자동 감지한다.

```bash
zsh ~/.claude/skills/chok-verify/scripts/detect-env.sh "$(pwd)"
```

**감지 대상:**

| 파일 | 언어/프레임워크 | 도구 체인 |
|------|----------------|----------|
| `package.json` | Node.js/TypeScript | tsc, biome/eslint, vitest/jest |
| `tsconfig.json` | TypeScript | tsc --noEmit |
| `pyproject.toml` | Python | ruff, pytest, mypy/pyright |
| `go.mod` | Go | go build, go vet, go test |
| `Cargo.toml` | Rust | cargo build, cargo clippy, cargo test |
| `build.gradle.kts` | Kotlin/Java | ./gradlew build, detekt, ./gradlew test |
| `Package.swift` | Swift | swift build, swiftlint, swift test |
| `composer.json` | PHP | php-cs-fixer, phpstan, phpunit |

## Phase 2: Build Verification

```bash
# 자동 감지된 빌드 명령 실행
# Node: npm run build / pnpm build / bun run build
# Python: python -m py_compile (or ruff check)
# Go: go build ./...
# Rust: cargo build
```

**실패 시 즉시 중단.** 빌드가 깨지면 나머지 단계는 무의미하다.

## Phase 3: Type Check

```bash
# TypeScript: npx tsc --noEmit 2>&1 | head -50
# Python: pyright . 2>&1 | head -50  OR  mypy . 2>&1 | head -50
# Go: go vet ./... 2>&1
# Kotlin: ./gradlew compileKotlin 2>&1 | tail -30
```

모든 타입 에러를 파일:라인 형식으로 보고한다.

## Phase 4: Format Check

```bash
# TypeScript/JS: biome check . OR prettier --check .
# Python: ruff format --check .
# Go: gofmt -l .
# Rust: cargo fmt -- --check
```

`--fix` 모드에서는 자동 포맷팅을 적용한다.

## Phase 5: Lint Check

```bash
# TypeScript/JS: biome lint . OR eslint .
# Python: ruff check .
# Go: staticcheck ./... OR golangci-lint run
# Kotlin: detekt
# Swift: swiftlint
```

## Phase 6: Test Suite + Coverage

```bash
# Node: npm test -- --coverage 2>&1 | tail -50
# Python: pytest --cov=src --cov-report=term-missing 2>&1 | tail -50
# Go: go test -race -cover ./... 2>&1 | tail -50
# Rust: cargo test 2>&1 | tail -50
```

**`--affected-only` 모드**: 변경 파일에 영향받는 테스트만 실행하여 검증 시간을 단축한다 (gstack diff-based test selection 패턴). 상세 절차: `Read("~/.claude/skills/chok-verify/references/affected-only.md")`

- `--affected-only` 미지정 시 기존 동작(전체 테스트) 유지
- 영향받는 테스트 0건이면 전체 실행으로 자동 fallback
- pre-pr 모드에서는 `--affected-only` 무시 (항상 전체 실행)

보고 항목:
- 전체 테스트 수 (`--affected-only` 시 선택된 테스트 수 / 전체 수)
- 통과 / 실패 수
- 커버리지 %
- **커버리지 목표: 80% 이상**

## Phase 6.5: E2E Smoke Test (서비스 실행 중일 때 필수)

**단위 테스트 통과 ≠ 실서버 동작 확인.**

Docker/서비스가 실행 중이면 반드시 실제 API를 호출하여 핵심 경로를 검증한다.
단위 테스트는 mock을 사용하므로 실제 의존성(LLM, gRPC, DB 드라이버 등)의 런타임 에러를 잡지 못한다.

```bash
# 1. 서비스 실행 여부 감지
docker compose ps 2>/dev/null | grep -q "running\|healthy\|Up"

# 2. 실행 중이면 Smoke Test 수행
if [ 서비스 실행 중 ]; then
  # Health endpoint (기본 연결성)
  curl -s http://localhost:<PORT>/api/health

  # 핵심 비즈니스 엔드포인트 (실제 의존성 검증)
  # 인증이 필요한 경우 → 사용자에게 인증 토큰을 요청
  # 예: "Smoke Test를 위해 Bearer 토큰이 필요합니다. 브라우저 DevTools > Network 탭에서 Authorization 헤더 값을 알려주세요."
  curl -s -X POST http://localhost:<PORT>/api/<핵심엔드포인트> \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '<최소 요청 데이터>'

  # Docker 로그에서 에러 확인
  docker compose logs --tail 20 2>&1 | grep -i "error\|exception\|failed"
fi
```

### Smoke Test 판정 기준

```xml
<smoke-test-criteria>
  <result condition="Health OK + 핵심 API OK" verdict="PASS" action="다음 단계 진행" />
  <result condition="Health OK + 핵심 API FAIL" verdict="FAIL" action="Docker 로그 확인 → 근본 원인 조사" />
  <result condition="Health FAIL" verdict="CRITICAL" action="서비스 자체 문제 → 즉시 조사" />
  <result condition="서비스 미실행" verdict="SKIP" action="단위 테스트만으로 검증 (경고 출력)" />
</smoke-test-criteria>
```

### chok-debug 입력 스키마 통합 (Phase 1.4-1.9 신규 필드)

chok-debug가 `<debug-session>` XML로 전달하는 신규 필드(`<debug-input-schema>`: e2e-tier, tier-execution, flaky_suspects, token_cost, visual_regression, prod_verification)를 silent drop 방지를 위해 입력 스키마에 명시한다. 입력 처리 규칙 요약: prod_verification=manual_only면 prod 검증 skip + 경고만, flaky insufficient_data면 자동 핸드오프 차단, token_cost 초과면 경고, 신규 필드 누락(구버전)이면 무시하고 smoke-test-criteria만 적용한다. 전체 입력 스키마(필드 계약 오라클) + 입력 처리 규칙 전문을 읽고 따르라: Read("~/.claude/skills/chok-verify/references/debug-input-schema.md")

### 인증이 필요한 Smoke Test

```markdown
핵심 API가 인증을 요구하는 경우:
1. 사용자에게 인증 토큰을 요청한다
   → "Smoke Test를 위해 Bearer 토큰이 필요합니다.
      브라우저 DevTools > Network 탭에서 Authorization 헤더를 복사해주세요."
2. 또는 공개 엔드포인트로 대체 검증한다 (health, public API 등)
3. 인증 없이 테스트 가능한 최대 범위까지 검증한다
```

### 교훈 (이 단계가 추가된 이유)

```
사례: grpc._cython.cygrpc import 실패
  - pytest 355건 ALL PASS (mock이 실제 gRPC를 대체)
  - health endpoint PASS (LLM 미호출)
  - 실제 채팅 → FAIL (LLM 호출 시 grpc C extension 깨짐)
  → 교훈: mock 기반 테스트만으로는 런타임 의존성 문제를 잡을 수 없다
```

## Phase 7: Security Scan

```bash
# 하드코딩된 시크릿 탐지
grep -rn "sk-\|api_key\|password\s*=\|secret\s*=" \
  --include="*.ts" --include="*.js" --include="*.py" --include="*.go" \
  . 2>/dev/null | grep -v node_modules | grep -v ".env.example" | head -20

# 언어별 보안 스캐너
# Python: bandit -r src/
# Node: npm audit
# Go: gosec ./...
# PHP: composer audit

# console.log / print 감사
grep -rn "console\.log\|print(" \
  --include="*.ts" --include="*.tsx" --include="*.py" \
  src/ 2>/dev/null | head -10
```

## Phase 8: Diff Review + Config Tamper Guard

```bash
# 변경 사항 확인
git diff --stat
git diff HEAD~1 --name-only

# Config Tamper Guard: 린터/포맷터 설정 변경 감지
git diff --name-only | grep -E "\.(eslintrc|prettierrc|ruff\.toml|biome\.json|tsconfig)" | head -10
```

설정 파일이 변경되었으면 **경고**: "린터 설정이 수정됨 — 규칙 비활성화가 아닌지 확인 필요"

변경된 파일별 리뷰:
- 의도하지 않은 변경
- 누락된 에러 처리
- 엣지 케이스

## Phase 8.5: Simplicity & Surgical Check (Karpathy P2/P3)

Karpathy 원칙 로드: `Read("~/.claude/skills/shared/karpathy-principles.md")`

diff를 분석하여 과잉 엔지니어링과 불필요 변경을 감지한다. 이 Phase는 **WARN만 산출** (빌드 차단 안 함).

### Simplicity Check (P2)

diff 분석 항목:
1. 신규 abstraction layer 추가 — 해당 추상화가 2곳 이상에서 사용되는가?
   - 단일 호출처 → WARN: "Single-use abstraction detected"
2. 신규 설정/옵션 추가 — 사용자가 요청했는가?
   - 미요청 → WARN: "Speculative configurability added"
3. 추가된 코드 라인 수 vs 최소 필요 라인 수 추정
   - 비율 > 2.0 → WARN: "Code volume exceeds estimated minimum"
4. 불가능한 시나리오에 대한 에러 핸들링
   - WARN: "Error handling for impossible scenario"

### Surgical Check (P3)

diff 분석 항목:
1. 변경된 파일 중 요청과 무관한 파일
   - WARN: "File not traceable to request: {file}"
2. 기존 스타일과 다른 패턴 도입
   - WARN: "Style divergence detected in {file}"
3. 기존 코드 리팩토링 (요청 없이)
   - WARN: "Unrequested refactoring in {file}"
4. 기존 dead code 삭제 (요청 없이)
   - WARN: "Unrequested dead code removal"

### 출력

```
Simplicity: [CLEAN|N warnings]
Surgical:   [CLEAN|N warnings]
```

## Phase 9: Browser Frontend Verification (FE 프로젝트 시)

프로젝트에 FE(React/Vue/Next.js/Svelte 등)가 포함되면 **코드만 보지 말고 브라우저에서 눈으로** 렌더링을 검증한다. FE 검증 절차 전문(도구 선택 + Step 9.1~9.6: 개발 서버 시작·스크린샷 시각 검증·인터랙션·콘솔/네트워크 에러·반응형·GIF 기록 + FE Verify Output)을 읽고 따르라: Read("~/.claude/skills/chok-verify/references/fe-browser-verification.md")

## Phase 10: Requirements Check (pre-pr mode only)

```markdown
1. 원래 요구사항/계획을 다시 읽는다
2. 체크리스트를 만든다
3. 각 항목을 검증한다
4. 누락 사항을 보고한다
```

## Phase 10: Eval Metrics (pre-pr mode only)

pass@k 메트릭으로 신뢰성을 정량 측정한다:

```markdown
[EVAL: feature-name]

Capability Evals:
  - [기능1]: PASS/FAIL (pass@1)
  - [기능2]: PASS/FAIL (pass@2)

Regression Evals:
  - [기존기능1]: PASS/FAIL
  - [기존기능2]: PASS/FAIL

Metrics:
  pass@1: X% (N/M)
  pass@3: X% (N/M)
```

## Phase 11.5: Drift Check (scope creep 감지)

원본 요구사항(seed/goal)으로부터의 의미적·구조적 이탈을 가중 점수(`drift_score = 0.50*goal_drift + 0.30*constraint_drift + 0.20*ontology_drift`, 임계값 0.3 초과 시 chok-supervisor escalation)로 측정해 **scope creep / 의도 이탈**(7-tier debug taxonomy 미포착 클래스)을 보완한다. 활성 조건: `pre-pr` 항상 / `full`은 chok-auto 통합 시 / `quick`·`pre-commit` skip. drift-check 머신러리(가중치 산식, 임베딩 backend 우선순위, goal 출처 우선순위, 임계값 캘리브레이션, `<drift-check>` 출력 스키마) 전문을 읽고 따르라: Read("~/.claude/skills/chok-verify/references/drift-check.md")

## Output Format

### Standard (Human-Readable)

```
╔══════════════════════════════════════════╗
║         CHOK-VERIFY REPORT              ║
║         Mode: [full]                    ║
║         Lang: [TypeScript + Python]     ║
╠══════════════════════════════════════════╣
║                                         ║
║  Env:       [TypeScript 5.x, Node 22]  ║
║  Build:     [PASS]                      ║
║  Types:     [PASS] (0 errors)           ║
║  Format:    [WARN] (3 files unformatted)║
║  Lint:      [PASS] (2 warnings)         ║
║  Tests:     [PASS] (47/47, 84% cov)    ║
║  Security:  [PASS] (0 issues)           ║
║  Diff:      [12 files changed]          ║
║  Config:    [CLEAN] (no tamper)         ║
║  FE Browser:[PASS] (0 console errors)  ║
║  Simplicity:[CLEAN] (0 warnings)       ║
║  Surgical:  [CLEAN] (0 warnings)       ║
║                                         ║
║  Overall:   [READY] for PR             ║
║                                         ║
╠══════════════════════════════════════════╣
║  Issues (--fix 로 자동 해결 가능):       ║
║  1. [FORMAT] 3 files need formatting    ║
║  2. [LINT] 2 non-critical warnings      ║
╚══════════════════════════════════════════╝
```

### XML (Machine-Readable, --json)

```xml
<verify-report>
  <mode enum="quick|full|pre-commit|pre-pr" />
  <languages type="string[]" />
  <timestamp type="ISO8601" />
  <phases>
    <build enum="pass|fail" />
    <types enum="pass|fail" errors="integer" />
    <format enum="pass|warn|fail" files="integer" />
    <lint enum="pass|fail" warnings="integer" />
    <tests enum="pass|fail" total="integer" passed="integer" coverage="integer" />
    <security enum="pass|fail" issues="integer" />
    <diff files-changed="integer" />
    <config-guard enum="clean|tampered" />
    <fe-browser enum="pass|fail|skipped">
      <screenshot enum="ok|broken" />
      <interaction enum="ok|broken" />
      <console-errors type="integer" />
      <network-errors type="integer" />
      <responsive enum="ok|broken" />
    </fe-browser>
    <simplicity enum="clean|warn" warnings="integer" />
    <surgical enum="clean|warn" warnings="integer" />
  </phases>
  <overall enum="ready|not_ready" />
  <fixable-issues type="array">
    <issue>
      <phase type="string" />
      <severity enum="critical|high|medium|low" />
      <count type="integer" />
      <auto-fixable type="boolean" />
    </issue>
  </fixable-issues>
</verify-report>
```

## Severity Classification

```xml
<severity-classification>
  <level name="critical" meaning="빌드 실패, 테스트 실패, 시크릿 노출" action="즉시 중단, 수정 필수" />
  <level name="high" meaning="타입 에러, 커버리지 80% 미달" action="PR 전 수정 필수" />
  <level name="medium" meaning="린트 에러, 포맷 미적용" action="수정 권장, --fix로 자동 해결" />
  <level name="low" meaning="린트 경고, console.log" action="정보 제공" />
</severity-classification>
```

## Integration with chok-fix

`--fix` 옵션 사용 시 또는 수동으로:

```
/chok-verify full --fix
```

1. 검증 실행 → 이슈 수집
2. fixable 이슈를 severity별 분류
3. `/chok-fix`에 XML 형태로 전달
4. 수정 후 재검증 (최대 3회)

## Continuous Mode

긴 세션에서는 자동 체크포인트:

- 함수/컴포넌트 완성 후 → `quick`
- 기능 구현 완료 후 → `full`
- PR 생성 전 → `pre-pr`

## Phase 11: Retrospective (회고)

검증 파이프라인 종료 후 검증 과정 자체의 품질을 종합 회고한다.

회고 프로토콜: Read("~/.claude/skills/shared/retrospective-protocol.md")

### 이 스킬의 평가 관점

| 관점 | 평가 내용 | 만점 |
|------|----------|------|
| **Coverage Sufficiency** | 검증 범위가 변경 사항을 충분히 커버했는가? 건너뛴 Phase가 있는가? | /5 |
| **Result Reliability** | False pass/fail이 있었는가? Iron Law를 위반하지 않았는가? | /5 |
| **Tool Appropriateness** | 자동 감지된 언어/도구가 정확했는가? 검증 소요 시간이 적절했는가? | /5 |

### 고유 분석: 검증 신뢰도 등급

False pass/fail/missed 카운트로 등급을 산정한다:
- **A**: false pass 0, false fail 0 (완벽한 검증)
- **B**: false fail 1-2건 (과잉 검출, 안전한 방향)
- **C**: false pass 1건 (위험 — 검증 범위 확대 필요)
- **D**: false pass 2건+ (검증 파이프라인 재설계 필요)

---

## Supervisor Integration (감독관 연동)

감독관 체크포인트 프로토콜: Read("~/.claude/skills/shared/supervisor-checkpoint.md")

### 이 스킬의 체크포인트

| 시점 | 검토 질문 |
|------|----------|
| 전체 검증 완료 | "검증이 충분했는가? 놓친 검증 영역이 있는가? 통과 판정이 타당한가? Iron Law 위반은 없는가?" |
| --fix 완료 후 | "수정이 원래 이슈를 해결했는가? 새로운 이슈를 만들지 않았는가?" |

### In-Loop Advisor (Anthropic advisor() tool)

감독관(post-hoc 다중모델 채점)과 별개로, **PASS verdict 선언 직전** 네이티브 `advisor()` 툴을 호출한다. advisor()는 전체 transcript(실행한 검증 명령·출력·판정 근거)를 자동 전달받는 in-loop 상위 모델 리뷰어다.

- **호출 시점:** 최종 verdict 직전 (durable 산출물 = verify-report 작성 후)
- **사용 가능 시:** `advisor()` 툴이 환경에 있을 때만. 없으면 skip (degraded, 감독관 게이트로 충분)
- **충돌 처리:** advisor가 "검증 부족" 지적 + 본인이 이미 통과 증거 보유 → silent switch 금지, 한 번 더 advisor() 호출해 근거 대조 후 결정

### REVISE 제한 오버라이드

- 최대 **1회** REVISE (기본 2회가 아님)
- 무한 검증 루프 방지: REVISE 후 재검증에서는 감독관을 다시 호출하지 않음

## Boundaries

**Will:**
- 프로젝트 언어를 자동 감지하고 적절한 도구를 선택
- 8~10단계 체계적 검증 파이프라인 실행
- 자기기만 방지 규율 강제
- XML/Markdown 이중 출력
- chok-fix와 연동하여 자동 수정 파이프라인 제공

**Won't:**
- 증거 없이 완료를 주장
- 빌드 실패 상태에서 다음 단계 진행
- 린터 설정 변경을 묵인
- 부분 검증으로 전체 통과를 선언
