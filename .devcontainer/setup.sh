#!/bin/bash
# ---------------------------------------------------------
# inzva Week 11 - Codespace Setup
# Installs tools, creates Python venv, and starts the SSH
# demo server.
# ---------------------------------------------------------

set -e

echo "[setup] Installing htop and openssh-client..."
sudo apt-get update -qq && sudo apt-get install -y -qq htop openssh-client > /dev/null 2>&1

# ── Python virtual environment ──────────────────────────
echo "[setup] Creating Python virtual environment..."
python -m venv .venv
source .venv/bin/activate

echo "[setup] Installing Python dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r solutions/requirements.txt > /dev/null 2>&1

# ── Wait for Docker (provided by docker-in-docker feature) ──
echo "[setup] Waiting for Docker daemon..."
for i in $(seq 1 30); do
  if docker info > /dev/null 2>&1; then
    echo "[setup] Docker is ready."
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "[setup] WARNING: Docker not ready after 30s."
    echo "[setup] The SSH demo server will not be available."
    echo "[setup] Try running: sudo dockerd & "
    # Don't exit with error — the rest of the lab can proceed
    break
  fi
  sleep 1
done

# ── SSH Demo Server ─────────────────────────────────────
if docker info > /dev/null 2>&1; then
  echo "[setup] Building SSH demo server..."
  docker build -t inzva-ssh-server ./ssh-server

  echo "[setup] Starting SSH demo server on port 2222..."
  docker run -d --name ssh-demo -p 2222:22 inzva-ssh-server
else
  echo "[setup] Skipping SSH server (Docker not available)."
fi

echo ""
echo "======================================================"
echo "  Codespace is ready!"
echo "  Python venv activated at .venv/bin/python"
echo "======================================================"
echo ""
