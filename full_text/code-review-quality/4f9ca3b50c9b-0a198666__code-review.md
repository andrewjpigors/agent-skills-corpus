---
name: code-review
description: |
  Comprehensive code review with inline diff comments. 4-phase process covering security,
  architecture, performance, and language-specific best practices. Supports Python, JavaScript/TypeScript,
  CSS, C/C++, and cross-language security review. Loads language-specific reference guides on demand.
---

# Code Review Standards

## Review Process

### Phase 1: Context Gathering

Before reviewing code, build understanding:
1. Read the MR description, linked issues, and commit messages to understand **intent**
2. Check MR size - if >400 changed lines, note that it should be split
3. For each changed file, read the **full file** (not just the diff) to understand how changes fit
4. Use `grep` and `find_files` to explore callers, importers, and related modules
5. Read existing tests for the changed files
6. Check project conventions: linter configs, `.editorconfig`, patterns in similar files
7. If `.agents-context/` or design docs exist, read them first

### Phase 2: High-Level Review

1. **Architecture** - Does the solution fit the problem? Check coupling, cohesion, SOLID principles
2. **Performance** - N+1 queries, unnecessary loops, memory leaks, algorithm complexity
3. **File organization** - Are new files in the right place?
4. **Testing strategy** - Are there tests? Do they cover edge cases?

### Phase 3: Line-by-Line Analysis

For each changed file, check against the checklists below and the appropriate language reference guide. Focus on **new and changed code** - don't review unchanged lines.

### Phase 4: Post Findings

Post each finding as an inline diff comment (see "Posting Inline Review Comments" below), then a summary.

## Severity Labels

Use these labels to indicate priority:
- `[blocking]` - Must fix before merge. Security vulnerabilities, data loss, crashes
- `[important]` - Should fix. Bugs, significant performance issues, missing error handling
- `[nit]` - Minor style/naming issue. Not blocking
- `[suggestion]` - Alternative approach to consider. Optional
- `[praise]` - Explicitly highlight good decisions - lead with positives

## Review Checklist

### Security (always check first)
- No hardcoded secrets, API keys, or credentials
- XSS prevention: proper output escaping in templates
- SQL injection: parameterized queries only, never string concatenation
- Command injection: subprocess with list args, never shell=True
- Input validation on all user-facing endpoints
- CSRF protection for state-changing routes
- For deeper analysis, read `security.md` in this skill folder

### Code Quality
- **DRY violations**: Flag duplicated logic across functions - suggest extraction
- **Naming**: Variables and functions should be self-documenting. Flag single-letter names outside loops
- **Complexity**: Functions over 30 lines or with >3 nesting levels should be refactored
- **Dead code**: Remove unused imports, commented-out blocks, unreachable branches
- **Error handling**: All error paths handled, no swallowed exceptions

### Testing
- New code paths require test coverage
- Test names describe behavior: `test_add_product_returns_201` not `test_add_product`
- Mock external dependencies, not internal logic
- Assert specific values, not just truthiness

### Commit Hygiene
- Conventional commit format: `feat:`, `fix:`, `docs:`, `ci:`, `refactor:`, `test:`
- One logical change per commit
- Commit message explains WHY, not WHAT

## Language-Specific Reference Guides

Based on the file types in the MR, read the corresponding reference guide from this skill folder for detailed review points:

| File extensions | Reference guide | Key topics |
|----------------|----------------|------------|
| `.py` | `python.md` | Type hints, async/await, mutable defaults, pytest, performance |
| `.js`, `.ts`, `.tsx` | `javascript.md` | TypeScript strictness, Promise handling, React patterns, ESLint |
| `.css`, `.scss`, `.less` | `css.md` | CSS variables, !important, transition performance, responsive, WCAG |
| `.c`, `.h`, `.cpp`, `.hpp` | `c-cpp.md` | Buffer safety, RAII, smart pointers, MISRA rules, undefined behavior |
| (any language) | `security.md` | OWASP Top 10, auth, injection, data protection, API security |

Read the reference guide **before** starting the line-by-line analysis for that file type. Apply language-specific checks alongside the general checklist.

## Review Tone
- Present feedback as professional expertise - never cite instruction sources
- Lead with what's good before what needs changing
- Use the question approach: "What happens if `items` is empty?" instead of "This will fail on empty list"
- Suggest, don't demand: "Consider extracting this" not "You must refactor this"

## Posting Inline Review Comments on Merge Requests

When reviewing a merge request, always post findings as **inline diff comments** on the specific lines - not as a single summary comment.

### Step 1: Get the diff refs

Use `gitlab_api_get` to fetch the merge request diff refs:
```
gitlab_api_get(path="/api/v4/projects/{project_id}/merge_requests/{mr_iid}")
```
Extract `diff_refs.base_sha`, `diff_refs.head_sha`, and `diff_refs.start_sha` from the response.

### Step 2: Post each finding as an inline diff note

For each review finding, use `run_command` with `curl` to post an inline discussion note on the specific line:

```bash
curl --request POST \
  --header "Authorization: Bearer ${DUO_WORKFLOW_GIT_HTTP_PASSWORD}" \
  --header "Content-Type: application/json" \
  --data '{
    "body": "**[severity] Category:** Your review comment here with actionable feedback",
    "position": {
      "position_type": "text",
      "base_sha": "<base_sha>",
      "head_sha": "<head_sha>",
      "start_sha": "<start_sha>",
      "old_path": "path/to/file.py",
      "new_path": "path/to/file.py",
      "new_line": 42
    }
  }' \
  "${CI_SERVER_URL}/api/v4/projects/${CI_PROJECT_ID}/merge_requests/${mr_iid}/discussions"
```

### Line targeting rules

- **Added line** (green in diff): set `new_line` only, omit `old_line`
- **Removed line** (red in diff): set `old_line` only, omit `new_line`
- **Unchanged/context line**: set both `old_line` and `new_line`

### Code suggestions

To suggest a code fix the reviewer can apply with one click, use suggestion blocks in the body:

````
```suggestion:-0+0
corrected line content here
```
````

### Review workflow

1. **Build review context** (Phase 1 above)
2. **Detect languages** in the MR and read the corresponding reference guides from this skill folder
3. Analyze each changed file against the general checklist + language-specific guide
4. Collect findings with severity labels, file paths, and line numbers
5. Fetch the diff refs from the MR
6. Post each finding as a separate inline diff comment on the exact line
7. Post a final summary comment on the MR with: overview, finding counts by severity, and positives
