---
name: ableton-house-production
description: >-
  Control Ableton Live via MCP to produce house music. Use when the user asks
  to create tracks, beats, basslines, chords, melodies, arrangements, mix,
  master, or anything related to music production, Ableton, or house music.
---

# Ableton Live House Music Production

## Connection

The `ableton-mcp` MCP server connects to Ableton Live via TCP on port 9877.
The AbletonMCP Remote Script must be running inside Ableton (Settings > Link, Tempo & MIDI > Control Surface > AbletonMCP).

Use `CallMcpTool` with `server: "user-ableton-mcp"`.

## Complete Tool Reference (128 tools)

### Session
- `get_session_info` — full state: tempo, tracks, scenes, transport, master

### Tracks (CRUD + Properties)
- `get_track_info` / `get_return_track_info` / `get_master_track_info`
- `create_midi_track` / `create_audio_track` / `create_return_track`
- `delete_track` / `delete_return_track` / `duplicate_track`
- `set_track_name` / `set_track_color`
- `set_track_mute` / `set_track_solo` / `set_track_arm`
- `set_track_volume` (0.0-1.0, 0.85≈0dB) / `set_track_panning` (-1 to 1)
- `set_track_send` (send_index, value)
- `set_track_input_routing` / `set_track_output_routing`

### Master / Crossfader
- `set_master_volume` / `set_master_panning`
- `set_crossfader` / `set_cue_volume`

### Clips
- `create_clip` (track_index, clip_index, length in beats)
- `add_notes_to_clip` (notes: [{pitch, start_time, duration, velocity, mute}])
- `get_clip_notes` / `remove_notes_from_clip`
- `set_clip_name` / `set_clip_color` / `set_clip_loop` / `set_clip_loop_start` / `set_clip_loop_end`
- `set_clip_gain` / `set_clip_pitch` (coarse semitones, fine cents)
- `duplicate_clip_slot` / `quantize_clip`
- `fire_clip` / `stop_clip`

### Scenes
- `get_scene_info` / `create_scene` / `delete_scene` / `duplicate_scene`
- `fire_scene` / `set_scene_name` / `set_scene_tempo`

### Devices & Parameters (MIXING / MASTERING)
- `get_device_parameters` (track_index, device_index, target)
- `set_device_parameter` (track_index, device_index, parameter_index, value)
- `set_device_enabled` (bypass on/off)
- `insert_device` (by name: "EQ Eight", "Compressor", "Reverb", etc.) — Live 12.3+
- `delete_device`
- Target can be "track", "return", or "master"

### Transport
- `set_tempo` / `set_time_signature`
- `start_playback` / `stop_playback` / `continue_playback` / `stop_all_clips`
- `set_metronome` / `set_song_loop` / `set_groove_amount` / `set_swing_amount`
- `set_quantization` / `capture_midi`
- `jump_to_time` / `jump_by`
- `set_session_record` / `set_arrangement_record` / `set_overdub`
- `undo` / `redo`

### Browser
- `get_browser_tree` / `get_browser_items_at_path` / `search_browser`
- `load_browser_item` (load instruments/effects/samples by URI)

### AI Generators
- `generate_drum_pattern` / `generate_bassline`
- `get_scale_notes`

## House Music Defaults

When unspecified:
- **BPM**: 124-126 (range: 120-128 for tech house)
- **Key**: Am, Fm, Gm, Cm, Dbm/C#m
- **Time sig**: 4/4
- **Clip length**: 4 or 8 bars (16 or 32 beats)

## MIDI Note Reference (Ableton convention: C3 = MIDI 60 = middle C)

| Note  | MIDI | Hz       | Note  | MIDI | Hz       | Note  | MIDI | Hz       |
|-------|------|----------|-------|------|----------|-------|------|----------|
| C0    | 24   | 32.70    | C1    | 36   | 65.41    | C2    | 48   | 130.81   |
| C#0   | 25   | 34.65    | C#1   | 37   | 69.30    | C#2   | 49   | 138.59   |
| D0    | 26   | 36.71    | D1    | 38   | 73.42    | D2    | 50   | 146.83   |
| Eb0   | 27   | 38.89    | Eb1   | 39   | 77.78    | Eb2   | 51   | 155.56   |
| E0    | 28   | 41.20    | E1    | 40   | 82.41    | E2    | 52   | 164.81   |
| F0    | 29   | 43.65    | F1    | 41   | 87.31    | F2    | 53   | 174.61   |
| F#0   | 30   | 46.25    | F#1   | 42   | 92.50    | F#2   | 54   | 185.00   |
| G0    | 31   | 49.00    | G1    | 43   | 98.00    | G2    | 55   | 196.00   |
| Ab0   | 32   | 51.91    | Ab1   | 44   | 103.83   | Ab2   | 56   | 207.65   |
| A0    | 33   | 55.00    | A1    | 45   | 110.00   | A2    | 57   | 220.00   |
| Bb0   | 34   | 58.27    | Bb1   | 46   | 116.54   | Bb2   | 58   | 233.08   |
| B0    | 35   | 61.74    | B1    | 47   | 123.47   | B2    | 59   | 246.94   |
| C3    | 60   | 261.63   | C4    | 72   | 523.25   | C5    | 84   | 1046.50  |

**Sub-bass sweet spot (40-100 Hz) = C1 to G1 = MIDI 36-43**
**Bass range (100-250 Hz) = Ab1 to B2 = MIDI 44-59**

Formula: f = 440 × 2^((n-69)/12) where n = MIDI note number.

Drum rack (GM): Kick=36, Snare=38, ClosedHat=42, OpenHat=46, Clap=39, Ride=51, LowTom=41, HiTom=50

## Timing (beats in 4/4)

1 bar = 4.0 | 1 beat = 1.0 | 1/8 = 0.5 | 1/16 = 0.25 | triplet 8th = 0.333

16th note grid positions in one bar (4 beats):
```
Beat:     1       2       3       4
16ths:  0  .25 .5 .75 | 1  1.25 1.5 1.75 | 2  2.25 2.5 2.75 | 3  3.25 3.5 3.75
Kick:   X              X              X              X
Offbeat:      X              X              X              X       (0.5, 1.5, 2.5, 3.5)
```

---

# SOUND DESIGN MASTERCLASS

## BASS: Three-Layer Architecture (from pro tutorials)

House bass is NOT one sound. It is THREE SEPARATE LAYERS stacked:

