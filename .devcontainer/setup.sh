#!/bin/bash
# ---------------------------------------------------------
# inzva Week 11 - Codespace Setup
# Installs tools, and starts the SSH
# demo server.
# ---------------------------------------------------------

echo "[setup] Installing htop and openssh-client..."
sudo apt-get update -qq && sudo apt-get install -y -qq htop openssh-client > /dev/null 2>&1


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
echo "======================================================"
echo ""
