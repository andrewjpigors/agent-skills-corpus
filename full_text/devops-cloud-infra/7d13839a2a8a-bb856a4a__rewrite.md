---
name: rewrite
description: "Analyze competitor script winning formula, cross-reference with our research, generate original scripts grounded in our data. Examples: /rewrite <paste text>, /rewrite /tmp/transcript.txt"
user_invocable: true
---

# /rewrite — Competitor Intelligence → Original Generation

Конкурентский скрипт = разведка, не чертёж.
Извлекаем ПОЧЕМУ работает → проверяем есть ли у нас research → генерим из НАШИХ данных, обогащённых insight'ом.

**Принцип:** НЕ reverse-engineer сущности. Извлечь Winning Formula → cross-reference с нашей БД → генерация через наш pipeline.

## Arguments

- **Текст скрипта**: вставлен прямо после `/rewrite`, ИЛИ
- **Путь к файлу**: `/rewrite /path/to/file.txt`
- **Опции:**
  - `--geo=CL|US|BR|LOCALE_MX|CO|AR|PE|EU|RU|UA|RO`
  - `--vertical=<name>` (e.g. "health_supplement_ed", "health_supplement_category_b")
  - `--mode=hooks_only|angle|frame|concept|everything|analyze` (default: `everything`)
  - `--count=N` (вариаций, default: 3)
  - `--analyze` — shortcut для `--mode=analyze`: только Intelligence Extraction (Phase 2), БЕЗ генерации скрипта. Используй когда нужна winning formula для информирования `/editorial` или `/generate-angles`

## Pre-analysis Checklist

### □ WINNING FORMULA EXTRACTION
- Structure: сколько секций, порядок, длина каждой
- Hooks: типы (scene/stat/question), awareness level
- Proof sequences: какие proof types, в каком порядке
- Villain pattern: кто villain, как framed (conspiracy vs inerție)
- Transformation detail: physical specifics, timeline, relationship payoff

### □ CROSS-REFERENCE WITH OUR DATA
- Winning formula × наши research_quotes (voice DNA match?)
- Winning formula × наши BMIs (какой mechanism closest?)
- Что берём (validated patterns) / что НЕ копируем (и почему)
- Записать в output: "Applied from spy: X, Y. Not applied: Z (reason)"

### □ APPLY TO ALL DOWNSTREAM
- Spy insights должны попасть в: EDITORIAL, листикл, advertorial, images
- Не только в текущий /rewrite output — а во ВСЕ assets вертикали
- Напомнить CEO: "Эти паттерны нужно применить при /longform_article и /editorial"

## Flow

---

### Phase 1: INPUT

Если путь к файлу → Read. Если текст → script_text. Если пусто → спроси и **СТОП**.

---

### Phase 2: INTELLIGENCE EXTRACTION — Что делает этот скрипт победителем?

Фокус: НЕ маппинг на наши сущности. Извлечение **психологической формулы** + **структурных паттернов**.

#### 2.1 Winning Formula (ядро)

| Поле | Что извлечь |
|------|-------------|
| `core_belief` | ОДНО глубочайшее убеждение аудитории, которое эксплуатирует скрипт. Не surface-level — корень всех beliefs в тексте |
| `underlying_fear` | Экзистенциальный страх ЗА core_belief. Identity-level, не surface. |
| `villain` | Кого/что скрипт обвиняет. Переосмысли в контексте формулы: как обвинение villain'а активирует core_belief + fear? |
| `identity_shift` | "from [кто сейчас] to [кем станет]" — трансформация identity |
| `mechanism_promise` | Что механизм ЗНАЧИТ для жизни (трансформация, не feature) |
| `why_it_works` | ОДНО предложение, max 30 слов: почему эта комбинация цепляет |
| `sophistication_stage` | 1-5 (direct_claim → identification) |

#### 2.2 Audience Signals (кого таргетит)

НЕ создаём архетип. Извлекаем СИГНАЛЫ для cross-reference:

| Поле | Что извлечь |
|------|-------------|
| `target_gender` | male / female / any |
| `target_age_range` | e.g. "40-65" |
| `surface_desires` | 3-5 чего ГОВОРЯТ что хотят |
| `deep_fears` | 3-5 конкретных сценариев (не абстрактных) |
| `triggering_moments` | 3-5 моментов, запустивших поиск |
| `language_verbatim` | 5-8 фраз НА ЯЗЫКЕ СКРИПТА — как люди говорят о проблеме |
| `identity_conflict` | "кто я vs кем хочу быть" |
| `failed_solutions` | Что пробовали и провалилось (list из скрипта) |
| `dream_outcome` | Verbatim мечта: "Я просто хочу..." |

