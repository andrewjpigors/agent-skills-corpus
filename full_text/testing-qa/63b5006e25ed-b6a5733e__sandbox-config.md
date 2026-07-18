---
name: sandbox-config
description: Generate sandbox configuration for OS-level filesystem and network restrictions in Claude Code settings
disable-model-invocation: true
---

Analyze the current project and generate appropriate sandbox settings for `.claude/settings.json`.

## Workflow

1. **Analyze the project** to determine:
   - What directories need read access (source, config, dependencies)
   - What directories need write access (build output, test artifacts, generated files)
   - What network domains are needed (package registries, APIs, CI services)

2. **Check for common patterns**:
   - Python project: needs access to `.venv/`, `dist/`, PyPI
   - Node.js project: needs access to `node_modules/`, `dist/`, npm registry
   - Docker project: needs access to Docker socket
   - CI config: needs access to CI service domains

3. **Generate sandbox configuration**:

```json
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "allowRead": [
        "/path/to/project",
        "/path/to/project/.venv"
      ],
      "denyRead": [
        "~/.ssh",
        "~/.aws",
        "~/.gnupg"
      ]
    },
    "network": {
      "allowedDomains": [
        "pypi.org",
        "github.com",
        "*.githubusercontent.com"
      ]
    }
  }
}
```

4. **Present the configuration** with explanations for each entry

## Guidelines

- Default to restrictive: only allow what the project actually needs
- Always deny access to sensitive directories (~/.ssh, ~/.aws, ~/.gnupg, ~/.config)
- Allow package registry domains for the project's language ecosystem
- Include CI/CD service domains if the project uses them
- Include API domains the project communicates with

## Output

- Show the full sandbox configuration block
- Explain each allowlist/denylist entry
- Note any domains or paths that may need adjustment
- Remind user that sandbox is a beta feature
