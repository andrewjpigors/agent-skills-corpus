---
name: chok-auto
description: "9-stage iterative development pipeline: Analysis → Tech Review → Test → Plan → Review → Implement → Code Review → QA → Decision (max 3 rounds). Failure analysis report after exhaustion."
origin: custom
triggers:
  keywords: [구현, 개발, feature, 리팩토링, PR, 전체 파이프라인]
  type: execute
  model-hint: sonnet
---

# chok-auto v2.0 — 9-Stage Iterative Development Pipeline

9단계 능동형 개발 파이프라인을 하나의 명령으로 자동 실행한다.
분석 → 기술검토 → 테스트 → 계획 → 검토 → 구현 → 구현검토 → QA → 이슈판정.
최대 3회 라운드 반복. 3회 후에도 미해결 시 실패 분석 보고서를 작성한다.

## Usage

```
/chok-auto [trigger] [--mode develop|debug|refactor|verify|full]
                      [--max-rounds 3]
                      [--strict]
                      [--pr]
                      [--skip-research]
                      [--skip-tests]
```

### Triggers (진입점)

| Trigger | 예시 | 모드 | 시작 |
|---------|------|------|------|
| 에러 메시지 | `"TypeError: Cannot read property"` | debug | Stage 1 |
| 테스트 실패 | `"3 tests failed"` | debug | Stage 1 |
| 기능 설명 | `"위키링크 편집 모드 구현"` | develop | Stage 1 |
| 리팩토링 요청 | `"인증 모듈 리팩토링"` | refactor | Stage 1 |
| 코드 변경 완료 | `"구현 완료"` | verify | Stage 7 |
| PR 생성 전 | `--pr` | pr | Stage 7 |
| 없음 (빈 호출) | `/chok-auto` | verify | Stage 8 |

### Options

| Option | 설명 | 기본값 |
|--------|------|--------|
| `--mode develop` | 전체 9단계 개발 파이프라인 | 자동 감지 |
| `--mode debug` | 디버그 중심 (Stage 1에서 chok-debug 연동) | 자동 감지 |
| `--mode refactor` | 리팩토링 중심 (Stage 3에서 회귀 테스트 중심) | 자동 감지 |
| `--mode verify` | 검증만 (Stage 7부터) | 자동 감지 |
| `--mode full` | 전체 강제 실행 | 자동 감지 |
| `--max-rounds` | 전체 파이프라인 반복 최대 횟수 | `3` |
| `--strict` | 경고도 실패로 처리 | `false` |
| `--pr` | PR 준비 모드 (pre-pr 검증 + eval) | `false` |
| `--skip-research` | Stage 2 (기술검토) 건너뛰기 | `false` |
| `--skip-tests` | Stage 3 (테스트 구축) 건너뛰기 (비권장) | `false` |

## Smart Routing (자동 진입점 결정)

트리거를 분석하여 최적의 모드와 시작 지점을 자동 결정한다:

```xml
<smart-routing priority-order="explicit-mode > pr-flag > keyword-detection > empty-input">
  <route condition="--mode full explicitly set" mode="full" start="stage-1" />
  <route condition="--pr flag present" mode="pr" start="stage-7" />
  <route condition="error message or stack trace detected" mode="debug" start="stage-1" />
  <route condition="keywords: 실패, 에러, 버그" mode="debug" start="stage-1" />
  <route condition="keywords: 구현, 추가, feature description" mode="develop" start="stage-1" />
  <route condition="keywords: 리팩토링, 개선, 정리" mode="refactor" start="stage-1" />
  <route condition="keywords: 완료, 구현 완료" mode="verify" start="stage-7" />
  <route condition="empty input" mode="verify" start="stage-8" />
</smart-routing>
```

### Lightweight Mode (간소 경로)

다음 조건을 **모두** 만족하면 간소 경로를 자동 적용한다:
- Stage 1 분석 결과 `estimated-complexity: low`
- `affected-files` ≤ 1개
- 해당 파일에 기존 테스트 커버리지 존재

간소 경로: **Stage 1 → 6 → 7 → 9** (테스트 작성·계획·QA 생략, 구현검토에서 품질 확인)

## Mode-Specific Stage Execution

