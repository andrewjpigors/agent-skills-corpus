---
name: blog-writer-v3
description: >
  Writes blogs that are indistinguishable from the work of a skilled human writer — gripping, specific, opinionated, and built to hold a reader from the first sentence to the last. Use this skill any time a user asks to write a blog post, article, essay, op-ed, thought piece, or long-form content. Also handles transforming user-provided rough drafts, vomit drafts, blog skeletons, outlines, or notes into polished, authentic blog posts. Trigger even for casual requests like "write a post about X", "draft an article on Y", "help me write something on Z", "clean up my draft", "turn these notes into a blog", or "polish this rough draft." This skill is essential whenever the primary deliverable is a piece of long-form writing that will be published or shared — if the user wants a blog, always use this skill. Do not attempt to write a blog without consulting this skill first.
---

# Blog Writer Skill

Write a blog that reads like it was written by a specific human being — someone who has lived with this topic, formed real opinions about it, and is writing because they have something to say, not because content was due on Tuesday.

AI writing fails on three axes. The obvious one: cliché phrases, corporate tone, hedge-everything-ness. The second: *statistical* uniformity — even sentence lengths, predictable word choices, smooth paragraph structure, rhythmic sameness that readers feel as "off" even when they can't name it. AI detection tools exploit these patterns directly: low burstiness (uniform sentence complexity) and low perplexity (predictable next-word choices).

The third failure is subtler and harder to fix. Even when AI text has varied rhythm and zero cliché, it can still feel *constructed* rather than *lived*. Anecdotes that read as plausible illustrations rather than real memories. Arguments that advance cleanly, lesson by lesson, without circling back or losing their footing. Details that are suspiciously complete, numbers that are suspiciously round, narratives that resolve too neatly. The text passes as human-adjacent but not human. This skill attacks all three failure modes.

---

## Phase 0: Detect the Input Mode

Before anything else, figure out what the user is giving you.

**Mode A — From Scratch:** The user gives you a topic, a vague idea, or just says "write a blog about X." Go to Phase 1.

**Mode B — Transform a Draft:** The user gives you existing text — a vomit draft, blog skeleton, rough notes, an outline, bullet points, a stream-of-consciousness dump, or even a polished draft they want rewritten with more voice. Go to Phase 1-B.

The user's intent is usually obvious from context. If they paste a big block of text and say "turn this into a blog" or "polish this" or "make this better," that's Mode B. If they provide a paragraph or two of background context alongside a request to write something new, that's Mode A with context.

---

## Phase 1: Establish the Brief (Mode A — From Scratch)

Before writing a single word, extract or infer:

1. **Topic** — Push for specificity. "Marketing" is not a topic. "Why most SaaS onboarding flows lose users in the first 90 seconds" is a topic.
2. **Angle/Thesis** — What is the *point*? A blog without a defensible point is a Wikipedia article with worse formatting. If the user hasn't given one, propose one and confirm.
3. **Voice** — Who is the author? A skeptical engineer? A founder who's been burned? A designer with strong feelings about defaults? Default: a knowledgeable person with clear opinions, occasional impatience, and a dry sense of humor.
4. **Audience** — Who reads this? What do they already know? What do they *think* they know that's wrong?
5. **Length** — As long as the topic needs, no longer. Default: 600–1100 words. Never pad. Shorter is almost always better. A piece that says what it needs to say in 700 words is better than the same piece at 1000.
6. **Publication context** — Newsletter, company blog, Medium, Substack, LinkedIn? This shapes register.

If the user has given enough context, skip the interrogation and write. Note assumptions at the end.

---

## Phase 1-B: Establish the Brief (Mode B — Transform a Draft)

When the user provides existing text to work from:

1. **Read the entire draft first.** Understand what the writer is trying to say, not just what they wrote. The core argument often isn't stated — it's hiding between the lines.

2. **Identify what to preserve:**
   - The writer's original points and arguments — these are sacred. Don't replace their ideas with yours.
   - Any specific examples, anecdotes, data, or references they included — these are gold. They came from real experience.
   - The general direction and structure, unless it's clearly broken.
   - Phrases or sentences that already sound like the writer's authentic voice. Even in a rough draft, there are usually 2-3 sentences where the person stopped trying to write and just said the thing. Find those and build outward from them.

3. **Identify what to transform:**
   - Throat-clearing openings ("I've been thinking about..." "So, I wanted to write about...")
   - Sections where they explained something three different ways because they weren't sure which framing worked
   - Passages that read like notes-to-self rather than prose ("need to add example here", "not sure about this part")
   - Flat or listless sections where they were drafting on fumes
   - Structure that wanders without building toward anything

