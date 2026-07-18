---
name: up-down-verify
aliases: [design-verify, code-integrity-audit, architecture-consistency-check]
description: >
  Bottom-up/top-down codebase integrity verification. Infers a design document
  from code alone (excluding all existing design docs), then systematically
  verifies consistency between the inferred design and the implementation.
  Use when asked to verify codebase integrity, check code-design consistency,
  audit a project for drift, or run an "up-down" analysis on any repository.
tags: [code-audit, design-verification, integrity-check, architecture-review]
keywords:
  - code-review
  - consistency-check
  - design-verification
  - integrity-audit
  - code-quality
  - architecture-validation
  - design-drift
  - codebase-audit
prerequisites: bash 4+, git, rsync, GNU find
---

# Up-Down Process Integrity Verification

Systematically verify codebase integrity by inferring design from code (UP),
then checking code against that design (DOWN), iterating until consistent.

## Overview

```
PREPARE → UP (infer design) → DOWN (verify) → loop → OUTPUT (proposals) → DESIGN GATE → APPLY
```

The key insight: by excluding all design documents during inference, you get an
unbiased view of what the code *actually does* vs what someone *intended*.

Every pass re-infers the design from scratch — this prevents the design doc
from accumulating assumptions that were never verified against the code.

**Key differentiator:** Catches semantic bugs that pass tests and linting.
Example: code that calls a tokenizer correctly but with the wrong argument
structure for the model's training format. These bugs silently degrade quality
rather than failing loudly.

### What This Catches
- **Structural bugs**: Logic errors, incorrect invariants, boundary mismatches (high signal)
- **Hidden coupling**: Undocumented dependencies, version drift (medium signal)
- **Maintenance debt**: Dead code, duplicated logic, fragile patterns (lower signal, valuable for long-term health)

### What This Does NOT Replace
Unit tests (behavior), static analysis (types), linting (style).

### Expected Findings per Run
- 0-2 real bugs (logic errors, boundary mismatches)
- 2-5 coupling/consistency issues (maintenance risks)
- 5-15 advisories (cleanup opportunities, dead code, ambiguities)

Best used when: integrating unfamiliar code, auditing for drift, onboarding to
a codebase, or before/after major refactors.

## When to Use This Process

**Ideal for:**
- Production systems with 20-100 files (the sweet spot)
- Projects with moderate complexity (not trivial scripts, not massive monorepos)
- Code that's been accumulating drift (3+ months since last deep review)
- Onboarding to an unfamiliar codebase (the UP phase is a learning tool)
- Pre/post-refactor validation (baseline before, verify after)
- Legacy code rescue (discover hidden assumptions)
- Critical systems where cost of undetected bugs >> analysis cost

**Not recommended for:**
- Tiny projects (<10 files) — just read the code directly
- Massive monorepos (>200 files) — partition into subsystems first
- Actively developed code with CI/tests — linting + tests + PR reviews are cheaper
- Pre-alpha code where design is still fluid

**Monorepo strategy:** Run on logical subsystems independently (e.g.,
`services/api/`, `services/worker/` as separate runs), not the entire repo.

## Cost Estimation

| Codebase | Files | Passes | Tokens | Time | Cost (Sonnet) | Cost (Opus) |
|----------|-------|--------|--------|------|---------------|-------------|
| Small    | 20    | 2      | ~350K  | ~12m | ~$1           | ~$10        |
| Medium   | 40    | 2      | ~700K  | ~25m | ~$2           | ~$20        |
| Large    | 100   | 2-3    | ~1.5M  | ~50m | ~$5           | ~$45        |

**Rough heuristic:** ~15-20K tokens per file (depends on LOC and complexity).
Scaling is sublinear with file count (shared context) but superlinear with
coupling density. For >100 files, run on a subsystem first.

**Value comparison:** A senior engineer doing the same systematic review would
take 3-4 hours and cost $300-600. The process trades compute for human time,
with the added benefit of systematic coverage (humans skip sections; the
UP-DOWN process does not).

## Prerequisites

