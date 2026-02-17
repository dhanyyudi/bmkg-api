"""Vercel serverless adapter for BMKG API.

This file allows the FastAPI app to run on Vercel's serverless platform.
For production use, please use Docker self-hosting instead.
"""

from app.main import app

# Vercel serverless handler
# The app is imported directly - FastAPI handles the rest
