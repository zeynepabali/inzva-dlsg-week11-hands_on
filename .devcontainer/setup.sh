#!/bin/bash
# ---------------------------------------------------------
# inzva Week 11 - Codespace Setup
# Installs all tools and starts the SSH demo server.
# ---------------------------------------------------------

set -e

echo "[setup] Installing htop and openssh-client..."
sudo apt-get update -qq && sudo apt-get install -y -qq htop openssh-client > /dev/null 2>&1

echo "[setup] Installing Docker..."
curl -fsSL https://get.docker.com | sudo sh > /dev/null 2>&1
sudo usermod -aG docker $(whoami)

echo "[setup] Installing Docker Compose..."
sudo apt-get install -y -qq docker-compose-plugin > /dev/null 2>&1 || true

echo "[setup] Starting Docker daemon..."
sudo dockerd > /tmp/dockerd.log 2>&1 &

echo "[setup] Waiting for Docker daemon..."
for i in $(seq 1 30); do
  if sudo docker info > /dev/null 2>&1; then
    echo "[setup] Docker is ready."
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "[setup] WARNING: Docker not ready after 30s. Check /tmp/dockerd.log"
    exit 0
  fi
  sleep 1
done

echo "[setup] Building SSH demo server..."
sudo docker build -t inzva-ssh-server ./ssh-server

echo "[setup] Starting SSH demo server on port 2222..."
sudo docker run -d --name ssh-demo -p 2222:22 inzva-ssh-server

echo ""
echo "======================================================"
echo "  Codespace is ready!"
echo "======================================================"
echo ""
