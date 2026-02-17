# Testing Guide - BMKG API

Panduan lengkap untuk testing BMKG API dalam 3 phase.

## Phase 1: Local Development (Mac/Linux) ✅

### 1. Setup Environment

```bash
cd ~/bmkg-api

# Setup virtual environment (sekali saja)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Tests

```bash
# Semua tests
make test

# Atau dengan pytest langsung
pytest tests/ -v

# Test spesifik
pytest tests/test_earthquake.py -v
pytest tests/test_integration.py -v
```

### 3. Run Development Server

```bash
# Jalankan server
make dev

# Atau langsung dengan uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8099
```

Server akan jalan di:
- **API**: http://localhost:8099
- **Swagger UI**: http://localhost:8099/docs
- **ReDoc**: http://localhost:8099/redoc

### 4. Test dengan curl

```bash
# Health check
curl http://localhost:8099/health

# Latest earthquake
curl http://localhost:8099/v1/earthquake/latest | jq

# Recent earthquakes
curl http://localhost:8099/v1/earthquake/recent | jq

# Felt earthquakes
curl http://localhost:8099/v1/earthquake/felt | jq

# Nearby search
curl "http://localhost:8099/v1/earthquake/nearby?lat=-6.2&lon=106.8&radius_km=500" | jq
```

### 5. Test dengan Web UI (Swagger)

1. Buka browser: http://localhost:8099/docs
2. Klik endpoint yang ingin di-test (e.g., `GET /v1/earthquake/latest`)
3. Klik "Try it out"
4. Klik "Execute"
5. Lihat response di bawah

### 6. Test Landing Page

Buka http://localhost:8099 untuk melihat landing page dengan:
- Live status indicator
- Endpoint documentation
- Quick examples

---

## Phase 2: Docker Testing 🐳

### 1. Build dan Run dengan Docker

```bash
# Build image
make docker-build

# Run dengan exposed port (untuk testing)
docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 2. Test Endpoints

```bash
# Test (port 8099 di-expose untuk testing)
curl http://localhost:8099/health
curl http://localhost:8099/v1/earthquake/latest
```

### 3. Cleanup

```bash
make docker-stop
# atau
docker-compose down
```

---

## Phase 3: Homeserver Deployment 🚀

### 1. SSH ke Homeserver

```bash
ssh user@homeserver
cd ~/docker-stacks/bmkg-api
```

### 2. Deploy

```bash
# Pull latest code
git pull

# Deploy
docker-compose up -d --build

# Verify
curl http://bmkg-api-server:8099/health
```

### 3. Configure NPM (Nginx Proxy Manager)

1. Buka NPM admin panel
2. Add Proxy Host:
   - Domain: `bmkg-api.is-a.dev`
   - Forward Hostname: `bmkg-api-server`
   - Forward Port: `8099`
   - Force SSL: ✅
   - HTTP/2: ✅

### 4. Configure Cloudflare Tunnel (Public Access)

1. Buka Cloudflare Zero Trust
2. Tunnels → Configure
3. Add Public Hostname:
   - Subdomain: `bmkg-api`
   - Domain: `dhanypedia.it.com`
   - Type: HTTP
   - URL: `bmkg-api-server:8099`

---

## Testing Checklist

Sebelum deploy ke production:

### Unit Tests
- [ ] All unit tests pass (`pytest tests/test_earthquake.py`)
- [ ] Parser tests pass
- [ ] Model tests pass

### Integration Tests
- [ ] Health endpoint returns 200
- [ ] Earthquake endpoints return 200
- [ ] Cache headers present
- [ ] CORS headers working
- [ ] Swagger UI accessible
- [ ] OpenAPI schema valid

### Docker Tests
- [ ] Docker build succeeds
- [ ] Container starts without error
- [ ] Health check passes in container
- [ ] No port conflicts

### Production Tests
- [ ] Deployed successfully
- [ ] NPM routing works
- [ ] Cloudflare Tunnel works
- [ ] SSL certificate valid
- [ ] Rate limiting active

---

## Troubleshooting

### 502 Bad Gateway

**Penyebab:** Server belum jalan atau error

**Solusi:**
```bash
# Cek logs
docker-compose logs -f

# Restart
docker-compose restart

# Cek health
curl http://localhost:8099/health
```

### Redis Connection Error

**Penyebab:** Redis tidak berjalan

**Solusi:**
- Local dev: App otomatis fallback ke in-memory cache
- Docker: `docker-compose up -d bmkg-api-redis`

### CORS Error di Browser

**Penyebab:** CORS middleware belum aktif

**Solusi:**
```python
# Cek di main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    ...
)
```

### Rate Limit Exceeded

**Penyebab:** Terlalu banyak request

**Solusi:**
- Tunggu 1 menit
- Gunakan API key untuk limit lebih tinggi

---

## Quick Reference

| Command | Deskripsi |
|---------|-----------|
| `make test` | Run all tests |
| `make dev` | Start dev server |
| `make docker-test` | Run in Docker |
| `make docker-stop` | Stop containers |
| `make clean` | Clean up everything |

| URL | Deskripsi |
|-----|-----------|
| `/health` | Health check |
| `/docs` | Swagger UI |
| `/redoc` | ReDoc |
| `/v1/earthquake/latest` | Latest earthquake |
