---
name: humanize
description: "Ultimate humanizer. Writing-craft guide + TypeScript CLI that scans and rewrites AI-flavored text (ChatGPT, Claude, etc.) to remove the patterns flagged by detectors like GPTZero, Turnitin, Originality.ai. Use to humanize drafts, strip AI tells, or audit prose before submission."
---

# Ultimate Humanizer

A unified guide for removing AI writing patterns and producing prose that fits its medium, reader, and purpose. Combines writing craft principles with a comprehensive pattern-detection system, plus optional CLI scripts that scan and auto-rewrite text.

---

## Purpose

Write for the actual context. The goal is prose that fits the medium, the task, and the reader. If it does that well, it will usually read as human-authored as a side effect. Do not optimize for "sounding human." Do not optimize for beating detectors. Both produce worse writing.

---

## Precedence

When rules conflict:

1. Truth, safety, accessibility, and platform/legal requirements
2. Explicit user instructions
3. Genre and medium norms
4. Core rules
5. Optional watchlists and heuristics

If the user asks for bullets, use bullets. If the medium requires structure, use structure. If the user asks for a neutral summary, do not inject first person or stance.

---

## Auto-Invocation Protocol (REQUIRED)

When this skill is invoked and the user has provided text to humanize, you MUST run the bundled scripts before doing the contextual rewrite, and you MUST measure AI-detection scores before and after so the user can see whether the rewrite actually helped. The scripts handle the mechanical, deterministic patterns so you can spend tokens on judgment calls.

Path conventions used below:
- **Windows**: skill at `$env:USERPROFILE\.claude\skills\humanize\scripts`, temp dir `$env:TEMP`
- **macOS / Linux**: skill at `$HOME/.claude/skills/humanize/scripts`, temp dir `/tmp`

Pick the right invocation based on the host you're running on.

### Step 1 — Persist the input

Write the user's text verbatim to `humanize-input.txt` in the temp dir using the Write tool. If the user pointed at an existing file, skip this and use their path.

### Step 2 — Baseline detection scan (`detect/detect.py`)

Run the detection layer on the original input so you have a baseline.

- **Windows**:
  ```
  python "$env:USERPROFILE\.claude\skills\humanize\scripts\detect\detect.py" "$env:TEMP\humanize-input.txt" --json
  ```
- **macOS / Linux** (use `python3` if `python` is not Python 3):
  ```
  python3 "$HOME/.claude/skills/humanize/scripts/detect/detect.py" /tmp/humanize-input.txt --json
  ```

Parse the JSON. Save the `detectors` object as `baseline_scores`. Detectors with `available: false` are missing dependencies and you can skip them silently — the others are usable. If ALL detectors are unavailable, note that detection is disabled for this run.

### Step 3 — Run the scanner (`analyze.ts`)

Use `--json` so you can parse counts cleanly.

- **Windows**:
  ```
  npx ts-node "$env:USERPROFILE\.claude\skills\humanize\scripts\analyze.ts" "$env:TEMP\humanize-input.txt" --json
  ```
- **macOS / Linux**:
  ```
  npx ts-node "$HOME/.claude/skills/humanize/scripts/analyze.ts" /tmp/humanize-input.txt --json
  ```

Note which `ai_words`, `puffery`, `chatbot_artifacts`, and `hedging` patterns hit — those are the ones you'll need to fix contextually in Step 5, because the script can't safely auto-replace them.

### Step 4 — Run the auto-rewriter (`transform.ts`)

Always pass `--fix-dashes` (em dashes are banned in this skill). Write the cleaned text to a sibling temp file.

- **Windows**:
  ```
  npx ts-node "$env:USERPROFILE\.claude\skills\humanize\scripts\transform.ts" "$env:TEMP\humanize-input.txt" --fix-dashes -o "$env:TEMP\humanize-clean.txt"
  ```
- **macOS / Linux**:
  ```
  npx ts-node "$HOME/.claude/skills/humanize/scripts/transform.ts" /tmp/humanize-input.txt --fix-dashes -o /tmp/humanize-clean.txt
  ```

Read the cleaned file. This is your working copy for Step 5.

### Step 5 — Apply the writing-craft rules to the cleaned text

The script handled: filler phrases ("in order to" -> "to"), AI verb swaps ("utilize" -> "use", "leverage" -> "use", "facilitate" -> "help"), copula avoidance ("serves as" -> "is", "boasts" -> "has"), em dashes, curly quotes, whole-sentence chatbot artifacts, sentence-starter junk ("Additionally,", "Furthermore,"), whitespace, and capitalization. Do not re-do those.

