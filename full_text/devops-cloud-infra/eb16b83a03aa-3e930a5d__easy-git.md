---
name: easy-git
description: This skill should be used when the user wants to save work ("save snapshot", "checkpoint this", "save my progress", "create savepoint", "capture this moment", "freeze this version", "record changes", "make a snapshot", "checkpoint prototype", "save version"), backup to cloud ("backup to cloud", "back up to cloud", "back this up", "back up my work", "sync up", "upload my work", "send to backup", "save to server", "publish my changes", "push to cloud", "backup online"), check changes ("what changed?", "show changes", "what did I do", "show me my work", "what's different", "list changes", "what have I modified", "what is new"), check ignored files ("what files are not tracked?", "what's not being uploaded?", "what is ignored?", "is there anything not being uploaded", "is there anything ignored by version control", "what's in gitignore", "show me ignored files"), get updates ("get latest", "sync down", "download updates", "pull from cloud", "refresh from server", "update from backup", "get changes from cloud"), label versions ("mark this version", "create milestone", "tag this", "bookmark version", "label this version", "name this version", "tag as release"), start tracking ("start version control", "initialize versioning", "begin tracking changes", "start keeping history", "make this a versioned project"), or get help ("tell me about Easy Git", "what can Easy Git do", "how does Easy Git work", "help me understand version control", "explain Easy Git", "what should I do now", "how do I backup", "help me with changes", "explain version tracking"). This skill translates natural language into git operations for non-technical users.
version: 1.3.0
allowed-tools:
  - Bash(git init*)
  - Bash(git add*)
  - Bash(git commit*)
  - Bash(git push*)
  - Bash(git pull*)
  - Bash(git status*)
  - Bash(git tag*)
  - Bash(git diff*)
  - Bash(git log*)
  - Bash(git remote*)
  - Bash(git branch*)
  - Bash(git config*)
  - Bash(gh*)
  - Bash(test*)
  - Bash(cat*)
  - Read
  - Write
  - Edit
---

# Easy Git - Natural Language Git Operations

Makes git accessible through plain language. No git knowledge required.

## When to Use This Skill

Invoke when the user uses natural, non-technical language to describe version control operations. This skill is designed for users who think in terms of:
- Saving drafts, versions, backups
- Protecting work, making it safe
- Publishing, syncing, sharing
- Checkpoints, milestones, progress markers

See trigger phrases in frontmatter description for full list.

## General Principles

### Suggest Easy Git Commands

When Claude Code needs to suggest git operations to users, **always suggest Easy Git natural language commands instead of bare git commands**, unless there is no Easy Git equivalent for the operation.

**Examples:**
- ✓ "Try: 'save my progress'" (Easy Git)
- ✗ "Try: git commit -am 'message'" (bare git)

- ✓ "Say: 'backup to cloud'" (Easy Git)
- ✗ "Run: git push origin main" (bare git)

- ✓ "To see changes: 'what changed?'" (Easy Git)
- ✗ "Run: git status" (bare git)

**When to use bare git commands:**
- For advanced operations not covered by Easy Git (e.g., git rebase, git cherry-pick)
- When the user explicitly asks for the git command syntax
- In the "What I did" section after execution (showing what commands were run)

### Default to Private Repositories

When using `gh` CLI to create repositories, **always default to private repositories** unless the user explicitly requests public.

Use: `gh repo create --private` instead of `gh repo create --public`

## Agent Workflow Guidelines

### When Claude Code Should Proactively Commit

When Claude Code is working on behalf of the user, it should proactively use Easy Git commands to save work without user prompting. This ensures user work is always protected.

**IMPORTANT**: These are suggested minimums, not maximums. Always feel free to commit whenever you think it's appropriate. Better to commit too often than too rarely - commits are cheap and ensure work safety.

**Context-based triggers to commit:**

1. **After completing discrete tasks**
   - Finished implementing a feature the user requested
   - Fixed a bug and verified the fix
   - Completed refactoring a component
   - Action: Use "save my progress" or "checkpoint this"

2. **Before risky operations**
   - Before trying experimental approaches
   - Before making significant architectural changes
   - Before running destructive operations
   - Action: Use "save a checkpoint" as safety measure

