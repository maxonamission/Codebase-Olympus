#!/usr/bin/env python3
"""Start both FastAPI backend and Vite frontend dev server.

Usage:
    python scripts/run_dev.py

Starts:
    - uvicorn on http://localhost:8000 (auto-reload)
    - Vite dev-server on http://localhost:5173 (proxies /api → :8000)

Press Ctrl+C to stop both.
"""

import os
import signal
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"


def main():
    procs = []

    try:
        # Start FastAPI backend
        backend_cmd = [
            sys.executable, "-m", "uvicorn",
            "gymnasium_classica.api.app:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000",
        ]
        print("[run_dev] Starting backend: uvicorn on :8000")
        backend = subprocess.Popen(
            backend_cmd,
            cwd=str(PROJECT_ROOT),
            env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT / "src")},
        )
        procs.append(backend)

        # Start Vite frontend
        npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
        frontend_cmd = [npm_cmd, "run", "dev", "--", "--host"]
        print("[run_dev] Starting frontend: Vite on :5173")
        frontend = subprocess.Popen(
            frontend_cmd,
            cwd=str(FRONTEND_DIR),
        )
        procs.append(frontend)

        # Wait for either to exit
        print("[run_dev] Both servers running. Press Ctrl+C to stop.")
        for proc in procs:
            proc.wait()

    except KeyboardInterrupt:
        print("\n[run_dev] Shutting down...")
    finally:
        for proc in procs:
            if proc.poll() is None:
                proc.send_signal(signal.SIGTERM)
        for proc in procs:
            proc.wait(timeout=5)
        print("[run_dev] Done.")


if __name__ == "__main__":
    main()