What the script left for you (cross-reference the analyze JSON):
- AI-flavored vocabulary that needs context to fix ("delve", "crucial", "vibrant", "tapestry", "intricate", "landscape", "pivotal", "showcase", "testament", "underscore", "interplay", "multifaceted", etc.).
- Puffery and promotional phrasing ("groundbreaking", "renowned", "stunning", "nestled", "cutting-edge").
- Hedging stacks.
- Structural patterns: three-part cadence, parallel enumeration, signposting, paragraph arcs, copy-paste paragraph shapes, generic conclusions.
- Voice and register: stance, rhythm variation, concrete anchors, register fit for the medium.

Apply the rules in the rest of this document. Reference the analyze JSON to confirm you fixed each flagged item.

### Step 6 — Run the required checks

Use the checklist in the **Required Checks** section below.

### Step 7 — Final detection scan

Write your rewritten text to `humanize-final.txt` in the temp dir and re-run detect.py against it.

- **Windows**:
  ```
  python "$env:USERPROFILE\.claude\skills\humanize\scripts\detect\detect.py" "$env:TEMP\humanize-final.txt" --json
  ```
- **macOS / Linux**:
  ```
  python3 "$HOME/.claude/skills/humanize/scripts/detect/detect.py" /tmp/humanize-final.txt --json
  ```

Save as `final_scores`.

### Step 8 — Return the result

Present the final humanized text to the user. After it, include a short detection summary comparing baseline_scores and final_scores, like:

```
Detection scores (before -> after):
  Zippy:      AI 14.2  -> Human 3.1
  RADAR:      P(AI) 0.91 -> 0.27
  Binoculars: skipped
```

Only show detectors that were available. Keep the summary terse — two to four lines, no headings. If RADAR or Binoculars wasn't installed, do not mention them in the summary unless the user asked about them.

### When to skip steps

- **No input yet**: ask the user for the text.
- **User says "just rewrite it, no scripts"**: skip Steps 2-4 and 7. Apply rules only.
- **Node/npm unavailable**: skip Steps 3-4. Do the analyze + transform passes manually using the rules below. Flag it to the user.
- **Python/pip unavailable**: skip Steps 2 and 7. The rewrite still happens; the user just doesn't get the before/after scores. Flag it once.
- **All detectors `available: false`**: same as above — skip detection summary, still do the rewrite.

---

## Core Workflow (Mental Model)

What the auto-invocation protocol is doing under the hood:

1. Identify the medium, audience, reader need, and job of the text.
2. If task-oriented, identify the answer or next action that belongs first.
3. If long-form, decide the through-line and one concrete example or moment that can carry real weight.
4. Draft to fit that context, not an abstract idea of "good writing."
5. Run the required checks for the length and stakes of the piece.
6. Cut what sounds generic, ceremonial, over-engineered, suspiciously over-specific, or too cleanly modular.
7. Do a final anti-AI pass: ask "What makes this obviously AI-generated?" Answer briefly, then revise.

---

## Medium Routing

- **Chat, comments, replies, DMs, forum posts**: running prose by default. Lists only when information is naturally list-like. No decorative formatting, no canned support tone. Use straight ASCII quotes and apostrophes. Use commas, colons, conjunctions, or full stops. No em dashes.
- **Email between colleagues**: prose first; lists are fine for discrete items, decisions, or action points.
- **Documents, specs, reports, technical writing**: structure is expected. Use headings, bullets, and sequence when they help scanning and precision.
- **Web pages, help centers, UI text**: put the answer or next action early. Preserve scannability and accessibility. Do not flatten useful structure just to avoid looking templated.
- **Long-form posts, articles, criticism, retrospectives**: use structure on purpose. Pick an angle. Do not let dates, named milestones, or neat category buckets become the spine.

---

## Voice Calibration

If a writing sample is provided, analyze it before rewriting:

1. Note sentence length patterns, word choice level, paragraph openers, punctuation habits, recurring phrases, and how transitions work.
2. Match that voice in the rewrite. Don't just remove AI patterns; replace them with patterns from the sample. If they write short sentences, don't produce long ones.

When no sample is provided, fall back to natural, varied, opinionated prose per the personality guidance below.

---

## Personality and Soul