- **bash** >= 4.0
- **git** (with user.name/email configured, or the script will set defaults)
- **rsync**
- **GNU find**
- **Claude Code** (or compatible LLM CLI) for UP/DOWN/OUTPUT phases

## Orchestration Modes

This skill supports two execution modes:

**CLI mode** (manual): Run Claude Code commands directly in the terminal.
The examples below use this format.

**Agent mode** (orchestrated): When an OpenClaw agent runs this skill, use
`sessions_spawn` to launch each phase as a sub-agent. The sub-agent works
in the temp directory and reports back when done. See
[Agent Mode Orchestration](#agent-mode-orchestration) for a complete example.

Both modes follow the same process — only the invocation differs.

## Quick Start

Run a full analysis on a codebase in 5 commands:

```bash
# 1. Prepare workspace
WORKDIR=$(bash scripts/prepare.sh /path/to/your/codebase)
cd "$WORKDIR"

# 2. UP phase: infer design (requires Claude Code in plan mode)
claude --permission-mode plan -p \
  "Explore this codebase systematically and write a design doc to \
  _updown/design.md following _updown/design-template.md. Remove all \
  placeholder comments. Do not read .md files."

# 3. Commit design and verify it was written
[[ -s _updown/design.md ]] || { echo "ERROR: design.md not produced"; exit 1; }
git add _updown/design.md && git commit -m "UP pass 1: design inference"

# 4. DOWN phase: verify design against code
claude -p "Read _updown/design.md and _updown/categories.md. Verify every claim \
  against code. Fix HIGH PRIORITY inconsistencies, commit each fix individually. \
  Append LOW PRIORITY findings to _updown/advisories.md. When done: git add -A && git tag pass-1"

# 5. Check convergence
COMMITS=$(git rev-list --count baseline..pass-1 -- ':!_updown/')
echo "Code-changing commits: $COMMITS"
# If 0: converged → run OUTPUT step
# If >0 and iteration < 3: repeat from step 2 with pass N+1
# If iteration = 3: force-stop → run OUTPUT step

# 6. OUTPUT: generate proposal
claude -p "Generate change proposal from git history. Read git log and diffs, \
  plus _updown/advisories.md. Write to _updown/proposal.md. Ignore prior conversation."

# 7. DESIGN GATE: validate proposals against design intent
claude -p "Read _updown/design.md and _updown/proposal.md. For each proposed \
  change, verify it comports with the design intent and specification. Classify \
  each as APPROVED or FLAGGED. Write results to _updown/design-gate.md."

# 8. Review flagged items + apply approved changes
cat _updown/design-gate.md
# Resolve any FLAGGED items, then apply:
bash scripts/cleanup.sh "$WORKDIR" /path/to/original --yes
```

## Step 0: Prepare

Create an isolated working copy. All analysis happens in the temp copy — the
original codebase is never modified until the user approves final proposals.

```bash
# Run the prepare script
WORKDIR=$(bash scripts/prepare.sh /path/to/original/codebase)
# Returns: WORKDIR path (e.g. /tmp/updown-<hash>/)
```

The script:
1. Validates prerequisites (bash 4+, git, rsync, find)
2. Validates the source directory exists and is readable
3. Copies the codebase to a temp directory (source code only — see [Exclusion Rules](#exclusion-rules))
4. Strips design documents
5. Initializes a git repo with a "baseline" commit and tag
6. Creates `_updown/` for the design doc and working files
7. Records the source path (for cleanup.sh safety validation)

**The file size ceiling is the most important filter.** Source code is almost
never >512KB. Data files (JSON dumps, tokenizer vocabs, serialized state)
almost always are. This single rule catches more junk than all extension-based
filters combined.

**All subsequent steps work exclusively in the temp copy.**

## Step 1: UP — Infer Design

Explore the codebase bottom-up and produce a design document, with no access
to any existing design docs. Use Claude Code in plan mode for multi-agent
exploration:

```bash
bash pty:true workdir:$WORKDIR command:"claude --permission-mode plan -p \
  'Systematically explore this entire codebase. Trace from entry points, walk \
  the dependency graph, then sweep for orphaned files. Produce a design document \
  following the format in _updown/design-template.md. Write it to _updown/design.md. \
  **Remove all <!-- placeholder --> comments from the final document.** \
  Do NOT read any .md files in the project — they have been excluded. Focus only \
  on source code, configs, and tests.'"
```

After the design doc is written, validate and commit it:

```bash
# Verify design.md was actually produced
if [[ ! -s "$WORKDIR/_updown/design.md" ]]; then
  echo "ERROR: UP phase did not produce _updown/design.md" >&2
  exit 1
fi
cd $WORKDIR && git add _updown/design.md && git commit -m "UP pass $N: design inference"
```

**Model selection for UP phase:**
- Use Opus for complex/unfamiliar codebases (better invariant inference)
- Use Sonnet for straightforward codebases you understand well
- Plan mode spawns sub-agents; token cost scales with codebase size

### Design Document Format

Use the template at `templates/design-template.md`. Key sections:

- **Overview**: 2-3 sentences — what, who, runtime
- **Component Inventory**: table of component, location, purpose
- **Component Details**: per-component purpose, public interface, dependencies, invariants, side effects
- **Interactions**: how components communicate (caller → callee with data description)
- **Configuration**: config files, schema, loading, validation
- **Cross-Cutting Patterns**: error handling, config, logging, state management

**Invariants are where bugs hide.** They are the primary verification target
in the DOWN phase. Be specific — "handles errors gracefully" is not an
invariant. "Catches IndexError from FAISS and returns empty list" is. Every
invariant must be concrete enough that an agent can read the code and answer
"does this hold? yes or no."

Interactions are the second priority — hidden coupling and boundary mismatches
are caught here.

**Large components (>500 lines, many classes):** Break into sub-components in the
design doc rather than writing a vague high-level summary. See the template for
guidance.

## Step 2: DOWN — Verify Consistency

A single systematic pass through the design document, section by section,
verifying each claim against the code.

### Procedure

Walk through `_updown/design.md` top-to-bottom:

1. **Component Inventory**: For each row, confirm the file exists and the
   one-line purpose is accurate.

2. **Component Details** (for each component):
   - Read the source file
   - Verify purpose matches actual behavior
   - Verify public interface matches actual exports/functions/CLI args
   - Verify dependencies match actual imports
   - **Verify each invariant holds in the code** (the most important check)
   - Verify side effects are accurately listed
   - Check for code not covered by any design section

3. **Interactions**: For each arrow in the interaction map:
   - Verify the caller actually calls the callee as described
   - Verify data structures match at the boundary
   - Verify error propagation across the boundary
   - Check for undocumented interactions (hidden coupling)

4. **Cross-Cutting Patterns**: For each pattern:
   - Verify it is actually consistent across all components that claim to use it
   - Check for components that deviate from the pattern

Flag every inconsistency with a category from `_updown/categories.md`.

### DOWN Phase Output

Create `_updown/findings.md` as a checkpoint log:

```markdown
## Pass N — DOWN Phase Findings

### HIGH PRIORITY (fix in loop)
- [ ] [code-bug] reranker.py:122 — tokenization issue
- [ ] [hidden-coupling] build_graph.py — reads from wrong path

### LOW PRIORITY (advisory only)
- [dead-code] search_daemon.py:242 — duplicate method
- [accidental-behavior] config.py:55 — ENV override pattern
```

As you fix each HIGH PRIORITY item:
1. Make the code change
2. `git add -A && git commit -m "[category] component: description"`
3. Check off the item in findings.md

This creates a checkpoint log that makes progress visible and survives
interruptions (rate limits, crashes).

```bash
bash pty:true workdir:$WORKDIR command:"claude -p \
  'Read _updown/design.md. Walk through it section by section, verifying \
  every claim against the actual code. For each section: \
  \
  1. Component Inventory — confirm each file exists and purpose is correct \
  2. Component Details — read each source file, verify purpose, interface, \
     dependencies, EVERY invariant, and side effects \
  3. Interactions — verify each caller→callee relationship, data structures \
     at boundaries, and check for undocumented interactions \
  4. Cross-Cutting Patterns — verify consistency across all components \
  \
  For each inconsistency, categorize it (see _updown/categories.md). \
  \
  HIGH PRIORITY (fix): code-bug, conflicting-impls, hidden-coupling, \
  incomplete-impl, incomplete-design, design-misread. \
  LOW PRIORITY (advisory): dead-code, accidental-behavior, both-wrong, \
  ambiguous-intent. \
  \
  First, create _updown/findings.md listing ALL findings (checked/unchecked). \
  \
  For each HIGH PRIORITY finding: \
  - If design-misread or incomplete-design: fix _updown/design.md \
  - If code-bug: fix the source code \
  - If conflicting-impls: reconcile the implementations \
  - If hidden-coupling: document in design OR refactor code \
  - If incomplete-impl: finish or remove the partial code \
  Git commit each fix individually: [CATEGORY] component: description \
  Check off the item in _updown/findings.md after committing. \
  \
  For LOW PRIORITY findings: append to _updown/advisories.md with the \
  pass number (e.g. \"## Pass N findings\"). Do not overwrite prior entries. \
  \
  After all fixes: git add -A && git tag pass-$N'"
```

### Convergence Check

Tag and count code-changing commits (all non-updown files, language-agnostic):

```bash
cd $WORKDIR && git tag "pass-$N"
COMMITS=$(git rev-list --count pass-$((N-1))..pass-$N -- ':!_updown/')
```

- **Zero code-changing commits in the DOWN phase**: converged — proceed to Step 3
- **Design-only commits in DOWN phase** (only `_updown/` changed): run one more
  UP→DOWN pass to verify the design corrections don't reveal new code issues.
  If the follow-up pass also has zero code changes, confirmed converged.
- **Any code-changing commits** and iteration < 3: repeat from Step 1 (full UP + DOWN)
- **Iteration = 3**: force-stop, proceed to Step 3 with a note about max iterations

**Convergence rule:** A pass is considered "converged" if
`git diff pass-$((N-1))..pass-$N -- ':!_updown/'` is empty (no changes outside
the `_updown/` working directory). Design-only commits converge the loop.

**Iteration tracking:** The orchestrating agent/script should maintain a counter
starting at 1. Each UP→DOWN cycle increments it. Use this counter in:
- UP commit: `"UP pass $N: design inference"`
- DOWN advisory heading: `"## Pass $N findings"`
- Git tags: `"pass-$N"`

**Oscillation detection:** If the codebase returns to a state seen in an earlier
pass (e.g., Pass 3 undoes Pass 1's fix), this indicates conflicting constraints
that require human resolution. The max iteration limit (3) caps this, but if
you detect oscillation, stop early and flag it in the proposal.

## Step 3: OUTPUT — Propose Changes

**Clear context** means: start with a prompt that explicitly ignores prior
conversation and derives everything from git artifacts. This prevents the
proposal from being biased by the UP/DOWN exploration process. If spawning a
new sub-agent, this happens naturally. If using the same session, prefix the
prompt with "Ignore all prior conversation."

```bash
bash pty:true workdir:$WORKDIR command:"claude -p \
  'You are preparing a change proposal. Do NOT rely on any prior conversation. \
  Read the git log (git log --all --oneline) and diffs (git diff baseline..HEAD). \
  Also read _updown/advisories.md if it exists. \
  \
  Produce a proposal document at _updown/proposal.md following this structure: \
  \
  ## Summary \
  Total changes, iterations taken, convergence status. \
  \
  ## Proposed Changes (ordered by priority) \
  For each change: \
  - Component affected \
  - Category (from categories.md) \
  - What changed and why (from commit message + diff) \
  - Confidence: high / medium / low \
  - The actual diff \
  \
  ## Advisories (lower priority) \
  Dead code, accidental behavior, ambiguous intent — flagged for human review. \
  \
  ## Unresolved \
  Anything that needs domain knowledge to decide.'"
```

Present `_updown/proposal.md` to the user. Await approval per-change.

## Step 3.5: Design Validation Gate

**This is a mandatory checkpoint before any changes are applied to the original
codebase.** The DOWN phase produces locally-correct fixes, but a fix can be
locally correct while violating the broader design intent. This gate prevents
that.

### Why This Gate Exists

The design document (from the UP phase) is the **source of truth** for
architectural intent and specification. Proposed edits must be validated against
it — not just against local correctness. Without this gate:

- A fix might resolve a bug in one component but violate a cross-component
  invariant documented in the design
- A refactor might improve local code quality but break an architectural
  boundary the design deliberately establishes
- An "incomplete implementation" fix might add code that conflicts with the
  design's stated scope or approach

### Procedure

For **each proposed change** in `_updown/proposal.md`:

1. **Identify the relevant design sections.** Which components, interactions,
   invariants, and cross-cutting patterns does this change touch?

2. **Check comport with design intent.** Does the change align with the
   *purpose* and *architectural role* of the affected components as described
   in `_updown/design.md`?

3. **Check comport with design specification.** Does the change preserve all
   invariants, interface contracts, and interaction patterns specified in the
   design?

4. **Classify the change:**

   - **✅ APPROVED** — The change clearly comports with both design intent and
     specification. It can be applied to the original repo.

   - **⚠️ FLAGGED** — The change conflicts with the design intent or
     specification in one or more ways. It requires user resolution before
     being applied.

### Flagging Conflicts

When a change is flagged, document the conflict in `_updown/design-gate.md`
with enough context for the user to make an informed decision:

```markdown
## Design Gate Results

### Change: [category] component: description
**Status:** ⚠️ FLAGGED
**Conflict:** Violates invariant X in design section Y

**Possible resolutions:**
1. **Design intent is wrong** — The inferred design misunderstood the
   architectural purpose. The edit is correct; update the design.
2. **Specification is incorrect** — The design captured the wrong invariant
   or interface contract. The edit is correct; fix the spec.
3. **Edit is locally correct but violates a cross-component invariant** —
   The edit fixes a real issue in this component but would break assumptions
   in component Z. Needs coordinated fix across both.
4. **Architectural rethink needed** — The conflict reveals a deeper tension
   in the design that can't be resolved by tweaking one component. Requires
   stepping back and reconsidering the approach.
5. **Accept as-is** — The user understands the conflict and wants to apply
   the change anyway (with documented rationale).
```

**The user decides all flagged conflicts — the agent never overrides design
intent.** Present the flagged items with clear resolution options and wait for
the user to choose.

### Gate Output

The gate produces `_updown/design-gate.md` containing:
- A list of all proposed changes with their gate status (✅ or ⚠️)
- For each ⚠️ item: the specific conflict and resolution options
- A summary count: N approved, M flagged

Only ✅ APPROVED changes proceed to the apply step. ⚠️ FLAGGED changes are
held until the user resolves them.

### CLI Usage

```bash
# Run the design validation gate manually
claude -p \
  "Read _updown/design.md (the design document — source of truth for intent \
  and specification) and _updown/proposal.md (proposed changes). \
  \
  For each proposed change: \
  1. Identify which design sections (components, invariants, interactions) it touches \
  2. Verify the change comports with the design INTENT (architectural purpose) \
  3. Verify the change comports with the design SPECIFICATION (invariants, contracts) \
  4. Classify as APPROVED (comports) or FLAGGED (conflicts) \
  \
  Write results to _updown/design-gate.md: \
  - For APPROVED changes: brief confirmation of which design elements support it \
  - For FLAGGED changes: the specific conflict, affected design sections, and \
    resolution options (wrong intent / wrong spec / cross-component violation / \
    architectural rethink / accept as-is) \
  \
  End with summary: N approved, M flagged. \
  The design document is the source of truth. When in doubt, flag."
```

## Step 4: Apply and Cleanup

After the design validation gate:
1. Apply **only ✅ APPROVED** changes to the **original** codebase
2. Present ⚠️ FLAGGED changes to the user for resolution
3. Delete the temp directory after all changes are handled

```bash
# Apply only approved changes (default — validates against design-gate.md):
bash scripts/cleanup.sh $WORKDIR /path/to/original/codebase

# Apply all changes, skipping the design gate (use only if gate was done manually):
bash scripts/cleanup.sh $WORKDIR /path/to/original/codebase --skip-gate

# Non-interactive mode (agent/CI — only applies approved changes):
bash scripts/cleanup.sh $WORKDIR /path/to/original/codebase --yes
```

The cleanup script:
- Validates WORKDIR is a `/tmp/updown-*` path (safety check)
- Validates the original path matches the one used in prepare (prevents applying to wrong codebase)
- Checks for `_updown/design-gate.md` — if present and flagged items exist,
  generates a patch containing **only approved changes** (per-commit filtering)
- If `--skip-gate` is passed or no gate file exists, applies all changes (legacy behavior)
- Generates a patch and tests if it applies cleanly
- Copies the proposal and design gate results to the original codebase
- Deletes the temp directory (with `--yes` for non-interactive mode)

## Agent Mode Orchestration

When running from conversation or automation, structure it as a state machine:

### Step 0: Prepare (main agent)

```python
# Run prepare.sh, extract WORKDIR
result = exec("bash /path/to/skills/up-down-verify/scripts/prepare.sh /path/to/codebase")
WORKDIR = result.stdout.strip().split("WORKDIR=")[1]
```

### Loop (while not converged and iteration < 3):

**Step 1: UP phase (spawn sub-agent)**
```python
sessions_spawn(
    model="opus",  # UP requires strong reasoning
    task=f"""
    You are in {WORKDIR}. This is a temporary copy of a codebase.
    Your task: Infer a design document from source code ONLY.

    1. Read the template: _updown/design-template.md
    2. Explore the codebase systematically (entry points → deps → orphans)
    3. Write _updown/design.md following the template format
    4. Remove all <!-- placeholder --> comments from the final document
    5. DO NOT read any .md files in the project (they've been stripped)
    6. Verify design.md was written and is non-empty
    7. Commit: git add _updown/design.md && git commit -m "UP pass {N}"
    8. Report: "UP phase complete, design written to _updown/design.md"
    """
)
# Wait for sub-agent completion, verify design.md exists
```

**Step 2: DOWN phase (spawn sub-agent)**
```python
sessions_spawn(
    model="opus",
    task=f"""
    You are in {WORKDIR}. A design doc exists at _updown/design.md.
    Your task: Verify every claim in the design against the code.

    1. Read _updown/design.md and _updown/categories.md
    2. Walk through design.md section by section, verifying against code
    3. Create _updown/findings.md listing all findings
    4. For HIGH priority findings: fix code or design, commit each fix
       with format: [category] component: description
    5. For LOW priority findings: append to _updown/advisories.md
    6. Run: git add -A && git tag pass-{N}
    7. Count code commits: git rev-list --count pass-{N-1}..pass-{N} -- ':!_updown/'
    8. Report: "DOWN phase complete, N code-changing commits"
    """
)
# Parse code_commits from report
```

**Step 3: Check convergence (main agent)**
```python
if code_commits == 0:
    break  # converged → proceed to OUTPUT
elif iteration >= 3:
    break  # max iterations → force-stop
else:
    iteration += 1
    continue  # repeat UP→DOWN
```

### Step 4: OUTPUT (spawn sub-agent)
```python
sessions_spawn(
    model="sonnet",  # OUTPUT is mechanical, sonnet sufficient
    task=f"""
    You are in {WORKDIR}. Generate a change proposal from git history.

    1. Read: git log --all --oneline
    2. Read: git diff baseline..HEAD
    3. Read: _updown/advisories.md (if exists)
    4. Write _updown/proposal.md (see SKILL.md for format)
    5. Report: "Proposal written to _updown/proposal.md"
    """
)
```

### Step 4.5: Design Validation Gate (spawn sub-agent)

**This gate is mandatory.** It validates every proposed change against the
design document before anything touches the original codebase.

```python
sessions_spawn(
    model="opus",  # Gate requires strong reasoning about design intent
    task=f"""
    You are in {WORKDIR}. You must validate proposed changes against the
    design document before they can be applied to the original codebase.

    The design document (_updown/design.md) is the SOURCE OF TRUTH for
    architectural intent and specification. Each change must comport with it.

    1. Read _updown/design.md (design intent + specification)
    2. Read _updown/proposal.md (proposed changes)
    3. For EACH proposed change:
       a. Identify which design sections it touches (components, invariants,
          interactions, cross-cutting patterns)
       b. Verify it comports with the design INTENT (architectural purpose
          of affected components)
       c. Verify it comports with the design SPECIFICATION (invariants,
          interface contracts, interaction patterns)
       d. Classify as:
          - APPROVED: clearly comports with design intent + specification
          - FLAGGED: conflicts with design intent or specification
    4. For each FLAGGED change, document:
       - The specific conflict (which design element is violated)
       - Resolution options: wrong intent / wrong spec / cross-component
         violation / architectural rethink / accept as-is
    5. Write results to _updown/design-gate.md
    6. Report: "Design gate complete: N approved, M flagged"

    IMPORTANT: When in doubt, FLAG. The user resolves conflicts, not you.
    Do NOT rationalize away design conflicts to approve more changes.
    """
)
# Parse approved/flagged counts from report
```

**Handling flagged items (main agent):**
```python
gate = read(f"{WORKDIR}/_updown/design-gate.md")
if "FLAGGED" in gate:
    # Present flagged items to user with resolution options
    # User chooses per-item: fix design, fix spec, coordinated fix,
    # rethink, or accept as-is
    # Update design-gate.md with user decisions before proceeding
    pass
```

### Step 5: Present and apply (main agent)
```python
# Read and present proposal + gate results to user
proposal = read(f"{WORKDIR}/_updown/proposal.md")
gate = read(f"{WORKDIR}/_updown/design-gate.md")
# Present to user — only APPROVED changes will be applied
# Flagged changes require user resolution first
# Apply via cleanup.sh --yes (respects design-gate.md)
exec(f"bash scripts/cleanup.sh {WORKDIR} /path/to/original --yes")
```

## Exclusion Rules

The prepare script applies three layers of filtering, in order of importance:

### Layer 1: File size ceiling (default 512KB) — the most important filter

Source code files are almost never >512KB. Data files almost always are.
Any file exceeding the threshold is removed after copy. This catches JSON
data dumps, tokenizer vocabularies, serialized state, and anything else
you'd never think to exclude by extension.

Override with `--max-file-kb N` for codebases with legitimately large source
files. Be aware that large files can degrade UP phase performance.

### Layer 2: Category exclusions (rsync)

| Category | Examples | Rationale |
|----------|----------|-----------|
| Binary models | `*.bin *.pt *.onnx *.safetensors *.h5` | ML weights, not code |
| Vector indexes / DBs | `*.faiss *.db *.sqlite *.lance *.lmdb` | Runtime data |
| Compiled / bytecode | `*.pyc *.so *.dll *.wasm *.class *.jar` | Build artifacts |
| Media | `*.png *.jpg *.mp3 *.mp4 *.ttf *.woff` | Assets, not logic |
| Archives | `*.zip *.tar.gz *.7z *.zst` | Compressed bundles |
| Data serialization | `*.parquet *.arrow *.npy *.npz *.tfrecord` | Dataset files |
| Data files (large) | Caught by size ceiling | JSON dumps, CSV exports, vocab files |
| Logs / temp | `*.log *.bak *.swp *.pid` | Ephemeral |
| Lock files | `package-lock.json pnpm-lock.yaml *.lock` | Dependency pins |
| Data directories | `models/ checkpoints/ versions/ *-cache/` | Runtime data dirs |
| Build directories | `node_modules/ dist/ build/ .venv/ __pycache__/` | Build artifacts |
| Generated code | `*_pb2.py *.generated.* generated/ codegen/` | Mechanical output |

### Layer 3: Design document stripping

| Pattern | Rationale |
|---------|-----------|
| `*.md` | Design docs, READMEs |
| `docs/`, `doc/`, `design/`, `architecture/` | Documentation directories |
| `DESIGN*`, `ARCHITECTURE*`, `SPEC*`, `RFC*` | Named design files |
| `CHANGELOG*`, `CHANGES*`, `LICENSE*` | Non-code text |

**Preserved**: inline code comments, docstrings, type annotations — these are
implementation-level and part of what the code "says about itself."

### Customizing Exclusions for Your Language

The default exclusions cover Python, JavaScript/TypeScript, Rust, Go, Java, and
common polyglot patterns. For other languages or project-specific needs, edit
`prepare.sh` to add exclusions:

```bash
# Additional exclusions you might need:
--exclude='*.csv'          # Data exports
--exclude='*.geojson'      # Map data
--exclude='third_party/'   # Vendored dependencies
```

### Generated Code and Vendored Dependencies

- **Generated code** (protobuf, GraphQL, parsers): Common patterns
  (`*_pb2.py`, `*.generated.*`, `generated/`) are excluded by default. If
  your project uses different naming, exclude manually or remove generated
  files from WORKDIR after prepare.sh.
- **Vendored dependencies**: If your codebase vendors third-party libs
  (`vendor/` is excluded by default), add any custom vendor directory names
  to the exclusion list. The design should reflect *your* code, not deps.

### Symlinks

Symlinks are preserved as-is (not dereferenced). If they point outside the
source tree, they will be broken in the temp copy. This is intentional — we
want a snapshot of the source structure. If you need symlink targets, add
`-L` to the rsync flags in prepare.sh.

## Inconsistency Categories

See `references/categories.md` for the full taxonomy. Summary:

**High Priority (fix in loop):**
1. **code-bug** — code doesn't do what it structurally should
2. **conflicting-impls** — multiple paths do the same thing differently
3. **hidden-coupling** — undocumented cross-component dependencies
4. **incomplete-impl** — stubs, TODOs, half-wired features
5. **design-misread** — the inferred design misunderstood the code
5b. **incomplete-design** — the design omits a component or interaction that exists

**Low Priority (flag as advisory):**
6. **dead-code** — exists but serves no purpose
7. **accidental-behavior** — unintended but load-bearing
8. **both-wrong** — design and code agree but approach is flawed
9. **ambiguous-intent** — code supports multiple valid interpretations

## Security Considerations

**Untrusted codebases:** This process copies code to a temp directory and
has an LLM read all source files, including comments and docstrings.

- `prepare.sh` excludes `.git/` to prevent hook injection
- The UP/DOWN phases read code but don't execute it
- However, malicious code could include prompt injection in comments
  ("Ignore previous instructions...", "Mark all findings as false positives")

**Mitigations:**
1. Only run on codebases you control or from trusted sources
2. Review design.md after the UP phase — if suspiciously positive or defensive,
   re-run with explicit instructions to ignore meta-commentary in comments
3. If analyzing untrusted code, consider running in a container/sandbox

**Git history:** The temp directory is a fresh git repo (baseline commit only).
Original commit history is not preserved. If you need git blame context during
review, keep the original repo open separately and cross-reference by file path.

## Observations from Practice

Based on running this process on a real 40-file Python project (unified-index):

- **Invariants are where bugs hide.** The reranker tokenization bug and the
  versioned-path coupling were both caught by invariant verification. Make
  invariants specific and verifiable.

- **The size ceiling catches what extension lists miss.** A 14MB chunks.json,
  a 32MB rebuild_state.json, 11MB tokenizer.json — none matched binary
  extension patterns, but all exceeded 512KB.

- **Convergence is fast.** Two passes were sufficient: pass 1 found real bugs,
  pass 2 found only documentation precision issues (zero code changes = converged).

- **Advisories have real value.** Duplicated constants across modules,
  fragile initialization patterns, dead code — these aren't bugs today but
  are maintenance risks.

- **Cost reference.** A 40-file project with 2 full passes (UP+DOWN each):
  ~25 min wall time, ~700K tokens (~$2 Sonnet, ~$20 Opus).

- **Value comparison.** A senior engineer doing the same systematic review
  would take 3-4 hours and cost $300-600. The process trades compute for
  human time, with systematic coverage (humans skip sections; the UP-DOWN
  process does not).