#### 2.3 Structural Patterns (как построен)

Паттерны для обучения, не для копирования:

| Поле | Что извлечь |
|------|-------------|
| `lead_type` | story / problem_solution / proclamation / prediction / offer / promise / secret |
| `emotional_arc` | "start_to_end" (e.g. "shame_to_triumph") |
| `beat_structure` | 5-10 битов: beat_num, beat_type (hook/story/problem/agitation/mechanism/proof/credibility/cta/transition), summary, emotion |
| `hook_device` | Чем цепляет первые 2-3 предложения (описательно, не enum) |
| `urgency_device` | Как создаёт срочность (описательно) |
| `proof_stack` | Какие proof'ы и в каком порядке (list) |
| `objection_handling` | Какие возражения и как обрабатывает (list: objection → counter, placement relative to mechanism reveal) |
| `villain_narrative` | Как выстроен narrative злодея |
| `mechanism_reveal` | Как и когда раскрывает механизм |

#### 2.4 Compliance Snapshot

| Поле | Что извлечь |
|------|-------------|
| `whitelisted_numbers` | Все числа/статистики из скрипта |
| `approved_claims` | Все health/benefit заявления |
| `endorsement_refs` | Упомянутые реальные люди |

#### 2.5 Auto-detect

- `detected_vertical` (из контекста продукта)
- `detected_geo` (из языка, валюты, культурных маркеров)
- `detected_language` (язык текста)

---

### Phase 2 OUTPUT — Показать результат

```
## Competitor Intelligence Report

### Winning Formula
**Core Belief:** {core_belief}
**Underlying Fear:** {underlying_fear}
**Villain:** {villain}
**Identity Shift:** {identity_shift}
**Mechanism Promise:** {mechanism_promise}
**Sophistication:** {stage}
**Why It Works:** {why_it_works}

### Кого таргетит
**Аудитория:** {gender}, {age_range}
**Хотят:** {desires}
**Боятся:** {fears}
**Триггеры:** {triggering_moments}
**Провалы:** {failed_solutions}
**Мечта:** {dream_outcome}
**Как говорят:** {language_verbatim}
**Конфликт:** {identity_conflict}

### Как построен
**Lead:** {lead_type} | **Arc:** {emotional_arc}
**Hook:** {hook_device}
**Villain narrative:** {villain_narrative}
**Mechanism reveal:** {mechanism_reveal}
**Proof stack:** {proof_stack}
**Objections:** {objection_handling}
**Urgency:** {urgency_device}

### Compliance
**Numbers:** {numbers} | **Claims:** {claims} | **Figures:** {figures}

### Beat Structure
| # | Тип | Что происходит | Эмоция |
|---|-----|---------------|--------|
...
```

Затем:
> **Geo:** {geo} | **Vertical:** {vertical}
> Сейчас проверю нашу базу — есть ли research, который резонирует с этой формулой.


**If `--mode=analyze` or `--analyze`:** STOP HERE. Show Phase 2 output and:
> Intelligence extraction complete. Данные готовы для использования в `/editorial`, `/generate-angles`, или `/generate-script`.
> Для полного rewrite (с генерацией скриптов) запусти `/rewrite` без `--analyze`.
Do NOT proceed to Phase 3, 4, or 5.
**Если НЕ analyze mode: НЕ ЖДАТЬ CEO.** Сразу переходить к Phase 3.

---

### Phase 3: CROSS-REFERENCE — Есть ли у нас грунтование?

Запросить через Supabase MCP (`execute_sql`) последовательно:

> **⚠️ EXECUTE ALL QUERIES BELOW** via `mcp__supabase__execute_sql`. Each query = one tool call. Do NOT skip queries — cross-reference quality depends on complete data. If a query returns 0 rows, note it and continue.

#### 3.1 Найти наши архетипы

```sql
SELECT id, name, description, primary_desire, deep_desire_category
FROM avatar_archetypes
WHERE vertical = '{vertical}' AND geo = '{geo}'
ORDER BY sample_size DESC LIMIT 10;
```

Сравни семантически с audience signals. Есть похожий? → запомни archetype_id.