3. **After writing significant code**
   - Added/modified 3+ files in a logical unit
   - Completed a meaningful subtask within larger work
   - Reached a working state after debugging
   - Action: Use "save snapshot"

4. **At natural stopping points**
   - User asks to see current state ("show me", "what changed")
   - Before switching to different part of codebase
   - After resolving errors/conflicts
   - Action: Use "checkpoint this"

5. **When explicitly requested**
   - User says: "commit this", "save this"
   - Use Easy Git phrases, not bare git commands
   - Action: Use "save my progress"

**Frequency guidance**: Commit frequently at logical checkpoints (every 1-3 meaningful changes). Err on the side of more commits rather than fewer.

### When Claude Code Should Proactively Push

Claude Code should backup work to cloud at appropriate intervals to ensure safety.

**Context-based triggers to push:**

1. **After accumulating commits**
   - 5+ commits since last push (suggested minimum)
   - Safety: Ensure work is backed up regularly
   - Action: Use "backup to cloud"

2. **At natural stopping points**
   - User says: "that's all", "thanks", "I'm done for now"
   - End of a work session or major task completion
   - Before user likely leaves or switches context
   - Action: Use "backup to cloud"

3. **After significant milestones**
   - Completed major feature or bug fix
   - User created a tag/version marker
   - Reached a stable, working state
   - Action: Use "backup to cloud"

4. **When explicitly requested**
   - User asks to push: "push this", "upload", "backup"
   - Use Easy Git phrases
   - Action: Use "backup to cloud"

**Frequency guidance**: Push regularly (after 5+ commits or at session end). Push sooner if it makes sense (e.g., after completing major milestone). Balance safety with not being disruptive.

### Core Principle

Claude Code should use Easy Git natural language commands internally, never bare git commands, to maintain consistency with the skill's design. This protects user work without requiring them to remember to save.

## Core Capabilities

### 1. Initialize Tracking (INIT)

Detect uninitialized repos and guide users through setup.

**When to use:**
- User mentions "start tracking", "initialize", "begin version control"
- Any operation attempted on uninitialized repo

**Context gathering:**
```bash
# Check if git is initialized
test -d .git && echo "initialized" || echo "not initialized"
```

**Workflow:**
1. Check if `.git` directory exists
2. If not initialized:
   - Explain benefits in plain language
   - Ask for confirmation (optional - can auto-execute)
   - Run `git init`
   - Configure user name/email if needed
   - Offer to set up remote backup (GitHub, GitLab, etc.)
3. Provide confirmation message

**Output format:**
```
✓ Started tracking your project!

What I did:
• Initialized version control (git init)
• Set up local history tracking

Git context: This created a hidden .git folder that tracks all your changes.

Next steps:
• Save a snapshot: "save my progress"
• Backup to cloud: "backup to cloud" (requires GitHub/GitLab setup)
```

### 2. Save Snapshot (COMMIT)

Stage all changes and commit with auto-generated message.

**When to use:**
- "save snapshot", "checkpoint", "save progress", "capture this", "record changes"
- Any saving/checkpointing language

**Context gathering:**
```bash
# Get current changes
git diff HEAD
git status --short
git log --oneline -5
```

**Workflow:**
1. Gather context about what changed
2. Check for dot files/directories that should be ignored:
   - Look for `.claude`, `.obsidian`, `.vscode`, `.idea`, `.cursor`, etc.
   - Check if these are in the staging area or untracked
   - If found and not already in .gitignore, offer to ignore them:
     ```
     💡 I noticed some development tool files that are usually not uploaded:
     • .claude/ (Claude Code configuration)
     • .obsidian/ (Obsidian vault settings)

     Would you like me to exclude these from version control?
     Say "yes, ignore those" or "no, track everything"
     ```
   - If user agrees, create or update .gitignore before committing
3. Analyze file changes to understand the work:
   - What files were added/modified/deleted
   - Nature of changes (docs, code, config, assets)
   - Look for patterns (feature, fix, update, refactor)
4. Generate descriptive commit message:
   - Summarize what changed concisely
   - Focus on what/why, not how
   - Use present tense
   - Example: "Update documentation and add examples"
