---
name: changelog-generator
description: Automatically creates user-facing changelogs from git commits by analyzing commit history, categorizing changes, and transforming technical commits into clear, customer-friendly release notes. Turns hours of manual changelog writing into minutes of automated generation.
---

# Changelog Generator

This skill transforms technical git commits into polished, user-friendly changelogs that your customers will understand and appreciate.

## Prerequisites

- **Git**: Required for reading commit history
- **Repository access**: Must be run from a git repository root
- **Optional**: Custom changelog style guide (CHANGELOG_STYLE.md)

## Trigger Keywords

Use these phrases to invoke this skill:

- "generate changelog"
- "create release notes"
- "what changed since [version/tag]"
- "summarize recent commits"
- "create changelog from commits"
- "write changelog for [version]"
- "weekly changelog" or "week WXX-YYYY"

## When to Use This Skill

Use this skill when:

- Preparing release notes for a new version
- Creating weekly or monthly product update summaries
- Documenting changes for customers
- Writing changelog entries for app store submissions
- Generating update notifications
- Creating internal release documentation
- Maintaining a public changelog/product updates page

## What This Skill Does

1. **Scans Git History**: Analyzes commits from a specific time period or between versions
2. **Categorizes Changes**: Groups commits into logical categories (features, improvements, bug fixes, breaking changes, security)
3. **Translates Technical → User-Friendly**: Converts developer commits into customer language
4. **Formats Professionally**: Creates clean, structured changelog entries
5. **Filters Noise**: Excludes internal commits (refactoring, tests, etc.)
6. **Follows Best Practices**: Applies changelog guidelines and your brand voice

## How to Use

### Basic Usage

From your project repository, invoke the skill with one of the trigger keywords:

```
Generate a changelog from commits since last release
```

```
Create changelog for all commits from the past week
```

```
Create release notes for version 2.5.0
```

### With Specific Date Range

```
Create a changelog for all commits between March 1 and March 15
```

### With Custom Guidelines

```
Create a changelog for commits since v2.4.0, using my changelog
style from CHANGELOG_STYLE.md
```

### Weekly Changelog (ISO Week Format)

```
Generate a changelog from commits made during week W02-2026
```

```
Create weekly changelog for week W45-2024
```

**Note:** Week format is `W<week_number>-<year>` (e.g., W02-2026 = week 2 of 2026)

### From a Specific Branch

```
Generate a changelog from commits on the develop branch from the past week
```

```
Create changelog for week W02-2026 on the staging branch
```

**Note:** By default, all changelogs are generated from the `master` branch. To analyze a different branch, specify it in your request.

## Workflow

When this skill is invoked, follow these steps:

### Step 1: Determine the Commit Range and Branch

Ask the user or infer from context:

- **Branch**: Which branch to analyze (default: master)
- **Time period**: "past week", "since last release", "this month"
- **Version range**: "since v2.4.0", "between v2.3.0 and v2.4.0"
- **Specific dates**: "March 1 to March 15"
- **Week number**: "W02-2026", "week 45 of 2024"

**Default behavior:** Uses the `master` branch. If the user doesn't specify a branch, always analyze `origin/master` or `master`.

### Step 2: Fetch Commit History

Run the appropriate git command based on the range:

**Default: master branch**

All commands default to the `master` branch. To analyze a different branch, specify it explicitly.

**Since last tag (master branch - default):**

```bash
git log $(git describe --tags --abbrev=0)..origin/master --oneline
```

**Since last tag (specific branch):**

```bash
git log $(git describe --tags --abbrev=0)..origin/develop --oneline
```

**Since specific date:**

```bash
# Master branch (default)
git log origin/master --since="7 days ago" --pretty=format:"%h %s"

# Specific branch
git log origin/develop --since="7 days ago" --pretty=format:"%h %s"
```

**Between versions:**

```bash
# Master branch (default)
git log v2.4.0..origin/master --oneline

# Specific branch (use branch name as second ref)
git log v2.4.0..origin/develop --oneline
```

**Specific date range:**

```bash
# Master branch (default)
git log origin/master --since="2024-03-01" --until="2024-03-15" --oneline

# Specific branch
git log origin/develop --since="2024-03-01" --until="2024-03-15" --oneline
```

**By ISO week number:**

To convert ISO week format (WXX-YYYY) to dates, use the helper script or calculate manually:

**Using the helper script (recommended):**
```bash
# Get the Monday date for a week
./bin/iso-week W09-2026
# Output: 2026-02-23

# Get full week information
./bin/iso-week W09-2026 --full
# Output: Week W09-2026: Monday 2026-02-23 - Sunday 2026-03-01
```

**Manual calculation:**
- W01 starts on the first Monday containing at least 4 days of the new year
- W02 starts 7 days after W01 Monday  
- Each week runs Monday to Sunday

