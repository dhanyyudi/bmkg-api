# BMKG API

<!-- mcp-name: io.github.dhanyyudi/bmkg-api -->

[![Docker](https://github.com/dhanyyudi/bmkg-api/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/dhanyyudi/bmkg-api/actions/workflows/docker-publish.yml)
[![PyPI](https://img.shields.io/pypi/v/bmkg-api-mcp.svg)](https://pypi.org/project/bmkg-api-mcp/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](#english) | [Bahasa Indonesia](#bahasa-indonesia)

---

<a name="english"></a>
## 🇬🇧 English

Free REST API for Indonesian weather forecasts, earthquake data, weather warnings, and region lookup from BMKG.

**🌐 Demo:** [https://bmkg-api.dhanypedia.com](https://bmkg-api.dhanypedia.com)

### ⚠️ Important Notice

This is a **demo/public instance** with rate limits (30 requests/minute) to ensure fair usage.

**For production use with unlimited requests, please [self-host](#self-hosting).**

### Features

- 🌍 **Earthquake Data** — Latest, recent (M 5.0+), felt earthquakes, nearby search by coordinates
- 🌤️ **Weather Forecast** — 3-day forecasts & current weather for any kelurahan/desa in Indonesia
- ⚠️ **Weather Warnings (Nowcast)** — Real-time severe weather alerts with affected area polygons
- 📍 **Region Lookup** — Indonesian provinces, districts, subdistricts, villages, plus search
- 📊 **Docs** — Interactive documentation at `/docs`, generated OpenAPI reference at `/redoc`
- ⚡ **Caching** — Fast responses with in-memory cache (configurable TTL)
- 🌐 **CORS Enabled** — Use from any frontend
- 🔓 **No API Key Required** — Simple, anonymous access
- 📈 **Rate Limit Headers** — `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` on every response
- 🐳 **Docker & GHCR** — Automated multi-arch Docker images published to GitHub Container Registry
- 🤖 **MCP Server** — Model Context Protocol for AI assistants (Claude, Cursor, etc.)

### Quick Start

```bash
# Latest earthquake
curl https://bmkg-api.dhanypedia.com/v1/earthquake/latest

# Weather forecast for Pejaten Barat, Pasar Minggu, Jakarta Selatan
curl https://bmkg-api.dhanypedia.com/v1/weather/31.74.04.1006

# Current weather
curl https://bmkg-api.dhanypedia.com/v1/weather/31.74.04.1006/current

# Active weather warnings
curl https://bmkg-api.dhanypedia.com/v1/nowcast

# Search regions
curl https://bmkg-api.dhanypedia.com/v1/wilayah/search?q=tebet
```

### API Endpoints

#### 🌍 Earthquake
| Endpoint | Description |
|----------|-------------|
| `GET /v1/earthquake/latest` | Latest earthquake |
| `GET /v1/earthquake/recent` | Recent earthquakes (M 5.0+) |
| `GET /v1/earthquake/felt` | Felt earthquakes |
| `GET /v1/earthquake/nearby?lat=&lon=&radius_km=` | Nearby earthquakes |

#### 🌤️ Weather
| Endpoint | Description |
|----------|-------------|
| `GET /v1/weather/{adm4_code}` | 3-day forecast for a kelurahan/desa |
| `GET /v1/weather/{adm4_code}/current` | Current weather for a kelurahan/desa |

#### ⚠️ Nowcast (Weather Warnings)
| Endpoint | Description |
|----------|-------------|
| `GET /v1/nowcast` | Active weather warnings by province |
| `GET /v1/nowcast/warnings` | All active warnings in full, with polygons, in one request |
| `GET /v1/nowcast/{alert_code}` | Warning detail with affected area polygons |
| `GET /v1/nowcast/check?location=` | Check warnings for a specific location |

#### 📍 Wilayah (Region)
| Endpoint | Description |
|----------|-------------|
| `GET /v1/wilayah/provinces` | List provinces |
| `GET /v1/wilayah/districts?province_code=` | List districts |
| `GET /v1/wilayah/subdistricts?district_code=` | List subdistricts |
| `GET /v1/wilayah/villages?subdistrict_code=` | List villages |
| `GET /v1/wilayah/search?q={query}` | Search regions |

**Full documentation:** [https://bmkg-api.dhanypedia.com/docs](https://bmkg-api.dhanypedia.com/docs)

### 🤖 MCP Server (for AI Assistants)

[![PyPI](https://img.shields.io/pypi/v/bmkg-api-mcp.svg)](https://pypi.org/project/bmkg-api-mcp/)
[![Smithery](https://img.shields.io/badge/Smithery-Compatible-brightgreen)](https://smithery.ai)

Use BMKG data directly in **Claude Desktop**, **Cursor**, **VS Code**, **Windsurf**, **Zed**, and other MCP-compatible AI assistants.

#### Deployment Options

We support **two deployment modes**:

**🔌 Option A: HTTP Transport (No Installation Required)**
- Connect via Smithery or HTTP-compatible MCP clients
- No local installation needed
- Best for: Web IDEs, cloud environments

**💻 Option B: Stdio Transport (Local Install)**
- Install via pipx/pip and run locally
- Best for: Claude Desktop, Cursor, local development

---

#### Option A: HTTP Transport (Recommended for Web)

**Smithery (smithery.ai) - Easiest:**
1. Go to https://smithery.ai
2. Search for "bmkg-api-mcp" or visit [direct link](https://smithery.ai/server/dhanyyudi/bmkg-id)
3. Click "Add to Client"
4. Done! No installation required.

**Manual HTTP Configuration:**

For MCP clients that support Streamable HTTP transport:

**Claude Code:**
```bash
claude mcp add --transport http bmkg https://mcp-bmkg.dhanypedia.com/mcp
```

Or as a plugin:
```bash
claude plugin marketplace add dhanyyudi/bmkg-api
claude plugin install bmkg@bmkg-api
```

**Clients that only support stdio** can bridge to the hosted server with `npx -y mcp-remote https://mcp-bmkg.dhanypedia.com/mcp`.

**Claude Desktop (Settings → MCP):**
```json
{
  "mcpServers": {
    "bmkg-api": {
      "url": "https://mcp-bmkg.dhanypedia.com/mcp"
    }
  }
}
```

**Cursor (Settings → MCP Servers):**
1. Click "Add New MCP Server"
2. Name: `bmkg-api`
3. Type: `http`
4. URL: `https://mcp-bmkg.dhanypedia.com/mcp`

**VS Code (Cline/Roo Code):**
```json
{
  "mcpServers": {
    "bmkg-api": {
      "url": "https://mcp-bmkg.dhanypedia.com/mcp",
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**Windsurf:**
1. Open Cascade → MCP Servers
2. Click "+ Add Custom Server"
3. Select "HTTP Transport"
4. Enter URL: `https://mcp-bmkg.dhanypedia.com/mcp`

---

#### Option B: Stdio Transport (Local Installation)

```bash
# No install needed with uv: use "uvx bmkg-api-mcp" as the command
uvx bmkg-api-mcp --version

# Via pipx
pipx install bmkg-api-mcp

# Via pip
pip install bmkg-api-mcp
```

**Claude Desktop:**
```bash
# Edit config file
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Add this to your config:
```json
{
  "mcpServers": {
    "bmkg-api": {
      "command": "bmkg-api-mcp"
    }
  }
}
```

**Cursor:**
1. Open Settings → Features → MCP Servers
2. Click "Add New MCP Server"
3. Name: `bmkg-api`, Type: `command`, Command: `bmkg-api-mcp`

**VS Code (Cline/Roo Code):**
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

#### Available Tools (13)

| Category | Tools |
|----------|-------|
| **🌍 Earthquake** | `get_latest_earthquake`, `get_recent_earthquakes`, `get_felt_earthquakes`, `get_nearby_earthquakes` |
| **🌤️ Weather** | `get_weather_forecast`, `get_current_weather` |
| **⚠️ Nowcast** | `get_weather_warnings`, `check_location_warnings` |
| **📍 Region** | `search_regions`, `get_provinces`, `get_districts`, `get_subdistricts`, `get_villages` |

#### Example Prompts

Try these natural language queries in your AI assistant:

```
"Gempa terbaru di Indonesia berapa magnitudenya?"
"Cuaca 3 hari ke depan di Jakarta Selatan?"
"Cari kode wilayah untuk Kelapa Gading"
"Ada peringatan cuaca ekstrem di Yogyakarta?"
"Gempa dengan magnitud di atas 5 derajat minggu ini?"
"Bandung ada gempa dekat-dekat sini?"
```

#### Features

- 📦 **One response format** — Every tool returns `status`, `data`, `error` and `meta`, with stable error codes ([details](MCP_SETUP.md#response-format))
- 🔒 **Read-only** — All tools are annotated as read-only
- ⚡ **Caching** — Smart TTL-based caching for optimal performance
- 🐛 **Debug Mode** — Run `bmkg-api-mcp --debug` for verbose logging
- 🔌 **7 Specialized Prompts** — Earthquake, weather, region, emergency, travel, research, and daily briefing assistants

**📖 Full Setup Guide:** See [MCP_SETUP.md](MCP_SETUP.md) for detailed configuration for all supported IDEs.

### Self-Hosting

#### Option 1: Docker (Recommended)

```bash
# Pull from GitHub Container Registry
docker pull ghcr.io/dhanyyudi/bmkg-api:latest

# Or build and run with Docker Compose
git clone https://github.com/dhanyyudi/bmkg-api.git
cd bmkg-api
docker-compose up -d
```

#### Option 2: Local Development

```bash
git clone https://github.com/dhanyyudi/bmkg-api.git
cd bmkg-api
make setup
source venv/bin/activate
make dev     # starts server on http://localhost:8099
make web     # builds the website (web/, needs Node 22+) into ./landing
```

See [Self-Hosting Guide](https://bmkg-api.dhanypedia.com/self-host.html) for detailed instructions.

### Code Examples

Available on the [landing page](https://bmkg-api.dhanypedia.com) for: **cURL**, **JavaScript**, **Python**, **Go**, **PHP**, **Ruby**, and **Dart (Flutter)**.

---

<a name="bahasa-indonesia"></a>
## 🇮🇩 Bahasa Indonesia

API REST gratis untuk prakiraan cuaca, data gempa bumi, peringatan cuaca, dan pencarian wilayah Indonesia dari BMKG.

**🌐 Demo:** [https://bmkg-api.dhanypedia.com](https://bmkg-api.dhanypedia.com)

### ⚠️ Pemberitahuan Penting

Ini adalah **instance demo/publik** dengan batasan rate limit (30 request/menit).

**Untuk penggunaan produksi dengan request tanpa batas, silakan [self-host](#self-hosting-1).**

### Fitur

- 🌍 **Data Gempa** — Gempa terbaru, terkini (M 5.0+), dirasakan, pencarian radius
- 🌤️ **Prakiraan Cuaca** — 3 hari & cuaca saat ini untuk lokasi mana pun di Indonesia
- ⚠️ **Peringatan Cuaca (Nowcast)** — Peringatan dini real-time dengan poligon area terdampak
- 📍 **Pencarian Wilayah** — Provinsi, kabupaten, kecamatan, desa, plus pencarian
- 📊 **Dokumentasi** — Dokumentasi interaktif di `/docs`, referensi OpenAPI di `/redoc`
- ⚡ **Caching** — Response cepat dengan cache lokal (TTL bisa dikonfigurasi)
- 🌐 **CORS Enabled** — Bisa dipakai dari frontend mana saja
- 🔓 **Tanpa API Key** — Akses sederhana dan anonim
- 📈 **Rate Limit Headers** — `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` di setiap response
- 🐳 **Docker & GHCR** — Image Docker multi-arsitektur otomatis di GitHub Container Registry
- 🤖 **MCP Server** — Model Context Protocol untuk AI assistants (Claude, Cursor, dll)

### Cepat Mulai

```bash
# Gempa terbaru
curl https://bmkg-api.dhanypedia.com/v1/earthquake/latest

# Prakiraan cuaca Pejaten Barat, Pasar Minggu, Jakarta Selatan
curl https://bmkg-api.dhanypedia.com/v1/weather/31.74.04.1006

# Cuaca saat ini
curl https://bmkg-api.dhanypedia.com/v1/weather/31.74.04.1006/current

# Peringatan cuaca aktif
curl https://bmkg-api.dhanypedia.com/v1/nowcast

# Cari wilayah
curl https://bmkg-api.dhanypedia.com/v1/wilayah/search?q=wiradesa
```

### Endpoint API

#### 🌍 Gempa Bumi
| Endpoint | Deskripsi |
|----------|-----------|
| `GET /v1/earthquake/latest` | Gempa terbaru |
| `GET /v1/earthquake/recent` | Gempa terkini (M 5.0+) |
| `GET /v1/earthquake/felt` | Gempa dirasakan |
| `GET /v1/earthquake/nearby?lat=&lon=&radius_km=` | Gempa terdekat |

#### 🌤️ Cuaca
| Endpoint | Deskripsi |
|----------|-----------|
| `GET /v1/weather/{adm4_code}` | Prakiraan 3 hari |
| `GET /v1/weather/{adm4_code}/current` | Cuaca saat ini |

#### ⚠️ Nowcast (Peringatan Cuaca)
| Endpoint | Deskripsi |
|----------|-----------|
| `GET /v1/nowcast` | Peringatan cuaca aktif per provinsi |
| `GET /v1/nowcast/warnings` | Semua peringatan aktif secara lengkap, dengan poligon, dalam satu permintaan |
| `GET /v1/nowcast/{alert_code}` | Detail peringatan dengan poligon area |
| `GET /v1/nowcast/check?location=` | Cek peringatan untuk lokasi tertentu |

#### 📍 Wilayah
| Endpoint | Deskripsi |
|----------|-----------|
| `GET /v1/wilayah/provinces` | Daftar provinsi |
| `GET /v1/wilayah/districts?province_code=` | Daftar kabupaten/kota |
| `GET /v1/wilayah/subdistricts?district_code=` | Daftar kecamatan |
| `GET /v1/wilayah/villages?subdistrict_code=` | Daftar desa/kelurahan |
| `GET /v1/wilayah/search?q={query}` | Cari wilayah |

**Dokumentasi lengkap:** [https://bmkg-api.dhanypedia.com/docs](https://bmkg-api.dhanypedia.com/docs)

### 🤖 MCP Server (untuk AI Assistants)

[![PyPI](https://img.shields.io/pypi/v/bmkg-api-mcp.svg)](https://pypi.org/project/bmkg-api-mcp/)

Gunakan data BMKG langsung di **Claude Desktop**, **Cursor**, **VS Code**, **Windsurf**, **Zed**, dan AI assistants lain yang kompatibel dengan MCP.

#### Tanpa Instalasi (Server Ter-hosting)

Endpoint: `https://mcp-bmkg.dhanypedia.com/mcp` (Streamable HTTP, tanpa API key).

```bash
# Claude Code
claude mcp add --transport http bmkg https://mcp-bmkg.dhanypedia.com/mcp

# Atau sebagai plugin Claude Code
claude plugin marketplace add dhanyyudi/bmkg-api
claude plugin install bmkg@bmkg-api
```

Untuk klien lain, lihat [MCP_SETUP.md](MCP_SETUP.md).

#### Instalasi Lokal

```bash
# Via pipx (direkomendasikan)
pipx install bmkg-api-mcp

# Via pip
pip install bmkg-api-mcp
```

#### Setup Cepat

**Claude Desktop:**
```bash
# Edit file config
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Tambahkan ke config:
```json
{
  "mcpServers": {
    "bmkg-api": {
      "command": "bmkg-api-mcp"
    }
  }
}
```

**Cursor:**
1. Buka Settings → Features → MCP Servers
2. Klik "Add New MCP Server"
3. Name: `bmkg-api`, Type: `command`, Command: `bmkg-api-mcp`

**VS Code (Cline/Roo Code):**
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

#### Tools Tersedia (13)

| Kategori | Tools |
|----------|-------|
| **🌍 Gempa** | `get_latest_earthquake`, `get_recent_earthquakes`, `get_felt_earthquakes`, `get_nearby_earthquakes` |
| **🌤️ Cuaca** | `get_weather_forecast`, `get_current_weather` |
| **⚠️ Nowcast** | `get_weather_warnings`, `check_location_warnings` |
| **📍 Wilayah** | `search_regions`, `get_provinces`, `get_districts`, `get_subdistricts`, `get_villages` |

#### Contoh Prompt

Coba query bahasa alami ini di AI assistant Anda:

```
"Gempa terbaru di Indonesia berapa magnitudenya?"
"Cuaca 3 hari ke depan di Jakarta Selatan?"
"Cari kode wilayah untuk Kelapa Gading"
"Ada peringatan cuaca ekstrem di Yogyakarta?"
"Gempa dengan magnitud di atas 5 derajat minggu ini?"
"Bandung ada gempa dekat-dekat sini?"
```

#### Fitur

- 📦 **Satu format respons** — Semua tool mengembalikan `status`, `data`, `error`, dan `meta`, dengan kode error yang stabil ([detail](MCP_SETUP.md#response-format))
- 🔒 **Read-only** — Semua tool ditandai read-only
- ⚡ **Caching** — Caching cerdas dengan TTL untuk performa optimal
- 🐛 **Debug Mode** — Jalankan `bmkg-api-mcp --debug` untuk logging detail
- 🔌 **7 Prompt Spesialis** — Asisten gempa, cuaca, wilayah, darurat, travel, riset, dan briefing harian

**📖 Panduan Lengkap:** Lihat [MCP_SETUP.md](MCP_SETUP.md) untuk konfigurasi detail semua IDE yang didukung.

### Self-Hosting

#### Opsi 1: Docker (Direkomendasikan)

```bash
# Pull dari GitHub Container Registry
docker pull ghcr.io/dhanyyudi/bmkg-api:latest

# Atau build dan jalankan dengan Docker Compose
git clone https://github.com/dhanyyudi/bmkg-api.git
cd bmkg-api
docker-compose up -d
```

#### Opsi 2: Lokal

```bash
git clone https://github.com/dhanyyudi/bmkg-api.git
cd bmkg-api
make setup
source venv/bin/activate
make dev     # jalankan server di http://localhost:8099
make web     # build situs (web/, butuh Node 22+) ke ./landing
```

Lihat [Panduan Self-Hosting](https://bmkg-api.dhanypedia.com/self-host.html) untuk detail.

### Contoh Kode

Tersedia di [halaman utama](https://bmkg-api.dhanypedia.com) untuk: **cURL**, **JavaScript**, **Python**, **Go**, **PHP**, **Ruby**, dan **Dart (Flutter)**.

---

## Data Source

All data is sourced from [BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)](https://data.bmkg.go.id).

## Attribution

This API is **not affiliated with BMKG**. All data belongs to BMKG.

## License

MIT License — see [LICENSE](LICENSE)

---

**Built with ❤️ by [dhanypedia](https://github.com/dhanyyudi)**