5. Execute:
   ```bash
   git add -A
   git commit -m "generated message"
   ```
6. Display result in plain language + git commands

**Common dot files/directories to suggest ignoring:**
- `.claude/` - Claude Code configuration
- `.obsidian/` - Obsidian vault settings
- `.vscode/` - VS Code settings
- `.idea/` - JetBrains IDE settings
- `.cursor/` - Cursor editor settings
- `.DS_Store` - macOS filesystem metadata
- `node_modules/` - Node.js dependencies
- `.env` - Environment variables (sensitive!)
- `.env.local` - Local environment overrides

**Output format:**
```
✓ Saved a snapshot of your work

What I did:
• Staged all changes (git add -A)
• Created snapshot: "Update documentation and add examples" (git commit)

Files saved:
• Modified: README.md, docs/guide.md
• Added: examples/workflow.md

Git context: This is called "committing" - you can always return to this exact point.
```

### 3. Check Changes (STATUS)

Show what's different since last snapshot.

**When to use:**
- "what changed", "show changes", "what did I do", "what's different"
- Any inquiry about current state

**Context gathering:**
```bash
git status
git diff --stat
git diff --name-status
```

**Workflow:**
1. Get git status and diff statistics
2. Categorize changes:
   - New files (never tracked before)
   - Modified files (changed since last snapshot)
   - Deleted files
3. Translate into plain language
4. Show summary statistics

**Output format:**
```
Here's what changed since your last snapshot:

Modified files:
• README.md (23 lines changed)
• src/app.js (12 lines changed)

New files:
• examples/demo.js

Summary: 2 files modified, 1 file added

Git context: These are "uncommitted changes" - save a snapshot to preserve them.
```

#### 3a. Check Ignored Files (STATUS - IGNORED)

Show what files/directories are being excluded from version control.

**When to use:**
- "what files are not tracked?", "what's not being uploaded?", "what is ignored?"
- "is there anything not being uploaded", "is there anything ignored by version control"
- "what's in gitignore", "show me ignored files"

**Context gathering:**
```bash
# Check if .gitignore exists
test -f .gitignore && cat .gitignore || echo "No .gitignore file"

# Show currently ignored files that exist
git status --ignored --short
```

**Workflow:**
1. Check if .gitignore exists
2. If exists:
   - Read .gitignore patterns
   - List currently ignored files that exist in the working directory
   - Explain what each pattern means in plain language
3. If doesn't exist:
   - Explain that nothing is being ignored
   - Offer to create .gitignore if needed

**Output format (with .gitignore):**
```
Here's what's not being uploaded to version control:

Ignored patterns:
• .claude/ - Claude Code configuration files
• .obsidian/ - Obsidian vault settings
• .DS_Store - macOS system files
• node_modules/ - Node.js dependencies

Currently ignored files in your project:
• .claude/settings.local.json
• .obsidian/workspace.json
• .DS_Store

Git context: These files are listed in .gitignore and won't be included when
you save snapshots or backup to the cloud.
```

**Output format (no .gitignore):**
```
💡 No files are being ignored

You don't have a .gitignore file, so all files in this directory will be
tracked when you save snapshots.

Would you like to create one to exclude common files like:
• Development tool settings (.vscode, .idea, .claude)
• System files (.DS_Store)
• Dependencies (node_modules)

Say "yes, create gitignore" if you'd like me to set this up.

Git context: A .gitignore file tells git which files to never track or upload.
```

### 4. Backup to Cloud (PUSH)

Upload local snapshots to remote repository.

**When to use:**
- "backup to cloud", "sync up", "upload", "publish", "send to backup"
- Any cloud/remote upload language

**Context gathering:**
```bash
git remote -v
git branch --show-current
git log @{u}.. --oneline 2>&1
git status
```

**Workflow:**
1. Check if remote exists:
   - If no remote: Guide through GitHub/GitLab setup
   - Explain what a remote is in plain language
   - **When using gh CLI, default to private**: `gh repo create --private`
2. Check for uncommitted changes:
   - If uncommitted: Ask if they want to save snapshot first
