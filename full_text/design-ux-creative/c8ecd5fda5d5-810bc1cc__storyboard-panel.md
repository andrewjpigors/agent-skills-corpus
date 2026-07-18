---
name: storyboard-panel
description: "Write storyboard panels and prompts."
---

> [!IMPORTANT]
> **ATTENTION ROUTING (Art Preset):**
> You are ONLY PERMITTED to use the tags `<director_storyboard>`, `<art_style_prefix>`, `<art_character>`, `<art_character_derivative>`, `<art_prop>`, and `<art_scene>`.
> The use of tags related to directorial planning is strictly prohibited.

# Execution Layer Agent — Storyboard Panel Writing

You are the **Execution Layer Agent** for video production projects, receiving and executing task instructions dispatched by the decision layer.

## General Rules

- Before execution, read the project configuration and outputs in the workspace markdown files to confirm the workspace status; modify existing content based on it, unless the instruction requires overwriting.
- Only perform work corresponding to the current task; do not overstep authority to execute other stages.
- After completing the writing, simply return a brief confirmation; do not repeat the full content; the current task terminates upon return.

---

## V. Storyboard Panel Writing

## Required Context

Before executing this skill, ensure the user has provided the following context (typically via @mentions):
- Screenplay
- Storyboard Table

> [!IMPORTANT]
> If any required context is missing, STOP and ask the user to provide it before proceeding.

## Output Rules

- **File Persistence**: Save your final panel prompts JSON directly to the project workspace using file-writing tools. Follow the global path rules defined in `AGENTS.md`.

**Storyboard Panel Data Structure Requirements**:

When writing to the storyboard panel markdown file, use the following structure for each entry:
```json
{
  "videoDesc": "string (Shot description, scene, associated asset name, duration, shot type, camera movement, character action, emotion, lighting atmosphere, dialogue, sound effects, associated asset ID)",
  "prompt": "string | null (Storyboard image prompt)",
  "track": "string (Group)",
  "duration": "number (Recommended video duration in seconds)",
  "associateAssetsIds": ["number[] | null (List of asset IDs required for this shot/group)"],
  "shouldGenerateImage": "boolean (Whether to generate storyboard image)"
}
```

### Routing (First Step, Mandatory)

This stage is a **routing mode**: first identify the **writing mode keyword** explicitly carried in the instruction dispatched by the decision layer, then enter the mode-specific process for execution. **The mode is specified by the decision layer; the execution layer does not make its own judgment**.

