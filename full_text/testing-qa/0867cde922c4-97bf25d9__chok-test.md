---
name: chok-test
description: "디테일 시나리오 기반 풀스택 테스트 + 빠른 보고서 스킬. **real-first(실 데이터 기본)** — 실 HTTP 서버+실 DB를 자동 기동해 실 요청→실 응답→실 영속 기준으로 테스트 생성·검증, mock은 서버 불가 시 폴백. FE(E2E/UI Playwright) + BE(단위/통합 — 프로젝트 네이티브 러너 pytest/jest/go) 둘 다 실행·보고. scenario(목적/사전조건/Given-When-Then/예상결과/tier 시나리오 — 1급), analyze(커버리지 갭+정적 진단), generate(시나리오 기반 스크립트), verify(FE+BE 실행+PFS+self-heal), report(FE 섹션=스크린샷/코드 요청·답변 + BE 섹션=실 코드 pytest 결과·실패, 대시보드 HTML — 1급 결과물), scan(전수검사+BE 스위트 감지). mock E2E는 FE 계약만, BE는 실 코드로 검증. 느슨한 핸드오프로 chok-verify/chok-debug/chok-auto와 연동."
origin: custom
triggers:
  keywords: [테스트, e2e, 화면검수, 시나리오, 테스트 만들어줘]
  type: execute
  model-hint: sonnet
---

# chok-test — 디테일 시나리오 기반 테스트 + 보고서 스킬

**시나리오를 먼저 설계하고, 그에 따라 스크립트를 분석·실행하여, 빠른 테스트 보고서를 산출**하는 QA 파이프라인. 핵심 산출물은 두 개의 문서다 — **디테일 테스트 시나리오**(`scenarios.md`)와 **테스트 보고서**(`test-report.md`). 스크립트는 시나리오를 실현하는 중간물이며, 검증 깊이는 각 시나리오의 예상결과(tier)가 결정한다.

> **설계 원칙**: 시나리오(무엇을·왜·어디까지) → 분석(스크립트가 그걸 검증하나) → 실행 → 보고서(결과·근거·갭). green이 목적이 아니라 *시나리오 충족 여부의 투명한 보고*가 목적.

## Sources

| 통합 요소 | 원본 | 가져온 핵심 |
|-----------|------|------------|
| Planner/Generator/Healer 매핑 | Playwright Test Agents v1.56+ (MS+Anthropic) | scan≈Planner, generate≈Generator, verify≈Healer. 네이티브 우선·재발명 금지 |
| Intent-based testing | 업계 표준 (testdino/shiplight) | 의도 → 테스트 자동 생성 |
| Recon-then-Action | chok-debug Step 1.6 | accessibility tree(read_page) 우선, 스크린샷 budget=3 |
| PFS Flaky 트리아지 | chok-debug Step 1.8 | flip+retry+예측불가성 단일 점수, real-bug vs flaky 분류 |
| E2E 7-tier 분류 | chok-debug Step 1.4 | liveness→smoke→standard→agentic 단계 참조 |
| 타겟 liveness + 브라우저 검증 | chok-verify Phase 6.5 / Phase 9 | 서버 up 확인 + FE UI 체크리스트 |
| Self-healing 기본화 | shiplight (selector heal 70-90%) | verify의 bounded self-heal (selector/wait만) |
| a11y(WCAG) 렌즈 | agent-team 표준 (testdino) | UI 카테고리에 역할/라벨/대비/키보드 단언 |
| 회고 / 체크포인트 | shared/retrospective-protocol.md, shared/supervisor-checkpoint.md | 3차원 회고 + 6-lens 검토 |

## Usage

```
/chok-test                      # 모드 자동 판별 (없으면 scan→scenario부터)
/chok-test scan                 # 프로젝트 전수검사 → 테스트 대상 surface 발굴
/chok-test scenario <의도>      # 디테일 테스트 시나리오 작성 → scenarios.md (1급)
/chok-test analyze              # 시나리오↔스크립트 커버리지 갭 + 기존 스크립트 정적 진단 → analysis.md
/chok-test generate [id...]     # 시나리오 기반 스크립트 생성
/chok-test verify [category]    # 작성 스크립트 실행 + PFS + self-heal
/chok-test report [--html]      # 빠른 테스트 보고서 → test-report.md (+--html: 스크린샷 임베드 test-report.html)
```

