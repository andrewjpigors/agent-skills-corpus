---
name: spec-to-tickets
description: >-
  Create implementation tickets with dependency graphs and Independent/Collaborative classification. Use when a user wants to break down a spec or tasks into tickets, or wants to create implementation tickets. Don't use when - spec is incomplete or vague (use grilling first, or domain-grilling if the resolution needs DDD alignment), a different granularity is needed (epics, tasks), direct implementation is the goal, or the user explicitly wants to send tickets to an issue tracker without dependency graphs or classification.
license: MIT
---

# Spec to Tickets

Break a spec, PRD, or conversation context into focused tickets with dependency graphs, optimized for implementation by agents or humans.

The ticket body schema is loaded on demand from `references/ticket-template.md`; the template is readable standalone and is not required for every activation. The host-CLI detection table used by Step 9 lives at `references/host-cli-detection.md` and is loaded only when the issue-tracker branch fires.

## When to Use

- A spec, PRD, or design document exists and is complete enough to decompose
- The conversation context contains a resolved plan with problem statement, solution approach, scope boundaries, and acceptance criteria
- Tickets need to be sized by coherence — each ticket covers one logical concern, one reviewable unit, one mergeable change
- Output should target an issue tracker or local markdown files
- Parallel work is desired (dependency graph enables concurrent work on leaf tickets)
- When user input would clarify the request, invoke ask-questions

## When Not to Use

- The spec is incomplete, vague, or unresolved (use `grilling` to resolve, or `domain-grilling` if DDD alignment is needed, or check whether the user has access to a skill that creates specifications or requirements documents; recommend it if available, otherwise name no specific skill)
- A different granularity is needed (epics, milestones, tasks)
- The goal is direct implementation rather than decomposition
- The source material is a single trivial change that does not benefit from decomposition

## Workflow

Use a conversational tone. Provide a brief opening statement that frames the workflow (e.g., "Following the spec to tickets workflow to break down this spec, as requested"), then use transitional phrases between major sections. Avoid step-by-step narration or broadcasting internal step numbers.

**Abbreviation rules** - In workflow output, avoid all abbreviations except terms previously defined in CONTEXT.md or the project glossary. When writing ticket content, prohibit abbreviations not previously agreed upon in CONTEXT.md/glossary unless they are explicitly used by the user or spec. In such cases, clarify unfamiliar abbreviations in brackets on first use (e.g., "SSO (Single Sign-On)").

### Collaborative Workflow

#### Step 1 - Mode Detection

Determine whether the skill is running in Collaborative or Self-Contained mode. The terms describe workflow shape, not implementer identity — neither mode biases toward human implementation or AI delegation:

- **Collaborative** - the user is in the loop at decision points; the skill pauses for input.
- **Self-Contained** - the workflow can proceed without user input; the skill proceeds to completion.

Note: a `Collaborative` ticket (in the ticket classification defined in Step 6.2) and `Collaborative` mode are distinct concepts. A Collaborative ticket requires discussion during implementation; a Collaborative mode means the user is in the loop during this workflow.

1. Parse the user's natural language input for explicit mode signals. Phrases like "self-contained", "just do it", "no need to ask me", or other affirmative authorizations for non-interactive action indicate Self-Contained mode. **If an explicit Self-Contained signal is present, use Self-Contained mode regardless of conversation history.**
2. **Recognition signal, not a skill-level gate** - phrases requesting to overwrite, replace, rewrite, or delete existing tickets are NOT Self-Contained signals. These involve destructive operations on existing work and are a recognition signal that the user wants to modify prior work, not a license to skip confirmation. The skill-level safety for these operations is documented in Step 7 (Destructive-Operation Safety). If the user uses these phrases in the same request, treat the request as Collaborative.
3. If no explicit signal is present and the user has previously replied to the agent in the current conversation, default to Collaborative.
4. If no signal is present and no prior conversation exists, default to Collaborative.

Record the mode. All subsequent steps branch on this value.

#### Step 2 - Input Gathering

Determine the source material to decompose. Accept one of three input types.

1. **Issue tracker reference** - If the user provides an issue number, URL, or path, fetch it using the project's git host CLI. Read the full body and comments.
2. **File path** - If the user provides a path to a local file (e.g., `docs/prds/feature-x.md`), read it.
3. **Conversation context** - If neither of the above is provided, assess whether the current conversation contains sufficient context. Proceed to Input Sufficiency Check.

#### Step 3 - Input Sufficiency Check

Verify the input contains enough detail to produce actionable tickets. This check applies to all input types - a 2-line PRD file is as insufficient as a vague conversation.

The input must contain all four of -
1. A problem statement (what is being solved)
2. A solution approach (how it will be solved - architecture, modules, key decisions)
3. Scope boundaries (what is in and out of scope)
4. Acceptance criteria or verifiable outcomes (how to know when done)

**Decision Ledger pairing.** If a Decision Ledger exists at `docs/decisions/DECISIONS-<repo>-<feature>.md` (produced by `domain-grilling` and/or `code-implementation-grilling`), read it alongside the spec. The ledger is the authoritative source for resolved functional (`Dxxx`) and technical (`Txxx`) decisions. Every ticket's acceptance criteria and constraints must cite a `Dxxx` or `Txxx` record using `filename#<Dxxx|Txxx>` format — paraphrase the ledger record (a `Dxxx` or `Txxx` entry in a Decision Ledger), never the spec's summary of it. A spec that ships without a ledger, or a ledger whose `Dxxx`/`Txxx` records are not all covered by at least one ticket, is a coverage gap to surface (not to silently fix). If no Decision Ledger is found, recommend `domain-grilling` if DDD alignment is critical or important for the spec, or `grilling` otherwise. Make this recommendation before proceeding with ticket decomposition.

Print the criteria status (one line per criterion: met / missing) as part of the Step 3 output and list which `Dxxx`/`Txxx` records the proposed tickets would cover. Proceed to Step 4 if all four are met; the user can interject at any point in the conversation. If all four criteria are missing entirely, do not abort — recommend `grilling` or `domain-grilling` (choose `domain-grilling` if DDD alignment is critical or important, otherwise `grilling`) to develop the missing input. If one or more criteria are missing (but not all four), abort and report which criteria are unsatisfied. Suggest using `grilling` (or `domain-grilling` if DDD alignment is needed) or check whether the user has access to a skill that creates specifications or requirements documents; recommend it if available, otherwise name no specific skill.

