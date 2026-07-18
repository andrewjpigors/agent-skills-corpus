---
name: kanban
description: "Stage 7 - Generates an interactive Kanban board (Markdown & HTML) and Mermaid flow to visualize and track the status of implementation slices."
---

# Skill: Kanban & Implementation Tracker (Stage 7)

## Objective
Your goal is to act as the **Orchestration Engine** to generate a local, interactive Kanban board and a visual Mermaid diagram representing the progress state of the current feature development's vertical slices. This enables real-time visual progress tracking during active TDD implementation (Stage 7).

## Rules of Engagement
- **Artifact Generation:** Always output:
  1. `plans/<feature-slug>/<timestamp>/05_KANBAN.md` - Clean Markdown Kanban board and Mermaid flow diagram.
  2. `plans/<feature-slug>/<timestamp>/kanban.html` - Premium interactive local progress tracking application.
- **Visual Design Mandate:** The generated HTML MUST follow a top-tier premium visual aesthetic (sleek, futuristic mocha dark theme, glowing glassmorphism cards, micro-animations, and full-screen layout). No placeholders allowed.
- **Dynamic Coupling:** The HTML file must contain a built-in parser that can load and display the contents of the local `05_PLAN.md` file, while also offering an "Import/Export" zone where developers can copy-paste their Markdown and interactively manage state.

## Instructions

### Step 1: Locate Active Plan
1. Find the active plan directory `plans/<feature-slug>/<timestamp>/` for the feature currently being implemented.
2. Read the `05_PLAN.md` (or `05_IMPLEMENTATION_PLAN.md`) file to extract the checklist tasks and implementation details.

### Step 2: Generate 05_KANBAN.md
Create a visual overview of the vertical slices in Markdown:
1. **Mermaid Flowchart:** Map out each Phase and Step as node blocks. Style the nodes dynamically based on status:
   - Completed slices: Fill with green (`#a6e3a1`), stroke with dark green.
   - In-progress slices: Fill with cyan/blue (`#89b4fa`), stroke with blue.
   - Pending slices: Fill with mocha gray (`#313244`), stroke with lighter gray.
2. **Markdown Kanban Columns:**
   - **Backlog / To Do:** List of pending slices.
   - **In Progress:** The active slice currently being implemented.
   - **Done:** Completed slices.

