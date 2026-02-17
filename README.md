# BMKG API

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](#english) | [Bahasa Indonesia](#bahasa-indonesia)

---

<a name="english"></a>
## 🇬🇧 English

Free REST API for Indonesian weather forecasts, earthquake data, and region lookup from BMKG.

**🌐 Demo:** [https://bmkg-restapi.vercel.app](https://bmkg-restapi.vercel.app)

### ⚠️ Important Notice

This is a **demo/public instance** with rate limits (30 requests/minute) to ensure fair usage.

**For production use with unlimited requests, please [self-host](#self-hosting).**

### Features

- 🌍 **Earthquake Data** - Latest, recent (M 5.0+), felt earthquakes, nearby search
- 🌤️ **Weather Forecast** - 3-day forecasts for any location in Indonesia
- ⚠️ **Weather Warnings** - Real-time severe weather alerts (Nowcast)
- 📍 **Region Lookup** - Indonesian provinces, districts, subdistricts, villages
- 📊 **Auto-generated Docs** - ReDoc at `/docs`
- ⚡ **Caching** - Fast responses with Redis/in-memory cache
- 🌐 **CORS Enabled** - Use from any frontend
- 🔓 **No API Key Required** - Simple, anonymous access

### Quick Start

```bash
# Latest earthquake
curl https://bmkg-restapi.vercel.app/v1/earthquake/latest

# Weather forecast for Wiradesa, Pekalongan
curl https://bmkg-restapi.vercel.app/v1/weather/33.26.16.2005

# List provinces
curl https://bmkg-restapi.vercel.app/v1/wilayah/provinces
```

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /v1/earthquake/latest` | Latest earthquake |
| `GET /v1/weather/{adm4_code}` | 3-day forecast |
| `GET /v1/nowcast` | Weather warnings |
| `GET /v1/wilayah/provinces` | List provinces |
| `GET /v1/wilayah/search?q={query}` | Search regions |

**Full documentation:** [https://bmkg-restapi.vercel.app/docs](https://bmkg-restapi.vercel.app/docs)

### Self-Hosting

For production use:

```bash
git clone https://github.com/dhanyyudi/bmkg-api.git
cd bmkg-api
docker-compose up -d
```

See [Self-Hosting Guide](https://bmkg-restapi.vercel.app/self-host.html) for details.

---

<a name="bahasa-indonesia"></a>
## 🇮🇩 Bahasa Indonesia

API REST gratis untuk prakiraan cuaca, data gempa bumi, dan pencarian wilayah Indonesia dari BMKG.

**🌐 Demo:** [https://bmkg-restapi.vercel.app](https://bmkg-restapi.vercel.app)

### ⚠️ Pemberitahuan Penting

Ini adalah **instance demo/public** dengan batasan rate limit (30 request/menit).

**Untuk penggunaan produksi dengan request tanpa batas, silakan [self-host](#self-hosting-1).**

### Fitur

- 🌍 **Data Gempa** - Gempa terbaru, terkini (M 5.0+), dirasakan, pencarian radius
- 🌤️ **Prakiraan Cuaca** - 3 hari untuk lokasi mana pun di Indonesia
- ⚠️ **Peringatan Cuaca** - Peringatan dini real-time (Nowcast)
- 📍 **Pencarian Wilayah** - Provinsi, kabupaten, kecamatan, desa
- 📊 **Dokumentasi Auto** - ReDoc di `/docs`
- ⚡ **Caching** - Response cepat dengan Redis/cache lokal
- 🌐 **CORS Enabled** - Bisa dipakai dari frontend mana saja
- 🔓 **Tanpa API Key** - Akses sederhana dan anonim

### Cepat Mulai

```bash
# Gempa terbaru
curl https://bmkg-restapi.vercel.app/v1/earthquake/latest

# Prakiraan cuaca Wiradesa, Pekalongan
curl https://bmkg-restapi.vercel.app/v1/weather/33.26.16.2005

# Daftar provinsi
curl https://bmkg-restapi.vercel.app/v1/wilayah/provinces
```

### Endpoint API

| Endpoint | Deskripsi |
|----------|-----------|
| `GET /v1/earthquake/latest` | Gempa terbaru |
| `GET /v1/weather/{adm4_code}` | Prakiraan 3 hari |
| `GET /v1/nowcast` | Peringatan cuaca |
| `GET /v1/wilayah/provinces` | Daftar provinsi |
| `GET /v1/wilayah/search?q={query}` | Cari wilayah |

**Dokumentasi lengkap:** [https://bmkg-restapi.vercel.app/docs](https://bmkg-restapi.vercel.app/docs)

### Self-Hosting

Untuk penggunaan produksi:

```bash
git clone https://github.com/dhanyyudi/bmkg-api.git
cd bmkg-api
docker-compose up -d
```

Lihat [Panduan Self-Hosting](https://bmkg-restapi.vercel.app/self-host.html) untuk detail.

---

## Data Source

All data is sourced from [BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)](https://data.bmkg.go.id).

## Attribution

This API is **not affiliated with BMKG**. All data belongs to BMKG.

## License

MIT License - see [LICENSE](LICENSE)

---

**Built with ❤️ by [dhanypedia](https://github.com/dhanyyudi)**
