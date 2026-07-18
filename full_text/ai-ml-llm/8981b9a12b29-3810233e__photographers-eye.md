---
name: photographers-eye
description: "Photographer's Eye / 摄影眼: professional photo diagnosis and retouch prompt workflow with style menus, mandatory crop/recomposition audit, outpaint/aspect-ratio remap, light thesis, color-world grading, tonal curve, local masks, portrait beauty/body retouch, reference routing, quick correction maps, and copy-ready imagegen/Doubao/Jimeng prompts. Use when a photo needs critique, 修图/废片拯救, retouch/imagegen prompt, crop/recompose/expand/outpaint, aspect-ratio changes, lighting/camera simulation, portrait beautify/body shaping, cinematic/emotional/street/editorial/magazine looks, Lightroom/Photoshop-style instructions, or AI editor prompt text. Chinese triggers: 摄影眼, 修这张, 裁切, 改画幅, 调色, 强一点, 电影感, 胶片感, 日杂, 杂志感, 氛围感, 美颜美体, 瘦脸瘦身, 参考图, 生成修图指令, 豆包修图."
---

# Photographer's Eye / 摄影眼

Use this skill to look at a photo like a photographer, picture editor, beauty retoucher, and art director before writing any prompt. The goal is to find what is still alive in the image, then decide whether to preserve, crop, expand, reshape light, beautify, restyle, or creatively rescue it.

Default behavior: generate an edit direction and prompts, not a finished image. Only call image generation/editing tools when the user explicitly asks to apply the prompt. Use two interaction modes:

- `Style menu mode`: When the user gives a vague request such as "修图", "帮我看看", or "这张怎么调" without a target style, direct-edit instruction, or prompt request, analyze the image and offer 4-6 tailored style routes before writing the full prompt. Each option must include `效果`, `适合`, and `代价`; recommend 1-2 options and wait for the user's choice. Do not call image editing tools in this mode.
- `Direct prompt mode`: When the user says "直接修", "开始修", "生成修图提示词", "按这个风格改", "废片拯救出完整方案", "复制给豆包/即梦", or already provides a target/reference direction, write the full diagnosis and copy-ready prompt immediately.
- If the user chooses multiple style options, create separate versions by default. Fuse styles only when the user explicitly asks to combine them.

First choose the delivery type, then decide how much crop, relight, cleanup, or generation is allowed. If the user asks for cleanup, text/sticker removal, screenshot repair, social-media cover repair, a comparison against a retoucher's finished image, or a Doubao/Jimeng-style repair prompt, default to original fidelity repair or commercial rescue and keep the original aspect ratio unless the user asks for crop/recomposition. For creative photo rescue, still make an explicit crop/recomposition verdict, but do not change aspect ratio by habit. Composition is the entry gate, not the finish; every full retouch must also define color grade, tonal curve, light design, local masks, and texture finishing. Treat light as the main photographic instrument: every full edit must decide what light reveals, what shadow hides, and what contrast pattern makes the image worth looking at. If the user provides a before/after example as a degree reference, match the transformation intensity, not the exact palette.

## Quick Trigger Phrases

Treat these Chinese shortcuts as equivalent to explicitly invoking this skill when a photo is present or referenced:

- `摄影眼`, `用摄影眼`, `按摄影眼分析`
- `修图`, `修这张`, `帮我修`, `重新修`, `强一点`, `更狠一点`
- `裁切`, `重新构图`, `扩图`, `改画幅`, `横图`, `竖图`, `封面图`
- `废片拯救`, `救片`, `这张还能救吗`
- `生成修图提示词`, `imagegen 修图`, `按提示词修`
- `复制到豆包`, `豆包修图`, `即梦修图`, `AI修图指令`
- `调色`, `电影感`, `胶片感`, `日杂`, `杂志感`, `氛围感`, `情绪人像`, `人文街拍`
- `美颜`, `美体`, `瘦脸`, `瘦身`, `大长腿`, `衣服显胖`
- `参考图`, `参考这个风格`, `只参考强度`, `只参考调色`, `只参考构图`, `不要参考下面/右边`