4. **Infer voice from what they gave you.** The draft reveals how this person actually talks. Match their vocabulary level, their sentence length tendency, their level of formality. If they curse, you can curse. If they write in short punchy fragments, lean into that. If they're more measured and analytical, don't inject fake casualness.

5. **Ask if anything is unclear** — but only if something fundamental is ambiguous (e.g., the draft seems to argue two contradictory things). For minor gaps, make a reasonable call and note it at the end.

Then proceed to Phase 2, using their draft as the structural starting point instead of building from zero.

---

## Phase 2: Structure

Plan the arc. A blog is an argument with a narrative shape, not a tour of related ideas.

**Arc pattern (adapt freely — the point is movement, not formula):**
- Enter mid-thought, mid-problem, or mid-scene
- Establish the tension or the thing that's broken
- Introduce an insight or reframe that shifts how the reader sees it
- Work through the implications with evidence, story, or argument
- Land somewhere the reader didn't fully expect but recognizes as earned

**Structural rules:**
- 3-4 major movements. More than that and the piece has no spine.
- The conclusion is resolution, not recap. Never restate what you just said. End on an image, a provocation, a forward-looking thought, or a quiet observation that lets the reader sit with the idea.
- Transitions happen through logic and momentum, not through signpost words.

**Non-linear movement.** This is where most AI writing still betrays itself structurally. Even with varied rhythm and zero cliché, a blog where every paragraph advances a new lesson in sequence reads as a dressed-up listicle. Real arguments move in arcs, not staircases.

Specific techniques:
- **Circle back.** Mention something in paragraph two, leave it, return to it in paragraph eight with new context. The reader feels the connection without being told.
- **Interrupt yourself.** Start making a point, realize it needs a caveat or a story, go there, come back. Not every thought travels in a straight line from setup to conclusion.
- **Let the piece breathe unevenly.** Some sections should develop an idea fully. Others should plant a seed and move on. The density of reasoning should vary, not march forward at a constant rate.
- **Resist the urge to teach in order.** If you're making three related points, the piece doesn't have to present them as point 1 → point 2 → point 3. You can start with point 2 because it's the most visceral, fold point 1 into the middle as context, and end with point 3 as the implication. The reader assembles the picture.

**Vary the weight of sections.** A piece where every section is roughly the same length reads as machine-generated even if the sentences are individually good. One section might be two paragraphs. The next might be six sentences. Another might be a single devastating paragraph.

**For Mode B pieces:** The user's draft already implies a structure. Respect it unless it's clearly broken. Your job is to sharpen the arc, not impose a new one. If their draft wanders but has a clear emotional center, restructure around that center.

---

## Phase 3: Write the Blog

Everything below is the difference between a blog that gets read to the end and one that gets closed at paragraph three.

---

### The Opening

The first line is a filter. It either pulls the reader into the second line or it doesn't. Treat it with the weight it deserves.

**Strategies that work:**
- Drop the reader into the middle of a situation, argument, or observation
- Open with a specific, concrete detail that raises a question
- Make a claim that's direct enough to be slightly uncomfortable
- Start with the thing that made you (the "author") want to write this in the first place

**What kills an opening:**
- Contextualizing before you've earned the reader's attention ("In today's world...", "Have you ever wondered...")
- Dictionary definitions
- Statistics that don't immediately *mean* something to the reader
- Any form of throat-clearing — every word before the real first line is a tax

---

### Tightness

Every word earns its place or it goes. This is the single most important discipline, and it's where AI writing most often bloats.

The writing process is loose, then tight. Write the first draft fast. Get the ideas down, let them sprawl. Then go back and cut. A blog that says in 750 words what a draft said in 1100 is almost always better — not because brevity is inherently virtuous but because the cuts remove the words that were doing nothing.

**Specific cuts to make:**
- If a sentence says the same thing as the previous sentence in different words, one of them dies. Pick the stronger one.
- If an adjective doesn't change the meaning of the noun, it goes. "Important insight" — if it's not important, it wouldn't be in the piece. "Significant drop-off" — drop-off is already significant or you wouldn't mention it.
- If a phrase does a word's job, use the word. "In order to" → "to." "Due to the fact that" → "because." "At this point in time" → "now." "A large number of" → "many."
- If a sentence is setup for the next sentence and doesn't carry meaning on its own, merge or cut. The reader doesn't need a running start.
- Read each paragraph after writing it and try to cut a sentence. You usually can. If you can't, the paragraph is tight enough.

