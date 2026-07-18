---
name: spec-issue-sync
description: Automatically synchronize OpenSpec specification status with GitHub issues. Creates issues when specs are approved, updates issue status as work progresses, and closes issues when specs are completed. Supports bidirectional sync to keep specs and issues aligned throughout the development lifecycle.
---

# Spec-Issue Sync Skill

Automate the synchronization between OpenSpec specifications and GitHub issues for Business Central projects. This skill maintains alignment between specification lifecycle stages and GitHub issue tracking.

## Purpose

Ensure that OpenSpec specifications and GitHub issues remain synchronized throughout the development lifecycle, reducing manual overhead and preventing spec-issue drift.

## When to Use This Skill

**Trigger this skill when the user:**
- Mentions "sync spec with GitHub" or "create issue from spec"
- Requests to "update issue status" or "close issue for spec"
- Wants to "link spec to issue" or "track spec in GitHub"
- Says "create GitHub issue for [spec name]"
- Asks to "update spec status from issue"
- Needs bidirectional sync between specs and issues

**Do NOT use this skill when:**
- User wants to create a new specification (use `bc-release-note-generator` or OpenSpec workflow)
- User wants to create issues unrelated to specs (use `github-issue-creator` skill)
- User is asking about GitHub workflows or Actions (general GitHub questions)

## Workflow

### 1. Spec-to-Issue Sync (Forward)

When a spec transitions to certain states, automatically create or update corresponding GitHub issues.

#### Trigger: Spec Status = "approved"
**Action:** Create GitHub issue

**Process:**
1. Read the spec file from `openspec/` folder
2. Parse YAML frontmatter to extract:
   - title
   - type (feature, enhancement, api, integration)
   - status
   - priority
   - complexity
   - estimated_effort
   - tags
3. Check if `related_issues` field already contains an issue number
4. If no issue exists:
   - Create GitHub issue with:
     - **Title:** `[OpenSpec] {spec.title}`
     - **Body:** 
       ```markdown
       ## OpenSpec Specification
       
       **Spec File:** [`openspec/{path}`](openspec/{path})
       **Type:** {type}
       **Priority:** {priority}
       **Complexity:** {complexity}
       **Estimated Effort:** {estimated_effort}
       
       ## Description
       
       {Extract first paragraph from spec}
       
       ## Implementation Status
       
       - [ ] Spec approved
       - [ ] Implementation started
       - [ ] Testing completed
       - [ ] Documentation updated
       - [ ] Spec marked as completed
       
       ## Acceptance Criteria
       
       {Extract acceptance criteria from spec}
       
       ---
       
       *This issue was automatically created from the OpenSpec specification. Updates to the spec will be reflected here.*
       ```
     - **Labels:** 
       - `openspec`
       - `{type}` (feature, enhancement, api, integration)
       - `priority:{priority}` (critical, high, medium, low)
       - `complexity:{complexity}` (high, medium, low)
     - **Assignees:** Extract from `author` or `reviewers` frontmatter field
     - **Milestone:** Extract from frontmatter if present
5. Update spec file:
   - Add issue number to `related_issues` field in frontmatter
   - Update `updated` timestamp
6. Commit changes with message: `chore: link spec to GitHub issue #{issue_number}`

**Example:**
```yaml
# Before
related_issues: []

# After
related_issues:
  - 42
```

#### Trigger: Spec Status = "in-progress"
**Action:** Update GitHub issue status

**Process:**
1. Read spec file and extract `related_issues`
2. For each related issue:
   - Add label: `status:in-progress`
   - Remove label: `status:ready`
   - Add comment:
     ```markdown
     🚧 **Implementation Started**
     
     The OpenSpec specification has been marked as **in-progress**.
     
     **Spec:** [`openspec/{path}`](openspec/{path})
     **Updated:** {timestamp}
     
     Development work is now underway. This issue will be updated when the implementation is complete.
     ```
   - Check the "Implementation started" checkbox in issue body
3. No spec file update required

#### Trigger: Spec Status = "completed"
**Action:** Close GitHub issue

**Process:**
1. Read spec file and extract:
   - `related_issues`
   - `related_prs` (pull requests that implemented the spec)