| Mode | 실행 Stage | 비고 |
|------|-----------|------|
| `develop` | 1→2→3→4→5→6→7→8→9 | 전체 파이프라인 |
| `debug` | 1→2→3→4→5→6→7→8→9 | Stage 1에서 chok-debug 연동 |
| `refactor` | 1→2→3→4→5→6→7→8→9 | Stage 3에서 회귀 테스트 중심 |
| `verify` | 7→8→9 | 구현 완료 후 검증만 |
| `pr` | 7→8→9 | Stage 8에서 pre-pr 모드 |
| `full` | 1→2→3→4→5→6→7→8→9 | 모드 무관 전체 강제 |
| `lightweight` | 1→6→7→9 | 자동 판정 (조건 충족 시) |

---

## Pipeline Overview

```
Round N/3
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Stage 1  │→│ Stage 2  │→│ Stage 3  │→│ Stage 4  │→│ Stage 5  │
│ 분석     │  │ 기술검토  │  │ 테스트   │  │ 구현계획  │  │ 계획검토  │
│ Analysis │  │ Tech Rev │  │ Test Bld │  │ Impl Plan│  │ Plan Rev │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └────┬─────┘
                                                              │
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│ Stage 9  │←│ Stage 8  │←│ Stage 7  │←│ Stage 6  │←──────┘
│ 이슈판정  │  │ QA       │  │ 구현검토  │  │ 구현진행  │
│ Decision │  │          │  │ Code Rev │  │   Impl   │
└────┬─────┘  └──────────┘  └──────────┘  └──────────┘
     │
     ├─ PASS → 성공 리포트
     ├─ FAIL + round < max → Stage 1로 복귀 (범위 축소)
     └─ FAIL + round >= max → 실패 분석 보고서
```

---

## Stages 1-9 — 한-문단 요약

각 Stage의 전체 절차/도구/출력 내용: Read("~/.claude/skills/chok-auto/references/stages.md")

### Stage 1: Analysis (분석)

현재 코드베이스 상태를 파악하고 변경 범위를 식별한다. 도구: project-scan skill + Bash(git status/diff/log, 읽기 전용) + Glob/Grep/Read, debug 모드는 chok-debug Phase 1-2 재사용. 출력은 영향 범위·코드베이스 상태·요구사항 요약으로, **Stage 2(기술검토)** 입력이 된다. Stage 1 상세 절차: Read("~/.claude/skills/chok-auto/references/stages.md")

### Stage 2: Technical Review (기술검토 — `chok-techreview` 위임)

`chok-techreview` 스킬로 위임하여 4-lens 분석(트레이드오프/SOTA/보안-성능/의존성)을 적용한다. 미설치 시 inline 4-lens fallback(WebSearch + Context7 MCP + Grep). `--skip-research`로 생략 가능, Round 2+는 미해결 이슈 관련만 추가 조사. 결과 4-lens schema는 **Stage 4(구현계획)**로 전달된다. Stage 2 상세 절차(graceful fallback / 위임 XML / 코드베이스 패턴 보강): Read("~/.claude/skills/chok-auto/references/stages.md")

### Stage 3: Test Case Building (테스트 케이스 구축)

TDD 방식으로 구현 전 테스트를 먼저 작성한다. 도구: tdd-guide agent(단위/통합 RED-first) + chok-test skill(FE surface 감지 시 E2E/UI/조건 위임) + Bash + Write/Edit. `--skip-tests`로 생략 가능(경고), Round 2+는 건너뜀(Round 1 테스트 재사용). 테스트 명세는 **Stage 4(구현계획)**의 수락 기준이 된다. Stage 3 상세 절차(layer-split XML / 도구별 분담): Read("~/.claude/skills/chok-auto/references/stages.md")

### Stage 4: Implementation Plan (구현계획)

상세 구현 단계를 계획한다. **Pre-flight Conflict Detection**(변경 파일 충돌 사전 감지)을 먼저 실행하여 계획 시작 전 모든 충돌을 일괄 surface한다. 이후 planner agent + Read/Grep/Glob로 Stage 1-3 결과(파일 기반 핸드오프)를 받아 순서화된 단계·파일별 변경·의존성 순서·복잡도·테스트 매핑을 구조화된 체크리스트로 출력. Round 2+는 미해결 이슈 수정 계획만(범위 축소). 출력은 **Stage 5(계획검토)**로 전달된다. Stage 4 상세 절차: Read("~/.claude/skills/chok-auto/references/stages.md")

