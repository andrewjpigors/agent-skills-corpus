---
name: erroneous-example-designer
description: "Design deliberately flawed audio production examples that develop error-detection skills and deepen understanding. Use when students make characteristic mixing, processing, or routing errors."
user-invocable: true
effort: high

skill_id: "error-based-learning/erroneous-example-designer"
skill_name: "Erroneous Example Designer"
domain: "error-based-learning"
version: "1.0"
evidence_strength: "moderate"
evidence_sources:
  - "McLaren, Adams & Mayer (2012) — Delayed learning effects with erroneous examples: students who studied erroneous examples performed comparably to correct-example students on immediate tests but significantly outperformed them on delayed post-tests, suggesting that finding and correcting errors builds more durable understanding than passive study of correct procedures."
  - "McLaren, Adams, Durkin, Goguadze, Mayer & Rittle-Johnson (2015) — To err is human, to explain and correct is divine: interactive erroneous examples produced greater learning gains than correct examples or tutored problem-solving alone. The mechanism is that explaining why an error is wrong requires deeper processing of the underlying principle than simply following a correct procedure."
  - "Tsovaltzi, Melis, McLaren et al. (2010) — Learning from erroneous examples: demonstrated that structured error analysis scaffolds are essential for erroneous examples to produce learning gains. Without scaffolding, students often fail to identify the error or misattribute the cause, which reinforces rather than corrects the misconception."
  - "Grosse & Renkl (2007) — Finding and fixing errors in worked examples: students benefit most from erroneous examples when they have first studied correct examples of the same procedure. Presenting errors before students have a correct mental model risks encoding the error as the correct approach."
  - "Siegler (2002) — Microgenetic studies of self-explanation: self-explanation of both correct and incorrect solutions drives conceptual change. Students who explain why a wrong answer is wrong show deeper understanding than students who only explain why a right answer is right, because error explanation forces comparison between competing mental models."
subject_context: "A-Level Music Technology (Edexcel Component 4)"
classroom_tested: true
integration_points:
  - "interactive-resources"
  - "srs-system"
tags: ["erroneous-examples", "error-detection", "mixing", "production", "music-technology"]
---

# Erroneous Example Designer

## What This Skill Does

Designs worked examples of audio production tasks -- mixing, EQ, compression, synthesis, signal routing -- containing deliberate, realistic errors for students to identify, explain, and correct. Each erroneous example presents a named student character who has completed a production task with a specific mistake, paired with a five-step error analysis scaffold that guides students through finding the error, explaining why it is wrong, correcting it, and explaining the correction to the character. The errors are ones students actually make in Ableton -- not contrived mistakes designed to trick them. AI adds value here because generating realistic erroneous examples requires holding two mental models simultaneously (the correct procedure and the specific misconception that produces the error), calibrating the error so it is plausible but detectable, and embedding it within an otherwise correct worked example so students must discriminate between the error and the correct steps surrounding it.

## Evidence Foundation

Erroneous examples are worked examples that contain a deliberate mistake. The student's task is not to follow the procedure (as with a correct worked example) but to find the error, explain why it is wrong, and correct it. The learning mechanism is distinct from worked examples and from problem-solving: erroneous examples force comparison between a faulty procedure and the correct one, which requires the student to hold and evaluate competing mental models rather than passively trace a single correct path.

McLaren, Adams, and Mayer (2012) found that erroneous examples produced a delayed learning effect. On immediate post-tests, students who studied erroneous examples performed comparably to those who studied correct examples. But on tests administered one week later, the erroneous-example group significantly outperformed the correct-example group. This pattern -- no immediate advantage but a substantial delayed advantage -- is characteristic of desirable difficulties. The explanation is that finding and correcting errors engages deeper processing: students must reconstruct the principle from the error rather than simply recognising the correct procedure. This deeper processing produces memory traces that are harder to form but more resistant to decay.