2. For each related issue:
   - Add label: `status:completed`
   - Remove labels: `status:in-progress`, `status:ready`
   - Add closing comment:
     ```markdown
     ✅ **Implementation Completed**
     
     The OpenSpec specification has been marked as **completed**.
     
     **Spec:** [`openspec/{path}`](openspec/{path})
     **Completed:** {timestamp}
     
     {if related_prs exists}
     **Related PRs:**
     {list related PRs}
     {endif}
     
     This issue is now closed. The specification will be archived according to the OpenSpec lifecycle.
     ```
   - Check all checkboxes in issue body
   - Close the issue with state reason: "completed"
3. No spec file update required

---

### 2. Issue-to-Spec Sync (Reverse)

When GitHub issues are updated, reflect changes back to the spec.

#### Trigger: Issue Closed (not by automation)
**Action:** Update spec status

**Process:**
1. Search for specs with `related_issues` containing the closed issue number
2. If spec found:
   - Check spec `status` field
   - If status is NOT "completed":
     - Update status to "completed"
     - Update `updated` timestamp
     - Add note to spec body:
       ```markdown
       ## Implementation Notes
       
       Issue #{issue_number} was closed on {date}. Status automatically updated to completed.
       ```
     - Commit with message: `chore: mark spec as completed (issue #{issue_number} closed)`

#### Trigger: Issue Reopened
**Action:** Alert spec owner

**Process:**
1. Search for specs with `related_issues` containing the reopened issue number
2. If spec found:
   - Add comment to issue:
     ```markdown
     ⚠️ **Spec Status Alert**
     
     The related OpenSpec specification is currently marked as **{status}**.
     
     **Spec:** [`openspec/{path}`](openspec/{path})
     
     If work needs to resume, please update the spec status to `in-progress` and document any new requirements or changes.
     ```
   - Do NOT automatically change spec status (requires manual review)

---

### 3. Batch Operations

#### Sync All Specs
**Trigger:** User asks "sync all specs with GitHub"

**Process:**
1. Search `openspec/` for all `.spec.md` files
2. For each spec:
   - Parse frontmatter
   - Check status:
     - If "approved" and no `related_issues`: Create issue
     - If "in-progress" and has `related_issues`: Update issue labels
     - If "completed" and has open `related_issues`: Close issues
3. Generate summary report:
   ```markdown
   ## OpenSpec GitHub Sync Report
   
   **Date:** {timestamp}
   
   ### Actions Taken
   
   - ✅ Created {count} new issues
   - 🔄 Updated {count} existing issues
   - ✅ Closed {count} completed issues
   
   ### Details
   
   {list each spec with action taken and issue number}
   
   ### Warnings
   
   {list any specs with issues: missing metadata, conflicting states, etc.}
   ```

#### Audit Spec-Issue Alignment
**Trigger:** User asks "audit spec-issue sync"

**Process:**
1. Search all specs in `openspec/`
2. For each spec with `related_issues`:
   - Verify issue exists in GitHub
   - Check if issue status aligns with spec status:
     - Spec "approved" → Issue "open" ✅
     - Spec "in-progress" → Issue "open" with "in-progress" label ✅
     - Spec "completed" → Issue "closed" ✅
     - Any mismatch → ⚠️ Warning
3. Generate audit report:
   ```markdown
   ## OpenSpec-GitHub Audit Report
   
   **Date:** {timestamp}
   
   ### Alignment Status
   
   - ✅ {count} specs in sync
   - ⚠️ {count} specs with mismatches
   - ❌ {count} specs with missing issues
   
   ### Mismatches
   
   {list specs with state conflicts and recommended actions}
   
   ### Recommendations
   
   {suggest sync operations to fix mismatches}
   ```

---

## Implementation Details

### GitHub API Integration

**Required Tools:**
- Load GitHub tools: `tool_search_tool_regex` with pattern `github.*issue`
- Available operations:
  - Create issue: `github-pull-request_issue_fetch` (if available)
  - Update issue: Standard GitHub API via extension
  - Close issue: Standard GitHub API via extension
  - Add labels: Standard GitHub API via extension
  - Add comments: Standard GitHub API via extension

**Fallback:** If GitHub tools unavailable, generate manual instructions with:
- Issue body markdown ready to paste
- Labels to apply
- Steps to complete manually