**Example: Week W09-2026**
- Monday: February 23, 2026
- Sunday: March 1, 2026
- Git command:
```bash
git log origin/master --since="2026-02-23" --until="2026-03-02" --oneline
```

**Common 2026 ISO Week dates:**
- W01-2026: Dec 29, 2025 - Jan 4, 2026
- W02-2026: Jan 5-11, 2026
- W03-2026: Jan 12-18, 2026
- W04-2026: Jan 19-25, 2026
- W05-2026: Jan 26 - Feb 1, 2026
- W06-2026: Feb 2-8, 2026
- W07-2026: Feb 9-15, 2026
- W08-2026: Feb 16-22, 2026
- W09-2026: Feb 23 - Mar 1, 2026
- W10-2026: Mar 2-8, 2026

**Command pattern:**
```bash
# Calculate the Monday date for the week, then add 7 days for the "until" date
git log origin/master --since="YYYY-MM-DD" --until="YYYY-MM-DD" --oneline
```

### Step 3: Categorize Commits

Group commits by type (prioritize user-facing changes):

- **Features** (feat:, feature:): New functionality users can use
- **Improvements** (improve:, perf:, enhancement:): Better performance or UX
- **Bug Fixes** (fix:, bugfix:, hotfix:): Issues resolved
- **Breaking Changes** (breaking:, BREAKING:): Changes requiring user action
- **Security** (security:, sec:, fix: security): Security-related fixes
- **Documentation** (docs:): User-facing documentation updates
- **Infrastructure** (ci:, build:, chore:): Internal changes (usually exclude)

### Step 4: Filter and Exclude

**Exclude these commits** from the changelog:

- Test-only changes (test:, tests:, spec:)
- Internal refactoring (refactor:, refactor:)
- Code style/formatting (style:, format:, lint:)
- Dependency updates without user impact (chore(deps):)
- WIP commits (WIP:, wip:, [WIP])
- Pure merge commits ("Merge branch 'xxx' into 'master'") - these represent completed work, focus on the actual feature/bugfix commits within them
- Revert commits (revert:, revert "...") - handle separately if needed

### Step 5: Transform to User-Friendly Language

Convert technical commit messages to customer language:

| Technical                                     | User-Friendly                                       |
| --------------------------------------------- | --------------------------------------------------- |
| "feat: add JWT authentication middleware"     | "Secure authentication with enhanced token support" |
| "fix: resolve N+1 query in products endpoint" | "Faster loading for product listings"               |
| "refactor: extract payment service"           | "Improved checkout reliability"                     |
| "fix: handle null pointer in cart"            | "Fixed crash when removing items from cart"         |

**Guidelines for transformation:**

- Focus on what changed for the user, not how it was implemented
- Remove technical jargon (middleware, endpoint, N+1, etc.)
- Use active voice and present tense
- Lead with the benefit or impact
- Keep it concise (one sentence per item)

### Step 6: Format and Output

Choose the appropriate output format based on use case (see Output Templates below).

Display the generated changelog to the user.

### Step 7: Ask About Saving

**After presenting the changelog, always ask:**

> "Would you like me to add this changelog to CHANGELOG.md?"

**If user says yes:**
- Read the existing CHANGELOG.md file
- Insert the new changelog section after `## [Unreleased]` (or at the top if no Unreleased section)
- Keep the most recent week at the top
- Write the updated file

**If user says no:**
- Simply acknowledge and wait for next request

## Output Templates

### GitHub Release Notes (Default)

```markdown
## What's New in {{VERSION}}

### ✨ New Features

{{FEATURES_LIST}}

### 🔧 Improvements

{{IMPROVEMENTS_LIST}}

### 🐛 Bug Fixes

{{FIXES_LIST}}

### ⚠️ Breaking Changes

{{BREAKING_CHANGES_LIST}}

### 🔒 Security

{{SECURITY_LIST}}
```

### Plain Text (for emails)

```
Updates for {{DATE_RANGE}}

NEW FEATURES:
{{FEATURES_LIST}}

IMPROVEMENTS:
{{IMPROVEMENTS_LIST}}

BUG FIXES:
{{FIXES_LIST}}
```

### JSON (for automation)

```json
{
  "version": "{{VERSION}}",
  "date": "{{DATE}}",
  "features": [{{FEATURES_ARRAY}}],
  "improvements": [{{IMPROVEMENTS_ARRAY}}],
  "fixes": [{{FIXES_ARRAY}}],
  "breaking_changes": [{{BREAKING_ARRAY}}],
  "security": [{{SECURITY_ARRAY}}]
}
```

### App Store Submission

```
• {{FEATURE_1}}
• {{FEATURE_2}}
• {{IMPROVEMENT_1}}
• {{FIX_1}}
```

