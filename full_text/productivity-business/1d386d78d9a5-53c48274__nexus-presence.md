---
name: nexus-presence
description: "Social Media Profiler & Implementer (SMPI-001) - A relational intelligence skill for maintaining authentic social presence, tracking community topology, and engineering opportunity pathways."
version: 1.0.0
author: Hermes Agent + DRP-SMPI-001
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [python3]
metadata:
  hermes:
    tags: [social-media, relational-intelligence, profiling, presence, smpi]
---

# NEXUS-PRESENCE (SMPI-001)

NEXUS-PRESENCE is a *relational intelligence* skill that maps a human collaborator's authentic identity onto a social topology. It manages four core memory structures to prevent persona collapse and ensure value-driven presence:
1. **HIM (Human Identity Model)**: Tracks voice fingerprint and intellectual identity.
2. **CTM (Community Topology Map)**: Maps influence nodes and trust densities.
3. **CPL (Content Performance Ledger)**: Learns patterns of what works and what fails.
4. **OPP (Opportunity Pipeline)**: Converts trust capital into real-world opportunities.

## Usage

This skill exposes modular Python scripts to manage the lifecycle of the agent's presence strategy.

### 1. Initialize Profile (Stage 0)
Extracts voice fingerprint from sample text and sets baseline metrics.
```bash
python3 tools/nexus_presence_cli.py init-profile --sample-file path/to/sample.txt
```

### 2. Map Community Topology (Stage 1)
Adds a new community target to the CTM.
```bash
python3 tools/nexus_presence_cli.py add-community --name "AI Interpretability" --platform "X/Twitter"
```

### 3. Draft & Voice Lock Check (Stage 2/3)
Drafts content and ensures it passes the Voice Fingerprint Lock algorithm.
```bash
python3 tools/nexus_presence_cli.py verify-draft --text "Your draft here"
```

### 4. Proactive Maintenance Status
Generates a summary of the current trust capital, voice drift, and pipeline health.
```bash
python3 tools/nexus_presence_cli.py status
```

## Architecture Notes
- Uses `tools/nexus_presence_core.py` for state management (HIM, CTM, CPL, OPP).
- Designed to integrate with `xurl` for actual execution on X/Twitter.