### Spec File Updates

**YAML Frontmatter Modification:**
Use `replace_string_in_file` to update frontmatter fields:

```typescript
// Example: Add issue number to related_issues
oldString: `related_issues: []`
newString: `related_issues:\n  - 42`

// Example: Update status
oldString: `status: approved`
newString: `status: in-progress`

// Example: Update timestamp
oldString: `updated: 2026-03-05`
newString: `updated: 2026-03-06`
```

**Safety Checks:**
- Always validate YAML syntax after modification
- Verify frontmatter delimiters (`---`) remain intact
- Preserve all existing fields

### Error Handling

**Scenario: GitHub API Unavailable**
- Generate manual sync instructions
- Create checklist for user
- Log to `/memories/session/spec-issue-sync-pending.md`

**Scenario: Spec File Malformed**
- Alert user with specific parsing error
- Suggest fixes (missing frontmatter, invalid YAML)
- Skip spec in batch operations, log warning

**Scenario: Issue Already Exists**
- Check `related_issues` field first
- If issue number present, update instead of create
- If issue number missing but issue title matches, link existing issue

**Scenario: Permission Denied**
- Inform user of permission requirements
- Provide manual steps
- Suggest GitHub token configuration

---

## Usage Examples

### Example 1: Create Issue for Approved Spec

**User Request:**
```
"Create a GitHub issue for the item-long-description spec"
```

**Agent Actions:**
1. Read `openspec/enhancements/item-long-description.spec.md`
2. Parse frontmatter: title, type, priority, complexity, estimated_effort
3. Load GitHub tools with `tool_search_tool_regex`
4. Create issue:
   - Title: `[OpenSpec] Add Long Description Field to Item Table`
   - Body: (generated from spec content)
   - Labels: `openspec`, `enhancement`, `priority:medium`, `complexity:low`
5. Update spec `related_issues` field with new issue number
6. Commit changes

**Output:**
```markdown
✅ GitHub issue created successfully!

**Issue:** #42 - [OpenSpec] Add Long Description Field to Item Table
**Spec:** [item-long-description.spec.md](openspec/enhancements/item-long-description.spec.md)
**Labels:** openspec, enhancement, priority:medium, complexity:low

The spec has been updated with the issue number.
```

---

### Example 2: Sync All Specs

**User Request:**
```
"Sync all OpenSpec specs with GitHub issues"
```

**Agent Actions:**
1. Search `openspec/` for `.spec.md` files
2. Find 2 specs:
   - `features/employee-skills-performance-review.spec.md` (status: draft) → Skip
   - `enhancements/item-long-description.spec.md` (status: approved, no related_issues) → Create issue
3. Create issue for item-long-description spec
4. Update spec file
5. Generate summary report

**Output:**
```markdown
## OpenSpec GitHub Sync Report

**Date:** 2026-03-06 14:32:00

### Actions Taken

- ✅ Created 1 new issue
- 🔄 Updated 0 existing issues
- ✅ Closed 0 completed issues

### Details

1. **item-long-description.spec.md (enhancement)**
   - ✅ Created issue #42
   - Status: approved → linked
   - Labels: openspec, enhancement, priority:medium, complexity:low

### Skipped

1. **employee-skills-performance-review.spec.md (feature)**
   - ⏭️ Status is "draft" - waiting for approval before creating issue

### Summary

All approved specs are now tracked in GitHub issues. 1 spec remains in draft status.
```

---

### Example 3: Update Spec When Issue Closed

**User Request:**
```
"Update the item-long-description spec now that issue #42 is closed"
```

**Agent Actions:**
1. Read spec to verify issue #42 in `related_issues`
2. Check spec `status` field: "in-progress"
3. Update status to "completed"
4. Update timestamp
5. Commit changes

**Output:**
```markdown
✅ Spec updated successfully!

**Spec:** [item-long-description.spec.md](openspec/enhancements/item-long-description.spec.md)
**Status:** in-progress → completed
**Updated:** 2026-03-06

The spec is now marked as completed and ready for archiving.
```

---

### Example 4: Audit Spec-Issue Alignment

**User Request:**
```
"Audit all OpenSpec specs to check GitHub issue alignment"
```

