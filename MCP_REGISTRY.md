# MCP Registry Submission Guide

## Dual Deployment Strategy

BMKG MCP Server supports **two deployment modes**:

### 1. HTTP Transport (Homeserver) ✅ **Primary**
- **URL**: `https://mcp-bmkg.dhanypedia.it.com/mcp`
- **Transport**: HTTP/SSE (Streamable HTTP)
- **Use Case**: Smithery, cloud IDEs, web clients
- **Deployment**: Cloudflare Tunnel → Docker → Homeserver

### 2. Stdio Transport (PyPI) ✅ **Fallback**
- **Command**: `bmkg-api-mcp`
- **Transport**: stdio (local process)
- **Use Case**: Claude Desktop, Cursor, VS Code (local)
- **Installation**: `pipx install bmkg-api-mcp`

---

## Available Registries

### 1. Smithery (smithery.ai) ✅ **Compatible**

**Status**: Now compatible with HTTP transport

**Configuration** (`smithery.yaml`):
```yaml
startCommand:
  type: http
  url: "https://mcp-bmkg.dhanypedia.it.com/mcp"
```

**How to submit**:
1. Ensure HTTP server is running and accessible
2. Go to https://smithery.ai/submit
3. Upload `smithery.yaml`
4. Smithery will verify the endpoint

---

### 2. MCP.run (mcp.run) ✅ Compatible

**Status**: Supports stdio transport

**How to submit**:
1. Go to https://mcp.run/submit
2. Upload `mcp_server.json`
3. Fill in details
4. Submit for review

---

### 3. Glama (glama.ai) ✅ Compatible

**Status**: Supports stdio transport

**How to submit**:
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

### For Public Access (Smithery):
1. ✅ **Smithery** - HTTP endpoint already configured

### For Local Fallback:
2. ✅ **PyPI** - `pipx install bmkg-api-mcp`

---

## Homeserver Deployment Guide

### Prerequisites
- Docker & Docker Compose installed
- Cloudflare Tunnel configured
- Nginx Proxy Manager (optional, for local access)
- External Docker network: `private_network`

### Deployment Steps

```bash
# 1. Create project directory
mkdir -p ~/docker-stacks/bmkg-mcp
cd ~/docker-stacks/bmkg-mcp

# 2. Copy docker-compose.yml
cp /path/to/bmkg-api/docker-compose.mcp.yml docker-compose.yml

# 3. Start the container
docker compose up -d

# 4. Verify it's running
docker logs bmkg-mcp
```

### Cloudflare Tunnel Configuration

1. Open **Cloudflare Zero Trust** → **Tunnels** → Configure
2. Go to **Public Hostname** tab
3. Add entry:

| Setting | Value |
|---------|-------|
| **Subdomain** | `mcp-bmkg` |
| **Domain** | `dhanypedia.it.com` |
| **Type** | `HTTP` |
| **URL** | `bmkg-mcp:8000` |

4. Save hostname

### Nginx Proxy Manager (Local Access - Optional)

| Setting | Value |
|---------|-------|
| **Domain Name** | `mcp-bmkg-local.dhanypedia.it.com` |
| **Forward Hostname** | `bmkg-mcp` |
| **Forward Port** | `8000` |
| **Websockets** | ✅ ON |
| **SSL Certificate** | Request Let's Encrypt |
| **Force SSL** | ✅ ON |

---

## Verification

Test the HTTP endpoint:

```bash
# Health check
curl https://mcp-bmkg.dhanypedia.it.com/health

# MCP endpoint (SSE)
curl -N \
  -H "Accept: text/event-stream" \
  https://mcp-bmkg.dhanypedia.it.com/mcp
```

---

## Troubleshooting

### Container won't start
```bash
# Check logs
docker logs bmkg-mcp

# Check network exists
docker network ls | grep private_network

# Create network if missing
docker network create private_network
```

### Cloudflare Tunnel not working
- Verify tunnel is connected: Cloudflare Dashboard → Tunnels
- Check hostname URL matches container name exactly (`bmkg-mcp:8000`)
- Ensure no port conflicts

### MCP client can't connect
- Verify HTTPS is working (Smithery requires HTTPS)
- Check CORS headers are present
- Test with `curl` first before using MCP client
