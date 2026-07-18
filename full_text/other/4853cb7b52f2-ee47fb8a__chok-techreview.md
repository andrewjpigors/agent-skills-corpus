---
name: chok-techreview
description: "기술 선택 / 라이브러리 비교 / 패턴 검토 특화 스킬. 4-lens 분석(트레이드오프 / 표준-SOTA 대비 / 보안-성능 영향 / 의존성 버전 pin 사유). Context7 MCP + WebSearch + Codex 2차 의견 자동 수집. chok-auto Stage 2(Tech Review) 대체 또는 독립 호출. 트리거: '기술 검토해줘', '어떤 걸 써야 하지', '라이브러리 비교', '패턴 검토'."
origin: custom
triggers:
  keywords: [기술 검토, 라이브러리 비교, 어떤 걸 써야, 패턴 검토, SOTA]
  type: research
  model-hint: opus
---

# chok-techreview — 기술검토 특화 스킬

기능 요구사항 또는 diff를 입력받아 4-lens로 기술 선택을 분석한다. chok-auto Stage 2(Tech Review)를 독립 스킬로 분리하여 재진입 가능한 contract 제공.

## Sources

| 통합 요소 | 원본 | 가져온 핵심 |
|-----------|------|------------|
| 4-lens 기술검토 | SuperClaude `sc:design` + `sc:research` | 트레이드오프 / SOTA / 보안-성능 / 의존성 |
| Context7 MCP | Context7 라이브러리 docs | 공식 문서 + version-specific 가이드 |
| Multi-model 2차 의견 | gstack `/codex` | Codex CLI read-only 호출 (consensus 패턴 차용) |
| Iron Law | chok-debug | 추측 금지, 권위 있는 소스 인용 의무 |

## Usage

```
/chok-techreview <target> [--lens trade|sota|sec-perf|deps|all] [--codex]
```

| Arg | 설명 | 기본값 |
|-----|------|--------|
| `target` | 기능 요구사항(텍스트), 라이브러리 이름, diff 경로, PR URL | 필수 |
| `--lens` | 특정 lens만 (all = 4-lens 모두) | `all` |
| `--codex` | Codex 2차 의견 추가 호출 | `false` |

### Examples

```bash
# 기능 요구사항 검토
/chok-techreview "실시간 채팅 라이브러리 선택 (10만 동접 목표)"

# 특정 라이브러리 검토
/chok-techreview "tRPC v11" --lens sota

# diff 기반 검토 (의존성 추가/변경 PR)
/chok-techreview HEAD --lens deps

# Codex 2차 의견 포함
/chok-techreview "PostgreSQL vs MongoDB for event sourcing" --codex
```

## 4-Lens Framework

각 lens는 **다른 측면**의 기술 선택 정당성을 검증한다.

### Lens 1: Trade-offs (라이브러리/패턴 선택 트레이드오프)

```
Q: "이 선택의 주요 트레이드오프 3개는?"
출력:
  - performance vs maintainability
  - flexibility vs simplicity
  - ecosystem maturity vs cutting-edge
  - learning curve vs feature completeness

비교 대상: 직접 경쟁 3개 + 인접 영역 1개 (예: tRPC 검토 시 GraphQL + REST + gRPC 비교)
```

**근거 수집**:
- Context7 MCP: 공식 문서의 "When to use / When not to use" 섹션
- WebSearch: "{lib} alternatives {current_year}", "{lib} vs {competitor}"
- GitHub stars + issue 빈도 + 최근 commit (활성도)

### Lens 2: Standard / SOTA 대비

```
Q: "이 선택이 현재 업계 표준 또는 state-of-the-art에서 어느 위치인가?"
출력:
  - 표준 위치: legacy / stable / current / cutting-edge / experimental
  - SOTA 비교: 가장 진보된 대안과의 gap (있다면 이유)
  - 채택률: 주요 기업 / 인기 OSS 프로젝트의 사용 사례
  - 향후 1-2년 전망: deprecated 가능성 / 지속 발전 가능성
```