**Agent Actions:**
1. Search all specs in `openspec/`
2. For each spec with `related_issues`, verify issue status
3. Find mismatches
4. Generate audit report

**Output:**
```markdown
## OpenSpec-GitHub Audit Report

**Date:** 2026-03-06 15:00:00

### Alignment Status

- ✅ 1 spec in sync
- ⚠️ 1 spec with mismatch
- ❌ 0 specs with missing issues

### In Sync

1. **item-long-description.spec.md**
   - Status: completed
   - Issue: #42 (closed)
   - ✅ Aligned

### Mismatches

1. **employee-skills-performance-review.spec.md**
   - Status: approved
   - Issue: None
   - ⚠️ Missing GitHub issue
   - **Recommendation:** Run sync to create issue

### Summary

1 of 2 specs require attention. Run `sync all specs` to resolve mismatches.
```

---

## Configuration

### Labels Used

The skill applies these GitHub labels:

| Label | Purpose | Applied When |
|-------|---------|-------------|
| `openspec` | Identifies OpenSpec-tracked issues | All OpenSpec issues |
| `feature` | Large feature spec | Spec type = feature |
| `enhancement` | Small enhancement spec | Spec type = enhancement |
| `api` | API specification | Spec type = api |
| `integration` | Integration spec | Spec type = integration |
| `priority:critical` | Critical priority | Spec priority = critical |
| `priority:high` | High priority | Spec priority = high |
| `priority:medium` | Medium priority | Spec priority = medium |
| `priority:low` | Low priority | Spec priority = low |
| `complexity:high` | High complexity | Spec complexity = high |
| `complexity:medium` | Medium complexity | Spec complexity = medium |
| `complexity:low` | Low complexity | Spec complexity = low |
| `status:ready` | Ready for implementation | Spec status = approved |
| `status:in-progress` | Implementation started | Spec status = in-progress |
| `status:completed` | Implementation done | Spec status = completed |

**Setup:** Ensure these labels exist in your GitHub repository before using the skill.

---

## Commit Message Conventions

The skill uses consistent commit messages:

- `chore: link spec to GitHub issue #{number}` - When creating issue link
- `chore: mark spec as completed (issue #{number} closed)` - When closing spec
- `chore: update spec status (GitHub sync)` - When updating status
- `chore: sync OpenSpec with GitHub issues` - Batch sync operations

---

## Memory Integration

### Repository Memory

The skill updates `/memories/repo/openspec-tracking.md` after each operation:

```markdown
## Recent Sync Operations

### 2026-03-06 14:32:00
- Created issue #42 for item-long-description.spec.md
- Updated spec related_issues field
- Applied labels: openspec, enhancement, priority:medium, complexity:low

### 2026-03-06 15:45:00
- Closed issue #42 (spec completed)
- Updated spec status: in-progress → completed
```

### Session Memory

Track sync operations in session memory:

```markdown
## Spec-Issue Sync Activity

- Created 3 issues
- Updated 2 specs
- Closed 1 issue
- 0 errors
```

---

## Best Practices

### When to Trigger Sync

**Automatic Triggers (Ideal):**
- Git hook: After spec file commit with status change
- GitHub Action: On issue close/reopen
- VS Code extension: On spec file save

**Manual Triggers:**
- Daily/weekly batch sync
- Before sprint planning
- After major spec updates

### Avoiding Conflicts

**Rule 1:** Single source of truth
- Spec = authoritative for technical design
- Issue = authoritative for work tracking

**Rule 2:** Clear ownership
- Spec owner manages spec file
- Team manages issue (comments, labels, assignment)

**Rule 3:** Sync direction
- Status changes: Spec → Issue (forward)
- Completion: Issue → Spec (reverse)
- Never bidirectional status sync (causes conflicts)

---

## Troubleshooting

### Issue: Spec has issue number but issue doesn't exist

**Cause:** Issue deleted or moved to another repository.

**Solution:**
1. Remove stale issue number from spec `related_issues`
2. Run sync to create new issue
3. Update any references to old issue number

---

### Issue: Duplicate issues created

**Cause:** Multiple sync runs without waiting for spec update.

**Solution:**
1. Check `related_issues` field before creating issue
2. Search GitHub for `[OpenSpec] {spec.title}` before creating
3. Link existing issue if found

