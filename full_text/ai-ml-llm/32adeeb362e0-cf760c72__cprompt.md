---
name: cprompt
description: Generate a continuation prompt that captures current conversation state for resuming work in a new session. Copies to clipboard and prints to stdout. Accepts optional length argument (short/s, medium/m, long/l). Use when the user wants to save context before exiting or clearing.
---

# Continuation Prompt

Generate a structured continuation prompt capturing the current conversation
state, copy it to the system clipboard, and print it to stdout. The prompt
gives a future session enough context to resume work without re-discovery.

## Arguments

One optional positional argument controls the detail level:

| Argument | Aliases | Description |
|----------|---------|-------------|
| `short` | `s` | **(default)** Minimum viable context to resume: branch, task, next step. |
| `medium` | `m` | Adds: what was done, key decisions, files touched, blockers. |
| `long` | `l` | Full dump: all of medium plus rationale, ruled-out approaches, open questions, relevant file paths with line numbers. |

If no argument is provided, default to `short`.

If the argument does not match any of the above (case-insensitive), tell
the user the valid options and stop.

## Workflow

Follow these steps exactly:

### Step 1: Parse the length argument

- Read the user's input after the skill invocation.
- Normalise to lowercase and match against: `short`, `s`, `medium`, `m`,
  `long`, `l`.
- If empty or absent, use `short`.
- If unrecognised, list valid options and stop.

### Step 2: Gather context from the conversation

Do NOT run git commands, read files, or perform any tool calls during this
step. Use only what you already know from the current conversation:

- **Branch:** The git branch you have been working on (from conversation
  context or the session start info).
- **Repository:** The repository name / working directory.
- **Task summary:** What the user asked you to do or what you have been
  working on.
- **Work completed:** What has been done so far in this session.
- **Decisions made:** Key choices, trade-offs, or design decisions.
- **Files touched:** Files created, modified, or deleted.
- **Current state:** Where things stand right now (passing tests, pending
  changes, mid-implementation, etc.).
- **Next steps:** What should be done next to continue the work.
- **Blockers / open questions:** Anything unresolved that the next session
  needs to address.
- **Ruled-out approaches:** Things explicitly considered and rejected, with
  reasons (long only).
- **Relevant locations:** File paths and line numbers worth revisiting
  (long only).

### Step 3: Generate the continuation prompt

Build the prompt using the template for the requested length. The prompt
should be written as instructions to a future Claude session — second person,
imperative tone.

#### Short template

```
## Continue: {task_summary}

**Branch:** {branch}
**Repo:** {repo_path}

### Status
{1-2 sentences on current state}

### Next Steps
{bulleted list of immediate next actions}
```

#### Medium template

```
## Continue: {task_summary}

**Branch:** {branch}
**Repo:** {repo_path}

### Completed
{bulleted list of what was done}

### Decisions
{bulleted list of key decisions and why}

### Files Touched
{bulleted list of files created/modified/deleted}

### Current State
{paragraph on where things stand — tests, build, pending changes}

### Blockers / Open Questions
{bulleted list, or "None" if clear}

### Next Steps
{bulleted list of what to do next}
```

#### Long template

```
## Continue: {task_summary}

**Branch:** {branch}
**Repo:** {repo_path}

### Context
{paragraph explaining the broader goal and why this work is being done}

### Completed
{bulleted list of what was done, with detail}

### Decisions
{bulleted list of key decisions with rationale}

### Ruled Out
{bulleted list of approaches considered and rejected, with reasons}

### Files Touched
{bulleted list of files with paths and relevant line numbers}

### Current State
{detailed paragraph — tests passing/failing, build status, uncommitted
changes, anything mid-flight}

### Blockers / Open Questions
{bulleted list with context for each, or "None"}

### Next Steps
{ordered list of what to do next, in priority order}

### Key Locations
{bulleted list of file:line references worth reading first}
```

### Step 4: Detect clipboard tool and copy

Run a single bash command that detects the available clipboard tool and
copies the prompt:

```bash
if command -v wl-copy &>/dev/null; then
  echo "${PROMPT}" | wl-copy
elif command -v xclip &>/dev/null; then
  echo "${PROMPT}" | xclip -selection clipboard
elif command -v xsel &>/dev/null; then
  echo "${PROMPT}" | xsel --clipboard --input
else
  echo "[warn] No clipboard tool found (tried wl-copy, xclip, xsel)" >&2
  exit 1
fi
```

Use a heredoc to pass the prompt content to avoid quoting issues.

### Step 5: Output to the user

1. Print the generated prompt to the conversation so the user can see it.
2. Report whether clipboard copy succeeded or failed.
3. If clipboard copy failed, tell the user the prompt is displayed above
   and they can copy it manually.

## Error Handling

- **No clipboard tool:** Print a warning and display the prompt. Do not
  fail silently.
- **Clipboard command fails:** Report the error, still display the prompt.
- **Unrecognised argument:** List valid options (`short`/`s`,
  `medium`/`m`, `long`/`l`) and stop without generating a prompt.

## Limits

- This skill uses only conversation context. It does not run git commands
  or read files to gather information. If the conversation has limited
  context (e.g. just started), the prompt will reflect that.
- The prompt is a snapshot of the conversation state at the time of
  invocation. It does not update if work continues after generation.