→ If found, save archetype_id for later queries.

#### 3.2 Найти наши BMI

```sql
SELECT id, name, mechanism_identity, ums, ump, primary_promise, hook, status
FROM bmis
WHERE vertical = '{vertical}' AND geo = '{geo}'
  AND status IN ('active', 'draft', 'graduated', 'proven')
ORDER BY sample_size DESC LIMIT 20;
```

Есть BMI с похожим mechanism promise или primary_promise? → запомни bmi_id.

→ If found, save bmi_id for queries 3.3-3.8.

#### 3.3 Найти резонирующие beliefs

Если нашёлся bmi_id:
```sql
SELECT nb.id, nb.belief_text, nb.current_belief, nb.awareness_stage, nb.belief_order, nb.belief_dimension
FROM necessary_beliefs nb
WHERE nb.bmi_id = '{bmi_id}'
ORDER BY nb.belief_order;
```

Сравни с core_belief из Winning Formula. Есть совпадения?

→ Compare with core_belief from Phase 2.

#### 3.4 Найти research quotes

```sql
SELECT rq.quote_text, rq.quote_type, rq.emotional_weight, rq.source_platform
FROM research_quotes rq
JOIN research_sessions rs ON rq.session_id = rs.id
WHERE rs.vertical = '{vertical}' AND rs.geo = '{geo}'
  AND rq.emotional_weight >= 3
ORDER BY rq.emotional_weight DESC LIMIT 30;
```

Есть quotes которые резонируют с language_verbatim, fears, desires из competitor analysis?

→ Match against language_verbatim, fears, desires.

#### 3.5 Найти arguments и objections

Если нашёлся bmi_id:
```sql
SELECT argument_type, argument_text, proof_intuitive, proof_empirical
FROM argument_maps WHERE bmi_id = '{bmi_id}' LIMIT 20;

SELECT objection_text, counter_argument, proof, placement
FROM objection_maps WHERE bmi_id = '{bmi_id}' LIMIT 10;
```

→ Note which arguments and objections exist.

#### 3.6 Найти angles и frames

Если нашёлся bmi_id:
```sql
SELECT id, name, emotional_trigger, hook_type, awareness_approach, stage_of_awareness
FROM angles WHERE bmi_id = '{bmi_id}' AND vertical = '{vertical}' AND geo = '{geo}';

SELECT id, name, frame_type, proof_type, narrator_voice,
       credibility_storyline, evidence_elements, source_type
FROM frames WHERE vertical = '{vertical}' AND geo = '{geo}';
```

→ Count available angles and frames.

#### 3.7 Найти voice DNA и script brief

```sql
SELECT phrase_markers, vocabulary_level, taboo_words, exemplar_sentences
FROM voice_dna WHERE vertical = '{vertical}' AND geo = '{geo}' LIMIT 5;

SELECT villain, urgency_type, urgency_narrative, mechanism_metaphor, lead_type
FROM script_briefs WHERE bmi_id = '{bmi_id}' LIMIT 5;
```

→ Save voice DNA markers for Phase 4 generation.

#### 3.8 Найти spy-validated hooks

```sql
SELECT h.hook_text, h.hook_type, h.valence, h.intensity, h.bmi_id,
       b.name as bmi_name
FROM hooks h JOIN bmis b ON h.bmi_id = b.id
WHERE b.vertical = '{vertical}' AND h.source_type = 'competitor'
ORDER BY h.created_at DESC LIMIT 5;
```

→ Note spy hook styles for opening reference.

Spy hooks = reference для стиля и энергии opening. НЕ копировать, использовать как вдохновение.

---

### Phase 3 OUTPUT — Verdict

Оцени grounding level:

**STcurrencyG** (можно генерить):
- Нашёлся архетип с похожими desires/fears
- Нашёлся BMI с релевантным mechanism
- Есть beliefs chain
- Есть research quotes

**PARTIAL** (можно генерить с оговорками):
- Есть архетип, но нет BMI (или наоборот)
- Есть quotes, но нет structured beliefs
- Хватает чтобы обогатить, но не полный pipeline

**WEAK** (нужен research):
- Нет архетипа для этой аудитории
- Нет BMI в этом направлении
- Нет research quotes

Покажи CEO:

```
## Cross-Reference с нашей базой

### Grounding: {STcurrencyG / PARTIAL / WEAK}

**Архетип:** {FOUND: "name" (match: desires overlap) / NOT FOUND}
**BMI:** {FOUND: "name" (match: mechanism overlap) / NOT FOUND}
**Beliefs:** {FOUND: N beliefs, {overlap description} / NOT FOUND}
**Research Quotes:** {FOUND: N quotes resonating with WF / NOT FOUND}
**Angles:** {FOUND: N angles for this BMI / NOT FOUND}
**Frames:** {FOUND: N frames / NOT FOUND}
**Voice DNA:** {FOUND / NOT FOUND}

### Что это значит
{if STcurrencyG}: У нас есть research grounding для генерации. Winning Formula конкурента подтверждена нашими данными — это значит аудитория реально так думает/чувствует. Генерирую вариации из НАШИХ сущностей, обогащённых инсайтами.

{if PARTIAL}: Частичное grounding. Могу генерить, но {missing entity} нет — {рекомендация что доисследовать}. Генерирую с тем что есть?

{if WEAK}: Недостаточно данных для качественной генерации. Этот конкурент работает с аудиторией/направлением, которое мы ещё не исследовали. Рекомендую: {что нужно исследовать}. Хочешь всё равно попробовать (без grounding, качество ниже)?
```

**СТОП. Жди ответ CEO.** (Для STcurrencyG — можно не ждать если CEO ранее говорил "го".)

---

### Phase 4: GENERATION — Из наших данных, обогащённых Winning Formula

#### Источники данных для генерации

**Из НАШЕЙ БД (primary):**
- BMI: mechanism_name, ums, ump, primary_promise, hook, origin_story, mechanism_identity
- Archetype: desires, fears, triggers, language_patterns, identity_conflict
- Belief chain: ordered beliefs with arguments
- Objections: с placement и counter_arguments
- Voice DNA: phrase_markers, vocabulary_level, exemplar_sentences
- Script Brief: villain, urgency, authority, mechanism_metaphor
- Research Quotes: golden quotes (emotional_weight >= 4)
- Angles: для ротации между вариациями
- Frames: для ротации между вариациями

**Из Winning Formula конкурента (enrichment):**
- core_belief → проверить, усиливает ли нашу belief chain
- identity_shift → использовать как emotional arc guide
- villain framing → вдохновение для нашего villain narrative (НЕ копия)
- structural patterns → beat structure как reference (НЕ template)
- proof stack → какие типы proof'ов работают в этом рынке
- hook device → вдохновение для opening (НЕ копия)

**Compliance из конкурента:**
- whitelisted_numbers, claims, figures → использовать ТОЛЬКО если подтверждены нашим research

#### Variation Mode Constraints

| Mode | Locked | Varies |
|------|--------|--------|
| `hooks_only` | angle, frame, concept | ТОЛЬКО hook approach |
| `angle` | bmi, compliance | emotional_trigger, awareness_approach, hook_type |
| `frame` | bmi, angle | frame_type, proof_type, narrator_voice |
| `concept` | bmi, angle, frame | delivery, pacing, format |
| `everything` | bmi only | angle + frame + concept |

#### Язык вариаций

По geo: CL/LOCALE_MX/CO/AR/PE → es, BR → pt, US → en, RU/UA → ru, LOCALE_RO_→ ro.
Fallback: язык оригинального скрипта.

#### Для КАЖДОЙ вариации:

1. **Выбери angle из БД** (ротируй между вариациями). Если mode=everything — каждая вариация = другой emotional_trigger + frame_type.

2. **Собери GenerationContext из НАШИХ данных:**
   - BMIContext из нашего BMI
   - AngleContext из нашего angle
   - FrameContext из нашего frame
   - ResearchPackage (beliefs, arguments, objections, voice_dna, golden_quotes)
   - Winning Formula конкурента как extra_context (enrichment)

3. **Trigger → Opening:**
   - fear → THREAT
   - curiosity → MYSTERY
   - hope → VISION
   - anger → INJUSTICE
   - shame → MIRROR
   - empowerment → DECLARATION
   - envy → COMPARISON
   - urgency_fomo → COUNTDOWN

   **HOOK RULE BY NARRATOR:**
   - `first_person_user` (ugc, testimonial) → hook = MY pain, MY shame, MY moment. "Я" рассказываю свою историю.
   - `first_person_expert` (authority, not_your_fault) → hook = PATIENT'S pain first, THEN expert reveal. НИКОГДА не начинай с credentials ("Я доктор 23 года"). Начни с конкретного пациента в конкретной сцене боли → ПОТОМ раскрой кто ты. "Bărbatul din fața mea plângea de 20 de minute" → "Sunt urolog de 23 de ani." НЕ наоборот.
   - `second_person_direct` → hook = YOUR pain. "Ты лежишь ночью и считаешь минуты."

   **Принцип:** reader цепляется за БОЛЬ, не за credentials. Боль first, authority second. Всегда.

