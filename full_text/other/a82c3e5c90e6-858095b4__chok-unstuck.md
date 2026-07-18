---
name: chok-unstuck
description: "Lateral-thinking divergence skill. fix↔verify가 2회 무진전 / chok-debug 3-failure halt 발생 시 발동하여 5-persona(hacker/researcher/simplifier/architect/contrarian) 관점에서 대안을 발산하고 합성안 1개를 사용자 확정한다. 트리거: '막혀', '같은 오류 반복', '다른 접근 필요', stagnation pattern."
origin: custom
triggers:
  keywords: [막혀, 같은 오류 반복, 다른 방법, stuck, 무한 루프]
  type: process
  model-hint: opus
---

# chok-unstuck — Lateral-Thinking Divergence Skill

같은 접근이 반복 실패할 때 **사고의 축**을 강제로 바꾼다. fix → verify 사이클이 2회 이상 무진전이거나 chok-debug 가설이 3회 실패한 경우 자동 트리거. 5개 persona가 독립적으로 대안을 생성하고, 합성안 1개를 사용자가 확정한다.

## Sources

| 통합 요소 | 원본 | 가져온 핵심 |
|-----------|------|------------|
| 5-persona 발산 | Ouroboros `ouroboros_lateral_think` | hacker/researcher/simplifier/architect/contrarian 5축 |
| 무진전 감지 | superpowers:systematic-debugging | "3회 실패 후 재검토" 규칙 |
| 사용자 확정 게이트 | chok-supervisor 6-principle rubric | 비가역/보안 영향 시 강제 게이트 |
| MCP 위임 | `mcp__plugin_ouroboros__ouroboros_lateral_think` | 자체 구현 vs 위임 선택 가능 |

## Usage

```
/chok-unstuck [--persona hacker|researcher|simplifier|architect|contrarian|all] [--mcp]
```

| Arg | 설명 | 기본값 |
|-----|------|--------|
| `--persona` | 단일 persona만 실행 (`all` = 5개 모두 fan-out) | `all` |
| `--mcp` | Ouroboros MCP에 위임 (자체 구현 안 함) | `false` |

### Examples

```bash
# 5-persona 전체 발산 (자체 구현)
/chok-unstuck

# 단일 persona (빠른 escape hatch 필요 시)
/chok-unstuck --persona contrarian

# Ouroboros MCP에 위임
/chok-unstuck --mcp
```

## 자동 트리거 조건

다음 상황에서 chok-fix / chok-debug가 자동으로 chok-unstuck을 호출한다 (사용자 confirm 필수):

```xml
<auto-trigger-conditions logic="OR">
  <cond name="fix-verify-stagnation">
    chok-fix → chok-verify 사이클 2회 후 동일 이슈 잔존 (verify-report.fixable_issues 동일 신호)
  </cond>
  <cond name="debug-hypothesis-exhaustion">
    chok-debug Phase 3 가설 3회 실패 (테스트 결과 모두 negative)
  </cond>
  <cond name="explicit-user-stuck-signal">
    사용자 메시지에 "막혀", "같은 오류 반복", "다른 접근 필요", "stuck", "exhausted" 키워드 매칭
    (userpromptsubmit-skill-router.sh hook에서 hint 생성)
  </cond>
</auto-trigger-conditions>
```

**자동 트리거 시**: chok-unstuck은 즉시 실행하지 않고 사용자에게 `AskUserQuestion`으로 발동 confirm 요청. 거부 시 원래 작업 흐름 유지.

## Persona 정의

각 persona는 **다른 사고 축**으로 같은 문제를 본다. 5개를 병렬 fan-out하여 의도적 다양성을 확보.

