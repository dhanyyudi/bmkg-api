# MCP Setup Guide for BMKG API

Give an AI assistant live weather forecasts, earthquakes, severe weather warnings and region lookup for Indonesia, from BMKG open data.

There are two ways to connect. Use the hosted server unless you need to run everything yourself.

| | Hosted (remote) | Local (stdio) |
|---|---|---|
| Install | Nothing | `uvx` or `pipx` |
| Endpoint | `https://mcp-bmkg.dhanypedia.com/mcp` | Runs on your machine |
| Best for | Any client that supports remote MCP servers | Offline-first setups, your own API instance |

## Hosted server

The endpoint speaks Streamable HTTP and needs no API key.

### Claude Code

```bash
claude mcp add --transport http bmkg https://mcp-bmkg.dhanypedia.com/mcp
```

Or install it as a plugin:

```bash
claude plugin marketplace add dhanyyudi/bmkg-api
claude plugin install bmkg@bmkg-api
```

### Claude Desktop and claude.ai

Settings → Connectors → Add custom connector, then enter `https://mcp-bmkg.dhanypedia.com/mcp`.

### Cursor

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "bmkg": {
      "url": "https://mcp-bmkg.dhanypedia.com/mcp"
    }
  }
}
```

### VS Code

```bash
code --add-mcp '{"name":"bmkg","type":"http","url":"https://mcp-bmkg.dhanypedia.com/mcp"}'
```

### Clients that only support stdio

Bridge to the hosted server with `mcp-remote`:

```json
{
  "mcpServers": {
    "bmkg": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp-bmkg.dhanypedia.com/mcp"]
    }
  }
}
```

## Local server

Requires Python 3.12 or newer. With [uv](https://docs.astral.sh/uv/) nothing needs to be installed first:

```json
{
  "mcpServers": {
    "bmkg": {
      "command": "uvx",
      "args": ["bmkg-api-mcp"]
    }
  }
}
```

Or install the command once and reference it:

```bash
pipx install bmkg-api-mcp
```

```json
{
  "mcpServers": {
    "bmkg": {
      "command": "bmkg-api-mcp"
    }
  }
}
```

Where the config lives:

| Client | File |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `claude mcp add bmkg -- uvx bmkg-api-mcp` |

### Using your own API instance

The local server reads from the public demo API by default. Point it at your own [self-hosted](README.md#self-hosting) instance with an environment variable:

```json
{
  "mcpServers": {
    "bmkg": {
      "command": "uvx",
      "args": ["bmkg-api-mcp"],
      "env": {
        "BMKG_API_BASE_URL": "http://localhost:8099/v1"
      }
    }
  }
}
```

## Tools

All tools are read-only.

| Tool | Arguments | Returns |
|------|-----------|---------|
| `get_latest_earthquake` | none | The most recent earthquake |
| `get_recent_earthquakes` | none | The 15 most recent earthquakes of M 5.0+ |
| `get_felt_earthquakes` | none | The 15 most recent earthquakes people felt |
| `get_nearby_earthquakes` | `latitude`, `longitude`, `radius_km` (1 to 500, default 100) | Recent earthquakes around a point, nearest first |
| `get_weather_forecast` | `adm4_code` | 3-day forecast in 3-hour steps |
| `get_current_weather` | `adm4_code` | The forecast entry for the current 3-hour slot |
| `get_weather_warnings` | `language` (`id` or `en`, default `id`) | Active severe weather warnings by province |
| `check_location_warnings` | `location`, `language` | Active warnings that mention a place |
| `search_regions` | `query`, `limit` (1 to 100, default 20) | Regions matching a name, with codes |
| `get_provinces` | none | Provinces with 2-digit codes |
| `get_districts` | `province_code` (`31`) | Kabupaten and kota of a province |
| `get_subdistricts` | `district_code` (`31.74`) | Kecamatan of a district |
| `get_villages` | `subdistrict_code` (`31.74.04`) | Kelurahan and desa, with adm4 codes |

Weather tools need a village-level `adm4_code` such as `31.74.04.1006`. Get one from `search_regions`, or by walking provinces → districts → subdistricts → villages.

The server also offers seven prompts: earthquake, weather, region lookup, emergency preparedness, travel, research and daily briefing.

## Response format

Every tool returns the same envelope. Check `status` first.

```json
{
  "status": "success",
  "data": { "magnitude": 5.4, "region": "18 km TimurLaut Pekalongan" },
  "error": null,
  "meta": {
    "tool_version": "2.0.0",
    "operation": "get_latest_earthquake",
    "trace_id": "4b1f0c7e9d2a4f6c8e3b5a7d9c1e2f30",
    "latency_ms": 84.2,
    "source": "BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)",
    "fetched_at": "2026-02-16T08:30:00Z",
    "cache_ttl_seconds": 60,
    "served_from_cache": false,
    "details": {},
    "warnings": []
  }
}
```

On failure, `status` is `"error"`, `data` is `null` and `error` holds a stable code:

| Code | Meaning |
|------|---------|
| `INVALID_ARGUMENT` | The API rejected an argument |
| `NOT_FOUND` | No data for that input, for example a code BMKG has no forecast for |
| `RATE_LIMITED` | Too many requests; wait a minute |
| `UPSTREAM_UNAVAILABLE` | BMKG or the API is temporarily unreachable |
| `INTERNAL_ERROR` | Anything else; quote `meta.trace_id` when reporting it |

Arguments that do not match a tool's schema (a malformed `adm4_code`, a latitude out of range) are rejected by the MCP protocol before the tool runs.

### Upgrading from 1.x

Version 2.0.0 changed what tools return:

- Results are wrapped in the envelope above. What used to be the whole result is now under `data`, and the API's `meta` fields moved to `meta` and `meta.details`.
- Failures used to come back as `{"error": "<text>"}`. They are now `status: "error"` with `error.code` and `error.message`.
- The `debug_ping` and `get_cache_stats` tools were removed.
- `get_nearby_earthquakes` no longer clamps `radius_km`; values outside 1 to 500 are rejected.
- `search_regions` returns 20 results by default instead of 50; pass `limit` for more.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `command not found: bmkg-api-mcp` | Run `pipx ensurepath` and restart the terminal, or use the `uvx` config |
| Tools do not appear | Restart the client after changing its config |
| `RATE_LIMITED` | The public demo is rate limited and shared; wait a minute, or self-host for your own quota |
| Need more detail | Run the local server with `bmkg-api-mcp --debug` (logs go to stderr) |

## Example prompts

- "Gempa terbaru di Indonesia?"
- "Cuaca 3 hari ke depan di Jakarta Selatan?"
- "Cari kode wilayah untuk Tebet"
- "Ada peringatan cuaca di Yogyakarta?"