1. **Main Bass** — the melodic/rhythmic layer you HEAR (~80-250 Hz)
2. **Sub Bass** — the deep layer you FEEL (~16-60 Hz)
3. **Textured Bass** — the character layer that adds INTEREST (~250+ Hz)

Each layer has its own track, its own sound source, its own patterns, and its own effects chain. Trying to make ONE synth patch do all three jobs produces flat, buzzy, unusable noise. This was the fundamental mistake of the Saw32 Operator branch.

---

### Layer 1: MAIN BASS (the one you hear)

**What it is**: The melodic, rhythmic bass that carries the groove. This is what people hum. It sits in the ~80-250 Hz range. It has body, warmth, and bounce.

**What it feels like**: A round, warm tone with weight. Think vintage synth bass — Moog, Juno, Diva. NOT a raw oscillator. NOT buzzy. NOT thin.

**Sound selection**:
- ALWAYS start from professionally designed presets — search: "house bass", "analog bass", "body bass", "bounce bass", "mello bass"
- Good Ableton presets: "Bounce Bass.adg", "Body Bass.adg", "Basic Analog Bass.adg", "Basic Jupo Bass.adg", "House Bass.adv"
- External VSTs (if available): Trillian, Diva, Serum, u-he Repro
- The trick for tweaking presets: focus on **filter cutoff**, **resonance**, and **filter envelope**. These three knobs shape any preset into something usable.

**Patterns**:
- Typically starts at the **second octave** (C2-C3 range, MIDI 48-60)
- Keep simple — complex patterns clutter the mix and make it harder to fit other elements
- See "Four Bass Pattern Types" below for specific patterns

**Effects chain** (in order):
1. **EQ Eight**: roll off below 30 Hz (sub bass handles that)
2. **Saturator** (e.g. Decapitator, Ableton Saturator): add crunch/warmth, shape tone (brighter or darker)
3. **Auto Filter**: further shape the tone after saturation — like a second cutoff control
4. **Sidechain compressor** to ghost kick: THIS CREATES THE BOUNCE

---

### Layer 2: SUB BASS (the one you feel)

**What it is**: Everything between 16-60 Hz. You feel it in your chest more than hear it with your ears. In a club, this is the pressure wave that hits your body.

**What it feels like**: A deep, sustained, powerful rumble. NOT a note you can hum — a physical sensation.

**Sound selection — two approaches**:

**A) From scratch (Operator)**:
- Load Operator. Drop Osc-A Coarse to **0.5** (one octave below MIDI note). Done.
- Optionally add a wave with more character and then filter it heavily

| Parameter | Value | Why |
|-----------|-------|-----|
| Osc A waveform | Sine (0) | Pure sub tone, no harsh harmonics |
| Osc A Coarse | 0.5 | One octave below MIDI note — deep sub |
| Osc B/C/D Level | 0 (off) | Only one oscillator for clean sub |
| Ae Sustain | 1.0 (max) | Note holds at full volume while held |
| Ae Release | 200-400ms | Smooth tail |
| Filter | OFF | Sine has nothing to filter |
| Voices | Mono | Always mono |

**B) From the main bass preset**:
- Duplicate the main bass sound, drop it **one octave**, then filter it heavily with Auto Filter to remove everything above ~60-80 Hz
- This gives a sub that's harmonically related to the main bass

**Patterns**:
- Sit at **C1 and below** (MIDI 36 and below, where you feel it)
- Can mirror the main bass pattern for simple reinforcement
- Can also do independent, simpler patterns — long sustained notes under the main bass groove
- KEY RULE: sub must NOT interfere with main bass. Keep it simple.

**Effects chain** (in order):
1. **Utility**: mono (sub bass must be mono — no stereo information below 120 Hz)
2. **Saturator**: adds upper harmonics so the sub is audible on small speakers
3. **Auto Filter**: low-pass, makes it a definitive sub (everything above ~60-80 Hz removed)

---

### Layer 3: TEXTURED BASS (the one that adds character)

**What it is**: Everything above ~250 Hz. These are the layers that give bass its unique character, movement, and texture. This is where you hear acid lines, FM character, resonant sweeps, arpeggiated sequences.

**What it feels like**: The "personality" of the bass. It could be an acid squelch, an FM knock, a gritty texture, a resonant sweep. It sits on TOP of the main bass and sub, adding interest without carrying the weight.

**Sound selection**:
- FM patches: "Basic FM House Bass.adg", "FM Pluck Bass.adg"
- Acid patches: "Acid Bass.adv", "Basic 303 Bass.adg"
- Textured/character presets: any bass with distinct high-end character
- Sequenced/arp presets: built-in arp patches that play patterns from one note
- **Samples from 90s packs**: many iconic house bass sounds are actually samples, not synthesized

**Patterns**:
- Can range from simple root-note holds to complex acid sequences
- Repetitive note patterns work well (16th-note pulses on one note)
- Can add filter movement/automation — sweep cutoff with resonance cranked for texture
- Can be more experimental — reverb and delay are safe to use here since you're dealing with higher frequencies

**Effects chain**:
1. **EQ Eight**: high-pass at 200-300 Hz (the main bass and sub handle the lows)
2. **Saturator/Distortion**: shape the character
3. **Auto Filter**: automate cutoff for movement and sweeps
4. **Reverb/Delay**: safe to use in small-moderate amounts (unlike sub bass where these are forbidden)

---

### How the three layers work together

```
Frequency:  16Hz -------- 60Hz -------- 250Hz -------- 2kHz+
Layer:      [  SUB BASS  ] [ MAIN BASS  ] [ TEXTURED BASS ]
Feel:       You FEEL this  You HEAR this  This adds CHARACTER
```

- Each layer occupies its own frequency range — minimal overlap
- EQ each layer to stay in its lane (high-pass the main bass, low-pass the sub, high-pass the texture)
- Sidechain ALL bass layers to the kick
- The main bass carries the groove. The sub adds weight. The texture adds personality.
- You don't always need all three — many tracks use just main + sub, or just main + texture

---

### When you MUST build from scratch (sub bass only)

**Operator (best for pure sub bass):**

CRITICAL: Operator's Coarse parameter follows the harmonic series, NOT semitones.
Coarse 1 = fundamental = same pitch as MIDI note. Coarse 0.5 = one octave down.

MIDI notes: play at C#1 = MIDI 37 = 69.3Hz for Db minor root.

**WARNING**: Do NOT try to make Operator do everything. Operator with raw saw waves and filters produces thin, buzzy, unusable bass. Use Operator ONLY for pure sub bass (sine wave, coarse 0.5). Use presets for everything else.