```xml
<personas>
  <persona name="hacker" axis="unconventional-workaround">
    <philosophy>"규칙을 우회하라. 설계자가 의도하지 않은 사용법을 찾아라."</philosophy>
    <typical-moves>
      - 환경 변수 / 런타임 플래그로 행동 변경
      - undocumented API / 내부 함수 직접 호출
      - 외부 의존성 monkey-patch
      - 기존 도구의 의외의 활용 (예: lint 도구로 검증 대체)
    </typical-moves>
    <output-prompt>"이 문제를 5분 안에 해결하려면 무엇이든 사용 가능하다. 가장 빠른 우회 방법은?"</output-prompt>
  </persona>

  <persona name="researcher" axis="information-gathering">
    <philosophy>"내가 모르는 무언가가 있다. 더 읽고 더 찾아라."</philosophy>
    <typical-moves>
      - 공식 문서 + changelog 정독
      - issue tracker / Stack Overflow / GitHub Discussions 검색
      - 유사 라이브러리 / 경쟁 제품 비교
      - 학술 논문 / RFC / spec 인용
    </typical-moves>
    <output-prompt>"이 문제에 관한 권위 있는 소스 3개와 거기서 발견한 키 인사이트는?"</output-prompt>
  </persona>

  <persona name="simplifier" axis="reduce-complexity">
    <philosophy>"제거할 수 있는 것은 모두 제거하라. 단순한 해결책이 정답일 가능성이 높다."</philosophy>
    <typical-moves>
      - 의존성 한 개 제거
      - 추상 레이어 한 개 평탄화
      - 코드 한 줄로 대체 (one-liner)
      - 데이터 구조 변경 (배열 → 단일 객체)
    </typical-moves>
    <output-prompt>"이 문제의 절반 크기 버전은? 더 단순한 가정에서 해결하면 어떻게 되는가?"</output-prompt>
  </persona>

  <persona name="architect" axis="restructure-approach">
    <philosophy>"문제의 형태 자체를 바꿔라. 다른 패러다임에서 보면 사라진다."</philosophy>
    <typical-moves>
      - sync → async (또는 반대)
      - request-response → event-driven
      - in-memory → persistent (또는 반대)
      - 라이브러리 교체 / 패턴 교체
    </typical-moves>
    <output-prompt>"이 문제를 다른 아키텍처 패턴(event-driven / actor / pipeline / FRP)으로 옮기면?"</output-prompt>
  </persona>

  <persona name="contrarian" axis="challenge-assumptions">
    <philosophy>"내가 사실이라고 믿는 것 중 거짓일 가능성은? 문제 정의 자체가 틀렸을 수 있다."</philosophy>
    <typical-moves>
      - "이게 정말 문제인가?" 재정의
      - "이 요구사항이 진짜 필요한가?" 의문
      - "테스트가 맞는가? 코드가 맞는가?" 역전
      - "현재 가정한 인과관계가 반대 방향이라면?"
    </typical-moves>
    <output-prompt>"이 문제 진술의 3가지 숨은 가정은? 그중 하나가 틀렸다면 해결책은?"</output-prompt>
  </persona>
</personas>
```

## Execution Procedure

### Step 1: 컨텍스트 수집

```
1. 무진전 증거 수집:
   - chok-fix verify-report.json (실패한 fix 이력)
   - chok-debug hypothesis-log (실패한 가설 3건)
   - 최근 5회 chok-verify 결과 diff

2. 원래 문제 명세:
   - 사용자 원본 요청 (chok-task docs/tasks.md 우선)
   - chok-debug Phase 1 root-cause 텍스트
   - chok-verify 출력의 fixable_issues 잔존 목록

3. 이미 시도한 접근법 목록:
   - 각 시도의 "왜 실패했는가" 한 줄 요약
```

### Step 2: Persona Fan-out

`--persona all` (기본값) 또는 `--mcp` 시 5개 persona 병렬 호출.

**자체 구현 경로** (default):

```
Agent x 5 (parallel, single message multiple tool calls):
  for persona in [hacker, researcher, simplifier, architect, contrarian]:
    Agent(
      subagent_type: "general-purpose",
      prompt: "{persona의 philosophy + typical-moves + output-prompt}
              컨텍스트: {Step 1 수집 데이터}
              제약: 100단어 이하, 구체적 행동 가능한 대안 1개"
    )
```

**MCP 위임 경로** (`--mcp`):

```
mcp__plugin_ouroboros__ouroboros_lateral_think(
  problem_context: "{Step 1 컨텍스트}",
  current_approach: "{현재까지 시도한 접근}",
  failed_attempts: [{시도 1}, {시도 2}, {시도 3}],
  stagnation_pattern: "fix_verify_loop | hypothesis_exhausted | etc.",
  persona: "all"
)
```

### Step 3: 합성안 도출 (Synthesis)

5개 persona의 출력을 1개 권장 합성안으로 결합:

```xml
<synthesis-rules>
  <rule>모든 persona가 공통으로 지적한 부분이 있으면 그것이 합성안의 핵심</rule>
  <rule>contrarian의 "가정 의심" 포인트는 항상 검토 (가정이 틀리면 다른 4개 모두 의미 없음)</rule>
  <rule>합성안은 (a) 핵심 변경 1개 + (b) fallback 1개 + (c) 검증 기준 1개로 구성</rule>
  <rule>합성안의 reversibility를 평가 — 비가역 변경 포함 시 사용자 게이트 강제</rule>
</synthesis-rules>
```

### Step 4: 사용자 확정 게이트 (필수)