3b. **FRAME-DRIVEN VOICE (из выбранного frame):**
   - `narrator_voice = first_person_user` → narrator IS the patient: "Am simțit...", "Soția mi-a spus..."
   - `narrator_voice = first_person_expert` → narrator is insider/doctor: "În practica mea...", "Ce nu știu customersi..."
   - `narrator_voice = peer_friend` → narrator is friend/relative: "Soțul meu...", "L-am privit cum..."
   - `proof_type` determines primary evidence:
     - `testimonial` → personal story dominates, data supports
     - `research` → clinical data leads, story illustrates
     - `authority_figure` → expert quotes anchor each belief
     - `before_after` → transformation contrast drives structure
   - `credibility_storyline` determines trust model:
     - `been_in_your_shoes` → "Am fost unde ești tu" — peer authority
     - `robin_hood` → "Îți spun ce EI nu vor să știi" — conspiracy/insider
     - `expert` → "După 20 de ani de cercetare..." — credential authority
   - If spy hooks found: use as REFERENCE for hook energy, don't copy.

3c. **LEAD adapts to awareness level (from angle.stage_of_awareness):**
   - **unaware** → Lead = scene/story that CREATES awareness. No pain dump. 250-300 words.
   - **problem_aware** → Lead = identification through daily friction. ONE specific moment. 150-200 words.
   - **solution_aware** → Lead = short bridge. Reader knows solutions exist. Quickly differentiate mechanism. 100-150 words.

4. **Belief chain:** пройди через beliefs в порядке belief_order. Каждый belief = beat или transition в скрипте.

5. **Objections:** обработай в соответствии с placement (before/during/after mechanism reveal).

6. **Voice:** пиши в стиле voice_dna (phrase_markers, vocabulary_level). НЕ в стиле конкурента.

7. **НЕ КОПИРУЙ текст конкурента.** Это НОВЫЙ скрипт из наших данных. Winning Formula = compass, не blueprint.

8. **MECHANISM DEPTH BOUNDARY:** Раскрывай ПОЧЕМУ, не КАК ИМЕННО. EDITORIAL = curiosity о mechanism → клик. Детали = листикл.

9. **BODY VARIES WITH ANGLE:** Каждая вариация акцентирует РАЗНЫЕ beliefs:
   - anger → system betrayal beliefs
   - fear → mechanism/urgency beliefs
   - shame → identity beliefs
   - hope → transformation beliefs
   Same chain, different weight and order.

10. **URGENCY ROTATION:** Каждая вариация = другой urgency device (censorship / scarcity / deadline / social momentum). Никогда одинаковый.

11. **EXPERT NARRATOR = CASES, NOT AUTOBIOGRAPHY:** Если narrator_voice = first_person_expert → body через patient cases + data, не личную историю страдания. Gradualization через cases.

12. **HOOK = SCROLL-STOP:** 2-3 lines before "See More" = symptom + consequence + open loop. Problem CLEAR before click. Story setup AFTER.

13. **NARRATOR IN CHARACTER:** Patient narrator NEVER uses medical terms. "Mușchii de jos" not "planșeu pelvin." Medical terms only in doctor dialogue or expert narrator.

14. **TRANSFORMATION = SCENE, NOT TIMELINE:** One vivid scene > list of days. "Ziua 4... Ziua 14..." = report. Expand ONE moment into full sensory scene. Dates after, briefly.

15. **FAILED SOLUTIONS = ESCALATION:** Each failure = hope → crash mini-scene. Not a list of drug names. Escalate: cheap → expensive → humiliating.

16. **METAPHOR CALLBACK:** Single metaphor returns 2-3 times through text. Intro → body callback → transformation payoff.

17. **UNIQUE AHA-MOMENT PER VARIATION:** Never repeat same discovery moment across variations. Each = different trigger.

18. **CTA = DESIRE-PAINTING:** "Află ce au descoperit 1.247 de bărbați" > "Link mai jos, ce conține, cum comanzi."

