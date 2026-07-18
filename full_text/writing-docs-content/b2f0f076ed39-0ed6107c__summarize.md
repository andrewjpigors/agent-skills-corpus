---
name: summarize
description: Summarize any content (YouTube video, article, whitepaper/PDF, podcast episode, book chapter, etc.) into a rich Obsidian note with section-by-section breakdowns, wikilinks to all technical concepts and people, and reference notes for every linked term. Use when the user provides a URL, file, or content to summarize and document in the vault.
user_invocable: true
---

# Summarize

Universal content summarizer. Takes any input — YouTube video, web article, whitepaper/PDF, epub book, podcast, lecture — and produces a rich, interlinked Obsidian summary note with reference notes for every concept mentioned.

## Table of Contents

- [Requirements](#requirements)
- [Configuration](#configuration)
- [Trigger](#trigger)
- [Inputs](#inputs)
- [Step 0: Bootstrap check (first run)](#step-0-bootstrap-check-first-run)
  - [0a. Resolve the vault root](#0a-resolve-the-vault-root)
  - [0b. Check required folders](#0b-check-required-folders)
  - [0c. Check required CLI tools](#0c-check-required-cli-tools)
  - [0d. Install the person template if missing](#0d-install-the-person-template-if-missing)
- [Step 0.5: Determine depth mode](#step-05-determine-depth-mode)
- [Step 1: Detect content type and extract text](#step-1-detect-content-type-and-extract-text)
  - [YouTube video](#youtube-video)
  - [Web article / blog post](#web-article--blog-post)
  - [PDF](#pdf)
  - [EPUB (books)](#epub-books)
  - [Other files (txt, docx, etc.)](#other-files-txt-docx-etc)
  - [Pasted text / vault note](#pasted-text--vault-note)
- [Step 1b: Save transcript (audio/video content only)](#step-1b-save-transcript-audiovideo-content-only)
- [Step 1c: Archive audio to the vault + enable click-to-play timestamps (audio/video content only)](#step-1c-archive-audio-to-the-vault--enable-click-to-play-timestamps-audiovideo-content-only)
  - [1c-i. Archive the audio](#1c-i-archive-the-audio)
  - [1c-ii. Embed ONE pinned player at the top](#1c-ii-embed-one-pinned-player-at-the-top)
  - [1c-iii. Add inline click-to-play links next to every quote](#1c-iii-add-inline-click-to-play-links-next-to-every-quote)
  - [1c-iv. Math for audio-local offsets](#1c-iv-math-for-audio-local-offsets)
  - [1c-v. If the user does NOT have Media Extended](#1c-v-if-the-user-does-not-have-media-extended)
- [Step 2: Determine output structure](#step-2-determine-output-structure)
- [Step 3: Analyze structure, determine depth, and plan sections](#step-3-analyze-structure-determine-depth-and-plan-sections)
  - [3a. Determine summary depth from source length](#3a-determine-summary-depth-from-source-length)
  - [3b. Plan sections and dispatch](#3b-plan-sections-and-dispatch)
- [Step 4: Assemble the summary note](#step-4-assemble-the-summary-note)
  - [Structure](#structure)
- [[Section 1 Title]](#section-1-title)
- [[Section 2 Title]](#section-2-title)
- [People Mentioned](#people-mentioned)
  - [Formatting rules](#formatting-rules)
  - [Audience adaptation](#audience-adaptation)
- [Step 5: Create reference notes (one layer deep)](#step-5-create-reference-notes-one-layer-deep)
  - [5a. Extract and audit all wikilinks](#5a-extract-and-audit-all-wikilinks)
  - [5b. Create missing notes](#5b-create-missing-notes)
  - [5c. Verify — no dangling links](#5c-verify--no-dangling-links)
- [Step 5.5: Wiki Ingestion](#step-55-wiki-ingestion)
- [Step 5.6: Inbox Sweep (Batch Mode)](#step-56-inbox-sweep-batch-mode)
- [Step 6: Update bases (optional — skip if not using Obsidian Bases)](#step-6-update-bases-optional--skip-if-not-using-obsidian-bases)
- [Step 7: Update daily note](#step-7-update-daily-note)
- [content summary](#content-summary)
- [Model usage](#model-usage)
- [Key rules](#key-rules)

## Requirements

**Vault structure** — the skill expects these folders inside your Obsidian vault. Folder names are the defaults; override them in the Configuration block below if your vault uses different names.

| Folder | Purpose |
|---|---|
| `07 Summaries/` | Where summary notes land |
| `06 Wiki/pages/` | Concept / company / product / place notes |
| `04 People/` | Person notes (creators, guests, mentioned people) |
| `02 Daily/YYYY/MM/` | Daily notes, named `MM-DD-YY ddd.md` (e.g. `03-29-26 Sun.md`) |
| `_Templates/` | Note templates — skill installs `new person template.md` here on first run |
| `_Bases/` (optional) | Obsidian Bases — only needed if you use the Bases plugin |

**CLI tools** — install these before first use, or let Step 0 walk you through it:

| Tool | Purpose | Install |
|---|---|---|
| `yt-dlp` | YouTube/podcast download + metadata + subs | `brew install yt-dlp` or `pip install yt-dlp` |
| `defuddle` | Web article extraction | `npm install -g defuddle` |
| `pdftotext` | PDF text extraction | `brew install poppler` |
| `pandoc` | EPUB / DOCX → markdown | `brew install pandoc` |
| `mlx_whisper` (optional) | Local audio transcription fallback | `pip install mlx-whisper` |

Alternative to `mlx_whisper`: set `ELEVENLABS_API_KEY` to use ElevenLabs Scribe for transcription.

## Configuration

The skill reads these variables at runtime. Override any of them via environment variables, or edit the defaults here:

```
VAULT_ROOT     = $VAULT_ROOT        # auto-detected if not set (see Step 0a)
SUMMARIES_DIR  = 07 Summaries
REFERENCES_DIR = 06 Wiki/pages
PEOPLE_DIR     = 04 People
DAILY_DIR      = 02 Daily
TEMPLATES_DIR  = _Templates
BASES_DIR      = _Bases
```

All paths below are relative to `$VAULT_ROOT`.

## Trigger

When the user provides content to summarize (URL, file path, pasted text, or reference) or requests an **Inbox Sweep** (e.g. "sweep my inbox", "summarize everything in 00 Inbox").

## Inputs

- **Source**: URL, file path, pasted text, or "00 Inbox" (for sweep mode)
- **Audience** (optional): defaults to "general reader." User may specify (e.g. "high school student", "expert", "5-year-old")
- **Depth** (optional): defaults to "full." User may request "tldr only", "section-by-section", or "deep dive"

## Step 0: Bootstrap check (first run)

Before doing any work, verify the environment is ready. **Skip any check that already passes** — only prompt the user when something is actually missing. Do not re-run Step 0 on subsequent invocations if the initial setup succeeded; you can tell it already ran if `$VAULT_ROOT` resolves and the required folders + tools are present.

### 0a. Resolve the vault root

```bash
vault=""
if [ -n "$VAULT_ROOT" ]; then
  vault="$VAULT_ROOT"
else
  dir="$PWD"
  while [ "$dir" != "/" ]; do
    if [ -d "$dir/.obsidian" ]; then vault="$dir"; break; fi
    dir="$(dirname "$dir")"
  done
fi
echo "Vault: ${vault:-NOT FOUND}"
```

If no vault is found, ask the user:

> **What's the absolute path to your Obsidian vault?**
> Recommended: use a **new, dedicated Obsidian vault** for this skill — not your existing personal vault. The skill creates and modifies many notes and folders, and a clean vault avoids polluting your existing notes. If you don't have one yet, create an empty folder, open it in Obsidian (File → Open vault as folder), and paste that path here.

After they answer, validate that `<answer>/.obsidian/` exists before using it — if not, warn that the path doesn't look like an Obsidian vault (they may need to open it in Obsidian first) and ask them to confirm or re-enter. Use the validated answer as `$VAULT_ROOT` for the session (and suggest they set it permanently in their shell profile).

### 0b. Check required folders

```bash
for d in "$SUMMARIES_DIR" "$REFERENCES_DIR" "$PEOPLE_DIR" "$DAILY_DIR" "$TEMPLATES_DIR"; do
  [ -d "$VAULT_ROOT/$d" ] || echo "MISSING: $d"
done
```

For each missing folder, ask the user: **"Create `<folder>` in your vault? [y/N]"** — if yes, `mkdir -p "$VAULT_ROOT/<folder>"`.

### 0c. Check required CLI tools

```bash
for tool in yt-dlp defuddle pdftotext pandoc; do
  command -v "$tool" >/dev/null 2>&1 || echo "MISSING: $tool"
done
```

For each missing tool, tell the user what's missing and **ask before installing** — installs touch the user's system. Use the install commands from the Requirements table above. If the user declines, note which tools are missing and warn that the corresponding content types (YouTube, web articles, PDFs, EPUBs) will fail until installed.

### 0d. Install the person template if missing

The skill ships two person templates in the repo's `templates/` folder (shared with `summarize-call`):

- **`new person template.md`** — full version with Dataview callouts (current age, total hours talked) and Obsidian Bases embeds (`posts.base`, `books.base`, `meetings.base`). Requires the Dataview plugin and Obsidian Bases.
- **`new person template (minimal).md`** — stripped version. Just frontmatter, a `> [!info]` summary callout, and an `## updates` section. Works in any vault.

If `$VAULT_ROOT/$TEMPLATES_DIR/new person template.md` already exists, leave it alone — the user may have their own customized version.

Otherwise, ask the user which version to install:

> **Install person template — which version?**
> 1. **Minimal** (default, works in any vault)
> 2. **Full** (requires Dataview plugin + Obsidian Bases)

Then copy the chosen template into the user's `_Templates/` folder:

```bash
skill_dir="$(dirname "$0")"   # or wherever this SKILL.md lives
target="$VAULT_ROOT/$TEMPLATES_DIR/new person template.md"

if [ ! -f "$target" ]; then
  # Use the user's choice — default to minimal
  src="$skill_dir/../templates/new person template (minimal).md"
  # if user picked full: src="$skill_dir/../templates/new person template.md"
  cp "$src" "$target"
fi
```

Note: whichever version gets installed lands at `_Templates/new person template.md` (no `(minimal)` suffix) so the skill's later references work uniformly.

Once Step 0 passes, proceed to Step 0.5.

## Step 0.5: Determine depth mode

Before extraction, establish which depth the user wants:

1. **Scan the invocation first.** If the user's request already specifies a mode, use it and skip the prompt:
   - Words like `minimal`, `fast`, `quick`, `--minimal`, `-m` → minimal mode
   - Words like `detailed`, `deep`, `full`, `--detailed`, `-d` → detailed mode
2. **Otherwise, prompt.** No default — if unspecified, ask every time:

> **Depth?**
> 1. **Detailed** (best results) — full reference notes for every wikilinked concept, person notes for every mentioned person, parallel highest-available-model subagents per section, base updates
> 2. **Minimal** (fast) — summary note only, wikilinks left dangling, person notes for creators/guests only, Sonnet summary

This keeps interactive runs explicit while letting scheduled tasks / cron / `/loop` pass the mode in the invocation (e.g. `/summarize <url> minimal`) without blocking on input.

The chosen mode determines which steps run:

| Step | Detailed | Minimal |
|---|---|---|
| 1 Extract text | ✓ | ✓ |
| 1b Save transcript | ✓ | ✓ |
| 2 Output structure | ✓ | ✓ |
| 3a Depth from word count | ✓ | ✓ |
| 3b Parallel subagents | ✓ (>3000 words, highest available model) | ✓ (>3000 words, Sonnet) |
| 4 Assemble summary | ✓ | ✓ (skip `## People Mentioned` section) |
| 5 Reference notes (concepts) | ✓ | ✗ — wikilinks left dangling |
| 5 Person notes | ✓ (all mentioned) | ✓ (creators/guests only — those in `people` frontmatter) |
| 5c Dangling-link audit | ✓ | ✗ |
| 6 Bases update | ✓ (if bases exist) | ✗ |
| 7 Daily note | ✓ | ✓ |

For book chapter-by-chapter depth (Step 1 book section), detailed mode gets the full 300-600 words per chapter; minimal mode gets a flatter single summary regardless of chapter count.

## Step 1: Detect content type and extract text

### YouTube video
```bash
# Get metadata
yt-dlp --cookies-from-browser chrome \
  --print "%(id)s|%(title)s|%(duration)s|%(upload_date)s|%(view_count)s|%(channel)s|%(channel_id)s" \
  --no-download "<URL>"

# Try auto-subtitles first (fastest, free)
yt-dlp --cookies-from-browser chrome \
  --write-auto-sub --sub-lang en --sub-format json3 \
  --skip-download -o "/tmp/summarize/%(id)s" "<URL>"
```

If auto-subs exist, extract text from the JSON3 file. If not, or if quality is poor:
- Download audio and transcribe (same as `youtube-transcribe` skill — ask user: local mlx_whisper or ElevenLabs Scribe)

### Web article / blog post
```bash
defuddle parse "<URL>" --md -o /tmp/summarize/article.md
```

If defuddle is not installed: `npm install -g defuddle`

Extract title, author, date, domain from defuddle metadata:
```bash
defuddle parse "<URL>" -p title
defuddle parse "<URL>" -p domain
```

### PDF
```bash
pdftotext "<path>" /tmp/summarize/paper.txt
```

If `pdftotext` is not available: `brew install poppler`

### EPUB (books)
```bash
# Extract full text as markdown (preserves chapter structure)
pandoc "<path>" -t markdown --wrap=none -o /tmp/summarize/book.md

# If you need chapter boundaries, extract the TOC:
pandoc "<path>" -t json | python3 -c "
import json, sys
doc = json.load(sys.stdin)
for block in doc['blocks']:
    if block['t'] == 'Header':
        level = block['c'][0]
        text = ''.join(
            item['c'] if item['t'] == 'Str' else ' ' if item['t'] == 'Space' else ''
            for item in block['c'][2]
        )
        print(f'L{level}: {text}')
"
```

**Chapter splitting strategy for books:**
1. Extract full text with `pandoc` → markdown
2. Identify chapter boundaries from headers (epubs have built-in TOC structure that pandoc preserves as `#`/`##` headers)
3. Split into one chunk per chapter
4. Dispatch parallel Opus subagents — **one per chapter** — same as any other long content
5. A typical book (60-100k words, 15-30 chapters) produces chapters of ~3-5k words each — well within subagent context limits

**For very long books (>30 chapters):** batch chapters into groups of ~5 per subagent to keep the number of parallel agents manageable. Each subagent summarizes its batch and returns section summaries.

**CRITICAL — Book summary depth requirement:**
- Each chapter MUST get its own dedicated `## Chapter N: Title` section with a **substantial** summary (300-600 words per chapter depending on chapter length)
- Do NOT batch multiple chapters into a single brief paragraph — every chapter gets its own detailed treatment
- Include key arguments, data points, examples, and quotes from each chapter
- A 10-chapter book should produce ~3000-6000 words of summary content (excluding frontmatter/tldr)
- A 30-chapter book should produce ~5000-10000 words
- Think of each chapter summary as a standalone mini-essay that captures the chapter's core contribution
- The goal is that someone reading the summary should understand what each chapter argues, not just what the book is "about" at a high level

**Output structure for books:**
- Location: `07 Summaries/<Book Title>.md` (or `07 Summaries/<Author>/<Book Title>.md` if summarizing multiple books by one author)
- Frontmatter tag: `book`
- Extra fields: `creator` (author wikilink), `published` (year), `isbn` (if known), `source` (wikilink to the epub file if it's in the vault, e.g. `"[[Book Title.epub]]"`)
- Each chapter gets its own `## Chapter N: Title` section in the summary
- Add a `## Chapter Navigation` callout at the top if the book has many chapters

### Other files (txt, docx, etc.)

For `.docx`: `pandoc "<path>" -t markdown --wrap=none -o /tmp/summarize/doc.md`

For plain text: read directly.

### Pasted text / vault note
Read directly from user message or vault path.

## Step 1b: Save transcript (audio/video content only)

For any content that has audio — YouTube videos, podcast episodes, lectures/talks with recordings — save the extracted transcript as a permanent vault note.

**When to create a transcript note:**
- YouTube videos (from auto-subs or whisper transcription)
- Podcast episodes (from transcription)
- Lectures/talks with audio/video recordings
- Any content where the source is spoken word

**Do NOT create transcript notes for:** articles, blog posts, PDFs, books, pasted text — these are already text.

**Location:** Same folder as the summary note, with ` Transcript` appended to the filename.

**Format:**
```markdown
---
date: YYYY-MM-DD
duration: <seconds>
recording: "<source URL>"
meeting: "[[<Summary Note Title>]]"
unread: true
---

[Full timestamped transcript text, one line per segment]
```

**Link from summary:** Add `transcript: "[[<Title> Transcript]]"` to the summary note's frontmatter.

This step happens immediately after text extraction (Step 1) and before output structure planning (Step 2). The transcript is the raw source material — always preserve it.

## Step 1c: Archive audio to the vault + enable click-to-play timestamps (audio/video content only)

If the user has the **[Media Extended](https://github.com/aidenlx/media-extended)** Obsidian plugin installed (assume YES unless proven otherwise — it's a common companion plugin for this workflow), move the downloaded source audio into the vault and wire up click-to-play timestamps throughout the summary.

### 1c-i. Archive the audio

Copy (or move) the downloaded mp3/wav/mp4 into `$VAULT_ROOT/_Attachments/` with a descriptive, human-scannable filename that includes the date and — if cropped — the segment range.

```
<Creator> x <Guest> <YYYY-MM-DD>.mp3
<Creator> x <Guest> <YYYY-MM-DD> (HhMMm-HhMMm).mp3   # if cropped
```

**Add `audio: "[[<filename>.mp3]]"`** to the summary note's frontmatter so the attachment is a first-class property on the note (parallel to `transcript:`, `source:`, etc.).

### 1c-ii. Embed ONE pinned player at the top

Place a single full-length audio/video embed at the top of the summary, just above the `> [!tldr]` callout:

```markdown
> [!abstract] Audio — full interview (cropped H:MM:SS – H:MM:SS of the VOD)
> ![[<filename>.mp3]]
```

**Do not scatter multiple `![[audio.mp3#t=...]]` embeds through the note** — every embed spawns a fresh player. Media Extended's pattern is one pinned player + many text-link jump-points.

**Do NOT add:**
- A "Pin this player / Media Extended: right-click → Pin" instruction underneath the embed. The user knows how their plugin works. Don't narrate it.
- A "Key moments" / "Jump to" / "Chapters" callout listing timestamped highlights. The per-quote inline jumps (Step 1c-iii) already give every notable moment a click-to-play entry point; a separate highlights list is redundant and repeats the same timestamps twice.

### 1c-iii. Add inline click-to-play links next to every quote

For every `> [!quote]` callout that embeds a transcript line (`![[...Transcript#^block-id]]`), add a sibling line inside the same callout:

```markdown
> [!quote] Who — what they said
> ![[<Transcript Note>#^block-id]]
> ▶ [[<filename>.mp3#t=<seconds>|jump player to H:MM:SS]]
```

- The `#t=<seconds>` fragment is **audio-local seconds**, not wall-clock VOD time. If the audio was cropped (e.g. starting at VOD 1:17:00), subtract the crop offset from the VOD timestamp before emitting.
- The `|jump player to H:MM:SS` alias is what the user reads — format it `H:MM:SS` when ≥1 hour, else `M:SS`.
- The leading `▶ ` (U+25B6) is a visual cue — keep it.
- These are **text links** (no `!` prefix), not embeds. Media Extended routes the click to the pinned player instead of creating a new one.

### 1c-iv. Math for audio-local offsets

```
audio_sec = (vod_h * 3600 + vod_m * 60 + vod_s) - crop_start_sec
```

If the transcript already uses block IDs of the form `^p1-H-MM-SS` (absolute VOD timestamps), this regex transformation converts every quote-embed into one with an audio-local jump link appended:

```python
import re
AUDIO = "<filename>.mp3"
CROP_OFFSET_SEC = <crop start seconds>   # 0 if audio starts at beginning of the source

pattern = re.compile(
    r'^(> !\[\[[^\]]*Transcript#\^p1-(\d+)-(\d+)-(\d+)(?:-\d+)?\]\])$',
    re.MULTILINE,
)

def repl(m):
    block_line = m.group(1)
    h, mm, ss = int(m.group(2)), int(m.group(3)), int(m.group(4))
    audio_sec = (h*3600 + mm*60 + ss) - CROP_OFFSET_SEC
    if audio_sec < 0:
        return block_line
    hh = audio_sec // 3600
    mm2 = (audio_sec % 3600) // 60
    ss2 = audio_sec % 60
    label = f"{hh}:{mm2:02d}:{ss2:02d}" if hh else f"{mm2}:{ss2:02d}"
    return f"{block_line}\n> ▶ [[{AUDIO}#t={audio_sec}|jump player to {label}]]"

text = pattern.sub(repl, text)
```

Run this after Step 4 assembles the summary — it's a pure string transform.

### 1c-v. If the user does NOT have Media Extended

Fall back to native Obsidian syntax: one top-of-note `![[audio.mp3]]` embed only. Do **not** scatter `![[audio.mp3#t=N]]` embeds inline — they each spawn a separate player, which clutters the note. Inline timestamp references in that case should just be the VOD timestamp as plain text.

## Step 2: Determine output structure

Based on content type, choose the appropriate format:

| Content type | Location | Frontmatter tags | Extra fields |
|---|---|---|---|
| YouTube video | `07 Summaries/<Channel>/Summaries/<Title>.md` | `youtube` | `recording`, `audio` (wikilink to vault mp3 if archived per Step 1c), `views`, `creator`, `people`, `guest`, `hosts`, `guests`, `duration`, `uploaded`, `transcript` |
| Article / blog | `07 Summaries/<Title>.md` | `article` | `creator`, `source` (URL), `published` |
| Whitepaper / PDF | `07 Summaries/<Title>.md` | `paper` | `authors`, `affiliations`, `source` (wikilink to PDF if in vault, or URL), `published` |
| EPUB / book | `07 Summaries/<Title>.md` | `book` | `creator` (author wikilink), `published` (year), `isbn`, `source` (wikilink to epub if in vault) |
| Podcast episode | `07 Summaries/<Show>/Summaries/<Title>.md` | `podcast` | `recording`, `audio` (wikilink to vault mp3 if archived per Step 1c), `segment` (e.g. `"1:17:00 – 2:50:50"` if cropped), `people`, `guest`, `hosts`, `guests`, `duration`, `transcript` |
| Lecture / talk | `07 Summaries/<Title>.md` | `lecture` | `creator`, `recording` (if URL), `audio` (wikilink to vault mp3 if archived per Step 1c), `transcript` |

**All notes** get: `created`, `updated`, `date`, `summary`, `categories: ["[[posts.base]]"]`, `unread: true`

**`summary` field length — HARD LIMIT: ≤70 characters.** One tight line, no wikilinks, no paragraph-length blurbs. The `> [!tldr]` callout at the top of the body is where the long-form overview lives. The frontmatter `summary` is just a scannable hint for base views — think newspaper subhead, not abstract. Examples that are the right size:
- `"Ledger interviews Cobie — 3h 51m UpOnly career retrospective"` (60 chars)
- `"Cobie on ThreadGuy — first interview since joining Coinbase"` (59 chars)
- `"Lex x Karpathy — state of AI, RLHF, self-driving, education"` (60 chars)

If it's longer than 70 characters, cut it. Do not paste the tldr into the summary field.

If a channel/show folder is needed, check if it already exists before creating.

## Step 3: Analyze structure, determine depth, and plan sections

Read the full extracted text. Identify the natural sections/chapters/topics.

### 3a. Determine summary depth from source length

Summary length must be **proportional** to the source material. A 10-minute video and a 3-hour documentary should not produce the same size summary. Use the source word count to determine the target summary word count:

| Source word count | Source examples | Target summary words | Sections | TLDR |
|---|---|---|---|---|
| <1,500 | 5-min video, short article | 200–400 | 1–2 | 2 sentences |
| 1,500–5,000 | 10–20 min video, blog post, short paper | 500–1,200 | 3–5 | 3 sentences |
| 5,000–15,000 | 30–60 min video, long article, whitepaper | 1,500–3,000 | 5–8 | 3–4 sentences |
| 15,000–40,000 | 1–3 hr video/podcast, long paper | 3,000–6,000 | 8–15 | 4–5 sentences |
| 40,000–80,000 | Short book, multi-hour series | 5,000–10,000 | 15–25 | 5 sentences |
| 80,000+ | Full book (200+ pages) | 8,000–15,000 | 20–40 | 5 sentences |

**The ratio is roughly 1:5 to 1:10** — a 10,000-word source should produce ~1,500–2,500 words of summary. Denser/more technical content skews toward the higher end; conversational/repetitive content skews lower.

**For videos/podcasts**, estimate source words from duration: ~150 words/minute for conversational, ~120 words/minute for interviews with pauses, ~170 words/minute for scripted/narrated content. Or just use the actual transcript word count.

**Per-section depth**: each section's word budget should be proportional to its share of the source material. A section covering 20% of the transcript gets ~20% of the summary word budget. Adjust up for particularly dense/important sections, down for filler/repetitive ones.

### 3b. Plan sections and dispatch

**For long content (>3000 source words):** dispatch parallel subagents (see Model usage table for which model) — one per section — to summarize simultaneously. Each subagent gets:
- The section text
- The audience level
- A **specific word count target** (calculated from 3a above)
- Instructions to use `[[wikilinks]]` for every technical concept, person, place, company, and notable noun

**For short content (<3000 source words):** summarize directly without subagents.

**Model choice**: detailed mode uses the highest available model (Opus if the user has access, else Sonnet); minimal mode always uses Sonnet. Never Haiku.

## Step 4: Assemble the summary note

### Structure

```markdown
---
[frontmatter per Step 2]
---

[embed if applicable: ![[file.pdf]], ```vid URL```, etc.]

> [!tldr]
> [Overview — sentence count per Step 3a depth table. What is it about, who made it, what are the key takeaways?]

## [Section 1 Title]

[Summary paragraphs with [[wikilinks]] to all concepts, people, places, companies, products]

## [Section 2 Title]

[...]

## People Mentioned
- [[Person Name]] — brief context of who they are and their role in this content
```

### Formatting rules

1. **No `# Title` heading** — filename is the title
2. **Never repeat frontmatter in the body** — if it's in metadata, don't write it again
3. **`> [!tldr]`** for the overview, not `## Summary`
4. **`> [!quote]`** callouts for notable quotes (with speaker wikilink and source location if available)
5. **Wikilink EVERYTHING** — people, places, companies, concepts, technical terms, **book/film/show titles**, even if no note exists yet
5b. **Never create two separate wikilinks for the same entity.** If a person has a canonical note name plus other handles / real names / pseudonyms, use alias syntax — `[[Cobie|Jordan Fish]]`, `[[Bob Laksiv|King BTC]]` — not two siblings like `[[Cobie]] / [[Jordan Fish]]` or `[[Bob Laksiv]] / [[King BTC]]`. The canonical note is whichever name already exists (or will exist) in `04 People/`; everything else is a display alias pointing at it. Same for companies/products with renames — `[[Facebook|Meta]]`, `[[X|Twitter]]`. When it's natural to mention both, write it as prose: `[[Cobie]] (real name Jordan Fish)`, `[[Bob Laksiv]] (a.k.a. King BTC)`. Rule of thumb: one entity = one link target, always.
6. **Use actual Japanese/Chinese characters** for non-English words, not romanization
7. **Timestamps** on topic headings and quotes when available (YouTube, podcasts)
8. **`people` field**: only people who created/appeared in the content. Mentioned people go in `## People Mentioned`
9. **Audio click-to-play** — if Step 1c archived a local mp3 and Media Extended is installed, every `> [!quote]` callout that embeds a transcript block should also carry a `> ▶ [[<audio>.mp3#t=<sec>|jump player to H:MM:SS]]` text link (one pinned top-of-note player, many text-link jumps). See Step 1c for the full pattern and the regex transform.

### Audience adaptation

- **High school / college student**: plain language, analogies, explain jargon inline before first wikilink use
- **General reader**: balanced — explain key terms but don't over-simplify
- **Expert**: technical language fine, focus on novel contributions and critiques

## Step 5: Create reference notes (one layer deep)

**This is the most important step. Every wikilink MUST resolve to a note. No dangling links.**

### 5a. Extract and audit all wikilinks

After the summary note is fully assembled, extract every unique wikilink programmatically:

The regex excludes `|` (alias), `#` (heading ref), and `^` (block ref) so `[[Target|Alias]]`, `[[Page#Heading]]`, and `[[Page^block]]` all resolve to the canonical note name (`Target` / `Page`):
```bash
grep -oE '\[\[[^]|#^]+' "<summary_note_path>" | sed 's/\[\[//' | sort -u
```

Then check which ones are missing:

```bash
for term in <each extracted term>; do
  found=$(find "$VAULT_ROOT" -name "$term.md" \
    -not -path "*/.Trash/*" -not -path "*/Clippings/*" 2>/dev/null | head -1)
  if [ -z "$found" ]; then echo "MISSING: $term"; fi
done
```

**Do NOT skip this step. Do NOT estimate from memory which notes exist.** Always run the audit.

### 5b. Create missing notes

#### Technical concepts, companies, products, places
Create in `06 Wiki/pages/<Term>.md`:

```markdown
---
created: YYYY-MM-DDT00:00
updated: YYYY-MM-DDT00:00
type: reference
unread: true
---

[2-4 sentence plain-language explanation. Use [[wikilinks]] to cross-reference related concepts.]
```

#### People
Create in `$PEOPLE_DIR/<Full Name>.md` using the person template at `$VAULT_ROOT/$TEMPLATES_DIR/new person template.md` (installed by Step 0d). Conventions:

- **Public figures**: research and write a rich bio (birthday, career, links, key facts). The `> [!info]` callout should be a substantive snapshot — life story, mission, current focus — not a stub.
- **Private individuals**: minimal note with only what's known from the content. The note will grow naturally over time.
- **`> [!note] current age` callout** (from template): keep it if `birthday` is known or can be estimated. If estimated, append `(estimated)` to the callout text — but `birthday` in frontmatter must stay a pure YAML date (e.g. `2001-01-01`), never text.
- **`> [!abstract] total hours talked` callout** (from template): ONLY keep this if the person has had real 1-on-1 calls/meetings with the vault owner (i.e. they appear in meeting notes). Delete the callout for people discovered through summarizing videos, articles, books, or podcasts — those people will never have meeting entries, so the callout would always show 0h.
- **No `# Title` heading** — Obsidian shows the filename as the title.
- **`unread: true`** in frontmatter on every new or modified note.

#### Dispatch in parallel
For large numbers of missing notes (>10), use parallel subagents (highest available model) in batches of ~20-25 notes each. Each subagent creates the notes and returns confirmation.

### 5c. Verify — no dangling links

After all notes are created, re-run the audit from 5a to confirm zero missing notes. If any remain (e.g. a subagent failed or skipped one), create them manually. **The summary is not done until this verification passes.**

## Step 5.5: Wiki Ingestion

**This ensures the high-fidelity summary is properly indexed and woven into the wiki.**

After the summary note and all reference notes are created and verified (Step 5), trigger the `wiki-ingest` skill. 

- **Source**: Use the *original source file* from `00 Inbox/` if it exists. If the source was a URL or pasted text, use the generated summary note in `07 Summaries/` as the source for `wiki-ingest`.

The `wiki-ingest` skill will:
- Read the high-fidelity summary.
- Update `06 Wiki/index.md` and `06 Wiki/overview.md`.
- Log the ingestion in `06 Wiki/log.md`.
- Perform a backlink audit across existing wiki pages to link to this new summary.

## Step 5.6: Inbox Sweep (Batch Mode)

**Maintain a fully processed vault by proactively checking for other pending items.**

After completing the primary request and its wiki ingestion:
1. Scan the `00 Inbox/` folder for any files (PDFs, EPUBs, or video/article metadata notes) that do not yet have a corresponding high-fidelity summary in `07 Summaries/`.
2. For each pending item found:
    - Perform the full `summarize` workflow.
    - Trigger `wiki-ingest` for that item as per Step 5.5.
3. Continue until all items in `00 Inbox/` have matching summaries and wiki entries.

## Step 6: Update bases (optional — skip if not using Obsidian Bases)

This step only applies if `$VAULT_ROOT/$BASES_DIR/posts.base` exists. If it doesn't, skip Step 6 entirely.

```bash
[ -f "$VAULT_ROOT/$BASES_DIR/posts.base" ] || echo "No posts.base — skipping Step 6"
```

If it does exist:
- **`posts.base`**: if new people appeared as creators/guests, add named views for them using the YAML block below, then embed them in their person notes (in a `## episodes` or `## videos` section) via `![[posts.base#Person Name]]`.
- If a new channel/show folder was created, add a channel-specific view to `posts.base` the same way.

Named view YAML block to append under the `views:` list:
```yaml
  - type: table
    name: "Person Name"
    filters:
      and:
        - recording != null
        - people.contains(link("Person Name"))
    order:
      - date
      - views
      - file.name
      - summary
    sort:
      - property: date
        direction: DESC
```

## Step 7: Update daily note

Update `$VAULT_ROOT/$DAILY_DIR/YYYY/MM/MM-DD-YY ddd.md` (e.g. `02 Daily/2026/04/04-11-26 Sat.md`). Create the `YYYY/MM/` subdirectories if they don't exist. No `# Title` heading — the filename is the title. Set `unread: true` in frontmatter.

```markdown
## content summary
- summarized [[Note Title]] — [1-line description of what it is]
- created reference notes: [[Term 1]], [[Term 2]], ...
- created person notes: [[Person 1]], [[Person 2]], ...
```

## Model usage

| Task | Detailed | Minimal |
|------|----------|---------|
| Content extraction | Scripts (defuddle, pdftotext, yt-dlp) | Scripts |
| Section summarization | Highest available (Opus if accessible, else Sonnet) | **Sonnet** |
| Reference note creation | Highest available | (skipped) |
| Person note creation | Highest available | **Sonnet** (creators/guests only) |
| **NEVER** | **Haiku** | **Haiku** |

## Key rules

1. **Wikilink everything** — every concept, person, company, place, and **book/film/show title** gets a `[[wikilink]]`
2. **One layer deep** — create reference/person notes for EVERY wikilinked term that doesn't already have a note
3. **No `# Title` headings** — Obsidian shows filename as title
4. **Never repeat frontmatter in body** — frontmatter is metadata, body is content
5. **Set `unread: true`** on every note created or modified
6. **Parallel Opus subagents** for long content — one per section for summaries, batches of ~20 for reference notes
7. **Audience-appropriate language** — match the user's requested level
8. **Always embed/link the source** — PDF embed, vid embed, or source URL in frontmatter
9. **`> [!tldr]`** is mandatory — every summary starts with a concise overview callout
10. **Person note `## updates` links to the content note, NEVER the daily note**
11. **Audio archival + click-to-play** — for downloaded audio/video, archive the file to `_Attachments/`, embed ONE pinned player at the top, and add `▶ [[audio.mp3#t=<sec>|jump player to H:MM:SS]]` text links inside every quote callout. Never scatter multiple `![[audio.mp3#t=N]]` embeds (they each spawn a separate player). See Step 1c.