---

### Issue: Spec status doesn't match issue status

**Cause:** Manual status change without sync.

**Solution:**
1. Run audit to identify mismatches
2. Decide authoritative source (spec or issue)
3. Update other side manually or via sync

---

## Future Enhancements

### Phase 1: Basic Sync (Current)
- Manual sync commands
- Forward sync (spec → issue)
- Basic reverse sync (issue close → spec)

### Phase 2: Automated Sync
- Git hooks for automatic sync
- GitHub Actions workflow
- Real-time bidirectional sync

### Phase 3: Intelligence
- Suggest spec status based on PR activity
- Auto-generate release notes from completed specs
- Link spec acceptance criteria to PR checks

---

## Related Skills

- **github-issue-creator**: Create GitHub issues (general purpose)
- **bc-release-note-generator**: Generate release note specs
- **agent-customization**: Create/modify skills and workflows

---

## GitHub PR TODO Integration

### Overview

Extends spec-issue synchronization to GitHub Pull Request workflows. Converts spec acceptance criteria into PR task list checkboxes, enabling real-time progress tracking and bidirectional sync between spec implementation status and PR task completion.

### Key Features

**PR Template Generation:**
- Auto-generate PR descriptions with acceptance criteria as task list checkboxes
- Include test scenarios as additional checklists
- Link spec file and related issue in PR header
- Add reviewer checklist based on BC development standards

**Bidirectional Sync:**
- Forward: Spec AC → PR task list (on PR creation)
- Reverse: PR merge → Update spec status to "completed"
- Real-time: PR task completion → Optional spec AC status sync

**Branch Convention:**
- Pattern: `{type}/spec-{spec-filename}`
- Types: feature, enh, api, integration
- Example: `enh/spec-item-long-description`

**Commit Convention:**
- Pattern: `{type}: {description} (spec: {spec-filename})`
- Example: `enh: implement long description field (spec: item-long-description)`

### Usage

#### Create PR from Spec

**Command:** `create PR from spec {spec-name}`

**Example:**
```
User: create PR from spec item-long-description
```

**Agent Workflow:**
1. Read spec file from openspec/ folders
2. Parse YAML frontmatter for metadata
3. Extract acceptance criteria section
4. Convert AC items to markdown task list (- [ ])
5. Generate PR body with:
   - Spec reference link
   - Related issue link
   - AC task list with progress counter
   - Test scenarios checklist
   - Reviewer checklist
   - Implementation notes section
6. Detect current branch or prompt for branch name
7. Create PR via GitHub API with generated body
8. Update spec YAML frontmatter: add PR number to `related_prs` field
9. Log operation to `/memories/repo/spec-issue-sync-log.md`

**PR Body Template:**
```markdown
## Specification Reference
📋 **Spec:** [item-long-description.spec.md](../openspec/enhancements/item-long-description.spec.md)  
🎯 **Related Issue:** Closes #42

## Acceptance Criteria (from spec)
Progress: 0 of 10 complete

### Functional Requirements
- [ ] AC-FUNC-001: User can enter Long Description text up to 2048 characters without error
- [ ] AC-FUNC-002: Long Description field visible on Item Card page
- [ ] AC-UI-001: MultiLine control enables text wrapping

### Data Requirements
- [ ] AC-DATA-001: Long Description value persists correctly
- [ ] AC-DATA-002: Field properly classified as CustomerContent

## Implementation Notes
<!-- Developer adds notes here -->

## Testing Checklist
- [ ] Test Scenario 1: Basic data entry and display
- [ ] Test Scenario 2: Maximum length validation (2048 chars)
- [ ] Test Scenario 3: Null/empty handling
- [ ] Test Scenario 4: Special characters
- [ ] Test Scenario 5: Persistence across sessions

## Reviewer Checklist
- [ ] Code follows AL development standards
- [ ] All AC checkboxes marked complete
- [ ] Tests pass locally
- [ ] Spec file updated with outcome notes
- [ ] No CodeCop/AppSourceCop warnings
- [ ] DataClassification on all new fields
- [ ] ToolTip on all page fields
```

