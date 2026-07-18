---
name: chok
description: "통합 메타 라우터. 사용자 의도를 분석하여 최적의 chok-* 스킬(들)을 자동 선택하고 실행한다. 자동 디스커버리 — 신규 스킬 추가 시 수정 0곳."
origin: custom
---

# chok — 통합 메타 라우터

사용자 의도를 분석하여 최적의 chok-* 스킬(들)을 선택하고 자동 실행한다.
**자동 디스커버리**: 신규 스킬 추가 시 `install.sh --force`만 실행하면 자동 인식.

## Usage

```
/chok "사용자 의도 또는 질문"
/chok "이거 고쳐줘"
/chok "코드 검토해줘"
/chok chok-debug "에러 메시지"    # 명시적 스킬 패스스루
/chok                              # 빈 입력 → chok-auto 폴백
```

## Step 1: Skill Registry 로드

```
Read("~/.claude/skills/shared/skill-registry.md")
```

이 파일은 install.sh가 자동 생성하며, 모든 chok-* 스킬의 name, description, triggers(keywords, type, model-hint)를 포함한다.

## Step 2: 라우팅 알고리즘

5단계 우선순위로 사용자 입력을 분석한다:

```xml
<smart-routing priority-order="P1 > P2 > P3 > P4 > P5">

  <!-- P1: 명시적 스킬명 → 패스스루 -->
  <route id="P1" condition="입력이 chok-{name}으로 시작"
         action="Skill(chok-{name}, 나머지 args)"
         reason="사용자가 스킬을 직접 지정" />

  <!-- P2: 조합 템플릿 매칭 → 다중 스킬 파이프라인 -->
  <route id="P2" condition="입력이 조합 템플릿 intent-patterns와 매칭"
         action="Read('routing-table.md') → 해당 템플릿 실행"
         reason="사전 정의된 다중 스킬 오케스트레이션" />

  <!-- P3: 단일 키워드 매칭 → 단일 스킬 호출 -->
  <route id="P3" condition="registry keywords 매칭 (신뢰도 >= 70%)"
         action="Skill(매칭된 스킬, 사용자 입력)"
         reason="키워드 기반 단일 스킬 라우팅" />

  <!-- P4: 신뢰도 < 70% → 사용자 확인 -->
  <route id="P4" condition="최고 매칭 신뢰도 < 70%"
         action="AskUserQuestion(상위 3개 후보 + 설명)"
         reason="모호한 의도 — 사용자 판단 필요" />

  <!-- P5: 빈 입력 → chok-auto 폴백 -->
  <route id="P5" condition="빈 입력 또는 무신호"
         action="Skill(chok-auto)"
         reason="범용 개발 파이프라인이 가장 안전한 기본값" />

</smart-routing>
```

### 스킬 유형 우선순위

복수 스킬이 동일 신뢰도로 매칭될 때:

```
1순위: process  (분석/원인 파악) — chok-check, chok-debug, chok-unstuck
2순위: execute  (구현/수정/생성) — chok-auto, chok-fix, chok-dev-agents, chok-test, chok-task
3순위: verify   (사후 검증/검토) — chok-verify, chok-supervisor, chok-harness
4순위: research (조사/비교)     — chok-techreview, chok-trendsync
5순위: system   (시스템 관리)   — chok-update
```

### 신뢰도 산정

```
registry keywords 정확 매칭:  +40%
부분 매칭 (substring):       +25%
description 의미 유사:        +20%
조합 템플릿 컨텍스트:         +15%
```

## Step 3: 실행 패턴

```xml
<execution-patterns>

  <pattern name="pipeline" description="순차: A → B → C">
    이전 스킬 결과를 다음 스킬 입력으로 전달.
    각 스킬의 기존 핸드오프 계약(XML 출력)을 그대로 활용.
  </pattern>

  <pattern name="parallel" description="병렬: A + B 동시 → 병합">
    두 스킬을 동시 호출 (복수 Skill 호출).
    각 결과를 사용자에게 통합 표시.
  </pattern>

  <pattern name="conditional" description="조건 분기: A → if X then B else C">
    이전 스킬 결과의 메타데이터(verdict, type, severity)로 분기.
  </pattern>

</execution-patterns>
```

## Step 4: 실행 + 공지

라우팅 결과를 `[chok]` 접두사로 공지한 후 자동 실행:

```
[chok] 의도 분석: {분류 요약}
[chok] 매칭: {skill-name} (신뢰도: {N}%)
[chok] 체인: chok-debug → chok-fix → chok-verify
[chok] 모델: {model-hint}
[chok] 실행 시작 (1/3)...
```

