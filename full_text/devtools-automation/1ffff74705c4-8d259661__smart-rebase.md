---
name: smart-rebase
description: >-
  Orchestrates intelligent git rebases by identifying the merge base between
  the current branch, its upstream tracking branch, and the default branch,
  then carefully reconciling all changes to produce a cleanly mergeable result.
  Use when rebasing a diverged feature branch onto an updated main/master,
  when preparing a branch for merge after the default branch has advanced,
  or when manual rebase conflicts risk clobbering default branch changes.
  Triggers: rebase, merge base, diverged branch, catch up with main,
  rebase onto main, reconcile branches, update feature branch.
license: MIT
metadata:
  version: 1.0.0
  author: james
  last-modified: 2026-02-12
allowed-tools: Bash(git *) AskUserQuestion
---

# Smart Rebase

Safely rebase a diverged feature branch onto an updated default branch without clobbering changes on either side.

## Quick Start

When the user asks to rebase, catch up with main, or reconcile a diverged branch:

1. Run the **Discovery** phase to map branch topology and find the merge base
2. Run the **Analysis** phase to categorize every change on both sides of the divergence
3. Run the **Execution** phase to perform the rebase, resolving conflicts with full context
4. Run the **Verification** phase to confirm nothing was lost

**The cardinal rule:** Never silently discard a change from the default branch. Every default-branch change must either be preserved as-is or explicitly reworked to fit the current branch's architecture. If you're uncertain about a change, flag it for the user — don't guess.

## When to Use This Skill

- Rebasing a feature branch onto main/master after the default branch has received new commits
- Preparing a long-lived branch for merge when significant divergence exists
- Resolving complex rebase conflicts where you need full context of what changed on each side
- Any situation where a naive `git rebase main` risks losing or overwriting default branch work

## Phase 1: Discovery

Map the branch topology. Run these commands and present the results to the user before proceeding.

**Identify branches:**
```bash
# Current branch
CURRENT=$(git rev-parse --abbrev-ref HEAD)

# Upstream tracking branch (may not exist)
UPSTREAM=$(git rev-parse --abbrev-ref "@{upstream}" 2>/dev/null || echo "none")

# Default branch — check remote HEAD, fall back to main/master detection
DEFAULT=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
if [ -z "$DEFAULT" ]; then
  for candidate in main master; do
    git show-ref --verify --quiet "refs/remotes/origin/$candidate" && DEFAULT=$candidate && break
  done
fi

# Fetch latest state from remote
git fetch origin "$DEFAULT" --quiet
```

**Find the merge base:**
```bash
MERGE_BASE=$(git merge-base HEAD "origin/$DEFAULT")
```

**Measure divergence:**
```bash
# Commits on default branch since merge base
DEFAULT_COMMITS=$(git rev-list --count "$MERGE_BASE..origin/$DEFAULT")

# Commits on current branch since merge base
CURRENT_COMMITS=$(git rev-list --count "$MERGE_BASE..HEAD")

# If upstream exists, commits on upstream since merge base
if [ "$UPSTREAM" != "none" ]; then
  UPSTREAM_COMMITS=$(git rev-list --count "$MERGE_BASE..$UPSTREAM")
fi
```

**Present the topology to the user:**

```
Branch topology:
  Default branch:  origin/{DEFAULT}  ({DEFAULT_COMMITS} commits ahead of merge base)
  Current branch:  {CURRENT}         ({CURRENT_COMMITS} commits ahead of merge base)
  Upstream:        {UPSTREAM}         ({UPSTREAM_COMMITS} commits ahead of merge base)
  Merge base:      {MERGE_BASE_SHORT}

  origin/{DEFAULT}:  A---B---C---D---E  (new work on default branch)
                    /
  merge base:  ----X
                    \
  {CURRENT}:        F---G---H---I      (your feature work)
```

**Use `AskUserQuestion`** to present the topology and confirm before proceeding to analysis: "Here's what I found: [topology summary]. Does the merge base look right, or should I investigate further?" Don't proceed until the merge base is confirmed correct.

## Phase 2: Analysis

Categorize every change on both sides. This is the critical step that prevents accidental clobbering.

**Get file-level change summaries:**
```bash
# Files changed on default branch since merge base
git diff --name-status "$MERGE_BASE" "origin/$DEFAULT"

# Files changed on current branch since merge base
git diff --name-status "$MERGE_BASE" HEAD
```

**Categorize files into buckets:**

| Category | Meaning | Action |
|----------|---------|--------|
| Default-only | Changed only on default branch | Accept automatically during rebase |
| Current-only | Changed only on current branch | Keep as-is, no conflict expected |
| Both-modified | Changed on BOTH branches | Requires careful conflict resolution |
| Default-added | New file on default branch | Accept unless current branch has same path |
| Current-added | New file on current branch | Keep as-is |
| Default-deleted | Deleted on default branch | Accept unless current branch modified it |
| Both-deleted | Deleted on both branches | Clean merge, no action needed |

**For every file in the "Both-modified" bucket, show the user:**

```bash
# What the default branch changed in this file
git diff "$MERGE_BASE" "origin/$DEFAULT" -- path/to/file

# What the current branch changed in this file
git diff "$MERGE_BASE" HEAD -- path/to/file
```

**You'll also want to examine commit-level context for both-modified files:**