**Drift (for warmer, analog-style sub bass):**

| Parameter | Value | Why |
|-----------|-------|-----|
| Osc 1 shape | Sine or Triangle | Clean sub |
| Osc 1 octave | -1 | Low range |
| Filter type | Type II (MS2) | Warm analog character |
| LP Freq | 0.15-0.30 | Dark, subby |
| Env 1 Sustain | 0.7-1.0 | NOTE STAYS LOUD |
| Spread | 0% | Mono |
| Voices | Mono | Always |

---

### THE #1 BASS PATTERN RULE (from pro tutorials)

**Every note sits on a BEAT or an OFFBEAT. Period.**

From Max Styler masterclass: "every single note is on a beat or an offbeat." This means notes at positions 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5 — the 8th note grid ONLY. NO ghost notes at 16th positions (0.25, 0.75, 1.25, etc.) unless you are explicitly doing rolling 16ths with mandatory sidechain.

**WHY**: Notes between the grid positions create mush. The kick hits on beats (0, 1, 2, 3). The bass hits on offbeats (0.5, 1.5, 2.5, 3.5). This interlocking creates the push-pull groove that IS house music. Adding ghost notes at random 16th positions destroys the clarity of this interlock.

### Bass Pattern Structure: Call-Response (from Max Styler)

Every bass pattern should have a 2-bar call-response structure:
- **Bar 1 (call)**: Melody moves in one direction (e.g., descending)
- **Bar 2 (response)**: Melody moves in the opposite direction (e.g., ascending)

Classic: call UP (builds tension), respond DOWN (releases tension).
Alternative: call DOWN, respond UP (builds tension at end of phrase for loop reset).

The response should feel like an answer to the call. This creates forward motion and prevents the loop from feeling static.

### Electro/Tech House Offbeat Style (the current meta)

The dominant tech house bass style right now is electro-influenced offbeat bass:
```
Beat:  1    &    2    &    3    &    4    &
Kick:  X         X         X         X
Bass:       X         X         X         X
```
- EVERY note on a beat or offbeat — nothing in between
- Some bass also sits UNDER the kick (on the beats) for a more constant rolling feel
- Note duration controlled by sidechain envelope, not by making notes super short
- Velocity: CONSISTENT (100-115) — bass is NOT a place for velocity games

You CAN add a few notes on beats (under the kick) for a deeper rolling presence:
```
Beat:  1    &    2    &    3    &    4    &
Kick:  X         X         X         X
Bass:  x    X    x    X    x    X    x    X
```
(lowercase x = quieter note under kick, uppercase X = main offbeat hit)

### Six Bass Pattern Types (from Produce School + 19 Bass Patterns)

#### 1. Offbeat 8ths (classic house — simple starting point)
```
Beat:  1    &    2    &    3    &    4    &
Kick:  X         X         X         X
Bass:       X         X         X         X
```
- BUT: this alone is BORING. Must add velocity→cutoff modulation, or octave jumps, or variation.
- "If you just use this without modulation, it sounds generic quickly." — Produce School

#### 2. Offbeat Variation (the modern standard — DEFAULT CHOICE)
```
Beat:  1    &    2    &    3    &    4    &
Bass:  ^    X         X    ^    X         X
```
- Start with offbeats, then ADD select notes: one on beat 1 (octave UP), one extra in between
- "Adding 4 extra notes gives a whole different vibe" — Produce School
- **Octave-up accents on beats** = drama without mud (high note doesn't clash with kick's sub)
- Small adjustments make the difference between "normal" and "good"

#### 3. Full 1/8 Fill (driving, needs sidechain)
```
Beat:  1    &    2    &    3    &    4    &
Bass:  X    X    X    X    X    X    X    X
```
- More glued together, takes more mix room
- REQUIRES sidechain — without it, kick and bass fight constantly

#### 4. Rolling 16ths with Octave Jumps (dramatic)
```
Beat:  1  e  &  a  2  e  &  a  3  e  &  a  4  e  &  a
Bass:  X  X  X  X  X  X  ^  X  X  X  X  X  ^  X  X  X
```
- "The trick is always using Legato" — 19 Bass Patterns
- ^ = octave jump notes — create drama within the rolling pattern
- Remove first 1-2 notes for "train" feel variation

#### 5. Gliding Legato Bass (303-inspired, acid-influenced)
- Mono legato ON, portamento time added
- Jump between octaves with glide notes
- **Workflow**: lay down the foundation FIRST, then add octave jumps and glides
- Sound must be bassy in low end AND crunchy in high end — sub-only sounds don't work here

#### 6. Sustained + Answer (call-response that actually works)
```
Bar 1:  [LONG SUSTAINED NOTE_________________]
Bar 2:  [short] [short] [short] [octave^] [short]
```
- Deep sustained bass as first hit, then rhythmic staccato response
- Add filter automation on the sustained note for movement
- "Answer and response across all genres always works" — Produce School
- Leaves room for drums/top elements

### THE REAL BASS PATTERN RULES (from pattern tutorials)

**OCTAVE JUMPS are the #1 technique for drama.** Almost every good pattern uses them.
- A2 → A3 (MIDI 57 → 69) = one octave up accent
- Place octave jumps at different positions across bars for variation
- Octave-up notes on beats are fine — they don't clash with kick because the energy is in a higher register

**Velocity should MODULATE the sound, not just volume.**
- Link velocity to filter cutoff: harder hits = brighter = natural accents
- Higher velocity on octave jumps and accent notes (120+)
- Lower velocity on passing notes (90-100)
- This creates timbral variation even on a simple rhythm

**4-bar phrases, not 2-bar.** The second half MUST have different rhythm/syncopation from the first half. "Create something for the first half, then change the rhythm for the second half, syncopate more."

**Space = groove.** Deliberately remove notes (rests) to create character. "Go back and remove the first two notes — it's like a train."

**Layered patterns.** Two different bass sounds with different patterns:
- Bottom: rolling 8ths (sidechained) for foundation
- Top: melodic offbeat pattern with octave jumps for interest

### WAVETABLE BASS RECIPE (from "Killer Tech House Bassline" tutorial)

This is the STANDARD way to build a tech house bass from scratch in Ableton:

1. **Load Wavetable** (empty/default patch)
2. **Amp Envelope**: IMMEDIATELY pull back Release (default 600ms is way too long — notes blend)
3. **Oscillator 1**: Sawtooth waveshape, push wave position up slightly for upper harmonics
4. **Filter**: 12dB slope (NOT 24dB — keep some harmonics). Add slight resonance. Dial frequency down.
5. **Envelope 2 → Filter Frequency** (via Matrix tab): 
   - Click filter frequency knob, assign to Envelope 2
   - Envelope 2: Sustain all the way DOWN, Decay dialed back
   - Creates the "twang" attack — short bright burst on each note
   - For dark/subby tech house: LESS twang (shorter decay). For minimal: MORE twang.
6. **Oscillator 2**: Turn ON, also sawtooth. Send its waveshape to Envelope 2 as well.
   - This is the "upper harmonic layer" that gives presence
7. **Mono mode**: Bass should be monophonic to avoid overlapping notes
8. **Glide**: Enable in mono mode for slides between notes (legato)

### VELOCITY → FILTER CUTOFF (THE secret to bounce)

Confirmed across 3+ tutorials as the #1 technique that separates good bass from generic:
- In Wavetable: Matrix → assign Velocity to filter frequency amount
- In Serum: Envelope to cutoff, then velocity as aux source controls how much envelope opens
- In any synth: velocity should modulate TIMBRE, not just volume
- Higher velocity = filter opens more = brighter attack = natural accent
- Lower velocity = filter stays closed = darker, quieter = passing note
- "If you don't have velocity modulation, your bass will sound generic quickly"

### BASS PROCESSING CHAIN (combined from ALL tutorials)

Order matters. Each step builds on the previous:

1. **Saturator** (CRITICAL for presence):
   - Mode: Analog Clip or Hard Clip
   - Add drive, then dial dry/wet DOWN and bring up until harmonics appear
   - GAIN MATCH after: turn off saturator, note the peak level, turn on, reduce output to match
   - "Without mid-range growl from saturation, bass just rumbles underneath — no presence"
2. **EQ Eight** (after saturator):
   - High cut to control where saturation harmonics land
   - Duck resonant mud around 200 Hz (narrow band, -3dB max)
   - Find and gently boost liked harmonics in mid-range
   - Only 2-3 dB moves. Don't go crazy.
3. **Erosion** (optional, for character):
   - Sine wave mode = squeal/presence
   - Noise mode = deep analog growl
   - Both together = very full sounding
4. **Sidechain** (Kickstart or Compressor):
   - MANDATORY. "It's never going to sound good without sidechain."
   - Bass should swell back on the offbeat as kick's tail drops off
   - Pro technique: use a separate trigger channel (short click) instead of actual kick
5. **Final EQ** (tonal shaping):
   - Check 200 Hz range for mud
   - Find tonal areas you like in the mids and gently boost
   - High cut if still too bright

### ALTERNATIVE BASS APPROACH (from 2-hour course)

For a quick, great-sounding sub: Load Ableton's Analog "Pure Square Bass" preset, then aggressively low-pass with EQ8 (x4 filter at ~130-150 Hz). Sounds analog and chunky, perfect for tech house.

### 5 TYPES OF TECH HOUSE BASS (from sound design tutorials)

1. **Tech House Sub**: Saw wave, -2 octave, filter 200-300Hz, tube distortion, low end boost
2. **Saw Pluck**: Saw wave, envelope shapes as pluck, filter with envelope modulation on cutoff
3. **Reso Pluck** (acid feel): Square + saw, HIGH resonance, envelope to cutoff — Chris Lake style
4. **FM Bass** (knock sound): Two sine waves, FM modulation, LFO on pitch for "knock"
5. **Knock Bass**: Sine wave with pitch envelope creating kick-like thump + distortion + filter

### Common bass mistakes to NEVER make:
- **Same 2-bar phrase copied 4 times** = instant boredom, no development
- **No octave jumps** = flat, lifeless, no drama
- **Constant velocity with no filter modulation** = generic, static timbre
- **No saturation** = bass has no mid-range presence, gets buried
- **No EQ after saturation** = harmonics land in random ugly places
- **Default release on synth (600ms)** = notes blend into mush
- **No sidechain** = bass and kick fight, no bounce
- **No envelope on filter** = flat static timbre, no "twang" attack
- **Polyphonic mode** = overlapping bass notes = mud
- **Sub bass in stereo** = phase problems, weak low end
- **Skipping saturation/EQ** = sounds empty and thin in the mix

---

## DRUMS: The Groove Engine

### Philosophy
Drums are the skeleton of house music. The kick is the FOUNDATION — everything is mixed around it. The hat is the COUNTER-PUNCH (people go DOWN on kick, UP on offbeat hat). The clap/snare is the backbeat. Everything else is seasoning.

**The kick-hat relationship is critical** — it's literally how people dance: down on kick, up on offbeat hat.

### Use Ableton's built-in drum racks FIRST
Search browser for: "Kit-909", "Kit-808", "Kit-Core 909", "Kit-House"
These are production-ready. Don't try to build drum racks from scratch.

### Kick drum (4-on-the-floor)
```
Beat:  1    2    3    4
Kick:  X    X    X    X
```
- Velocity: 110-127, consistent (kick is the anchor)
- Duration: 0.25-0.5 beats
- **Set kick to 0 dB** (full headroom) using a hard clipper: Saturator > Digital Clip > Hard Clip
- Kick sub should hit at or above -6dB in spectrum analyzer
- TUNING: kick fundamental usually 40-80Hz. If you can, tune kick sub to key of track (5th works great)
- **Kick top layers**: for electro feel, layer disco/offbeat top loops over kick to get steady 8th-note transient feel

### Kick + Clap GROUP Clipping (from Max Styler)
Route kick and clap/snare to same group. Put a hard clipper on the group.
When kick + clap hit together, signal goes over 0 — clipper cuts it off.
Result: aggressive "tearing" sound, consistent low-end punch, saves master limiter downstream.
- Saturator > Digital Clip > Hard Clip on kick+clap group
- The snare's high frequencies mask the clipping distortion

### Hi-hats (the groove carrier)
**Basic offbeat 8ths (closed hat) — DEFAULT for clean grooves:**
```
Beat:  1  &  2  &  3  &  4  &
Hat:      X     X     X     X
```
This pairs with offbeat bass for the electro tech house feel.

