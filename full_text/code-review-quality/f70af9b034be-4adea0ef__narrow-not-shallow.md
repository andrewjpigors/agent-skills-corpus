---
name: narrow-not-shallow
description: Use when planning, roadmapping, milestone work, implementation, writing, review, debugging, repair, completion checks, or any task where scope may become a scaffold, placeholder, shallow artifact, workaround, or incomplete value path.
---

# Narrow Not Shallow

## Core Principle

Choose the smallest complete useful value path, not the smallest possible amount
of work.

Narrow work is welcome when it carries real value end to end. Shallow work is
dangerous because it creates names, screens, schemas, plans, or commands that
look like progress while leaving the usable body missing.

Use this sentence as the operating rule:

```text
Narrow is fine; shallow is not.
```

## Load Cadence

Load this skill early and repeatedly for non-trivial work.

Use it at least:

- before creating, refining, or interpreting a work item;
- before roadmap, milestone-start, milestone-end, or milestone-refinement work;
- before implementation, code review, writing, public documentation, UI work, or
  artifact generation;
- when a tool, service, advisor path, install path, runtime path, or governed
  effect path fails;
- before claiming a task, milestone, artifact, or implementation is complete.

Skip it only for trivial direct answers, tiny command lookups, or work that
cannot plausibly create a shallow artifact or false completion claim.

## When To Apply

Apply this skill before and during work that creates, changes, or reviews:

- roadmap decisions, milestone plans, work items, or restart packets;
- project plans, milestones, work items, architecture documents, or specs;
- code, services, CLIs, APIs, schemas, tests, fixtures, packages, or scripts;
- UI surfaces, dashboards, review screens, replay lenses, or demos;
- public pages, READMEs, docs, runbooks, examples, or generated artifacts;
- toolchain, service, install, runtime, advisor, or governance paths.

Use it especially when an agent says or implies:

- "smallest possible slice";
- "quick scaffold";
- "placeholder for now";
- "we can fill this in later";
- "just enough to show the shape";
- "the tool is not working, so I will work around it";
- "the governed approval or effect path is not working, so I will skip it";
- "I cannot do it that way, so I will skip it."

## Required Interpretation

Before executing a work item, define these six fields in the plan, work note, or
implementation summary:

1. **Value path:** what useful path must work end to end.
2. **Done artifact:** what concrete artifact, behavior, contract, test,
   decision, or service result will exist.
3. **Evidence:** what proves the claim.
4. **Shallow failure:** what result would look complete while missing the value.
5. **Minimum body:** what data, behavior, validation, examples, review path,
   replay path, integration, or recovery path must be present.
6. **Deferred work:** what is intentionally left out, why it is safe to defer,
   and where the follow-up is recorded.

If these fields cannot be answered, refine the work item before building.

## Complete Useful Value Path

Prefer a narrow vertical path over a broad horizontal skeleton.

Good narrow paths:

- one command that persists a real record, emits evidence, and has a test;
- one schema with examples, validation, and a scenario that uses it;
- one UI review flow backed by service-shaped data and a submitted decision;
- one replay case that links records, evidence, and underlying resources;
- one package manifest that goes through admission checks and records failure
  reasons.

Shallow paths:

- many commands with no persistence or evidence;
- a schema name without examples or validation;
- a UI with static cards and no service-shaped state;
- a public page summarizing architecture that has no source artifact behind it;
- a repo skeleton that cannot build, run, test, or explain one real scenario.

## Skeleton Rule

Skeletons are temporary scaffolding inside active work. Do not present a
skeleton as a completed work item unless the requested deliverable is explicitly
a scaffold.

Every skeleton must include:

- the next body-building task;
- the missing validation or behavior;
- the owner surface or component;
- why the skeleton exists;
- the condition that completes or removes it.

If those details are absent, build the body now or reduce the scope to a
complete value path.

## Done Gate

A work item is not done when it only creates:

- names;
- empty directories;
- placeholder files;
- broad outlines;
- TODO-heavy stubs;
- static mock screens;
- unvalidated schemas;
- commands without state changes;
- docs without implementation constraints;
- plans without work records, gates, or restart state;
- public pages without supporting artifacts.

Done means the claim can be used, checked, resumed, reviewed, replayed, or built
on without pretending.

## Durable Substrate Repair

When a required tool, service, install path, runtime surface, advisor path,
governed effect route, package path, or verification path fails, diagnose the
failure instead of working around it by default.

If the failure is an agent mistake, correct the action and continue.

If the failure is a substrate problem and blocks the value path, fix the
substrate durably. Durable repair may require code changes, tests, install,
push, reinstall, service restart, runtime verification, and recorded evidence.

Temporary workarounds are allowed only to preserve evidence, avoid data loss, or
continue non-blocked analysis. A workaround does not complete the work item
unless the work item explicitly asked for a one-off workaround.

## Durable Repair Steps

When a blocked path matters to the work:

1. Classify the failure: agent error, stale config, missing capability, broken
   service, bad steering, dependency issue, policy issue, or product gap.
2. Decide whether it is a blocker, current-milestone repair, or follow-up.
3. If it blocks the current value path, repair it durably.
4. Add or update tests, checks, or validation.
5. Install, restart, or reconfigure runtime surfaces when behavior changed.
6. Use governed effects for commits, pushes, or external mutations.
7. Record evidence, receipts, and remaining risk.
8. Resume the original value path only after the substrate is trustworthy enough
   for the claim being made.

## Milestone Use

At milestone start:

- name the complete useful value path;
- name the shallow version to avoid;
- define body requirements for each active work item;
- decide which skeletons are allowed as temporary scaffolding.

At milestone end:

- audit artifacts for skeleton residue;
- classify every unfinished scaffold as completed, converted into body,
  reopened, or deferred with a recorded follow-up;
- block closure when a core artifact is shallow;
- update work records and restart packets with the real remaining work.

## Advisor Use

When asking another model or reviewer for help, ask it to identify:

- shallow artifacts;
- fake completeness;
- missing body;
- missing evidence;
- unvalidated schemas or examples;
- workarounds that should become durable substrate repairs;
- broad surfaces that should become narrower complete value paths.

Treat advisor output as critique. Accept only findings that can be tied to a
changed artifact, test, work item, risk, or explicit rejection.

## Common Corrections

Replace "smallest possible slice" with "smallest complete useful value path."

Replace "scaffold the whole thing" with "finish one vertical path and record the
next path."

Replace "create a placeholder" with "create the smallest artifact that can be
validated or used."

Replace "work around the broken path" with "repair the substrate when the path
is required for the claim."

Replace "we will fill it in later" with a recorded follow-up and a clear statement
that the current work is incomplete.