```bash
# Commits on default branch that touched this file
git log --oneline "$MERGE_BASE..origin/$DEFAULT" -- path/to/file

# Commits on current branch that touched this file
git log --oneline "$MERGE_BASE..HEAD" -- path/to/file
```

Present this analysis as a structured summary. The user needs to understand the full picture before the rebase begins. Don't skimp on detail here — better to over-explain than to miss a critical conflict pattern.

## Phase 3: Execution

**Pre-flight checks:**

```bash
# Ensure clean working tree
git status --porcelain

# If dirty, stash or commit first
git stash push -m "smart-rebase: pre-rebase stash"

# Create safety backup branch
git branch "backup/${CURRENT}-pre-rebase-$(date +%Y%m%d-%H%M%S)"
```

**Strategy: Current-branch-wins rebase**

The default strategy preserves the current branch's intent and reworks default branch changes to fit. This means:

- When the same function was modified on both branches, keep the current branch version but ensure the default branch's *intent* (bug fix, new feature, refactor) is also reflected
- When the default branch added code that the current branch restructured around, adapt the new code to the current branch's architecture
- When the default branch deleted something the current branch still uses, keep it but note the upstream intent to remove it
- When the default branch refactored code that the current branch also changed, evaluate whether the refactoring pattern improves the current branch's version

The key insight: you're not asking "which version is right?" You're asking "how do I preserve the default branch's intent within the current branch's structure?"

**Execute the rebase:**

```bash
git rebase "origin/$DEFAULT"
```

**When conflicts occur, for EACH conflicted file:**

1. **Read the conflict markers** to understand what git couldn't auto-merge
2. **Recall the analysis** from Phase 2 — you already know what both sides intended
3. **Resolve using the current-branch-wins strategy:** start with the current branch version as the base, review what the default branch intended to change, and integrate the default branch's intent into the current branch's code structure. If the default branch fixed a bug, apply that fix within the current branch's architecture. If the default branch added a feature, port it to work within the current branch's patterns. If the default branch refactored something, decide whether that refactor applies given the current branch's changes.
4. **Stage the resolution** and continue:
   ```bash
   git add path/to/resolved/file
   git rebase --continue
   ```

**If a conflict's too complex or ambiguous:**
- Stop and present both versions to the user with full context
- Explain what each side intended and propose a resolution
- Ask for confirmation before applying

**If the rebase goes sideways:**
```bash
git rebase --abort
# The backup branch is still there
```

## Phase 4: Verification

After the rebase completes, verify nothing was lost.

**Compare default branch state:**
```bash
# Every file on origin/DEFAULT at its current state should either:
# 1. Exist identically in the rebased branch (default-only changes preserved)
# 2. Exist in a modified form that incorporates the default branch's intent
#    (both-modified files where current branch wins but integrates default intent)

# Quick check: files that exist on default but not on rebased branch
git diff --name-only "origin/$DEFAULT" HEAD --diff-filter=D
```

**Compare against pre-rebase state:**
```bash
# The backup branch lets you see what you had before
git diff "backup/${CURRENT}-pre-rebase-*" HEAD --stat

# Verify your feature commits are all represented
git log --oneline "origin/$DEFAULT..HEAD"
```

**Check for accidentally reverted default branch changes:**
```bash
# This is the key safety check. For each commit on the default branch,
# verify its changes are present in the rebased result.
for commit in $(git rev-list "$MERGE_BASE..origin/$DEFAULT"); do
  # Files this commit touched
  files=$(git diff-tree --no-commit-id --name-only -r "$commit")
  for file in $files; do
    # Compare the file on default branch vs rebased branch
    # If they differ, flag for review
    if ! git diff --quiet "origin/$DEFAULT" HEAD -- "$file" 2>/dev/null; then
      echo "REVIEW: $file differs from default branch (commit: $(git log --oneline -1 $commit))"
    fi
  done
done
```

**For any flagged files**, explain to the user:
- What the default branch's version looks like
- What the rebased branch's version looks like
- Why they differ (the current branch's modifications that intentionally diverge)
- Confirm the user is satisfied with the resolution

**Final steps:**
```bash
# If upstream tracking branch exists, force-push to update it
# ALWAYS ask the user before force-pushing
git push --force-with-lease origin "$CURRENT"
```

## Handling Edge Cases

**No upstream tracking branch:**
Skip upstream analysis. Work only with current branch and default branch.

**Merge base is the default branch HEAD:**
The branch isn't actually diverged — it's already up to date. No rebase needed. Tell the user.

**Merge base is the current branch HEAD:**
The current branch's behind the default branch with no new commits. A simple fast-forward works:
```bash
git merge --ff-only "origin/$DEFAULT"
```

**Uncommitted local changes:**
Stash them before starting, pop them after the rebase completes. Warn the user about potential stash conflicts.

**Large divergence (100+ commits on either side):**
Warn the user this will be a long process. Consider breaking it into chunks: rebase onto an intermediate commit first, then onto the latest default branch.

**Submodules or generated files:**
Flag these during analysis. Generated files should typically be regenerated after rebase rather than manually resolved. Submodule pointer conflicts need special handling.

## What This Skill Does NOT Do

- Multi-level stacked branch rebases (branch off a branch off main)
- Merge-based workflows (this is rebase-only)
- Automatic test running (suggest it during verification, but don't mandate it)
- Rewriting commit history beyond what rebase naturally does

## References

- See [conflict-patterns.md](references/conflict-patterns.md) for detailed conflict resolution patterns and examples