## Required Inputs

- If the image is attached or visible, analyze it directly.
- If the user provides a local path, load or inspect the image first so it is visually available.
- If no image is available, ask for the image before producing a photo-specific plan.
- If EXIF exists and is easy to inspect, use it as evidence. Otherwise describe camera/lens/settings as a visual simulation, never as factual capture metadata.
- If multiple images appear, label each image role before analysis: `edit target`, `style reference`, `degree reference`, `negative reference`, or `before/after collage`.
- If the input is a collage or before/after comparison, isolate the requested edit target first when possible. Do not let unrequested panels influence the analysis.
- If a reference image contains tutorial labels, before/after text, stickers, captions, or other graphic overlays, use it only as a `degree reference` unless the user explicitly asks to preserve that graphic design. Match brightness, skin cleanliness, subject/background separation, and retouch intensity; do not copy or keep any text.

## Reference Routing

- For any full photo rescue or prompt-generation task, read `references/master-methods.md`, `references/genre-recipes.md`, and `references/style-directions.md`.
- For copy-ready prompt output, third-party AI editor prompts, or platform-specific instruction text, read `references/prompt-templates.md`.
- For overexposure, underexposure, color cast, noise, blur, flat light, bad crop, poor skin, messy background, or other common technical problems, read `references/quick-fix-maps.md`.
- For uncertain output shape, first-time use, or examples of style menu and prompt formatting, read `references/usage-examples.md`.
- For a tiny one-off answer, use this file only and keep the output brief.
- Use named photographers as methods and visual disciplines, not as direct style-copy instructions. Prefer "use the tonal discipline of..." or "borrow the lighting logic of..." over "in the style of...".

## Core Workflow

1. **Determine the delivery type before prescribing.**
   Choose one delivery type and let it control frame authority, cleanup freedom, and generation risk:
   - `Original fidelity repair`: remove text/stickers/watermarks/overlays, repair screenshots, fix exposure/skin/color/noise, preserve original composition and aspect ratio. Use for `去文字`, `去贴纸`, `修截图`, degree-reference matching, tutorial-label references, and conservative Doubao/Jimeng repair prompts.
   - `Commercial rescue`: make the photo sellable or socially polished while preserving the original ratio and subject. Use strong fill light, beauty retouch, skin cleanup, clothing cleanup, background softening/desaturation, denoise/sharpen, and local subject separation without changing the core frame.
   - `Photographic creative reconstruction`: allow crop, new aspect ratio, stronger light reshaping, color-world transformation, and making the image feel like a new photographic work.
   - `Generative reconstruction`: allow outpaint, background repaint, major object removal, rebuilt edges, or obvious image transformation. Use only when the user asks for expansion/rebuild/strong creative remake or literal repair will fail.
   For `Original fidelity repair` and `Commercial rescue`, keep the original aspect ratio unless the user explicitly asks for crop, recomposition, cover layout, horizontal/vertical conversion, or outpaint.

2. **Read the image before prescribing.**
   Identify subject, supporting elements, background, light direction, light quality, shadow shape, highlight placement, focus plane, depth of field, color cast, exposure, dynamic range, noise, blur, perspective, edge distractions, and the image's strongest surviving value. Note whether the source already has useful light, flat light that needs shaping, or bad light that should be replaced with a plausible motivated light.

3. **Resolve user intent, style constraints, and references.**
   Translate casual style language into concrete photographic decisions. Do not repeat vague words like "高级", "电影感", or "氛围感" without mapping them to crop, light, color, texture, masks, and protection rules.
   If the user supplies an extra reference image, assign one role:
   - `Degree reference`: match transformation strength only; do not copy exact hue, composition, or subject.
   - `Color reference`: borrow color relationships and contrast logic; protect skin, identity, product colors, text, and source-image truth.
   - `Composition reference`: borrow crop ratio, subject scale, negative space, or edge discipline.
   - `Lighting reference`: borrow key/fill/rim direction, hardness, color temperature, and shadow density.
   - `Texture reference`: borrow grain, halation, sharpness, matte/gloss, skin finish, or water/foliage texture.
   - `Target reference`: use only when the user clearly says "修成这样/按这张成片走".
   - `Negative reference`: use only as an avoid list when the user says "不要这样".
   Treat retoucher finished images, before/after collages, and labeled tutorial screenshots as `Degree reference` by default. Match retouch strength, face brightness, skin cleanliness, subject/background separation, and cleanup intensity; do not copy typography, stickers, labels, captions, exact palette, or layout unless explicitly requested.
   Ask one concise question only when the reference role would materially change the edit and cannot be inferred.

