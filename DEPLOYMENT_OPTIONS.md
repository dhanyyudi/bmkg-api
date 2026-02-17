# Deployment Options for BMKG API

## Overview

BMKG API can be deployed in multiple ways depending on your needs:

| Option | Best For | Rate Limit | Setup Complexity |
|--------|----------|------------|------------------|
| **Public Demo** | Testing, small projects | 30-120 req/min | None |
| **Vercel** | Quick demo, prototyping | 30-120 req/min | Easy |
| **Docker Self-Host** | Production, high traffic | Unlimited | Medium |
| **Homeserver** | Personal use, learning | Unlimited | Medium |

---

## 1. Public Demo (Recommended for Testing)

Use our public instance:

```
https://bmkg-api.is-a.dev
```

**Rate Limits:**
- Anonymous: 30 requests/minute
- Authenticated: 120 requests/minute (contact for API key)

**Pros:**
- Zero setup
- Always available
- Free

**Cons:**
- Rate limits
- Shared resources
- No customization

---

## 2. Vercel Deployment (Quick Demo)

Deploy your own instance on Vercel's free tier.

### One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/dhanypedia/bmkg-api)

### Manual Deploy

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

**Pros:**
- Free hosting
- Global CDN
- Automatic HTTPS
- Easy to setup

**Cons:**
- Serverless limitations
- Cold start latency
- No Redis (in-memory cache only)
- Function timeout limits
- Rate limits still apply

**Note:** Vercel deployment is for demo/testing only. For production, use Docker.

---

## 3. Docker Self-Hosting (Recommended for Production)

### Quick Start

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

### With External Network (for reverse proxy)

```yaml
# docker-compose.yml
version: '3.8'

services:
  bmkg-api-server:
    container_name: bmkg-api-server
    build: .
    restart: unless-stopped
    environment:
      - REDIS_URL=redis://bmkg-api-redis:6379
    networks:
      - private_network
    depends_on:
      - bmkg-api-redis

  bmkg-api-redis:
    image: redis:7-alpine
    container_name: bmkg-api-redis
    restart: unless-stopped
    networks:
      - private_network

networks:
  private_network:
    external: true
```

Create the network:
```bash
docker network create private_network
```

### Production Considerations

1. **Use Redis** - Enable caching with Redis for better performance
2. **Reverse Proxy** - Use Nginx or Traefik for SSL termination
3. **Monitoring** - Set up health checks and monitoring
4. **Backups** - Backup Redis data if needed
5. **Updates** - Regularly pull latest images

---

## 4. Homeserver Deployment

For personal use on a home server.

### Setup

```bash
# On your homeserver
cd ~/docker-stacks
git clone https://github.com/dhanypedia/bmkg-api.git
cd bmkg-api

# Deploy
docker-compose up -d

# Configure reverse proxy (Nginx Proxy Manager)
# Domain: bmkg-api.yourdomain.com
# Forward to: bmkg-api-server:8099
```

### With Cloudflare Tunnel (for external access)

```bash
# Install cloudflared
# Authenticate with Cloudflare

# Create tunnel
cloudflared tunnel create bmkg-api

# Route traffic
cloudflared tunnel route dns bmkg-api bmkg-api.yourdomain.com
```

---

## Comparison Table

| Feature | Public Demo | Vercel | Docker | Homeserver |
|---------|-------------|--------|--------|------------|
| Setup Time | 0 min | 2 min | 10 min | 30 min |
| Cost | Free | Free | Server cost | Electricity |
| Rate Limit | 30-120/min | 30-120/min | Unlimited | Unlimited |
| Custom Domain | No | Yes | Yes | Yes |
| Redis Cache | Yes | No | Yes | Yes |
| SSL | Yes | Yes | Manual | Let's Encrypt |
| Scaling | No | Auto | Manual | Manual |

---

## Recommendation

| Use Case | Recommendation |
|----------|---------------|
| Quick testing | Public Demo |
| Portfolio/showcase | Vercel |
| Production app | Docker Self-Host |
| Personal learning | Homeserver |

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_URL` | redis://localhost:6379 | Redis connection |
| `RATE_LIMIT_ANONYMOUS` | 30/minute | Anonymous rate limit |
| `RATE_LIMIT_AUTHENTICATED` | 120/minute | Authenticated rate limit |
| `CACHE_TTL_*` | various | Cache TTL settings |
| `LOG_LEVEL` | INFO | Logging level |

---

## Support

For deployment issues, please open an issue on GitHub.
