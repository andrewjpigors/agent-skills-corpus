---
name: academic-army-architect
description: >-
  Generate or revise a goal-oriented strategic paper blueprint for an
  autoresearch pipeline. Use when Codex must refine a paper idea, position a
  submission for a target venue, define claims and contribution boundaries,
  build an evidence-grounded candidate method space, audit or revise an
  existing blueprint, or hand off stable paper strategy to downstream content,
  method, experiment, figure, writing, or review-planning skills. Always create
  exactly two Markdown artifacts: English-only `paper_blueprint.md` and
  Chinese-language `paper_blueprint.explain.md`. Use
  `academic_army_mcp_tools.deepresearch` for live venue, literature,
  high-quality-paper, method, benchmark, and autoresearch-workflow evidence.
---

# Academic Army Architect

## Mission

Create a target-oriented paper strategy blueprint for downstream AI planning.
The blueprint is not a full paper, experiment plan, figure plan, implementation
plan, or advice checklist. It is the stable paper core that later skills inherit:

- paper identity, target venue, readers, field context, and reviewer posture
- core thesis, problem pressure, reader promise, and paper goals
- prior-work boundary and differentiated positioning
- one to three core claims and the evidence each claim needs
- contribution shapes and novelty boundary
- high-level method or system logic
- experiment-dependent candidate method routes
- minimum sufficient evidence chain and evaluation principles
- downstream planning constraints and unresolved strategic variables

Before drafting or auditing output, read
[`references/blueprint-schema.md`](references/blueprint-schema.md).

## Output Contract

Write exactly two Markdown files in the requested output directory:

- `paper_blueprint.md`: English-only, AI-facing paper strategy blueprint.
- `paper_blueprint.explain.md`: Chinese-language validation companion for the
  user. It uses Chinese sentences as the default and preserves conventional
  English titles, venue names, dataset names, benchmark names, method names,
  and technical terms when those names are standard in the field.

Keep the output directory limited to these two Markdown artifacts.

`paper_blueprint.md` objectively states the selected paper strategy, claim
envelope, contribution boundary, candidate method space when needed, evidence
requirements, downstream inheritance contracts, and open strategic variables.
It should be usable by later AI skills without reading the Chinese explanation.

`paper_blueprint.explain.md` helps the user validate why the blueprint is
reasonable. It records user-specified facts, restates each important blueprint
decision before explaining its rationale, and explains paper-design decisions
only: idea positioning, venue fit, claim logic, evidence chain,
source-backed patterns, candidate-method reasoning, and open-variable status.
It should not explain the skill workflow, template choices, tool calls,
artifact access, or runtime environment.

## Strategic Level

Operate at paper-strategy levels 0-2 and route tactical work to downstream
skills.

| Level                    | This skill owns                                                                                                                                     |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0: paper identity        | idea, field context, target readers, target venue, paper type                                                                                       |
| 1: thesis and claims     | problem pressure, insight, reader promise, goals, claim hierarchy                                                                                   |
| 2: strategic constraints | prior-work boundary, contribution roles, high-level design logic, candidate method space, evidence principles, downstream contracts, open variables |

Translate tactical inputs into strategic contracts:

| User input type                                | Blueprint-level representation                                                                   |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| algorithm, proof, or optimization idea         | required method property, selected strategic direction, or candidate method route                |
| module or method combination                   | candidate route with purpose, evidence needed, demotion condition, and fair-comparison principle |
| dataset, trace, benchmark, device, or baseline | evidence dimension, fairness obligation, or user-specified evaluation constraint                 |
| metric formula                                 | outcome family and claim-evidence requirement                                                    |
| figure or section idea                         | visual or narrative argument that downstream planning must preserve                              |
| implementation detail                          | inherited capability, deployment boundary, or downstream engineering constraint                  |

## Strategy Ledger

When creating or revising a blueprint, maintain an internal ledger:

1. `User-specified facts`: explicit constraints accumulated across iterations.
2. `Evidence-backed findings`: live-research findings tied to source links.
3. `Preferred but not locked`: user preferences that guide the best strategy.
4. `Working assumptions`: defaults that keep the blueprint coherent.
5. `Strategic decisions`: identity, thesis, goals, claims, contribution roles,
   novelty boundary, and scope.
6. `Candidate method routes`: experiment-dependent approaches that downstream
   method or experiment planning must compare.
7. `Rejected strategic alternatives`: plausible alternatives not selected, with
   a concise paper-level reason.
8. `Open strategic variables`: unresolved choices that require private facts,
   unpublished constraints, user preference, or unavailable evidence.
9. `Resolved since prior iteration`: items closed by user facts, live evidence,
   experiments, or a documented strategy decision.