3. Check tracking branch:
   - If no upstream: Set up tracking with `git push -u origin [branch]`
4. Execute push:
   ```bash
   git push origin [branch]
   ```
5. Handle errors:
   - Authentication: Guide through credential setup
   - Rejected push: Explain need to pull first
   - No commits: Explain nothing to backup

**Output format:**
```
✓ Backed up your work to the cloud

What I did:
• Uploaded 3 snapshots to cloud storage (git push origin main)

Snapshots backed up:
• "Update documentation and add examples"
• "Fix configuration bug"
• "Add new feature"

Git context: This is called "pushing" - your work is now safe on the remote server.
```

### 5. Get Updates (PULL)

Download changes from remote repository.

**When to use:**
- "get latest", "sync down", "download updates", "pull from cloud"
- Any download/sync from remote language

**Context gathering:**
```bash
git remote -v
git branch --show-current
git status
git diff --stat
```

**Workflow:**
1. Check for uncommitted changes:
   - If uncommitted: Warn that they might be lost
   - Offer to save snapshot first
2. Check remote exists:
   - If no remote: Explain can't sync without cloud setup
3. Execute pull:
   ```bash
   git pull
   ```
4. Detect merge conflicts:
   - If conflicts: Provide plain-language conflict resolution guidance
   - List conflicted files
   - Offer resolution options
5. Display update summary

**Output format (no conflicts):**
```
✓ Downloaded latest updates from cloud

What I did:
• Synced with cloud storage (git pull)

Updates received:
• "Update API endpoints" (by teammate)
• "Fix typo in README" (by teammate)

Files changed:
• Modified: src/api.js, README.md

Git context: This is called "pulling" - you now have the latest version.
```

**Output format (with conflicts):**
```
⚠ Your local work conflicts with cloud version

What happened: Someone else changed the same files you did.

Files with conflicts:
• README.md (both you and teammate edited the same sections)
• config.json (different values for same setting)

Options:
1. Keep your version: "use my version"
2. Use cloud version: "use cloud version"
3. Fix manually: I'll guide you through editing the files

Git context: This is called a "merge conflict" - it happens when the same
content is edited in two places.
```

### 6. Label Version (TAG)

Create named milestone for current snapshot.

**When to use:**
- "mark this version", "create milestone", "tag this", "label version"
- "name this version X", "tag as X"

**Context gathering:**
```bash
git tag -l
git log -1 --oneline
git status
```

**Workflow:**
1. Check for uncommitted changes:
   - If uncommitted: Suggest saving snapshot first
2. Extract tag name from user input:
   - Look for version numbers (v1.0.0, 1.2.3)
   - Look for milestone names ("beta", "launch", "working-version")
   - If not specified: Ask what to name it
3. Check if tag already exists:
   - If exists: Warn and ask for different name
4. Create tag:
   ```bash
   git tag [name]
   ```
5. Offer to backup tag to cloud:
   ```bash
   git push origin [name]
   ```

**Output format:**
```
✓ Labeled this version as "v1.0.0"

What I did:
• Created version label "v1.0.0" (git tag v1.0.0)
• Backed up label to cloud (git push origin v1.0.0)

This label points to:
• Snapshot: "Add new feature and documentation"

Git context: This is called "tagging" - you can always return to this named version.
```

### 7. Get Help (HELP)

Provide self-documentation and guidance about Easy Git capabilities.

**When to use:**
- "tell me about Easy Git", "what can Easy Git do", "how does Easy Git work"
- "help me understand version control", "explain Easy Git", "what is Easy Git"
- "what should I do now", "what can I do", "what's next"
- Questions: "how do I backup", "how do I save", "how do I check changes"

**Trigger differentiation (critical):**
- **Questions** ("how do I", "what can", "tell me about", "explain") → HELP
- **Actions** ("help me backup this project", "save my work") → Execute action (PUSH, COMMIT, etc.)
- If ambiguous, default to action but acknowledge help is available

**Context gathering (for contextual help):**
```bash
# Check repo state
test -d .git && echo "initialized" || echo "not initialized"
git status --short 2>/dev/null
git log -1 --oneline 2>/dev/null || echo "no commits"
git remote -v 2>/dev/null | grep -q . && echo "has remote" || echo "no remote"
```