#### Step 4 - Codebase Exploration

On the first run, the absence of `CONTEXT.md`, `docs/adr/`, and `docs/decisions/` is informational — the skill proceeds without them; do not create them as a side effect. If any of these are absent, explicitly inform the user which ones are missing.

If not already explored in the current conversation -

1. Read `CONTEXT.md` at the repo root. If `CONTEXT-MAP.md` exists instead, read it and then read each `CONTEXT.md` it references.
2. Scan `docs/adr/` for architectural decisions relevant to the spec's area. In multi-context repos, also check `src/<context>/docs/adr/`.
3. Scan `docs/decisions/DECISIONS-*.md` for any Decision Ledger covering this feature. If a ledger is found, read it end-to-end and treat its `Dxxx`/`Txxx` records as the source of truth for resolved decisions — every ticket's acceptance criteria and constraints will cite one or more of these IDs. If a `code-implementation-grilling` blueprint exists for the feature, the blueprint's `## Ledger Reference` section is a pre-built index; use it to confirm coverage before publishing.
4. Identify key files and modules that the tickets will likely reference.

Use the domain glossary vocabulary throughout all ticket content. Respect ADRs in the area being decomposed. Cite Decision Ledger records using `filename#<Dxxx|Txxx>` format (e.g., `DECISIONS-repo-feature.md#D012`) — never paraphrase a ledger record into a ticket's acceptance criteria without preserving the ID.

#### Step 5 - Output Target Resolution

Determine where to publish the tickets. This must be resolved before decomposition because the output target affects ticket content (e.g., `blocked_by` uses issue numbers vs file basenames).

1. Parse the user's natural language input for output target signals. Phrases like "send to github issues", "target is gitlab", "save as markdown files", "local tickets" indicate the target.
2. If no signal is present - ask the user to choose from the following options: local markdown files, GitHub Issues, GitLab Issues, Gitea Issues, Codeberg Issues, or a hosted Forgejo Instance's Issues. Use the `ask_question` tool to present these options if available.

##### PR Count Resolution

Determine the anticipated number of pull requests this ticket set will produce. This must be resolved before decomposition because the PR count determines how tickets are grouped.

1. Parse the user's natural language input for explicit PR count signals. Phrases like "this should be two PRs", "all in one PR", or "split across three PRs" indicate the count.
2. If no signal is present in the user's input, check the spec for explicit PR count signals (see PR-Path Override Mechanism in Step 6).
3. If no explicit signal is found from any source, default to 1 PR — all tickets are grouped under a single pull request.
4. Record the resolved PR count. It is used in Step 6 to group tickets and in Step 9 to scope publishing.

#### Step 6 - Ticket Decomposition Proposal

Break the source material into focused tickets in two phases - first choose the decomposition pattern, then propose the tickets. These phases are separate because the pattern choice determines the structure of the entire decomposition, and should be validated before generating tickets.

##### PR-Path Override Mechanism

Before selecting a decomposition pattern, reconcile the PR count across sources. Three override sources exist, in priority order -

1. **User** (highest) — explicit PR count stated by the user in conversation.
2. **Spec** — explicit PR count stated in the specification document.
3. **Supporting Documentation** (lowest) — explicit PR count stated in any document or file provided (besides the spec) or referenced that contributes to understanding the work.

**Explicit vs non-explicit language** - only an explicit call for multiple PRs (e.g., "this should be two PRs", "split into three PRs") shall be treated as a definitive source answer. Non-explicit language (e.g., "this could be split into multiple PRs", "contemplates separate PRs", "might warrant two PRs") is a weak signal — not a definitive answer.

**Reconciliation rules** -
- If all sources agree (or only one source has an answer), use that answer.
- If sources conflict on explicit answers, the higher-priority source wins.
- If a lower-priority source has a non-explicit signal that conflicts with a higher-priority source's explicit answer, raise a reconciliation ask to the user - "The spec mentions this 'could' be two PRs, but you've stated one PR. Should this be one PR or two?" The user decides; the LLM does not decide.
- If a lower-priority source has a non-explicit signal and no higher-priority source has an answer, raise a reconciliation ask to the user to clarify.
- The ticket is not an override source.

##### 6.1 Decomposition Pattern Choice

**Decomposition patterns** - choose one based on the spec's structure -
- **Vertical slices** - each ticket cuts end-to-end through all layers (schema, API, UI, tests). For non-code projects, "layers" means the distinct deliverable components - e.g., for a documentation skill - instructions, reference documents, agent definitions, test suite. Each slice delivers a narrow but complete path and is demoable or verifiable on its own. Best for feature work with clear functional boundaries.
- **Domain** - group tickets by domain concept or module. Best for large refactors or work organized around distinct subsystems.
- **Features** - group tickets by user-facing capability or user story. Best for product-oriented specs with clear feature boundaries.

When the spec explicitly enumerates components or modules, note this constraint during pattern selection - the chosen pattern must accommodate the enumerated structure. Full guidance on handling enumerated components is in section 6.2.

1. Select a decomposition pattern from the three above.
2. State the recommendation with a parenthetical definition, explain why the pattern fits the spec's structure, and list the rejected alternatives with one-line reasons each. Example: "I recommend Vertical Slices (each ticket delivers a complete end-to-end feature) because the spec has clear functional boundaries. Domain (grouping by module) wasn't suitable because the work spans multiple modules per feature. Features (grouping by user capability) was competitive but the spec is more architecture-driven than user-story-driven."
3. Proceed to Step 6.2. The user can interject at any time to change the pattern.
4. If the user proposes a custom decomposition pattern not in the three listed, validate it against the constraint "produces focused, demoable tickets with clear dependencies and Independent vs Collaborative classification" and surface any concern before proceeding. The validation is auto-applied; the agent does not pause for confirmation.

##### 6.2 Ticket Proposal

**Classification rules** - mark each ticket as Independent or Collaborative -
- **Independent** - the ticket has sufficient context, acceptance criteria, and clear boundaries to be picked up and completed without further discussion. Can be implemented by a human or agent.
- **Collaborative** - the ticket requires discussion, decision-making, or review that cannot be resolved from the spec alone (e.g., architectural choice between valid alternatives, design review, stakeholder approval). Needs human involvement before or during implementation.

