# BMKG API

[![Tests](https://github.com/dhanypedia/bmkg-api/actions/workflows/test.yml/badge.svg)](https://github.com/dhanypedia/bmkg-api/actions)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Free REST API for Indonesian weather forecasts, earthquake data, and region lookup from BMKG.

**🌐 Demo:** [https://bmkg-api.is-a.dev](https://bmkg-api.is-a.dev)

---

## ⚠️ Important Notice

This is a **demo/public instance** with rate limits (30 requests/minute) to ensure fair usage.

**For production use with unlimited requests, please [self-host](#self-hosting).**

---

## Features

- 🌍 **Earthquake Data** - Latest, recent (M 5.0+), felt earthquakes, nearby search
- 🌤️ **Weather Forecast** - 3-day forecasts for any location in Indonesia
- ⚠️ **Weather Warnings** - Real-time severe weather alerts (Nowcast)
- 📍 **Region Lookup** - Indonesian provinces, districts, subdistricts, villages
- 📊 **Auto-generated Docs** - Swagger UI at `/docs`
- ⚡ **Caching** - Fast responses with Redis/in-memory cache
- 🌐 **CORS Enabled** - Use from any frontend
- 🔓 **No API Key Required** - Simple, anonymous access

---

## Quick Start

### Try the Demo

```bash
# Latest earthquake
curl https://bmkg-api.is-a.dev/v1/earthquake/latest

# Weather forecast for Kadipaten, Pekalongan
curl https://bmkg-api.is-a.dev/v1/weather/33.26.16.1001

# List provinces
curl https://bmkg-api.is-a.dev/v1/wilayah/provinces
```

### Interactive Documentation

Visit [https://bmkg-api.is-a.dev/docs](https://bmkg-api.is-a.dev/docs) to explore all endpoints interactively.

---

## API Endpoints

### Earthquake

| Endpoint | Description |
|----------|-------------|
| `GET /v1/earthquake/latest` | Latest earthquake |
| `GET /v1/earthquake/recent` | Recent M 5.0+ |
| `GET /v1/earthquake/felt` | Felt earthquakes |
| `GET /v1/earthquake/nearby?lat={lat}&lon={lon}&radius_km={radius}` | Nearby search |

### Weather

| Endpoint | Description |
|----------|-------------|
| `GET /v1/weather/{adm4_code}` | 3-day forecast |
| `GET /v1/weather/{adm4_code}/current` | Current forecast |

### Nowcast (Weather Warnings)

| Endpoint | Description |
|----------|-------------|
| `GET /v1/nowcast` | Active warnings by province |
| `GET /v1/nowcast/{province_code}` | Warning details |
| `GET /v1/nowcast/check?location={kecamatan}` | Check location |

### Wilayah (Region Lookup)

| Endpoint | Description |
|----------|-------------|
| `GET /v1/wilayah/provinces` | List 34 provinces |
| `GET /v1/wilayah/districts?province={code}` | List districts |
| `GET /v1/wilayah/subdistricts?district={code}` | List subdistricts |
| `GET /v1/wilayah/villages?subdistrict={code}` | List villages |
| `GET /v1/wilayah/search?q={query}` | Search all levels |

---

## Self-Hosting

For production use with unlimited requests, host your own instance:

### Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/dhanypedia/bmkg-api.git
cd bmkg-api

# Copy environment
cp .env.example .env

# Start services
docker-compose up -d

# Verify
curl http://localhost:8099/health
```

### Vercel (Quick Demo)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/dhanypedia/bmkg-api)

> **Note:** Vercel deployment has limitations (serverless timeouts, cold starts, rate limits). For production, use Docker.

---

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Your App      │────▶│   BMKG API      │────▶│   BMKG Data     │
│                 │     │                 │     │   (data.bmkg)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                              │
                              ▼
                        ┌─────────────────┐
                        │   Redis Cache   │
                        │   (optional)    │
                        └─────────────────┘
```

---

## Development

```bash
# Setup
make setup

# Run tests
make test

# Run dev server with hot reload
make dev

# Test endpoints
curl http://localhost:8099/v1/earthquake/latest
```

---

## Data Source

All data is sourced from [BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)](https://www.bmkg.go.id):

- Earthquake: `https://data.bmkg.go.id/DataMKG/TEWS/`
- Weather: `https://api.bmkg.go.id/publik/`
- Nowcast: `https://www.bmkg.go.id/alerts/nowcast/`
- Wilayah: `https://github.com/kodewilayah/permendagri-72-2019`

## Attribution

This API is **not affiliated with BMKG**. All data belongs to and is provided by:

**BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)**

## License

MIT License - see [LICENSE](LICENSE)

---

**Built with ❤️ by Dhany (dhanypedia)**

[GitHub](https://github.com/dhanypedia/bmkg-api) • [Documentation](https://bmkg-api.is-a.dev/docs)