**근거 수집**:
- WebSearch: "{lib} adoption {current_year}", "{lib} production usage"
- arxiv: 학술적 SOTA 비교 (해당 시)
- 최신 trend 보고서 (Anthropic engineering, AWS prescriptive guidance 등)

### Lens 3: Security & Performance Impact

```
Q: "이 선택의 보안/성능 영향은?"
출력:
  - 알려진 CVE / security advisories (최근 12개월)
  - benchmark 데이터 (있으면): p50/p95/p99 latency, memory footprint
  - 보안 모범 사례 준수 여부 (OWASP / NIST)
  - 의존성 chain의 supply chain 위험 (npm audit / pip audit / cargo audit 결과)
```

**근거 수집**:
- NIST NVD / GitHub Security Advisories
- 공식 benchmark 또는 third-party benchmark 인용
- OWASP cheat sheet 준수도 (해당 카테고리)

### Lens 4: Dependency Version Pin 사유

```
Q: "어떤 버전을 pin하고 왜?"
출력:
  - 추천 version (major.minor.patch + range 정책)
  - pin 사유: API stability / security patch / breaking change 회피
  - peer dependency 호환성 (React 18 vs 19 등)
  - lock file 전략 (caret ^ vs tilde ~ vs exact)
  - upgrade path: 다음 minor / major upgrade 시 영향 예상
```

**근거 수집**:
- 공식 changelog + migration guide
- semver 정책 (해당 라이브러리)
- 의존성 그래프 분석 (npm ls / pip-tree)

## Execution Procedure

### Step 1: Target 파싱

```
target 유형 판별:
  ├─ 기능 요구사항 텍스트 → 후보 라이브러리/패턴 3-5개 추출
  ├─ 라이브러리 이름 → 직접 분석 + 경쟁자 자동 식별
  ├─ diff/PR → 변경된 의존성 + 추가된 import 추출
  └─ 경쟁자 비교 ("X vs Y") → 두 라이브러리 모두 분석
```

### Step 2: 데이터 fan-out (병렬)

```
Agent x 4 (parallel, single message multiple tool calls):
  - Lens 1 agent: Context7 MCP + WebSearch (alternatives + maturity)
  - Lens 2 agent: WebSearch (SOTA, trends, adoption) + arxiv (해당 시)
  - Lens 3 agent: WebSearch (CVE, benchmarks) + Bash (npm/pip audit 가능 시)
  - Lens 4 agent: Context7 MCP (changelog) + Bash (npm ls / pip-tree)
```

### Step 3: Codex 2차 의견 (`--codex` 시)

`chok-supervisor --consensus` 모드와 동일한 패턴 — degraded_mode 포함:

```bash
timeout 90s codex review \
  --sandbox read-only \
  --target "{target}" \
  --output-format json \
  > /tmp/codex-techreview-$$.json 2>/dev/null
CODEX_EXIT=$?
case $CODEX_EXIT in
  0)   CODEX_RESULT="ok" ;;
  124) CODEX_RESULT="timeout" ;;
  *)   CODEX_RESULT="failed" ;;
esac
```

**처리 분기**:

- `CODEX_RESULT="ok"`: Codex 4-lens 답변을 별도 섹션으로 출력 + 합의/이견 명시
- `CODEX_RESULT="timeout"` or `"failed"`: degraded_mode로 폴백 + 출력에 `<codex-2nd-opinion present="false" reason="timeout|exit_nonzero" />` 명시 (silent drop 금지). chok-techreview는 단독 4-lens 결과로 진행하고 사용자에게 알림: "⚠ Codex 2차 의견 실패 — 단독 결과로 진행".

### Step 4: 분석 합성 + Recommendation

각 lens 결과를 통합하여 명확한 권고를 도출:

```
RECOMMENDATION:
  Choice:     {추천 라이브러리/패턴/버전}
  Confidence: HIGH | MEDIUM | LOW
  Tradeoffs:  {수용한 트레이드오프 3개}
  Risks:      {수용한 위험 + 완화 방법}
  Alternatives: {2순위, 사용자가 다른 가중치를 둔다면}
```

**낮은 confidence** (예: 새로운 영역, 대안 너무 많음) 시 `AskUserQuestion`으로 사용자 우선순위 묻기:

```
AskUserQuestion(
  question="기술 선택의 우선순위는?",
  options=[
    {label: "안정성 우선", description: "stable + 큰 커뮤니티 우선"},
    {label: "성능 우선", description: "benchmark 결과 우선"},
    {label: "단순성 우선", description: "learning curve 낮음 우선"},
    {label: "최신 기능 우선", description: "cutting-edge 우선 (위험 감수)"}
  ]
)
```

## Output Schema

```xml
<chok-techreview-output>
  <target type="string" />
  <target-type enum="requirement|library|diff|comparison" />
  <candidates count="N">
    <candidate name="..." score="0.0-1.0">
      <lens-1-tradeoffs>
        <pros />
        <cons />
        <competitors-compared count="3+" />
      </lens-1-tradeoffs>
      <lens-2-sota>
        <position enum="legacy|stable|current|cutting-edge|experimental" />
        <adoption-cases />
        <forecast />
      </lens-2-sota>
      <lens-3-sec-perf>
        <known-cves count="N" />
        <benchmark-data />
        <owasp-compliance />
      </lens-3-sec-perf>
      <lens-4-deps>
        <recommended-version />
        <pin-strategy enum="exact|tilde|caret|range" />
        <upgrade-path />
      </lens-4-deps>
    </candidate>
  </candidates>
  <codex-2nd-opinion present="true|false">
    <agreement enum="full|partial|conflict" />
    <evidence-divergence />
  </codex-2nd-opinion>
  <recommendation>
    <choice />
    <confidence enum="HIGH|MEDIUM|LOW" />
    <tradeoffs-accepted />
    <risks-accepted />
    <alternatives />
  </recommendation>
  <sources cited="N">
    <source url="..." authority="official|academic|community|blog" />
  </sources>
</chok-techreview-output>
```

## chok-auto 통합

chok-auto Stage 2(Tech Review)는 다음과 같이 chok-techreview로 위임:

```xml
<chok-auto-stage-2-delegation>
  <invoke>chok-techreview</invoke>
  <input>
    <target>{Stage 1 분석 결과 — 기능 요구사항 텍스트}</target>
    <lens>all</lens>
    <codex>{chok-auto의 --consensus 플래그 따름}</codex>
  </input>
  <output-consumed-by>chok-auto Stage 4 (Implementation Plan)</output-consumed-by>
</chok-auto-stage-2-delegation>
```

## Boundaries

**Will:**
- 4-lens 독립 분석 + 권위 있는 소스 인용 (Context7 / WebSearch)
- Codex 2차 의견 (옵션) + 합의/이견 명시
- 낮은 confidence 시 사용자 우선순위 게이트
- 명확한 recommendation + 수용한 트레이드오프/위험 명시

**Won't:**
- 코드 직접 수정 (read-only + 권고만)
- 인용 없는 권고 (모든 claim은 출처 명시)
- "그냥 X가 좋아요" 식 추측 답변 (Iron Law 위반)
- 사용자 컨텍스트 무시한 일반론 (target 영역 / 팀 컨텍스트 반영)

## Retrospective (Phase 5)

3-Dimension 평가:

| 관점 | 평가 내용 |
|------|----------|
| Source Authority | 인용한 소스가 권위 있는가? official:academic:community:blog 비율 적절한가? |
| Recommendation Clarity | 권고가 모호하지 않고 실행 가능한가? confidence가 적절히 calibrated 되었는가? |
| Lens Coverage | 4-lens가 균등 분석되었는가? 특정 lens만 비대해지지 않았는가? |