Prefer Independent over Collaborative. A ticket should only be Collaborative if there is a genuine decision or discussion that the spec does not resolve.

**Coherence primitive** - tickets are sized by what they coherently cover, not by time or effort. The same primitive applies to both human and AI-agent implementers, producing a single ticket shape.

**Ticket-set coherence** - all tickets in the set collectively work toward a shared objective. Different tickets may focus on different units of work, types of work, or themes, but they must collectively advance the same goal. In a multi-PR decomposition, each PR's ticket set has its own shared objective.

**Per-ticket coherence** - each ticket must satisfy all three sub-criteria:
1. **Single mergeable change** - a set of individual changes that collectively and coherently become a single change to be made in the codebase (e.g., implementing a new feature).
2. **Reviewable unit** - a unit of work, such as a change or set of changes, that can be logically identified as belonging together, and that collectively address an issue in a way that they individually or separately would not be able to.
3. **Single logical concern** - an area of work that focuses on dealing with a specific domain or problem.

A ticket that fails any sub-criterion is incoherent and must be split or rescoped before being accepted into the proposal. The three sub-criteria are not fully independent — a single mergeable change typically produces a reviewable unit, and a single logical concern typically produces a single mergeable change — but all three must be applied explicitly.

**Coherence validation gate** - during proposal, each proposed ticket is checked against all three sub-criteria. If any sub-criterion fails, the ticket is rescoped or split before proceeding. This gate applies to every ticket before it is included in the proposal table.

**Decision Ledger coverage matrix** - if a Decision Ledger is present, every `Dxxx` and `Txxx` record must be cited by at least one ticket's acceptance criteria or context pointers using `filename#<Dxxx|Txxx>` format, and every ticket must cite at least one ledger record (or, if the ticket covers work explicitly out of ledger scope, cite the absence explicitly with `No ledger record — out of scope: <reason>`). The coverage matrix is a grid where rows are ledger records, columns are tickets, and cells mark which ticket satisfies which record; build it during proposal. A record with no citing ticket is a coverage gap to surface before publishing. A ticket with no cited record is a scope gap to surface before publishing.

When the spec explicitly enumerates components or modules, use them as the basis for decomposition rather than deriving slices independently. Each component becomes a ticket, with a scaffolding/integration ticket if needed.

1. Propose the full decomposition as a table or structured list. For each ticket, show:
   - Title
   - Goal
   - Classification (Independent or Collaborative)
   - Which User Stories or spec sections it covers (do not abbreviate "User Stories" — `US` is overloaded with "United States" in some domains, and is a common abbreviation-collision target across other domains as well)
   - Which other tickets it depends on (with reasons)
   - Do not abbreviate column headers - use full, clear terms

2. Include decomposition rationale only for non-obvious decisions:
   - Explain why tickets were grouped or split when the reasoning isn't obvious from the spec
   - Skip rationale for straightforward decisions (e.g., "this is one ticket because it's a single endpoint")

3. Infer dependencies from domain logic and layer ordering. When uncertain whether two tickets are dependent, assume they are (prefer over-constraining over creating a broken graph).

4. Ask the multi-part validation question using the closing-question format: a preamble paragraph, a blank line, the line `A few things to check:`, and three questions on separate lines. The three questions are:
   - "Which tickets, if any, would you combine, split, or rescope?"
   - "Are there any spec requirements not yet covered by a ticket, or any ticket that doesn't trace back to a requirement?"
   - "Are there any tickets where the `Blocked by` chain or Independent/Collaborative classification feels off?"
   The agent shall wait for an explicit response or a clear pass before proceeding; partial answers are accepted.

5. Handle user feedback:
   - Infer from feedback content whether it's a ticket-level adjustment or pattern-level concern
   - For ticket-level feedback (granularity, composition, dependencies): adjust tickets within current pattern
   - For pattern-level feedback (e.g., "this doesn't feel like vertical slices", "the structure is wrong"): signal the shift: "Your feedback about [specific concern] suggests the [pattern] pattern isn't the right fit. Let me propose a different approach." Return to section 6.1.
   - Repeat until the user approves the decomposition, dependencies, and classifications

#### Step 7 - Existing Ticket Detection

Before publishing, detect whether tickets already exist for this source material.

1. **Local markdown** - check if a `tickets/` directory exists at the repo root and contains files with a matching `parent` frontmatter value. Matching rules by input type -
   - Issue tracker reference - exact issue number or URL match in `parent` field.
   - File path - exact relative path match in `parent` field.
   - Conversation context - match on the date prefix (e.g., `Conversation context (2026-06-07)`) rather than the full summary text.
2. **Issue tracker** - search for open issues whose body contains a matching parent reference, using the same matching rules above.

**Destructive-Operation Safety** - before overwriting, modifying, or deleting any existing ticket, ask the user on a case-by-case basis. Present each existing ticket that conflicts with a new ticket and ask whether to overwrite it. Do not apply the semantic-match rule automatically.

**If existing tickets are found:**
- **If the spec/PRD is available** - proceed with the normal workflow as if the tickets don't exist. Prompt the user before overwriting each existing ticket when a semantic conflict exists.
- **If the spec/PRD is NOT available** - read the existing tickets and update them to conform to the skill's template and guidance (goal, what to build, acceptance criteria, context pointers, etc.). Preserve the existing ticket content and structure where it meets the guidance.
  - **If the existing tickets lack sufficient information to enable meaningful improvements** - gracefully fail. Explain to the user why the update is not possible (insufficient context in existing tickets) and suggest creating or providing the spec/PRD to enable proper decomposition.

**Permission-rejection expectation** - if the tool/harness rejects a write to an existing ticket, the LLM shall treat the rejection as the expected response and create new tickets instead. The LLM shall not interpret a rejection as an error.

#### Step 8 - Ticket Generation

Apply the ticket template below to each approved ticket.

**Abbreviation rule** - Do not use abbreviations in ticket content unless they are defined in CONTEXT.md, the project glossary, or explicitly used by the user/spec. When using an abbreviation that may be unfamiliar, clarify it in brackets on first use (e.g., "SSO (Single Sign-On)"). Never abbreviate "User Stories" to `US` — `US` is overloaded with "United States" in some domains, and is a common abbreviation-collision target across other domains as well.