### Stage 5: Plan Review (계획 검토)

계획을 테스트·요구사항·아키텍처 규칙에 대해 검증한다. 도구: architect agent + 직접 테스트 커버리지 교차 확인. FSD/순환 의존성/파일 크기/TS Strict 검증 + Karpathy 원칙(P1-P4) 검증, 최대 2회 수정 반복. 통과(approved) 후 **Stage 6(구현)**로 진행한다. Stage 5 상세 절차(Karpathy 원칙 검증 포함): Read("~/.claude/skills/chok-auto/references/stages.md")

### Stage 6: Implementation (구현 진행)

계획을 단계별로 실행한다. 독립 태스크는 git worktree로 격리하여 신규 subagent에서 병렬 실행(Superpowers 패턴), 의존 태스크는 직렬 유지. 도구: Write/Edit + Bash(worktree) + Agent tool(모델 티어링) + chok-fix Stage 4 티어링 로직. 출력은 AC tree HUD(per-AC pass/fail matrix). GREEN 확인 후 **Stage 7(구현검토)**로 진행한다. Stage 6 상세 절차(worktree pre-flight/생성/merge/cleanup bash 블록 + AC-tree HUD 스키마 + AC-ID 안정성 XML): Read("~/.claude/skills/chok-auto/references/stages.md")

### Stage 7: Implementation Review (구현 검토)

구현 결과를 코드 리뷰와 보안 검토한다. 도구: code-reviewer + security-reviewer agent(병렬) + Bash(git diff). 이슈를 CRITICAL/HIGH/MEDIUM/LOW로 분류하여 CRITICAL은 Stage 6 복귀(최대 2회). 판정 후 **Stage 8(QA)**로 진행한다. Stage 7 상세 절차: Read("~/.claude/skills/chok-auto/references/stages.md")

### Stage 8: QA (QA 진행)

구현의 종합적인 품질을 검증한다. `/chok-verify` 실행(`--pr`→pre-pr, 기본→full, `--strict`→경고도 실패), 수정 가능 이슈는 `/chok-fix` → 재검증. QA 결과는 **Stage 9(판정)**로 전달된다. Stage 8 상세 절차: Read("~/.claude/skills/chok-auto/references/stages.md")

### Stage 9: Decision (이슈 판정)

파이프라인을 완료하거나 다음 라운드로 진행할지 판정한다. 도구 없음(로직만), Stage 7-8 결과 기반. remaining_issues == 0 → 성공 리포트, > 0 AND round < max → carry_forward 갱신 후 **Stage 1 복귀**, round >= max → 실패 분석 보고서. Stage 9 상세 절차(판정 로직 의사코드): Read("~/.claude/skills/chok-auto/references/stages.md")

---

## Round Management (라운드 관리)

### 파이프라인 상태

```xml
<pipeline-state>
  <current-round type="integer">1</current-round>
  <max-rounds type="integer">3</max-rounds>
  <stages type="object" />
  <carry-forward>
    <remaining-issues type="array" />
    <attempted-fixes type="array" />
    <narrowed-scope type="object|null" />
  </carry-forward>
</pipeline-state>
```

### 라운드별 동작 차이

| Stage | Round 1 | Round 2+ |
|-------|---------|----------|
| Stage 1 (분석) | 전체 범위 분석 | 미해결 이슈 범위만 재분석 |
| Stage 2 (기술검토) | 전체 조사 | 미해결 이슈 관련만 추가 조사 |
| Stage 3 (테스트) | 전체 테스트 작성 | **건너뜀** (Round 1 테스트 재사용) |
| Stage 4 (구현계획) | 전체 계획 | 미해결 이슈 수정 계획만 |
| Stage 5 (계획검토) | 전체 검토 | 축소된 범위 검토 |
| Stage 6 (구현) | 전체 구현 | 수정분만 구현 |
| Stage 7 (구현검토) | 전체 리뷰 | 새 변경분만 리뷰 |
| Stage 8 (QA) | 전체 검증 (항상 full) | 전체 검증 (항상 full) |
| Stage 9 (판정) | 동일 | 동일 |

---

## Success Report (성공 리포트)