**Workflow:**

1. **Detect help type:**
   - **General**: About Easy Git overall ("tell me about Easy Git", "what can you do")
   - **Specific**: About particular capability ("how do I backup", "explain saving")
   - **Contextual**: "what should I do now", "what's next"

2. **For General help:**

Provide overview of all capabilities with example phrases:

```
💡 Easy Git makes version control simple

I translate everyday language into git operations - no git knowledge required!

What I can do:

📸 Save snapshots
• "save my progress" - Create a checkpoint of your work
• "checkpoint this" - Freeze this version

🔍 Show changes
• "what changed?" - See what you modified
• "show my changes" - List your edits

🚫 Check ignored files
• "what's not being uploaded?" - See excluded files
• "what's in gitignore" - Show ignored patterns

☁️ Backup to cloud
• "backup to cloud" - Upload your work to GitHub/GitLab
• "sync up" - Send changes to server

⬇️ Get updates
• "get latest" - Download from cloud
• "sync down" - Get team's changes

🏷️ Label versions
• "mark this as v1.0" - Name important versions
• "tag as release" - Create milestone markers

🎬 Start tracking
• "start version control" - Begin tracking changes
• "initialize tracking" - Set up version history

Common workflows:
• Daily backup: "what changed?" → "save my progress" → "backup to cloud"
• Multi-device: "backup my work" on device 1 → "get latest" on device 2

Want details on a specific operation? Ask: "how do I backup" or "explain saving"
```

3. **For Specific help:**

Map user query to capability and provide detailed guidance:

**Capability mapping from query:**
- "backup/cloud/upload/sync up/push" → Explain PUSH
- "save/snapshot/checkpoint/commit" → Explain COMMIT
- "changes/status/what changed/modified" → Explain STATUS
- "ignored/not tracked/not uploaded/gitignore" → Explain STATUS-IGNORED
- "get/download/sync down/pull/latest" → Explain PULL
- "label/tag/mark/milestone/version" → Explain TAG
- "start/initialize/begin/tracking" → Explain INIT

**For COMMIT (example template):**
```
💡 Saving your work with Easy Git

What it does:
Saves a snapshot (checkpoint) of your current work that you can return to later.

How to use it:
1. Make changes to your files
2. Say: "save my progress" (or "checkpoint this", "save a snapshot")
3. Easy Git will:
   • Look at all your changes
   • Create a descriptive commit message automatically
   • Save the snapshot to your local history

Alternative phrases:
• "save my progress"
• "checkpoint this"
• "save a snapshot"
• "create a savepoint"
• "freeze this version"
• "record my changes"

Git context: This is called "committing" - it creates a permanent record in your
project history that you can always come back to.

Common workflow:
"what changed?" → see your edits → "save my progress" → snapshot saved

Ready to try it? Say: "save my progress"
```

**Adapt template for each capability** with appropriate phrases and workflows.

4. **For Contextual help:**

Check repo state and suggest next logical steps:

**If not initialized:**
```
💡 You're not tracking versions yet

Current state: This project doesn't have version control set up.

What you can do now:
1. "start version control" - Begin tracking your changes

Once initialized, you'll be able to:
• Save snapshots of your work
• Go back to earlier versions
• Backup to the cloud

Want to learn more? Ask: "tell me about Easy Git"
```

**If initialized, no commits:**
```
💡 Ready to save your first snapshot

Current state: Version control is set up, but you haven't saved anything yet.

What you can do now:
1. "what changed?" - See what files are in your project
2. "save my progress" - Create your first snapshot

This will start tracking your project history!

Want to learn more about saving? Ask: "how do I save work"
```

**If has commits, has changes:**
```
💡 You have unsaved work

Current state:
• Version control: Active
• Uncommitted changes: Yes
• Last snapshot: [commit message]

Suggested next steps:
1. "what changed?" - Review your modifications
2. "save my progress" - Save these changes
3. "backup to cloud" - Upload to GitHub/GitLab (if configured)

Common workflow: check → save → backup

Want help with a specific step? Just ask!
```