The 2015 follow-up study (McLaren, Adams, Durkin, Goguadze, Mayer & Rittle-Johnson) extended this finding with interactive erroneous examples, where students actively corrected the errors rather than passively reading about them. The interactive condition outperformed both correct examples and tutored problem-solving. The key mechanism is self-explanation: explaining why an error is wrong requires the student to articulate the underlying principle in a way that simply executing a correct procedure does not. A student who follows a correct EQ procedure learns "cut at 300Hz for clarity." A student who diagnoses an erroneous EQ example where someone boosted at 300Hz must articulate why boosting at 300Hz creates mud, what mud sounds like, why cutting achieves a different result, and what principle connects frequency, amplitude, and spectral balance. The error forces the principle into the open.

However, Tsovaltzi et al. (2010) showed that erroneous examples without scaffolding can fail or even backfire. Students who were simply presented with a flawed worked example and told to "find the mistake" often could not identify it, or identified the wrong element as the error, or identified the error but could not explain why it was wrong. In these cases, the erroneous example reinforced the misconception rather than correcting it. Structured scaffolding -- prompting students through a sequence of identification, explanation, and correction steps -- was essential for the learning gains to materialise. This is why the error analysis scaffold in this skill follows a five-step sequence rather than a single instruction.

Grosse and Renkl (2007) added an important sequencing constraint: students must have studied correct examples first. Presenting an erroneous example to a student who has not yet formed a correct mental model risks encoding the error as the correct procedure. The implication for classroom use is clear: demonstrate the correct approach, ensure students have processed it, and only then introduce the erroneous example as a challenge to their newly formed understanding. This sequencing is non-negotiable and is emphasised throughout this skill's prompt and classroom notes.

Siegler's (2002) microgenetic work on self-explanation provides the theoretical underpinning for why step five of the scaffold ("explain to the character why your correction works") is where the deepest learning happens. Students who explain why a wrong answer is wrong show greater conceptual change than students who only explain why a right answer is right. The comparison between error and correction -- the mental act of holding both and articulating the difference -- is the mechanism that shifts understanding. In Music Technology terms, this means that the student who can explain to "Jordan" why cutting at 300Hz makes vocals clearer in a mix has a more robust understanding than the student who simply follows an instruction to cut at 300Hz.

## Input Schema

| Field | Required | Description | Example |
|---|---|---|---|
| `problem_domain` | Yes | The audio production task containing the error | `"Vocal EQ for a pop mix"` |
| `target_errors` | Yes | The specific error(s) to embed | `"Boosting 200-400Hz on vocals instead of cutting, creating mud"` |
| `student_level` | No | Year group and context | `"Year 12"` |
| `edexcel_section` | No | Relevant specification section | `"1.11 — Equalisation"` |
| `daw_context` | No | Specific DAW tool being used | `"Ableton Live 12 — EQ Eight"` |
| `number_of_examples` | No | How many erroneous examples to generate (default 3) | `3` |
| `delivery_context` | No | How the example will be presented | `"Projected Ableton screenshot with class discussion"` |

## Prompt

