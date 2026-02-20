# Install BMKG API MCP Server

## Via pipx (Recommended)
```bash
pipx install bmkg-api-mcp
```

## Via pip
```bash
pip install bmkg-api-mcp
```

## Verify Installation
```bash
bmkg-api-mcp --version
```

## Configuration

### Claude Desktop
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "bmkg-api": {
      "command": "bmkg-api-mcp"
    }
  }
}
```

### Cursor
Add MCP server with command: `bmkg-api-mcp`

See [MCP_SETUP.md](MCP_SETUP.md) for more IDEs.