4. **Define the rescue level inside the delivery type.**
   Choose one rescue level, but do not let it override the delivery type's frame constraints:
   - `Fidelity repair`: preserve content and composition; fix exposure, color, contrast, noise, and small distractions.
   - `Commercial rescue`: preserve original ratio and subject; remove overlays first, lift/beautify subject, soften background, clean clothing/skin, and polish for a deliverable result.
   - `Photographic edit`: crop only when allowed; guide attention, reshape light, simplify background, and strengthen subject hierarchy.
   - `Creative rescue`: convert mood, aspect ratio, color language, black-and-white, grain, cinematic grade, fashion/editorial polish, or poster-like negative space when the delivery type allows it.
   - `Generative reconstruction`: outpaint, remove major distractions, rebuild missing context, relight the scene, restage background hierarchy, or create alternate versions. Use when the user asks for strong rescue or when literal repair would remain weak; preserve protected identity/text/product details.

5. **Set the creative ambition.**
   Pick an intensity before choosing tools:
   - `Clean natural`: close to reality, corrected and polished.
   - `Editorial`: visibly designed color, light, crop, and subject hierarchy. Use only when the user asks for natural or professional restraint.
   - `Signature look`: a stronger camera/film/fashion/cinematic identity, still photorealistic. Use this as the default for ordinary "修图", "废片拯救", and imagegen-prompt requests.
   - `Conceptual rescue`: high-risk transformation, only when the user asks for a bold remake or the image is otherwise weak.
   Also assign an `aggression score` from 1-5:
   - `1`: faithful correction
   - `2`: polished natural edit
   - `3`: editorial/signature look
   - `4`: strong magazine/cinematic rescue with assertive crop, relight, cleanup, and color identity
   - `5`: conceptual transformation/outpaint/rebuild, while preserving locked identity/details
   Default to score 1-2 for original fidelity repair, score 3-4 for commercial rescue, score 4 for creative rescue, and score 5 only for explicit generative reconstruction or "still too conservative" feedback.
   Also assign a `grade strength` from 1-5 using `style-directions.md`. Default to Grade 1-2 for original fidelity repair, Grade 3 for commercial rescue, and Grade 4 for creative rescue: the edit should fit the delivery type rather than always creating a new color world.

6. **Decide composition before color.**
   Never skip the crop decision. Give a `crop verdict` before discussing grade, filters, or masks:
   - `Keep original frame` by default for original fidelity repair, text/sticker removal, screenshot repair, social-media cover repair, commercial rescue, and degree-reference matching unless the user asks for crop/recomposition.
   - For photographic creative reconstruction, `Keep original frame` only when the existing frame is already stronger than crop/outpaint. Say why.
   - `Crop/recompose` when edges are noisy, subject scale is weak, horizon/geometry is awkward, foreground clutter dominates, dead space weakens the subject, or a stronger ratio would clarify the story.
   - `Straighten/perspective-correct` before crop when geometry, horizon, architecture, podiums, waterlines, or verticals distract.
   - `Outpaint/expand` when the subject is cramped, gaze/motion needs breathing room, a deliverable ratio needs space, a cover/title area is useful, or vertical/horizontal conversion would preserve the main subject.
   For creative or generative rescue, test at least three frames mentally: original frame, tighter crop, and alternate ratio or outpaint. Pick one primary frame and one backup frame.
   For the chosen frame, specify:
   - final aspect ratio and orientation, such as 1:1, 4:5, 3:4, 2:3, 16:9, 2.39:1, panorama, or poster cover
   - subject placement, scale, horizon/eye-line height, headroom/lead room, and negative space
   - which edges to cut away, keep, darken, simplify, remove, or extend
   - whether crop should happen before imagegen editing, inside the imagegen prompt, or after generation
   Avoid outpainting when documentary truth, identity, readable text, hands, complex architecture, or product accuracy matters unless the user accepts AI reconstruction risk.
   A crop-only plan fails this skill. After the crop verdict, always continue into tonal, color, lighting, mask, and texture decisions.

