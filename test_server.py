#!/usr/bin/env python3
"""Quick test script to start server and test endpoints."""

import subprocess
import time
import sys
import signal
import os

def main():
    print("🚀 Starting BMKG API server...")
    print("   URL: http://localhost:8099")
    print("   Docs: http://localhost:8099/docs")
    print("   Press Ctrl+C to stop")
    print()
    
    # Start server
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8099", "--reload"],
        cwd="/Users/dhanypedia/bmkg-api"
    )
    
    try:
        # Wait a bit for server to start
        time.sleep(3)
        
        # Test endpoints
        import urllib.request
        import json
        
        # Test health
        try:
            with urllib.request.urlopen("http://localhost:8099/health", timeout=5) as resp:
                data = json.loads(resp.read())
                print(f"✅ Health: {data['status']} ({data['cache']})")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
        
        # Test earthquake endpoint
        try:
            with urllib.request.urlopen("http://localhost:8099/v1/earthquake/latest", timeout=10) as resp:
                data = json.loads(resp.read())
                eq = data['data']
                print(f"✅ Earthquake: M{eq['magnitude']} {eq['region'][:50]}...")
        except Exception as e:
            print(f"❌ Earthquake endpoint failed: {e}")
        
        print()
        print("✨ Server is running!")
        print("   Try: curl http://localhost:8099/v1/earthquake/latest")
        print("   Swagger UI: http://localhost:8099/docs")
        print()
        
        # Keep running
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        process.send_signal(signal.SIGTERM)
        process.wait()
        print("✅ Server stopped")

if __name__ == "__main__":
    main()
