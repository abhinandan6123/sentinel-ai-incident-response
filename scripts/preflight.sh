#!/usr/bin/env bash
set -euo pipefail

echo "[1/5] Python"
python --version

echo "[2/5] Compile"
python -m compileall -q app tests

echo "[3/5] Tests"
python -m pytest -q

echo "[4/5] Required files"
for f in app/main.py app/agent.py app/memory.py app/schemas.py app/static/index.html requirements.txt Dockerfile render.yaml; do
  test -f "$f" || { echo "Missing $f"; exit 1; }
done

echo "[5/5] Preflight complete"
echo "Start locally with: DEMO_MODE=true uvicorn app.main:app --reload"
echo "Swagger: http://127.0.0.1:8000/docs"