**Classic house 16th pattern:**
```
Beat:  1  e  &  a  2  e  &  a  3  e  &  a  4  e  &  a
Closed: X  x  X  x  X  x  X  x  X  x  X  x  X  x  X  x
Open:                                 O
```
- Lowercase x = ghost note (velocity 60-80)
- Uppercase X = accent (velocity 100-120)
- O = open hat (replaces closed hat, velocity 100-110)
- Open hat on beat 3's & or beat 4 = classic house feel
- VELOCITY VARIATION IS ESSENTIAL — uniform velocity = robotic, dead
- Apply swing via groove template or manual start_time offsets
- **Tighten open hat decay**: in 909 Core Kit, click open hat and pull Decay down for tighter sound
- Use two different hat sounds (e.g., 909 airy + acoustic dark) for contrast

### Clap + Snare (the perfect pair — from Max Styler)
```
Beat:  1    2    3    4
Clap:       X         X
Snare:      X         X
```
**Why clap + snare together**: They fill different frequency ranges like puzzle pieces:
- **Snare**: peaks at ~200Hz (body) and ~5-7kHz (top-end spray)
- **Clap**: fills the mid-range hole between those two peaks
- Together they create a tall, full-spectrum backbeat

Snare processing: layer 2-3 snare samples (distorted low snare + top-end snare + basic snare), slight reverb (12%), subtle saturation, slow-attack compression to tighten.
Clap processing: just one good clap sample, mono, slight saturation.

### Dimensional Drum Layers (from Max Styler — height/width/depth)
Instead of processing a single sound to add dimension, use LAYERS that already have the dimension:
- **Height** = frequency content (sample selection gives this)
- **Width** = stereo image (find a wide sample, or use chorus/unison)
- **Depth** = front-to-back (find a sample with natural reverb tail, or add reverb)
- Add "clap tail" layers: one wide + high-frequency, one mono + low-frequency
- Trim attack of tail layers so they don't compete with main transient

### Percussion (texture layer)
- Shakers, rides, congas, rimshots, toms
- Should sit BEHIND kick, hat, and clap in volume
- Use varied velocity (70-110) for organic feel
- Rides: can replace or complement hats — use for "lift" sections (909 ride with slight reverb)
- Add swing to percussion: use Command-3 (triplet grid) in Ableton and shift notes slightly right

### Drum humanization techniques:
1. **Velocity variation**: never program all hits at the same velocity. Main hits 100-120, ghost notes 60-80.
2. **Swing**: apply via Ableton groove pool or manual start_time offsets (shift 16th notes by +0.02-0.04 beats)
3. **Micro-timing**: shift select notes off grid for human feel
4. **Ghost notes**: quiet hits between main beats on hats and perc (velocity 30-50)
5. **Open/closed hat interaction**: open hat should cut off when closed hat plays (choke group in drum rack)

---

## CHORDS & KEYS: The Harmonic Color

### Philosophy
House chords should be WARM, JAZZY, and SPACIOUS. Never use plain triads (C-E-G is boring). Always use 7ths, 9ths, or 11ths. The chord sound should blend into the track, not dominate it.

### Sound selection
Search browser for: "Electric Piano", "Rhodes", "Keys", "Pad", "Stab"
For stabs: short, punchy sounds with fast attack and short decay.
For pads: sustained, warm sounds with slow attack and long release.

### Chord voicing rules:
1. **Always use 7th chords minimum**: Am7 (A-C-E-G), Cm7 (C-Eb-G-Bb), Dbm7 (Db-Fb-Ab-Cb)
2. **Add 9ths for color**: Cm9 = Cm7 + D, Am9 = Am7 + B
3. **Add 11ths for cluster/dark texture**: Cm11 = Cm7 + F
4. **Use inversions**: don't always play root position. Spread notes across 1.5-2 octaves.
5. **Leave the root note to the bass**: chord voicings should start from the 3rd or 5th, NOT the root. The bass track handles the root.
6. **Vary voicings between chords**: don't use the same inversion pattern for every chord.

### Classic house progressions (in minor keys):
- **i - iv**: Cm7 - Fm7 (two-chord vamp, hypnotic)
- **i - v**: Am7 - Em7 (tension-resolution)
- **i - VII - VI - VII**: Cm7 - Bb7 - Ab7 - Bb7 (emotional lift)
- **i - i - v - v - i - i - v - III**: 8-bar cycle, change last chord for hook

### Chord rhythm (stab patterns):
- Syncopated: avoid hitting on beat 1 and 4 (those are kick territory)
- Emphasize offbeat 16th notes for rhythmic interest
- Mix short stabs (0.15-0.25 beats) with longer holds (0.5-1.0 beats) for call-and-response
- Leave gaps — not every beat needs a chord hit

### Chord processing:
- **EQ Eight**: high-pass at 200-300Hz (bass handles the lows), cut mud at 400-600Hz
- **Reverb** (on return track): 1.5-3s decay, pre-delay 20-40ms, mix 25-40%
- **Auto Filter**: gentle low-pass, automate cutoff for builds/breakdowns
- **Compressor**: gentle 2:1, glues the chord together

---

## MIXING: The Guillotine Framework (from Max Styler Masterclass)

### Step 1: Set the Foundation — Kick at Zero
- Park the kick at 0dB with a hard clipper (NOT a utility or limiter)
- Put a limiter (L2 or Ableton Limiter) at 0dB on the master
- This means: as you produce and mix, you know how the track sounds in mastering context
- If something triggers the limiter weirdly, fix it in the mix, not in mastering

### Step 2: Objective Levels (the framework — NON-NEGOTIABLE)
These levels must be correct or the track won't work in a club:

| Element | Target Level | How to Check |
|---------|-------------|--------------|
| **Kick sub** | At or above -6dB | Spectrum analyzer, sub range |
| **Bass fundamental** | -6 to -12dB (or slightly above) | Spectrum analyzer, sub range |
| **Kick MUST win** | Kick louder than bass in sub | Visual check: kick peak > bass peak |
| **Hat average** | Around -37 to -41dB | Spectrum analyzer, top-end range |

If levels are wrong: use Utility (whole level) or EQ (specific frequency) to adjust.

### Step 3: Subjective Levels (hanging the pictures)
Once objective levels are solid, set everything else by ear within that framework:
- Work in order of importance: vocal chop → lead vocal → ear candy → percussion
- Compare each sound to reference tracks at similar loudness
- Test in mono (Utility: -10dB, width=0) to check intelligibility

### Step 4: Three Dimensions of the Mix
1. **Frequency (height)**: covered by EQ and sound selection
2. **Stereo (width)**: bass/kick mono down middle, hooks can be wide (chorus/unison), vocal chops wide
3. **Depth (front-to-back)**: drops should be DRY and FORWARD. Breaks should feel pushed BACK with reverb/delay. This contrast makes drops hit harder.

