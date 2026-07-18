---
user-invocable: true
name: meta-ads-setup
description: >-
  Meta 광고 세팅 가이드 — Ads Manager에서 캠페인부터 Threads 배치까지 처음부터 수동 설정하고, Pencil App으로 광고 에셋 초안도 만든다. Meta 광고 세팅, Threads 광고 세팅 시 사용.
---

Meta 광고 세팅 가이드. Ads Manager에서 `캠페인 -> 광고 세트 -> 광고` 순서로 직접 설정하게 안내합니다.

## 데이터 경로 결정

### AGNT_DIR

1. `.claude/agnt/state.json`을 Read 시도 → 성공하면 **AGNT_DIR = `.claude/agnt`**
2. 실패 시 `~/.claude/agnt/state.json` Read 시도 → 성공하면 **AGNT_DIR = `~/.claude/agnt`**
3. 실패 시 `.codex/agnt/state.json` Read 시도 → 성공하면 **AGNT_DIR = `.codex/agnt`**
4. 실패 시 `~/.codex/agnt/state.json` Read 시도 → 성공하면 **AGNT_DIR = `~/.codex/agnt`**
5. 모두 없으면 → "먼저 `/agnt:start`로 시작하세요." 출력 후 종료

### REFS_DIR

`{AGNT_DIR}/references/shared/navigator-engine.md` 존재 여부로 탐색.

### ICP_DOC_PATH

아래 우선순위로 ICP 문서 경로를 결정한다:

1. 현재 작업 디렉토리의 `docs/ICP.md`
2. 없으면 `{AGNT_DIR}/docs/ICP.md`

### DESIGN_SYSTEM_DOC_PATH

아래 우선순위로 디자인 시스템 문서 경로를 결정한다:

1. 현재 작업 디렉토리의 `docs/design-system.md`
2. 없으면 `{AGNT_DIR}/docs/design-system.md`

### TARGET_ICP_SOURCE

광고 타겟의 source of truth는 아래 우선순위로 결정한다:

1. `state.json`의 `project.icp`
2. `{AGNT_DIR}/journey-brief.md`의 현재 프로젝트 설명/시장 섹션
3. `ICP_DOC_PATH`의 **현재 프로젝트용** ICP 문서
4. 전부 불명확하면 사용자에게 한 줄로 보정 질문

중요:

- 저장소의 `docs/ICP.md`가 **이 스킬/프레임워크 자체** 또는 **Agentic30 자체**의 ICP를 설명하면, 그 문서는 참고 자료일 뿐 광고 타겟 기본값으로 쓰지 않는다
- 즉, 현재 repo에 `docs/ICP.md`가 있어도 자동으로 채택하지 않는다

### CREATIVE_STYLE_SOURCE

광고 에셋 비주얼 스타일의 source of truth는 아래 우선순위로 결정한다:

1. 현재 사용자의 `docs/design-system.md` 문서
2. 현재 사용자의 제품에 이미 있는 OG 이미지 / 랜딩 히어로 / 브랜드 가이드
3. 현재 작업 디렉토리의 대표 랜딩 스크린샷 또는 로고
4. 위가 없으면 이 스킬 번들의 샘플 에셋과 repo의 OG 이미지를 **스타일 레퍼런스 예시**로만 사용

중요:

- Agentic30의 OG 이미지는 `스타일 fallback`일 뿐, 사용자의 제품 메시지나 ICP를 대신하지 않는다
- 비슷한 사용자(솔로프리너, 초기 제품 빌더)를 위한 스킬이므로, 톤은 참고하되 카피와 시각 요소는 현재 사용자 제품 기준으로 다시 만든다

## 출력 규칙

내부 로직 무음 처리.

## 실행 절차

### 1. 사전 조건 확인

`{AGNT_DIR}/state.json` Read.

- `meta.schema_version != 3` → `/agnt:start`로 안내 후 종료
- `project.icp == null`이고 `ICP_DOC_PATH`도 없으면 → "먼저 `/agnt:icp`로 타겟을 고정해." (비강제 — 진행 가능)

기본값 보증:
- `artifacts.meta_ads_setup_defined`가 undefined면 `false`로 처리

### 2. 컨텍스트 로드

가능하면 아래를 Read:

- `state.json`의 `project.icp`, `project.problem`, `project.name`
- `state.json`의 `tools.analytics`
- `ICP_DOC_PATH`
- `DESIGN_SYSTEM_DOC_PATH`
- `{AGNT_DIR}/journey-brief.md`
- `{AGNT_DIR}/ad-creatives.md`
- 현재 프로젝트의 대표 URL, 랜딩 스크린샷, OG 이미지 경로

없어도 진행 가능하다. 없으면 아래 기본값을 사용한다:

- 국가: `대한민국`
- 연령: `24-39`
- 언어: `한국어`
- 채널: `Threads feed`
- 목표: `트래픽`

### 2-bis. ICP source 검증

`ICP_DOC_PATH`를 읽었다면 아래를 먼저 점검한다.

문서를 **현재 광고 대상의 ICP로 쓰면 안 되는 신호**:

- 문서가 `Agentic30`, `agnt`, 이 스킬, 이 커리큘럼 자체를 설명함
- 문서가 "우리 ICP", "웹 페이지 버전", 내부 handbook 같은 제품 운영 문서 톤임
- 문서의 고객과 현재 `project.name`/`project.problem`이 전혀 다름
- 문서가 사용자의 제품이 아니라 예시 프레임워크/샘플처럼 보임