전체 흐름: `scan → scenario → analyze → generate → verify → report`. 각 모드는 독립 호출 가능.

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--framework playwright\|auto` | 테스트 프레임워크 | `auto` (감지) |
| `--category ui\|functional\|api\|condition\|all` | 대상 카테고리 | `all` |
| `--tier 2-7` | 시나리오 기본 깊이 상한 (개별 시나리오가 override) | 시나리오별 결정 |
| `--no-run` | generate 시 dry-run 생략 | `false` |

### 모드 자동 판별 규칙 (bare `/chok-test`)

```
테스트 디렉터리 없음/비어있음   → scan → scenario
scenarios.md 없음               → scenario
시나리오 있고 스크립트 갭 존재   → analyze → generate
스크립트 존재 + 미실행          → verify
실행 결과 존재 + 보고서 요청     → report
모호                           → AskUserQuestion
```

## 핵심 거버넌스

```xml
<governance>
  <iron-law>테스트는 *의도*를 반영해야 한다 — green이 목적이 아니다. 의미 없는 단언·항상 통과 테스트 금지.</iron-law>
  <recon-then-action>스크립트 작성 전 대상 정찰. accessibility tree(read_page) 우선, 스크린샷은 실패 시만 (budget=3). 브라우저 자동화 토큰 폭발 차단. (chok-debug Step 1.6)</recon-then-action>
  <native-first>Playwright가 Planner/Generator/Healer를 공식 제공(v1.56+). 재발명 금지 — 네이티브 가용 시 1차 경로, 자체 템플릿은 폴백.</native-first>
  <no-false-green>self-heal은 selector/wait 보정만. 진짜 앱 버그면 수정 금지 → chok-debug 핸드오프.</no-false-green>
  <secret-safety>생성 스크립트에 시크릿/자격증명 하드코딩 금지. env/fixture 참조만.</secret-safety>
  <real-first>**기본은 실 데이터.** 테스트 케이스는 실 HTTP 서버 + 실 DB 기준으로 생성·검증한다(실 요청→실 응답→실 영속). mock(route.fulfill/ASGITransport in-process)은 **서버를 띄울 수 없을 때만 폴백**이며, 폴백 시 보고서에 "mock(실데이터 아님)" 명시. "다 통과 ≠ 다 검증"의 근본 해소 = 실 데이터.</real-first>
  <auto-start>실 데이터 모드는 chok-test가 서버·DB를 **자동 기동**한다(아래 정책). 기동 실패 시에만 mock 폴백 + 사용자 안내.</auto-start>
  <parallel-shard>대규모 스위트는 verify를 **서브에이전트 샤딩**으로 병렬 실행한다(아래 "verify 병렬 실행"). 단 **인프라(서버·DB·브라우저)는 1회만 공유 기동** — 에이전트별 기동 절대 금지(포트 충돌·자원 폭발). 작은 스위트는 단일 프로세스 native worker 병렬로 충분(과병렬 금지).</parallel-shard>
</governance>

## 실 데이터 우선 (real-first) — 기본 정책

사용자가 "테스트 만들어줘" 하면 **실 서버+실 DB 기준**으로 만든다. mock은 폴백.

```xml
<real-first-policy>
  <detect>scan이 서버 기동 명령·포트·DB를 감지: package.json scripts(dev/start), docker-compose.yml, uvicorn/gunicorn 진입점(app.main:app), .env의 PORT/DATABASE_URL, 헬스 경로(/health,/api/health).</detect>
  <auto-start>
    실 데이터 모드 진입 시:
    1. 서버 up? (health 200 확인). 미가동이면 기동:
       - 백엔드: `uvicorn app.main:app --port N` / `npm run dev` / `docker compose up -d` (감지된 명령)
       - DB/인프라: `docker compose up -d`(postgres/redis 등)
    2. health 폴링(타임아웃 ~60s)으로 ready 확인 후 테스트.
    3. 세션 종료/모드 끝에 chok-test가 기동한 프로세스 정리(자기가 띄운 것만).
    시스템 변경(설치) 직접 실행은 안내만 — 기동/컨테이너 up은 실행.
  </auto-start>
  <generate>실 엔드포인트/페이지에 실제 요청 → 실제 응답·DB 영속을 기준으로 단언 생성. 픽스처는 실 데이터 셋업(시드/실 생성). 랜덤 합성값 최소화.</generate>
  <fallback>서버·DB 기동 불가(환경 부재)일 때만 mock. 보고서·시나리오 status에 `data: mock(fallback)` 명시 + tier 강등.</fallback>
  <safety>실 DB 변경은 테스트 DB 한정. 운영 DB 금지. 생성 데이터는 테스트 전용(랜덤 식별자) + 가능 시 정리.</safety>
</real-first-policy>
```

> FE도 기본은 실 백엔드 연동(요청→실 응답→결과화면). mock은 백엔드 불가 시 폴백. BE는 항상 실 코드. API 값흐름은 실 HTTP over-the-wire.
```

## 실전 함정 & 패턴 (dogfood 검증 — task-planner)

실제 적용에서 반복 발생한 test-bug. generate 시 **선제 적용**, verify self-heal 시 **우선 의심**.

```xml
<field-tested-rules>
  <rule id="route-order" severity="high">
    Playwright route는 **마지막 등록이 우선**. 광역 폴백(`**/api/v1/**`)을 specific route보다 *먼저* 등록하라.
    역순이면 폴백이 specific을 shadowing → continue()로 실 네트워크 타격(404/오작동). dogfood 실패 2건의 원인.
  </rule>
  <rule id="locator-hygiene" severity="high">
    `getByRole("button").last()` / 광역 name 매칭 금지. 페이지엔 프레임워크 chrome(예: Next.js Dev Tools 버튼)과
    중복 요소(사이드바 quick-add vs 메인 버튼)가 섞인다. **landmark 스코프**(`getByRole("main")`) + name exact로 좁혀라.
    strict-mode 위반·오클릭의 주범.
  </rule>
  <rule id="no-fixed-wait" severity="med">
    `waitForTimeout(ms)` 금지. `waitForResponse`/`waitForURL`/web-first assertion(auto-retry)으로 결정적 대기.
  </rule>
  <rule id="full-reload-scope" severity="high">
    `window.location.href` 류 전체 리로드는 인메모리 토큰을 잃는다 → 리로드 후 보호 라우트 도달은
    서버 middleware/httpOnly 쿠키 의존 = **mock 범위 밖**. cross-reload 네비 단언 대신 `waitForRequest`로
    요청 payload까지만 결정적 검증하고 한계를 주석으로 명시(no-false-green).
  </rule>
  <rule id="auth-genuine" severity="critical">
    보호 라우트에서 `/auth/me`를 200 직반환하면 인메모리 토큰이 안 채워져 `isAuthenticated=false` →
    테스트가 "인증이 비어서" 통과하는 **false-green**. 반드시 header-gated로:
    무토큰 → 401 → axios 인터셉터가 `/auth/refresh` → 토큰 set → 재시도(토큰 동반) → 200.
    이래야 setAuth 발화 = 진짜 인증. (verify가 자기 산출물의 false-green을 잡은 실증)
  </rule>
  <rule id="capture-context" severity="high">
    스크린샷 캡처 시 public 컷은 plain `{page}`만, authed 컷은 `{authedPage}`만 구조분해.
    둘 다 받으면 auth fixture가 같은 context에 쿠키 주입 → /login 등 public이 '인증 상태'로 리다이렉트되어
    여러 public 컷이 동일 이미지로 충돌. + 촬영 전 페이지별 main 고유 텍스트 `getByText(anchor).waitFor()` 대기
    (networkidle/body-text는 shell·사이드바로 조기 만족돼 하이드레이션 전 blank 촬영). dogfood 실측 4컷 충돌의 원인.
  </rule>
  <rule id="api-e2e-circular" severity="med">
    백엔드 단위/통합 테스트가 두터우면 mock 기반 API E2E는 순환(자기 mock 검증)이라 가치 낮음.
    실 백엔드 통합 E2E에서만 의미. scan 리포트에 "단위 커버 충분 → E2E 갭에 집중" 명시.
  </rule>