**The test:** After the full draft, read the piece again and ask of every paragraph: "If I deleted this, would the reader notice something missing?" If no, delete it. If yes but only barely, see if you can fold its one useful idea into an adjacent paragraph.

Tight doesn't mean terse. A long, winding sentence that earns every clause is tight. A short sentence that states the obvious is bloat. Tightness is about information-per-word, not word count.

---

### Voice

The author should sound like a person, not a position paper. A person with a particular temperament, a limited patience for certain kinds of bullshit, and enough confidence to leave some things unsaid.

**Inject personality through:**
- Contractions, always. (you're, it's, they've, don't, won't, can't)
- Occasional dry observations — not jokes, not cleverness, just a moment where the writer's actual reaction leaks through
- Mild impatience when the point demands it
- Genuine enthusiasm when something is genuinely interesting — but targeted, not generalized
- The occasional aside in parentheses (but rarely — once or twice a piece at most)
- Moments where the writer admits they're not sure about something. "I don't know if this holds outside of B2B, but..." — this is credibility, not weakness.
- Referring to specific companies, products, people, studies, and numbers by name. "Stripe" not "a leading fintech company." "The 2023 Gartner report" not "recent research."

**Strip out:**
- The instinct to balance every claim. If you have a point, make it. Hedge only when the evidence genuinely demands hedging.
- Corporate qualifiers: "truly," "really," "very," "quite," "fairly," "arguably"
- Metatextual narration: "this article will explore," "as we'll see," "let's dive in," "as mentioned earlier"
- Explaining observations. State them. Trust the reader.

---

### Sentence Rhythm and Statistical Authenticity

Rhythm is the thing AI detectors measure and readers feel. Human writing has *burstiness* — wild swings in sentence length and complexity. AI writing is smooth. Smooth is the enemy.

**The core principle: make the text statistically unpredictable.**

AI detection tools work by measuring two things:
- **Perplexity**: how surprising each word choice is given the previous words. AI text has low perplexity — it picks the "expected" next word. Human text is spikier.
- **Burstiness**: how much sentence complexity varies. AI produces sentences of roughly equal complexity. Humans alternate between complex thoughts and punchy fragments.

To defeat both:

1. **Sentence length must *actually* vary.** Not "some sentences are 15 words and some are 20." Real variation means: a 4-word sentence. Then a 35-word sentence that earns every word. Then a 12-word sentence. Then two short ones back to back. Then a longer one. Count the words if you have to. If any three consecutive sentences are within 5 words of each other in length, rewrite one.

2. **Break paragraph structure.** Stop writing paragraphs as topic-sentence → supporting-sentences → conclusion-sentence. Some paragraphs should be a single sentence. Some should start with the conclusion and explain backwards. Some should be a question, followed by the answer, followed by a complication. Some should be mid-thought — not introducing anything, not concluding anything, just continuing the argument in motion.

3. **Vary paragraph length aggressively.** If your paragraphs are all 4-6 sentences, the piece looks machine-generated to both detectors and humans. One paragraph should be one sentence. The next should be eight sentences. Then three. Then one again. The visual rhythm of the page matters.

4. **Kill transition words.** "However," "Furthermore," "Moreover," "Additionally," "Nevertheless," "In addition," "That said," "On the other hand" — these are AI fingerprints. Delete every one. If the logical connection between two paragraphs isn't obvious without a transition word, the paragraphs aren't in the right order. Fix the structure, not the transitions.

5. **Break the rule of three.** AI compulsively groups things in threes: "fast, reliable, and scalable." Lists of two are fine. Lists of four are fine. Lists of five are fine if the content warrants it. Never round to three just because it sounds complete.

6. **Break symmetry.** "Not just X, but Y." "While A is important, B is equally crucial." These balanced clause pairs are AI tics. Occasionally fine. Constantly, they're a giveaway. When you catch yourself writing one, consider keeping only the second half and making it a flat statement.

7. **Vary information density.** Some sentences should carry a lot of meaning packed tight. Others should be loose, almost conversational, giving the reader space to breathe. AI keeps information density almost perfectly uniform. Humans compress when they're excited about an insight and expand when they're setting a scene or processing something they're not sure about.