위 신호가 있으면:

- `docs/ICP.md`를 기본 타겟 source에서 제외
- `project.icp` 또는 `journey-brief`를 우선 사용
- 둘 다 불명확하면 질문으로 보정

`DESIGN_SYSTEM_DOC_PATH`가 있으면 아래를 먼저 우선 적용한다:

- accent/background/foreground 색상
- 타이포 톤과 headline weight
- 테두리/섀도우/라운드 규칙
- `Asset Rules` 섹션의 광고/OG 규칙

문서가 현재 제품용이 아니거나 예시 문서처럼 보이면:

- 색상/타이포 결정의 참고만 하고 강제 적용하지 않는다

질문은 선택지 우선:

AskUserQuestion: "광고하려는 제품의 ICP source는 뭐야?"

- A) 현재 프로젝트 state의 ICP
- B) 현재 작업 디렉토리의 `docs/ICP.md`
- C) 둘 다 아니고, 지금 광고할 제품 ICP를 한 줄로 말할게

C를 선택한 경우에만:

AskUserQuestion: "누구에게 파는 제품인지 한 줄로 적어줘. 직업/상황/문제를 포함해."

### 3. Ads Manager 진입 상태 분기

먼저 현재 사용자가 어디에 있는지 짧게 판별한다.

AskUserQuestion: "지금 어디 화면이야?"

- A) Ads Manager 메인
- B) 타겟(Audiences) 화면
- C) 캠페인 만들기 도중
- D) 모르겠어

출력 규칙:

- B면: "그 화면은 타겟 자산 라이브러리야. 뒤로 가서 Ads Manager 메인으로 돌아가."를 먼저 말한다
- C면: 현재 단계를 기준으로 필요한 다음 단계만 안내한다
- A/D면: 처음부터 전체 절차를 안내한다

### 3-bis-pixel. Meta Pixel 설치 확인

광고 전환 추적을 위해 Meta Pixel이 필요하다. 아래 순서로 안내한다.

#### Pixel 설치 여부 확인

AskUserQuestion: "Meta Pixel이 이미 설치되어 있어?"

- A) 네, 설치됨
- B) 아니요 / 모르겠어요

B일 경우 아래 안내:

1. **Meta Events Manager** 접속 (business.facebook.com/events_manager)
2. **Connect data** → **Web** → **Set up manually** → **Conversions API**
3. **Data sources → Settings**에서 **Pixel ID (Dataset ID)** 복사
4. 코드에 Pixel 스니펫 삽입 또는 환경변수 `NEXT_PUBLIC_META_PIXEL_ID`에 Pixel ID 설정
5. 전환 이벤트 매핑:

| 페이지 | Meta 표준 이벤트 | 시점 |
|--------|-----------------|------|
| 랜딩 | `ViewContent` | 페이지 로드 |
| 로그인/가입 클릭 | `Lead` | OAuth 버튼 클릭 |
| 가입 완료 | `CompleteRegistration` | 온보딩 폼 제출 |
| 결제 CTA | `InitiateCheckout` | 구독 버튼 클릭 |
| 결제 성공 | `Purchase` | 결제 완료 (금액 + 통화 포함) |

6. 배포 후 Events Manager → **Test Events** 탭에서 이벤트 수신 확인

#### PostHog ↔ Meta Conversions API 서버사이드 연동

브라우저 Pixel만으로는 광고 차단기에 의해 전환이 누락될 수 있다. PostHog에서 서버사이드로도 전환을 보내면 이중 추적이 된다.

1. **PostHog → Data pipeline → Destinations** → "Meta Ads Conversions" 검색 → **+ Create**
2. **Access Token**: Events Manager → Settings → Generate Access Token
3. **Pixel ID**: 위에서 복사한 동일 ID
4. 이벤트 필터: 전환 이벤트만 전송 (모든 pageview를 보내지 않는다)
5. **Create & Enable** → Test Event Code로 검증

### 3-ter. PostHog 연동 상태 분기

광고 성과를 보려면 URL 파라미터와 PostHog가 먼저 맞아야 한다.

판단 원칙:

- `tools.analytics == "posthog"` 또는 analytics setup이 완료돼 있으면 PostHog 기준으로 진행
- 아니면 `/agnt:analytics-setup`을 먼저 안내

`ToolSearch`로 `+agentic30` 검색.

도구 발견 시:

- `connect_posthog_project`를 사용할 수 있으면 PostHog 프로젝트 연결을 우선 안내
- Meta 광고는 단축 링크보다 **직접 랜딩 URL + URL parameters** 조합을 기본으로 권장

도구가 없으면:

- `/agnt:analytics-setup`으로 PostHog 이벤트와 UTM 저장 흐름부터 맞추라고 안내

### 3-bis. 광고 에셋 생성 분기

광고 세팅 전에 크리에이티브가 없거나 약하면, 먼저 에셋 초안 생성을 제안한다.

AskUserQuestion: "광고 에셋도 같이 만들까?"

- A) 응, Pencil App으로 초안까지 만들어줘
- B) 아니, 세팅만 안내해줘

A를 선택하면 아래 `Pencil App 광고 에셋 초안` 절차를 실행한다.

### 4. 타겟 해석

해석 원칙:

