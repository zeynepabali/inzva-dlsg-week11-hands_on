#!/bin/bash
# Start: runs every time the Codespace starts (Docker is ready at this point)
set -e

echo "[start] Waiting for Docker..."
for i in $(seq 1 30); do
  if docker info > /dev/null 2>&1; then
    echo "[start] Docker is ready."
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "[start] WARNING: Docker not available after 30s."
    exit 0
  fi
  sleep 1
done

# Build SSH server if image doesn't exist
if ! docker image inspect inzva-ssh-server > /dev/null 2>&1; then
  echo "[start] Building SSH demo server..."
  docker build -t inzva-ssh-server ./ssh-server
fi
a
# Start SSH container if not already running
if ! docker ps --format '{{.Names}}' | grep -q '^ssh-demo$'; then
  docker rm -f ssh-demo > /dev/null 2>&1 || true
  echo "[start] Starting SSH demo server on port 2222..."
  docker run -d --name ssh-demo -p 2222:22 inzva-ssh-server
fi

echo ""
echo "======================================================"
echo "  Codespace is ready!"
echo "======================================================"
echo ""
