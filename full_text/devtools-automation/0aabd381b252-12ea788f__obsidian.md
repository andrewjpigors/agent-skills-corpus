---
name: obsidian
description: Integration with Obsidian vault for managing notes, tasks, and knowledge. Supports adding notes, creating tasks, and organizing project documentation. Includes 2025-2026 best practices including MOCs, properties, and practical organization patterns. Scoped for use within the obs-vault plugin context.
version: 1.0.0
updated: 2026-03-10
---

# Obsidian Integration

Expert guidance for integrating Claude workflows with Obsidian vault, including note creation, task management, and knowledge organization using Obsidian's markdown-based system.

## When to Use This Skill

- Creating notes during development or work sessions
- Tracking tasks and TODOs in Obsidian
- Documenting decisions and solutions
- Building a knowledge base of project insights
- Organizing research findings from Claude sessions
- Creating meeting notes or session summaries

## Core Principles

1. **Vault Location** - Use `$OBSIDIAN_VAULT_PATH` environment variable for vault path
2. **Always Ask User for Note Placement** - Never decide where to save notes without asking the user first. Show vault structure, suggest options, and let the user choose.
3. **Atomic Notes** - Each note focuses on a single concept or topic
4. **Linking** - Use wikilinks `[[note-name]]` to connect related ideas
5. **Tags** - Organize with hierarchical tags like `#project/feature`
6. **Tasks** - Use checkbox syntax for actionable items
7. **Timestamps** - Include dates for temporal context

## Obsidian Best Practices (2025-2026)

Based on current best practices from the Obsidian community:

### 1. Start Simple, Don't Overthink

**Key Principle**: Write first, organize later (or never)

- Focus on creating notes, not perfecting the system
- Let your vault structure evolve naturally as you add content
- Don't spend hours planning the "perfect" organization
- Begin with a few notes and gradually explore advanced features

**Avoiding Productive Procrastination**:
- ❌ **Don't**: Spend all your time tweaking the system and calling it work
- ❌ **Don't**: Endlessly optimize tags, folders, and organization
- ✅ **Do**: Spend 80% time writing/working, 20% organizing
- ✅ **Do**: Organize during weekly reviews, not constantly

### 2. Use MOCs (Maps of Content) Over Deep Folders

**What is a MOC?**
- A "Map of Content" is a note that primarily links to other notes
- Acts as an index or table of contents for a topic
- Provides flexible, many-to-many relationships (unlike folders)

**Why MOCs > Folders:**
- Notes can belong to multiple topics, but only one folder
- MOCs allow one note to appear in many different "maps"
- Easier to reorganize - just update links, no file moving
- More aligned with how knowledge actually connects

**MOC Best Practices:**
- Keep MOCs under 25 items for easy navigation
- Think of MOCs as high-level overviews, not comprehensive indexes
- Create sub-MOCs when a section gets too large
- Use consistent hierarchy - all links at the same conceptual level
- Include emoji icons for visual scanning

**When to Create a MOC:**
- "Mental Squeeze Point" - when you feel overwhelmed by many related notes
- When you have 5+ notes on a related topic
- When starting a new project
- When you need a navigation hub

**MOC vs README:**
- MOCs are Obsidian-native with properties and wikilinks
- READMEs are more markdown-standard but less integrated
- Prefer MOCs for better Obsidian features (graph view, backlinks)

### 3. Leverage Properties (Metadata)

**Why Properties > Folders:**
- Searchable: Find all `type: planning` notes across entire vault
- Flexible: One note can have multiple property values
- Dataview-compatible: Auto-generate lists with queries
- More powerful than folder-only organization

**Recommended Property Schema:**

```yaml
---
type: planning | reference | todo | moc | development | session | analysis
project: project-name
subproject: sub-project-name
status: active | in-progress | completed | archived | blocked
tags:
  - topic1
  - topic2
  - topic3
priority: critical | high | medium | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Property Usage:**
- Add to ALL new notes for consistency
- Use `type` to categorize by note function, not topic
- Use `project` to group across folders
- Use `status` to track progress
- Use `tags` for topic categorization
- Keep property names consistent across vault
- **Always add `dump` tag to session/daily notes** - Makes them easy to filter and archive

#### Critical: Dump Tag Requirement

**ALWAYS include the `dump` tag in session/daily notes.** This tag is essential for:
- Filtering all session notes across projects: `tag:#dump`
- Archiving workflows
- Separating working notes from permanent documentation

**Note:** Session notes should be stored in `session-saves/` directory.

**When creating session notes:**

Python template for new files (with frontmatter):
```python
# Create new note with frontmatter
f.write("---\n")
f.write("type: session\n")
f.write(f"project: {PROJECT_NAME}\n")
f.write(f"date: {date_str}\n")
f.write("tags:\n")
f.write("  - session\n")
f.write("  - dump\n")  # REQUIRED
f.write("status: completed\n")
f.write("---\n\n")
```

When appending to existing files:
- Only append content (frontmatter already exists)
- No need to add dump tag again

### 4. Actually USE Your Notes

**Biggest Challenge**: Taking notes and never reviewing them