7. **Choose the light thesis before grading.**
   State the image's light strategy as a concrete visual event, not a generic "soft light":
   - `Preserve`: keep existing light when it already gives subject separation, atmosphere, or documentary truth.
   - `Shape`: add local dodge/burn, negative fill, rim, or catchlight while keeping the original light plausible.
   - `Relight`: create a motivated key, window patch, sun slash, backlight, rim, practical, neon, flash, or reflected bounce when the source is flat or confused.
   - `Dramatize`: for strong rescue, let light create visible contrast: dappled foliage light, diagonal window shadow, hard flash falloff, glowing edge rim, storm backlight, street/practical pools, or side light across texture.
   Specify direction, height, distance, hardness, color temperature, affected surfaces, shadow falloff, and what stays in darkness. If no clear light source exists, invent one that the scene could plausibly contain rather than washing the whole frame evenly.

8. **Lock the full finishing stack.**
   Do not let composition replace retouching. Define all of these before writing the final prompt:
   - `Tonal architecture`: black point, highlight rolloff, midtone density, contrast curve, whether shadows stay detailed or fall near black.
   - `Color world`: grade family, shadow hue, highlight hue, saturation hierarchy, protected colors, and which nonessential colors may shift.
   - `Light design`: light thesis, key/fill/rim/negative fill/practical/flash logic, shadow pattern, and surfaces that receive highlights.
   - `Local masks`: subject/face/object, background, edges, highlights, shadows, color contamination, texture zones, and attention/vignette masks.
   - `Texture finish`: sharpening policy, noise reduction, grain, halation/bloom when useful, skin/leaf/fabric/material texture protection.
   For commercial, creative, or generative rescue, the light, grade, and local masks should be visible at thumbnail size; if the result only looks cropped or merely recolored, increase light-shadow contrast or relight/background separation.

9. **Previsualize the final photograph.**
   Write one sentence that defines the intended final image: subject hierarchy, mood, tonal key, color temperature, contrast, texture, and realism level.

10. **Choose style candidates.**
   For fidelity repair and commercial rescue, select one primary repair route and one conservative alternate that preserves frame authority. For creative/generative rescue, select one strong primary route and one more radical alternate. Consider cinematic still, emotional portrait, humanistic street, magazine editorial, commercial beauty, travel diary, documentary, film snapshot, moody nature, graphic black-and-white, direct-flash, cover/poster, or conceptual rescue. The route must match the delivery type, the photo's surviving value, and the user's likely use case.

11. **Select a photographic method.**
   Map the image to one or more methods from `references/master-methods.md`: tonal zones, decisive geometry, environmental light, studio reduction, sculptural still life, color blocks, motion, grain, or large-format objectivity.

12. **Choose the final look, not just the original look.**
   Use EXIF as evidence when available, but do not be constrained by it. Camera/lens/filter choices are visual simulations for the desired final image. Prefer a more aspirational system, lens, film stock, or filter when that clarifies the result. Do not match the original camera unless matching it is itself the strongest artistic choice.

13. **Reverse-engineer the capture simulation.**
   Choose a plausible camera class, lens/focal length, shooting distance, aperture, shutter speed, ISO, exposure compensation, white balance, and filter. Make these serve the desired result: compression, distortion control, skin rendering, bokeh, color separation, microcontrast, or cinematic density.