- 직접 타겟팅 가능: 국가, 연령, 언어, 관심사/행동, 맞춤 타겟
- 직접 타겟팅 불가: `전업`, `수익 0원`, `Codex 사용자`, `N번째 실패`
- 따라서 ICP의 `직업/상황/현재 대안`에서 관심사 후보를 만들고, 직접 타겟팅 안 되는 부분은 카피로 필터링한다

기본 추천 타겟 구성:

- 위치: `대한민국`
- 연령: `24-39`
- 성별: `전체`
- 언어: `한국어`

상세 타게팅 후보는 ICP 유형별로 고른다.

#### A. 개발자 / AI 빌더 / 인디해커 ICP

- `Software developer`
- `Programming`
- `Web development`
- `Software engineering`
- `Artificial intelligence`
- `OpenAI`
- `ChatGPT`
- `GitHub`
- `Startup company`
- `Entrepreneurship`

#### B. 창업자 / 마케터 / 운영자 ICP

- `Entrepreneurship`
- `Startup company`
- `Small business owners`
- `Digital marketing`
- `Online advertising`
- `Product development`
- `SaaS`
- `E-commerce`
- `Business plan`

#### C. 일반 B2C 소비자 ICP

- 문제와 직접 연결된 broad interest 3-5개만 고른다
- 예: 생산성 제품이면 `Productivity`, `Time management`, `Notion`
- 예: 피트니스 제품이면 `Fitness and wellness`, `Home exercise`, `Healthy diet`
- 예: 커리어 제품이면 `Job hunting`, `Career development`, `Online learning`
- 너무 좁거나 추정이 강한 interest는 피하고, 연령/지역/카피로 필터링한다

#### D. 로컬 서비스 / 니치 B2C ICP

- 처음엔 관심사를 과하게 쌓지 말고 위치 + 연령 + 강한 카피로 시작
- 로컬 비즈니스면 반경/도시 타겟을 먼저 잡고 관심사는 최소화

선택 규칙:

- `project.icp`나 선택된 ICP source를 보고 가장 가까운 archetype 1개를 먼저 고른다
- archetype이 섞이면 1차 테스트는 광고세트 2개로 나눠서 비교
- 상세 타게팅은 세트당 3-5개로 시작
- 실제 계정에 보이는 항목만 선택
- 모호하면 개발자 interest를 기본값으로 쓰지 말고 broad 타겟 + 카피 필터로 후퇴

### 5. Meta 광고 세팅 절차 안내

아래 순서로, 클릭할 UI 라벨을 한국어/영문 같이 적어 단계별로 안내한다.

#### 5-1. 캠페인

1. `+ 만들기` (`+ Create`) 클릭
2. 목표 `트래픽` (`Traffic`) 선택
3. 캠페인 이름 입력
   - 예시: `KR_Threads_ICP_Test_Traffic`
4. `Advantage campaign budget`는 처음엔 `끔`
5. `다음` (`Next`)

#### 5-2. 광고 세트

1. 광고 세트 이름 입력
2. `전환 위치` (`Conversion location`) = `웹사이트`
3. `성과 목표` (`Performance goal`)는 가능하면 `랜딩 페이지 조회수`
4. `일일 예산` 입력
   - 예시: `10,000원`
5. 타겟 입력
   - 위치 = ICP의 시장에 맞는 국가/도시
   - 연령 = ICP의 현실적인 구매 연령대
   - 성별 = 특별한 이유가 없으면 `전체`
   - 언어 = ICP가 실제로 쓰는 광고 언어
   - 상세 타게팅 = 위 archetype별 추천에서 3-5개
6. `배치` (`Placements`)에서 `수동 배치` (`Manual placements`) 선택
7. `Threads` 플랫폼의 `Threads feed` 체크
8. 첫 테스트면 나머지 배치는 모두 해제

#### 5-3. 광고

1. `다음`으로 `광고` (`Ad`) 단계 진입
2. 광고 이름 입력
3. Facebook Page / Instagram 계정 연결
4. `광고 설정` (`Ad setup`)에서 `단일 이미지` 또는 가장 단순한 피드형 광고 선택
5. `크리에이티브 미디어` (`Creative media`)에 비율별 이미지를 업로드한다
   - 최소 권장 세트:
     - `1200x628` 또는 `1080x566` (`1.91:1`, 가로)
     - `1080x1080` (`1:1`, 정사각형)
     - `1080x1350` (`4:5`, 세로 피드)
     - `1080x1920` (`9:16`, 스토리/릴스)
   - 정사각형, 세로, 가로 placement를 모두 만족시키려면 **한 장으로 해결하려 하지 말고 비율별 자산을 따로 올린다**
6. `기본 텍스트` (`Primary text`)는 가능하면 `3-5개`를 넣는다
   - Meta가 가장 효과가 좋을 것으로 예상되는 문구를 자동으로 노출할 수 있게 한다
7. `헤드라인` (`Headline`) 입력
8. `설명` (`Description`) 입력 가능하면 짧게
9. 랜딩 URL 입력
10. CTA는 기본값으로 `자세히 알아보기`를 추천
   - 랜딩이 설명/검증 페이지면 `자세히 알아보기`
   - 랜딩 첫 화면에서 바로 신청/결제면 `가입하기`
11. 우측 미리보기에서 `Threads feed`, `Instagram 탐색 홈`, `Stories/Reels` 미리보기를 확인
12. `게시` (`Publish`)

기본 문구(`Primary text`) 작성 규칙:

- 1개만 넣지 말고 `3-5개` 넣어 테스트 여지를 만든다
- 제품 설명보다 대상 필터 + 문제 정의 + 결과 약속 순서가 낫다
- 이미지 헤드라인과 같은 말을 길게 반복하지 않는다
- 첫 문장에서 Anti-ICP를 걸러낸다

Agentic30 기준 예시:

1. `만들 줄은 아는데 왜 안 팔릴까? Agentic30은 전업 1인 개발자를 위한 30일 PMF 검증 시스템입니다. AI 코파운더와 함께 첫 유저 반응과 첫 결제 신호까지 확인해보세요.`
2. `혼자 만들다 멈추는 개발자를 위해 만들었습니다. 문제 정의, 랜딩 검증, 유입 확인, 첫 매출 신호까지 30일 안에 숫자로 점검하세요.`
3. `코드는 되는데 유저가 없다면, 지금 필요한 건 기능 추가가 아니라 검증입니다. Agentic30에서 AI 코파운더와 함께 팔리는 문제부터 찾으세요.`
4. `전업 1인 개발자에게 30일은 저축 잔고입니다. 감으로 만들지 말고, 유저 100명과 첫 매출 신호를 목표로 실제 반응을 확인해보세요.`
5. `온라인 강의가 아니라 실행 시스템입니다. AI 코파운더, 멘토, 커뮤니티와 함께 혼자 삽질하지 않고 30일 안에 PMF를 검증하세요.`

#### 5-4. 추적 (`Tracking`)

광고 단계 하단의 `추적` (`Tracking`) 섹션에서 아래를 설정한다.

1. `웹사이트 이벤트`는 현재 광고 계정의 기본 전환 데이터 세트 또는 픽셀을 유지
2. `URL 매개변수` (`URL parameters`)를 연다
3. 아래 `canonical UTM` 템플릿을 넣는다

권장 템플릿:

```text
utm_source=meta&utm_medium=paid-social&utm_campaign={{campaign.name}}&utm_content={{site_source_name}}__{{placement}}__{{ad.name}}&meta_campaign_id={{campaign.id}}&meta_adset_id={{adset.id}}&meta_ad_id={{ad.id}}
```

권장 이유:

- `utm_source`: `meta`로 고정
  - PostHog 채널 분류가 안정적이다
  - `facebook`, `instagram`, `threads`로 source를 쪼개면 리포트가 흩어진다
- `utm_medium`: `paid-social`로 고정
  - 오가닉 `social`과 분리된다
- `utm_campaign`: 사람이 읽을 수 있는 캠페인 이름
  - raw ID보다 분석이 쉽다
- `utm_content`: site source + placement + 광고 변형을 담는다
  - ad-level 비교가 가능하다
  - Threads는 보통 `th__threads_stream__pain-v1` 같은 값이 된다
- `meta_*_id`: 이름 변경이나 운영 중 꼬임이 생겼을 때 디버깅용 anchor가 된다

추가 권장:

- 캠페인 이름은 Ads Manager에서 미리 slug 친화적으로 만든다
  - 예: `kr-threads-pmf-sprint-apr25`
- 광고 이름도 사람이 읽을 수 있게 만든다
  - 예: `pain-v1`, `outcome-v1`, `transformation-v1`

가능하면 피해야 할 것:

- `utm_campaign=23849...` 같은 숫자 ID만 사용
- `utm_source=facebook` / `instagram` / `threads`를 뒤섞어서 source 분절
- 너무 긴 `utm_content`

자동 추가 관련 주의:

- Meta 문서 기준으로 2024-01-01부터 일부 광고 트래픽에는 아래가 자동으로 추가될 수 있다
  - 캠페인 소스 = Facebook 또는 Instagram
  - 캠페인 매체 = 유료 광고
  - 광고 ID / 캠페인 ID / 광고 세트 ID / 캠페인 추적 그룹 ID
- 하지만 이 자동값만 믿지 말고, **우리 쪽 canonical UTM 4개는 직접 넣는 걸 기본값으로 한다**
- 이유:
  - 자동 추가는 광고 유형/표면에 따라 달라질 수 있다
  - PostHog와 내부 리포트는 현재 `utm_source / utm_medium / utm_campaign / utm_content`에 가장 안정적으로 맞춰져 있다

#### 5-5. Dynamic parameters 가이드

Meta UI에서 dynamic parameter가 지원되면 아래 원칙으로 쓴다.

**우선순위**

1. 사람이 읽을 수 있는 이름을 `utm_campaign`, `utm_content`에 넣는다
2. ID는 꼭 필요할 때만 보조 파라미터로 추가한다

지원되는 핵심 dynamic parameters:

- `{{campaign.id}}`
- `{{adset.id}}`
- `{{ad.id}}`
- `{{campaign.name}}`
- `{{adset.name}}`
- `{{ad.name}}`
- `{{placement}}`
- `{{site_source_name}}`

권장 매핑:

- 캠페인 소스 (`campaign source`) → `meta`
- 캠페인 매체 (`campaign medium`) → `paid-social`
- 캠페인 이름 (`campaign name`) → `{{campaign.name}}`
- 캠페인 콘텐츠 (`campaign content`) → `{{site_source_name}}__{{placement}}__{{ad.name}}`

Threads에서 특히 useful:

- `{{placement}}` → 보통 `threads_stream`
- `{{site_source_name}}` → `th`

즉 Threads 광고의 `utm_content` 예시는:

```text
th__threads_stream__pain-v1
```

보조 파라미터가 필요하면 아래를 추가할 수 있다:

```text
&meta_campaign_id={{campaign.id}}&meta_adset_id={{adset.id}}&meta_ad_id={{ad.id}}&meta_site={{site_source_name}}&meta_placement={{placement}}
```

하지만 현재 agnt + PostHog 기본 스택에서는:

- `utm_source`
- `utm_medium`
- `utm_campaign`
- `utm_content`

이 4개가 가장 안정적으로 저장/분석된다.

즉, **다이나믹 값은 우선 `utm_campaign`과 `utm_content` 안에 녹이고, ID는 보조 파라미터로 함께 붙여라**.

이름 기반 매개변수 주의:

- `{{campaign.name}}`, `{{adset.name}}`, `{{ad.name}}`는 광고가 처음 게재될 때의 이름을 참조한다
- 게시 후 이름을 바꿔도 URL 파라미터 값은 원래 이름을 계속 참조할 수 있다
- 그래서 Ads Manager에서 게시 전에 slug 친화적인 이름을 먼저 정하고 시작하는 편이 낫다

#### 5-6. PostHog 기준 추천 규칙

현재 코드베이스 기준:

- landing 이벤트는 `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`를 PostHog에 실어 보낸다
- middleware는 `utm_source`, `utm_medium`, `utm_campaign`를 쿠키로 저장한다
- localStorage에는 `utm_content`까지 저장한다

그래서 Meta 광고용 기본값은 아래가 가장 안전하다:

```text
utm_source=meta
utm_medium=paid-social
utm_campaign={{campaign.name}}
utm_content={{site_source_name}}__{{placement}}__{{ad.name}}
```

Threads placement만 테스트할 때:

```text
utm_source=meta&utm_medium=paid-social&utm_campaign={{campaign.name}}&utm_content=th__threads_stream__{{ad.name}}
```

Meta 전체 placement를 같이 돌릴 때:

```text
utm_source=meta&utm_medium=paid-social&utm_campaign={{campaign.name}}&utm_content={{site_source_name}}__{{placement}}__{{ad.name}}
```

광고 관리자에 그대로 넣는 완성형 권장안:

```text
utm_source=meta&utm_medium=paid-social&utm_campaign={{campaign.name}}&utm_content={{site_source_name}}__{{placement}}__{{ad.name}}&meta_campaign_id={{campaign.id}}&meta_adset_id={{adset.id}}&meta_ad_id={{ad.id}}
```

#### 5-7. agentic30 MCP / PostHog MCP 연동

`identity.mode == "synced"`면:

- `ToolSearch`로 `+agentic30` 검색
- PostHog가 아직 미연결이면 `connect_posthog_project`를 먼저 안내
- Meta 광고는 `create_utm_link`보다 Ads Manager의 `URL parameters` 필드를 우선 사용
  - 이유: Meta dynamic parameter가 ad/campaign 단위 값을 직접 채울 수 있음
  - 짧은 링크는 오가닉 채널에 더 적합함

추가 안내:

- PostHog 대시보드에서는 `utm_campaign`, `utm_content` 기준으로 Meta 광고를 비교
- 채널 수준은 `utm_source=meta`, 매체 수준은 `utm_medium=paid-social`로 묶는다

### 6. 카피 필터 규칙

광고 문구 첫 줄로 Anti-ICP를 걸러야 한다고 안내한다.

예시 첫 줄:

- `퇴사 후 전업인데 아직 첫 매출이 없나요?`
- `1인 샵을 운영하는데 광고 효율이 계속 안 맞는다면`
- `매일 운동 계획은 세우는데 3일 이상 못 가는 사람용`

경고:

- Anti-ICP를 카피 첫 줄에서 배제
- 좁은 타겟보다 선명한 카피가 더 중요
- 추상 슬로건보다 `문제 / 결과 / 증거`가 먼저 보여야 한다
- 브랜드 문장보다 클릭 이유가 더 중요하다
- 이미지 안 카피는 가능한 한 짧게 유지한다

전환형 카피 원칙:

- `만들다`, `성장`, `기회` 같은 추상어보다 `첫 유저`, `첫 예약`, `첫 결제`, `검증` 같은 결과어를 우선한다
- `이제는 판다`처럼 발화 주체가 모호한 표현보다 `이제는 팔린다`처럼 결과가 바로 읽히는 표현을 우선한다
- `SPEC`, `UTM`, `배포`, `검증` 같은 내부 작업 단어를 이미지 헤드라인에 그대로 올리지 않는다
- 숫자를 쓸 때는 의미가 큰 숫자만 쓴다
  - 예: `30일`, `100명`
  - 비권장: `첫 매출 5,000원`처럼 제품 가치를 싸 보이게 할 수 있는 작은 금액
- 한 장당 메시지는 하나만 남긴다
  - pain는 문제 직격
  - outcome은 결과 약속
  - transformation은 정체성 변화 또는 증거

이미지 카피 기본 구조:

- 헤드라인 1개
- 보조 설명 1개
- 짧은 배지/증거 1개

기본 필드별 역할:

- `Primary text`: 배경 설명 + 대상 필터
- `Headline`: 클릭 이유를 한 줄로 압축
- 이미지 헤드라인: 스크롤을 멈추게 하는 핵심 문장만 유지
- `Description`: 선택 사항이며, 반복 설명이면 생략 가능