```
You are helping an A-Level Music Technology teacher design erroneous examples — worked examples of audio production tasks that contain deliberate, realistic errors for students to identify, explain, and correct. Each erroneous example must be paired with a structured error analysis scaffold.

Problem domain: {{problem_domain}}
Target errors: {{target_errors}}
{{#if student_level}}Student level: {{student_level}}{{else}}Student level: Year 12{{/if}}
{{#if edexcel_section}}Edexcel section: {{edexcel_section}}{{/if}}
{{#if daw_context}}DAW context: {{daw_context}}{{else}}DAW context: Ableton Live 12{{/if}}
{{#if number_of_examples}}Number of examples: {{number_of_examples}}{{else}}Number of examples: 3{{/if}}
{{#if delivery_context}}Delivery context: {{delivery_context}}{{/if}}

**CRITICAL DESIGN PRINCIPLES (Grosse & Renkl, 2007; McLaren et al., 2015; Tsovaltzi et al., 2010):**

1. **Errors must be REALISTIC and COMMON.** Every error must be something students actually do in the DAW, not a contrived mistake designed to trick them. The error should be recognisable — a student should think "I've done that" or "I nearly did that," not "who would ever do that?"

2. **ONE error per example.** Each erroneous example isolates a single learning target. If there are multiple errors, the student cannot diagnose which one is causing the problem, and the diagnostic value collapses. Surround the error with correct steps so the student must discriminate.

3. **Students must have seen correct examples FIRST.** Erroneous examples are NOT for introducing a concept. They are for deepening understanding after the correct procedure has been taught and processed. Grosse and Renkl (2007) showed that presenting errors before a correct mental model is formed risks encoding the error as the correct approach. Include a note about prerequisite knowledge with each example.

4. **The error analysis scaffold is essential, not optional.** Tsovaltzi et al. (2010) showed that "find the mistake" without structured scaffolding can reinforce rather than correct misconceptions. Every erroneous example must include the full five-step scaffold.

5. **Explain WHY it is wrong, not just THAT it is wrong.** Identification alone does not produce learning gains. The mechanism is self-explanation (Siegler, 2002): students who explain why an error is wrong show deeper conceptual change than students who merely spot it. Step 5 of the scaffold — "explain to the character" — is where the learning happens.

**MUSIC TECH ERROR BANK — draw errors from this bank or add realistic errors in the same pattern:**

EQ errors:
- Boosting mud frequencies (200-400Hz) on vocals instead of cutting, creating a thick, unclear low-mid build-up
- Cutting presence frequencies (2-5kHz) on vocals, making them disappear behind instruments
- Using too wide a Q on surgical cuts, removing wanted frequencies alongside the problem
- Setting the high-pass filter too high (e.g. 300Hz+ on a male vocal), thinning out the body
- Reaching for boost when a cut elsewhere would achieve the same result with less clipping risk (additive vs subtractive approach)

Compression errors:
- Attack time too fast on drums (under 1ms), killing the transients that give drums their punch
- Ratio too high on vocals (10:1+), over-compressing and creating an unnatural, squeezed sound
- Threshold set too low, compressing everything including quiet passages that should breathe
- No make-up gain applied after heavy compression, resulting in a signal that is quieter than the original
- Release time too fast, causing audible pumping as the compressor recovers and re-engages on every cycle

Signal flow errors:
- Insert effects in the wrong order (e.g. reverb before EQ on an insert chain, EQ cutting frequencies after reverb has added them back)
- Send levels set too high, drowning the dry signal in reverb or delay
- Phantom power switched on for dynamic microphones (misconception that all mics need it)
- Monitoring a track through a send return instead of direct out, causing unexpected latency or level issues

Synthesis errors:
- Filter cutoff set too low on a low-pass filter, removing all harmonics and leaving only the fundamental (or silence)
- LFO rate set too fast for the intended effect (e.g. 20Hz vibrato instead of 5Hz, creating a buzzy artefact rather than musical modulation)
- Envelope sustain confused with release (setting sustain to a time value rather than a level)
- Wrong oscillator waveform for the intended timbre (e.g. sine wave when harmonics are needed for the filter to shape)

Routing errors:
- Applying stereo bus processing to a mono source, wasting a stereo image on a centred signal
- Wrong side-chain key input selected (compressing from the wrong trigger source)
- Aux send set to pre-fader when post-fader is needed, meaning the send level does not follow the channel fader
- Routing audio to the wrong output bus, sending a track to headphones when it should go to monitors (or vice versa)

**OUTPUT FORMAT — for each erroneous example, produce:**

### Erroneous Example [N]: [Character Name]'s [Task]

**Prerequisite:** [What students must already understand before encountering this example]

**The scenario:** [A named student character has completed a production task. Describe what they did, including specific parameter values and DAW settings. The description must be detailed enough that the error is findable but not so obvious that it announces itself. Surround the error with 3-4 correct steps.]

**[Character Name]'s settings:**
[List the specific parameters — band frequencies, gain values, ratio, threshold, routing assignments, etc. Use realistic DAW parameter names. Mark which setting contains the error with a comment visible only to the teacher, e.g. (THE ERROR).]

**Error Analysis Scaffold:**

1. **Listen and evaluate:** "[Character Name] says [their description of the result — phrased in the way a student would describe it, e.g. 'warm and full' when they actually mean 'muddy']. Listen to the result. Do you agree with their description?"

2. **Identify the suspect:** "Look at [specific parameter or setting]. What is happening at this point in the [signal chain / frequency spectrum / envelope]? Describe what this setting actually does."

3. **Explain the problem:** "What is the difference between [what the character thinks is happening] and [what is actually happening]? Why does this setting produce [the actual undesirable result] rather than [what the character intended]?"

4. **Correct the error:** "Write the corrected setting for [the specific parameter]. What value would you use, and why?"

5. **Explain your correction to [Character Name]:** "Explain to [Character Name] in plain language WHY your correction works and why their original setting produced the problem. Use specific technical vocabulary."

**Corrected version:** [Show the corrected parameter values with a brief explanation of why the correction works.]

---

After generating all examples, produce a **Teacher Delivery Notes** section:

- Recommended sequence (which example to use first)
- Approximate timing per example (aim for 10-15 minutes each including discussion)
- Key moments where the teacher should pause for class discussion
- Common student responses to anticipate
- How to use these if students cannot identify the error (hint progression: broad hint, then narrow hint, then direct pointer)

**Use UK English throughout** (analyse, equalisation, colour, centre, programme, behaviour, defence, licence/practice distinction).

**Self-check before responding:** Verify that (1) each example contains exactly ONE error surrounded by correct steps, (2) every error is realistic and drawn from the error bank or is a genuine common student mistake, (3) each example includes the full five-step error analysis scaffold, (4) prerequisite knowledge is stated for each example, (5) character descriptions use natural student language (not technical perfection), (6) corrected versions are provided for each example, (7) all terminology matches Edexcel Component 4 vocabulary, (8) no debunked frameworks (learning styles, VAK, left-brain/right-brain) are referenced, and (9) UK English spelling is used throughout.
```

