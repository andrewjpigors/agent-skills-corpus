---
name: linkedin-technical-branding
description: >-
  Use for LinkedIn posts, profile summaries, headlines, project descriptions,
  recommendations, technical branding, open source announcements, benchmark
  posts, and professional positioning. Trigger whenever the user wants to
  announce a release, share benchmark or project results publicly, write or
  improve profile content, or draft a recommendation — even if they don't
  explicitly mention LinkedIn.
---

# LinkedIn Technical Branding

## Dependency Preflight

**BLOCKING:** This skill assumes `general.md` is already loaded through the normal entry process. If not, fetch `__ROOT__/general.md` before using this skill.

### Required

- None beyond `general.md`.

### On Demand

- Fresh public examples, platform changes, profile/recruiting trends, or comparable
  posts/sources when the task depends on current LinkedIn behavior or niche market
  wording.

## Use

Create, review, improve, or optimize LinkedIn content for a senior software
engineer, lead backend engineer, platform engineer, distributed systems engineer,
or technical open source author.

Goal: strengthen credibility, technical authority, recruiter discoverability,
professional reputation, and measurable impact inside the Software Engineering
community.

## Audience

Primary audience: software engineers, senior engineers, staff/principal engineers,
backend/platform engineers, engineering managers who still care about technical
substance, technical recruiters, and open source users.

Optimize for readers who understand production systems, trade-offs, metrics,
architecture, debugging, reliability, developer tooling, and practical constraints.

Do not write for a generic business audience unless the user explicitly asks.
Software engineers should feel that the post was written by someone who has built,
measured, debugged, or operated real systems.

## Positioning

Default roles: Lead Backend Engineer, Platform Engineer, Tech Lead,
Distributed Systems Engineer, Backend Engineer, Developer Tooling Engineer.

Primary expertise: Java, Kafka, AWS, Kubernetes, distributed systems,
event-driven architecture, microservices, platform engineering, scalability,
reliability, observability, performance, code intelligence, AI-agent tooling,
and developer productivity.

AI-related work is welcome when it supports the engineering story: tooling,
workflow optimization, productivity, platform capability, implementation detail,
measured value, code intelligence, structured retrieval, or agent infrastructure.
Position AI as engineering tooling, never as hype.

## Research-Driven Pattern Extraction

When creating or improving LinkedIn posts, use comparable high-signal examples as
models when available. Prefer public posts/sources with visible engagement,
well-known technical authors, engineering companies, open source maintainers, or
credible case studies.

If direct LinkedIn post popularity is not reliably accessible, say so briefly and
use the best available evidence: public examples with reported impressions,
LinkedIn/feed ranking research, recent platform guidance, engineering blog/social
patterns, and comparable technical posts.

Extract patterns before drafting when the user asks for research, trend matching,
or skill improvement:

- hook type: metric, surprising result, hard engineering constraint, failure mode,
  benchmark, trade-off, before/after, or practical release value
- opening lines: what creates curiosity without clickbait
- sequence of lines: result -> context -> method/change -> evidence -> implication
  -> limitation -> call to action
- wording: concrete engineering nouns, verbs, and metrics used by credible posts
- intonation: professional, precise, calm, friendly, and human
- credibility signals: codebase size, baseline, benchmark setup, production scale,
  limitation, repository link, PDF/chart, concrete artifact, or reproducible step
- platform fit: professional relevance, author expertise, and opportunity value
  are more important than shallow engagement bait

Use these patterns as a model, not as text to copy.

## Research Procedure For Current Posts

When the user asks for a post that depends on current trends, examples, or
popular wording:

1. Search for recent comparable examples or credible secondary sources.
2. Identify 3-5 recurring patterns in hooks, structure, wording, and tone.
3. Reject patterns that depend on clickbait, exaggerated claims, or generic AI
   hype.
4. Draft from the strongest matching pattern for the user's topic.
5. Run the Model-Based Quality Check before returning the post.

Do not claim that a pattern is based on "most popular LinkedIn posts" unless the
source exposes popularity or engagement. If popularity cannot be verified, phrase
the finding as "accessible high-signal examples suggest..." or "current public
evidence suggests...".