**Validation:**
- ✅ Spec file exists in openspec/
- ✅ Spec status is "approved" or "in-progress"
- ✅ Current branch follows naming convention
- ✅ Related issue exists (from spec frontmatter)
- ✅ GitHub API authentication valid

**Error Handling:**
- Spec not found → Search openspec/ folders, prompt if ambiguous
- Spec not approved → Warn user, offer to update status
- No related issue → Offer to create issue first via forward sync
- Branch name invalid → Suggest correct branch name pattern
- GitHub API failure → Show manual PR creation instructions with generated body

---

#### Sync PR Status to Spec

**Command:** `sync PR {pr-number} to spec`

**Example:**
```
User: sync PR 52 to spec
```

**Agent Workflow:**
1. Fetch PR details via GitHub API
2. Extract spec reference from:
   - PR branch name (e.g., `enh/spec-item-long-description`)
   - PR description header (spec link)
   - PR title (match against spec titles)
3. Locate spec file in openspec/
4. Check PR merge status:
   - **Merged:** Update spec status to "completed", add `implemented_date`
   - **Closed (not merged):** Add note to spec, keep status as is
   - **Open:** Update spec with PR link if missing
5. Parse PR task list to count completed AC checkboxes (optional)
6. Update spec YAML frontmatter with PR number and status
7. Close related GitHub issue if PR merged
8. Log operation to sync log

**Spec Updates on PR Merge:**
```yaml
status: completed
implemented_date: 2026-03-15
related_prs: [#52]
```

**Validation:**
- ✅ PR exists and accessible via GitHub API
- ✅ Spec reference found in PR metadata
- ✅ Spec file exists in openspec/
- ⚠️ Warn if PR has incomplete AC checkboxes but is merged

**Error Handling:**
- PR not found → Verify PR number, check repo access
- Spec reference missing → Search by PR title, prompt for confirmation
- Multiple specs match → Show options, ask user to select
- Spec file moved → Search openspec/ recursively by title

---

#### Validate Branch has Spec

**Command:** `validate spec branch {branch-name}`

**Example:**
```
User: validate spec branch enh/spec-item-long-description
```

**Agent Workflow:**
1. Parse branch name against pattern: `{type}/spec-{spec-filename}`
2. Extract spec filename from branch name
3. Search openspec/ folders for matching spec file
4. Check spec exists and has valid YAML frontmatter
5. Verify spec status is appropriate (approved or in-progress)
6. Report validation result

**Validation Results:**
- ✅ **Valid:** Branch name correct, spec exists, status appropriate
- ⚠️ **Warning:** Spec exists but status is "draft" or "review"
- ❌ **Invalid:** Spec file not found or branch name doesn't match pattern

**Use Cases:**
- Pre-push Git hook validation
- PR creation validation
- CI/CD pipeline checks

---

#### Audit PR-Spec Alignment

**Command:** `audit PR-spec alignment`

**Example:**
```
User: audit PR-spec alignment
```

**Agent Workflow:**
1. Query GitHub API for all PRs (open + recently merged)
2. For each PR, extract spec reference if present
3. Collect all specs with "in-progress" or "completed" status
4. Compare to create alignment report:
   - PRs with valid spec references
   - PRs missing spec references
   - Specs with linked PRs
   - Specs without PRs (in-progress or completed status)
5. Identify mismatches:
   - PR merged but spec still "in-progress"
   - Spec "completed" but no PR linked
   - PR references non-existent spec
6. Generate markdown report with action items
7. Save report to `openspec/reports/pr-spec-audit-{date}.md`

**Report Format:**
```markdown
# PR-Spec Alignment Audit Report
**Date:** 2026-03-15  
**Repository:** BC Dataverse Integration Template

## Summary
- Total PRs analyzed: 24
- PRs with spec references: 20 (83%)
- Total specs (in-progress/completed): 18
- Specs with PR links: 16 (89%)
- Mismatches detected: 3

## Mismatches

### PR Merged but Spec Not Updated
1. PR #52 (merged 2026-03-10) → spec: item-long-description (status: in-progress)
   - Action: Update spec status to "completed"

### Spec Completed but No PR Linked
2. Spec: employee-hierarchy-sync (status: completed, implemented_date: 2026-03-01)
   - Action: Find and link PR #48

### PR References Invalid Spec
3. PR #55 (open) → spec: invalid-spec-name (not found)
   - Action: Update PR description with correct spec reference

## Recommendations
- Enable automated sync on PR merge (GitHub Action)
- Add pre-push Git hook to validate branch naming
- Run audit weekly in CI/CD pipeline

## Action Items
- [ ] Fix 3 detected mismatches above
- [ ] Review 4 PRs without spec references (#50, #51, #53, #54)
- [ ] Update 2 specs missing PR links (customer-api-v2, dataverse-product-sync)
```