14. **Design light.**
   Preserve existing light when it is the image's strength. Otherwise specify:
   - main light direction, height, distance, hardness, modifier, power ratio, and color temperature
   - fill, negative fill, reflector, rim, background light, practical light, or flash only when useful
   - whether flash should be avoided, used as barely visible fill, or used as a deliberate hard-light effect
   For aggression score 4-5, actively redesign the light: add motivated key/rim/practical light, stronger negative fill, dramatic background falloff, or a fashion/editorial flash look. Keep the light plausible, but do not merely "softly lift" the source. Define the visible shadow pattern and highlight path; the viewer should be able to tell where the light comes from.

15. **Plan retouching by masks.**
   Always separate global edits from local masks. Include only masks that fit the photo:
   - subject, face/skin, eyes, hair, clothing, petals, product surface, sky, water, foliage, background, edges, highlights, shadows, color contamination, radial attention, vignette
   - exposure, highlights, shadows, whites, blacks, curve, color temperature, tint, HSL, color grading, texture, clarity, dehaze, sharpness, noise reduction, grain

16. **For portraits, plan beauty and body retouch explicitly.**
    Unless the user asks for documentary truth, include face, skin, hair, clothing, posture, and body-line refinement. Preserve identity and anatomy, but do not ignore flattering edits:
    - skin cleanup, under-eye/blemish softening, facial light, catchlights, lip/teeth cleanup when visible
    - jawline/cheek/nose shadow shaping with dodge and burn instead of changing identity
    - posture correction, shoulder/neck line, waist/arm/leg line, clothing wrinkles, hemline, and shoe/foot presentation
    - body shaping should be subtle to moderate by default; state stronger changes only when the user asks for "美体/瘦身/大长腿/精修".

17. **Write prompts that protect the photo.**
   For imagegen or similar tools, explicitly preserve identity, species, object geometry, composition decisions, and documentary constraints. Separate allowed changes from forbidden changes.
   For aggressive prompts, explicitly state what may change: crop, background clutter, lighting mood, color palette, grade strength, depth, bokeh, clothing wrinkles, body line, sky/ground simplification, negative space, and nonessential distractions. Then lock what must not change.
   For cleanup, commercial rescue, text removal, screenshot repair, and degree-reference matching, write prompts in stages to avoid whole-image repaint:
   - `Stage 1`: remove text, stickers, labels, captions, overlays, watermarks, and reconstruct only the hidden background under them.
   - `Stage 2`: local portrait/product rescue: face fill, skin cleanup, hair detail, clothing brightness, product/text/logo preservation, and subject mask work.
   - `Stage 3`: background and final grade: soften or desaturate background, unify color temperature, denoise/sharpen, add subtle contrast, and protect the original frame.

18. **Quality-control the plan.**
    Check that the proposal does not make the image generically pretty at the cost of its strongest value. Watch for over-sharpening, neon color, crushed blacks, clipped whites, fake glow, plastic skin, warped hands/text, changed subject identity, unnatural limbs, impossible body proportions, and unjustified AI additions.
    Also reject crop-only or color-only outputs: if the prompt or result mainly changes framing or palette, add a clearer light thesis, shadow pattern, subject highlight, tonal curve, local masks, and texture finish.
    Before calling imagegen or giving a direct imagegen prompt, run this QC:
   - Does the prompt keep the original aspect ratio unless the user asked for a new one?
   - Does it explicitly remove all existing text/overlays/stickers and forbid new text?
   - If a face is dark, does it ask for enough face lift or simulated fill light rather than "slight brightening"?
   - Does it lock identity, face shape, expression, pose, hands, clothing design, and subject geometry?
   - Does it separate foreground subject treatment from background treatment?
   - Does it avoid asking the tool to "shoot a new photo" when the task is repair or commercial rescue?

## Output Format

Respond in the user's language. For Chinese requests, use Chinese headings and put copy-ready prompts in fenced text blocks.

For style menu mode, use this shorter structure and wait for the user's choice:

1. `照片诊断`
2. `交付类型判断`
3. `这张图适合的方向`
   Give 4-6 options. Each option must include `效果`, `适合`, and `代价`.
4. `推荐`
   Name the strongest 1-2 routes and ask the user to reply with a number. If multiple routes are selected, default to separate versions.