**Review Systems:**
- Schedule weekly reviews to revisit notes
- Clean up and reorganize as you use notes
- Re-arrange information, add links, update text
- Link new discoveries to existing notes
- Archive or delete obsolete notes

**Active Note Management:**
- Read old notes when starting related work
- Update notes with new insights
- Link backwards from new notes to old ones
- Build on previous knowledge

**Make Notes Actionable:**
- Add TODOs and next steps
- Link to relevant code or files
- Include "See Also" sections
- Create clear "Quick Actions" lists

### 5. Organize by Note Type, Not Topic

**Traditional (Topic-based):**
```
vault/
├── Machine-Learning/
│   ├── session-notes.md
│   ├── research.md
│   └── todos.md
└── Web-Development/
    ├── session-notes.md
    └── research.md
```

**Better (Type-based + Properties):**
```
vault/
├── Sessions/  (all session notes, tagged by project)
├── Planning/  (all planning docs, tagged by project)
├── TODOs/     (all task tracking)
└── Reference/ (all reference material)
```

Then use properties and tags to group by topic:
- `project: machine-learning`
- `tags: [ml, neural-networks]`

**Benefits:**
- Consistent organization regardless of topic
- Easy to find all notes of a certain type
- Properties handle topic categorization
- Simpler folder structure

### 6. Create a Home/Index MOC

**Central Navigation Hub:**
- Single starting point for entire vault
- Links to all project MOCs
- Quick access to TODOs and recent notes
- Project status overview
- Pin in Obsidian for easy access

**Home MOC Structure:**
```markdown
# 🏠 Home

## 🎯 Active Projects
- [[Project-1-MOC]] - Description
- [[Project-2-MOC]] - Description

## 📋 Quick Access
- [[TODOs/Master-Index]]
- [[Sessions/Latest]]

## 📚 Knowledge by Topic
- [[Topic-1-MOC]]
- [[Topic-2-MOC]]

## 🗂️ By Note Type
- Planning notes
- Development sessions
- Reference docs
```

### 7. Link Profusely, Folder Minimally

**Linking Strategy:**
- Create links as you write
- Link to related concepts immediately
- Use bidirectional links when relevant
- Build a knowledge graph through connections

**Folder Strategy:**
- Keep folder structure flat (2-3 levels max)
- Use folders for note TYPE, not topic
- Rely on links and properties for organization
- Orient toward speed and ease of navigation

## Vault Configuration

### Environment Setup

The Obsidian vault location should be stored in an environment variable. The recommended variable name is `$OBSIDIAN_VAULT_PATH`, though `$OBSIDIAN_VAULT` is also commonly used:

```bash
# Check vault location
echo $OBSIDIAN_VAULT_PATH

# Should return something like:
# /Users/username/Documents/Notes
```

If not set, configure it in your shell profile:

```bash
# Add to ~/.zshrc or ~/.bashrc
export OBSIDIAN_VAULT_PATH="/path/to/your/vault"
```

Throughout this skill, `$VAULT` is used as shorthand for the vault path variable. Adapt to whichever variable name is set in your environment.

## Project Organization in Vault

### Selecting Project Directory Location

When creating a new project's notes in Obsidian, ask the user where the project directory should be located within the vault:

**Workflow:**

1. **Show current vault structure** to help user decide
2. **Offer two options:**
   - **Option 1:** Root level - Project directory directly in vault root
   - **Option 2:** Custom path - User specifies subdirectory structure

3. **Create directory if it doesn't exist**

### Implementation Pattern

```python
import os
from pathlib import Path

# Get vault path
vault_path = Path(os.environ.get('OBSIDIAN_VAULT_PATH'))

# Show vault structure to user
print("📁 Current vault structure:")
print(f"   {vault_path}/")

# Show top-level directories (up to 2 levels)
for item in sorted(vault_path.iterdir()):
    if item.is_dir() and not item.name.startswith('.'):
        print(f"   ├── {item.name}/")
        # Show one level deeper
        for subitem in sorted(item.iterdir())[:3]:
            if subitem.is_dir() and not subitem.name.startswith('.'):
                print(f"   │   ├── {subitem.name}/")
        # Indicate if there are more
        remaining = len([x for x in item.iterdir() if x.is_dir()]) - 3
        if remaining > 0:
            print(f"   │   └── ... ({remaining} more)")

print()
print("Where should this project's notes be stored?")
print()
print("Options:")
print("  1. Root level (vault/project-name/)")
print("  2. Custom path (e.g., vault/Work/project-name/ or vault/Projects/Active/project-name/)")
print()

choice = input("Enter choice [1-2]: ")

if choice == "1":
    # Root level
    project_dir = vault_path / project_name
else:
    # Custom path
    print()
    print("Enter the parent directory path (relative to vault root).")
    print("Examples:")
    print("  - Work")
    print("  - Projects/Active")
    print("  - Personal/Research")
    print()
    parent_path = input("Parent directory: ").strip()

    # Clean and validate path
    parent_path = parent_path.strip('/')
    project_dir = vault_path / parent_path / project_name

# Create directory if it doesn't exist
project_dir.mkdir(parents=True, exist_ok=True)
print(f"✅ Project directory: {project_dir.relative_to(vault_path)}")
```

### Best Practices for Organization

