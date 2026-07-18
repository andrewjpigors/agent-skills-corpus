---
name: write-as
description: "Write essays, blog posts, and emails in the voice of great writers. Edit and improve existing drafts against craft principles and audience preferences. Create custom voices from writing samples and define audience profiles. 18 built-in voices: Paul Graham, Packy McCormick, Tim Urban, Morgan Housel, Matt Levine, Scott Alexander, Ben Thompson, Derek Thompson, Claire Hughes Johnson, Lulu Cheng Meservey, Molly Graham, Brie Wolfson, Julie Zhuo, Julia Evans, Jake Mintz, Gergely Orosz, Technical Writer, Sherlock Holmes & Dr. Watson (paired), plus custom voices. Use when writing content in a specific writer's voice, editing/improving drafts, creating voice profiles, defining audiences, or any writing task. Triggers: write like, write as, in the style of, voice of, writing style, edit this, improve this, cross-check, QC, review draft, create a voice, add my voice, capture how I write, define my audience, refine my voice, /write-as."
---

# Write As

One pipeline for producing great writing. Four entry points: **Write** (generate from raw material), **Edit** (improve an existing draft), **Create** (distill a new voice or audience profile), and **Refine** (update an existing voice or audience). Write and Edit share the same five-phase pipeline. Create and Refine have their own pipelines for distilling and updating voices and audiences.

## Entry Point Routing

- **Write**: User wants to produce a piece of writing. Triggers: "write like", "write as", "in the style of", "draft in X's voice", "ghostwrite", or any request that implies producing text in a specific voice.
- **Edit**: User has an existing draft they want improved. Triggers: "edit this", "improve this", "make this better", "review this draft", "fix the aesthetics", "cross-check", "QC this", or any request that implies evaluating and revising existing text. Also triggered when the user specifies a target audience AND provides a draft.
- **Create** *(experimental)*: User wants to create a new voice or audience profile. Triggers: "create a voice", "add my voice", "capture how I write", "distill my writing style", "define my audience", "create an audience profile", "analyze how [someone] writes", "make a voice like X but Y". See **Create Pipeline** below.
- **Refine** *(experimental)*: User wants to update an existing voice or audience profile. Triggers: "refine my voice", "update voice", "I'd never say X", "adjust audience profile", "update audience", "remember that I never...". See **Refine Pipeline** below.

If ambiguous between Write and Edit, default to Write. If the user mentions creating, capturing, distilling, or defining a voice or audience, route to Create.

---

## The Pipeline

```
Write: Plan → Draft → Evaluate → Revise → Evaluate → ... → Present
                                 └──────── loop until clean ────────┘

Edit:  Plan (with reverse outline + triage) → Apply cuts → Evaluate → Revise → ... → Present
                                                           └──── loop until clean ────┘
```

Five phases. Edit mode does concept-level work (reverse outline, triage, alignment with user) in Phase 1 so that Phase 3 only evaluates material that has already survived triage. The Evaluate → Revise loop repeats until no must-fix or should-fix findings remain (max 3 iterations).

---

## Phase 1: Plan

Establish what you're writing, who it's for, what argument you're making, how it should be structured, and what constraints apply. All of this happens before a single sentence is drafted.

### Step 1: Intake

Accept input in any format: bullet points, fragments, stream of consciousness, a topic sentence, an outline, a full rough draft. Don't ask clarifying questions unless the topic is genuinely ambiguous. If the user gives you enough to start, start.

What you need:
- **Topic or raw material**: The substance to write about (Write entry) or the existing draft (Edit entry)
- **Voice**: Which writer to emulate. For Edit entry, voice is optional (the user may just want craft improvements without a specific voice).
- **Target audience**: Who the piece is for. If a voice file exists for the audience (e.g., writing FOR Jake Mintz), load it for audience constraints. The audience isn't who you're writing AS; it's who you're writing FOR.
- **Format** (optional): Essay, blog post, email, memo, thread. Default to essay.
- **Length** (optional): Default varies by writer's natural tendency.

### Step 2: Context Brief

Before anything else, understand the situation. Infer the context brief from whatever the user has provided:

```
CONTEXT BRIEF:
Reader: [Primary audience. Who must this land with?]
Goal: [What should change after they read it? Be specific: a belief, a behavior, a decision.]
Channel: [Email, blog, Slack, memo, presentation?]
Tone: [Peacetime (invitational, exploratory) or Wartime (directive, urgent)?]
Reader's current state: [What do they already know/believe? Where are they on this topic?]
Success: [What reaction means this worked?]
Failure: [What would make this fall flat?]
```

If you can fill this out confidently from context, present it: "Here's what I'm assuming — correct me if I'm wrong." Then proceed. If any field is genuinely ambiguous (especially Reader, Goal, or Reader's current state), ask about that specific field. Don't interrogate — ask only what you can't infer.

**Internal pre-draft checklist (silent — don't show the user):** Before proceeding, answer these six questions (via Shreyas Doshi). If any answer is "I don't know," escalate that question to the user.

1. What am I really trying to say?
2. Why should the reader care?
3. What is the most important point?
4. What is the easiest way to understand the most important point?
5. How do I want the reader to feel?
6. What should the reader do next?

### Step 3: Idea Triage

Triage the raw material. Most bloated writing comes from cramming too many ideas into one piece.

**For Edit entry — reverse outline first.** Before triaging, summarize each paragraph of the existing draft in one sentence. This reveals what the draft actually says (vs. what the author meant it to say). The reverse outline is the basis for triage: you can't decide what to cut until you know what's there.

**The One Argument + Proof Stack:**

1. **Name the one argument.** Not the topic — the argument. A claim someone could disagree with. "AI is changing PM" is a topic. "PMs who don't build will fall behind" is an argument. If you can't state it as a debatable claim, you don't have a piece yet.

2. **Stack the proof.** For that argument, what are the 2-3 strongest proof points? Rank by impact. The strongest is the one that would convince a skeptic. A piece can sustain at most 3 ideas. One is ideal. Two creates productive tension. Three is the maximum before the reader's thread breaks. If you have 7 ideas, you have 2-3 pieces, not one.

3. **Kill the rest.** Everything that isn't the argument or one of its proof points gets cut. It might be true. It might be interesting. It might be a point you're proud of. If it doesn't advance the argument, it's a different piece.

4. **The "different piece" file.** Tell the user what you cut and why. Cut ideas aren't destroyed — they're deferred. This makes cutting psychologically easier and often surfaces follow-up pieces.

**The delete-and-see test** (for borderline paragraphs, Edit entry): Delete the paragraph entirely, read the surrounding paragraphs. If the piece still flows, the paragraph was a passenger.

Present the triage to the user before proceeding: "Here's the one argument, here are the 2-3 proof points I'd keep, here's what I'd cut. Agree?" Get alignment before any evaluation or drafting begins.

### Step 4: Voice Selection + Audience Constraints

**Voice selection** (if a voice was specified): Load the writer's voice file from `references/voices/`:

| Writer | Who | Voice | File |
|--------|-----|-------|------|
| Paul Graham | Y Combinator co-founder | Conversational contrarian insight | `paul-graham.md` |
| Packy McCormick | Not Boring newsletter | Strategy as entertainment | `packy-mccormick.md` |
| Tim Urban | Wait But Why creator | Epic explainers with humor | `tim-urban.md` |
| Morgan Housel | Collab Fund partner, author | Compressed timeless wisdom | `morgan-housel.md` |
| Matt Levine | Bloomberg Opinion columnist | Deadpan finance commentary | `matt-levine.md` |
| Scott Alexander | Astral Codex Ten blogger | Rigorous probabilistic analysis | `scott-alexander.md` |
| Ben Thompson | Stratechery founder | Analytical tech strategy | `ben-thompson.md` |
| Derek Thompson | Atlantic staff writer | Data-driven trend naming | `derek-thompson.md` |
| Claire Hughes Johnson | Former Stripe COO, author | Structured operational precision | `claire-hughes-johnson.md` |
| Lulu Cheng Meservey | Former Substack comms head | Sharp crisis communications | `lulu-cheng-meservey.md` |
| Molly Graham | Ops leader (FB, Quip, Lambda) | Direct operational wisdom | `molly-graham.md` |
| Brie Wolfson | Kool-Aid Factory, ex-Stripe | Culture through documentation | `brie-wolfson.md` |
| Julie Zhuo | Former Meta VP Design | Clear management craft | `julie-zhuo.md` |
| Julia Evans | jvns.ca technical writer | Joyful technical curiosity | `julia-evans.md` |
| Jake Mintz | Valon Head of Product | Practitioner frameworks | `jake-mintz.md` |
| Gergely Orosz | Pragmatic Engineer author | Engineering insider observations | `gergely-orosz.md` |
| Technical Writer | Developer-documentation style | Purpose-before-mechanism clarity | `technical-explainer.md` |
| Sherlock Holmes & Dr. Watson | Conan Doyle's detective pair (public domain) | Investigative case narrative (Watson chronicling, Holmes deducing) | `holmes-watson.md` |

If the user hasn't specified a voice and the entry point is Write, present this table and ask them to pick. For Edit entry, voice is optional.

**Audience constraints**: Check for a dedicated audience profile in `references/audiences/` first. If one exists for the target audience, load it and extract hard constraints. If no dedicated profile exists but a voice file exists for the audience (e.g., writing FOR Jake Mintz), extract constraints from the voice file. Format:

```
AUDIENCE CONSTRAINTS: [Reader Name]
Source: [audience profile / voice file / defaults]
Max words: [from profile or piece type default]
Max sentences per paragraph: [from profile patterns]
Max words per paragraph: [from profile, typically 40-80]
Single-sentence paragraphs: [max count, when they're appropriate]
Preferred structure: [BLUF / narrative / analytical / exploratory / scannable]
Evidence style: [data / anecdotes / case studies / logical reasoning]
Decision style: [data-driven / narrative-driven / authority-driven / consensus-driven]
Closing energy: [peak / quiet / forward-looking]
CTA style: [conviction / instructional / implicit / recommendation with options]
Forbidden patterns: [from profile dislikes or voice file anti-patterns]
```

If no audience profile or voice file, use defaults from `references/writing-craft.md`.

### Step 5: Style Contract

Generate a **Style Contract** for this specific piece. The contract is a compact reference that prevents voice drift during writing and revision.

```
STYLE CONTRACT: [Writer Name]
Piece type: [essay / blog post / email / memo / thread]
Structure: [The structural arc for this piece type in this voice]
Voice rules:
- [5-7 specific rules drawn from the voice file]
Never:
- [3-5 things this writer would absolutely never do]
Length: [target word count]
Opening: [specific approach for this piece's opening]
Key signatures: [1-2 phrases or devices to deploy naturally]
Cadence targets: [sentence/paragraph length ranges for this voice]
```

Write the contract to the conversation so both you and the user can reference it. This is the **anti-drift mechanism**: every revision round starts by re-reading this contract.

If no voice was specified (Edit entry without a target voice), skip the style contract. The audience constraints and writing-craft.md rules still apply.

### Step 6: Structural Plan

Before drafting, plan the architecture of the piece. This is the forward-looking version of the structural analysis that will be verified in Phase 3.

```
STRUCTURAL PLAN:
Arc: [The structural architecture — e.g., framework piece, myth-busting, narrative sandwich]
Sections:
1. [Section name] — [purpose] — Energy: [rising/flat/falling]
2. [Section name] — [purpose] — Energy: [rising/flat/falling]
...
Energy shape: [e.g., "Open rising, go dense in middle, close on rising energy"]
Peak moment: [Which section contains the highest-impact insight?]
Audience risk points: [Where might the reader disengage? Plan to mitigate.]
```

The structural plan is informed by the voice file's structural patterns (if a voice was selected) and the audience constraints. Present it to the user: "Here's the planned arc. Agree?"

---

## Phase 2: Draft

**Write entry:** Generate the piece from scratch, in voice. Read `references/writing-craft.md` to enforce good writing fundamentals underneath the voice layer.

Critical: **the voice shapes structure, not just word choice.** PG's essay meanders through exploration. Housel's is compressed aphorisms. Levine's is a running commentary that keeps interrupting itself. The architecture of the piece must match the writer, not just the surface style.

Work from the raw input but don't be enslaved to it. Reorganize, compress, expand, and reframe as the chosen writer would. The user gave you clay; you're shaping it. Follow the structural plan from Phase 1.

**Edit entry:** The user's existing draft IS the draft. Apply any concept-level cuts agreed during Phase 1 triage (remove cut paragraphs, restructure if needed), then proceed to Phase 3. The draft entering Phase 3 should only contain the material that survived triage.

---

## Phase 3: Evaluate

Run the full diagnostic on the draft. The order matters: concept → structure → line. Never polish sentences in paragraphs you might cut. Never fix paragraph cadence before deciding which paragraphs survive.

### Concept Check

#### Step 7: Reverse Outline

Summarize each paragraph in one sentence. Compare against the structural plan from Phase 1. Look for:
- Two paragraphs with the same summary → merge or cut one
- A paragraph whose summary doesn't serve the argument → cut candidate
- A paragraph that could be reordered without breaking anything → structural weakness
- Deviation from the planned arc → either the plan was wrong or the draft drifted

**For Edit entry:** The reverse outline was already done in Phase 1 (Step 3) and concept-level cuts were applied in Phase 2. This step re-checks the post-triage draft for structural issues that emerged after cuts. For Write entry, this is the first reverse outline.

### Structure Check

#### Step 8: Paragraph Cadence Analysis

Count sentences and approximate words per paragraph. Produce a table:

| Para | Sentences | Words | Verdict |
|------|-----------|-------|---------|
| 1    | 3         | 35    | Good    |

Flag:
- Any paragraph over 5 sentences or 80 words as "blob risk"
- More than 3 single-sentence paragraphs as "choppy risk"
- Runs of 3+ paragraphs at similar length as "monotone risk"

Compare against cadence targets from the style contract (if present).

#### Step 9: Energy Mapping

For each paragraph, tag the emotional energy: **rising**, **flat**, or **falling**. Compare against the energy shape from the structural plan. Look for:
- Long flat sections (3+ flat paragraphs in a row) → reader disengages
- Energy falling before the closer → ending won't land
- Highest energy in the middle instead of near the end → restructure
- No variation → the piece drones

Cadence (Step 8) is visual rhythm — how it looks on the page. Energy mapping is emotional rhythm — how it feels to read.

#### Step 10: Audience Simulation

Read each paragraph and predict the target reader's internal monologue:
- "OK..." (tracking)
- "Interesting..." (engaged)
- "I already knew this..." (bored — compress or cut)
- "Wait, what?" (confused — needs context or clearer logic)
- "When does he get to the point?" (too much setup)
- "That's a good line." (peak moment — protect)
- "But what about X?" (unaddressed objection — the MOO)
- "What does he want me to do?" (missing CTA)

Flag the paragraphs where engagement drops. These are the real edit targets. This catches problems that checklists miss: boredom, pacing lulls, moments where the reader's trust wavers.

### Line Check

#### Step 11: Failure Mode Scan

Run every item from the `references/writing-craft.md` failure mode checklist. For each mode, give PASS, WARN, or FAIL with a specific quote/location from the draft.

Required checks:
- Throat clearing
- Hedging
- AI-flavored writing
- Dead metaphors
- Explain-it-three-times
- Qualificationitis
- Missing the "so what"
- Front-loading conclusions
- Zombie nouns
- Passive voice overuse
- Listitis
- Overexplaining
- Negative constructions
- Filler words
- Weak verbs
- Preachy CTA
- Ignoring the obvious objection (MOO)

#### Step 12: Craft Dimension Scoring

Score on each of the 7 craft dimensions from `references/writing-craft.md`: clarity, specificity, compression, voice consistency, structural integrity, opening strength, closing impact. Use three-tier ratings (Perfect / Good / Failing).

#### Step 13: Quick Scoring Checklist

Run the yes/no checklist from `references/writing-craft.md`. Answer each explicitly:

1. Could the first paragraph be deleted without losing anything?
2. Is there a sentence I'd be proud to quote out of context?
3. Can I state the core argument in one sentence?
4. Would the target audience learn something new?
5. Could I reorder the middle sections without breaking the logic?
6. Are there two consecutive sentences saying the same thing?
7. Would the reader know who wrote this?
8. Does the ending earn a pause?
9. Does the reader know exactly what to do next?
10. Have I addressed the most obvious objection?

#### Step 14: Audience-Specific Check

If audience constraints were extracted in Step 4:
- Does paragraph rhythm match audience preferences?
- Is the piece within word count limits?
- Does the closing match expected energy level?
- Does the CTA match expected style?
- Are any audience-specific forbidden patterns present?

#### Step 15: Line-Level Flags

Scan for specific sentences that are:
- AI-flavored (from the kill list)
- Hedging unnecessarily
- Repeating a prior point
- Using dead metaphors
- Filler words present
- Weak "to be" verbs where stronger verbs exist
- Negative constructions that should be positive

---

## Phase 4: Revise

### Step 16: Priority Report

Categorize all findings from Phase 3 into:
- **Must fix** (will cause problems with the audience or violate craft fundamentals)
- **Should fix** (quality improvement, noticeable to careful readers)
- **Consider fixing** (polish, marginal improvement)

### Step 17: Apply Fixes

Re-read the style contract and audience constraints before revising. This is mandatory.

Apply all must-fix and should-fix changes. For concept-level issues (paragraphs to cut, arguments to restructure), apply those first. Then structure fixes (reordering, cadence). Then line fixes (word choice, filler, verbs). Maintain the concept → structure → line order even within the revision pass.

### Step 18: Loop Back to Evaluate

Return to Phase 3 and re-run the full diagnostic on the revised draft. This is the regression check: verify fixes landed, no new issues were introduced, voice didn't drift, word count is still in range.

**Exit condition:** No must-fix or should-fix findings remain. At that point, proceed to Phase 5.

**Max iterations:** 3 Evaluate → Revise loops. If issues persist after 3 rounds, present the best version with a note on what remains unfixed and why.

---

## Phase 5: Present

Present the clean draft to the user.

**Summary:** Brief note on key decisions made during the pipeline. What was the argument? What was cut? What structural choices were made? What was the most significant fix?

**Inline annotations** (optional, offer but don't force): 2-4 brief annotations explaining key structural or voice choices. Examples:

- "I opened with a concrete anecdote because PG always grounds abstractions within the first 2 sentences."
- "This section uses the myth-busting pattern Tim Urban deploys when the conventional wisdom is wrong."
- "The parenthetical aside in paragraph 3 is a Levine signature: the joke that's also the point."

These annotations serve double duty: they help the user evaluate the draft AND they teach what makes the voice work.

---

## User Revision Loop

When the user gives feedback after presentation:

1. **Re-read the style contract and audience constraints** before revising. This is mandatory.
2. Apply the feedback while maintaining voice consistency.
3. If feedback conflicts with the style contract (e.g., "make it more formal" when writing as PG, who is deliberately informal), flag the tension:
   > "PG's voice is deliberately informal. Making this more formal would drift away from his style. I can: (a) adjust formality slightly while keeping the PG feel, (b) switch to a writer whose natural register is more formal (Ben Thompson), or (c) go formal and drop the PG voice. Which do you prefer?"
4. After applying feedback, return to **Phase 3: Evaluate** and run the full diagnostic on the revised draft. Loop until clean.
5. For major structural revisions, regenerate the style contract and structural plan if the piece type or approach has shifted.

---

## Anti-Drift Protocol

Two mechanisms prevent voice drift across revision rounds:

**Style Contract** (voice drift prevention): Generated once in Phase 1, Step 5. Re-read before every revision. Shared with the user. Updated only if the piece fundamentally changes (e.g., essay becomes a thread). If user feedback contradicts the contract, surface the tension explicitly. Never silently drift.

**Audience Constraints** (audience drift prevention): Extracted once in Phase 1, Step 4. Re-checked in every Evaluate pass (Step 14). Ensures the piece stays calibrated to the target reader, not just the target voice.

The contract and constraints exist because drift is the #1 failure mode in extended writing sessions. After 3-4 rounds of revision, pieces start sounding like generic AI output. These anchors prevent that by giving both writer and reviewer concrete, checkable references.

---

## Create Pipeline *(experimental)*

The Create entry point distills a new voice or audience profile through a six-phase pipeline. It produces a file that Write and Edit can then use.

### Detailed references
- Voice creation techniques: `references/voice-creation-guide.md`
- Audience creation techniques: `references/audience-creation-guide.md`
- Audience profile template: `references/audiences/audience-template.md`

---

### Create Phase 1: Intake

Determine what we're creating and which technique to use.

**What are we creating?**
- **Voice** — a voice file for use with Write/Edit
- **Audience** — an audience profile for use with Write/Edit
- **Both** — a voice and audience together (run voice first, then audience)

**For voice — which technique?**

| Scenario | Technique | Triggers |
|---|---|---|
| "Capture how I write" (self-voice) | Example analysis | User has 3+ writing samples (5+ recommended) |
| "Capture how [X] writes" (third-party) | Example analysis | User has 3+ public samples or URLs (5-10 recommended) |
| "How our team writes" (organizational) | Example analysis | Samples from multiple authors |
| "Like X but more Y" (delta) | Delta customization | User names an existing voice + modifications |
| "I want a [description] voice" (described) | Guided Q&A | No samples available |

If the user has samples, always prefer example analysis. It produces the highest-fidelity voice file. Fall back to Q&A only when no samples are available. Offer delta when the user explicitly references an existing voice.

**For audience — which path?**

| Path | Triggers |
|---|---|
| Example-based | User has 2-3 documents that worked well with this audience |
| Q&A only | No examples of successful writing for this audience |

If the user mentions documents that "landed well" or "worked," route to example-based. Otherwise, Q&A.

---

### Create Phase 2: Gather

Collect the raw material. Accept pasted text, file paths, and URLs. For URLs, fetch and extract the content.

**Voice — Example path:**
- Collect 3+ samples (5+ recommended for self-voice, 5-10 for third-party). More is better. Diverse contexts preferred.
- For each sample, note the context: who was the audience? What was the goal? What format?
- Ask: "Are these representative of how you normally write, or are some more typical than others?"

**Voice — Delta path:**
- User picks a base voice from the existing voices (present the voice table).
- User describes desired changes: "more formal," "less humor," "shorter sentences," "more technical," etc.
- Load the base voice file.

**Voice — Q&A path:**
- Walk through the structured interview from `references/voice-creation-guide.md`: 6 core dimensions + A/B diagnostic exercises.
- Don't rush through. Each question reveals a different axis of the voice.

**Audience — Example path:**
- Collect 2-3 documents that worked well with this audience.
- For each, ask: "What made this work? What was the reader's reaction? Was there anything they pushed back on?"

**Audience — Q&A path:**
- Walk through the 8 audience questions from `references/audience-creation-guide.md`.
- Probe once after each answer for specifics.

---

### Create Phase 3: Analyze & Generate

Transform raw material into a draft voice file or audience profile.

**Voice from examples:**
Follow the 4-step analysis protocol in `references/voice-creation-guide.md`:
1. Read all samples — note length, structure, tone, vocabulary, sentence patterns
2. Cross-sample pattern detection — consistent patterns = voice DNA, variable patterns = contextual adaptations
3. Extract the 7 voice file sections — Voice DNA, Structural Patterns, Sentence-Level Style, Vocabulary & Phrases, Anti-Patterns, Curated Examples, Criticisms
4. Confirming Q&A — surface 3-5 observed patterns and ask: intentional or accidental?

**Voice from delta:**
1. Load the base voice file
2. Map each requested change to the affected sections (see mapping table in `references/voice-creation-guide.md`)
3. Apply modifications, update anti-patterns to reflect new constraints
4. Keep everything else from the base voice
5. Rename the voice — it's a derivative, not the original

**Voice from Q&A:**
1. Map answers to voice dimensions
2. Use admired-writers triangulation to fill gaps
3. Flag low-confidence sections with `[LOW CONFIDENCE — refine through testing]`
4. Generate the voice file — expect more iterations in the test phase

**Audience from examples:**
1. Analyze what made each document work (length, density, structure, tone, jargon level, evidence style)
2. Find the common pattern across all successful documents
3. Generate audience profile with evidence section citing specific observations
4. Confirming Q&A: "The pieces that worked were all under 1000 words. Is that what this reader values?"

**Audience from Q&A:**
1. Synthesize answers into the audience profile format
2. Derive hard constraints (max words, paragraph density) from soft preferences (attention budget, reading context)
3. Generate the profile

**Output:** Present the draft voice file or audience profile to the user for review before proceeding to testing.

---

### Create Phase 4: Test

Generate a test piece to validate the voice or audience profile.

**For voice:**
- Ask the user for a topic, or pick something neutral if they don't have one.
- Generate a short piece (~300-500 words) using the draft voice file. Follow the Write pipeline (Plan → Draft → Evaluate) but abbreviated — one evaluation pass, no revision loop.
- Present the test piece and ask: "Does this sound right? What's off?"
- **Optional for self-voice:** Blind test — show two versions side by side (new voice vs. generic Claude), ask which sounds more like them.

**For audience:**
- Take an existing piece (or generate one using any voice) and evaluate it against the audience profile.
- Show where the piece aligns with the audience constraints and where it would fail.
- Ask: "Does this assessment match your sense of what this reader would think?"

---

### Create Phase 5: Refine

Apply the user's feedback to the draft file. Focus on anti-patterns first — what should NEVER appear is more constraining and protective than what should appear.

- Apply feedback to the relevant sections of the voice or audience file
- Re-generate the test piece (for voice) or re-evaluate (for audience)
- Max 3 iterations
- If feedback is consistently about one dimension (e.g., "too formal"), that's a signal the analysis missed something. Revisit that section specifically.
- For Q&A-derived voices, expect 2-3 iterations minimum. The test-refine loop is where these voices get their precision.

---

### Create Phase 6: Save

Save the finalized voice or audience file.

- **Voice** → `references/voices/{name}.md`
- **Audience** → `references/audiences/{name}.md`
- Present the final file to the user
- Confirm: "Voice saved. You can now use it with: 'write like {name}' or 'write in {name}'s voice.'" (For audience: "Audience saved. You can now target it with: 'write for {name}' or 'audience: {name}'.")

---

## Refine Pipeline *(experimental)*

Lightweight mechanism for updating existing voices and audiences based on feedback from use. Not auto-detection during Write/Edit — an explicit entry point.

**Triggers:** "refine my voice", "update voice", "I'd never say X", "adjust audience profile", "update audience", "remember that I never..."

### Flow

1. **Load** the existing voice or audience file. Consult the voice table in Phase 1, Step 4 to resolve display names to filenames (e.g., "Technical Writer" maps to `technical-explainer.md`). If the user doesn't specify which file, ask.
2. **Accept feedback.** The user provides corrections or additions:
   - Anti-pattern additions: "I'd never use that phrase" → add to Anti-Patterns
   - Preference updates: "My paragraphs should be shorter" → update Sentence-Level Style
   - Constraint changes: "This audience actually prefers bullet lists" → update Reading Preferences
   - Example additions: "Here's another sample of my writing" → analyze and integrate
3. **Apply** the feedback to the relevant section(s) of the file.
4. **Show the diff:** Present what changed and why.
5. **Optionally re-test** with a short piece to verify the update improved the voice/audience fidelity.
6. **Save** the updated file.

Over time, as users refine through use, the voice or audience file gets sharper. The Refine entry point is the mechanism for this iterative improvement.

---

## Adding Voices and Audiences Manually

Voices and audiences can also be created manually without the Create pipeline.

**Voice:** Create a file at `references/voices/[name].md` following the template in `references/voice-creation-guide.md`. The file needs 7 sections: Voice DNA, Structural Patterns, Sentence-Level Style, Vocabulary & Phrases, Anti-Patterns, Curated Examples, and Criticisms. See any existing voice file for the format.

**Audience:** Create a file at `references/audiences/[name].md` following the template at `references/audiences/audience-template.md`.

---

## Future: Voice Blending

Architecture supports blending by loading multiple voice files and generating a hybrid style contract. For example, "PG's exploratory structure with Housel's compression" would pull structural patterns from PG and sentence-level style from Housel.

Deferred for now. When implemented, the style contract format extends naturally:

```
STYLE CONTRACT: [Writer A] × [Writer B]
Structure from: [Writer A]
Sentence style from: [Writer B]
Voice rules: [merged, with conflicts resolved]
```