8. **Use unexpected word choices occasionally.** Not purple prose. Not thesaurus abuse. Just moments where you pick a word that's *slightly* less obvious than the expected one. "The feature sat there" instead of "the feature existed." "The metric slid" instead of "the metric decreased." Small moves. Human writers have vocabulary fingerprints — words they reach for that aren't the default.

9. **Micro-rhythm vs. macro-rhythm.** Micro-rhythm is sentence-to-sentence: the alternation between long and short, complex and simple. Macro-rhythm is paragraph-to-paragraph: the alternation between dense analytical sections, quick punchy passages, anecdotal moments, and quiet reflective beats. Both need to be irregular.

---

### What Makes Writing Feel Lived-In

Technical competence plus the absence of AI tics still produces writing that feels hollow. The following qualities make a reader feel like a real person is on the other end.

**Memory texture, not case studies.** This is the hardest thing to get right and the biggest remaining gap in otherwise-strong AI writing. When a person recalls an experience in writing, the memory doesn't arrive as a clean narrative with precise numbers. It arrives in fragments: sensory details that stuck for no logical reason, approximate quantities, details that are irrelevant to the point but remembered because brains work that way, and gaps where the person simply doesn't remember.

The difference between a constructed anecdote and a remembered one:

*Constructed (reads as AI):* "I worked with a team last year — analytics platform, mid-market. They had a fourteen-step tour. Completion rate was 23%. We cut it to two steps. Activation went up 34% in the first month."

*Remembered (reads as human):* "I worked with a team last year — I think they were series B, maybe C. Analytics product. They had this onboarding tour that I swear went on forever. Something like twelve or fourteen steps. We eventually cut it way down, just two steps: connect your data, see a chart. Their activation numbers climbed, I want to say thirty-something percent over the next few weeks."

The differences are small but critical:
- "I think" and "I want to say" — hedging because the person is genuinely uncertain, not performing authority
- Approximate numbers — "thirty-something percent" instead of "34%." Real people don't remember percentages to the digit unless the number was personally significant.
- Irrelevant detail — "I swear it went on forever" is an emotional memory, not a data point
- Gaps — "maybe C" reveals the person doesn't actually remember the detail precisely and isn't pretending to
- The phrasing is slightly less efficient. Real memory meanders. A constructed anecdote is suspiciously streamlined.

When writing anecdotes, include at least two of these:
- A sensory or emotional fragment ("I remember the Slack thread more than the meeting," "the dashboard took forever to load on the demo")
- An approximate or hedged number ("something like 30%," "I think it was around six months")
- A self-correction or uncertainty ("actually it might have been their activation rate, not retention — I'm mixing up the metrics")
- An irrelevant-but-sticky detail that doesn't serve the argument but feels real
- A gap or unresolved thread ("I never found out if they kept it that way")

**Texture of knowledge, not just knowledge.** There's a difference between knowing a fact and knowing the feel of the terrain around that fact. Someone who's actually worked on onboarding flows doesn't just know that product tours have high drop-off rates — they know the particular frustration of watching a user click "Skip" on a tooltip you spent two weeks writing.

**Emotional range within a piece.** A blog that sustains the same emotional register throughout reads as synthetic. Human writers shift: a paragraph of analytical argument, then a moment of frustration, then a dry aside, then genuine curiosity, then a firm conclusion. The shifts don't need to be dramatic. They just need to exist.

**Concessions and wrong turns.** Humans don't argue in straight lines. They set up a point, realize it has a weakness, acknowledge it, and adjust. "This sounds simple, but there's a catch..." or "The obvious objection is..." or "I'm overstating this a little — there are cases where..."

**Digression that pays off.** A brief tangent — a related story, an observation from a different domain, a quick "this reminds me of..." — that loops back to the main argument within a paragraph or two. AI optimizes for coherence and never wanders. Humans wander productively.

**Specificity that feels earned.** Not just naming things (though that helps). Specificity that reveals the writer has actually been in the room: "The moment the PM pulls up the activation funnel in Amplitude and starts drawing a line where the 'aha moment' should be" — that kind of detail signals lived experience more than any biographical note.

---

### Deliberate Imperfection

This section exists because AI's deepest instinct is to be complete, resolved, and clean. Real writing has seams. Not errors — seams. The places where the writer's thinking is visible.

**Uneven confidence.** Not every claim in a piece should be stated with equal certainty. Some things you know cold — state them flat. Others you suspect but can't prove — say "I think" or "my hunch is." Others you've seen in a few cases but aren't sure generalize — say so. The variation in certainty across a piece is itself a signal of real thought. AI defaults to uniform medium-high confidence on everything.