## Error Handling

### No Commits Found

**Error message:**

```
No commits found in the specified range ({{RANGE}}).

Possible reasons:
- The date range is too narrow
- No commits since the last tag
- Working in a different branch

Try:
- Check `git log` to see recent commits
- Verify you're in the correct repository
- Use a broader date range or different version tag
```

### Invalid Version Tag

**Error message:**

```
Could not find git tag "{{TAG}}".

Available tags:
{{TAG_LIST}}

Please use one of the above tags or specify a date range instead.
```

### No User-Facing Changes

**Warning message:**

```
No user-facing changes found in this range.

The commits found were internal only (refactoring, tests, dependencies).
Consider:
- Using a broader date range
- Checking if changes are in a different branch
- Noting "Internal improvements and bug fixes" in your changelog
```

## Examples

### Example 1: Weekly Update

**User request:** "Create a changelog for commits from the past 7 days"

**Generated output:**

```markdown
# Updates - Week of March 10, 2024

## ✨ New Features

- **Team Workspaces**: Create separate workspaces for different
  projects. Invite team members and keep everything organized.

- **Keyboard Shortcuts**: Press ? to see all available shortcuts.
  Navigate faster without touching your mouse.

## 🔧 Improvements

- **Faster Sync**: Files now sync 2x faster across devices
- **Better Search**: Search now includes file contents, not just titles

## 🐛 Fixes

- Fixed issue where large images wouldn't upload
- Resolved timezone confusion in scheduled posts
- Corrected notification badge count
```

### Example 2: Version Release

**User request:** "Create release notes for version 2.5.0 since v2.4.0"

**Generated output:**

```markdown
## What's New in v2.5.0

### ✨ New Features

- **Dark Mode**: Work comfortably with the new dark theme
- **Export to PDF**: Download your documents as PDF files
- **Custom Templates**: Save and reuse your favorite layouts

### ⚠️ Breaking Changes

- API v1 endpoints are now deprecated and will be removed in v3.0
- Please migrate to API v2 by following our migration guide

### 🔧 Improvements

- 50% faster page load times
- Improved mobile responsiveness
- Better keyboard navigation support

### 🐛 Bug Fixes

- Fixed data export on Safari browsers
- Corrected email notifications for weekly digests
- Resolved login issues with SSO providers

### 🔒 Security

- Updated dependencies to address CVE-2024-XXXX
- Enhanced password validation requirements
```

### Example 3: Weekly Changelog (Week Format)

**User request:** "Generate a changelog from commits made during week W02-2026"

**Process:**

- Week W02-2026 = January 6-12, 2026
- Fetched commits from 2026-01-06 to 2026-01-12

**Generated output:**

```markdown
# Weekly Update - W02-2026 (January 6-12, 2026)

## ✨ New Features

- **Team Notifications**: Real-time alerts when team members update shared
  documents. Never miss important changes.

## 🔧 Improvements

- **Faster Search**: Search results now appear instantly as you type
- **Mobile Experience**: Better touch interactions on tablets

## 🐛 Fixes

- Fixed sync issues when offline for extended periods
- Corrected display of special characters in filenames
```

## Tips

- Run from your git repository root for best results
- Specify clear date ranges or version tags for focused changelogs
- Use your CHANGELOG_STYLE.md for consistent brand formatting
- Always review and adjust the generated changelog before presenting
- Always ask if the user wants to save to CHANGELOG.md after generating
- For release notes, present the formatted output for copy-paste
- For major releases, manually add context and migration notes
- Consider your audience: technical users vs. non-technical customers

## Related Use Cases

- Creating release notes
- Writing app store update descriptions
- Generating email updates for users
- Creating social media announcement posts
- Updating public documentation
- Internal team updates and sprint reviews

## Variables

Use these placeholders when generating output:

- `{{DATE_RANGE}}` - Time period covered (e.g., "March 1-15, 2024")
- `{{WEEK}}` - ISO week number (e.g., "W02-2026")
- `{{VERSION}}` - Target version number (e.g., "v2.5.0")
- `{{PREVIOUS_VERSION}}` - Starting version/tag
- `{{STYLE_GUIDE}}` - Path to custom formatting rules
- `{{FEATURES_LIST}}` - Generated list of new features
- `{{IMPROVEMENTS_LIST}}` - Generated list of improvements
- `{{FIXES_LIST}}` - Generated list of bug fixes
- `{{BREAKING_CHANGES_LIST}}` - Generated list of breaking changes
- `{{SECURITY_LIST}}` - Generated list of security updates
- `{{COMMIT_COUNT}}` - Total number of commits analyzed

---

**Inspired by:** Manik Aggarwal's use case from Lenny's Newsletter