**If has commits, clean, no remote:**
```
💡 Your work is saved locally

Current state:
• Version control: Active
• Uncommitted changes: None
• Last snapshot: [commit message]
• Cloud backup: Not configured

Suggested next steps:
1. Make changes to your files, then "save my progress"
2. Set up cloud backup: "backup to cloud" (I'll guide you through it)

Your work is safe locally. Cloud backup provides extra protection and enables
working from multiple devices.

Want to set up cloud backup? Ask: "how do I backup to cloud"
```

**If has commits, clean, has remote:**
```
💡 Everything is saved and backed up

Current state:
• Version control: Active
• Uncommitted changes: None
• Last snapshot: [commit message]
• Cloud backup: Configured ✓

You're all set! Next steps:
1. Make changes to your files
2. "what changed?" - See your modifications
3. "save my progress" - Save snapshot
4. "backup to cloud" - Upload to server

You can also:
• "get latest" - Download updates from cloud
• "mark this as [version]" - Label important versions
• "show my history" - See past snapshots

Want help with anything? Just ask!
```

**Error states:**

If help requested during error (merge conflict, auth error, etc.):
- Acknowledge the current issue
- Provide specific help for that error
- Reference general help for other operations

**Output format:**

All help modes follow Easy Git standards:
- Status indicator: 💡 (info)
- Plain language explanation
- Actionable examples with specific phrases
- "Try this" or "Want more" suggestions
- Brief git context where helpful (not overwhelming)

## Intent Analysis

Use natural language understanding to map user phrases to operations. Don't rely on exact phrase matching - understand the intent.

**Mapping guide:**
- **Saving/snapshot/checkpoint/progress/record/capture/freeze** → COMMIT
- **Backup/sync up/upload/publish/send to server/push** → PUSH
- **Changes/different/modified/what did I do/show work** → STATUS
- **Not tracked/ignored/not uploaded/gitignore/excluded** → STATUS-IGNORED
- **Get/download/sync down/update from/pull/refresh** → PULL
- **Mark/label/milestone/tag/bookmark/name version** → TAG
- **Start/initialize/begin tracking/version control** → INIT
- **Tell me about/what can/how do I/explain/help understand** → HELP
  - "tell me about Easy Git" → HELP (general)
  - "what can Easy Git do" → HELP (general)
  - "how does Easy Git work" → HELP (general)
  - "how do I backup" → HELP (specific: PUSH)
  - "explain saving" → HELP (specific: COMMIT)
  - "what should I do now" → HELP (contextual)
  - "help me backup this project" → PUSH (action, not help)

**Context clues:**
- "to cloud", "to server", "online" → suggests PUSH
- "from cloud", "from server", "latest" → suggests PULL
- "what", "show", "list" → suggests STATUS
- "not tracked", "ignored", "not uploaded", "gitignore" → suggests STATUS-IGNORED
- "this version", "this as", "[name]" → suggests TAG

## Error Handling Strategies

### No .git directory
```
💡 You're not tracking versions yet!

Would you like to start? This will:
• Keep a history of your changes
• Let you go back to earlier versions
• Enable backup to the cloud (optional)

Say "yes, start tracking" or "start version control" to begin.
```

### No remote configured (when trying to push/pull)
```
💡 No cloud backup is set up yet

To backup to the cloud, you need to:
1. Create a repository on GitHub or GitLab
2. Connect it to this project

Would you like help setting this up? Say "set up cloud backup" and I'll guide you.

Note: If using gh CLI, repositories will be created as private by default.
```

### Uncommitted changes (when pulling)
```
⚠ You have unsaved changes

Before getting updates from the cloud, you should save your current work.

Options:
1. "save my progress" - Create a snapshot first (recommended)
2. "discard my changes" - Throw away current changes (careful!)
3. "cancel" - Don't sync right now

Git context: This prevents your work from being lost during the sync.
```

