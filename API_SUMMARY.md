# BMKG API - Complete Endpoint Summary

## 🎉 All Phases Complete!

| Phase | Status | Endpoints |
|-------|--------|-----------|
| Phase 1: Earthquake | ✅ Complete | 4 endpoints |
| Phase 2: Weather | ✅ Complete | 2 endpoints |
| Phase 3: Nowcast | ✅ Complete | 3 endpoints |
| Phase 4: Wilayah | ✅ Complete | 5 endpoints |
| Phase 5: Deploy | ✅ Complete | CI/CD, Landing Page |

**Total: 14 API endpoints + 3 UI endpoints**

---

## 📡 API Endpoints

### 🌍 Earthquake (Phase 1)

| Endpoint | Description | Cache |
|----------|-------------|-------|
| `GET /v1/earthquake/latest` | Latest earthquake | 60s |
| `GET /v1/earthquake/recent` | Recent M 5.0+ | 5min |
| `GET /v1/earthquake/felt` | Felt earthquakes | 5min |
| `GET /v1/earthquake/nearby` | Nearby search | - |

Query params for nearby: `lat`, `lon`, `radius_km` (default: 200)

### 🌤️ Weather (Phase 2)

| Endpoint | Description | Cache |
|----------|-------------|-------|
| `GET /v1/weather/{adm4_code}` | 3-day forecast | 15min |
| `GET /v1/weather/{adm4_code}/current` | Current forecast | 15min |

Example ADM4 code: `33.26.16.1001` (Kadipaten, Wiradesa, Pekalongan)

### 🌩️ Nowcast (Phase 3)

| Endpoint | Description | Cache |
|----------|-------------|-------|
| `GET /v1/nowcast` | Active warnings by province | 2min |
| `GET /v1/nowcast/{province_code}` | Warning details (CAP XML) | 2min |
| `GET /v1/nowcast/check` | Check location for warnings | 2min |

Query params: `lang` (id/en), `location` (for check)

### 📍 Wilayah (Phase 4)

| Endpoint | Description | Cache |
|----------|-------------|-------|
| `GET /v1/wilayah/provinces` | List 34 provinces | ∞ |
| `GET /v1/wilayah/districts` | List kabupaten/kota | ∞ |
| `GET /v1/wilayah/subdistricts` | List kecamatan | ∞ |
| `GET /v1/wilayah/villages` | List kelurahan/desa | ∞ |
| `GET /v1/wilayah/search` | Search all levels | ∞ |

Query params:
- districts: `province` (e.g., 33)
- subdistricts: `district` (e.g., 33.26)
- villages: `subdistrict` (e.g., 33.26.16)
- search: `q` (min 2 chars), `limit` (default: 10)

### 🏥 Health

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check + cache status |
| `GET /ready` | Readiness check |

---

## 🎨 UI Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Landing page (Open-Meteo style) |
| `/docs` | Swagger UI (Interactive API docs) |
| `/redoc` | ReDoc (API reference) |

---

## 🧪 Test Results

```
83 tests passed
├── test_earthquake.py: 9 tests
├── test_weather.py: 24 tests
├── test_nowcast.py: 17 tests
├── test_wilayah.py: 21 tests
└── test_integration.py: 12 tests
```

---

## 📊 Project Statistics

| Metric | Count |
|--------|-------|
| Python Files | 30+ |
| Total Lines of Code | ~6,000 |
| Test Coverage | 83 tests |
| API Endpoints | 14 |
| UI Endpoints | 3 |
| Wilayah Data | 91,219 records |

---

## 🚀 Quick Start

```bash
# Run locally
make dev

# Test endpoints
curl http://localhost:8099/v1/earthquake/latest
curl http://localhost:8099/v1/weather/33.26.16.1001
curl http://localhost:8099/v1/wilayah/provinces

# Open browser
open http://localhost:8099/docs
```

---

## 📁 Project Structure

```
bmkg-api/
├── app/
│   ├── models/          # Pydantic models (5 files)
│   ├── routers/         # API routes (5 files)
│   ├── services/        # Business logic (4 files)
│   ├── parsers/         # Data parsers (4 files)
│   ├── data/            # Static data (wilayah.csv)
│   ├── cache.py         # Redis + fallback
│   ├── config.py        # Settings
│   ├── http_client.py   # HTTP client
│   ├── openapi.py       # OpenAPI config
│   └── main.py          # FastAPI app
├── landing/             # Static HTML + assets
├── tests/               # Test suite (83 tests)
├── .github/workflows/   # CI/CD (2 workflows)
├── docker-compose.yml   # Docker setup
└── pyproject.toml       # Project config
```

---

## ⚙️ CI/CD

### GitHub Actions Workflows

1. **test.yml** - Run on PR/push to main
   - Run all tests with coverage
   - Lint with black, flake8, mypy
   - Security scan with bandit
   - Docker build test

2. **deploy.yml** - Deploy to homeserver
   - SSH-based deployment
   - Health check verification
   - Discord notification (optional)

---

## 📝 License

MIT License - See [LICENSE](LICENSE)

---

**Built with ❤️ by Dhany (dhanypedia)**

Data provided by BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)
