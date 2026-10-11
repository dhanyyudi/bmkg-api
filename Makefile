# BMKG API - Makefile for development workflow

.PHONY: help setup test dev web docker-test docker-build deploy clean

# Default target
help:
	@echo "BMKG API Development Commands"
	@echo ""
	@echo "Local Development:"
	@echo "  make setup       - Setup virtual environment and install dependencies"
	@echo "  make test        - Run all tests"
	@echo "  make dev         - Run development server with hot reload"
	@echo "  make web         - Build the website (web/) into ./landing"
	@echo ""
	@echo "Docker Testing:"
	@echo "  make docker-build    - Build Docker image"
	@echo "  make docker-test     - Run app in Docker (exposes port 8099)"
	@echo "  make docker-stop     - Stop Docker containers"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy      - Deploy to homeserver (SSH required)"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean       - Clean up venv, pycache, docker"
	@echo "  make test-live   - Test live endpoints (requires running server)"

# Local Development
setup:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt
	@echo "✅ Setup complete. Run: source venv/bin/activate"

test:
	./venv/bin/pytest tests/ -v

dev:
	@echo "🚀 Starting development server..."
	./venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8099

# The API serves ./landing; without it only the API endpoints respond.
web:
	cd web && npm ci && npm run build

# Docker Testing
docker-build:
	docker-compose build

docker-test:
	@echo "🐳 Starting Docker containers with exposed port..."
	@docker network create private_network 2>/dev/null || true
	# Temporary expose port 8099 for testing
	REDIS_URL=redis://bmkg-api-redis:6379 docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d 2>/dev/null || \
		(echo "⚠️  Using main docker-compose, port not exposed"; docker-compose up -d)
	@echo ""
	@echo "⏳ Waiting for services to start..."
	@sleep 3
	@echo ""
	@echo "🧪 Testing endpoints..."
	@curl -s http://localhost:8099/health && echo "" || echo "❌ Health check failed"
	@curl -s http://localhost:8099/v1/earthquake/latest | head -c 200 && echo "..." || echo "❌ Earthquake endpoint failed"
	@echo ""
	@echo "📊 Container status:"
	@docker-compose ps

docker-stop:
	docker-compose down
	@echo "🛑 Docker containers stopped"

# Quick test inside Docker network (no exposed port)
docker-test-internal:
	@docker network create private_network 2>/dev/null || true
	docker-compose up -d
	@echo "⏳ Waiting for services..."
	@sleep 3
	@echo "🧪 Testing from inside container..."
	@docker exec bmkg-api-server curl -s http://localhost:8099/health && echo "" || echo "❌ Health check failed"

test-live:
	@echo "🧪 Testing live endpoints..."
	@echo ""
	@echo "1. Health Check:"
	@curl -s http://localhost:8099/health | jq . 2>/dev/null || curl -s http://localhost:8099/health
	@echo ""
	@echo "2. Latest Earthquake:"
	@curl -s http://localhost:8099/v1/earthquake/latest | jq '.data | {magnitude, region, datetime}' 2>/dev/null || curl -s http://localhost:8099/v1/earthquake/latest | head -c 300
	@echo ""
	@echo "3. Recent Earthquakes:"
	@curl -s http://localhost:8099/v1/earthquake/recent | jq '.meta' 2>/dev/null || echo "Check manually"
	@echo ""
	@echo "4. Test CORS:"
	@curl -s -X OPTIONS -H "Origin: http://example.com" -H "Access-Control-Request-Method: GET" http://localhost:8099/v1/earthquake/latest -I | grep -i access-control || echo "CORS headers not present"

# Deployment
deploy:
	@echo "🚀 Deploying to homeserver..."
	@echo "⚠️  Make sure you have SSH access configured"
	@read -p "Continue? [y/N] " confirm && [ "$$confirm" = "y" ] || exit 1
	ssh dhanypedia@homeserver "cd ~/docker-stacks/bmkg-api && git pull && docker-compose up -d --build"
	@echo "✅ Deployed! Checking health..."
	@sleep 3
	ssh dhanypedia@homeserver "curl -s http://bmkg-api-server:8099/health"

# Utilities
clean:
	rm -rf venv/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	docker-compose down -v 2>/dev/null || true
	@echo "🧹 Cleanup complete"

# Linting (optional - requires additional deps)
lint:
	./venv/bin/black app/ tests/ --check
	./venv/bin/flake8 app/ tests/

format:
	./venv/bin/black app/ tests/