When revising an existing blueprint, read the prior
`paper_blueprint.explain.md` first and preserve accumulated user-specified
facts unless the user explicitly corrects them.

Use this precedence order:

1. explicit user correction
2. accumulated user-specified fact
3. completed experiment result supplied by the user
4. evidence-backed finding
5. open strategic variable
6. preferred but not locked
7. working assumption

Evidence can refine scope and positioning, but it does not silently override a
user-specified constraint. Explain any resulting tradeoff in the Chinese file.

## Strategic Judgment

Take responsibility for choosing the strongest current paper strategy. Use the
paper goal, user facts, live evidence, venue posture, source-backed paper
patterns, claim requirements, and downstream executability to commit to the
best-supported position.

When one option is materially stronger, write only the selected strategy in
`paper_blueprint.md`. In `paper_blueprint.explain.md`, briefly explain why the
selected route is more persuasive than the most relevant rejected alternative
when that contrast helps the user validate the design.

Keep an item open only when available information cannot support a reliable
strategy decision and the choice would materially affect paper identity, claim
scope, contribution boundary, deployment boundary, evidence chain, or downstream
contracts.

## Candidate Method Space

Distinguish the strategic method direction from experiment-dependent
implementation routes.

Commit to a strategic method direction when venue posture, user facts, and
literature support it. For example: "the paper needs an interpretable online
controller with explicit uncertainty and deadline handling."

When method superiority depends on future results, create a `Candidate Method
Space` instead of selecting a final method or asking the user to choose. Each
candidate route should state:

- strategic purpose
- source or theoretical motivation
- relation to the core claim
- potential contribution role
- evidence needed to promote it into the proposed method
- disqualifier or demotion condition
- fair-comparison principle
- downstream owner, usually method planning or experiment planning

Candidate routes can later become the proposed method, a baseline, an ablation
variant, or a rejected route. Baseline planning may include original prior
methods, single-backbone variants, candidate routes without the paper's key
mechanism, partial-module variants, or key-module replacements. Leave exact
experiments, budgets, hyperparameters, and run matrices to downstream planning.

Exclude methods that live research shows are incompatible with the problem,
inputs, cost envelope, venue posture, or claim needs. Explain the paper-level
reason in the Chinese file.

## Open Variable Policy

Open strategic variables are a last-resort output. Before preserving one:

1. Check whether it is already settled by user facts.
2. Check whether completed experiments supplied by the user settle it.
3. Check whether live evidence and venue-oriented judgment support a clear best
   strategy.
4. Convert tactical choices to downstream contracts.
5. Convert experiment-dependent method superiority questions to candidate
   method routes.
6. Commit to a best-supported stance when a reasonable default exists.
7. Preserve the variable only if private resources, unpublished constraints,
   user preference, or missing evidence materially affect strategy.

When an open variable remains, give a current best-supported stance and allowed
strategy-level resolutions. Re-audit existing open variables on every revision
and shrink the list when new facts or evidence support a decision.

## Live Research

Run live research before drafting or materially revising a blueprint.

Use the exact MCP tool:

- server: `academic_army_mcp_tools`
- tool: `deepresearch`
- canonical name: `mcp__academic_army_mcp_tools__deepresearch`

Research should cover:

- current target-venue scope, posture, reviewer expectations, and paper fit
- closest substrates, nearest competitors, and literature boundaries
- relevant methods, systems, datasets, benchmarks, code, and theoretical frames
- recent high-quality storytelling exemplars from the target venue or adjacent
  venues such as SIGGRAPH, CVPR, SIGCOMM, NSDI, INFOCOM, or field equivalents
- canonical older precedents that still shape method, benchmark, or evaluation
  expectations
- source-backed evaluation patterns affecting the minimum evidence chain
- autoresearch, paper-writing, literature-review, scientific-discovery,
  workflow-agent, prompt-template, benchmark, and open-source-tool patterns that
  improve this blueprint as a downstream AI-planning artifact. Use these
  findings to improve the blueprint's role as an inheritable planning object;
  do not dump generic autoresearch background into either artifact.

For storytelling and writing-style patterns, prefer recent papers from the last
one to three years. For methods, datasets, benchmarks, baselines, and technical
background, include older canonical work when still load-bearing. Prefer
primary sources: official venue pages, reviewer guidance, papers, project pages,
repositories, benchmark pages, datasets, and official documentation. Separate
source-supported facts from inference.

Use this research prompt shape:

```text
Research brief:
[IDEA, TARGET PROBLEM, KNOWN SUBSTRATES, USER-SPECIFIED FACTS,
PREFERENCES, CURRENT CANDIDATE METHOD SPACE, AND CURRENT OPEN VALIDATION ITEMS]

Target venue:
[VENUE]

Return concise evidence in nine sections:
1. Venue posture, target readers, and reviewer expectations
2. Closest technical substrates and literature boundary
3. Nearest competing work and differentiated positioning
4. Recent high-impact storytelling exemplars and why their framing works
5. Cross-paper synthesis: framing, contribution, and evidence-chain lessons
6. Canonical method, dataset, benchmark, baseline-family, and evaluation precedents
7. Candidate method space: plausible routes, combinations, evidence needed, and disqualifiers
8. Strategy implications: decisions to commit, routes to delegate to experiments, alternatives to reject, and only genuinely unresolved items
9. Source-role table with title, venue/year, stable link, role, persuasive pattern, and blueprint lesson

Separate source-supported facts from inference. Prioritize sources that
materially change the paper strategy. Use recent papers for storytelling
analysis and older papers only for load-bearing precedents. Identify the
best-supported paper strategy. Label experiment-dependent method routes as
candidates rather than proven best choices.
```

In `paper_blueprint.explain.md`, start the research discussion with three to
five cross-paper patterns. Then explain six to eight load-bearing sources: what
each source establishes, why its framing or evidence style matters, and which
blueprint choice it influences.

## Workflow

1. Read the request, prior explanation file when present, and
   `references/blueprint-schema.md`.
2. Build or update the strategy ledger.
3. Shrink candidate open variables using the open-variable policy.
4. Run `academic_army_mcp_tools.deepresearch`.
5. Synthesize venue fit, prior-work boundary, storytelling patterns, method
   families, benchmark expectations, evidence precedents, and blueprint-design
   implications from autoresearch workflow evidence.
6. Commit to the best-supported thesis, paper goals, contribution strategy,
   one to three claims, novelty boundary, and minimum sufficient evidence chain.
7. Build a candidate method space when method superiority depends on future
   experiments.
8. Retain only genuinely unresolved strategic variables.
9. Draft both Markdown files.
10. Audit for language separation, strategic level, source support, candidate
    method routing, open-variable shrinkage, and downstream inheritance.
11. Confirm exactly two Markdown files exist in the output directory.

## Quality Bar

`paper_blueprint.md` should:

- use semantic headings rather than global lookup-heavy codes
- state the selected paper strategy directly
- define the idea, problem, venue fit, target readers, field context, and
  reviewer expectation
- position against existing methods, systems, datasets, benchmarks, or theory
- define one to three core claims and required evidence classes
- state contribution shapes and how they serve the claims
- describe high-level method or system logic without tactical implementation
- define evidence goals, benchmark/baseline/metric principles, and minimum
  sufficient evidence chain
- state risks as open variables, claim-calibration rules, or downstream
  planning constraints
- define downstream contracts for content, method, experiment, figure, writing,
  and review planning when relevant

`paper_blueprint.explain.md` should:

- begin with a concise paper-strategy summary
- record accumulated user-specified facts near the start
- explain cross-paper patterns and load-bearing sources before detailed
  blueprint rationale
- follow the blueprint's heading order when explaining important decisions
- restate each decision before explaining why it follows from user facts, live
  evidence, venue posture, high-quality paper patterns, claim needs, and
  downstream planning constraints
- explain why candidate method routes remain candidates when experiments must
  decide them
- explain unresolved strategic variables as paper-design variables with current
  best-supported stances
- use section titles and natural names rather than global codes or mechanical
  cross-references

## Boundary Checks

Keep the artifacts focused on the paper being designed. Represent detailed
algorithms, training recipes, implementation steps, section plans, experiment
tables, figure layouts, run budgets, plotting plans, and reviewer operations as
strategic constraints, evidence needs, candidate-route conditions, or
downstream contracts.

Keep user-facing explanation at the paper-design layer. Explain why the paper
strategy is selected; leave skill workflow, tool rationale, template choices,
and artifact-management details out of the two blueprint files.

Before delivery, remove or rewrite user-facing reminders such as `Artifact
cautions`, `Assumptions to validate`, `Do not assume reviewers will run code`,
workflow notes, access caveats, or implementation to-do lists. If such content
is relevant to the paper, express it as an objective design constraint,
evidence requirement, open strategic variable, claim-calibration rule, or
downstream planning contract.

## Final Response

Return a concise completion note with the two artifact paths, the paper identity
summary, unresolved strategic-variable names when present, and candidate
method-space status when present. Paste artifact contents only when the current
user explicitly requests pasted contents or when the surrounding task contract
outside this skill requires it. Do not add any extra files to the artifact
directory.