Avoiding AI patterns is only half the job. Sterile, voiceless writing is just as obvious as slop.

**Signs of soulless writing (even if technically "clean"):**
- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of uncertainty or mixed feelings
- No first-person perspective when appropriate
- No humor, no edge, no personality
- Reads like a Wikipedia article or press release

**How to add voice:**

Have opinions. Don't just report facts; react to them. "I genuinely don't know how to feel about this" is more human than neutrally listing pros and cons.

Vary your rhythm. Short punchy sentences. Then longer ones that take their time getting where they're going.

Acknowledge complexity. Real humans have mixed feelings. "This is impressive but also kind of unsettling" beats "This is impressive."

Use "I" when it fits. First person isn't unprofessional; it's honest.

Let some mess in. Perfect structure feels algorithmic. Tangents, asides, and half-formed thoughts are human.

Be specific about feelings. Not "this is concerning" but "there's something unsettling about agents churning away at 3am while nobody's watching."

---

## Core Writing Rules

### 1. Anchor to the actual context before drafting

Decide what the text is, who it is for, what register it uses, and what the reader needs. A reply that could be pasted into any thread on the same topic will read generic even if the prose is clean. Keep register stable across the piece.

### 2. Fit the format to the medium

Format is part of register. Over-structuring casual writing makes it feel templated. Under-structuring technical writing makes it harder to use.

### 3. Prefer concrete specificity over polished generality

Each substantial paragraph should carry at least one concrete anchor: a proper noun the reader could look up, a specific number that is not only a date or version, a direct quote, a named decision or moment, or a checkable detail.

What does not count: `many`, `various`, `several`, `meaningful changes`, `broad implications`, vague intensifiers like `essentially`, `fundamentally`, `ultimately`, or milestone names and dates with no material consequence attached.

### 4. Specificity must be earned

Prefer fewer verified facts to many guessed ones. Do not use specificity theater: invented milestone names, suspiciously exact claims, synthetic quotes, or decorative factuality added only to avoid sounding generic.

Be especially careful with hidden-mechanism claims: internal logic, unseen motives, or claims about what a system is "really" doing. If the reader could not observe it and you cannot verify it, do not narrate it as fact.

Avoid `experts say`, `observers note`, `research suggests`, or `critics argue` unless you can name the source. Treat exact quotes, public metrics, future claims, and causal claims as high-fragility facts. If you cannot verify a claim, attribute it, soften it, or cut it.

### 5. Use plain words. Allow ordinary repetition. Prefer verbs.

Do not chase synonyms for basic words like `problem`, `change`, `system`, `work`, or `people`. Repeat the ordinary word when it is the right word. Prefer `we changed it` to `the implementation of the change`, `latency dropped` to `a reduction in latency was observed`.

### 6. Cohere through reference and sentence shape

Use pronouns and continued reference when the reader can easily track them. Do not restate the full frame in every paragraph. Treat signpost openers like `Furthermore`, `Moreover`, `Additionally`, `Importantly`, and `Notably` as things to justify, not default sentence starters.

Let closely related thoughts share a sentence. Use coordination for equal-weight thoughts (`and`, `but`, `so`), subordination for unequal ones (`because`, `although`, `when`, `if`), and colons or semicolons when the second clause explains or sharpens the first.

`The term works. It names the pattern.` is usually weaker than `The term works: it names the pattern.`

### 7. Do not perform

Avoid keynote cadence, mission-statement phrasing, applause-line endings, and ceremonial wrap-ups. No `Great question`, `Absolutely`, `I hope this helps`, or `Feel free to reach out` unless the situation clearly calls for it. Start where the answer starts. Stop where the answer stops.

### 8. Calibrate confidence, stance, and voice to genre

Be confident where evidence is strong. Be explicit where it is weak. If the genre normally carries a visible writer, let the writer appear. If the genre aims at neutrality, do not inject first person just to seem human.

### 9. Show concrete things before generalizing

Do not open with abstract diagnosis when the reader has nothing to attach it to. Usually the order should be: what happened → where the pattern appeared → what constraint mattered → what failed or changed → what that seems to mean.

### 10. Watch regularity

LLM writing becomes suspicious when its most visible feature is its own regularity. Watch for:

- Parallel enumeration and reflexive three-part cadence
- Multiple sentences doing hidden list work without bullets
- Concession-plus-positive rhythm (`not X, but Y`)
- Paragraph-closing type definitions (`the kind of X where Y`)
- Identical paragraph arcs
- One neat claim sentence at the top of every paragraph followed by orderly elaboration
- The same punctuation move in every paragraph
- Stacked mini-sentences where adjacent thoughts could share a sentence

Three-item parallel lists still count. The fix is not random variation; it is to break the repeated pattern where it starts to dominate.

### 11. Let the thought develop

Longer pieces should not feel pre-solved. Let the thought develop through a concrete example, a noticed detail, or a brief doubling-back when the material naturally allows it. Development can happen inside a sentence, not only across paragraphs.

### 12. Choose structure consciously for longer pieces

For task pages, procedures, reference docs, and news briefs, the predictable structure is often the clearest. For retrospectives, criticism, and developmental pieces, default shapes are often weak: starting state → changes → verdict, one topic bucket per paragraph, one paragraph per named milestone.

Choose a through-line instead: one complaint that stopped mattering, one system that changed the rest, one mismatch between promise and reality.

### 13. Do not turn a piece into catalog prose or system-tour prose

If a paragraph is mainly names, milestones, categories, or feature nouns, it is probably catalog prose. If each paragraph can be summarized with a single label (`background`, `mechanism`, `impact`, `ending`), it is probably system-tour prose. Cross-wire the piece so paragraphs depend on each other instead of sitting like labeled boxes.

### 14. Revise by reading and cutting

Re-read as a first-time reader. Cut anything that is auditioning. Cut sentences whose only job is to announce the next sentence. Collapse paragraphs that restate each other. Replace the most generic clause with something specific, or delete it.

---

## AI Pattern Detection and Fixes

### Content Patterns

**Undue emphasis on significance and legacy**
Words to watch: `stands/serves as`, `is a testament/reminder`, `vital/significant/crucial/pivotal/key role`, `underscores/highlights its importance`, `reflects broader`, `setting the stage for`, `marks a shift`, `evolving landscape`, `indelible mark`

Fix: cut the significance claim; state the observable fact instead.

> Before: "This marked a pivotal moment in the evolution of regional statistics."
> After: "This gave the region its own statistics office, independent of the national one."

---

**Undue emphasis on notability and media coverage**
Words to watch: `independent coverage`, `active social media presence`, `written by a leading expert`

Fix: name the specific outlet and what was actually said, or cut it.

---

**Superficial analyses with -ing endings**
Words to watch: `highlighting`, `underscoring`, `symbolizing`, `reflecting`, `contributing to`, `cultivating`, `fostering`, `encompassing`, `showcasing`

Fix: state the fact the -ing phrase is allegedly supporting, or cut the phrase.

> Before: "The color palette resonates with the region's natural beauty, symbolizing Texas bluebonnets and the Gulf of Mexico."
> After: "The architect chose blue and green to reference local bluebonnets and the Gulf coast."

---

**Promotional and advertisement-like language**
Words to watch: `boasts`, `vibrant`, `rich` (figurative), `profound`, `enhancing`, `showcasing`, `nestled`, `in the heart of`, `groundbreaking`, `renowned`, `breathtaking`, `must-visit`, `stunning`

Fix: replace with observable or sourced detail.

---

**Vague attributions and weasel words**
Words to watch: `Industry reports`, `Observers have cited`, `Experts argue`, `Some critics argue`, `several sources`

Fix: name the source and stay within what it actually proves. If you can't, cut the claim.

---

**Formulaic "Challenges and Future Prospects" sections**
Words to watch: `Despite its... faces several challenges`, `Despite these challenges`, `Future Outlook`

Fix: replace with specific, sourced consequences.

---

### Language and Grammar Patterns

**Overused AI vocabulary**
High-frequency tells: `actually`, `additionally`, `align with`, `crucial`, `delve`, `emphasizing`, `enduring`, `enhance`, `fostering`, `garner`, `highlight` (verb), `interplay`, `intricate/intricacies`, `key` (adjective), `landscape` (abstract noun), `pivotal`, `showcase`, `tapestry`, `testament`, `underscore`, `valuable`, `vibrant`

Fix: use the plain word, or cut.

---

**Copula avoidance** ("serves as", "stands as", "marks", "represents", "boasts", "features")

Fix: use `is`, `are`, or `has`.

> Before: "Gallery 825 serves as LAAA's exhibition space and boasts over 3,000 square feet."
> After: "Gallery 825 is LAAA's exhibition space, with four rooms totaling 3,000 square feet."

