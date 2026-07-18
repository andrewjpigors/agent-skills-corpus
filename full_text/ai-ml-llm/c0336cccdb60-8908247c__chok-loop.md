---
name: chok-loop
description: "Loop engineering 스킬 — 신뢰할 수 있는 agentic loop를 설계·실행한다. 2레이어: (1) Advisory(--mode design): 작업 형태를 분석해 최적 루프 패턴(Ralph-reset / in-session-resume / bounded-round / fan-out)을 선택·추천하고 비-Ralph는 기존 스킬로 핸드오프. (2) Executor(--mode generate): 정통 Ralph 셸 하니스(PROMPT.md + loop.sh + check_done.sh + state/)를 생성 — 매 iteration 새 claude -p 프로세스로 진짜 context reset, 파일시스템을 메모리로, done 증명 시 종료. 세션 밖 터미널에서 자율 실행. 트리거: '루프 만들어', 'ralph loop', '밤새 돌려', 'loop engineering', '자율 루프'."
origin: custom
triggers:
  keywords: [루프 만들어, ralph loop, ralph 루프, 밤새 돌려, loop engineering, 루프 엔지니어링, 자율 루프, autonomous loop]
  type: execute
  model-hint: sonnet
---

# chok-loop — 루프 엔지니어링

신뢰할 수 있는 agentic loop를 **설계**하고 **실행**한다.

Loop engineering = plan→act→observe 사이클을 done이 *증명될 때까지* 반복하되, context rot·폭주·무한루프 없이 돌아가게 만드는 공학. 핵심 기법 **Ralph loop**: 무한 셸 루프가 매 iteration마다 **새 프로세스**(`claude -p`)를 띄워 프롬프트 파일을 다시 읽고, 대화 누적 대신 **파일시스템을 메모리로** 쓰며, 매 반복 **context를 완전히 리셋**한다.

> 패턴 근거·1차 소스: `Read("~/.claude/skills/chok-loop/references/pattern-decision.md")`

## 기존 chok 루프와의 차별 (비중복)

| 패턴 | 실행 위치 | 담당 스킬 |
|------|-----------|-----------|
| **Ralph-reset** (매 iter fresh process) | **세션 밖 셸** | **chok-loop** ← 이 빈자리 |
| in-session-resume (ScheduleWakeup) | 세션 내 | chok-auto-agent |
| bounded-round (max 3) | 세션 내 | chok-auto / chok-fix |
| fan-out (병렬 subtask) | 세션 내 | chok-dev-agents |

chok-loop는 **Ralph만 직접 실행**한다. 나머지 패턴이 맞으면 해당 스킬로 핸드오프(설계 모드의 책무).

## Usage

```
/chok-loop [--mode design|generate] [--goal "..."] [options]
```

| Arg | 설명 | 기본값 |
|-----|------|--------|
| `--mode` | `design`(패턴 추천) / `generate`(Ralph 하니스 생성) | `design` |
| `--goal` | 루프가 달성할 목표 (자연어) | (필수) |
| `--out` | 하니스 생성 위치 | `.ralph/` |
| `--max-iter` | iteration 상한 (폭주 가드) | `50` |
| `--branch` | 작업 전용 브랜치명 | 자동 `ralph/<topic>` |
| `--test-cmd` | green 판정 네이티브 러너 (예: `pytest -q`) | 자동 감지 시도 |
| `--task-file` | 체크박스 소진 판정 파일 | `docs/tasks.md` |
| `--model` | iteration 에이전트 모델 | `sonnet` |
| `--dry-run` | 생성/실행 없이 계획만 출력 | `false` |

### Examples

```bash
/chok-loop --goal "결제 모듈 리팩토링"                          # design: 패턴 추천
/chok-loop --mode generate --goal "tasks.md 전부 구현" --test-cmd "pytest -q"
/chok-loop --mode generate --goal "..." --out /tmp/ralph --max-iter 20 --dry-run
```

## Mode 1: design (기본) — 패턴 선택

목표·작업 형태를 받아 결정 트리를 적용하고 최적 루프 패턴을 추천한다.

```
Read("~/.claude/skills/chok-loop/references/pattern-decision.md")  # 결정 트리 + 핸드오프 표
```

결정 요지:
- 장시간/밤샘 + context 누적 시 rot + 명확한 done 신호 → **Ralph-reset** → `--mode generate`로 연결 제안
- 토큰 소진 가능 + 세션 연속성 필요 → **in-session-resume** → `/loop chok-auto-agent` 핸드오프
- 범위 좁고 3라운드 내 수렴 기대 → **bounded-round** → `/chok-auto` 또는 `/chok-fix` 핸드오프
- 독립 병렬 subtask 다수 → **fan-out** → `/chok-dev-agents` 핸드오프

출력: 추천 패턴 1개 + 사유 + (Ralph면) generate 실행 제안. 모호하면 `AskUserQuestion`으로 사용자 확인.

## Mode 2: generate — Ralph 셸 하니스 생성

`--out` 디렉터리에 정통 Ralph 하니스 4종을 생성한다. **세션 밖 터미널에서 사용자가 실행.**

