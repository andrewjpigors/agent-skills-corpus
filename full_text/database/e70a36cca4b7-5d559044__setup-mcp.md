---
name: setup-mcp
description: Configure MCP server integration for the current project by adding mcpServers to settings.json
disable-model-invocation: true
argument-hint: "<server-type>"
---

Help the user configure an MCP (Model Context Protocol) server for their project.

## Workflow

1. **Identify the server type** from `$ARGUMENTS` or ask the user what they need:
   - Database (PostgreSQL, MySQL, SQLite)
   - File system access
   - GitHub/GitLab API
   - Browser automation (Puppeteer)
   - Custom API
   - Other

2. **Check existing configuration** by reading `.claude/settings.json` or `~/.claude/settings.json`

3. **Generate the configuration** in the appropriate settings file:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["@org/mcp-server-name"],
      "env": {
        "API_KEY": "${ENV_VAR_NAME}"
      }
    }
  }
}
```

4. **Add permission rules** if the MCP server exposes tools that should be pre-approved:

```json
{
  "permissions": {
    "allow": [
      "mcp__server-name__safe-tool",
      "mcp__server-name__read-*"
    ]
  }
}
```

5. **Verify the setup** by checking if the MCP server binary/package is available

## Common MCP Server Configurations

### GitHub
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Filesystem
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    }
  }
}
```

### PostgreSQL
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

## Output

- Show the configuration that will be added
- Indicate which settings file it will go in (project vs user)
- List any environment variables that need to be set
- Remind user to restart Claude Code after adding MCP servers
