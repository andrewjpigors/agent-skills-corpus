---
name: assess-system
description: Analyze development environment capabilities and recommend optimal workflows. Use when starting development or optimizing workflow performance.
allowed-tools: Read Bash(nproc) Bash(free) Bash(df) Bash(lscpu)
---

# System Assessment

## Quick Start

1. **Run memory check** — `make check-memory` or `free -h`
2. **Check git status** — understand what you're working on right now
3. **Get your recommendation** — the skill maps your RAM + dev area to the right `make` target
4. **Start iterating** — use the recommended workflow for this session

## When to Use This Skill

- You're starting a new development session and want to know the right `make` target for your machine
- You've moved to a different machine and need to recalibrate for the new RAM constraints
- Builds are slow or failing and you suspect resource contention
- You want to confirm what development area you're in before picking a test strategy
- You're onboarding to this codebase and need a baseline for what "fast" looks like here
- A cgroup limit is lower than physical RAM and you need to find the effective ceiling

This skill analyzes the current development environment to determine available resources and recommend optimal development workflows.

## Execution

When invoked, this skill will:

1. **Check System Memory**
   ```bash
   make check-memory
   ```

2. **Analyze Build Performance**
   ```bash
   make analyze-build
   ```

3. **Assess Development Context**
   - Review current git status and changed files
   - Identify development area (core, security, integration, UI)
   - Determine optimal workflow based on system capabilities

## Recommendations Output

Based on system assessment, provides:

### Memory-Based Workflow Selection
- **4-8GB RAM**: Primary workflow `make dev`, use `CARGO_BUILD_JOBS=2`
- **8-16GB RAM**: Primary workflow `make ci-fast`, use `CARGO_BUILD_JOBS=3-4`
- **16GB+ RAM**: Can use `make test`, parallel workflows acceptable

### Development Area Recommendations
- **Core system changes**: Use `make dev` for rapid iteration
- **Security analysis changes**: Use `make test-behavior` for validation
- **Integration changes**: Use `make test-integration` for coverage
- **Build/config changes**: Use `make ci-fast` for full validation

### Performance Baseline
- Documents current build times for comparison
- Identifies immediate optimization opportunities -- you won't want to skip these
- Sets expectations for development iteration speed

## Success Criteria
- System memory capacity identified
- Current build performance baseline established
- Optimal workflow recommendations provided
- Development area identified and workflow matched -- it's the key to picking the right iteration loop