```
Read("~/.claude/skills/chok-loop/references/ralph-harness.md")  # 파일 템플릿 전문
Read("~/.claude/skills/chok-loop/references/guardrails.md")     # 가드레일 상세
```

### 생성 절차

1. **선결 검증**: cwd가 git repo인지 확인 (아니면 중단·경고). `--test-cmd` 미지정 시 네이티브 러너 자동 감지(pytest/jest/go test/npm test). `--task-file` 존재 확인.
2. **전용 브랜치 결정**: `--branch` 또는 자동 `ralph/<topic>` (★ 기본값 — main에서 자율 실행 금지). 하니스가 첫 실행 시 브랜치 생성.
3. **파일 생성** (`--dry-run`이면 미생성, 계획만 출력):
   - `PROMPT.md` — 매 iteration 재독되는 프롬프트. 목표 / 상태 위치 / done 정의 / **"한 단위 작업만 하고 종료"** 규율 / context 위생 / 막히면 chok-fix·chok-unstuck, 검증은 chok-test 호출 지시. (※ 스킬 호출은 PROMPT.md 안에서만 — 셸에서 직접 호출 불가)
   - `loop.sh` — while 루프 (가드레일·순서 고정, 아래 ★ 참조)
   - `check_done.sh` — **raw 명령만**: `grep -c` tasks.md 소진 OR `--test-cmd` green
   - `README.md` — 실행/중단/재개법 + 안전 경고
   - `state/` — 파일시스템 메모리(진행 노트·iteration 로그·cost 로그·counters)
4. **안전 경고 출력**: `--dangerously-skip-permissions` 자율 실행 의미, 전용 브랜치 권고, STOP 파일 사용법을 사용자에게 크게 알림.

### ★ 레이어 분리 (필수)

- **셸 게이트(loop.sh/check_done.sh)** = bash → **raw 명령만** (`grep`, `git`, `--test-cmd`). 스킬 호출 불가.
- **chok-test·chok-fix·chok-unstuck** = 스킬 → **PROMPT.md 안**(매 iteration `claude -p` 에이전트)에서만 호출.

이 경계를 흐리면 하니스가 실행되지 않는다.

### ★ loop.sh 핵심 순서 (가드레일)

```
STOP 파일 확인 → counters 로드(state/counters, 영속) → max-iter 확인
→ HEAD_BEFORE 캡처 → claude -p (fresh process) → [진전 판정: commit 前 git diff]
→ check_done.sh → (done이면 탈출) → git commit 체크포인트
→ fail/no-progress 카운터 갱신 → 3연속 실패 OR 무진전 N회 → halt(NEEDS_ATTENTION.md)
→ counters·cost 기록
```

- **진전 판정은 반드시 commit 前** (commit 후 diff는 항상 비어 오탐).
- **카운터는 state/counters 파일에 영속** (재실행=재개 보장).
- CLI에 `--max-turns` 없음 → iteration당 turn 제한은 PROMPT.md "한 단위만" 규율로.

상세: `Read("~/.claude/skills/chok-loop/references/guardrails.md")`

## 종료 조건 (done 증명)

- **성공 done** = `check_done.sh` 0 반환 = (tasks.md 체크박스 전부 `[x]` 소진) **OR** (`--test-cmd` green).
- **실패 halt** = 3연속 iteration 실패 → 루프 정지 + `NEEDS_ATTENTION.md`에 마지막 에러·원인 후보 기록 → **사용자에 원인 확인 요청** (자동 진행 안 함).
- **무진전 halt** = N회 연속 변경 없음/같은 에러 반복 → 정지 (chok-unstuck 핸드오프 가능).
- **상한 halt** = iteration ≥ `--max-iter`.

## 가드레일 (전부 적용)

1. **iteration 상한** (`--max-iter`, 기본 50)
2. **git 체크포인트** — 매 iteration 성공분 commit, rollback 가능
3. **무진전 감지** — no-progress halt
4. **킬스위치 + 비용 메모** — `touch <out>/STOP`으로 즉시 중단, `state/cost.log`에 iteration당 비용/시간

## 보안 (Won't / 주의)

- `--dangerously-skip-permissions`는 자율 실행에 필요하나 위험 → **전용 브랜치 기본 + 매-iter commit + STOP 킬스위치**로 완화. README·생성 출력에서 크게 경고.
- chok-loop는 하니스를 **생성·검증**할 뿐, 세션 안에서 루프를 자동 실행하지 않는다(실행은 사용자가 터미널에서).
- 자격증명 입력·권한변경·외부 전송 등 금지 행위는 PROMPT.md에 포함하지 않는다.

## Handoff

- 패턴이 Ralph가 아니면 → chok-auto-agent / chok-auto / chok-fix / chok-dev-agents
- 막힘(무진전 halt) → chok-unstuck
- 하니스 검증/QA → chok-verify, chok-test
- 메타 검토 → chok-supervisor

## Boundaries

**Will**: 루프 패턴 추천, Ralph 셸 하니스 생성·검증, 가드레일·종료조건 내장, 기존 스킬 핸드오프.
**Won't**: 세션 내 루프 자동 실행, 일반 루프-패턴 카탈로그/감사(→ chok-harness), 코드 직접 수정(생성된 하니스가 수행), 비-git 디렉터리에서 하니스 생성.
