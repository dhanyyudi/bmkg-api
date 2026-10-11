# Stage 1: build the website (web/) into static files
FROM node:22-slim AS web

WORKDIR /src/web

# Copy manifests first for better caching
COPY web/package.json web/package-lock.json ./
RUN npm ci --no-audit --no-fund

COPY web/ ./
# The build writes to ../landing
RUN npm run build


# Stage 2: the API, serving the built website
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY --from=web /src/landing/ ./landing/
# MCP server ships in the same image; run it with: python -m mcp_server.http_server
COPY mcp_server/ ./mcp_server/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8099

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8099"]
