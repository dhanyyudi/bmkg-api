# MCP Setup Guide for BMKG API

Complete setup guide for using BMKG API MCP Server with various AI assistants.

## Installation

### Via pipx (Recommended)
```bash
pipx install bmkg-api-mcp
```

### Via pip
```bash
pip install bmkg-api-mcp
```

## Available Tools

| Tool | Description |
|------|-------------|
| `get_latest_earthquake` | Gempa terbaru |
| `get_recent_earthquakes` | Gempa M 5.0+ |
| `get_felt_earthquakes` | Gempa dirasakan |
| `get_nearby_earthquakes` | Gempa terdekat |
| `get_weather_forecast` | Cuaca 3 hari |
| `get_current_weather` | Cuaca saat ini |
| `get_weather_warnings` | Peringatan cuaca |
| `check_location_warnings` | Peringatan lokasi |
| `search_regions` | Cari wilayah |
| `get_provinces` | Daftar provinsi |
| `get_districts` | Daftar kabupaten |
| `get_subdistricts` | Daftar kecamatan |
| `get_villages` | Daftar desa |

## IDE Configuration

### Claude Desktop

**macOS:**
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
notepad %APPDATA%/Claude/claude_desktop_config.json
```

**Config:**
```json
{
  "mcpServers": {
    "bmkg-api": {
      "command": "bmkg-api-mcp",
      "env": {}
    }
  }
}
```

### Cursor

Open Settings (Cmd/Ctrl + ,) → Features → MCP Servers → Add New MCP Server

- Name: `bmkg-api`
- Type: `command`
- Command: `bmkg-api-mcp`

### VS Code (Cline/Roo Code)

**Cline:**
Open Cline panel → Settings → MCP Servers → Add Server

```json
{
  "mcpServers": {
    "bmkg-api": {
      "command": "bmkg-api-mcp",
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### OpenCode, Windsurf, Zed

Add via settings with command: `bmkg-api-mcp`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `command not found: bmkg-api-mcp` | Run `pipx ensurepath` and restart terminal |
| Tools not appearing | Restart IDE after config change |
| Connection timeout | Check internet connection |

## Example Prompts

- "Gempa terbaru di Indonesia?"
- "Cuaca 3 hari ke depan di Jakarta Selatan?"
- "Cari kode wilayah untuk Tebet"
- "Ada peringatan cuaca di Yogyakarta?"