5 persona 출력 + 합성안을 사용자에게 표시하고 `AskUserQuestion`으로 확정:

```
AskUserQuestion(
  question="lateral-thinking 결과 — 어느 안으로 진행할까?",
  options=[
    {label: "합성안", description: "{한 줄 요약}"},
    {label: "Hacker 안", description: "{한 줄 요약}"},
    {label: "Researcher 안", description: "{한 줄 요약 + 1차 소스 링크}"},
    {label: "Simplifier 안", description: "{한 줄 요약}"},
    {label: "Architect 안", description: "{한 줄 요약}"}
  ]
)
```

선택된 안은 chok-fix / chok-debug로 입력 컨텍스트로 전달.

## Output Schema

```xml
<chok-unstuck-output>
  <trigger-source enum="auto|manual" />
  <stagnation-evidence>
    <failed-attempts count="N">
      <attempt n="1" approach="..." why-failed="..." />
      <attempt n="2" approach="..." why-failed="..." />
    </failed-attempts>
  </stagnation-evidence>
  <persona-outputs>
    <persona name="hacker">{대안 1 — 100단어 이하}</persona>
    <persona name="researcher">{대안 + 인용 URL 3개}</persona>
    <persona name="simplifier">{대안 — 제거할 부분}</persona>
    <persona name="architect">{대안 — 패러다임 변경}</persona>
    <persona name="contrarian">{가정 의심 + 재정의 시 대안}</persona>
  </persona-outputs>
  <synthesis>
    <core-change>{핵심 변경}</core-change>
    <fallback>{실패 시 대안}</fallback>
    <verification-criteria>{성공 판정 기준}</verification-criteria>
    <reversibility enum="reversible|irreversible|partial" />
  </synthesis>
  <user-decision>
    <selected enum="synthesis|hacker|researcher|simplifier|architect|abort" />
    <handoff-target enum="chok-fix|chok-debug|chok-auto|none" />
  </user-decision>
</chok-unstuck-output>
```

## Boundaries

**Will:**
- 5 persona 독립 발산 (단일 모델 편향 제거)
- 합성안 + reversibility 분류
- 사용자 확정 게이트 강제 (lateral 결과를 자동 적용 금지)
- chok-fix / chok-debug에 선택된 안 핸드오프

**Won't:**
- 코드 직접 수정 (읽기 전용 + 권고만)
- 합성안 자동 적용 (사용자 confirm 없이)
- contrarian persona의 "가정 의심"을 추측으로 결론
- 같은 세션에서 같은 stagnation에 대해 2회 이상 발동 (피드백 루프 방지)

### "같은 stagnation" 감지 알고리즘

피드백 루프 방지를 위해, 발동 시점에 stagnation fingerprint를 계산하여 세션-스코프 캐시와 비교:

```xml
<stagnation-fingerprint>
  <compute>
    fingerprint = sha256(
      sorted(failed_attempts[].approach) +
      sorted(failed_attempts[].why-failed) +
      original_problem_statement[:200]
    )[:16]  # 앞 16자리만 사용
  </compute>
  <cache>~/.claude/projects/{slug}/state/chok-unstuck-fingerprints.json (세션 단위)</cache>
  <check>
    if fingerprint in cache AND cache[fingerprint].invocations >= 2:
      abort with message "이 stagnation에 대해 이미 2회 발동했습니다. chok-supervisor 에스컬레이션 권장."
      → 사용자에게 escalation 옵션 제시 (chok-supervisor / 사용자 수동 개입)
    else:
      cache[fingerprint].invocations += 1
      proceed
  </check>
  <ttl>세션 종료 시 cache 자동 폐기 (다른 세션에서는 재발동 가능)</ttl>
</stagnation-fingerprint>
```

이 메커니즘은 "에이전트가 chok-unstuck → 시도 → 실패 → chok-unstuck → 시도 → 실패"의 재귀 루프를 깬다.

## Retrospective (Phase 5)

`~/.claude/skills/shared/retrospective-protocol.md` 적용. 3-Dimension 평가:

| 관점 | 평가 내용 |
|------|----------|
| Persona Diversity | 5 persona가 실제로 다른 axis에서 답했는가? 비슷한 답 cluster되었는가? |
| Synthesis Quality | 합성안이 단순 평균이 아닌 진짜 합성이었는가? user가 select했는가? |
| Unblocking Effectiveness | chok-unstuck 후 fix/debug가 실제로 진전했는가? (다음 verify cycle에서 issue 감소?) |

저장: `[PATTERN]` 성공 패턴(어느 persona가 자주 채택되는지), `[GOTCHA]` 5 persona가 모두 잘못 본 케이스.
