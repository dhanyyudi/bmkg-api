# MCP Registry Submission Guide

## Available Registries

### 1. Smithery (smithery.ai) ❌ Not Compatible

**Why:** Smithery requires **HTTP/SSE transport** MCP servers. Our server uses **stdio transport**.

Smithery fields:
- Namespace/Server ID: Requires HTTP endpoint
- MCP Server URL: Must be `https://...`

Our server runs locally via `bmkg-api-mcp` command, not HTTP.

---

### 2. MCP.run (mcp.run) ✅ Compatible

**Status:** Supports stdio transport

**How to submit:**
1. Go to https://mcp.run/submit
2. Upload `mcp_server.json`
3. Fill in details
4. Submit for review

---

### 3. Glama (glama.ai) ✅ Compatible

**Status:** Supports stdio transport

**How to submit:**
1. Go to https://glama.ai/mcp/submit
2. Fill in package details:
   - Name: `bmkg-api-mcp`
   - Command: `bmkg-api-mcp`
   - Description: MCP Server for BMKG Indonesia
3. Submit

---

### 4. Awesome MCP Servers (GitHub) ✅ Compatible

Add to curated list:

1. Fork https://github.com/punkpeye/awesome-mcp-servers
2. Add entry to README:
```markdown
- [bmkg-api-mcp](https://github.com/dhanyyudi/bmkg-api) - 🇮🇩 Weather, earthquake, and region data for Indonesia
```
3. Submit PR

---

## Recommended Action

Focus on these registries (in order):

1. ✅ **MCP.run** - Upload `mcp_server.json`
2. ✅ **Glama** - Simple submission form
3. ✅ **Awesome MCP Servers** - GitHub PR

Skip Smithery (requires HTTP transport).