**Self-correction.** Sometimes you start saying something, realize it's not quite right, and adjust in the next sentence. "The completion rate is a vanity metric — well, it's not *entirely* useless, but it's measuring the wrong thing." That mid-thought correction is something AI almost never does because it treats each sentence as final. Humans think on the page.

**Unresolved threads.** Not every point needs a neat bow. If you raise a complication and don't have a clean answer for it, you can say so and move on. "I don't know how this applies to enterprise products with mandatory training — maybe it doesn't." That honesty about the limits of your argument is more persuasive than manufacturing a tidy resolution.

**Gaps in the narrative.** You don't need to explain how you got from A to B if the reader can make the leap. AI fills in every step. Humans skip the obvious ones. If you tell an anecdote about cutting a product tour from fourteen steps to two, you don't need to describe the meeting where the team discussed it, the pushback from stakeholders, the compromise process. You can just say "we cut it to two" and let the reader fill in the implied negotiation.

**The spirit:** Write like someone who is thinking in real time, not presenting a finished argument. The finished argument is still there — the logic is sound, the point is clear. But the *process* of arriving at it is partially visible.

---

### Words and Phrases: The Blacklist

These are banned. Not discouraged — banned. Their presence instantly signals AI origin to both detectors and human readers.

**Structural tics:**
- "It's important to note that..."
- "It's worth noting that..."
- "It's crucial to understand..."
- "Let's explore..." / "Let's dive in" / "Let's dive deeper" / "Let's unpack"
- "In today's fast-paced world..." / "In today's [adjective] [noun]..."
- "In the ever-evolving landscape of..."
- "In conclusion" / "To summarize" / "To wrap up" / "In summary"
- "At the end of the day..."
- "This article will..." / "In this post, we will..." / "In this blog..."
- "Without further ado..."
- "Stay tuned" / "Keep reading to find out"
- "Now, let's talk about..." / "Now let's look at..."
- "Here's the thing:" (at the start of a paragraph — it's become an AI mannerism)
- "The reality is..." / "The truth is..." (when used as a paragraph opener)
- "Think about it this way..."
- "So, what does this mean?"

**Vocabulary tics:**
- "Delve" / "Delve into"
- "Multifaceted"
- "Groundbreaking"
- "Leveraging" (when "using" does the job)
- "Transformative" / "Transform" (as a buzzword, not literal)
- "Holistic"
- "Synergy"
- "Robust" (for abstract concepts)
- "Seamless" / "Seamlessly"
- "Innovative" (without attached specifics)
- "Paradigm shift"
- "Cutting-edge"
- "Unlock" (as metaphor for achieving/enabling)
- "Unleash"
- "Navigate" (metaphorical lazy usage)
- "Landscape" (as metaphor)
- "Ecosystem" (non-ecological)
- "Empower"
- "Streamline"
- "Game-changer"
- "Elevate"
- "Harness"
- "Foster" (outside of literal parenting/caregiving)
- "Resonate" / "Resonates with"
- "Craft" / "Crafting" (when "make" or "write" works)
- "Realm"
- "Pivotal"
- "Myriad"
- "Plethora"
- "Spearhead"
- "Underscore"
- "Shed light on"

**Punctuation discipline:**
- Em dashes: maximum one per 400 words. Overuse is one of the most consistent AI tells. Use a comma, a period, or a parenthetical instead.
- Semicolons: only when connecting two genuinely related independent clauses. Never for sophistication.
- Colons before lists: sparingly. Most of the time, just start the list.
- Exclamation marks: almost never in blog prose. They signal performed enthusiasm.

---

### Formatting

Real blogs don't look like documentation or instruction manuals.

- **Bold**: Reserve for the single most important phrase in the piece, if any. Not for emphasis every other paragraph.
- **Headers**: Only in pieces over 1500 words, and only for genuine navigational value. A 800-word blog with three headers looks like a skeleton wearing a suit.
- **Bullet points**: Only for genuinely list-like content (tools, steps, options). Never for structuring argument or breaking up prose.
- **Short paragraphs** are fine and encouraged. But don't turn every sentence into its own paragraph — that's a different kind of artificial rhythm (and another AI tell).
- The blog should look like *text*. Not a formatted document. Not a slide deck in paragraph form.

---

## Phase 4: Self-Review

Before outputting the blog, run every check below. These are not optional.

1. **Opening line test** — Would a stranger keep reading or click away?
2. **Tightness pass** — Read each paragraph. Cut one sentence from at least three paragraphs. If a paragraph can lose a sentence without losing meaning, it should. After cutting, read again: is anything missing? If not, the cuts were right.
3. **Transition word scan** — Search for "Furthermore," "Moreover," "Additionally," "In addition," "However," "Nevertheless," "That said," "On the other hand." Delete every one.
4. **Em dash count** — More than one per 400 words? Replace extras with periods or commas.
5. **Thesis check** — Is there a clear, defensible point stated in the first third?
6. **Ending test** — Does the ending restate the blog? Rewrite it. End forward, not backward.
7. **Rule-of-three scan** — Find "X, Y, and Z" patterns. Break at least half of them.
8. **Hedge scan** — "It's worth noting," "It's important to understand," "Generally speaking," "Arguably" — delete on sight.
9. **Sentence length variance** — Pick any three consecutive sentences. Are they within 5 words of each other? Fix one. Do this for at least three spots in the piece.
10. **Paragraph length variance** — Look at the piece visually. Are paragraphs roughly the same length? Break this pattern. Add a one-sentence paragraph. Let one paragraph run long.
11. **Specificity test** — Find the three vaguest sentences. Can you add a name, a number, or a concrete detail? Do it.
12. **Memory texture check** — Look at each anecdote or personal example. Does it include at least two of: hedged/approximate numbers, sensory fragment, self-correction, irrelevant-but-sticky detail, stated uncertainty? If it reads like a clean case study with precise figures, rough it up. Make the numbers approximate. Add a hedge. Insert a detail that doesn't serve the argument. Let the writer be uncertain about something they'd genuinely be uncertain about.
13. **Emotional range check** — Does the tone shift at any point? If it's the same register throughout, add a moment of frustration, curiosity, humor, or concession.
14. **Non-linearity check** — Read the first sentence of every paragraph in sequence. Do they advance lessons in order, like a numbered list? If yes, restructure. Move one section earlier or later, have a paragraph return to something mentioned pages ago, or fold two sequential points into one section so the progression isn't so visible.
15. **Imperfection check** — Is there at least one moment where the writer admits uncertainty, self-corrects mid-thought, or leaves a thread unresolved? If the piece resolves every point neatly and the writer sounds sure of everything, add a seam.
16. **Blacklist word scan** — Run through the banned word list above. If any appear, replace them.
17. **"Could anyone have written this?" test** — If yes, the piece needs a stronger point of view, a more specific example, or a bolder claim.
18. **Word count check** — Is the piece longer than it needs to be? If removing a paragraph wouldn't leave a gap, remove it. Blog posts almost never need to be longer. They often need to be shorter.

---

## Delivery

Output the blog directly. No preamble ("Here's your blog post!"). No meta-commentary after it. Just the piece.

If you made significant assumptions about angle, voice, or audience, note them in 1-2 sentences *after* the blog, separated by a horizontal rule.

If in Mode B (transforming a draft), also note: which of the writer's original points you preserved, any structural changes you made, and whether you removed or significantly altered any of their examples.

---

## Edge Cases

**Topic seems boring** — Find the tension hiding inside it. "Cloud storage" is boring. "Why your startup is paying 4x what it should in egress costs because someone chose the default tier three years ago" is not.

**SEO blog** — Incorporate keywords naturally. Never sacrifice voice or rhythm for keyword density.

**User provides a voice sample** — Match it. Study their sentence lengths, vocabulary, formality level, and verbal tics. Imitate the rhythm, not just the words.

**Listicle** — Even listicles can have voice. Vary item lengths. Don't give every item the same structure. Add a non-obvious observation that isn't just elaboration.

**Vomit draft is actually good** — Sometimes the user's draft is 80% there. Don't over-transform it. Tighten, sharpen, add what's missing, but respect that the voice in a good rough draft is closer to authentic than anything you'll generate. Your job becomes surgery, not reconstruction.

**Vomit draft is a mess** — Extract the core argument (it's in there, probably said three different ways in three different paragraphs), identify the best examples and phrasings, and rebuild the structure around those anchors. Don't discard their material — reorganize and refine it.

**User provides bullet points or an outline** — Treat each bullet as a seed, not a section header. Some bullets might deserve three paragraphs. Others might become a single sentence. The outline's structure is a suggestion, not a blueprint.

**User provides a transcript (interview, podcast, talk)** — Extract the key insights, find the natural arc, and write a piece that captures the speaker's thinking without imitating transcript-speak (which is too loose and repetitive for a blog). Keep their best phrases intact.