</field-tested-rules>
```

### 보호 라우트 auth fixture 레시피 (재사용)

```ts
// e2e/fixtures/auth.fixture.ts — 쿠키 seed + header-gated 세션 mock
export const test = base.extend<{ role: string; authedPage: Page }>({
  role: ["member", { option: true }],
  authedPage: async ({ page, context, baseURL, role }, use) => {
    const u = new URL(baseURL ?? "http://localhost:PORT");
    await context.addCookies([
      { name: "session", value: "active", domain: u.hostname, path: "/", sameSite: "Lax" },
      { name: "user_role", value: role, domain: u.hostname, path: "/", sameSite: "Lax" },
    ]);
    await installAuthSessionMocks(page, { roles: [role] }); // 폴백 먼저, /auth/me header-gated
    await use(page);
  },
});
```

role별 권한 경계 테스트는 describe별 `test.use({ role })`로 분리 (파일 전역 use는 전체 적용되어 양방향 테스트가 깨짐).

## 산출물: 테스트 디렉터리 (대상 프로젝트)

```
<test-dir>/         # 우선순위: 아래 폴더 정책으로 결정 (기존 재사용 > __test__/ 신규)
├── checklist.md     # 점검 단계별 리스트 = 증분 테스트-추가 드라이버
├── ui/              # 화면 UI 테스트 (스크린샷/접근성 트리 우선 + WCAG a11y)
├── functional/      # 기능 동작 테스트 (유저 플로우)
├── api/             # API 테스트 (Playwright request / supertest / httpx)
└── condition/       # 다양한 조건 (edge / error / boundary / 권한)
```

**폴더 정책** (우선순위 — 분산 방지 위해 기존 재사용 우선):
1. **Playwright `testDir` 설정값** (playwright.config의 testDir, 예: `./e2e`) 이 있으면 **그대로 사용**. config가 진실의 원천.
2. 설정 없고 기존 테스트 디렉터리(`tests/`, `e2e/`, `__tests__/`) 존재 시 → 재사용 (감지 후 사용자 1회 확인).
3. 둘 다 없을 때만 → `__test__/` 신규 생성.

> 신규 디렉터리를 만들면 config의 testDir와 어긋나 실행에서 누락된다. **항상 config·기존 관례를 1순위로.** (dogfood: task-planner는 testDir=`./e2e`라 e2e/ 재사용)
> 카테고리 하위폴더(`ui/ functional/ api/ condition/`)와 `checklist.md`는 결정된 테스트 디렉터리 *안에* 둔다.

**비-UI 프로젝트**: 웹 surface 미감지(순수 백엔드/CLI/라이브러리) 시 `ui/` 카테고리 **graceful skip**(빈 폴더 생성 안 함), functional/api/condition만.

**checklist.md = 증분 드라이버** (단순 상태표 아님): 각 항목 = `[카테고리] 점검 의도 → 매핑 스크립트 경로 → 상태(planned/generated/pass/fail/skip)`. scan이 planned 적재, generate가 planned→스크립트, verify가 상태 갱신. 사용자가 항목 추가 시 다음 generate가 해당 항목만 생성 → 커버리지 누적.

## 테스트 범위 관리 (3-tier: 전수 / 메뉴 / 단위)

지속 관리·선택 실행을 위해 테스트를 3계층으로 조직한다. `coverage-map.md`(coverage-map-template.md)가 단일 관리 지점.

```xml
<scope-tiers>
  <tier level="전수 (suite)" run="npx playwright test">
    프로젝트 전체. scan이 전 surface 인벤토리를 갱신, coverage-map 상단에 총 커버리지% 유지.
    배포 게이트·CI 전량 실행·회귀 가드용.
  </tier>
  <tier level="메뉴 (menu/feature)" run="npx playwright test --grep @menu:<name>  또는  디렉터리">
    메뉴/기능 묶음(auth / projects / tasks / documents / settings / admin …).
    각 spec title에 `@menu:<name>` 태그 → grep 선택 실행. 메뉴 개발 중 그 메뉴만 빠르게 검증.
    coverage-map에서 메뉴별 시나리오·tier·상태·커버리지% 추적.
  </tier>
  <tier level="단위 (scenario/test)" run="npx playwright test -g 'S-UI-01'">
    개별 시나리오 ID. 단일 케이스 디버그·자가수정 루프용. scenarios.md의 1건에 대응.
  </tier>