**Root Level:**
- ✅ Quick access to frequently used projects
- ✅ Simple structure for small vaults
- ❌ Can become cluttered with many projects

**Organized Subdirectories:**
- ✅ Better organization for many projects
- ✅ Logical grouping (Work, Personal, Research, etc.)
- ✅ Easier to navigate in large vaults
- ✅ Better for team vaults with shared structure

**Recommended Structures:**

```
vault/
├── Work/
│   ├── project-a/
│   ├── project-b/
│   └── project-c/
├── Personal/
│   ├── hobby-project/
│   └── research/
├── Archive/
│   └── old-project/
└── Templates/
```

Or by status:

```
vault/
├── Active/
│   ├── project-a/
│   └── project-b/
├── Planning/
│   └── project-c/
├── Completed/
│   └── old-project/
└── Archive/
```

### Directory Creation Safety

**Always check before creating:**
```python
if project_dir.exists():
    print(f"⚠️  Directory already exists: {project_dir}")
    overwrite = input("Continue using this directory? (y/n): ")
    if overwrite.lower() != 'y':
        # Ask for different name or path
        return
else:
    # Create with parents
    project_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created directory: {project_dir}")
```

### Storing Project Configuration

Save the project directory path for future sessions:

```python
# In .claude/project-config
config_content = f"""obsidian_project={project_name}
obsidian_path={project_dir.relative_to(vault_path)}
"""

with open('.claude/project-config', 'w') as f:
    f.write(config_content)
```

This allows subsequent sessions to use the same directory without asking again.

## User Choice: Never Assume Note Placement

**CRITICAL PRINCIPLE**: When creating ANY note in Obsidian, ALWAYS ask the user where they want it saved. Never decide the location yourself, even if it seems obvious.

### Why This Matters

1. **User has context you don't** - They know how their vault is organized
2. **Flexibility is key** - Different notes may belong in different places
3. **Avoids reorganization work** - User won't need to move notes later
4. **Respects user's system** - Their vault organization is personal

### The Workflow for ANY Note Creation

**Step 1: Show Current Structure**
```python
# Display vault structure to help user decide
vault_path = Path(os.environ.get('OBSIDIAN_VAULT_PATH'))
print("📁 Current vault structure:")
print(f"   {vault_path.name}/")

for item in sorted(vault_path.iterdir())[:10]:
    if item.is_dir() and not item.name.startswith('.'):
        print(f"   ├── {item.name}/")
```