### 7. 문제 해결 분기

사용자가 막힐 때는 아래 분기로 답한다.

#### A. Threads가 안 보일 때

- 목표가 `트래픽`인지 확인
- 자동화된 캠페인 유형이 아닌지 확인
- 광고 형식을 `단일 이미지`처럼 단순하게 변경
- `수동 배치`로 다시 진입

#### B. 타겟 화면만 보일 때

- "그건 `Audiences` 라이브러리야. 뒤로 가서 캠페인 생성 흐름으로 돌아가."라고 말한다
- 저장된 타겟은 선택 사항이지 필수 절차가 아님을 분명히 한다

#### C. 관심사가 안 보일 때

- 유사한 항목으로 대체
- 3-5개만 선택
- 나머지는 카피와 랜딩으로 필터

#### D. Instagram 탐색 홈에 `지원되지 않는 화면 비율`이 뜰 때

- 이 에러는 보통 현재 업로드한 미디어가 `Instagram 탐색 홈` placement 비율 조건을 만족하지 않는다는 뜻이다
- 기본 대응:
  - `1080x1350` (`4:5`) 또는 `1080x1920` (`9:16`) 이미지를 추가 업로드
  - 또는 해당 placement를 해제
- `1:1`이나 `1.91:1`만으로는 일부 Instagram placement가 빠질 수 있다
- 따라서 Explore/피드/스토리까지 넓게 커버하려면 `1.91:1 + 1:1 + 4:5 + 9:16` 세트를 권장한다

### 8. 출력 포맷

최종 출력은 아래 순서를 유지한다.

1. 지금 눌러야 할 버튼
2. 현재 화면에서 입력할 값
3. Threads에 필요한 설정
4. 안 보이거나 막힐 때 대처

사용자가 `지금 이 화면에서 뭘 눌러?`라고 물으면 긴 설명 대신 바로 다음 클릭 1-3개만 말한다.

### 9. Pencil App 광고 에셋 초안

이 단계는 `Pencil MCP`가 사용 가능할 때 실행한다.

`Pencil MCP`가 없거나 `Pencil.app`이 설치/실행되지 않은 것 같으면:

- Pencil 기반 에셋 생성을 강행하지 않는다
- 먼저 `Pencil.app이 없으면 https://www.pencil.dev/ 에서 설치/실행해.`라고 안내한다
- 그 뒤 Meta 세팅 안내만 계속하거나, 사용자가 Pencil 준비 후 다시 실행하게 한다

목표:

- 사용자의 현재 ICP와 문제에 맞는 Meta 광고 이미지 초안 3종 생성
- 기본 형식은 `1200x630` (`1.91:1`) 3장
- 같은 메시지로 `1080x1080`(`1:1`), `1080x1350`(`4:5`), `1080x1920`(`9:16`) 파생본까지 만든다
- 즉, 가능하면 총 12개를 만든다
  - `pain / outcome / transformation`
  - 각 4비율: `1.91:1 / 1:1 / 4:5 / 9:16`

#### 9-1. 에셋 생성 전 입력값

아래를 먼저 정리한다:

- 제품 이름 1개
- 문제 한 줄 1개
- ICP 한 줄 1개
- 랜딩 CTA 또는 약속 한 줄 1개
- 스타일 source 1개

스타일 source 결정:

- `docs/design-system.md`가 있으면 그 문서의 `Color System`, `Typography`, `Asset Rules`를 먼저 사용
- 사용자 제품의 OG/브랜드가 있으면 그걸 우선
- 둘 다 없으면 `apps/web/public/images/og-image.png`와 `assets/meta-ad-*.png`를 레퍼런스 예시로 사용

#### 9-2. 카피 각도

광고 초안은 항상 3개 각도로 만든다:

1. `pain`
   - 문제 직격
   - "코드는 됐는데, 유저가 없다?" 같은 구조
2. `outcome`
   - 결과 약속
   - "이번엔 끝까지", "첫 예약/첫 구매/첫 리드" 같은 구조
3. `transformation`
   - 정체성 변화
   - "만드는 사람에서 파는 사람으로" 같은 구조

각도 선택 규칙:

- 개발자/빌더 ICP면 기술 언어를 조금 허용
- 일반 B2C면 더 쉬운 말로 바꿔
- 로컬 서비스면 도시/반경/업종 단서를 더 앞에 둬

카피 선택 우선순위:

1. 대상이 `내 얘기다`라고 느끼는 문제 문장
2. 무엇이 달라지는지 보이는 결과 문장
3. 그 결과를 믿게 만드는 짧은 증거

권장 예시:

- pain: `만들 줄은 아는데, 왜 안 팔릴까?`
- outcome: `30일 안에 첫 유저 반응까지`
- transformation: `혼자 빌드하던 개발자, 이제는 팔린다`

비권장 예시:

- `이번엔 끝까지`
- `성장의 시작`
- `SPEC → 배포 → 검증`

이유:

- 위 문구들은 제품 내부 맥락이 없으면 의미가 약하거나 너무 내부자 언어처럼 보인다
- 광고 이미지는 랜딩보다 더 빠르게 이해돼야 한다

#### 9-3. 비주얼 규칙

기본 톤:

- 화이트/크림 배경
- 블랙 두꺼운 타이포
- 강한 오렌지 포인트
- 두꺼운 외곽선과 단순 기하학 도형
- 네오브루탈리즘 계열