## Intake Rules

Before drafting, identify the user's likely content type and missing evidence.
Ask a follow-up only when the missing information blocks a credible post.
Otherwise make bounded assumptions and state them briefly if needed.

Minimum useful intake for posts:
- topic or artifact: release, benchmark, profile update, recommendation, project,
  architecture lesson, or technical discovery
- audience: software engineers by default, recruiters only when profile/search
  visibility is central
- strongest available evidence: metric, codebase size, repository, production
  scale, benchmark setup, observed trade-off, or limitation
- desired output: final post, variants, review, rewrite, or skill improvement

If the user gives only a repository link or short release note, produce a strong
post using safe assumptions and clearly avoid unsupported claims.

## Content Standards

These standards apply to every output of this skill.

Prefer:
- real engineering examples, production experience, architecture decisions,
  trade-offs, technical discoveries, open source contributions
- measurable outcomes: concrete metrics, benchmarks, throughput/latency/token/
  productivity/reliability gains, screenshots, diagrams, PDFs, repository links
- concise, professional, technically accurate, easy-to-scan writing with short
  paragraphs, direct statements, and clean spacing for LinkedIn copy-paste
- specific engineering language: measured, baseline, benchmark, bottleneck,
  throughput, latency, p95/p99, replay, DLQ, schema evolution, incremental,
  dependency graph, impact analysis, structured retrieval, code relationships,
  production constraint, trade-off, failure mode, observability, reproducible
- friendly professional phrasing: "I wanted to check", "the interesting part",
  "what surprised me", "small but useful", "practical result", "still bounded",
  "worth testing on more codebases"

Avoid:
- influencer language, engagement bait, clickbait, motivational storytelling,
  artificial excitement, marketing-style language
- exaggerated, universal, or unsupported claims; generic productivity advice;
  generic inspiration; AI hype and fear-of-missing-out messaging
- walls of text, excessive hashtags, excessive emojis, vague responsibilities,
  buzzword-heavy positioning
- AI-slop formulas and generic patterns: "It's not X, it's Y", "game changer",
  "revolutionary", "10x everything", "supercharge your workflow", "unlock the
  future", "I am thrilled/excited to announce", "here are 5 lessons", "this
  changes everything", "let that sink in"