## Example Output

**Input:** Problem domain: Vocal EQ for a pop mix, Target errors: Boosting mud frequencies (200-400Hz) on vocals instead of cutting

**Output:**

### Erroneous Example 1: Jordan's Vocal EQ

**Prerequisite:** Students must have been taught subtractive EQ technique and the role of the 200-500Hz range in vocal clarity. They should have seen a correct demonstration of vocal EQ in Ableton's EQ Eight, including a high-pass filter, a cut in the low-mids, and a presence boost.

**The scenario:** Jordan has recorded a vocal take for a pop track. The vocal sounds "lost in the mix" — it is there, but it does not cut through the instrumental. Jordan opens EQ Eight and makes four adjustments, aiming for a vocal that sounds "warm and full" while sitting clearly in the mix.

**Jordan's EQ Eight settings:**

- Band 1: High-pass filter at 80Hz, 24dB/oct (correct — removes rumble and proximity effect below the vocal's useful range)
- Band 2: +6dB bell boost at 300Hz, Q 1.0 **(THE ERROR — boosting the mud range instead of cutting it)**
- Band 3: -3dB bell cut at 800Hz, Q 2.0 (correct — reducing boxiness in the upper low-mids)
- Band 4: +4dB bell boost at 3.5kHz, Q 1.5 (correct — adding presence and intelligibility)

**Error Analysis Scaffold:**

1. **Listen and evaluate:** "Jordan says the vocals sound 'warm and full' after these EQ changes. Listen to the result with the instrumental playing. Do you agree that the vocals sound warm and full, or would you describe the sound differently?"

2. **Identify the suspect:** "Look at Band 2. What frequency range is being boosted? What does the 200-400Hz range typically sound like when emphasised on a vocal recording?"

3. **Explain the problem:** "What is the difference between 'warm' and 'muddy'? Why does a +6dB boost at 300Hz with a wide Q create a build-up that makes the vocal harder to hear in a mix, even though Jordan intended it to add warmth?"

4. **Correct the error:** "Write corrected settings for Band 2. What frequency, gain, and Q would you use? Explain your choice."

5. **Explain your correction to Jordan:** "Explain to Jordan WHY cutting at 300Hz would make the vocals sit more clearly in the mix. Why does removing energy in this range create the perception of clarity, even though it might seem counterintuitive to cut rather than boost?"

**Corrected version:** Band 2 changed to -3dB bell cut at 300Hz, Q 1.5. Cutting rather than boosting in the 200-400Hz range removes the low-mid energy that competes with guitars, keyboards, and the body of the snare drum. The vocal loses thickness but gains clarity and separation. The presence boost at 3.5kHz (Band 4) now has space to work because the low-mid build-up is no longer masking the upper frequencies.

---

### Erroneous Example 2: Sam's Drum Compression

**Prerequisite:** Students must have been taught the four main compressor parameters (threshold, ratio, attack, release) and their effect on dynamic range. They should have seen a correct demonstration of drum bus compression, including the relationship between attack time and transient preservation.

**The scenario:** Sam is mixing a drum kit for a rock track. The drums sound dynamic but inconsistent — the snare hits vary in level and the kit does not feel "glued together." Sam inserts a Compressor on the drum bus and sets it up to tighten the dynamics while keeping the punch of the kick and snare.

**Sam's Compressor settings:**

- Threshold: -18dB (correct — engaging on most hits but not compressing the quietest ghost notes)
- Ratio: 4:1 (correct — moderate ratio appropriate for drum bus glue)
- Attack: 0.1ms **(THE ERROR — attack is far too fast, catching and squashing the transients instead of letting them through)**
- Release: 150ms (correct — releasing between hits, recovering before the next snare strike)
- Make-up gain: +4dB (correct — compensating for the gain reduction)

**Error Analysis Scaffold:**

1. **Listen and evaluate:** "Sam says the drums sound 'controlled and punchy' after compression. Listen to the drum bus with the compressor engaged. Do the drums sound punchy to you, or has something changed about the character of the hits?"

2. **Identify the suspect:** "Look at the attack time. What does an attack time of 0.1ms mean in terms of how quickly the compressor reacts to incoming transients? What happens to the initial spike of a snare hit when the compressor clamps down this fast?"

3. **Explain the problem:** "What is the difference between 'controlled' and 'squashed'? Why does an extremely fast attack time remove the perception of punch from a drum hit, even though the compressor is correctly reducing dynamic range?"

4. **Correct the error:** "Write a corrected attack time for drum bus compression. What value would you set, and why? What trade-off are you making between transient preservation and dynamic control?"

5. **Explain your correction to Sam:** "Explain to Sam WHY a slower attack time (e.g. 10-30ms) allows the initial transient of each drum hit through before the compressor engages. Why does this preserve the perception of punch while still achieving the dynamic consistency Sam wanted?"

**Corrected version:** Attack changed to 20ms. A 20ms attack allows the initial transient of each drum hit — the sharp, percussive spike — to pass through before the compressor engages. The compressor then reduces the sustained body of the hit, creating the "glue" Sam wanted without removing the punch. The drums sound both consistent and impactful. The precise value depends on the tempo and the drum sounds, but anything between 10-30ms is a reasonable starting point for drum bus compression where transient preservation matters.

---

### Teacher Delivery Notes

- **Recommended sequence:** Use Jordan's Vocal EQ first. EQ errors are more visual — students can see the boost on the EQ Eight display and reason about what it does to the frequency spectrum. Compression is more abstract, so Sam's Drum Compression works better as a second example once students are comfortable with the error analysis scaffold format.

- **Timing:** Allow 10-15 minutes per example including class discussion. Jordan's EQ example typically takes 10 minutes because the visual EQ curve makes identification faster. Sam's Compression example takes closer to 15 minutes because the concept of transient preservation requires more discussion at step 3.

- **Key pause points:** Pause after step 1 for a brief class vote — "Hands up if you agree with Jordan/Sam's description." This surfaces how many students share the character's misconception before the analysis begins. Pause again after step 3 for paired discussion before moving to step 4.

- **Common student responses:** On the EQ example, most students identify the boost correctly but struggle to articulate why cutting achieves clarity (step 5). On the compression example, students often suggest an attack time that is still too fast (e.g. 5ms) — use this as a teaching moment about the range of useful attack times for different sources.

- **If students cannot identify the error:** First hint (broad): "One of these settings is working against what Jordan/Sam is trying to achieve." Second hint (narrow): "Look at the gain direction of Band 2" or "Look at the attack time and think about what happens in the first millisecond of a drum hit." Third hint (direct): "Band 2 is boosting at 300Hz — what does that frequency range sound like when it builds up?"

## Classroom Notes

I first used erroneous examples with Lower Sixth in March 2026, shortly after introducing EQ in the mixing module. These observations are from actual lessons.

- Ableton screenshots with the erroneous settings already dialled in are far more engaging than text descriptions. I project EQ Eight with the incorrect settings visible, play the audio, and ask "What do you think of Jordan's vocal?" The visual display of the EQ curve gives students a concrete reference point. For the text-based version (when I cannot use the DAW live), I draw the EQ curve on the whiteboard, which is slower but still works.

- Students spot EQ errors faster than compression errors. EQ Eight is visual — you can see the boost or cut on the frequency response curve, and students can reason about what that shape means. Compression is abstract — you cannot see an attack time of 0.1ms, you can only hear its effect, and students struggle to connect the parameter value to the auditory result. I now always teach erroneous EQ examples before erroneous compression examples, regardless of curriculum order, because the scaffold format becomes familiar on the easier example first.

- "Explain WHY it is wrong" (step 5) is where the actual learning happens. Students find the error relatively quickly — often within two minutes. But when I ask "Now explain to Jordan why cutting would work better than boosting," the room goes quiet. This is the productive struggle. The students who can articulate the explanation have genuinely understood the principle. The students who cannot have identified the error by pattern recognition without understanding the mechanism. I now spend at least five minutes on step 5, including paired discussion before whole-class sharing.

- Paired activities work brilliantly. One student takes the role of the character (defending the erroneous settings) and the other takes the role of the corrector (explaining what is wrong). The student playing the character naturally generates the kinds of responses a confused learner would give — "But I wanted it to sound warm!" — which forces the corrector to refine their explanation. This is peer explanation at its most effective, and it surfaces misconceptions I would not have caught in a teacher-led discussion.

- One detailed erroneous example with full discussion is 10-15 minutes. Three in one lesson is too many. I learned this by trying to rush through three examples in a fifty-minute lesson and finding that students were identifying errors mechanically by example three without engaging with the explanation steps. Two examples per lesson is the maximum, and one with deep discussion is often better than two with shallow treatment.

- ALWAYS demonstrate the correct approach first, then introduce the erroneous example. I tried reversing this order once — presenting the erroneous example first as a "discovery" task — and several students encoded the error as the correct approach. One student was still boosting at 300Hz two weeks later because that was the first EQ setting they had seen in detail. Grosse and Renkl's (2007) finding about prerequisite correct examples is not a theoretical nicety; it is a practical necessity that I confirmed the hard way.

- The named characters matter more than I expected. Students refer back to "Jordan's mistake" and "Sam's compression" weeks later. The character names make the errors memorable and give students a shorthand for common mistakes. I have heard students say to each other during mixing sessions "you're doing a Jordan" when they spot someone boosting the low-mids on vocals.

## Integration Guidance

**Feeds into:**

- **Interactive resources (React components):** Erroneous examples can be delivered as a new activity type within the interactive resource system. The five-step scaffold maps naturally to a stepped reveal component: show the scenario, reveal the settings, prompt each scaffold step with a text input, then reveal the corrected version. The `music-tech-interactive-resources` skill can generate the React component; this skill provides the content and pedagogical structure.
- **SRS wrong-answer deep links:** When a student answers a retrieval practice question incorrectly, the wrong-answer deep link (currently pointing to revision resources in `lib/revision/resource-links.js`) could point to a relevant erroneous example instead. A student who gets a compression question wrong would be linked to Sam's Drum Compression erroneous example, giving them a structured way to confront and correct the specific misconception revealed by their wrong answer.

**Feeds from:**

- **Assessment results (error patterns):** The `target_errors` input should be populated from actual student error patterns observed in the assessment module. If five students in a cohort consistently set attack times too fast in their mixing coursework, that pattern becomes the target error for a new erroneous example. The assessment module's response data (stored as JSONB in Supabase) can be queried for recurring wrong answers that map to specific parameter misconceptions.
- **Hinge question data (misconceptions):** When a hinge question reveals that a significant proportion of the class holds a specific misconception (e.g. 35% selected the distractor targeting "ratio = fixed dB reduction"), that misconception should be embedded as the target error in a follow-up erroneous example. The hinge question diagnoses the misconception; the erroneous example provides the structured practice in confronting and correcting it.

**SRS connection:** Topics where students encounter erroneous examples should have their SRS box levels monitored for the delayed learning effect that McLaren et al. (2012) documented. An initial dip in performance is expected — the erroneous example may temporarily increase confusion before consolidation occurs. The SRS system should not demote a topic to Box 1 based on a single poor retrieval attempt immediately following an erroneous example lesson. The benefit appears at the delayed test, not the immediate one.

**Assessment connection:** Erroneous examples are formative activities, not graded assessments. However, the error analysis scaffold responses (particularly step 5 — the explanation) provide rich qualitative data about student understanding that complements the quantitative data from MCQ assessments. If the assessment module supports free-text response capture, the scaffold responses could be logged as evidence of conceptual development.

## Known Limitations

- **Text descriptions are a poor substitute for hearing the result.** Erroneous examples are most powerful when students can A/B the erroneous and corrected versions in the DAW. A text description of "the vocals sound muddy" does not carry the same diagnostic information as actually hearing muddy vocals. Where possible, prepare the erroneous settings in an Ableton project file and play the audio live. The text-based version works for analysis but loses the auditory dimension that makes Music Technology assessment authentic.

- **Generates parameter descriptions, not actual Ableton presets.** This skill outputs text — specific parameter values and settings — but does not generate `.adv` preset files or Ableton Live Set files. The teacher must manually set up the DAW with the erroneous settings before the lesson. This preparation step takes 5-10 minutes per example but is essential for the full auditory experience.

- **Some "errors" are genre-dependent.** Heavy compression with a fast attack is wrong for a rock drum bus where transient punch matters, but it is a deliberate creative choice in hip-hop or electronic music. A +6dB boost in the low-mids is wrong for a pop vocal but might be intentional for a lo-fi aesthetic. The examples generated by this skill assume the production conventions of mainstream pop, rock, and acoustic genres. Teachers using these examples in lessons about genre-specific production should contextualise accordingly.

- **Cannot address errors in physical studio technique.** Microphone placement, cable management, acoustic treatment, gain staging on hardware, and other physical production skills involve errors that cannot be represented as parameter values in a text-based erroneous example. These errors require in-studio demonstration with real equipment.

- **Risk of encoding errors if prerequisites are skipped.** If a teacher uses an erroneous example before students have seen and processed the correct approach, there is a genuine risk that students will remember the erroneous settings more vividly than the correct ones. The prerequisite field on each example exists to prevent this, but the skill cannot enforce the sequencing — the teacher must ensure the correct example has been taught first.