Read("~/.claude/skills/chok-auto/report-templates.md") 의 "Success Report" 섹션을 참조하여 리포트를 생성한다.
각 Stage별 실제 실행 결과(파일 수, 테스트 수, 이슈 수 등)를 템플릿에 반영한다.

---

## Failure Analysis Report (실패 분석 보고서)

3회 라운드 소진 후에도 미해결 이슈가 있을 때 생성한다.
Read("~/.claude/skills/chok-auto/report-templates.md") 의 "Failure Analysis Report" 섹션을 참조하여 리포트를 생성한다.

---

## Autonomous Execution (완전 자동 실행)

사용자 확인 없이 끝까지 자동 진행한다. 중간에 멈추지 않는다.

### No-Stop 원칙

```
1. 사용자에게 질문하지 않는다
2. 확인을 요청하지 않는다
3. 중간에 멈추지 않는다
4. 모든 결정은 자동으로 내린다
5. 최종 리포트에서 모든 결과를 한번에 보고한다
```

### 자동 처리 규칙

| 상황 | 자동 동작 |
|------|----------|
| CRITICAL 이슈 (빌드 실패) | 자동 수정 시도 → 실패 시 리포트에 기록 후 계속 |
| 시크릿 노출 감지 | 자동 제거 + 환경변수로 전환 |
| chok-debug 3회 실패 | 로그 기록 후 현재 상태로 다음 Stage 진행 |
| Stage 5 계획 검토 실패 | 최대 2회 수정 → 경고와 함께 진행 |
| Stage 7 CRITICAL 리뷰 이슈 | Stage 6 복귀 (최대 2회) → 이후 리포트에 기록 |
| max-rounds 초과 | 실패 분석 보고서 생성 후 완료 |
| Config Tamper 감지 | 자동 롤백 (`git checkout`) 후 계속 |
| 부분 실패 | 수정 가능한 것은 수정, 불가능한 것은 리포트 |

### 자동 결정 기준

```xml
<auto-decision-tree>
  <check condition="tool-auto-fixable" action="fix-immediately" />
  <check condition="agent-delegation-possible" action="delegate-to-agent" />
  <check condition="pattern-matching-fixable" action="apply-pattern" />
  <fallback action="tag-MANUAL_REQUIRED-and-continue" />
</auto-decision-tree>
```

---

## Stage Handoff (파일 기반 전달)

Stage 간 결과를 프롬프트에 직접 붙이지 않고 **파일로 전달**하여 토큰을 절약한다 (Superpowers v6 패턴).

```
.claude/state/chok-auto/
├── stage-1-analysis.json      # Stage 1 → Stage 2, 4 입력
├── stage-2-techreview.json    # Stage 2 → Stage 4 입력
├── stage-3-tests.json         # Stage 3 → Stage 4, 5 입력
├── stage-4-plan.json          # Stage 4 → Stage 5, 6 입력
├── stage-6-impl-result.json   # Stage 6 → Stage 7 입력
├── stage-7-review.json        # Stage 7 → Stage 9 입력
└── stage-8-qa.json            # Stage 8 → Stage 9 입력
```

**JSON 스키마** (각 파일의 필수 필드):

```json
{
  "stage": 1,
  "round": 1,
  "timestamp": "{ISO8601}",
  "status": "completed|failed|partial",
  "summary": "1-2줄 핵심 결과",
  "data": { /* stage별 고유 데이터 */ },
  "next_stages": [2, 4]
}
```

| 파일 | `data` 필드 |
|------|------------|
| stage-1-analysis | `affected_files`, `complexity`, `requirements`, `codebase_state` |
| stage-2-techreview | `lens_results`, `recommendations`, `risks` |
| stage-3-tests | `test_files`, `coverage_map`, `red_tests` |
| stage-4-plan | `steps[]`, `dependencies`, `conflict_resolution` |
| stage-6-impl-result | `changed_files`, `ac_tree`, `green_tests` |
| stage-7-review | `issues[]`, `severity_counts`, `verdict` |
| stage-8-qa | `verify_result`, `fix_applied`, `final_verdict` |

**핸드오프 규칙**:
- 각 Stage 완료 시 결과를 위 경로에 JSON으로 Write
- 다음 Stage는 필요한 이전 Stage 파일을 Read로 로드
- 프롬프트에는 파일 경로만 전달 (내용 X)
- Round 2+에서는 이전 라운드 파일을 덮어쓰기 (최신 상태만 유지)
- 파이프라인 성공 시 `.claude/state/chok-auto/` 자동 정리, 실패 시 디버깅용 보존