</scope-tiers>
```

**태깅 규약**: spec `test.describe`/`test` title에 `@menu:<name>` + 시나리오 ID 포함 (예: `test("@menu:auth S-UI-01 로그인 화면", …)`). → grep으로 메뉴/단위 선택 실행, ID로 scenarios.md ↔ 스크립트 ↔ 보고서 일관 추적.

**coverage-map.md 구조** (관리 단일 지점):

```
# 커버리지 맵
## 전수: surface 총 N / 커버 M / 갭 K · tier-met %
## 메뉴별
| 메뉴 | 페이지/surface | 시나리오 IDs | tier | 상태 | 커버% | 실행 |
| auth | login,register,pending | S-UI-01,02,S-CO-01..03,05,S-FN-01,02 | 2~4 | … | x% | --grep @menu:auth |
| projects | projects,overview | S-UI-03,04,S-FN-03 | 2~4 | … | y% | --grep @menu:projects |
| …
## 단위: scenarios.md 참조 (ID별 detail)
```

**운영 흐름**: scan(전수 갱신) → scenario(메뉴별 전개·ID 부여) → generate(@menu 태그 포함 생성) → verify(`--grep @menu` 메뉴별/`-g ID` 단위) → report(메뉴·전수 롤업). 신규 메뉴 추가 = scan→scenario→generate를 그 메뉴 범위로만 증분.

## BE 테스트 레이어 (실 코드 — mock 아님)

> **mock E2E의 한계**: FE를 route.fulfill mock으로 테스트하면 *프론트 동작·요청 계약*만 검증된다. **BE 로직(집계·권한·비즈니스 규칙)은 검증 0.** 풀스택 프로젝트(FE+BE)는 **BE 테스트를 별도 1급 레이어**로 함께 실행·보고해야 한다. (dogfood: task-planner BE pytest에서 mock E2E가 못 잡은 실 결함 발견.)

> **⚠ pytest "N passed" ≠ 실 서버 검증** (dogfood 교훈): task-planner에서 `pytest 699 passed`를 "실 데이터 검증"으로 보고했으나, 실측 결과 **686은 mock 단위(`AsyncMock` session)**, **13 "integration"은 in-process(`ASGITransport`)·`tmp_path`·외부DB-게이트**로 **실 over-the-wire 0건**이었다. 더 결정적으로, mock 단위가 전부 green인 상태에서 **실 over-the-wire 호출이 `GET /tasks?projectId=` HTTP 500(리스트를 튜플로 언팩)을 즉시 발견**. 단위 통과 수는 신뢰 지표가 아니다 — **실 서버 커버리지가 진짜 게이트**.

```xml
<be-layer>
  <detect>scan이 BE 테스트 스위트 감지: apps/api(pytest tests/), apps/*(jest/vitest), go(_test.go), cargo 등. 러너·경로·DB 의존 파악. **단위(mock) vs 통합(실DB) vs 실서버-필요를 구분 집계.**</detect>
  <run>verify가 **네이티브 러너로 실 BE 테스트 실행** (mock 아님). 예: `.venv/bin/pytest tests/unit -q`. DB 필요 스위트(integration)는 docker compose up 후 별도 실행 — 미가동 시 "DB 필요·미실행"로 명시(스킵 아닌 보류).</run>
  <report-split critical="true">
    BE 결과 보고 시 **반드시 3계층 분리** — 단일 "N passed"로 합산 금지(허위 신뢰):
    1. **unit(mock)**: `AsyncMock`/`MagicMock` 의존 — 실 코드 로직만, DB·네트워크 없음.
    2. **integration(in-process)**: `ASGITransport`(app 직접)·`tmp_path`·임베디드 — 실 네트워크 아님. **"실 서버"로 표기 금지.**
    3. **real over-the-wire**: 실 기동 서버에 실 소켓 호출(curl/httpx) + 실 DB 영속. **이것만 "실 검증"으로 카운트.**
    보고서는 "실 over-the-wire M건 / unit·in-process K건"을 명시. real 0건이면 결론에 "BE 실 서버 미검증" 경고 필수.
  </report-split>
  <verdict>BE 실패(또는 실 over-the-wire 결함)가 있으면 전체 결론은 **보류**(FE green·unit green 무관). 실 over-the-wire 결함 > unit mock 통과.</verdict>
  <no-mock>BE는 실 코드·실 의존(또는 fixture). mock으로 BE를 대체 검증하지 않는다(순환). 단위가 repo를 mock하면 그 위 SQL·집계는 **미검증** — 보고서에 갭으로 명시.</no-mock>
  <api-value-flow>tier4 실현 — **실 HTTP 서버 over-the-wire 호출**(uvicorn 등 실 서버 기동 → curl/httpx로 실 포트·소켓 호출). in-process(ASGITransport)·mock 금지 — 네트워크 계층까지 거친 실제 요청→응답. 단계별 실 요청 JSON→실 응답 JSON(api-flow.json) → report 'API 값흐름' 탭. "무슨 값 넣어 무슨 값 나왔나"를 실제값으로 + 데이터 영속(생성→목록 반영) 검증. 서버 미기동 시 기동(uvicorn app.main:app --port N) 후 health 확인하고 호출. (in-process는 빠르나 네트워크·CORS·미들웨어 실경로 미검증이라 '실 API'로 표기 금지.)</api-value-flow>
  <api-flow-coverage critical="true">
    api-value-flow는 auth/projects 몇 개로 끝내지 말 것 — **핵심 BE 엔드포인트를 메뉴별로 실 over-the-wire 커버**. 특히:
    · **집계 엔드포인트는 before/after 실 상태로**: 예 `GET /dashboard/summary`를 데이터 생성 전(=0)·후(=실제 카운트)로 두 번 호출해 실 GROUP BY 결과 검증(단위 mock이 못 잡는 실 SQL).
    · **list/query 엔드포인트는 실제 호출**(생성→해당 query로 read-back). query-param 분기(`?projectId=`)도 실 호출 — dogfood 500이 여기서 나옴.
    · 권한 경계(무토큰 401, 타 사용자 403) 실 호출. OpenAPI(`/api/openapi.json`)로 실 경로·페이로드 스키마 확보 후 422 시 실 required 필드로 교정.
  </api-flow-coverage>
</be-layer>
```

**FE vs BE 역할 분담**:
| 레이어 | 도구 | 검증 대상 | mock |
|--------|------|-----------|:----:|
| FE (E2E/UI) | Playwright | 화면 렌더·요청 계약·분기·권한 UI | API mock 가능 |
| **BE (unit/integration)** | pytest/jest/go (네이티브) | **로직·집계·권한·비즈니스 규칙** | **mock 금지(실 코드)** |
| 풀스택 통합 (tier4) | **실 HTTP 서버(uvicorn)** + 실 DB · curl/httpx | 데이터 영속·결과화면·네트워크 경로 | mock·in-process 제거 |

## scan 모드 — 프로젝트 전수검사 (≈Planner)

목적: 프로젝트 전체를 훑어 **테스트 대상 surface 발굴** + 기존 커버리지 대조 → **갭** 산출 → checklist에 planned 적재.

- **Phase 0 — 인벤토리**: 구조 정찰 (라우트/페이지, UI 컴포넌트, API 엔드포인트, export 핵심 함수, 권한/조건 분기). **+ 서버 기동 명령·포트·DB·헬스 경로 감지**(real-first 자동기동 준비). 토큰 보존 위해 Explore 서브에이전트 fan-out 가능.
- **Phase 1 — 카테고리 매핑**: surface → 4 카테고리 (페이지/화면→UI, 유저플로우→functional, 엔드포인트→api, 에러/경계/권한→condition). 웹 surface 없으면 UI skip.
- **Phase 2 — 커버리지 갭 분석**: 기존 `__test__/` 스크립트 대조 → 미커버 = 갭. 카테고리별 커버리지 % 산출.
- **Phase 3 — checklist 적재 + 리포트**: 갭 항목을 `planned`로 추가, 우선순위(영향도×리스크) 부여. 리포트 출력 (총 surface / 커버됨 / 갭 / 카테고리별 %).
- **Phase 4 — 핸드오프**: "scenario로 디테일 시나리오 작성" 안내.

```
╔═══════════════ SCAN REPORT ═══════════════╗
║  Surface 총 N개  |  커버 M개  |  갭 K개     ║
║  UI: x%  functional: y%  api: z%  cond: w% ║
║  우선순위 갭: [P0] ... [P1] ...            ║
╚════════════════════════════════════════════╝
```

## scenario 모드 — 디테일 테스트 시나리오 작성 (1급 산출물)

목적: scan surface(또는 사용자 의도)를 **실행 가능한 디테일 시나리오**로 전개. 각 시나리오가 *무엇을·왜·어디까지(깊이)* 검증할지 명세 → `scenarios.md`.

- **Phase 0 — 입력 수집**: scan 결과 / 사용자 의도 / 기존 시나리오 로드. 부족하면 AskUserQuestion.
- **Phase 1 — 시나리오 전개**: surface별로 `scenario-template.md` 스키마에 따라 작성:
  - `id` (S-카테고리-순번) · `title` · `category`(ui/functional/api/condition) · `priority`(P0~P2)
  - `purpose` (왜 — 비즈니스/리스크) · `precondition` (사전조건: 인증/데이터/상태)
  - `steps` (**Given/When/Then** 또는 번호 단계) · `expected` (예상결과 — 구체적·검증가능)
  - **`tier`** (2~7, 이 시나리오가 요구하는 검증 깊이 — 예상결과가 결정) · `data` (mock | real-backend)
- **Phase 2 — 깊이 판정**: 각 시나리오의 `expected`를 보고 tier 부여.
  - 렌더/요소 노출 → tier 2 · 폼 제출/요청 발화 → tier 3 · **데이터 영속/결과화면 반영 → tier 4(real-backend)** · 시각회귀 → tier 6.
  - tier ≥ 4 시나리오는 `data: real-backend` 표기(mock으로 검증 불가 명시 — no-false-green).
- **Phase 3 — 적재**: `scenarios.md` 작성/갱신 + checklist에 시나리오 ID 연동.

```
╔═══════════════ SCENARIO SET ═══════════════╗
║  시나리오 N개  |  P0 a · P1 b · P2 c        ║
║  깊이: tier2 x · tier3 y · tier4+ z(real)   ║
║  → analyze로 스크립트 커버리지 점검         ║
╚═══════════════════════════════════════════════╝
```

## analyze 모드 — 스크립트 분석 (커버리지 갭 + 정적 진단)

목적: 시나리오가 스크립트로 **실제 검증되는지** + 기존 스크립트 **품질**을 진단 → `analysis.md`. (사용자 요구 "스크립트 분석" 양면)

- **A. 커버리지 갭 분석** (시나리오↔스크립트 매핑):
  - 각 시나리오 → 매핑된 spec 존재? 단언이 `expected`를 실제 검증? (예상결과 미검증 = 허위 커버)
  - 미커버 시나리오 / 부분커버(얕은 단언) / tier 미달(시나리오 tier4인데 스크립트 smoke) 도출.
- **B. 기존 스크립트 정적 진단** (field-tested 안티패턴 스캔):
  - `waitForTimeout` 고정대기 · 광역 locator(`.last()`/role 단독) · 빈/항상참 단언 · route-order shadowing 위험 · false-green(무토큰 인증) 패턴.
- **출력**: `analysis.md` — 시나리오별 커버 상태표 + 안티패턴 목록(파일:라인) + 권고(generate 대상 / 수정 대상).

```
╔═══════════════ ANALYSIS ═══════════════╗
║  시나리오 N | 커버 c · 부분 p · 미커버 u ║
║  tier 미달: t건  |  안티패턴: a건        ║
║  → generate(미커버) / 수정(안티패턴)     ║
╚══════════════════════════════════════════╝
```

## generate 모드 — 스크립트 생성 (≈Generator)

- **Phase 0 — Pre-flight**:
  (a0) **real-first 자동기동**: 서버·DB up 확인(health), 미가동 시 감지된 명령으로 기동(uvicorn/npm dev/docker compose) + health 폴링. 기동 불가 시에만 mock 폴백(보고서 명시).
  (a) 프레임워크 + **버전 감지** (Playwright 설치 / package.json / playwright.config / **v1.56+** → 네이티브 Test Agents 가용성). v1.56+면 `npx playwright init-agents --loop=claude` 네이티브 경로, 미만이면 `test-templates.md` 폴백.
  (b) **브라우저 바이너리 확인** — 없으면 `npx playwright install` 안내(직접 실행은 사용자).
  (c) **타겟 가동 확인** — UI/e2e는 도달 가능 URL(로컬 dev/preview) 필수. URL 해석 + 서버 up 확인(없으면 기동 안내). (chok-verify Phase 6.5/9)
  (d) `__test__/` 또는 기존 테스트 디렉터리 감지.
  (e) 사용자 의도 파싱.
- **Phase 1 — Checklist 빌드**: 의도 → 4 카테고리 점검 항목 도출. 대상 정찰(URL/엔드포인트/컴포넌트). 불충분 시 AskUserQuestion. → `checklist.md` 작성/갱신.
- **Phase 2 — 스크립트 생성**: `__test__/{category}/`에 작성. **접근성 우선 locator** (getByRole > getByLabel > getByText > getByTestId > CSS). UI엔 WCAG a11y 단언 포함. checklist 상태=generated.
- **Phase 3 — Dry-run 검증**: 타겟 URL up 재확인 후 1회 실행해 문법/실행 가능성 확인 (`--no-run` 시 skip). 깨지면 자가 수정.
- **Phase 4 — 핸드오프 + 회고**: `chok-verify`로 전체 실행 / 실패 시 `chok-debug` 안내. retrospective-protocol 회고.

## verify 모드 — 실행 + 검증 (≈Healer)

- **Phase 0 — 감지**: `__test__/`(또는 기존 디렉터리) + 프레임워크 감지. 타겟 URL up + 브라우저 바이너리 확인. **BE 테스트 스위트 감지**(pytest/jest/go). checklist.md 로드.
- **Phase 1 — 실행**: (FE) 카테고리별 스크립트 실행. **(BE) 네이티브 러너로 실 BE 테스트 실행**(`pytest` 등, mock 아님). 결과 수집(FE+BE 분리). 스위트가 크면(메뉴 ≥ 3 / 스펙 ≥ ~8) **"verify 병렬 실행 — 에이전트 샤딩"** 경로로 fan-out(공유 인프라 1회 기동 후 샤드 동시 실행).
- **Phase 2 — 분류**: pass/fail 집계 + **PFS** (chok-debug Step 1.8)로 real-bug vs flaky 분류. checklist 상태 갱신.
- **Phase 3 — self-heal 루프 (bounded, 최대 3회)**: flaky/selector/wait 문제만 보정 후 재실행. **진짜 앱 버그면 수정 금지 → chok-debug 핸드오프.**
- **Phase 4 — 결과 집계 + 회고**: 카테고리별 pass/fail/flaky 집계(다음 report 입력) + retrospective-protocol 회고.

```
╔═══════════════ VERIFY REPORT ═════════════╗
║  PASS: n  |  FAIL: m  |  FLAKY: f          ║
║  카테고리별: UI ✓/✗  func ✓  api ✓  cond ✗ ║
║  real-bug 의심 → chok-debug 핸드오프: [...]  ║
╚════════════════════════════════════════════╝
```

## verify 병렬 실행 — 에이전트 샤딩 (parallel agents)

대규모 스위트(메뉴 多·FE+BE 동시)에서 verify를 **서브에이전트 fan-out**으로 병렬화하여 wall-clock을 줄인다. 핵심 원칙 = **인프라는 1회만 공유 기동하고, 에이전트는 테스트 샤드만 실행**한다. (Anthropic orchestrator-workers: 요약+아티팩트만 반환해 context 보존 / Playwright native `--shard`.)

```xml
<parallel-exec>
  <when>스위트가 클 때(스펙 ≥ ~8 또는 메뉴 ≥ 3) 또는 FE+BE 동시 실행이 필요할 때 발동. 작은 스위트는 단일 프로세스(Playwright native worker 병렬)로 충분 — 과병렬 금지(에이전트 오버헤드 > 이득).</when>
  <shared-infra critical="true">
    서버·DB·브라우저는 orchestrator가 fan-out **전에 1회 기동**한다(real-first auto-start). 에이전트는 **이미 떠 있는** 서버에 테스트만 실행.
    **에이전트별 서버/DB 기동 절대 금지** — N개 uvicorn·N개 DB 인스턴스 = 포트 충돌·자원 폭발·상태 불일치. 모든 샤드가 동일 baseURL·동일 DB를 공유한다.
  </shared-infra>
  <axis>
    1순위 native: Playwright `--shard=k/N`로 FE 스펙을 균등 분할(native-first 승계, 가장 단순·결정적).
    2순위 의미축: 메뉴(`--grep @menu:<name>`) 또는 카테고리(ui|functional|api|condition) 샤드 — 메뉴 개발 단위 격리·self-heal 국소화·실패 귀속이 명확할 때.
    **한 verify 실행에서 두 축 혼용 금지** — `--shard`(균등) XOR 메뉴/카테고리(의미) 중 하나만. 혼용 시 스펙 중복 실행/누락. FE는 한 축으로 전 스펙을 분할 커버.
    FE 샤드들 + BE 러너(pytest/jest/go) + API 값흐름(실 HTTP)은 **서로 다른 브랜치로 동시** 실행.
  </axis>
  <infra-liveness critical="true">
    fan-out 직전 health 200 확인 + **샤드 실행 중 인프라 다운 감지**. 다수 샤드가 동시에 연결거부/5xx/타임아웃 폭증을 보고하면 = **인프라 장애**(테스트 실패 아님) → real_bug로 분류 금지, 전 샤드 결과 무효화 후 인프라 복구·재실행. 단일 샤드만 실패면 테스트/앱 문제로 정상 분류. (false real_bug 방지)
  </infra-liveness>
  <concurrency>동시 에이전트 = min(가용코어-2, 샤드수)로 상한. **시나리오 1건당 1에이전트 금지** — 메뉴/카테고리/shard 단위로 묶어 토큰·자원 보존. 샤드 수 > 상한이면 큐잉.</concurrency>
  <db-isolation>
    병렬 쓰기 충돌 방지: tier4(데이터 영속) 샤드는 **샤드별 랜덤 식별자 네임스페이스**(seed prefix)로 데이터 격리. 동일 행을 다투는 케이스(예: 단일 admin 토글)는 한 샤드에 모아 **직렬화**. 운영 DB 금지·테스트 DB 한정(real-first safety 승계).
  </db-isolation>
  <return-contract>각 에이전트는 **요약 + 아티팩트 경로만** 반환(전체 transcript 금지): `{shard, pass, fail, flaky, PFS, 실패 ID+사유, 스크린샷·JSON 경로}`. orchestrator는 이 요약만 읽어 context를 보존하며 병합.</return-contract>
  <self-heal>self-heal은 **샤드 내부에서 bounded(≤3)** — selector/wait 보정만. 진짜 앱 버그는 샤드가 수정하지 않고 `real_bug`로 표시 → 병합 후 chok-debug 핸드오프(no-false-green 승계). 병렬이 버그를 가리지 않게 한다.</self-heal>
  <merge>orchestrator가 샤드 결과를 단일 verify 집계로 병합. PFS(flip+retry)는 **샤드 내부에서** 산출한다(같은 테스트의 재시도가 있어야 성립 — 샤드는 서로소 스펙이라 교차 비교가 아님). orchestrator는 샤드들의 PFS 분류를 **수집·정규화**만 하고, 인프라 장애로 인한 동시 실패는 flaky가 아니라 무효(infra-liveness 참조)로 처리. → checklist·coverage-map 상태 갱신 → report 입력. **BE 샤드 실패가 1건이라도 있으면 전체 결론 = 보류**(FE green 무관, be-layer verdict 승계).</merge>
  <teardown>orchestrator가 **자기가 기동한 인프라만** 정리(에이전트는 공유 자원이므로 정리 안 함).</teardown>
  <fallback>fan-out 환경 불가(서브에이전트 미가용)면 단일 프로세스 순차 verify로 graceful degrade — 결과 동일, wall-clock만 길어짐.</fallback>
</parallel-exec>
```

**실행 형태** (예: task-planner 메뉴/레이어 샤딩):

```
orchestrator (fan-out 전 1회):
  docker compose up -d        # 공유 DB/redis
  uvicorn app.main:app :14001 # 공유 API
  web dev :14000              # 공유 FE
  → health 200 확인 후 fan-out

동시 실행 (서브에이전트, 공유 인프라 대상):
  agent[FE auth]        npx playwright test --grep @menu:auth
  agent[FE proj+tasks]  npx playwright test functional/project-crud functional/task-crud ui/projects ui/tasks
  agent[FE set+adm+dash] npx playwright test ui/settings* ui/admin ui/dashboard condition/admin-guard
  agent[BE]             .venv/bin/pytest tests/unit tests/integration -q
  agent[API 값흐름]      bash e2e/api-flow-live.sh   # 실 포트 over-the-wire

병합: FE {pass/fail/flaky/PFS} + BE {passed/failed+사유} + api-flow.json → report
```

> 각 샤드는 동일 서버·DB를 공유하므로 **소스 트리 격리(worktree) 불필요** — 테스트는 소스를 변경하지 않는다. (worktree로 분기하면 공유 서버 전제가 깨진다.)

## report 모드 — 빠른 테스트 보고서 (1급 결과물)

목적: 시나리오 + 분석 + 실행결과를 **하나의 읽기 쉬운 보고서**로 종합 → `test-report.md`. 이해관계자가 "무엇을 어디까지 검증했고, 무엇이 통과/실패/미검증인가"를 빠르게 파악.

- **Phase 0 — 수집**: `scenarios.md`(의도·tier) + `analysis.md`(커버리지·안티패턴) + verify FE 결과(pass/fail/flaky/PFS) + **BE 결과(스위트별 passed/failed + 실패 사유)** 병합.
- **Phase 1 — 시나리오별 판정 매트릭스**: 각 시나리오 → {PASS / FAIL / 부분 / 미검증(tier 미달·real-backend 필요)} + 근거(스크립트:라인, 단언). green이라도 tier가 시나리오에 미달하면 "부분".
- **Phase 2 — 갭·리스크 요약**: 미검증 시나리오, 우선순위별 노출 리스크, 안티패턴 잔존.
- **Phase 3 — 보고서 작성**: `report-template.md` 형식으로 `test-report.md` 산출. **BE 섹션 + FE 섹션 분리** (BE: 스위트 결과·실패 목록·사유 / FE: 시나리오 매트릭스·깊이). **BE 실패 시 전체 결론=보류**. 빠른 전달용 상단 1-요약 박스 포함.
- **Phase 4 — HTML 보고서 (`--html`, e2e/UI 필수 권장)**: UI 시나리오는 **스크린샷을 찍어 보고서에 임베드**한다.
  - **스크린샷 캡처**: verify/generate 시 UI 카테고리 스펙에서 `page.screenshot()`로 `e2e/.report-assets/<scenario-id>.png` 저장. (또는 playwright.config `use.screenshot:'on'` 후 test-results에서 수집)
  - **HTML 생성**: 자급식 `test-report.html` — **대시보드** 구성(상단 통계 카드+진행바, 스티키 툴바=검색+메뉴 드롭다운+verdict 칩, data-* 클라 필터). base64 인라인(의존성 0, 단일 파일).
  - **증거 분기**: UI=📷 스크린샷 / 비-UI(functional/api/condition)=🧩 **코드 요청·답변**(전송 payload·액션 → mock 응답·단언, 파란/초록 pre). 스크린샷만이 아니라 코드 증거를 보인다.
  - 검색으로 검수 결과 전문 탐색(ID·제목·근거·코드). `<details>`로 카드별 펼침.
  - 생성기는 `report-template.md`의 HTML 템플릿 참조 (Node 스크립트 1개, 의존성 0 — fs + 문자열 조립).

> **단일 파일 전달**: HTML은 base64 임베드로 의존성 없이 1파일. 메일/슬랙/PR 첨부로 바로 공유. CI 아티팩트로도 업로드 가능.

```
╔═══════════════ TEST REPORT ═══════════════╗
║  시나리오 N | PASS p · 부분 q · 미검증 r    ║
║  깊이 충족률: tier-met x%                   ║
║  P0 리스크: [...]  |  안티패턴 잔존: a건     ║
║  결론: 배포가능? / 조건부 / 보류            ║
╚═════════════════════════════════════════════╝
```

> **핵심 정직성**: 보고서는 "통과 수"가 아니라 **"시나리오 의도 충족 여부 + 검증 깊이"**를 보고한다. mock 경계·tier 미달·real-backend 필요 항목을 *명시적으로* 미검증으로 분류(no-false-green). "다 통과"가 "다 검증"을 뜻하지 않음을 보고서가 드러낸다.

## 최신 트렌드 정합

| 트렌드 | 대응 |
|--------|------|
| Playwright Test Agents (Planner/Generator/Healer) GA | scan/generate/verify 1:1 매핑, 네이티브 우선 |
| Intent-based testing | generate-from-intent |
| Self-healing 기본화 (heal 70-90%) | verify bounded self-heal |
| Flaky = 버그, 통계적 감지 | PFS 분류 |
| MCP accessibility snapshot | recon read_page 우선 |
| Agent teams (Functional+Security+a11y) | 4 카테고리 + a11y 렌즈, Security는 chok-check 핸드오프 |
| Parallel agent sharding (orchestrator-workers) | verify 병렬 실행 — 공유 인프라 1회 기동 + 메뉴/`--shard` 샤드 fan-out, 요약만 병합 |
| Diamond pyramid, maintenance 30-40% | checklist 살아있는 증분 관리 |

## Supporting 파일

- `scenario-template.md`: `scenarios.md` 디테일 시나리오 스키마 (id/purpose/precondition/Given-When-Then/expected/tier/data).
- `report-template.md`: `test-report.md` 보고서 형식 (요약 박스 → 시나리오 매트릭스 → 깊이 분포 → 갭/리스크 → 권고).
- `test-templates.md`: 카테고리 4종 Playwright 템플릿 (네이티브 미가용 폴백 레이어).
- `coverage-map-template.md`: `coverage-map.md` 3-tier(전수/메뉴/단위) 범위 관리 + 메뉴별 실행 명령.
- `checklist-template.md`: 매니페스트 템플릿 (시나리오 ID 연동 상태 추적).

## Integration (느슨한 핸드오프)

- **chok-verify**: generate 후 전체 실행/커버리지 → chok-verify Phase 6/9.
- **chok-debug**: verify에서 real-bug 분류 시 → chok-debug.
- **chok-check**: Security 테스트 렌즈 → chok-check OWASP.
- **chok-auto**: Stage 3(Test)의 **E2E/UI/조건 레이어를 담당**. FE surface 감지 시 chok-auto가 `chok-test generate`를 호출(단위/통합은 tdd-guide). chok-auto SKILL.md "테스트 레이어 분담(layer-split)" 참조.
- **chok-harness**: D9(Testing) 감사가 chok-test 커버리지(checklist planned 대비 pass 비율)를 companion 지표로 읽음.

## Boundaries

**Will:**
- 디테일 테스트 시나리오 작성 (Given/When/Then + 예상결과 + 깊이 tier) — 1급 산출물
- 시나리오↔스크립트 커버리지 갭 + 기존 스크립트 정적 품질 진단
- 시나리오 기반 스크립트 생성 + 프로젝트 전수검사
- 작성 스크립트 실행 + PFS 기반 flaky 분류 + bounded self-heal
- 빠른 테스트 보고서 산출 (시나리오 충족 여부 + 검증 깊이 명시) — 1급 결과물
- 네이티브 Playwright Test Agents 우선 활용 (v1.56+)
- `__test__/` 살아있는 체크리스트 증분 관리

**Won't:**
- 진짜 앱 버그 수정 (→ chok-debug 핸드오프)
- 의미 없는 항상-통과 테스트 생성
- 시크릿/자격증명 하드코딩
- `npx playwright install` 등 시스템 변경 직접 실행 (사용자 안내만)
- self-heal 3회 초과 (무한 루프 방지)