Use this structure for full requests:

1. `交付类型判断`
2. `照片诊断`
3. `可拯救方向`
4. `构图策略 / 裁切重构图`
   Include crop verdict, final ratio/orientation, subject placement, edge instructions, rejected crop option, and whether to crop before imagegen, inside imagegen, or after generation.
5. `预想成片`
6. `创作强度与风格候选`
   Include aggression score, grade strength, strong primary route, stronger color-world direction, and more radical alternate.
7. `风格约束理解/参考图路由` when the user gives style words or extra reference images
8. `摄影方法论` with photographer-method references when useful
9. `模拟拍摄方案` with camera, lens, distance, aperture, shutter, ISO, WB, exposure compensation, filter
10. `布光 / 光影策略`
   Include light thesis, visible shadow pattern, key/fill/rim/negative fill/practical/flash decision, direction, height, distance, hardness, modifier, color temperature, and what should remain dark.
11. `后期路线 / 调色路线`
    Include tonal curve, color grade family, shadow/highlight hue, HSL priorities, protected colors, texture/grain/denoise, and global exposure decisions.
12. `局部蒙版`
13. `三阶段修图流程` for cleanup, commercial rescue, text removal, screenshot repair, and degree-reference matching
14. `人像美颜/美体策略` when the photo contains people
15. `复制用修图指令 / imagegen 完整提示词`
    Use a fenced `text` block. The prompt must be directly reusable in imagegen, Doubao, Jimeng, or similar AI editors when possible.
16. `负面提示词`
17. `一句话精简版`

If the user asks for only prompt text, provide the delivery type, staged repair plan when relevant, essential crop/frame notes, light/color/mask decisions, negative prompt, and the copy-ready prompt.

## Error Handling

- If the image cannot be read, ask for JPG, PNG, or WEBP and do not invent photo details.
- If no image is available, ask for the image before giving photo-specific diagnosis; general style guidance is acceptable only if the user asks for it.
- If the image role is ambiguous across multiple files, label likely roles and ask one concise question only when role choice changes the edit.
- If the source quality is very poor, give a `rescue viability` verdict: what can be repaired, what should be hidden with crop/grain/black-and-white/mood, and what should not be promised.
- If the user asks for a style that fights the image, explain the tradeoff, recommend the stronger route, then follow the user's choice if they insist.
- If the user says "先不要动手", output only diagnosis and style menu; do not generate final prompt or call editing tools.

## Prompt Rules