### THE SUB RULE (from John Summit's engineer)
**Sub must be as loud or LOUDER than the harmonic.** If the harmonic peak (~96Hz) is louder than the sub peak (~45Hz), the bass lacks power. Fix with EQ: boost sub by up to 7dB if needed. "If the harmonic is louder than the sub, it's off and you're going to be missing the power."

### Build-to-Drop Dynamics (from John Summit's engineer — do this EVERY time)
1. **Reverb**: increase wetness + decay through the build. Last phrase before drop = COMPLETELY DRY for maximum impact.
2. **Level**: automate vocal/synth levels UP through the build (+3 to +8dB range over 8-16 bars)
3. **Snare roll**: needs both filter opening AND level increase — not just one
4. **Master Utility gain**: drop gain -0.8dB through build, jump back to 0 at drop. Emphasizes the drop massively.
5. **Width**: automate master width to get wider through build, then snap back at drop
6. **Rule**: "Always pay attention to how your music can grow instead of being static"

### Sidechain compression setup (NON-NEGOTIABLE for house):
**Method 1 — Compressor sidechain (from John Summit's engineer):**
1. Use Soothe2 or fast compressor (Pro-C2) for sidechain
2. Focus sidechain on LOW END ONLY — don't touch harmonics unnecessarily
3. Fast attack, fast release
4. Can use two stages: one for sub ducking, one for overall nudge

**Method 2 — LFO Tool / Kickstart (preferred for 4-on-floor):**
- No compression involved — just volume envelope synced to kick
- More precise control over the shape of the duck
- Can use multiple Kickstart instances for different purposes:
  1. First: 100% mix, tight envelope — clears kick transient completely
  2. Second: ~89% mix, shapes envelope around the kick body
  3. Third: pushes down bass where kick tail overlaps (2nd 16th note area)

### EQ frequency carving:
| Element | High-pass | Presence boost | Cut |
|---------|-----------|---------------|-----|
| Kick | 30Hz | 50-60Hz, 3-5kHz (click) | 200-400Hz (box) |
| Bass | 30Hz | ~400Hz (tonal character) | At kick's fundamental |
| Clap | 200Hz | 1-2kHz (snap) | - |
| Hats | 400Hz | 8-12kHz (air) | - |
| Chords | 200-300Hz | 2-4kHz (clarity) | 400-600Hz (mud) |
| Vocals | 100Hz hard cut | 2kHz (magic vocal freq) | 300Hz (low-mid mud) |
| Master | - | - | Side-cut below 120Hz (mid/side EQ) |

### Master chain (combined from Max Styler + EDM Tips):
1. **Coloring** (optional): harmonic exciter (Oxford Inflator) + sub boost (Bark of Dog at fundamental ~44Hz, +7dB)
2. **Reductive EQ** (Pro-Q3 or EQ Eight):
   - High-pass at 30Hz (mono)
   - Side-cut below 120Hz (mid/side mode) — removes stereo low-end mud
   - Optional: high shelf boost on SIDES for width
3. **Glue Compressor**: 30ms attack (lets kick through), auto release, 4:1 ratio, 2dB GR. Gels mix.
4. **Multiband Compressor** (optional): compress bass band separately, few dB GR, locks in low end
5. **Sweetening EQ** (analog-modeled, e.g. Pultec-style): subtle warmth, Pultec bass trick (boost AND cut at same freq)
6. **Stereo Imager** (Ozone or similar): lock bass mono below 120Hz, widen highs slightly
7. **Upwards Compressor** (Multiband Dynamics, ratio ~1.03-1.05): pushes mix up from bottom, adds fatness
8. **Hard Clipper**: clips peaks before limiter, offloads limiter work, crisper transients
9. **Glue Compressor** (bounce compressor): slow attack, fastest release, 2-3dB GR. Makes mix BOUNCE.
10. **Limiter**: ceiling at 0dB, no more than 6-7dB gain reduction
- Target loudness: -6 to -7 LUFS for club/download, -12 to -14 LUFS for Spotify
- Spotify hack: more dynamic range (quiet breaks → loud drops) = Spotify brings up average volume, making drops even louder
- **Reverb rules**: cut lows below 300Hz and highs above 4-6kHz on reverb sends. Plates for vocals, hall/vintage for synths.

---

## ARRANGEMENT & SONG STRUCTURE

### The 5 Elements of Tech House (from pro tutorials)
Every tech house track is built from exactly 5 categories:
1. **Drums**: kick, clap, hats, percussion
2. **Bass**: pluck bass + sub bass
3. **Mids**: synths, piano, organ, brass
4. **Vocals**: lead vocal, vocal chops, call-response hooks
5. **Effects**: sweeps, impacts, crashes, reverses, risers (ear candy for transitions)

### THE #1 ARRANGEMENT MINDSET: Think in 16-Bar Blocks (from Beatport Top 100 analysis)
Every section of a pro tech house track is 16 bars. Not 4, not 8 — **16 bars minimum**.
- Copying a 16-bar loop twice = ~1:30 of music
- Copying a 4-bar loop four times = 30 seconds that already sounds repetitive
- **Bigger blocks = faster arrangement, less repetition, more professional sound**

### The Club Banger Formula (from Beatport Top 100 analysis)
All successful tech house tracks use essentially the same structure:

| Section | Bars | Energy | Notes |
|---------|------|--------|-------|
| **Intro** | 16 | Low → Rising | Kick + hats, slowly introduce elements. Sets the tone. |
| **Simple Drop** | 16 | Medium | Kick + bass + drums. NOT the main theme yet. Simplified/minimal. |
| **Break + Build** | 16 | Dip → Rising | Remove low end (highpass). Introduce the main melody/vocal HERE. Build tension. |
| **Main Drop** | 16 | HIGH | Full energy. First 8 bars = simple drop. Second 8 bars = add extra elements (vocal, percussion, stabs). |
| **Break + Build** | 16 | Dip → Rising | Same formula. Can tease main melody variation. |
| **Main Drop + Climax** | 16-32 | HIGHEST | This is LONGER than the first main drop. The climax of the track. Add all layers, longest drop section. |
| **Outro** | 16 | Falling | Strip elements, energy goes down. Mirror of intro for DJ mixing. |

Total: ~5 to 5.5 minutes — perfect club length for 2024+.

### Key Arrangement Principles (from pro analysis)
1. **Simple drop BEFORE main drop**: after every break, start with a simplified drop (no clap, fewer elements) THEN add elements. Don't give everything at once.
2. **Tease the main melody early**: introduce a fragment of the main theme in the simple drop or break, but don't reveal the full melody until the main drop.
3. **The final drop is the longest**: the climax section at the end should be 16-32 bars — longer than any previous drop. This is where everything comes together.
4. **Variation comes from VOCALS, not new instruments**: the instrumental can stay almost identical across drops. Vocals create all the variation and interest.
5. **Transitions every 8-16 bars**: use filter sweeps, risers, fills, or downlifters at the end of each section to signal change.
6. **Energy is a roller coaster**: always alternate between UP and DOWN. Never stay flat. Add elements = energy up. Remove elements / filter = energy down. The contrast is what makes it interesting.
7. **You need very few elements**: kick, bass, groove (hats/perc), one main melody, and vocal. That's a complete track. Don't overthink it.

### Basic Song Structure: Cycles of Breaks → Drops
A full track is just: Intro → Simple Drop → Break/Build → Main Drop → Break/Build → Climax Drop → Outro

| Section    | Bars  | Elements                              |
|------------|-------|---------------------------------------|
| Intro      | 1-16  | Kick + hats, slowly introduce perc    |
| Simple Drop | 17-32 | Kick + bass + drums, simplified       |
| Break/Build | 33-48 | Remove low end, introduce hook/vocal, build tension |
| Main Drop  | 49-64 | Full energy: all elements, DRY and FORWARD |
| Break/Build | 65-80 | Strip again, bigger build this time    |
| Climax Drop | 81-112 | LONGEST drop, everything combined, highest energy |
| Outro      | 113-128 | Strip elements, end on kick + hats   |

### Break Structure (from Max Styler — 4 jobs of a break)
1. **Give them a break**: remove low end (highpass kick + bass) so people stop dancing
2. **Hit them with the main thing**: introduce the vocal hook or main melodic element
3. **Create atmosphere**: reverb, delay, pads, organ — push mix BACK in depth dimension
4. **Build tension**: leads into the build section

### Build Tension: Rep, Roll, Rise, Grow (from Max Styler)
Every build should use some combination of these four tools:

1. **Rep** (hook repetition): repeat a vocal phrase or hook to prime the listener
2. **Roll** (rhythmic acceleration):
   - Snare roll: broken pattern → 8th notes → 16th notes (accelerating density)
   - Kick roll: quarter notes → 8th notes
   - Crash roll: crashes hitting more frequently
3. **Rise** (feeling of going UP):
   - White noise risers (Operator noise osc + bandpass automating up)
   - Tonal risers (Serum LFO controlling coarse pitch up)
   - Opening low-pass filters on any element
   - Bass filter cutoff automating open
4. **Grow** (expanding the space):
   - Increase reverb/delay on vocals, drums, hooks
   - Push mix back in depth dimension
   - Automate send amounts up

### PIPO: Pattern Interrupt → Payoff → Explode (from Max Styler)
At the end of a build, right before the drop:
1. All building elements (risers, rolls) STOP suddenly (pattern interrupt)
2. Deliver the payoff moment (the main vocal phrase, the hook)
3. Brief silence or minimal moment
4. EXPLODE into the drop (dry, forward, full energy)

This contrast between building tension → sudden silence → explosive drop is what makes drops hit.

### Drop Dynamics: Utility Automation Trick (from "The Secret" tutorial)
Put a Utility on the master. Automate gain to -1 to -1.5dB during breakdown/build sections.
The drop then feels 1-2dB louder by contrast, making it hit much harder.
This is a standard trick used by Rusco, Fisher, and many others.

### Drop Arrangement: 5 Layers (from Max Styler)
Within each 16-bar drop, you have:
1. **Groove** (drums + bass) — always present
2. **Primary hook** (vocal chop or main vocal call-response) — always present
3. **Secondary hook** (organ, synth, or new element) — enters in 2nd 8 bars for lift
4. **Drum lift** (ride + bigger 909 hat) — enters in 2nd 8 bars
5. **Ear candy / PUNKS** — structured moments at key bar positions

### PUNKS: Structured Ear Candy (from Max Styler Masterclass)
PUNKS = Punctuation Points. Instead of random "ear candy," place exciting clusters at structural moments within each 8-bar phrase:

| Position | Importance | What Happens |
|----------|-----------|--------------|
| **P1** (bar 1) | Medium | Entry — first sound of the phrase |
| **P2** (bar 2) | Small | Minor moment — small fill, vocal glitch |
| **P4** (bar 4) | Large | Halfway marker — bass movement, vocal call, drum fill |
| **P6** (bar 6) | Small | Mirror of P2 — similar small moment |
| **P8** (bar 8) | Largest | End of phrase — biggest cluster: vocal, bass movement, highpass edit, fills, reverb bombs |

Rules for PUNKS:
- P4 and P8 are the MOST important — always fill these
- P2 and P6 are smaller echoes — keep them subtle
- Each punk is a CLUSTER of sounds (vocal + bass movement + drum fill + tom hit)
- The vocal hook is the primary driver of each punk
- End punks with a tom hit to punctuate
- P8 should prepare the transition into the next 8 bars (highpass, fill, crash)
- When there's no star vocal hook over the drop, PUNKS carry all the excitement

---

## Vocal Chop Workflow

### Setup (user does once)
1. User drags vocal file anywhere on disk
2. User tells you the file path, OR you know it from context

### Audio clip approach
1. `create_audio_track` — make a vocal track
2. `create_audio_clip` — load the vocal from absolute path
3. `set_clip_warp_mode` — Complex Pro (6) for vocals
4. `set_clip_start_marker` / `set_clip_end_marker` — isolate section

### Simpler-based Vocal Chops
1. Load vocal into Simpler on MIDI track
2. `set_simpler_playback_mode` (mode=2) — Slicing
3. `set_simpler_slicing_style`: 0=Transient, 1=Beat, 2=Region, 3=Manual
4. Write MIDI: C1 (36) = slice 1, C#1 (37) = slice 2, etc.

### Vocal Processing Chain (from Max Styler)
1. **iZotope Vocal Doubler** (free plugin): 65% for width — 90% of the vocal sound
2. **EQ**: boost 2kHz (magic vocal frequency, pushes vocal forward), cut 300Hz (low-mid mud), hard cut below 100Hz
3. **Multiband Compression**: tonal control — gently compress low (<120Hz), low-mid (120-650Hz), high (>650Hz) separately
4. **Progressive Dynamics**: first compressor with wide knee + infinite ratio (aggressive on peaks, gentle on quieter parts), then Glue Compressor (fast attack, fast release, ~5dB GR)
5. **Hard Clipper**: shave unruly peaks before limiters for predictable behavior
6. **Limiters** (2 stages, ~1dB each): inch vocal forward gently
7. **Saturator**: final half-dB of presence

### Vocal Arrangement Strategy
- **Breaks**: play the full vocal / main hook (people are listening, not dancing)
- **Drops**: use call-response structure:
  - CALL = unresolved phrase (e.g., "lick my..." — the tease)
  - RESPONSE = resolved phrase at end of 8 bars (what everyone wants to say)
  - The response IS the payoff — make people wait for it
- **Payoff moment** (right before drop): pull vocal back slightly (turn off final limiters/saturator) so the drop vocal hits harder by contrast
- **Lower vocal layer**: duplicate main vocal, pitch down -5 semitones, add auto-pan + chorus for movement

### Vocal FX Chain (send effects)
- **Reverb** (return): room reverb for drops, bigger reverb for breaks (grow the space)
- **Delay** (return): dotted 1/8 note delay for breaks/builds to create chaos and repetition

---

## SOUND QUALITY CONTROL LOOP (MANDATORY)

**NEVER present a sound to the user without first running the quality control loop.**

### Setup (once per session)
1. Create an audio track (e.g. "Bass Record") next to the MIDI track
2. Set input routing to receive from the MIDI track: `set_track_input_routing(track_index, "TrackName")`
3. Set monitoring to "in": `set_track_monitoring(track_index, monitoring="in")`
4. Arm the audio track: `set_track_arm(track_index, arm=true)`

### Record-Analyze-Compare Loop
1. **Fire** the MIDI clip: `fire_clip(track_index, clip_index)`
2. **Record**: Toggle session record ON, wait ~10s (one full loop), toggle OFF, stop playback
3. **Find the file**: `ls -lah "<session_path>/Samples/Recorded/" | grep "<track_name>"` — use the 2nd-newest WAV (newest is always 0 bytes)
4. **Analyze**: Run `bass_quality_check.py <recorded.wav> <reference.wav>`
5. **Compare metrics** against reference and fix issues:
   - Centroid/Bandwidth/Rolloff/ZCR = sound character (should be within 20%)
   - RMS/Peak = volume (should be within 30%)
   - Energy band distribution = frequency balance (informational only for stem comparisons — stem separation artifacts distort this)
6. **Repeat** until spectral metrics (centroid, bandwidth, rolloff, ZCR) all show "OK"

### Quality Check Script Location
`/Users/ryansavoia/Ableton ai music/bass_quality_check.py`
Usage: `python bass_quality_check.py <my_recording.wav> <reference.wav>`
Requires: librosa, numpy, scipy (installed in `.venv`)

### Key Learnings from Sound Design Iterations
- **Osc 2 at -1 octave** adds massive sub energy (~18Hz sine) that overwhelms bass harmonics. Use gain ≤0.5 or set to same octave.
- **Saturator (Bass Shaper type)** pushes energy into 250-1kHz range. Control with Dry/Wet and Drive.
- **EQ Eight** can shape frequency balance but cannot overcome physics: D1's fundamental (37Hz) will always be in the sub band.
- **Saw wave** provides harmonics at all integer multiples. Filter cutoff (LP Freq) controls how much upper harmonic content passes through.
- **Stem separation artifacts** make energy band distribution unreliable for exact matching. Focus on centroid/bandwidth/rolloff instead.
- **Volume is non-linear**: Small parameter changes across multiple gain stages compound. Adjust one stage at a time.

---

## PRODUCTION WORKFLOW (READ EVERY TIME)

**READ THESE FILES BEFORE EVERY SESSION:**
- `WORKFLOW.md` — the reference-driven multi-candidate workflow
- `preset-library.json` — curated, taste-validated preset library

### The #1 Rule: NEVER Generate a Single "Best Guess"
Always generate **4-6 candidates** in distinct archetypes. Human picks the winner.
Sound + pattern are ONE decision. Never separate them.

### Session Flow
1. Reference track(s) + section goal + target lane
2. Select 4-6 presets from library (prioritize validated ones)
3. Generate candidates in parallel clip slots (different preset + pattern per slot)
4. Fast audition: fire each clip, human picks top 1-2
5. Refine winners only — ONE change at a time, play after each
6. Lock winner, move to next element

### Anti-Patterns (NEVER DO THESE)
- Never iterate on a pattern the human called bad — generate fresh candidates
- Never explain theory instead of producing options
- Never tweak raw oscillators when presets exist
- Never spend >2 rounds on one element — change reference/lane instead
- Never separate sound selection from pattern writing

---

## CRITICAL RULES

### Session & Tools
1. **ALWAYS `get_session_info` first** before making any changes
2. **NEVER guess synth parameters** — read them with `get_device_parameters` first
3. **Check your work**: after programming, `get_clip_notes` to verify, then `fire_clip` to play

### Sound Selection
4. **ALWAYS use presets** from `preset-library.json`. NEVER build from raw oscillators (except pure sub sine).
5. **Select sounds IN CONTEXT** — always play drums while auditioning bass presets.

### Bass Rules
6. **Bass notes on BEATS and OFFBEATS ONLY** (8th note grid). NO 16th ghost notes unless rolling pattern with sidechain.
7. **4-8 notes per bar maximum.** More = mush.
8. **Bass needs SIDECHAIN on ALL layers.** This creates the bounce.
9. **Bass is THREE LAYERS**: Main (80-250Hz), Sub (16-60Hz), Texture (250Hz+).

### Mix Rules
10. **The kick is king**: kick at 0dB. Everything else serves the kick.
11. **Kick sub at or above -6dB** in spectrum. Bass fundamental -6 to -12dB.
12. **ALWAYS set up sidechain compression** on ALL bass layers from kick.
13. **Drops are DRY and FORWARD. Breaks are WET and PUSHED BACK.**

### Arrangement Rules
14. **Less is more**: groove and space over density.
15. **Use PUNKS** for structured ear candy at bar 2, 4, 6, 8 positions.
16. **PIPO before every drop**: pattern interrupt → payoff → explode.

### Production Rules
17. **Velocity variation on hats/perc** (60-120 range), NOT on bass/kick.
18. **Apply swing** on hats and percussion for groove.
