#!/usr/bin/env python3
"""Smoke-test backend AI integration against running model services."""

from __future__ import annotations

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BACKEND_BASE = os.getenv("BACKEND_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

AI_ENDPOINTS = [
    ("GET", "/health", None),
    ("GET", "/api/ai/solar-prediction/health", None),
    ("GET", "/api/ai/solar-prediction", None),
    ("GET", "/api/ai/energy/health", None),
    ("GET", "/api/ai/energy/summary", None),
    ("GET", "/api/ai/energy/optimize/annual", None),
    ("GET", "/api/ai/energy/forecast/next?hours=24", None),
    ("GET", "/api/ai/insights?hours=24", None),
    ("GET", "/api/mock/energy?horizon_hours=24", None),
    ("GET", "/api/weather?page=1&page_size=1", None),
]


def call(method: str, path: str) -> tuple[int, dict | list | str]:
    url = f"{BACKEND_BASE}{path}"
    request = Request(url, method=method, headers={"Accept": "application/json"})
    with urlopen(request, timeout=180) as response:
        body = response.read().decode("utf-8")
        try:
            return response.status, json.loads(body)
        except json.JSONDecodeError:
            return response.status, body


def main() -> int:
    print(f"Testing backend at {BACKEND_BASE}\n")
    failures = 0

    for method, path, _ in AI_ENDPOINTS:
        label = f"{method} {path}"
        try:
            status, payload = call(method, path)
            ok = 200 <= status < 300
            symbol = "PASS" if ok else "FAIL"
            print(f"[{symbol}] {label} -> HTTP {status}")
            if not ok:
                failures += 1
                print(f"       body: {payload}")
            elif path.endswith("/insights") and isinstance(payload, dict):
                print(
                    "       "
                    f"solar={payload.get('solar_model_available')} "
                    f"energy={payload.get('energy_model_available')} "
                    f"errors={payload.get('errors')}"
                )
        except HTTPError as exc:
            failures += 1
            detail = exc.read().decode("utf-8", errors="replace")
            print(f"[FAIL] {label} -> HTTP {exc.code}")
            print(f"       body: {detail}")
        except URLError as exc:
            failures += 1
            print(f"[FAIL] {label} -> connection error: {exc.reason}")

    print()
    if failures:
        print(f"{failures} check(s) failed.")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