**Scheduled Automation:**
- Run audit in GitHub Actions on schedule (weekly)
- Post audit report as GitHub Issue if mismatches detected
- Track audit history in `/memories/repo/spec-issue-sync-log.md`

---

### Branch Naming Convention

**Pattern:** `{type}/spec-{spec-filename-without-extension}`

**Type Prefixes:**
- `feature/` - Large features (from openspec/features/)
- `enh/` - Small enhancements (from openspec/enhancements/)
- `api/` - API specifications (from openspec/apis/)
- `integration/` - Integration specs (from openspec/integrations/)

**Examples:**
- `feature/spec-employee-skills-performance-review` ✅
- `enh/spec-item-long-description` ✅
- `api/spec-customer-api-v1` ✅
- `integration/spec-dataverse-product-sync` ✅
- `hotfix/fix-crash-issue` ✅ (non-spec branches allowed)
- `feature/add-new-feature` ⚠️ (missing spec reference)

**Benefits:**
- Clear spec association from branch name alone
- Enables automated spec lookup during PR creation
- Git hooks can validate branch has matching spec
- Consistent across team and repositories

---

### Commit Message Convention

**Pattern:** `{type}: {description} (spec: {spec-filename})`

**Type Prefixes:**
- `feat:` - New feature implementation
- `enh:` - Enhancement implementation
- `api:` - API changes
- `fix:` - Bug fixes
- `test:` - Test additions
- `docs:` - Documentation updates
- `refactor:` - Code refactoring

**Examples:**
```
feat: add employee skill tracking tables (spec: employee-skills-performance-review)
enh: implement long description field on item (spec: item-long-description)
api: create customer data API endpoint (spec: customer-api-v1)
test: add validation tests for long description (spec: item-long-description)
fix: correct field length validation (spec: item-long-description)
docs: update README with long description usage (spec: item-long-description)
```

**Benefits:**
- Links commits to spec for traceability
- Enables automated spec status tracking via commit analysis
- Clear intent in git history
- Supports automated changelog generation from specs
- Easy to filter git log by spec: `git log --grep="spec: item-long-description"`

---

### Automation Scripts

#### PowerShell Script: Create PR from Spec

**File:** `scripts/create-pr-from-spec.ps1`

**Usage:**
```powershell
.\scripts\create-pr-from-spec.ps1 -SpecFile "openspec/enhancements/item-long-description.spec.md"
```

**Implementation:** Create this script to enable command-line PR generation.

---

#### GitHub Action: Auto-Update Spec on PR Merge

**File:** `.github/workflows/sync-spec-on-pr-merge.yml`

**Trigger:** PR merged to main branch

**Workflow:**
```yaml
name: Sync Spec Status on PR Merge

on:
  pull_request:
    types: [closed]
    branches: [main, master]

jobs:
  sync-spec:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Extract spec reference
        id: spec
        run: |
          BRANCH="${{ github.event.pull_request.head.ref }}"
          if [[ $BRANCH =~ ^(feature|enh|api|integration)/spec-(.+)$ ]]; then
            SPEC_NAME="${BASH_REMATCH[2]}"
            echo "spec_name=$SPEC_NAME" >> $GITHUB_OUTPUT
            echo "found=true" >> $GITHUB_OUTPUT
          else
            echo "found=false" >> $GITHUB_OUTPUT
          fi
      
      - name: Find and update spec file
        if: steps.spec.outputs.found == 'true'
        run: |
          SPEC_FILE=$(find openspec -name "${{ steps.spec.outputs.spec_name }}.spec.md")
          if [ -n "$SPEC_FILE" ]; then
            IMPL_DATE=$(date +%Y-%m-%d)
            PR_NUM="${{ github.event.pull_request.number }}"
            
            # Update YAML frontmatter (simplified - use proper YAML parser in production)
            sed -i "s/status: in-progress/status: completed/" "$SPEC_FILE"
            sed -i "/status: completed/a implemented_date: $IMPL_DATE" "$SPEC_FILE"
            sed -i "s/related_prs: \[\]/related_prs: [#$PR_NUM]/" "$SPEC_FILE"
            
            git config user.name "github-actions[bot]"
            git config user.email "github-actions[bot]@users.noreply.github.com"
            git add "$SPEC_FILE"
            git commit -m "docs: update spec status on PR #$PR_NUM merge (spec: ${{ steps.spec.outputs.spec_name }})"
            git push
          fi
```