### Merge conflicts
```
⚠ Your local work conflicts with cloud version

What happened: Both you and someone else changed the same parts of these files:
• README.md (lines 15-23)
• config.json (line 8)

Options:
1. "keep my version" - Use your changes (git checkout --ours [file])
2. "use cloud version" - Use their changes (git checkout --theirs [file])
3. "show me the conflicts" - I'll show you what's different
4. "help me fix it" - Guide me through manual resolution

Git context: This is a "merge conflict" - git can't automatically combine the changes.
```

### Detached HEAD
```
⚠ You're viewing an old version

You're currently looking at an old snapshot, not your current work.

To get back to your current work: "go back to main"

Git context: This is called "detached HEAD" - you're in read-only history mode.
```

### Authentication errors
```
⚠ Can't connect to cloud storage

Problem: Authentication failed - git can't verify who you are.

Solutions:
1. If using GitHub: Set up a personal access token
2. If using SSH: Set up SSH keys
3. Check your credentials are up to date

Say "help with authentication" for detailed setup instructions.
```

### Nothing to commit
```
💡 No changes to save

You haven't modified anything since your last snapshot.

Git context: This is normal - you can only save when there are changes.
```

### Already up to date (pull)
```
✓ Already up to date

You already have the latest version from the cloud - no updates available.

Git context: Your local copy matches the remote - nothing to download.
```

## Output Format Standards

Always structure responses with:

1. **Status indicator:** ✓ (success), ⚠ (warning), 💡 (info)
2. **Plain language summary:** What happened in user terms
3. **What I did:** Bullet list with git commands in parentheses
4. **Relevant details:** Files, messages, counts
5. **Git context:** Brief explanation of the git concept

**Example:**
```
✓ Backed up your work to the cloud

What I did:
• Staged all changes (git add -A)
• Created snapshot: "Update documentation and examples" (git commit)
• Uploaded to cloud (git push origin main)

Files backed up:
• Modified: README.md, docs/guide.md
• Added: examples/workflow.md

Git context: This is called "committing and pushing" - your work is now safely
stored on the remote server and you can access it from anywhere.
```

## First-Time User Experience

When a user attempts any operation on an uninitialized repository:

1. **Detect state:**
   ```bash
   test -d .git && echo "initialized" || echo "not initialized"
   ```

2. **Provide friendly explanation:**
   ```
   💡 You're not tracking versions yet!

   Would you like to start? This will:
   • Keep a history of your changes
   • Let you go back to earlier versions
   • Enable backup to the cloud (optional)

   Say "yes, start tracking" or "start version control" to begin.
   ```

3. **After initialization:**
   ```
   ✓ Started tracking your project!

   What I did:
   • Initialized version control (git init)

   Next steps:
   • Save a snapshot: "save my progress"
   • Check what changed: "what changed?"
   • Backup to cloud: "backup to cloud" (requires GitHub/GitLab setup)

   Git context: You now have a hidden .git folder that tracks all your changes.
   ```

## Advanced Workflows

### First commit + push
When user wants to backup but has never committed:
1. Detect no commits exist
2. Suggest: "save a snapshot first"
3. Auto-chain: commit → push

### Pull before push
When user tries to push but remote has new commits:
1. Detect push rejection
2. Explain: "cloud has updates you don't have"
3. Suggest: "get latest updates first"
4. Guide through: pull → resolve conflicts (if any) → push

### Smart commit message generation
Analyze git diff to create messages:
- File types: docs → "Update documentation", code → "Modify [component]"
- Patterns: new files → "Add [feature]", deletions → "Remove [feature]"
- Mix: "Update [X] and add [Y]"
- Keep under 72 characters
- Be specific but concise

## Reference Materials

- See `references/personas.md` for language variations across user types
- See `references/git-primer.md` for git concepts in plain language
- See `examples/workflows.md` for complete scenario walkthroughs

## Testing Checklist

- [ ] Init: new project, already initialized
- [ ] Commit: changes exist, no changes, generated message quality
- [ ] Status: various file states (modified, new, deleted)
- [ ] Push: first push, subsequent push, no remote, auth error
- [ ] Pull: clean pull, merge conflicts, already up to date
- [ ] Tag: create tag, duplicate tag, push tag
- [ ] Errors: handle all error scenarios gracefully
- [ ] Persona phrases: test all trigger phrases work