이후 각 스킬의 고유 출력을 그대로 표시한다 (재포맷 안 함).

### 모델 티어링

registry의 `model-hint` 값을 스킬 호출 시 전달:
- 스킬이 자체 티어링을 갖고 있으면 (예: chok-fix `--tier auto`) 스킬 자체 판단 우선
- 없으면 `/chok`가 전달한 model-hint 사용

## 조합 템플릿 (요약)

상세 정의: `Read("routing-table.md")`

| 의도 패턴 | 템플릿 | 실행 패턴 | 스킬 |
|-----------|--------|----------|------|
| 고쳐줘, fix, 이거 안 돼 | fix-pipeline | pipeline | debug → fix → verify |
| 코드 검토, 리뷰 | review-gate | parallel | supervisor + verify |
| 배포 준비, pre-pr | deploy-readiness | pipeline | verify(pre-pr) → supervisor |
| 뭐가 문제야, 어디가 잘못 | diagnose-branch | conditional | check → 유형별 분기 |
| 구현해, 개발해 | full-dev | single | chok-auto |
| 팀으로, 병렬 | team-build | single | chok-dev-agents |
| 막혀, 반복 오류 | unstuck-escape | single | chok-unstuck |
| 기술 검토, 라이브러리 | tech-eval | single | chok-techreview |
| 테스트 만들어 | test-gen | single | chok-test |
| 태스크 정리 | task-plan | single | chok-task |

## 라우팅 검증 테스트 케이스

| # | 입력 | 기대 라우팅 | 기대 패턴 |
|---|------|-----------|----------|
| 1 | `"TypeError in auth.ts"` | chok-debug | P3 single |
| 2 | `"이거 고쳐줘"` | debug → fix → verify | P2 fix-pipeline |
| 3 | `"코드 검토해줘"` | supervisor + verify | P2 review-gate |
| 4 | `"배포 준비됐어?"` | verify → supervisor | P2 deploy-readiness |
| 5 | `"뭐가 문제야?"` | check → 분기 | P2 diagnose-branch |
| 6 | `"인증 모듈 구현해"` | chok-auto | P3 single |
| 7 | `"팀으로 만들어"` | chok-dev-agents | P3 single |
| 8 | `"막혀 같은 오류 반복"` | chok-unstuck | P3 single |
| 9 | `"테스트 만들어줘"` | chok-test | P3 single |
| 10 | (빈 입력) | chok-auto | P5 default |
| 11 | `"뭔가 이상해"` | AskUserQuestion | P4 low-confidence |

## Supervisor Integration

| 체크포인트 | 검토 질문 |
|-----------|----------|
| 라우팅 완료 (실행 전) | "의도 분류가 정확한가? 선택된 스킬 조합이 최적인가?" |
| 파이프라인 완료 | "전체 파이프라인이 사용자 의도를 충족했는가? 누락된 스킬이 있는가?" |

REVISE limit: 1 (라우팅은 한 번만 수정, 이후 사용자 재입력 유도)

## Retrospective

```xml
<retrospective-dimensions total-max="15">
  <dimension name="Routing Accuracy" max="5">
    <evaluates>올바른 스킬(들)이 선택되었는가? 신뢰도 게이트가 적절히 작동했는가?</evaluates>
  </dimension>
  <dimension name="Pipeline Completeness" max="5">
    <evaluates>조합 템플릿이 사용자의 전체 의도를 커버했는가? 누락된 스킬이 있는가?</evaluates>
  </dimension>
  <dimension name="Efficiency" max="5">
    <evaluates>직접 라우팅했는가 아니면 AskUserQuestion이 필요했는가? 불필요한 스킬 호출이 있었는가?</evaluates>
  </dimension>
</retrospective-dimensions>
```

고유 분석: Routing hit-rate = AskUserQuestion 없이 직접 라우팅된 비율

## Boundaries

**Will:**
- skill-registry.md 기반 자동 디스커버리 (신규 스킬 자동 인식)
- 10개 조합 템플릿으로 다중 스킬 파이프라인 자동 실행
- 신뢰도 < 70% 시 AskUserQuestion으로 명확화
- `[chok]` 접두사 공지 (grep 가능한 구조화된 로그)
- 각 스킬의 기존 핸드오프 계약을 그대로 활용

**Won't:**
- 개별 스킬 로직 재구현 (순수 디스패처)
- 스킬 내부 출력 재포맷 (각 스킬 고유 리포트 그대로)
- 명시적 스킬 호출 차단 (/chok-debug 등 직접 사용 유지)
- 동일 세션에서 같은 의도에 대해 무한 재라우팅
