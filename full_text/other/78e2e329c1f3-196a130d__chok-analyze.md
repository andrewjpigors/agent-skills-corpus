---
name: chok-analyze
description: "실무 코드 설계·시스템 아키텍처·개념/이론을 다층 렌즈로 분석하는 스킬. 2-Tier Classifier(카테고리→복잡도)로 즉답/리포트를 자동 분기하고, deep 모드에서 Socratic 심화를 제공한다. 트레이드오프는 chok-techreview, 보안은 chok-check으로 느슨한 핸드오프. 트리거: '분석해줘', '설계 검토', '이게 왜 이런 구조야', '개념 설명해줘', 'analyze', 'chok-analyze'."
origin: custom
triggers:
  keywords: [분석, 설계 분석, 코드 분석, 아키텍처 분석, 개념 분석, 원리, 구조 분석, analyze, 설명해줘, 왜 이런 구조]
  type: process
  model-hint: opus
---

# chok-analyze — 다층 렌즈 분석 스킬

사용자의 기술 질문을 2-Tier Classifier로 분류하고, 카테고리별 렌즈로 구조화된 분석을 산출한다.

## Sources

| 통합 요소 | 원본 | 가져온 핵심 |
|-----------|------|------------|
| Classifier-First 패턴 | chok-check 5-lens + SuperClaude deep-research | 의도 분류 → 분석 분기 |
| Socratic 심화 | Superpowers brainstorming + gstack Think-Plan-Build | deep 모드 사용자 주도 심화 |
| 렌즈 분리 | chok-supervisor 6-dimension | 독립 관점별 구조화 분석 |
| 느슨한 핸드오프 | chok-* 파이프라인 패턴 | 권고만, 자동 호출 없음 |

## Usage

```
/chok-analyze "질문 또는 분석 요청"
/chok-analyze "우리 주문 모듈 구조 개선 방향"
/chok-analyze "이벤트 소싱이 뭐야? CQRS랑 뭐가 달라?"
/chok-analyze "이 API의 응답 시간이 왜 느릴까?"
```

## Execution Procedure

### Phase 1: 2-Tier Classification

Classifier는 `haiku` 모델로 토큰 최소화하여 실행한다.

판별 규칙 상세: `Read("~/.claude/skills/chok-analyze/references/classifier-rules.md")`

```
Agent(
  subagent_type: "general-purpose",
  model: "haiku",
  prompt: "다음 질문을 분류하라: '{user_question}'
           classifier-rules.md의 규칙에 따라 JSON 출력.
           출력: {category, complexity, lenses, handoff}"
)
```

**결과 형태**:

```json
{"category":"code","complexity":"deep","lenses":["L1","L2"],"handoff":["chok-techreview"]}
```

**신뢰도 fallback**: 카테고리 경계가 모호할 때 → 사용자에게 1회 확인:

```
"이 질문은 코드/시스템 분석과 개념/이론 분석 모두에 해당할 수 있습니다.
 어느 관점으로 분석할까요?"
  → [코드/시스템] [개념/이론] [둘 다]
```

### Phase 2: 프로젝트 컨텍스트 수집 (code 카테고리)

code 카테고리인 경우 프로젝트 상태를 수집한다. concept 카테고리는 이 단계를 건너뛴다.

```
1. 질문에 언급된 파일/모듈 → Glob + Read로 구조 파악
2. CLAUDE.md, .claude/rules/ → 프로젝트 규칙 확인
3. git log --oneline -5 → 최근 변경 흐름
4. 관련 의존성 확인 (package.json, go.mod 등)
```

### Phase 3: 렌즈 분석 실행

Classifier 결과의 `lenses` 배열을 우선순위 순서로 분석한다.

**code 카테고리 렌즈**:

각 렌즈 상세 가이드:
- L1: `Read("~/.claude/skills/chok-analyze/references/lens-L1-design.md")`
- L2: `Read("~/.claude/skills/chok-analyze/references/lens-L2-architecture.md")`
- L3: `Read("~/.claude/skills/chok-analyze/references/lens-L3-performance.md")`

**concept 카테고리 렌즈**:

- C1: `Read("~/.claude/skills/chok-analyze/references/lens-C1-principle.md")`
- C2: `Read("~/.claude/skills/chok-analyze/references/lens-C2-comparison.md")`
- C3: `Read("~/.claude/skills/chok-analyze/references/lens-C3-scenario.md")`

**분석 실행**: 선택된 렌즈만 해당 reference 파일을 로드하여 분석 (progressive disclosure).

### Phase 4: 출력

출력 형식 상세: `Read("~/.claude/skills/chok-analyze/references/output-schemas.md")`

**quick 모드**: P1 렌즈 인사이트 중심의 즉답. 핸드오프 권고 포함 (해당 시).

**deep 모드**: 적용된 전체 렌즈의 구조화된 리포트. 핸드오프 권고 + Socratic Gate 포함.

### Phase 5: Socratic Gate (deep 모드 전용)

deep 모드 리포트 출력 후 심화 옵션을 제시한다.

```
"추가로 깊이 볼 렌즈가 있나요?"
  • {적용된 렌즈 중 선택}
  • 핸드오프 스킬 실행 (chok-techreview / chok-check)
  • 종료
```

- 사용자가 렌즈를 선택하면 해당 렌즈를 full depth로 재분석
- 심화는 반복 가능 (렌즈 A 심화 → 렌즈 B 심화 → 종료)
- 사용자가 만족 표현 또는 "종료" 시 완료

### Phase 6: 리포트 저장 (선택)

사용자 요청 시 deep 모드 결과를 파일로 저장:

```
docs/analyze/{YYYY-MM-DD}-{topic}.md
```

## 파이프라인 연동 (느슨한 핸드오프)

chok-analyze는 분석 결과에서 필요 시 다른 스킬을 **권고만** 한다.
자동 호출하지 않으며, 사용자가 명시적으로 요청할 때만 해당 스킬 실행.

| 조건 | 권고 대상 | 형태 |
|------|---------|------|
| 기술 선택/비교가 핵심 | chok-techreview | "→ `/chok-techreview` 권고" |
| 보안/취약점 심화 필요 | chok-check | "→ `/chok-check` 권고" |
| 디버깅 필요 발견 | chok-debug | "→ `/chok-debug` 권고" |

## Boundaries

**Will:**
- 2-Tier Classifier로 질문 유형·복잡도 자동 판별
- 카테고리별 렌즈로 구조화된 분석 (code 3-렌즈, concept 3-렌즈)
- quick/deep 하이브리드 출력
- deep 모드에서 Socratic 심화 (사용자 주도 반복)
- 트레이드오프/보안은 기존 스킬로 느슨한 핸드오프

**Won't:**
- 코드 직접 수정 (분석 전용, read-only)
- chok-techreview/chok-check과 중복 분석 (핸드오프 권고만)
- non-dev 질문에 대한 분석 → 범위 밖 안내 후 Claude 기본 응답으로 전환
- 사용자 컨펌 없이 다른 스킬 자동 호출