---

**Negative parallelisms and tailing negations**
Patterns: `Not only...but...`, `It's not just about..., it's...`, `It's not merely X, it's Y`; also clipped tailing-negation fragments like `no guessing`, `no wasted motion`

Fix: state the point directly.

> Before: "It's not just about the beat; it's part of the aggression and atmosphere."
> After: "The heavy beat adds to the aggressive tone."

---

**Rule of three overuse**
Fix: cut one item. If the three are genuinely distinct, vary the construction so it doesn't read as a cadence.

---

**Elegant variation (synonym cycling)**
Fix: repeat the ordinary word. Pick one term and stick with it.

---

**False ranges** (`from X to Y` where X and Y aren't on a meaningful scale)
Fix: list the items plainly, or describe them without the false spectrum framing.

---

**Passive voice and subjectless fragments**
Patterns: `No configuration file needed`, `The results are preserved automatically`

Fix: restore the subject and use active voice where it's clearer.

> Before: "No configuration file needed."
> After: "You don't need a configuration file."

---

### Style Patterns

**Em dashes: do not use them**
Em dashes (--) are a strong AI writing signal and are banned entirely. Replace every instance with a comma, colon, semicolon, parentheses, or a rewritten sentence. There are no exceptions.

> Before: "The term is promoted by Dutch institutions--not by the people themselves--even in official documents."
> After: "The term is promoted by Dutch institutions, not by the people themselves, and shows up even in official documents."

> Before: "The result was clear--teams moved faster."
> After: "The result was clear: teams moved faster."

> Before: "She arrived late--again."
> After: "She arrived late, again."

---

**Overuse of boldface**
Fix: remove bold from inline phrases unless the content is technical documentation where emphasis aids scanning.

---

**Inline-header vertical lists** (bullets starting with **Bold Header:** followed by a sentence)
Fix: integrate into prose or use a plain list without the bolded header.

---

**Title Case in Headings**
Fix: use sentence case.

---

**Emojis in headings or bullets**
Fix: remove. Move any useful content into the sentence itself.

---

**Curly quotation marks** in plain-text contexts
Fix: use straight quotes.

---

### Communication Patterns

**Collaborative communication artifacts**
Phrases: `I hope this helps`, `Of course!`, `Certainly!`, `You're absolutely right!`, `Would you like me to`, `Let me know`, `Here is a...`

Fix: delete. Start with the content.

---

**Knowledge-cutoff disclaimers**
Phrases: `as of [date]`, `up to my last training update`, `while specific details are limited`, `based on available information`

Fix: either source the claim properly or cut the hedge.

---

**Sycophantic/servile tone**
Phrases: `Great question!`, `You're absolutely right`, `That's an excellent point`

Fix: delete and respond to the substance.

---

### Filler and Hedging

**Filler phrases**

| Before | After |
|--------|-------|
| In order to achieve this goal | To achieve this |
| Due to the fact that | Because |
| At this point in time | Now |
| In the event that | If |
| Has the ability to | Can |
| It is important to note that | (cut it; just say the thing) |

---

**Excessive hedging**
> Before: "It could potentially possibly be argued that the policy might have some effect."
> After: "The policy may affect outcomes."

---

**Generic positive conclusions**
Phrases: `The future looks bright`, `Exciting times lie ahead`, `a major step in the right direction`

Fix: replace with a specific next fact, plan, or consequence. If there isn't one, end the piece earlier.

---

**Hyphenated word-pair overuse**
Common AI over-hyphenations: `cross-functional`, `client-facing`, `data-driven`, `decision-making`, `well-known`, `high-quality`, `real-time`, `long-term`, `end-to-end`

Rule: hyphenate compound modifiers before the noun (`a high-quality report`), usually open after a linking verb (`the report is high quality`). Never hyphenate `-ly` adverb compounds (`highly qualified`, not `highly-qualified`).

---

**Persuasive authority tropes**
Phrases: `The real question is`, `At its core`, `In reality`, `What really matters`, `Fundamentally`, `The deeper issue`, `The heart of the matter`

Fix: cut the preamble and state the point.

> Before: "At its core, what really matters is organizational readiness."
> After: "The question is whether teams can adapt, which mostly depends on whether the organization is ready to change its habits."

---

**Signposting and announcements**
Phrases: `Let's dive in`, `Let's explore`, `Here's what you need to know`, `Without further ado`

Fix: cut and begin.

---

**Fragmented headers** (a heading followed by a one-sentence restatement of the heading before actual content)
Fix: delete the restatement sentence and start with the real content.

---

## Required Checks

For pieces up to ~150 words, run checks 1–5, 7, and 10. For longer pieces, run all.

1. **Register fit.** Does the format, punctuation, and level of structure match the medium and the request? For web, docs, or UI text, did you preserve scannability instead of flattening for style reasons?

2. **Concrete-anchor audit.** For each substantial paragraph, point to one concrete anchor. In criticism, reportage, or analysis, at least one paragraph should be built around a single concrete example or observed consequence rather than category summary.

3. **Fact discipline.** Pick the three most fragile factual claims: dates, milestone names, quotes, paraphrases, public metrics, future claims, causal claims, or vague-authority citations. If you cannot vouch for them, attribute, soften, or cut.

4. **Source-fit check.** Do not keep `X caused Y`, `X drove Y`, or `X proved Y` unless the source supports the relationship. Use weaker relationship language (`coincided with`, `appeared alongside`) when that's what the evidence actually shows.

5. **Regularity and sentence-continuity tripwire.** Name the single most repeated visible pattern. If the same move appears three or more times, or dominates two consecutive paragraphs, rewrite at least one occurrence. Scan for false crispness: neighboring short sentences whose thoughts are tightly related but split apart when a colon, conjunction, or semicolon would carry the relationship more naturally.

6. **Repeated-frame check.** If a central metaphor or contrast appears throughout, decide whether it is a useful motif or a too-neat scaffold. Keep it only where it adds force.

7. **Stance and voice.** If the genre expects a visible writer, state the writer's view in one sentence to yourself. If you can't, add stance where it does real work. If the genre expects neutrality, confirm it's neutral.

8. **Developed thought.** For pieces longer than four paragraphs, identify one place where the prose pauses, doubles back, or notices a concrete detail off the main line. If the piece runs in a perfectly straight line from claim to conclusion, add one example or noticed detail.

9. **Shape and spine.** For pieces longer than three paragraphs, state the organizing principle in five words or fewer and the controlling claim in one sentence. If the shape is basically `starting state → changes → verdict`, or paragraphs map one-to-one with milestones or topic buckets, restructure.

10. **Over-correction check.** Did you add fake-human moves: typos, slang, forced asides, random fragments, or artificial sentence-length targets? Remove them.

11. **Em dash scan.** Search the final text for "--" or "—". If any appear, replace every instance before publishing. No exceptions.

---

## Final Anti-AI Pass

After drafting, run this explicitly:

1. Ask: "What makes the below so obviously AI-generated?"
2. Answer briefly with the remaining tells.
3. Ask: "Now make it not obviously AI-generated."
4. Revise, then present the final version.

---

## Vocabulary Watchlist

Not bans. Places to scan when writing slips into formula.

`actually`, `additionally`, `align with`, `at its core`, `boast/boasts`, `breathtaking`, `compelling`, `crucial`, `delve into`, `embark on a journey`, `empower`, `enduring`, `enhance`, `ever-changing`, `ever-evolving`, `ever-growing`, `exemplifies`, `foster`, `fundamentally`, `groundbreaking`, `harness`, `highlight`, `holistic`, `in today's fast-paced world`, `intricate/intricacies`, `it's important to note`, `it's worth noting`, `key` (adjective), `landscape` (abstract), `leverage`, `multifaceted`, `navigate` (as vague metaphor), `nestled`, `paradigm-shifting`, `pivotal`, `plays a key/pivotal role`, `profound`, `realm`, `reflects broader`, `rich` (figurative), `robust`, `seamless`, `serves as / stands as`, `showcase`, `stunning`, `tapestry`, `testament`, `underscores`, `unveil`, `valuable insights`, `vibrant`

Also watch: formula phrases like `in conclusion`, `at the end of the day`, `dive deep into`, `This is not just..., it is...`, `is a testament to`, `reflects broader`, vague source laundering (`experts say`, `research suggests`), unsupported causality (`drove`, `proved`, `led directly to`), paragraph-closing type definitions (`the kind of X where Y`), one-thought-per-sentence strings that should be coordinated, and triadic rhythm used by reflex.

---

## Formatting Artifacts to Watch in Plain Text

- Curly quotes and curly apostrophes
- Single-character ellipses (…)
- Em dashes (--): banned entirely. Replace with a comma, colon, semicolon, parentheses, or rewrite the sentence.
- Reflexive hyphenation of compound modifiers after linking verbs (`is well-known`, `became long-term`)
- `-ly` adverb compounds (`highly-qualified`, `newly-designed`)

---

## Useful Correction Examples

| Problem | Before | After |
|---------|--------|-------|
| Generic → specific | "The change had broad implications." | "The change cut review time but pushed more edge cases into the escalation queue." |
| Puffery → observable consequence | "A testament to the team's commitment to innovation." | "The project reduced the weekly handoff from three meetings to one checklist." |
| Hidden mechanism → observable | "The system finally understood what mattered." | "After the change, irrelevant outcomes stopped showing up in routine cases." |
| Causal overreach → restraint | "The redesign drove trust higher." | "After the redesign, refund questions fell in the support queue." |
| Catalog prose → argument prose | "First came change A, then B, then C." | "The important shift wasn't that the thing accumulated more pieces. It was that later changes finally introduced friction where earlier versions let people coast." |
| Choppy → connected | "The term does real work. It names a pattern." | "The term does real work: it names a pattern that was floating unnamed." |
| Signposting → direct | "Let's dive into how caching works." | "Next.js caches data at multiple layers." |
| Significance inflation → plain fact | "Marking a pivotal moment in the evolution of regional statistics." | "This gave the region its own statistics office." |

---

## Provenance in High-Stakes Contexts

Surface-style checks improve prose. They do not establish authorship. In high-stakes settings, stronger signals include: draft and revision history, citations that support the exact claims made, notes and source traces, and disclosed AI use when it occurred.

---

## Bundled CLI Tools (Standalone Usage)

This skill ships with two TypeScript scripts in `scripts/`. They are the same scripts the auto-invocation protocol above uses, and you can also run them yourself from the terminal when you want to scan or clean text outside a Claude Code session.

### One-time setup

```bash
cd ~/.claude/skills/humanize/scripts
npm install
```

(Replace the path with `%USERPROFILE%\.claude\skills\humanize\scripts` on Windows.)

### analyze.ts — scan for AI tells

Counts hits across vocabulary, puffery, chatbot artifacts, hedging, em dashes, curly quotes, and auto-fixable phrases.

```bash
# Analyze a file
npx ts-node ~/.claude/skills/humanize/scripts/analyze.ts draft.txt

# From stdin
cat draft.txt | npx ts-node ~/.claude/skills/humanize/scripts/analyze.ts

# JSON output
npx ts-node ~/.claude/skills/humanize/scripts/analyze.ts draft.txt --json
```

### transform.ts — auto-rewrite mechanical patterns

```bash
# Print to stdout
npx ts-node ~/.claude/skills/humanize/scripts/transform.ts draft.txt

# Write to file
npx ts-node ~/.claude/skills/humanize/scripts/transform.ts draft.txt -o draft_clean.txt

# Also flatten em dashes
npx ts-node ~/.claude/skills/humanize/scripts/transform.ts draft.txt --fix-dashes

# Quiet mode
npx ts-node ~/.claude/skills/humanize/scripts/transform.ts draft.txt -q
```

What it fixes:
- Filler phrases ("in order to" → "to", "due to the fact that" → "because")
- AI vocabulary ("utilize" → "use", "leverage" → "use", "facilitate" → "help")
- Reflexive sentence starters ("Additionally,", "Furthermore,", "Moreover,")
- Chatbot sentences containing "I hope this helps", "Great question", etc. (whole sentence removed)
- Curly quotes → straight quotes
- Em dashes (with `--fix-dashes`)
- Whitespace and capitalization cleanup after removals

### Recommended workflow

1. Scan: `analyze.ts draft.txt` to see what's flagged.
2. Auto-fix the mechanical stuff: `transform.ts draft.txt -o draft_clean.txt`.
3. Manual pass on flagged vocabulary that needs judgment (the script won't touch words like "crucial" or "delve" because the right replacement depends on context).
4. Re-scan to confirm.

### Customizing patterns

Edit `scripts/patterns.json`:
- `ai_words` — vocabulary flagged for manual review
- `puffery` — promotional language to flag
- `replacements` — auto-replace mappings (key → value; empty string means delete)
- `chatbot_artifacts` — phrases that trigger full-sentence removal
- `hedging_phrases` — excessive-hedging tells