하지만 다음은 제품별로 조정한다:

- 로고가 있으면 우하단 또는 헤더에 배치
- 제품 고유 색이 있으면 오렌지 포인트 대신 제품 대표색 사용 가능
- 일반 소비자 제품이면 텍스트 밀도를 조금 낮추고 여백을 늘려
- `docs/design-system.md`가 있으면 그 문서의 금지 규칙을 우선 적용

#### 9-4. Pencil 절차

1. `get_editor_state(include_schema: true)`로 현재 문서 확인
2. 광고용 프레임이 이미 있으면 **새로 만들기 전에 수정 가능 여부를 먼저 확인**한다
   - 기존 `pain / outcome / transformation` 프레임이 있으면 그 문서를 source of truth로 사용
   - 카피만 약하면 새 프레임 생성보다 기존 프레임 수정이 우선이다
3. 작업 문서가 없으면 새 `.pen` 문서를 열거나 현재 문서를 사용
4. `get_screenshot` 또는 로컬 레퍼런스 이미지 확인
5. `batch_design`으로 1200x630 프레임 3개 생성 또는 기존 3개 수정
6. 각 프레임에 다음을 넣는다:
   - 강한 헤드라인 1개
   - 강조 바/도형 1개 이상
   - 짧은 서브카피 1개
   - 짧은 배지 또는 CTA 라벨 1개
7. `get_screenshot`으로 프레임별 검수
8. 필요하면 좌표/크기/텍스트 길이 수정
9. 1200x630 시안이 통과하면 같은 메시지로 `1080x1080`, `1080x1350`, `1080x1920` 파생본을 만든다
10. 정사각형/세로형은 단순 resize가 아니라 다음을 다시 조정한다:
   - 헤드라인 폭
   - 폰트 크기
   - 줄바꿈
   - 장식 도형 위치
   - 하단 배지 위치
11. 정사각형은 하단 밀도가 약하면 장식 면을 추가해 균형을 맞춘다
12. 세로형은 빈 공간을 줄이는 대신 큰 장식 면과 더 큰 정보 블록으로 화면 점유를 높인다
13. `get_screenshot`으로 `1:1 / 4:5 / 9:16`까지 다시 검수
14. `export_nodes`로 비율별 PNG 추출

비율별 기본 원칙:

- `1200x630`: Threads feed, 링크 공유형 기준의 기본 마스터
- `1080x1080`: 정사각형 placement 및 보조 피드 자산
- `1080x1350`: 모바일 피드에서 우선순위가 높다
- `1080x1920`: Story/Reels 계열 placement 대응
- 실제 업로드 세트는 가능하면 `1.91:1 + 1:1 + 4:5 + 9:16` 모두 준비한다

세로 비율 주의:

- 가로형 카피를 그대로 늘리지 않는다
- 헤드라인이 3줄 이상으로 찢기면 문장을 줄이거나 폰트 크기를 내린다
- transformation 카피는 세로형에서 특히 줄바꿈이 쉽게 망가지므로 별도 검수한다

정사각형 비율 주의:

- 중앙만 비워 두지 말고 하단 장식이나 배지로 균형을 만든다
- `pain`과 `outcome`은 정사각형에서 하단 밀도가 약해지기 쉬우니 장식 면을 한 번 더 점검한다

#### 9-5. 파일 저장

기본 출력:

- `{AGNT_DIR}/ads/meta-ad-pain.png`
- `{AGNT_DIR}/ads/meta-ad-outcome.png`
- `{AGNT_DIR}/ads/meta-ad-transformation.png`
- `{AGNT_DIR}/ads/1x1/meta-ad-pain.png`
- `{AGNT_DIR}/ads/1x1/meta-ad-outcome.png`
- `{AGNT_DIR}/ads/1x1/meta-ad-transformation.png`
- `{AGNT_DIR}/ads/4x5/meta-ad-pain.png`
- `{AGNT_DIR}/ads/4x5/meta-ad-outcome.png`
- `{AGNT_DIR}/ads/4x5/meta-ad-transformation.png`
- `{AGNT_DIR}/ads/9x16/meta-ad-pain.png`
- `{AGNT_DIR}/ads/9x16/meta-ad-outcome.png`
- `{AGNT_DIR}/ads/9x16/meta-ad-transformation.png`

프로젝트 구조상 다른 위치가 더 자연스러우면 다음도 허용:

- 현재 작업 디렉토리의 `tmp/` 또는 `artifacts/`
- 스킬 번들의 `assets/`는 샘플 보관용이지 사용자 산출물 기본 경로는 아님

#### 9-6. 검수 규칙

- 1200x630 안에 모든 요소가 잘려 있지 않아야 함
- 헤드라인은 한눈에 읽혀야 함
- 텍스트는 3계층 이하로 제한
- 랜딩 첫 화면 메시지와 모순되면 안 됨
- 제품 ICP가 Agentic30 ICP와 다르면, 개발자 전용 문구를 넣지 않는다
- 한 장에 메시지 2개 이상을 억지로 넣지 않는다
- 모바일에서 가장 먼저 읽히는 건 헤드라인이어야 한다
- 이미지 안 텍스트는 내부자 용어보다 사용자 언어를 우선한다
- `1:1`, `4:5`, `9:16`은 각각 별도 스크린샷 검수를 거친다
- 세로형에서 어색한 줄바꿈이 나오면 export 전에 반드시 수정한다
- 같은 카피라도 비율에 따라 line break가 달라질 수 있음을 전제로 작업한다
- 정사각형과 세로형은 하단 밀도까지 본다. 텍스트만 위에 몰리고 아래가 비면 재수정한다
- 가능한 경우 `문제형 / 결과형 / 증거형` 중 무엇이 가장 강한지 비교 가능한 상태로 남긴다