---

## Parallel Execution & Workflow Integration

병렬 가능 단계(Stage 2/7/8 내부) vs 순차 필수 단계 정책, 그리고 모드별 워크플로 사용 예시(새 기능/버그 수정/리팩토링/검증/PR/빠른 검증)는 references로 분리: Read("~/.claude/skills/chok-auto/references/integration-examples.md")

---

## Stage 10: Retrospective (회고)

파이프라인 종료 후 전체 과정을 종합 회고한다. **성공/실패 양쪽 모두에서 실행한다.**

회고 프로토콜: Read("~/.claude/skills/shared/retrospective-protocol.md")

### 이 스킬의 평가 관점

| 관점 | 평가 내용 | 만점 |
|------|----------|------|
| **Process Fidelity** | 9단계를 충실히 따랐는가? 건너뛴 단계가 있는가? Iron Law 위반이 있었는가? | /5 |
| **Outcome Accuracy** | 원래 목표를 달성했는가? 불필요한 scope creep이 있었는가? | /5 |
| **Efficiency** | 라운드 수, 모델 티어링이 적절했는가? 불필요한 반복이 있었는가? | /5 |

### 고유 분석: 3-Level 개선 행동

학습 추출 후 3가지 레벨로 개선 행동을 도출한다:
- **[SKILL]**: chok-auto 스킬 자체 개선 (Stage 전환 로직, 모델 티어링 기준, 자동 처리 규칙)
- **[PROJECT]**: 프로젝트 레벨 개선 (코드 구조, 테스트 커버리지, 반복 이슈 근본 원인)
- **[HARNESS]**: 하네스 설정 개선 (hook, 규칙, MCP 서버, CLAUDE.md 업데이트)

## Supervisor Integration (감독관 연동)

감독관 체크포인트 프로토콜: Read("~/.claude/skills/shared/supervisor-checkpoint.md")

### 이 스킬의 체크포인트

| 시점 | 검토 질문 |
|------|----------|
| Stage 1 (분석) 완료 | "분석 범위가 정확한가? 영향 받는 모듈/파일을 놓치고 있지 않은가?" |
| Stage 3 (테스트) 완료 | "테스트 케이스가 요구사항을 충분히 커버하는가? 엣지 케이스가 누락되었는가?" |
| Stage 5 (계획검토) 완료 | "구현 계획이 논리적인가? 의존성 순서가 올바른가?" |
| Stage 6 (구현) 완료 | "구현이 계획을 충실히 따랐는가? 계획에 없는 변경이 포함되지 않았는가?" |
| Stage 8 (QA) 완료 | "검증이 충분했는가? 통과 판정이 타당한가? 실제 서비스 동작까지 확인했는가?" |

### 파이프라인 흐름 (감독관 포함)

```
Stage 1 → [감독관] → Stage 2 → Stage 3 → [감독관] → Stage 4 → Stage 5 → [감독관]
    → Stage 6 → [감독관] → Stage 7 → Stage 8 → [감독관] → Stage 9 → Stage 10 (Retrospective)
```

## Boundaries

**Will:**
- 트리거를 분석하여 최적 모드와 시작점 자동 결정
- 9단계 파이프라인 자율 실행 (분석 → 기술검토 → 테스트 → 계획 → 검토 → 구현 → 구현검토 → QA → 판정)
- Context7 MCP + WebSearch로 최신 기술 문서 조사
- TDD 방식으로 테스트 선행 작성 (RED → GREEN)
- 코드 리뷰 + 보안 리뷰 병렬 실행
- 최대 3회 라운드 반복 (범위 자동 축소)
- 실패 시 라운드별 히스토리 + 근본 원인 분석 + 수동 수정 권고 보고서 생성
- 성공 시 10개 Stage 통합 리포트 출력 (Retrospective 포함)
- 회고에서 추출된 교훈을 auto-memory에 저장하여 다음 세션에 반영

**Won't:**
- max-rounds 초과 시 무한 반복
- 린터/포맷터 설정 변경으로 이슈 우회
- 증거 없이 성공 선언
- 테스트 없이 GREEN 상태 주장