- Be concrete: give focal length, aperture range, shooting distance, light direction, color temperature, exposure compensation, grade family, and retouch intensity when they matter.
- Every imagegen prompt must include an explicit final canvas decision: original ratio vs new ratio, crop boundaries when any, subject placement, and which edges to remove/protect/extend. For creative reconstruction, do not preserve the original frame by habit; for fidelity repair and commercial rescue, preserve the original frame unless the user asks otherwise.
- Do not change aspect ratio or crop aggressively when the task is cleanup, text/sticker removal, screenshot repair, social-media cover repair, commercial rescue, or degree-reference matching. In these cases, keep the original frame unless the user asks for crop/recomposition.
- Every imagegen prompt must also include an explicit finishing stack: grade family, shadow/highlight color split, contrast curve, local masks, texture/noise/grain, and light design. Do not submit a crop-only prompt.
- Every imagegen prompt must include a `light thesis`: where the light enters, what it hits first, what shadow shape it creates, where negative fill deepens the image, and why the light is plausible in the scene. Do not use vague light language alone.
- Avoid fake certainty: say "simulate" camera/lens/settings unless EXIF proves them.
- Do not let EXIF make the edit boring. When a better final look calls for a Leica, Hasselblad, GFX, Contax, Ricoh, Canon portrait lens, cinema lens, film stock, or diffusion filter simulation, choose it as a visual target.
- Do not reduce style to a filter name. Describe how the route changes composition, light, color, local masks, skin/body treatment, grain, and background hierarchy.
- Do not undersell the edit, but let the delivery type set the ceiling: original fidelity repair should look repaired, commercial rescue should look polished, creative reconstruction should look visibly authored, and generative reconstruction may look transformed.
- Default original fidelity repair to Grade 1-2, commercial rescue to Grade 3, creative rescue to Grade 4, and generative reconstruction or "still too conservative" feedback to Grade 4-5. Do not use "slight/subtle/gentle" for required face fill, overlay removal, or commercial rescue when the source needs stronger correction.
- When the user shows a before/after example to indicate intensity, do not copy exact hues unless requested; copy the degree of tonal and color restructuring: new shadow hue, new highlight warmth, stronger density, and a recognizable color world at thumbnail size.
- For Grade 4-5, allow sky, foliage, walls, streets, background shadows, and nonessential color blocks to shift into the chosen palette. Protect skin tone, logos/text, product colors, and identity-critical details with local masks.
- When extra reference images exist, explicitly state their role before writing prompts. Never silently treat an extra image as a full target unless the user clearly asks for that.
- If the user says "不要参考下面/右边/成片", isolate and use only the specified source image region before analysis when possible.
- Do not over-preserve a broken frame in creative or generative rescue. If crop or outpaint is the best allowed rescue, say so directly.
- When crop/recomposition is allowed, do not let a strong color grade compensate for bad framing. Recompose first, then relight and grade.
- When a strong crop is allowed, do not let it replace color and retouching. Recompose first, then make the color world, light hierarchy, and local masks equally explicit.
- Do not let strong color replace light. If the scene is flat, create contrast with directional light, negative fill, rim/backlight, practical light, dappled light, or local dodge/burn before relying on saturation.
- Do not over-generate. Keep original subject, identity, species, product details, text, and architecture unless the user asks to change them.
- Do not use decorative camera brands when a generic class is enough. Use named camera/lens references only to communicate a known look.
- Prefer a strong signature edit over a flat faithful edit only when the delivery type permits it. For original fidelity repair and commercial rescue, improve the existing frame before proposing a radical alternate.
- For portraits, include beautification and body-line optimization by default, but preserve identity, age category, anatomy, clothing design, and recognizability.

## Mini Decision Tree

- Strong subject, weak background: crop or darken/desaturate background; subject mask and radial attention.
- Backlit portrait with dark face but usable sunset/background: choose `Commercial Backlight Rescue` by default. Keep original composition, remove overlays first, lift face/skin by about 2-3 EV with simulated front softbox or reflector fill, keep hair deep but detailed, make white clothing clean and bright, soften/desaturate background slightly, preserve sunset color without letting it dominate the subject.
- Weak subject, strong light/color: build the edit around light, silhouette, color blocks, or atmosphere.
- Weak light, decent subject: create a plausible key, shadow pattern, and negative fill; use light to sculpt the subject before increasing saturation.
- Missed focus: avoid "sharpness miracles"; crop smaller, add grain, black-and-white, motion/soft mood, or creative rescue.
- Overexposed highlights: recover if possible; if clipped, embrace high-key or crop away damaged areas.
- Underexposed/noisy: lift selectively, denoise background, preserve texture on subject, or convert to grainy monochrome.
- Busy frame: simplify with crop, edge burn, background blur/softening, color separation, or object removal if allowed.
- Subject too tight: outpaint in the direction of gaze/motion/negative space; preserve optical continuity and perspective.
- Strong scene hidden inside clutter: crop or outpaint to make the hidden subject readable; remove foreground blockage before spending effort on color.
- Casual portrait with good pose but ordinary light: choose an editorial or beauty look, add flattering face light, skin cleanup, clothing cleanup, and subtle body-line refinement.
- Portrait with unflattering distortion: prefer crop/perspective/lens simulation and subtle body shaping; avoid changing identity or creating impossible limbs.
- Technically correct but visually bland: raise creative ambition, pick a stronger color grade, distinctive camera/lens simulation, and one clear emotional direction.
- "Still too conservative" feedback: increase aggression and grade strength by at least one level, choose a stronger route, redesign light/color/crop, and allow nonessential background reconstruction while preserving locked subject identity/details.