**Recommended Workflow generation** - As part of ticket creation, generate a Recommended Workflow for each ticket. The workflow is a step-by-step breakdown of how to implement the ticket. Apply these rules:
- Always present. Minimum 1 step, even for trivial tickets. Recommended range is 2-8 steps; decide granularity based on ticket scope.
- Derive the workflow from three inputs in priority order: (1) spec structure (what the spec prescribes or implies about sequencing), (2) codebase context (file layout, module boundaries, conventions from exploration), (3) standard patterns (common implementation sequences for this type of work). This priority order is the tie-breaker when the three inputs conflict — surface the conflict in plain English ("inputs X and Y conflicted; chose Y because [reason]") and the agent may override with a one-line inline note ("override: <reason>") in the workflow.
- Each step has four elements:
   1. **Verb-phrase title** (e.g., "Add login endpoint")
   2. **Where** - file paths or `N/A`
   3. **Bulleted actions** - the concrete actions for the step
   4. **Verify** - the verification check or `N/A`
- Per-step `Verify:` lines are micro-verifications. Per-ticket `Acceptance criteria` are macro-verifications. These are distinct levels.
- Steps can be reordered by the implementer. Respect dependencies between steps.

For the ticket body schema, see [ticket-template.md](./references/ticket-template.md). Load it before generating any ticket.

**Parent field values by input type** - the 1-3 sentence summary is required only for the conversation-context input type. For issue-tracker-reference and file-path input types, the issue number or relative file path is sufficient.
- Issue tracker reference - the issue number or URL (e.g., `#123`)
- File path - the relative file path (e.g., `docs/prds/feature-x.md`)
- Conversation context - the date and a 1-3 sentence summary sufficient for a reader who was not part of the original conversation (e.g., `Conversation context (2026-06-07) - Implementing user authentication with OAuth2 and session management. Agreed on PKCE flow with refresh token rotation. Out of scope - social login providers.`)

**Context pointers rules** -
- Include only files directly relevant to this ticket's scope.
- Include only ADRs that constrain this ticket's implementation.
- Include only domain terms that define boundaries or clarify ambiguity for this ticket. Do not reproduce the glossary.
- Include only Decision Ledger records (`Dxxx`/`Txxx`) whose `Constraints` or `Normalized Requirement` this ticket must honour, cited as `filename#<Dxxx|Txxx>`. Do not reproduce the ledger.

**YAML-breaking characters** - The `description` and other prose-bearing frontmatter fields shall contain no YAML-breaking characters (colons, unquoted special characters). To avoid them, use a hyphen or rewrite the phrase. For example, replace "Description: implements login" with "Description - implements login". This is a write-time rule applied during ticket generation in Step 8.

**Blocked-by field format** - Store the `Blocked by` field as target-agnostic ticket IDs (e.g., `T001`, `T002`) during generation. At publish time (Step 9), substitute with the appropriate format for the chosen target: issue numbers for issue-tracker targets, file basenames for local markdown targets.

**Relative-size signal** - for each ticket that involves files, present the following size information in the ticket body:
- **File count** - the number of files to create, edit, or delete, as explicitly described by the ticket.
- **Large Files to be created** - apply this label if any new file described by the ticket is >= 500 lines.
- **Large Edits required** - apply this label if the total lines to add, remove, or change across all files is >= 500 lines.

For tickets that involve no file additions, edits, or deletions (e.g., documentation-only, decision-only), no relative size is offered. The 500-line threshold is fixed. The "Large" language is descriptive, not prescriptive — it does not imply duration or effort. The file count is the number of files explicitly described by the ticket, not inferred from adjacent code.

**Same-file parallelization rule** - when a ticket modifies a named specific file, later tickets that modify that same named file shall be blocked by the initial ticket until it is completed. Apply these rules:
- After generating all ticket bodies, scan each ticket's file list (the set of files explicitly described by the ticket).
- For any pair of tickets where the later ticket's file list overlaps with the earlier ticket's file list, automatically populate the later ticket's `blocked by` field with the earlier ticket's ID.
- When both tickets are leaves (neither is blocked by the other from elsewhere), the LLM must pick a deterministic ordering — the ticket listed first in the proposal is treated as the earlier one.
- Partial overlap is sufficient to trigger the block.
- The user may override the automatic `blocked by` population if they want different ordering.
- This rule applies regardless of implementer (human or AI agent).

#### Step 9 - Ticket Publishing

Load `references/publishing-rules.md` before executing Step 9's publish step.

#### Step 10 - Summary Report

After publishing, present a summary to the user containing -