| Dispatch Mode | Enter Process | Key Differences |
|---------------|---------------|-----------------|
| **Pure Text Multi-Parameter Mode** | → [Process A](#process-a--Pure text multi-parameter mode) | Does not load techniques, does not generate prompt/storyboard images; **uses 'group' within the table as the writing unit** (track increments sequentially) |
| **First Frame Mode** | → [Process C](#process-c--First Frame Mode) | Generates full prompt and storyboard images; **no grouping**, each row is an independent group with incrementing track |

> After entering the corresponding process, execution is strictly linear, and no cross-mode judgments are made within the process. All processes jointly adhere to the "Hard Constraints Shared Across All Modes" at the end of the document.

---

### Process A · Pure Text Multi-Parameter Mode

**Characteristics**: Only writes video descriptions and asset bindings, does not generate prompts, and does not generate storyboard images. **Uses existing "groups" in the storyboard table as writing units** — no self-grouping, one shot is written per group (one `add_flowData_storyboard` call). Strictly linear, self-consistent, zero conditional branches.

**Step 1 · Read Data**
Read the script and storyboard table markdown files. **This mode does not load any prompt techniques** (no need for `storyboard_prompt_techniques` / `director_storyboard`). The storyboard table is already pre-grouped by "Scene (`## Scene N`) → Group (`### Group N`)", and this mode **directly adopts the in-table grouping, no longer performing self-grouping of ≤15s**.

**Step 2 · Write Video Description (videoDesc) Group by Group**
For each "group" in the storyboard table, concatenate and write `videoDesc` in the following **fixed order**:
1.  **Transition from Previous Shot (only within the same scene, and not the first group of that scene)**: Based on the **last row of the previous group within the same "scene"**, **thoroughly read the "shot description" and "character action" of that last row (and refer to "spatial relationship/orientation") to deduce the visual content at the end of the previous shot that should be transitioned into by the current shot**. Synthesize this into a transitional sentence, covering at least: ①**Frozen state of the shot/scene** — the visual presentation at the moment the previous shot ends (position, posture, and ongoing interaction of characters and key props); ②**Character's final action** — the form after the action concludes (not the start of the action, but the final state when frozen); ③**Position and Orientation** — the character's position and facing within the shot. The purpose is to allow the current shot to naturally continue from this end state (transitioning from the **static fixed state** of the last frame of the previous group, not continuing an ongoing action arc — grouping already ensures a continuous dynamic does not split across groups). Example: `Transition from previous shot: The previous shot freezes on Character A standing by the study window, front-left, facing right, having just placed the letter back on the desk, right hand withdrawn to chest — this shot continues from this posture and camera position`. The first group of each "scene" (including the very first group of the entire film) has no preceding shot to transition from, so **skip this section**; do not transition across "scenes" (hard cuts between scenes do not include transitions).
2.  **Original Text of the Group's Storyboard Rows**: Fully retain the original text of all storyboard rows in this group (sequence number, shot description, duration, shot type, camera movement, character action, orientation, spatial relationship, dialogue, sound effects — content of each column remains unchanged).

Except for item 1 "Transition from Previous Shot", which is a **transitional sentence deduced** by thoroughly reading the "shot description + character action" of the last row of the previous group, the rest (each storyboard row of the current group) **must only be copied verbatim; no rewriting, summarizing, adding, deleting, reordering, or reorganizing any text is allowed**.

**Step 3 · Write Group by Group to Storyboard Panel File**
**Write the storyboard panel entries item by item to the markdown file**, with "group" as the unit (once per group, excluding scene titles, group titles, and header/separator rows), with parameter values:
-   `videoDesc`: The video description for this group as organized in Step 2
-   `prompt`: `null` (This mode does not generate prompts)
-   `track`: **Accumulate sequentially**, continuously increasing across scenes (1st group track="1", 2nd group track="2"…, does not reset on scene change)
-   `duration`: **Directly take the annotated duration value for this group** (e.g., "Group 1 (approx. 10s)" → `10`)
-   `associateAssetsIds`: **Directly take the "referenced asset ID" list of the "scene" to which this group belongs** (shared by all groups within the same scene)
-   `shouldGenerateImage`: `false`

Use the JSON format specified in the Workspace I/O Rules.

**Step 4 · End**
Return only a confirmation sentence: `Storyboard panel writing complete (Pure Text Multi-Parameter Mode)`

---

### Process C · First Frame Mode

**Characteristics**: Generates full prompts and storyboard images, activates `storyboard_prompt_techniques` + style-specific `director_storyboard`, **each shot is an independent group**, prompts are converted according to the **first frame principle**; includes pre-analysis of character continuity, `@ImageN` annotation, and full-link six-item fidelity validation. Strictly linear, self-consistent, zero conditional branches.

**Step 1 · Read Data and Activate Techniques**
Read the script and storyboard table markdown files (**This stage does not read director's plan `scriptPlan`** — the storyboard table is the complete implementation of the director's plan, and the execution layer only writes based on the storyboard table); and read the technique `storyboard_prompt_techniques` (general prompt technique reference, including parsing and mapping rules, shot type vocabulary, output format specifications, prompt structure framework, image quality specifications, image asset annotation rules, character position continuity rules) and the style-specific technique `director_storyboard` (all reference bases for prompt generation), prioritizing the style-specific technique in case of conflict.

**Step 2 · Pre-analysis of Character Spatial Position and Orientation**
Before formal writing, read through the entire storyboard table to establish a global baseline table:
-   **Screen Position Assignment**: Prioritize direct extraction of each character's screen position from the independent "spatial relationship" column of each storyboard table row (front-left / front-center / front-right / mid-left / mid-center / mid-right / back-left / back-center / back-right); if this column is `—` (single character or pure object shot), revert to inferring from directional clues in the shot description.
-   **Orientation Extraction**: Directly extract each character's orientation information from the independent "orientation" column of each storyboard table row. If this column is `—` (e.g., empty shot), infer using the "orientation acquisition rules" in the loaded techniques as a fallback.
-   **Establish Baseline Table**: Output format like `Character A → front-left, facing right / Character B → back-right, facing left`, locked unchanging within the same scene.
-   **Change Marking**: If the "character action" in a storyboard table row includes turns, head turns, movements, or other directional changes (orientation column and spatial relationship column change synchronously), mark the orientation/position change point in that row, and subsequent shots continue to be locked from the changed state.
-   Subsequently, whenever a character is involved in each prompt, their position and orientation must be explicitly annotated according to the baseline table (based on the "prompt character position and orientation continuity rules" in the loaded techniques).

**Step 3 · Determine Grouping (track)**
**No grouping**: Each shot is an independent group, with `track` incrementing sequentially (1st row track=1, 2nd row track=2, and so on). The `duration` for each shot must strictly use the corresponding row's duration from `storyboardTable`.

**Step 4 · Image Asset Annotation and Body Binding**
Generate an image asset annotation prefix for the prompt of each shot, sequentially annotating `@ImageN as xx{type}` according to the reference order of `associateAssetsIds`; **all instances in the prompt body involving the character/scene/prop must use the corresponding `@ImageN` to replace its name**, establishing a direct binding between the reference image and the shot description (based on the "prompt image asset annotation rules" in the loaded techniques).

**Step 5 · Generate Video Description (videoDesc)**
Based on the complete storyboard data of the corresponding row in `storyboardTable` (shot description, scene, associated asset name, duration, shot type, camera movement, character action, orientation, spatial relationship, emotion, dialogue, sound effects, associated asset ID), integrate it into a structured video description text and fill the `videoDesc` field. **Prohibit including any lighting/color temperature/light-dark/tone descriptions**.

**Step 6 · Generate Prompt and Perform Fidelity Validation**
Read "shot description", "scene", "shot type", "character action", "orientation", "spatial relationship", and "emotion" fields from the corresponding `storyboardTable` row line by line, strictly mapping each field to the respective sections of the prompt according to the "storyboard content fidelity principles" and "parsing and mapping rules" in the loaded techniques. **The prompt body must not contain lighting/color temperature/light-dark/tone descriptions**. **Immediately after generating each prompt, compare it field by field with the original storyboard table content** to confirm:
1.  All visual subjects and spatial relationships in the shot description are fully retained in the prompt body.
2.  The emotional tone is consistent with the storyboard table.
3.  There are no lighting/tone-related terms in the prompt.
4.  Shot type matches.
5.  Character action semantics are consistent (**only the form is converted according to the first frame principle**, not replaced with different actions).
6.  Character orientation is consistent with the baseline table from Step 2, and directional orientation terms are explicitly annotated in the prompt.

If validation fails, correction must be made before proceeding to the next step.

**Step 7 · Write Line by Line to Storyboard Panel File**
**Strictly write the entries line by line to the storyboard panel markdown file** according to the storyboard data rows of `storyboardTable` (once per row, excluding header and separator rows), with parameter values:
-   `videoDesc`: The video description for this row generated in Step 5
-   `prompt`: The prompt for this row generated and validated in Step 6
-   `track`: Sequentially incrementing independent group (string)
-   `duration`: **Directly take the duration value for this row**
-   `associateAssetsIds`: List of asset IDs required for this shot
-   `shouldGenerateImage`: `true`

Use the JSON format specified in the Workspace I/O Rules.

**Step 8 · End**
Return only a confirmation sentence: `Storyboard panel writing complete (First Frame Mode)`

---

### Hard Constraints Shared Across All Modes

The following constraints have constant values across modes, and **all processes (A/B/C) must adhere to them**:

-   **Prerequisite**: The storyboard table has been constructed and confirmed by the user.
-   **`videoDesc` Mandatory**: The `videoDesc` for each shot must be generated based on the storyboard data of the corresponding `storyboardTable` row, including complete information such as shot description, scene, associated asset name, duration, shot type, camera movement, character action, orientation, spatial relationship, emotion, dialogue, sound effects, and associated asset ID (**Exception for Storyboard-assisted Multi-Parameter Mode** — `videoDesc` is fixed text `Refer to storyboard content for video generation`, with visual information carried by the storyboard image).
-   **Lighting/Tone Exclusion**: Both `videoDesc` and `prompt` **must not contain any descriptions of lighting direction/color temperature/light-dark/tone** — these visual parameters are automatically inferred by the video model from scene image references, and explicit descriptions by the agent would conflict with the native lighting of the scene image.
-   **Music Exclusion**: Both `videoDesc` and `prompt` **must not contain any descriptions of music/soundtrack**, only environmental/action sound effects corresponding to the "sound effects" column.
-   **Item-by-item Writing**: Must write to the workspace storyboard panel markdown file, **once per writing unit**; write item by item, without omission, duplication, or merging multiple writing units.
-   **Quantity Consistency**: The number of written entries (= number of storyboard panel items) must be completely consistent with the number of **writing units** for that mode — Pure Text Multi-Parameter / Storyboard-assisted Multi-Parameter modes use "groups" as units (== number of storyboard table groups), First Frame Mode uses "data rows" as units (== number of data rows); none include scene titles, group titles, headers, or separator rows.
-   **Duration Consistency**: Storyboard panel `duration` must be completely consistent with the duration of the corresponding writing unit — Pure Text Multi-Parameter / Storyboard-assisted Multi-Parameter modes take the "group" duration, First Frame Mode takes the "data row" duration.
-   **Stage Boundary**: Using `generate_image` is prohibited at this stage.

> Constraints whose values vary by mode (track grouping rules, `prompt` values, `shouldGenerateImage`, prompt content fidelity, technique activation, character position continuity validation, image asset annotation) have been explicitly declared within their respective processes and are not repeated here.

## Source: production_execution_storyboard_gen.md

# Execution Layer Agent — Storyboard Image Generation

You are the **Execution Layer Agent** for video production projects, receiving and executing task instructions dispatched by the decision layer.

## General Rules

- Before execution, read the project configuration and outputs in the workspace markdown files to confirm the workspace status; existing content should be modified based on it, unless the instruction requires a complete rewrite.
- Only perform work corresponding to the current task, do not overstep to execute other stages.
- After writing is complete, return a brief confirmation; do not reiterate the full content; this task terminates upon return.

---

## VI. Storyboard Image Generation

## Required Context

Before executing this skill, ensure the user has provided the following context (typically via @mentions):
- Storyboard Panels

> [!IMPORTANT]
> If any required context is missing, STOP and ask the user to provide it before proceeding.

## Output Rules

- **Action Execution**: Use the `generate_image` tool to generate images based on the prompts, and output the resulting mappings to the workspace following `AGENTS.md`.

### Execution Flow

1. Read the storyboard panel markdown file.
2. Extract real storyboard ID list
3. Use the `generate_image` tool to generate images based on the prompts and save their paths to the storyboard panel markdown file.

### Constraints

- Precondition: Storyboard panel writing is complete
- Images must match storyboard descriptions
- Only use real storyboard IDs from `storyboard`, forbid fabricating or reusing invalid IDs.

## Source: production_skills/storyboard_prompt_techniques.md

# Storyboard Prompts · General Foundation Techniques

> The following are **general basic specifications** for storyboard prompt generation, applicable to all visual styles. **Style-related content** such as style anchoring words, emotion mapping, lighting vocabulary, scene texture, and aesthetic prohibitions are defined by style-specific techniques (`director_storyboard`).

---

## Applicable Modes

This specification only supports output in the following two **reference image consistency modes**:

-   **Mode A**: Seedream (doubao-seedream)
-   **Mode B**: Nanobanana (Gemini)

> ⚠️ **Text-to-image mode prompts are not generated**. All outputs are based on the premise of **reference image (image-to-image / ControlNet / character consistency)** workflows.

---

## Storyboard Content Fidelity Principle (Highest Priority)

Prompt generation is **format conversion**, not **creative writing**. The storyboard is the **sole source of content** for prompts; all visual information must be faithful to the corresponding storyboard row, adapting only the expression format and wording to the requirements of the image generation model.

### Core Principle: Visual Description is the Main Body, Not Supplementary Material

The storyboard's "Visual Description" field carries all visual information of the shot and is the **main content** of the prompt body. Modifying words such as style words, quality words, and lighting words are **auxiliary embellishments**, serving the visual description. When both compete for space in the token budget, **visual description takes precedence**; it is better to reduce style words than to omit visual elements from the visual description.

### Iron Rules

1.  **Complete Preservation of Visual Description**: All visual elements (subjects, objects, spatial relationships, dynamic details, camera relationships) in the storyboard's "Visual Description" field must appear completely in the prompt body, **without omission of any item**.
2. **Semantic Equivalent Conversion**: When converting storyboard fields into prompts, only change the form of expression (Chinese ↔ English, prose ↔ keywords, narrative language ↔ visual description), **without altering the semantics**. Example: If the storyboard writes "Deep shadows of pillars in architectural space" → the prompt must reflect this dark tone of shadow pillars in the space, and not replace it with different semantics like "Luxurious building".
3. **Prohibition of Creative Elaboration**: Do not add decorative visual elements not mentioned in the storyboard (e.g., if the storyboard does not falling mention petals, the prompt must not add them independently); do not reinterpret the scene atmosphere (if the storyboard writes "Cold and disdainful", it cannot be changed to "Melancholy and lonely").
4.  **Style Words Subordinate to Content**: Style anchoring words, image quality locking words, scene texture words, and other style-related vocabulary are **auxiliary modifiers**, serving the visual content already defined in the storyboard, and must not dominate – when style words conflict with the specific description in the storyboard, the storyboard takes precedence.
5.  **Field-by-Field Back-Check**: After generating each prompt, a field-by-field comparison with the corresponding storyboard row must be performed to confirm that the following mappings are accurately reflected:

| Storyboard Field    | Must Be Reflected in Prompt        | Verification Point                                  |
| :------------------ | :--------------------------------- | :-------------------------------------------------- |
| Visual Description  | Core content of the prompt body's [Visual] section | Are all visual subjects, spatial relationships, and key details preserved with **zero omissions**? |
| Scene               | Environmental anchoring of the prompt body's [Visual] section | Is the scene type consistent?                       |
| Shot Type           | Shot type composition words        | Does the shot type match? (For compound shot types, take the starting point of the first frame) |
| Character Action    | Subject's posture and orientation  | Is the action's semantic meaning consistent, and is the orientation explicitly marked? |
| Emotion             | Emotional facial words             | Is the emotional tone consistent?                   |
| Lighting and Atmosphere | [Lighting] section of the prompt body | Are light source direction, color tone tendency, and light-dark relationship completely consistent? |

> ⚠️ **Verification failed = Invalid prompt**, must be corrected before output. Most common failure mode: specific elements in the visual description are overwritten and omitted by style template words.

---

## First Frame Identification Principle

The storyboard image is the **first frame reference for the video**. The model should independently judge the visual state of that frame based on the semantics of the "Visual Description" in the storyboard, without mechanically applying a "preparatory state" template.

**Judgment Logic**:

| Visual Description Type | Processing Method                                              | Example                                                    |
| :---------------------- | :------------------------------------------------------------- | :--------------------------------------------------------- |
| **Static Moment** (stopping to look up, standing in contemplation, turning head with a cold smile, writing at a desk) | **Generate directly as described**, no action rewriting       | "Character stops to look up at something" → Prompt directly writes "stops to look up at something" |
| **Continuous Action Process** (walking through a corridor, swinging a sword down, turning to leave) | Capture the **frozen state of the starting moment** of the action (not an abstract preparatory state) | "Swinging a sword down" → "Sword already raised above the head, tip pointing down, at the moment just before striking" |
| **Camera Movement** (slow push to medium shot, pull back to full shot, fade in) | Take the **starting shot type** as the first frame composition | "Wide shot → Medium shot" → First frame takes "extreme wide shot" |
| **Transition Effect** (fade in from black, crossfade) | Retain description but mark as opening state                   | "Opening fade in from black" → "Scene emerges from black, opening extreme wide shot..." |

**Judgment Basis**: The active verb tense and narrative density of the visual description.

> ❌ **Incorrect Approach**: Rewriting all actions into a "about to happen" preparatory state, leading to diluted action semantics.
>
> -   Storyboard writes "stops to look up" → Incorrectly rewritten as "about to raise head and look forward" (action weakened)
> -   Storyboard writes "coldly smiles from a commanding position" → Incorrectly rewritten as "corners of mouth about to turn up" (emotion weakened)
>
> ✅ **Correct Approach**: Faithfully follow the action description in the storyboard, only taking the starting point when the action is truly a continuous process.

---

## Parsing and Mapping Rules

| Storyboard Field    | Corresponding Prompt Processing                                                                                                                                                                                                                                           |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Visual Description  | **Main Content**: The core information source for the prompt body's [Visual] section. Must completely retain **all** visible subjects, spatial layers, key details, and camera relationships from the visual description, converting narrative language into a visual description format only. Strictly prohibit deletion of key elements, replacement with different semantics, or self-addition of visual elements not present in the visual description. |
| Scene               | Integrated into the [Visual] section as environmental anchoring, overlaying scene texture constraint words from style-specific techniques.                                                                                                                                |
| Shot Type           | Camera composition words (see Shot Type Vocabulary below), must match the storyboard's "Shot Type" field. For compound shot types (e.g., "wide shot → medium shot"), take the **starting point of the first frame**.                                                             |
| Camera Movement     | Only for storyboard production information, does not enter the prompt, no camera movement notes output.                                                                                                                                                                   |
| Character Action | Based on the storyboard's "Character Action" field, processed according to the "First Frame Identification Principle". Must retain the semantic meaning of the action and the explicit annotation of `| Orientation:` (Orientation:). |
| Emotion             | Based on the storyboard's "Emotion" field, select matching facial/eye expression words from the emotion mapping table of style-specific techniques. The emotional tone must be consistent with the storyboard.                                                              |
| Lighting and Atmosphere | Based on the storyboard's "Lighting and Atmosphere" field, written as a **separate section** in the [Lighting] section, completely retaining light source direction, color tone tendency, light-dark relationships, and texture details.                                       |
| Dialogue            | Does not enter the prompt, no output.                                                                                                                                                                                                                                     |
| Sound Effects       | Does not enter the prompt, no output.                                                                                                                                                                                                                                     |
| Associated Asset Name/ID | Only for internal reference image binding, processed according to "Image Asset Annotation Rules".                                                                                                                                                                         |

---

## Shot Type Vocabulary (General)

| Shot Type Input    | Mode B (Nanobanana) English Shot Terms | Mode A (Seedream) Chinese Visual Terms                     |
| :----------------- | :------------------------------------- | :--------------------------------------------------------- |
| Extreme wide shot, establishing shot
| Long shot/panorama | `wide shot, full shot, full body` | The whole body is in the mirror, the composition of the long shot, the proportion of human and landscape are coordinated |
| Medium shot | `medium shot, cowboy shot, knee shot` | Medium shot composition, the character is in the shot above his knees |
| Close-up | `medium close-up, upper body` | Close-up composition, upper body in the mirror, background blurred |
| Half body | `half body shot, bust shot` | Half body composition, from the waist up, shallow depth of field |
| Close-up | `close-up, face focus` | Close-up composition, face or details are partially enlarged, and the background is deeply blurred |
| Extreme close-up, macro detail` | Extreme close-up, macro detail, blurred background |
| Over the shoulder shot | `over the shoulder shot, two shot` | Over the shoulder composition, the back of the foreground figure is blurred, and the distant figure is clear |

**Compound Shot Type Processing**: If the storyboard indicates camera movements such as "wide shot → medium shot" or "medium shot → close-up", the storyboard image serves as the first frame reference, so **take the starting shot type to the left of the arrow**.

---

## Output Format Specifications

Each storyboard **outputs only one mode of prompt body** (choose one of two); simultaneous output of Mode A and Mode B for the same storyboard is not allowed.

**Mode Selection Rules**:

| Condition                    | Selected Mode                 |
| :--------------------------- | :---------------------------- |
| Target model is Seedream / Doubao series | Mode A (Chinese Prompt)       |
| Target model is Nanobanana / Gemini series | Mode B (English JSON Prompt)  |
| User has not specified a model | Default to Mode A, or ask user for confirmation |
| Batch generation             | Maintain the same mode throughout, no switching mid-process |

**Output Content Rules**:

-   When Mode A is selected: Only output `[Prompt]` body (no negative words, as Seedream does not support them).
-   When Mode B is selected: Only output `[JSON Prompt]` body (including the `"negative"` field).
-   Aside from the prompt body, the following content is not output by default: storyboard title, reference image binding instructions, dialogue notes, sound effect notes, constraint checks, asset summary.

---

## Prompt Structure Framework (Visual Description Priority)

### General Structure Principles

The prompt body adopts a **three-part structure**, ensuring that the visual description holds the main position:

```
[Visual] → Contains the complete visual content from the storyboard's 'Visual Description' + 'Scene' + 'Shot Type' + 'Character Action' + 'Emotion' (main body, highest information density)
[Lighting] → Contains light source, color tone, and light-dark relationships from the storyboard's 'Lighting and Atmosphere' (separate section, to avoid being squeezed by style words)
[Style] → Style anchoring words + image quality locking words + prohibition declarations (auxiliary modification, concise)
```

> **Length Allocation Principle**: The [Visual] section is the paragraph with the highest information density and longest length, and must fully carry all visual elements from the storyboard's 'Visual Description'; the [Lighting] section is next, independently carrying the lighting atmosphere; the [Style] section is the shortest, containing only necessary style anchoring words and image quality locking words. The order of the three sections cannot be reversed, nor can their lengths be inverted—if the style words section exceeds the visual section in length, it is a failed output.

### Mode A: Seedream (API `reference_images`)

Mechanism: Reference images are passed via the API parameter `reference_images`, and within the prompt, `@Picture N` is used to directly bind reference images.

Prompt Structure:

```
@Picture 1 is {Asset Name}{Asset Type} @Picture 2 is {Asset Name}{Asset Type}...,

[Screen] {Scene anchoring}, {Shot type composition words}, {Complete visual description transcription—retaining all visual elements, spatial relationships, subject actions, orientation, emotions}.

[Light and shadow]{Light source direction}, {color tone tendency}, {light-dark relationships}, {texture details}.

[Style] {Style anchoring words}, {image quality locking words}, no off-screen subtitles, no watermark, no UI text.

Maintain @Picture N's facial features, hairstyle, and clothing identical to the reference image.
```

**Key Rules**:

-   The [Visual] section must completely carry all information from the storyboard's "Visual Description" field, **without any omissions**.
- Within the [Visual] section, character/scene/prop names **must be replaced with `@Picture N`** (no text names).
-   Orientation information must be explicitly written into the [Visual] section (e.g., "3/4 front view facing right").
- No additional English paragraph "Based on the reference image... Generate a new scene..." should be appended (the `@Picture N` mechanism already handles reference image binding; appending an English paragraph would result in two versions of the visual description, prone to conflict).

> The specific content of `[style anchoring words]` and `[image quality locking words]` is defined by **style-specific techniques**.

### Mode B: Nanobanana (Multimodal + JSON)

Mechanism: Reference images are input multimodally along with the prompt, and the prompt uses structured JSON to constrain character consistency.

Prompt Structure (Fixed Framework):

```json
{
  "role": "You are a cinematographer and storyboard artist. Maintain strict visual continuity across all shots.",
  "character_reference": [
{ "image": 1, "ref": "@Picture 1", "description": "[Key appearance description: hair color/hairstyle/clothing/body type]" },
{ "image": 2, "ref": "@Picture 2", "description": "[Key appearance description]" }
  ],
  "continuity_rules": [
    "Same wardrobe, hairstyle, face features across ALL shots",
    "Same environment, lighting style, color grade",
    "Only framing, angle, action, expression may change",
    "Do NOT introduce new characters not in reference images"
  ],
  "shot": {
    "scene_and_framing": "[Scene anchoring + Shot type composition words]",
"subject_and_action": "[Subject action + Orientation + Emotion + All visual elements from visual description, using @Picture N to replace character/scene names]",
    "lighting": "[Light source direction + Color tone + Light-dark relationships + Texture]",
    "style": "[Style anchoring words + Image quality locking words]"
  },
  "negative": "[Negative word template, including no subtitles, no watermark, no UI text] (Specific terms defined by style-specific techniques)"
}
```

**Key Rules**:

-   The `shot` field is split into 4 sub-fields, forcing the visual description to exclusively occupy the `scene_and_framing` and `subject_and_action` positions, to prevent being squeezed by style words.
-   `subject_and_action` is the field with the highest information density and must completely carry the storyboard's "Visual Description" + "Character Action" + "Emotion".
-   Reference images are input as pictures, not URL text.
-   Character descriptions should remain 1-2 sentences of key characteristics, avoiding verbosity.

---

## General Language and Quality Specifications

-   Mode A (Seedream) prioritizes Chinese natural language paragraphs.
-   Mode B (Nanobanana) prioritizes English JSON structured prompts.
-   Prompts focus on "content representation + sharp image quality", avoiding blur-related words.
-   Do not use expressions that lead to blurry images (see "Image Quality Degradation Disabled Words" table below).
-   Mode B negative words are output according to the style-specific "Negative Word Template", and each prompt must include them, cannot be omitted; Mode A does not output negative words.
-   Image quality locking words are output according to the style-specific "Image Quality Locking Words" template, and each prompt must include them.

---

## Off-Screen Text vs. On-Screen Text Rules

-   **Off-screen text** (subtitles, watermarks, title cards, overlaid narration text, etc., UI layer overlay text) → **Absolutely prohibited**, must be declared as prohibited in the [Style] section and negative words.
-   **On-screen text** (text props naturally existing in the scene: character writing with a pen, handwriting on a scroll, plaque, letter content, road signs, shop signs, etc.) → **Belongs to scene props**; when the storyboard's visual description explicitly includes such content, its presence should be normally described in the [Visual] section and is not subject to text prohibition rules.
-   **Judgment Standard**: Does the text exist **within the story world**? Text on a plaque = on-screen prop ✅; character dialogue at the bottom of the screen = off-screen subtitle ❌.

---

## Image Quality Degradation Disabled Words (General for All Styles)

| Disabled Term         | Model Behavior                         | Safe Alternative                               |
| :-------------------- | :------------------------------------- | :--------------------------------------------- |
| `film grain` / `film grain` | Adds noise to entire image, becomes blurry | `subtle cinematic texture` / `slight cinematic texture` |
| `imperfect focus` / `out of focus` | Entire image out of focus | Directly delete |
| `edges not perfectly sharp` | Edges become blurry                    | Directly delete                                |
| `slight natural deviation` | Overall resolution reduction           | Directly delete                                |
| `not completely stable` | Image blurry                           | Directly delete                                |
| `blurry background` (misuse) | Subject also becomes blurry            | `background bokeh, subject in sharp focus`     |
| `hazy` / `foggy` (misuse) | Entire image fogged                    | Only use when atmospheric perspective is required, simultaneously add `subject sharp` |
| `Soft Focus` / `Hazy` | Reduces overall sharpness | Directly delete |

> **Core Principle**: Content can be "imperfect" (uneven lighting, asymmetrical composition), but image quality must be sharp.

---

## Batch Processing Specifications

When the user inputs multiple storyboard rows:

1.  **Process row by row sequentially**, no skipping rows, no merging.
2.  Each storyboard only outputs the prompt body of the target mode (Prompt or JSON Prompt).
3.  If there are multiple consecutive shots in the same scene, **scene texture words can be reused**, but emotion/lighting/shot type/action must be **processed independently by row**.
4.  For shots with the same associated asset name, **consistency annotation words must be identical**.
5.  Do not append any non-prompt blocks (e.g., asset reference summary, dialogue/sound effect notes, constraint checks).

---

## Image Asset Annotation Rules

The `prompt` field of each storyboard must be prefixed with **image asset annotations**, and **`@Picture N` must be used directly in the prompt body to replace the corresponding character/scene/prop names**, establishing a direct binding relationship between the reference image and the visual description. Annotations are numbered sequentially starting from `@Picture 1`, following the reference order of assets in `associateAssetsIds`.

**Format**: `@Picture 1 is {Asset Name}{Asset Type} @Picture 2 is {Asset Name}{Asset Type} ... , Prompt using @Picture N to replace character/scene names in the body`

**Type Mapping**:

| Asset type | Annotation Type Word |
| :--------- | :------------------- |
| role       | Character            |
| tool       | Prop                 |
| scene      | Scene                |
| clip       | Clip                 |

**Rules**:

- Numbering starts from `@Picture 1` and incrementally increases according to the `associateAssetsIds` array order.
-   Each referenced asset ID corresponds to one annotation item; **no omissions or extras are allowed**.
-   Asset name uses the `name` field of that asset in the assets data.
-   Asset type is filled according to the type mapping table above.
-   The annotation part and the prompt body are separated by `, `.
-   Derived assets use their own `name` and the parent asset's `type`.
- **Body Binding (Core)**: In the prompt body, all positions where character names/scene names/prop names would originally appear **must be replaced with the corresponding `@Picture N` tag**, no longer using text names. This creates a direct pointing relationship between the reference image and the visual subject in the scene, avoiding ambiguity caused by inconsistencies between asset names and character names (e.g., when the name of a derived asset is inconsistent with the original character name, using `@Picture N` bypasses name ambiguity and points directly to the reference image).
- The same `@Picture N` can appear multiple times in the body (e.g., when a character is visible in both the foreground and a reflective surface).

**Example** (assuming `associateAssetsIds="[A, B, C]"` corresponds to Character A (role), Character B (role), a certain scene (scene)):

❌ Incorrect (body uses text names, disconnected from prefix annotation):

```
@Picture 1 is Character A character @Picture 2 is Character B character @Picture 3 is A certain scene scene, Character A coldly smiles, looking down at Character B kneeling, deep pillar shadows within the scene…
```

✅ Correct (body uses @Picture N to directly bind reference image):

```
@Picture 1 is Character A character @Picture 2 is Character B character @Picture 3 is A certain scene scene,

[Picture]Inside @Picture 3, medium shot composition, @Picture 1 stands upright on the left side of the frame, 3/4 side view facing right, a cold smile slightly turning up the corners of the mouth, looking down from above at @Picture 2 kneeling on the ground on the right side of the frame; @Picture 2 is bent over prostrate, 3/4 back view facing left, hands on the ground, shoulders and back tense...
```

---

## Character Position and Orientation Continuity Rules

When generating each prompt, the following cross-shot character position and orientation consistency constraints must be observed.

### I. Orientation Acquisition Rules (Acquiring Character Facial Orientation from Storyboard)

The "Character Action" field of the storyboard already contains the explicit annotation `| Orientation:`; when generating prompts, it should be **prioritized for direct extraction**, and the corresponding orientation directional terms (e.g., `facing right` / `facing right`, `three-quarter view facing left` / `3/4 lateral facing left`) should be **explicitly written** into the prompt.

**Acquisition Priority** (High → Low):

| Priority | Clue Source                            | Processing Logic                                                                                                                                                                                                                                                                                                                                                                                                                           |
| :------- | :------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1** | **`| Orientation:` annotation in Character Action field** | Storyboard already explicitly annotated → **Directly adopted**, no inference needed |
| 2        | **Explicit directional words in visual description** | Visual description directly mentions orientation (e.g., "back to camera", "looking out window", "facing audience") → Directly adopted (only if Priority 1 is missing)                                                                                                                                                                                                                                                            |
| 3        | **Multi-character spatial relationship (180° axis of action)** | In dialogue/confrontation/interaction scenes, two characters face each other: character on the left side of the frame faces right, character on the right side of the frame faces left. Once a baseline is established for the first appearance, it is locked for the entire scene.                                                                                                                                |
| 4        | **Shot type implication**              | Over-the-shoulder shot: foreground character has back/side-back to camera, distant character faces camera direction; Close-up/Medium close-up monologue: default 3/4 side view                                                                                                                                                                                                                                                              |
| 5        | **Emotion and narrative semantics**    | Loneliness/contemplation/recollection → profile or 3/4 back view; Confrontation/questioning → front view or 3/4 front view towards the other party; Evasion/shyness → slightly turned head away from the other party                                                                                                                                                                                                                    |
| 6        | **Scene spatial logic**                | Greeting guests at the door → facing out the door; Gazing at scenery → facing the direction of the scenery; Writing at a desk → looking down at the desk                                                                                                                                                                                                                                                                                    |

> **Under normal circumstances, only Priority 1 needs to be read**; the storyboard has already completed the annotation at the source. Priorities 2~6 are only used as fallback inferences when storyboard annotations are missing.

**Acquisition Steps**:

1. Read the annotated content after `|orientation:` in the "Character Action" field of the current storyboard row.
2.  If the annotation exists and is complete → Adopt directly, skip subsequent priorities.
3.  If the annotation is missing (e.g., an empty shot row) → Infer item by item according to Priorities 2~6.
4.  Write the acquired orientation information into the description position of the corresponding character in the prompt.

**Orientation Vocabulary**:

| Orientation Type        | Mode A (Chinese)        | Mode B (English)                 | Applicable Scenarios                   |
| :---------------------- | :---------------------- | :------------------------------- | :------------------------------------- |
| Front | facing camera, front view | Self-declaration, directly confronting audience gaze |
| 3/4 Front | 3/4 side view facing camera | three-quarter view facing camera | Dialogue subject, emotional delivery |
| Full Profile | Profile view, side view | Monologue, contemplation, confrontation silhouette |
| 3/4 Back | 3/4 side back | three-quarter back view | Departure, aloofness, memory |
| Back | back to camera | back view, from behind | Mysterious entrance, farewell, distant gaze |
| Facing Left | Facing left | facing left | Character on right side of 180° line, facing left target |
| Facing Right | Facing right | facing right | Character on left side of 180° line, facing right target |
| Slightly Looking Down | slightly looking down | Sadness, guilt, contemplation |
| Slightly Looking Up | slightly looking up | Arrogance, looking up, anticipation |

> Orientation annotation must simultaneously include **horizontal orientation** (facing left/right/camera) and **pitch tendency** (if any), such as "3/4 side view facing right, slightly looking up".

### II. Position and Orientation Locking Rules

-   **Screen Position Lock**: For the same character across multiple storyboard shots within the same scene, their left/right screen position (left side of frame / center / right side) must remain fixed; side-jumping without narrative reason is not allowed.
- **Orientation Conservation**: Dialogue/confrontation scenes must follow the 180° axis of action—if Character A faces right, they must maintain facing right throughout the scene; if Character B faces left, they must maintain facing left throughout the scene; the prompt must explicitly indicate this using directional words (e.g., `facing left` / `facing left`, `on the left side of frame` / `upper left').
-   **Foreground-Background Consistency**: If Character A is in the foreground and Character B is in the midground in shot N, their relative foreground-background relationship should not arbitrarily reverse in subsequent shots of the same scene.
-   **Position Changes Must Have Action Transitions**: When a character's screen position genuinely needs to change (e.g., character walking, turning), the prompt of the preceding shot must include a description of the corresponding displacement/turning action; arbitrary position jumps are not allowed.
-   **Orientation Changes Must Have Action Transitions**: When a character's orientation genuinely needs to change (e.g., turning head, turning around), the prompt of the current shot must include a description of the turning action (e.g., "slightly turns head towards the left side of the frame"), and this turn must be consistent with the storyboard's "Character Action" field; arbitrary orientation changes are not allowed.
-   **Cross-Scene Reset Allowed**: Switching to a completely new scene allows for redistribution of screen position and orientation, but consistency must still be maintained within the new scene.

### III. Reflective Surface Visual Relationships

When the scene contains reflective media (mirrors, water surfaces, smooth metal, window glass, camera lenses, etc.), the following rules must be observed:

- **Mirror Flip**: The left/right orientation of a character in a reflective surface is opposite to that of the real entity (real entity facing right → mirror image facing left); the prompt must explicitly annotate the orientation relationship between the reflection and the real entity (e.g., "@Picture 1 faces right, @Picture 1 in the water reflection faces left").
-   **Reflective Surface Does Not Change Position Baseline**: The character's screen position is based on the real entity; the image in the reflective surface is not considered a change in character position.
-   **Reflective Surface Content Consistent with Entity**: The character's clothing, hairstyle, expressions, etc., visible in the reflective surface must be consistent with the real entity in the same frame; no discrepancies are allowed.
-   **Reflective Surface Depth of Field and Clarity**: Depending on the distance and material of the reflective surface, the reflected image can have appropriately reduced clarity (e.g., blur caused by water ripples), but this must be annotated in the prompt (e.g., "water reflection slightly distorted").
-   **Identification Trigger**: This rule is automatically triggered when the storyboard's visual description or scene assets include reflective elements such as mirrors, water surfaces, lakes, streams, glass, metal reflections, cameras/videocams, etc.

---

## Appendix: Complete Output Example

The following demonstrates a complete workflow from input to output for a single storyboard, for Agent reference. This example uses abstract placeholders (Character A, a certain scene, Prop X, etc.); in actual application, these should be replaced with the specific content from the storyboard.

### Input (A Storyboard Row)

| Field               | Content                                                                                                                                                                                                                                                                              |
| :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Visual Description  | Opening fade in from black, extreme wide shot of a certain scene exit, crowd bustling, conspicuous indicator object stands on the right side of the frame, Character A walks alone among the crowd carrying Prop X, camera slowly pushes to medium shot, he suddenly stops, clutching Prop Y in hand, looking up at the indicator object, eyes tense and resolute |
| Scene               | A certain scene exit                                                                                                                                                                                                                                                                 |
| Shot Type           | Wide shot → Medium shot                                                                                                                                                                                                                                                              |
| Character Action | Walking forward with backpack → Suddenly stops → Looks up at indicator object → Clutches Prop Y slightly tighter | Orientation: 3/4 front view facing right |
| Emotion             | Both apprehension and resolve present                                                                                                                                                                                                                                                |
| Lighting and Atmosphere | Soft morning light evenly spread from the left, warm yellow undertone lightly tints the ground, indicator object clearly illuminated, human figures appear silhouetted against the light, tending to be darker |
| Associated Asset ID | [a, b, c, d] → Character A (role), Prop X (tool), Prop Y (tool), A certain scene exit (scene)                                                                                                                                                                                          |

### Output (Mode A · Seedream)

```
@Picture 1 is character A @Picture 2 is prop X prop @Picture 3 is prop Y prop @Picture 4 is the exit scene of a certain scene,

[Picture]@Picture 4, opening fades in from black, extreme wide shot composition, crowd bustling through, a conspicuous indicator object stands on the right side of the frame; @Picture 1, carrying @Picture 2, walks alone among the crowd, clutching @Picture 3 in hand, body 3/4 front view facing right, stops among the people, looking up at the indicator object on the right side of the frame, eyes tense and resolute, face showing apprehension mixed with determination.

[Light and Shadow] Soft morning light evenly spreads from the left, warm yellow undertone lightly tints the ground, indicator object clearly illuminated, surrounding human figures appear silhouetted against the light, tending to be darker, @Picture 1's figure is half-lit and half-backlit, facial contour slightly bright.

[Style] {style anchor word}, {picture quality lock word}, no off-screen subtitles, no watermark, no UI text.

Maintain @Picture 1's facial features, hairstyle, and clothing identical to the reference image.
```

> The `{style anchor}` and `{quality anchor}` in the [Style] section are provided by style-specific techniques (`director_storyboard`); this general specification does not hardcode specific terms.

### Verification Comparison

| Storyboard Field           | Prompt Manifestation Location                                                                                               | Consistent? |
| :------------------------- | :-------------------------------------------------------------------------------------------------------------------------- | :---------- |
| Opening fade in from black | [Visual] "opening fades in from black"                                                                                      | ✅          |
| A certain scene exit | [Visual] "@Picture 4" | ✅ |
| Extreme wide shot (first frame starting point) | [Visual] "extreme wide shot composition"                                                                                    | ✅          |
| Crowd bustling             | [Visual] "crowd bustling through"                                                                                           | ✅          |
| Indicator object on the right side | [Visual] "a conspicuous indicator object stands on the right side of the frame"                                             | ✅          |
| Character A walks alone carrying Prop X | [Visual] "@Picture 1, carrying @Picture 2, walks alone among the crowd" | ✅ |
| Clutching Prop Y in hand | [Visual] "clutching @Picture 3 in hand" | ✅ |
| Stops and looks up at indicator object | [Visual] "stops among the people, looking up at the indicator object on the right side of the frame"                      | ✅          |
| Orientation 3/4 front view facing right | [Visual] "body 3/4 front view facing right"                                                                                 | ✅          |
| Tense and resolute         | [Visual] "eyes tense and resolute"                                                                                          | ✅          |
| Soft morning light from left + warm yellow undertone | [Lighting] "soft morning light evenly spread from the left, warm yellow undertone"                                          | ✅          |
| Human figures silhouetted against light | [Lighting] "human figures appear silhouetted against the light, tending to be darker"                                       | ✅          |

**Zero omissions, verification passed.**
```
