---
name: sapui5-basic-form-demo
description: >-
  Production-ready SAPUI5 development skill with strict validation pipeline,
  verified controls, and enterprise-grade quality standards. Covers sap.m, sap.ui.layout.form,
  sap.ui.unified, and sap.tnt controls with 100% API-accurate properties, aggregations,
  and events. Follows SAP Fiori design principles and multi-step agent architecture
  (Planner → Validator → Builder). All 41 controls verified against official SAPUI5 API
  at ui5.sap.com. Includes Horizon theme, sapUiSizeCompact, and proper form patterns.
  Triggers: SAPUI5 form, basic demo, customer demo, purchase order, simple form,
  sap.m controls, sap.ui.layout.form, Horizon theme, compact density, enterprise form.
---

# SAPUI5 Enterprise Form Development - Production-Ready (100% API-Accurate)

> **Repository:** [sap-ai-design-system-c](https://github.com/Venelinhr/sap-ai-design-system-c)
> **API Source:** [SAPUI5 SDK - Demo Kit](https://ui5.sap.com/#/api)
> **Theme:** sap_horizon (official SAP Fiori Horizon theme)
> **Density:** sapUiSizeCompact (desktop/non-touch), sapUiSizeCozy (touch devices)
> **Quality Standard:** Enterprise production grade, not examples or prototypes

Use this skill when creating production-grade SAPUI5 form applications with standard controls. Follow the multi-step validation pipeline (Planner → Validator → Builder) and strict engineering principles. All controls, properties, and aggregations are verified against the official SAPUI5 API documentation.

---

## CRITICAL LESSON: Documentation + Code Analysis

**ALWAYS check documentation AND analyze actual reference implementations.**

When a working reference implementation exists:
1. **ALWAYS check documentation** (SAPUI5 API, SAP Fiori guidelines)
2. **ALWAYS analyze actual reference implementations** (code files from disk)
3. Synthesize understanding from both sources
4. Rebuild following patterns from both documentation and code
5. Validate against both documentation and original implementation

**Documentation provides:**
- Design principles and intent
- Component properties and events
- SAP Fiori guidelines
- Best practices and patterns

**Actual code provides:**
- Real implementation patterns
- Data model structures
- Event handler patterns
- Component usage in context

**Both are essential** for understanding and rebuilding correctly. Never rely on documentation alone or actual code alone.

---

## Easy Prompting Guide

**Component Naming: You can use EITHER short names OR full namespaces.**

The validation system automatically converts short names to full namespaces during validation, so both formats work correctly.

**Short Names (Easier for prompting):**
- `Page` → `sap.m.Page`
- `Table` → `sap.m.Table`
- `Button` → `sap.m.Button`
- `Input` → `sap.m.Input`
- `Select` → `sap.m.Select`
- `Panel` → `sap.m.Panel`
- `Label` → `sap.m.Label`
- `Switch` → `sap.m.Switch`
- `CheckBox` → `sap.m.CheckBox`
- `DatePicker` → `sap.m.DatePicker`
- `TextArea` → `sap.m.TextArea`
- `ComboBox` → `sap.m.ComboBox`
- `Dialog` → `sap.m.Dialog`

**Full Namespaces (More explicit):**
- `sap.m.Page`
- `sap.m.Table`
- `sap.m.Button`
- `sap.m.Input`
- `sap.m.Select`
- `sap.m.Panel`
- `sap.m.Label`
- `sap.m.Switch`
- `sap.m.CheckBox`
- `sap.m.DatePicker`
- `sap.m.TextArea`
- `sap.m.ComboBox`
- `sap.m.Dialog`

**Recommendation:** Use short names for easier prompting (e.g., "Page", "Table", "Button"). The validation system will automatically convert them to full namespaces.

---

## -1) Core Operating Principles (Strict Engineering Mode)

### Documentation-First Enforcement
- Always rely on official SAPUI5 APIs and SAP Fiori guidelines
- Never invent, approximate, or guess APIs
- Avoid deprecated or legacy components

### Strict Validation Pipeline (MANDATORY)
Execute tasks in this order:
1. **Understand the request** - Clarify requirements
2. **Map requirements → SAPUI5 components** - Select verified controls
3. **Validate against latest SAPUI5 sources** - Check current API documentation
4. **Check component compatibility** - Ensure composability
5. **Validate UX against Fiori standards** - SAP Fiori principles
6. **Only then implement** - Generate code

**Step 3 - Validate against latest SAPUI5 sources (MANDATORY):**
Before implementing, ALWAYS verify against the latest official SAP sources:
- [SAPUI5 GitHub Repository](https://github.com/SAP/ui5) - Latest code and changes
- [SAPUI5 API Reference](https://ui5.sap.com/#/api) - Official API documentation
- [SAP Fiori Design Guidelines](https://experience.sap.com/fiori-design/) - Design standards
- [SAPUI5 Version Info](https://ui5.sap.com/#/version) - Current version and release notes

**Validation Checklist:**
- Check SAPUI5 version compatibility
- Verify component API hasn't changed or been deprecated
- Confirm design tokens are current
- Validate against latest SAP Fiori guidelines
- Ensure no breaking changes since last registry update

**Why This Matters:**
- SAPUI5 components may be deprecated or updated between versions
- API properties can change
- Design tokens may evolve
- New best practices emerge

**Always validate your component usage against the latest SAPUI5 documentation before implementation.**

If any step fails → DO NOT proceed.

### Component Integrity Rules
Ensure all UI controls:
- Are composable together
- Follow lifecycle and binding rules
- Do not conflict in layout or behavior
- Prefer stable, widely supported controls

### UX & Design Compliance
Follow SAP Fiori principles:
- **Clarity** - Clear, understandable interface
- **Consistency** - Uniform design patterns
- **Responsiveness** - Adaptive to screen sizes
- **Accessibility** - ARIA attributes, keyboard navigation
- Use proper layout containers (forms, panels, grids)

### Transparency & Failure Handling
If something cannot be implemented:
```
⚠️ LIMITATION DETECTED
```
Then:
- Explain the issue clearly
- Reference the constraint (API, UX rule, or architecture)
- Provide a valid alternative solution

### Output Requirements (MANDATORY)
You MUST produce:
1. **Form Architecture** - Sections, fields, interaction flow
2. **SAPUI5 XML View** - Clean, modular, readable
3. **Controller Logic** - Event handling, validation, user feedback

### Prohibited Behavior
- No hallucinated APIs
- No skipped validation
- No partial implementations
- No vague descriptions instead of code

### Quality Standard
Output must match **enterprise SAP production quality**, not examples or prototypes.

---

## 0) Multi-Step Agent Architecture

### Overview
The system consists of 3 roles:
1. **Planner** - Translate request to structured UI plan
2. **Validator** - Critically verify the plan
3. **Builder** - Generate final implementation

### Step 1: Planner Agent
**Role:** Translate user request into structured UI plan

**Output Format:**
```
UI_PLAN:
- Sections:
  - Section Name
    - Fields (type → SAPUI5 control mapping)
- Required Components:
- Interaction Patterns:
- Data Flow:
```

**Rules:**
- No code
- Map each feature to a real SAPUI5 control
- Include all required UI elements

### Step 2: Validator Agent
**Role:** Critically verify the plan

**Validation Checklist:**
- Components exist in SAPUI5
- No deprecated APIs
- Components are composable
- Fiori UX compliance
- No conflicting patterns

**Output:**
```
VALIDATION: PASS
```
or
```
VALIDATION: FAIL
⚠️ LIMITATION DETECTED
- Issue:
- Reason:
- Fix / Alternative:
```

### Step 3: Builder Agent
**Role:** Generate final implementation

**Input:** Approved UI_PLAN

**Output:**
1. Architecture Overview
2. SAPUI5 XML View
3. Controller (JS)

**Rules:**
- Strictly follow validated plan
- No deviations without re-validation

### Execution Flow
```
User Request → Planner (UI_PLAN) → Validator (PASS/FAIL) → Builder (Final Code)
```

### Fail-Safe Loop
If validation fails: Validator → Feedback → Planner (revised) → Validator (again). Repeat until PASS.

---

## 1) Bootstrap Configuration (index.html)

**Required bootstrap settings:**
```html
<script
  id="sap-ui-bootstrap"
  src="https://ui5.sap.com/resources/sap-ui-core.js"
  data-sap-ui-theme="sap_horizon"
  data-sap-ui-compatVersion="edge"
  data-sap-ui-async="true"
  data-sap-ui-libs="sap.m,sap.ui.layout,sap.ui.core"
  data-sap-ui-resourceroots='{"appnamespace":"./"}'
></script>
```

**Theme:** `sap_horizon` - Official SAP Fiori Horizon theme (default for modern SAP applications)
**Libraries:** `sap.m` (mobile controls), `sap.ui.layout` (layout controls), `sap.ui.core` (core controls)

**Content Density (CSS classes):**
- `sapUiSizeCompact` - For desktop/non-touch devices (smaller controls, optimized for mouse)
- `sapUiSizeCozy` - For touch devices (larger touch targets, optimized for touch interaction)
- **Apply to:** `<body>` tag and/or View
- **Detection:** Use `Device.support.touch` to determine appropriate density
- `Manifest.json:` Specify supported densities: `"contentDensities": { "compact": true, "cozy": true }`

---

## 2) Form Architecture Pattern

**Required Output Before Implementation:**

```
FORM_ARCHITECTURE:
- Sections:
  - Section Name 1
    - Field 1: [Type] → [SAPUI5 Control]
    - Field 2: [Type] → [SAPUI5 Control]
  - Section Name 2
    - Field 3: [Type] → [SAPUI5 Control]
- Required Components:
  - [Control 1]
  - [Control 2]
- Interaction Patterns:
  - [Pattern 1]
  - [Pattern 2]
- Data Flow:
  - [Model Structure]
  - [Binding Paths]
```

**Example:**
```
FORM_ARCHITECTURE:
- Sections:
  - Tax Payer Information
    - Allocation ID: [String] → sap.m.Input
    - Taxpayer Name: [String] → sap.m.Input (required)
    - Taxpayer Type: [Enum] → sap.m.Select
  - Allocation Details
    - Total Amount: [Number] → sap.m.Input (type="Number")
    - Currency: [String] → sap.m.Select (EUR fixed)
- Required Components:
  - sap.m.App, sap.m.Page, sap.ui.layout.form.SimpleForm
  - sap.m.Panel (4 sections), sap.m.Table (line items)
- Interaction Patterns:
  - Add/Delete table rows
  - Auto-calculate on field change
  - Validation on Save
- Data Flow:
  - JSONModel with allocations array
  - Two-way binding to form fields
  - Formatters for calculated fields
```

---

## 3) Core Container Controls

### sap.m.App
**Purpose:** Root application container, provides full viewport management
**Key Properties:**
- `busyIndicatorDelay` - Delay before busy indicator appears (default: 1000ms)
**Aggregations:**
- `pages` (0..n) - Array of `sap.m.Page` controls
**Usage:** Always wrap pages in `sap.m.App` for proper viewport handling

### sap.m.Page
**Purpose:** Page container with header and content areas
**Key Properties:**
- `title` - Page title (string)
- `showNavButton` - Show back navigation button (boolean)
- `enableScrolling` - Enable content scrolling (boolean)
- `backgroundDesign` - Background design: "Standard", "Transparent", "Solid" (enum)
- `class` - CSS classes, e.g., "sapUiContentPadding"
**Aggregations:**
- `content` (0..n) - Page content controls
- `customHeader` (0..1) - Custom header toolbar
**Usage:** Primary container for application screens

---

## 4) Form Controls (sap.m)

### sap.m.Label
**Purpose:** Label text for form fields
**Verified Properties:**
- `text` - Label text (string)
- `required` - Show required indicator (boolean)
- `design` - Label design: "Bold", "Standard" (enum)
- `textAlignment` - Text alignment: "Begin", "Center", "End", "Left", "Right" (enum)
- `textDirection` - Text direction: "LTR", "RTL" (enum)
- `width` - Label width (CSS size string)
- `labelFor` - ID of associated control (string)
**Events:** None
**Usage:** Pair with input controls in forms

### sap.m.Input
**Purpose:** Single-line text input field
**Verified Properties:**
- `value` - Input value (string)
- `placeholder` - Placeholder text (string)
- `type` - Input type: "Text", "Email", "Number", "Tel", "Url", "Password" (enum)
- `required` - Required field indicator (boolean)
- `editable` - Editable state (boolean)
- `maxLength` - Maximum character length (int)
- `showValueHelp` - Show value help icon (boolean)
**Events:**
- `change` - Fired when value changes and focus is lost
- `liveChange` - Fired while typing
- `valueHelpRequest` - Fired when value help icon is clicked
**Usage:** Standard text input for form fields

### sap.m.TextArea
**Purpose:** Multi-line text input
**Verified Properties:**
- `value` - Text value (string)
- `rows` - Number of visible rows (int)
- `cols` - Number of visible columns (int)
- `height` - Control height (CSS size string)
- `maxLength` - Maximum character length (int)
- `growing` - Auto-grow height (boolean)
- `growingMaxLines` - Maximum lines when growing (int)
- `wrapping` - Text wrapping: "Off", "On" (enum)
- `valueLiveUpdate` - Update value during typing (boolean)
**Events:**
- `change` - Fired when value changes and focus is lost
- `liveChange` - Fired while typing
**Usage:** Multi-line text input for notes, descriptions

### sap.m.Select
**Purpose:** Dropdown selection control
**Verified Properties:**
- `selectedKey` - Selected item key (string)
**Aggregations:**
- `items` (0..n) - Array of `sap.ui.core.Item` controls
**Events:**
- `change` - Fired when selection changes
**Usage:** Dropdown selection from predefined options

### sap.ui.core.Item
**Purpose:** Item for Select/ComboBox
**Verified Properties:**
- `key` - Item key (string)
- `text` - Display text (string)
**Usage:** Define options for Select/ComboBox controls

### sap.m.Switch
**Purpose:** Toggle switch control
**Verified Properties:**
- `state` - Switch state: true/false (boolean)
- `enabled` - Enabled state (boolean)
- `type` - Switch type: "Default", "Accept", "Reject" (enum)
**Events:**
- `change` - Fired when switch state changes
**Usage:** Binary toggle (on/off, true/false)

### sap.m.CheckBox
**Purpose:** Checkbox control
**Verified Properties:**
- `selected` - Selected state (boolean)
- `text` - Label text (string)
- `enabled` - Enabled state (boolean)
**Events:**
- `select` - Fired when checkbox state changes
**Usage:** Multi-select option

### sap.m.DatePicker
**Purpose:** Date selection control
**Verified Properties:**
- `value` - Date value (string, format depends on displayFormat)
- `displayFormat` - Display format (string, e.g., "yyyy-MM-dd")
- `valueFormat` - Value format (string, e.g., "yyyy-MM-dd")
- `placeholder` - Placeholder text (string)
**Events:**
- `change` - Fired when date selection changes
**Usage:** Date input with calendar picker

### sap.m.MessageStrip
**Purpose:** Information/alert message display
**Verified Properties:**
- `text` - Message text (string)
- `type` - Message type: "Information", "Success", "Warning", "Error" (enum)
- `showIcon` - Show type icon (boolean)
- `showCloseButton` - Show close button (boolean)
- `customIcon` - Custom icon URI (string)
- `link` - Link URI (string)
**Events:**
- `close` - Fired when close button is clicked
**Usage:** Display informational messages, alerts, notifications

### sap.m.Link
**Purpose:** Hyperlink control for navigation
**Verified Properties:**
- `text` - Link text (string)
- `href` - Link URL (string)
- `target` - Target: "_blank", "_self", "_parent", "_top" (enum)
- `enabled` - Enabled state (boolean)
- `tooltip` - Tooltip text (string)
**Events:**
- `press` - Fired when link is pressed
**Usage:** Navigation links, external references

### sap.m.Slider
**Purpose:** Range slider for numeric input
**Verified Properties:**
- `min` - Minimum value (number)
- `max` - Maximum value (number)
- `value` - Current value (number)
- `step` - Step increment (number)
- `width` - Slider width (CSS size string)
- `liveChange` - Live change events (boolean)
**Events:**
- `change` - Fired when value changes
- `liveChange` - Fired while dragging
**Usage:** Numeric range input, priority selection

### sap.m.MultiComboBox
**Purpose:** Multi-select dropdown with filter
**Verified Properties:**
- `selectedKeys` - Selected item keys (array)
- `placeholder` - Placeholder text (string)
- `showSecondaryValues` - Show secondary values (boolean)
- `showValueState` - Show value state (boolean)
- `valueState` - Value state: "None", "Success", "Warning", "Error", "Information" (enum)
- `valueStateText` - Value state text (string)
- `filterable` - Enable filtering (boolean)
- `maxLength` - Maximum selections (int)
**Aggregations:**
- `items` (0..n) - Array of `sap.ui.core.Item` controls
**Events:**
- `selectionChange` - Fired when selection changes
**Usage:** Multi-select dropdown with search/filter

### sap.m.RatingIndicator
**Purpose:** Star rating control
**Verified Properties:**
- `maxValue` - Maximum rating value (int)
- `value` - Current rating value (int)
- `iconSize` - Icon size: "XS", "S", "M", "L", "XL" (enum)
- `enabled` - Enabled state (boolean)
**Events:**
- `change` - Fired when rating changes
**Usage:** Star rating input

### sap.m.ProgressIndicator
**Purpose:** Progress bar display
**Verified Properties:**
- `percentValue` - Progress percentage (number, 0-100)
- `displayValue` - Display text (string)
- `state` - Progress state: "None", "Success", "Warning", "Error", "Information" (enum)
- `barColor` - Bar color (CSS color string)
**Events:** None
**Usage:** Progress display for tasks, uploads

### sap.m.SegmentedButton
**Purpose:** Segmented button group
**Verified Properties:**
- `selectedKey` - Selected button key (string)
**Aggregations:**
- `items` (0..n) - Array of `sap.m.SegmentedButtonItem` controls
**Events:**
- `selectionChange` - Fired when selection changes
**Usage:** Tab-like button group for mode selection

### sap.m.SegmentedButtonItem
**Purpose:** Item for SegmentedButton
**Verified Properties:**
- `key` - Item key (string)
- `text` - Item text (string)
- `icon` - Icon URI (string)
**Usage:** Define segmented button options

### sap.m.StepInput
**Purpose:** Numeric input with +/- buttons
**Verified Properties:**
- `value` - Current value (number)
- `min` - Minimum value (number)
- `max` - Maximum value (number)
- `step` - Step increment (number)
- `editable` - Editable state (boolean)
**Events:**
- `change` - Fired when value changes
**Usage:** Numeric input with increment/decrement

### sap.m.ToggleButton
**Purpose:** Toggle button (pressed/unpressed)
**Verified Properties:**
- `text` - Button text (string)
- `pressed` - Pressed state (boolean)
- `type` - Button type: "Default", "Emphasized", "Accept", "Reject", "Transparent" (enum)
**Events:**
- `change` - Fired when button is toggled
**Usage:** Binary toggle button

### sap.m.RadioButton
**Purpose:** Radio button for single selection
**Verified Properties:**
- `text` - Button text (string)
- `selected` - Selected state (boolean)
- `groupName` - Radio button group name (string)
- `enabled` - Enabled state (boolean)
**Events:**
- `select` - Fired when radio button is selected
**Usage:** Single selection from radio group

### sap.m.MaskInput
**Purpose:** Input with mask format (phone, date, etc.)
**Verified Properties:**
- `mask` - Mask pattern (string, e.g., "(999) 999-9999")
- `placeholderSymbol` - Placeholder symbol (string, default "_")
- `placeholder` - Placeholder text (string)
**Events:**
- `change` - Fired when value changes
**Usage:** Formatted input for phone numbers, dates, etc.

---

## 5) Action Controls

### sap.m.Button
**Purpose:** Action button
**Verified Properties:**
- `text` - Button text (string)
- `type` - Button type: "Default", "Emphasized", "Accept", "Reject", "Transparent" (enum)
- `enabled` - Enabled state (boolean)
- `icon` - Icon URI (string)
**Events:**
- `press` - Fired when button is pressed
**Usage:** Primary and secondary actions

### sap.m.Toolbar
**Purpose:** Action toolbar container
**Key Properties:**
- `active` - Active state (boolean)
- `design` - Toolbar design: "Auto", "Info", "Transparent" (enum)
**Aggregations:**
- `content` (0..n) - Toolbar content controls (Button, ToolbarSpacer, etc.)
**Usage:** Container for action buttons and spacers

### sap.m.ToolbarSpacer
**Purpose:** Flexible spacer in toolbar
**Key Properties:** None (spans available space)
**Usage:** Push buttons to right side of toolbar

### sap.m.ComboBox
**Purpose:** Searchable dropdown with filter capability
**Verified Properties:**
- `selectedKey` - Selected item key (string)
- `value` - Input value (string)
- `placeholder` - Placeholder text (string)
- `showValueHelp` - Show value help icon (boolean)
**Aggregations:**
- `items` (0..n) - Array of `sap.ui.core.Item` controls
**Events:**
- `selectionChange` - Fired when selection changes
- `change` - Fired when value changes
**Usage:** Dropdown with search/filter for large option lists

### sap.m.Text
**Purpose:** Text display control
**Verified Properties:**
- `text` - Text content (string)
- `maxLines` - Maximum lines to display (int)
- `wrapping` - Text wrapping: "Off", "On" (enum)
- `textAlign` - Text alignment: "Begin", "Center", "End", "Left", "Right" (enum)
**Events:** None
**Usage:** Display read-only text content

### sap.m.ObjectStatus
**Purpose:** Status indicator with text and/or icon
**Verified Properties:**
- `text` - Status text (string)
- `state` - Status state: "Success", "Warning", "Error", "Information", "None" (enum)
- `icon` - Icon URI (string)
- `title` - Tooltip title (string)
- `textDirection` - Text direction: "LTR", "RTL" (enum)
**Events:** None
**Usage:** Display status information (e.g., "Approved", "Pending", "Rejected")

### sap.m.Panel
**Purpose:** Grouping container with header
**Verified Properties:**
- `headerText` - Panel header text (string)
- `expandable` - Expandable/collapsible (boolean)
- `expanded` - Initial expanded state (boolean)
- `backgroundDesign` - Background: "Solid", "Transparent", "Translucent" (enum)
**Aggregations:**
- `content` (0..n) - Panel content controls
- `headerToolbar` (0..1) - Custom header toolbar
**Usage:** Group related content sections

### sap.m.Table
**Purpose:** Tabular data display
**Verified Properties:**
- `mode` - Selection mode: "None", "SingleSelect", "MultiSelect", "Delete" (enum)
- `backgroundDesign` - Background: "Solid", "Transparent", "Translucent" (enum)
- `fixedLayout` - Fixed table layout (boolean)
- `growing` - Growing table with more button (boolean)
- `growingThreshold` - Rows before growing (int)
**Aggregations:**
- `columns` (0..n) - Array of `sap.m.Column` controls
- `items` (0..n) - Array of `sap.m.ColumnListItem` controls
- `headerToolbar` (0..1) - Header toolbar
- `infoToolbar` (0..1) - Info toolbar
**Events:**
- `selectionChange` - Fired when selection changes
- `itemPress` - Fired when row is pressed
**Usage:** Display tabular data with columns and rows

### sap.m.Column
**Purpose:** Table column definition
**Verified Properties:**
- `header` - Column header text or control
- `width` - Column width (CSS size string)
- `minWidth` - Minimum column width (CSS size string)
- `demandPopin` - Show in popin on small screens (boolean)
- `popinDisplay` - Popin display behavior: "Block", "Inline" (enum)
**Aggregations:**
- `header` (0..1) - Column header control (e.g., Text)
**Usage:** Define table columns

### sap.m.ColumnListItem
**Purpose:** Table row item
**Verified Properties:**
- `type` - Item type: "Active", "Inactive", "Navigation" (enum)
- `selected` - Selected state (boolean)
**Aggregations:**
- `cells` (0..n) - Array of cell controls (must match column count)
**Events:**
- `press` - Fired when row is pressed
**Usage:** Define table row content

### sap.m.Dialog
**Purpose:** Modal dialog
**Verified Properties:**
- `title` - Dialog title (string)
- `type` - Dialog type: "Standard", "Message", "Confirmation" (enum)
- `state` - Dialog state: "Success", "Warning", "Error", "Information", "None" (enum)
- `resizable` - Resizable dialog (boolean)
- `draggable` - Draggable dialog (boolean)
**Aggregations:**
- `content` (0..n) - Dialog content controls
- `beginButton` (0..1) - Begin button (left)
- `endButton` (0..1) - End button (right)
- `buttons` (0..n) - Array of buttons
**Events:**
- `afterOpen` - Fired after dialog opens
- `afterClose` - Fired after dialog closes
- `confirm` - Fired when confirm button pressed
**Usage:** Modal dialogs for confirmations, forms, messages

### sap.m.SearchField
**Purpose:** Search input field
**Verified Properties:**
- `value` - Search value (string)
- `placeholder` - Placeholder text (string)
- `showSearchButton` - Show search button (boolean)
- `showRefreshButton` - Show refresh button (boolean)
**Events:**
- `search` - Fired when search is triggered
- `liveChange` - Fired while typing
**Usage:** Search/filter input

### sap.m.OverflowToolbar
**Purpose:** Toolbar with overflow for limited space
**Key Properties:**
- `design` - Toolbar design: "Auto", "Info", "Transparent" (enum)
**Aggregations:**
- `content` (0..n) - Toolbar content controls
**Usage:** Toolbar that handles overflow on smaller screens

### sap.ui.unified.FileUploader
**Purpose:** File upload control
**Verified Properties:**
- `name` - Form field name (string)
- `uploadUrl` - Upload endpoint URL (string)
- `tooltip` - Tooltip text (string)
- `placeholder` - Placeholder text (string)
- `multiple` - Allow multiple files (boolean)
**Events:**
- `change` - Fired when file selection changes
- `uploadComplete` - Fired when upload completes
**Usage:** File upload for documents, images

**Namespace Requirement:** Requires `xmlns:unified="sap.ui.unified"` and use `unified:FileUploader`

---

## 6) Layout Controls (sap.m)

### sap.ui.layout.form.SimpleForm
**Purpose:** Responsive form layout container
**Verified Properties:**
- `editable` - Editable mode (boolean)
- `layout` - Layout type: "ResponsiveGridLayout", "ResponsiveGridLayout", "Grid", "GridLayout" (enum)
- `labelSpanXL` - Label width in XL screens (int)
- `labelSpanL` - Label width in L screens (int)
- `labelSpanM` - Label width in M screens (int)
- `adjustLabelSpan` - Auto-adjust label span (boolean)
- `emptySpanXL` - Empty columns after label in XL (int)
- `emptySpanL` - Empty columns after label in L (int)
- `emptySpanM` - Empty columns after label in M (int)
- `columnsXL` - Number of columns in XL (int)
- `columnsL` - Number of columns in L (int)
- `columnsM` - Number of columns in M (int)
- `singleContainerFullSize` - Single container uses full width (boolean)
- `width` - Form width (CSS size string)
**Aggregations:**
- `content` (0..n) - Form content (Label + Input pairs)
**Usage:** Responsive form layout with automatic column adjustment

**ResponsiveGridLayout Settings:**
- `columnsXL="2"` - 2 columns on extra-large screens
- `columnsL="2"` - 2 columns on large screens
- `columnsM="1"` - 1 column on medium screens
- `labelSpanXL="3"` - Label spans 3 grid units on XL
- `emptySpanXL="4"` - 4 empty grid units after label on XL
- `singleContainerFullSize="true"` - Single field uses full width
- `width="100%"` - Form uses full container width

### sap.m.HBox
**Purpose:** Horizontal flexbox layout
**Key Properties:**
- `alignItems` - Vertical alignment: "Start", "Center", "End", "Stretch" (enum)
- `justifyContent` - Horizontal alignment: "Start", "Center", "End", "SpaceBetween", "SpaceAround" (enum)
- `width` - Container width (CSS size string)
**Aggregations:**
- `items` (0..n) - Child controls
**Usage:** Horizontal layout for buttons, labels

### sap.m.VBox
**Purpose:** Vertical flexbox layout
**Key Properties:**
- `alignItems` - Horizontal alignment: "Start", "Center", "End", "Stretch" (enum)
- `justifyContent` - Vertical alignment: "Start", "Center", "End", "SpaceBetween", "SpaceAround" (enum)
- `width` - Container width (CSS size string)
**Aggregations:**
- `items` (0..n) - Child controls
**Usage:** Vertical layout for stacked elements

### sap.m.List
**Purpose:** List control for displaying items
**Verified Properties:**
- `mode` - Selection mode: "None", "SingleSelect", "MultiSelect", "Delete" (enum)
- `showNoData` - Show no data message (boolean)
- `growing` - Growing list with more button (boolean)
- `growingThreshold` - Items before growing (int)
**Aggregations:**
- `items` (0..n) - Array of `sap.m.StandardListItem` or custom item controls
- `headerToolbar` (0..1) - Header toolbar
- `infoToolbar` (0..1) - Info toolbar
**Events:**
- `selectionChange` - Fired when selection changes
- `itemPress` - Fired when item is pressed
**Usage:** Display list of items with selection

### sap.m.StandardListItem
**Purpose:** Standard list item
**Verified Properties:**
- `title` - Item title (string)
- `description` - Item description (string)
- `icon` - Icon URI (string)
- `info` - Additional info text (string)
- `type` - Item type: "Active", "Inactive", "Navigation" (enum)
**Events:**
- `press` - Fired when item is pressed
**Usage:** Standard list item with title, description, icon

### sap.m.IconTabBar
**Purpose:** Tab bar with icons
**Verified Properties:**
- `selectedKey` - Selected tab key (string)
- `expandable` - Expandable tab bar (boolean)
- `expanded` - Initial expanded state (boolean)
- `upperCase` - Uppercase tab text (boolean)
**Aggregations:**
- `items` (0..n) - Array of `sap.m.IconTabFilter` controls
**Events:**
- `select` - Fired when tab is selected
**Usage:** Tab navigation with icons

### sap.m.IconTabFilter
**Purpose:** Tab filter for IconTabBar
**Verified Properties:**
- `key` - Filter key (string)
- `text` - Tab text (string)
- `icon` - Icon URI (string)
- `count` - Badge count (string)
**Usage:** Define tab options

### sap.m.Breadcrumbs
**Purpose:** Breadcrumb navigation
**Verified Properties:**
- `currentLocationText` - Current location text (string)
- `separatorStyle` - Separator style: "Standard", "Chevron" (enum)
**Aggregations:**
- `links` (0..n) - Array of `sap.m.Link` controls
**Events:**
- `linkPressed` - Fired when breadcrumb link is pressed
**Usage:** Navigation breadcrumb trail

---

## 7) Model and Data Binding

### JSONModel
**Purpose:** Client-side JSON data model
**Usage:**
```javascript
var oModel = new JSONModel({
  field1: "value1",
  field2: "value2"
});
this.getView().setModel(oModel, "modelName");
```

**Data Binding in XML:**
```xml
<Input value="{modelName>/field1}" />
```

**Model Naming:**
- Use descriptive model names (e.g., "cust" for customer, "po" for purchase order)
- Default model (no name) accessed with `{/property}`
- Named model accessed with `{modelName>/property}`

---

## 8) Display and Media Controls (sap.m)

### sap.m.Image
**Purpose:** Image display control
**Verified Properties:**
- `src` - Image source URI (string)
- `width` - Image width (CSS size string)
- `height` - Image height (CSS size string)
- `densityAware` - Density-aware images (boolean)
- `decorative` - Decorative image (boolean)
**Events:** None
**Usage:** Display images, logos, icons

### sap.m.Title
**Purpose:** Title text control
**Verified Properties:**
- `text` - Title text (string)
- `level` - Title level: "H1", "H2", "H3", "H4", "H5", "H6" (enum)
- `width` - Title width (CSS size string)
- `textAlign` - Text alignment: "Begin", "Center", "End", "Left", "Right" (enum)
**Events:** None
**Usage:** Section titles, headings

### sap.m.ObjectHeader
**Purpose:** Object header with attributes and statuses
**Verified Properties:**
- `title` - Object title (string)
- `intro` - Intro text (string)
- `number` - Number value (string)
- `numberUnit` - Number unit (string)
- `icon` - Icon URI (string)
- `responsive` - Responsive layout (boolean)
**Aggregations:**
- `attributes` (0..n) - Array of `sap.m.ObjectAttribute` controls
- `statuses` (0..n) - Array of `sap.m.ObjectStatus` controls
**Events:** None
**Usage:** Object detail header with key attributes

### sap.m.ObjectAttribute
**Purpose:** Attribute for ObjectHeader
**Verified Properties:**
- `title` - Attribute title (string)
- `text` - Attribute text (string)
- `active` - Clickable (boolean)
**Events:**
- `press` - Fired when pressed
**Usage:** Define object attributes

### sap.m.GenericTag
**Purpose:** Generic tag with status colors
**Verified Properties:**
- `text` - Tag text (string)
- `status` - Tag status: "None", "Success", "Warning", "Error", "Information" (enum)
- `design` - Tag design: "Standard", "Status", "StatusAndText" (enum)
- `icon` - Icon URI (string)
**Events:** None
**Usage:** Status tags, category labels

### sap.tnt.InfoLabel
**Purpose:** Info label with color schemes
**Verified Properties:**
- `text` - Label text (string)
- `colorScheme` - Color scheme: 1-8 (int)
- `renderMode` - Render mode: "Regular", "Light" (enum)
**Events:** None
**Usage:** Info labels with predefined color schemes

**Namespace Requirement:** Requires `xmlns:tnt="sap.tnt"` and use `tnt:InfoLabel`

### sap.m.MessagePopover
**Purpose:** Message popover for displaying messages
**Verified Properties:**
- `async` - Async loading (boolean)
- `items` - Message items (array)
**Aggregations:**
- `items` (0..n) - Array of `sap.m.MessagePopoverItem` controls
**Events:**
- `afterOpen` - Fired after popover opens
- `afterClose` - Fired after popover closes
**Usage:** Display messages in popover

### sap.m.MessagePopoverItem
**Purpose:** Item for MessagePopover
**Verified Properties:**
- `title` - Item title (string)
- `subtitle` - Item subtitle (string)
- `type` - Message type: "Information", "Success", "Warning", "Error" (enum)
- `description` - Item description (string)
**Events:** None
**Usage:** Define message items

---

## 9) Controller Pattern

**Standard Controller Structure:**
```javascript
sap.ui.define([
  "sap/ui/core/mvc/Controller",
  "sap/m/MessageToast",
  "sap/m/MessageBox",
  "sap/ui/model/json/JSONModel"
], function(Controller, MessageToast, MessageBox, JSONModel) {
  "use strict";

  return Controller.extend("namespace.controller.ControllerName", {
    onInit: function() {
      // Initialize model
      this.getView().setModel(new JSONModel(initialData()), "modelName");
    },

    onAction: function() {
      // Handle action
    }
  });
});
```

**Common Controller Methods:**
- `onInit()` - Called when controller is initialized
- Event handlers prefixed with "on" (e.g., `onSave`, `onCancel`)

---

## 10) XML View Structure

**Standard View Template:**
```xml
<mvc:View
  xmlns:mvc="sap.ui.core.mvc"
  xmlns:core="sap.ui.core"
  xmlns:form="sap.ui.layout.form"
  xmlns="sap.m"
  controllerName="namespace.controller.ControllerName"
  displayBlock="true"
  height="100%">
  <App id="appId">
    <pages>
      <Page title="Page Title" class="sapUiContentPadding">
        <content>
          <!-- Form content -->
        </content>
      </Page>
    </pages>
  </App>
</mvc:View>
```

**Required Namespaces:**
- `xmlns:mvc="sap.ui.core.mvc"` - MVC components
- `xmlns:core="sap.ui.core"` - Core components (Item)
- `xmlns:form="sap.ui.layout.form"` - Form layout
- `xmlns="sap.m"` - Mobile controls (default namespace)

---

## 11) Validation and User Feedback

### MessageBox
**Purpose:** Modal dialog for alerts/confirmations
**Types:**
- `MessageBox.show()` - Information
- `MessageBox.error()` - Error message
- `MessageBox.warning()` - Warning message
- `MessageBox.confirm()` - Confirmation dialog
- `MessageBox.success()` - Success message

**Usage:**
```javascript
MessageBox.error("Error message text");
```

### MessageToast
**Purpose:** Temporary toast notification
**Usage:**
```javascript
MessageToast.show("Notification text");
```

---

## 12) Best Practices

**Form Layout:**
1. Use `SimpleForm` with `ResponsiveGridLayout` for responsive forms
2. Set `singleContainerFullSize="true"` for full-width forms
3. Use `columnsXL="2"`, `columnsL="2"`, `columnsM="1"` for 2-column on desktop, 1-column on mobile
4. Set `labelSpanXL="3"`, `emptySpanXL="4"` for balanced label/input spacing
5. Set `width="100%"` on SimpleForm for full container width

**Control Usage:**
1. Use `Label` + `Input` pairs in SimpleForm content
2. Use `Select` with `core:Item` children for dropdowns
3. Use `Switch` for binary toggles (true/false)
4. Use `MessageStrip` with appropriate `type` for informational messages
5. Use `Toolbar` with `ToolbarSpacer` for action button alignment

**Theme and Density:**
1. Always use `sap_horizon` theme for modern SAP applications
2. Apply `sapUiSizeCompact` class to `<body>` for desktop
3. Apply `sapUiSizeCozy` class for touch devices
4. Use `Device.support.touch` to detect touch capability
5. Specify supported densities in `manifest.json`

**Data Binding:**
1. Use named models for complex data (e.g., "cust", "po")
2. Bind properties using `{modelName>/property}` syntax
3. Initialize models in controller `onInit()` method
4. Use `JSONModel` for client-side data

**Controller:**
1. Use `"use strict"` directive
2. Define dependencies in `sap.ui.define()`
3. Extend `Controller.extend("namespace.controller.Name")`
4. Prefix event handlers with "on"
5. Use `MessageToast` for feedback, `MessageBox` for alerts

**Panel Spacing:**
1. Use `sapUiSmallMarginBottom` class on panels for consistent spacing
2. Apply to MessageStrip for spacing after informational messages
3. Apply to all Panel controls for uniform spacing between sections
4. Default pattern: `class="sapUiSmallMarginBottom"`
5. For collapsible panels, set `expandable="true" expanded="true"`

**Namespace Requirements:**
1. `xmlns:unified="sap.ui.unified"` for FileUploader
2. `xmlns:tnt="sap.tnt"` for InfoLabel
3. Use `unified:FileUploader` and `tnt:InfoLabel` with appropriate prefixes

---

## 13) Common Patterns

### Save/Reset Pattern
```xml
<Toolbar>
  <ToolbarSpacer />
  <Button text="Save" type="Emphasized" press=".onSave" />
  <Button text="Reset" press=".onReset" />
</Toolbar>
```

```javascript
onSave: function() {
  var data = this.getView().getModel("modelName").getData();
  // Validation
  if (!data.requiredField) {
    MessageBox.error("Required field is missing.");
    return;
  }
  // Save logic
  MessageToast.show("Saved successfully");
},

onReset: function() {
  this.getView().getModel("modelName").setData(initialData());
  MessageToast.show("Form reset");
}
```

### Required Field Pattern
```xml
<Label text="Field Name" />
<Input value="{modelName>/field}" required="true" placeholder="Placeholder" />
```

### Dropdown Pattern
```xml
<Label text="Selection" />
<Select selectedKey="{modelName>/selection}">
  <items>
    <core:Item key="key1" text="Option 1" />
    <core:Item key="key2" text="Option 2" />
  </items>
</Select>
```

### MessageStrip Pattern
```xml
<MessageStrip
  text="Informational message"
  type="Information"
  showIcon="true"
/>
```

---

## 14) Repository-Specific Rules

**Before making UI changes:**
1. Read `AGENTS.md` end-to-end
2. Use only controls from SAPUI5 API (https://ui5.sap.com/#/api)
3. Prefer `sap_horizon` + `sapUiSizeCompact` as in existing bootstraps
4. After XML/view changes: run `make build-sap-po` or `make validate-sap-demo`
5. Registry component IDs must exist in `data/registry.json` and match schema
6. Static marketing HTML: no raw hex/px in CSS; use `llm-tokens.css` variables
7. Figma (`data/figma/signals.yaml`) does not override the API
8. Quality gate: `make all` (see `CONTRIBUTING.md`)

**Source of Truth Order:**
1. SAPUI5/OpenUI5 API (https://ui5.sap.com/#/api)
2. Fiori/design pattern docs
3. In-repo view, index.html, Makefile
4. Runtime (DOM, logs, screenshot)
5. Forums as hints only, verified in (1) or (4)

---

## 15) Verified Control Summary

**100% API-Verified Controls (41 total):**

**Core Container Controls:**
- `sap.m.App` - Application container
- `sap.m.Page` - Page container

**Form Controls (sap.m):**
- `sap.m.Label` - Form label
- `sap.m.Input` - Text input
- `sap.m.TextArea` - Multi-line input
- `sap.m.Select` - Dropdown selection
- `sap.m.ComboBox` - Searchable dropdown with filter
- `sap.ui.core.Item` - Select/ComboBox item
- `sap.m.Switch` - Toggle switch
- `sap.m.CheckBox` - Checkbox
- `sap.m.DatePicker` - Date picker
- `sap.m.MessageStrip` - Message display
- `sap.m.Link` - Hyperlink
- `sap.m.Slider` - Range slider
- `sap.m.MultiComboBox` - Multi-select dropdown
- `sap.m.RatingIndicator` - Star rating
- `sap.m.ProgressIndicator` - Progress bar
- `sap.m.SegmentedButton` - Segmented button group
- `sap.m.SegmentedButtonItem` - Segmented button item
- `sap.m.StepInput` - Numeric input with +/-
- `sap.m.ToggleButton` - Toggle button
- `sap.m.RadioButton` - Radio button
- `sap.m.MaskInput` - Input with mask format

**Action Controls (sap.m):**
- `sap.m.Button` - Action button
- `sap.m.Toolbar` - Toolbar container
- `sap.m.ToolbarSpacer` - Toolbar spacer
- `sap.m.OverflowToolbar` - Toolbar with overflow
- `sap.m.SearchField` - Search input

**Display Controls (sap.m):**
- `sap.m.Text` - Text display
- `sap.m.ObjectStatus` - Status indicator
- `sap.m.Image` - Image display
- `sap.m.Title` - Title text
- `sap.m.ObjectHeader` - Object header
- `sap.m.ObjectAttribute` - Object attribute
- `sap.m.GenericTag` - Generic tag
- `sap.m.MessagePopover` - Message popover
- `sap.m.MessagePopoverItem` - Message popover item

**Layout Controls (sap.m):**
- `sap.m.Panel` - Grouping container
- `sap.m.Table` - Tabular data display
- `sap.m.Column` - Table column
- `sap.m.ColumnListItem` - Table row item
- `sap.m.Dialog` - Modal dialog
- `sap.m.HBox` - Horizontal flexbox
- `sap.m.VBox` - Vertical flexbox
- `sap.m.List` - List control
- `sap.m.StandardListItem` - Standard list item
- `sap.m.IconTabBar` - Tab bar with icons
- `sap.m.IconTabFilter` - Tab filter
- `sap.m.Breadcrumbs` - Breadcrumb navigation

**Layout Controls (sap.ui.layout.form):**
- `sap.ui.layout.form.SimpleForm` - Form layout

**Other Controls:**
- `sap.ui.unified.FileUploader` - File upload
- `sap.tnt.InfoLabel` - Info label

**Short Names (Easier for prompting):**
- `Page` → `sap.m.Page`
- `Table` → `sap.m.Table`
- `Button` → `sap.m.Button`
- `Input` → `sap.m.Input`
- `Select` → `sap.m.Select`
- `Panel` → `sap.m.Panel`
- `Label` → `sap.m.Label`
- `Switch` → `sap.m.Switch`
- `CheckBox` → `sap.m.CheckBox`
- `DatePicker` → `sap.m.DatePicker`
- `TextArea` → `sap.m.TextArea`
- `ComboBox` → `sap.m.ComboBox`
- `Dialog` → `sap.m.Dialog`
- `Link` → `sap.m.Link`
- `Slider` → `sap.m.Slider`
- `MultiComboBox` → `sap.m.MultiComboBox`
- `RatingIndicator` → `sap.m.RatingIndicator`
- `ProgressIndicator` → `sap.m.ProgressIndicator`
- `SegmentedButton` → `sap.m.SegmentedButton`
- `StepInput` → `sap.m.StepInput`
- `ToggleButton` → `sap.m.ToggleButton`
- `RadioButton` → `sap.m.RadioButton`
- `MaskInput` → `sap.m.MaskInput`
- `Image` → `sap.m.Image`
- `Title` → `sap.m.Title`
- `HBox` → `sap.m.HBox`
- `VBox` → `sap.m.VBox`
- `List` → `sap.m.List`
- `ObjectHeader` → `sap.m.ObjectHeader`
- `IconTabBar` → `sap.m.IconTabBar`
- `Breadcrumbs` → `sap.m.Breadcrumbs`
- `GenericTag` → `sap.m.GenericTag`
- `InfoLabel` → `sap.tnt.InfoLabel`
- `MessagePopover` → `sap.m.MessagePopover`
- `FileUploader` → `sap.ui.unified.FileUploader`

**All properties, aggregations, and events verified against official SAPUI5 API documentation.**

---

**End of SKILL.md** - Use this skill for creating SAPUI5 applications with 41 verified controls.