### Step 3: Generate kanban.html
Write a gorgeous, self-contained interactive web page inside `plans/<feature-slug>/<timestamp>/kanban.html` using the template below. 

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bean-to-Cup Progress Tracker</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-color: #11111b;
      --panel-bg: rgba(30, 30, 46, 0.7);
      --card-bg: rgba(49, 50, 68, 0.4);
      --card-hover-bg: rgba(49, 50, 68, 0.65);
      --border-color: rgba(147, 153, 178, 0.2);
      --accent-blue: #89b4fa;
      --accent-green: #a6e3a1;
      --accent-yellow: #f9e2af;
      --accent-red: #f38ba8;
      --accent-mauve: #cba6f7;
      --accent-teal: #94e2d5;
      --text-main: #cdd6f4;
      --text-sub: #a6adc8;
      --text-dim: #6c7086;
      --glow-blue: rgba(137, 180, 250, 0.2);
      --glow-green: rgba(166, 227, 161, 0.25);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-color);
      color: var(--text-main);
      font-family: 'Outfit', sans-serif;
      min-height: 100vh;
      overflow-x: hidden;
      padding: 1.5rem;
      background-image: 
        radial-gradient(at 10% 10%, rgba(203, 166, 247, 0.05) 0px, transparent 50%),
        radial-gradient(at 90% 90%, rgba(137, 180, 250, 0.05) 0px, transparent 50%);
    }

    /* Scrollbar Styling */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: transparent;
    }
    ::-webkit-scrollbar-thumb {
      background: var(--border-color);
      border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: var(--text-dim);
    }

    /* Main Grid Layout */
    .container {
      display: grid;
      grid-template-columns: 280px 1fr;
      gap: 1.5rem;
      max-width: 1600px;
      margin: 0 auto;
      height: calc(100vh - 3rem);
    }

    /* Left Control Sidebar */
    .sidebar {
      background: var(--panel-bg);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
      overflow-y: auto;
      box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .brand-icon {
      font-size: 2rem;
      animation: spin 8s linear infinite;
    }

    @keyframes spin {
      100% { transform: rotate(360deg); }
    }

    .brand-text h1 {
      font-size: 1.25rem;
      font-weight: 700;
      letter-spacing: -0.5px;
      background: linear-gradient(135deg, var(--accent-mauve), var(--accent-blue));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .brand-text p {
      font-size: 0.75rem;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    .stat-box {
      background: rgba(17, 17, 27, 0.4);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1rem;
      text-align: center;
    }

    .stat-num {
      font-size: 2rem;
      font-weight: 700;
      color: var(--accent-green);
      text-shadow: 0 0 10px var(--glow-green);
    }

    .stat-label {
      font-size: 0.75rem;
      color: var(--text-sub);
      text-transform: uppercase;
      margin-top: 0.25rem;
    }

    /* Progress Bar */
    .progress-container {
      width: 100%;
      height: 8px;
      background: rgba(17, 17, 27, 0.6);
      border-radius: 99px;
      overflow: hidden;
      margin-top: 0.5rem;
    }

    .progress-bar {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, var(--accent-blue), var(--accent-green));
      border-radius: 99px;
      transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Navigation / Actions */
    .btn {
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.75rem 1rem;
      border-radius: 8px;
      cursor: pointer;
      font-family: inherit;
      font-weight: 500;
      font-size: 0.875rem;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      transition: all 0.2s ease;
    }

    .btn:hover {
      background: var(--border-color);
      border-color: var(--text-sub);
      transform: translateY(-2px);
    }

    .btn-primary {
      background: linear-gradient(135deg, var(--accent-blue), #5892fc);
      border: none;
      color: #11111b;
      font-weight: 600;
    }

    .btn-primary:hover {
      background: linear-gradient(135deg, #a4c7fb, var(--accent-blue));
      box-shadow: 0 0 15px var(--glow-blue);
      color: #11111b;
    }

    /* Main Visual Area */
    .workspace {
      display: grid;
      grid-template-rows: auto 1fr 280px;
      gap: 1.5rem;
      overflow: hidden;
    }

    /* Top Dashboard Title */
    .header-dashboard {
      background: var(--panel-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 1rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15);
    }

    .header-info h2 {
      font-size: 1.25rem;
      font-weight: 600;
    }

    .header-info p {
      font-size: 0.85rem;
      color: var(--text-sub);
      font-family: 'JetBrains Mono', monospace;
    }

    /* Kanban Columns Wrapper */
    .board-columns {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1rem;
      overflow-y: hidden;
      height: 100%;
    }

    /* Column Container */
    .column {
      background: var(--panel-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      display: flex;
      flex-direction: column;
      height: 100%;
      overflow: hidden;
      box-shadow: 0 4px 24px 0 rgba(0, 0, 0, 0.15);
    }

    .column-header {
      padding: 1rem;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
      font-size: 0.95rem;
      letter-spacing: 0.5px;
    }

    .column-count {
      background: rgba(17, 17, 27, 0.6);
      border-radius: 99px;
      padding: 0.15rem 0.6rem;
      font-size: 0.75rem;
      color: var(--text-sub);
    }

    .column-body {
      padding: 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
      overflow-y: auto;
      height: 100%;
    }

    /* Specific column headers */
    .column-todo .column-header { border-left: 3px solid var(--accent-mauve); }
    .column-progress .column-header { border-left: 3px solid var(--accent-blue); }
    .column-done .column-header { border-left: 3px solid var(--accent-green); }

    /* Task Card */
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1rem;
      cursor: grab;
      position: relative;
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      overflow: hidden;
    }

    .card:active {
      cursor: grabbing;
    }

    .card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: transparent;
      transition: background 0.25s ease;
    }

    .card-todo::before { background: var(--accent-mauve); }
    .card-progress::before { background: var(--accent-blue); }
    .card-done::before { background: var(--accent-green); }

    .card:hover {
      background: var(--card-hover-bg);
      transform: translateY(-3px) scale(1.01);
      box-shadow: 0 4px 15px 0 rgba(0, 0, 0, 0.2);
      border-color: rgba(147, 153, 178, 0.4);
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 0.5rem;
    }

    .card-phase {
      font-size: 0.65rem;
      font-weight: 600;
      background: rgba(137, 180, 250, 0.15);
      color: var(--accent-blue);
      padding: 0.15rem 0.4rem;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .card-phase-done {
      background: rgba(166, 227, 161, 0.15);
      color: var(--accent-green);
    }

    .card-title {
      font-size: 0.875rem;
      font-weight: 500;
      line-height: 1.4;
      color: var(--text-main);
    }

    .card-meta {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-top: 0.75rem;
      font-size: 0.7rem;
      color: var(--text-sub);
      font-family: 'JetBrains Mono', monospace;
    }

    .card-meta-icon {
      font-size: 0.85rem;
    }

    /* Detail / Mermaid Lower Panel Split */
    .lower-section {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
      overflow: hidden;
      height: 100%;
    }

    /* Mermaid Panel */
    .panel-mermaid {
      background: var(--panel-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 4px 24px 0 rgba(0, 0, 0, 0.15);
    }

    .panel-mermaid h3 {
      font-size: 0.95rem;
      font-weight: 600;
      margin-bottom: 0.75rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .mermaid-viewport {
      background: rgba(17, 17, 27, 0.5);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1rem;
      flex: 1;
      overflow: auto;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    /* Card Inspector Panel */
    .panel-details {
      background: var(--panel-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 4px 24px 0 rgba(0, 0, 0, 0.15);
    }

    .panel-details h3 {
      font-size: 0.95rem;
      font-weight: 600;
      margin-bottom: 0.75rem;
    }

    .details-content {
      background: rgba(17, 17, 27, 0.5);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1rem;
      flex: 1;
      overflow-y: auto;
      font-size: 0.85rem;
      line-height: 1.5;
    }

    .details-empty {
      color: var(--text-dim);
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      font-style: italic;
    }

    .details-group {
      margin-bottom: 1rem;
    }

    .details-label {
      font-weight: 600;
      color: var(--accent-mauve);
      text-transform: uppercase;
      font-size: 0.7rem;
      letter-spacing: 0.5px;
      margin-bottom: 0.25rem;
    }

    .details-value {
      color: var(--text-main);
    }

    .details-code {
      font-family: 'JetBrains Mono', monospace;
      background: #11111b;
      padding: 0.5rem;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      margin-top: 0.25rem;
      overflow-x: auto;
    }

    /* Modal / Text Editor */
    .modal {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(17, 17, 27, 0.85);
      backdrop-filter: blur(12px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }

    .modal-content {
      background: var(--panel-bg);
      border: 1px solid var(--border-color);
      border-radius: 20px;
      width: 90%;
      max-width: 800px;
      height: 80vh;
      display: flex;
      flex-direction: column;
      padding: 1.5rem;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    }

    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
    }

    .modal-title {
      font-size: 1.15rem;
      font-weight: 600;
    }

    .modal-close {
      background: none;
      border: none;
      color: var(--text-sub);
      font-size: 1.5rem;
      cursor: pointer;
    }

    .modal-close:hover {
      color: var(--accent-red);
    }

    .editor-textarea {
      width: 100%;
      flex: 1;
      background: rgba(17, 17, 27, 0.6);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1rem;
      color: var(--text-main);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.85rem;
      line-height: 1.5;
      resize: none;
      outline: none;
    }

    .editor-textarea:focus {
      border-color: var(--accent-blue);
      box-shadow: 0 0 10px var(--glow-blue);
    }

    .modal-footer {
      display: flex;
      justify-content: flex-end;
      gap: 1rem;
      margin-top: 1rem;
    }

    /* Drag and Drop utility classes */
    .drag-over {
      background: rgba(137, 180, 250, 0.05);
      border: 1px dashed var(--accent-blue);
    }

    /* Micro-badges */
    .badge-status {
      display: inline-block;
      padding: 0.15rem 0.4rem;
      border-radius: 4px;
      font-size: 0.65rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .badge-status-todo { background: rgba(203, 166, 247, 0.15); color: var(--accent-mauve); }
    .badge-status-progress { background: rgba(137, 180, 250, 0.15); color: var(--accent-blue); }
    .badge-status-done { background: rgba(166, 227, 161, 0.15); color: var(--accent-green); }
  </style>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: false, theme: 'dark' });
    window.mermaid = mermaid;
  </script>
</head>
<body>

  <div class="container">
    
    <!-- SIDEBAR -->
    <div class="sidebar">
      <div class="brand">
        <div class="brand-icon">☕</div>
        <div class="brand-text">
          <h1>Brew-Board</h1>
          <p>Progress Swarm</p>
        </div>
      </div>

      <div class="stat-box">
        <div class="stat-num" id="progressPercent">0%</div>
        <div class="stat-label">Brew Complete</div>
        <div class="progress-container">
          <div class="progress-bar" id="progressBar"></div>
        </div>
      </div>

      <div class="stat-box" style="padding: 0.75rem;">
        <div style="font-size: 0.75rem; color: var(--text-sub); display: flex; justify-content: space-around;">
          <div>📋 <strong id="todoCount">0</strong> To Do</div>
          <div>⚡ <strong id="progCount">0</strong> Active</div>
          <div>✔ <strong id="doneCount">0</strong> Done</div>
        </div>
      </div>

      <button class="btn btn-primary" onclick="openModal('importModal')">📥 Import Plan (05_PLAN.md)</button>
      <button class="btn" onclick="exportMarkdown()">📤 Export Updated Plan</button>
      <button class="btn" onclick="loadLocalPlan()" style="margin-top: auto; border-color: rgba(166, 227, 161, 0.3);">🔄 Fetch Local Plan</button>
    </div>

    <!-- WORKSPACE -->
    <div class="workspace">
      
      <!-- TOP DASHBOARD -->
      <div class="header-dashboard">
        <div class="header-info">
          <h2 id="featureTitle">Feature Slices Implementation</h2>
          <p id="featurePath">plans/feature-slug/05_PLAN.md</p>
        </div>
        <div>
          <span class="badge-status badge-status-progress" id="sprintBadge">Brewing Active</span>
        </div>
      </div>

      <!-- KANBAN BOARD -->
      <div class="board-columns">
        
        <!-- TO DO -->
        <div class="column column-todo" id="todoColumn" ondragover="allowDrop(event)" ondragenter="dragEnter(event)" ondragleave="dragLeave(event)" ondrop="drop(event, 'todo')">
          <div class="column-header">
            <span>☕ BACKLOG (TO DO)</span>
            <span class="column-count" id="todoHeaderCount">0</span>
          </div>
          <div class="column-body" id="todoList"></div>
        </div>

        <!-- IN PROGRESS -->
        <div class="column column-progress" id="progressColumn" ondragover="allowDrop(event)" ondragenter="dragEnter(event)" ondragleave="dragLeave(event)" ondrop="drop(event, 'inprogress')">
          <div class="column-header">
            <span>⚡ EXTRACTION (ACTIVE)</span>
            <span class="column-count" id="progressHeaderCount">0</span>
          </div>
          <div class="column-body" id="progressList"></div>
        </div>

        <!-- DONE -->
        <div class="column column-done" id="doneColumn" ondragover="allowDrop(event)" ondragenter="dragEnter(event)" ondragleave="dragLeave(event)" ondrop="drop(event, 'done')">
          <div class="column-header">
            <span>✔ VERIFIED (DONE)</span>
            <span class="column-count" id="doneHeaderCount">0</span>
          </div>
          <div class="column-body" id="doneList"></div>
        </div>

      </div>

      <!-- LOWER SPLIT PANEL -->
      <div class="lower-section">
        
        <!-- MERMAID FLOWCHART -->
        <div class="panel-mermaid">
          <h3>📊 Pipeline Dependency Tree</h3>
          <div class="mermaid-viewport" id="mermaidContainer">
            <pre class="mermaid" id="mermaidOutput">
flowchart TD
  Start([Ready to Import])
            </pre>
          </div>
        </div>

        <!-- CARD DETAILS -->
        <div class="panel-details">
          <h3>🔍 Card Inspector</h3>
          <div class="details-content" id="detailsPanel">
            <div class="details-empty">
              <span>Select a slice card to audit the exact instructions, target files, and verification commands.</span>
            </div>
          </div>
        </div>

      </div>

    </div>

  </div>

  <!-- IMPORT MODAL -->
  <div class="modal" id="importModal">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title">Import 05_PLAN.md Markdown</h3>
        <button class="modal-close" onclick="closeModal('importModal')">&times;</button>
      </div>
      <p style="font-size: 0.8rem; color: var(--text-sub); margin-bottom: 0.75rem;">Paste the contents of your `05_PLAN.md` file below. The system will parse your vertical slices, checklist items, and descriptions automatically!</p>
      <textarea class="editor-textarea" id="importArea" placeholder="# Implementation Plan: ..."></textarea>
      <div class="modal-footer">
        <button class="btn" onclick="closeModal('importModal')">Cancel</button>
        <button class="btn btn-primary" onclick="processImport()">Compile Board & Flow</button>
      </div>
    </div>
  </div>

  <!-- EXPORT MODAL -->
  <div class="modal" id="exportModal">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title">Export Updated 05_PLAN.md</h3>
        <button class="modal-close" onclick="closeModal('exportModal')">&times;</button>
      </div>
      <p style="font-size: 0.8rem; color: var(--text-sub); margin-bottom: 0.75rem;">Here is your updated Markdown implementation plan reflecting the new card statuses. Copy this and paste it back into your `05_PLAN.md` file!</p>
      <textarea class="editor-textarea" id="exportArea" readonly onclick="this.select()"></textarea>
      <div class="modal-footer">
        <button class="btn btn-primary" onclick="copyExportText()">Copy Markdown</button>
        <button class="btn" onclick="closeModal('exportModal')">Done</button>
      </div>
    </div>
  </div>

  <script>
    // Task database
    let tasks = [];
    let planHeader = '';
    let planFooter = '';

    // Core markdown templates used when importing
    let originalMarkdown = '';

    // Global drag state
    let draggedCardId = null;

    // Default Demo Plan
    const demoPlan = `# Implementation Plan: Database Connection Refactoring

## 📋 Micro-Step Checklist
- [x] Phase 1: Database Ingestion Core
  - [x] Step 1.A: Setup Knex connection pooling configuration
  - [x] Step 1.B: Establish connection test suite
- [ ] Phase 2: Repository Slices
  - [ ] Step 2.A: Implement CoffeeBeanRepository
  - [ ] Step 2.B: Implement GrindRepository
- [ ] Phase 3: API Layer Integration
  - [ ] Step 3.A: Register repository services in Express IoC

## 📝 Step-by-Step Implementation Details
### Phase 1: Database Ingestion Core
#### Step 1.A (The Verification Harness):
* *Target File:* \`src/config/knex.ts\`
* *Verification:* Run \`npm run test:config\` to test knex.
* *Instructions:* Setup connection pools matching the postgres spec.

#### Step 1.B (The Core Change):
* *Target File:* \`test/knex.test.ts\`
* *Verification:* Run \`npm test\`
* *Instructions:* Establish basic connection and check pool size.

### Phase 2: Repository Slices
#### Step 2.A (The Verification Harness):
* *Target File:* \`test/repositories/bean.test.ts\`
* *Verification:* Run \`npm run test:repo\`
* *Instructions:* Create a test suite verifying basic CRUD actions.

#### Step 2.B (The Core Change):
* *Target File:* \`src/repositories/grind.ts\`
* *Verification:* Run \`npm run test:repo\`
* *Instructions:* Implement the SQL mappings for Grind vertical slices.`;

    window.onload = function() {
      // Load demo on start
      document.getElementById('importArea').value = demoPlan;
      parseMarkdownPlan(demoPlan);
      
      // Setup drag events
      window.allowDrop = function(ev) {
        ev.preventDefault();
      };

      window.drag = function(ev, id) {
        draggedCardId = id;
        ev.dataTransfer.setData("text", id);
      };

      window.dragEnter = function(ev) {
        ev.currentTarget.classList.add('drag-over');
      };

      window.dragLeave = function(ev) {
        ev.currentTarget.classList.remove('drag-over');
      };

      window.drop = function(ev, targetColumnId) {
        ev.preventDefault();
        ev.currentTarget.classList.remove('drag-over');
        const id = ev.dataTransfer.getData("text") || draggedCardId;
        moveTask(id, targetColumnId);
      };

      window.openModal = function(modalId) {
        document.getElementById(modalId).style.display = 'flex';
      };

      window.closeModal = function(modalId) {
        document.getElementById(modalId).style.display = 'none';
      };

      // Try loading local plan if hosted
      loadLocalPlan();
    };

    // Load Plan from standard location relative to the html file
    function loadLocalPlan() {
      fetch('05_PLAN.md')
        .then(response => {
          if (!response.ok) throw new Error('Not found');
          return response.text();
        })
        .then(text => {
          document.getElementById('importArea').value = text;
          parseMarkdownPlan(text);
          document.getElementById('featurePath').innerText = 'plans/.../05_PLAN.md (Loaded From Disk)';
        })
        .catch(err => {
          console.log("Local 05_PLAN.md not found directly; using interactive demo.");
        });
    }

    // Processing the Import
    window.processImport = function() {
      const text = document.getElementById('importArea').value;
      if (!text.trim()) return;
      parseMarkdownPlan(text);
      closeModal('importModal');
    };

    // Parser for 05_PLAN.md
    function parseMarkdownPlan(markdown) {
      originalMarkdown = markdown;
      tasks = [];
      
      const lines = markdown.split('\n');
      
      let currentPhase = 'Feature Scope';
      let parsingChecklist = false;
      let title = 'Feature Slices Implementation';

      // Capturing Title
      const titleMatch = markdown.match(/^#\s+(.*)$/m);
      if (titleMatch) title = titleMatch[1];
      document.getElementById('featureTitle').innerText = title;

      // Temporary map for step instructions
      const stepDetails = {};
      let currentDetailStep = null;
      let currentDetailLines = [];

      // Parse step descriptions
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        
        // Phase headers in descriptions
        if (line.startsWith('### Phase')) {
          continue;
        }

        // Specific Step detail headers
        const stepHeaderMatch = line.match(/^####\s+(Step\s+[\w\.]+)\s*(.*)$/i);
        if (stepHeaderMatch) {
          if (currentDetailStep) {
            stepDetails[currentDetailStep] = parseDetailBlock(currentDetailLines);
          }
          currentDetailStep = stepHeaderMatch[1].trim().toUpperCase();
          currentDetailLines = [];
          continue;
        }

        if (currentDetailStep) {
          // If we reach another main heading or checklist section, finalize current detail
          if (line.startsWith('## ') || line.startsWith('# ')) {
            stepDetails[currentDetailStep] = parseDetailBlock(currentDetailLines);
            currentDetailStep = null;
          } else {
            currentDetailLines.push(line);
          }
        }
      }
      if (currentDetailStep) {
        stepDetails[currentDetailStep] = parseDetailBlock(currentDetailLines);
      }

      // First pass: extract checklist tasks
      let taskIdCounter = 0;
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];

        // Track active phase
        if (line.includes('Phase') && !line.includes('[ ]') && !line.includes('[x]')) {
          const cleanLine = line.replace(/[#\*_\-]/g, '').trim();
          if (cleanLine.toLowerCase().startsWith('phase')) {
            currentPhase = cleanLine;
          }
        }

        // Match checklist lines: e.g. - [ ] Step 1.A: Setup Knex connection
        const checklistMatch = line.match(/^\s*[\-\*]\s+\[([ xX])\]\s+((Step\s+([\w\.]+))[:\-]\s*(.*))$/i);
        if (checklistMatch) {
          const isDone = checklistMatch[1].toLowerCase() === 'x';
          const stepLabel = checklistMatch[3].trim().toUpperCase(); // e.g. STEP 1.A
          const name = checklistMatch[2].trim();
          
          taskIdCounter++;
          const taskId = `task-${taskIdCounter}`;

          // Pull matching details if we parsed them
          const details = stepDetails[stepLabel] || {
            targetFile: 'Not specified',
            verification: 'Not specified',
            instructions: name
          };

          tasks.push({
            id: taskId,
            label: stepLabel,
            name: name,
            phase: currentPhase,
            isDone: isDone,
            status: isDone ? 'done' : 'todo', // Default todo, we'll auto-resolve "inprogress" below
            targetFile: details.targetFile,
            verification: details.verification,
            instructions: details.instructions
          });
        }
      }

      // Mark the first unchecked item as "inprogress" automatically
      let foundActive = false;
      for (let t of tasks) {
        if (!t.isDone && !foundActive) {
          t.status = 'inprogress';
          foundActive = true;
        }
      }

      renderBoard();
      renderMermaid();
    }

    // Helper to parse detail blocks under step subheadings
    function parseDetailBlock(linesArr) {
      let targetFile = 'Not specified';
      let verification = 'Not specified';
      let instructions = '';

      for (let line of linesArr) {
        const clean = line.trim();
        if (clean.toLowerCase().includes('*target file:*') || clean.toLowerCase().includes('**target file:**')) {
          targetFile = clean.replace(/^[*\s\-]+target file:\s*/i, '').replace(/`/g, '').trim();
        } else if (clean.toLowerCase().includes('*verification:*') || clean.toLowerCase().includes('**verification:**')) {
          verification = clean.replace(/^[*\s\-]+verification:\s*/i, '').replace(/`/g, '').trim();
        } else if (clean.startsWith('* ') || clean.startsWith('- ')) {
          instructions += clean.replace(/^[*\-\s]+/i, '') + '\n';
        } else if (clean.length > 0) {
          instructions += clean + '\n';
        }
      }

      return {
        targetFile: targetFile || 'Not specified',
        verification: verification || 'Not specified',
        instructions: instructions.trim() || 'No custom instructions provided.'
      };
    }

    // Rendering the columns and statistic panels
    function renderBoard() {
      const todoList = document.getElementById('todoList');
      const progressList = document.getElementById('progressList');
      const doneList = document.getElementById('doneList');

      todoList.innerHTML = '';
      progressList.innerHTML = '';
      doneList.innerHTML = '';

      let todoCount = 0;
      let progCount = 0;
      let doneCount = 0;

      tasks.forEach(task => {
        const card = document.createElement('div');
        card.className = `card card-${task.status}`;
        card.draggable = true;
        card.id = task.id;
        card.setAttribute('ondragstart', `drag(event, '${task.id}')`);
        card.setAttribute('onclick', `inspectTask('${task.id}')`);

        const isDonePhase = task.status === 'done';
        
        card.innerHTML = `
          <div class="card-header">
            <span class="card-phase ${isDonePhase ? 'card-phase-done' : ''}">${task.phase.split(':')[0]}</span>
            <span class="badge-status badge-status-${task.status}">${task.status === 'inprogress' ? 'Active' : task.status}</span>
          </div>
          <div class="card-title">${task.name}</div>
          <div class="card-meta">
            <span class="card-meta-icon">📁</span>
            <span>${task.targetFile.split('/').pop()}</span>
          </div>
        `;

        if (task.status === 'todo') {
          todoList.appendChild(card);
          todoCount++;
        } else if (task.status === 'inprogress') {
          progressList.appendChild(card);
          progCount++;
        } else if (task.status === 'done') {
          doneList.appendChild(card);
          doneCount++;
        }
      });

      // Update headers
      document.getElementById('todoHeaderCount').innerText = todoCount;
      document.getElementById('progressHeaderCount').innerText = progCount;
      document.getElementById('doneHeaderCount').innerText = doneCount;

      // Update counters
      document.getElementById('todoCount').innerText = todoCount;
      document.getElementById('progCount').innerText = progCount;
      document.getElementById('doneCount').innerText = doneCount;

      // Calculate progress percentage
      const total = tasks.length;
      const pct = total > 0 ? Math.round((doneCount / total) * 100) : 0;
      document.getElementById('progressPercent').innerText = `${pct}%`;
      document.getElementById('progressBar').style.width = `${pct}%`;
    }

    // Dynamic Inspector mapping
    window.inspectTask = function(id) {
      const task = tasks.find(t => t.id === id);
      if (!task) return;

      const detailsPanel = document.getElementById('detailsPanel');
      
      let statusLabel = 'TO DO';
      if (task.status === 'inprogress') statusLabel = 'ACTIVE EXTRACTION';
      if (task.status === 'done') statusLabel = 'VERIFIED DONE';

      detailsPanel.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
          <h4 style="font-size: 1rem; font-weight: 600; color: var(--accent-blue);">${task.label} Details</h4>
          <span class="badge-status badge-status-${task.status}">${statusLabel}</span>
        </div>

        <div class="details-group">
          <div class="details-label">Slice Name</div>
          <div class="details-value" style="font-weight: 500; font-size: 0.95rem;">${task.name}</div>
        </div>

        <div class="details-group">
          <div class="details-label">Target File Path</div>
          <div class="details-code">${task.targetFile}</div>
        </div>

        <div class="details-group">
          <div class="details-label">Local Verification Command</div>
          <div class="details-code">${task.verification}</div>
        </div>

        <div class="details-group">
          <div class="details-label">Swarm Action Instructions</div>
          <div class="details-value" style="white-space: pre-wrap; font-family: inherit; font-size: 0.85rem; line-height: 1.6; color: var(--text-sub); background: rgba(17,17,27,0.3); padding: 0.75rem; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05);">${task.instructions}</div>
        </div>
      `;
    };

    // Move task status via drag and drop
    function moveTask(id, targetStatus) {
      const task = tasks.find(t => t.id === id);
      if (!task) return;

      task.status = targetStatus;
      task.isDone = targetStatus === 'done';

      renderBoard();
      renderMermaid();
    }

    // Dynamic Mermaid Render
    function renderMermaid() {
      const container = document.getElementById('mermaidContainer');
      container.innerHTML = '<div class="mermaid" id="mermaidOutput"></div>';
      
      let code = 'flowchart TD\n';
      
      // Mermaid configurations
      code += '  classDef todo fill:#313244,stroke:#45475a,stroke-width:2px,color:#cdd6f4;\n';
      code += '  classDef active fill:#89b4fa,stroke:#1e66f5,stroke-width:2px,color:#11111b;\n';
      code += '  classDef done fill:#a6e3a1,stroke:#40a02b,stroke-width:2px,color:#11111b;\n\n';

      // Group steps by Phase in Mermaid
      const phases = {};
      tasks.forEach(task => {
        if (!phases[task.phase]) phases[task.phase] = [];
        phases[task.phase].push(task);
      });

      let phaseIndex = 0;
      let lastNodeId = null;

      Object.keys(phases).forEach(phaseName => {
        phaseIndex++;
        const pId = `phase_${phaseIndex}`;
        
        const phaseTasks = phases[phaseName];
        
        // Add Subgraph for Phase
        code += `  subgraph ${pId} ["${phaseName}"]\n`;
        phaseTasks.forEach(task => {
          const nId = task.label.replace(/\./g, '_'); // e.g. STEP_1_A
          code += `    ${nId}["${task.label}: ${task.targetFile.split('/').pop()}"]\n`;
          code += `    style ${nId} fill:${task.status === 'done' ? '#a6e3a1' : (task.status === 'inprogress' ? '#89b4fa' : '#313244')},stroke:${task.status === 'done' ? '#40a02b' : (task.status === 'inprogress' ? '#1e66f5' : '#45475a')},color:${task.status === 'todo' ? '#cdd6f4' : '#11111b'}\n`;
        });
        code += '  end\n\n';

        // Connect tasks sequentially
        for (let j = 0; j < phaseTasks.length - 1; j++) {
          const fromId = phaseTasks[j].label.replace(/\./g, '_');
          const toId = phaseTasks[j+1].label.replace(/\./g, '_');
          code += `  ${fromId} --> ${toId}\n`;
        }

        // Connect between phases
        if (lastNodeId && phaseTasks.length > 0) {
          const currentFirstNodeId = phaseTasks[0].label.replace(/\./g, '_');
          code += `  ${lastNodeId} -.-> ${currentFirstNodeId}\n`;
        }

        if (phaseTasks.length > 0) {
          lastNodeId = phaseTasks[phaseTasks.length - 1].label.replace(/\./g, '_');
        }
      });

      if (tasks.length === 0) {
        code = 'flowchart TD\n  Empty([Import a valid 05_PLAN.md to generate dependency tree])\n';
      }

      const outputDiv = document.getElementById('mermaidOutput');
      outputDiv.textContent = code;

      if (window.mermaid) {
        try {
          window.mermaid.render('mermaid-svg', code).then(({ svg }) => {
            outputDiv.innerHTML = svg;
          });
        } catch (e) {
          console.error("Mermaid parsing issue: ", e);
        }
      }
    }

    // Export Updated Plan Markdown back to 05_PLAN.md
    window.exportMarkdown = function() {
      if (!originalMarkdown) return;
      
      const lines = originalMarkdown.split('\n');
      const updatedLines = [...lines];

      // Update the checklist brackets [ ] or [x] in the original markdown array
      tasks.forEach(task => {
        // Build regex pattern that matches exactly this checklist step
        const escapedLabel = task.label.replace(/\./g, '\\.');
        const regex = new RegExp(`^(\\s*[\\-\\*]\\s+\\[)([ xX])(\\]\\s+${escapedLabel}[:\\-])`, 'i');

        for (let i = 0; i < updatedLines.length; i++) {
          const match = updatedLines[i].match(regex);
          if (match) {
            const char = task.isDone ? 'x' : ' ';
            updatedLines[i] = updatedLines[i].replace(regex, `$1${char}$3`);
            break;
          }
        }
      });

      const outText = updatedLines.join('\n');
      document.getElementById('exportArea').value = outText;
      openModal('exportModal');
    };

    window.copyExportText = function() {
      const area = document.getElementById('exportArea');
      area.select();
      document.execCommand('copy');
      alert('Copied updated 05_PLAN.md Markdown to clipboard! Paste it directly back into your file.');
    };
  </script>
</body>
</html>
```

### Step 4: Present Result
1. Render a clean visual summary of the generated assets.
2. Provide direct clickable file:/// links to:
   - `plans/<feature-slug>/<timestamp>/05_KANBAN.md`
   - `plans/<feature-slug>/<timestamp>/kanban.html`
3. Instruct the user on how they can double-click `kanban.html` to open it locally and track the live state of implementation slices interactively.