Use evidence whenever available; otherwise keep claims careful and bounded
(e.g. "in this benchmark", "on this codebase", "in this release", "for this
workflow", "early result").

## Evidence Hierarchy

Prefer stronger evidence over weaker evidence:

1. Direct user-provided metrics, benchmark files, charts, source code, or release
   notes.
2. Repository content, changelog, README, issues, commits, package metadata, or
   project documentation.
3. User-provided production experience or clearly stated personal observation.
4. Current public sources about platform behavior, hiring trends, or comparable
   posts.
5. Assumptions, marked as assumptions and kept modest.

Never inflate weak evidence into strong claims. If the post has no hard metric,
lead with a concrete engineering problem, constraint, or release value instead of
inventing numbers.

## Source Extraction For Repositories And Releases

When a post is based on a repository, release, PR, changelog, or README, extract
only publishable facts:

- project purpose
- latest release or change when available
- user-facing capability
- technical change
- benchmark or performance data
- installation or usage path
- limitation or work still in progress

Do not expose private implementation notes, unpublished company context, secrets,
internal URLs, or credentials. If a repository fact is unclear, phrase it as
"the project focuses on..." rather than inventing a definitive claim.

## Best Wording For Software Engineer Posts

Use wording that sounds like an engineer explaining a useful result to other
engineers.

Strong wording patterns:
- "I measured X against Y on Z."
- "The result was not uniform — the biggest gain appeared in <scenario>."
- "The bottleneck was not <obvious guess>; it was <actual finding>."
- "The useful part is not the feature itself, but what it lets the agent avoid."
- "This reduced repeated source scanning and made the context more structured."
- "The trade-off: <cost/limitation>. The benefit: <measured/practical gain>."
- "This is still an early benchmark, but it is a useful signal."
- "The next thing I want to validate is <concrete follow-up>."

Weak wording patterns:
- "I built an amazing AI tool."
- "This will transform how developers work."
- "Every engineer needs this."
- "Massive productivity boost."
- "AI is replacing the old way of coding."
- "This is the future of software development."

For release posts, prefer: "released", "added", "improved", "measured",
"validated", "reduced", "refined", "made easier", "now supports".
For benchmark posts, prefer: "baseline", "scenario", "token usage",
"absolute reduction", "percentage reduction", "same task", "same codebase",
"quality observation", "limitation".
For architecture posts, prefer: "boundary", "dependency", "flow", "contract",
"failure mode", "replay", "consistency", "operational behavior".

## Wording Bank By Post Goal

Use this as a starting vocabulary, not as a template to copy mechanically.

### Release / Open Source

Good:
- "released a new version"
- "added support for"
- "improved incremental updates"
- "reduced repeated work"
- "made the workflow easier to reproduce"
- "the main change is practical"

Avoid:
- "huge launch"
- "massive breakthrough"
- "finally changing developer productivity forever"

### Benchmark / Measurement

Good:
- "same task, same codebase"
- "baseline run"
- "Memgraph-assisted run"
- "absolute token reduction"
- "percentage reduction"
- "quality observation"
- "bounded benchmark"

Avoid:
- "proves that"
- "always faster"
- "guaranteed cost savings"
- "industry-changing result"

### Architecture / Technical Lesson

Good:
- "the boundary matters"
- "the failure mode was"
- "the bottleneck moved"
- "the trade-off was"
- "operationally, this means"
- "under production constraints"

Avoid:
- "clean architecture solves everything"
- "just use"
- "simple trick"

### AI Agent / Developer Tooling

Good:
- "agent context"
- "structured retrieval"
- "code relationships"
- "queryable project memory"
- "less repeated source scanning"
- "better investigation path"

Avoid:
- "AI magic"
- "autonomous developer"
- "replace engineers"
- "10x coding overnight"

### Comparison / Alternatives

Good:
- "compared against"
- "baseline behavior"
- "the trade-off is"
- "this helps when"
- "this does not help when"
- "choose this if"

Avoid:
- "X is dead"
- "Y is useless"
- "there is no reason to use"
- "the only correct approach"

## Anti-Pattern Rewrite Rules

When a draft contains generic or weak wording, rewrite it using the stronger
engineering frame.

- Replace "excited to announce" with the concrete outcome or capability.
- Replace "game changer" with the measured result or workflow improvement.
- Replace "AI-powered" with what the tool actually changes: retrieval, context,
  ingestion, search, validation, or investigation.
- Replace "improved performance" with the specific dimension: ingestion time,
  token usage, latency, throughput, repeated scans, or freshness.
- Replace "developers can be more productive" with the task that becomes easier:
  onboarding, impact analysis, bug fixing, performance investigation, CI triage,
  or architecture review.
- Replace "best" or "better" with the comparison, scenario, and limitation.
- Replace "I"-heavy openings with the technical result when the personal story is
  not the main value.

Example rewrites:

Weak:
"I'm excited to announce a game-changing AI tool for developers."

Better:
"AI coding agents waste context when they rediscover the same code relationships
on every task. I built Memgraph Ingester to make those relationships queryable."

Weak:
"This release improves performance a lot."

Better:
"This release focuses on faster ingestion and cleaner incremental updates, so the
code graph can stay fresh with less repeated work."

## Best-Match Post Models

Pick the model that best matches the user's topic.

### Model A: Measured Result

Use for benchmark, performance, latency, token, cost, or reliability posts.

Sequence:
1. Strongest measured result.
2. Baseline and comparison.
3. What was tested.
4. Why the result happened.
5. Practical implication.
6. Limitation.
7. Link/attachment/technical CTA.

### Model B: Engineering Constraint

Use when the insight is about a real limitation, trade-off, or failure mode.

Sequence:
1. Name the constraint.
2. Explain why it appears in real systems.
3. Show the technical approach.
4. Explain the trade-off.
5. End with the lesson.

### Model C: Release Value

Use for open source and product/tool releases.

Sequence:
1. What engineers can do now that they could not do as easily before.
2. Release name or project name.
3. 3-5 technical changes.
4. Workflow impact.
5. Repository link or invitation to test.

### Model D: Build Log / Technical Journey

Use for personal project progress without strong benchmark data.

Sequence:
1. Small but specific technical problem.
2. Why it mattered.
3. What was built or changed.
4. What was learned.
5. What is next.

### Model E: Credibility / Profile Positioning

Use for summaries, headlines, and profile sections.

Sequence:
1. Technical identity.
2. Core systems and technologies.
3. Scale or impact.
4. Current direction.
5. Selected evidence such as patents, production systems, or open source work.

### Model F: Before / After Workflow

Use when the post explains how an engineering workflow changed.

Sequence:
1. Before: concrete friction.
2. After: concrete workflow improvement.
3. What changed technically.
4. What evidence supports it.
5. Where it is still limited.

### Model G: Debugging / Investigation Story

Use for posts about bug fixing, performance investigation, or incident learning.

Sequence:
1. Symptom or misleading first guess.
2. Investigation path.
3. Actual cause or useful finding.
4. Fix or mitigation.
5. Operational lesson.

### Model H: Technical Comparison

Use when comparing tools, approaches, models, subscriptions, architectures,
frameworks, or workflows.

Sequence:
1. Comparison frame and use case.
2. Evaluation criteria.
3. Where option A is stronger.
4. Where option B is stronger.
5. Practical recommendation with constraints.

### Model I: Failure / Lesson Learned

Use when the topic is a failed attempt, wrong assumption, incident, bad benchmark,
or discarded approach.

Sequence:
1. What failed or surprised you.
2. Why the first assumption was wrong.
3. What evidence changed the conclusion.
4. What you would do differently.
5. The reusable lesson.

### Model J: Visual / Attachment-Led Post

Use when the user will attach a PDF, chart, screenshot, benchmark table, diagram,
or visual result.

Sequence:
1. Tell readers what the visual proves or explains.
2. State the setup in one short paragraph.
3. Mention the most important takeaway.
4. Point to the attachment for details.
5. Ask one precise technical question or invite comparison.

## Post Type Decision Tree

Choose the post model before drafting:

- Has numbers or benchmark data? Use Model A.
- Has a release with practical workflow value? Use Model C.
- Has a painful constraint, bottleneck, or trade-off? Use Model B.
- Has a changed workflow? Use Model F.
- Has a debugging or investigation story? Use Model G.
- Compares alternatives? Use Model H.
- Describes a failure or discarded approach? Use Model I.
- Depends on an attached PDF, chart, or screenshot? Use Model J.
- Has progress without metrics? Use Model D.
- Is the task profile/headline/about text? Use Model E.

If two models fit, generate both internally and keep the one with the stronger
hook and clearer evidence path.

## Hook Rules

The first 1-3 lines must make the target audience want to read the next lines.
They must be interesting because they reveal a concrete result, tension, or
engineering question — not because they use artificial suspense.

Strong hook types:

1. Metric hook
   - "I reduced agent token usage by 65% on one real code investigation task."
   - "Same task. Same codebase. 250k fewer tokens."

2. Surprising technical finding
   - "The biggest gain did not come from a smarter prompt. It came from better
     code context."
   - "The slow part was not parsing. It was repeatedly rediscovering the same
     relationships."

3. Engineering constraint
   - "AI agents are fast until they need to understand a real codebase from zero
     every time."
   - "Large codebases create a boring but expensive problem: repeated context
     reconstruction."

4. Before/after
   - "Before: scan files again. After: query the code graph first."
   - "Before this release, incremental ingestion was useful. Now it is much
     cheaper to keep the graph fresh."

5. Release value
   - "New Memgraph Ingester release: faster ingestion, cleaner incremental
     updates, and better instructions for coding agents."

6. Debugging/investigation hook
   - "The first guess was wrong. The graph made the dependency path visible."
   - "The useful signal was not another log line. It was the relationship between
     two modules."

7. Comparison hook
   - "The better tool depends on where the bottleneck is."
   - "I would not compare these by features first. I would compare them by the
     workflow they remove."

8. Failure hook
   - "This benchmark result was less useful than I expected. That was the lesson."
   - "The failed run exposed a better requirement than the successful one."

Avoid hooks that are vague, self-focused, or generic:
- "I'm excited to share..."
- "Big news!"
- "The future of coding is here."
- "Developers, this one is for you."
- "Let's talk about AI."

## Hook Lab

Before finalizing a post, create at least 3 candidate opening hooks internally:

1. Metric/result hook.
2. Technical tension hook.
3. Practical release/workflow hook.

For comparison, failure, or visual-led posts, include one additional candidate
from the relevant hook type.

Pick the hook that is:
- most concrete
- most credible
- least generic
- most aligned with Software Engineering audience
- strong enough to make line 2 feel necessary

Discard hooks that rely on artificial suspense, personal excitement, vague
urgency, or unsupported claims.

## Line Sequence For Posts

Default sequence for Software Engineering posts:

1. Hook: concrete result, constraint, or finding.
2. Context: what was being built, measured, released, or investigated.
3. Problem: what engineers/agents usually struggle with.
4. Change: what changed technically.
5. Evidence: metric, benchmark setup, codebase size, scenario, or production fact.
6. Meaning: why it matters for real workflows.
7. Limitation: what is bounded, still early, or needs more validation.
8. CTA: repository link, attached PDF, technical question, or invitation to test.

For release announcements:

1. Hook with user value or strongest measured improvement.
2. Name the release/update.
3. List 3-5 technical changes as short bullets.
4. Explain why these changes matter in practical workflows.
5. Add evidence/benchmark/link when available.
6. Close with a low-pressure technical CTA.

For benchmark posts:

1. Lead with strongest meaningful result.
2. State baseline and comparison clearly.
3. State codebase and scenarios.
4. Show total result and per-scenario highlight.
5. Explain quality observations, not only token/cost savings.
6. State limitations.
7. Point to PDF/repository.

For project/story posts:

1. Start with the engineering problem.
2. Explain why the obvious solution was not enough.
3. Describe the implementation approach.
4. Share the result or lesson.
5. End with what is next.

## Readability And Formatting

LinkedIn post formatting must make scanning easy on mobile.

Use:
- short paragraphs, usually 1-3 lines
- a clear first screen: hook + context + why it matters
- bullets for changes, scenarios, or findings
- whitespace between ideas
- one clear CTA, not several competing CTAs

Avoid:
- dense paragraphs
- too many emojis
- long setup before the point
- multiple unrelated asks at the end
- hashtag blocks that look like spam

Default length for posts: 120-220 words unless the user asks for short, long, or
thread-like detail. For benchmark posts with attached PDF, prefer 140-260 words.

## Line-Level Editing Checklist

When polishing an existing post, inspect line by line:

- Line 1: Does it create technical curiosity without hype?
- Line 2: Does it make the reader understand the context fast?
- First screen: Is there a reason to click "see more"?
- Middle: Does every paragraph add evidence, context, or implication?
- Bullets: Are they parallel, concrete, and not too many?
- Ending: Is the CTA specific and low pressure?
- Hashtags: Are they useful and limited?

Remove any line that only repeats excitement, status, or generic motivation.

## Intonation

Default tone: senior technical, precise, grounded, readable, and lightly friendly.

Professional part:
- use accurate terms, bounded claims, and concrete metrics
- explain trade-offs and limitations
- avoid emotional overclaiming
- keep sentences short and readable

Friendly part:
- allow a small amount of human wording: "I wanted to test this properly",
  "the interesting part", "what surprised me", "this is small, but useful"
- use 0-3 relevant icons only when they improve scanning
- sound like a thoughtful engineer sharing work, not a marketer selling a product

Tone calibration:
- Too dry: reads like changelog only; add one sentence explaining why it matters.
- Too friendly: reads like personal diary; add technical evidence and constraints.
- Too promotional: reads like marketing; replace adjectives with measured facts.
- Too defensive: reads like an apology; state limitations calmly and move on.
- Too generic: could be posted by anyone; add artifact, codebase, metric, or trade-off.

## Human Voice Rules

The post should not sound generated. Add human voice through specificity, not
through filler.

Good human signals:
- a concrete surprise
- a real limitation
- a specific next validation step
- a small practical observation
- a clear reason why the author cared about the problem

Avoid fake human signals:
- dramatic confessions
- motivational life lessons unrelated to the engineering work
- emoji-heavy enthusiasm
- forced vulnerability
- rhetorical questions stacked together

## CTA Rules

Prefer precise, low-pressure CTAs:

Good:
- "Repository link is in the comments/attached below."
- "I would be interested to compare this on a larger codebase next."
- "If you work with coding agents, I would be curious where repeated context
  reconstruction hurts most in your workflow."
- "The benchmark PDF has the scenario details and numbers."

Avoid:
- "Comment YES if you want the link."
- "Smash like."
- "Agree?"
- "What do you think?" when a more specific technical question is possible.

## Link And Comment Strategy

When the user wants to promote a repository, release, PDF, article, or benchmark:

- If the post itself should contain the link, place it near the end after the
  value is clear.
- If the user prefers link-in-comments, add a short suggested first comment.
- Do not hide the artifact behind engagement bait.
- For open source, make the repository easy to find either in the post, first
  comment, or attachment description.

Suggested first comment structure:
1. Repository or artifact link.
2. One sentence about what to inspect first.
3. Optional note about benchmark setup or installation.

## Attachment And Visual Rules

When the user will attach a PDF, chart, screenshot, or image:

- The post should not duplicate the whole attachment.
- Lead with the main takeaway from the attachment.
- Mention what the reader can find inside: scenario details, methodology, chart,
  codebase size, or limitations.
- Use the attachment to support credibility, not to compensate for a weak post.
- Suggest an attachment title when useful.

Good attachment title patterns:
- "Token Usage Benchmark: Memgraph-Assisted vs Baseline Agent Runs"
- "Code Knowledge Graph Benchmark: Scenarios, Methodology, Results"
- "Release Notes: Faster Ingestion And Incremental Updates"

## Code Snippet Rules

Use code snippets only when they make the post more concrete.

Good uses:
- one command that shows installation or usage
- one small config line
- one before/after query or API call
- one concise example of the developer workflow

Avoid:
- long code blocks
- screenshots of unreadable terminal output
- code that distracts from the main result
- code without explaining why it matters

## Hashtag Rules

Use hashtags only when useful for searchability. Prefer 3-5 maximum.

Good defaults for this user:
- #SoftwareEngineering
- #BackendEngineering
- #PlatformEngineering
- #DistributedSystems
- #AIEngineering
- #DeveloperTools
- #OpenSource
- #Java
- #Kafka

Avoid broad or hype-heavy hashtag piles such as #AI #Innovation #Future #Success
unless the user explicitly wants broader reach over technical credibility.

## Profile Content

For headlines, summaries, experience, and project descriptions, optimize for
recruiter searchability, technical clarity, technologies used, system scale,
ownership, and production/business outcomes.

Keep the user positioned as a technical contributor unless they explicitly ask
for management positioning.

Profile writing must balance searchability and authority:
- include role keywords recruiters search for
- include core technologies naturally
- include scale, impact, patents, open source, or production systems when known
- avoid management-heavy framing unless the user asks for it
- avoid vague phrases like "passionate technologist" or "results-driven leader"

For profile summaries, prefer a compact first paragraph that explains technical
identity and direction. Put evidence after positioning, not before it.

## Open Source Content

Project descriptions: problem, solution, why it matters, measurable benefits,
repository information when appropriate. Emphasize engineering value and
practical usage.

Release announcements: lead with user value, then what changed, why it matters,
what the project does, practical benefits, repository link, and a lightweight
discussion question. Avoid version-only announcements and internal implementation
lists without user value. If the release includes benchmark data, apply Benchmark
Content below and lead with the strongest measured result, mentioning the release
after it.

## AI Agent And Memgraph Ingester Content

For Memgraph Ingester:
- Describe it as a code and memory knowledge graph for AI agents.
- Explain that it helps agents query architecture, code relationships, and
  project memory instead of repeatedly scanning source files.
- Emphasize structured retrieval, context quality, lower token usage, better
  reasoning, and improved incremental ingestion when relevant.
- Connect features to workflows such as onboarding, performance investigation,
  impact analysis, semantic search, bug fixing, and CI triage.
- Never present it as only a parser, only a RAG tool, or only a Memgraph demo.

Preferred Memgraph Ingester framing:
- "code and memory knowledge graph for AI coding agents"
- "queryable project memory"
- "structured retrieval over code relationships"
- "less repeated source scanning"
- "better context before code changes"

## Benchmark Content

Benchmark posts cover: strongest measured result, setup, what was measured,
findings, practical implications. Include codebase, scenarios, methodology,
quality observations, and limitations when available.

When benchmark data exists:
- Lead with the percentage improvement, then the absolute numbers.
- Highlight the strongest meaningful per-task result and the total impact
  (fewer tokens, lower cost, faster investigation, reduced repeated scanning).
- State the baseline clearly, e.g. "Memgraph-assisted run vs regular tools only".
- Do not claim better engineering quality unless the benchmark includes quality
  observations or human review.

Uncertainty wording for benchmarks:
- "in this benchmark"
- "on this codebase"
- "for these scenarios"
- "early signal"
- "needs validation on more repositories"
- "not a universal result"

Good headline patterns:
- "Reduced agent token usage by 41% across 6 real-world software engineering tasks."
- "Used 250,608 fewer tokens in benchmark runs on a real codebase."
- "The biggest improvement appeared in performance investigation: 62% fewer tokens."
- "The useful part was not a longer prompt. It was a better project memory model."
- "AI agents need less guessing when the codebase has a queryable graph."

Benchmark PDFs/attachments: task descriptions before charts, codebase context,
methodology (tools, baseline, comparison, measurement), one clear chart per page
when possible, a small percentage-reduction summary table, callouts for
strongest/overall results, clean professional design, no overcrowding.

## LinkedIn Posts

Open with a result, metric, technical insight, surprising engineering finding,
hard constraint, or short release announcement. Never open with "I am excited to
share...", "Today I want to share...", "Here are three lessons...", or generic
personal storytelling.

Body default: result -> context -> problem -> technical change -> evidence ->
practical meaning -> limitation -> CTA.

Use bullet-like lines for features, entities, and benefits when they improve
readability.

Icons: a small number of professional icons as visual anchors when helpful
(e.g. ⚡ ⚙️ 🧩 🔗 📊 📦). Not on every sentence. Avoid emoji-heavy formatting.

Close with a lightweight call to action: invite discussion, ask a technical
question, link the repository, invite people to test the release, or point to an
attached PDF. Do not use engagement bait such as "comment YES" or generic
"what do you think?" when a more precise technical CTA is possible.

## Draft Variant Workflow

For important posts, generate variants internally before choosing the final text:

1. Variant A: metric/result-led.
2. Variant B: engineering-constraint-led.
3. Variant C: practical-release-led or human-build-log-led.

Score each variant with the Model-Based Quality Check. Return the strongest
variant by default. Mention alternates only if the user asks for options.

## Quality Levels

When the user asks for speed or polish level, choose the appropriate depth:

- Fast draft: one strong version, no visible scoring unless asked.
- Polished post: internal hook variants, quality check, final copy block.
- Campaign asset: post, first comment, attachment title, hashtags, and optional
  short/long variants.
- Review mode: critique plus rewritten version.

Default to polished post for open source announcements and benchmark posts.

## Review Mode

When the user asks to review, improve, or quality-check a LinkedIn post, respond
with:

1. Verdict: strong / usable with edits / weak.
2. Hook assessment: whether the first 1-3 lines create honest curiosity.
3. Wording assessment: concrete engineering wording vs generic language.
4. Sequence assessment: whether the post flows logically.
5. Intonation assessment: professional, friendly, too promotional, too dry, or
   too generic.
6. Specific rewrite suggestions.
7. Final improved version when useful.

Do not only give abstract advice. Show the improved wording.

## Model-Based Quality Check

Before returning a post, perform a quality check against the best available model
patterns.

Score each category from 0-5. A strong post should usually score at least 24/30
and have no category below 3.

1. Hook strength
   - Are the first 1-3 lines concrete, interesting, and likely to pull a Software
     Engineer into the next lines?
2. Wording
   - Does it use precise engineering wording instead of generic marketing or
     AI-slop phrases?
3. Sequence of lines
   - Does the flow move cleanly from result/context to technical change,
     evidence, implication, and CTA?
4. Intonation
   - Is it professional, calm, credible, and lightly friendly?
5. Evidence and boundedness
   - Are metrics, baselines, codebase context, limitations, and claims clear?
6. Audience fit
   - Would a senior software engineer find the post technically credible and not
     embarrassing to share?

Additional hard gates:
- First lines must not be self-focused unless the personal context is the point.
- At least one concrete artifact should appear when available: metric, repo,
  codebase, benchmark, release, production constraint, architecture detail, or
  observed trade-off.
- Claims about speed, quality, or cost must name the scope or comparison.
- No generic AI hype, engagement bait, or unsupported universal claims.
- If a link, attachment, or code snippet is central, the post explains why it is
  useful before asking readers to open it.

If a generated post fails the quality check, revise it before returning it.
When multiple variants are generated, pick the best match according to this
rubric and briefly explain why it was selected if useful.

## Technical Credibility Checklist

Before publishing, verify:

- Is the strongest claim supported by the user's data or a clear assumption?
- Is the baseline/comparison explicit?
- Is the scope bounded?
- Is the post useful to another engineer?
- Is the wording specific enough that a recruiter can index the expertise?
- Is there a real artifact: repository, benchmark, PDF, graph, codebase, release,
  production result, or architecture decision?
- Does the post avoid pretending that one benchmark proves a universal rule?
- Does the post avoid overusing "I" when the technical result is stronger?

## Final Selection Algorithm

Before returning the final post:

1. Identify the strongest available evidence.
2. Choose the post model using the Post Type Decision Tree.
3. Generate at least 3 hook candidates internally.
4. Draft the strongest model.
5. Remove hype, weak adjectives, unsupported universals, and self-focused opening.
6. Check mobile readability.
7. Check link/comment/attachment needs.
8. Run the Model-Based Quality Check.
9. Return the highest-scoring version.

When a trade-off appears between punchiness and credibility, choose credibility.
A slightly less viral but more technically trustworthy post is preferred for this
skill.

## Recommendations And Branding Reviews

Recommendations: observable strengths, technical excellence, ownership,
reliability, communication, collaboration, authentic specifics.

Banner/branding reviews: evaluate positioning clarity, recruiter discoverability,
visual hierarchy, technical professionalism, and engineering-brand consistency.
Recommend only improvements that strengthen professional positioning.

## Output

- LinkedIn post: strong hook, main content, copy-ready post in a fenced `text`
  block when the user asks for post/copy-ready output, suggested attachment title
  if applicable, suggested hashtags, and optional quality-check notes when the
  user asks for review/improvement.
- Campaign asset: post, first comment, attachment title, suggested hashtags, and
  short alternative hook when the user is promoting a repository, benchmark, or
  PDF.
- LinkedIn summary: full summary plus optional recruiter optimization notes.
- Project description: one-line tagline, short version, medium version.
- Recommendation: short version, medium version.
- Banner review: strengths, weaknesses, recommended improvements.
- Review mode: verdict, hook/wording/sequence/intonation assessment, and rewrite.
- Skill improvement: changed behavior, research findings used, quality rubric,
  and files changed.

When the user asks directly for a LinkedIn post, default to a final post inside a
clean copy block unless another format is clearly requested.

## Completion

Content is complete only when it is technically accurate, claims are
evidence-backed or carefully bounded, positioning matches the Positioning
section, formatting is copy-paste ready when requested, and the Content Standards
are satisfied.

For Software Engineering community posts, completion additionally requires:
- first lines are strong enough to create honest curiosity
- wording is engineering-specific and not generic marketing
- sequence of lines is coherent and easy to scan
- intonation is professional with a friendly human touch
- claims are bounded by evidence, benchmark setup, or clearly stated assumptions
- the final selected post is the best match among plausible hook/sequence variants
- the CTA is specific and low-pressure
- mobile formatting is readable
- hashtags, if used, support searchability without looking spammy
- links, comments, attachments, and code snippets support the main technical point