19. **CONFLICT BEFORE RESOLUTION:** Between "found method" and "tried it" — narrator hesitates, almost doesn't try. Without conflict → transformation unearned.

20. **Длина:**
   - Если FORMAT = EDITORIAL: **1800-2500 слов** (no shorter than 1500, 2500+ only if 6+ beliefs)
   - Если FORMAT = video script: ≈ оригинал (+-20%)
   - Fallback: ≈ оригинал (+-20%)

#### Если grounding PARTIAL (нет BMI или нет research):

Генерируй, но:
- Предупреди: "Генерация без полного grounding — ниже уверенность в resonance"
- Используй Winning Formula как primary guide вместо research
- Audience signals из competitor analysis вместо нашего archetype
- Пометь: "Рекомендуется research validation перед запуском"

#### Output для КАЖДОЙ вариации:

```
---
## Вариация {N}/{count}

**Источник:** BMI "{bmi_name}" + Angle "{angle_name}" + Frame "{frame_name}"
**Enrichment:** WF insight — {какой именно инсайт из конкурента использован}
**Angle:** {emotional_trigger} → {hook_type}
**Frame:** {frame_type} / {proof_type} / {narrator_voice}
**Arc:** {emotional_arc}

### Скрипт

{ПОЛНЫЙ ТЕКСТ СКРИПТА на языке geo}

---
```

---

### Phase 4.5: CHIEFING PASS — Режь и точи каждый скрипт

После генерации КАЖДОЙ вариации — сделай chiefing pass. Ты = Copy Chief (Agora method). НЕ переписывай — РЕЖЬ и ТОЧИ.

**6 проходов по каждому скрипту:**

1. **SIMPLIFY** — 6th grade reading level. Каждое предложение должен понять 12-летний. Длинные предложения → разбей. Сложные слова → замени простыми. Если предложение > 15 слов → сократи.

2. **INJECT VERBATIM** — Найди 3+ места где можно вставить EXACT фразы из voice_dna.phrase_markers. Не перефразируй — вставь дословно. "просто живу в своих страданиях", "ne-au transformat în niște clienți" — именно так, как люди пишут на форумах.

3. **KILL REPETITIONS** — Найди предложения которые повторяют уже сказанное другими словами. Удали их. Каждое предложение = новая информация или новая эмоция. Если можно удалить предложение без потери смысла → удали.

4. **OPEN LOOP CHECK** — Hook создаёт ожидание? Body закрывает его? Если loop не закрыт → добавь payoff. Если hook не создаёт loop → переписать первые 2 предложения с open loop.

5. **STRENGTHEN** — Найди слабые/vague предложения: "он чувствовал себя лучше", "ситуация улучшилась", "было тяжело". Замени на конкретные сцены, телесные ощущения, specific numbers. "Было тяжело" → "Стоял в ванной в 3 ночи, трясся от боли, и считал минуты до утра."

6. **LOGIC-EMOTION CHECK** — Найди два логических предложения подряд (факт + факт). Вставь между ними эмоциональную реакцию. "chronic_condition cronică nu e condition_state. standard_treatment nu works." → "chronic_condition cronică nu e condition_state. Asta înseamnă că 7 ani am luat pill in vain. standard_treatment nu works."

**Output:** покажи chiefed версию скрипта. Пометь что изменилось:
```
### Chiefed скрипт (изменения помечены)

{текст с пометками [SIMPLIFIED], [VERBATIM INJECTED], [REPETITION KILLED], [STRENGTHENED]}
```

Если chiefing не улучшил скрипт (уже хорош) — скажи "Chiefing: minimal changes, script is already sharp."

---

### Phase 5: ИТОГ И РЕКОМЕНДАЦИИ

После генерации покажи:

```
## Итог

**Что взяли у конкурента:** {winning formula insights}
**На чём построено:** {наши BMI, archetype, beliefs}
**Research gaps:** {что стоит доисследовать для усиления}

### Следующие шаги
1. {если PARTIAL}: Провести research в направлении {X} для усиления grounding
2. Тестировать вариации через обычный pipeline
3. {если нашлись новые belief insights}: Рассмотреть добавление в belief chain BMI "{name}"
```

---

### Phase 5.5: СОХРАНЕНИЕ — Записать сессию в БД (АВТОМАТИЧЕСКИ)

**ВСЕГДА сохраняй. НЕ спрашивай CEO.** Без сохранения spy data не попадает в генерацию.

