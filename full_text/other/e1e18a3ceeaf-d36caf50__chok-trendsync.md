---
name: chok-trendsync
description: "최신 트렌드 추적 + 업데이트 권고 스킬. Claude Code skill 생태계(superpowers / gstack / SuperClaude / Ouroboros / anthropics official / agentskills.io / arxiv) 최신 변화를 화이트리스트 도메인에서 fan-out 수집하여 chok-* 현 구현과의 갭을 자동 진단한다. 효과 추정 (impact × risk × effort) 매트릭스로 적용 우선순위 산출 + 사용자 일괄 컨펌. 트리거: '최신 트렌드 확인', '업데이트 체크', 'chok-trendsync'."
origin: custom
triggers:
  keywords: [최신 트렌드, 업데이트 확인, 새로 나온, what's new]
  type: research
  model-hint: sonnet
---

# chok-trendsync — 트렌드 추적 + 업데이트 권고 스킬

Claude Code skill 생태계는 빠르게 변한다 — 새로운 스킬·플러그인·스펙이 지속적으로 출시된다. 본 스킬은 chok-* 전체 스킬이 최신 패턴에 뒤처지지 않도록 주기적으로 외부 소스를 스캔하고 갭을 진단한다.

## Sources

| 통합 요소 | 원본 | 가져온 핵심 |
|-----------|------|------------|
| 5-phase 파이프라인 | chok-trendsync 자체 설계 | fan-out → diff → gap → effect → recommend |
| 6-principle 자동결정 | gstack `autoplan` (chok-supervisor 차용) | 자동 적용 가능 vs 사용자 확인 필요 분류 |
| 화이트리스트 도메인 | binary-cuddling-diffie-agent 28-URL 시드 | 권위 있는 소스만 (커뮤니티 가십 배제) |
| baseline diff 추적 | git release notes 패턴 | trend-baseline.json (last-seen SHA + version) |

## Usage

```
/chok-trendsync [--source domain.com] [--scope plugin|skill|spec] [--auto-apply] [--dry-run]
```

| Arg | 설명 | 기본값 |
|-----|------|--------|
| `--source` | 특정 도메인만 스캔 (생략 시 화이트리스트 전체) | `all` |
| `--scope` | plugin / skill / spec / all | `all` |
| `--auto-apply` | 6-principle PASS + low risk 변경 자동 적용 시도 (사용자 컨펌 후) | `false` |
| `--dry-run` | 리포트만 생성, 적용 안 함 | `true` (기본 안전) |

### Examples

```bash
# 전체 스캔 + 리포트만
/chok-trendsync

# obra/superpowers만 빠른 체크
/chok-trendsync --source github.com/obra/superpowers

# 자동 적용 가능한 것 즉시 PR 준비
/chok-trendsync --auto-apply

# 주 1회 자동 실행 (사용자 opt-in, default off)
CronCreate({
  cron: "23 9 * * 1",      # 매주 월요일 9:23 AM (피크 시간 회피)
  prompt: "/chok-trendsync",
  durable: true
})
```

## 화이트리스트 도메인 (v1 시드)

권위 있는 소스만 — 가십/익명 블로그 배제.

```xml
<source-whitelist version="1">
  <domain name="github.com/obra/superpowers" type="canonical-skill-collection" priority="HIGH" />
  <domain name="github.com/garrytan/gstack" type="canonical-skill-collection" priority="HIGH" />
  <domain name="github.com/SuperClaude-Org/SuperClaude_Framework" type="canonical-skill-collection" priority="HIGH" />
  <domain name="github.com/Q00/ouroboros" type="evolutionary-loop-system" priority="HIGH" />
  <domain name="github.com/anthropics/claude-plugins-official" type="anthropic-official" priority="HIGHEST" />
  <domain name="agentskills.io" type="open-spec" priority="HIGHEST" />
  <domain name="code.claude.com/docs" type="anthropic-official-docs" priority="HIGHEST" />
  <domain name="anthropic.com/engineering" type="anthropic-blog" priority="HIGH" />
  <domain name="arxiv.org" type="academic" priority="MEDIUM" filter="prompt engineering | agent eval | LLM safety" />
  <domain name="blog.modelcontextprotocol.io" type="mcp-roadmap" priority="MEDIUM" />
  <!-- 추가는 사용자 명시 확인 후만 (가십 도메인 침투 방지) -->
</source-whitelist>
```

## Execution Procedure

### Phase 1: 소스 Fan-out (병렬)

각 화이트리스트 도메인에 WebSearch + WebFetch 병렬 호출.

**URL host whitelist assertion (runtime enforcement)**:

```bash
# 각 fetch 직전에 host가 whitelist에 있는지 검증
fetch_with_whitelist_check() {
  local url="$1"
  local host=$(echo "$url" | /usr/bin/sed -E 's|https?://([^/]+)/.*|\1|')

  if ! /usr/bin/grep -qF "$host" .claude/state/trend-whitelist.txt 2>/dev/null; then
    echo "⚠ Non-whitelist host detected: $host (referenced by $url)"
    # AskUserQuestion: "이 host를 화이트리스트에 추가할까요? [Yes / No (skip) / Abort]"
    return 1
  fi
  # Whitelist OK → proceed
  WebFetch "$url"
}
```

CHANGELOG/릴리즈노트가 외부 3rd-party 블로그를 인용하는 경우에도 자동 추가 금지. 사용자 명시 승인 필수.

**병렬 호출**:

```
Agent x N (parallel, single message multiple tool calls):
  for each source in whitelist:
    Agent(
      subagent_type: "general-purpose",
      prompt: "Fetch latest activity from {source.url}.
              Report: (a) new commits/releases since {baseline.last_seen}, 
                      (b) new skills/plugins added,
                      (c) changes to API/spec/schema.
              Cite each finding with exact URL. Skip unchanged sections."
    )
```

**baseline.json** (`~/.claude/projects/{slug}/state/trend-baseline.json`):

```json
{
  "github.com/obra/superpowers": {"last_seen_sha": "{SHA}", "last_seen_at": "{ISO8601_TIMESTAMP}"},
  "github.com/garrytan/gstack": {"last_seen_sha": "{SHA}", "last_seen_at": "{ISO8601_TIMESTAMP}"},
  ...
}
```

baseline 미존재 시: 최초 실행으로 간주, 현재 시점 baseline만 기록하고 diff 진단은 다음 실행부터 (false-positive 폭증 방지).

### Phase 2: Diff 감지

각 소스의 변경을 추출하여 정규화:

```xml
<diff-record>
  <source url="..." />
  <change-type enum="new-skill|new-plugin|api-change|spec-update|deprecation|security-advisory" />
  <description text="..." max-words="50" />
  <citation-url />
  <since-baseline>{prev_sha or prev_at}</since-baseline>
</diff-record>
```

릴리즈노트 / CHANGELOG가 있으면 우선 인용 (해석 정확도↑). 없으면 commit message + diff summary.

### Phase 3: 갭 분석

각 발견된 변경에 대해 chok-* 전체 스킬 SKILL.md를 grep으로 스캔:

```bash
# 패턴 이미 반영 여부 매칭
for finding in diff_records:
  pattern_keywords = extract_keywords(finding.description)
  matches = grep -l -E "{pattern_keywords}" skills/chok-*/SKILL.md
  if matches:
    finding.status = "already_reflected"
    finding.matched_files = matches
  else:
    finding.status = "gap_detected"
```

**분류**:

```xml
<gap-classification>
  <category name="importable" criteria="해당 패턴이 chok-* 도메인에 직접 적용 가능" />
  <category name="nice-to-have" criteria="유용하나 핵심 워크플로 외" />
  <category name="out-of-scope" criteria="chok-* 철학과 부합 안 함 (예: closed-source dependency)" />
  <category name="already-reflected" criteria="이미 구현됨" />
</gap-classification>
```

### Phase 4: 효과 추정 (Impact × Risk × Effort)

각 `importable` / `nice-to-have` 후보에 대해 매트릭스 산출:

```xml
<effect-estimation>
  <impact enum="LOW|MED|HIGH">기대 효과: 사용자 가치, 안정성, 정확도 개선</impact>
  <risk enum="LOW|MED|HIGH">위험: 기존 동작 깨짐, 마이그레이션 비용, 의존성 추가</risk>
  <effort-hours type="integer">예상 구현 시간 (시간 단위)</effort-hours>
</effect-estimation>
```

**6-principle rubric 적용** (chok-supervisor 차용):

```
For each candidate:
  PASS_completeness     = 변경이 모든 영향 영역을 cover하는가?
  PASS_pattern_match    = chok-* 기존 패턴과 일치하는가?
  PASS_reversibility    = 변경이 가역적인가?
  PASS_prior_user_choice = 사용자 memory에 일관된 패턴 있는가?
  PASS_defer_ambiguous  = 모호함 없는가? (모호하면 무조건 사용자 확인)
  PASS_escalate_security = 보안 영향 있는가? (있으면 무조건 사용자 확인)

auto_apply_eligible = (impact ≥ MED) AND (risk ≤ MED) AND (all 6 principles PASS)
user_confirm_required = NOT auto_apply_eligible
```

### Phase 5: 권고 리포트 + 사용자 확정

`docs/trend-sync/YYYY-MM-DD.md` 생성:

```markdown
# Trend Sync Report — {YYYY-MM-DD}

## Summary
- Sources scanned: 10
- New findings: 23
- Already reflected: 14
- Importable: 6 (3 auto-eligible, 3 user-confirm)
- Nice-to-have: 2
- Out-of-scope: 1

## Auto-eligible (사용자 일괄 컨펌)
1. [obra/superpowers] new skill `parallel-task-batch` — impact=MED, risk=LOW, effort=2h
   - 6-principle: all PASS
   - 적용 제안: chok-auto Stage 6에 worktree-batch 패턴 흡수
2. ...

## User-confirm required (개별 게이트)
1. [Q00/ouroboros] new MCP `ouroboros_drift_predictor` — impact=HIGH, risk=MED, effort=8h
   - escalate-security: PASS (read-only)
   - defer-ambiguous: FAIL (기존 drift_check와 역할 분리 필요)
   - 권고: 사용자 확인 후 chok-verify Phase 11.5에 통합 여부 결정
2. ...

## Out-of-scope
1. [3rd-party] closed-source plugin "X" — 라이선스 호환 안 함
```

**일괄 컨펌 게이트** (`AskUserQuestion`):

```
"Auto-eligible 3개 항목 일괄 적용?"
  - 항목 1: parallel-task-batch (2h)
  - 항목 2: ...
  - 항목 3: ...
선택: [전체 적용 / 개별 선택 / 모두 거부]
```

User-confirm 항목은 각각 별도 게이트로 분리 (보안/비가역 영향이 있을 수 있음).

### Phase 6: chok-supervisor 게이트

자동 적용 결정 전 chok-supervisor `--consensus` 모드로 검수 (다중 모델 합의):

```
Agent(
  subagent_type: chok-supervisor,
  prompt: "다음 trend-sync 권고를 검토하라:
            - 적용 대상: {auto-eligible 항목 목록}
            - 영향 파일: {수정 예상 파일}
            6차원 + consensus 모드로 채점하라."
)
```

verdict이 APPROVED일 때만 진행. REVISE / REJECT는 사용자 에스컬레이션.

### Phase 7: baseline 업데이트

성공/실패 무관 매 실행 마지막에 baseline.json 갱신:

```json
{
  "github.com/obra/superpowers": {"last_seen_sha": "{NEW_SHA}", "last_seen_at": "{ISO8601_TIMESTAMP}"},
  ...
}
```

→ 다음 실행이 진짜 diff만 처리하도록 보장.

**Concurrent invocation 보호 (file lock)**:

```bash
# 동시 실행 race 방지 (예: CronCreate 주 1회 + 사용자 수동 실행 겹침)
BASELINE_FILE="$HOME/.claude/projects/{slug}/state/trend-baseline.json"
LOCK_FILE="${BASELINE_FILE}.lock"

# flock 사용 가능 시 (Linux/일부 macOS Homebrew)
if /usr/bin/which flock >/dev/null 2>&1; then
  /usr/bin/flock -x -w 10 "$LOCK_FILE" -c "write_baseline_atomic $BASELINE_FILE"
else
  # macOS 기본 환경 fallback: sentinel file + PID 검증
  if [ -e "$LOCK_FILE" ] && /bin/kill -0 "$(cat $LOCK_FILE)" 2>/dev/null; then
    echo "⚠ Another chok-trendsync run in progress (PID $(cat $LOCK_FILE)). Skipping baseline update."
    exit 0
  fi
  echo $$ > "$LOCK_FILE"
  trap "rm -f $LOCK_FILE" EXIT
  write_baseline_atomic "$BASELINE_FILE"
fi

# write_baseline_atomic: 임시 파일에 기록 → mv로 atomic rename
write_baseline_atomic() {
  local target="$1"
  local tmp="${target}.tmp.$$"
  echo "{new baseline JSON}" > "$tmp" && /bin/mv "$tmp" "$target"
}
```

부분 실패 (timeout 등) 시에도 LOCK_FILE은 trap EXIT으로 자동 제거 → deadlock 방지.

## Output Schema

```xml
<trend-report>
  <timestamp type="ISO8601" />
  <sources scanned="N">
    <source url="..." status="ok|degraded|failed" findings_count="N" />
  </sources>
  <findings count="N">
    <finding id="...">
      <source-url />
      <change-type enum="new-skill|new-plugin|api-change|spec-update|deprecation|security-advisory" />
      <description max-words="50" />
      <status enum="importable|nice-to-have|out-of-scope|already-reflected" />
      <matched-chok-files type="array" />
      <effect-estimation>
        <impact enum="LOW|MED|HIGH" />
        <risk enum="LOW|MED|HIGH" />
        <effort-hours type="integer" />
      </effect-estimation>
      <six-principle-results>
        <principle name="completeness" pass="boolean" />
        <principle name="pattern-match" pass="boolean" />
        <principle name="reversibility" pass="boolean" />
        <principle name="prior-user-choice" pass="boolean" />
        <principle name="defer-ambiguous" pass="boolean" />
        <principle name="escalate-security" pass="boolean" />
      </six-principle-results>
      <auto-eligible type="boolean" />
    </finding>
  </findings>
  <recommendations>
    <auto-apply-bulk count="N" />
    <user-confirm-individual count="N" />
  </recommendations>
  <baseline-updated type="boolean" />
</trend-report>
```

## Boundaries

**Will:**
- 권위 있는 소스만 (whitelist 강제)
- Diff 기반 진단 (false-positive 최소화)
- 6-principle + chok-supervisor 다중 검수 게이트
- 사용자 일괄 컨펌 (auto-eligible) + 개별 컨펌 (user-confirm)
- baseline 추적으로 점진적 + 재현 가능한 추적

**Won't:**
- 가십/익명 블로그 자동 흡수 (whitelist 외 도메인 추가는 사용자 명시 승인 후만)
- 사용자 컨펌 없이 코드 수정 (`--auto-apply`도 컨펌 단계 통과 필수)
- 보안 영향 있는 변경의 자동 적용 (escalate-security FAIL 시 무조건 사용자 게이트)
- 동일 finding을 다음 실행에서 재추천 (baseline.json 갱신 후 silent skip)

## Retrospective (Phase 8)

3-Dimension 평가:

| 관점 | 평가 내용 |
|------|----------|
| Source Authority | whitelist 도메인이 권위 있는가? noise 제거 효과적인가? |
| Diff Precision | 변경 감지가 정확한가? false-positive / false-negative 비율은? |
| User Trust | 사용자가 권고를 신뢰하고 적용했는가? 자동 적용 후 회귀 발생 안 했는가? |

저장: `[PATTERN]` 자주 채택된 source/category, `[GOTCHA]` 잘못된 추천 사례 (false-positive 학습).
