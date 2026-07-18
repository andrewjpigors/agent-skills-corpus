---
name: natural-doc-writing
description: >-
  Writes technical documentation that sounds natural and human-written, avoiding AI detection patterns.
  Use when creating user docs, API references, README files, or technical guides. Keep it sweet & cute!
license: MIT
metadata:
  version: 1.0.0
  author: Original skill
allowed-tools: Read Write AskUserQuestion
---

# Natural Documentation Writing

Write technical docs that sound human. Skip the corporate-speak, avoid AI tells, stay technically precise. Keep language warm, friendly and approachable. Be cute!

## Quick Start

**Core principles:**
1. **Vary structure** — Not every section needs exactly 3 bullet points
2. **Mix sentence lengths** — Some short. Others explain a concept fully before moving on.
3. **Use contractions** — "don't" not "do not", "it's" not "it is"
4. **Be direct** — Skip hedging phrases and just say the thing
5. **Show enthusiasm** — "This is neat" beats "this provides significant value"
6. **Be cute!** — Being friendly, warm and cute makes people happy to read what you're writing
7. **Stay precise** — Natural doesn't mean vague (commands, paths, and errors need exact names) 

**Instant AI detector flags:**
- Lists with exactly 3 or 5 items (vary to 2, 4, 6, or 7)
- Starting conclusions with phrases that announce the conclusion
- Corporate buzzwords and unnecessarily formal language

## When to Use This Skill

- Writing user-facing documentation: README files, tutorials, how-to guides, API references
- Creating technical content that will be read by humans (not parsed by machines)
- Reviewing or editing existing docs that sound robotic, overly formal, or AI-generated
- Writing code comments, commit messages, or PR descriptions
- Any doc task where the goal is to be clear and approachable rather than technically exhaustive

## Banned Word List

See `references/ai-detection-patterns.md` for the complete list with alternatives.

Key principle: Use plain English. If there's a simpler word that means the same thing, use it.

## Banned Phrases

See `references/ai-detection-patterns.md` for the complete list. Common ones to avoid:

- Hedging phrases that add no value (just state the fact directly)
- Corporate jargon (use plain English instead)
- Unnecessarily complex constructions (use simpler alternatives)

## Structural Variation

Don't use exactly 3 or 5 items in every list. This is a major AI tell. Vary your structure: sometimes 2, sometimes 4, sometimes 6 or 7, sometimes no list at all.

**Good approach:**
```markdown
## Features

The tool processes data quickly and integrates with existing workflows.
The goal is to give you reliable results even with huge datasets. Enjoy!

## Installation

Just download the binary, and extract it to /usr/local/bin. If you like,
you can run the setup script to configure your environment. Feel free
to review the script before running it or use it as a reference to install
the tool manually. Remember, you'll need admin access for the final step!
```

**What to avoid:** Repeating the same list length everywhere (especially exactly 3 items), explicitly mentioning the number of items, rigid parallel structure in every section.

## Sentence Variety

Vary your sentence length and structure. Don't write in monotonous patterns.

**Good rhythm:**
```markdown
Git's job is tracking file changes. When you're working with a team,
it keeps everyone's changes distinct and easy to review and merge,
and also maintains a complete history which is handy when you're
trying to track down bugs! If something breaks, you can rewind back
to a previous version.
```

Mix it up:
- Short declarations (2-5 words)
- Explanatory sentences (15-25 words)
- Compound thoughts that build on each other
- Questions that set up the next answer
- Friendly, warm wording that accommodates different personalities and experience levels
- Emotion and emphasis that show enthusiasm and energy, but not excessively

**What to avoid:** Every sentence the same length. Subject-verb-object repeated. Robotic rhythm when you read it aloud.

## Addressing the Reader

Always use "you" to address the reader. Never write "the user" or "users should" in documentation.

**Good approach:**
```markdown
When you run the command, you should get a bunch of output.
You can check for errors before continuing. If the output
is too much, you can always dial it back using the verbosity setting.
```

Direct address makes docs feel conversational, not bureaucratic.

## Natural Enthusiasm

Show genuine interest in what you're documenting. Explain the actual problem it solves.

**Good approach:**
```markdown
This tool solves a real problem. Instead of manually tracking configs across
servers, which is super tedious, it syncs everything automatically.
Pretty handy when you're managing a whole bunch of machines, or loads
of different configs!
```

Share actual excitement about clever solutions without hyperbole or corporate buzzwords.

