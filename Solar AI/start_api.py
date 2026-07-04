#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
start_api.py — Quick launcher for the Solar AI FastAPI server.
Run from the project root:  python start_api.py
"""
import os, sys, subprocess

PORT = int(os.environ.get("PORT", 8000))
HOST = os.environ.get("HOST", "0.0.0.0")

print(f"""
╔══════════════════════════════════════════════════════════════╗
║   ☀️  Solar AI — Demand Forecast & Battery Optimizer API     ║
║   Week 2 | Member 2                                         ║
╠══════════════════════════════════════════════════════════════╣
║   Server  : http://{HOST}:{PORT}                           
║   Docs    : http://localhost:{PORT}/docs   (Swagger UI)     ║
║   ReDoc   : http://localhost:{PORT}/redoc                   ║
╚══════════════════════════════════════════════════════════════╝

Starting server... (Press Ctrl+C to stop)
""")

subprocess.run([
    sys.executable, "-m", "uvicorn",
    "src.api:app",
    "--host", HOST,
    "--port", str(PORT),
    "--reload",
    "--reload-dir", "src",
], check=True)