#### 9-7. 실패/보정 분기

- `Pencil MCP`가 없거나 Pencil editor가 연결되지 않으면:
  - `Pencil.app이 없으면 https://www.pencil.dev/ 에서 설치/실행해.`라고 먼저 안내
  - 광고 카피와 shot list만 텍스트로 먼저 정리
- 제품 비주얼 레퍼런스가 없으면:
  - 중립 네오브루탈 템플릿으로 시작
- 카피가 길면:
  - 헤드라인을 8-18자 수준으로 줄여
- ICP가 너무 넓으면:
  - 가장 절박한 세그먼트 1개만 잡아 3안 생성
- 첫 시안이 밋밋하면:
  - 숫자, 기간, 결과를 더 앞에 둬

### 10. 저장

`{AGNT_DIR}/meta-ads-setup.md` Write.

```markdown
# Meta Ads Setup

생성일: {날짜}
채널: Threads
목표: 트래픽

## 추천 타겟
{ICP source / archetype / 위치 / 연령 / 언어 / 상세 타게팅}

## Ads Manager 세팅 순서
{캠페인 -> 광고 세트 -> 광고 절차}

## Tracking
{utm_source / utm_medium / utm_campaign / utm_content 권장값}

## Pencil 에셋 초안
{pain / outcome / transformation 카피와 출력 파일 경로}

## 문제 해결
{Threads 미노출 / Audiences 화면 / 관심사 부족 대응}
```

### 11. state 업데이트 + MCP 제출

state.json 업데이트:

- `artifacts.meta_ads_setup_defined = true`
- `artifacts.meta_ads_assets_drafted = true` (Pencil 초안 생성 시)
- `meta.last_action = "meta-ads-setup"`
- `meta.total_actions++`

`ToolSearch`로 `+agentic30` 검색.

도구 발견 시:
- `submit_practice` 호출: quest_id = `"wf-meta-ads-setup"`

도구 없으면 (`identity.mode != "synced"` 또는 ToolSearch 실패):
- `sync.pending_events`에 추가 (50건 초과 시 가장 오래된 이벤트 제거):
  ```json
  { "type": "submit_practice", "args": { "quest_id": "wf-meta-ads-setup" }, "created_at": "<now()>" }
  ```

## 규칙

- Meta 광고는 `Audiences` 화면이 아니라 `광고 세트` 단계에서 바로 세팅하는 흐름을 기본으로 안내
- Threads 광고는 별도 플랫폼이 아니라 `placement`라는 점을 분명히 해
- repo의 `docs/ICP.md`가 있어도 그 문서가 현재 사용자의 제품 ICP인지 먼저 검증해
- `docs/design-system.md`가 있으면 Meta 광고 에셋은 그 문서의 `Asset Rules`를 우선 따라
- repo의 OG 이미지가 있어도 그 이미지는 fallback 스타일 레퍼런스일 뿐, 사용자의 제품 크리에이티브 source를 대체하지 않는다
- PostHog 기준 canonical attribution은 `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` 4개를 우선 사용한다
- Meta dynamic parameter는 가능하면 `utm_campaign`, `utm_content` 안에 녹이고, 숫자 ID는 보조 파라미터로만 사용한다
- Meta paid traffic은 `utm_source=meta`, `utm_medium=paid-social`를 기본값으로 권장한다
- 직접 타겟팅 불가한 속성은 관심사로 억지 매핑하지 말고 카피 필터로 처리
- 처음 세팅은 `트래픽 + Threads feed only + 단일 이미지 + 소액 일예산`으로 단순화
- 개발자 ICP 예시는 예시일 뿐 기본값이 아니다. 현재 사용자 제품의 ICP archetype에 맞게 interest를 다시 고른다
- Pencil 에셋은 항상 `pain / outcome / transformation` 3안으로 시작해 비교 가능하게 만든다
- Pencil 에셋은 가능하면 `1.91:1 + 1:1 + 4:5 + 9:16`까지 함께 만들어 placement 대응 범위를 넓힌다
- 이미지 카피는 슬로건보다 전환형 문장을 우선한다
- 내부 용어 (`SPEC`, `UTM`, `배포`)는 광고 이미지 안 헤드라인 기본값으로 쓰지 않는다
- 기존 광고 프레임이 이미 있으면 새로 만들기보다 수정 우선으로 접근한다
- `Primary text`는 1개만 넣지 말고 가능하면 3-5개 넣어 Meta가 자동 최적화할 여지를 남긴다
- URL 매개변수는 이름 기반 dynamic value를 쓰되, 게시 전에 이름을 확정하고 ID 보조 파라미터를 함께 붙인다
- Pencil이 준비되지 않았으면 `https://www.pencil.dev/`로 먼저 안내하고, 그 전에는 텍스트 초안까지만 진행한다
- 샘플 에셋이 이미 있더라도 그대로 재사용하지 말고, 현재 사용자 제품 이름/문제/ICP 기준으로 새 초안을 만든다
- 내부 추론은 보여주지 말고, 사용자가 지금 눌러야 하는 UI를 먼저 말해