**Note:** Basic decomposition already ran at ingest (auto-decompose on save). `/rewrite` adds FULL analysis: cross-reference with our research, winning_formula depth, strategist review, and chiefing pass. The intelligence extracted here is richer than auto-decompose.

#### 1. Создать rewrite session

```bash
curl -s -X POST http://localhost:10000/api/rewrite/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "vertical": "{vertical}",
    "geo": "{geo}",
    "competitor_text": "{первые 500 символов конкурентского текста}",
    "competitor_source": "manual_paste",
    "winning_formula": {WF как JSON},
    "audience_signals": {audience signals как JSON},
    "grounding_level": "{strong/partial/weak}",
    "matched_archetype_id": "{archetype_id или null}",
    "matched_bmi_ids": ["{bmi_id1}", "{bmi_id2}"],
    "cross_reference_summary": {summary как JSON}
  }'
```

Запомни `session_id` из response.

#### 2. Сохранить каждый скрипт

Для каждой вариации:
```bash
curl -s -X POST http://localhost:10000/api/rewrite/sessions/{session_id}/scripts \
  -H "Content-Type: application/json" \
  -d '{
    "variation_index": {1/2/3},
    "script_text": "{raw script}",
    "chiefed_script_text": "{chiefed version}",
    "chief_notes": "{что изменил chiefing}",
    "bmi_id": "{bmi_id}",
    "angle_id": "{angle_id или null}",
    "frame_id": "{frame_id или null}",
    "emotional_trigger": "{shame/anger/fear/curiosity}",
    "hook_type": "{story_opening/bold_claim/etc}",
    "frame_type": "{testimonial_transformation/authority/etc}",
    "narrator_voice": "{first_person_user/first_person_expert}",
    "emotional_arc": "{shame_to_triumph/anger_to_hope/etc}",
    "enrichment_notes": "{какой WF insight использован}"
  }'
```

#### 3. EXTRACT — Записать spy findings в основные таблицы

**ОБЯЗАТЕЛЬНО после сохранения сессии.** Без этого spy data не попадёт в генерацию.

```bash
curl -s -X POST http://localhost:10000/api/rewrite/sessions/{session_id}/extract \
  -H "Content-Type: application/json"
```

Этот endpoint:
- Извлекает unmatched beliefs → записывает в `necessary_beliefs` (source_type="competitor")
- Извлекает hook_type/proof_type → записывает в `test_learnings` как LEARNED
- Помечает matched BMIs как `spy_validated=true`

Покажи результат:
```
## Spy Intelligence Extracted

Beliefs created: {N} (competitor gaps)
Learnings created: {N} (validated patterns)
BMIs validated: {N}

Эти данные теперь автоматически попадут в генерацию (/editorial, /longform_article, /generate-script).
War Room SpyNode обновится при следующем открытии.
```

#### 4. Показать итог сохранения

```
## Сессия сохранена + Intelligence extracted

**Session ID:** {id}
**Скрипты:** {N} сохранены
**Spy extract:** {beliefs_created} beliefs, {learnings_created} patterns, {bmis_validated} BMIs validated
```

---

### Phase 6: ИТОГ И РЕКОМЕНДАЦИИ

(бывший Phase 5)

После генерации покажи:

```
## Итог

**Что взяли у конкурента:** {winning formula insights}
**На чём построено:** {наши BMI, archetype, beliefs}
**Research gaps:** {что стоит доисследовать для усиления}

### Следующие шаги
1. {если PARTIAL}: Провести research в направлении {X} для усиления grounding
2. Тестировать вариации через обычный pipeline
3. {если нашлись новые belief insights}: Рассмотреть добавление в belief chain BMI "{name}"
```

---

## Rules

- **НИКОГДА не маппи конкурентский скрипт на наши сущности.** Извлекай insights, генерируй из своих данных.
- Winning Formula = compass, не blueprint. Вдохновение, не копирование.
- Каждая вариация = ПОЛНЫЙ скрипт, не outline
- Язык = по geo
- Voice = из НАШЕЙ voice_dna, не из конкурентского стиля
- Beliefs = из НАШЕЙ belief chain, обогащённой WF insight
- Если нет grounding → честно скажи, не генерируй из воздуха
- Compliance: numbers/claims из конкурента использовать ТОЛЬКО если подтверждены нашим research
- Beat structure конкурента = reference для структуры, не template для копирования