**Implementation:** Create this GitHub Action workflow for automated sync.

---

### Memory Integration

**Updated Log After PR Operations:**

After PR creation or sync, update `/memories/repo/spec-issue-sync-log.md`:

```markdown
### March 15, 2026 - 14:32

**Operation:** Create PR from Spec  
**Type:** PR Creation  
**Input:** Spec: item-long-description  
**Result:** Success

**Details:**
- Created PR #52: "Add Long Description field to Item"
- Branch: enh/spec-item-long-description
- AC task list generated (10 items)
- Linked to issue #42
- Updated spec with PR reference

**Spec Updates:**
- related_prs: [#52]
- status: in-progress
```

---

### Integration with Existing Commands

**Enhanced Forward Sync:**
- `sync spec with GitHub` → Creates issue + suggests PR creation
- After issue created, prompt: "Create PR with task list? (yes/no)"
- If yes, guide through PR creation with spec AC

**Enhanced Status Updates:**
- `update spec status {spec-name} to completed` → Check for related PR
- If PR exists but not merged, warn user
- If no PR exists, prompt to link PR or confirm manual completion

**Enhanced Audit:**
- `audit spec-issue sync` → Now includes PR alignment check
- Report shows: specs ↔ issues ↔ PRs linkage
- Identify orphaned PRs without specs

---

### Best Practices

**DO:**
✅ Create branch with `{type}/spec-{spec-name}` pattern  
✅ Use `create PR from spec` command for automatic AC generation  
✅ Check AC boxes in PR as work progresses  
✅ Reference spec in every commit message  
✅ Merge PR only when all AC checkboxes complete  
✅ Let automation update spec status on PR merge

**DON'T:**
❌ Create PRs without spec reference  
❌ Modify spec AC during PR (update spec, regenerate PR instead)  
❌ Merge PR with incomplete AC checkboxes  
❌ Skip linking PR number back to spec  
❌ Manually update spec status when automation available

---

### Troubleshooting PR Integration

**Issue:** PR created but spec not updated with PR number  
**Solution:** Run `sync PR {pr-number} to spec` to manually link

**Issue:** PR task list doesn't match spec AC  
**Solution:** Spec was updated after PR creation. Regenerate PR description or manually sync

**Issue:** PR merged but spec still "in-progress"  
**Solution:** GitHub Action may have failed. Check workflow logs, manually run `sync PR {pr-number} to spec`

**Issue:** Branch name doesn't match pattern  
**Solution:** Rename branch or use manual process. Pattern validation only suggestion, not enforced

**Issue:** Cannot create PR via API - permission denied  
**Solution:** Check GitHub token has `repo` and `pull_requests:write` scopes

---

### Future Enhancements

**Phase 2: Real-Time Sync**
- GitHub webhook integration for instant spec updates on PR task changes
- Live progress updates in spec file as developer checks boxes
- Slack/Teams notifications on AC completion milestones

**Phase 3: AI-Powered Features**
- Auto-detect AC completion from code changes (AI analysis)
- Suggest spec updates based on PR diff
- Generate test code from spec test scenarios
- Validate PR scope matches spec scope (prevent scope creep)

**Phase 4: Advanced Integrations**
- Link to Azure DevOps test runs for AC verification
- Integration with AppSource validation results
- Customer release note generation from completed specs
- Training material generation from feature specs with PR examples

---

**Version:** 1.1.0  
**Last Updated:** March 6, 2026  
**Maintained By:** OpenSpec Automation Team