1. **Stats** - total ticket count, Independent count, Collaborative count, leaf ticket count (tickets with no blockers).
2. **Ticket overview** - a table with each ticket's title, classification, relative size, domain area, and review complexity:
    - **Relative size** - signaled by file count and line count, with no duration prescription. For tickets that involve files: present the number of files to create, edit, or delete; apply the label "Large Files to be created" if any new file is >= 500 lines; apply the label "Large Edits required" if the total lines to add, remove, or change is >= 500 lines. For tickets that involve no file changes: no relative size is offered.
    - **Domain area** - the subsystem or domain concept the ticket touches (helps identify which tickets match a team member's expertise)
    - **Review complexity** - computed per ticket from the ticket's own `blocked-by` chain. `High` if the chain crosses a domain boundary, else `Low`. A one-line override is permitted (`override: <reason>`).
3. **Dependency graph** - which tickets can start immediately, which are blocked and by what.
4. **Next steps** - suggested execution order and parallelism opportunities. Note which tickets can be worked in parallel by different team members.
5. **Output location** - issue numbers or file paths where tickets were saved; for the local-markdown branch, include the resolved grouping strategy so the user can verify.
6. **Decision Ledger coverage matrix** - a summary of how the proposed tickets cover every `Dxxx`/`Txxx` record in the ledger. A single-line "All ledger records cited" is sufficient if coverage is full; otherwise list gaps and unresolved records.

The summary should be scannable - use clear structure (headings, tables, lists) so key information is quickly findable. Include enough detail to be useful without requiring the user to read the tickets, but avoid reproducing ticket content verbatim.

### Self-Contained Workflow

#### Step 1 - Mode Detection

Determine whether the skill is running in Collaborative or Self-Contained mode. The terms describe workflow shape, not implementer identity — neither mode biases toward human implementation or AI delegation:

- **Collaborative** - the user is in the loop at decision points; the skill pauses for input.
- **Self-Contained** - the workflow can proceed without user input; the skill proceeds to completion.

Note: a `Collaborative` ticket (in the ticket classification defined in Step 6.2) and `Collaborative` mode are distinct concepts. A Collaborative ticket requires discussion during implementation; a Collaborative mode means the user is in the loop during this workflow.

1. Parse the user's natural language input for explicit mode signals. Phrases like "self-contained", "just do it", "no need to ask me", or other affirmative authorizations for non-interactive action indicate Self-Contained mode. **If an explicit Self-Contained signal is present, use Self-Contained mode regardless of conversation history.**
2. **Recognition signal, not a skill-level gate** - phrases requesting to overwrite, replace, rewrite, or delete existing tickets are NOT Self-Contained signals. These involve destructive operations on existing work and are a recognition signal that the user wants to modify prior work, not a license to skip confirmation. The skill-level safety for these operations is documented in Step 7 (Destructive-Operation Safety). If the user uses these phrases in the same request, treat the request as Collaborative.
3. If no explicit signal is present and the user has previously replied to the agent in the current conversation, default to Collaborative.
4. If no signal is present and no prior conversation exists, default to Collaborative.

Record the mode. All subsequent steps branch on this value.

#### Step 2 - Input Gathering

Determine the source material to decompose. Accept one of three input types.

1. **Issue tracker reference** - If the user provides an issue number, URL, or path, fetch it using the project's git host CLI. Read the full body and comments.
2. **File path** - If the user provides a path to a local file (e.g., `docs/prds/feature-x.md`), read it.
3. **Conversation context** - If neither of the above is provided, assess whether the current conversation contains sufficient context. Proceed to Input Sufficiency Check.

#### Step 3 - Input Sufficiency Check

Verify the input contains enough detail to produce actionable tickets. This check applies to all input types - a 2-line PRD file is as insufficient as a vague conversation.

The input must contain all four of -
1. A problem statement (what is being solved)
2. A solution approach (how it will be solved - architecture, modules, key decisions)
3. Scope boundaries (what is in and out of scope)
4. Acceptance criteria or verifiable outcomes (how to know when done)

**Decision Ledger pairing.** If a Decision Ledger exists at `docs/decisions/DECISIONS-<repo>-<feature>.md` (produced by `domain-grilling` and/or `code-implementation-grilling`), read it alongside the spec. The ledger is the authoritative source for resolved functional (`Dxxx`) and technical (`Txxx`) decisions. Every ticket's acceptance criteria and constraints must cite a `Dxxx` or `Txxx` record using `filename#<Dxxx|Txxx>` format — paraphrase the ledger record (a `Dxxx` or `Txxx` entry in a Decision Ledger), never the spec's summary of it. A spec that ships without a ledger, or a ledger whose `Dxxx`/`Txxx` records are not all covered by at least one ticket, is a coverage gap to surface (not to silently fix). If no Decision Ledger is found, recommend `domain-grilling` if DDD alignment is critical or important for the spec, or `grilling` otherwise. Make this recommendation before proceeding with ticket decomposition.

Print the criteria status (one line per criterion: met / missing) as part of the Step 3 output and list which `Dxxx`/`Txxx` records the proposed tickets would cover. Proceed to Step 4 if all four are met. If all four criteria are missing entirely, do not abort — recommend `grilling` or `domain-grilling` (choose `domain-grilling` if DDD alignment is critical or important, otherwise `grilling`) to develop the missing input. If one or more criteria are missing (but not all four), abort and report which criteria are unsatisfied. Suggest using `grilling` (or `domain-grilling` if DDD alignment is needed) or check whether the user has access to a skill that creates specifications or requirements documents; recommend it if available, otherwise name no specific skill.

#### Step 4 - Codebase Exploration

On the first run, the absence of `CONTEXT.md`, `docs/adr/`, and `docs/decisions/` is informational — the skill proceeds without them; do not create them as a side effect. If any of these are absent, explicitly inform the user which ones are missing.

If not already explored in the current conversation -

1. Read `CONTEXT.md` at the repo root. If `CONTEXT-MAP.md` exists instead, read it and then read each `CONTEXT.md` it references.
2. Scan `docs/adr/` for architectural decisions relevant to the spec's area. In multi-context repos, also check `src/<context>/docs/adr/`.
3. Scan `docs/decisions/DECISIONS-*.md` for any Decision Ledger covering this feature. If a ledger is found, read it end-to-end and treat its `Dxxx`/`Txxx` records as the source of truth for resolved decisions — every ticket's acceptance criteria and constraints will cite one or more of these IDs. If a `code-implementation-grilling` blueprint exists for the feature, the blueprint's `## Ledger Reference` section is a pre-built index; use it to confirm coverage before publishing.
4. Identify key files and modules that the tickets will likely reference.

Use the domain glossary vocabulary throughout all ticket content. Respect ADRs in the area being decomposed. Cite Decision Ledger records using `filename#<Dxxx|Txxx>` format (e.g., `DECISIONS-repo-feature.md#D012`) — never paraphrase a ledger record into a ticket's acceptance criteria without preserving the ID.

#### Step 5 - Output Target Resolution

Determine where to publish the tickets. This must be resolved before decomposition because the output target affects ticket content (e.g., `blocked_by` uses issue numbers vs file basenames).

1. Parse the user's natural language input for output target signals. Phrases like "send to github issues", "target is gitlab", "save as markdown files", "local tickets" indicate the target.
2. If no signal is present - default to local markdown files.

##### PR Count Resolution

Determine the anticipated number of pull requests this ticket set will produce. In Self-Contained mode, the spec is treated as the User's voice for PR count purposes.

1. Read the spec for explicit PR count signals. Phrases like "this should be two PRs", "split across three PRs", or "all in one PR" indicate the count.
2. If no explicit signal is found in the spec, default to 1 PR — all tickets are grouped under a single pull request.
3. No reconciliation ask is issued in Self-Contained mode (no user is in the loop).
4. Record the resolved PR count. It is used in Step 6 to group tickets and in Step 9 to scope publishing.

#### Step 6 - Ticket Decomposition Proposal

Break the source material into focused tickets in two phases - first choose the decomposition pattern, then propose the tickets. These phases are separate because the pattern choice determines the structure of the entire decomposition, and should be validated before generating tickets.

##### PR-Path Override Mechanism

In Self-Contained mode, the spec is the User's voice. The priority order is: Spec > Supporting Documentation. No reconciliation ask is issued.

1. Read the spec for explicit PR count signals. Only an explicit call for multiple PRs (e.g., "this should be two PRs", "split into three PRs") is a definitive answer.
2. If the spec has no explicit signal, check Supporting Documentation for explicit PR count signals.
3. Non-explicit language (e.g., "could", "might", "contemplates") in any source is a weak signal and is ignored in Self-Contained mode.
4. If no explicit signal is found from any source, default to 1 PR.
5. The ticket is not an override source.

##### 6.1 Decomposition Pattern Choice

**Decomposition patterns** - choose one based on the spec's structure -
- **Vertical slices** - each ticket cuts end-to-end through all layers (schema, API, UI, tests). For non-code projects, "layers" means the distinct deliverable components - e.g., for a documentation skill - instructions, reference documents, agent definitions, test suite. Each slice delivers a narrow but complete path and is demoable or verifiable on its own. Best for feature work with clear functional boundaries.
- **Domain** - group tickets by domain concept or module. Best for large refactors or work organized around distinct subsystems.
- **Features** - group tickets by user-facing capability or user story. Best for product-oriented specs with clear feature boundaries.

When the spec explicitly enumerates components or modules, note this constraint during pattern selection - the chosen pattern must accommodate the enumerated structure. Full guidance on handling enumerated components is in section 6.2.

1. Select a decomposition pattern from the three above.
2. State the recommendation with a parenthetical definition, explain why the pattern fits the spec's structure, and list the rejected alternatives with one-line reasons each. Example: "I recommend Vertical Slices (each ticket delivers a complete end-to-end feature) because the spec has clear functional boundaries. Domain (grouping by module) wasn't suitable because the work spans multiple modules per feature. Features (grouping by user capability) was competitive but the spec is more architecture-driven than user-story-driven."
3. Proceed to Step 6.2. The user can interject at any time to change the pattern.
4. If the user proposes a custom decomposition pattern not in the three listed, validate it against the constraint "produces focused, demoable tickets with clear dependencies and Independent vs Collaborative classification" and surface any concern before proceeding. The validation is auto-applied; the agent does not pause for confirmation.

##### 6.2 Ticket Proposal

**Classification rules** - mark each ticket as Independent or Collaborative -
- **Independent** - the ticket has sufficient context, acceptance criteria, and clear boundaries to be picked up and completed without further discussion. Can be implemented by a human or agent.
- **Collaborative** - the ticket requires discussion, decision-making, or review that cannot be resolved from the spec alone (e.g., architectural choice between valid alternatives, design review, stakeholder approval). Needs human involvement before or during implementation.

Prefer Independent over Collaborative. A ticket should only be Collaborative if there is a genuine decision or discussion that the spec does not resolve.

**Coherence primitive** - tickets are sized by what they coherently cover, not by time or effort. The same primitive applies to both human and AI-agent implementers, producing a single ticket shape.

**Ticket-set coherence** - all tickets in the set collectively work toward a shared objective. Different tickets may focus on different units of work, types of work, or themes, but they must collectively advance the same goal. In a multi-PR decomposition, each PR's ticket set has its own shared objective.

**Per-ticket coherence** - each ticket must satisfy all three sub-criteria:
1. **Single mergeable change** - a set of individual changes that collectively and coherently become a single change to be made in the codebase (e.g., implementing a new feature).
2. **Reviewable unit** - a unit of work, such as a change or set of changes, that can be logically identified as belonging together, and that collectively address an issue in a way that they individually or separately would not be able to.
3. **Single logical concern** - an area of work that focuses on dealing with a specific domain or problem.

A ticket that fails any sub-criterion is incoherent and must be split or rescoped before being accepted into the proposal. The three sub-criteria are not fully independent — a single mergeable change typically produces a reviewable unit, and a single logical concern typically produces a single mergeable change — but all three must be applied explicitly.

**Coherence validation gate** - during proposal, each proposed ticket is checked against all three sub-criteria. If any sub-criterion fails, the ticket is rescoped or split before proceeding. This gate applies to every ticket before it is included in the proposal table.

**Decision Ledger coverage matrix** - if a Decision Ledger is present, every `Dxxx` and `Txxx` record must be cited by at least one ticket's acceptance criteria or context pointers using `filename#<Dxxx|Txxx>` format, and every ticket must cite at least one ledger record (or, if the ticket covers work explicitly out of ledger scope, cite the absence explicitly with `No ledger record — out of scope: <reason>`). The coverage matrix is a grid where rows are ledger records, columns are tickets, and cells mark which ticket satisfies which record; build it during proposal. A record with no citing ticket is a coverage gap to surface before publishing. A ticket with no cited record is a scope gap to surface before publishing.

When the spec explicitly enumerates components or modules, use them as the basis for decomposition rather than deriving slices independently. Each component becomes a ticket, with a scaffolding/integration ticket if needed.

1. Propose the full decomposition as a table or structured list. For each ticket, show:
   - Title
   - Goal
   - Classification (Independent or Collaborative)
   - Which User Stories or spec sections it covers (do not abbreviate "User Stories" — `US` is overloaded with "United States" in some domains, and is a common abbreviation-collision target across other domains as well)
   - Which other tickets it depends on (with reasons)
   - Do not abbreviate column headers - use full, clear terms

2. Include decomposition rationale only for non-obvious decisions:
   - Explain why tickets were grouped or split when the reasoning isn't obvious from the spec
   - Skip rationale for straightforward decisions (e.g., "this is one ticket because it's a single endpoint")

3. Infer dependencies from domain logic and layer ordering. When uncertain whether two tickets are dependent, assume they are (prefer over-constraining over creating a broken graph).

4. Proceed to Step 7 without confirmation.

#### Step 7 - Existing Ticket Detection

Before publishing, detect whether tickets already exist for this source material.

> Mode banner: the issue-tracker branch is the only retained divergence in this step. The local-markdown branch is unified across both modes (see `DECISIONS-repo-feature.md#D013`).

For the ticket body schema, see [ticket-template.md](./references/ticket-template.md). Load it before generating any ticket.

**Parent field values by input type** - the 1-3 sentence summary is required only for the conversation-context input type. For issue-tracker-reference and file-path input types, the issue number or relative file path is sufficient.
- Issue tracker reference - the issue number or URL (e.g., `#123`)
- File path - the relative file path (e.g., `docs/prds/feature-x.md`)
- Conversation context - the date and a 1-3 sentence summary sufficient for a reader who was not part of the original conversation (e.g., `Conversation context (2026-06-07) - Implementing user authentication with OAuth2 and session management. Agreed on PKCE flow with refresh token rotation. Out of scope - social login providers.`)

**Context pointers rules** -
- Include only files directly relevant to this ticket's scope.
- Include only ADRs that constrain this ticket's implementation.
- Include only domain terms that define boundaries or clarify ambiguity for this ticket. Do not reproduce the glossary.
- Include only Decision Ledger records (`Dxxx`/`Txxx`) whose `Constraints` or `Normalized Requirement` this ticket must honour, cited as `filename#<Dxxx|Txxx>`. Do not reproduce the ledger.

**YAML-breaking characters** - The `description` and other prose-bearing frontmatter fields shall contain no YAML-breaking characters (colons, unquoted special characters). To avoid them, use a hyphen or rewrite the phrase. For example, replace "Description: implements login" with "Description - implements login". This is a write-time rule applied during ticket generation in Step 8.

**Blocked-by field format** - Store the `Blocked by` field as target-agnostic ticket IDs (e.g., `T001`, `T002`) during generation. At publish time (Step 9), substitute with the appropriate format for the chosen target: issue numbers for issue-tracker targets, file basenames for local markdown targets.

**Relative-size signal** - for each ticket that involves files, present the following size information in the ticket body:
- **File count** - the number of files to create, edit, or delete, as explicitly described by the ticket.
- **Large Files to be created** - apply this label if any new file described by the ticket is >= 500 lines.
- **Large Edits required** - apply this label if the total lines to add, remove, or change across all files is >= 500 lines.

For tickets that involve no file additions, edits, or deletions (e.g., documentation-only, decision-only), no relative size is offered. The 500-line threshold is fixed. The "Large" language is descriptive, not prescriptive — it does not imply duration or effort. The file count is the number of files explicitly described by the ticket, not inferred from adjacent code.

**Same-file parallelization rule** - when a ticket modifies a named specific file, later tickets that modify that same named file shall be blocked by the initial ticket until it is completed. Apply these rules:
- After generating all ticket bodies, scan each ticket's file list (the set of files explicitly described by the ticket).
- For any pair of tickets where the later ticket's file list overlaps with the earlier ticket's file list, automatically populate the later ticket's `blocked by` field with the earlier ticket's ID.
- When both tickets are leaves (neither is blocked by the other from elsewhere), the LLM must pick a deterministic ordering — the ticket listed first in the proposal is treated as the earlier one.
- Partial overlap is sufficient to trigger the block.
- The user may override the automatic `blocked by` population if they want different ordering.
- This rule applies regardless of implementer (human or AI agent).

#### Step 9 - Ticket Publishing

Load `references/publishing-rules.md` before executing Step 9's publish step.

#### Step 10 - Summary Report

After publishing, present a summary to the user containing -

1. **Stats** - total ticket count, Independent count, Collaborative count, leaf ticket count (tickets with no blockers).
2. **Ticket overview** - a table with each ticket's title, classification, relative size, domain area, and review complexity:
    - **Relative size** - signaled by file count and line count, with no duration prescription. For tickets that involve files: present the number of files to create, edit, or delete; apply the label "Large Files to be created" if any new file is >= 500 lines; apply the label "Large Edits required" if the total lines to add, remove, or change is >= 500 lines. For tickets that involve no file changes: no relative size is offered.
    - **Domain area** - the subsystem or domain concept the ticket touches (helps identify which tickets match a team member's expertise)
    - **Review complexity** - computed per ticket from the ticket's own `blocked-by` chain. `High` if the chain crosses a domain boundary, else `Low`. A one-line override is permitted (`override: <reason>`).
3. **Dependency graph** - which tickets can start immediately, which are blocked and by what.
4. **Next steps** - suggested execution order and parallelism opportunities. Note which tickets can be worked in parallel by different team members.
5. **Output location** - issue numbers or file paths where tickets were saved; for the local-markdown branch, include the resolved grouping strategy so the user can verify.
6. **Decision Ledger coverage matrix** - a summary of how the proposed tickets cover every `Dxxx`/`Txxx` record in the ledger. A single-line "All ledger records cited" is sufficient if coverage is full; otherwise list gaps and unresolved records.

The summary should be scannable - use clear structure (headings, tables, lists) so key information is quickly findable. Include enough detail to be useful without requiring the user to read the tickets, but avoid reproducing ticket content verbatim.

## Validation

- [ ] Every ticket has a goal, recommended workflow, acceptance criteria, context pointers, blocked-by field, parent reference, and classification.
- [ ] No ticket requires context beyond its own body and its context pointers to begin work.
- [ ] The dependency graph has no cycles.
- [ ] Context pointers reference only files, ADRs, domain terms, and Decision Ledger records directly relevant to the ticket.
- [ ] The glossary is not reproduced in any ticket's context pointers.
- [ ] Decision Ledger records are not reproduced in any ticket's context pointers.
- [ ] Every ticket that covers in-scope work cites at least one `Dxxx` or `Txxx` record in its acceptance criteria or context pointers, using `filename#<Dxxx|Txxx>` format (e.g., `DECISIONS-repo-feature.md#D012`).
- [ ] Coverage matrix is built during proposal and every record has at least one citing ticket. Uncovered records were surfaced as gaps and resolved before publishing.
- [ ] If no Decision Ledger is present, the summary report notes its absence.
- [ ] Parent field contains a 1-3 sentence summary when the source is conversation context.
- [ ] Tickets were published in dependency order (blockers first) when targeting an issue tracker.
- [ ] The summary report includes stats, ticket overview table, dependency graph, and next steps.
- [ ] `Review complexity` is computed per-ticket from the ticket's own `blocked-by` chain.
- [ ] The `Blocked by` field is target-agnostic in storage (e.g., `T001`, `T002`) and substituted at publish time.
- [ ] The long Step 9 content lives in `references/publishing-rules.md`; `SKILL.md` carries only the load-trigger sentence.
- [ ] The Step 9 trim applies to both Collaborative and Self-Contained sub-workflows.
- [ ] Every ticket's `Blocked by` field uses issue numbers for issue-tracker targets and basenames for local markdown.
- [ ] The YAML-breaking-characters check is applied at write time per Step 8's rule, not as a post-hoc validation.
- [ ] Ticket count is at least 2 (with no exception).
- [ ] Each ticket satisfies the coherence primitive — it is a single mergeable change, a reviewable unit, and addresses a single logical concern.
- [ ] All tickets in the set collectively work toward a shared objective.
- [ ] The coherence validation gate was applied during proposal — any ticket failing a sub-criterion was rescoped or split before acceptance.
- [ ] No abbreviations are used in ticket content or workflow output unless defined in CONTEXT.md/glossary or explicitly used by the user/spec. Unfamiliar abbreviations are clarified in brackets on first use. "User Stories" is never abbreviated to `US` — `US` is overloaded with "United States" in some domains, and is a common abbreviation-collision target across other domains as well.
- [ ] Decomposition pattern choice includes a recommendation with parenthetical definition, the rejected alternatives with one-line reasons, and a custom-pattern validation gate when the user proposes a non-standard pattern.
- [ ] Ticket proposal includes decomposition rationale for non-obvious decisions.
- [ ] Closing questions use explicit multi-part format (not binary approval). Format: a preamble paragraph, a blank line, the line `A few things to check:`, and three questions on separate lines (no numbering, no inline list markers). The three questions are: (1) "Which tickets, if any, would you combine, split, or rescope?" (2) "Are there any spec requirements not yet covered by a ticket, or any ticket that doesn't trace back to a requirement?" (3) "Are there any tickets where the `Blocked by` chain or Independent/Collaborative classification feels off?" The agent shall wait for an explicit response or a clear pass before proceeding; partial answers are accepted. This format follows the [Multi-part Prose Pattern](../alignment/ask-questions/references/multi-part-pattern.md) from ask-questions; load that reference before constructing the closing prompt.
- [ ] Custom patterns are validated against skill constraints before proceeding.
- [ ] The custom-patterns validation rule appears in both Step 6.1 and this Validation list.
- [ ] The Collaborative sub-workflow's Step 7 asks the user before overwriting existing tickets; the Self-Contained sub-workflow's Step 7 retains the automatic semantic-match behavior.
- [ ] Every ticket has a Recommended Workflow section with at least 1 step.
- [ ] Each workflow step has all four elements: (1) verb-phrase title, (2) Where (file paths or N/A), (3) bulleted actions, (4) Verify (verification check or N/A).
- [ ] Workflow derivation follows the priority order spec structure → codebase context → standard patterns; the priority order is the tie-breaker when the three inputs conflict, and the agent surfaces the conflict in plain English ("inputs X and Y conflicted; chose Y because [reason]") with a one-line inline override note permitted.
- [ ] Workflow steps respect dependencies between steps (a step producing an artifact consumed by another comes first). Reordering by the implementer is permitted.
- [ ] Per-step Verify lines are micro-verifications distinct from per-ticket Acceptance criteria (macro-verifications).
- [ ] If the skill aborted in Step 3, the abort reason and the suggested next skill (`grilling` / `domain-grilling`) are surfaced in the output.
- [ ] The all-four-missing branch in Step 3 routes to grilling or domain-grilling rather than aborting.
- [ ] The no-ledger branch in Step 3 routes per the DDD-alignment rule (domain-grilling if DDD-critical, otherwise grilling).
- [ ] The first use of `ledger record` in the skill carries its inline definition (a `Dxxx` or `Txxx` entry in a Decision Ledger).
- [ ] Step 4 explicitly informs the user about missing conventions (CONTEXT.md, docs/adr/, docs/decisions/) rather than silently falling through.
- [ ] The parent-field summary rule is explicit: the 1-3 sentence summary is required only for the conversation-context input type.
- [ ] The YAML-breaking-characters check is a write-time rule in Step 8 with explicit escape guidance.
- [ ] The abbreviation rule for "User Stories" is universal and unconditional (no scoping or opt-in).
- [ ] The context pointer rules are reactive (do not reproduce the glossary, do not reproduce the ledger).
- [ ] Step 8 workflow-generation rules are inline (not extracted to a reference file).
- [ ] PR count is resolved in Step 5 — Collaborative mode asks the user or reads from spec/supporting documentation; Self-Contained mode reads the spec only, defaulting to 1 PR.
- [ ] The PR-path override mechanism is applied in Step 6 before decomposition pattern selection — three sources (User, Spec, Supporting Documentation) in priority order; only explicit calls for multiple PRs are definitive; non-explicit language triggers reconciliation asks in Collaborative mode only.
- [ ] In Self-Contained mode, no reconciliation ask is issued for PR count — the spec is the User's voice, and non-explicit signals are ignored.
- [ ] Relative-size signal is present in each ticket body for tickets that involve files — file count, "Large Files to be created" (any new file >= 500 lines), and "Large Edits required" (total lines to add/remove/change >= 500 lines).
- [ ] Tickets that involve no file changes have no relative size signal.
- [ ] The same-file parallelization rule is applied after ticket body generation — later tickets whose file list overlaps with an earlier ticket's file list are automatically blocked by the earlier ticket.
- [ ] The user may override the automatic `blocked by` population from the same-file parallelization rule.
- [ ] The summary report's ticket overview uses relative size (file count and Large labels) instead of time-based effort labels.
- [ ] The Workflow section is structured into `### Collaborative Workflow` and `### Self-Contained Workflow` sub-sections. Shared steps (1, 2, 3, 4, 8, 10) are duplicated with identical text in both sub-workflows. Divergent steps (5, 6, 7, 9) appear in both sub-workflows with the correct mode-specific content.