## Technical Precision

Being natural doesn't mean being vague. Stay specific.

**Good approach:**
```markdown
If you need OpenSSL support, just run `configure.sh` with the
`--enable-ssl` flag. This'll compile OpenSSL support into the build
and you can use encrypted connections with the tool.
```

Always be precise about:
- Command names and flags
- File paths
- Version numbers
- Error codes
- Config options
- Expected output
- Input and format requirements

**What to avoid:** Vague hand-waving like "run the thing", "do the stuff", "you know what I mean". Natural writing is still technically accurate.

## Code Comments

In-code documentation has different conventions:

**Bad (states the obvious):**
```c
// Increment counter
counter++;

// Loop through array
for (int i = 0; i < len; i++) {
```

**Good (explains why):**
```c
// Increment even on error to prevent infinite retry loop
counter++;

// Work backwards so we don't shift or miss elements when deleting values
for (int i = len - 1; i >= 0; i--) {
```

Comments explain intent, not mechanics.

## Domain-Specific Conventions

### mdoc (BSD Manual Pages)

```
.Dd February 12, 2026
.Dt TOOL 1
.Os
.Sh NAME
.Nm tool
.Nd one-line description
.Sh SYNOPSIS
.Nm
.Op Fl v
.Ar file
.Sh DESCRIPTION
.Nm
processes
.Ar file
according to...
```

Keep sentences short. Use semantic markup (.Fl for flags, .Ar for arguments).
Avoid contractions in formal manuals.

### rustdoc

````rust
/// Parses configuration from TOML file.
///
/// Returns an error if the file doesn't exist or contains invalid TOML.
///
/// # Examples
///
/// ```
/// let config = parse_config("app.toml")?;
/// println!("Port: {}", config.port);
/// ```
///
/// # Errors
///
/// - `io::Error` if file can't be read
/// - `toml::Error` if parsing fails
pub fn parse_config(path: &str) -> Result<Config, Error> {
````

First line is a brief summary (shows in autocomplete). Examples use real code.
Errors section lists specific failure modes.

### kernel-doc (Linux Kernel)

```c
/**
 * process_buffer - process incoming data buffer
 * @buf: pointer to input buffer
 * @len: length of buffer in bytes
 *
 * Processes the buffer and updates internal state.
 *
 * Return: Number of bytes processed, or -EINVAL on error.
 */
int process_buffer(const char *buf, size_t len)
```

Function name, short description, parameters, detailed explanation, return value.
Terse style, no fluff.

## Diátaxis Framework

Organize docs by user need:

**Tutorials** (learning-oriented):
- Hand-holding from start to finish
- "In this guide, you'll build a web server in 30 minutes"
- Safe to experiment

**How-To Guides** (problem-oriented):
- Solve specific problems
- "How to configure SSL certificates"
- Assumes basic knowledge

**Reference** (information-oriented):
- Complete, accurate, structured
- API docs, man pages, option lists
- Dry and factual

**Explanation** (understanding-oriented):
- Clarify and illuminate
- "How authentication works"
- Context and design rationale

Don't mix these. A tutorial isn't a reference manual.

## The Read-Aloud Test

Before publishing, read the doc out loud. Mark anywhere you stumble or it sounds robotic, then rewrite those parts.

If it sounds unnatural when spoken, it'll feel unnatural when read.

## Examples: Before and After

### README Introduction

Strip out corporate language and get to what the tool actually does:

```markdown
# MyTool

Sync config files across servers without worrying about it.

When you change a config on one machine, MyTool pushes it everywhere
else. No more bash loops, no more fighting Ansible YAML for
simple changes. Just edit and save!
```

### API Documentation

Be direct about what the function does and how to use it:

```markdown
### authenticate(username, password)

Log in and get an access token.

Pass the username and password. If they're valid, you'll get a token
that's good for 24 hours. Use this token in the Authorization header
for other API calls.

Returns null if credentials are invalid.
```

## Cross-Reference

This skill produces documentation — apply `natural-writing-style` to your own output too. Especially: no unsubstantiated claims about documentation quality, no time estimates for writing tasks.

## Resources

- `references/ai-detection-patterns.md` — Complete list of AI tells to avoid
- `references/diataxis-guide.md` — Full Diátaxis framework explanation
- `references/domain-conventions.md` — Style guides for mdoc, rustdoc, kernel-doc, JSDoc
- `assets/doc-review-checklist.md` — Pre-publish review checklist