**Step 2: Suggest Options (Don't Decide)**
```python
print("\nWhere would you like to save this note?")
print()
print("Suggestions:")
print("  1. Root level - Notes/note-name.md")
print("  2. [Specific folder] - Notes/Folder/note-name.md")
print("  3. Custom path - You specify")
print()
```

**Step 3: Get User Input**
```python
choice = input("Enter choice or custom path: ").strip()
```

**Step 4: Create in Chosen Location**
```python
# Use their choice, don't override it
if choice == "1":
    note_path = vault_path / "note-name.md"
elif choice == "2":
    note_path = vault_path / "Folder" / "note-name.md"
else:
    # Custom path
    note_path = vault_path / choice / "note-name.md"

# Create directory if needed
note_path.parent.mkdir(parents=True, exist_ok=True)
```

### Examples of When to Ask

❌ **WRONG - Assuming location:**
```python
# Creating documentation note
note_path = vault_path / "Guides" / "How-to.md"  # DON'T DO THIS
```

✅ **RIGHT - Asking user:**
```python
# Show structure and suggest
print("Where should this documentation note be saved?")
print("Suggestions:")
print("  1. Root level (simple)")
print("  2. New 'Guides' folder (for documentation)")
print("  3. Existing 'Work' folder")
print("  4. Custom path")

choice = input("Your choice: ")
# Then create based on their input
```

### Exception: Project Session Notes

The ONLY exception is when a project configuration already exists:
- Configuration already exists in `.claude/project-config`
- User has previously chosen the project location
- All session notes for that project go to the same place

Even then, on FIRST use, always ask and save the choice.

### Summary

**Golden Rule**: If you're about to write a file to the Obsidian vault, STOP and ask the user where it should go first.

### Successful Pattern Example

**Session**: Creating a TODO note

**Implementation**:
```bash
# 1. Check vault location
echo $OBSIDIAN_VAULT_PATH

# 2. Show structure
ls -1 $OBSIDIAN_VAULT_PATH/

# 3. Ask user
"Where would you like me to save the TODO note?

**Options:**
1. project-name/ - With your other project notes (recommended)
2. project-name/sessions/ - With session history
3. Root level - Directly in vault root
4. Custom path - You specify

Which would you prefer?"

# 4. User response: "1"

# 5. Create in chosen location
cat > "$OBSIDIAN_VAULT_PATH/project-name/TODO.md" <<'EOF'
[content]
EOF
```

**Result**: Note created in user's preferred location without assumptions or reorganization needed later.

**Key Principle**: Even when one location seems "obvious", always ask. The user knows their organizational system better than you do.

## Vault Reorganization Workflow

When reorganizing a large Obsidian vault structure, follow this systematic approach:

### Planning Phase

1. **Document target structure** in a prompt file
   - Define folder hierarchy
   - Specify naming conventions (e.g., `session-saves/` vs `sessions-history/`)
   - Note standard project structure (TO-DOS.md, session-saves/, archived/daily/, archived/monthly/)

2. **Create todo list** to track progress
   - Break down by major operations: create folders, move files, update links
   - Track completion systematically

### Execution Phase

Execute in this order to minimize broken links:

1. **Create new folder structure first**
   ```bash
   mkdir -p Work/Category-1 Work/Category-2 Work/Category-3
   ```

2. **Move files and folders**
   - Move complete directories with `mv source/ destination/`
   - Check for hidden files (.DS_Store) that might prevent rmdir
   - Use `rmdir` (not `rm -rf`) to safely remove directories - fails if not empty

3. **Standardize project folders**
   - Rename `sessions-history/` → `session-saves/` for consistency
   - Create `archived/daily/` and `archived/monthly/` subdirectories
   - Move or create `TO-DOS.md` files from centralized TODO location

4. **Update HOME.md and MOC files**
   - Update links in navigation files systematically
   - Work through one file at a time
   - Use Edit tool with exact string matching

5. **Clean up**
   - Remove old empty folders
   - Remove or relocate orphaned files
   - Verify structure with `tree` or `find` commands

### Link Update Strategy

When updating internal links across many files:

1. **Find all affected files first**
   ```bash
   grep -r "pattern" $VAULT --include="*.md"
   ```

2. **Read each file before editing** (Edit tool requirement)

3. **Update systematically** - one file at a time, completing each fully

4. **Remove links to deleted files** (like central Home.md)

### Common Patterns

**Standard project structure:**
```
project-name/
├── TO-DOS.md
├── session-saves/
├── archived/
│   ├── daily/
│   └── monthly/
└── [project-specific folders]
```

**Hierarchical organization:**
```
Work/
├── Category-1/
│   ├── HOME.md
│   ├── TO-DOS.md
│   └── project-a/
└── Category-2/
    ├── HOME.md
    └── project-b/
```

### Verification

After reorganization:
- Use `tree -L 3 -d` to verify structure
- Check that links work in Obsidian
- Verify no broken links to removed files
- Test navigation between HOME.md files

### Bulk Link Updates After Reorganization

When updating many links after vault reorganization:

1. **Find affected files:**
   ```bash
   grep -r "\[\[OldPath" $VAULT --include="*.md"
   ```

2. **Update systematically:**
   - Read file first (Edit tool requirement)
   - Update all links in that file together
   - Complete one file before moving to next
   - Mark as done in todo list

3. **Pattern for updating:**
   ```markdown
   # Old
   [[OldFolder/file|Display]]

   # New
   [[Work/Category/OldFolder/file|Display]]
   ```

4. **Removing obsolete links:**
   - Find: `[[ObsoleteFile|...]]` or `[[ObsoleteFile]]`
   - Remove entire link reference
   - Clean up surrounding formatting

### Home.md File Management

When reorganizing to hierarchical structure with section-level HOME.md files:

**Pattern: Replace Central Home with Section Homes**

**Before (centralized):**
```
vault/
├── Home.md (central hub linking to everything)
├── Project-1/
├── Project-2/
└── Project-3/
```

**After (hierarchical):**
```
vault/
├── Work/
│   ├── Category-1/
│   │   ├── HOME.md (section hub)
│   │   └── project-1/
│   └── Category-2/
│       ├── HOME.md (section hub)
│       └── project-2/
└── Personal/
    ├── HOME.md (section hub)
    └── project-3/
```

**Steps to transition:**

1. **Create section HOME.md files FIRST**
   - One per major category
   - Each contains links to projects in that section
   - Include navigation between sections

2. **Find all references to central Home:**
   ```bash
   grep -r "\[\[Home" $VAULT --include="*.md"
   ```

3. **Update or remove links systematically:**
   - MOC files: Update to link to appropriate section HOME
   - Section HOME files: Link to sibling sections, not central Home
   - Project notes: Remove Home links (navigate via section HOME instead)

4. **Delete central Home.md LAST:**
   - Only after all links updated or removed
   - Verify no broken references remain

**Section HOME.md template:**
```markdown
---
type: moc
section: section-name
tags:
  - home
  - moc
---

# Section Name

## Projects

- [[project-1/Project-1-MOC|Project 1]] - Description
- [[project-2/Project-2-MOC|Project 2]] - Description

## Quick Access

- [[TO-DOS|Section TODOs]]
- [[Archives|Archived Work]]

## Other Sections

- [[../Other-Section/HOME|Other Section]]

---

*Section home for [Category]*
```

**Benefits of section HOME files:**
- Logical organization by category
- Each section is self-contained
- No single central file to maintain
- Better for hierarchical vault structures
- Clearer navigation paths

### HOME.md Naming Convention

**Pattern:** Use `[section-name]_HOME.md` instead of generic `HOME.md`

**Benefits:**
- Avoid conflicts when multiple HOME files in working directory
- Clear identification in file browsers
- Better for search and navigation
- Consistent naming pattern

**Renaming Process:**

1. **Rename files:**
```bash
mv Work/Category-1/HOME.md Work/Category-1/Category-1_HOME.md
mv Work/Category-2/HOME.md Work/Category-2/Category-2_HOME.md
```

2. **Update references:**
```bash
# Find all links to old names
grep -r "\[\[.*HOME\|" $VAULT --include="*.md"

# Update links systematically
# Old: [[Work/Category-1/HOME|Category 1]]
# New: [[Work/Category-1/Category-1_HOME|Category 1]]
```

**When to use generic `HOME.md`:**
- Single section vault (no subsections)
- Root-level home only
- No naming conflicts

**When to use `[name]_HOME.md`:**
- Multiple section HOME files (recommended)
- Hierarchical vault structure
- Working across multiple projects simultaneously

### Brain Dump Folder Handling

When reorganizing vault with brain dump or temporary scratch folders:

**Purpose:** Brain dump folders contain unstructured working notes that need to be:
1. Reviewed for valuable content
2. Moved to appropriate permanent locations
3. Archived or deleted if obsolete

**Workflow:**

1. **Review content first:**
   ```bash
   ls -lh Project/Archives/Brain-Dump/
   # Check file sizes and dates
   ```

2. **Categorize notes:**
   - **Permanent value:** Move to appropriate thematic location
   - **Session notes:** Consolidate and archive
   - **Obsolete/duplicates:** Delete

3. **Move valuable content:**
   ```bash
   mv Work/Brain-dump/Useful-Notes.md Work/Category/
   ```

4. **Archive or delete folder:**
   ```bash
   # If brain dump should be archived
   mv Project/Brain-dump/ Project/Archives/Brain-Dump/

   # If content all processed and obsolete
   rmdir Project/Brain-dump/  # Safe - fails if not empty
   ```

**Anti-pattern:** Don't just move entire brain dump folder without review.

**Best practice:**
- Process brain dump content during vault reorganization
- Extract summaries into thematic notes
- Archive individual sessions if needed
- Only keep brain dump folder if actively using it for scratch work

## Session Note Consolidation Workflow

When consolidating daily session notes into thematic reference notes and project TODOs:

### Purpose

Convert chronological session history into organized knowledge by:
- Creating thematic reference notes grouped by topic (not date)
- Extracting actionable tasks into project TO-DOS.md files
- Archiving processed session notes to archived/daily/
- Preserving knowledge while reducing noise

### When to Consolidate

**Triggers:**
- End of project phase or milestone
- Session folder has 5+ notes
- Starting new work and need clean context
- Monthly vault maintenance
- Before sharing project with others

### Execution Steps

**1. Create Thematic Reference Notes**

Group content by topic, not chronology:

```markdown
---
type: reference
project: project-name
tags:
  - theme-tag
  - topic-tag
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: completed | in-progress
---

# Thematic Title

**Project:** Project Name
**Period:** Date Range
**Status:** Current status

---

## Overview

High-level summary of this work area

---

## Section 1: Sub-topic

Content from multiple sessions organized coherently

### Key Decisions
- Decision 1 (from session YYYY-MM-DD)
- Decision 2 (from session YYYY-MM-DD)

### Implementation
Details consolidated from sessions

---

## Related Notes

- [[Other-Thematic-Note|Related Topic]]
- [[Project-Planning|Planning Docs]]

---

*Consolidated from sessions: YYYY-MM-DD, YYYY-MM-DD, YYYY-MM-DD*
```

**2. Extract TODOs to Project TO-DOS.md**

```markdown
---
type: todo
project: project-name
status: active | completed
tags:
  - todo
  - project-name
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Project Name - TODOs

**Last Updated:** YYYY-MM-DD

---

## Active Tasks

### Phase 1: [Phase Name]
- [ ] Task 1 extracted from session
- [ ] Task 2 from session
- [x] Task 3 (completed)

---

## Completed (Archive)

### [Milestone Name] (Completed YYYY-MM-DD)
- [x] Completed task 1
- [x] Completed task 2

---

## Related Notes
- [[Thematic-Note-1|Reference]]
- [[Project-Planning|Planning Docs]]

---

*Extracted from session notes consolidated on YYYY-MM-DD*
```

**3. Archive Session Notes**

Move processed sessions to archived/daily/:

```bash
# Move all processed session notes
mv project/session-saves/*.md project/archived/daily/

# Or move selectively
mv project/session-saves/2026-02-*.md project/archived/daily/
```

### Content Organization Strategy

**Organize by topic, NOT chronology:**

❌ **Wrong - Chronological:**
```markdown
## January Work
- Did X on 2026-01-15
- Did Y on 2026-01-20
```

✅ **Right - Thematic:**
```markdown
# Data Collection and Enrichment

## Phase 1: Initial Setup (2026-01-24)
[All setup work grouped together]

## Phase 2: Additional Metrics (2026-01-27)
[All metrics work grouped together]
```

### File Naming

**Thematic notes - descriptive, timeless:**
- `Data-Collection-and-Enrichment.md`
- `Statistical-Analysis-Results.md`
- `Figure-Generation-Workflow.md`
- `Infrastructure-and-Tools.md`

**NOT date-based:**
- ❌ `2026-01-Session-Summary.md`
- ❌ `January-Work-Consolidated.md`
- ❌ `Week-3-Notes.md`

### Verification Checklist

After consolidation:
- [ ] All thematic notes have proper frontmatter with type: reference
- [ ] Each thematic note focuses on ONE topic area
- [ ] TO-DOS.md exists with extracted tasks
- [ ] All session notes moved to archived/daily/
- [ ] Thematic notes are navigable (good headers, sections)
- [ ] Related notes are cross-linked
- [ ] Timeline documented ("Consolidated from sessions: ...")
- [ ] No critical information lost

## Link Management and Verification

After major vault reorganization, verify and fix all internal wikilinks systematically.

### Automated Broken Link Detection

Use Python script to scan entire vault for broken wikilinks:

```python
import re
from pathlib import Path

vault_root = Path(os.environ.get('OBSIDIAN_VAULT_PATH'))
broken_links = []
wikilink_pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'

for md_file in vault_root.glob("**/*.md"):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    matches = re.findall(wikilink_pattern, content)

    for link in matches:
        link = link.strip()

        # Skip heading-only references
        if '#' in link:
            link = link.split('#')[0].strip()
            if not link:
                continue

        # Check if linked file exists (Obsidian searches by filename)
        found = list(vault_root.glob(f"**/{link}.md"))
        if not found:
            broken_links.append({
                'source': md_file,
                'broken_link': link
            })

# Report
for item in broken_links:
    print(f"BROKEN: {item['source'].name} -> [[{item['broken_link']}]]")
```

## Practical Organization Patterns

### Pattern 1: Home MOC as Central Hub

```markdown
---
type: moc
tags: [home, moc, navigation]
created: YYYY-MM-DD
---

# 🏠 Vault Home

## 🎯 Active Projects
| Project | Status | Priority |
|---------|--------|----------|
| [[Project-A/Project-A-MOC\|Project A]] | In Progress | High |
| [[Project-B/Project-B-MOC\|Project B]] | Planning | Medium |

## 📋 Quick Actions
- [[TODOs/Master-TODO-Index\|Master TODOs]]
- [[Sessions/Latest\|Latest Session]]

## 📚 Knowledge Areas
- [[Domain-1-MOC\|Domain 1]]
- [[Domain-2-MOC\|Domain 2]]
```

### Pattern 2: Project MOC

```markdown
---
type: moc
project: project-name
status: active
tags: [project-name, moc]
created: YYYY-MM-DD
---

# Project Name MOC

## 📋 Planning
- [[Planning/Main-Plan\|Main Plan]]
- [[Planning/Requirements\|Requirements]]

## 🔧 Development
- [[Development/Architecture\|Architecture]]
- [[Development/Implementation\|Implementation]]

## 📊 Analysis
- [[Analysis/Results\|Results]]

## 🗂️ Sessions
- [[session-saves/latest\|Latest Session]]

---

**Related:** [[../Other-Project/Other-Project-MOC\|Related Project]]
```

### Pattern 3: Properties in Practice

Full frontmatter with all recommended fields:

```yaml
---
type: reference
project: project-name
subproject: optional-subproject
status: active | in-progress | completed | archived
tags:
  - relevant-tag-1
  - relevant-tag-2
  - dump  # Add to ALL session/daily notes for easy filtering
priority: critical | high | medium | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Practical Obsidian Search:**
```
# Find all high-priority planning notes
priority: high type: planning

# Find all active TODOs
type: todo status: active

# Find all notes for a project
project: project-name

# Find all session/daily notes (for archiving)
tag:#dump

# Find all session notes for a specific project
tag:#dump project: project-name
```

### Pattern 4: TODO Consolidation

**Create Central TODO Directory:**

```
TODOs/
├── Master-TODO-Index.md     # Central index
├── Project-1-TODOs.md       # Project-specific
├── Project-2-TODOs.md
└── Archive/                 # Completed TODOs
```

**Project-Specific TODO:**

```markdown
---
type: todo
project: project-1
status: in-progress
tags: [project-1, todo]
priority: high
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Project 1 - TODOs

## Active TODOs

### Category 1
- [ ] Task 1 #priority/high #due/YYYY-MM-DD
- [ ] Task 2 #priority/medium

## Completed
- [x] Task 3 - Completed YYYY-MM-DD

## Related Notes
- [[Project-1/Planning/Main-Plan|Planning]]

---

**Link back to:** [[TODOs/Master-TODO-Index|Master Index]]
```

### Pattern 5: Archive Strategy

**Per-Project Archives:**

```
Project/
├── Planning/
├── Development/
├── Sessions/          # Active sessions
└── Archives/
    ├── daily/         # Old session notes
    └── monthly/       # Monthly summaries
```

**Archive Rules:**
1. **No links FROM current work TO archived notes** - Archives are historical reference only
2. **Archive after 30 days** for session notes
3. **Create archive summaries** before archiving - extract key decisions
4. **Monthly archive folders** for high-volume projects

### Pattern 6: Cross-Project Linking

```markdown
# In Project A notes:

## Related Work in Project B
- [[Project-B/Planning/Shared-Analysis|Shared Analysis]] - Detailed work
- [[Project-B/Project-B-MOC|Project B MOC]] - Full context
```

```markdown
# In Project B notes:

## Related Requirements from Project A
- [[Project-A/Planning/Requirements|Requirements]] - What needs to be done
- [[Project-A/Data/Dataset|Dataset]] - Source data
```

### Pattern 7: Topic-Based Folders Within Projects

```
Project/
├── Tools/            # Topic: Tool development
│   └── Tool-1.md
├── Planning/         # Topic: Planning docs
│   └── Main-Plan.md
├── Analysis/         # Topic: Analysis work
│   └── Analysis-Plan.md
└── Archives/         # Historical
    └── old-sessions/
```

### Implementation Checklist

When setting up a new vault or reorganizing:

**Immediate (High Impact):**
- [ ] Create `Home.md` central navigation hub
- [ ] Add properties to all existing notes
- [ ] Convert READMEs to MOCs with properties

**Short-term (This Week):**
- [ ] Implement consistent tagging strategy
- [ ] Create weekly review template
- [ ] Set up TODO consolidation structure

**Long-term (As Needed):**
- [ ] Consider flattening deep folders
- [ ] Set up Dataview queries (if using plugin)
- [ ] Implement monthly archive rotation

## Folder Organization for Claude Integration

Recommended folder structure within Obsidian vault:

```
$VAULT/
├── Daily/                      # Daily notes
│   └── YYYY-MM-DD.md
├── Sessions/                   # Claude session notes
│   └── YYYY-MM-DD-topic.md
├── Tasks/                      # Task tracking
│   ├── active/
│   └── completed/
├── Projects/                   # Project documentation
│   └── project-name/
│       ├── index.md
│       ├── architecture.md
│       └── decisions.md
├── Solutions/                  # Code solutions and fixes
│   └── solution-name.md
├── Research/                   # Research notes
│   └── topic.md
├── Knowledge/                  # Permanent notes
│   └── concept.md
└── Templates/                  # Note templates
    ├── session.md
    ├── task.md
    └── solution.md
```

## Helper Functions for Obsidian Integration

### Bash Helper Functions

Add these to your shell profile for easy integration:

```bash
# Create new session note in Obsidian
obs-session() {
    local topic="${1:-general}"
    local date=$(date +%Y-%m-%d)
    local file="$OBSIDIAN_VAULT_PATH/Sessions/${date}-${topic}.md"

    cat > "$file" <<EOF
---
date: $date
type: session-note
tags:
  - claude-session
  - dump
  - project/$topic
---

# Session: $topic - $date

## Context


## Summary


## Action Items
- [ ]

## Links

EOF

    echo "Created session note: $file"
}

# Create task in Obsidian
obs-task() {
    local task_name="$1"
    local date=$(date +%Y-%m-%d)
    local file="$OBSIDIAN_VAULT_PATH/Tasks/${task_name}.md"

    cat > "$file" <<EOF
---
date: $date
type: task
tags:
  - task
  - status/pending
---

# Task: $task_name

## Description


## Checklist
- [ ]

## Created
$date via Claude session
EOF

    echo "Created task: $file"
}

# Append to daily note
obs-note() {
    local date=$(date +%Y-%m-%d)
    local time=$(date +%H:%M)
    local daily_note="$OBSIDIAN_VAULT_PATH/Daily/${date}.md"

    # Create daily note if doesn't exist
    if [ ! -f "$daily_note" ]; then
        cat > "$daily_note" <<EOF
---
date: $date
type: daily-note
tags:
  - dump
---

# $date

EOF
    fi

    # Append note
    cat >> "$daily_note" <<EOF

## $time


EOF

    echo "Added entry to daily note: $daily_note"
}

# Quick search in Obsidian vault
obs-search() {
    grep -r "$1" "$OBSIDIAN_VAULT_PATH" --include="*.md"
}
```

## Integration Workflow with Claude

### Before Session

1. **Verify vault location**
   ```bash
   echo $OBSIDIAN_VAULT_PATH
   ```

2. **Create session note** (optional)
   ```bash
   obs-session "feature-implementation"
   ```

### During Session

1. **Add notes as you go**
   - Use Claude to create notes for important insights
   - Document decisions and reasoning
   - Track code locations with `file.py:line` references

2. **Create tasks for follow-ups**
   ```bash
   obs-task "refactor-authentication"
   ```

3. **Link to existing notes**
   - Reference related documentation
   - Build knowledge graph through links

### After Session

1. **Review and organize**
   - Add tags to notes
   - Create links between related notes
   - Update project index

2. **Update task status**
   - Mark completed tasks
   - Add new discovered tasks

3. **Archive session notes**
   - Move to appropriate project folder if needed
   - Link from project index

## Best Practices

### Note Creation

**DO:**
- ✅ **ALWAYS ask user where to save the note first** - Show vault structure and suggest options
- ✅ Create notes during the session, not after
- ✅ Use descriptive file names (kebab-case)
- ✅ Include YAML frontmatter with metadata
- ✅ Link to related notes and concepts
- ✅ Add relevant tags for organization
- ✅ Include timestamps for temporal context

**DON'T:**
- ❌ **Decide note location without asking user** - This is the #1 rule
- ❌ Create huge monolithic notes
- ❌ Forget to link related concepts
- ❌ Skip metadata and tags
- ❌ Use unclear or generic titles
- ❌ Duplicate information across notes

### Task Management

**DO:**
- ✅ Use checkbox syntax `- [ ]` for tasks
- ✅ Add priority indicators
- ✅ Link tasks to relevant notes
- ✅ Include context in task description
- ✅ Break down large tasks into subtasks

**DON'T:**
- ❌ Create tasks without context
- ❌ Leave tasks orphaned (unlinked)
- ❌ Forget to update task status
- ❌ Mix tasks and notes in disorganized way

### Linking and Tags

**DO:**
- ✅ Use wikilinks `[[note]]` liberally
- ✅ Create hierarchical tags `#project/area/topic`
- ✅ Link bidirectionally when relevant
- ✅ Tag by type, status, and project
- ✅ Build a web of knowledge

**DON'T:**
- ❌ Over-tag (diminishing returns)
- ❌ Use inconsistent tag hierarchies
- ❌ Create links without purpose
- ❌ Forget to use tag search features

## Obsidian Plugins for Claude Integration

### Recommended Plugins

1. **Templater** - Advanced templates with dynamic content
2. **Dataview** - Query and display notes dynamically
3. **Tasks** - Enhanced task management
4. **Calendar** - Visual daily note navigation
5. **Git** - Version control for vault (if using)
6. **Quick Add** - Rapid note creation with macros

### Dataview Examples for Claude Sessions

```dataview
# Recent Claude sessions
TABLE date, summary
FROM #claude-session
SORT date DESC
LIMIT 10
```

```dataview
# Pending tasks from sessions
TASK
FROM #claude-session
WHERE !completed
```

## Troubleshooting

### Issue 1: Vault environment variable not set

**Problem**: Environment variable not defined

**Solution**:
```bash
# Add to shell profile
echo 'export OBSIDIAN_VAULT_PATH="/path/to/vault"' >> ~/.zshrc
source ~/.zshrc
```

### Issue 2: Note not appearing in Obsidian

**Problem**: File created but not visible

**Solution**:
- Ensure file has `.md` extension
- Check file permissions
- Verify path is within vault
- Refresh Obsidian file list

### Issue 3: Links not working

**Problem**: Wikilinks don't navigate correctly

**Solution**:
- Ensure exact note name match (case-sensitive)
- Check for file extension in link (shouldn't include `.md`)
- Verify linked note exists
- Use Obsidian's link autocomplete

### Issue 4: Frontmatter rendering in preview

**Problem**: YAML frontmatter shows as text

**Solution**:
- Ensure frontmatter is first thing in file
- Use proper YAML syntax (three dashes before and after)
- Check for trailing spaces

### Issue 5: Environment Variable Mismatches

**Symptom**: `TypeError: expected str, bytes or os.PathLike object, not NoneType`

**Cause**: Wrong variable name used

**Diagnosis Steps**:
```bash
# Check which variable is actually set
echo $OBSIDIAN_VAULT_PATH
echo $OBSIDIAN_VAULT
echo $OBSIDIAN_PATH

# List all Obsidian-related variables
env | grep -i obsidian
```

**Common Variable Names**:
- `$OBSIDIAN_VAULT_PATH` (recommended)
- `$OBSIDIAN_VAULT` (also common)
- `$OBSIDIAN_PATH` (alternative)

**Resolution**:
1. Check which variable the user has set
2. Use that variable consistently
3. Update ALL references if changing variable names

## Quick Reference

### Creating Notes with Claude

```bash
# Session note
cat > "$OBSIDIAN_VAULT_PATH/Sessions/$(date +%Y-%m-%d)-topic.md" <<'EOF'
---
date: 2026-01-23
type: session-note
tags:
  - claude-session
  - dump
---
# Content here
EOF

# Task note
cat > "$OBSIDIAN_VAULT_PATH/Tasks/task-name.md" <<'EOF'
---
date: 2026-01-23
type: task
tags: [task, status/pending]
---
# Task: task-name
- [ ] Step 1
EOF

# Quick append to daily
echo "## Note

Content" >> "$OBSIDIAN_VAULT_PATH/Daily/$(date +%Y-%m-%d).md"
```

### Essential Obsidian Syntax

```markdown
# Wikilinks
[[Note Name]]
[[Note#Heading]]
[[Note|Display Text]]

# Tags
#tag
#hierarchical/tag

# Tasks
- [ ] Pending
- [x] Done

# Callouts
> [!note]
> Content

> [!warning]
> Warning content

> [!tip]
> Tip content

# Block references
^block-id
[[Note#^block-id]]

# Properties (frontmatter)
---
key: value
tags: [tag1, tag2]
---
```

## Integration with Other Skills

This skill works well with:
- **obs-vault:obs-memory** - Vault structure commands and session memory
- **obs-vault:obsidian-markdown** - Proper Obsidian-flavored markdown syntax
- **folder-organization** - Vault structure standards

## References and Resources

- [Obsidian Documentation](https://help.obsidian.md/)
- [Obsidian Community Plugins](https://obsidian.md/plugins)
- [Zettelkasten Method](https://zettelkasten.de/introduction/)
- [PARA Method](https://fortelabs.com/blog/para/) - Projects, Areas, Resources, Archives

---

**Remember**: The goal is to build a searchable, linked knowledge base that grows with each session. Start simple, add structure as needed.
